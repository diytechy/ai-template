+++
id = "WI-822"
title = "Coordinator context guard: at 50% context, stop new lanes, close out, hand off, relaunch at session end"
workstream = "process"
specref = "docs/specs/WI-822.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Context

Filed by hand by the coordinator on 2026-10-04 at the owner's direction, to be built
FIRST in the next coordinator session (priority 9; every other queued row is 3).

The owner's concern: a coordinator session in Claude Code (the hand path, which also
runs the in-lane adjudication cycle) builds up context over many lanes, and
compaction then degrades it. The owner: "Is it possible to prime the adjudicator to
prepare a handoff and close out current work items (without starting new lanes) if
it's context grows over 50%? In theory it could also schedule a cmd file to launch a
new session from said handoff." Then: "agree with WI-822 and a relaunch on session
end". A single adjudication is not the risk; the session's growth over many lanes
is.

Nothing filed covers it. WI-802's reset terms apply to sessions the kit LAUNCHES
(`ask`), not to the interactive coordinator session itself. The unattended loop's
protection (`agent-resume`, `agent_loop.py`) is a separate path the owner is testing
elsewhere.

The design (what Claude Code provides, the five parts, and the scope) is the spec
of record, [docs/specs/WI-822.md](../../specs/WI-822.md).

## Done-when

- The occupancy reader computes the share from a transcript fixture's newest
  assistant `usage`, including cache reads and cache creation, against the declared
  window. A transcript with no usage yet reads as unknown, never as 0%, and is
  reported.
- Crossing the threshold injects the instruction once per crossing, plus bounded
  reminders, keyed by `session_id`. It is tested below, at and above the threshold,
  and across a fresh session.
- Past the threshold, `PreToolUse` refuses `integrate.py claim` and
  `git worktree add`, naming the reason. Other tool calls, landings and closes pass.
  Tested both ways.
- The relaunch request is written by the session as part of its handoff. The
  `SessionEnd` hook launches the next session only when a request exists, then
  consumes it. A request naming a missing handoff refuses and reports, launching
  nothing. Tested with the launch command stubbed. The launcher template exists
  for Windows and POSIX, and uses the handoff's own prompt.
- `PreCompact` writes its marker, and the next handoff template reports a marker
  found.
- The threshold and window are declared values in the one dial home (no
  hard-coded 50 or 1M in the script). Changing them needs no code change.
- The hook registration is in a tracked `.claude/settings.json`, and an
  end-to-end dry run is recorded in the row's report: a fixture transcript over
  the threshold yields the instruction, a refused claim, and a launch command at
  session end.
- `session-protocol` (or the coordinator handoff template) tells a coordinator what
  the instruction means, so the close-out is the same every time.
- The row's test bar: its module tests plus the smoke tier. Review bar: A (one
  cross-family REVIEW-A). RESYNC_PACK: none while it is this repo's tooling (say
  so); an entry if it ships.
