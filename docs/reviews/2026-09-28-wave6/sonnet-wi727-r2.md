<!-- Claude Sonnet (read-only) confirmation of WI-727's fix round, build/wi-727 c88f16fa..427fbaf4. -->

427fbaf4 SOUND

BLOCKER: none

MAJOR: none

MINOR:
- **`traj_graph.py:248-260`: `margin = 0.05` is an empirical constant tied to the 0.1px grid**, not an epsilon bound. It stays sound at every magnitude this renderer produces, with about nine orders of magnitude of headroom: the rounding error of `rx+rw` at 5e4 is about 1.1e-11. It would break down only near 1e14. *Coordinator: accepted as argued.*
- **`tests/test_traj_graph.py:181-197` (`test_polyline_hit_test_includes_bbox_edge_and_degenerate_rect_touches`) still passes with the margin removed.** Its floats are exact, so it never exercises the rounding failure. It is legitimate coverage of the boundary logic, but not a regression guard for the defect. The other two new tests are. *Coordinator: accepted; the Deliverable says so.*

**The fuzz** ran the fixed `_polyline_hits` against the `_seg_hits_rect` nested-loop oracle:

| Cases | Coordinates | False rejections | False acceptances |
|---|---|---|---|
| 300,000 | ±50, flush-biased | 0 | 0 |
| 100,000 | ±5e4 | 0 | 0 |
| 50,000 | ±2e6 | 0 | 0 |
| 50,000 | ±1e13 | 0 | 0 |

Targeted probes at 1e14 to 1e16 found no false rejection. The reported repro case now returns True.

**Would the new tests fail with the margin removed?**
- The repro test (`test_polyline_hit_test_keeps_a_rounded_flush_edge_candidate`): **fails**.
- The seeded oracle test (`test_polyline_hit_test_matches_segment_oracle_for_seeded_flush_edges`): **fails**, on 1 of 501 cases.
- The exact-boundary test: passes.

**The WHY comment** (`traj_graph.py:248-254`) states the touch-as-hit semantics, the source of the rounding, the grid tie, and the bbox-superset property.

**Byte identity:** an independent render of f1733daa and 427fbaf4 on the same live registries gives identical bytes and SHA-256 for both Knowledge (`3b8364bd…`) and When (`e82969d5…`). The absolute sizes differ from the first review's figures, a measurement-basis loose end that does not affect the controlled comparison.

**Run:** `python -m pytest -q -n 2 tests/test_traj_graph.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py -p no:cacheprovider --durations=5` → **35 passed in 90.97s**. `test_meta_knowledge_and_when_wires_avoid_unrelated_boxes` took 37.74 s under `-n 2`.
