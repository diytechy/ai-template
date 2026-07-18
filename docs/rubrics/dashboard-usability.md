# Rubric — Dashboard usability (SR-054)

**Adjudicates:** SR-054 (dashboard usability, `Verification=Critique`).
**Used by:** the SR-047 critique loop — a fresh, provider-heterogeneous CRITIQUE
session judges the generated `PROJECT_STATE.html` against the numbered anchors
below, receiving this rubric + the SN/SR intent + the artifact recipe and **never
the implementer's self-assessment**. Authored at `[v3]-[g2]` (WI-135) from the
SR-054 / SN-024 / SN-023 intent, not from the possibly-lax TC.

The verdict is `VERDICT: APPROVE|CHANGES-REQUESTED findings=N` with each finding
citing an anchor id (`T1`…`T4`). APPROVE requires every anchor satisfied. Judge as
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
start-collapsed per the SR-051 `>3` rule so a large project is not a wall of
nodes on open — while a small project still reads flat. *Bad:* the When view opens
fully exploded with hundreds of overlapping nodes.

**T3 — Detail in context.** Revealing detail (descending a container, opening a
detail panel) does not lose the surrounding context — a breadcrumb or inline panel
keeps the reader oriented. *Bad:* descending a layer replaces the whole view with
no way back to where you were.

**T4 — Label legibility.** Labels stay readable at default zoom, with no clipped,
truncated-without-affordance, or overlapping text. *Bad:* node labels collide or
run past their block at the default render.

## Notes for the critic

- Do the three tasks yourself against the generated `PROJECT_STATE.html` and
  report, per task, the number of tab switches / clicks it actually took.
- A clipped or overlapping label is a T4 failure even if everything else is clean
  — legibility is a floor.
