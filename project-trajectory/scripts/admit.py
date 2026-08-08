#!/usr/bin/env python3
"""admit.py — the ONE transaction that owns every move into the queue.

Several producers writing straight into `queued/` is how an unclassified or
stale row reaches a worker. Each producer re-implements the preconditions, the
copies drift, and the weakest copy quietly becomes the real rule. This module
removes the copies: `draft/` is where anything may be *proposed*, and `admit` is
the only way out of it — so the preconditions become a property of the STATE
rather than of whoever happened to write the row (SN-032, SR-152).

Three things live here, and each closes a specific hole:

  admit               ONE TRANSACTION. Validate everything, move the spec, record
                      the ruling. The preconditions are checked TOGETHER, so a row
                      cannot satisfy some producer's subset; and they are checked
                      by the mover, so nothing can enter the queue past them.

  overlap_graph       FINDINGS, NOT CONFLICTS. Two rows touching one file may be
                      perfectly compatible in a declared order, and deciding that
                      is a judgement. Calling mechanical overlap a conflict would
                      stall the queue on every ordinary pair; leaving it
                      unrecorded would let a real collision through. So the graph
                      is EVIDENCE, handed to an adjudicator (SR-153, LLR-179).

  admission_verdict   THE RULING, CARRYING THE DIGESTS IT WAS COMPUTED AGAINST.
                      A verdict that outlives the state it judged is worse than
                      no verdict, because it reads as a current ruling. Recording
                      the scope and spine digests turns expiry into a mechanical
                      property `check_trajectory.admission_verdict_findings`
                      reads off, rather than a habit someone has to remember
                      (SR-158, LLR-180).

THE ORDERING IS THE DESIGN — validate, MOVE, then RECORD. Two alternatives were
rejected, and the reason is what a crash between the steps leaves behind:

  * record-then-move  A crash between them leaves a verdict in an APPEND-ONLY
                      ledger for a row still sitting in `draft/`. The ledger
                      cannot be retracted, so the repair is a second event
                      contradicting the first, and the history now asserts an
                      admission that never happened. Worse, the recorded scope
                      digest names a still-editable draft: the ruling silently
                      becomes a ruling about text nobody judged.
  * two-phase         A `pending` event, the move, then a `committed` event.
                      Every reader then has to JOIN two events and decide what a
                      lone pending one means — which re-creates exactly the
                      derived-state problem the immutable single event deletes.
  * move-then-record  A crash between them leaves a queued row with NO verdict —
                      which is precisely the state LLR-180 refuses BY NAME. The
                      half-state is loud and self-healing: the strict trajectory
                      check names the row, and re-running `admit` on it records
                      the missing ruling. The failure mode is a visible refusal,
                      never a silent pass, which is the only direction this kit
                      accepts.

The verdict payload is BUILT AND VALIDATED BEFORE the move, so the recording
step is a plain append that has nothing left to refuse. That is what makes the
window between the two steps as small as a filesystem rename plus one write.

**The migration word.** This repo's own queue predates the transaction, so its
rows carry no ruling and would red the strict check on day one. The answer is
`attest.BASELINE`'s, dogfooded: `seed` writes a `pre-transaction` verdict — a
distinguishable word, so a ledger of migrated rows is never counted as that many
adjudications — carrying the scope and spine digests measured AT MIGRATION. The
debt is therefore recorded and still expires: if a migrated row's scope or its
referenced spine moves afterwards, the freshness gate reds it and it must be
admitted properly. An exemption list would have done none of that.

**No F5 copies here, deliberately.** The kit duplicates a small helper so a
script stays independently copy-able — a rule that earns its cost on the hot
paths (a git hook, `integrate.py`'s claim). This module is a trunk-side
transaction that must not RE-DERIVE the scope digest at all (`outcome`'s is the
one home, and an admission event's `scope` has to be the same number an outcome
event's is, or the two cannot be joined), so it already imports its siblings.
A second copy of the ledger helpers on top of that would buy nothing and add a
fourth thing for `tests/test_ledger_helper_sync.py` to pin. Every sibling import
is DEFERRED to the function that needs it, so an unbuilt or absent sibling never
breaks an import chain.

Stdlib only; Windows + POSIX (path math is `posixpath`, I/O is `pathlib`, every
read declares its encoding).

Usage (from the repo root):
    python scripts/admit.py --root . docs/work/draft/WI-420-thing.md
    python scripts/admit.py --root . docs/work/draft/WI-420-thing.md \\
        --verdict compatible-overlap --ordering WI-415 --ordering WI-420
    python scripts/admit.py --root . --overlaps docs/work/draft/WI-420-thing.md
    python scripts/admit.py --root . --seed        # the one-time migration
"""

from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import posixpath
import re
import sys
from pathlib import Path

SCHEMA = 1

# The ledger this module owns (contracts §2). Outside `docs/work/` on purpose:
# `agent_common.spec_files` walks `rglob("WI-*.md")` there, so an event parked
# under the work folder would enter the work-item registry as a malformed spec.
EVENTS_DIR = "docs/events"
ADMISSIONS_LEDGER = EVENTS_DIR + "/admissions.jsonl"

WORK_DIR = "docs/work"
DRAFT_DIR = "draft"
QUEUED_DIR = "queued"

# Directory -> Status, the F5-mirrored table (`check_trajectory`,
# `agent_common`, `schedule`, `wi_convert`). Copied here for the reason those
# copies exist: a folder declared in some readers and not others is SKIPPED by
# the ones that do not know it, so its ids go missing from exactly the
# uniqueness guard this transaction leans on.
SPEC_STATUS_DIRS = {
    "draft": "draft",
    "queued": "queued",
    "active": "active",
    "deferred": "deferred",
    "cancelled": "cancelled",
    "complete": "done",
    "partial": "partial",
}

# The three TERMINAL folders. A candidate carrying one of their ids is a REVIVAL
# (decision 6 / SR-151: an attempted item never returns to the frontier — its
# remaining scope is a newly minted successor with lineage), and a predecessor
# in `cancelled/` or `partial/` is a dependency that will never be satisfied.
# `complete/` is exempt from that second rung: depending on finished work is
# ordinary.
TERMINAL_DIRS = ("complete", "cancelled", "partial")
UNSATISFIABLE_DIRS = ("cancelled", "partial")

# The three adjudicated verdicts (decisions §1 glossary), plus the ONE word the
# migration writes. `pre-transaction` is kept distinct for `attest.BASELINE`'s
# reason: a machine cannot adjudicate, and a ledger of machine baselines spelled
# `no-conflict` reads — to every later counter, card and adjudicator — as that
# many rulings that were never made.
NO_CONFLICT = "no-conflict"
COMPATIBLE = "compatible-overlap"
CONFLICT = "conflict"
VERDICTS = (NO_CONFLICT, COMPATIBLE, CONFLICT)
BASELINE = "pre-transaction"
DECISIONS = VERDICTS + (BASELINE,)

