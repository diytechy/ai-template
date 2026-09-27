+++
id = "WI-672"
title = "The suite's own honesty: tie a test case's tier to smoke membership, drive the trunk regen table whole, print a module's spine-linked tests, and clear ruff's noqa warning"
workstream = "quality"
specref = "tests/conftest.py"
buildtier = "medium"
safety_class = "spine"
priority = 6
needs = []
supersedes = "WI-663;WI-598;WI-619"
+++

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-663 (Fix the invalid noqa directive ruff reports in the stage-ladder test), WI-598 (drive the trunk regen step table WHOLE instead of sampling five names — the printed skip and the declared order), WI-619 (Point builders at the tests the spine links to their module, as an inner loop beside the smoke bar (S5)). Each is a place where what the suite or its test cases say disagrees with what runs. WI-672 and WI-619 read the same join (a test case's `evidence` node ids to modules and tiers), so one builder writes it once; WI-598 and WI-663 are small fixes in the same test files' territory. WI-672's check would have caught the stale live-frame pin WI-678 fixed. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

Build the evidence-to-module join once and use it for both WI-672's tier check and WI-619's per-module test listing. A tier amendment of an approved test case is left `Approved` and unanchored for the spine-acts batch; this lane files no adjudication.

Found by WI-652's re-tier and its codex review (arbitration ruling 4(ii) of
`docs/reviews/2026-09-26-wave3/ARBITRATION.md`). An approved test case's
`tier` cell says whether its evidence runs in the per-commit smoke tier
(Smoke) or only at close (Full); D31 of the spine map puts each Smoke case in
a fast in-memory module and each Full one in a module registered in
`tests/conftest.py` `SLOW_MODULES`. Nothing checks it. WI-652 settled the
cases its own re-tier moved (six amended to Full, two kept Smoke with fast
evidence), but thirteen evidence modules for Smoke-tier cases were already
slow before it, among them `test_bootstrap`, `test_trace`,
`test_trajectory`, `test_trajectory_staged`, `test_handback` and
`test_baseline_snapshot`.

IN SCOPE: (1) a check that reads each approved test case's `tier` and
`evidence` node ids and reports a Smoke case none of whose evidence runs in
the smoke tier (`conftest.smoke_tier_for`), and a Full case none of whose
evidence is slow (advisory, since the Full tier runs everything); decide
whether it lives in `check_trajectory` or `trace` and whether it gates.
(2) Settle the older mismatches the check reports: per case, split its
in-memory clauses into a fast module and move the traced `evidence` pointer,
or amend `tier` to Full in place (left Approved) and file the adjudication.

## Done-when

- The check exists, is tested (a Smoke case with slow-only evidence is
  reported; one with fast evidence is not), and runs in the declared bar.
- Every approved test case it reports is settled by a pointer move or an
  adjudicated tier amendment; the commit bar passes.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-663 (Done-when, verbatim)

- `ruff check tests/test_stage_ladder.py` prints no warning, and the commit
  bar passes.

### From WI-598 (Done-when, verbatim)

- `test_regen_skips_absent_artifact_families` asserts, for every `REGEN_STEPS`
  row, its `ok` line or its named skip on a bare scaffold, reading the table
  rather than a literal list of names; the `verdict-rollup` skip notice is among
  them.
- `test_regen_runs_in_declared_dependency_order` asserts that the executed
  order is the declared order across every row, not a sampled subsequence.
- A row added to `REGEN_STEPS` is covered by both arms with no edit to the test.
- `trunk_step.py` is unchanged, both arms still run on an empty temporary tree,
  and the commit bar passes with no spine row's `Status` changed.

### From WI-619 (Done-when, verbatim)

- A command prints, for a module, the test files the spine links to it,
  derived from the registries, with no hand-kept map.
- The builder brief says to run those while iterating, and the smoke bar
  before every commit.
- A test pins the map for a module whose tests do not follow the
  `test_<module>` naming.
