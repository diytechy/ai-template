# 112-CRITIQUE — dashboard render, post-WI-257/258/267 (edge-router round 3 + clip-edge mask + retired bucket)

**Trigger:** the WI-243 perceptual re-fire — the render surface changed under the
repo-review-2026-07-21 backlog: **WI-257** (edge-router round 3: backward edges
now lane-routed instead of keep-direct-cubic), **WI-258** (clip-edge mask fade at
the point of cut + drill focus-ring recolor to indigo `--accent`), and **WI-267**
(a terminal `retired` work-item status with its own dashboard bucket + legend
entry). 080-CRITIQUE ruled APPROVE f=0 but tracked (1) backward edges hiding
under their own endpoint boxes, (2) the clip announced only by a caption cue with
no edge-of-card marker, and (3) a keyboard focus ring that near-matched the
active-accent orange — the exact surfaces WI-257/258 were filed to fix. This
fresh session re-judges the full `T1…T8` anchor set
([dashboard-usability.md](../rubrics/dashboard-usability.md)) cold and re-dates
the perceptual evidence past those render changes.

**Artifact:** `node scripts/dashboard-shots/shoot.mjs` on committed HEAD `2bd8fc9`
(the fully-integrated backlog; the recipe regenerates first, so the render's
as-of stamp reads `54c4117` — the last spine-input commit at generation, the
WI-267 close; the committed HTML is byte-identical bar that one stamp line, which
lags one commit by the known pre-commit-generation behavior 080 also noted). The
full declared matrix (36 PNGs: 390/1280/1680 × light/dark × 5 tabs, full +
landing folds) read directly, plus — following 080's precedent for the drill
views the matrix omits — supplementary captures at `deviceScaleFactor:3`: the
When-DAG and How-SW top graphs magnified (both themes), the drill descents
When›unphased and How›CMP-004 (focus+Enter, both themes), and a focus-ring
capture with the accent stroke read back from computed style. Wire hotspots were
cross-checked against the emitted `--accent`/`--active`/`--retired` values and the
drill focus CSS in `PROJECT_STATE.html`.

## Anchor verdicts

