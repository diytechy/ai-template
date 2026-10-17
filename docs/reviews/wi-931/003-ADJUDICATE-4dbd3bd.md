# WI-931 adjudication 003: amendment of SR-238, LLR-026 and TC-026

I judged the three amended rows at `4dbd3bd78`. Since their anchors, the registries moved only in these rows. The SR, LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**The scope the change rests on:** the work item's Context records the owner's ruling (D-011, on the contrived-guards audit) that WI-881's sub-second launch-window and late-spawn guards are not worth their cost: launch-window ownership, `TreeNotEnded` as a `BaseException`, and closing the job before the kill's snapshot. The PID-reuse check goes with them (D-018). Kept: containment of every descendant in the session job and refusal of an uncontainable child; the terminate; the member snapshot and wait before the terminate; the raise for an unopenable member; the 10 s bound and the POSIX group kill; and ending the tree on a deadline or an interruption while the coordinator supervises.

**What I checked, because the error class now becomes an ordinary `OSError`:**
- **`run_session` (`agent_session.py:806-840`):** `_spawn_session`'s `except (OSError, ValueError)` covers only the launch. The tree kill runs in the supervision `finally`, outside that conversion, so a tree-end failure propagates.
- **`session_service.act`:** it re-raises every exception.
- **Keep-warm's ping:** it catches the tree-end error by name before its generic handler.
- **`agent_loop` and `dispatch`:** their `except OSError` handlers wrap file reads only, never a session launch.

So the coordinator still stops on an unended tree, as SR-238 requires. The seven tests TC-026 keeps all exist, and `test_a_tree_not_ended_within_the_bound_raises` asserts the raised error is an `OSError`.

## amendment

- [MEANING] SR-238 AcceptanceCriteria and Rationale -> once the platform's process creation returned the child, every process still in the session group or job has ended before the coordinator continues (with the job closed to new members, a late joiner is covered); an interruption inside process creation is not covered -> the guarantee runs while the coordinator supervises a launched session, over the group on POSIX or the job's member list as the kill takes it on Windows; a process joining the job later in the kill is terminated with the job, but may still be ending for milliseconds; the Rationale names the two excluded windows (an interruption during launch, which can leave a running child, and the late joiner) as sub-second and on no supported workflow's ordinary path -> the guaranteed scope narrowed. An interruption between creation and supervision, and a late joiner, were covered before and are not now. **Blessed.**
  - The owner ruled those windows contrived under PROCESS.md §6.
  - The new text states its limits honestly instead of over-promising, and keeps every supervised-case guarantee and the 10 s stop.
  - No file or symbol is named.
- [MEANING] LLR-026 Detail and Rationale -> the launch owns the child from when Popen returns; the Windows kill first closes the job to new members, then holds each member, then terminates; a tree-end failure raises `TreeNotEnded`, "which no ordinary handler converts into a session result" -> an interruption ends the tree only once the coordinator supervises the session (one during launch is outside the kill); the Windows kill holds each member and then terminates; a tree-end failure raises "the named tree-end error"; the Rationale drops the close-before-snapshot argument -> the job-close step, launch-window ownership and the stated non-conversion guarantee are all removed. **Blessed.** It decomposes SR-238's narrowed guarantee exactly. Its removed symbol is a carrier the naming rule bars from row text, and the trace cells still carry it.
  - **Advisory:** the dropped "no ordinary handler converts it into a session result" holds today only by structure (above). SR-238 still forbids continuing, but LLR-026 no longer says why a future broad `except OSError` around a launch would breach it. A later edit could restate that the tree-end error propagates past the launch-error conversion, without naming a carrier.
- [MEANING] TC-026 Expected and Method -> verify interruptions before containment, after resume, during I/O setup and at the deadline handoff; no process entering the job once the kill begins; and the tree-end error raising instead of a session result, with six tests for those windows -> verify an interruption during supervision ends the tree as a deadline does, plus the uncontainable child, the unopenable member, the 10 s overrun and the ordinary launch error, with exactly the seven kept tests named -> the verification set is narrowed to the kept behaviour. **Blessed.** It drops exactly the six tests the Context lists for the removed guards, keeps every test for the retained kill, and names only tests that exist.

VERDICT: MEANING rows=3

**Aftermath:** this session re-attests all three rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests SR-238,LLR-026,TC-026`

SITTING: JUDGED kinds=amendment
