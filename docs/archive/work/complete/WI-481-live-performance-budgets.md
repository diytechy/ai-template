+++
id = "WI-481"
title = "Seed the live performance-budget registry: the perf gate is green because it compares nothing (repo review 2026-08-19 M-16)"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Seeded `docs/requirements/performance-budgets.csv` with four real PB rows
covering the feedback-path commands the review named: PB-001 trace.py full
analysis (measured 0.97s, budget 5s), PB-002 the derive_gate+gen_trajectory
freshness pair (6.46s, budget 20s), PB-003 check_docs (1.94s, budget 8s),
PB-004 the whole pre-commit hook end to end (7.7s, budget 30s) — each
wall-clock figure measured on this box at 94489f7a on a second (warm) run,
carrying its `fig:` provenance marker and a single-machine disclaimer, at <!-- fig-ok: prose ABOUT the convention -->
Gate=warn per the stack.ini noisy-runtime-metric convention, budgets at
3–5x measured. Refs verified resolvable (budgets=4 budget-findings=0); the
stale declared-absences line removed with its three readers checked; the PB
watermark rose 0 → 4 via --bump-ids. `check_perf --tier all` moved from
the vacuous "no budgets to compare" OK to an honest "4 budget(s), SKIP (no
metrics wired)" — the automated measurement emitter stays unwired per the
spec's own scope and is the named residue. 177 targeted tests + smoke
green.

**CORRECTION (2026-08-20)** — this WI's own commit title reads "the perf
gate stops being vacuous", and that claim is too strong. What changed is
the MESSAGE, not the gate: the SKIP names what is missing, and the gate
still cannot fail while all four rows sit at `Gate=warn` and no metrics
emitter is wired — both deliberate, recorded postures, neither of them a
comparison. The step is also dormant at this repo's derived gate. So the
honest reading is that the perf layer stopped being SILENT: it now states
the two reasons it is not yet comparing anything, which is what makes them
discharge-able. Raised by the 2026-08-20 batch review (ROUND-OPUS
MAJOR-8), which drove `check_perf` and read the exit code rather than the
line.

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
convention (`fig:` marker with producing command + rev). PB rows are <!-- fig-ok -->
off-spine; no spine cell moves.
