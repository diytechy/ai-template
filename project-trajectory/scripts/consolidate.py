#!/usr/bin/env python3
"""consolidate.py — the CONSOLIDATION census: which queued rows are one work
item wearing several ids, and the guard that stops the question being asked
twice.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

WHY THIS MODULE EXISTS (the 2026-09-02 backlog-restructure plan §1). A queue
accumulates overlap on its own: rows cut from one plan, rows commissioned by one
ruling, rows that edit the same module from two directions. `check_trajectory.
queue_conflict_findings` has reported that overlap as a warn since LLR-160 and
nothing ever acted on it — the `adjudicate-conflict` brief that was supposed to
was never minted, never assembled and never read. This module is the producer
that turns the warn into a judgement: a census over the QUEUED rows that mints
ONE `consolidate` adjudication row over the overlapping cluster, whose verdict
may absorb several rows into one successor.

IT IS ITS OWN MODULE, not a widening of `intake`, for two reasons the plan
states and one this file adds. The plan's: consolidation is the only judgement
that CLOSES ROWS IT WAS NOT MINTED FROM, and it is built as its own function set
rather than by widening `disposition`. This file's: `intake.py` is the largest
module under the size ratchet, and the census's decision half — digests,
clusters, guards — is testable with no repository at all, which the mint half
is not.

THE THREE GUARDS, and why a census needs guards a merge hook does not. A mint at
merge fires on an event; a census fires on a STATE, so it will fire again on the
next tick unless something remembers. All three are read off typed cells:

  1. **Never stack a judgement.** `_pending_refusal`: no row is minted while any
     adjudication row is queued or active. A consolidation must not judge a row a
     lane is holding, and two judgements in the frontier at once is the shape the
     scheduler's rank-1 exclusivity exists to avoid.
  2. **A judged queue state is never judged again.** `_judged_refusal`: the
     minted row carries `Digests` — the queue sha and the spine sha it saw — and
     a `consolidate` row carrying THIS queue sha, in ANY status including the
     archived terminals, refuses the mint. The archived half is the load-bearing
     one: a guard that stops holding when the row closes mints the same
     judgement forever.
  3. **A consolidation does not re-litigate its own output.** A successor is
     recognisable from the registry alone — it is a row whose `Supersedes` names
     a `restructured` row, and only a consolidation close files a row there — so
     `_seed_pairs` drops any pair involving one. Its successors still reach the
     brief (as open rows, and as `{prior}`), because a cluster formed for other
     reasons may legitimately contain one; what they never do is SEED a cluster.
     Re-absorbing one is refused outright at the mint (`reabsorption_refusal`),
     which is the RETURN-TO-DRAFT-that-pages-the-owner the plan asks for: the
     judgement to overturn is the earlier consolidation's, and that is a human's
     call, not a second machine mint.

ONE ROW PER CENSUS, over the UNION of every candidate cluster. Two disjoint
overlapping pairs are still one question — "which of these are the same work
item?" — asked of one judge with the whole picture, and guard 1 means a second
row could not run beside the first anyway. The plan's acceptance (§4) reads the
same way: five rows with two overlapping pairs mint exactly ONE row.

THE DECISION AND NOT THE EFFECT. `census_draft` answers "what would this census
mint", and NOTHING here writes a spec or allocates an id: the mint arm is
`intake.mint_consolidation`, beside its `mint_gap_rows` sibling, because
`intake._mint` is the one allocator of a WI id (ruling R1) and the import arrow
between these two modules must run one way. It ran BOTH ways for one commit —
`intake` importing this module for its refusal, this module reaching back for
`_mint` — and `tests/test_import_layers.py` reported the cycle, correctly.

THE CONTRACT, stated here because no interface row owns this seam yet:
`census_draft(root, rows=None)` returns `(draft, None)` for the row this census
would mint, or `(None, reason)` — a reason and not an exception for every
"nothing to do" arm, because an idle station with no overlap is the healthy
case. Every input is a typed registry cell — `Status`, `Brief`, `Digests`,
`Supersedes`, `SR-Refs`, `SpecRef` — or a spec body read off disk; never a prior
verdict, so the census is reproducible from the tree alone.
"""

from __future__ import annotations

import hashlib
import re
import tomllib
from pathlib import Path

import agent_common as ac
import spec_move
import spine_carrier
from kitlib import registry as kitregistry

WORK = "docs/work"
#: Terminal history's home since WI-504 — the archive half of the one registry
#: `read_spec_rows` unions.
ARCHIVE_WORK = "docs/archive/work"
#: The `Brief` cell the census mints, and the one the guards look for.
BRIEF = "consolidate"
#: The spec-of-record a minted row points at, as ORDERED EXISTENCE PROBES —
#: first one that resolves to a FILE wins. The queue IS the subject, so the
#: forward bridge (R-E) resolves to the document defining what the queue's
#: statuses mean; the SR registry is the fallback every repo with a spine has,
#: and is the same fallback `intake._census_specref` takes.
#:
#: PROBES AND NOT A LITERAL, because `integrate.claim` REFUSES a row whose
#: SpecRef does not resolve to an in-repo file (R-E, WI-370). A hard
#: `docs/work/README.md` on a repo that does not ship it mints a judgement that
#: can never be claimed, `_judgement_first` puts it at the head of the frontier,
#: and the run exits 1 on every tick from then on — the queue wedged by the
#: census that was supposed to unblock it. Measured the moment the census was
#: wired into `dispatch._admit` (2026-09-04), on a fixture repo with no
#: `docs/work/README.md`.
SPECREF_PROBES = (
    "docs/work/README.md",
    "docs/requirements/system-requirements.toml",
    "docs/requirements/system-requirements.csv",
)
#: `priority = 9` (plan §1.3 clause 4): the frontier sorts `Priority` desc inside
#: a rank, and `dispatch._judgement_first` already puts judgements first, so this
#: needs no rank-table change to run ahead of the rows it is judging.
PRIORITY = 9
#: Consolidation is design-shaping by construction — it moves scope between rows
#: and closes some of them — so the tier is declared, not estimated from breadth.
BUILDTIER = "strong"

#: The registries the spine sha covers, in this fixed order.
SPINE_REGISTRIES = (
    "docs/requirements/system-requirements.toml",
    "docs/requirements/low-level-requirements.toml",
    "docs/test/test-cases.toml",
)
LLR_REGISTRY = "docs/requirements/low-level-requirements.toml"

#: Statuses a row occupies while it is still somebody's to run.
OPEN_STATUSES = frozenset({"draft", "queued", "active", "deferred"})
QUEUED = "queued"
RESTRUCTURED = "restructured"

