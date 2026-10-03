# Sonnet review — WI-758, fix round 1 (build/wi-758 at c011016a)

Reviewer: Claude Sonnet 5.5 (read-only). Range `e2874075..c011016a` (one file, 71+/52-).

c011016a SOUND

**BLOCKER:** none. **MAJOR:** none. **MINOR:** none.

**Behaviour preserving:** a pure extraction into module-level helpers, no nested defs, no logic change: `_column_channels` replaces the per-side loop (distinct `(edge[0], side)` keys); `_occupied_lanes`, `_arrival_lane`, `_gap_route`, `_reserve_route`, `_detour_obstacles` keep the original expressions and argument order. `gen_trajectory.py --check` at the tip: "project-state dashboard up to date" (the committed dashboard untouched by the fix), so the render is byte-identical for this repo's data.

**Complexity (cognitive):** `_route_edges` 69 -> 38 (<= 48); `_wire_channels` 16 -> 0; helpers `_column_channels` 10, `_occupied_lanes` 3, `_arrival_lane` 2, `_gap_route` 3, `_reserve_route` 3, `_detour_obstacles` 5.

**Commands:** `pytest -q -n 2 tests/test_traj_lanes.py tests/test_traj_graph.py tests/test_traj_views.py tests/test_traj_panels.py`: `142 passed in 71.86s`; the other four `test_traj_*` modules: `59 passed in 35.78s`; `check_complexity.py --report | grep traj_graph`; `gen_trajectory.py --check`.
