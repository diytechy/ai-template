#!/usr/bin/env python3
"""resume_plan.py — the pure resume planner: what does this tree owe next?

Stack-agnostic, standard-library only. This module answers ONE question —
"given this tree, what is the next thing to do?" — and it answers it as a
FUNCTION rather than as a walk through ambient state. That split is the whole
design (plan §9, SR-145):

    snapshot(root)  ->  one frozen record of everything the answer depends on
    plan(snapshot)  ->  one typed Decision, touching no file, spawning nothing

`dispatch.run`'s tick already had a precedence; what it did not have was a
precedence anybody could TEST. Every rung was entangled with the read that fed
it, so proving "a lower rung is never selected while a higher rung has work"
meant standing up a live station with real git repos, real subprocesses and a
real clock — which is why that property was asserted in prose and driven
nowhere. With the read separated from the decision, each rung is a fixture and
the ordering is arithmetic. It also makes SR-145's actual promise true rather
than plausible: two readers of one tree dispatch the same work, because the
decision is a function of the snapshot and of nothing else.

THE PRECEDENCE (plan §9's flowchart, in its order), and what each rung means:

    1. outcomes     an outcome event nobody has adjudicated. First, because
                    every later rung reasons about a spine and a queue that an
                    unadjudicated attempt may still be about to change.
    2. digests      an artifact whose current normative text is not accepted.
                    A successor drafted at rung 1 stays Draft until this rung
                    has established what the spine currently SAYS (plan §9).
    3. drafts       candidates in `docs/work/draft/` awaiting the admission
                    transaction's conflict ruling (SR-152). Rung 1 produces
                    them; only admission moves them into `queued/`.
    4. checkpoint   a human checkpoint or an open final-review request. The
                    typed stop.
    5. spine        current-stage spine work, admitted as ONE exclusive batch
                    whose scope is a connected component (SR-146).
    6. ordinary     other ready work, under the declared parallel/exclusive
                    policy.
    7. remediation  stage 4 (the breakdown is complete and attested) AND the
                    declared bar is red: persist one failure event and draft
                    one repair (SR-147).
    8. drained      nothing is owed.

WHY THE HUMAN STOP SITS AT 4 AND NOT AT THE END. Plan §9's prose says the human
stop "fires only when no unresolved outcome/prose adjudication or PERMITTED
current-level work remains", which reads at first like it belongs after rung 6.
The flowchart puts it before, and the flowchart is right: `permitted` is the
load-bearing word. §A8's premise is that once a ratification is pending no work
may be taken, so work below an open checkpoint is not permitted work that the
stop is jumping ahead of — it is work that is not permitted at all. The two
statements agree once `permitted` is read; they would contradict if the stop
were moved.

ADOPTION IS PRESENCE, NOT ASSUMPTION. Rungs 1-3 read ledgers that a repo may
never have adopted. A repo with no `docs/events/outcomes.jsonl` has not adopted
the outcome contract, and a rung that treated its silence as "nothing pending"
versus "not adopted" would be right by accident. Worse is the other direction:
`attest.detect_candidates` over a repo with no attestation ledger reports EVERY
spine row as unattested, so an ungated rung 2 would stop every existing repo on
its first tick with a queue full of work it was perfectly able to do. So each
of those rungs keys off the LEDGER'S PRESENCE — the same presence-as-consent
shape `docs/agents-enabled` and the admission-verdict rung already use: silent
until the repo has adopted the thing, total from then on.

AN UNREADABLE INPUT IS THE RUNG'S OWN REFUSAL, not a fall-through. A corrupt
outcomes ledger must not read as "no outcomes pending" and let the loop dispatch
rung-6 work past it. `snapshot` records such a failure AGAINST THE RUNG whose
input it was, and `plan` returns that rung with `REFUSE` — so the precedence
fails closed at exactly the height of the damage, and every rung above it still
runs.

WHAT THIS MODULE DOES NOT DO. It never claims another component's fact. Stage 4
is `derive_gate.spine_stage`'s attestation half; the bar's greenness is
`check.py`'s; this module only JOINS them (decisions §3). And `plan` decides
nothing about HOW work runs — the §A8 policy table, the barrier and the merge
slot stay in `dispatch.py`. This module says WHAT is next; that one says how.

Contracts: see docs/mechanized-loop-contracts.md §3 for the symbol map and §5
for the refusal form.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import NamedTuple

MODULE = "resume_plan"

# --- the rungs ---------------------------------------------------------------
# In precedence order. `RANK` turns the order into arithmetic so a test can
# assert "no lower rung while a higher one has work" without restating the list.
OUTCOMES = "outcomes"
DIGESTS = "digests"
DRAFTS = "drafts"
CHECKPOINT = "checkpoint"
SPINE = "spine"
ORDINARY = "ordinary"
REMEDIATION = "remediation"
DRAINED = "drained"

RUNGS = (
    OUTCOMES,
    DIGESTS,
    DRAFTS,
    CHECKPOINT,
    SPINE,
    ORDINARY,
    REMEDIATION,
    DRAINED,
)
RANK = {name: index for index, name in enumerate(RUNGS)}

# The verbs a Decision hands its caller. Two words rather than one boolean per
# rung, for the reason `attest.tier_routing` gives: "recommend" tells a reader
# what happens next where `False` only says what does not.
ADJUDICATE = "adjudicate"  # a machine may enact this judgement
RECOMMEND = "recommend"  # every item at this rung is a human's to decide
VET = "vet"  # run the admission transaction over these candidates
STOP = "stop"  # drain, surface, end the run at 0 — the typed stop
BATCH = "batch"  # admit these ids as one exclusive batch
DISPATCH = "dispatch"  # admit under the declared concurrency policy
REMEDIATE = "remediate"  # mint the failure event, draft the repair
DRAIN = "drain"  # nothing owed
REFUSE = "refuse"  # this rung's input could not be read

# The ledgers whose PRESENCE is a repo's consent to the rung that reads them.
LEDGERS = {
    OUTCOMES: "docs/events/outcomes.jsonl",
    DIGESTS: "docs/events/attestation.jsonl",
    DRAFTS: "docs/events/admissions.jsonl",
    CHECKPOINT: "docs/events/review-requests.jsonl",
}

DRAFT_DIR = "docs/work/draft"
EXAMPLE_PREFIX = "WI-000-"

# The spine registries the trace graph is read from, and the ref cell of each.
# Duplicated small loaders rather than an import of the joined-spine engine, per
# the kit's independently-copyable-script rule (F5).
TRACE_SOURCES = (
    ("docs/requirements/system-requirements.csv", "SR-ID", "SN-Refs"),
    ("docs/requirements/low-level-requirements.csv", "LLR-ID", "SR-Refs"),
    ("docs/test/test-cases.csv", "TC-ID", "Verifies"),
    ("docs/requirements/interfaces.csv", "IF-ID", "SR-Refs"),
)

_REF_SPLIT_RE = re.compile(r"[;,\s]+")


def _refuse(what, why):
    """The contracts §5 refusal line, so every message in this module names the
    offending thing and the reason in one shape."""
    return "{}: REFUSED - {} ({})".format(MODULE, what, why)


# --- the typed records --------------------------------------------------------


class Bar(NamedTuple):
    """One declared-harness result, as the planner needs it.

    Supplied BY the caller, never run here: running a bar is a subprocess, and
    the whole point of the split is that neither `snapshot` nor `plan` has one.
    `tree` is the git tree id the bar was run against, `step` the failing step's
    name and `output` the harness text the fingerprint is derived from — the
    three halves of `outcome.failure_event`'s key."""

    ok: bool
    tree: str = ""
    step: str = ""
    output: str = ""
    gate: str = ""


