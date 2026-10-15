# WI-913 adjudication 010: lane checkpoint at 76dc6746a (amendment; first-approval)

I judged the rows as they stand at `76dc6746a`, reading their chains in the live registries and checking the trace homes against the code. The SR, LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **Tests:** every `Evidence` test named by TC-333 and TC-367 exists.
- **Symbols:** all 38 of LLR-337's `CodeSymbol` entries resolve in `plan_gate.py` or `kitlib/plan_pass.py`.
- **Checks:** `check_trajectory.py --strict` raises only staleness and overlap warnings for the WIs that cite SR-154. `trace.py --strict` raises only the SR-154 `Form` advisory, which predates this lane.
- **Shared code:** the filing step's pass form (`review_brief.py:822`) calls `plan_gate.record_problems`, the gate's own check, so the writer and the gate apply one rule.

## amendment

- [MEANING] SR-154 Requirement, AcceptanceCriteria and Rationale -> obtain each review or critique verdict that the declared policy requires at unattended integration from a non-author session, routed across families with documented degradation -> it adds: where a claimed item is marked for an in-lane single plan, build output is refused at its making or landing until a pass record binds its plan and Done-when; the AC adds the plan's coverage and delta, a cross-family critique launch, one revision with a fresh critique, dispute dismissal or the owner at the cap, re-recording after a plan or Done-when change, ticks exempt, and the closed plan-mark set; the Rationale adds a fan-out re-stamp -> a new obligation, new cases and a new actor ("the delivered planning control"). **Not blessed.** The single-plan gate itself is sound, and hanging it from SR-154 is the filing's ruled call (Q7). One AC clause cannot stand: "its critique is launched from a model family other than the planner's".
  - **The Requirement does not state it.** Its first sentence makes family routing apply when unattended work reaches integration, with degradation to a documented same-family mode. Its second sentence, the only one about the single plan, says nothing about the critic. The AC therefore observes an obligation the Requirement never makes, the defect that sends a row back.
  - **It has no degradation path,** unlike the routing obligation it echoes. In a repository with one configured family, the clause can never be met, and nothing says what happens then.
  - **Nothing verifies it.** The row's Verification is `Test`, but no TC or test checks the critic's family. The lane's own spec says the filing "validates the critique's text, not its author", and the launch is an attended step in the coordinator's skill. Review 008's MINOR on SR-154 flagged exactly this. The checkpoint reworded the clause ("has an independent cross-family approval" became "is launched from a model family other than the planner's") but did not move or verify it.
  - **Also in that text:** the new Requirement sentence says "refuses" where the registry's obligation form is "shall refuse".
