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
thread (scope critique 2026-10-10 leg 02, answered on trunk):

- **Producer and transfer:** `session_service.KeepWarmer._ping`, on the ping
  thread, catches the `TreeNotEnded` its `act()` raised and appends it with
  the finished call to `KeepWarmer.finished`, the one existing transfer
  route. No other value crosses. A ping still in flight has no outcome yet;
  it is not a fatal outcome, and its handling is unchanged.
- **Consumers** (`rg` over `project-trajectory/scripts` for `self.finished`,
  `_record_finished`, `warmer.tick`, `warmer.finish`):
  `KeepWarmer.tick`, `KeepWarmer._record_finished` and `KeepWarmer.finish`
  in `project-trajectory/scripts/session_service.py`; the outward tick caller
  `project-trajectory/scripts/dispatch.py` (`_keep_warm`); and the exit
  callback `keep_warmer` registers with `atexit`.
- **Ruling: the stop never waits on telemetry.**
  - `_record_finished` records each finished call, then re-raises a carried
    `TreeNotEnded` from a `finally`, so a failed recording never replaces or
    loses it (the recording error rides as its context).
  - `tick`: a finished entry carrying `TreeNotEnded` is raised at the tick
    that sees it. Over a clean trunk it is recorded first, as above; over a
    dirty trunk the dirty-trunk hold does not defer it: the session log is
    not written (its hold line still applies) and the exception is raised.
  - `finish`: after its join, the same rule. Over a dirty trunk it prints its
    existing not-recorded line and raises instead of clearing the entry.
  - The `atexit` route: `finish` raising there is reported to stderr by the
    interpreter at exit, the run being already at its end; this satisfies
    SR-238 on that occasion (the run does not continue), and no further
    handling is added.
  - Every other ping exception keeps today's recorded ERROR. Per
    `project-trajectory/PROCESS.md` §3, "When a guard is owed", the
    in-process carrier is trusted; no validation is added.

## Done-when

- A `TreeNotEnded` raised in a keep-warm ping reaches the dispatcher thread
  and propagates from it; other ping failures are recorded as today.
- Test: a ping whose act raises `TreeNotEnded` makes the next tick (or
  `finish`) raise it, after recording the call over a clean trunk; over a
  dirty trunk the tick and `finish` raise it unrecorded; a recording failure
  does not replace it; an ordinary ping error is still recorded and
  swallowed.
- LLR rows that state the keep-warm ping's error handling are amended if
  the change makes them untrue (traced cells otherwise).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
