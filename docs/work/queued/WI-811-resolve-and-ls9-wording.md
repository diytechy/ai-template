+++
id = "WI-811"
title = "RESOLVE for disputed findings, and LS9's builder and reviewer wording"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-resolve-ls9"
sr_refs = ["SR-154"]
needs = ["WI-809", "OI-111", "WI-860", "WI-865", "WI-853"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-resolve-ls9 (ch.4 §4.1, §9, §11; LS5, LS9;
OI-103 Q3). In rework a builder fixes or disputes each finding with evidence and a
class; the adjudicator rules each dispute `uphold`, `dismiss` or `advice` in the
sitting record, and its call is final: `_verdict_gate` treats a CHANGES-REQUESTED as
cleared when every finding is dismissed or marked advice (README change 12,
RULING-7). Any `uphold` returns the lane; `advice` goes to MINT. LS9's refined
wording lands in the rework brief, the reviewer brief (`[ADVICE]`, which
`kitlib/verdict.py` learns) and `AGENTS.template.md`'s retry rule (change 24). This
row carries SR-154's third amendment: the resolution is final, and the final
review is never a session that authored any range, and a family other than every
author's is preferred (README A1 step 3); the kit's alternative-agent rule
(OI-108) is the recorded case where the preference yields (OI-111 ruled
2026-10-07 (a)).

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

Ordering (coordinator, 2026-10-04, from the pre-execution consolidation check; the WI-805 edge was DROPPED by the owner on 2026-10-08, see Done-when): it
needed WI-805 too, because the note's matrix amends SR-154 three times "in `needs`
order" (WI-801, then WI-805, then this row) and the filed graph did not enforce
the second step.

## Done-when

- A fully dismissed CHANGES-REQUESTED lands with no re-review.
- An `uphold` returns the lane.
- `[ADVICE]` is not counted in `findings=N`.
- A finding the builder disputed and the adjudicator resolved counts as
  covered for WI-853's findings gate, citing the resolution.
- The rework brief, `prompts/reviewer.template.md` and `AGENTS.template.md:172-176`
  carry ch.4 §9's wording.
- Each spine row the README matrix gives this row (SR-154's final-resolution
  amendment, third in `needs` order; a new dispute-resolution row) is amended or
  added and passes in-lane adjudication.
- SR-154's third amendment states that the final review is never a session that
  authored any range, and a family other than every author's is preferred
  (README A1 step 3); the kit's alternative-agent rule (OI-108) is the recorded
  case where the preference yields (OI-111 ruled 2026-10-07 (a)).
- The row's test bar: its affected modules' tests (verdict, brief) plus the smoke
  tier at `-n 2`, plus the byte budget (`AGENTS.template.md`).
- The loop's dispute sitting reuses the brief class and verdict grammar WI-865 builds for the
  coordinator's entry point (owner, 2026-10-08: the coordinator path split out of this row so it
  does not wait behind WI-809); no second copy of the class.
- Of WI-811 and WI-805, whichever lands second states in its rows that, in the loop, the third-round
  dispute sitting comes before WI-805's tier-up build, and the tier-up build answers only upheld
  findings (the LLR-081 amendment the two rows share; WI-864's sitting, MINOR). The owner dropped this
  row's `needs` on WI-805 on 2026-10-08: it ordered SR-154's text amendments only, not behaviour.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit; the shipped briefs and
  `AGENTS.template.md` wording change.
