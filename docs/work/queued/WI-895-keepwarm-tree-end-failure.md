+++
id = "WI-895"
title = "A keep-warm ping whose session tree cannot be ended stops the run, not a recorded error"
workstream = "process"
sr_refs = ["SR-238"]
specref = "project-trajectory/scripts/session_service.py"
needs = ["WI-881"]
buildtier = "quick"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed by the coordinator on 2026-10-10 from WI-881's round 5 (decision D-007
in WI-881's decisions record). WI-881 makes a failure to end a session's
process tree raise `agent_session.TreeNotEnded`, a BaseException no ordinary
handler catches, so the coordinator stops instead of continuing beside a
writer that may still be live (SR-238). One caller outside WI-881's surface
still swallows it: `session_service.KeepWarm._ping` runs `act()` on a
background thread inside `except BaseException: pass` and records ERROR.
A keep-warm session whose tree could not be ended is therefore recorded and
dropped.

Anchor: SR-238 (approved at WI-881's sitting 004).

Landing order: one deliverable, after WI-881 lands.

## Trust

No file gains authority. The carrier is an in-process exception crossing a
thread: the ping thread produces it, and the dispatcher thread
(`_record_finished`, `finish`) consumes it. Ruling: a `TreeNotEnded` from a
ping is re-raised on the dispatcher thread at its next tick or at `finish`,
after the call is recorded; every other exception keeps today's ERROR record.

## Done-when

- A `TreeNotEnded` raised in a keep-warm ping reaches the dispatcher thread
  and propagates from it; other ping failures are recorded as today.
- Test: a ping whose act raises `TreeNotEnded` makes the next tick (or
  `finish`) raise it, after recording the call; an ordinary ping error is
  still recorded and swallowed.
- LLR rows that state the keep-warm ping's error handling are amended if
  the change makes them untrue (traced cells otherwise).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
