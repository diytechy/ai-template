+++
id = "WI-745"
title = "Plant the re-seed test's Drafted LLR row itself: the phase-close full suite is red because no live LLR is Drafted any more"
workstream = "process"
specref = ""
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

The re-seed test no longer depends on the live spine's approval progress, so the
phase-close full suite's one red is gone.

- `tests/test_baseline_snapshot.py`: the re-seed test plants its own Drafted LLR
  before seeding (the `_seeded_with_a_drafted_sr` pattern), then flips it back as
  the real flip; the assertion's meaning is unchanged.
- `tests/baseline_snapshot_fixtures.py`: `_tree` sets every SR, LLR and TC status
  to Approved in its temp copy, so every caller plants the maturity it needs and a
  fully approved or fully drafted live spine cannot break the suite.
- Proof: `test_baseline_snapshot` at the old HEAD 1 failed, 123 passed; with the
  change 124 passed. Reviewer: 128 passed over both baseline modules.
- **Review:** Sonnet 5.5, SOUND at b4d9d00b
  (`docs/reviews/2026-10-02-wave7/sonnet-wi745.md`); two cosmetic minors accepted.

## Context

Wave 6's phase-close full unfiltered suite, on trunk a4919610, gave
`1 failed, 4839 passed, 15 skipped in 2683.18s (0:44:43)`. The one
failure:

    tests/test_baseline_snapshot.py::test_a_RESEED_over_a_standing_record_is_judged_over_the_WHOLE_tree
    AssertionError: fixture substring not found: status = "Drafted"
    (at _rewrite(root, LLR_REL, 'status = "Drafted"', 'status = "Approved"'), tests/test_baseline_snapshot.py:588)

The fixture `_seeded` copies this repository's live registries, and the test
flips the first `status = "Drafted"` LLR it finds. Spine-acts batch I
(7a6536f9) approved the last Drafted LLRs (LLR-266 to LLR-270), so the
substring no longer exists. The test was coupled to the live spine's state,
and it went red when the spine was fully approved. The module is
slow-tier, so no lane's module run reached it. This is not a product
defect.

## Done-when

- The test plants its own Drafted LLR before it seeds, following the
  existing pattern `_seeded_with_a_drafted_sr` in the same file, which
  flips an approved SR to Drafted before `copy_live(seed=True)`. It then
  flips it back as "a real flip", as it does now. The assertion's meaning
  is unchanged.
- Sweep the module, and `tests/baseline_snapshot_fixtures.py`'s other
  callers, for any other `_rewrite` that assumes a live row in a given
  status. Plant those too, so a fully approved or fully drafted spine
  cannot break the suite.
- `python -m pytest -q -n 2 tests/test_baseline_snapshot.py
  -p no:cacheprovider` passes, with
  `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`.