#: How many hex characters of each sha the cell carries. Twelve is the same
#: width `gen_prompt_catalog` publishes: long enough that a collision is not a
#: practical concern for a per-repo queue, short enough that the cell stays
#: readable in a registry row a human is scanning.
DIGEST_CHARS = 12
#: The cell's shape: `<queue sha>|<spine sha>`.
DIGEST_SEP = "|"

#: A module path named in a row's own prose. Anchored on the extension so a
#: sentence mentioning `intake` does not count and `project-trajectory/scripts/
#: intake.py` does. Deliberately narrow: this signal feeds a judge, and a
#: pre-filter that fires on everything selects nothing.
_MODULE_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.py\b")
#: Clip on one rendered finding, so a cluster of near-duplicate titles cannot
#: produce a mint context nobody reads.
_LINE_CLIP = 200


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:DIGEST_CHARS]


def _cell(row, name):
    return (row.get(name) or "").strip()


def read_rows(root):
    """The whole work-item registry — `docs/work/` unioned with its archive
    sibling, which is what `read_spec_rows` already means by one registry. The
    guards need the terminal rows (an ARCHIVED consolidation still holds its
    queue sha), so nothing here may read the active workspace alone."""
    return ac.read_spec_rows(Path(root) / WORK)


def queued_rows(rows):
    return [r for r in rows if _cell(r, "Status") == QUEUED]


def queue_digest(rows):
    """The sha of the QUEUE STATE: sorted `(id, title, needs, safety_class)`
    over the `queued/` rows (plan §1.3).

    FOUR FIELDS AND NOT THE WHOLE ROW, deliberately. The question a
    consolidation answers is "are these the same work item, and may they run
    together" — which is decided by what each row is (title), what it waits on
    (needs) and how it must be scheduled (safety_class). A row whose Deliverable
    or BuildTier was edited is the SAME queue question, and hashing those would
    re-arm the census on an edit that changes no answer. Sorted, so the digest
    is a property of the set and not of directory order."""
    keyed = sorted(
        (
            _cell(r, "WI-ID"),
            _cell(r, "Title"),
            _cell(r, "Predecessors"),
            _cell(r, "SafetyClass"),
        )
        for r in queued_rows(rows)
    )
    return _sha("\n".join("\x1f".join(parts) for parts in keyed))


def spine_digest(root):
    """The sha of the three spine registries as they are on disk.

    Whichever carrier is live (`spine_carrier.resolve`), and a registry that is
    ABSENT hashes as the empty string rather than being skipped — a repo that
    gains its first LLR registry has moved the spine, and the verdict recorded
    against the old pair should read as stale."""
    parts = []
    for rel in SPINE_REGISTRIES:
        live = spine_carrier.resolve(Path(root) / rel, spine_carrier.CARRIERS)
        try:
            parts.append(live.read_text(encoding="utf-8") if live else "")
        except (OSError, UnicodeDecodeError):
            parts.append("")
    return _sha("\x1e".join(parts))


def digests(root, rows):
    """The `Digests` cell: `<queue sha>|<spine sha>`."""
    return queue_digest(rows) + DIGEST_SEP + spine_digest(root)


def parse_digests(cell):
    """`(queue_sha, spine_sha)` from a `Digests` cell; `("", "")` when the cell
    is empty or malformed. A malformed cell reads as NO recorded digest, so the
    guard it feeds fails OPEN into "this state has not been judged" — which is
    the safe direction here: the alternative is a typo'd cell that silences the
    census forever."""
    queue, sep, spine = str(cell or "").strip().partition(DIGEST_SEP)
    if not sep or not queue.strip() or not spine.strip():
        return "", ""
    return queue.strip(), spine.strip()


# --- who is a consolidation, and who a consolidation minted --------------------


def consolidations(rows):
    """Every row whose declared `Brief` is `consolidate`, whatever its status."""
    return [r for r in rows if _cell(r, "Brief").lower() == BRIEF]


def _superseded(row):
    return {tok.strip() for tok in _cell(row, "Supersedes").split(";") if tok.strip()}


def consolidation_successors(rows):
    """The ids of rows a consolidation MINTED — read from the registry, not
    remembered.

    A successor is a row whose `Supersedes` names a `restructured` row, and that
    is exact rather than heuristic: `restructured/` is the one terminal folder a
    lane may not close into, so only a consolidation close (or a hand trunk
    commit standing in for one) puts a row there. Counting `len(Supersedes) > 1`
    instead would have been a guess — a disposition names one predecessor and a
    consolidation that absorbed exactly one row would be invisible."""
    absorbed = {_cell(r, "WI-ID") for r in rows if _cell(r, "Status") == RESTRUCTURED}
    return {
        _cell(r, "WI-ID")
        for r in rows
        if absorbed & _superseded(r) and _cell(r, "WI-ID")
    }


def prior_absorbs(rows):
    """`{consolidation id: [absorbed ids]}` for every consolidation that has
    already run — the `{prior}` evidence (plan §1.4).

    Derived from the ABSORBED rows' own status and lineage rather than from any
    verdict file: a verdict is a claim, the registry is the record, and rule 1
    of `adjudicate_brief` says a judge's evidence comes from the second."""
    out = {}
    for row in rows:
        if _cell(row, "Status") != RESTRUCTURED:
            continue
        for successor in sorted(_superseded(row)):
            out.setdefault(successor, [])
            wid = _cell(row, "WI-ID")
            if wid and wid not in out[successor]:
                out[successor].append(wid)
    return {succ: sorted(ids) for succ, ids in out.items()}


# --- the two signals the mechanical pre-filter does not carry ------------------


def _commissioning_docs(row):
    """What COMMISSIONED this row: its spec-of-record document (anchor stripped)
    and every open-item id it hard-waits on.

    The second half is what `queue_conflict_findings`' shared-`SpecRef` signal
    cannot see. Two rows cut from one ruling routinely carry different specrefs
    — one points at the plan, one at the open-items registry — while the thing
    that makes them one question is the OI id they both wait on."""
    docs = set()
    spec = _cell(row, "SpecRef").split("#", 1)[0].strip()
    if spec:
        docs.add(spec)
    for token in _cell(row, "Predecessors").split(";"):
        token = token.strip().lstrip("~")
        if token.startswith("OI-"):
            docs.add(token)
    return docs


