+++
id = "WI-869"
title = "The smoke tier is back under its wall-clock and membership budgets on this workstation"
workstream = "process"
specref = "docs/stack.ini"
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Context

Filed by the coordinator on 2026-10-08 at the owner's direction ("after WI-852 lands we should tackle the smoke tier to get it back under budget"). The per-commit bar (CLAUDE.md: `python -m pytest -q -n auto -m smoke && python scripts/check_smoke_budget.py --mode enforce`, 60 s wall) has failed its wall-clock budget on every landing of the last two coordinator sessions, though every test passed: 88.7 s and 91.7 s in the second 2026-10-08 session, then 60.8 s, 65.2 s and 69.0 s in the third. The membership cap (`docs/stack.ini [smoke-budget] max-tests`) was re-stamped to the exact collected count, 2438, by WI-852 at the owner's choice, so it has no headroom left: the next in-process test anywhere trips it. The previous session traced the wall-clock rise to the workstation's job-object change, which WI-859 records for the conftest isolation test. CLAUDE.md is explicit that the budget is not moved to fit one box.

## Done-when

- The wall-clock cost is measured, not assumed: three quiet `-n auto` runs on this workstation, with the per-module durations (`--durations`), stated in the log with the commands and revisions (the declared-figure convention).
- The cause is named from that evidence (heavy modules that crept into the tier, per-test fixture cost, or the environment), and the fix follows the cause: re-tier heavy modules into `tests/conftest.py` `SLOW_MODULES` while every script family keeps an in-process pin (CLAUDE.md), or make the costly fixtures cheaper. An environment-caused share is surfaced to the owner, not tooled around.
- Three quiet runs then pass `check_smoke_budget.py --mode enforce` at 60 s, and `max-tests` is re-stamped with headroom (earlier stamps kept about 4%), each with its reason and declared figure in `docs/stack.ini`.
- No test is deleted to fit the budget; a move to the slow tier keeps its TC's tier cell true (amend the cell where it changes, through the in-lane sitting).
- Review bar: A (one cross-family REVIEW-A).