class Partition(NamedTuple):
    """The answer of `spine_components`: the batches, and why (if at all) the
    proposed partition collapsed to one.

    `reasons` is empty exactly when connectivity alone decided. It is not
    decoration: "these rows form one batch because they are connected" and
    "these rows form one batch because nobody could tell me who owns them" are
    the same tuple of ids and completely different facts, and the second is the
    one a reviewer needs to see."""

    batches: tuple = ()
    reasons: tuple = ()

    @property
    def collapsed(self):
        return bool(self.reasons)


class Snapshot(NamedTuple):
    """Everything `plan` is allowed to depend on, read once and frozen.

    Frozen matters twice. It is what makes `plan` reproducible — two calls over
    one snapshot cannot disagree because there is nothing left to re-read — and
    it is what makes the precedence testable, because a fixture is a literal of
    this shape rather than a directory tree somebody has to build."""

    root: str = ""
    adopted: frozenset = frozenset()
    outcomes: tuple = ()  # {"event", "wi", "outcome", "triggers"}
    digests: tuple = ()  # attest.detect_candidates entries + "decider"
    drafts: tuple = ()  # repo-relative candidate paths
    checkpoint: str = ""  # the block sentence; "" when clear
    spine_ready: tuple = ()  # ready spine-kind rows, as flat declarations
    trace: tuple = ()  # ((spine id, (ids it traces to)), ...) — the declared graph
    ordinary_ready: tuple = ()  # (wi id, kind) for ready non-spine work
    stage: object = None  # derive_gate.spine_stage, or None when unknowable
    gate: str = ""  # the verification gate that stage maps to
    boundary: object = None  # the human ratification boundary in force
    bar: object = None  # a Bar, or None when no bar result is in hand
    findings: tuple = ()  # (rung, message) — an input that would not read


