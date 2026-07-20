# Rubric — Dashboard usability (SR-054)

**Adjudicates:** SR-054 (dashboard usability, `Verification=Critique`).
**Used by:** the SR-084 critique dispatch — a fresh, provider-heterogeneous CRITIQUE
session judges the generated `PROJECT_STATE.html` against the numbered anchors
below, receiving this rubric + the SN/SR intent + the artifact recipe and **never
the implementer's self-assessment**. Authored at `[v3]-[g2]` (WI-135) from the
SR-054 / SN-024 / SN-023 intent, not from the possibly-lax TC.

The verdict is `VERDICT: APPROVE|CHANGES-REQUESTED findings=N` with each finding
citing an anchor id (`T1`…`T7`). APPROVE requires every anchor satisfied. Judge as
a **first-time reviewer** opening the dashboard cold.

## The core reading tasks (the concrete "one tab switch" list)

SR-054's "within one tab switch" concretizes to these three tasks. From the
landing view, each must be reachable with **at most one tab switch** (one click on
a nav button — no hunting, no scrolling a dense graph to find the entry point):

1. **Find the project state** — what gate the project is at and what is done
   vs open (the roadmap / phase summary or the Process tab's lifecycle panel).
2. **Find the next work** — the next action / next WI (the status surface or the
   resume-loop panel).
3. **Find how the parts connect** — the module map / interface seams (the How-SW
   view).

## Anchors

**T1 — Task findability.** Each of the three tasks above is reachable within one
tab switch and the entry point is obvious (a labelled tab, not an unlabelled
region). *Bad:* "how the parts connect" requires two tab switches or expanding
three nested blocks to locate.

**T2 — Default-density legibility.** Views default to a legible density —
start-collapsed per the SR-089 `>3` rule so a large project is not a wall of
nodes on open — while a small project still reads flat. *Bad:* the When view opens
fully exploded with hundreds of overlapping nodes.

**T3 — Detail in context.** Revealing detail (descending a container, opening a
detail panel) does not lose the surrounding context — a breadcrumb or inline panel
keeps the reader oriented. *Bad:* descending a layer replaces the whole view with
no way back to where you were.

**T4 — Label legibility.** Labels stay readable at default zoom, with no clipped,
truncated-without-affordance, or overlapping text. *Bad:* node labels collide or
run past their block at the default render.

**T5 — Interactive-control legibility, in every theme.** Every control a reader
must find and operate — tab buttons, expand/collapse affordances, focus rings,
and any filter or field — clears the same contrast floor as body text against
its own background, and clears it in **both** themes the dashboard ships (light
and dark), not only the one it was designed in. This anchor does not restate the
numbers: the WCAG AA thresholds live in the accessibility rubric's [A4 — Text
contrast](dashboard-accessibility.md); T5 extends that floor to interactive
controls and adds the both-themes obligation. *Bad:* the active-tab underline or
a focus ring is crisp in light theme but washes into its background in dark.

**T6 — Theme-lock (no mid-view inversion).** The dashboard renders in one theme
at a time — light, dark, or a system-following auto — applied to the whole page;
no tab, panel, or detail view flips to the opposite theme mid-view. A reader
scrolling or switching tabs under one theme selection never crosses a light/dark
seam. *Bad:* under the same theme setting the When tab renders dark while the
Process tab renders on a light card, so switching tabs inverts the page.

**T7 — Viewport fit at the declared widths.** The layout fits each width in the
declared render matrix — the 390px mobile landing and the declared desktop widths
(the `render-dashboard-critique` shot set is the source of truth) — with no
horizontal scroll and nothing clipped past the viewport edge at the initial,
above-the-fold view; narrow content reflows rather than forcing a sideways
scroll. (T4 governs the legibility of an individual label; T7 governs whole-layout
fit.) *Bad:* at 390px the nav bar or a graph spills past the right edge and needs
horizontal scrolling to read.

## Notes for the critic

- Do the three tasks yourself against the generated `PROJECT_STATE.html` and
  report, per task, the number of tab switches / clicks it actually took.
- A clipped or overlapping label is a T4 failure even if everything else is clean
  — legibility is a floor.
- T5–T7 are floors too: check T5 in **both** themes, not just the default, and
  confirm T7 against the 390px shot specifically — a layout that fits at desktop
  can still overflow at mobile.

---

*Anchors T5–T7 distill the mandatory legibility pre-flight from
[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill/blob/98565e65bc3274ddf6eb0838734341714057178b/skills/taste-skill/SKILL.md)
(MIT, © 2026 Leonxlnx), pinned at commit `98565e6`, reduced to their
stack-neutral, checkable core — its Tailwind class names and aesthetic dogma are
not adopted.*
