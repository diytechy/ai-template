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
- Spine rows `SR-183` / `LLR-206` / `TC-202` (Drafted; approval is the owner's
  reviewed Status-change). No `IF-` row — the closest sibling
  (`check_dupes_census.py`) declares none, and declaring one arms the
  `Contract IF-###:` body gate for a seam better declared deliberately.
- `docs/id-watermark` bumped via `trace.py --bump-ids`; `docs/cli-reference.md`
  regenerated.

## Decisions & traps

- **Baseline seeded from the shipped script, on this repo.** The plan is emphatic
  that only the shipped script's own first run may be stamped; the prototype's
  figures are what the ruling is read against, not what lands in a cell.
- **No `[step:]` wiring, no `stack.ini` change.** Report-only means the gate
  machinery is not touched this phase — verified by grepping `docs/stack.ini` for
  `complexity` (nothing).
- **Tiering:** decided by measurement (recorded below).

## Verification

(pasted at close)
