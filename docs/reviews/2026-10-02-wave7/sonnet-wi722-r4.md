# Sonnet review — WI-722 rebuild, fix round 2 (build/wi-722 at 45a0bab2)

Reviewer: Claude Sonnet 5.5 (read-only). Range `ed57db9f..45a0bab2`, and the whole lane `2e13b2bd..45a0bab2` as the landing candidate.

45a0bab2 SOUND

**BLOCKER:** none. **MAJOR:** none. **MINOR:** none.

**r3 findings resolved.**
- Estimates `traj_render.py:511-514`: `_BLAB_CH = ceil(0.7 x 12) = 9`, `_BSUB_CH = ceil(0.65 x 10.5) = 7`, derived from `NODE_TYPE_PX`. The band test (`tests/test_traj_views.py:1109-1117`) pins 0.65-0.85 em against the emitted tokens: 9/12 = 0.75, 7/10.5 = 0.67 pass; 1.0 em (1.0, 1.05) fails the ceiling; the original 7/5 at the new sizes (0.58, 0.48) fails the floor. Not vacuous.
- Seam budget `traj_views.py:555-556`: `_SW_LABEL_CH = ceil(0.65 x 12) = 8`, budget `(168-16)//8 = 19`. The test (`1120-1145`) requires `gen_trajectory`, `traj_render.py` and a 19-char name in full, and a 20-char name truncated to 18 + ellipsis.
- Scan gaps closed: `font:` shorthand and `#id` selectors (with `svg_ids`), parametrized detection cases (`1091-1105`).
- Comment `traj_render.py:65-66` reads as the ~86% shrink limit, the 9 px floor stated separately.

**Accepted consequence.** "W4 Human & adopter surfaces" (27 chars) at the 172 px cap: 148 px of text; at ~0.55 em (5.8 px/char at 10.5 px) it needs ~156 px; fitting needs <= 0.52 em, unrealistic. Caused by the larger type, not the estimate; raising the cap is out of scope. Not a defect of this lane.

**Whole lane.** `git diff 2e13b2bd 45a0bab2 -- docs/requirements docs/test docs/rubrics`: LLR-116 `detail` and `code_symbol`, TC-121 `method` and `expected`, the rubric T7 line; nothing else. The wording matches the final code (`NODE_TYPE_PX = {"nlabel": 12, "nsub": 10.5, "nhead": 13}`, `traj_render.py:74`; min-width = ceil(natural x 9 / smallest token)); the character estimates are layout-only and not in the wording. Worktree clean.

**Commands:** `pytest -q -n 2 -p no:cacheprovider tests/test_traj_views.py tests/test_traj_panels.py tests/test_gen_trajectory.py tests/test_traj_render.py`: `152 passed in 46.61s`.
