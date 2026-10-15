# WI-913 adjudication 011: amendment re-sit of SR-154 and TC-333's Tier

This re-sits what sitting 010 returned (SR-154, its Dispositions items 1 and 2) and advised (TC-333's `Tier`), on the text at `c338f81da`. The SR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What changed since 010, read from the cells and D-008:**
- **The family clause is gone.** "its critique is launched from a model family other than the planner's" is removed from the AcceptanceCriteria, as item 1's first option asked.
- **The planning hold is in the obligation form.** It is now a second predicate under the Requirement's one `shall` ("...escalated through the declared approval level, and, where a claimed work item is marked for an in-lane single plan, refuse build output..."). The unattended condition moved behind the `shall`, so it scopes only the routing predicate. D-008 records this as the owner's in-session choice (2026-10-15), over a second `shall` that the one-`shall` rule would report. That meets item 2's intent, an obligation rather than a description, within the registry's form rule. I take the owner's choice as given and judge the text it produced.

**Checks:** `trace.py --strict` reports nothing new for SR-154 or TC-333. The `Form` advisory on SR-154 predates this lane.

- [MEANING] SR-154 Requirement, AcceptanceCriteria and Rationale -> (anchor c10cce0bb) when unattended work reaches integration, obtain each review or critique verdict the declared policy requires from a non-author session, routed across declared families with documented degradation, every selection logged and non-convergence escalated -> the same routing obligation, now scoped by a condition placed after the `shall`, plus a second predicate: where a claimed item is marked for an in-lane single plan, refuse build output at its making or landing until a pass record binds its plan and Done-when. The AC adds the observable conditions of that hold: plan coverage or reasoned exclusion; a delta of `none` or carried within scope; one revision with a fresh critique; at the cap, only an accepted dismissal of every blocking or major finding, else the owner; a fresh record after a plan or Done-when change but not after a tick or evidence; the closed plan-mark set, with an unrecognized mark held. The Rationale gains a fan-out re-stamp -> a new obligation and its acceptance; the reordering alone would have been clarity, but the added predicate is not. **Blessed.**
  - **Upward:** SN-026 and SN-024's second opinion, which the row realizes, now gates the single plan's build as well as integration, the Q7 placement.
  - **Each AC clause observes something the Requirement states,** either the hold or what a binding pass record consists of. The clause that 010 found unstated, without a degradation path and unverified is gone.
  - **Downward:** the hold is verified through LLR-337 and TC-367, and the record's preconditions through LLR-313 and TC-333, all approved at 010.
  - **The re-stamp gives a reason a reader can argue with,** and the cross-family routing obligation still carries its own degradation in the first predicate.
  - **Advisory:** "fresh independent critique" names a second round that the filing does observe (round 2, bound to the revised plan, coverage over the first findings). The critic's independence from the planner is still a launch procedure, like the clause removed, which no check reads. It is not a new defect, since the word restates the row's own non-author premise rather than adding a specific unverifiable condition. A later edit could say "a second fresh critique".
- [MEANING] TC-333 Tier -> Smoke: the cheapest tier at which every cited arm runs is the per-commit smoke tier -> Full: that tier is the full suite -> the verification claim changed. Under the new cell, evidence could leave the smoke tier, which the old cell forbade. **Blessed.** The cited `test_review_brief_git` and `test_plan_filing` are both in `tests/conftest.py`'s `SLOW_MODULES`, so `Smoke` over-claimed. `Full` is the honest label under TC-205's rule that the tier is the whole cited set's. The Expected and Method still say which brief renders stay per-commit, so nothing promised about the smoke tier is lost.

VERDICT: MEANING rows=2

**Aftermath:** this session re-attests both rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests SR-154,TC-333`
