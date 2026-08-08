#!/usr/bin/env python3
"""attest.py — what the spine's text was last APPROVED TO SAY, kept as evidence.

Stack-agnostic, standard-library only. Approval on the spine is recorded today
as a Status *word* in a row (`Verified`, `Modified`), and a word cannot answer
the one question a checkpoint actually asks: **is the text a human approved
still the text that is there?** A word survives an edit; it is set by the same
hand that made the edit; and only an SR carries the post-attestation amendment
state at all, so amended *need* prose has no baseline whatsoever — the loop
reads a stale approval as a current one (SN-029).

So this module stops trusting the word and keeps the evidence: a **content
digest** over the cells that carry obligation, plus an **append-only ledger** of
the decisions taken about those digests (decisions §2.7). Three consequences are
the whole design, and each is a refusal:

  * **A re-wrap is not a meaning change.** Cells are canonicalised (NFC, line
    endings, inline whitespace) before hashing, so reflowing a paragraph costs
    nobody a re-attestation — while one reworded obligation is caught. The rule
    carries its own schema version in the `attest-v1` prefix, so changing the
    rule makes old anchors recognisably old rather than silently wrong.
  * **A chain is a history, not a set.** `append_event` refuses a write whose
    `parent` is not the current head of that artifact's chain, so two writers
    cannot interleave into a record that reads as one sequence. Nothing is ever
    rewritten, and a malformed line is a hard read error naming file and line —
    never a silently skipped record, which is how a ledger loses the one event
    that mattered.
  * **A migration is not a decision.** `seed` writes `baseline`, never
    `ratified`: acceptance is read off the decision WORD, so a ledger of machine
    baselines spelled `ratified` is later counted as that many human approvals.
    It only ever writes a FIRST anchor — a row with any history at all, and a
    need parked under a heading that says it is unratified, are both left alone.
  * **The open set is derived, never stored.** A full-spine review request lives
    as an event and its open-ness is recomputed by replaying request and
    decision events in order (SR-144). That is exactly why it survives a
    relaunch — which is precisely when an unattended loop would otherwise walk
    past the ask.

`requires_human` routes ONE cell; `ratification_projection` is the other half of
SR-142 and SR-144 — what an owner SEES and what therefore blocks. It answers the
sixteen cells the boundary dial is actually choosing between, how many rows of
each tier are waiting, every open request with its reason and its asker, and
whether the full-spine checkpoint is blocked. It is computed here rather than in
`gen_open_items.py` because that generator renders and owns no second opinion
about what is pending. Nothing in it raises: an unvalidatable config, a
hand-edited ledger line or an unparseable registry becomes a *finding*, and the
answer it would have produced is OMITTED rather than guessed — a surface showing
the DEFAULT matrix while the configured one was unreadable would be telling a
human the wrong thing about what they owe.

`detect_candidates` is the reason the digest exists. `check_trajectory.
staged_spine_amendments` can only see an amendment that is *staged in one diff*
against a still-`Verified` row, and it deliberately skips a row whose Status
moved — so the sanctioned amend-and-flip-to-`Modified` is invisible to it, and
so is any change that landed in an earlier commit. Comparing the current digest
to the accepted anchor has neither blind spot: it asks the tree, not the diff.
That module is left exactly as it is; this one is simply strictly better at the
question, and the two are read together.

`enact` is what ANSWERS a candidate, and the three verdicts differ in exactly
one property each (SR-143's enactment half):

  * **`clarity` advances the anchor to the NEW digest.** It writes an accepting
    event at the text standing in the TREE — never at the digest the anchor
    already holds. That is the subtle half: re-accepting the old digest would
    leave every surface reading "accepted" while the anchor silently lagged the
    text, which is the stale approval this whole module exists to end. The
    digest is therefore computed here and cannot be passed in.
  * **`meaning` writes a NON-accepting event** at that same digest, which is the
    whole of the regression: `derive_gate.spine_stage` derives the stage from
    the ledger, so the verdict is the only thing to write for "this tier is back
    in process" to be true on every surface at once. Nothing here computes a
    stage — that is the other component's fact (decisions §3).
  * **`override` appends like anything else.** History is never edited, so a
    human reversing an adjudicator's enactment is one more line and the derived
    state simply re-reads. This is why the boundary needs no second dial: at or
    below `human_ratification_through` the adjudicator RECOMMENDS and writes
    nothing, above it it may enact, and a human may always decide either way.

Event ids are **content-derived** (contracts §2): the first 16 hex of the
SHA-256 of the canonical payload with `id` and `ts` removed. Duplicate detection
and exactly-once semantics are then free, and any reader holding the payload can
verify the ledger instead of trusting it — which `read_events` does on every
read. Nothing here consults the wall clock except the human-readable `ts`, which
is excluded from the digest for that reason: observing the same fact twice is
not two events.

Usage (from the repo root):
    python scripts/attest.py --seed [--root .] [--by NAME]
    python scripts/attest.py --candidates            # exit 1 when any row moved
    python scripts/attest.py --open                  # open full-spine requests
    python scripts/attest.py --request "why" --by NAME
    python scripts/attest.py --decide <request-id> --by NAME [--verdict V]
    python scripts/attest.py --boundary              # the configured tier matrix
    python scripts/attest.py --checkpoint            # exit 1 while it is blocked
    python scripts/attest.py --clarity SR-001 --by NAME     # anchor -> new text
    python scripts/attest.py --meaning SR-001 --by NAME     # stage -> that tier
    python scripts/attest.py --override SR-001 --accept --by NAME
    python scripts/attest.py --meaning SR-001 --actor adjudicator --by ROUTE

The small CSV/markdown loaders below are duplicated from trace.py / derive_gate.py
per the kit's independently-copyable-script convention (the F5 rule).
"""

import argparse
import csv
import datetime
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

SCHEMA = 1

# The canonicalisation + digest RULE version (contracts §4). It is inside the
# hashed bytes, so an anchor written under an older rule cannot be mistaken for
# one written under this rule — old evidence reads as old, never as wrong.
DIGEST_PREFIX = "attest-v1"

# Field/record separators inside the digest input. Unit/record separator, so no
# cell value can forge a boundary the way a comma or a newline could.
_FS, _RS = "\x1f", "\x1e"

DOCS_DIR = "docs"
EVENTS_DIR = "events"
ATTESTATION = "attestation.jsonl"
REVIEW_REQUESTS = "review-requests.jsonl"

# Which ledger each event kind lives in (contracts §2, one file per kind-group).
LEDGERS = {
    "attestation": ATTESTATION,
    "review-request": REVIEW_REQUESTS,
    "review-decision": REVIEW_REQUESTS,
}

# The spine tiers, in order. The INDEX is the human-ratification-boundary axis
# (decisions §1) and the spine-stage axis (decisions §3) at once — one ordering,
# so a caller can never route by one and report by the other.
TIERS = ("SN", "SR", "LLR", "TC")
TIER_INDEX = {name: i for i, name in enumerate(TIERS)}
MAX_BOUNDARY = len(TIERS) - 1

ID_COLUMN = {"SN": "SN-ID", "SR": "SR-ID", "LLR": "LLR-ID", "TC": "TC-ID"}

# The cells whose change alters MEANING (decisions §4). Everything outside these
# lists — evidence pointers, phase labels, areas, the Status word itself — may
# move without invalidating an anchor, which is what keeps a re-attestation
# about obligation rather than bookkeeping.
NORMATIVE_CELLS = {
    # The CORE stakeholder-needs table only. That file carries a SECOND table
    # with a different shape, declared beside this one in `SN_TABLES`.
    "SN": ("Need", "Why", "Priority", "Acceptance"),
    "SR": (
        "Title",
        "SN-Refs",
        "Requirement",
        "AcceptanceCriteria",
        "Permutations",
        "Priority",
        "Verification",
    ),
    "LLR": ("SR-Refs", "Title", "Detail"),
    "TC": ("Verifies", "Level", "Method", "Parameters", "Expected"),
}