# The declared safety classes — a COPY of `schedule.SAFETY_CLASSES` (which
# `config.py` already copies for the same reason). Pulling the scheduler in to
# read one tuple would make a trunk-side transaction pay for the whole
# dispatcher; `tests/test_admit.py` pins the two equal.
SAFETY_CLASSES = (
    "ordinary",
    "spine",
    "gate",
    "attestation",
    "protected",
    "high-risk",
    "adjudication",
)

# The candidate's own frontmatter keys — the declaration `admit` validates and
# the overlap graph is computed from. They are LISTS, and an ABSENT key is not
# an empty one: `interfaces = []` declares "this touches no seam", which is a
# statement an adjudicator can weigh, where a missing key only says nobody
# thought about it. That distinction is the whole of the `unclassified` rung.
DECLARED_LISTS = ("components", "modules", "interfaces", "likely_files")

# The one non-event origin a candidate may name. It is a VISIBLE claim recorded
# verbatim in the admission event — a reviewer can challenge "owner" — where an
# optional `source` would make its absence unremarkable. Anything else must be
# an event id that resolves in `docs/events/`, so a machine producer cannot
# invent its own provenance word.
SOURCE_OWNER = "owner"

# The overlap dimensions LLR-179 declares, in report order, each naming the
# candidate frontmatter key it reads. `modules` is validated as a declaration
# but is deliberately NOT a dimension: LLR-179 names the axes, and a module is
# already reached through its files and its component, so a sixth axis would
# raise findings the specification does not declare.
OVERLAP_DIMENSIONS = (
    ("requirement", "sr_refs"),
    ("component", "components"),
    ("interface", "interfaces"),
    ("file", "likely_files"),
    ("predecessor", "needs"),
)

# What each dimension is called in a finding sentence, so the message reads as
# English rather than as a key name.
_DIMENSION_NOUN = {
    "requirement": "requirement reference(s)",
    "component": "component(s)",
    "interface": "interface seam(s)",
    "file": "likely file(s)",
    "predecessor": "predecessor(s)",
}

# The spine digest's schema version, carried INSIDE the hashed bytes. Changing
# the rule changes the prefix, so a digest computed under the old rule is
# recognisably old rather than silently agreeing (the `attest-v1` idea,
# contracts §4).
SPINE_PREFIX = "spine-v1"
_FS, _RS = "\x1f", "\x1e"

SR_CSV = "docs/requirements/system-requirements.csv"
IF_CSV = "docs/requirements/interfaces.csv"
CMP_CSV = "docs/requirements/components.csv"

# The registries a declared id is resolved against: key -> (csv, id column,
# id prefix). One table so the two resolvers cannot spell the same rule twice.
DECLARED_REGISTRIES = {
    "components": (CMP_CSV, "CMP-ID", "CMP-"),
    "interfaces": (IF_CSV, "IF-ID", "IF-"),
}

_WI_RE = re.compile(r"^WI-\d+$")
_FILE_ID_RE = re.compile(r"^(WI-\d+)-")
_DIGEST_RE = re.compile(r"^[0-9a-f]{16}$")
_SPINE_ID_RE = re.compile(r"^(SN|SR|LLR|TC)-\d+$")
EXAMPLE_PREFIX = "WI-000-"

TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _refuse(what, why):
    """One refusal in the program's declared shape (contracts §5): the module,
    the offending thing, and the reason — never a bare boolean, and never a
    message whose subject a caller has to guess."""
    return "admit: REFUSED - {} ({})".format(what, why)


# --- the deferred sibling imports ---------------------------------------------
# Each is resolved at CALL time with the `check_trajectory` -> `check_docs`
# fallback: a script directory that is not already on `sys.path` (an importlib
# load from elsewhere) is added once, then the import is retried.


def _sibling(name):
    try:
        return __import__(name)
    except ImportError:  # pragma: no cover - exercised via the sys.path fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        return __import__(name)


def _outcome():
    """`outcome.py` — the spec parser, the frozen scope digest and the ledger
    helpers. The scope digest especially: an admission event's `scope` must be
    the same number an outcome event's is, or the two records cannot be joined
    for one work item."""
    return _sibling("outcome")


def _attest():
    """`attest.py` — the spine rows, the normative digest and the accepted
    anchors the reference-currency rung reads."""
    return _sibling("attest")


# --- the work registry --------------------------------------------------------


def _read_csv_ids(path, column):
    """The non-empty ids in one registry column; `set()` when the file is absent.

    `utf-8-sig`, matching every other reader here: a BOM'd registry (the
    realistic Excel round-trip on a Windows-first kit) would otherwise glue the
    BOM to the first column name and hide every row."""
    path = Path(path)
    if not path.is_file():
        return set()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {
            (row.get(column) or "").strip()
            for row in csv.DictReader(handle)
            if (row.get(column) or "").strip()
        }


def registry(root):
    """Every work item under `docs/work/`, keyed by id.

    Each record is `{"id", "rel", "folder", "status", "data", "text", "homes"}`.
    The id comes from the FILENAME, not the frontmatter, and that is deliberate:
    this mapping is what the uniqueness and revival rungs read, and a spec whose
    TOML fails to parse must still occupy its id — otherwise a malformed row in
    `complete/` would let the same id be minted again as a candidate, which is
    the revival this transaction exists to refuse. (Filename and frontmatter
    disagreeing is `check_trajectory.parse_spec_id`'s finding, not this one's.)

    **`homes` is not decoration.** An id claimed by two files is the exact state
    the uniqueness rung exists to catch, and a plain `{id: record}` LOSES it: the
    second file overwrites the first, so the transaction reads one home, decides
    the id is free, and admits the collision it was asked to prevent. The same
    loss silently defeats the revival rung — a draft sorting ahead of the
    `partial/` row it is reviving would hide the terminal home entirely. So every
    claim on an id is kept, and the rungs that care read all of them; the record's
    own scalar fields are the first home in path order, which is what every other
    rung wants.

    A file sitting DIRECTLY in `docs/work/` has no status directory above it and
    is not a registry entry (`spec_files`' rule); the inert `WI-000-` example is
    skipped like everywhere else."""
    work = Path(root) / WORK_DIR
    out = {}
    if not work.is_dir():
        return out
    for path in sorted(work.rglob("WI-*.md")):
        if path.parent == work or path.name.startswith(EXAMPLE_PREFIX):
            continue
        match = _FILE_ID_RE.match(path.name)
        if not match:
            continue
        rel = path.relative_to(work).as_posix()
        folder = rel.split("/")[0]
        home = {
            "rel": WORK_DIR + "/" + rel,
            "folder": folder,
            "status": SPEC_STATUS_DIRS.get(folder, ""),
        }
        existing = out.get(match.group(1))
        if existing is not None:
            existing["homes"].append(home)
            continue
        text = path.read_text(encoding="utf-8")
        try:
            data, _body = _outcome().parse_spec(text)
        except ValueError:
            data = {}
        out[match.group(1)] = dict(
            home, id=match.group(1), data=data, text=text, homes=[home]
        )
    return out


def _homes_in(record, folders):
    """The record's homes that sit in one of `folders`, in path order."""
    return [h for h in (record or {}).get("homes", ()) if h["folder"] in folders]


