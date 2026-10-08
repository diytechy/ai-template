+++
id = "WI-849"
title = "An independent adjudicator may take the approval act in the authoring lane, kit-wide"
workstream = "process"
sr_refs = ["SR-178", "SR-156"]
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §7.1b,
row P2), carrying the owner's ruling 6 of 2026-10-07
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`): an independent
adjudicator may take the approval act in the authoring lane, kit-wide. It
supersedes the trunk-side clause of the 2026-09-01 ruling. The WI-788 design
already moves acts into the lane (README change 8), so this row is that
change's docs and rung, landed on today's machinery.

Today the merge slot admits a lane's acts only when every claimed spec is of
the `adjudication` kind (`integrate._adjudication_lane`), so an ordinary lane
carrying acts is refused, and the coordinator's in-lane acts stay unjudged
because it lands by hand. WI-841 already built the question the rung should
ask: is each act backed by an accepted verdict that judged that act's own
rows (`kitlib.sitting.unaccepted_refusal`, `uncovered_refusal`)?

Not this row: switching the coordinator's landings to the slot is WI-808's
("Both paths yield one landing per lane"). WI-809 builds the loop's in-lane
lifecycle on this rung.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- PROCESS.md §4's "Fixed points" sentence, process-options "Who performs the
  approval act" (with its division-of-labour table) and the `spine-authoring`
  preamble state the one rule: the approval act is an independent
  adjudicator's, never the session's that authored the rows, taken in the
  authoring lane or on trunk.
- The merge slot's approval-act rung admits a lane's acts when every act is
  backed by an accepted verdict from a session that did not author the rows,
  judging that act's own rows. This replaces "every claimed spec is
  adjudication kind" as the actor test. A lane act with no such verdict is
  refused, naming the act and the reason.
- TC-218's method, LLR-158 (and its `code_symbol`) and
  `prompts/worker.template.md`'s approval-act paragraph state the rule, so the
  doc never runs ahead of the check. These move here from WI-809.
- The rows it amends (SR-178's chain: LLR-158, LLR-278, TC-218, and any it
  adds) are authored as one change set and judged in one combined sitting.
- Tests: an in-lane act backed by an accepted, independent verdict merges at
  the slot. Each of these is refused: no verdict, a failed verdict, a verdict
  judging other rows, and a verdict from the authoring session.
- Byte deltas on PROCESS.md and process-options are re-stamped
  (`byte-budget-guard`).
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. An adopter's loop lanes
  gain the admitted path; nothing that merged before is refused.