def spec_bodies(root):
    """`{wi id: body text}` for every spec in the registry's two roots.

    The census's module signal is declared to read each row's Context and
    Done-when (plan §1.3), and those live in the spec BODY, which
    `read_spec_rows` does not carry (it carries cells). Read once per census and
    passed down, so the pairwise loop does not re-open every file.

    Through `agent_common`'s re-exports rather than `kitlib.registry` directly:
    the shared reader is already imported here, and a second import of the same
    thing under a second name is a deferred edge the import-layer census counts
    for nothing."""
    out = {}
    for work_dir in (Path(root) / WORK, Path(root) / ARCHIVE_WORK):
        for path in ac.spec_files(work_dir):
            rel = path.relative_to(work_dir).as_posix()
            try:
                data, body = ac.parse_spec_frontmatter(
                    path.read_text(encoding="utf-8"), rel
                )
            except (OSError, ValueError, UnicodeDecodeError):
                continue
            wid = str(data.get("id") or "").strip()
            if wid:
                out[wid] = body
    return out


def touched_modules(root, row, llrs=None, body=""):
    """The module set a row would edit: the `Module` cells of every LLR on the
    row's SR-Refs (the `intake._code_map_lines` join the worker brief already
    makes), plus any module path the row's own Context/Done-when names.

    BOTH HALVES, because each is blind where the other sees. The LLR join is
    authoritative and traceable but says nothing about a row that cites no SR —
    which is most process rows. The prose scan sees those and is noisy, which is
    why it is anchored on a `.py` suffix and why this whole signal is a
    pre-filter feeding a judge rather than a finding of its own.

    Compared by BASENAME. A row's prose writes `intake.py` where an LLR's
    `Module` cell writes `project-trajectory/scripts/intake.py`, and a signal
    that only fired when two rows spelled a path the same way would fire on
    almost nothing."""
    llrs = _llr_rows(root) if llrs is None else llrs
    srs = {tok.strip() for tok in _cell(row, "SR-Refs").split(";") if tok.strip()}
    named = _MODULE_RE.findall(_cell(row, "Title") + " " + (body or ""))
    return _llr_modules(srs, llrs) | {Path(name).name for name in named}


def _llr_modules(srs, llrs):
    """The `Module` basenames of every LLR row owned by one of `srs`."""
    return {
        Path(mod.strip()).name
        for llr in llrs
        if srs & {tok.strip() for tok in (llr.get("SR-Refs") or "").split(";")}
        for mod in (llr.get("Module") or "").split(";")
        if mod.strip()
    }


def _llr_rows(root):
    return spine_carrier.load(Path(root) / LLR_REGISTRY, "LLR-ID")


# --- the clusters --------------------------------------------------------------


def _model(rows):
    """The queued rows in the shape `check_trajectory.queue_conflict_pairs`
    reads. A projection of the ONE registry reader, never a fourth loader."""
    return [
        {
            "id": _cell(r, "WI-ID"),
            "title": _cell(r, "Title"),
            "status": _cell(r, "Status"),
            "srs": [
                tok.strip() for tok in _cell(r, "SR-Refs").split(";") if tok.strip()
            ],
            "specref": _cell(r, "SpecRef"),
        }
        for r in rows
    ]


def pair_findings(root, rows):
    """`[(first, second, finding)]` over the QUEUED rows — the mechanical
    pre-filter (`queue_conflict_pairs`) plus the two signals of plan §1.3.

    `check_trajectory` is imported HERE rather than at module scope: it is the
    validator and this is the scheduling side, so the arrow is paid for only on
    the ticks that actually run a census."""
    import check_trajectory as ct

    queued = queued_rows(rows)
    out = list(ct.queue_conflict_pairs(_model(queued)))
    llrs = _llr_rows(root)
    bodies = spec_bodies(root)
    facts = {
        _cell(r, "WI-ID"): (
            _commissioning_docs(r),
            touched_modules(root, r, llrs, bodies.get(_cell(r, "WI-ID"), "")),
        )
        for r in queued
    }
    ids = sorted(facts)
    for i, a_id in enumerate(ids):
        for b_id in ids[i + 1 :]:
            (a_docs, a_mods), (b_docs, b_mods) = facts[a_id], facts[b_id]
            shared_docs = sorted(a_docs & b_docs)
            if shared_docs:
                out.append(
                    (
                        a_id,
                        b_id,
                        "{} and {} were commissioned by the same {}".format(
                            a_id, b_id, ";".join(shared_docs)
                        )[:_LINE_CLIP],
                    )
                )
            shared_mods = sorted(a_mods & b_mods)
            if shared_mods:
                out.append(
                    (
                        a_id,
                        b_id,
                        "{} and {} both touch {}".format(
                            a_id, b_id, ";".join(shared_mods)
                        )[:_LINE_CLIP],
                    )
                )
    return sorted(set(out))


def _seed_pairs(rows, findings):
    """The findings that may SEED a cluster: everything except a pair involving
    a row an earlier consolidation minted (guard 3).

    The successor is not hidden — it is still an open row in the brief, and its
    lineage is `{prior}` — it simply does not, on its own, make the census ask
    the question the earlier consolidation already answered. Without this the
    plan's §4 third measurement is unreachable: after a close absorbs two rows
    the successor inherits their overlaps, so the very next census would mint a
    judgement over the judgement it just enacted."""
    minted = consolidation_successors(rows)
    return [f for f in findings if f[0] not in minted and f[1] not in minted]


def clusters(root, rows):
    """`(ids, findings)` — the candidate set and the pre-filter lines that
    selected it, or `([], [])` when nothing overlaps.

    ONE candidate set, the union of every connected component of the seed graph
    (see this module's header): two disjoint overlapping pairs are still one
    question, and only one judgement may be live at a time anyway. `findings` is
    every finding among the selected ids — including the ones a successor is in,
    which are evidence the judge should see once the cluster exists."""
    findings = pair_findings(root, rows)
    seeds = _seed_pairs(rows, findings)
    ids = sorted({f[0] for f in seeds} | {f[1] for f in seeds})
    if len(ids) < 2:
        return [], []
    chosen = set(ids)
    return ids, [f for f in findings if f[0] in chosen and f[1] in chosen]


# --- the guards ----------------------------------------------------------------


def _pending_refusal(rows):
    """Guard 1: no judgement is minted beside another judgement."""
    live = [
        _cell(r, "WI-ID")
        for r in rows
        if _cell(r, "SafetyClass").lower() == "adjudication"
        and _cell(r, "Status") in ("queued", "active")
    ]
    if live:
        return (
            "an adjudication row is already {} ({}) - a consolidation never "
            "stacks on another judgement and never judges a row a lane "
            "holds".format("queued or active", ";".join(sorted(live)))
        )
    return None