def declaration(record):
    """One registry record as the flat declaration `overlap_graph` reads — the
    spec's own frontmatter with the id filled in from the record, so a spec
    whose frontmatter omits `id` still names itself in a finding."""
    decl = dict(record.get("data") or {})
    decl["id"] = record["id"]
    return decl


def _in_folders(reg, folders):
    """The declarations of every work item with a home in `folders`.

    Read through `homes` rather than the record's own folder: an id claimed by
    two files is already a refusal, but the overlap graph must still SEE the
    queued claim while that refusal is being reported, or the two findings a
    reader needs arrive one run apart."""
    return [declaration(r) for r in reg.values() if _homes_in(r, folders)]


# --- the mechanical overlap graph (LLR-179) -----------------------------------


# The two normalisations, keyed by the frontmatter cell they apply to — one
# table, so the overlap graph and the validation rungs can never normalise the
# same cell two ways and then disagree about whether two rows share a token.
_ID_LIST_KEYS = ("needs", "supersedes")
_PATH_LIST_KEYS = ("modules", "likely_files")


def _tokens(value, key):
    """One declaration cell as a normalised token set.

    A bare string reads as a one-element list (a hand-written `components =
    "CMP-004"` is a legible declaration, and refusing it here would only move
    the refusal away from the rung that names it). A `~` soft-predecessor prefix
    is stripped, because an advisory ordering hint still names the same row.
    Path cells fold `\\` to `/` and normalise `./` away, so one file declared
    two ways is one token — otherwise the whole file dimension is defeated by a
    Windows author writing the separator their shell prints."""
    if value is None:
        return set()
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, (list, tuple)):
        return set()
    out = set()
    for item in value:
        token = str(item).strip()
        if key in _ID_LIST_KEYS:
            token = token.lstrip("~").strip()
        elif key in _PATH_LIST_KEYS and token:
            token = posixpath.normpath(token.replace("\\", "/"))
        if token:
            out.add(token)
    return out


def _dimensions(decl):
    """`{dimension: {token}}` for one declaration."""
    return {name: _tokens(decl.get(key), key) for name, key in OVERLAP_DIMENSIONS}


def _pair_findings(a_id, a_dims, b_id, b_dims):
    """Every dimension on which two declarations share a token, in report order."""
    out = []
    for name, _key in OVERLAP_DIMENSIONS:
        shared = sorted(a_dims[name] & b_dims[name])
        if not shared:
            continue
        out.append(
            {
                "a": a_id,
                "b": b_id,
                "dimension": name,
                "shared": shared,
                "finding": (
                    "{} and {} both declare {} {} — an overlap for the "
                    "adjudicator to dispose of, not a conflict (a declared "
                    "ordering or partition may make it compatible)".format(
                        a_id,
                        b_id,
                        _DIMENSION_NOUN[name],
                        ", ".join(shared),
                    )
                ),
            }
        )
    return out


def overlap_graph(candidates, active, queued):
    """LLR-179 — the mechanical overlap between candidates and work in flight,
    as FINDINGS.

    `candidates`, `active` and `queued` are lists of flat declarations (a spec's
    frontmatter with `id`); `declaration` builds one from a registry record.
    Each finding is `{"a", "b", "dimension", "shared", "finding"}` — `a` is
    always the candidate, `shared` is the sorted intersection, and `finding` is
    the sentence a reader sees.

    **These are findings, never conflicts, and the asymmetry is the reason.**
    Two rows touching one file are commonly fine in a declared order; calling
    that a conflict would stall the queue on every ordinary pair, and a queue
    that stalls on the ordinary case gets its gate switched off. Missing a real
    collision costs one bad merge, which is expensive but visible and repairable.
    So the mechanical half reports EVERYTHING it can see and rules on nothing,
    and the semantic judgement stays with the adjudicator, who is the only party
    that can read two scopes and say whether they compose.

    Candidates are paired against active and queued work AND AGAINST EACH OTHER:
    a batch admitted in one sitting can collide inside itself, and a graph blind
    to that would wave the collision through precisely when several rows arrive
    together. Self-pairs are skipped, and each unordered pair is reported once,
    so re-admitting a row does not double every finding it already had."""
    cand = [(d.get("id"), _dimensions(d)) for d in candidates]
    others = [(d.get("id"), _dimensions(d)) for d in list(active) + list(queued)]
    out, seen = [], set()
    for index, (a_id, a_dims) in enumerate(cand):
        for b_id, b_dims in others + cand[index + 1 :]:
            if not a_id or not b_id or a_id == b_id:
                continue
            key = tuple(sorted((a_id, b_id)))
            if key in seen:
                continue
            seen.add(key)
            out.extend(_pair_findings(a_id, a_dims, b_id, b_dims))
    order = [name for name, _key in OVERLAP_DIMENSIONS]
    return sorted(out, key=lambda f: (f["a"], f["b"], order.index(f["dimension"])))


# --- the two digests a verdict names ------------------------------------------


def spine_refs(data):
    """The spine ids one declaration references, sorted and de-duplicated."""
    return sorted(_tokens(data.get("sr_refs"), "sr_refs"))


def spine_view(root, docs=None):
    """`({id: (kind, row)}, {id: anchor digest})` for the whole current spine.

    Read ONCE and passed down, because both the reference-currency rung and the
    spine digest ask the same two questions of every referenced row, and reading
    the attestation ledger twice per admission would be pure cost."""
    attest = _attest()
    docs = Path(docs) if docs else Path(root) / "docs"
    artifacts = attest.load_artifacts(docs)
    chains = attest.chain_map(
        attest.read_events(attest.ledger_path(root, "attestation"))
    )
    rows, anchors = {}, {}
    for kind in attest.TIERS:
        for row in artifacts.get(kind, []):
            rid = attest.row_id(kind, row)
            rows[rid] = (kind, row)
            anchor = attest.anchor_in(chains.get((kind, rid), []))
            anchors[rid] = anchor["digest"] if anchor else ""
    return rows, anchors


def spine_digest(root, refs, view=None):
    """The 16-hex digest of the spine state a verdict was computed against.

    Per REFERENCED row: its id, its current normative digest, and its accepted
    anchor. Either half moving stales the verdict — an amendment to the cited
    requirement, or an attestation event that pulled the anchor out from under
    it — which is the pair SR-158 exists to catch.

    **THE BOUNDARY, STATED RATHER THAN LEFT TO BE DISCOVERED.** Only the rows
    the candidate CITES are covered, so a row citing nothing digests the empty
    set and no spine edit can ever stale its verdict. That is deliberate and it
    is the narrower of two honest choices. Digesting the WHOLE spine instead
    would stale every queued verdict on every unrelated requirement edit, in a
    repo that amends requirements continuously — and a freshness rule that reds
    the queue daily is one that gets switched off, which converts a precise
    signal into no signal at all. The narrow rule moves exactly when the thing
    the verdict cited moves, which is also what LLR-178's own bullet scopes the
    admission's spine obligation to ("a current attestation anchor for every
    REFERENCED normative row"). The residue — an off-spine candidate whose
    verdict cannot expire through the spine — is named here so a later widening
    is a decision rather than a discovery; widening it must change
    `SPINE_PREFIX`, so old digests read as old rather than as agreeing."""
    rows, anchors = view if view is not None else spine_view(root)
    attest = _attest()
    blob = SPINE_PREFIX + "\n"
    for rid in sorted({r for r in refs if r}):
        entry = rows.get(rid)
        current = attest.normative_digest(*entry) if entry else ""
        blob += rid + _FS + current + _FS + anchors.get(rid, "") + _RS
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def candidate_digests(root, spec_text, view=None):
    """`(scope, spine)` for one spec's CURRENT text — the pair a verdict names
    and the freshness gate recomputes.

    ONE home for the recomputation, so `admit` (which records the pair) and
    `check_trajectory.admission_verdict_findings` (which compares against it)
    cannot disagree about what "the current one" means. A second derivation
    would be a second place to be wrong, and its wrongness would show up as a
    queue that reds for no reason."""
    data, _body = _outcome().parse_spec(spec_text)
    return (
        _outcome().scope_digest(spec_text),
        spine_digest(root, spine_refs(data), view=view),
    )


