+++
id = "WI-479"
title = "The dashboard renders an unbounded active-WI title into the hero: defensive truncation and disclosure, start-aligned grid, and a warn on non-concise titles (repo review 2026-08-19 M-03)"
workstream = "dashboard"
sr_refs = ["SR-052"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

The hero is defended: `build_html`'s active-WI line routes every title
through the same `_next_work_title` disclosure the Next-work card already
uses (native details/summary — same CSS, same keyboard operability, no new
JS); verified against the live WI-455 title, 2,253 raw chars → 187
rendered. `.cards` aligns start (the equal-height slab dies) and the
opened line is bounded at 60ch. The registry side is a WARN-ONLY advisory
(`_title_length_warns`, 120-char bound, open WIs only, summarized to ONE
line worst-first per the house precedent against unreadable warn floods)
— currently naming 12 open titles, no existing title reworded. Verified by
rendering a throwaway copy and screenshotting with the repo's own tooling
at 390/1280/1680px plus a 320px reflow check, and by exercising the
disclosure's keyboard path. Judged and recorded rather than churned: the
sticky-header capture artifact is the shots-README's own documented
caveat; the 10px/8.5px graph labels are real but their fix risks the
text-fitting math in two views — own WI; `_title_clause`'s abrupt
first-dash split is a pre-existing shared property now more visible.
Full suite 2660/13 green (one failure was the orchestrator's own R-D
token, fixed at close). check_trajectory.py re-stamped 4075→4131 with
reason.

## Context

`gen_trajectory.py` (~:754-773) concatenates every active WI's ENTIRE title
into the hero's `.sub.nowat` with no length or disclosure rule, and the
Definition/Execution grid (~:372-380) stretches both cells to equal height —
so one program-narrative title (WI-455's, in the review's screenshot matrix)
expands the Execution card to thousands of vertical pixels with a matching
blank slab beside it, and on mobile the reader scrolls screens of orange
prose before reaching navigation. Across the 390/1280/1680 px matrix the
review rates the landing view "largely unusable" — a robustness AND
accessibility failure (magnification and narrow screens pay worst), which
matters because the underlying practice (SR-052's keyboard/contrast/responsive
tests) is otherwise good.

The fix is defensive rendering FIRST, advisory second — ten of the eleven live
frontier titles are multi-sentence narratives, so a validation-only fix would
demand a mass reword of owner-authored registry text: (1) truncate the hero
title behind the same native `details/summary` disclosure "Next work" already
uses; (2) grid items align start, not stretch; constrain the active summary's
measure; (3) a warn-first advisory on WI title length at registry validation
(concise title; rationale belongs in the body) — warn, never error, and never
reword existing titles mechanically. Also from the same screenshot pass, judge
each: the sticky header overlays content in long-page capture (~:354-358), and
the fixed 10px/8.5px graph label sizes are hard to read in dense DAG views
(the review suggests a co-equal textual table view). Re-test keyboard focus
and zoom at 200%/400% against the dashboard-accessibility rubric. Adjacent:
WI-470 words the same surface's colour-carried meanings; no ordering
constraint, but the two should not fight over the hero markup in parallel.
