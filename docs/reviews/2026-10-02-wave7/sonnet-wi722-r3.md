# Sonnet review — WI-722 rebuild, fix round 1 (build/wi-722 at ed57db9f)

Reviewer: Claude Sonnet 5.5 (read-only). Range `e5e42767..ed57db9f`, and the lane `2e13b2bd..ed57db9f`.

ed57db9f NOT YET SOUND

Round 1's BLOCKER and MINOR resolved; its MAJOR resolved by an over-correction that regresses legibility.

**BLOCKER:** none. `traj_views.py:637` uses `font-size:var(--nlabel)`; no non-token SVG size remains in `rendering/*.py`.

**MAJOR**
- `traj_render.py:513-514` `_BLAB_CH = 12`, `_BSUB_CH = 11` (1.0 em/char) roughly halves label capacity. Uses: `_tier_col_width` (525), `nbudget` sub and name-line budget (748), `max_label` (764), the seam budget (`traj_views.py:631`). Real sans ~0.6-0.65 em bold, ~0.55-0.6 em regular. (a) Any label of 13+ characters now pins columns at the 172 px cap (a 14-char label: 122 px before, 192->172 now). (b) At the cap (148 px of text): bold budget 21 -> 12 chars (real fit ~20); sub budget 29 -> 13 (real ~25); `_fit_lines` 2-line budget 58 -> 26; the CMP name line 29 -> 13, so "W4 Human & adopter surfaces" (27) is now cut to 12 + ellipsis, though the comment at 744-747 says that line exists so the full name reads. Proportional fix: ~0.7 em bold, ~0.62-0.65 em regular, rounded up (`_BLAB_CH = 9`, `_BSUB_CH = 7`), still 20-25% over; pin a 0.65 em floor (and optionally a ~0.85 em ceiling) in `test_t4_drill_character_estimates_cover_emitted_type_tokens`.
- Seam-node budget cut from 22 to 12 chars ((168-24)//12); regular 12 px text at ~7 px/char fits ~20, so 13-22 char names (`gen_trajectory`, `traj_render.py`) now truncate. `test_t4_seam_node_labels_fit_their_rectangles` uses the same 1 em model, so cannot catch it. Fix: a seam-specific regular-weight budget, ~0.65 em: (168-16)//8 = 19.

**MINOR**
- `traj_render.py:65-66` phrasing of the 86% shrink limit reads as the floor.
- `_svg_type_escapes` gaps: the `font:` shorthand; a CSS rule targeting SVG only by `#id`.

**Scan test** sound for its scope: iterates every fresh emitter document, asserts the seam page is present, checks attributes, inline styles and CSS rules; would have caught the original literal.

**Commands:** `pytest -q -n 2 -p no:cacheprovider tests/test_traj_views.py tests/test_traj_panels.py tests/test_gen_trajectory.py tests/test_traj_render.py`: `145 passed in 47.08s`. Nothing rendered.

**Coordinator:** the MAJOR's arithmetic checked against the code; the proportional fix adopted for round 2.