# --- the admission ledger -----------------------------------------------------


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime(TS_FORMAT)


def ledger_path(root, ledger=None):
    return Path(ledger) if ledger else Path(root) / ADMISSIONS_LEDGER


def read_admissions(root, ledger=None):
    """Every admission event in file order. A malformed line is a hard read
    error naming the file and the line number (contracts §2) — `outcome`'s
    reader, which also re-derives each id, so a hand-edited ledger line is
    caught rather than trusted."""
    return [
        e
        for e in _outcome().read_events(ledger_path(root, ledger))
        if e.get("kind") == "admission"
    ]


def latest_admission(root, wi, ledger=None):
    """The NEWEST admission event for one work item, or None.

    Newest-wins, like `attest.anchor_in`: a re-admission after an amendment is a
    legitimate second ruling, and the ledger is append-only, so the current
    verdict is the last one written rather than the first."""
    found = None
    for event in read_admissions(root, ledger):
        if event.get("wi") == wi:
            found = event
    return found


# The CLOSED schema. `_verdict_payload` builds from this list alone and refuses
# any other keyword — the mechanical half of "the event carries facts, never
# instructions": there is no extension point a reader might act on, so a would-be
# instruction has to arrive as `rationale`, one delimited string every consumer
# renders as quoted evidence.
ADMISSION_FACTS = (
    "ordering",
    "partition",
    "cancels",
    "replacement",
    "source",
    "declared",
    "by",
    "rationale",
)


def _wi_list(name, value, findings):
    out = []
    if not isinstance(value, (list, tuple)):
        findings.append(
            _refuse("{} is not a list".format(name), "got {!r}".format(value))
        )
        return out
    for item in value:
        if not isinstance(item, str) or not _WI_RE.match(item.strip()):
            findings.append(
                _refuse(
                    "{} entry {!r} is not a WI-### id".format(name, item),
                    "an ordering or partition names work items",
                )
            )
            continue
        out.append(item.strip())
    return out


def _partition(value, findings):
    """A partition as a list of disjoint id groups; every group validated."""
    if not isinstance(value, (list, tuple)):
        findings.append(
            _refuse("partition is not a list of groups", "got {!r}".format(value))
        )
        return []
    out, seen = [], set()
    for group in value:
        ids = _wi_list("partition group", group, findings)
        overlap = sorted(seen & set(ids))
        if overlap:
            findings.append(
                _refuse(
                    "partition groups share {}".format(", ".join(overlap)),
                    "a partition PARTITIONS: an id in two groups states that the "
                    "work is both separable and not",
                )
            )
        seen |= set(ids)
        out.append(sorted(ids))
    return out


def _decision_findings(wi, decision, overlaps, ordering, partition, extra):
    """The rungs that make a verdict answer the evidence it was given."""
    out = []
    if decision == NO_CONFLICT and overlaps:
        out.append(
            _refuse(
                "{} records {} over {} mechanical overlap(s)".format(
                    wi, NO_CONFLICT, len(overlaps)
                ),
                "an overlap that exists is disposed of, not ignored: rule it "
                "{} with a declared ordering or partition, or {} with a "
                "cancellation or a replacement draft".format(COMPATIBLE, CONFLICT),
            )
        )
    if decision == COMPATIBLE and not (ordering or partition):
        out.append(
            _refuse(
                "{} records {} with neither an ordering nor a partition".format(
                    wi, COMPATIBLE
                ),
                "compatible means compatible UNDER SOMETHING; without the "
                "ordering or the partition the ruling states no way to run the "
                "two rows safely",
            )
        )
    if decision == CONFLICT and not (extra.get("cancels") or extra.get("replacement")):
        out.append(
            _refuse(
                "{} records {} with neither a cancellation nor a replacement "
                "draft".format(wi, CONFLICT),
                "a conflict resolves: the candidate is cancelled, or it is "
                "replaced by a draft that does not collide",
            )
        )
    if decision == BASELINE and (
        ordering or partition or extra.get("cancels") or extra.get("replacement")
    ):
        out.append(
            _refuse(
                "{} records {} carrying a ruling".format(wi, BASELINE),
                "the migration DECIDED nothing; it records what the queue held "
                "when the ledger opened",
            )
        )
    return out


def _verdict_payload(wi, decision, scope, spine, overlaps, extra):
    """The validated `admission` event body, and EVERY problem with it.

    Every finding, not the first: a caller fixing a malformed ruling learns all
    of them in one run rather than one per attempt (contracts §5)."""
    findings = []
    if not isinstance(wi, str) or not _WI_RE.match(wi or ""):
        findings.append(
            _refuse("{!r} is not a WI-### id".format(wi), "the event is keyed by it")
        )
    if decision not in DECISIONS:
        findings.append(
            _refuse(
                "{!r} is not an admission verdict".format(decision),
                "the vocabulary is " + " | ".join(DECISIONS),
            )
        )
    for name, value in (("scope", scope), ("spine", spine)):
        if not isinstance(value, str) or not _DIGEST_RE.match(value or ""):
            findings.append(
                _refuse(
                    "{} digest {!r} is not 16 hex".format(name, value),
                    "the verdict names the state it was computed against, or it "
                    "names nothing and cannot expire",
                )
            )
    undeclared = sorted(set(extra) - set(ADMISSION_FACTS))
    if undeclared:
        findings.append(
            _refuse(
                "undeclared event field(s): " + ", ".join(undeclared),
                "the admission schema is closed so no field can arrive as an "
                "instruction; the declared facts are " + ", ".join(ADMISSION_FACTS),
            )
        )
    ordering = _wi_list("ordering", extra.get("ordering", ()), findings)
    partition = _partition(extra.get("partition", ()), findings)
    findings += _decision_findings(wi, decision, overlaps, ordering, partition, extra)
    rationale = extra.get("rationale", "")
    if not isinstance(rationale, str):
        findings.append(
            _refuse(
                "rationale is not a string",
                "it is one delimited value a reader renders as quoted evidence, "
                "never a structure a reader walks",
            )
        )
        rationale = ""
    payload = {
        "schema": SCHEMA,
        "kind": "admission",
        "wi": wi,
        "verdict": decision,
        "scope": scope,
        "spine": spine,
        "overlaps": sorted(
            "{} {} {}".format(f["b"], f["dimension"], " ".join(f["shared"]))
            for f in overlaps
        ),
        "ordering": ordering,
        "partition": partition,
        "cancels": str(extra.get("cancels") or ""),
        "replacement": str(extra.get("replacement") or ""),
        "source": str(extra.get("source") or ""),
        "declared": dict(extra.get("declared") or {}),
        "by": str(extra.get("by") or ""),
        "rationale": rationale,
    }
    return payload, findings


