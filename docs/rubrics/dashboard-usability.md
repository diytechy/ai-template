# Rubric — Dashboard usability (SR-054)

**Adjudicates:** SR-054 (dashboard usability, `Verification=Critique`).
**Used by:** the SR-084 critique dispatch — a fresh, provider-heterogeneous CRITIQUE
session judges the generated `PROJECT_STATE.html` against the numbered anchors
below, receiving this rubric + the SN/SR intent + the artifact recipe and **never
the implementer's self-assessment**. Authored at `[v3]-[g2]` (WI-135) from the
SR-054 / SN-024 / SN-023 intent, not from the possibly-lax TC.

The verdict is `VERDICT: APPROVE|CHANGES-REQUESTED findings=N` with each finding
citing an anchor id (`T1`…`T8`). APPROVE requires every **live** anchor satisfied.
Judge as a **first-time reviewer** opening the dashboard cold.

> **T1, T3, T6 and T7 are bound as tests, not critique anchors** (owner rulings
> 2026-07-26) — T1 to `LLR-115`/`TC-120`, T3 to `LLR-100`/`TC-103`, T6 to
> `LLR-117`/`TC-122`, T7 to `LLR-116`/`TC-121`; none is **yours to judge**. The
> live anchor set is **T2, T4, T5, T8**.

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

**T1 — Task findability. BOUND as a test 2026-07-26 (owner ruling, WI-315) —
the mechanizable bar is `LLR-115`/`TC-120`; do not judge it here.** The bar it
stated: each of the three tasks above is reachable within one tab switch from the
landing view, and its entry point is a **labelled** nav control or a **named
surface on the landing view** — never an unlabelled region the reader has to
discover by clicking around. (Reworded by the 2026-07-26 ruling: the anchor no
longer turns on the word *obvious*. "Obvious" was always glossed here as
labelled-not-unlabelled, and that gloss is the whole bar.) The reword left
nothing perceptual, so — like T3 — T1 left the critique: `TC-120` resolves each
task's entry point from the **rendered artifact carrying its real registry
data**, never the nav skeleton. 119-CRITIQUE's MAJOR was a next-work surface that
exists in the emitter but rendered *nothing* because no work item was `active`,
which a structural nav-skeleton check would have passed — `WI-305` fixed the
surface, `WI-315` froze it. A critic who believes findability is violated has
found a gap in `TC-120` — route it through change-intake to harden the test,
never through a verdict. *Bad (the test's job now):* "how the parts connect"
requires two tab switches or expanding three nested blocks to locate.

**T2 — Default-density legibility.** Views default to a legible density —
start-collapsed per the SR-089 `>3` rule so a large project is not a wall of
nodes on open — while a small project still reads flat. *Bad:* the When view opens
fully exploded with hundreds of overlapping nodes.

**T3 — Detail in context. RETIRED as a critique anchor 2026-07-26 (owner ruling)
— bound to `LLR-100`/`TC-103`; do not judge it here.** The bar it stated:
revealing detail (descending a container, opening a detail panel) does not lose
the surrounding context — the drill emits a breadcrumb whose crumb click
**truncates the trail to that ancestor**, restoring the parent view, and detail
opens in a persistent inline panel. *Bad:* descending a layer replaces the whole
view with no way back to where you were.

The reason it left: **the critique cannot verify T3's actual claim, and the test
can.** The shot matrix captures initial views only, so a static-PNG reviewer sees
that a breadcrumb *exists* and stops — 115-CRITIQUE passed it on markup, and
119-CRITIQUE passed it with the caveat "no descended/breadcrumb state was
captured in this shot set, so the return path itself is unverified". `TC-103`
clicks the crumb and asserts the restore. The residual clause "keeps the reader
oriented" never independently passed or failed a round; the breadcrumb *is* the
orientation the anchor asked for. A critic who believes T3 is violated has found
a gap in `TC-103` — route it through change-intake to harden the test, never
through a verdict.

**T4 — Label legibility.** Labels stay readable at default zoom, with no clipped,
truncated-without-affordance, or overlapping text. *Bad:* node labels collide or
run past their block at the default render.

*Two measurable halves of this anchor are now tests*, both `LLR-119`/`TC-124`:
**ink outside its own box** (WI-318 — every label line of every drill block is
measured against that block's rect, on both axes, in the emitted document) and
**the next-work card's own truncation** (WI-319 — it no longer budgets by
character count, and any residue it does cut carries a visible, script-free
reveal). A label you see running past its block, or that card cutting a title
dead, is therefore a **gap in `TC-124`** — route it through change-intake to
harden the test, never through a verdict.

What stays yours is the clause a measurement cannot settle **anywhere else in
the document**: whether a truncation a reader meets is **actionable**. An
ellipsis with no way to reveal the rest still fails T4.

**T5 — Interactive-control legibility, in every theme.** Every control a reader
must find and operate — tab buttons, expand/collapse affordances, focus rings,
and any filter or field — clears the same contrast floor as body text against
its own background, and clears it in **both** themes the dashboard ships (light
and dark), not only the one it was designed in. This anchor does not restate the
numbers: the WCAG AA thresholds live in the accessibility rubric's [A4 — Text
contrast](dashboard-accessibility.md); T5 extends that floor to interactive
controls and adds the both-themes obligation. *Bad:* the active-tab underline or
a focus ring is crisp in light theme but washes into its background in dark.

