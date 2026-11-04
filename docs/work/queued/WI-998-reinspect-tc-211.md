+++
id = "WI-998"
title = "TC-211 is re-inspected on the first decomposition round whose record carries the stopping-boundary line, its inputs amended to that sample before the observation is recorded"
workstream = "process"
sr_refs = ["SR-186", "SR-161"]
specref = "docs/reviews/wi-976/021-ADJUDICATE-095bb79.md"
needs = ["WI-983"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

The second deliverable WI-983's scope critique split out (S1): WI-983's lane
holds no decomposition round, and a round elsewhere composes from trunk, which
gets the stopping-boundary line only when WI-983 lands. So the re-inspection
cannot finish in WI-983's lane. TC-211's fail stands as the observation of
record until this row closes.

This row stays off the coordinator's queue table until a sample exists. Its
sample is the first round composed after WI-983's landing whose brief is
committed beside its verdict. No row now scheduled is known to draft such a
round, so the handoff lists the sample's scheduling for the owner.

**Architectural delta (S5).** None: an approved cell's input list moves through
the existing amendment route, and the observation writer is unchanged.

## Done-when

- [ ] TC-211's `inputs` name the sample's brief and verdict, through the
      existing amendment route: the cell is approved, and the observation
      writer never writes the registry.
- [ ] A fresh session that wrote none of the sample inspects it, by the recipes'
      Inspection TC route.
- [ ] The result is written into the procedure's result section.
- [ ] The observation writer records it last. It digests the declared inputs as
      they stand and the procedure file is one of them, so a record written
      earlier would anchor to the old sample or go stale at once. A fail is
      recorded as a fail.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