def _duplicate_finding(root, payload, ledger=None):
    """A refusal when these exact facts are already in the ledger.

    Duplicate detection is free in an UNCHAINED ledger (contracts §2, property
    1): the id is the digest of the payload with `id`/`ts` removed, so a second
    write of the same ruling derives the same id. `ts` is excluded precisely so
    that observing the same fact twice is not two events."""
    event_id = _outcome().event_id(payload)
    for event in read_admissions(root, ledger):
        if event.get("id") == event_id:
            return _refuse(
                "{} already carries this exact ruling (event {})".format(
                    payload.get("wi"), event_id
                ),
                "the ledger is append-only and the id is derived from the facts, "
                "so re-recording an unchanged verdict would add a second event "
                "asserting one ruling",
            )
    return None


def admission_verdict(
    root, wi, verdict, scope, spine, *, overlaps=(), ts=None, ledger=None, **extra
):
    """Record the conflict ruling that permits (or refuses) one candidate:
    `(event, [refusals])`.

    The verdict carries the SCOPE digest and the SPINE digest it was computed
    against, which is what turns expiry into a mechanical property rather than a
    habit: `check_trajectory.admission_verdict_findings` recomputes both and
    refuses the row when either has moved. Without them a ruling made against
    last week's requirement text still READS as a current ruling, which is worse
    than no ruling at all.

    `no-conflict` may not be recorded over a non-empty overlap graph,
    `compatible-overlap` must name its ordering or partition, and `conflict`
    must name its cancellation or its replacement draft — each refusal names the
    missing half, because a verdict that answers none of its evidence is a
    rubber stamp with a vocabulary."""
    payload, findings = _verdict_payload(wi, verdict, scope, spine, overlaps, extra)
    if findings:
        return None, findings
    duplicate = _duplicate_finding(root, payload, ledger)
    if duplicate:
        return None, [duplicate]
    payload["ts"] = ts or _now()
    return _outcome().append_event(ledger_path(root, ledger), payload), []


# --- the preconditions --------------------------------------------------------


def _read_candidate(root, candidate_path):
    """`(candidate, refusal)` for the draft spec at `candidate_path`.

    The path may be absolute or repo-relative; what it may NOT be is anywhere
    but `docs/work/draft/`. `draft/` is the state that means "proposed, not
    ruled on", so admitting from anywhere else would mean the transaction had
    already been bypassed by whoever put the file there."""
    root = Path(root)
    path = Path(candidate_path)
    if not path.is_absolute():
        path = root / path
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None, _refuse(
            "{} is outside the repo at {}".format(path, root),
            "a candidate is a tracked spec in this repo's draft folder",
        )
    expected = WORK_DIR + "/" + DRAFT_DIR + "/"
    if not rel.startswith(expected):
        return None, _refuse(
            "{} is not in {}".format(rel, expected),
            "`draft/` is the proposed-but-unruled state, and admission is the "
            "only way out of it; a spec elsewhere has already bypassed this "
            "transaction",
        )
    if not path.is_file():
        return None, _refuse(
            "there is no candidate file at {}".format(rel),
            "the transaction moves a spec that exists",
        )
    match = _FILE_ID_RE.match(path.name)
    if not match:
        return None, _refuse(
            "{} does not carry a WI-### id in its filename".format(rel),
            "the filename is what reserves the id across every state folder",
        )
    text = path.read_text(encoding="utf-8")
    try:
        data, _body = _outcome().parse_spec(text)
    except ValueError as exc:
        return None, str(exc)
    return {
        "id": match.group(1),
        "rel": rel,
        "name": path.name,
        "path": path,
        "text": text,
        "data": data,
    }, None


def _identity_findings(candidate, reg):
    """Unique id, and the frontmatter agreeing with the filename."""
    out = []
    wid = candidate["id"]
    declared = str(candidate["data"].get("id") or "").strip()
    if declared != wid:
        out.append(
            _refuse(
                "{} declares id {!r} but its filename carries {}".format(
                    candidate["rel"], declared, wid
                ),
                "two homes for one fact; the id is compared here rather than "
                "trusted apart",
            )
        )
    record = reg.get(wid)
    others = [
        h["rel"]
        for h in (record or {}).get("homes", ())
        if h["rel"] != candidate["rel"]
    ]
    if others:
        out.append(
            _refuse(
                "{} is already the id of {}".format(wid, ", ".join(others)),
                "a work-item id names ONE item for the life of the registry; two "
                "rows sharing one id make every join ambiguous",
            )
        )
    return out


def _provenance_findings(root, candidate, scope):
    """The immutable scope digest and the source event.

    The declared `scope_digest` is compared against the digest of the spec AS IT
    NOW STANDS. They differ exactly when the draft was edited after its digest
    was frozen — which is the state a producer must never be able to carry into
    the queue, because everything downstream compares delivered work against
    that number."""
    out = []
    data = candidate["data"]
    wid = candidate["id"]
    declared = str(data.get("scope_digest") or "").strip()
    if not _DIGEST_RE.match(declared):
        out.append(
            _refuse(
                "{} declares scope_digest {!r}, which is not 16 hex".format(
                    wid, declared
                ),
                "it is `outcome.scope_digest`'s output or it is not a scope digest",
            )
        )
    elif declared != scope:
        out.append(
            _refuse(
                "{} declares scope_digest {} but its frozen scope now digests "
                "{}".format(wid, declared, scope),
                "the draft was edited after its digest was frozen; re-freeze it "
                "deliberately rather than admitting text nobody has read",
            )
        )
    out += _source_findings(root, wid, data)
    return out


def _source_findings(root, wid, data):
    """The producing event, resolved in `docs/events/`."""
    source = str(data.get("source") or "").strip()
    if not source:
        return [
            _refuse(
                "{} declares no source".format(wid),
                "a candidate names the event that produced it (a 16-hex id in "
                "docs/events/) or the one declared non-event origin {!r}; "
                "provenance nobody records is provenance nobody can "
                "challenge".format(SOURCE_OWNER),
            )
        ]
    if source == SOURCE_OWNER:
        return []
    if not _DIGEST_RE.match(source):
        return [
            _refuse(
                "{} declares source {!r}".format(wid, source),
                "a source is an event id (16 hex) or {!r}; a producer may not "
                "invent its own provenance word".format(SOURCE_OWNER),
            )
        ]
    if source in _event_ids(root):
        return []
    return [
        _refuse(
            "{} declares source event {} which resolves in no ledger under {}/".format(
                wid, source, EVENTS_DIR
            ),
            "a source that names nothing recorded is indistinguishable from no "
            "source at all",
        )
    ]


