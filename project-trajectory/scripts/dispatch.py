"""dispatch.py — the dispatcher: tick loop, admission, merge slot (the scheduling front end).

WI-374 restored this loop as drive.py after concurrency-restructure Phase 5
deleted the parallel dispatcher; WI-381 (docs/concurrency-v2.md §A4.2) renamed
it to what its job now is — the DISPATCHER — and extracted the lane half into
the sibling lane.py (ensure worktree, launch the worker subprocess, run the
§A2 refresh). What lives here is the deciding half: the tick loop, the
frontier read, admission, the merge slot and the stall guard. A plain
`agent-resume` launch (agent_loop.py with no role, IF-015) lands here instead
of refusing, and the dispatcher composes the independently-proven parts:

    schedule.py frontier (IF-053)  ->  next ready WI in build order
    integrate.py claim   (IF-080)  ->  the §2.3 trunk claim + branch cut
    lane.py worker       (IF-015)  ->  one worker session on the claimed branch
    integrate.py refresh (IF-080)  ->  the §A2 station refresh, OUTSIDE the slot
    integrate.py integrate (IF-080) -> the merge slot

The frontier is re-derived from the registry at the top of EVERY tick, so a
WI filed mid-run (by a worker, a review, or a human) is picked up in the same
run — no restart needed. Up to `lanes` worker lanes run at once (the §A4.3
dial: CLI --lanes > AGENT_LANES > docs/stack.ini [agent-loop] lanes > 1; the
template seeds 2, an absent key means 1 so no adopter is upgraded into
concurrency silently). At lanes=1 this degenerates to the serial loop it grew
from.

ADMISSION IS THE ONE SCHEDULING DECISION THIS MODULE OWNS (§A4.1/§A8, the
authority the deleted `_claim_refusal` safety arm moved here). The §A8 policy
table, per kind x session hold: ordinary/critique dispatch parallel at
every level; high-risk/protected dispatch exclusive at every level; a `spine`
row dispatches at every level — building a scope change is WORK, not an
approval — but EXCLUSIVELY and BATCHED: an exclusive-kind row on the
frontier stops new admission, the dispatcher waits for every lane back in the
station, then admits ALL spine rows TOGETHER as one batch (one branch, one
`agent_loop --wi 'A;B'` worker, one re-attest window, one owner sitting). An
`attestation`/`gate` row does NOT dispatch while the tier in process is still
HUMAN-HELD: the lanes drain, the cards stay on open-items.html, and the run
exits 0 — the machine finished everything it was allowed to do
(`agent_route.failure_action(human_held=True)` is the contract this
implements). With `keep_nondependent` those rows dispatch only as the queued
batch once nothing else remains; on a LOOP-HELD tier they dispatch outright (a
recorded fresh-context reviewer verdict approves). The three retired enum words
(`attended` / `single-approve` / `autonomous`) each named one cell of that
two-dial table, which is why they could not express the fourth. The fixed
points hold at every level: the owner's final read is the human's, no un-run greens, the
harness is still the bar, approved owner decisions are never re-decided.

Beyond admission it adds ORDERING only, no authority: every refusal stays
where it already lives (the tracked docs/work/pause, a dirty trunk, the
SpecRef and status-prose claim rungs, the §A2 refresh bar, the RULING-7
verdict gate, docs/push-policy). Any refusal from a composed part STOPS the
run loudly — admission halts, the in-flight lanes drain, and the run exits
with the refusal's code; the dispatcher never skips past one, never
force-merges, and NEVER pushes (there is deliberately no flag to ask it to;
docs/push-policy is honored by construction). A parked claimed branch from an
interrupted run is resumed (worker relaunched on it) rather than refused, so
the walk-away loop restarts with the same double-click that started it.

EVERY LANE ENDS IN A MERGE (docs/concurrency-v2.md §A3, WI-387). A worker that
cannot finish no longer stops the run: the dispatcher reads its exit code, and a
DECIDED one (`_WORKER_OUTCOMES`) closes the lane as a HANDBACK — the work so
far committed as-is, the specs back in `queued/` blocked on a blockref, the
branch merged like any other. A CRASH is not a hang and keeps the parked-resume
path unchanged. The WRITES themselves stay in the handback.py sibling, which
owns closing a lane; what lives here is only the DECISION of which outcome a
cycle reached.

Explicitly NOT here, by spec: worktree pools, reservations, train grouping,
run-state files, disposition arms. If a change starts to grow this module
toward the deleted dispatcher's shape, stop and escalate as a written case
(process-options.md, the design-escalation clause).
"""

from __future__ import annotations

import calendar
import os
import sys
import time
from pathlib import Path

import adjudicator_session
import agent_common as ac
import agent_session
import census
import handback
import intake
import integrate
import lane
import schedule

SCRIPTS = Path(__file__).resolve().parent


def _say(msg, err=False):
    print(
        "dispatch: {}".format(msg), file=sys.stderr if err else sys.stdout, flush=True
    )


