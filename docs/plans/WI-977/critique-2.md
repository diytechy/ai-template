Reviewed: e93ecf74cfb4dcd9dd45c3493ee4e8e2bdbe27e1

### PLAN-CRITIC — WI-977 — Round 2 — 2026-10-25

Fresh non-author session: the independent critic invocation assigned to `2026-10-25d-leg22/pcrit2-977`. This session did not produce the plan. No provider session id was supplied. Review stance: second and final single-plan critique, convergence. Carrier: this verdict file, for coordinator recording; no checkout changes or commit.

Rubric: `docs/rubrics/plan-decomposition.md` at the reviewed commit, blob `4f183eb6aa17a459c9b0741391791d03a8f76293`. Intent sources: the full committed `docs/work/active/wi-977/WI-977-one-work-item-per-lane.md`, its specref `docs/plans/2026-10-11-review-churn/README.md#15-one-work-item-per-lane` (owner revision 25, worker clarification revision 30), SN-027 in `docs/requirements/stakeholder-needs.toml`, and SR-144, SR-148, SR-156 and unchanged SR-026 in `docs/requirements/system-requirements.toml`. The supplied coverage report is the clause census. The artifact was read directly with `git show` at the bound commit; no text proxy was necessary. No earlier critique, decisions record, review directory, session notes, status or log was consulted. Revision commentary embedded in the required plan was not treated as independent evidence.

Rubric sufficiency: the anchors independently cover this planning intent. DevStg-Tests and B2 require substantive coverage of one-item admission, pre-mutation claim/resume/close refusal, worker preflight, historical evidence, spine amendments and shipping obligations; DevStg-Reqs checks executable build units; G4/B4 checks their order; DevStg-Impl/B3 checks the intentionally coupled decomposition; B1 checks ownership at existing seams. These are broader than any permissive test case and do not substitute a TC for the written intent. No additional failure class or new B-number is needed.

Anchor judgments:
- DevStg-Reqs: the rows and their detail identify bounded deliverables and checkable outcomes, including concrete refusal inputs and preserved one-item behavior.
- DevStg-Tests / B2: the deliverables substantively cover the reported D1–D20 clauses and F1. The exclusion notes leave unrelated SR arms unchanged rather than excluding the retirement contract. Historical joined subjects remain readable through a separate reader while new claims narrow. No Done-when gap found.
- DevStg-Impl / B3: D3 separates intent authoring from reconciliation to built code; D15 separates red-first evidence from the final sweep; F1 spans distinct signature/caller transitions. Those overlaps have distinct outputs and are not padding.
- G4 / B4: the resume-to-launch, dispatcher-to-claim and close-writer-to-composer ordering is coherent, except for the intermediate `_Lane` consumer identified below.
- B1: the plan consumes existing claim, lane, prompt, close and verdict seams; the inspected interface rows do not require a duplicate seam for scalar assignments.

DELTA: `none` is correct under the stated four questions. Removing `batch`, narrowing assignment cardinality and deleting a prompt slot add no state, domain value, input dependency or boundary crossing. The plan carries those removals and their adopter-facing consequences explicitly.

Transfer caveat: the debate/selection evidence comes from QA, math and code with objective verifiers; it does not benchmark plan artifacts, and reconciliation evaluated for plan quality remains an open research gap. This rubric is an extrapolation, not a proven instrument.

- [MINOR] B4 / G4 -> `docs/plans/WI-977/plan.md:232` changes `_Lane.wi_ids` to scalar `_Lane.wi_id` in W4, but line 546 assigns the corresponding `_poll` merged-count change to W10. At this commit, `project-trajectory/scripts/dispatch.py:888` reads `len(ln.wi_ids)`. In the supported dispatcher workflow, the first successfully merged lane after W4 therefore raises `AttributeError` before W10, contradicting the plan's runnable intermediate steps. The final deliverable already includes the fix, so this is an intermediate build-order defect, not a final Done-when gap, fail-open or data-loss finding; convergence severity is MINOR. -> Move `_poll`'s scalar-compatible merged-count update into W4 with the `_Lane` field change, and remove that implementation responsibility from W10. -> @plan-author

VERDICT: APPROVE findings=1