def _judged_refusal(rows, queue_sha):
    """Guard 2: this exact queue state has already been handed to a judge.

    ANY status, terminal included. The archived arm is the one that matters:
    once the consolidation closes, an active-only guard reads "nobody has judged
    this" and mints the identical row on the next idle tick."""
    for row in consolidations(rows):
        recorded, _spine = parse_digests(_cell(row, "Digests"))
        if recorded and recorded == queue_sha:
            return (
                "{} ({}) already judged this queue state (queue digest {}) - a "
                "queue state that has been judged is never judged again".format(
                    _cell(row, "WI-ID"), _cell(row, "Status"), queue_sha
                )
            )
    return None


def reabsorption_refusal(rows, absorbed):
    """Guard 3's hard half: a draft may not absorb a row an earlier
    consolidation MINTED.

    Overturning a consolidation is a RETURN-TO-DRAFT of THAT judgement (plan
    §1.3), and this refusal is what makes it one: the mint stops, the run pages
    the owner, and the earlier verdict is re-opened by a human rather than
    silently replaced by a second machine mint. `intake._supersedes_refusal`
    covers the adjacent case — absorbing a row already ABSORBED — which is a
    lineage chain rather than an overturned judgement."""
    minted = consolidation_successors(rows)
    hit = sorted(set(absorbed) & minted)
    if hit:
        return (
            "the draft absorbs {} - {} minted by an earlier consolidation. "
            "Re-absorbing one overturns that judgement, which is a "
            "RETURN-TO-DRAFT for the owner to rule, never a second mint; "
            "nothing minted".format(";".join(hit), "a row" if len(hit) == 1 else "rows")
        )
    return None


# --- the draft -----------------------------------------------------------------


def census_draft(root, rows=None):
    """`(draft, None)` for the row this census would mint, or `(None, reason)`.

    A REASON AND NOT AN EXCEPTION for every "nothing to do" arm, because the
    caller is a tick of the dispatcher and every one of these is an ordinary
    state: an idle station with no overlap is the healthy case."""
    root = Path(root)
    rows = read_rows(root) if rows is None else rows
    refusal = _pending_refusal(rows)
    if refusal:
        return None, refusal
    queue_sha = queue_digest(rows)
    refusal = _judged_refusal(rows, queue_sha)
    if refusal:
        return None, refusal
    ids, findings = clusters(root, rows)
    if not ids:
        return None, "no queued rows overlap - there is nothing to consolidate"
    specref = _specref(root)
    if not specref:
        return None, (
            "no candidate spec-of-record resolves in this repo ({}) - a row "
            "minted with an unresolvable SpecRef is refused at claim (R-E) and "
            "would sit at the head of the frontier forever".format(
                ", ".join(SPECREF_PROBES)
            )
        )
    cell = queue_sha + DIGEST_SEP + spine_digest(root)
    return {
        # DETERMINISTIC FOR THE QUEUE STATE, like every other derived title, so
        # the mint's exact-title dedup is a real second line of defence behind
        # the digest guard rather than an accident of wording.
        "title": "adjudicate queue overlap [{}]: {}".format(queue_sha, ";".join(ids)),
        "kind": "adjudication",
        "brief": BRIEF,
        "workstream": "process",
        "buildtier": BUILDTIER,
        "specref": specref,
        "priority": PRIORITY,
        "adjudicates": ids,
        "digests": cell,
        "context": _context(ids, findings, cell),
    }, None


def _specref(root):
    """The first `SPECREF_PROBES` entry that is a file in this repo, or ""."""
    for rel in SPECREF_PROBES:
        if (Path(root) / rel).is_file():
            return rel
    return ""


def _context(ids, findings, cell):
    """The minted row's derived `## Context`: what the census saw, and nothing
    it concluded. Naming the cluster and the findings is evidence; naming an
    outcome would be the mint pre-judging its own judge."""
    return (
        "Minted by the CONSOLIDATION CENSUS (the 2026-09-02 backlog-restructure "
        "plan §1.3), which runs from an idle station with no other judgement "
        "queued or active. The candidate cluster is {n} queued row(s): {ids}.\n\n"
        "The mechanical pre-filter selected them; it has concluded NOTHING. "
        "Each line below is a hint a string comparison can produce, and two "
        "rows deliberately cut from one plan share its path and always will:\n\n"
        "{findings}\n\n"
        "This row's `Adjudicates` cell fixes the population — judge those rows "
        "and no others. Its `Digests` cell is `{cell}`: the queue state and the "
        "spine state this question was asked against, so the census never asks "
        "it twice and a verdict that has gone stale is detectable rather than "
        "assumed fresh."
    ).format(
        n=len(ids),
        ids=";".join(ids),
        findings="\n".join("> " + line for _a, _b, line in findings),
        cell=cell,
    )


# --- the close (the 2026-09-02 restructure plan §1.5) --------------------------

#: The heading the verdict's TYPED outcome block lives under, in the
#: adjudication row's OWN spec. Not in the verdict file, for two reasons:
#: `handback.close_adjudication` is handed `(root, branch)` and nothing else, so
#: it reads the lane's tree rather than a path only `agent_loop` knows; and an
#: outcome recovered from prose is the `NEEDS-HUMAN` fold (WI-417).
VERDICT_SECTION = "## Consolidation"
#: The enum, lower-cased — the same four alternatives as
#: `adjudicate_brief.VERDICT_GRAMMAR["consolidate"]`, which is where the session
#: is told them.
OUTCOMES = ("queue", "queue-with-edge", "return-to-draft", "consolidate")
#: The keys the block may carry. An unknown key is a REFUSAL and never a skip,
#: for the reason `intake._DRAFT_KEYS` states: a silently dropped cell on a
#: judgement enacted with nobody watching is the loss this machinery exists to
#: prevent.
VERDICT_KEYS = frozenset({"outcome", "edges", "returns", "finding"})
_FENCE_RE = re.compile(r"```toml\s*\n(.*?)```", re.S)
#: One `queue-with-edge` edge: the waiter, then the row it must wait on.
_EDGE_RE = re.compile(r"^(WI-\d+)\s+needs\s+(WI-\d+)$")
#: The frontmatter `needs = [...]` line, rewritten surgically so the rest of a
#: spec is untouched (`intake._SPEC_NEEDS_RE`'s shape, and its reason).
_NEEDS_RE = re.compile(r"(?m)^needs\s*=\s*\[.*?\]\s*$")
#: The WHOLE Deliverable of an absorbed row — `check_trajectory`'s R-A grammar
#: for `restructured`: one line, naming the successor and nothing else.
DELIVERABLE = "Restructured into {}."


