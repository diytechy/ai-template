+++
id = "WI-881"
title = "A session's deadline kill returns at once, not after taskkill's latency"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

Landed 2026-10-10. A session's deadline or interruption kill no longer calls `taskkill`: on Windows the child is created suspended, placed in a job object of its own and resumed (decision D-001), and the kill closes the job to new members, takes a SYNCHRONIZE handle on each member, terminates the job and waits until each has ended; on POSIX the kill signals the child's process group and waits until it is empty. The kill returns only once the tree has ended, and anything not ended within 10 s raises `TreeNotEnded`, a BaseException no ordinary handler swallows (D-003, D-007). The launch owns the child until it hands it over, and one owner in `run_session` ends the tree on any exit but a natural one (D-006). Residuals are bounded in SR-238's Rationale (D-002, D-006): a POSIX descendant that leaves the group, a process a service starts outside the job, and an interruption inside the standard library's process creation. The idle-deadline test passes within its unchanged 40 s bound; tests pin a grandchild's death on Windows and POSIX. The tip re-grep found no executable `taskkill` call. Spine: SR-238 approved, LLR-026 and TC-026 re-attested (acts 99 to 102). Fresh full-lane gate 011 APPROVE, 0 findings, reviewed by Codex gpt-6-luna for gpt-6.1-sol (D-008). The keep-warm ping's swallowed tree-end failure is WI-895.

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

Landing order (scope critique, 2026-10-10): one deliverable, one lane. The
kill helper's change, its grandchild-death tests and the RESYNC entry land
together; the entry follows the script change it describes.

## Done-when

- A deadline kill ends the direct child at once and the tree without
  depending on `taskkill`'s latency. A grandchild (a `.cmd` shim's `node`)
  still dies: the reason `_kill_tree` walks the tree (repo-review 2026-07-21
  H-2) stands.
- The idle-deadline test passes on this workstation within its bound, with
  no bound raised. A test pins a grandchild's death on Windows and POSIX.
- The audit of the kit's other `taskkill` sites is done at filing
  (scope critique, 2026-10-10): `agent_session._kill_tree` is the kit's only
  `taskkill` call, reached from the idle/wall deadline and the stdin-feed
  failure paths of `run_session`. The lane re-greps at its tip and records
  the result; a new site found there is fixed here, at the one kill helper.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped script changes).