class Decision(NamedTuple):
    """ONE answer. `rung` says which precedence rung was selected, `action` what
    the caller should do, `items` the ids/paths it applies to, `reason` the
    sentence a reader sees in the log."""

    rung: str
    action: str
    items: tuple = ()
    reason: str = ""

    @property
    def rank(self):
        """The rung's position in the declared precedence. Derived, so a test
        asserting "no lower rung while a higher has work" compares numbers
        rather than re-listing the order and drifting from it."""
        return RANK[self.rung]


# --- LLR-170: the connected-component partition -------------------------------


def _ref_tokens(*values):
    """A frozenset of ids out of whatever shape a declaration carries them in.

    A spec's TOML frontmatter holds lists; a registry cell holds a `;`-separated
    string; a hand-written frontmatter may hold a bare string. All three name the
    same rows, so all three normalise to the same tokens — otherwise the graph's
    edges would depend on which reader filled the record. A `~` soft-predecessor
    prefix is stripped for the same reason `admit._tokens` strips it: an advisory
    ordering hint still names the row."""
    out = set()
    for value in values:
        if value is None:
            continue
        items = [value] if isinstance(value, str) else value
        if not isinstance(items, (list, tuple, set, frozenset)):
            continue
        for item in items:
            for token in _REF_SPLIT_RE.split(str(item).strip()):
                token = token.lstrip("~").strip()
                if token:
                    out.add(token)
    return frozenset(out)


def _row_view(row):
    """One candidate row as `(id, refs, interfaces, components)`.

    Accepts the flat declaration shape `admit.declaration` produces (a spec's
    frontmatter with `id` filled in) so the planner and the admission
    transaction read one record rather than two."""
    row = row or {}
    return (
        str(row.get("id") or "").strip(),
        _ref_tokens(row.get("sr_refs"), row.get("refs"), row.get("spine_refs")),
        _ref_tokens(row.get("interfaces")),
        _ref_tokens(row.get("components"), row.get("component")),
    )


