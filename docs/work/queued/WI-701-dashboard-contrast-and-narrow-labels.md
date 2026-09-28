+++
id = "WI-701"
title = "Dashboard: clear TC-055's cross-family Critique findings (T5 contrast of the selection fade and the light-theme descend arrows, T4 labels at 390 px)"
workstream = "dashboard"
specref = "docs/reviews/wi-698-re-judge-tc-055-declared-inpu/001-ADJUDICATE-8bebd4cf.md"
sr_refs = ["SR-054"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

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
