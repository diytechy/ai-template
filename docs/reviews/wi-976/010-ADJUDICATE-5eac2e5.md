# WI-976 dispute sitting at 5eac2e5

DISPUTE: findings=RB3-F1

## RB3-F1: the merge-mint route widens a sitting by the adjudication row's tags

**The behaviour holds, and it is the defect sitting 004 already ruled.** I reproduced the reviewer's probe at this tip. For an amended SN-036:
- an authoring row tagged `scripts`/`personal-data` gets CROSS-PLATFORM and DATA-PROTECTION;
- the minted shape (`process`/`adjudication`) gets neither;
- WI-976's own tags (`process`/`ordinary`) give the same eleven hats as the minted shape, so this lane's sample sitting is unaffected.

Since sitting 004 (`004-ADJUDICATE-81e623b.md`, accepted), the only code change under `project-trajectory/scripts` or `scripts/coordinator` is `mkprompt.py`'s author-prompt rule. Neither `round_questions`'s widening nor the merge mint's row shape has moved. Sitting 004 ruled exactly this class, RB1-F1, SUCCESSOR. That successor is to make both routes widen by the authoring work item's declared tags, state so in LLR-360, and pin it with a test that composes both row shapes; the lane recorded it (D-006) to be filed at the landing. The reviewer could not see that verdict, so it found the class afresh.

**The convergence-class tag does not change the call.** I weighed it again and reach 004's conclusion:
- *Not a fail-open:* no gate reads the hat block. Under the 2026-09-06 ruling, a missing outcome is a review finding, never a check.
- *No data loss:* nothing is lost.
- *Not a Done-when gap:* the Done-when's tested states hold on the route it names, and its sample (this lane's checkpoint sitting, composed in-lane over WI-976) is unaffected, as the probe shows.

What the merge-mint route lacks is the authoring item's provenance on the minted row. That gap lives in `intake.py`'s mint, outside the spec's declared surface, and it is what the successor exists to close.

**Why DISMISS, and which class.** Ruling SUCCESSOR again would file a second row for the one defect the 004 successor already owes. A duplicate row is churn, not a fix.

Ruling FIX would undo an accepted ruling with no new fact. It would also pull the mint change into this lane, which 004 kept out for reasons that still stand: the routing `SafetyClass` cannot carry the lane's class, and the branchless sweep has no merged item.

The reviewer's fallback, to stop widening by the adjudication row's own tags here, would only half-solve it. It would trade FIRST-RUN-ADOPTER for nothing, while the successor is about to supply the right tags. And it would change LLR-360's rule twice in two rows.

Any further remedy in this lane therefore costs more than the defect it removes, which the successor already removes. The class stays owed. Nothing in this ruling releases it.

**For the checkpoint, not a ruling:** LLR-360 is Drafted. Its sitting may still weigh naming "the authoring work item's" tags, as sitting 004 noted, so that the successor implements a stated rule.

RULING: RB3-F1 DISMISS not-worth-cost the same route-dependent widening sitting 004 ruled as RB1-F1, unchanged since, already owed by that verdict's successor (both routes widened by the authoring work item's tags, with a both-shapes test); a second successor would duplicate it and an in-lane fix would undo an accepted ruling with no new fact, while this lane's own sample sitting is unaffected