class _Union:
    """The smallest union-find that does the job. Path-compressed only; the
    graphs here are one queue's worth of rows, so the second optimisation would
    be cost with no measurement behind it."""

    def __init__(self):
        self.parent = {}

    def find(self, item):
        self.parent.setdefault(item, item)
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != root:
            self.parent[item], item = root, self.parent[item]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def spine_components(rows, trace=None):
    """LLR-170 — partition candidate spine rows into independently admissible
    batches. Returns a `Partition`.

    THE GRAPH. Each row contributes its own id, the spine ids it references, and
    the interfaces it declares; a row is unioned with each of those tokens, so
    two rows citing one requirement, or declaring one seam, land in one
    component. `trace` adds the DECLARED trace edges between spine ids
    themselves — what `trace_edges` reads out of the registries — so a row
    touching `LLR-155` and a row touching the `SR-140` it decomposes are
    connected even though neither cites the other. It is accepted as a mapping
    (`{id: [ids]}`) or as a sequence of pairs, because a `Snapshot` carries it
    as pairs (a frozen record holds no dict) and a caller holding registries
    holds a mapping; refusing one of the two would only move a conversion to
    every call site.

    THE COLLAPSE, and why it is this way round. The *proposed* partition is by
    declared owning component; connectivity either confirms it or destroys it.
    Two things collapse the whole thing to ONE project-wide batch:

      * **a row with no declared owner.** Nothing says which partition it
        belongs to, so every partition that excludes it is a guess. Guessing
        wrong ships an unreviewed composition; collapsing costs one exclusive
        batch that would have been exclusive anyway.
      * **an edge that crosses the proposed partition** — two rows in one
        connected component declaring disjoint owning components. That is
        precisely the state SR-146 names: the ownership boundary claims they are
        independent and the graph says they are not.

    Both fail toward the single batch, and the direction is the requirement, not
    a convenience. Splitting wrongly lets two batches amend rows that reference
    each other and the composition is reviewed by nobody; collapsing wrongly
    costs throughput and is visible in the log. The criterion is connectivity —
    never size — for the same reason: size is a throttle (`admission.
    max_batch_size`), and a throttle that decided independence would be a
    correctness rule set by a performance dial.

    Pure, and deliberately so: it is called from `plan`."""
    views = [_row_view(row) for row in (rows or ())]
    reasons = []
    named = []
    for rid, refs, ifaces, comps in views:
        if not rid:
            reasons.append(
                _refuse(
                    "a candidate row declares no id",
                    "a row nobody can name cannot be placed in a batch, so the "
                    "safe partition is the one that assumes it touches "
                    "everything",
                )
            )
            continue
        if not comps:
            reasons.append(
                _refuse(
                    "{} declares no owning component".format(rid),
                    "missing ownership collapses to one project-wide spine "
                    "batch: an unowned row cannot be excluded from a partition "
                    "without guessing",
                )
            )
        named.append((rid, refs, ifaces, comps))

    union = _Union()
    for rid, refs, ifaces, _comps in named:
        union.find(rid)
        for token in refs | ifaces:
            union.union(rid, token)
    edges = trace or ()
    for source, targets in edges.items() if hasattr(edges, "items") else edges:
        for target in _ref_tokens(targets):
            union.union(str(source).strip(), target)

    groups = {}
    for rid, _refs, _ifaces, comps in named:
        groups.setdefault(union.find(rid), []).append((rid, comps))
    for members in groups.values():
        owners = [comps for _rid, comps in members if comps]
        for index, left in enumerate(owners):
            for right in owners[index + 1 :]:
                if not (left & right):
                    reasons.append(
                        _refuse(
                            "a declared edge joins components {} and {}".format(
                                ", ".join(sorted(left)), ", ".join(sorted(right))
                            ),
                            "an edge crossing the proposed partition means the "
                            "partition's independence claim is false, so the "
                            "work collapses to one project-wide spine batch",
                        )
                    )
    reasons = tuple(dict.fromkeys(reasons))
    ids = sorted(rid for rid, _r, _i, _c in named)
    if not ids:
        return Partition((), reasons)
    if reasons:
        return Partition((tuple(ids),), reasons)
    batches = sorted(
        tuple(sorted(rid for rid, _c in members)) for members in groups.values()
    )
    return Partition(tuple(batches), ())


# --- LLR-168: the pure decision ----------------------------------------------


def _finding_stop(snapshot, rung):
    """The refusal Decision for a rung whose input would not read, or None.

    Checked at each rung IN TURN rather than up front, so the damage stops the
    precedence at exactly its own height: an unreadable outcomes ledger must not
    let rung 6 dispatch work, and an unreadable draft folder must not hide an
    outcome that rung 1 can still act on."""
    hits = tuple(msg for where, msg in snapshot.findings if where == rung)
    if not hits:
        return None
    return Decision(
        rung,
        REFUSE,
        hits,
        "the {} rung's input could not be read, so the loop stops here rather "
        "than reading its silence as 'nothing pending'".format(rung),
    )


