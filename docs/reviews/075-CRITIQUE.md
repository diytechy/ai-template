# 075 — CRITIQUE (rendered-pixel critique of the current dashboard; WI-243 baseline re-date)

**Scope:** SR-054 (usability, T1–T7) primary; SR-052 (accessibility) and SR-053
(uniformity) spot-checked. Judged against
`docs/rubrics/dashboard-{usability,accessibility,uniformity}.md` — including the
**new T5–T7 anchors** (WI-244).
**Artifact:** the rendered PNG matrix from `scripts/dashboard-shots/shoot.mjs`
(36 shots, widths 390/1280/1680 × light/dark × the 5 tabs) at commit `3c3a968` —
the render recipe WI-243 wired into TC-053/054/055. This is a critique of
**pixels**, not the ~790 KB markup.
**Critic:** Claude (agent), via the `render-dashboard-critique` loop (WI-189).
Honest caveat: an agent critique is a weaker form than an independent
family-heterogeneous critic or a human eye (SR-047) — but it judges the rendered
view, which the frozen 2026-07-15 markup baseline could not. Owner-directed
2026-07-20 ("run the critique first, then decide the gate strength").

VERDICT: CHANGES-REQUESTED findings=5

## Findings

Ranked; each cites its shot and its tracking WI.

1. **[T2 default-density] Knowledge (OKF) tab opens fully exploded — the primary
   "hard to read" tab.** Every SN/SR/LLR/TC/IF concept node (100s) renders at
   once under a dense mesh of crossing edges — a wall of nodes, the exact T2
   *Bad* example. Unlike the When/DAG and How/SW tabs (which start-collapsed per
   the `>3` rule, SR-089), the Knowledge graph has **no** collapse/tiering.
   *Shots:* `1280px-{light,dark}-know-full.png`. → **the fix is the already-filed
   but DEFERRED [WI-159](../work/)** (Knowledge-tab density,
   start-collapsed re-spec); this critique **re-affirms it with fresh evidence**
   and it is the load-bearing finding.
2. **[T4 label legibility — clipping] Knowledge graph TC-column labels are
   clipped** at the graph container's right edge — TC ids truncate to
   "TC-03…", "TC-04…", indistinguishable. A symptom of the same over-wide exploded
   graph; **resolves when WI-159's collapse lands** (folds into finding 1).
   *Shot:* `1280px-light-know-full.png`.
3. **[T4 label legibility — truncation, MINOR] How (SW) component-block labels
   truncate** with an ellipsis: "CMP-003 — Quality ch…", "CMP-001 — Traceabili…",
   "CMP-004 — Unattended…", "CMP-005 — Scaffold &…". Truncation-*with*-affordance
   (borderline T4), but the full component name is unreadable at default zoom.
   *Shot:* `1280px-light-sw-full.png`. (Recorded in WI-189's findings; unfiled.)
4. **[T5 / uniformity — MINOR] When (roadmap DAG) phase-accent palette has low
   hue separation** — adjacent phases (1, 1+2, 2, 2+3, 3, 4) are near-identical
   maroon/purple in both the legend swatches and the blocks, hard to tell apart.
   *Shot:* `1280px-light-dag-full.png`. (WI-189 finding; unfiled.)
5. **[T7 viewport-fit — MINOR, carried] What (SR breakdown) icicle overflows at
   390px** — per WI-189, only SN+SR fit at mobile width; LLR/TC need horizontal
   scroll. **Carried from WI-189, not independently re-verified this session.**

## Cleared (checked, not findings)

- **When/DAG, How/SW, Process tabs:** start-collapsed / clean layout at 1280px —
  T1/T2/T3 hold (the Process working-loop enclosures A/B render fine, WI-165).
- **Mobile (390px) graphs:** get a "↔ Scroll sideways" affordance + a scroll
  container; the page body does not overflow — T7 handled *for the graphs*.
- **Both themes:** node-fill contrast holds in dark as in light — T5 (fills) OK;
  the density, not contrast, is the problem.
- **The 390px sticky-header / EXECUTION-card overlap** in the `-full` shots is the
  documented `fullPage` + `position:sticky` capture artifact (WI-189 (b)), **not**
  a real defect — confirmed by the README caveat.

## Disposition

Per the render-critique loop (build the eyes, not a redesign): findings become
WIs, never an inline edit here. Finding 1 (+2) = **WI-159** (deferred — its
priority is the owner's call, given this re-affirmation). Findings 3–5 are minor
polish recorded in WI-189 but never filed as rows; whether to file them is queued
for the owner. This verdict **re-dates the perceptual evidence** (it is now newer
than the render surface), so the WI-243 staleness warn clears — the dashboard has
been judged against its current render, and the judgment's open items are tracked.
