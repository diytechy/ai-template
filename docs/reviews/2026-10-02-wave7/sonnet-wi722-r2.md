# Sonnet review — WI-722 rebuild, round 1 (build/wi-722 at e5e42767)

Reviewer: Claude Sonnet 5.5 (Agent subagent, read-only). Builder: Codex Sol (gpt-6.1-sol). Range `2e13b2bd..e5e42767`. (File name r2: r1 is the first build's review, wave 6.)

e5e42767 NOT YET SOUND

**BLOCKER**
- `project-trajectory/scripts/rendering/traj_views.py:635` (`sw_graph`) emits a literal `font-size="10"` on node text, outside the `--nlabel` token. `sw_graph` returns through `_svg_wrap`, whose min-width is `ceil(natural * 9 / 10.5)`, so that text renders at 10 x 9/10.5 = 8.57 px at the floor, below the owner's 9 px floor for every label. Same class as r1's 8.5 px sub-label: the floor is derived from the token table, not from the smallest text actually emitted. The fixture and PROJECT_STATE.html emit no seam graph, so no test saw it. Fix: route through a token or include it in the derivation; the test should scan every emitted svg for non-token text sizes, or a fixture should force the seam graph.

**MAJOR**
- `traj_render.py:511-512` `_BLAB_CH = 7`, `_BSUB_CH = 5` (px/char, used at 523 and 746/762) are commented as over-estimates of the glyph widths; set for 10 px / 8.5 px. At 12 px bold, 7 px/char is about the real width; at 10.5 px, 5 px/char is under the ~5.3-5.8 px a sans font needs, so the claim is false for sub-labels and right-sized drill blocks and the `max_label`/`nbudget` budgets may clip or overrun. Not rendered; the 24 px padding probably absorbs most of it, but no change or evidence was given.

**MINOR**
- `traj_render.py:64-70` header comment still says "squeezing a 900px graph into 390px shrinks a 12px label to ~5px". Stale.
- `tests/test_traj_panels.py` station test is sound (reads emitted style and CSS).

**Checks.** r1's findings resolved: floor above max-width (min-width ~0.857 x natural, tests assert `0 < floor <= natural` and that `floor - 1` breaks 9 px); the 8.5 px sub-label (now 10.5 px, tested `>= 9`); the tests mirroring the formula (they read emitted CSS and min/max widths); the rubric/LLR-116/TC-121 now consistent ("390 x 10.5 / 9" correct). `_svg_fit_style` reaches dag/sw/know, the icicle, `_drill_layer_svg`, `traj_context.py:289` and the station panel. Edge labels use `--nsub`. Scope: `--nhead` was already 13 px at 2e13b2bd (`gen_trajectory.py:372`); the NODE_TYPE_PX table moves the declaration into Python, values changed only nlabel 10->12 and nsub 8.5->10.5. Amended cells: exactly LLR-116 code_symbol + detail, TC-121 method + expected, rubric T7; text matches the code. Golden fixture: only the token values and three min-widths.

**Commands:** in the worktree, `pytest -q -n 2 -p no:cacheprovider tests/test_traj_views.py tests/test_traj_panels.py tests/test_gen_trajectory.py`: `109 passed in 34.98s`. Read-only git diff/grep/sed; nothing rendered.

**Coordinator:** both the blocker and the major verified by grep (`traj_views.py:635` is the only non-token SVG font size; `_BLAB_CH`/`_BSUB_CH` unchanged). Sent to a fix round on the same lane.