def parse_verdict(text, where):
    """`(record, refusal)` — the `## Consolidation` block's typed outcome.

    `(None, None)` when the section is absent, which is how every NON-consolidation
    adjudication row reads: the caller uses that to tell "not my case" from "my
    case, malformed". Everything else is a refusal and never a default — reading
    a malformed block as `queue` would silently discard a judgement that closes
    rows."""
    _head, sep, tail = text.partition("\n" + VERDICT_SECTION)
    if not sep:
        return None, None
    blocks = _FENCE_RE.findall(tail.split("\n## ", 1)[0])
    if len(blocks) != 1:
        return None, "{}: {} carries {} toml block(s) - one verdict, one block".format(
            where, VERDICT_SECTION, len(blocks)
        )
    try:
        data = tomllib.loads(blocks[0])
    except tomllib.TOMLDecodeError as exc:
        return None, "{}: the {} block is not valid TOML ({})".format(
            where, VERDICT_SECTION, exc
        )
    unknown = sorted(set(data) - VERDICT_KEYS)
    if unknown:
        return None, "{}: the {} block carries unknown key(s) {}".format(
            where, VERDICT_SECTION, unknown
        )
    outcome = str(data.get("outcome") or "").strip().lower()
    if outcome not in OUTCOMES:
        return None, "{}: outcome {!r} is not one of {}".format(
            where, data.get("outcome"), "|".join(OUTCOMES)
        )
    for key in ("edges", "returns"):
        refusal = _list_refusal(data.get(key), key, where)
        if refusal:
            return None, refusal
    edges, refusal = _parse_edges(data.get("edges"), where)
    if refusal:
        return None, refusal
    returns, refusal = _parse_returns(data.get("returns"), where)
    if refusal:
        return None, refusal
    record = {
        "outcome": outcome,
        "edges": edges,
        "returns": returns,
        "finding": str(data.get("finding") or "").strip(),
    }
    refusal = _shape_refusal(record, where)
    # A shape refusal returns NO record, like every other arm: a caller handed
    # both would have to remember not to use the one it was given, and "parsed
    # but do not act on it" is not a state worth being able to represent.
    return (None, refusal) if refusal else (record, None)


def _list_refusal(value, key, where):
    """Refuse anything but a list of strings for a collection key.

    TYPED, not coerced, and the two failures this closes were both silent.
    `returns = 1` reached a `for` loop and RAISED an uncaught `TypeError` out of
    a parser whose whole contract is `(record, refusal)` — a crash where a named
    refusal was promised. `returns = "WI-401"` iterated the STRING and parsed as
    six single-character targets, so a verdict naming one row enacted six
    nonexistent ones. TOML makes the author's intent unambiguous here, so
    reading a bare string as a one-element list would be tolerance nobody asked
    for; the authored grammar is a list, and the refusal says so."""
    if value is None:
        return None
    if not isinstance(value, list):
        return (
            "{}: `{}` is {!r} - a TOML LIST of `WI-###` strings, always, even "
            'for one entry ({} = ["WI-401"])'.format(where, key, value, key)
        )
    bad = [item for item in value if not isinstance(item, str)]
    if bad:
        return "{}: `{}` holds non-string entr(ies) {!r}".format(where, key, bad)
    return None


def _duplicate_refusal(seen, item, key, where):
    """Refuse a target named twice.

    A duplicate is not harmless: the close walks the list and MOVES each target,
    so the second pass finds the row already gone and fails half-way through a
    close that advertises itself as all-or-nothing. Refusing at the parse is the
    cheaper end of the same rule."""
    if item in seen:
        return "{}: `{}` names {} twice - one target, one entry".format(
            where, key, item if isinstance(item, str) else repr(item)
        )
    seen.add(item)
    return None


def _parse_returns(items, where):
    """`([ids], None)` or `(None, refusal)` for the `returns` list."""
    out, seen = [], set()
    for item in items or []:
        token = item.strip()
        if not token:
            continue
        if not ac.WI_TOKEN_RE.match(token):
            return None, "{}: `returns` entry {!r} is not a WI-### id".format(
                where, item
            )
        refusal = _duplicate_refusal(seen, token, "returns", where)
        if refusal:
            return None, refusal
        out.append(token)
    return out, None


def _parse_edges(items, where):
    """`([(waiter, blocker)], None)` or `(None, refusal)` for the `edges` list."""
    out, seen = [], set()
    for item in items or []:
        matched = _EDGE_RE.match(" ".join(str(item).split()))
        if matched is None:
            return None, (
                "{}: edge {!r} is not `<WI-###> needs <WI-###>` - the waiter "
                "first, then the row it must wait on".format(where, item)
            )
        if matched.group(1) == matched.group(2):
            return None, "{}: edge {!r} makes a row wait on itself".format(where, item)
        pair = (matched.group(1), matched.group(2))
        refusal = _duplicate_refusal(seen, pair, "edges", where)
        if refusal:
            return None, refusal
        out.append(pair)
    return out, None


def _shape_refusal(record, where):
    """What each outcome OWES, and what it may not carry.

    Both directions, because each is silent on its own: a `return-to-draft`
    naming no row enacts nothing while reporting a judgement, and a `queue`
    carrying `returns` has those rows quietly ignored — the verdict said one
    thing and the close did another."""
    outcome = record["outcome"]
    owed = {"queue-with-edge": "edges", "return-to-draft": "returns"}.get(outcome)
    if owed and not record[owed]:
        return "{}: outcome {} names no `{}` - it would enact nothing".format(
            where, outcome, owed
        )
    if outcome == "return-to-draft" and not record["finding"]:
        return (
            "{}: return-to-draft carries no `finding` - a refusal without a "
            "named reason is not actionable and will simply be re-queued".format(where)
        )
    for key in ("edges", "returns"):
        if key != owed and record[key]:
            return "{}: outcome {} carries `{}`, which it does not enact".format(
                where, outcome, key
            )
    return None


def absorbed_ids(drafts):
    """The rows a verdict's `## Dispositions` drafts ABSORB — the union of their
    `supersedes` values, ordered and de-duplicated.

    THE ONE CARRIER of the absorbed set, deliberately: the `## Consolidation`
    block does NOT repeat it, because the mint reads `supersedes` and a second
    copy could disagree with the value that actually acts."""
    out = []
    for draft in drafts or []:
        value = draft.get("supersedes")
        items = value if isinstance(value, (list, tuple)) else [value]
        for item in items:
            for token in str(item or "").split(";"):
                token = token.strip()
                if token and token not in out:
                    out.append(token)
    return out


#: The verdict file's one machine line, as `adjudicate_brief.VERDICT_GRAMMAR`
#: declares it for this brief: the label, then the two counters.
_MACHINE_RE = re.compile(r"^\s*OUTCOME:\s*(?P<label>[A-Z-]+)(?P<rest>.*)$", re.M)
_COUNTER_RE = re.compile(r"\b(needs|absorbs)\s*=\s*(\S+)")


