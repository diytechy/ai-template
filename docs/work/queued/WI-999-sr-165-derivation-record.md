+++
id = "WI-999"
title = "SR-165's derivation record is built, or retired with LLR-172 and TC-166, as OI-129 rules"
workstream = "process"
sr_refs = ["SR-165"]
specref = "docs/requirements/open-items.toml"
needs = ["OI-129"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand in headless leg 33 (2026-11-04) as OI-127's placeholder. OI-127
was ruled (b), revised, on 2026-11-05, and this row became the routed work for
TC-166: no test and no code stand behind it, and LLR-172 states "NOT BUILT
YET". The record cells do not exist on the component schema. OI-129 states the
evidence and the choice. Owes its scope critique before its claim.

## Done-when

- [ ] OI-129 Q1 is ruled, and the ruling commit replaces this list with the
      work it routes: for (a), the record cells, the check and a record for
      each live component; for (b), the retirement of the three rows and what
      the ruling says of SN-040.
- [ ] TC-166's `evidence` names the test that verifies it, or the case retires.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
