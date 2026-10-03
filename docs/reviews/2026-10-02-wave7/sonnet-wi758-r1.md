# Sonnet review — WI-758 (build/wi-758 at e2874075)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range `a8dee5b7..e2874075`.

e2874075 NOT YET SOUND

**BLOCKER**
- The complexity ratchet fails on this lane's code: `traj_graph.py::_route_edges` cognitive 40 -> 69 (cyclomatic 43 -> 86); `_wire_channels` new and unbaselined (16/21); `_detour_d` fell 32 -> 23 (re-stamp downward in the same commit). The commit touches no baseline. Trunk enforces the ratchet at commit. `_route_edges` nearly doubling is not proportionate: the new direct-gap lane block and the `lane_pref`/`occupied` logic belong in helpers.

**MAJOR:** none

**MINOR**
- `tests/test_traj_lanes.py` `_violations` exempts shared terminals by coordinates (first/last points equal), not by node id; the effect is as intended (a join away from the shared terminal is flagged).
- The test checks every wire pair, stricter than "edges sharing no endpoint": fine.
- The `ctxrel`/`data-edge` tag plumbing in `_Tags` (lines 14-30) is complex for what it does; no defect found.

**Held:** the oracle is not vacuous (with the base `traj_graph.py` swapped into a TEMP copy the new test gave `2 failed, 4 passed`, [dag] and [sw]); it pins the x=452 overlap, the x=220 join, a perpendicular crossing, a 0.1-unit separated pair, a shared terminal and a corner join (1e-7 collinearity tolerance); the sweep covers dag, sw, context, process, every SVG subtree and `ctxrel`; the rubric binds lane separation to LLR-292/TC-305 and box clearance to LLR-120/TC-125, no other anchor changed; LLR-120 already says lane separation is "DELIBERATELY NOT" claimed; the When cyclic routes pass.

**Commands:** `pytest -q -n 2 tests/test_traj_lanes.py tests/test_traj_graph.py tests/test_traj_views.py tests/test_traj_panels.py`: `142 passed in 73.84s`; `check_complexity.py --report | grep traj_graph`: `_route_edges 69/86`, `_wire_channels 16/21`, `_detour_d 23/44`; base-router TEMP run: `2 failed, 4 passed`.
