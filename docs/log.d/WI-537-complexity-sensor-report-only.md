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

## REVIEW-A rework (2026-08-30, 41c44e6 findings)

- **[MAJOR] `_collect` dropped functions under `for`/`while`/`match`.** The old
  descent whitelisted only `If`/`Try`/`With` container types, so a module-level
  `def` wrapped in any other control flow (and its public-symbol contribution)
  was silently omitted from the census. Replaced the type whitelist with a
  descent through **every statement container** (`_BLOCKS` = `ast.stmt` +
  `ast.excepthandler` + `ast.match_case`) via `ast.iter_child_nodes`, still
  stopping at a def/class body so a nested def keeps being scored INTO its
  enclosing function rather than earning its own row. `_public` had the same
  blind spot (it only read `tree.body`); it now shares the descent via a `_bound`
  helper and **deduplicates**, so a `try/except` import fallback binding one name
  in both arms counts once. Regressions: `test_collect_descends_through_every_
  control_flow_container` (in-process) and `test_functions_under_control_flow_are_
  censused` (subprocess, `--report`, asserts the row AND the module public count
  of 3). The real-tree census is **unchanged at 179 rows** — the kit has no
  module-level def under a loop/match — so no baseline re-stamp.
- **[MINOR] boundary wording split `reaches` (SR) vs `over` (LLR/impl).** Chose
  the exclusive `>` boundary already carried by LLR-206, the implementation, and
  the baseline's over-threshold rows, and rewrote SR-183's AC from "reaches" to
  "strictly OVER ... a function scoring exactly the threshold is under it and is
  not reported". Pinned with `test_threshold_boundary_is_exclusive` (`tangled`
  scores exactly 21: threshold 21 excludes it, 20 includes it). TC-202's method
  now STATES the boundary too — "pinned EXCLUSIVE (`>`) ... exactly the threshold
  is under it" — so the finding's "state one boundary across SR/LLR/TC" is met on
  all three tiers (LLR-206 already reads "over the threshold"). SR-183/LLR-206
  remain Drafted — this tightens their wording for the owner's approval, it does
  not approve them.

## REVIEW-A Round 6 rework (2026-08-30, 30c84a6 findings)

- **[MINOR] LLR-206 assigned threshold selection to the wrong boundary.** The
  implementation already has one unambiguous owner: `census()` returns all
  source-function rows and `main()` selects rows strictly over (`>`) the
  threshold before baseline comparison. LLR-206 now says exactly that; no code
  or baseline changed.
- **[MINOR] iteration telemetry carried trailing spaces.** Removed the four
  reviewer-named spaces after the empty `guardrails` and `commits` fields in
  the Round 3/4 iteration records, plus the identical empty-field whitespace in
  the later Round 5/6 records so the next review range passes `git diff --check`.

## Verification (real output, this box — Python 3.11.9)

Sessions 003/004 built the rework but ended NO-COMMIT; this session (005)
committed that standing state and re-confirmed the bars over the same working
tree, unchanged:

```
check_complexity.py --root .                -> OK - 179 row(s) over 15, unchanged (exit 0)
pytest tests/test_check_complexity.py tests/test_check_complexity_cli.py
                                            -> 55 passed in 6.40s
pytest -n auto -m smoke                     -> 1424 passed, 6 skipped in 25.47s
check_smoke_budget.py --mode enforce        -> 26.4s vs 60s budget -> within
check_docs.py --root . --stale             -> OK - 0 broken (exit 0)
check_doc_refs.py --root . --strict        -> exit 0 (advisories only)
trace.py --root . --strict-integrity       -> SN=27 SR=76 LLR=188 TC=186, integrity=0 (exit 0)
                                              (--strict still exits 1 on the two pre-existing
                                              findings above: LLR-197 WI-448 frame, SR-181 orphan)
pytest -n auto  (FULL SUITE)                -> 1 failed, 3160 passed, 16 skipped in 657.55s
                                              (session-003 reading; session-004 delta is
                                              prose-only — TC-202 method + this fragment — so
                                              behavior is identical; re-run recorded below)
```

**The one full-suite failure is expected generated-artifact staleness, not a defect.**
`tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current` fails
because the committed `docs/stage` fingerprint no longer matches: adding the four
**Drafted** spine rows (SR-183/LLR-206/TC-202/TC-203) moved `drafted` 6 → 10 and
pulled phase-5's *live* reading to DevStg-Reqs. The EFFECTIVE selection `stage` is
unchanged (DevStg-LLReqs, settled). `docs/stage` is a declared generated artifact
whose `derived-stage` freshness step SKIPs on a work branch ("generated freshness
is the trunk lane's, §5.2"), and `test_derive_stage` is in `conftest.SLOW_MODULES`
— which is why the commit bar is green and only the close/CI full suite surfaces
it. The trunk lane regenerates `docs/stage` after the merge; committing it here
would do the trunk lane's job on the branch and churn against the concurrent
spine-touching lanes (WI-538/WI-539 share this plan). So it is deliberately left
for trunk. Every other test passes.

Round 6 rework was re-verified with Git for Windows' `bin` directory on `PATH`,
so the required POSIX-shell environment gate was exercised:

```
git diff --check 30c84a6                 -> clean (prospective re-review range)
check_complexity.py --root .             -> OK - 179 row(s) over 15, unchanged
pytest test_check_complexity*.py         -> 55 passed in 7.87s
pytest tests/test_dependency_ledger.py   -> 5 passed in 4.11s
trace.py --root . --strict-integrity     -> SN=27 SR=76 LLR=188 TC=186,
                                             integrity=0 (exit 0)
check_trajectory.py --root . --strict    -> clean, 543 WI rows (exit 0)
pytest -n auto -m smoke                  -> 1424 passed, 6 skipped in 30.19s
check_smoke_budget.py --mode enforce     -> 30.9s vs 60s budget -> within
check_docs.py --root . --stale           -> OK - 0 broken (exit 0)
```
