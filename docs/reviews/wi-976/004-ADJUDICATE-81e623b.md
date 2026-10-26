# WI-976 dispute sitting at 81e623b

DISPUTE: findings=RB1-F1

## RB1-F1: the sitting's hat set depends on the route that composed it

**The finding holds at this range.** I reproduced it with the lane's own composer. `plan_briefs.sitting_hat_block` builds its contexts as the composing row's own context plus each parent need, every need widened by that row's `Workstream` and `SafetyClass` (`hat_surface_for_work_item`, `_hat_parent_context`). The two routes hand it different rows:
- `scripts/coordinator/compose_lane.py` passes the authoring work item's row, overriding only `Brief`, `Adjudicates` and `SR-Refs`.
- The merge-mint route passes the minted adjudication row. `intake._first_approval_drafts` and `_amendment_drafts` hard-code `"workstream": "process"`, and `agent_loop.session_body` composes from that row. It carries no link back to the authoring item.

Results:

| SR | lane tags | in-lane route | merge-mint route |
|---|---|---|---|
| SR-157 | `scripts` | includes CROSS-PLATFORM | no CROSS-PLATFORM |
| SR-161 | `unattended` | includes UNATTENDED-OPS, no FIRST-RUN-ADOPTER | no UNATTENDED-OPS, includes FIRST-RUN-ADOPTER |

The builder's sweep of 109 differing work items out of 403 is consistent with this. `compose_lane.py`'s own docstring says it exists "so the adjudicator reads the brief the merge's mint would hand a sitting", and with the hat block that is no longer true.

**It is in scope and reachable.** The merge-mint route is the kit's shipped route: an adopter's loop lands a lane carrying Drafted SRs, and intake mints the sitting the loop then composes. No hostile host, hand edit or contrived ordering is needed, so PROCESS.md §6's bound does not exclude it. The effect is the one SN-036 names: a perspective applicable to the decomposition's own work goes unasked on one route.

**It is not convergence-class, so SUCCESSOR is open.**
- *Not a fail-open:* no code gates on the hat block. Under the 2026-09-06 ruling the spec carries, a missing outcome is a review finding, never a check, so no gate passes what it should refuse.
- *No data loss:* nothing is lost.
- *Not a Done-when gap:* each route widens by the tags of the row it is handed. The Done-when's tested states (the closed round predicate, the per-need widening, the slot, the combined sitting, the roster refusals, the author prompt "computed from the lane's work item") hold, and this lane's own checkpoint sitting composes in-lane over WI-976, whose tags agree with the minted shape for its SRs.

The defect lives in the minted row's provenance. That is the merge-mint route in `intake.py`, outside the surface the spec declares (the roster reader, the sitting-brief composer, the planner briefs' applicability function and the coordinator's prompt filler).

**Why not FIX here.** The right remedy is a design call, not a one-liner:
- Remedy (b), which makes the in-lane route compose the minted shape, is cheap. But it gives every sitting FIRST-RUN-ADOPTER and drops lane-specific hats such as CROSS-PLATFORM. That fixes the inconsistency by choosing the less informed set.
- Remedy (c), dropping the work item's tags from a sitting's widening, contradicts the Done-when's "widened by the work item's tags".
- The remedy that keeps the right set is (a): the minted row carries the authoring lane's tags. It touches the mint, needs a cell other than `SafetyClass` (which means `adjudication` on a minted row and routes it), and must answer the branchless sweep.

That is its own row, under CLAUDE.md's "edit conservatively", and it lands better after this lane than widening this lane's surface past its declared one.

**For this lane, not a ruling:** LLR-360 is Drafted and will be judged at the checkpoint sitting. Its phrase "the work item's declared tags" does not say which work item. That sitting may weigh naming the authoring work item, which is the intended meaning and the one the in-lane route computes, so the successor implements a stated rule rather than choosing one.

RULING: RB1-F1 SUCCESSOR make both routes widen a sitting's parent needs by the authoring work item's declared tags: carry the merged lane's Workstream and SafetyClass (in a cell other than the routing SafetyClass) or a link to it onto every minted first-approval and amendment row, resolve the branchless sweep, state in LLR-360 that the authoring work item's tags widen, and add a test that composes the minted row shape and the in-lane shape for one SR and asserts one hat set
