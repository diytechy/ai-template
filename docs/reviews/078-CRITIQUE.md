# 078-CRITIQUE — dashboard render, post-WI-249/250 (first judgment under T8)

**Trigger:** the WI-243 perceptual re-fire — `check_trajectory` flagged the
render surface (`gen_trajectory.py`, WI-249/250 flow-diagram work) as newer
than 077-CRITIQUE. This critique re-judges the current render and re-dates the
evidence. First critique scored against the full `T1…T8` anchor set
([dashboard-usability.md](../rubrics/dashboard-usability.md); T8 added
2026-07-20 at the WI-253 filing — the owner's edge-routing acceptance).

**Artifact:** `node scripts/dashboard-shots/shoot.mjs` on commit `e6184cb` —
the full declared matrix (36 PNGs: 390/1280/1680 × light/dark × 6 tabs,
full + fold). Judged shots read directly: `1280px-light-dag-full`,
`1280px-dark-sw-full`, `1680px-dark-know-full`, `390px-light-process-full`,
`390px-light-arch-fold`.

## Anchor verdicts

- **T1 (task findability) — PASS.** Project state (When/Process), next work
  (status/resume panels), and how-the-parts-connect (How-SW) are each one
  labelled tab switch from landing; entry points are labelled tabs.
- **T2 (default density) — PASS.** When opens as the tiered roadmap (8 phase
  blocks, not the exploded item graph); Knowledge opens start-collapsed at 6
  OKF type-blocks (the WI-159 fix holding); How-SW opens at 5 components.
- **T3 (detail in context) — PASS** (static evidence: drill affordances +
  breadcrumb documented on-panel; interactive descent re-verified at 077,
  unchanged since).
- **T4 (label legibility) — PASS.** CMP blocks wrap id/name in full
  (WI-246 holding); phase blocks, OKF type blocks, stat tiles all read at
  default zoom; no clipped or colliding labels in the judged shots.
- **T5 (control contrast, both themes) — PASS.** Active-tab accent + labels
  clear their backgrounds in light and dark; legends readable in both.
- **T6 (theme-lock) — PASS.** No mid-view inversion in any judged shot;
  every panel follows the page theme.
- **T7 (viewport fit) — PASS.** 390px fold shows a clean single-column
  stack, no horizontal overflow; the header band bisecting the 390px `-full`
  process shot was confirmed against the `-fold` shot as the documented
  fullPage sticky-header capture artifact, not a rendering defect.
- **T8 (edge routing) — FAIL.** The owner-reported gap, confirmed in pixels:
  - *When DAG (1280 light):* the wire bundle from the phase-`2` block to
    `3`/`unphased`/`1` crosses the outbound wires of `1+3`/`2+3`/`4`
    repeatedly in the corridor between the columns; several crossings land
    close under block edges and port fans, where source attribution is lost.
  - *How-SW (1280 dark):* CMP-002's and CMP-003's wires to CMP-001 cross in
    an X immediately left of CMP-001's port cluster; CMP-002's lower wire
    passes tight against CMP-003's box corner and reads as touching it.
  Disposition: **already filed as [WI-253](../specs/WI-253.md)** (queued,
  SR-052;SR-053) — obstacle-aware deterministic detours + crossing
  reduction. Per the T8 anchor text, the filed WI is citable but does not
  lift the anchor: APPROVE stays blocked until the render passes.

## Verdict

`VERDICT: CHANGES-REQUESTED findings=1` — the single finding is T8,
disposition WI-253 (filed, queued). All other anchors pass; the WI-249/250
arrowhead/port-fan/hoop work renders correctly in both themes and at 390px.
This critique re-dates the perceptual evidence past the WI-249/250 render
change (the staleness re-fire clears); the T8 gap remains gated by the
anchor + the WI-253 row, which is exactly the tracking the owner directed.
