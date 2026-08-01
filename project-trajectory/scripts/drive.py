"""drive.py — the serial claim->build->integrate driver (the scheduling front end).

WI-374: concurrency-restructure Phase 5 deleted the parallel dispatcher, and
job 2 of that module — read the ready frontier, claim the next WI, launch a
worker, merge — went out with job 1 (the train/worktree/reservation bloat).
This module restores job 2 and ONLY job 2: a plain `agent-resume` launch
(agent_loop.py with no role, IF-015) lands here instead of refusing, and the
driver joins the four existing, independently-proven parts in one serial lane:

    schedule.py frontier (IF-053)  ->  next ready WI in build order
    integrate.py claim   (IF-080)  ->  the §2.3 trunk claim + branch cut
    agent_loop.py --wi   (IF-015)  ->  one worker session on the claimed branch
    integrate.py refresh (IF-080)  ->  the §A2 station refresh, OUTSIDE the slot
    integrate.py integrate (IF-080) -> the merge slot

The frontier is re-derived from the registry at the top of EVERY cycle, so a
WI filed mid-run (by a worker, a review, or a human) is picked up in the same
run — no restart needed.

Adds ORDERING only, no authority: every refusal stays where it already lives
(the tracked docs/work/pause, a dirty trunk, the SpecRef and status-prose
claim rungs, the §A2 refresh bar, the RULING-7 verdict gate,
docs/push-policy). Any refusal from a composed part STOPS the run loudly —
the driver never skips past one, never force-merges, and NEVER pushes (there
is deliberately no flag to ask it to; docs/push-policy is honored by
construction). A parked claimed branch from an interrupted run is resumed
(worker relaunched on it) rather than refused, so the walk-away loop restarts
with the same double-click that started it.

Explicitly NOT here, by spec: worktree pools, reservations, train grouping,
run-state files, disposition arms. If a change starts to grow this module
toward the deleted dispatcher's shape, stop and escalate as a written case
(process-options.md, the design-escalation clause).

Contracts: IF-015 (the plain-launch drive mode is agent_loop.py's seam; this
module is its implementation, invoked only via agent_loop or in-process).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import agent_common as ac
import integrate
import schedule

SCRIPTS = Path(__file__).resolve().parent

# The lane worktree home is integrate.py's to name: the worker builds there and
# the station refresh runs there, so the two must agree by construction rather
# than by two matching literals.
WORKTREE_SUFFIX = integrate.LANE_WORKTREE_SUFFIX


def _say(msg, err=False):
    print("drive: {}".format(msg), file=sys.stderr if err else sys.stdout, flush=True)


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


def _default_worker(root, branch, wi_ids, args):
    """Launch one worker session loop on the claimed branch's worktree and
    return its exit code. Stdio is inherited so the walk-away console shows the
    worker's own live echo; AGENT_CMD and the routing env pass through the
    environment exactly as an attended launch would see them."""
    wt, err = integrate.lane_worktree(root, branch)
    if err:
        _say(err, err=True)
        return ac.EXIT_PREFLIGHT
    argv = [
        str(ac.harness_python(root)),
        str(SCRIPTS / "agent_loop.py"),
        "--worktree",
        str(wt),
        "--wi",
        ";".join(wi_ids),
        "--train",
        branch,
    ]
    if args.agent_cmd is not None:
        argv += ["--agent-cmd", args.agent_cmd]
    if args.session_timeout:
        argv += ["--session-timeout", str(args.session_timeout)]
    if args.no_session_echo:
        argv += ["--no-session-echo"]
    if args.live_status:
        argv += ["--live-status"]
    # The plain launch's session dials ride to the worker EXPLICITLY - env
    # inheritance covers the launcher-set slots, but a flag given on the
    # command line would otherwise be silently dropped (codex cross-review
    # finding, WI-374 round 1). model/model-map arrive here already resolved
    # (CLI > env > stack.ini), so forwarding them as flags preserves exactly
    # the plain launch's resolution.
    for flag, value in (
        ("--model", args.model),
        ("--model-map", args.model_map),
        ("--cmd-map", args.cmd_map),
        ("--prompt-map", args.prompt_map),
        ("--tier-map", args.tier_map),
        ("--prefer-map", args.prefer_map),
        ("--stall-limit", str(args.stall_limit)),
    ):
        if value:
            argv += [flag, value]
    if args.wait_on_limit:
        argv += [
            "--wait-on-limit",
            str(args.wait_on_limit),
            "--limit-retry-fallback",
            str(args.limit_retry_fallback),
        ]
    proc = subprocess.run(argv, cwd=str(root), stdin=subprocess.DEVNULL)
    return proc.returncode


def _session_config_refusal(root, args):
    """The pre-claim config preflight: an empty AGENT_CMD with no
    managed-routing enable-list means every worker would refuse at its own
    preflight - AFTER the claim had already parked a branch. Refuse here
    instead, with nothing claimed yet. Returns the refusal string, or None."""
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


def _drain(root, tier):
    """Refresh every finished branch, then run the merge slot. An exit code.

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

    A red refresh STOPS the run - it is the same failure a red merge bar used
    to be, moved to where the lane that caused it can fix it.
    """
    for branch in integrate.finished_branches(root):
        _sha, refusal = integrate.refresh(root, branch, tier)
        if refusal:
            _say(refusal, err=True)
            return 1
    return integrate.integrate(root, tier)


def _stranded_claims(root):
    """active/<branch>/ directories that still hold specs but whose branch ref
    is GONE — a half-completed claim (the trunk commit landed, the branch cut
    or a later deletion did not). Invisible to both the frontier (the WI is
    `active`) and the parked-resume read (no ref), so without this check a
    run would report the queue DRAINED over work nobody can reach (codex
    cross-review finding, WI-374 round 1)."""
    active = root / "docs" / "work" / "active"
    if not active.is_dir():
        return []
    return [
        p.name
        for p in sorted(active.iterdir())
        if p.is_dir()
        and any(p.glob("WI-*.md"))
        and ac.git(root, "rev-parse", "--verify", "--quiet", "refs/heads/" + p.name)[0]
        != 0
    ]


def _resume_or_claim(root, cycle, tier, merged, config_refusal):
    """One cycle's assignment: `(branch, wi_ids, None)` to build, or
    `(None, None, exit_code)` when the run ends here — the drained queue
    (EXIT_DONE), a claim refusal's code, a stranded claim, or a
    registry/frontier mismatch. `config_refusal` (string or None) is applied
    only when there is work that needs a worker — BEFORE a claim would park a
    branch, but never blocking an empty queue from draining to success."""
    parked = _parked_branches(root)
    if parked:
        if config_refusal:
            _say(config_refusal, err=True)
            return None, None, ac.EXIT_PREFLIGHT
        branch = parked[0]
        wi_ids = integrate._claimed_wi_ids(root, branch)
        _say(
            "cycle {} - resuming parked branch {} ({})".format(
                cycle, branch, ";".join(wi_ids)
            )
        )
        return branch, wi_ids, None
    stranded = _stranded_claims(root)
    if stranded:
        _say(
            "claimed spec(s) with NO branch ref - refusing to treat this "
            "queue as drainable: {}. Restore the branch, or move the specs "
            "back to queued/ in a reviewed trunk commit, then relaunch.".format(
                ", ".join(stranded)
            ),
            err=True,
        )
        return None, None, ac.EXIT_PREFLIGHT
    ready = [
        r for r in schedule.frontier(schedule._load(root)) if r["status"] == "queued"
    ]
    if not ready:
        # A finished branch may still be waiting (e.g. built by hand between
        # runs) - drain before declaring the queue empty, and COUNT what that
        # drain merges (REVIEW-A round 1: the banner undercounted residue).
        residue = len(integrate.finished_branches(root))
        code = _drain(root, tier)
        if code != 0:
            return None, None, code
        _say(
            "queue drained - no ready work items; {} WI(s) integrated this run.".format(
                merged + residue
            )
        )
        return None, None, ac.EXIT_DONE
    if config_refusal:
        _say(config_refusal, err=True)
        return None, None, ac.EXIT_PREFLIGHT
    wid = ready[0]["id"]
    branch = _branch_for(root, wid)
    if branch is None or ac.git(root, "check-ref-format", "--branch", branch)[0] != 0:
        _say(
            "no single queued spec matches {}, or its filename does not map "
            "to a valid git branch name - fix the spec folder, then "
            "relaunch".format(wid),
            err=True,
        )
        return None, None, ac.EXIT_PREFLIGHT
    _say("cycle {} - claiming {} on {}".format(cycle, wid, branch))
    code = integrate.claim(root, wid, branch)
    if code != 0:
        # The refusal ladder already printed its reason - a refusing rung
        # STOPS the run (never skipped, never talked past).
        return None, None, code
    return branch, [wid], None


def _worker_stop_code(branch, code):
    """None to continue the loop, else the exit code the worker's outcome ends
    the run with — the claim stays parked either way, so a relaunch resumes."""
    if code == ac.EXIT_NEEDS_HUMAN:
        _say(
            "NEEDS-HUMAN from the worker on {} - act on its ask, then "
            "relaunch; the claim stays parked and resumes.".format(branch),
            err=True,
        )
        return code
    if code != ac.EXIT_DONE:
        _say(
            "worker on {} exited {} - stopping (the claim stays parked; "
            "relaunching resumes it).".format(branch, code),
            err=True,
        )
        return code
    return None


def _cycle_stall(root, head_before, stall):
    """The stall counter after one green cycle: a cycle that leaves the trunk
    unmoved — a worker that reported DONE without finishing its branch merges
    nothing — increments it; any trunk advance resets it."""
    head_after = ac.git(root, "rev-parse", "HEAD")[1].strip()
    return stall + 1 if head_after == head_before else 0


def run(root, args, worker=None, tier="all"):
    """The drive loop. `worker` is the one injection seam (tests): a callable
    `(root, branch, wi_ids, args) -> exit code` standing in for the worker
    session launch; None means the real subprocess launch. `tier` is the
    bar tier the §A2 refresh runs (default: the full gate bar).

    Lock note: the plain-launch caller (agent_loop) holds out/agent-loop.lock
    for the process lifetime; integrate.py takes and releases its own
    out/integrate.lock per drain inside the same process. agent_common keeps
    one held-descriptor slot, so the coordinator lock's descriptor is simply
    left to the OS's exit-time release — exactly the guard's intended span.
    """
    worker = worker or _default_worker
    # Computed once, APPLIED lazily: _resume_or_claim refuses on it only when
    # work actually needs a worker, so an empty queue still drains to exit 0
    # on an unwired scaffold (the spec's empty-frontier contract; codex
    # cross-review finding, round 1).
    config_refusal = (
        _session_config_refusal(root, args) if worker is _default_worker else None
    )
    merged = 0
    stall = 0
    for cycle in range(1, max(1, args.max_iterations) + 1):
        # The pause is checked at the top of every cycle so one appearing
        # MID-RUN stops the next claim, not just the first (§5.6: pause means
        # stop claiming; the claim rung would refuse anyway - this stops with
        # the banner instead of a refusal exit).
        paused = ac.tracked_pause(root / "docs")
        if paused is not None:
            _say(
                "PAUSED - docs/work/pause is present (since {}: {}); {} WI(s) "
                "integrated before the stop. Unpausing is a reviewed deletion "
                "commit.".format(
                    paused.get("since", ""), paused.get("reason", ""), merged
                ),
                err=True,
            )
            return ac.EXIT_PAUSED
        # The claim rung's clean-trunk refusal, hoisted to the cycle top so
        # the PARKED-resume path meets it too - otherwise a worker session
        # runs (in its own worktree) only for the merge to refuse on dirt
        # that was visible before it started (codex cross-review, round 1).
        if ac.working_tree_dirty(root):
            _say(
                "the trunk working tree is dirty - claims, resumes and merges "
                "all need a clean trunk; commit or stash it, then relaunch "
                "({} WI(s) integrated before the stop).".format(merged),
                err=True,
            )
            return ac.EXIT_PREFLIGHT

        head_before = ac.git(root, "rev-parse", "HEAD")[1].strip()
        branch, wi_ids, code = _resume_or_claim(
            root, cycle, tier, merged, config_refusal
        )
        if branch is None:
            return code

        code = _worker_stop_code(branch, worker(root, branch, wi_ids, args))
        if code is not None:
            return code

        # Count what the drain will actually merge — every finished branch,
        # residue included, not just this cycle's own (REVIEW-A round 2: the
        # branch-gone read undercounted a mixed residue+claim drain). On a
        # green drain every finished branch merged (a held branch exits
        # nonzero above), so the pre-drain count is exact.
        finished = len(integrate.finished_branches(root))
        code = _drain(root, tier)
        if code != 0:
            # Red refresh bar / verdict refusal / held branch: the reason is
            # already printed; a red queue stops rather than skips (§5.5).
            return code
        merged += finished

        stall = _cycle_stall(root, head_before, stall)
        if stall >= max(1, args.stall_limit):
            _say(
                "STALL - {} consecutive cycle(s) left the trunk unmoved; "
                "aborting rather than looping.".format(stall),
                err=True,
            )
            return ac.EXIT_STALL
    _say(
        "iteration ceiling ({}) reached with work remaining - relaunch to "
        "continue ({} WI(s) integrated this run).".format(args.max_iterations, merged),
        err=True,
    )
    return ac.EXIT_BUDGET
