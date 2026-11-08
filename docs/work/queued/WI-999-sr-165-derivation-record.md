+++
id = "WI-999"
title = "SR-165's derivation record is built: the record cells, the component check and a record for each live component"
workstream = "process"
sr_refs = ["SR-165"]
specref = "docs/requirements/low-level-requirements.toml#LLR-172"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand in headless leg 33 (2026-11-04) as OI-127's placeholder. OI-127
was ruled (b), revised, on 2026-11-05, and this row became the routed work for
TC-166: no test and no code stand behind it, and LLR-172 states "NOT BUILT
YET". The record cells do not exist on the component schema. OI-129 was
ruled (a) on 2026-11-08: an approved row is built unless evidence shows
substantial work, and none does. The derivation the records hold was worked in
the 2026-08-16 derivation plans under docs/plans/. Owes its scope critique
before its claim.

## Done-when

- [ ] The component registry's schema carries the derivation-record cells
      LLR-172 names: the candidate partitions, the objective, the
      constraints, a score per candidate, the selected partition, the human
      ruling, and an optional human override.
- [ ] The existing component pass reports each rule LLR-172 states: a missing
      element, naming the row and the element; a recorded ranking that does
      not recompute from the record's own inputs; and a selection the scores
      do not rank first with no recorded override. No second reader of the
      component registry is added.
- [ ] Every live component row carries its record, and the strict trace is
      clean over them.
- [ ] TC-166's `evidence` names the test that verifies it.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
