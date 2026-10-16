+++
id = "WI-931"
title = "The session kill drops its launch-window and late-spawn guards; the job object's kill of the tree stays"
workstream = "process"
sr_refs = ["SR-238"]
specref = "docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = []
+++

## Context

Filed from the owner's ruling of 2026-10-15 (coordinator-2026-10-15 D-011),
on the audit of guards built on contrived findings
(`docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md`).
WI-881's interrupt-window guards and its late-spawn closing of the job are
removed: not impactful enough to build anything around. This row removes
them and builds nothing in their place.

WI-881 (landed 2026-10-10, squash `b059c8a45`) replaced `taskkill` with a
Windows job object. Three of its later rounds answered findings that need a
sub-second timing window, and PROCESS.md section 6 puts such a window
outside a spec's promise:

- **The launch owns the child until hand-over** (wi-881 D-006, gate 006).
  A Ctrl-C landing between the child's resume and the publication of its
  job left a running child. `_spawn_session` now catches `BaseException`
  and ends what it owns through `_end_launch` and `_end_suspended`.
- **`TreeNotEnded` is a `BaseException`** (wi-881 D-007, narrow review 007).
  The new launch cleanup could raise an `OSError` into `run_session`'s
  launch-error conversion. The class exists only because the previous
  bullet put a tree kill inside that conversion.
- **The job is closed to new members before the kill's snapshot** (wi-881
  D-004, narrow review 002). A process created between the snapshot and the
  terminate was terminated with the job but could still be unsignalled, for
  milliseconds, when the kill returned. `_close_job` sets the job's
  active-process limit to 1.

What stays is the job object's ordinary kill of the tree:

- containment of every descendant in the session's job, and the refusal of
  a child that cannot be contained, before it runs (D-001);
- the terminate, which reaches an orphaned grandchild;
- the member snapshot and the SYNCHRONIZE wait taken before the terminate
  (D-003's measured fix for the job count reaching zero before a member is
  signalled);
- the raise for a member the kill cannot open;
- the 10 s bound, and the POSIX group kill;
- ending the tree on an interruption while the coordinator waits on the
  session. This predates WI-881, and `run_session`'s one `finally` now owns
  it.

