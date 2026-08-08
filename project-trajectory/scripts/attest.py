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
  * **The open set is derived, never stored.** A full-spine review request lives
    as an event and its open-ness is recomputed by replaying request and
    decision events in order (SR-144). That is exactly why it survives a
    relaunch — which is precisely when an unattended loop would otherwise walk
    past the ask.

`detect_candidates` is the reason the digest exists. `check_trajectory.
staged_spine_amendments` can only see an amendment that is *staged in one diff*
against a still-`Verified` row, and it deliberately skips a row whose Status
moved — so the sanctioned amend-and-flip-to-`Modified` is invisible to it, and
so is any change that landed in an earlier commit. Comparing the current digest
to the accepted anchor has neither blind spot: it asks the tree, not the diff.
That module is left exactly as it is; this one is simply strictly better at the
question, and the two are read together.

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

# Where each tier's rows live, relative to the docs directory.
SN_MD = ("requirements", "stakeholder-needs.md")
REGISTRIES = {
    "SR": ("requirements", "system-requirements.csv"),
    "LLR": ("requirements", "low-level-requirements.csv"),
    "TC": ("test", "test-cases.csv"),
}

# The four verdicts an attestation may record (decisions §1 glossary).
DECISIONS = ("ratified", "clarity", "meaning", "override")
# The three that make an event an ACCEPTED anchor. `override` accepts only when
# it says so — a human override is as often a refusal as a blessing.
ACCEPTING = ("ratified", "clarity")

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
    for name in NORMATIVE_CELLS[kind]:
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


def sn_rows(text):
    """The SN table rows of stakeholder-needs.md as `{SN-ID, Need, Why, Priority,
    Acceptance}` dicts, example `-000` rows excluded.

    Cells 1..4 after the id are the four normative cells (contracts §4). A row
    with fewer cells — the file's second, edge-case table is 3 wide — pads with
    empty strings rather than being dropped: an edge-case need is still a need,
    and digesting the cells it HAS is what lets it be attested at all.

    An `SN-###` mentioned only in prose has no cells and is therefore not a row
    here, while derive_gate's `sn_all_ids` scrapes the whole text. The two
    universes answer different questions (what can be attested vs. what the
    coverage rung must account for) and are deliberately not merged."""
    rows = []
    for line in text.splitlines():
        if not _SN_ROW_RE.search(line):
            continue
        cells = [c.strip() for c in _SN_CELL_SPLIT_RE.split(line.strip())]
        # A leading pipe yields an empty first field; drop it so cells[0] is the id.
        if cells and not cells[0]:
            cells = cells[1:]
        if not cells or not _SN_ROW_RE.search("|{}|".format(cells[0])):
            continue
        if is_example(cells[0]):
            continue
        cells += [""] * (5 - len(cells))
        rows.append(
            {
                "SN-ID": cells[0],
                "Need": cells[1],
                "Why": cells[2],
                "Priority": cells[3],
                "Acceptance": cells[4],
            }
        )
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


def _validate_event(event, where=None):
    """Refuse an event whose shape, kind, decision or derived id is wrong.

    Run on WRITE and on every READ. Verifying the id on read is what turns the
    ledger from something trusted into something checked: a hand-edited line
    recomputes to a different id and is refused by name, naming file and line."""
    at = "{}: ".format(where) if where else ""
    _check_envelope(event, at)
    if event["kind"] == "attestation":
        _check_attestation(event, at)
    _check_derived_id(event, at)
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


def _check_derived_id(event, at):
    if "id" in event and event["id"] != event_id(event):
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
        events.append(_validate_event(obj, where))
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
def boundary_from_config(root):
    """`[attestation] human_ratification_through` from `docs/config.toml`, or the
    kit default when the loader is not present yet.

    Lazily imported (contracts §6) so this module never fails to import because
    a sibling slice has not landed — and so a downstream repo that has not
    adopted the config file still gets the declared default rather than a
    crash."""
    try:
        import config  # deferred by contract (contracts §6), see the docstring
    except ImportError:
        return DEFAULT_BOUNDARY
    try:
        cfg, _findings = config.load_config(root)
        return int(cfg.attestation.human_ratification_through)
    except (AttributeError, KeyError, TypeError, ValueError):
        # The sibling slice's accessor shape is not this module's to assert. An
        # unreadable boundary falls back to the declared default rather than
        # crashing a caller that only wanted to route one tier.
        return DEFAULT_BOUNDARY


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


# --- CLI ----------------------------------------------------------------------
def seed(root, docs=None, by="seed", ts=None):
    """Write a `ratified` anchor for every current spine row that has none.

    The one-time migration: without it every row reads as changed on the first
    run, which would make the first `--candidates` report pure noise and teach
    its reader to ignore it. Idempotent by construction — a row already accepted
    at its current digest is skipped, so re-running after an amendment seeds only
    what is genuinely new."""
    docs = Path(docs) if docs else Path(root) / DOCS_DIR
    ts = ts or datetime.datetime.now(datetime.timezone.utc).strftime(TS_FORMAT)
    chains = chain_map(read_events(ledger_path(root, "attestation")))
    written = {kind: 0 for kind in TIERS}
    artifacts = load_artifacts(docs)
    for kind in TIERS:
        for row in artifacts.get(kind, []):
            rid = row_id(kind, row)
            digest = normative_digest(kind, row)
            chain = chains.get((kind, rid), [])
            if chain_state(chain, digest) == ACCEPTED:
                continue
            parent = chain[-1]["id"] if chain else None
            event = append_event(
                root,
                attestation_event(kind, rid, digest, "ratified", parent, by),
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
    print(
        "attest: {} row(s) need a decision (ratified | clarity | meaning | "
        "override).".format(len(candidates))
    )
    return 1


def _arm_seed(root, docs, by):
    written = seed(root, docs, by=by or "seed")
    print(
        "attest: seeded {} anchor(s) ({}).".format(
            sum(written.values()),
            " ".join("{}={}".format(k, written[k]) for k in TIERS),
        )
    )


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


def _arm_decide(root, request_id, verdict, by):
    if not by:
        raise _refuse("--decide needs --by (only a human decision closes a request)")
    append_event(
        root, review_decision_event(request_id, verdict, by, _review_head(root))
    )
    print("attest: closed review request {}.".format(request_id))


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
        help="write a ratified anchor for every current spine row that has none",
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
        "--by", default=None, help="who is recording this (required to ask)"
    )
    args = ap.parse_args(argv)
    root = Path(args.root)
    docs = Path(args.docs) if args.docs else root / DOCS_DIR

    try:
        if args.seed:
            _arm_seed(root, docs, args.by)
        if args.request:
            _arm_request(root, args.request, args.by)
        if args.decide:
            _arm_decide(root, args.decide, args.verdict, args.by)
        if args.open_:
            _arm_open(root)
        if args.candidates:
            return _print_candidates(root, docs)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