def plan(snapshot):
    """LLR-168 — the whole precedence, as one pure function over one snapshot.

    TOUCHES NO FILE AND SPAWNS NO PROCESS, and that is a property, not a style
    note: it is what lets every rung be driven by a literal, and it is what makes
    two readers of one tree agree. Nothing below imports (a deferred import is a
    file read), reads a clock, or asks the filesystem anything — every fact it
    needs was frozen by `snapshot`, including the ones that would otherwise need
    a sibling module's pure helper (a digest candidate's decider is annotated at
    read time for exactly that reason).

    The rungs are the module docstring's, in that order. A lower rung is
    unreachable while a higher one has work, by construction: each returns."""
    for rung in RUNGS:
        stop = _finding_stop(snapshot, rung)
        if stop is not None:
            return stop
        if rung == OUTCOMES and snapshot.outcomes:
            events = tuple(str(o.get("event") or "") for o in snapshot.outcomes)
            return Decision(
                OUTCOMES,
                ADJUDICATE,
                events,
                "{} worker outcome(s) await adjudication ({}); a successor "
                "drafted here stays Draft until the spine and the queue have "
                "ruled".format(
                    len(events),
                    ", ".join(
                        "{} {}".format(
                            o.get("wi") or "?", "/".join(o.get("triggers") or ())
                        )
                        for o in snapshot.outcomes
                    ),
                ),
            )
        if rung == DIGESTS and snapshot.digests:
            ids = tuple(str(c.get("id") or "") for c in snapshot.digests)
            human = [c for c in snapshot.digests if c.get("decider") == "human"]
            machine = len(ids) - len(human)
            return Decision(
                DIGESTS,
                ADJUDICATE if machine else RECOMMEND,
                ids,
                "{} artifact(s) carry normative text nobody has accepted "
                "({} inside the human ratification boundary, {} an adjudicator "
                "may enact)".format(len(ids), len(human), machine),
            )
        if rung == DRAFTS and snapshot.drafts:
            return Decision(
                DRAFTS,
                VET,
                tuple(snapshot.drafts),
                "{} draft candidate(s) await the admission transaction; only "
                "admission moves a candidate into queued/".format(len(snapshot.drafts)),
            )
        if rung == CHECKPOINT and snapshot.checkpoint:
            return Decision(
                CHECKPOINT,
                STOP,
                (snapshot.checkpoint,),
                "a human checkpoint is due: " + snapshot.checkpoint,
            )
        if rung == SPINE and snapshot.spine_ready:
            partition = spine_components(snapshot.spine_ready, snapshot.trace)
            batch = partition.batches[0] if partition.batches else ()
            return Decision(
                SPINE,
                BATCH,
                batch,
                "current-stage spine work: {} of {} batch(es){}".format(
                    len(batch),
                    len(partition.batches),
                    "; collapsed to one project-wide batch — " + partition.reasons[0]
                    if partition.collapsed
                    else "",
                ),
            )
        if rung == ORDINARY and snapshot.ordinary_ready:
            ids = tuple(str(w) for w, _k in snapshot.ordinary_ready)
            return Decision(
                ORDINARY,
                DISPATCH,
                ids,
                "{} ready non-spine row(s) under the declared concurrency "
                "policy".format(len(ids)),
            )
        if rung == REMEDIATION and _red_bar(snapshot):
            return Decision(
                REMEDIATION,
                REMEDIATE,
                (snapshot.bar.step,),
                "the breakdown is complete and attested (stage 4) and the "
                "declared {} bar is red at step {!r}: one failure event, one "
                "repair draft".format(snapshot.gate or "?", snapshot.bar.step),
            )
    return Decision(
        DRAINED,
        DRAIN,
        (),
        "nothing is owed: no unadjudicated outcome, no unaccepted normative "
        "text, no draft awaiting admission, no checkpoint, no ready work and "
        "no red declared bar",
    )


def _red_bar(snapshot):
    """The stage-4-AND-red join, in one place (decisions §3).

    Neither half is guessed from the other: stage 4 is the attestation fact
    `derive_gate.spine_stage` owns, red is the harness fact `check.py` owns, and
    this is the only line in the program that reads them together. A snapshot
    holding no bar result answers False — "we did not look" is not "it is
    green"."""
    bar = snapshot.bar
    return snapshot.stage == 4 and bar is not None and not bar.ok


# --- LLR-169: the snapshot reader ---------------------------------------------


def _load_csv(path):
    """One registry CSV as dict rows; `[]` when absent. `utf-8-sig` because a
    BOM'd registry is the realistic Excel round-trip on a Windows-first kit, and
    a BOM glued to the first column name hides every row."""
    path = Path(path)
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def trace_edges(root):
    """`{id: [ids it traces to]}` for the declared spine and interface graph.

    Read off the registries' own ref cells — an SR's `SN-Refs`, an LLR's
    `SR-Refs`, a TC's `Verifies`, an IF row's `SR-Refs` — so the edges the
    partition uses are the edges the registries declare, not a second graph
    somebody maintains beside them. Missing files contribute nothing, which is
    the non-adopter posture every loader in this kit takes."""
    root = Path(root)
    edges = {}
    for rel, id_column, ref_column in TRACE_SOURCES:
        for row in _load_csv(root / rel):
            rid = (row.get(id_column) or "").strip()
            if not rid or rid.endswith("-000"):
                continue
            targets = _ref_tokens(row.get(ref_column))
            if targets:
                edges.setdefault(rid, set()).update(targets)
    return {rid: sorted(targets) for rid, targets in edges.items()}


