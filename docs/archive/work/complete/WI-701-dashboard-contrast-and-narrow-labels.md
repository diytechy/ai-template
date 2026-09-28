+++
id = "WI-701"
title = "Dashboard: clear TC-055's cross-family Critique findings (T5 contrast of the selection fade and the light-theme descend arrows, T4 labels at 390 px)"
workstream = "dashboard"
specref = ""
sr_refs = ["SR-054"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built by one builder, reviewed SOUND by Codex Sol at 86ea26c8. The last
Done-when bullet (TC-055 re-judged cross-family) is WI-703's, which waits on
this row and runs in the commits right after this close. Its record is the
log fragment's section "WI-703: TC-055 re-judged on the fixed dashboard".

- **T5 (both findings, one cause).** Every node de-emphasis faded by
  opacity (`.35` on the drill's trace-muted, `.15` on the icicle, flat
  roadmap and knowledge hover dims), which left white labels on phase fills
  at 1.28 to 2.0:1. Reaching 4.5:1 by opacity alone needs .98. All four
  rules now use one theme-invariant `:root` token, `--mute: saturate(.2)`.
  Edge fades keep their opacity, and `--o-ghost` is gone. TC-296 (Drafted,
  under new Drafted LLR-285) computes each de-emphasised node's label
  contrast in both themes, red at 1.28:1 before the fix. The model matched
  Chrome's rendered pixels on five sampled blocks.
- **T4 at 390 px: within the approved floor, nothing changed.** Every
  diagram wider than its card renders at exactly SHRINK_FLOOR 0.62, so node
  labels land at 6.2 px (`--nlabel`) and 5.27 px (`--nsub`), the floor
  TC-121 pins. Recorded for the owner: the floor's own comment calls about
  5 px illegible, so SHRINK_FLOOR looks miscalibrated for today's 10 and
  8.5 px node type. Moving it means amending LLR-116 and TC-121.
- **The What drill's overflow card** fades its bottom edge while content is
  cut below (`.clipb`, beside `.clipr`). A keyboard focus ring hidden by the
  mask is now drawn inside the box.
- The page golden is regenerated for the intended CSS and JS only.

Also recorded: the rubric's T5 does not yet say its de-emphasis half is now
a test (LLR-285, TC-296). The rubric is a declared input of TC-055, so it is
left for a change that re-judges TC-055 anyway.

## Context

TC-055 (the dashboard usability Critique; SR-054, LLR-055) records a FAIL at
8bebd4cf. That is its first qualifying result: a cross-family judge (Codex
Sol) read every shot of the declared matrix as unscaled native-resolution
tiles. The verdict is the specref. Its findings, with the tiles that show
them:

- **T5 at 1680 px (and in principle every width):** the When roadmap's
  default render auto-selects a card and fades every other phase card and
  its ports. In the light theme the faded cards are pale with white text,
  below the contrast floor T5 holds every control to
  (`1680px-{light,dark}-dag-full-t03`).
- **T5 at 390 px:** in the light theme, the When diagram's white descend
  arrows wash into the pastel phase blocks (`390px-light-dag-full-t05`).
- **T4 at 390 px:** the station-cycle card annotations and the How
  system-context crossing descriptions are scaled below comfortable
  default-zoom reading (`390px-*-process-full-t05`/`t06`,
  `390px-*-sw-full-t04`). The same judge passed T4 at 390 px on a focused
  look at fe96ec69 (`docs/reviews/2026-09-27-wave5/sol-tc055-t4.md`), so
  settle this one against the rubric's scale-to-fit legibility floor
  (TC-121) before changing anything.

Also on this surface, from the same-family session at fe96ec69 (not a
qualifying judge; recorded as an observation): the What (spine) drill shows 9
of 31 SN blocks inside a `max-height:660px; overflow:auto` card, with no
visible scroll affordance under overlay scrollbars.

The tiles are regenerated from `scripts/dashboard-shots/shoot.mjs`. Attach
tall shots to a judge as native tiles, never whole: a 24,076 px shot sent as
one image is downsampled into a false T4 finding (wave-5 ruling 31).

## Done-when

- The two T5 findings are fixed, with a mechanized contrast check where one
  is possible (a faded, non-selected control and the descend arrow each
  clear the body-text floor in both themes), red first.
- The T4 finding at 390 px is either fixed or shown to be within the
  TC-121 legibility floor, with the reason recorded.
- The What drill's overflow card carries a visible scroll affordance, or the
  reason it needs none is recorded.
- TC-055 is re-judged by a cross-family Critique session over native tiles,
  and its recorded result is pass.
- The commit bar passes.