def _event_ids(root):
    """Every event id recorded in any ledger under `docs/events/`."""
    outcome = _outcome()
    ids = set()
    events = Path(root) / EVENTS_DIR
    if not events.is_dir():
        return ids
    for path in sorted(events.glob("*.jsonl")):
        for event in outcome.read_events(path):
            if event.get("id"):
                ids.add(event["id"])
    return ids


def _revival_findings(candidate, reg):
    """No attempted WI is ever revived (decision 6, SR-151).

    Three rungs, each naming a different way the same mistake arrives: the
    candidate carrying a TERMINAL row's own id; a `supersedes` target that is
    absent, still live, or the candidate itself; and a predecessor parked in
    `cancelled/` or `partial/`, which is a dependency that can never be
    satisfied because the row it names will never finish."""
    out = []
    wid = candidate["id"]
    terminal = _homes_in(reg.get(wid), TERMINAL_DIRS)
    if terminal:
        out.append(
            _refuse(
                "{} is already terminal at {}".format(
                    wid, ", ".join(h["rel"] for h in terminal)
                ),
                "an attempted item never returns to the frontier; its remaining "
                "scope is a NEWLY minted successor with `supersedes` lineage, "
                "never this row re-queued as itself",
            )
        )
    for target in sorted(_tokens(candidate["data"].get("supersedes"), "supersedes")):
        out += _supersedes_findings(wid, target, reg)
    for pred in sorted(_tokens(candidate["data"].get("needs"), "needs")):
        dead = _homes_in(reg.get(pred), UNSATISFIABLE_DIRS)
        if dead:
            out.append(
                _refuse(
                    "{} depends on {}, which is {}".format(
                        wid, pred, dead[0]["status"]
                    ),
                    "a terminal-but-unfinished predecessor can never be "
                    "satisfied; depend on its successor instead",
                )
            )
    return out


def _supersedes_findings(wid, target, reg):
    if target == wid:
        return [
            _refuse(
                "{} supersedes itself".format(wid),
                "lineage points BACKWARD at the attempt whose scope this row "
                "carries; a self-reference is the revival written differently",
            )
        ]
    record = reg.get(target)
    if record is None:
        return [
            _refuse(
                "{} supersedes {}, which is not a work item".format(wid, target),
                "lineage names a row that exists, or it records nothing",
            )
        ]
    if not _homes_in(record, TERMINAL_DIRS):
        return [
            _refuse(
                "{} supersedes {}, which is {}".format(wid, target, record["status"]),
                "a successor carries the REMAINING scope of a finished attempt; "
                "superseding live work would leave two rows owning one scope",
            )
        ]
    return []


def _cycle_finding(candidate, reg):
    """Predecessor existence and acyclicity, in one walk.

    The candidate is new, so a cycle can only close THROUGH it: walk forward
    over predecessor edges from each declared predecessor and refuse if the
    candidate is reached. The `seen` set also guards the walk against a cycle
    that already exists in the registry — that one is
    `check_trajectory.validate`'s finding to report, not this transaction's to
    hang on."""
    out = []
    wid = candidate["id"]
    preds = sorted(_tokens(candidate["data"].get("needs"), "needs"))
    for pred in preds:
        if pred not in reg:
            out.append(
                _refuse(
                    "{} declares predecessor {}, which is not a work item".format(
                        wid, pred
                    ),
                    "a DAG edge to a row that does not exist can never be "
                    "satisfied, so the candidate would never become ready",
                )
            )
    seen, stack = set(), [p for p in preds if p in reg or p == wid]
    while stack:
        node = stack.pop()
        if node == wid:
            out.append(
                _refuse(
                    "{}'s predecessors close a dependency cycle".format(wid),
                    "a trajectory that depends on itself can never start",
                )
            )
            break
        if node in seen:
            continue
        seen.add(node)
        record = reg.get(node)
        if record:
            stack += sorted(_tokens(record["data"].get("needs"), "needs"))
    return out


def _specref_findings(root, candidate):
    """The candidate's SpecRef resolves — rule R-E, checked HERE rather than
    after the row is already in the queue.

    `check_trajectory.specref_findings` is the one home for the rule (both
    halves of a `path#anchor`), reused rather than re-derived so a SpecRef
    cannot pass at admission and fail at the gate. A tree without that module
    falls back to the path half alone: degrading to a weaker check is
    acceptable, silently skipping the precondition is not."""
    wid = candidate["id"]
    spec = str(candidate["data"].get("specref") or "").strip()
    row = {"id": wid, "specref": spec, "status": "queued"}
    try:
        messages = _sibling("check_trajectory").specref_findings(root, row)
    except (ImportError, AttributeError):  # pragma: no cover - absent sibling
        messages = []
        if not spec:
            messages = ["{}: open WI has no SpecRef".format(wid)]
        elif not (Path(root) / spec.partition("#")[0].strip()).is_file():
            messages = [
                "{}: SpecRef {!r} does not resolve to an in-repo file".format(wid, spec)
            ]
    return [
        _refuse(
            message,
            "a candidate's forward bridge must resolve BEFORE it is queued; a "
            "dangling SpecRef is discovered by the worker who needed it",
        )
        for message in messages
    ]


def _reference_findings(root, candidate, view):
    """Current spine references, and a current attestation anchor for each.

    An anchor at a different digest means the requirement text moved after it
    was accepted: the candidate would be built against a version nobody has
    ratified, and the whole point of admitting against the spine is that the
    spine it was admitted against is the one that is standing."""
    out = _specref_findings(root, candidate)
    rows, anchors = view
    attest = _attest()
    wid = candidate["id"]
    for rid in spine_refs(candidate["data"]):
        if not _SPINE_ID_RE.match(rid):
            out.append(
                _refuse(
                    "{} references {!r}, which is not a spine id".format(wid, rid),
                    "a reference names an SN/SR/LLR/TC row",
                )
            )
            continue
        entry = rows.get(rid)
        if entry is None:
            out.append(
                _refuse(
                    "{} references {}, which resolves to no spine row".format(wid, rid),
                    "the reference is stale or the row was never written",
                )
            )
            continue
        anchor = anchors.get(rid, "")
        current = attest.normative_digest(*entry)
        if not anchor:
            out.append(
                _refuse(
                    "{} references {}, which has no accepted attestation anchor".format(
                        wid, rid
                    ),
                    "building against unattested text means the obligation can "
                    "change under the work without anyone having decided it did",
                )
            )
        elif anchor != current:
            out.append(
                _refuse(
                    "{} references {}, whose normative text has moved since its "
                    "accepted anchor ({} -> {})".format(
                        wid, rid, anchor[:12], current[:12]
                    ),
                    "re-attest the row (a `clarity` verdict if the meaning did "
                    "not move) before admitting work against it",
                )
            )
    return out