def _iso_epoch(stamp):
    """The UTC epoch of a store `%Y-%m-%dT%H:%M:%SZ` stamp, or None. `timegm`
    (not `mktime`) so the "Z" is honoured as UTC rather than local time."""
    try:
        return calendar.timegm(time.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ"))
    except (TypeError, ValueError):
        return None


def _keepwarm_tick(root, table, now):
    """WI-540 (plan §3.5, owner ruling OI-69 (c2)): keep the ANTHROPIC prompt
    cache warm for a RETAINED adjudicator session while work is pending, pinging
    THROUGH the blackout. A STRICT NO-OP when the dial or `keepwarm_minutes` is
    off (shipped state) — and best-effort even when on: every failure is
    swallowed, because a keep-warm ping must never wedge the dispatcher
    (SN-016). `table` truthy means lanes are active (the work-pending proxy)."""
    cfg = ac.adjudicator_config(root / "docs")
    if not cfg.enabled or cfg.keepwarm_minutes <= 0:
        return
    for record in adjudicator_session.load_family(root, "ANTHROPIC"):
        if not adjudicator_session.keepwarm_due(
            record,
            cfg,
            "ANTHROPIC",
            now,
            _iso_epoch(record.get("last_used")),
            bool(table),
        ):
            continue
        sid = record.get("session_id")
        if not sid:
            continue
        try:
            agent_session.run_session(
                ["claude", "-p", "--resume", sid, "--max-turns", "1"],
                root,
                120,
                stdin_input="ack",
            )
        except OSError:
            continue
        record["last_used"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        adjudicator_session.save(root, record)


def _branch_for(root, wid):
    """The §5.4 WI-scoped branch name: the queued spec's filename, lowercased
    id, without the .md — e.g. WI-374-...-claimer.md -> wi-374-...-claimer.
    Single-segment by construction (spec filenames carry no separators the
    claim's flat-directory rung refuses)."""
    hits = sorted((root / "docs" / "work" / "queued").glob(wid + "-*.md"))
    if len(hits) != 1:
        return None
    stem = hits[0].stem
    return "wi-" + stem[len("WI-") :]


def _parked_branches(root):
    """Claimed branches from an interrupted run: active/<branch>/ still holds
    specs AND the branch ref exists. (A finished branch — specs all moved out —
    is the integrator's to merge, not ours to resume.) Reuses the integrator's
    own finished-branch read so the two never disagree about "finished"."""
    active = root / "docs" / "work" / "active"
    if not active.is_dir():
        return []
    finished = set(integrate.finished_branches(root))
    candidates = [
        p.name
        for p in sorted(active.iterdir())
        if p.is_dir() and p.name not in finished and any(p.glob("WI-*.md"))
    ]
    return [
        b
        for b in candidates
        if ac.git(root, "rev-parse", "--verify", "--quiet", "refs/heads/" + b)[0] == 0
    ]


def _session_config_refusal(root, args):
    """The pre-claim config preflight: an empty AGENT_CMD with no
    managed-routing enable-list means every worker would refuse at its own
    preflight - AFTER the claim had already parked a branch. Refuse here
    instead, with nothing claimed yet. Returns the refusal string, or None."""
    # SN-028: the mixed-config refusal rides HERE, not at the policy read
    # itself - `run` reads the level once at :985 and a raised exception there
    # would rewrite an exit-code contract. This rung already gates every claim,
    # so a half-migrated config can never reach the dispatcher's policy read.
    conflicts = ac.config_conflicts(root / "docs")
    if conflicts:
        return conflicts[0]
    template = (
        args.agent_cmd
        if args.agent_cmd is not None
        else os.environ.get("AGENT_CMD", "")
    )
    if template.strip():
        return None
    enabled = root / "docs" / "agents-enabled"
    routed = enabled.is_file() and any(
        ln.strip() and not ln.lstrip().startswith("#")
        for ln in enabled.read_text(encoding="utf-8", errors="replace").splitlines()
    )
    if routed:
        return None
    return (
        "no agent command wired (AGENT_CMD empty, docs/agents-enabled "
        "absent/empty) - a worker session cannot launch; fill the "
        "launcher slot or the enable-list, then relaunch"
    )


def _residue_wi_count(root):
    """How many WI **ids** the finished-but-unmerged branches carry.

    The banner promises "N WI(s) integrated", and that is not the branch count:
    a spine batch is ONE branch carrying several WIs, and the barrier-open
    drain is exactly where batches turn up. Counted off the TRUNK's claim
    directories (`integrate._claimed_wi_ids`) — the same evidence the merge
    slot reads — so the banner and the merge can never disagree about how many
    WIs a branch was carrying (REVIEW-A finding 1)."""
    return sum(
        len(integrate._claimed_wi_ids(root, branch))
        for branch in integrate.finished_branches(root)
    )


def _drain(root, tier):
    """Refresh every finished branch, then run the merge slot. An exit code.

    NOT TRANSACTIONAL, and no caller may assume it is: `integrate.integrate`
    merges the finished branches in sequence and stops at the first refusal, so
    a NONZERO return can still have merged some of them (driven at REVIEW-A
    finding 3). Both call sites answer that by printing no success count at all
    rather than crediting a partial drain; a caller that ever needs the partial
    figure must have this function report what it actually integrated instead
    of counting beforehand.

    THE SPECULATIVE HALF of the station protocol (docs/concurrency-v2.md §A2.0,
    ruled 2026-07-31). The 11-minute bar runs HERE, outside the slot, so the
    exclusive turn to advance trunk is held for a sub-second ancestor check and
    the merge itself; a lane that loses a race redoes a refresh it would have
    owed anyway going second, and nothing else is reconciled because ancestry
    is the only thing being speculated on.

    THIS CALL IS THE WHOLE SPECULATION. Deleting the refresh loop below
    restricts the design to pessimistic: `integrate_one` refreshes in-slot for
    any branch that arrives un-refreshed, so the queue keeps working, one lane
    at a time, with the bar inside the lock. That is the owner's recorded
    caveat priced at one line.

    A red refresh STOPS the run for a branch that asserts it is DONE - it is
    the same failure a red merge bar used to be, moved to where the lane that
    caused it can fix it. A branch that asserts the opposite is the §A3
    exception the ruling covers: see `_refresh_or_quarantine`.
    """
    for branch in integrate.finished_branches(root):
        ready, _why = integrate._merge_ready(root, branch)
        if ready:
            # A lane's own refresh (or a hand refresh) already attested this
            # exact tip against the current trunk — redoing the disposable
            # commit would spend a full bar to reproduce it.
            continue
        refusal = _refresh_or_quarantine(root, branch, tier)
        if refusal:
            _say(refusal, err=True)
            return 1
    return integrate.integrate(root, tier)


def _refresh_or_quarantine(root, branch, tier):
    """The §A2 refresh, with the §A3 red-handback ruling behind it. A refusal
    string, or None.

    A merged lane that reds the bar has broken something and is told so: its
    outcome ASSERTS the work is done, and the run stops for the lane to fix it.
    A lane that merged nothing asserts the opposite - it is handing the work
    back, or throwing it away - and stopping the run over red code nobody
    claimed was finished is exactly the hanging branch this design abolishes.
    So it is quarantined once (ruled option 1: revert the code, keep the failing
    diff as a bar-inert `.patch`) and refreshed again. Once, deliberately: a
    second red on a tree whose product changes have all been reverted is a real
    anomaly, not a case to loop on.
    """
    _sha, refusal = integrate.refresh(root, branch, tier)
    if not refusal:
        return None
    outcomes, unresolved = integrate.branch_outcomes(root, branch)
    if unresolved or "merged" in outcomes.values():
        return refusal
    _say("{} - quarantining it (§A3: it merges nothing).".format(refusal), err=True)
    refusal = handback.quarantine(root, branch, refusal)
    if refusal:
        return refusal
    _sha, refusal = integrate.refresh(root, branch, tier)
    return refusal


def _kind_action(kind, human_held, approval_held=False):
    """The §A8 policy table — what the dispatcher does with a frontier row of
    `kind`, and the one place this module must not invent policy:

        kind                  human-held tier      loop-held tier
        ordinary, critique    parallel             parallel
        high-risk, protected  exclusive            exclusive
        spine                 batch                batch
        attestation, gate     surface              exclusive

    `human_held` is the SN-029 comparison already made: is the tier this repo's
    spine is currently in process at still the human's to approve
    (`agent_common.human_holds`)? It replaces the three-value gate-authority enum,
    which could not express "TCs are human-held but LLRs are not" — the whole
    reason the approval dial became an ordinal read against the 0-5 spine
    stage ladder (the dial's own levels stay 0-4: the four SPINE tiers plus
    "nothing", and implementation is not an approval tier).

    A `spine` row dispatches EITHER WAY because building a scope change is
    WORK, not an approval — it opens a window; closing it is the next row's
    job. `attestation`/`gate` close a window, which on a human-held tier is the
    human's act (drain, surface the cards, exit 0) and otherwise dispatches — a
    recorded fresh-context reviewer verdict approves. The last arm also covers
    `adjudication`: exclusive, like every non-parallel kind.

    `approval_held` IS THE OFF-SPINE AXIS (owner ruling OI-30 D3, 2026-08-15),
    and it is a SECOND reason to surface rather than a widening of the first.
    `human_held` answers about the SPINE tier the repo is in; a WI whose action
    would move an `approval` cell in an off-spine registry is governed by THAT
    registry's own rung — `agent_common.human_approves(docs, registry)`, which
    reads the same `human_approval_through` dial through
    `agent_common.APPROVAL_RUNGS`. Either hold surfaces: a loop session must not
    write an approval a human owes, even on a spine tier the project has
    declared machine-approvable.

    IT DEFAULTS FALSE AND EVERY CALLER IN THIS MODULE PASSES THE DEFAULT, which
    is stated rather than hidden: NO WI KIND CARRIES A REGISTRY IDENTITY TODAY.
    The frontier is `(id, kind)` pairs, and threading a registry through
    admission to satisfy a rule with no live writer would be building the wrong
    half first. This parameter is the SEAM the rule is enforced at, placed so the
    caller that first learns which registry a row would touch has somewhere to
    say so — and `tests/test_approval_level.py` pins that no shipped loop
    module writes an `approval` cell in the meantime, which is the guard that
    actually bites today.

    Implements: SR-148, LLR-149
    """
    if kind in ("ordinary", "critique"):
        return "parallel"
    if kind == "spine":
        return "batch"
    if kind in ("attestation", "gate"):
        return "surface" if (human_held or approval_held) else "exclusive"
    return "exclusive"


def _judgement_first(ready_kinds):
    """SR-148 — DISPOSE FIRST: `adjudication` rows move to the head of
    the frontier, everything else keeping its relative order.

    A stable partition, not a re-sort: `schedule._KIND_RANK` is §A1's RULED
    table and is not renumbered here (renumbering it would migrate every
    downstream repo's ordering for a rung that belongs to admission anyway).
    Where the two disagree — and they disagree in exactly one place, spine
    (rank 0) vs adjudication (rank 1) — the loop-order contract wins AT
    ADMISSION only, and the rank table still gives `--explain` its total order.

    WHY dispositions outrank even a scope change: an adjudication row exists
    because a lane CLAIMED an outcome (a partial close, a cancellation, an
    amendment that may have moved meaning) and nothing has judged that claim
    yet. A spine batch re-attests requirements. Running the batch first
    re-approves a spine on a premise the pending judgement may overturn, and an
    approval is the one thing this loop cannot cheaply take back — the
    attestation ledger is append-only by design. Judge, then build."""
    return sorted(ready_kinds, key=lambda wk: wk[1] != "adjudication")


def _admission(ready_kinds, human_held, busy, free, keep_nondependent=False):
    """THE SPINE BARRIER, as a pure decision (§A4/§A8): what may start now?

    `ready_kinds` is the ordered frontier as `(wi_id, kind)` pairs (rank
    already sorted spine first), `human_held` the SN-029 comparison (is the
    tier in process still the human's to approve?), `busy` whether any lane is
    out, `free` how many lanes are open, and `keep_nondependent` the orthogonal
    dial an ordinal cannot carry — may other work keep running while an
    approval is queued? Returns `(verb, payload)`:

      ("admit", [batch, ...])       fill lanes with parallel rows, one per lane
      ("admit-exclusive", batch)    ONE batch that must run alone — all spine
                                    rows together, or the first exclusive row,
                                    or the queued approval batch at the
                                    close under `keep_nondependent`
      ("wait", [])                  an exclusive-kind row is pending: stop
                                    admitting and let the lanes come home
      ("surface", ids)              attestation/gate rows that may not dispatch
                                    at this level: drain, surface, exit 0
      ("empty", [])                 nothing ready at all

    The barrier property is the wait arm: any exclusive-kind row on the
    frontier (they all sort ahead of parallel kinds by rank) stops NEW
    admission outright — nothing slips past it into a free lane — and the
    batch admits only into an idle station, as the sole toucher of trunk.

    Implements: SR-148, LLR-149, LLR-159
    """
    if not ready_kinds:
        return "empty", []
    ready_kinds = _judgement_first(ready_kinds)
    surfaced = [w for w, k in ready_kinds if _kind_action(k, human_held) == "surface"]
    dispatchable = [
        (w, k) for w, k in ready_kinds if _kind_action(k, human_held) != "surface"
    ]
    if surfaced and not keep_nondependent:
        # The human-held stop (§A8 premise: once an approval is pending, no
        # work can be taken): drain and exit 0 into the owner's queue.
        return "surface", surfaced
    if not dispatchable:
        if not surfaced:
            return "empty", []
        # THE CLOSE UNDER `keep_nondependent`: the non-dependent work has all
        # drained and only the approval rows remain. They still SURFACE.
        #
        # This arm used to admit them, inherited from the retired
        # `single-approve` word — "dispatches only as the queued batch once
        # nothing else remains". Under the ordinal that is a contradiction:
        # `human_held` is TRUE here, which is the statement that this tier is
        # the human's to approve, and `keep_nondependent` answers an entirely
        # different question — may OTHER lanes keep running while a
        # approval is queued. Letting the second dial override the first is
        # the machine approving what a human declared theirs, reached by a
        # combination the enum could not even express (level 4 +
        # keep_nondependent, the fourth cell).
        if busy:
            return "wait", []
        return "surface", surfaced
    first_w, first_k = dispatchable[0]
    action = _kind_action(first_k, human_held)
    if action in ("batch", "exclusive"):
        if busy:
            return "wait", []
        if action == "batch":
            return "admit-exclusive", [w for w, k in dispatchable if k == first_k]
        return "admit-exclusive", [first_w]
    batches = [
        [w] for w, k in dispatchable if _kind_action(k, human_held) == "parallel"
    ]
    batches = batches[: max(0, free)]
    if not batches:
        return "wait", []
    return "admit", batches


def _lane_count(args, root):
    """The lanes dial (§A4.3, ruled 2026-07-31), on the established ladder:
    CLI --lanes > AGENT_LANES > docs/stack.ini [agent-loop] lanes > 1.

    The TEMPLATE seeds `lanes = 2` — the smallest count that proves the
    barrier, the merge slot and the refresh race are real rather than vacuous
    — but an ABSENT key means 1: docs/stack.ini is adopter-owned (a re-sync
    never overwrites it), so a kit-seeded key never appears in an existing
    adopter's file and a code default of 2 would have switched long-adopted
    repos from serial to concurrent SILENTLY on upgrade. A malformed or sub-1
    value falls to 1, loudly — fail toward serial, never toward concurrency."""
    declared = getattr(args, "lanes", None)
    if declared is None:
        raw = os.environ.get("AGENT_LANES", "").strip()
        if not raw:
            raw = ac.read_agent_loop_config(root / "docs").get("lanes", "")
        if not raw:
            return 1
        try:
            declared = int(raw)
        except ValueError:
            _say(
                "lanes value {!r} is not an integer - running serial (lanes=1)".format(
                    raw
                ),
                err=True,
            )
            return 1
    if declared < 1:
        _say(
            "lanes value {} is below 1 - running serial (lanes=1)".format(declared),
            err=True,
        )
        return 1
    return declared


def _branch_exclusive(root, branch):
    """Must this claimed branch run ALONE? Read off the TRUNK's claimed specs,
    the same one-home read the merge slot uses for outcomes — a parked branch
    predates this run, so its kind exists nowhere else. Unreadable
    frontmatter fails toward exclusivity, never toward sharing the station."""
    specs = integrate._claimed_specs(root, branch)
    for _wid, name in specs:
        try:
            meta = integrate._spec_frontmatter(root / integrate.ACTIVE / branch / name)
        except (OSError, ValueError):
            return True
        if (meta.get("safety_class") or "").strip().lower() != "ordinary":
            return True
    return False


# The exit codes a worker DECIDES on: it ran, reached a conclusion, and said so.
# Every one of them is a lane that cannot finish, which under §A3 is a HANDBACK
# — the lane closes into trunk and the run keeps going. Anything else (a
# traceback's 1, a signal, a killed process) is a CRASH, which is deliberately
# NOT a hang and keeps the machinery that already handles it: the branch exists,
# the specs are still in active/<branch>/, so the next cycle's _parked_branches
# re-assigns a lane to it and the stall guard bounds a worker that keeps dying.
#
# `EXIT_TRAIN_END` (10) is deliberately NOT here, and as of WI-383 the constant
# it named no longer exists: session grouping is gone (§A6.1) and
# `agent_common` keeps only a note reserving the number. This set was written
# without it while that deletion was still in flight on a sibling lane —
# naming it would have made this module an AttributeError at import the moment
# the two merged. A code no worker emits needs no arm; were one ever to arrive
# it falls to the crash path, which parks and resumes rather than deciding an
# outcome on behalf of a worker that decided none.
#
# A TRADE THIS SET MAKES, stated here rather than left in the literal (REVIEW-A
# round 1). `EXIT_BUDGET` and `EXIT_STALL` are RESUMABLE conditions: before
# WI-387 a worker that hit its session ceiling stopped the run with the claim
# parked, and a relaunch resumed the same lane, so a WI needing more than one
# worker budget finished across relaunches with no human in the loop. They are
# decided exits, so they now hand back — and `hand_back` sets a `blockref`,
# which `schedule._disposition` reads as `blocked`, so an unattended run can
# never pick that WI up again until a human clears it. §A3's ruling is "any
# non-zero worker exit that is not a crash", and its justification (the dominant
# shape is green-but-not-approved or cannot-proceed-for-config-reasons) is about
# EXIT_NEEDS_HUMAN, not about a ceiling. The alternative — hand back WITHOUT a
# blockref so a ceiling stays resumable — re-opens the claim/return/re-claim
# loop this row closed, bounded then only by --max-iterations, so it is an owner
# call rather than a builder's: filed as a finding, not decided here.
_WORKER_OUTCOMES = frozenset(
    {
        ac.EXIT_PREFLIGHT,
        ac.EXIT_BLOCKED,
        ac.EXIT_STALL,
        ac.EXIT_WAITING,
        ac.EXIT_BUDGET,
        ac.EXIT_NEEDS_HUMAN,
        ac.EXIT_PAUSED,
    }
)


def _lane_close(root, branch, code):
    """What a non-DONE worker outcome does to the lane: None to keep driving,
    else the exit code the run ends with (§A3).

    THE RUN-STOPS THIS REPLACES. `EXIT_NEEDS_HUMAN` used to end the whole drive
    loop and any other non-zero exit stopped it with the branch parked — so one
    WI wanting a human froze a walk-away run, and its partial work sat where
    nobody would find it. Neither is an exceptional outcome that deserves an
    exceptional path: the lane hands back, the WI returns to trunk blocked and
    visible on the owner surface, and the dispatcher moves to the next one.

    A lane that ALREADY CLOSED its specs is left alone whatever it exited with.
    Its tree has already named an outcome — `complete/`, `cancelled/`, wherever
    it moved them — and the drain will merge it on that. Handing it back would
    be the dispatcher overruling the tree with an exit code, and it cannot anyway:
    `hand_back` reads the claimed spec out of `active/<branch>/` in the LANE,
    where a closed lane no longer has one, so it failed with an OSError and
    stopped the run over a branch that would have merged cleanly (REVIEW-A
    round 1, driven — a review escalation lands at the END of a lane, which is
    exactly when the close may already be written).

    A failed handback DOES stop the run, and must: it is the one state the
    invariant cannot express, so it is reported rather than driven past.
    """
    if branch in integrate.finished_branches(root):
        _say(
            "worker on {} exited {} but its specs are already out of active/ - "
            "the tree has named an outcome, so the drain merges it on that "
            "rather than handing back over the top of it.".format(branch, code)
        )
        return None
    if code == ac.EXIT_REVIEW_OWED:
        # C2 (docs/plans/2026-08-30-stall-guard-plan.md): the build is
        # committed and no reviewer could be drawn. Deliberately parked, not
        # decided — the next cycle resumes the lane, whose worker schedules
        # the owed round first (the out/review-owed marker). A reviewer
        # outage never hands finished work back (owner direction 2026-08-30).
        _say(
            "worker on {} exited REVIEW OWED (exit {}) - the build is "
            "committed and no reviewer could be drawn; the lane stays parked "
            "with its work and the next cycle resumes it to draw the "
            "round.".format(branch, code)
        )
        return None
    if code not in _WORKER_OUTCOMES:
        _say(
            "worker on {} CRASHED (exit {}) - the claim stays in active/{}/ "
            "and the next cycle resumes it; a worker that keeps dying trips "
            "the stall guard.".format(branch, code, branch),
            err=True,
        )
        return None
    reason = "worker exit {}{}".format(
        code, " (NEEDS-JUDGEMENT)" if code == ac.EXIT_NEEDS_HUMAN else ""
    )
    # SR-144: the dispatcher's own close carries the TYPED fields the report
    # schema declares, rather than smuggling them through the reason string.
    # (SR-144 owns the report's SHAPE; LLR-161 owns what the disposition row
    # minted from it may then do — lineage, not fields.)
    # The tier is keyed off the EXIT-CODE CLASS — a fact the dispatcher already
    # holds — not off a substring of prose: `NEEDS_HUMAN`, `needs human` or any
    # typo used to downgrade a disposition silently, because a case-folded
    # search for `NEEDS-HUMAN` was the tier's only input. The label in the
    # reason is now decoration; the field is the contract.
    fields = {
        "suggested_tier": "strong" if code == ac.EXIT_NEEDS_HUMAN else "medium",
        # THE DISPATCHER CANNOT JUDGE THE KEEP/DISCARD SPLIT and says so, in a
        # typed field, rather than leaving the report silent. It has no view of
        # the work at all — the worker exited or crashed — so the honest answer
        # is that the split is OWED, and the disposition row this close mints is
        # what owes it. Silence here is the shape that let a rejected diff merge
        # as-is; an explicit deferral is not.
        "split_decided_by": "adjudicator",
        "not_delivered": (
            "The worker exited {} before moving its specs out of active/{}/, "
            "so nothing in this row's Done-when can be assumed met. Read the "
            "commit range above.".format(code, branch)
        ),
    }
    _ids, refusal = handback.close_partial(root, branch, reason, fields)
    if refusal:
        _say("cannot close {} as partial: {}".format(branch, refusal), err=True)
        return ac.EXIT_PREFLIGHT
    return None


class _Lane:
    """One live lane, dispatcher-side: which branch, which WIs, which phase.

    The MECHANICS live in lane.py (the worker subprocess, the refresh
    subprocess); this record is only the dispatcher's bookkeeping. There is
    deliberately no state FILE (§A4.2): the tree signals (specs moved out of
    active/<branch>/) plus these in-memory handles are the whole protocol, so
    a crashed dispatcher leaves nothing to reconcile beyond the parked
    branches the next run already resumes."""

    def __init__(self, branch, wi_ids, exclusive, head):
        self.branch = branch
        self.wi_ids = list(wi_ids)
        self.exclusive = exclusive
        self.head = head  # trunk head at admission — the stall baseline
        self.phase = "worker"  # -> "refresh" -> closed (removed from table)
        self.proc = None  # the live subprocess handle of the current phase
        self.code = None  # a sync-injected worker's already-decided exit
        self.retried = False  # the one §A3 quarantine retry


def _launch(root, table, branch, wi_ids, exclusive, args, worker):
    """Create the live lane record for `branch` and start its worker — the
    injected sync callable (tests), or lane.py's real subprocess. The lane is
    ALWAYS appended: a spawn failure becomes the lane's own EXIT_PREFLIGHT
    outcome, so it closes through the one §A3 decision path (`_lane_close`)
    instead of a side exit."""
    ln = _Lane(branch, wi_ids, exclusive, ac.git(root, "rev-parse", "HEAD")[1].strip())
    if worker is not None:
        ln.code = worker(root, branch, wi_ids, args)
    else:
        proc, err = lane.spawn_worker(root, branch, wi_ids, args)
        if err:
            _say(err, err=True)
            ln.code = ac.EXIT_PREFLIGHT
        else:
            ln.proc = proc
    table.append(ln)


def _advance(root, ln, tier):
    """Advance one lane's state machine by one poll: None while busy, else a
    `(verb, code)` event —

      ("merged", 0)     the lane's branch merged through the slot; lane closed
      ("closed", None)  closed without a merge: a crash (parked for the next
                        tick's resume) or a DONE worker that finished nothing
                        (the stall candidate)
      ("fatal", code)   the run must end with `code` once the station drains
    """
    if ln.phase == "worker":
        code = ln.code if ln.proc is None else ln.proc.poll()
        if code is None:
            return None
        ln.proc = None
        if code != ac.EXIT_DONE:
            rc = _lane_close(root, ln.branch, code)
            if rc is not None:
                return ("fatal", rc)
        if ln.branch in integrate.finished_branches(root):
            # The lane's tree named an outcome — run ITS refresh in ITS own
            # subprocess (§A4.3: N bars must overlap, not queue here).
            ln.phase = "refresh"
            ln.proc = lane.spawn_refresh(root, ln.branch, tier)
            return None
        return ("closed", None)
    rc = ln.proc.poll()
    if rc is None:
        return None
    ln.proc = None
    if rc == 0:
        # THE MERGE SLOT, scoped to this lane's branch: another lane may be
        # mid-refresh on its own branch and must not be pulled into the slot
        # half-attested.
        code = integrate.integrate(root, tier, branches=[ln.branch])
        if code != 0:
            return ("fatal", code)
        return ("merged", 0)
    return _refresh_failed(root, ln, tier, rc)


def _refresh_failed(root, ln, tier, rc):
    """The §A3 red-refresh ruling for a lane whose refresh subprocess exited
    nonzero — the same decision `_refresh_or_quarantine` makes for residue
    branches, read off the subprocess's exit code (its refusal detail is its
    own stderr in the walk-away log, plus the retained out/run-logs file):
    fatal for a branch that asserts DONE, quarantine-once for one that merges
    nothing, and a second red after the quarantine is a real anomaly."""
    outcomes, unresolved = integrate.branch_outcomes(root, ln.branch)
    if unresolved or "merged" in outcomes.values() or ln.retried:
        _say(
            "the refresh is RED for {} (exit {}){} - the reason is printed "
            "above by the refresh itself; the run stops for the lane to fix "
            "it.".format(ln.branch, rc, " after its quarantine" if ln.retried else ""),
            err=True,
        )
        return ("fatal", 1)
    _say(
        "refresh exit {} for {} - quarantining it (§A3: it merges nothing).".format(
            rc, ln.branch
        ),
        err=True,
    )
    refusal = handback.quarantine(
        root,
        ln.branch,
        "the §A2 refresh bar refused (exit {}; see the run log above and "
        "out/run-logs/refresh-refused-*.log)".format(rc),
    )
    if refusal:
        _say("cannot quarantine {}: {}".format(ln.branch, refusal), err=True)
        return ("fatal", 1)
    ln.retried = True
    ln.proc = lane.spawn_refresh(root, ln.branch, tier)
    return None


def _poll(root, table, args, tier, state):
    """One poll pass over the live lanes; True when any lane moved. Outcome
    bookkeeping: a merge resets the stall counter, a lane that closed with
    the trunk exactly where its admission found it increments it (a worker
    that keeps reporting DONE without finishing cannot loop forever), and the
    first fatal event freezes admission while the station drains."""
    event = False
    for ln in list(table):
        adv = _advance(root, ln, tier)
        if adv is None:
            continue
        event = True
        verb, code = adv
        table.remove(ln)
        if verb == "fatal":
            if state["fatal"] is None:
                state["fatal"] = code
        elif verb == "merged":
            # WI(s), NOT lanes: an exclusive spine batch is ONE branch carrying
            # several WIs, so crediting the lane under-reports exactly the
            # admission path the barrier exists for (REVIEW-A finding 1).
            state["merged"] += len(ln.wi_ids)
            state["stall"] = 0
        else:
            head_now = ac.git(root, "rev-parse", "HEAD")[1].strip()
            state["stall"] = state["stall"] + 1 if head_now == ln.head else 0
            if state["stall"] >= max(1, args.stall_limit):
                _say(
                    "STALL - {} consecutive cycle(s) left the trunk unmoved; "
                    "aborting rather than looping.".format(state["stall"]),
                    err=True,
                )
                if state["fatal"] is None:
                    state["fatal"] = ac.EXIT_STALL
    return event


def _cycle_gate(args, table, state):
    """May another lane be admitted inside the iteration budget? "ok" to
    admit, "wait" to let the live lanes drain first, "budget" to end the run
    (station idle, ceiling reached, work remaining)."""
    if state["cycles"] < max(1, args.max_iterations):
        return "ok"
    return "wait" if table else "budget"


def _budget_exit(args, state):
    _say(
        "iteration ceiling ({}) reached with work remaining - relaunch to "
        "continue ({} WI(s) integrated this run).".format(
            args.max_iterations, state["merged"]
        ),
        err=True,
    )
    return ac.EXIT_BUDGET


def _pending_cards(root):
    """The pending owner cards, from the SAME `pending_block(root)` read the
    dashboard and open-items.html share (the WI-381 amendment, ruled
    2026-08-01: gen_open_items renders `pending.pending_block` verbatim, and
    the dispatcher's exit banner must derive from that one read so
    agent-resume and the owner surfaces can never disagree about what is
    blocking). Blocked rows with a BlockRef plus Drafted/drifted spine rows;
    the tracked-pause card is excluded because a pause has its own earlier
    exit, and the coordinator's git-trailer reads stay for in-flight lanes
    only.

    THE IMPORT MOVED AT WI-483 SLICE 3, and the move is the point. It used to
    be the FACADE — `import gen_trajectory`, reaching in for the private
    `_blocked_pending` and `_spine_pending` — which the 2026-08-19 review
    recorded twice over: a ~1,000-line render family imported for a state
    query, through private names used as a cross-module API (H-02, M-02). The
    old judgment note argued the facade crossed no *forbidden* seam, which was
    true and beside the point: a scheduling composer does not depend on a
    dashboard to learn what the owner owes. The derivation now sits in
    `pending.py`, below all three of its readers, and this asks it in its own
    vocabulary — `owner_cards`, which is `pending_items` minus the pause,
    declared once there rather than re-assembled here from two of the three
    sources. Still deferred, so the tick loop pays the read only at an exit
    banner."""
    import pending

    return pending.owner_cards(root)


def _surface_banner(root, surfaced):
    """The §A8 attended stop's banner: exit 0, naming what waits — and naming
    the RIGHT surface, which is the whole of this row (REVIEW-A finding 1).

    The count used to be `max(cards, surfaced)`. That did not merely
    over-report, it MISLABELED: with a queued gate row and zero pending cards
    it sent the owner to open-items.html to read "None - no durable owner
    action is pending", exactly the disagreement the ruled amendment forbids
    ("must derive from the SAME pending_block(root) read ... can never
    disagree").

    THE JUDGMENT, REVISED UNDER REVIEW. The first attempt made the two arms
    exclusive: cards if any exist, else the queued rows. That still could not
    disagree with `pending_block`, but review drove the cost — one unrelated
    card silently SUPPRESSED two genuinely queued attestation rows, hiding
    work the owner had every reason to see. The reason given for suppressing
    them (that the populations overlap, since `_pending_cards` yields blocked
    rows with a BlockRef plus Drafted/drifted spine rows while `surfaced`
    yields queued gate/attestation frontier rows, and one row can be both)
    justifies never SUMMING them — it does not justify hiding one.

    So both are named, separately labelled, never added together, with the
    possible overlap stated in the line itself. A reader can see each source
    for what it is; no arithmetic asserts a total that neither read supports;
    and the cards arm still says exactly what it always said, off the shared
    read the amendment names."""
    cards = len(_pending_cards(root))
    queued = len(surfaced)
    if cards and queued:
        return (
            "queue drained - {} approval(s) waiting in open-items.html; "
            "{} queued attestation row(s) on the frontier (the two reads may "
            "name the same row)".format(cards, queued)
        )
    if cards:
        return "queue drained - {} approval(s) waiting in open-items.html".format(cards)
    return (
        "queue drained - {} queued attestation row(s); no card has projected "
        "to open-items.html yet".format(queued)
    )


# --- the registry-gap census, re-exported ------------------------------------
#
# THE CENSUS MOVED DOWN (WI-483 slice 2). It used to be defined here, which made
# every reader of a census line import the scheduling composer to reach it —
# including `intake`, whose deferred `import dispatch` was a back edge of the
# five-module strongly connected component the 2026-08-19 review recorded
# (H-02). The census reads registries and decides nothing about lanes, so it now
# lives in the sibling `census.py`, below all three of its readers. IF-089 moved
# with it.
#
# These aliases exist so no caller had to move: the dispatcher's own rung-1 call
# below, and the station render's pin on `dispatch.gap_census`, both still read
# the names they always did. Same shape as `integrate`'s re-export of the
# lane-close outcome vocabulary after slice 1.
gap_census = census.gap_census
red_tc_census = census.red_tc_census
parse_red_tc = census.parse_red_tc
RED_TC_PREFIX = census.RED_TC_PREFIX


def _pre_admit(args, table, state, config_refusal):
    """The rungs every admission owes before a lane may launch — the session
    config preflight (applied only when work actually needs a worker), then
    the iteration budget. `(action, code)`: "ok" to admit, "hold" to let the
    live lanes drain first, "exit" to end the run with `code`."""
    if config_refusal:
        if table:
            return "hold", None
        _say(config_refusal, err=True)
        return "exit", ac.EXIT_PREFLIGHT
    gate = _cycle_gate(args, table, state)
    if gate == "wait":
        return "hold", None
    if gate == "budget":
        return "exit", _budget_exit(args, state)
    return "ok", None


def _admit_parked(root, table, args, worker, parked, free, config_refusal, state):
    """Resume interrupted lanes first — an unfinished claim must come home
    before any barrier can open. `(admitted, exit_code)`."""
    admitted = False
    for branch in parked:
        if free <= 0:
            break
        excl = _branch_exclusive(root, branch)
        if excl and table:
            break  # an exclusive resume waits for an idle station
        action, code = _pre_admit(args, table, state, config_refusal)
        if action != "ok":
            return admitted, code
        state["cycles"] += 1
        wi_ids = integrate._claimed_wi_ids(root, branch)
        _say(
            "cycle {} - resuming parked branch {} ({})".format(
                state["cycles"], branch, ";".join(wi_ids)
            )
        )
        _launch(root, table, branch, wi_ids, excl, args, worker)
        admitted = True
        free -= 1
        if excl:
            break
    return admitted, None


def _claim_lanes(root, table, args, worker, batches, exclusive, config_refusal, state):
    """Claim and launch one lane per batch. `(admitted, exit_code)`. A claim
    refusal stops the run (never skipped, never talked past) — with lanes
    live it freezes admission and lets the station drain first."""
    admitted = False
    for batch in batches:
        action, code = _pre_admit(args, table, state, config_refusal)
        if action != "ok":
            return admitted, code
        branch = _branch_for(root, batch[0])
        if (
            branch is None
            or ac.git(root, "check-ref-format", "--branch", branch)[0] != 0
        ):
            _say(
                "no single queued spec matches {}, or its filename does not map "
                "to a valid git branch name - fix the spec folder, then "
                "relaunch".format(batch[0]),
                err=True,
            )
            if table:
                state["fatal"] = (
                    ac.EXIT_PREFLIGHT if state["fatal"] is None else state["fatal"]
                )
                return admitted, None
            return admitted, ac.EXIT_PREFLIGHT
        state["cycles"] += 1
        _say(
            "cycle {} - claiming {} on {}{}".format(
                state["cycles"],
                ";".join(batch),
                branch,
                " (exclusive)" if exclusive else "",
            )
        )
        code = integrate.claim(root, batch, branch, dispatch_lock_held=True)
        if code != 0:
            if table:
                state["fatal"] = code if state["fatal"] is None else state["fatal"]
                return admitted, None
            return admitted, code
        _launch(root, table, branch, batch, exclusive, args, worker)
        admitted = True
    return admitted, None


def _admit(
    root,
    table,
    args,
    worker,
    tier,
    human_held,
    keep_going,
    lanes_total,
    config_refusal,
    state,
):
    """One tick's admission, enacted: `(admitted, exit_code)`. The exit code
    is non-None only when the run ends here — the drained queue, the surfaced
    approvals, a refusal — and only ever with the station idle."""
    exclusive_live = any(ln.exclusive for ln in table)
    free = 0 if exclusive_live else max(0, lanes_total - len(table))
    if free == 0:
        return False, None
    busy = bool(table)
    live = {ln.branch for ln in table}
    parked = [b for b in _parked_branches(root) if b not in live]
    if parked:
        return _admit_parked(
            root, table, args, worker, parked, free, config_refusal, state
        )
    wis = schedule._load(root)
    ready = [r for r in schedule.frontier(wis) if r["status"] == "queued"]
    kinds = {w["id"]: schedule.kind_of(w) for w in wis}
    verb, payload = _admission(
        [(r["id"], kinds.get(r["id"])) for r in ready],
        human_held,
        busy,
        free,
        keep_going,
    )
    if verb in ("surface", "empty"):
        if busy:
            return False, None  # drain the lanes, THEN exit into the queue
        return False, _station_exit(root, tier, verb, payload, state)
    if verb == "wait":
        return False, None
    if verb == "admit-exclusive":
        # THE BARRIER OPENS. The station is idle by construction (`_admission`
        # answers wait while any lane is out); settle any residue so the batch
        # runs as the sole toucher of trunk.
        #
        # COUNT IT BEFORE THE DRAIN, exactly as `_station_exit` does: after
        # the drain those branches have merged and are no longer residue, so
        # the number is unrecoverable at exit. Crediting it here is what keeps
        # the banner's contract — every WI integrated in the run is counted,
        # whatever admission path merged it — true for the barrier-open arm
        # too (WI-412, WI-381 REVIEW-A finding 3; the same undercount rounds 1
        # and 2 fixed for the exit arm). Credited only on a GREEN drain - a
        # red one CAN also have merged branches, but that arm prints no count,
        # so there is nothing to misreport (see `_drain`).
        residue = _residue_wi_count(root)
        code = _drain(root, tier)
        if code != 0:
            return False, code
        state["merged"] += residue
        return _claim_lanes(
            root, table, args, worker, [payload], True, config_refusal, state
        )
    return _claim_lanes(
        root, table, args, worker, payload, False, config_refusal, state
    )


def _station_exit(root, tier, verb, payload, state):
    """The run's honest ends, station idle: the surfaced-approval stop
    (§A8 attended: drain, leave the cards, exit 0) and the drained queue — or,
    on rung 1, NOT an end at all: a minted gap row re-fills the frontier and
    the return is None (keep driving). A finished branch may still be waiting
    (e.g. built by hand between runs), so every arm drains the residue first —
    and the drained banner COUNTS what that drain merges (REVIEW-A round 1:
    the banner undercounted residue)."""
    residue = _residue_wi_count(root)
    code = _drain(root, tier)
    if code != 0:
        return code
    if verb == "surface":
        _say(_surface_banner(root, payload))
        return ac.EXIT_DONE
    # THE EMPTY-FRONTIER LADDER (§A4 amendment, ruled 2026-08-01), replacing
    # the bare queue-drained exit. Rung 1: a mechanical gap census — HANDED to
    # the WI-388 intake mint, which turns each gap into a concrete gap-closure
    # row (derived description, no model in the path) and dedupes against the
    # rows that already exist, so the ladder cannot mint one gap forever.
    # Rung 2: census empty but a pending attestation exists — that is not
    # missing work; the cards are on open-items.html and the banner counts
    # them off the shared read. Rung 3: census empty and registries complete —
    # honest drain.
    census = gap_census(root)
    if census:
        minted, refusal = intake.mint_gap_rows(root, census)
        if refusal:
            _say(refusal, err=True)
            return 1
        if minted:
            _say(
                "empty frontier - {} registry gap(s); minted {} gap-closure "
                "row(s) at intake (WI-388, docs/concurrency-v2.md §A5.2): "
                "{}.".format(len(census), len(minted), ", ".join(w for w, _ in minted))
            )
            return None  # the frontier is no longer empty — keep driving
        for line in census:
            _say("gap census: {}".format(line))
        _say(
            "empty frontier - {} registry gap(s) named above already carry "
            "minted rows (open or built); nothing new to mint - the remainder "
            "is the owner's to read.".format(len(census))
        )
        return ac.EXIT_DONE
    cards = _pending_cards(root)
    if cards:
        _say(
            "queue drained - {} approval(s) waiting in open-items.html".format(
                len(cards)
            )
        )
        return ac.EXIT_DONE
    drained = (
        "queue drained - no ready work items; {} WI(s) integrated this run.".format(
            state["merged"] + residue
        )
    )
    # SN-029's separate end-of-run hold. The ordinal answers "which TIER is the
    # human's"; this answers "do I get a last look before the run walks away",
    # and they are different questions — which is exactly why it is its own
    # dial. Without a reader it was a declared, type-checked promise that
    # nothing kept: a run at level 0 with `final_review = "always"` closed
    # silently, which is the state an owner sets this dial to prevent.
    _say(drained)
    if ac.final_review(root / "docs"):
        # EXIT_DONE, deliberately, and this is the part worth being careful
        # about. `NEEDS-HUMAN` means BLOCKED — something is owed before work can
        # continue — and a clean drain is the opposite of that: everything
        # merged, the bar is green, nothing is owed by the machine. Returning 7
        # here would make every successful walk-away run report failure to the
        # launchers, which is how a dial meant to add a READ ends up inverting
        # an exit-code contract.
        #
        # What the dial actually buys is that the run does not close SILENTLY:
        # the loop stops (this IS the end of the run) and says so loudly enough
        # that a human reads it rather than discovering it in a log later.
        _say(
            "FINAL REVIEW - the run is COMPLETE and nothing is blocked, but "
            "docs/process.toml [attestation] final_review is not 'off', so it "
            "ends here for a human read rather than closing quietly. Read the "
            "run; set the dial to 'off' when you no longer want the stop."
        )
    return ac.EXIT_DONE


# The tick loop's poll cadence while lanes are busy: long enough not to spin,
# short enough that a finished worker starts its refresh promptly (the bars
# behind it run minutes, so half a second is noise).
_POLL_SECONDS = 0.5


def run(root, args, worker=None, tier="all"):
    """The dispatch loop (docs/concurrency-v2.md §A4). `worker` is the one
    injection seam (tests): a callable `(root, branch, wi_ids, args) -> exit
    code` standing in for the worker session launch, run synchronously at
    admission; None means lane.py's real subprocess launch. `tier` is the bar
    tier the §A2 refresh runs (default: the full gate bar).

    EACH TICK: poll the live lanes (a worker exit decides an outcome; a
    finished branch refreshes in its own subprocess; a green refresh merges
    through the slot), then admit per `_admission` — the §A8 policy table plus
    the spine barrier. A fatal event (a red refresh of a done-asserting
    branch, a failed handback, a merge refusal, the stall guard) freezes
    admission at once, drains the in-flight lanes, and exits with the first
    fatal code.

    Lock note: the plain-launch caller (agent_loop) holds the DISPATCH lock
    (out/agent-loop.lock) for the process lifetime — which is why the claims
    here pass `dispatch_lock_held=True`, and why a hand `integrate claim`
    against a live dispatcher cannot happen at all (§A4.1). integrate.py takes
    and releases its own out/integrate.lock per merge inside the same process;
    agent_common keeps one held-descriptor slot, so the coordinator lock's
    descriptor is simply left to the OS's exit-time release — exactly the
    guard's intended span.
    """
    lanes_total = _lane_count(args, root)
    # SN-029: one ordinal comparison, made once per run, threaded down exactly
    # as the enum was. `spine_stage_of` reads the tier currently in process
    # through `kitlib.stage.read_stage`; `human_holds` compares it against the
    # declared `human_approval_through`.
    human_held = ac.human_holds(root / "docs", ac.spine_stage_of(root))
    keep_going = ac.keep_nondependent(root / "docs")
    # Computed once, APPLIED lazily: admission refuses on it only when work
    # actually needs a worker, so an empty queue still drains to exit 0 on an
    # unwired scaffold (the spec's empty-frontier contract; codex
    # cross-review finding, round 1).
    config_refusal = _session_config_refusal(root, args) if worker is None else None
    state = {"merged": 0, "stall": 0, "cycles": 0, "fatal": None}
    table = []
    while True:
        # WI-540: keep a retained adjudicator session's prompt cache warm
        # (plan §3.5). A no-op when the dial ships off; guarded so it can never
        # wedge the loop.
        _keepwarm_tick(root, table, time.time())
        # The pause is checked at the top of every tick so one appearing
        # MID-RUN stops the next claim, not just the first (§5.6: pause means
        # stop claiming; in-flight lanes finish and integrate first).
        paused = ac.tracked_pause(root / "docs")
        if paused is not None and not table:
            _say(
                "PAUSED - docs/work/pause is present (since {}: {}); {} WI(s) "
                "integrated before the stop. Unpausing is a reviewed deletion "
                "commit.".format(
                    paused.get("since", ""), paused.get("reason", ""), state["merged"]
                ),
                err=True,
            )
            return ac.EXIT_PAUSED
        # The claim rung's clean-trunk refusal, hoisted to the tick top so the
        # PARKED-resume path meets it too; with lanes live it only freezes
        # admission (their own merges refuse on dirt by themselves).
        dirty = ac.working_tree_dirty(root)
        if dirty and not table:
            _say(
                "the trunk working tree is dirty - claims, resumes and merges "
                "all need a clean trunk; commit or stash it, then relaunch "
                "({} WI(s) integrated before the stop).".format(state["merged"]),
                err=True,
            )
            return ac.EXIT_PREFLIGHT

        event = _poll(root, table, args, tier, state)
        if state["fatal"] is not None:
            if table:
                time.sleep(_POLL_SECONDS)
                continue
            return state["fatal"]

        admitted = False
        if paused is None and not dirty:
            admitted, code = _admit(
                root,
                table,
                args,
                worker,
                tier,
                human_held,
                keep_going,
                lanes_total,
                config_refusal,
                state,
            )
            if code is not None:
                return code
        if not (event or admitted):
            # Nothing moved this tick: wait for a subprocess rather than spin.
            time.sleep(_POLL_SECONDS if table else 0.05)