**T6 — Theme-lock (no mid-view inversion).** *Bound to `LLR-117`/`TC-122`
(WI-314) — not a critique anchor; kept here as the stated intent the test
mechanizes.* The dashboard renders in one theme
at a time — light, dark, or a system-following auto — applied to the whole page;
no tab, panel, or detail view flips to the opposite theme mid-view. A reader
scrolling or switching tabs under one theme selection never crosses a light/dark
seam. *Bad:* under the same theme setting the When tab renders dark while the
Process tab renders on a light card, so switching tabs inverts the page.

**T7 — Viewport fit at the declared widths. BOUND as a test 2026-07-26 (WI-307) — `LLR-116`/`TC-121`; do not judge it here.** The bar it stated: the layout fits each width in the
declared render matrix — the 390px mobile landing and the declared desktop widths
(the `render-dashboard-critique` shot set is the source of truth) — with no
horizontal scroll and nothing clipped past the viewport edge at the initial,
above-the-fold view; narrow content reflows rather than forcing a sideways
scroll. (T4 governs the legibility of an individual label; T7 governs whole-layout
fit.) *Bad:* at 390px the nav bar or a graph spills past the right edge and needs
horizontal scrolling to read.

**T8 — Edge routing legibility (owner acceptance, 2026-07-20 / WI-253).** In
every wired diagram (When DAG, How-SW graph, Knowledge graph, the drill views,
the Process hoops), a reader can follow any edge from source to target: **no
edge passes through an unrelated node box**, and edge crossings are minimized —
where a crossing is unavoidable it happens in open space, not under a label or
port cluster. *Bad:* a dependency wire cuts straight through an intermediate
WI's box so it reads as connected to it; three edges cross inside a port fan
and the sources become unattributable. (Known open finding: WI-253 tracks the
current crossing/through-box gap — a critique may cite it as filed, but T8
still blocks APPROVE until the render passes.)

## Notes for the critic

- Findability (T1) is now bound to `LLR-115`/`TC-120` — a test owns "each of the
  three tasks reachable in ≤ 1 labelled tab switch," so do **not** re-judge it.
  Still open the generated `PROJECT_STATE.html` cold, as a first-time reviewer, to
  judge the live legibility / layout anchors below.
- A clipped or overlapping label is a T4 failure even if everything else is clean
  — legibility is a floor.
- T5 is a floor too: check it in **both** themes, not just the default. T6 is no
  longer yours — `TC-122` holds the document to one theme mechanism at `:root`
  and forbids a mixed-family surface/ink pair, swept over every emitter; a seam
  you believe you see is a gap in that test and routes through change-intake.
  T7 is no longer yours either — `TC-121` holds every emitted diagram to scale-to-fit
  with a legibility floor. A view that still scrolls sideways at 390px is the
  floor working as designed (its natural width exceeds 390 / SHRINK_FLOOR), not
  a T7 finding; if you believe it is a defect, that is a gap in `TC-121` and
  routes through change-intake, never a verdict.

---

*Anchors T5–T7 distill the mandatory legibility pre-flight from
[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill/blob/98565e65bc3274ddf6eb0838734341714057178b/skills/taste-skill/SKILL.md)
(MIT, © 2026 Leonxlnx), pinned at commit `98565e6`, reduced to their
stack-neutral, checkable core — its Tailwind class names and aesthetic dogma are
not adopted.*
