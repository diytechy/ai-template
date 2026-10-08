+++
id = "WI-852"
title = "The coordinator renders its review and critique briefs from the kit's templates"
workstream = "process"
sr_refs = ["SR-146", "SR-154"]
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
needs = ["WI-860"]
+++

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §4(a),
§6 and §7.4; rows P5 and P8, folded together by the queue reconciliation §8.1).

The coordinator hand-writes each Sol brief from untracked templates in
`C:/Projects/ai-template.wt/coordinator-tools/`, not from the kit's
`prompts/reviewer.template.md`. That template asks the reviewer to name the
failure classes a change admits and hunt those first, and to say for a
guard-adding remedy why the defect cannot be made unrepresentable. The hand
brief asks for neither, so WI-841's findings arrived as instances and were
fixed as instances. The coordinator's `sol-review-*.md` files also use their
own format, so the generated verdict rollup sees no coordinator-era lane.

Render only: WI-801 owns launching (`ask.py`), so no coordinator launch script
enters the repository.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- The coordinator's narrow-round review, its full-lane review and the scope
  critique (ruling 2) are rendered through `prompts.py` from
  `prompts/reviewer.template.md` and `prompts/critique.template.md`, with the
  lane's facts as fill values. No brief is hand-composed.
- The scope critique carries ruling 2's two questions (each independently
  landable deliverable, and whether a file gains authority over a hold, an act
  or a gate) and a scope rubric under `docs/rubrics/` as its rubric input.
- A coordinator review is written as a kit round file
  (`docs/reviews/<scope>/NNN-REVIEW-A-<sha>.md`), so the verdict gate and
  `gen_verdict_rollup.py` read it.
- The coordinator-tools brief templates retire. What they carried that the kit
  templates lack (the scratch-root and basetemp rules, the regenerated-views
  note) moves into the fill values or the kit templates.
- WI-847's narrow-round render is this render.
- Tests:
  - a rendered review brief carries the failure-class and unrepresentable
    clauses;
  - an unfilled slot refuses;
  - a coordinator round file appears in the rollup.
- Its rows (SR-146's and SR-154's chains) are authored as one change set and
  judged in one combined sitting.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit if a shipped template
  changes.
