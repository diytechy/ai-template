+++
id = "WI-853"
title = "Every review finding is a clause the rework plan must cover before the fix is dispatched"
workstream = "process"
sr_refs = ["SR-155"]
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
needs = ["WI-852"]
+++

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
