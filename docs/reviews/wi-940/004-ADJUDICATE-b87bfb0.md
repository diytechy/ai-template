# WI-940 checkpoint sitting at b87bfb0

## first-approval

TC-374 is a re-sit, after sitting 003-ADJUDICATE-c0ce587 returned it with three findings. I re-read the row against both chains it hangs under (SR-238 with LLR-026, and IF-302's data cell) and against the lane's answer (commit b87bfb0ce and wi-940 D-009). All three findings are answered, and the row is ready.

- [APPROVE] TC-374 -> the obligation: run its eight named tests and assert the following:
  - for SR-238 and LLR-026, that the session job's active-process reader governs the tree-end bound, so an overrun past 10 s raises naming the survivor and an unopenable live member raises after the terminate;
  - for IF-302, that the shared module imports without loading kernel32, that the session reaches its shared declarations, and that an unnamed joined job's CPU reading sums user and kernel time, counting its exited descendants and excluding an outside process.

  -> what its chain shows: `Verifies` is now SR-238, LLR-026 and IF-302. The false SR-026 link (finding 1) is gone, and SR-238 with LLR-026 still meets the registry's rule that a TC may not verify an interface row alone, so the remaining links are earned rather than padding. The two session-tree arms are SR-238's 10 s bound and LLR-026's member-handle rule, now exercised through the moved reader. They are cited beside TC-026's, which reads as the move-validation evidence the arms map calls for, not an overlap of decisions. Expected now states each condition against the row it satisfies (finding 2), so the CPU-reading arms are claimed for IF-302 alone, the interface whose data cell declares `create_joined_job` and `job_cpu_seconds`, and no longer read as SR-238 coverage. The design smell (finding 3) was surfaced for the coordinator or the owner, not as a defect of this row's text. It is now a recorded call: the coordinator keeps the readers where the passed plan placed them, high risk for the owner to overrule into a successor row, with the RESYNC entry naming what adopters receive (D-009). The disposition asked that the call be recorded, not that it go one way -> why it is ready: every Expected clause is an observable condition with its threshold (10 s; raises naming the survivor; included descendants; an excluded outsider). The Method asserts the same set and nothing more. Automated, Level and Tier are unambiguous, and Full is honest for platform cases with real processes. No arm verifies a requirement the row does not name, and nothing the row names goes unverified by its own arms. The Method's repetition of the Evidence cell's test names follows approved precedent (TC-153, TC-331) and does not hold the row back.

OUTCOME: APPROVE rows=1

SITTING: JUDGED kinds=first-approval