def scope_of(meta):
    """A closing row's `Adjudicates` cluster as a set, from spec frontmatter.

    Tolerant of both spellings the format produces — `wi_convert` writes the
    COLUMN `;`-joined and `parse_spec` reads the frontmatter key back as a TOML
    list — because this reader is handed whichever the caller happens to hold,
    and a scope silently read as empty is the widening the cell exists to
    prevent."""
    value = meta.get("adjudicates") if hasattr(meta, "get") else None
    items = value if isinstance(value, (list, tuple)) else [value]
    return {
        token.strip()
        for item in items
        for token in str(item or "").split(";")
        if token.strip()
    }


def parse_machine_line(text):
    """`(label, {counter: value})` for the verdict file's `OUTCOME:` line, or
    None when it carries none.

    None is not a refusal: `agent_loop.worker_endstate` has already gated the
    session's DONE on this line, so re-deriving that precondition here would
    turn a hand close or a fixture into a false refusal. What this exists for is
    the case where the line IS there and says something else."""
    matched = _MACHINE_RE.search(text or "")
    if matched is None:
        return None
    counters = {
        key: value for key, value in _COUNTER_RE.findall(matched.group("rest") or "")
    }
    return matched.group("label").strip(), counters


def _counter_ids(value):
    """A counter's value as a set of ids; `-` (the declared "none") is empty."""
    if not value or value.strip() == "-":
        return set()
    return {token.strip() for token in value.split(";") if token.strip()}


def reconcile_refusal(machine, record, absorbed, where):
    """Refuse when the verdict file and the typed block describe different
    judgements. The two are ONE fact and this is what makes that true.

    Checked in the order a reader would ask: is it the same OUTCOME, does
    `absorbs=` name the same rows the drafts supersede, does `needs=` name the
    same rows the edges make wait. A counter the grammar requires and nothing
    compares is a second carrier, and a second carrier of one fact is how a
    session reports one verdict while the machinery performs another."""
    label, counters = machine
    if label.lower() != record["outcome"]:
        return (
            "{}: the verdict file says `OUTCOME: {}` but the ## Consolidation "
            "block says outcome = {!r} - one judgement, one answer".format(
                where, label, record["outcome"]
            )
        )
    said = _counter_ids(counters.get("absorbs"))
    if said != set(absorbed):
        return (
            "{}: the verdict file says `absorbs={}` but the ## Dispositions "
            "draft supersedes {} - the counter and the lineage cell are one "
            "fact".format(
                where,
                counters.get("absorbs") or "(absent)",
                ";".join(sorted(absorbed)) or "nothing",
            )
        )
    waiters = {waiter for waiter, _blocker in record["edges"]}
    said = _counter_ids(counters.get("needs"))
    if said != waiters:
        return (
            "{}: the verdict file says `needs={}` but the ## Consolidation "
            "block edges make {} wait - the counter and the block are one "
            "fact".format(
                where,
                counters.get("needs") or "(absent)",
                ";".join(sorted(waiters)) or "nobody",
            )
        )
    return None


def close_refusal(root, record, absorbed, rows, where, *, scope, drafts, recorded):
    """Why this verdict may not be enacted, or None. Read ONCE, before the close
    writes anything, so a half-enacted verdict is unrepresentable.

    SIX REFUSALS, and every one of them was a hole an adversarial round drove a
    real verdict through:

    1. **The outcome and the absorbed set agree, both ways.** A `consolidate`
       that supersedes nothing is not one; any other outcome whose draft
       supersedes rows would archive them while the verdict said to leave them
       alone.
    2. **EXACTLY ONE successor for a consolidation.** Plan §1.2 says the session
       drafts ONE; two drafts each superseding part of the cluster used to close
       cleanly, minting two rows that split the scope with nothing recording the
       split.
    3. **Every row this verdict touches is inside the row's `Adjudicates`
       scope.** The scope cell was decorative on this path: a draft superseding
       a row the census never clustered closed, merged and archived it. The
       first-approval sibling has enforced exactly this bound since WI-572
       (`is OUTSIDE `Adjudicates` scope`), and for the same reason — a live
       re-derivation with no scope to intersect asks a wider question than the
       mint asked.
    4. **The recorded `Digests` still describe the tree.** The pair is recorded
       at the mint precisely so a stale verdict is detectable, and nothing
       compared it: a forged or simply out-of-date cell enacted a verdict
       against a queue that had moved underneath it.
    5. **Every row it touches is still `queued`.** The census guard makes a
       claimed cluster row a race only a hand claim can produce (plan §1.5), and
       when it happens the close refuses BY NAME rather than archiving work a
       lane is building.
    6. **The lineage the mint will refuse is refused HERE.** `reabsorption_refusal`
       used to run only inside `_pre_mint_refusal`, one commit after the close
       had committed and the merge had stood — so a verdict absorbing an earlier
       consolidation's successor closed, merged, minted NOTHING, and left the
       queue byte-identical to the state its own `Digests` cell had recorded.
       `_judged_refusal` then answered "already judged" forever and the cluster
       was un-consolidatable without a hand edit. A refusal that can be evaluated
       before the close must be evaluated before the close.

    `scope` is the closing row's `Adjudicates` set, `drafts` its parsed
    `## Dispositions` blocks, `recorded` its `Digests` cell."""
    # ORDER IS THE MESSAGE. The specific causes run first: a row this verdict
    # names that a lane has claimed is reported BY NAME, before the drift rung
    # notices that the queue digest moved — which it also did, because that
    # claim is what moved it. "WI-402 is no longer queued" is actionable;
    # "the queue has moved" is the same fact with the row filed off.
    for rung in (_outcome_refusal, _scope_refusal, _queued_refusal, _drift_rung):
        refusal = rung(root, record, absorbed, rows, where, scope, drafts, recorded)
        if refusal:
            return refusal
    return reabsorption_refusal(rows, absorbed)


def _touched(record, absorbed):
    """Every row id this verdict would move: absorbed, returned, or edged."""
    named = set(absorbed) | set(record["returns"])
    for waiter, blocker in record["edges"]:
        named |= {waiter, blocker}
    return named


def _outcome_refusal(_root, record, absorbed, _rows, where, _scope, drafts, _recorded):
    """Rungs 1-2: the outcome and the absorbed set agree, and a consolidation
    drafts EXACTLY ONE successor."""
    consolidating = record["outcome"] == "consolidate"
    if consolidating and not absorbed:
        return (
            "{}: outcome consolidate but the ## Dispositions draft supersedes "
            "nothing - a consolidation that absorbs no row is not one".format(where)
        )
    if not consolidating and absorbed:
        return (
            "{}: outcome {} but the ## Dispositions draft supersedes {} - only "
            "a CONSOLIDATE verdict absorbs rows".format(
                where, record["outcome"], ";".join(sorted(absorbed))
            )
        )
    if consolidating and len(drafts or []) != 1:
        return (
            "{}: outcome consolidate drafted {} successor(s) - a consolidation "
            "replaces its cluster with ONE row (plan §1.2), and several drafts "
            "split the absorbed scope with nothing recording the "
            "split".format(where, len(drafts or []))
        )
    return None


