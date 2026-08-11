"""lane.py — one lane's mechanics (docs/concurrency-v2.md §A4.2, WI-381).

The lane half of the dispatcher split: everything about RUNNING one claimed
branch, extracted from the tick loop that decides WHICH branches run. A lane

    ensures its worktree      (`ensure_worktree` — integrate.py's home, one
                               path both the worker and the refresh agree on
                               by construction),
    launches the worker       (`run_worker` / `spawn_worker` — one worker
                               session loop on the claimed branch's worktree,
                               agent_loop.py --worktree --wi A;B), and
    runs the §A2 refresh      (`spawn_refresh` — the WI-386 station refresh as
                               its own subprocess, so N lanes' 11-minute bars
                               genuinely overlap instead of queueing at the
                               dispatcher; §A4.3 is why that matters),

and it REPORTS an outcome rather than deciding one: a lane declares itself
finished by moving its specs out of active/<branch>/ — the tree-derived signal
`integrate.finished_branches` reads — and every decision about what an exit
code or a red refresh MEANS stays in dispatch.py, where the serial trunk
writes live. There is deliberately no back-channel and no state file: the
worker subprocess, the refresh subprocess and the spec moves are the whole
protocol (§A4.2 — "the handshake the sketch worried about does not exist").

No `Contracts:` line, deliberately — the same posture as handback.py: the
dispatcher seam this module serves has no IF row yet (part of the drift
docs/concurrency-v2.md §A9.1 hands to the program-close row WI-390 rather
than to any single builder), and declaring a row here from the extracted
half would paper over that drift instead of recording it.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import agent_common as ac
import integrate

SCRIPTS = Path(__file__).resolve().parent


def ensure_worktree(root, branch):
    """The lane worktree holding `branch`: `(path, error)`, created if needed.

    integrate.py's `lane_worktree` IS the implementation — the worker builds
    there and the station refresh runs there, so the two must agree by
    construction rather than by two matching literals."""
    return integrate.lane_worktree(root, branch)


def worker_argv(root, wt, branch, wi_ids, args):
    """The worker session's argv: one agent_loop.py --wi run on the lane
    worktree. The plain launch's session dials ride to the worker EXPLICITLY —
    env inheritance covers the launcher-set slots, but a flag given on the
    command line would otherwise be silently dropped (codex cross-review
    finding, WI-374 round 1). model/model-map arrive here already resolved
    (CLI > env > stack.ini), so forwarding them as flags preserves exactly the
    plain launch's resolution."""
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
    return argv


def spawn_worker(root, branch, wi_ids, args):
    """Launch one worker session loop on the claimed branch's worktree,
    NON-blocking: `(Popen, None)` or `(None, refusal)`. Stdio is inherited so
    the walk-away console shows the worker's own live echo; AGENT_CMD and the
    routing env pass through the environment exactly as an attended launch
    would see them."""
    wt, err = ensure_worktree(root, branch)
    if err:
        return None, err
    argv = worker_argv(root, wt, branch, wi_ids, args)
    return subprocess.Popen(argv, cwd=str(root), stdin=subprocess.DEVNULL), None


def run_worker(root, branch, wi_ids, args):
    """The BLOCKING worker launch — `spawn_worker` waited to completion, with
    the refusal printed here (the sync path has no lane record to carry it).
    Returns the worker's exit code.

    WHO CALLS THIS: nothing inside the kit — it is a DECLARED SEAM (LLR-150's
    `code_symbol` names it) kept for a caller that wants one lane run
    synchronously: an attended single-lane run, or a downstream driver that
    does not want `dispatch.py`'s poll loop. `dispatch._launch`'s own default
    is `spawn_worker` (non-blocking, so N lanes overlap), and its `worker=`
    injection is what tests substitute — so a dead-symbol sweep sees zero
    callers here and must not read that as dead. Verified 2026-08-11 (WI-422)."""
    proc, err = spawn_worker(root, branch, wi_ids, args)
    if err:
        print("lane: {}".format(err), file=sys.stderr, flush=True)
        return ac.EXIT_PREFLIGHT
    return proc.wait()


def spawn_refresh(root, branch, tier):
    """The §A2 station refresh for `branch`, NON-blocking: a Popen running
    `integrate.py refresh` as its own subprocess with inherited stdio.

    A subprocess, not a thread and not an in-dispatcher call, for one reason
    (§A4.3): the refresh carries the ~11-minute bar, and N lanes finishing
    together must run N bars CONCURRENTLY — an in-dispatcher refresh would
    queue them at the station and put the whole contention win back. The
    invoker's own integrate.py is launched (its `_branch_tree_script` still
    picks the BRANCH's trunk_step/check.py copies, exactly as the in-process
    call did), under the harness interpreter, printing to the same console.
    The dispatcher reads only the exit code; the refusal detail is the
    subprocess's own stderr plus the retained out/run-logs/ file
    (`integrate._keep_refused_output`)."""
    argv = [
        str(ac.harness_python(root)),
        str(SCRIPTS / "integrate.py"),
        "--root",
        str(root),
        "refresh",
        "--branch",
        branch,
        "--tier",
        tier,
    ]
    return subprocess.Popen(argv, cwd=str(root), stdin=subprocess.DEVNULL)
