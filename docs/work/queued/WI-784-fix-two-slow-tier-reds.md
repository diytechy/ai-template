+++
id = "WI-784"
title = "Fix the two slow-tier reds the full suite found: the work README's open-items link, and the cadence columns' cell class"
workstream = "process"
specref = "project-trajectory/scripts/acceptance_record.py"
sr_refs = ["SR-215"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand by the wave-9 coordinator, 2026-10-03. The full unfiltered suite ran
for the first time in three waves, at trunk `d040ad75`, after the owner freed disk:
**2 failed, 4929 passed, 13 skipped** in 572 s. Both reds are in slow-tier modules,
which the per-commit smoke bar does not run, and each was introduced by a recent
landing:

1. `tests/test_check_docs.py::test_an_absent_open_items_registry_is_itself_the_s3_finding`.
   WI-746 (`9dbb5103`) wrote `owner gates follow [IF-073](../requirements/open-items.toml)`
   into `project-trajectory/work/README.template.md` (line 25), which is copied to
   every scaffold's `docs/work/README.md`. In a scaffold without the open-items
   registry, that link is broken, so `check_docs` exits 1. The absence should be the
   S-3 WARN alone, exit 0. The dogfooded copy `docs/work/README.md` carries the same
   line.
2. `tests/test_trajectory_staged.py::test_spine_cell_split_classifies_every_shipped_column`.
   WI-747 added the test-case columns `Trigger`, `Rubric` and `MinWorkItems`.
   Neither half of the §A5.1 split classifies them: `acceptance_record.SPINE_APPROVED_CELLS`
   and `SPINE_TRACED_CELLS`. Today they fall to the fail-safe residual, which reads
   them as approved. The test exists so that a new column is ruled explicitly
   rather than riding in on that residual.

## Done-when

- The template's line names the owner gate without a link a scaffold can break, for
  example a code span or a link to an always-present target. The dogfooded copy
  matches it byte for byte (`tests/test_dogfood_sync.py`).
- `Trigger`, `Rubric` and `MinWorkItems` are classified explicitly in the test-case
  entry of `SPINE_APPROVED_CELLS`, which keeps today's residual behaviour: each
  states how the row's claim is judged or kept current, as `MaxAge` and `Inputs` do.
  The comment above the table says so. Any reference table that mirrors the split
  (`docs/registry-machinery-reference.md`) lists them too.
- Both named tests pass, together with every module that touches the changed files.
  The smoke tier passes within its 60 s budget, and `check_trajectory --strict` and
  `check_docs` are clean.
- No spine row text changes. If the builder finds that a row's text must change to
  stay true, it stops and reports rather than amending.

## Deliverable
