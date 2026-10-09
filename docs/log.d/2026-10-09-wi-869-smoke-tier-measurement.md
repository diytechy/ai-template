## 2026-10-09 — WI-869: the smoke tier's wall-clock, measured, its cause named, and the re-tier

The declared-figure record WI-869's first Done-when asks for. Measured by the
kit-builder in the lane, at revision `295687c7` (trunk at the claim), on this
workstation: 12 cores / 24 threads, `-n auto` = 12 workers under the root
conftest's 50% CPU cap. Other agent sessions were live (CPU about 21% at the
start), so the runs are quiet, not idle.

**Before (unchanged tree, `295687c7`).** Command:
`python -m pytest -q -n auto -m smoke -p no:cacheprovider --durations=0 --basetemp <review-tmp>/w869-m<N>`.

| Run | Result | Wall |
|---|---|---|
| 1 | 2436 passed, 2 skipped | 71.26 s |
| 2 | 2436 passed, 2 skipped | 61.68 s |
| 3 | 2436 passed, 2 skipped | 62.50 s |

`python scripts/check_smoke_budget.py --mode enforce` read 69.7 s (exit 1).
Collected 2438. Summed per-test time (setup + call + teardown) 512.8 / 508.0 /
526.7 s, mean 515.8 s.

Per module, the mean of the three runs (the top eleven; the full table is in
the lane notes):

| Module | Tests | Mean s | % | First added |
|---|---|---|---|---|
| test_done_when_blessing | 82 | 142.4 | 27.6 | 2026-10-07 |
| test_text_then_act | 20 | 71.3 | 13.8 | 2026-10-05 |
| test_session_keep | 70 | 55.7 | 10.8 | 2026-09-28 |
| test_decision_overrule | 44 | 36.7 | 7.1 | 2026-10-05 |
| test_coordinator_adjudicate | 52 | 35.8 | 6.9 | 2026-10-06 |
| test_ruling_sync | 16 | 26.0 | 5.0 | 2026-10-04 |
| test_coordinator_guard | 77 | 16.8 | 3.3 | 2026-10-05 |
| test_adjudicator_token | 28 | 14.9 | 2.9 | 2026-10-08 |
| test_session_service | 39 | 13.3 | 2.6 | 2026-09-28 |
| test_dispute | 34 | 10.9 | 2.1 | 2026-10-08 |
| test_import_layers | 7 | 9.0 | 1.8 | 2026-08-20 |

Fixed costs and the environment:
- collection (`pytest --collect-only -q -m smoke`): 3.25 s and 3.20 s;
- xdist start-up with no test selected: 12.5 s cold, 6.2 s warm;
- process spawns, 30 per loop: `python -c pass` 35.7 ms (35.6 ms inside the
  capped job at BelowNormal priority), `git --version` 17.8 ms (18.7 ms inside),
  `git rev-parse HEAD` 21.7 ms, `git init` 45.7 ms;
- one run with the CPU cap off (`PYTEST_CPU_CAP=off`): 60.03 s.

**Cause: membership.** Ten of the eleven heaviest modules joined the tier
after the 2026-09-27 re-tier (then 1558 tests, 26.4 / 26.4 / 25.7 s); the tier
grew to 2438. The heaviest build real git repositories or lanes per case. The
environment's share is small: spawn costs are the same inside the job object as
outside, and the cap is worth about 2 to 10 s. The job-object change did not
push the tier over.

**Fix.** `test_done_when_blessing`, `test_text_then_act` and `test_dispute`
join `tests/conftest.py` `SLOW_MODULES`; every script family they exercise
keeps a smoke pin; nothing is deleted; TC-325 to TC-328's tier cells move to
Full (sitting 001, act 75). `test_decision_overrule` and `test_ruling_sync`
stay, because moving them would leave `migrate_decisions` with no smoke pin
and make TC-313, TC-319 and TC-320 untrue. The 60 s budget is unchanged;
`max-tests` is re-stamped 2438 -> 2395 (2302 collected, about 4% headroom).

**After (the lane's change on `295687c7`).** Summed per-test time 271.6 s.
`check_smoke_budget.py --mode enforce` read 33.4 / 33.2 / 39.4 s (builder,
three runs) and 35.8 s (coordinator, the full commit bar: 2300 passed, 2
skipped in 32.8 s at `04858f3e`).

**Found, not fixed here:** `session_keep.primary_out_dir` spawns
`git rev-parse --git-common-dir` on every store access (about 1,260 spawns in
`test_session_keep` alone), which makes the remaining heavy in-process modules
heavy. It is filed as its own row (`docs/decisions/wi-869.toml` D-003).
