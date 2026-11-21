+++
id = "WI-1039"
title = "The smoke tier is brought back under its CPU budget by moving its heaviest cases to the full tier"
workstream = "process"
sr_refs = []
needs = []
specref = "docs/archive/work/complete/WI-940-cpu-time-smoke-budget.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Context

Filed on trunk on 2026-11-21 at the operator's direction (queue-drill
HANDOFF §3.4), from WI-1019's commit checks. The operator asked why
iteration is slow; the per-commit smoke tier is where a builder waits.

CLAUDE.md: the smoke tier's CPU seconds and wall time are only reported at
the commit; `run.cmd audit` judges them against `docs/stack.ini`
`[smoke-budget]`, and "a breach is filed as a re-tier row, never charged to
the lane that ran it". This is that row.

**The readings.** WI-940 stamped the budget on 2026-10-21 on this
24-logical-CPU workstation (`-n auto`, 12 workers): quiet, about 335 CPU
seconds and 55 seconds wall; loaded by two concurrent tier runs, about 425
CPU seconds and 105 seconds wall; `cpu-seconds = 540` is the highest loaded
reading plus 25%. WI-1019's `run_menu.py smoke` on 2026-11-21 read 1,014.6
CPU seconds and 351 seconds wall for 3,698 passed and 3 skipped, against
`max-tests = 3720`. The test count rose about 9% since the stamp; the CPU
rose about threefold. Part of that reading may be load (the coordinator ran
reviewer sessions beside it), so this row measures before it moves anything.

**The rule it keeps.** Heavy cases live in `tests/conftest.py`
`SLOW_MODULES`, and every script family keeps an in-process pin in the smoke
tier (CLAUDE.md, "Self-test before claiming done"). A module moves to the full
tier only with a named in-process pin for its script family, recorded beside
its `SLOW_MODULES` entry as the existing entries do.

**Scope answers.** S1: one deliverable, the tier back under budget; the
measurement and the moves land together, since a move without its reading
cannot be judged. S2: no file gains authority; the budget step stays
warn-only at the commit. S3: the candidate set is closed: the smoke tier's
modules ranked by their measured CPU, taken heaviest first; a module with no
in-process pin for its family is not moved, and the gap is named in the
Deliverable. S4: `planmode = "single"`: the moves are an empirical selection
over the measured modules and their pins, so the plan records the readings
and the chosen set before any move. S5:
no change to any script or its behaviour; only test-tier membership. S6:
nothing waits.

## Done-when

- [ ] The budget step's own reading (`check_smoke_budget.py --mode warn`)
      is taken three times on a quiet box (no other test run, no reviewer
      sessions launched), and quoted in the Deliverable.
- [ ] Per-module CPU is measured, not inferred from elapsed time: one
      `pytest -m smoke --durations=0` run shortlists the 30 modules with
      the largest summed durations, and each shortlisted module is then run
      alone (`pytest -m smoke -p no:xdist <module>`) under the budget step's
      own process-tree meter (on Windows the job object of `kitlib.winjob`,
      descendants and exited processes included; elsewhere
      `getrusage(RUSAGE_CHILDREN)`). The ranking is by that CPU reading,
      quoted per module in the plan.
- [ ] If the quiet readings are under `cpu-seconds`, the Deliverable says
      the breach was load, and nothing moves. Otherwise the heaviest
      modules move to `SLOW_MODULES`, each with its family's in-process pin
      named, until three quiet readings sit under 80% of `cpu-seconds`.
- [ ] `max-tests` and `[smoke-budget]`'s comments are re-stamped from the
      new collection and readings, in the file's existing record shape; the
      budget value itself is not raised.
- [ ] The full unfiltered suite still collects every moved case, and
      `test_dogfood_sync`, `test_import_layers` and the budget step's own
      tests pass.