def _classification_findings(root, candidate):
    """The declared blast radius and the safety class.

    An ABSENT list is not an empty one. `interfaces = []` declares "this touches
    no seam" — a statement an adjudicator can weigh and a reviewer can refute —
    where a missing key says only that nobody thought about it. The whole
    overlap graph is computed from these four cells, so a row that declares none
    of them is invisible to it: it would be admitted against no evidence at all
    and read, afterwards, as having been cleared."""
    out = []
    data = candidate["data"]
    wid = candidate["id"]
    safety = str(data.get("safety_class") or "").strip()
    if safety not in SAFETY_CLASSES:
        out.append(
            _refuse(
                "{} declares safety_class {!r}".format(wid, safety),
                "the vocabulary is " + " | ".join(SAFETY_CLASSES),
            )
        )
    for key in DECLARED_LISTS:
        if key not in data:
            out.append(
                _refuse(
                    "{} declares no {}".format(wid, key),
                    "an absent declaration is not an empty one — write {} = [] to "
                    "state that it touches none".format(key),
                )
            )
        elif not isinstance(data[key], (list, tuple)):
            out.append(
                _refuse(
                    "{}'s {} is not a list".format(wid, key),
                    "got {!r}".format(data[key]),
                )
            )
    for key in DECLARED_REGISTRIES:
        out += _registry_id_findings(root, wid, data, key)
    for key in ("modules", "likely_files"):
        out += _path_declaration_findings(wid, data, key)
    return out


def _registry_id_findings(root, wid, data, key):
    """Declared CMP/IF ids resolve to real registry rows."""
    rel, column, prefix = DECLARED_REGISTRIES[key]
    if not isinstance(data.get(key), (list, tuple)):
        return []
    known = _read_csv_ids(Path(root) / rel, column)
    out = []
    for token in sorted(_tokens(data.get(key), key)):
        if not token.startswith(prefix):
            out.append(
                _refuse(
                    "{} declares {} {!r}".format(wid, key, token),
                    "a {} entry is a {}### id".format(key, prefix),
                )
            )
        elif token not in known:
            out.append(
                _refuse(
                    "{} declares {} {}, which resolves to no row in {}".format(
                        wid, key, token, rel
                    ),
                    "declaring a boundary that does not exist states no boundary",
                )
            )
    return out


def _path_declaration_findings(wid, data, key):
    """Declared paths are repo-relative — the form the overlap graph compares.

    An absolute path or a `..` escape names a file outside this repo, which no
    other declaration can meaningfully overlap with, so the file dimension would
    silently stop working for exactly the row that wrote one."""
    if not isinstance(data.get(key), (list, tuple)):
        return []
    out = []
    for token in sorted(_tokens(data.get(key), key)):
        if posixpath.isabs(token) or re.match(r"^[A-Za-z]:", token):
            out.append(
                _refuse(
                    "{} declares absolute path {!r} in {}".format(wid, token, key),
                    "declarations are repo-relative, so two rows naming one file "
                    "name it the same way",
                )
            )
        elif token == ".." or token.startswith("../"):
            out.append(
                _refuse(
                    "{} declares {!r} in {}, which escapes the repo".format(
                        wid, token, key
                    ),
                    "a file outside this repo cannot overlap with anything "
                    "declared inside it",
                )
            )
    return out


# --- the transaction ----------------------------------------------------------


def _verdict_request(verdict, wi, overlaps):
    """`(decision, extra, findings)` for the caller's `verdict` argument.

    `None` is legal ONLY when the overlap graph is empty: there was nothing to
    judge, so recording `no-conflict` is a statement of fact rather than a
    machine pretending to have adjudicated. With overlaps present, an absent
    verdict is the "unreviewed overlap" precondition failing — the one this
    module exists to make unrepresentable."""
    if verdict is None:
        if overlaps:
            return (
                None,
                {},
                [
                    _refuse(
                        "{} has {} mechanical overlap(s) with queued or active "
                        "work and no adjudicated verdict".format(wi, len(overlaps)),
                        "mechanical overlap is a candidate finding, not a "
                        "conflict — an adjudicator disposes of it as {} with a "
                        "declared ordering or partition, or as {} with a "
                        "cancellation or a replacement draft".format(
                            COMPATIBLE, CONFLICT
                        ),
                    )
                ],
            )
        return NO_CONFLICT, {}, []
    if isinstance(verdict, str):
        return verdict, {}, []
    if isinstance(verdict, dict):
        extra = dict(verdict)
        return extra.pop("verdict", None), extra, []
    return (
        None,
        {},
        [
            _refuse(
                "the verdict {!r} is neither a word nor a ruling".format(verdict),
                "pass one of {} or a mapping carrying `verdict` plus its "
                "ordering / partition / cancellation".format(" | ".join(VERDICTS)),
            )
        ],
    )


def _declared_record(data):
    """The declaration the ruling was computed from, recorded as FACTS on the
    event. It is not a fourth digest and does not gate anything (LLR-180 names
    three rungs and this module implements exactly those) — it is there so a
    reader of the ledger can see WHAT the adjudicator was looking at without
    re-reading a spec that has since moved."""
    out = {key: sorted(_tokens(data.get(key), key)) for key in DECLARED_LISTS}
    out["sr_refs"] = spine_refs(data)
    out["needs"] = sorted(_tokens(data.get("needs"), "needs"))
    out["supersedes"] = sorted(_tokens(data.get("supersedes"), "supersedes"))
    out["safety_class"] = str(data.get("safety_class") or "").strip()
    return out


def _move(root, candidate):
    """The `draft/` -> `queued/` half of the transaction: `(dest, refusal)`.

    `spec_move.move_spec` is the declared indivisible ritual — move, rebase the
    moved file's own links, redirect every inbound link — and it is used rather
    than a rename because a plan or a log commonly links the draft it discusses,
    and a bare rename strands those links exactly when the row becomes work
    somebody is about to read."""
    dest = "{}/{}/{}".format(WORK_DIR, QUEUED_DIR, candidate["name"])
    _touched, refusal = _sibling("spec_move").move_spec(root, candidate["rel"], dest)
    if refusal:
        return None, _refuse(
            "cannot move {} to {}: {}".format(candidate["rel"], dest, refusal),
            "the move is the transaction's first half and it did not happen, so "
            "nothing was recorded",
        )
    return dest, None


def admit(root, candidate_path, *, verdict=None, ts=None, ledger=None):
    """LLR-178 — validate a `draft/` candidate, move it to `queued/`, and record
    its admission verdict, as ONE transaction: `(event, [refusals])`.

    Every precondition is checked before anything is written, and EVERY failure
    is reported rather than the first, so a producer fixing a candidate learns
    all of them in one run. The preconditions, in the order the plan §8 states
    them: a unique id; a valid immutable scope digest and a source event that
    resolves; predecessor existence, acyclicity and no attempted-WI revival; a
    current SpecRef and current spine references with a current attestation
    anchor behind each; a declared blast radius (components, modules,
    interfaces, likely files) and safety class; and no queued or active item
    with an unreviewed overlap.

    The write order is validate -> MOVE -> RECORD; the module docstring states
    which orderings were rejected and what a crash between the steps leaves
    behind. The verdict payload is built and validated in the FIRST phase, so
    the recording step is a plain append with nothing left to refuse and the
    window between the two halves is one rename wide."""
    root = Path(root)
    candidate, refusal = _read_candidate(root, candidate_path)
    if refusal:
        return None, [refusal]
    reg = registry(root)
    view = spine_view(root)
    scope = _outcome().scope_digest(candidate["text"])
    spine = spine_digest(root, spine_refs(candidate["data"]), view=view)
    findings = _identity_findings(candidate, reg)
    findings += _provenance_findings(root, candidate, scope)
    findings += _cycle_finding(candidate, reg)
    findings += _revival_findings(candidate, reg)
    findings += _reference_findings(root, candidate, view)
    findings += _classification_findings(root, candidate)
    overlaps = overlap_graph(
        [declaration(candidate)],
        _in_folders(reg, ("active",)),
        _in_folders(reg, (QUEUED_DIR,)),
    )
    payload, ruling_findings = _ruling(
        root, candidate, scope, spine, overlaps, verdict, ledger=ledger
    )
    findings += ruling_findings
    if findings:
        return None, findings
    _dest, refusal = _move(root, candidate)
    if refusal:
        return None, [refusal]
    payload["ts"] = ts or _now()
    return _outcome().append_event(ledger_path(root, ledger), payload), []


