# WI-537 — check_complexity.py: a stdlib cognitive-complexity + SLOC census, report-only (OI-68 phase 1)

**Branch:** `wi-537-complexity-sensor-report-only` · integration base `127fdd3e`.
**SpecRef:** `docs/plans/2026-08-29-complexity-sensor-plan.md#phase-1--the-sensor-report-only`.

## What shipped

Phase 1 of the OI-68 complexity-sensor program: the sensor itself, **report-only**
— it lands, it is tested, its census seeds a central baseline, but nothing in this
repo wires it as a gate. Arming (`[step:complexity]`) and retiring the line
ratchet are phase 2; shipping it downstream is phase 3.

- **new** `project-trajectory/scripts/check_complexity.py` — stdlib-`ast`
  SonarSource cognitive-complexity + SLOC census per function, plus a
  reported-never-gated per-module public-symbol count. Modes `--report`,
  `--restamp`, `--mode warn` (default), `--mode enforce`. Central TSV baseline at
  `docs/complexity-baseline`, exact equality both directions, no inline
  suppression pragma. Adapted from the validated research prototype under
  `C:\Projects\ai-template-plans\complexity-pushback\prototype\` (oracle-checked
  against the Sonar white paper's worked examples and cross-validated at 89.5%
  agreement with `cognitive_complexity` 1.3.0, with the two divergences it found
  fixed and tested).
- **new** `tests/test_check_complexity.py` — the two correctness traps (elif
  flattening, operator runs), the nested-def/decorator battery, the Sonar oracle
  battery, and subprocess CLI drives of every mode.
- **new** `docs/complexity-baseline` — seeded from THIS script's own first run on
  this repo at the WI's base, not from the prototype's numbers (the prototype's
  walker was unvalidated where it disagreed; only the shipped script's reading is
  stamped).
- Spine rows `SR-183` / `LLR-206` / `TC-202` (Smoke, the in-process metric) /
  `TC-203` (Full, the CLI drives) — all Drafted; approval is the owner's reviewed
  Status-change. No `IF-` row — the closest sibling (`check_dupes_census.py`)
  declares none, and declaring one arms the `Contract IF-###:` body gate for a
  seam better declared deliberately.
- `docs/id-watermark` bumped via `trace.py --bump-ids` (SR 182→183, LLR 205→206,
  TC 201→203). `docs/cli-reference.md` is a declared generated artifact whose
  freshness step SKIPs on a work branch — the trunk lane regenerates it after the
  merge (§5.2), so it is deliberately NOT committed here; a local regen confirmed
  the new `scripts/check_complexity` entry renders.

## Decisions & traps

- **Baseline seeded from the shipped script, on this repo.** The plan is emphatic
  that only the shipped script's own first run may be stamped; the prototype's
  figures are what the ruling is read against, not what lands in a cell. The
  shipped script's first run over `project-trajectory/scripts/**/*.py` reads
  **179 rows over cognitive 15** — matching the prototype's headline for that
  tree, re-derived here by the shipped code.
- **No `[step:]` wiring, no `stack.ini` step change.** Report-only means the gate
  machinery is not armed this phase — grepping `docs/stack.ini` for a
  `[step:complexity]` returns nothing. The only `stack.ini` edit is the
  `[smoke-budget]` `max-tests` re-stamp below.
- **Tiering, decided by measurement.** The one test module measured 5.38 s (well
  over the plan's ~1 s split threshold), dominated by subprocess CLI drives. So
  it was SPLIT per the plan's guidance: `tests/test_check_complexity.py` — the
  in-process metric (traps, oracle battery, SLOC, baseline round-trip), 44 cases
  at 0.22 s, stays in the commit-bar smoke tier; `tests/test_check_complexity_cli.py`
  — the 8 subprocess CLI drives at ~2.6 s — re-tiered into `conftest.SLOW_MODULES`
  beside the other subprocess suites, so it runs at slice/phase close + CI.
- **`[smoke-budget]` `max-tests` re-stamped 1390 → 1440** for the 44 in-process
  metric tests (the WI-122 legitimate growth); measured 1428 collected, +12
  headroom, the house convention. The `seconds = 60` budget is untouched — the
  addition is 0.22 s.
- **Two pre-existing `trace --strict` findings are not mine.** LLR-197's WI-448
  provenance frame and SR-181's orphan predate this branch; my four rows add zero
  findings (orphans and provenance-findings counts unchanged before/after), and
  the gate bar uses `--strict-integrity` (integrity=0, passes).

## Verification (real output, this box — Python 3.11.9)

```
check_complexity.py --root . --restamp      -> re-stamped 179 row(s)
check_complexity.py --root .                -> OK - 179 row(s) over 15, unchanged (exit 0)
pytest tests/test_check_complexity.py       -> 44 passed in 0.22s
pytest tests/test_check_complexity_cli.py   -> 8 passed in 2.62s
pytest -n auto -m smoke                     -> 1422 passed, 6 skipped in 23.91s
check_smoke_budget.py --mode enforce        -> 21.9s vs 60s budget -> within
check_docs.py --root . --stale             -> OK - 0 broken (exit 0)
trace.py --root . --strict                 -> SN=27 SR=76 LLR=188 TC=186, integrity=0
                                              (exit 1 on the two pre-existing findings above)
check_trajectory.py --root . --strict      -> clean (exit 0)
pytest tests/test_dependency_ledger.py      -> 5 passed (stdlib claim proven)
pytest tests/test_smoke_budget.py tests/test_smoke_tier.py
       tests/test_generated_freshness_wiring.py tests/test_dogfood_sync.py
                                            -> 53 passed, 1 skipped
pytest -n auto  (FULL SUITE)                -> (pasted below at close)
```
