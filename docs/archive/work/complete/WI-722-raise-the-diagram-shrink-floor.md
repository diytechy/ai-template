+++
id = "WI-722"
title = "Raise the diagram shrink floor to a rendered-pixel label minimum, and settle TC-055's T5 at 1280 px (OI-96)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-054"]
needs = []
buildtier = "medium"
priority = 0
safety_class = "spine"
+++

## Deliverable

The diagram shrink floor is a rendered-pixel label minimum (OI-96 (a), the owner's
2026-09-29 direction), rebuilt from trunk after the first build's loss.

- **Type scale:** one `NODE_TYPE_PX` table (`traj_render.py`) emits 12 px node
  labels, 10.5 px sub-labels and the existing 13 px headline; every SVG text size
  goes through these tokens (the seam graph's literal `font-size="10"` included).
- **Floor:** each SVG's `min-width` is `ceil(natural x 9 / smallest emitted token)`,
  so no node label renders below 9 px and a diagram shrinks to about 86% of natural
  width before it scrolls with its cue; `min-width` never exceeds natural width.
- **Layout estimates:** drill column and truncation estimates derived from the tokens
  (0.7 em bold, 0.65 em regular), pinned to a 0.65-0.85 em band; seam labels have
  their own regular-weight budget (19 characters). Against trunk, most drill columns
  widen (124 -> 164 px); one 27-character component name truncates at the 172 px
  column cap because of the larger type.
- **Tests:** every emitted SVG is scanned for a text size outside the tokens
  (attributes, inline styles, CSS rules, `font:` shorthand, `#id` selectors), with
  the seam graph forced; floor, band and seam-budget tests read emitted values.
- **Rows amended in place** (status left Approved, for this merge's spine-acts
  adjudication): LLR-116 `detail` (and its `code_symbol` pointer), TC-121 `method`
  and `expected`; the rubric's T7 threshold expression.
- **T5 at 1280 px:** recorded, not judged: the roadmap (natural 1408 px, min 1207 px)
  does not fit beside the 320 px detail column, so the scroll cue's right-edge
  gradient applies, and phase 3 is also trace-muted by the default selection. The
  perceptual call is WI-713's.
- **Reviews:** Sonnet 5.5, three rounds (`docs/reviews/2026-10-02-wave7/sonnet-wi722-r2.md`
  to `-r4.md`): NOT YET SOUND (a literal 10 px seam label below the floor; stale
  width estimates), NOT YET SOUND (estimates over-corrected to 1.0 em), SOUND at
  45a0bab2.

## Context

HELD 2026-09-29, mid-lane. The first build is on `build/wi-722` at d451cb64.
Sonnet found it NOT YET SOUND
(`docs/reviews/2026-09-28-wave6/sonnet-wi722-r1.md`):
- the node sub-label token (8.5 px) is below the 9 px floor at natural size;
- so `min-width` exceeded `max-width`, and every diagram rendered at a
  fixed width;
- the tests re-derived the floor with the same formula, and so could not
  see it.

The owner's direction for the fix round (OI-96, DIRECTION 2026-09-29) is:
- raise the node type scale to 12 px labels and 10.5 px sub-labels;
- keep a 9 px floor for every label, so a diagram shrinks to about 86% of
  its natural width before it scrolls;
- the tests must assert that the floor never exceeds the natural width;
- re-check the rubric's T7 sentence and LLR-116 and TC-121 against the new
  numbers.

WI-713, TC-055's cross-family re-judge, follows, with a non-Codex judge,
because Codex wrote the rendering.

Released 2026-09-29 by the coordinator, under the owner's OI-96 condition. After the wave-6 lanes, the only queued rows left besides WI-739 and WI-740 are gated on the owner or on a person: WI-541, WI-657, WI-667 and WI-697, and WI-684 and WI-688. So the queue is "mostly free". WI-713, TC-055's cross-family re-judge, follows this row. The judge must be from a family other than this row's builder's.

DEFERRED by the owner's direction (2026-09-28, ruling OI-96): the fix is
ruled, but it and TC-055's re-judge (WI-713, which needs this row) wait until
the rest of the queue is mostly done. The owner's words: "I would prefer for
other work items to be completed (unless there are dependencies) until
perception judgement happens again just so more churn waits till the queue is
mostly free." Nothing else depends on this row. The coordinator moves it to
`queued/` once the ordinary frontier has largely drained; until then TC-055
keeps its recorded FAIL.

OI-96 ruled (a): replace the ratio floor with a rendered-pixel minimum.
Approved LLR-116 and TC-121 pin `SHRINK_FLOOR = 0.62` of natural width
(`project-trajectory/scripts/rendering/traj_render.py`). At 390 px that
leaves `--nlabel` at 6.2 px and `--nsub` at 5.27 px, which TC-055's
cross-family Critique failed on T4 (`docs/reviews/wi-703-re-judge-tc-055-declared-inpu/`).
The ratio was chosen for 12 px labels; the node type scale is now 10 and
8.5 px, so it drifted.

Scope:

- **Amend in place** (status left Approved, for the next spine-acts batch's
  adjudication): LLR-116 `detail` states the floor as the smallest rendered
  node-label size (for example 9 px, derived from the smallest node type
  token, not a hand-set ratio); TC-121 `method` and `expected` pin that
  minimum against the emitted type tokens rather than a ratio.
- **Build** the floor so each SVG's `min-width` follows from its smallest
  label size, and keep the sideways-scroll cue for views that pass it.
- **T5 at 1280 px:** the second finding, on the `3` phase card at the
  roadmap's far right. The coordinator's reading is that it is the overflow
  edge fade marking a sideways scroll, not the de-emphasis (the same judge
  passed T5 at 1680 px). Confirm it on native tiles and fix it here if it is
  a real defect; otherwise record why it is not.
- The slow tests pinning the floor (`tests/test_traj_views.py`
  `test_t7_*`) move with it.

Done when the amendments are drafted, the build is green, and WI-713 can
re-judge TC-055 cross-family on native tiles (wave-5 ruling 31).
