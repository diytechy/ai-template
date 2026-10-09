+++
id = "WI-853"
title = "Every review finding is a clause the rework plan must cover before the fix is dispatched"
workstream = "process"
sr_refs = ["SR-155", "SR-236"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
needs = ["WI-852"]
+++

## Deliverable

`plan_coverage.py --findings` now also reads a review verdict: through one shared step, `finding_clauses`, its finding lines become the clauses F1..Fn in the order written (a declared `F#` file reads as before; mixing the two shapes is malformed). The coordinator's attended rework round runs the gate over the builder's plan and dispatches the fix only on exit 0 (the session-protocol skill, which WI-848 moves into the coordinator-cycle skill); WI-805's loop replan is to call the same step. An `F#` exclusion citing a dispute verdict resolves the finding only when an accepted DISMISS ruled that same finding, shown by the findings file kept beside the verdict recording the excluded finding's text; a FIX or ESCALATE ruling, an unaccepted call, another finding or a missing file is a finding. Known limit (dispute 006, DISMISS not-worth-cost): two dispute rounds in one lane reusing finding ids refuse a valid dismissal (fail-closed); the class fix, binding the findings file into the sitting's binding, is filed as a follow-up row. Rows: SR-236 (derived; the dispute sitting 003 ruled SR-155 does not state the gate) drafted and approved (verdict 004, act 79); LLR-069 and TC-069 amended, judged MEANING and re-attested twice (verdict 001, act 77; verdict 004, act 78); IF-046 merged by meaning with WI-870's text (D-004); IF-287 and IF-290 gain `plan_coverage` as a requestor. Codex 6.1 Sol (medium): two fresh full-lane reviews; the second's one finding was dismissed by the final dispute ruling (`docs/reviews/wi-853-findings-gate-in-rework/sol-review-full.md`, D-005). Decisions: `docs/decisions/wi-853.toml` (D-001 to D-006).

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §4(b),
row P6). WI-803 built `plan_coverage.py --findings`, which makes each open
finding an `F#` clause a replan must cover, but nothing calls it. At WI-841
each fix covered the instance a review named (the carrier check fixed for
TOML, then CSV, then markdown), and the next fresh review found the sibling.

The loop's half belongs to WI-805's replan, whose Done-when already runs this
gate. This row builds the shared step and the coordinator's half.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- One shared step turns a review verdict's finding lines into the `F#` clauses
  `plan_coverage.py --findings` reads. The coordinator's rework and WI-805's
  replan both use it.
- The coordinator's rework round runs
  `plan_coverage.py --item <spec> --findings <review>` over the builder's plan
  (the sweep table of the `coordinator-cycle` skill: finding, class, every site
  of the class with the search that found it, and the one owning boundary). The
  fix is not dispatched until every `F#` is covered or excluded with a reason.
- A finding the builder disputed and the adjudicator resolved counts as
  covered, citing the resolution (WI-811).
- Tests: an uncovered finding refuses the dispatch; a covered or excluded one
  passes; a resolved dispute passes.
- Its rows (SR-155's chain: LLR-069 and its TC) are authored as one change set
  and judged in one combined sitting.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
