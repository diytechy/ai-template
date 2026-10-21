# WI-940 checkpoint sitting at c0ce587

## first-approval

One row awaits a first approval: TC-374. I read it against both chains it hangs under (SR-026 with LLR-026, LLR-061, LLR-143 and their TCs; SR-238 with LLR-026, LLR-270 and theirs), against IF-302's data cell, against the WI-940 spec's anchor section and arms map, and against the coordinator's scope facts. It is not ready.

- [RETURN] TC-374 -> the obligation it claims: run eight named tests and assert that the shared Windows job module imports without loading kernel32, that the session reaches its shared declarations, that the active-process reader governs the session-tree bound, that the CPU reader sums user and kernel time, and that an unnamed joined job reports its descendants while excluding an outside process. Its Verifies cell names SR-026, SR-238, LLR-026 and IF-302 -> what its chain shows: the row's arms fall into three groups, and only two of them have a home in what it claims to verify.
  1. **The session-tree arms.** An overrun raises naming the survivor, and an unopenable member raises. These are SR-238's and LLR-026's: the 10 s bound, and the member-handle rule. Both tests are already TC-026's evidence.
  2. **The move-validation arms.** The deferred kernel32 load and the session reaching the shared helpers. These are IF-302's seam, and the arms map places them there.
  3. **The CPU-reading arms.** User plus kernel time; a joined job counting an exited grandchild; an outside process excluded. These verify IF-302's `create_joined_job` and `job_cpu_seconds`. Those serve only this repository's smoke-budget step, which the spec states no SR or LLR covers, and SR-238 and LLR-026 say nothing of CPU accounting.

  Nothing in the row verifies SR-026, a headless resume with stdin closed so no prompt wedges the loop. The coordinator's scope facts say the SR and LLR ids were added because the registry refuses a TC that verifies an interface row alone -> why it is not ready, three findings:
  - (1) **A false verification claim.** `Verifies` names SR-026 while no arm, no evidence node and no Expected clause touches SR-026's criterion. A trace link entered to satisfy a schema rule claims coverage the row does not give, and it inflates SR-026's coverage in every reader that counts it. SR-238 and LLR-026 are honest links for the session-tree arms, and they already satisfy the schema rule on their own.
  - (2) **Expected does not say which condition holds which verified row.** It states IF-302's provisions alone, so a reader cannot tell which arms satisfy SR-238 and LLR-026 and which hold only the interface. The CPU-reading arms then read as SR-238 coverage they are not. Acceptance must be the observable condition per claimed row, not an interface inventory.
  - (3) **A design smell, surfaced as a separate finding and not fixed here.** IF-302's owner is a shipped kit module, so `create_joined_job` and `job_cpu_seconds` ship to every adopter as behaviour no requirement states. IF-302's own notes concede they serve "untraced local callers outside the architecture map". Either the CPU readers move to this repository's own tooling, leaving the shipped seam the session contract alone, or a requirement row states why the kit ships them. That is the coordinator's or owner's call, not this TC's text to settle.

  The Method's repetition of the evidence names follows approved precedent and is not one of the findings.

OUTCOME: RETURN rows=1

## Dispositions answered in the lane (wi-940 D-009)

```toml
title = "WI-940 TC-374: verify only what it holds - drop SR-026, state Expected per verified row, and settle where the joined-job CPU readers live"
workstream = "process"
sr_refs = ["SR-238"]
needs = ["WI-940"]
safety_class = "ordinary"
buildtier = "medium"
```

This is spine text, plus one placement decision. Do two things in TC-374:
- Remove SR-026 from `Verifies`. No arm verifies SR-026's headless-resume criterion, and SR-238 with LLR-026 already meets the rule that a TC may not verify an interface row alone.
- Rewrite `Expected` as the condition per verified row:
  - SR-238 and LLR-026: the session job's active-process reader governs the tree-end bound, so an overrun past 10 s raises naming the survivor and an unopenable live member raises after the terminate;
  - IF-302: the module imports without loading kernel32, the session reaches the shared declarations, and an unnamed joined job's CPU reading sums user and kernel time, counting its exited descendants and excluding an outside process.

Then settle the CPU readers' home, recording the call. Either move `create_joined_job` and `job_cpu_seconds` out of the shipped kit module into this repository's own tooling, narrowing IF-302's data to the session contract and moving their three tests' citation off TC-374. Or keep them shipped and draft the requirement row that states why adopters receive them, TC-first. Re-sit TC-374 for first approval once its text matches.

SITTING: JUDGED kinds=first-approval
