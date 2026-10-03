# Sonnet review — WI-750 (build/wi-750 at 9884f643)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range `579cd187..9884f643`.

9884f643 SOUND

**BLOCKER:** none. **MAJOR:** none.

**MINOR**
1. The Done-when's "removed or justified" is not met for the When perimeter and return-route crossings: the builder stopped at `traj_render.py:851-854`, pinned by `test_wi750_when_trunks_clear_sibling_output_fans`. Honest and proportional; the comment says a return route is necessary and minimising the rest needs joint routing, not that the crossings are unavoidable. TC-055's T8 may still fail on perimeter wires at the next re-judge. (Coordinator: no successor filed in advance; the re-judge due at this merge decides.)
2. `tests/test_traj_graph.py:~715` computes the floor with the same expression as `traj_render.py:84`; it reads the tokens and fixes a test red on trunk since 6a40d7b2, but calling the production helper would be stronger.

**T4:** `carrymax = int((x2 - x1) // _BSUB_CH)` with `_BSUB_CH = 7` (0.667 em, in band); captions painted after the system box; `_ctx_cut` ends in an ellipsis; REL labels `text-anchor="end"` clear of the curve. Live captions: capacity 33 characters, 231 units against the 234-unit lane (370-604; the 246-unit gap less 6 each side); every cut caption fits. `test_wi750_context_captions_fit_the_emitted_gap` checks extents against the emitted box edges, paint order and the `<title>` (the old cut of 54 x 7 = 378 units would fail it).

**T8:** Process exits swapped, both Béziers sampled at every shared y; How: same-row neighbours sorted by x, `stub=col_gap` with turns staggered by port rank, emitted segments checked for overlaps and T-junctions; When: the detour trunk sits half across the column gap, no other vertical inside the "1+5"/"4" fan reach. The router changes are gated on `fan_terminals`; shared-centre emitters keep their order; no byte-identity check for other explicit-port layouts.

**Scope:** no requirement row, test-case row or golden fixture changed.

**Commands:** `pytest -q -n 2 tests/test_traj_views.py tests/test_traj_panels.py tests/test_traj_graph.py tests/test_traj_render.py tests/test_gen_trajectory.py`: `189 passed in 103.97s`; `tests/test_traj_parse.py tests/test_traj_render_sweeps.py tests/test_traj_status.py`: `27 passed in 41.66s`; a caption-fit script under %TEMP%.