# `stakeholder-needs.md` carries TWO tables with different shapes, and the digest
# declares BOTH rather than assuming the first (contracts §4). The cell NAMES are
# inside the hashed bytes, so reading the edge-case table with the core table's
# names records `Lifecycle` under the name `Need` — a record that would mislead
# anyone reading a diff, which is exactly why §4 declares them per table.
SN_TABLES = {
    "core": NORMATIVE_CELLS["SN"],
    "edge": ("Lifecycle", "Scenario", "Expected"),
}

# Two facts about the section a need sits under, carried on the row so the digest
# and `seed` can each ask for the one they need. They are ORTHOGONAL: the shipped
# template's Draft table is the CORE shape, so draft-ness is not a third set of
# cell names. Neither key is a normative cell — a row's table is a property of
# the file's structure, and a heading rename is not an amendment.
SN_TABLE_KEY = "SN-Table"
SN_DRAFT_KEY = "SN-Draft"

# Where each tier's rows live, relative to the docs directory.
SN_MD = ("requirements", "stakeholder-needs.md")
REGISTRIES = {
    "SR": ("requirements", "system-requirements.csv"),
    "LLR": ("requirements", "low-level-requirements.csv"),
    "TC": ("test", "test-cases.csv"),
}

# The one word `seed` writes. It is NOT a verdict: the migration decided
# nothing, it only recorded what the text said when the ledger opened. Kept
# distinct from `ratified` because `is_accepting` reads the decision word and
# nothing else, so a ledger of machine baselines spelled `ratified` reads — to
# every later counter, card and adjudicator — as that many human ratifications.
BASELINE = "baseline"

# The four verdicts an attestation may record (decisions §1 glossary), plus the
# migration's own word above.
VERDICTS = ("ratified", "clarity", "meaning", "override")
DECISIONS = VERDICTS + (BASELINE,)
# The ones that make an event an ACCEPTED anchor. `override` accepts only when
# it says so — a human override is as often a refusal as a blessing. `baseline`
# accepts: it is the text the ledger opened on, and a migration that left every
# row unattested would make the first `--candidates` run pure noise.
ACCEPTING = ("ratified", "clarity", BASELINE)

# What a chain says about one artifact's CURRENT text.
ACCEPTED, PENDING, CHANGED, UNATTESTED = (
    "accepted",
    "pending",
    "changed",
    "unattested",
)

# The scope id a whole-spine review request chains under. Requests are a chain
# like any artifact's, so the same head-parent rule serialises them.
FULL_SPINE = "full-spine"
REVIEW_KIND = "review"

# The boundary a tree with no configuration answers to (contracts §1's
# `human_ratification_through`). Read through `boundary_from_config` so the
# default lives in ONE place once config.py exists.
DEFAULT_BOUNDARY = 1

# The persistent whole-spine review policy a tree with no configuration answers
# to. Beside the boundary for the same reason: a repo that has not adopted
# docs/config.toml must still get an answer rather than a crash.
DEFAULT_FINAL_REVIEW = "never"

# The two dotted config paths this module reads, named once so the projection,
# the CLI and the refusal messages cannot spell them three ways.
BOUNDARY_KEY = "attestation.human_ratification_through"
FINAL_REVIEW_KEY = "attestation.final_full_spine_review"

# Who may enact a ratification at one tier. Declared words rather than a bare
# boolean, because these are printed on the owner's surface: "adjudicator" tells
# a reader what happens next, where `False` only tells them what does not.
HUMAN, ADJUDICATOR = "human", "adjudicator"

TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is (the same
    guard as derive_gate.py / check.py — a non-ASCII cell can't wedge a cp1252
    console)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _refuse(what):
    """The program's one refusal shape (contracts §5): a string naming the
    offending thing, raised so a library caller cannot ignore it and an entry
    point can print it and exit non-zero."""
    return ValueError("attest: REFUSED - {}".format(what))


# --- canonicalisation + the normative digest (LLR-163) ------------------------
_SPACE_RUN_RE = re.compile(r"[ \t]+")


