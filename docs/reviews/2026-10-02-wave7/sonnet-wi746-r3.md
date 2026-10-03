# Sonnet review — WI-746, fix round 2 (build/wi-746 at d1681906)

Reviewer: Claude Sonnet 5.5 (read-only). Range `acc1e195..d1681906`. Context: SOUND at acc1e195, but composed onto trunk the smoke tier failed three tests the lane caused.

d1681906 SOUND

**BLOCKER:** none. **MAJOR:** none.

**MINOR**
- `schedule.py:133`: the module-scope `import spine_carrier` moves a sibling-absent failure from call time to import time. Acceptable: `spine_carrier.py` ships in the bootstrap MAPPING beside `schedule.py`, and optional consumers already guard the import (`traj_parse.py:77-84`, `check_trajectory.py:263`).
- `tests/test_dashboard_size_budget.py:89-98`: "measurement travels in the coordinator handoff" is not in the repo; the numbers are checkable (committed dashboard 3,013,555 bytes at 2a902b50, 3,026,786 at acc1e195: +13,231). The 11,231/2,000 split and "no duplicate embed" were not re-measured. (Coordinator: the measurement is recorded in the wave-7 log fragment.)

**Confirmations:** `gates` -> `owner_holds` a pure local rename, guard and allow-list untouched; `spine_carrier` imports only stdlib and `kitlib` (no cycle), `agent_brief` imports `schedule` in both branches of its fallback, `test_import_layers.py` passes in full; 3,480,000 is 14.97% over 3,026,786, the file's documented ~15% convention with a logged reason; only the three files changed (18+, 9-).

**Commands:** `pytest -q -n 2 tests/test_import_layers.py tests/test_stage_ladder.py tests/test_dashboard_size_budget.py tests/test_schedule.py tests/test_open_item_readiness.py`: `84 passed in 5.87s`; `git cat-file -s` of the dashboard at the three commits; a manual load of `schedule.py` without the scripts directory raises `ModuleNotFoundError: spine_carrier`, as expected.