def _ruling(root, candidate, scope, spine, overlaps, verdict, ledger=None):
    """`(payload, findings)` — the event this admission WILL append, validated
    to the last rung while the candidate is still in `draft/`.

    Building the record in the validation phase is what makes the write phase a
    plain append: by the time the spec moves there is nothing left that could
    refuse, so the only window a crash can land in is one rename wide."""
    decision, extra, findings = _verdict_request(verdict, candidate["id"], overlaps)
    if findings:
        return None, findings
    if decision == CONFLICT:
        # A conflict ruling is a refusal TO ADMIT, so the transaction stops here
        # and writes nothing: SR-153 says a conflict cancels the candidate or
        # replaces it with a draft, and both of those are moves AWAY from the
        # queue. Recording the ruling is `admission_verdict`'s job, called
        # directly by whoever made it — which also keeps this module's ordering
        # invariant exact (nothing is ever recorded unless the row moved).
        return None, [
            _refuse(
                "{} is ruled {} and cannot be admitted".format(
                    candidate["id"], CONFLICT
                ),
                "a conflict ruling cancels the candidate or replaces it with a "
                "draft that does not collide; record the ruling with "
                "`admission_verdict` and move the spec to cancelled/, never into "
                "the queue it was just ruled out of",
            )
        ]
    extra.setdefault("source", str(candidate["data"].get("source") or "").strip())
    extra.setdefault("declared", _declared_record(candidate["data"]))
    payload, findings = _verdict_payload(
        candidate["id"], decision, scope, spine, overlaps, extra
    )
    if findings:
        return None, findings
    duplicate = _duplicate_finding(root, payload, ledger)
    return (None, [duplicate]) if duplicate else (payload, [])


# --- the migration arm --------------------------------------------------------


def seed(root, ts=None, by="seed", ledger=None):
    """Write a `pre-transaction` verdict for every queued row that has none.

    The one-time migration, and it is `attest.seed`'s shape for `attest.seed`'s
    reason. This repo's queue predates the transaction, so without it the strict
    check would red every legacy row on the day this ships — and a gate that
    reds on arrival teaches its reader to switch it off. It is a MIGRATION, not
    a decision, so it writes `pre-transaction` rather than `no-conflict`: a
    machine cannot adjudicate, and a ledger of machine baselines spelled with an
    adjudicated word is later counted as that many rulings.

    What it deliberately does NOT do is exempt anything. The event carries the
    scope and spine digests measured AT MIGRATION, so a migrated row is still
    subject to the freshness rule: edit its scope or amend the requirement it
    cites and the strict check reds it, and the fix is a real admission. The
    debt is recorded, current, and shrinks by itself.

    A row that already has any admission event is skipped — the migration may
    only ever add a FIRST ruling, never write over one somebody made."""
    root = Path(root)
    ts = ts or _now()
    view = spine_view(root)
    written = []
    for wid, record in sorted(registry(root).items()):
        if record["folder"] != QUEUED_DIR:
            continue
        if latest_admission(root, wid, ledger) is not None:
            continue
        scope, spine = candidate_digests(root, record["text"], view=view)
        event, findings = admission_verdict(
            root,
            wid,
            BASELINE,
            scope,
            spine,
            ts=ts,
            ledger=ledger,
            by=by,
            source=str(record["data"].get("source") or "").strip(),
            declared=_declared_record(record["data"]),
            rationale="queued before the admission transaction existed; digests "
            "measured at migration so the row still expires",
        )
        if event is None:
            return written, findings
        written.append(wid)
    return written, []


# --- the CLI ------------------------------------------------------------------


def _print(lines):
    for line in lines:
        print(line, file=sys.stderr)


def _report_overlaps(root, candidate_path):
    candidate, refusal = _read_candidate(root, candidate_path)
    if refusal:
        _print([refusal])
        return 1
    reg = registry(root)
    findings = overlap_graph(
        [declaration(candidate)],
        _in_folders(reg, ("active",)),
        _in_folders(reg, (QUEUED_DIR,)),
    )
    for finding in findings:
        print("admit: OVERLAP - {}".format(finding["finding"]))
    print("admit: {} overlap finding(s) for {}".format(len(findings), candidate["id"]))
    return 0


def _verdict_from_args(args):
    if args.verdict is None:
        return None
    return {
        "verdict": args.verdict,
        "ordering": list(args.ordering or ()),
        "partition": [group.split(",") for group in (args.partition or ())],
        "cancels": args.cancels or "",
        "replacement": args.replacement or "",
        "by": args.by or "",
        "rationale": args.rationale or "",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("candidate", nargs="?", help="repo-relative path of the draft spec")
    ap.add_argument(
        "--verdict", choices=VERDICTS, help="the adjudicated conflict ruling"
    )
    ap.add_argument(
        "--ordering", action="append", help="an id in the declared run order (repeat)"
    )
    ap.add_argument(
        "--partition",
        action="append",
        help="a comma-separated partition group (repeat)",
    )
    ap.add_argument("--cancels", help="the id this conflict cancels")
    ap.add_argument("--replacement", help="the replacement draft this conflict files")
    ap.add_argument("--by", help="who recorded the ruling")
    ap.add_argument("--rationale", default="", help="the ruling's recorded reasoning")
    ap.add_argument(
        "--overlaps",
        action="store_true",
        help="report the candidate's overlap graph and stop (no move, no record)",
    )
    ap.add_argument(
        "--seed",
        action="store_true",
        help="the one-time migration: a `pre-transaction` verdict per unruled "
        "queued row",
    )
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    if args.seed:
        written, findings = seed(root)
        _print(findings)
        print("admit: seeded {} pre-transaction verdict(s)".format(len(written)))
        return 1 if findings else 0
    if not args.candidate:
        ap.error("give a candidate path, or --seed")
    if args.overlaps:
        return _report_overlaps(root, args.candidate)
    event, findings = admit(root, args.candidate, verdict=_verdict_from_args(args))
    if findings:
        _print(findings)  # every finding, never just the first
        return 1
    print(
        "admit: {} -> {}/{} ({}, event {})".format(
            event["wi"], WORK_DIR, QUEUED_DIR, event["verdict"], event["id"]
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