def _scope_refusal(_root, record, absorbed, _rows, where, scope, _drafts, _recorded):
    """Rung 3: every row this verdict touches is inside the row's cluster."""
    outside = sorted(_touched(record, absorbed) - set(scope or ()))
    if not outside:
        return None
    return (
        "{}: {} OUTSIDE this row's `Adjudicates` scope ({}) - a consolidation "
        "acts on the cluster the census handed it and on no other row; an "
        "unstated boundary read as 'every queued row' is the widening the cell "
        "exists to prevent".format(
            where, ";".join(outside), ";".join(sorted(scope or ())) or "empty"
        )
    )


def _drift_rung(root, _record, _absorbed, rows, where, _scope, _drafts, recorded):
    """Rung 4, as the uniform five-argument shape the driver walks."""
    return _drift_refusal(root, rows, recorded, where)


def _queued_refusal(_root, record, absorbed, rows, where, _scope, _drafts, _recorded):
    """Rung 5: every row it touches is still `queued`."""
    status = {
        (r.get("WI-ID") or "").strip(): (r.get("Status") or "").strip() for r in rows
    }
    off = sorted(wid for wid in _touched(record, absorbed) if status.get(wid) != QUEUED)
    if not off:
        return None
    return (
        "{}: {} named by this verdict {} no longer queued - a consolidation "
        "acts on the queue it judged, and a row a lane has claimed is not its "
        "to move".format(where, ";".join(off), "is" if len(off) == 1 else "are")
    )


def _drift_refusal(root, rows, recorded, where):
    """Refuse a verdict whose recorded `Digests` no longer describe the tree.

    BOTH HALVES are compared and they fail differently, so the message says
    which. A moved QUEUE means the population this verdict judged is not the one
    it would act on; a moved SPINE means the requirements a contradiction was
    judged against have changed. An absent or malformed cell is its own refusal:
    the pair is what makes staleness detectable, so a verdict carrying none is
    not verifiable and must not be enacted.

    The judging row itself is `active` while the close runs, so it is out of the
    queued set and the digest it recorded at the mint still holds — drift here
    means something ELSE moved."""
    want_queue, want_spine = parse_digests(recorded)
    if not want_queue:
        return (
            "{}: the closing row carries no usable `Digests` cell, so the queue "
            "state its verdict judged is unrecorded and staleness is not "
            "detectable - the close will not enact an unverifiable "
            "verdict".format(where)
        )
    live_queue, live_spine = queue_digest(rows), spine_digest(root)
    if live_queue != want_queue:
        return (
            "{}: the QUEUE has moved since this verdict was minted (recorded "
            "{}, now {}) - the rows it judged are not the rows it would act "
            "on".format(where, want_queue, live_queue)
        )
    if live_spine != want_spine:
        return (
            "{}: the SPINE has moved since this verdict was minted (recorded "
            "{}, now {}) - contradiction with the spine is one of the three "
            "questions it answered".format(where, want_spine, live_spine)
        )
    return None


# --- the pure text transforms the callers write back --------------------------


def restructured_text(text, successor):
    """An absorbed row's spec, rewritten for `archive/work/restructured/`; None
    when the frontmatter fence is absent.

    Its SCOPE TEXT IS BYTE-IDENTICAL and `specref` is KEPT — the same rule
    `partial` follows, for the reason R-F's carve-out states: the successor's
    lineage is worth nothing if the thread it continues has already been cut.
    The only edit is the Deliverable, which is exactly one line, before
    `## Context` (a Deliverable placed after it parses as EMPTY and reds R-A)."""
    lines = text.split("\n")
    close = _fence_close(lines)
    if close is None:
        return None
    head = "\n".join(lines[: close + 1])
    body = "\n".join(lines[close + 1 :])
    return (
        head
        + "\n"
        + "\n## Deliverable\n\n"
        + DELIVERABLE.format(successor)
        # TWO newlines, and the second is load-bearing: `parse_spec_deliverable`
        # clips the body at `\n## Context\n`, so a Deliverable running straight
        # into that heading leaves the section unterminated and the whole spec
        # reads as a malformation - the row then DROPS OUT of the registry, and
        # every reader of it reports the absorbed row as missing rather than
        # restructured.
        + "\n\n"
        + body.lstrip("\n")
    )


def _fence_close(lines):
    """The index of a spec's CLOSING `+++` line, or None.

    LINE-WISE against the shared fence constant, exactly as
    `kitlib.registry.parse_spec_frontmatter` does, and that is the whole point:
    a `text.partition("\n+++\n")` finds nothing on a CRLF checkout (Windows with
    `core.autocrlf=true`), so `restructured_text` returned None and the absorbed
    row was skipped — on EVERY absorbed row, on that platform, with no message.
    The suite could not see it because every fixture calls `conftest.pin_autocrlf`."""
    stripped = [ln.rstrip("\r") for ln in lines]
    if not stripped or stripped[0] != kitregistry.SPEC_FENCE:
        return None
    for index in range(1, len(stripped)):
        if stripped[index] == kitregistry.SPEC_FENCE:
            return index
    return None


def returned_text(text, finding):
    """A RETURN-TO-DRAFT row's spec with the verdict's finding quoted into its
    `## Context` — verbatim, under a line saying where it came from.

    Quoted rather than summarised for the plan's own reason (decompose, don't
    paraphrase) and for a practical one: a row bounced back with no named
    referent is a row that gets re-queued unchanged, which is the loop this
    outcome exists to break."""
    note = (
        "Returned to `draft/` by a consolidation judgement (the 2026-09-02 "
        "backlog-restructure plan §1.5). The finding, verbatim:\n\n"
        + "\n".join("> " + line for line in (finding or "").splitlines() or [""])
        + "\n"
    )
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if line.rstrip("\r") == "## Context":
            # Line-wise for `_fence_close`'s reason: a CRLF checkout matched no
            # `\n## Context\n` and the return appended a SECOND `## Context`
            # heading to the spec.
            return (
                "\n".join(lines[: index + 1])
                + "\n\n"
                + note
                + "\n".join(lines[index + 1 :])
            )
    return text.rstrip("\n") + "\n\n## Context\n\n" + note


