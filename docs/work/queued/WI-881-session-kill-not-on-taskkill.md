+++
id = "WI-881"
title = "A session's deadline kill returns at once, not after taskkill's latency"
workstream = "process"
specref = "project-trajectory/scripts/agent_session.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed by the coordinator on 2026-10-10.
`tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child`
fails deterministically on this workstation: it fails alone, 3 of 3, at about
43 s against its 40 s bound. It is also the one failure in the 2026-10-10 full
suite on WI-859's tip (1 failed, 5632 passed, 21 skipped). The 2026-10-09c
handoff read it as load-sensitive. That reading is wrong.

The idle deadline fires on time: `timed_out == "idle"` holds. The time goes
to `agent_session._kill_tree`, which runs `taskkill /F /T /PID` before
`proc.kill()`. On this workstation `taskkill` takes about 50 s, with or
without `/T` (probe, 2026-10-10: 49.4 s and 49.2 s). The workstation's OS
build changed on 2026-10-08, and WI-859's job-object notice dates from the
same change. Every idle or wall kill in the live loop therefore holds the
coordinator for about a minute. Surfaced, not tooled around (owner rule).

## Done-when

- A deadline kill ends the direct child at once and the tree without
  depending on `taskkill`'s latency. A grandchild (a `.cmd` shim's `node`)
  still dies: the reason `_kill_tree` walks the tree (repo-review 2026-07-21
  H-2) stands.
- The idle-deadline test passes on this workstation within its bound, with
  no bound raised. A test pins a grandchild's death on Windows and POSIX.
- The other `taskkill` call sites in the kit are checked for the same
  latency and either fixed here or shown to be off the hot path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped script changes).