- [MEANING] LLR-313 Detail and Title -> render and file attended review and scope-critique briefs, accept only a canonical bound verdict, file round records -> it adds:
  - the first and second plan critiques (bound to their lane commit, coverage over the Done-when, the second also over the first critique's finding ids without their text, in convergence stance, refusing a revision that leaves a first finding uncovered);
  - the strict single-plan brief and its revision mode;
  - critique filing, the pass record's preconditions, and the cap's dispute findings file;
  - the title widens to cover them.

  New behaviour and refusals. **Blessed.** Upward, its plan arms decompose SR-154's planning sentence, which I do not contest, and the AC clauses that sentence derives (coverage, delta, one revision, the cap). The returned family clause is not stated here. Sideways, it owns the writer side (render, file, pass form), while LLR-337 owns the commit-time reader. Both read one record grammar (`kitlib/plan_pass.py`) and one check (`plan_gate.record_problems`), so the two consumers cannot disagree. Downward, TC-333 names a test for each new arm. It has no `shall`.
- [MEANING] TC-333 Expected and Method -> verify the attended review and scope-critique renders, refusals, filing and rollup -> it adds per-commit single-plan brief renders and refusals, and full-suite plan-critique rendering, filing, the pass form and the cap cases (a MINOR before a MAJOR, two blocking findings with one dismissed, a revision missing a first finding, line-ending conversion against a real edit), the second brief never carrying first-critique text, writing only the record, the missing-input and beyond-delta refusals, and the catalogued, skill-free planner template -> the verification obligations grew. **Blessed.** The Method is closed over LLR-313's new arms, and every named test exists.
  - **Advisory:** the row's `Tier` is still `Smoke`, while its evidence includes `test_plan_filing` and `test_review_brief_git`, both in `SLOW_MODULES`. The Expected says honestly which half runs where. The `Tier` cell (not amended here) should read `Full`, by TC-205's own rule that the tier is the whole cited set's.

VERDICT: MEANING rows=3

**Aftermath:**
- **Re-attested by this session:** LLR-313 and TC-333, in their own act commit: `python project-trajectory/scripts/intake.py snapshot --reattests LLR-313,TC-333`.
- **Not blessed:** SR-154. It stays drifted, and the SR registry stays unanchored, until its corrected text is re-sat.

## Dispositions answered in the lane (sitting 011 approved and anchored the reworked rows)

```toml
title = "WI-913 spine rework: SR-154's single-plan acceptance states only what its requirement derives (answer checkpoint 010)"
workstream = "process"
sr_refs = ["SR-154"]
needs = ["WI-913"]
safety_class = "ordinary"
buildtier = "medium"
```

Spine text only; no code change is called for.

1. Remove "its critique is launched from a model family other than the planner's" from SR-154's AcceptanceCriteria. The alternative is to state the critic-family obligation in the Requirement, with its configured-family condition and the documented same-family degradation the first sentence already allows, and to name a verification that can observe it (`Attest` or `Demonstrate`, because the filing reads text, not author). The launch procedure itself belongs to the coordinator-cycle skill's carrier, not to an acceptance clause no check reads.
2. Write the Requirement's single-plan sentence in the registry's obligation form ("shall refuse").
3. Re-sit SR-154 alone. LLR-313, TC-333, LLR-337 and TC-367 are judged at this sitting and need no re-sit unless the rework touches them.

## first-approval

- [APPROVE] LLR-337 -> the single-plan pass gate:
  - **Scope:** it reads only rows claimed in the lane's own active folder at the claim base, under a closed plan-mark set. Absent, empty, `none` and `dual` pass; `single`, any other value and any non-string are held by name.
  - **Before a record:** the closed record homes and a close may change. Any other change is build output, refused unless a parent holds a pass record binding the row, the plan digest and the Done-when digest.
  - **A changed pass record** is checked against its first parent: the nine-key grammar, a `none` or `within` delta line from the plan, matching digests, a byte-identical bound critique of round 1 or 2, and, for a second-round non-approval, an accepted DISMISS of every blocking and major finding.
  - **Where it runs:** on staged, squash-carried and landing commits oldest first; a merge against every parent; an unattributed squash and unreadable inputs held.
  - **Exempt:** trunk and lanes with no `single` row; a tick or added evidence never unbinds a record.

  -> **Upward:** SR-154's planning sentence ("refuses build output at its making or landing until a pass record binds its plan and Done-when") calls for exactly this. The returned AC clause (the critic's family) is not one this row states or implements, and the rework drafted above leaves this row unchanged, so returning SR-154 withholds nothing from it. **Sideways:** it is the reader beside LLR-313's writer, through one shared check. **Downward:** TC-367 names a test for each arm, all existing.

  -> **Ready.** One decision (commit and landing admission from bound evidence), the right parent sentence, no `shall`, and trace homes that agree.
  - **Advisory:** the cap and dismissal arm (`_cap_problems` and `_dismissals`) is exercised by the `at_the_cap` tests that TC-333 cites, through the pass form's call into `record_problems`, rather than by a test TC-367 cites. Adding those tests to TC-367's Evidence, or LLR-337 to TC-333's Verifies, would make the link explicit. The code under the claim is tested either way.
- [APPROVE] TC-367 -> drive a claimed single-plan lane through the pre-commit, squash and landing checks before and after a pass record. Exercise plan and Done-when edits against a tick; absent, unreadable, malformed, other-row and other-digest records; parent support; each record home and a close; rebase and merge; the claimed plan mark, including a non-string one; trunk and a lane with no `single` row; an unattributed squash; a past-cap critique; the shipped hook's step list; the refresh merge's compiled log and views against a view regenerated outside a merge; and a critique that reviewed another Done-when -> it verifies SR-154, LLR-337 and IF-295, with 30 named tests, all existing. Its Expected is a condition (held until a supported record binds, unbound by a change but not by a tick, the closed set, one record grammar) -> **Ready.** It is closed over LLR-337's arms except the cap arm noted above, and claims nothing its tests do not show.

OUTCOME: APPROVE rows=2

**Act:** after the re-attestation act above, flip LLR-337 and TC-367 to `Approved` and run `intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-913;docs/test/test-cases.toml=WI-913"`, in one commit.

SITTING: JUDGED kinds=amendment;first-approval
