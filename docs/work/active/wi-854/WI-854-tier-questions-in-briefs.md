+++
id = "WI-854"
title = "The adjudication briefs carry spine-authoring's tier questions, composed from one home"
workstream = "process"
sr_refs = ["SR-146"]
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §7.3,
row P7). `spine-authoring` calls itself "the adjudicator's question list per
tier", but no adjudication brief references it, and
`adjudicate-first-approval.template.md` carries its own short method instead.
The judging criteria have two homes, and the adjudicator sees the thinner one.

A brief cannot simply point at the skill. Skills are opt-in accelerators an
adopter may not install, and the brief feeds a gate, so it must stay
self-contained. The fix is one home that the brief composes at render time,
the way the combined brief composes the per-kind briefs.

It lands before WI-812, which edits the same two templates.

Scope settled before the claim (coordinator, 2026-10-09 leg 03, after a
Sol scope critique). The two deliverables, extracting the tier questions to
one shipped home with the skill reading it, and composing that home into the
briefs in place of their short method, land together in one lane: either
alone leaves two homes for the judging questions, which is the defect. The
home gains no authority over a hold, an act or a gate: it is instructional
text the brief renderer composes, the adjudicator's verdict stays the gate's
one authority, and an absent or unreadable home refuses the render (no
fallback, as the Done-when says), so no `## Trust` section is owed.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- The first-approval and amendment briefs, and each combined section composing
  them, carry the tier questions for the tiers of the rows they judge, composed
  at render time from one home in the shipped kit. The skill and the brief read
  that one home; neither holds a second copy. The brief composes in every
  adopting repo, skills installed or not, with no fallback path.
- The templates' own short method is replaced by the composed questions, not
  kept beside them.
- Tests:
  - a rendered brief carries the questions for its rows' tiers;
  - a change to the home changes the brief;
  - the duplicate-code census finds no second copy.
- Its rows (SR-146's chain: LLR-167 and its TC) are authored as one change set
  and judged in one combined sitting.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; the shipped adjudicate
  prompts change.
