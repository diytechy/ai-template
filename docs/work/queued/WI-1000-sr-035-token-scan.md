+++
id = "WI-1000"
title = "SR-035's token scan is built, or the clause retires from SR-035, LLR-171 and TC-165, as OI-129 rules"
workstream = "process"
sr_refs = ["SR-035"]
specref = "docs/requirements/open-items.toml"
needs = ["OI-129"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-11-05 (attended), routed by OI-127's ruling. TC-165 has
two halves. Its scaffold half is driven by a test in `tests/test_profile.py`;
its token scan of the shipped registry templates and ID vocabulary has no test.
OI-129 states the evidence and the choice. Owes its scope critique before its
claim.

## Done-when

- [ ] OI-129 Q2 is ruled, and the ruling commit replaces this list with the
      work it routes: for (a), the scan and its test; for (b), the amendment
      dropping the clause.
- [ ] TC-165's `evidence` names the tests that verify what remains of it.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