def _adopted(root):
    """The rungs whose ledger this repo has actually adopted (module docstring:
    presence is consent)."""
    root = Path(root)
    return frozenset(rung for rung, rel in LEDGERS.items() if (root / rel).is_file())


def _pending_outcomes(root, registry, config, findings):
    """Outcome events with no disposition that `adjudicate.needs_adjudication`
    says a dedicated adjudicator owes an answer on.

    The trigger set is P7's, not a second policy: Partial and Cancelled always,
    Complete only on the declared risk/sampling triggers. Re-deriving "which
    outcomes are pending" here would be a second opinion about the one thing
    that module exists to rule on."""
    import adjudicate

    try:
        events = adjudicate.read_events(Path(root) / adjudicate.OUTCOMES_LEDGER)
    except (OSError, ValueError) as exc:
        findings.append((OUTCOMES, str(exc)))
        return ()
    ruled = {e.get("outcome_event") for e in events if e.get("kind") == "disposition"}
    out = []
    for event in events:
        if event.get("kind") != "outcome" or event.get("id") in ruled:
            continue
        record = registry.get(event.get("wi") or "") or {}
        triggers = adjudicate.needs_adjudication(
            event, record.get("data") or {}, config
        )
        if not triggers:
            continue
        out.append(
            {
                "event": event.get("id"),
                "wi": event.get("wi"),
                "outcome": event.get("outcome"),
                "triggers": tuple(triggers),
            }
        )
    return tuple(out)


def _digest_candidates(root, docs, findings):
    """`attest.detect_candidates`, annotated per candidate with WHO may decide.

    The annotation is done HERE, at read time, because `plan` must stay pure:
    `attest.requires_human` is itself pure, but reaching it from `plan` would
    mean a deferred import, and an import is a file read. One line moved is the
    whole cost of keeping the decision provably offline."""
    import attest

    try:
        boundary = attest.boundary_from_config(root)
        candidates = attest.detect_candidates(root, docs)
    except (OSError, ValueError) as exc:
        findings.append((DIGESTS, str(exc)))
        return (), None
    out = []
    for candidate in candidates:
        index = attest.TIER_INDEX.get(candidate.get("kind"), 0)
        try:
            human = attest.requires_human(index, boundary)
        except ValueError as exc:
            findings.append((DIGESTS, str(exc)))
            human = True  # a boundary nobody could read never auto-enacts
        out.append(dict(candidate, decider="human" if human else "adjudicator"))
    return tuple(out), boundary


def _draft_candidates(root, findings):
    """The candidate specs sitting in `docs/work/draft/`, repo-relative.

    The inert `WI-000-` exemplar is skipped, exactly as every other reader in
    this kit skips it — a scaffold must read as vacuously drained, not as one
    candidate short of a vetting round."""
    folder = Path(root) / DRAFT_DIR
    if not folder.is_dir():
        return ()
    try:
        names = sorted(
            p.name
            for p in folder.glob("WI-*.md")
            if not p.name.startswith(EXAMPLE_PREFIX)
        )
    except OSError as exc:
        findings.append((DRAFTS, str(exc)))
        return ()
    return tuple(DRAFT_DIR + "/" + name for name in names)


def _checkpoint(root, findings):
    """The sentence naming why a human checkpoint is due, or `""`.

    ONE source, `attest.full_spine_block`, which already joins the persistent
    policy and any open one-shot request. Reassembling that sentence here would
    be a second home for the thing a blocked checkpoint prints, and two homes is
    how a gate and its explanation drift into disagreeing.

    Pending human-tier ratifications are deliberately NOT a second trigger: they
    are rung 2's population, and counting them here as well would make this rung
    fire on every tree rung 2 already stopped, so it could never be reached on
    its own."""
    import attest

    try:
        _boundary, policy, refusals = attest.attestation_config(root)
        if refusals:
            findings.append((CHECKPOINT, refusals[0]))
            return ""
        return attest.full_spine_block(root, policy) or ""
    except (OSError, ValueError) as exc:
        findings.append((CHECKPOINT, str(exc)))
        return ""


