+++
id = "WI-822"
title = "Coordinator context guard: at 50% context, stop new lanes, close out, hand off, relaunch at session end"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Deliverable

`coordinator_guard.py` is the coordinator context guard, shipped dormant (`[coordinator] context_guard_pct = 0` in the template; this repo's dial is 50). It reads the coordinator's context occupancy from the newest valid post-compaction usage in its transcript, holds one coordinator lease under the primary checkout (passed only to a relaunched successor or by the owner's recorded release), latches drain mode at the threshold, and refuses every guarded claim route (integrate's claim, CLI and wrapper; the live dispatcher's route is outside it, D-001) from a non-holder or after the latch. At the holder's true session end it relaunches a successor from the handoff's session prompt through the repo's launchers, restoring the request on any launch failure, under the store lock it already holds. The hook registration (`.claude/settings.json`) and the launchers (`scripts/coordinator-relaunch.{cmd,sh}`) stay this repo's until a live relaunch is verified (D-002). Rows: SR-229, SR-230, LLR-300, LLR-301, TC-315 to TC-318 approved and LLR-140, LLR-270 re-attested in the lane (act seq 33; verdicts 003 to 005 in `docs/reviews/wi-822-context-guard/`); IF-271 to IF-275 and IF-277 to IF-281 declared. Codex 6.1 Sol: four rounds, the last SOUND. Decisions: `docs/decisions/wi-822.toml`.

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
of record, [docs/specs/WI-822.md](../../specs/WI-822.2026-10-05.md).

## Done-when

- **Occupancy** is read from version-identified transcript fixtures: the newest
  valid usage after the last compaction boundary on the live branch, counting
  cache reads and creation. Fixtures cover a branched transcript, one after
  compaction, one after a resume, malformed or partial usage, and a mismatched
  window. No valid usage reads as unknown, never 0%.
- **Coordinator identity:** only the lease holder's transcript is measured or
  drained. A subagent's hook call and another session's hook call are no-ops,
  each tested.
- **The lease transfers only at exit or by the owner:**
  - a held lease is never taken because time passed: a silent but live holder
    keeps it;
  - the relaunched successor takes it at `SessionStart`;
  - the owner's explicit release, which is recorded, frees it;
  - a session that does not hold it has its claims refused, naming the holder
    and the release command.

  Each case tested.
- **Drain latches:** above threshold, then compaction below it, then a claim is
  still refused. The latch survives a resumed session, and clears only on the
  successor's lease take or the owner's recorded clear. The instruction is
  injected once at the latch, then bounded reminders, on tool, failed-tool,
  prompt and stop events. Each case tested.
- **The claim boundary:** `integrate.claim` refuses while draining, whatever the
  caller: the CLI, a wrapper, or an import. It reads the lease's transcript
  itself and latches on a crossed threshold. A fixture covers the exact sequence
  round 2 named: the last measured reply is below the threshold, the next reply
  crosses it, and its first tool call is a claim. The claim is refused, both via
  the `PreToolUse` measurement and with no hook run. Close-out passes while draining:
  - landing, archive and sweep;
  - the scoped-unpause restore;
  - a verification `git worktree add --detach`, and worktree removal.

  Each case tested.
- **The relaunch:**
  - It launches only on an exit reason, never `clear` or `resume`, and only from
    the lease holder, and only for a request from that same session, for this
    repo, naming an existing handoff.
  - The request is acquired atomically: two concurrent handlers launch once.
  - A failed launch restores the request. A request from another session is
    refused and reported.
  - The launch runs in the declared repo root, with the handoff's prompt; the
    Windows and POSIX launchers are both tested with the launch stubbed.
- **Compaction:** `PreCompact` records the trigger, the occupancy and the guard
  state, and the handoff template classifies a missed threshold, a manual
  compaction and compaction during a drain.
- **Dials:** the threshold and the window are declared in
  `docs/process.toml` and in the shipped template (template threshold 0 = off,
  so the dogfood sync holds). Nothing is hard-coded.
- **Registration and dry run:** hooks are registered in a tracked
  `.claude/settings.json`. The row's report records an end-to-end dry run: a
  fixture over threshold yields the latch, the instruction and a refused claim;
  a stubbed exit then launches exactly once.
- **Close-out wording:** `session-protocol` (or the coordinator handoff template)
  tells a coordinator what the instruction means, so the close-out is the same
  every time.
- **Shipping:** whether the script and hook registration ship to adopters is
  decided and recorded.
- **Bars:** the test bar is its module tests plus the smoke tier. Review bar: A.
  RESYNC_PACK: an entry for the template's new dial keys, plus the tooling if it
  ships.
