+++
id = "WI-481"
title = "Seed the live performance-budget registry: the perf gate is green because it compares nothing (repo review 2026-08-19 M-16)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

`check_perf.py --tier all` reports `OK - no performance budgets to compare`:
no live `docs/requirements/performance-budgets.csv` exists (only the shipped
PB-000 template), so the performance step's green is vacuous — the framework
shipped, the measurements never did. The one honest exception is the smoke
wall-clock budget (`docs/stack.ini` `[smoke-budget]`), which is exactly the
pattern to extend. Meanwhile the full suite runs ~10 minutes locally and the
hook/agent feedback path runs `trace`, `derive_gate` + dashboard regeneration,
and `check_docs` on every commit — regressions there degrade every session
and nothing would notice.

Scope: seed a SMALL live budget set for the commands that dominate feedback
latency (candidates: `trace.py` full analysis, `derive_gate.py` +
`gen_trajectory.py` regeneration, `check_docs.py`, the pre-commit hook path),
measured on representative fixture sizes. Prefer machine-independent size/
operation metrics where possible; reserve wall-clock for CI with generous
thresholds (the review's wording — one machine is one data point, per the
standing status.md rule). Every recorded number follows the declared-figure
convention (`fig:` marker with producing command + rev). PB rows are
off-spine; no spine cell moves.
