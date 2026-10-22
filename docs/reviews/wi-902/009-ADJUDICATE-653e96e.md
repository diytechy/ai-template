# WI-902 adjudication 009: dispute on review 008

Range: `ccd663919..4a8e7f64c`. The code is unchanged at HEAD `653e96e0b`, which adds only the review and the findings file. Scope bound: project-trajectory/PROCESS.md §6 "Review threat model". Only finding DB (review 008 F1) is disputed. F2 (MINOR) is not before me.

## Finding DB: a refused landing sweep is later replayed as if it had been consumed

**What the code does.** `_merged_dispositions` (`intake.py:1781-1815`) sets `consumed = bool(adoptions) and _landed_before(root, before, hit.name)`. `_landed_before` (`intake.py:1818-1831`) answers one question: did `complete/<disposition spec>` already exist at `before`? With `consumed` set, `adoption_lineage` calls `row_refusal(..., consumed=True)`, which finds the adopted item in any state and checks only its `Supersedes`.

The trouble is that the spec exists in `complete/` after a landing sweep that REFUSED the adoption, exactly as it does after one that accepted it. The landing refusal leaves the merge standing, mints nothing and writes no record. So the next bare sweep (`before = after = HEAD`) reads that refused adoption as already consumed. It skips the open-state rule and re-points the dependents.

**Reproduction.** I ran it myself, outside this worktree, using `tests/test_intake.py`'s own real-git constructors (`_adopted_lineage`, `_sweep`, `intake.intake_after_merge`):

| Successor state | Landing sweep | Bare sweep that follows |
| --- | --- | --- |
| complete | Refused: `adopts WI-020, which names no open row (draft/queued/active) on trunk - nothing minted`. WI-021 still needs WI-005. | Printed `re-pointed queued/WI-021-waiter.md's edge(s) WI-005 -> WI-020`, returned 0. WI-021 now needs WI-020. |
| cancelled | The same refusal. | The same re-point and exit 0. WI-021 now waits on a cancelled row. |

**Why this is a defect, not an accepted residual.** The approved spine says otherwise:
- SR-148's acceptance (re-anchored at sitting 006) admits only "an already-open item that supersedes it".
- LLR-335 (approved at sitting 007) allows the lineage-only read only "on a replay after the disposition was already consumed". A refused adoption was never consumed.

The code therefore breaks both rows, and it breaks the invariant this whole row protects: OI-73's rule that an early close must leave a live continuation. In the complete case, the dependent is released while the partial work has no open successor. In the cancelled case, it is parked on a dead row. Both outcomes come back with exit 0 from the recovery command that the refusal path documents. A refusal that the next `intake.py sweep` silently overturns is a fail-open.

**The coordinator's position, weighed.** D-001 does record this exact gap, so the lane did not hide it. But the record does not settle it:
- D-001's own `why_not_escalated` hands the call to review ("the next Sol round judges it").
- Its `review` is empty, it carries no `owner` key, and it is listed in `high_risk`. So the owner has neither confirmed nor overruled it.
- A delegated decision cannot make code that contradicts two approved rows conformant. Keeping the gap would mean amending SR-148 and LLR-335 to allow it, and that amendment has not been made.

**Scope.** The reproduction needs only agent-written repository content (a disposition adopting a row that is already closed) and the kit's own documented recovery command. That is inside §6. Nothing about the host is contrived.

**Worth.** The coordinator objects that the reviewer's remedy is D-001's rejected alternative, a durable consumed marker with authority over the re-point. That objection does not decide the finding, because the fix does not need a new carrier. The thing to fix is the replay test: "the disposition spec existed at `before`" has to become "the first consumption accepted this adoption".

That fact can be re-derived from git, which the sweep already reads. For example, apply the open-state rule against the registry in the tree where the disposition landed in `complete/`. That reproduces the landing sweep's own verdict, deterministically and on every replay, and writes nothing. The lane may choose another mechanism that binds replay to successful consumption, but a guard bolted on top of the current existence test would not do.

Either way, the cost is one function's eligibility rule, a rejected-then-replayed regression for both terminal states, and the LLR-335/TC-360 wording that the change touches. The defect it removes is a silent fail-open on the row's central invariant. ESCALATE does not apply: the approved spine already answers the question. What remains open is D-001's record, and the coordinator should mark it superseded by this ruling.

RULING: DB FIX replay eligibility (_landed_before: disposition spec present at `before`) is also true after a REFUSED landing sweep, so a bare sweep accepts the refused adoption on lineage alone and re-points dependents to a complete or cancelled successor (reproduced, exit 0), contradicting SR-148's already-open acceptance and LLR-335's "after the disposition was already consumed"; bind replay to evidence that first consumption accepted (derivable from git, no new carrier needed) and add the rejected-then-replayed regression
