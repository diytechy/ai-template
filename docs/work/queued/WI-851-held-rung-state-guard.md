+++
id = "WI-851"
title = "Held-rung spine rows are protected by state: the registry, the snapshot and the dial"
workstream = "process"
sr_refs = ["SR-208", "SR-178"]
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
needs = ["WI-828", "WI-849"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §7.1,
row P4), carrying the owner's ruling 5 of 2026-10-07
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`): held-rung rows are
protected by state alone. The rule judges what lands from a lane. A direct
trunk approval by the owner or an authorized approver is not judged.

Today two checks protect a held rung, and neither judges state:
- `held-status` (pre-commit and a merge-slot rung) is armed only for commits
  carrying the `Loop-Session` trailer. "A person's own lane is not governed",
  and no coordinator-path commit carries the trailer, so a coordinator lane
  counts as a person's.
- `held_reattest_refusal` requires an adjudication act to name a CLARITY
  verdict in the act ledger.

The coordinator lands by hand, so the rule rides the lane-commit walk that
WI-828 makes shared between the merge slot and the hook's squash and merge
paths.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- On every lane commit, judged against its parent, a row is refused when all
  of these hold: its registry's rung is held by the dial as committed on
  trunk; the commit moved the row's snapshot copy; and the live row equals
  that copy. The one exception is a row whose Status is unchanged and which a
  verdict in the lane's range rules CLARITY, bound to its exact text by a
  digest. The refusal names the row, its rung and the dial.
- The walk is WI-828's shared lane-commit walk: the merge slot, and the hook
  on a squash or merge landing. A plain trunk commit is not judged.
- The trailer-armed arm of `held-status` (LLR-246's loop-marker condition) and
  the act-ledger CLARITY arm (LLR-278's held clause) retire into this one rule,
  in this row.
- `spine-authoring`'s `references/in-lane.md` held CLARITY line follows the
  rule (proposal §8.4).
- WI-800, WI-807, WI-809 and WI-810 amend LLR-246 after this row and cite this
  rule.
- Its rows (SR-208, LLR-246, LLR-278 and their TCs) are authored as one change
  set and judged in one combined sitting.
- Tests:
  - a lane commit that approves a held SN is refused;
  - a CLARITY re-attestation bound to the exact text passes;
  - text changed after that verdict is refused;
  - a plain trunk commit approving a held row passes;
  - loop and coordinator lanes are judged alike.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. It names the two retired
  arms and says an adopter's trunk approvals are untouched.