def canonical_cell(value):
    """One cell reduced to its MEANING-BEARING form (contracts §4), in order:
    NFC, CRLF/CR to LF, every run of spaces/tabs to one space, then strip each
    line and the whole.

    The order matters and is the contract's: collapsing before stripping means a
    line of only spaces becomes empty rather than a lone space, so an editor
    that trims trailing whitespace on save never moves a digest."""
    text = unicodedata.normalize("NFC", value or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _SPACE_RUN_RE.sub(" ", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return text.strip()


def row_id(kind, row):
    """The artifact id in `row`, refusing a kind this module has no cell list for
    and a row whose id cell is blank (an id-less row cannot be anchored)."""
    if kind not in NORMATIVE_CELLS:
        raise _refuse(
            "{!r} is not a spine artifact kind (expected one of {})".format(
                kind, ", ".join(TIERS)
            )
        )
    rid = (row.get(ID_COLUMN[kind]) or "").strip()
    if not rid:
        raise _refuse(
            "a {} row carries no {} cell (an artifact with no id cannot be "
            "attested)".format(kind, ID_COLUMN[kind])
        )
    return rid


def cells_for(kind, row=None):
    """The declared normative cells for ONE row — per TABLE, not per kind.

    Only `SN` has more than one shape: `stakeholder-needs.md` carries a core and
    an edge-case table (contracts §4), and `sn_rows` stamps each row with the one
    it came from. A row with no stamp (a hand-built dict, a caller holding a
    registry row) reads as the core table, which is the shape every other reader
    of that file assumes."""
    if kind not in NORMATIVE_CELLS:
        raise _refuse(
            "{!r} is not a spine artifact kind (expected one of {})".format(
                kind, ", ".join(TIERS)
            )
        )
    if kind != "SN":
        return NORMATIVE_CELLS[kind]
    table = (row or {}).get(SN_TABLE_KEY) or "core"
    if table not in SN_TABLES:
        raise _refuse(
            "an SN row names table {!r}, which is not one of the declared "
            "stakeholder-needs tables ({})".format(table, ", ".join(sorted(SN_TABLES)))
        )
    return SN_TABLES[table]


def normative_digest(kind, row):
    """The SHA-256 hex of one artifact's declared normative cells, canonicalised.

    The input is `attest-v1\\n<kind>\\n<id>\\n` followed by
    `<cell><FS><canonical value><RS>` per declared cell in the declared order —
    so the KIND and the ID are inside the hash (two different artifacts with
    identical prose are two anchors) and a cell that is absent digests exactly
    like a cell that is empty, which is what a registry gaining a column must
    not disturb."""
    rid = row_id(kind, row)  # also the kind check — one gate, not two
    blob = "{}\n{}\n{}\n".format(DIGEST_PREFIX, kind, rid)
    for name in cells_for(kind, row):
        blob += name + _FS + canonical_cell(row.get(name)) + _RS
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# --- loading the spine rows (duplicated per the F5 rule) ----------------------
def is_example(rid):
    return (rid or "").endswith("-000")


def load_csv(path):
    if not Path(path).exists():
        return []
    with Path(path).open(newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


# A stakeholder-need table row, matched with the SAME `\|\s*(SN-\d+)\s*\|` shape
# the dashboard and the knowledge export already use (contracts §4) — one parse
# of that file across the kit, so the digest and the views can never disagree
# about which rows exist.
_SN_ROW_RE = re.compile(r"\|\s*(SN-\d+)\s*\|")
# Cells split on an UNESCAPED pipe: a `\|` inside a cell is table syntax, not a
# boundary, and splitting on it would shift every later cell by one.
_SN_CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
# The markdown heading a row sits under. Same shape derive_gate/trace use, so
# "which section is this row in" has one answer across the kit.
_SN_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)")


def sn_table_of(heading):
    """Which declared table a heading opens: `edge` for the edge-case
    expectations, `core` otherwise (contracts §4).

    Matched on the heading TEXT rather than on an exact title, the same
    section-as-state read `derive_gate.sn_draft_ids` makes — so an adopter who
    retitles the section still gets the three-cell shape their table actually
    has, instead of silently recording it under the core table's names."""
    return "edge" if "edge" in (heading or "").lower() else "core"


def sn_is_draft(heading):
    """True for a heading that declares its rows unratified (section-as-state
    §4a). The SAME substring rule `derive_gate.sn_draft_ids` applies, duplicated
    per the F5 rule — the two must not drift, because a draft heading this call
    misses is a need `seed` would anchor as though someone had approved it."""
    return "draft" in (heading or "").lower()


def sn_rows(text):
    """The SN table rows of stakeholder-needs.md, example `-000` rows excluded.

    Each row carries its id, its table's DECLARED cells (contracts §4: core is
    need/why/priority/acceptance, the edge-case table is lifecycle/scenario/
    expected), and the two structural facts `SN-Table` / `SN-Draft`.

    A row with fewer cells than its table declares pads with empty strings rather
    than being dropped — an under-filled need is still a need, and digesting the
    cells it HAS is what lets it be attested at all. A row with MORE cells is
    REFUSED: silently reading the first N would drop the tail out of the hash, so
    an edit past the last declared cell would change meaning and move no digest.

    An `SN-###` mentioned only in prose has no cells and is therefore not a row
    here, while derive_gate's `sn_all_ids` scrapes the whole text. The two
    universes answer different questions (what can be attested vs. what the
    coverage rung must account for) and are deliberately not merged."""
    rows = []
    heading = ""
    for line in text.splitlines():
        found = _SN_HEADING_RE.match(line)
        if found:
            heading = found.group(1)
            continue
        if not _SN_ROW_RE.search(line):
            continue
        cells = [c.strip() for c in _SN_CELL_SPLIT_RE.split(line.strip())]
        # The opening and closing pipes each yield one empty field; they are
        # syntax, not cells. Only ONE trailing field is dropped, so a genuinely
        # empty last cell still counts.
        if cells and not cells[0]:
            cells = cells[1:]
        if cells and not cells[-1]:
            cells = cells[:-1]
        if not cells or not _SN_ROW_RE.search("|{}|".format(cells[0])):
            continue
        if is_example(cells[0]):
            continue
        table = sn_table_of(heading)
        names = SN_TABLES[table]
        values = cells[1:]
        if len(values) > len(names):
            raise _refuse(
                "{} carries {} cells but the {} stakeholder-needs table declares "
                "{} ({}) — the content past the last declared cell would not be "
                "digested, so an edit there would change meaning and move no "
                "digest".format(
                    cells[0], len(values), table, len(names), ", ".join(names)
                )
            )
        values += [""] * (len(names) - len(values))
        row = {
            "SN-ID": cells[0],
            SN_TABLE_KEY: table,
            SN_DRAFT_KEY: sn_is_draft(heading),
        }
        row.update(zip(names, values))
        rows.append(row)
    return rows


def load_artifacts(docs):
    """`{kind: [row, ...]}` for the four tiers under `docs`, example rows excluded.

    Rows are returned as dicts keyed by their registry column names, which is
    exactly what `normative_digest` reads — no intermediate model, so a column
    rename shows up as a digest change rather than as a silent empty cell."""
    docs = Path(docs)
    out = {}
    sn_path = docs.joinpath(*SN_MD)
    text = (
        sn_path.read_text(encoding="utf-8-sig", errors="replace")
        if sn_path.exists()
        else ""
    )
    out["SN"] = sn_rows(text)
    for kind, parts in REGISTRIES.items():
        col = ID_COLUMN[kind]
        out[kind] = [
            r
            for r in load_csv(docs.joinpath(*parts))
            if (r.get(col) or "").strip() and not is_example(r[col])
        ]
    return out


# --- the append-only ledgers (LLR-164) ----------------------------------------
def events_dir(root):
    """`<root>/docs/events` — outside `docs/work/` so `agent_common.spec_files`'
    `rglob("WI-*.md")` cannot see these records (decision D-3)."""
    return Path(root) / DOCS_DIR / EVENTS_DIR


def ledger_path(root, kind):
    if kind not in LEDGERS:
        raise _refuse(
            "{!r} is not an event kind this module owns (expected one of {})".format(
                kind, ", ".join(sorted(LEDGERS))
            )
        )
    return events_dir(root) / LEDGERS[kind]


def _canonical_json(payload):
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def event_id(payload):
    """The first 16 hex of the SHA-256 of the canonical payload with `id` and
    `ts` removed (contracts §2). Deriving the id from the FACTS is what makes a
    second write of the same facts detectable without a dedup token, and what
    lets a reader recompute the id instead of trusting it."""
    body = {k: v for k, v in payload.items() if k not in ("id", "ts")}
    return hashlib.sha256(_canonical_json(body).encode("utf-8")).hexdigest()[:16]


# Required and optional keys per event kind. Strict on purpose: an unknown key
# is refused by name rather than carried, because a typo'd `desicion` that rode
# along would change the id and quietly fork the chain.
_REQUIRED = {
    "attestation": ("artifact_kind", "artifact_id", "digest", "decision", "parent"),
    "review-request": ("artifact_kind", "artifact_id", "reason", "by", "parent"),
    "review-decision": (
        "artifact_kind",
        "artifact_id",
        "request",
        "verdict",
        "by",
        "parent",
    ),
}
_OPTIONAL = {
    "attestation": ("by", "note", "accepted"),
    "review-request": ("note",),
    "review-decision": ("note",),
}
_ENVELOPE = ("schema", "kind", "id", "ts")


def chain_key(event):
    """The chain one event belongs to: `(artifact_kind, artifact_id)`. Review
    events chain under `("review", <scope>)`, so ONE head-parent rule serialises
    every ledger rather than each kind inventing its own ordering."""
    return (event.get("artifact_kind") or "", event.get("artifact_id") or "")


def chain_map(events):
    """`{chain_key: [event, ...]}`, each list oldest-first — the replay index
    every derived answer here is computed from."""
    out = {}
    for e in events:
        out.setdefault(chain_key(e), []).append(e)
    return out


def _validate_event(event, where=None, require_id=False):
    """Refuse an event whose shape, kind, decision or derived id is wrong.

    Run on WRITE and on every READ. Verifying the id on read is what turns the
    ledger from something trusted into something checked: a hand-edited line
    recomputes to a different id and is refused by name, naming file and line.

    `require_id` is the difference between the two callers. On READ the id must
    be THERE — a line carrying none is unverifiable, and an unverifiable line is
    not evidence. On WRITE it must be absent, because `append_event` mints it
    from the facts after this call."""
    at = "{}: ".format(where) if where else ""
    _check_envelope(event, at)
    if event["kind"] == "attestation":
        _check_attestation(event, at)
    _check_derived_id(event, at, require_id)
    return event


def _check_envelope(event, at):
    if not isinstance(event, dict):
        raise _refuse("{}an event must be a JSON object".format(at))
    kind = event.get("kind")
    if kind not in _REQUIRED:
        raise _refuse(
            "{}event kind {!r} is not one of {}".format(
                at, kind, ", ".join(sorted(_REQUIRED))
            )
        )
    if event.get("schema") != SCHEMA:
        raise _refuse(
            "{}event schema {!r} is not the supported schema {}".format(
                at, event.get("schema"), SCHEMA
            )
        )
    _check_keys(event, kind, at)


def _check_keys(event, kind, at):
    """Every declared key present and non-empty, and nothing undeclared.

    Strict in both directions on purpose: a typo'd `desicion` riding along would
    change the derived id and quietly fork the chain, and a blank `by` would
    make an unattributed ask look attributed."""
    allowed = set(_ENVELOPE) | set(_REQUIRED[kind]) | set(_OPTIONAL[kind])
    for key in sorted(set(event) - allowed):
        raise _refuse("{}{} event carries unknown key {!r}".format(at, kind, key))
    for key in _REQUIRED[kind]:
        if key not in event:
            raise _refuse("{}{} event has no {!r} field".format(at, kind, key))
        # `parent` is the one required field that is legitimately None — a first
        # event has no predecessor.
        if key != "parent" and not (isinstance(event[key], str) and event[key].strip()):
            raise _refuse("{}{} event has an empty {!r} field".format(at, kind, key))


def _check_attestation(event, at):
    if event["decision"] not in DECISIONS:
        raise _refuse(
            "{}decision {!r} is not one of {}".format(
                at, event["decision"], ", ".join(DECISIONS)
            )
        )
    if event["decision"] == "override" and not isinstance(event.get("accepted"), bool):
        raise _refuse(
            "{}an override event must say whether it ACCEPTS (a boolean "
            "`accepted`) — a human override is as often a refusal".format(at)
        )
    if event["artifact_kind"] not in TIERS:
        raise _refuse(
            "{}artifact_kind {!r} is not a spine tier ({})".format(
                at, event["artifact_kind"], ", ".join(TIERS)
            )
        )


def _check_derived_id(event, at, require_id=False):
    """Verify the derived id — and, on a read, that there IS one.

    Gating the check on the presence of the field it checks would make dropping
    `id` the one edit that passes every rung: the line would then be trusted as
    an anchor, and the first reader to index it by id would die on a bare
    KeyError instead of refusing by name."""
    if "id" not in event:
        if require_id:
            raise _refuse(
                "{}{} event carries no `id` — the id derives from the facts, so "
                "a line without one cannot be checked against its payload and is "
                "not evidence".format(at, event.get("kind"))
            )
        return
    if event["id"] != event_id(event):
        raise _refuse(
            "{}event id {!r} does not match its payload (derives {!r}) — the "
            "line was edited after it was written".format(
                at, event["id"], event_id(event)
            )
        )


def read_events(path):
    """Every event in one ledger, oldest first, each verified.

    A malformed line is a HARD read error naming the file and the 1-based line
    number (contracts §2) — never a skipped record. A ledger that silently drops
    the line it could not parse is worse than no ledger: the one event that
    mattered is exactly the one an editor is most likely to have corrupted."""
    path = Path(path)
    if not path.exists():
        return []
    events = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue  # a blank line carries no record; it is not a dropped one
        where = "{}:{}".format(path.as_posix(), n)
        try:
            obj = json.loads(s)
        except json.JSONDecodeError as exc:
            raise _refuse("{} is not one JSON object ({})".format(where, exc.msg))
        events.append(_validate_event(obj, where, require_id=True))
    return events


def append_event(root, event, ts=None):
    """Append one event to its ledger and return it, stamped with `id` and `ts`.

    Refuses, by name: a malformed event; a `parent` that is not the current head
    of that artifact's chain; an id already in the ledger. The parent rule is
    what makes the chain a HISTORY rather than a set — two writers that both
    read the same head cannot both land, so an interleaving is refused instead
    of being flattened into a sequence that never happened."""
    event = dict(event)
    if "id" in event:
        # The ledger mints the id from the facts. A caller that brought its own
        # is either replaying a read event into an append-only file or has a
        # bug; silently overwriting it would hide both.
        raise _refuse(
            "an event to append must not carry an `id` (it is derived from the "
            "payload, not supplied) — got {!r}".format(event["id"])
        )
    event.setdefault("schema", SCHEMA)
    _validate_event(event)
    path = ledger_path(root, event["kind"])
    existing = read_events(path)

    key = chain_key(event)
    chain = [e for e in existing if chain_key(e) == key]
    head = chain[-1]["id"] if chain else None
    if event["parent"] != head:
        raise _refuse(
            "{} {} names parent {!r} but the head of that chain is {!r} — the "
            "chain moved under this write".format(key[0], key[1], event["parent"], head)
        )
    if event["kind"] == "review-decision":
        _validate_decision_target(event, existing)

    event["ts"] = ts or datetime.datetime.now(datetime.timezone.utc).strftime(TS_FORMAT)
    event["id"] = event_id(event)
    # The second line of defence, kept because contracts §2 names it: within a
    # CHAINED ledger the parent rule above already refuses a re-write of the
    # same fact (`parent` is part of the digested payload, so the duplicate also
    # names a stale head). This catches the case the chain cannot see — a ledger
    # repaired, replayed or appended to out of band.
    if any(e["id"] == event["id"] for e in existing):
        raise _refuse(
            "event {} is already in {} (the id derives from the facts, so this "
            "is the same fact written twice)".format(event["id"], path.as_posix())
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(_canonical_json(event) + "\n")
    return event


def _validate_decision_target(event, existing):
    """A review decision must name a request that exists and is still open —
    otherwise 'closed' would be a claim nobody can check."""
    requests = {e["id"] for e in existing if e.get("kind") == "review-request"}
    if event["request"] not in requests:
        raise _refuse(
            "review decision names request {!r}, which is not in the ledger".format(
                event["request"]
            )
        )
    if event["request"] not in {r["id"] for r in _open_requests(existing)}:
        raise _refuse("review request {} is already closed".format(event["request"]))


# --- event builders -----------------------------------------------------------
def attestation_event(kind, rid, digest, decision, parent=None, by=None, **extra):
    """One well-formed attestation event. Built here rather than at each call
    site so the field names exist in exactly one place."""
    event = {
        "schema": SCHEMA,
        "kind": "attestation",
        "artifact_kind": kind,
        "artifact_id": rid,
        "digest": digest,
        "decision": decision,
        "parent": parent,
    }
    if by:
        event["by"] = by
    event.update(extra)
    return event


def review_request_event(reason, by, parent=None, scope=FULL_SPINE, **extra):
    event = {
        "schema": SCHEMA,
        "kind": "review-request",
        "artifact_kind": REVIEW_KIND,
        "artifact_id": scope,
        "reason": reason,
        "by": by,
        "parent": parent,
    }
    event.update(extra)
    return event


def review_decision_event(request, verdict, by, parent=None, scope=FULL_SPINE, **extra):
    event = {
        "schema": SCHEMA,
        "kind": "review-decision",
        "artifact_kind": REVIEW_KIND,
        "artifact_id": scope,
        "request": request,
        "verdict": verdict,
        "by": by,
        "parent": parent,
    }
    event.update(extra)
    return event


# --- the derived answers ------------------------------------------------------
def is_accepting(event):
    """True when this event ACCEPTS the digest it names: `ratified`, `clarity`,
    or an `override` that says it accepts. A `meaning` verdict never does — it
    writes a pending record and leaves the previous anchor standing."""
    decision = event.get("decision")
    if decision in ACCEPTING:
        return True
    return decision == "override" and bool(event.get("accepted"))


def anchor_in(chain):
    """The newest accepting event in one chain, or None — 'what the current
    attested text IS', which a later pending event does not erase."""
    for event in reversed(chain):
        if is_accepting(event):
            return event
    return None


def accepted_anchor(root, kind, rid):
    """The accepted anchor for one artifact, read from the ledger under `root`."""
    events = read_events(ledger_path(root, "attestation"))
    return anchor_in(chain_map(events).get((kind, rid), []))


def chain_state(chain, digest):
    """What one chain says about the CURRENT text: accepted / pending / changed /
    unattested.

    The head decides, not the anchor. An anchor at an older digest is history;
    what a checkpoint needs to know is whether the text standing here now has
    been accepted — so a chain whose head names a different digest reads
    `changed`, and one whose head names this digest but does not accept it
    (a `meaning` verdict, or an override that refused) reads `pending`."""
    if not chain:
        return UNATTESTED
    head = chain[-1]
    if head.get("digest") != digest:
        return CHANGED
    return ACCEPTED if is_accepting(head) else PENDING


def detect_candidates(root, docs=None):
    """Every artifact whose current normative text is not accepted, tier order.

    This is the check `check_trajectory.staged_spine_amendments` structurally
    cannot make. That one reads ONE diff and skips a row whose Status moved, so
    the two amendments that matter most are invisible to it: a row edited while
    it stays `Verified` in an earlier commit, and the sanctioned
    amend-and-flip-to-`Modified`. Digest-versus-anchor has neither blind spot —
    Status is not a normative cell, and the comparison is against the tree
    rather than against a diff. Nothing there is modified; this is simply the
    better instrument, and both are read."""
    docs = Path(docs) if docs else Path(root) / DOCS_DIR
    chains = chain_map(read_events(ledger_path(root, "attestation")))
    artifacts = load_artifacts(docs)
    out = []
    for kind in TIERS:
        for row in artifacts.get(kind, []):
            rid = row_id(kind, row)
            digest = normative_digest(kind, row)
            chain = chains.get((kind, rid), [])
            state = chain_state(chain, digest)
            if state == ACCEPTED:
                continue
            anchor = anchor_in(chain)
            out.append(
                {
                    "kind": kind,
                    "id": rid,
                    "digest": digest,
                    "state": state,
                    "anchor": anchor["digest"] if anchor else None,
                    "reason": _candidate_reason(rid, state, chain, digest, anchor),
                }
            )
    return out


def _candidate_reason(rid, state, chain, digest, anchor):
    if state == UNATTESTED:
        return "{} has no attestation event".format(rid)
    if state == CHANGED:
        return "{} normative text changed since {} (anchor {}, now {})".format(
            rid,
            "its accepted anchor" if anchor else "its last event",
            (anchor or chain[-1])["digest"][:12],
            digest[:12],
        )
    return "{} has a pending {} event at the current text".format(
        rid, chain[-1].get("decision")
    )


def _open_requests(events):
    """The open review requests in one already-read ledger, oldest first."""
    open_set = {}
    for event in events:
        if event.get("kind") == "review-request":
            open_set[event["id"]] = event
        elif event.get("kind") == "review-decision":
            open_set.pop(event["request"], None)
    return list(open_set.values())


def review_requests(root):
    """The OPEN full-spine review requests, derived by replaying the ledger.

    Open-ness is never stored, only replayed (SR-144). That is the whole point:
    a one-shot ask held in memory or in a launcher flag disappears at the next
    relaunch — which is exactly the moment an unattended loop would proceed past
    the checkpoint it was told to stop at. Replay costs one file read and
    survives any crash."""
    return _open_requests(read_events(ledger_path(root, "review-request")))


def full_spine_block(root, policy="never"):
    """Why the full-spine checkpoint is blocked, or None.

    Two independent sources, deliberately: the PERSISTENT policy
    (`final_full_spine_review = "always"`) and any open one-shot request. A team
    that wants a review more often than its policy says asks with an event
    rather than editing configuration, so a temporary ask never becomes a
    permanent dial nobody remembers turning back."""
    reasons = []
    if policy == "always":
        reasons.append("final_full_spine_review=always")
    for request in review_requests(root):
        reasons.append(
            "open review request {} ({})".format(request["id"], request["reason"])
        )
    return "; ".join(reasons) if reasons else None


# --- the human-ratification boundary (LLR-162) --------------------------------
def attestation_config(root):
    """`(boundary, final_full_spine_review, [refusal, ...])` — the two attestation
    dials as configured, plus every reason a reader should not trust them.

    Lazily imported (contracts §6) so this module never fails to import because
    a sibling slice has not landed — and so a downstream repo that has not
    adopted the config file still gets the declared defaults rather than a
    crash.

    The refusal list is deliberately SCOPED to the findings that make *these two
    dials* untrustworthy: the dials themselves, the document-level ones (an
    absent `schema`, unreadable bytes, malformed TOML) under which every resolved
    value is a default standing in for text nobody could read, and every finding
    the loader could NOT attribute to a declared section. A finding on some
    unrelated dial is `config_query`'s report to make; repeating the whole config
    report on the ratification card would bury the one line that changes what a
    human owes. But an UNRECOGNISED key is not an unrelated dial — `[attestaton]`
    and `final_full_spine_reveiw` are the likeliest way these two dials go
    unread, and a dial nobody could read must never answer "checkpoint clear".

    Refusals are strings, not the loader's `Finding` tuples: this value crosses
    into a renderer, and a renderer that had to know the loader's record shape
    would be the second opinion this projection exists to avoid."""
    try:
        import config  # deferred by contract (contracts §6), see the docstring
    except ImportError:
        return DEFAULT_BOUNDARY, DEFAULT_FINAL_REVIEW, []
    try:
        cfg, findings = config.load_config(root)
        boundary = int(cfg.attestation.human_ratification_through)
        policy = str(cfg.attestation.final_full_spine_review)
    except (AttributeError, KeyError, TypeError, ValueError):
        # The sibling slice's accessor shape is not this module's to assert. An
        # unreadable dial falls back to the declared default rather than
        # crashing a caller that only wanted to route one tier.
        return DEFAULT_BOUNDARY, DEFAULT_FINAL_REVIEW, []
    scoped = ("schema", config.CONFIG_REL, BOUNDARY_KEY, FINAL_REVIEW_KEY)
    refusals = [
        "{} ({})".format(f.key, f.reason)
        for f in findings
        if f.key in scoped or not _elsewhere(config, f.key)
    ]
    return boundary, policy, refusals


# The array-valued tables. They are not `config.SECTIONS` entries (they have no
# scalar defaults), but a finding on one is still attributable to a declared
# place that is not this section.
_DECLARED_TABLES = ("routes", "jobs", "prompts")


def _elsewhere(config, key):
    """True when a finding's key belongs to a declared config section that is
    NOT `[attestation]` — the only findings the ratification card may drop.

    Membership is tested the other way round from the obvious spelling, and that
    is the whole point: a filter that listed the correctly-spelled dials could by
    construction never match a MISSPELLING of one, so `[attestaton]` and
    `final_full_spine_reveiw` — the two findings that most make these dials
    untrustworthy — were the two it could not see."""
    head = key.split(".", 1)[0].split("[", 1)[0]
    if head == BOUNDARY_KEY.split(".", 1)[0]:
        return False  # anything under our own section is ours to report
    # `getattr`, not attribute access: a sibling slice that has not landed its
    # section table yet must make this card MORE careful, never crash it.
    sections = getattr(config, "SECTIONS", ())
    return head in sections or head in _DECLARED_TABLES


def boundary_from_config(root):
    """`[attestation] human_ratification_through` from `docs/config.toml`, or the
    kit default when the loader is not present yet.

    One line over `attestation_config` rather than a second reader: two paths to
    one dial is two places for the fallback to drift, and the fallback is the
    whole reason a caller can ask at all."""
    return attestation_config(root)[0]


def requires_human(tier_index, boundary):
    """True when a ratification at `tier_index` owes a HUMAN decision.

    The boundary is cumulative and inclusive (decisions §1): 0 = SN only,
    1 = SN+SR, 2 = SN+SR+LLR, 3 = the whole spine. One ordinal comparison
    replaces the retired enum's five call sites — and, unlike an enum naming
    *who* ratifies, it says *which tiers*, which is the question a repo
    automating test-case ratification while signing off needs actually has.

    Both arguments are validated: an out-of-range boundary is refused by name
    rather than clamped, because clamping would silently route a tier to the
    adjudicator that the adopter meant to reserve for a human."""
    _check_ordinal(boundary, "human ratification boundary")
    _check_ordinal(tier_index, "spine tier index")
    return tier_index <= boundary


def _check_ordinal(value, what):
    """Refuse anything that is not an integer in 0..3. `bool` is excluded
    explicitly — it is an `int` subclass, so `True` would otherwise pass as the
    SR tier and route a whole tier by accident."""
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 0 <= value <= MAX_BOUNDARY
    ):
        raise _refuse(
            "{} {!r} is outside 0..{} (the four spine tiers are {})".format(
                what, value, MAX_BOUNDARY, ", ".join(TIERS)
            )
        )


# --- the projection: what an owner sees, and what blocks (SR-142 / SR-144) ----
def tier_routing(boundary):
    """The whole ratification matrix for one boundary: one entry per spine tier,
    in spine order, each naming who may decide.

    `requires_human` answers one cell; an adopter setting the dial is choosing
    between the four ROWS of this table, and the owner surface and the CLI both
    print it. Built on that predicate rather than beside it, so the matrix a
    human reads and the routing a caller obeys cannot disagree — including the
    refusal: an out-of-range boundary raises here too, so a projection can never
    show a table the router would not honour."""
    matrix = []
    for index, tier in enumerate(TIERS):
        human = requires_human(index, boundary)
        matrix.append(
            {
                "tier": tier,
                "index": index,
                "requires_human": human,
                "decider": HUMAN if human else ADJUDICATOR,
            }
        )
    return matrix


def _pending_by_tier(root, docs, findings):
    """`{tier: count}` of rows whose current text is not accepted — or `{}` plus a
    finding when the ledger or the registries refuse to be read.

    Counting is what turns "SR ratifications are the human's" from a rule into a
    queue length. `findings` is appended to rather than raised through, so one
    unreadable input costs the owner that one line and not the whole card."""
    try:
        candidates = detect_candidates(root, docs)
    except (ValueError, OSError) as exc:
        findings.append(str(exc))
        return {}
    counts = {tier: 0 for tier in TIERS}
    for candidate in candidates:
        counts[candidate["kind"]] += 1
    return counts


def ratification_projection(root, docs=None):
    """What an owner must SEE about ratification: `{boundary, policy, tiers,
    requests, block, findings}` (module docstring for why it lives here).

    `boundary` is None exactly when the configured value could not be trusted,
    and `tiers` is then empty: a refused dial must render NO matrix, because the
    default it fell back to is not what the adopter wrote and a printed matrix is
    read as the configured one. `findings` is the refusal list — a caller treats
    a non-empty one as blocking, since "we could not tell" and "nothing is
    pending" must never print the same word."""
    boundary, policy, findings = attestation_config(root)
    tiers = []
    if findings:
        boundary = None
    else:
        try:
            tiers = tier_routing(boundary)
        except ValueError as exc:
            findings.append(str(exc))
            boundary = None
    pending = _pending_by_tier(root, docs, findings)
    for entry in tiers:
        entry["pending"] = pending.get(entry["tier"])
    requests, block = [], None
    try:
        requests = review_requests(root)
        # `full_spine_block` re-reads the (tiny) ledger rather than being
        # reassembled from `requests` here: the sentence a blocked checkpoint
        # prints has ONE home, and two homes for it is how a gate and its
        # explanation drift into disagreeing.
        block = full_spine_block(root, policy)
    except (ValueError, OSError) as exc:
        findings.append(str(exc))
    return {
        "boundary": boundary,
        "policy": policy,
        "tiers": tiers,
        "requests": requests,
        "block": block,
        "findings": findings,
    }


# --- enacting a verdict on one artifact (SR-143's enactment half) -------------
# Detection and enactment are two calls on purpose: `detect_candidates` reads and
# decides nothing, so a card, a hook or an adjudicator can list what is OWED with
# no way to accidentally record an answer while listing it.

# What an actor may DO about a verdict at one tier. Two words rather than a
# boolean for the reason `tier_routing` gives two: "recommend" tells a reader
# what happens next, where `False` only tells them what does not. The same two
# words `intake.adjudication_action` already answers with, so the two mechanical
# tools an adjudication row drives speak one vocabulary.
RECOMMEND, ENACT = "recommend", "enact"

# The verdicts THIS arm writes. `ratified` is a FIRST acceptance and belongs to
# the ratification sitting; `baseline` is the migration's word and decides
# nothing. Enacting either here would let a mechanical tool spell an approval
# nobody gave — the exact confusion `BASELINE` exists to prevent.
ENACTABLE = ("clarity", "meaning", "override")


def kind_of(rid):
    """The spine tier an artifact id belongs to, read off its declared prefix.

    Refuses an unknown prefix rather than guessing a tier: a verdict filed under
    the wrong kind digests a different cell list AND chains under a different
    key, so it would record an approval of something else entirely."""
    token = (rid or "").strip().split("-", 1)[0].upper()
    if token not in TIER_INDEX:
        raise _refuse(
            "{!r} carries no spine tier prefix (expected one of {})".format(
                rid, ", ".join(t + "-" for t in TIERS)
            )
        )
    return token


def find_row(docs, rid):
    """`(kind, row)` for the CURRENT text of one artifact, refusing an id that no
    registry carries.

    The row is read from the tree on every call and is never passed in: a caller
    that could supply the row could supply an OLD one, and a verdict recorded
    against text that is no longer there is precisely the stale approval this
    module exists to end."""
    kind = kind_of(rid)
    for row in load_artifacts(docs).get(kind, []):
        if row_id(kind, row) == rid:
            return kind, row
    raise _refuse(
        "{} is in no current {} registry under {} (a verdict cannot be recorded "
        "about text that is not there)".format(rid, kind, Path(docs).as_posix())
    )


def verdict_action(kind, boundary, actor=HUMAN):
    """`enact` or `recommend` — what `actor` may do about a verdict at `kind`'s
    tier, under the cumulative boundary (decisions §1).

    At or below the boundary an adjudicator prepares the brief and stops; above
    it, it may write. A HUMAN always enacts: the dial says which tiers REQUIRE a
    human, never which tiers forbid one, and that asymmetry is what keeps a later
    human override available at every tier without inventing a second dial."""
    if actor not in (HUMAN, ADJUDICATOR):
        raise _refuse(
            "{!r} is not an actor this module knows ({} or {})".format(
                actor, HUMAN, ADJUDICATOR
            )
        )
    if kind not in TIER_INDEX:
        raise _refuse("{!r} is not a spine tier ({})".format(kind, ", ".join(TIERS)))
    if actor == HUMAN:
        return ENACT
    return RECOMMEND if requires_human(TIER_INDEX[kind], boundary) else ENACT


def _enact_refusal(rid, verdict, accepted, chain, digest):
    """Everything wrong with one enactment, decided BEFORE the ledger is opened
    and returned as a string naming it (contracts §5).

    The two `clarity` rungs are the ones worth reading twice. That verdict claims
    the digest moved and the obligation did not, so a row with no history has no
    anchor for it to advance, and a row already accepted at this very text has
    nothing to decide. Writing either would put a decision-SHAPED record in an
    append-only ledger that decided nothing — and every later counter, card and
    adjudicator reads decision words, not intentions."""
    if verdict not in ENACTABLE:
        return "{!r} is not a verdict this arm enacts ({})".format(
            verdict, " | ".join(ENACTABLE)
        )
    if verdict == "override" and not isinstance(accepted, bool):
        return (
            "an override of {} must say whether it ACCEPTS (--accept / --reject)"
            " — a human override is as often a refusal".format(rid)
        )
    if verdict != "clarity":
        return None
    if not chain:
        return (
            "{} has no attestation event, so a clarity verdict has no anchor to "
            "advance (seed or ratify it first)".format(rid)
        )
    if chain_state(chain, digest) == ACCEPTED:
        return (
            "{} is already accepted at its current text ({}) — a clarity verdict "
            "here would record a decision that decided nothing".format(rid, digest[:12])
        )
    return None


def enact(root, docs, rid, verdict, by, actor=HUMAN, accepted=None, note=None, ts=None):
    """Record ONE verdict about an artifact's current text.
    `(action, event_or_None, digest)` — `action` is `enact` (the event was
    appended) or `recommend` (nothing was written).

    What each verdict does, and why, is the module docstring's; this is the one
    place all three are written, so they cannot drift apart at three call sites.
    The digest is computed from the tree here and is deliberately not a
    parameter."""
    if not (by or "").strip():
        raise _refuse(
            "a verdict on {} must name who recorded it (an unattributed decision "
            "is not one)".format(rid)
        )
    kind, row = find_row(docs, rid)
    digest = normative_digest(kind, row)
    chain = chain_map(read_events(ledger_path(root, "attestation"))).get(
        (kind, rid), []
    )
    refusal = _enact_refusal(rid, verdict, accepted, chain, digest)
    # Malformedness is judged BEFORE the boundary, so an adjudicator's
    # recommendation can never be the thing that hides a bad verdict from its
    # author: "we would have refused this" is what they need to hear, not
    # "a human will decide".
    if refusal:
        raise _refuse(refusal)
    boundary, _policy, dial_refusals = attestation_config(root)
    action = verdict_action(kind, boundary, actor)
    if action == RECOMMEND:
        return action, None, digest
    # `attestation_config` falls back to the DECLARED DEFAULT when the dial
    # could not be read, which is right for a reader and wrong for a writer: a
    # machine would then enact under a boundary the adopter never wrote. A human
    # is unaffected — they enact at every tier by definition, so no dial was
    # consulted on their behalf.
    if dial_refusals and actor != HUMAN:
        raise _refuse(
            "{} may not enact a verdict on {} while the ratification boundary "
            "cannot be read ({}) — an unreadable dial must never authorise a "
            "machine".format(actor, rid, "; ".join(dial_refusals))
        )
    extra = {"note": note} if note else {}
    if verdict == "override":
        extra["accepted"] = bool(accepted)
    event = append_event(
        root,
        attestation_event(
            kind, rid, digest, verdict, chain[-1]["id"] if chain else None, by, **extra
        ),
        ts=ts,
    )
    return action, event, digest


# --- CLI ----------------------------------------------------------------------
def seed(root, docs=None, by="seed", ts=None):
    """Write a `baseline` anchor for every current spine row that has NO history.

    The one-time migration: without it every row reads as changed on the first
    run, which would make the first `--candidates` report pure noise and teach
    its reader to ignore it. It is a MIGRATION, not a decision, so it writes
    `baseline` rather than `ratified` — a machine cannot ratify, and a ledger of
    machine baselines spelled `ratified` is later counted as that many human
    approvals.

    Two rows it must never touch, and both are refusals of the same shape — the
    migration may only ever ADD a first anchor, never answer a question:

      * a row with ANY history. The guard asks "does this chain exist?", not "is
        the current text accepted?": a row whose text moved reads `changed` and a
        row a human marked `meaning` reads `pending`, and an `== ACCEPTED` test
        lets BOTH through — re-ratifying an amendment and writing straight over
        the one verdict this module documents as never accepting.
      * a need parked under a heading that says it is unratified. Anchoring a
        Draft need would make the declared ratification act — moving the row up
        into the core table in a reviewed commit — produce no candidate and no
        event, because the row would already be accepted at that very text."""
    docs = Path(docs) if docs else Path(root) / DOCS_DIR
    ts = ts or datetime.datetime.now(datetime.timezone.utc).strftime(TS_FORMAT)
    chains = chain_map(read_events(ledger_path(root, "attestation")))
    written = {kind: 0 for kind in TIERS}
    artifacts = load_artifacts(docs)
    for kind in TIERS:
        for row in artifacts.get(kind, []):
            rid = row_id(kind, row)
            if chains.get((kind, rid)):
                continue
            if row.get(SN_DRAFT_KEY):
                continue
            event = append_event(
                root,
                attestation_event(
                    kind, rid, normative_digest(kind, row), BASELINE, None, by
                ),
                ts=ts,
            )
            chains.setdefault((kind, rid), []).append(event)
            written[kind] += 1
    return written


def _print_candidates(root, docs):
    candidates = detect_candidates(root, docs)
    for candidate in candidates:  # every finding, never just the first
        print("attest: CANDIDATE - {}".format(candidate["reason"]))
    if not candidates:
        print("attest: OK - every spine row matches its accepted anchor.")
        return 0
    # The VERDICTS, not DECISIONS: `baseline` is the migration's word and is not
    # something a human may answer a candidate with.
    print(
        "attest: {} row(s) need a decision ({}).".format(
            len(candidates), " | ".join(VERDICTS)
        )
    )
    return 1


# The generated artifacts that read these ledgers, per ledger, with the command
# that rewrites each. `pre-commit` runs both as unconditional `--check` steps, so
# any append here leaves the tree UNCOMMITTABLE until they are regenerated. The
# tool that broke the tree is the one that must say so: a refusal at commit time
# naming a generator the author never ran reads as a mystery, and the documented
# way to ASK for a review must not be the thing that silently reds the bar.
_GEN = "python project-trajectory/scripts/{} --root ."
STALES = {
    ATTESTATION: (
        ("docs/gate", _GEN.format("derive_gate.py")),
        ("docs/open-items.html", _GEN.format("gen_open_items.py")),
    ),
    REVIEW_REQUESTS: (("docs/open-items.html", _GEN.format("gen_open_items.py")),),
}


def _note_staled(ledger):
    """Name, on stdout, every generated artifact this ledger write just staled."""
    for artifact, command in STALES.get(ledger, ()):
        print(
            "attest: NOTE - this write staled {} (a pre-commit step checks it); "
            "regenerate with `{}`.".format(artifact, command)
        )


def _arm_seed(root, docs, by):
    written = seed(root, docs, by=by or "seed")
    print(
        "attest: seeded {} anchor(s) ({}).".format(
            sum(written.values()),
            " ".join("{}={}".format(k, written[k]) for k in TIERS),
        )
    )
    if sum(written.values()):
        _note_staled(ATTESTATION)


def _review_head(root):
    """The head of the review chain — every review event chains under one scope,
    so the last line of that ledger IS the parent a new event must name."""
    events = read_events(ledger_path(root, "review-request"))
    return events[-1]["id"] if events else None


def _arm_request(root, reason, by):
    if not by:
        raise _refuse("--request needs --by (an unattributed ask is not one)")
    event = append_event(root, review_request_event(reason, by, _review_head(root)))
    print("attest: recorded review request {}.".format(event["id"]))
    _note_staled(REVIEW_REQUESTS)


def _arm_decide(root, request_id, verdict, by):
    if not by:
        raise _refuse("--decide needs --by (only a human decision closes a request)")
    append_event(
        root, review_decision_event(request_id, verdict, by, _review_head(root))
    )
    print("attest: closed review request {}.".format(request_id))
    _note_staled(REVIEW_REQUESTS)


def _arm_boundary(root, docs):
    """Print the configured boundary and the matrix it implies.

    Exits non-zero when a dial was refused and prints no table: a matrix that is
    not the configured one is worse than no matrix, because a reader acts on
    it."""
    projection = ratification_projection(root, docs)
    for refusal in projection["findings"]:  # every finding, never just the first
        print("attest: REFUSED - {}".format(refusal), file=sys.stderr)
    if projection["boundary"] is None:
        return 1
    print(
        "attest: boundary {} ({}) - at or below it a human decides.".format(
            projection["boundary"], BOUNDARY_KEY
        )
    )
    for entry in projection["tiers"]:
        pending = entry["pending"]
        print(
            "attest: {} ({}) -> {} - {} row(s) awaiting a decision".format(
                entry["tier"],
                entry["index"],
                entry["decider"],
                "?" if pending is None else pending,
            )
        )
    print("attest: {}={}".format(FINAL_REVIEW_KEY, projection["policy"]))
    return 0


def _arm_checkpoint(root, docs):
    """The full-spine checkpoint as a GATE: exit 1 while it is blocked.

    Fail-closed by construction — an input that could not be read blocks too,
    which is the difference between a checkpoint and a decoration."""
    projection = ratification_projection(root, docs)
    for refusal in projection["findings"]:
        print("attest: REFUSED - {}".format(refusal), file=sys.stderr)
    if projection["block"]:
        # The reason already names every open request and the persistent policy
        # (`full_spine_block`), so nothing is re-listed here.
        print("attest: CHECKPOINT BLOCKED - {}".format(projection["block"]))
        return 1
    if projection["findings"]:
        return 1
    print(
        "attest: checkpoint clear - no open review request, {}={}.".format(
            FINAL_REVIEW_KEY, projection["policy"]
        )
    )
    return 0


def _accepted_flag(accept, reject):
    """The override's accept/reject pair as one tri-state (None = neither given).

    Both at once is a REFUSAL rather than a precedence rule: a caller who typed
    both does not know which they meant, and neither does this module."""
    if accept and reject:
        raise _refuse(
            "--accept and --reject were both given (an override says one or the "
            "other, never both)"
        )
    if accept:
        return True
    if reject:
        return False
    return None


def _enacted_line(verdict, rid, kind, digest, event):
    """The one sentence each enacted verdict prints — its DISTINGUISHING
    property, since that is what a reader has to check was the intended one."""
    if verdict == "clarity":
        return (
            "attest: clarity recorded for {} - the accepted anchor advances to "
            "{}.".format(rid, digest[:12])
        )
    if verdict == "meaning":
        return (
            "attest: meaning recorded for {} - the derived spine stage pulls "
            "back to {} ({}).".format(rid, TIER_INDEX[kind], kind)
        )
    return (
        "attest: override recorded for {} - it {} the current text; history is "
        "unchanged, the ledger only grew.".format(
            rid, "ACCEPTS" if event.get("accepted") else "REFUSES"
        )
    )


def _arm_verdict(root, docs, rid, verdict, args):
    """One `--clarity` / `--meaning` / `--override` arm.

    A recommendation exits 0, not non-zero: the adjudicator was asked and
    answered correctly for its authority, and nothing was claimed — the row is
    still a candidate, so the owed act remains visible on every surface. That is
    `intake.adjudication_action`'s ruled shape (owner decision 2), kept here so
    the two tools cannot disagree about what "recommend" costs."""
    accepted = _accepted_flag(args.accept, args.reject)
    action, event, digest = enact(
        root,
        docs,
        rid,
        verdict,
        args.by,
        actor=args.actor,
        accepted=accepted,
        note=args.note,
    )
    kind = kind_of(rid)
    if action == RECOMMEND:
        print(
            "attest: RECOMMEND - {} {} at {}; {} is at or below the boundary, so "
            "enacting it is a human's act ({}). Nothing was written.".format(
                rid, verdict, digest[:12], kind, BOUNDARY_KEY
            )
        )
        return 0
    print(_enacted_line(verdict, rid, kind, digest, event))
    _note_staled(ATTESTATION)
    return 0


def _arm_verdicts(root, docs, args):
    """Every verdict arm one run carries, in declared order. Extracted from
    `main` rather than inlined as three more `if`s, so the entry point stays one
    line per arm."""
    code = 0
    for verdict in ENACTABLE:
        # The option's dest IS the verdict word, so the vocabulary is declared
        # once: a fourth enactable verdict is one `add_argument` and nothing
        # here, and a verdict with no option would fail loudly rather than be
        # silently unreachable.
        rid = getattr(args, verdict)
        if rid:
            code = max(code, _arm_verdict(root, docs, rid, verdict, args))
    return code


def _arm_open(root):
    requests = review_requests(root)
    for request in requests:
        print(
            "attest: OPEN - {} {} ({})".format(
                request["id"], request["reason"], request["by"]
            )
        )
    if not requests:
        print("attest: OK - no open review requests.")


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--docs", default=None, help="docs directory (default: <root>/docs)"
    )
    ap.add_argument(
        "--seed",
        action="store_true",
        help="write a baseline anchor for every current spine row that has no "
        "history at all (the one-time migration; it decides nothing)",
    )
    ap.add_argument(
        "--candidates",
        action="store_true",
        help="report every row whose normative text is not accepted; exit 1 if any",
    )
    ap.add_argument(
        "--open", dest="open_", action="store_true", help="list open review requests"
    )
    ap.add_argument(
        "--request", default=None, help="record a full-spine review request"
    )
    ap.add_argument("--decide", default=None, help="close the named review request")
    ap.add_argument("--verdict", default="reviewed", help="verdict for --decide")
    ap.add_argument(
        "--boundary",
        action="store_true",
        help="print the configured human-ratification boundary and the tier "
        "routing it implies; exit 1 when a dial was refused",
    )
    ap.add_argument(
        "--checkpoint",
        action="store_true",
        help="exit 1 while the full-spine checkpoint is blocked (an open review "
        "request, the persistent policy, or an input that could not be read)",
    )
    for verdict in ENACTABLE:
        ap.add_argument(
            "--" + verdict,
            default=None,
            metavar="ID",
            help="record a {} verdict about that row's CURRENT text".format(verdict),
        )
    ap.add_argument(
        "--accept",
        action="store_true",
        help="an --override that ACCEPTS the current text",
    )
    ap.add_argument(
        "--reject",
        action="store_true",
        help="an --override that REFUSES the current text",
    )
    ap.add_argument(
        "--actor",
        choices=(HUMAN, ADJUDICATOR),
        default=HUMAN,
        help="who is enacting: an adjudicator only RECOMMENDS at or below "
        "{} (default: {})".format(BOUNDARY_KEY, HUMAN),
    )
    ap.add_argument("--note", default=None, help="free-text note carried on the event")
    ap.add_argument(
        "--by", default=None, help="who is recording this (required to ask)"
    )
    args = ap.parse_args(argv)
    root = Path(args.root)
    docs = Path(args.docs) if args.docs else root / DOCS_DIR

    # Arms compose in one run, so the exit code is the WORST of them: a blocked
    # checkpoint beside a successful --seed must not report success.
    code = 0
    try:
        if args.seed:
            _arm_seed(root, docs, args.by)
        if args.request:
            _arm_request(root, args.request, args.by)
        if args.decide:
            _arm_decide(root, args.decide, args.verdict, args.by)
        # Before the reporting arms: a run that enacts and then reports must
        # report the state its own write produced, not the one it walked in on.
        code = max(code, _arm_verdicts(root, docs, args))
        if args.open_:
            _arm_open(root)
        if args.boundary:
            code = max(code, _arm_boundary(root, docs))
        if args.checkpoint:
            code = max(code, _arm_checkpoint(root, docs))
        if args.candidates:
            return max(code, _print_candidates(root, docs))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return code


if __name__ == "__main__":
    sys.exit(main())
