# WI-911 adjudication 011: amendment re-sit of SR-234 (with SR-233, SR-236 and TC-334)

This re-sits sitting 010's return on the text at `8676e5c5f`. Since 010's act (`dcadf1481`) only SR-234 and TC-334 changed. SR-233 and SR-236 are the text 010 blessed, carried because the SR registry anchors whole. The SR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **TC-334's new evidence node exists and asserts the bound.** `tests/test_prompts.py::test_the_dispute_brief_offers_successor_and_never_for_a_convergence_class_finding` checks the shipped dispute directions for the SUCCESSOR ruling form and the exact sentence "A convergence-class finding (a fail-open path, data loss or a gap in the work item's Done-when) is never ruled SUCCESSOR: rule it FIX, or ESCALATE it."
- **The other TC-334 SUCCESSOR evidence still exists:** `test_a_successor_ruling_is_accepted_and_parsed` and `test_a_dispute_verdict_ruling_a_finding_successor_is_valid_and_bound`.

## amendment

- [MEANING] SR-234 Requirement and AcceptanceCriteria -> (anchor b803dd019) preserve each contested or third-round finding and accept only a verdict ruling each exactly once as a fix, a reasoned dismissal or an escalation -> "a successor row" joins the ruling set, and the Requirement now also obliges the adjudication content to direct the sitting to rule out a successor row for a fail-open, data-loss or Done-when-gap finding. The AC adds that a SUCCESSOR has a reason, an unknown ruling names the set, and the shipped dispute directions carry the bound -> a new ruling and a new obligation. **Blessed.** Sitting 010's return is answered:
  - **The Requirement states the bound,** so the AC no longer observes an obligation the Requirement never made.
  - **It is stated as what the delivered content does** ("direct the dispute sitting to rule out"), and the AC observes the shipped directions rather than promising a judge's output.
  - **TC-334 verifies it directly,** with the test above, as an SR-234 child.
  - **No file is named** in either cell, and the condition stays fronted (`Where ...`).
- [MEANING] TC-334 Expected (and one Evidence node) -> verify the dispute brief, the findings refusals, the verdict parse including SUCCESSOR, and the entry point -> it adds that the shipped dispute directions rule out SUCCESSOR for a convergence-class finding (fail-open, data-loss or Done-when-gap), backed by the new prompts test -> a new verification obligation. **Blessed.** It closes SR-234's new clause with a test that asserts the shipped sentence verbatim. Its `Full` tier, blessed at 010, is unchanged.
- [MEANING] SR-233 AcceptanceCriteria -> (anchor b803dd019) the review scope's normal-environment boundary, one definition, the recorded one-line dismissal, and briefs that cite it -> it adds reachability-tied severity directions, the contrived-scenario definition, re-grading, the promise bound, dispute plausibility, out-of-set classification, and the convergence review's confirmations, tags and reachability gate -> new acceptance conditions. **Blessed**, unchanged since 010. Each clause makes concrete the Requirement's "limit findings to defects reachable in a normal working environment". It is stated as directions or ruling-party acts, as the row's approved text already is. LLR-311 and TC-332 decompose and verify it.
- [MEANING] SR-236 Requirement and AcceptanceCriteria -> (anchor b803dd019) a dispute-ruling exclusion resolves a finding only on an accepted dismissal of the same finding -> an accepted dismissal or successor ruling of the same finding resolves it, and a ruling of another finding or round, or any other ruling, is refused -> the resolving set widened. **Blessed**, unchanged since 010. LLR-069 and TC-069 decompose and verify it, and the plan-cap path stays DISMISS-only.

VERDICT: MEANING rows=4

**Aftermath:** this session re-attests all four rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests SR-233,SR-234,SR-236,TC-334`

SITTING: JUDGED kinds=amendment