Also removed (coordinator-2026-10-15 D-018, not ruled by D-011): D-005's
check that a held handle's process is still in the job (against PID reuse),
which was built in the same round without a finding (the audit's pattern 6).

## Deliverables

1. **Launch-window ownership removed (wi-881 D-006 and D-007).**
   - `_spawn_session` catches `OSError` only. On a containment failure it
     kills and reaps the never-run child, closes its pipes and re-raises.
     This is the shape before D-006, and D-001's refusal is unchanged.
   - `_end_launch` and `_end_suspended` are deleted.
   - `TreeNotEnded` stops being a `BaseException`. It becomes an ordinary
     `OSError` subclass, as the failure was before D-007 (D-018).
   - `_kill_tree` still raises the named error for a tree that is not
     ended.
   - `run_session`'s single `finally` stays as the owner of the supervised
     session, ending the tree at a deadline or an interruption (D-018). Its comment and the docstrings stop claiming the launch and
     hand-off windows.
2. **The late-spawn close removed (wi-881 D-004).**
   - `_close_job`, `_JobBasicLimit`, `_JOB_BASIC_LIMIT`,
     `_JOB_LIMIT_ACTIVE_PROCESS` and the `SetInformationJobObject` prototype
     are deleted.
   - `_terminate_job` snapshots the members, then terminates the job.
3. **The PID-reuse check removed (wi-881 D-005; D-018).** D-005 had the
   kill drop a held handle whose process is no longer in the job, "so a
   reused PID never makes the wait hang on an unrelated process"; it was
   "adjacent to F1, not part of it; built in the same round because it sits
   at the same boundary". With it gone, a reused PID between the job's PID
   list and the open makes the kill wait on an unrelated process and raise
   at the 10 s bound: a loud stop in a microsecond window.
   - `_in_job` and the `IsProcessInJob` prototype in `_win32` are deleted,
     with the check in `_open_job_members` and its docstring sentence.
   - `_MEMBER_ACCESS` loses its query bit and becomes SYNCHRONIZE alone.
   - Tests: none pins it; none changes.
   - Spine: LLR-026's CodeSymbol drops `_in_job`; no Detail, SR or TC text
     states it.
4. **Tests.** Six tests and five helpers are deleted, in
   `tests/test_session_stdin.py`:

   | Test | Pinned | Action |
   |---|---|---|
   | `test_an_interruption_after_the_resume_ends_the_launching_child` | D-006 | delete |
   | `test_an_interruption_before_the_job_ends_the_suspended_child` | D-006 | delete |
   | `test_an_interruption_in_supervision_ends_the_child` (both stages) | D-006's windows | delete |
   | `test_an_interrupted_launch_whose_tree_cannot_be_verified_raises` | D-007 | delete |
   | `test_a_launch_cleanup_that_cannot_terminate_raises` | D-007 | delete |
   | `test_a_member_spawned_during_the_kill_has_ended_when_it_returns` | D-004 | delete |
   | helpers `_marker_child`, `_session_outcome`, `_InterruptingThread`, `LATE_SPAWNER`, `_late_spawn_round` | used only by the above | delete |
   | `test_a_tree_not_ended_within_the_bound_raises` | D-003 | keep; gains one assertion that the raised error is an `OSError` (inverts D-007) |
   | `test_a_member_the_kill_cannot_open_makes_it_raise` | denied access | keep |
   | `test_an_ordinary_launch_error_still_returns_the_session_error` | missing executable | keep; comment reworded, no longer citing D-007 |
   | `test_a_deadline_kill_ends_the_grandchild`, `test_an_interruption_ends_the_grandchild`, `test_an_uncontainable_child_errors_before_it_runs`, the idle and wall tests | ordinary kill | keep, unchanged |
   | `tests/test_session_keep.py`'s four carried-`TreeNotEnded` tests (WI-895) | keep-warm carrier | keep, unchanged |

5. **Spine.** Each change is judged at the lane's checkpoint sitting.

   - **SR-238 (Approved): amended.**
     - AcceptanceCriteria: "At a wall deadline, an idle deadline, or a
       coordinator interruption while the coordinator supervises a launched
       session, the direct session child and every process in the session
       process group on POSIX, or in the session job when the kill takes its
       member list on Windows, have ended before the coordinator continues;
       a process that joins the session job later in the kill is terminated
       with the job; if any has not ended within 10 s of the kill, the
       coordinator stops with an error naming what survived instead of
       continuing."
     - Rationale: the last sentence ("An interruption inside platform
       process creation ... is not covered") becomes the one statement of
       residue: "Two windows lie outside the guarantee, each sub-second and
       on no supported workflow's ordinary path: an interruption while the
       session is still being launched, before the coordinator supervises
       it, which can leave a running child; and a process that joins the
       session job while the kill takes its member list, which is terminated
       with the job but can still be ending, for milliseconds, when the
       coordinator continues."
   - **LLR-026 (Approved): amended.**
     - Detail:
       - The launch-ownership sentence becomes "An interruption ends the
         tree only once the coordinator supervises the session; one that
         lands while the session is still being launched is outside the
         kill."
       - "after Popen returns the child" becomes "while the coordinator
         supervises the session".
       - "first closes the job to new members, then takes a handle" becomes
         "takes a handle".
       - The sentence about the tree-end error that no ordinary handler
         converts becomes "A failure to end the tree, or to show that it
         ended, raises the named tree-end error."
     - Rationale: the clause "Closing the Windows job before its member
       snapshot makes that snapshot complete, and" is dropped.
     - CodeSymbol: drops `_end_launch`, `_end_suspended` and `_close_job`,
       and `_in_job` (deliverable 3).
   - **TC-026 (Approved): amended.**
     - Method and Evidence drop the six deleted tests.
     - Expected becomes "Satisfies SR-026 AcceptanceCriteria; the bounded
       descendants have ended when the coordinator continues, with no grace
       period; an interruption during supervision ends them as a deadline
       does; an uncontainable child errors before it runs; an unopenable
       member or an overrun past 10 s raises; and an ordinary launch error
       still returns the session error."
   - **Unchanged.**
     - SN-006 and SR-026.
     - IF-064: no exported name changes, and the error class keeps its
       name.
     - LLR-270 and TC-268: WI-895's carrier keeps its key (D-018).
     - The TC at `test-cases.toml` line 3533 (`verifies` only).
6. **RESYNC_PACK.**
   - An entry anchored at a trunk commit: `scripts/agent_session.py` is
     overwritten.
   - `TreeNotEnded` is an `OSError` again, so an adopter's own
     `except OSError` or `except Exception` around a session catches a
     failed tree end again; let it stop the run. A handler that follows the
     earlier advice (catch `BaseException` and re-raise) keeps working.
   - The two residual windows are named.
   - No setting, registry or migration is forced.

## Done-when

- `agent_session.py` has no `_end_launch`, `_end_suspended`, `_close_job`,
  `_JobBasicLimit` or `SetInformationJobObject`, and `_spawn_session` has no
  `except BaseException`. A grep of the file finds each of these before the
  change.
- `test_a_tree_not_ended_within_the_bound_raises` asserts that the raised
  error is an `OSError`. The assertion fails on the code before the change,
  where `TreeNotEnded` derives from `BaseException`.
- The kept ordinary-kill tests pass unchanged on Windows and POSIX:
  - `test_an_uncontainable_child_errors_before_it_runs`
  - `test_a_deadline_kill_ends_the_grandchild`
  - `test_an_interruption_ends_the_grandchild`
  - `test_a_member_the_kill_cannot_open_makes_it_raise`
  - `test_an_ordinary_launch_error_still_returns_the_session_error`
  - the idle and wall tests
  - WI-895's four keep-warm tests

  These pin what must survive, so they pass both before and after the
  change; that they stay green is the check.
- The six tests and five helpers in the deliverables table are gone, and
  TC-026's Method and Evidence name none of them.
  `trace.py --strict-integrity` and `check_trajectory.py --strict` are
  clean.
- The plan records a census of every handler of `OSError` or `Exception`
  in the kit scripts between `run_session`'s `finally` and the run's exit,
  with a verdict for each: carries the error, re-raises it, or is fixed in
  this row. Where it converts a failed tree end into a continuing run, the
  row fixes that one handler. The 2026-10-10 sitting 004 check found none.
- SR-238, LLR-026 and TC-026 carry the amendments above. They are blessed
  or approved at the lane's checkpoint sitting, and their acts are
  recorded.
- `RESYNC_PACK.md` carries the entry.
- The commit bar is green within its smoke budget. Review bar A (one
  cross-family REVIEW-A).

## Scope answers

- **S1, deliverables.** There are two independently landable deliverables:
  - **D1:** deliverable 1, the launch window. `TreeNotEnded`'s
    `BaseException` standing guards only the launch cleanup, so it cannot
    leave alone.
  - **D2:** deliverables 2 and 3, the late-spawn close and D-005's check,
    in one function.

  They are kept in one row on purpose. Both amend the same cells of SR-238,
  LLR-026 and TC-026 at one checkpoint sitting, in the same two files. Split,
  they would cost a second sitting on those cells and a rebase of the
  second lane's row text over the first's. Inside the lane, D2 lands first:
  it is smaller and changes no error contract (D-018).
- **S2, authority.** No deliverable gives a file authority over a hold, an
  act or a gate. There is no Trust section.
- **S3, coverage.** There is no promise over an input space. The row
  narrows SR-238's promise to the supervised session and to the job's
  members at the kill's snapshot. The two sub-second windows it gives up
  are stated once, as residue in SR-238's Rationale, in PROCESS.md section
  6's terms.
- **S4, planmode `single`.** The row changes an error contract that crosses
  from `agent_session` into `session_service` (WI-895's keep-warm carrier)
  and the dispatch callers: two script families and the IF-064 seam. The
  handler census is the plan's work.
- **S5, architectural delta.** The row removes a state (a job closed to new
  members) and an error class's out-of-band standing. It adds no state,
  value, input or boundary.
- **S6, dependencies.** None: `needs = []`.
  - No open lane touches `agent_session.py`, `tests/test_session_stdin.py`,
    LLR-026 or TC-026.
  - wi-798 and wi-923 edit LLR-270, TC-268, `session_service.py` and
    `tests/test_session_keep.py`, which this row leaves alone (D-018).
  - No new package.
- **B1 to B4.**
  - B1: nothing in Context commits to unlisted work.
  - B2: no split is proposed on a work branch.
  - B3: no reader re-derives a decision.
  - B4: no owner act inside the build; the calls below were ruled at
    filing.

## Calls ruled at filing

Coordinator-2026-10-15 D-018 (2026-10-15i):

1. **`run_session`'s single `finally` stays** as the owner of the
   supervised session: it also replaced the older interrupt and deadline
   kills, and reverting it would add code back. Only its tests of the
   sub-second interrupt windows are deleted, and SR-238 states those windows
   once as accepted gaps.
2. **`TreeNotEnded` keeps its name as an ordinary `OSError` subclass**,
   losing only its `BaseException` status, because WI-895's keep-warm ping
   catches that type.
3. **wi-881 D-005's PID-reuse check is removed in this row** (deliverable
   3): the same contrived kill-window class, and it stops loudly at the
   10 s bound when it would fire.
4. **One row, the late-spawn removal landing first** (the coordinator's S1
   call): all three removals amend SR-238, LLR-026 and TC-026 at one
   sitting.