def _ready_work(root, registry, findings):
    """`(spine rows, other ready rows)` off the SAME frontier `dispatch` admits
    from — `schedule.frontier` over the spec folder, queued rows only.

    The spine rows come back as flat DECLARATIONS (`admit.declaration`), not as
    scheduler records, because `spine_components` needs the cells the scheduler
    does not carry: the declared components and interfaces. One join, read from
    the spec frontmatter that already holds them."""
    import schedule

    try:
        wis = schedule._load(root)
    except (OSError, ValueError) as exc:
        findings.append((SPINE, str(exc)))
        return (), ()
    kinds = {w["id"]: schedule.kind_of(w) for w in wis}
    ready = [r for r in schedule.frontier(wis) if r["status"] == "queued"]
    spine, other = [], []
    for row in ready:
        wid = row["id"]
        kind = kinds.get(wid)
        if kind == "spine":
            record = registry.get(wid)
            declaration = dict(record.get("data") or {}) if record else {}
            declaration["id"] = wid
            spine.append(declaration)
        else:
            other.append((wid, kind))
    return tuple(spine), tuple(other)


def _stage_and_gate(docs, findings):
    """`(spine_stage, verification_gate)` — the two derived axes, joined by the
    declared mapping and never inferred one from the other (decisions §2.3)."""
    import derive_gate

    try:
        stage = derive_gate.spine_stage(docs)
    except (OSError, ValueError) as exc:
        findings.append((REMEDIATION, str(exc)))
        return None, ""
    if stage is None:
        return None, ""
    try:
        return stage, derive_gate.verification_gate_for(stage)
    except ValueError as exc:
        findings.append((REMEDIATION, str(exc)))
        return stage, ""


def snapshot(root, *, docs=None, bar=None, config=None):
    """LLR-169 — every input the decision depends on, read once, returned frozen.

    Separating this from `plan` is what makes the decision pure, and the split
    pays twice: the reads happen once per cycle instead of once per rung, and a
    test of the precedence needs no tree at all.

    `bar` is the caller's declared-harness result (a `Bar`) or None. It is an
    argument rather than something read here because running a bar is a
    subprocess and this function does not own one; a snapshot with no bar simply
    cannot select the remediation rung, which is the honest reading of "we did
    not look".

    Every read is caught and recorded AGAINST ITS RUNG rather than raised: one
    unreadable ledger must cost the loop that rung, loudly, and not the whole
    cycle. Rungs 1-3 additionally read nothing at all until their ledger exists
    (module docstring: presence is consent)."""
    root = Path(root)
    docs = Path(docs) if docs else root / "docs"
    findings = []
    adopted = _adopted(root)

    import admit

    try:
        registry = admit.registry(root)
    except (OSError, ValueError) as exc:
        findings.append((OUTCOMES, str(exc)))
        registry = {}

    outcomes = (
        _pending_outcomes(root, registry, config, findings)
        if OUTCOMES in adopted
        else ()
    )
    digests, boundary = (
        _digest_candidates(root, docs, findings) if DIGESTS in adopted else ((), None)
    )
    drafts = _draft_candidates(root, findings) if DRAFTS in adopted else ()
    checkpoint = _checkpoint(root, findings) if CHECKPOINT in adopted else ""
    spine_ready, ordinary_ready = _ready_work(root, registry, findings)
    stage, gate = _stage_and_gate(docs, findings)
    # Read only when there is spine work to partition, and carried as PAIRS: a
    # frozen record holds no dict, and reading the four registries on every
    # idle tick to build a graph nothing will ask about is pure cost.
    try:
        trace = tuple(sorted(trace_edges(root).items())) if spine_ready else ()
    except (OSError, ValueError) as exc:
        findings.append((SPINE, str(exc)))
        trace = ()
    return Snapshot(
        root=str(root),
        adopted=adopted,
        outcomes=outcomes,
        digests=digests,
        drafts=drafts,
        checkpoint=checkpoint,
        spine_ready=spine_ready,
        trace=trace,
        ordinary_ready=ordinary_ready,
        stage=stage,
        gate=gate,
        boundary=boundary,
        bar=bar if isinstance(bar, Bar) else None,
        findings=tuple(findings),
    )