def edged_text(text, blocker):
    """A QUEUE-WITH-EDGE row's spec with `blocker` added to its hard `needs`;
    None when the row carries no readable `needs` line.

    A surgical rewrite of the ONE frontmatter line, like
    `intake._replace_inbound_edges`, so the row's Context and Deliverable are
    untouched. Idempotent: a row that already waits on the blocker (hard, or
    softly with the `~` prefix) comes back unchanged, and the caller reports a
    no-op rather than committing one."""
    matched = _NEEDS_RE.search(text)
    if matched is None:
        return None
    try:
        current = [str(v) for v in tomllib.loads(matched.group(0)).get("needs") or []]
    except tomllib.TOMLDecodeError:
        return None
    if blocker in current or ("~" + blocker) in current:
        return text
    rendered = ", ".join('"{}"'.format(tok) for tok in current + [blocker])
    return (
        text[: matched.start()] + "needs = [" + rendered + "]" + text[matched.end() :]
    )


def archive_absorbed(root, minted):
    """THE CONSOLIDATION'S OTHER HALF (the 2026-09-02 restructure plan §1.5):
    move every ABSORBED row from `queued/` into `archive/work/restructured/`,
    with `Restructured into WI-<successor>.` as its whole Deliverable and its
    scope text byte-identical.
    `([(absorbed id, successor id, dest relpath)], None)` or `([], refusal)`.

    ALL OR NOTHING, PREFLIGHTED. Every absorbed row is resolved to a readable
    queued spec BEFORE the first move, and a single unresolvable one refuses the
    whole call with the id named. The earlier shape skipped silently and let the
    mint commit anyway: claiming one cluster row in the window between the close
    and the merge produced two `restructured` lines instead of three, no message
    about the third, and a successor whose `Supersedes` cell named a row that
    was still `active` on its own lane — two live rows covering one scope, with
    the ABSENCE of one line among three as the only signal. The identical race
    is refused BY NAME at the close, so the design guarded it loudly in one
    place and silently in the other.

    IT RUNS AT THE MINT AND NOT AT THE CLOSE, and the ordering is forced from
    both ends. The Deliverable NAMES THE SUCCESSOR, whose id `_write_draft`
    allocates during the mint — the close runs on the lane before the merge and
    cannot know it. And `intake._supersedes_refusal`'s `absorbed_ids` arm
    refuses a draft continuing an ALREADY `restructured` row (lineage does not
    chain), so archiving these rows at the close would make the mint refuse its
    own successor. It runs AFTER the edge re-point for the third half of the
    same argument: `_open_specs` skips a terminal row, so a dependent's edge has
    to move while the absorbed row is still open."""
    plan, refusal = _archive_plan(root, minted)
    if refusal:
        return [], refusal
    moved = []
    for successor, dead_id, src, dest, new_text in plan:
        _touched, refusal = spec_move.move_spec(root, src, dest, new_text=new_text)
        if refusal:
            return moved, (
                "the consolidation close could not archive {} into {}: {}".format(
                    dead_id, successor, refusal
                )
            )
        moved.append((dead_id, successor, dest))
    return moved, None


def _archive_plan(root, minted):
    """`([(successor, dead_id, src, dest, new_text)], None)` for every absorbed
    row, or `([], refusal)` naming the first that cannot be moved.

    The whole preflight, before any write: the row is a queued spec, it is
    readable, and its frontmatter fence parses so the Deliverable can be
    rewritten. `minted` is `intake._mint`'s `[(wi_id, [absorbed ids])]` — the
    whole verdict, resolved at once, for the same reason the edge re-point is."""
    queued = Path(root) / WORK / "queued"
    plan = []
    for successor, absorbed in minted:
        for dead_id in absorbed:
            hits = sorted(queued.glob(dead_id + "-*.md")) if queued.is_dir() else []
            if not hits:
                return [], (
                    "the consolidation close cannot archive {}: it is no longer "
                    "a queued spec (claimed or moved between the close and this "
                    "merge). Nothing archived; the mint is refused whole rather "
                    "than leaving {}'s lineage cell naming a row it did not "
                    "absorb".format(dead_id, successor)
                )
            try:
                text = hits[0].read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                return [], "the consolidation close cannot read {}: {}".format(
                    hits[0].name, exc
                )
            new_text = restructured_text(text, successor)
            if new_text is None:
                return [], (
                    "the consolidation close cannot rewrite {}: it carries no "
                    "closed `+++` frontmatter fence".format(hits[0].name)
                )
            plan.append(
                (
                    successor,
                    dead_id,
                    "{}/queued/{}".format(WORK, hits[0].name),
                    "{}/restructured/{}".format(ARCHIVE_WORK, hits[0].name),
                    new_text,
                )
            )
    return plan, None


def absorbed_done_when(root, ids):
    """Each absorbed row's `## Done-when` block, verbatim, under its old id —
    the successor Context's second half (plan §1.5, Done-when 4).

    QUOTED AND NOT SUMMARISED, because it is the SPEC the successor must still
    satisfy: "decompose, don't paraphrase". Without it the shipped brief's own
    promise ("each absorbed row's Done-when block quoted under its old id … do
    NOT paraphrase") was false, so a judge who followed the brief wrote a
    boundary sentence and nothing else, and the successor a lane then built
    carried no acceptance criteria at all.

    Read while the absorbed rows are still in `queued/` — this runs at the mint,
    before `archive_absorbed` moves them. A row whose block cannot be read is
    STATED as such rather than skipped: a missing criterion that leaves no trace
    is the failure this whole section is about."""
    bodies = spec_bodies(root)
    out = []
    for dead_id in ids:
        block = _done_when_block(bodies.get(dead_id))
        out.append(
            "### {} (absorbed) — its Done-when, verbatim\n\n{}".format(
                dead_id,
                block or "(this row's spec declared no `## Done-when` section)",
            )
        )
    if not out:
        return ""
    return (
        "The absorbed rows' acceptance criteria, carried across UNCHANGED. This "
        "is the spec this row must still satisfy — the ids are historical, the "
        "obligations are not:\n\n" + "\n\n".join(out)
    )


def _done_when_block(body):
    """One spec body's Done-when section, verbatim, or "".

    Through `kitlib.registry.done_when_section` and NOT a local match: this
    repo's live specs spell the heading four ways, and the narrow
    `== "## done-when"` test this replaces dropped 8 of 30 of them - then said
    so, in the successor's Context, as "declared no `## Done-when` section".
    An affirmative false statement about another row's acceptance criteria is
    worse than a missing one, because it reads as a checked fact."""
    return "\n".join(kitregistry.done_when_section(body)).strip("\n").strip()
