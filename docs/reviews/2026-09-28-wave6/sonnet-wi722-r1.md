<!-- Claude Sonnet (read-only) review of WI-722, build/wi-722 a297b9ff..d451cb64. Built by Codex Sol; committed by the coordinator. -->

d451cb64 NOT YET SOUND

BLOCKER:
- **The floor formula makes every SVG a fixed, non-scaling width** (`project-trajectory/scripts/rendering/traj_render.py:70-85`).
  - `_svg_fit_style` computes `min_width = width * MIN_RENDERED_NODE_LABEL_PX / smallest_label_px`, with the minimum at 9 and `smallest_label_px = min(10, 8.5) = 8.5`. That is a ratio of about 1.0588, so `min-width` always exceeds `max-width`. For example, `_svg_fit_style(390)` gives `max-width:390px; min-width:413px`.
  - When min-width exceeds max-width, CSS applies min-width. So every diagram renders at a fixed `natural × 1.0588` at every viewport and always overflows. That reintroduces the fixed-width defect the mechanism exists to prevent.
  - The refreshed golden carries it: `max-width:848px; min-width:898px` and `max-width:672px; min-width:712px`.
  - The root cause is that `--nsub` is 8.5 px at natural size, already below the 9 px floor, so no shrink room exists.
  - `tests/test_traj_views.py:1051-1070` re-derives the floor with the same formula and never asserts `floor <= natural`, so it cannot see this.

MAJOR:
- **The rubric's rewritten anchor** (`docs/rubrics/dashboard-usability.md:152-158`) is needed, because `SHRINK_FLOOR` is gone. Combined with the blocker, though, it would bless scrolling at any width. Re-check it once the floor is fixed.
- **LLR-116's `detail` and TC-121's `method` and `expected`** describe "scale-to-fit until the smallest node label reaches 9 px, then overflow". That cannot occur while `--nsub` is 8.5 px. It has the same root cause as the blocker.

MINOR: none

**Verified:**
- The diff is scoped to the floor mechanism, and LLR-116 and TC-121 are still Approved.
- `_svg_fit_style` at 300, 390, 900 and 2000 px gives min above max in every case.
- The golden shows the same inversion.

**Run:** `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt python -m pytest -q -n 2 tests/test_traj_views.py tests/test_traj_panels.py tests/test_gen_trajectory.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py -p no:cacheprovider` → **114 passed in 98.01s**. The relevant assertions mirror the buggy formula, so this is not evidence the floor works.

*Coordinator: the fix needs a value choice inside OI-96 (a), namely what the 9 px minimum means when a sub-label token is 8.5 px at natural size. That choice was put to the owner; WI-722's lane is held until the owner answers.*