# --- SR-147: the exactly-once remediation rung --------------------------------


class Remediation(NamedTuple):
    """What the red-bar rung did: the failure event's id, the repair candidate's
    path (None when one already existed), and every refusal on the way."""

    event: str = ""
    draft: object = None
    findings: tuple = ()


def _existing_failure(root, bar, ledger=None):
    """The bar-failure event already recorded for this `(tree, step,
    fingerprint)` key, or None.

    Looked up by KEY rather than by catching `failure_event`'s refusal string,
    and the difference is a real recovery case: a cycle that minted the event
    and then died before drafting must, on its next pass, find that event and
    draft from it. Parsing an id back out of a refusal sentence would make that
    recovery depend on the wording of a message."""
    import outcome

    path = Path(ledger) if ledger else Path(root) / outcome.FAILURES_LEDGER
    fingerprint = outcome.failure_fingerprint(root, bar.output)
    for event in outcome.read_events(path):
        if (
            event.get("kind") == "bar-failure"
            and event.get("tree") == bar.tree
            and event.get("step") == bar.step
            and event.get("fingerprint") == fingerprint
        ):
            return event
    return None


def remediate(root, bar, *, effort="", ledger=None, work=None, **cells):
    """SR-147 — persist the ONE failure event for a red declared bar and draft
    the ONE repair candidate for it. Returns a `Remediation`.

    This is the rung's ENACTMENT and it is deliberately not in `plan`: it
    writes. `plan` selects it; this performs it.

    EXACTLY-ONCE IS THE IDENTITY, not a dedup pass. `outcome.failure_event` keys
    the event by tree, failing step and normalised fingerprint, so ten cycles
    watching one defect mint one event; `adjudicate.draft_remediation` keys the
    candidate by that event's id, so one event drafts one candidate. Both halves
    already refuse a second write by name (LLR-171, LLR-186) — this function
    composes them and adds nothing, which is the point: a third dedup rule here
    would be a third place for "how many is one" to be answered differently.

    A repeat therefore returns `draft=None` and the refusals that say which row
    already carries it; a different failing step or a different fingerprint is a
    different key and drafts its own. `effort`, `buildtier` and `planmode` are
    the ADJUDICATED estimate, passed through untouched — nothing here judges."""
    import adjudicate
    import outcome

    # Checked by DECLARED FIELDS, not by `isinstance`. The key is read off
    # `ok`/`tree`/`step`/`output`/`gate`, so those are what a result has to
    # carry; a class check would additionally refuse a `Bar` handed over from a
    # differently-imported copy of this module, which is a fact about import
    # machinery and not about the failure. A mapping fails it — `{"ok": False}`
    # has no `.ok` — which is the shape this rung actually has to refuse.
    if not all(hasattr(bar, name) for name in Bar._fields):
        return Remediation(
            "",
            None,
            (
                _refuse(
                    "the bar result {!r} does not carry the declared bar fields "
                    "({})".format(type(bar).__name__, ", ".join(Bar._fields)),
                    "the failure key is read off those fields, so an untyped "
                    "result would key the event on whatever it happened to carry",
                ),
            ),
        )
    if bar.ok:
        return Remediation(
            "",
            None,
            (
                _refuse(
                    "the declared bar is GREEN",
                    "a remediation event asserts a failure; minting one from a "
                    "pass would put a defect nobody observed in the queue",
                ),
            ),
        )
    try:
        event = _existing_failure(root, bar, ledger=ledger)
    except (OSError, ValueError) as exc:
        return Remediation("", None, (str(exc),))
    findings = []
    if event is None:
        event, mint_findings = outcome.failure_event(
            root, bar.tree, bar.step, bar.output, gate=bar.gate, ledger=ledger
        )
        if event is None:
            return Remediation("", None, tuple(mint_findings))
        findings.extend(mint_findings)
    kwargs = dict(cells)
    if work is not None:
        kwargs["work"] = work
    if ledger is not None:
        kwargs["ledger"] = ledger
    draft, draft_findings = adjudicate.draft_remediation(
        root, event["id"], effort=effort, **kwargs
    )
    return Remediation(event["id"], draft, tuple(findings) + tuple(draft_findings))
