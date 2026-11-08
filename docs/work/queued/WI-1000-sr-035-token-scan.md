+++
id = "WI-1000"
title = "SR-035's token scan is built: a test scans the shipped registry templates and ID vocabulary for language-specific tokens"
workstream = "process"
sr_refs = ["SR-035"]
specref = "docs/requirements/low-level-requirements.toml#LLR-171"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand on 2026-11-05 (attended), routed by OI-127's ruling. TC-165 has
two halves. Its scaffold half is driven by a test in `tests/test_profile.py`;
its token scan of the shipped registry templates and ID vocabulary has no test.
OI-129 was ruled (a) on 2026-11-08: an approved row is built unless evidence
shows substantial work, and none does. Owes its scope critique before its
claim.

## Done-when

- [ ] A standing test scans the shipped registry templates and the ID
      vocabulary and finds no language-specific token, as LLR-171 states; the
      token list it scans for is declared in one place.
- [ ] The test fails when a planted language-specific token is added to a
      shipped template.
- [ ] TC-165's `evidence` names the tests that verify what remains of it.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