- **T1 (task findability) — PASS.** As a first-time reviewer: project state = 1
  tab switch (When roadmap, or Process's "Current gate: G3" panel); next work = 1
  tab switch (Process resume-loop; the landing header already reads 254/265 · 0
  active); how the parts connect = 1 tab switch (How-SW). All three entry points
  are labelled tabs.
- **T2 (default density) — PASS.** When opens as the tiered roadmap (8 phase
  blocks), not exploded into 265 work items; Knowledge opens start-collapsed at 6
  OKF type blocks; How-SW opens at 5 components. Descent is opt-in per the SR-089
  `>3` rule.
- **T3 (detail in context) — PASS.** Verified interactively in both themes:
  focus+Enter into When›unphased returns the `Roadmap › unphased` breadcrumb over
  the workstream layer; How›CMP-004 returns `Architecture › CMP-004` over its
  file/module members. Context is preserved; the breadcrumb returns.
- **T4 (label legibility) — PASS.** No colliding or clipped-without-affordance
  labels in any judged shot. Long drill names truncate with an explicit ellipsis
  and the documented click-to-read affordance; icicle SN cells and phase labels
  read cleanly at default zoom. WI-246 (How-SW truncation polish) remains valid as
  filed.
- **T5 (control contrast + focus ring, both themes) — PASS.** The WI-258 recolor
  is delivered and confirmed at the computed level: a focused roadmap block's
  `rect` stroke computes to `rgb(129,140,248)` = `#818cf8` = `--accent` at `2.5px`
  in dark (and `--accent` = `#4f46e5` in light), via `.drill .block:focus
  rect{stroke:var(--accent)}` (the roadmap is itself a `.drill` container, so the
  rule applies at every layer). That indigo is a clearly different hue from the
  "active — you are here" accent `--active` = `#b45309` (burnt amber) — the
  near-match orange 080 flagged is gone. Tabs, active-tab underline, legends,
  breadcrumbs, and scroll cues clear their backgrounds in both themes.
- **T6 (theme-lock) — PASS.** No mid-view inversion anywhere. Every light shot is
  uniformly light and every dark shot uniformly dark, including both drill layers,
  the Process hoops, and the Knowledge graph.
- **T7 (viewport fit + clip marker) — PASS.** 390px landing is a clean
  single-column stack: the nav reflows to a vertical button list, the stat tiles
  wrap to a 3-up grid, and there is **no page-level horizontal scroll** (the
  icicle scrolls inside its own card; the mid-page header band in the `-full` shot
  is the documented `fullPage` sticky-header artifact, confirmed against
  `390px-light-arch-fold`). The WI-258 clip marker is delivered: at 1280 light and
  1680 dark the What-icicle's rightmost (green TC) column **fades to transparent at
  the card's right edge** — the `.clipr` alpha mask (`linear-gradient(to left,
  transparent, #000 2.2rem)`) toggled by the same actual-overflow measure that
  drives the `↔ Scroll sideways` caption — so the cut is marked *where it happens*.
  The fitting case holds the contrast: the How-SW top view shows **neither** cue
  **nor** edge fade in either theme.
- **T8 (edge routing) — PASS.** Re-verified in magnified pixels against the
  emitted geometry; the mechanized floor holds everywhere — **no wire enters any
  unrelated node box** in any top view or drill, either theme — and the WI-257
  backward-edge fix is delivered:
  - *When DAG (both themes):* long-range and backward edges travel two full-width
    horizontal corridor lanes in the gaps just above and below the middle row. The
    080-tracked backward runs (1→unphased, unphased→2/3/4) are now **lane-routed
    and traceable end-to-end** — a wire from phase `1` drops to the lower corridor
    and travels left, wrapping the *outside* of box 1's ports rather than diving
    beneath its own endpoint box. The old "doubled line between 3/unphased/1"
    reading is gone.
  - *How-SW (both themes):* the CMP-001→CMP-004 and CMP-001→CMP-002 backward edges
    are lane-routed through an upper corridor (between CMP-002/CMP-003) and a lower
    corridor (between CMP-004/CMP-005), wrapping CMP-001's right port on the
    outside and returning to the left column's in-ports — traceable the whole way.
    The forward fan-in converges in the open gap left of CMP-001's in-port, under
    no box or label.
  - *Knowledge (collapsed):* the SR→TC spine link visibly detours **below** the
    LLR block, not through it.
  - *Drill views (When›unphased, How›CMP-004, both themes):* wires thread the
    inter-column gaps and horizontal lanes; crossings land between blocks, never
    inside one.

## The WI-257 / WI-258 / WI-267 surfaces, in pixels

- **WI-257 backward-edge lane routing → delivered.** Both the When-DAG and How-SW
  backward edges now ride dedicated corridor lanes in the row gaps and wrap box
  endpoints on the outside; the 080 finding "backward edges hide under their own
  endpoint boxes" is resolved in pixels in both themes. Multiple wires share a
  corridor but remain individually traceable at magnification.
- **WI-258 clip-edge mask → delivered.** The right (clip) edge of an overflowing
  scroll card fades via the `.clipr` mask at the point of cut, cleared once
  scrolled to the end — visible on the What-icicle at 1280/1680, absent on the
  fitting How-SW top view. The 080 "cue-without-edge-marker" polish item is closed.
- **WI-258 focus-ring recolor → delivered.** Drill focus ring is `--accent` indigo
  (`#4f46e5`/`#818cf8`, 2.5px), decoupled from the amber active accent; 080's
  "focus ring matches the active colour closely enough to misread" is resolved.
- **WI-267 retired bucket → present and coherent.** `--retired:#78716c` (stone) is
  defined and the status legend renders `retired — won't build (terminal)` as a
  plain stone swatch consistent with the done/active/queued entries; the dashboard
  sub-line correctly suppresses the retired clause at count 0 ("254 of 265 work
  items done · 0 active"). Honest caveat, verified vacuous not verified working:
  the `⊗` glyph WI-267 defines for `retired` (`STATUS_GLYPH`) is a drill
  work-item **node-label** glyph, not a legend glyph — with 0 retired items it
  renders nowhere, so a viewer cannot see the `⊗`↔retired pairing from this render
  (the stone legend swatch alone stands in).

## Verdict

Every anchor passes; the WI-257/258/267 surfaces are delivered in pixels in both
themes, and T8's blocking condition (no wire through an unrelated box) holds
across all top views and drills. This critique re-dates the perceptual evidence
past the edge-router / clip-mask / retired-bucket render changes, so the WI-243
staleness re-fire clears.

Tracked-but-passing observations the orchestrator may want as follow-up WIs (none
block APPROVE): (1) the `retired` `⊗` glyph is node-label-only and thus
unobservable at count 0 — consider surfacing the glyph in the legend swatch so the
pairing is learnable without a live retired node; (2) minor keyboard-flow nit
unrelated to any T-anchor: after a focus+Enter descent the focus drops to `<body>`
rather than being placed on the new layer, so a keyboard user must Tab back into
the re-rendered graph (top-level block focus itself works and shows the indigo
ring); (3) the already-filed WI-246 (How-SW truncation polish) remains valid; (4)
queued (`#94a3b8` slate) and retired (`#78716c` stone) are both muted greys and
sit close in the legend — distinguishable, and blocks carry text labels so nothing
relies on hue alone, but worth awareness.

VERDICT: APPROVE findings=0
