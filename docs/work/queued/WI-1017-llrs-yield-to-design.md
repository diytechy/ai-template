+++
id = "WI-1017"
title = "The guidance says an LLR yields to a sustainable design: it may be split, merged, moved or retired"
workstream = "docs"
sr_refs = ["SR-186"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand on 2026-11-21 at the operator's direction. The operator's
concern, stated as speculation: the tooling works to maintain LLRs rather
than toward a sustainable design, which will sometimes need redesign.

What the guidance says today:

- PROCESS.md §5's change intake has a branch for it ("parent sound; LLR
  unsuitable" → amend the LLR and its verification, keep the parent's
  acceptance), and the reviewer prompt asks whether a workaround preserves
  an unsuitable LLR.
- But the spine-authoring skill says "Keep IDs where meaning remains" and
  is silent on what happens when meaning does not remain; the chart's
  "code only" path adds LLR rows on the existing modules, with no branch
  for re-decomposing (splitting, merging, moving or retiring several LLRs
  when the design changes shape); and SR-186 asks each child for an
  independent purpose without mentioning re-decomposition.
- Only 4 LLRs have retirement records since the record began. Adding code
  under existing rows needs no act, while reshaping rows needs retirement
  records and re-acceptance, so the cheaper path keeps the rows.
- WI-1015's evidence (`docs/reviews/2026-11-21-code-vs-interfaces/`) shows
  LLRs trailing the code: 33 tags on functions their LLR does not name, and
  7 named symbols that no longer exist. The rows are being maintained after
  the fact rather than redesigned with the code.

## Done-when

- [ ] First, check whether the concern holds: sample recent lanes (decisions
      records, review verdicts, handbacks) for a design bent to fit an
      existing LLR, or an LLR kept when the design had changed. Record what
      was found in this row's Deliverable; the extent of the changes below
      follows from it.
- [ ] PROCESS.md §5 states once that an LLR records the current design, not
      a commitment. When a sustainable design needs a different
      decomposition, LLRs are split, merged, moved or retired (`retire.py`)
      under their tier's acceptance authority, keeping the parent SR's
      acceptance and the enduring regression tests. The change-intake chart
      gains that branch.
- [ ] The spine-authoring skill, the builder's instructions and the
      scope-critique and reviewer prompts point at that statement instead of
      restating it, and "keep IDs where meaning remains" says what to do when
      it does not.
- [ ] Nothing in the guidance rewards keeping an unsuitable LLR to avoid an
      acceptance act.
