+++
id = "WI-1073"
title = "The component view's header and its generator's docstring state placement as the placement row does"
workstream = "process"
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
sr_refs = ["SR-070", "SR-249"]
needs = ["WI-1071"]
buildtier = "light"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, from
WI-1071's plan (its decision D13, left out of its scope).

LLR-403 (accepted) places a design row through its `constrains` cell and
through the test cases verifying it (WI-1024's slice 1). The generated
component view's header, written by the component view generator, still
says "A design row sits at the owner component of each interface a test
case verifying it names", and the generator's module docstring says the
same: the placement before `constrains` existed. The view itself places
rows as LLR-403 states; only the explanatory text is stale. WI-1071
restates LLR-199's header clause by the header's four elements (generated,
not to be hand-edited, cite the registries, the regeneration command), so
no spine row carries the stale sentence.

Critiqued 2026-11-24 (Sol and Hydrogen;
`docs/reviews/2026-11-24-scope-critiques/WI-1073.md`): `planmode` is `none`.

## Done-when

- [ ] The header's placement sentence and the generator's docstring state
      the placement LLR-403 states (through `constrains`, and through the
      verifying test cases), without restating its precedence rules beyond
      what a reader of the view needs; the committed view is regenerated.
- [ ] No spine row's text changes; a test pins the header's placement
      sentence if one already pins the header.
- [ ] A RESYNC entry for the shipped generator.
