# WI-881 lane checkpoint: adjudication sitting 001 at 291f389

Read with `git diff b29650f6..HEAD` (`agent_session._spawn_session`, `_contain_in_job`, `_kill_tree` and `_wait_for_exit`, the new real-process tests in `tests/test_session_stdin.py`) and decision D-001.

The Windows mechanism is sound. The child is created suspended and assigned to a fresh job, then resumed. A failed containment kills the never-run child and surfaces as a session error, and a deadline terminates the job. The selected tests pass here: `tests/test_session_stdin.py` gave 23 passed, under a run that itself sits inside an outer job, so nested assignment works. The findings below are about what the TEXT promises beyond that mechanism.

## amendment

Anchor: `docs/archive/last_approved` (low-level-requirements.toml and test-cases.toml at c31a23cd).

- [MEANING] LLR-026 Detail + Rationale -> headless launch with a stdin prompt, the codex last-message capture, and stdin otherwise closed. Nothing said what a deadline or interruption ends -> the same, PLUS: a wall or idle deadline, or an interruption, "ends the whole session process tree". On POSIX it ends the child's process group; on Windows it ends the job the child was born into, suspended, contained, then resumed. A child that cannot be contained ends as a session error before it runs. The Rationale adds why -> not the same: a new behaviour, a new mechanism and a new refusal (the Rationale is the clarity half; the Detail carries the meaning). NOT BLESSED this sitting.
  - The Windows half is true of the code.
  - The POSIX half promises "the whole session process tree" but delivers `os.killpg` on the child's process group. A descendant that leaves that group never receives the kill: one that calls `setsid()`, which daemonizing tools do, or one that runs in its own group. It is still a descendant and still able to edit the worktree, which is exactly the survivor the Rationale names.
  - This is ordinary agent-run behaviour, not a contrived host, so it is in scope under `PROCESS.md` §6.
  - The row must either bound its claim to what the group kill reaches, or strengthen the POSIX mechanism. See SR-238 below; the two are judged together.
- [MEANING] TC-026 Expected + Method -> "Satisfies SR-026 AcceptanceCriteria"; the agent-loop suite, headless resume and stdin delivery -> "Satisfies SR-026 and SR-238 AcceptanceCriteria"; the same, PLUS `test_a_deadline_kill_ends_the_grandchild` (real processes; an idle deadline ends the grandchild on POSIX and, through a `.cmd` shim, on Windows) and the idle deadline returning within 40 s -> not the same: a new parent, and new verification owed. NOT BLESSED this sitting. The TC now claims to verify SR-238, but reading down, two of SR-238's obligations and one of LLR-026's go unverified:
  - **Interruption.** `_wait_for_exit`'s `except (KeyboardInterrupt, SystemExit)` branch is a separate code path, and no test drives it. The arms map says so itself.
  - **The containment refusal.** A child that cannot be contained ends before it runs, and no test drives it. The arms map says so itself.
  - **The bound.** SR-238 requires every descendant to have ended "before the coordinator continues", and the test accepts the grandchild exiting up to 5 s after `run_session` returns. Neither platform waits for the descendants: `_kill_tree` returns after `killpg` or `TerminateJobObject`, and `proc.wait()` reaps only the direct child.

  The wall deadline shares the idle path's `_kill_tree` call, so the idle test covers it honestly.

VERDICT: MEANING rows=2

Aftermath: neither row is blessed, so neither is re-attested. The corrective work is drafted below, together with SR-238's, because the three rows change together.

### Answered in the lane

Both returns below were answered in the lane: the claim bounded (D-002) and the wait-until-ended with one stated bound (D-003), built in rounds 2 and 3 and judged at sitting 004.

WI-881 is an ordinary work lane, and intake mints drafts only from adjudication-kind specs. These drafts are therefore the lane's to answer before its merge, written in the shape intake reads for the coordinator to route:

```toml
title = "WI-881 return: SR-238 / LLR-026 promise every descendant ends, but a POSIX descendant outside the process group survives"
safety_class = "ordinary"
sr_refs = ["SR-238"]
```

Make the claim and the mechanism agree on POSIX. Choose one:
- **Bound the claim.** State in SR-238's AC and LLR-026's Detail that the guarantee covers every descendant still in the session's process group (POSIX) or job (Windows). Record the residual, a POSIX descendant that detaches into its own session or group, in SR-238's Rationale or as an assumption row, so a later reader knows it is a decided gap.
- **Strengthen the mechanism** so it reaches such a descendant, for example by tracking the session's descendants rather than its group.

In both cases, re-submit SR-238, LLR-026 and TC-026 together.

```toml
title = "WI-881 return: TC-026 does not verify SR-238's interruption arm, the containment refusal, or 'before the coordinator continues'"
safety_class = "ordinary"
sr_refs = ["SR-238"]
```

TC-026 needs three things:
- **A real-process test of the interruption path:** a KeyboardInterrupt during `_wait_for_exit` ends the grandchild, as the deadline test shows for a deadline.
- **A test that an uncontainable Windows child ends as a session error before it runs.** For example, force `_contain_in_job` to fail, then show that the child produced no output and that `run_session` returned the session-error result.
- **One consistent bound.** Either make the coordinator wait until the descendants have ended, for example until the job's active-process count is zero on Windows, or soften SR-238's "before the coordinator continues" to a stated bound. Then make the test assert that same bound instead of a 5 s grace period it never states.

## first-approval

- [RETURN] SR-238 -> when a declared deadline or coordinator interruption ends a session, the delivered coordinator leaves no live process in that session's process tree; acceptance: at a wall deadline, idle deadline or interruption, the direct child and every descendant have ended before the coordinator continues -> its chain is LLR-026, whose POSIX mechanism is a process-group SIGKILL, and TC-026, which drives the idle deadline only and tolerates the grandchild ending up to 5 s after the coordinator continues -> not ready. The row itself is well made:
  - its EARS `When` is right;
  - its Rationale argues the lens and records the rejected alternative;
  - `UNATTENDED-OPS` passes the listens-for test, since a surviving writer is a silent degrade nobody is paged for;
  - SN-006, a walk-away run stays safe, calls for it.

  But its absolute does not close over its domain. "Every descendant" includes a POSIX descendant that leaves the process group, and the mechanism its only LLR states cannot reach that process. The AC's "before the coordinator continues" is a threshold neither the code (no wait for descendants on either platform) nor the test (a 5 s grace period) holds. And its chain verifies one of its three triggers directly, plus a second (the wall deadline) through the shared kill path, leaving interruption with no test at all. Coverage by children is not earned. See the Dispositions under the amendment section.

OUTCOME: RETURN rows=1

No registry cell was changed and no approval snapshot was taken.

SITTING: JUDGED kinds=amendment;first-approval
