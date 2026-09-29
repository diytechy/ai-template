<!-- Claude Sonnet (read-only) review of WI-727, build/wi-727 f1733daa..c88f16fa. Built by Codex Sol; committed by the coordinator. -->

c88f16fa NOT YET SOUND

BLOCKER:
- **The bounds pre-check is unsound in floating point.** The check is `project-trajectory/scripts/rendering/traj_graph.py:248`, `if rx > x_hi or rx + rw < x_lo or ry > y_hi or ry + rh < y_lo: continue`. *Coordinator: in scope for fix round 1.*
  - Algebraically, it is the correct negation of AABB overlap, and a rectangle disjoint from the whole polyline's box is disjoint from every segment.
  - But `rx + rw` is computed fresh and compared strictly. When a rectangle's edge touches the path's box edge, the sum can land one ULP past it. `_seg_hits_rect` counts a touch as a HIT.
  - **Reproduced** against the production module: `pts=[(10.431583, 10.307511), (-3.82, -18.52)]`, `rect=(-9.65, -20.82, 5.83, 7.29)`. `_polyline_hits(pts,[rect])` returns False, while `_seg_hits_rect(...)` returns True, because `rx+rw` evaluates to `-3.8200000000000003`.
  - A 300,000-case fuzz, biased to flush edges, found 21 false rejections and no false acceptance.
  - It could silently drop a real T8 through-box violation on future data.

MAJOR:
- `tests/test_traj_graph.py:132` only proves the pre-check does something for rectangles that are clearly disjoint. It would not catch the pre-check becoming unsound at a boundary. *Coordinator: in scope. Add the reproduced case, flush-edge boundary cases, and a seeded property test against the nested-loop oracle.*

MINOR:
- No comment explains why the pre-check is safe (the bbox-superset argument), unlike `_seg_hits_rect`'s float-aware docstring. *Coordinator: in scope.*

**Verified:**
- The real-scale sweep is unchanged in scope: the live registries, and the same `_wire_through_box_violations(...) == []`.
- "Loads geometry once" is a pure refactor of the test's own helper.
- **Byte-identical output**, independently, in a scratch copy with the old module imported beside the new one:
  - Knowledge: 519,856 bytes, `3b8364bd…`;
  - When: 1,078,729 bytes, `e82969d5…`.

  Both are equal, so the defect is latent on today's data.
- The ratchets are unaffected.

**Run:** `python -m pytest -q -n 2 tests/test_traj_graph.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py -p no:cacheprovider --durations=5` → **32 passed in 139.60s**.
- `test_meta_knowledge_and_when_wires_avoid_unrelated_boxes`: 48.17 s.
- `test_fallback_dag_and_sw_graph_wires_avoid_unrelated_boxes`: 33.73 s.
- `test_t8_no_wire_passes_through_an_unrelated_node_box` is now the file's slowest, at 50.97 s. It is outside this row.
