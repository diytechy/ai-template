# 080-CRITIQUE — dashboard render, post-WI-255/256 (edge-router hardening + desktop clip affordances)

**Trigger:** the WI-243 perceptual re-fire — the render surface changed at
commits `3e0fc24` (WI-255, edge-router hardening: full-polyline obstacle
re-verify + detoured edge-label anchoring) and `cd444aa` (WI-256, desktop clip
affordances + wire-terminal port snap), both delivering SR-052/SR-053/SR-054.
079-CRITIQUE ruled APPROVE f=0 but tracked the desktop icicle clip, the silent
wide-drill clip at 1280, and steep wires ending on block edges — the surfaces
WI-256 was filed to fix. This fresh session re-judges the full `T1…T8` anchor
set ([dashboard-usability.md](../rubrics/dashboard-usability.md)) and re-dates
the perceptual evidence past the cd444aa render change.

**Artifact:** `node scripts/dashboard-shots/shoot.mjs` on commit `cd444aa` —
the full declared matrix (36 PNGs: 390/1280/1680 × light/dark × 5 tabs, full +
landing folds; the render's as-of stamp reads `4a0d6db`, the last spine-input
commit at generation — `gen_trajectory` reported already-up-to-date).
Judged shots read directly: `1280px-light-arch-full`, `1680px-dark-arch-full`,
`1280px-light-dag-full`, `1680px-dark-know-full`, `1280px-dark-sw-full`,
`1280px-light-process-full`, `390px-light-arch-full`, `390px-light-arch-fold` —
plus magnified crops of every wire hotspot (When-DAG and How-SW halves at 4×,
both themes; the two steep-terminal corners at 6×, cross-checked against the
emitted SVG path coordinates), and (following 079's precedent for the drill
views the declared matrix does not cover) four supplementary drill captures
taken with the same pinned Playwright at 1280 via focus+Enter descent:
When›unphased (light + dark), How›CMP-004 (light + dark). The declared matrix
in `shoot.mjs` was not modified.

## Anchor verdicts

- **T1 (task findability) — PASS.** Done as a first-time reviewer: project
  state = 1 tab switch (When, or Process's gate panel "Current gate: G3");
  next work = 1 tab switch (Process resume-loop; the landing header already
  shows 241/254 · 0 active); how the parts connect = 1 tab switch (How-SW).
  All entry points are labelled tabs.
- **T2 (default density) — PASS.** When opens as the tiered roadmap (8 phase
  blocks); Knowledge opens start-collapsed at 6 OKF type blocks; How-SW opens
  at 5 components; descent is opt-in per the `>3` rule.
- **T3 (detail in context) — PASS** (re-verified interactively: focus+Enter
  descent into When›unphased returns the `Roadmap › unphased` breadcrumb plus
  the PHASE detail panel; How›CMP-004 returns `Architecture › CMP-004` plus
  the COMPONENT panel, in both themes).
- **T4 (label legibility) — PASS.** No colliding or clipped-without-affordance
  labels in any judged shot; long names truncate with an ellipsis and the
  documented click-to-read affordance (drill module names, icicle SN cells).
  No floating detoured edge label found anywhere (the WI-255 anchoring fix has
  nothing left to show against — this repo's sw view is containerized, so the
  `sw_graph` fallback emitter never renders here). WI-246 (How-SW truncation
  polish) remains valid as filed.
- **T5 (control contrast, both themes) — PASS.** Tabs + active accent,
  legends, breadcrumbs, scroll cues, and detail-panel text clear their
  backgrounds in light and dark across all judged tabs and both drill themes.
  Tracked: the phase-accent legend's neighbouring hues still sit close
  (WI-247, already filed); blocks carry text labels so nothing relies on hue
  alone.
- **T6 (theme-lock) — PASS.** No mid-view inversion anywhere, including both
  drill layers under dark; every panel follows the page theme.
- **T7 (viewport fit) — PASS.** 390px landing is a clean single-column stack
  with no page-level horizontal scroll (the header band bisecting the `-full`
  shots confirmed against `-fold` as the documented fullPage sticky-header
  artifact). The 079 tracked imperfection is resolved into a cued overflow:
  the "↔ Scroll sideways to see the full view" cue now renders at **desktop**
  wherever content overflows its card — the What-icicle at 1280 and 1680 in
  both themes, and both wide drill layers at 1280 — while the How-SW top view,
  which fits, correctly shows **no** cue (the overflow-measuring toggle is
  per-view, judged from what actually rendered in the shots). The TC lane
  (icicle) and the drill layers' rightmost columns still sit past the card
  edge until scrolled, but the overflow is now announced.
- **T8 (edge routing) — PASS.** Re-verified in pixels after the router change,
  in magnified crops cross-checked against the emitted path coordinates:
  - *When DAG (both themes):* long-range wires travel the two horizontal
    corridor lanes above/below the middle row; the mechanized floor holds —
    no wire enters any **unrelated** block anywhere. Crossings sit in open
    space: the fan-out at phase-`2`'s port crosses only same-source wires;
    the 4-out ascent crosses the unphased→4 diagonal mid-corridor, beside
    (not under) 2+3's out-port; the lane-descents into unphased's in-port
    converge on the port circle without crossing under it.
  - *Wire terminals (the WI-256 snap):* delivered — **every** roadmap and
    How-SW wire now starts and ends exactly on a port circle (all emitted
    path endpoints are port coordinates; the 6× corner crops show the
    approach stubs arrowing into the ports). The 079 finding "steep wires
    terminate on a block edge" is gone as a terminal defect; what remains is
    a routing idiom (below).
  - *How-SW (both themes):* the CMP-001→CMP-002 return lane runs the open
    corridor and wraps to CMP-002's in-port; CMP-002's drop crosses it
    mid-corridor (the 079-accepted crossing); the in-port fan converges with
    one crossing (CMP-001→CMP-004 over CMP-004→CMP-001) in the open gap left
    of CMP-001's in-port — near the fan but not under the port circle or any
    label, and every wire stays traceable to its source.
  - *Knowledge (collapsed):* the SR→TC spine wire visibly detours **under**
    the LLR block, not through it.
  - *Drill views (When›unphased, How›CMP-004, both themes):* wires thread
    the corridors between columns (dashboard→Docs runs beneath the tooling
    box, not through it); crossings land between blocks.

## The WI-255 / WI-256 surfaces, in pixels

- **WI-256 desktop icicle clip → delivered.** The scroll cue renders above the
  icicle card at 1280 light and 1680 dark (and at 390 as before); the clipped
  TC lane is now discoverable and reachable. Still tracked as polish: the cue
  is a static caption above the card — there is no edge-of-card gradient or
  shadow marking *where* the clip happens, so the TC lane header remains
  invisible until the reader actually scrolls.
- **WI-256 wide drill layers → delivered.** Both When›unphased and
  How›CMP-004 at 1280 show the cue; the "Docs / process…" block and the
  rightmost CMP-004 column still cut at the card edge but are announced.
- **WI-256 steep-wire port snap → delivered** (terminals verified at port
  coordinates in SVG and pixels).
- **WI-255 full-polyline re-verify → nothing contradicts it in pixels:** no
  through-unrelated-box wire exists in any judged panel, top views or drills,
  either theme. The label-anchoring half is unobservable in this repo (no
  `sw_graph` fallback render, no edge labels emitted) — verified vacuous, not
  verified working.

## Verdict

`VERDICT: APPROVE findings=0` — every anchor passes; the WI-255/256 surfaces
are delivered in pixels in both themes, so this critique re-dates the
perceptual evidence past the cd444aa render change (the WI-243 staleness
re-fire clears). Tracked-but-passing imperfections the orchestrator may want
as follow-up WIs: (1) **backward edges hide under their own endpoint boxes** —
the designed keep-the-direct-cubic idiom lets a wire whose only obstacles are
its *own* endpoints dive beneath them (When: 1→unphased, unphased→3,
unphased→2, unphased→4; How-SW: CMP-001→CMP-004), so the reader sees a wire
sprout from unphased's bottom edge, cross CMP-004's right edge beside the
collapse dash, or surface only as a gap segment + port stub — the T8 letter
holds (no *unrelated* box, terminals on ports) but the unphased→3 and
1→unphased runs are effectively untraceable end-to-end and read as a doubled
line between 3/unphased/1; worth a WI to lane-route backward edges instead;
(2) the in-port-fan crossing in How-SW's narrow gap (open space, but the
busiest region of the view); (3) the cue-without-edge-marker polish from the
WI-256 section above; (4) the already-filed WI-246 (How-SW truncation) and
WI-247 (phase-accent hue separation) remain valid; (5) minor: the keyboard
descent capture shows the `tooling` block carrying an orange outline while
the header reports 0 active — presumably the focus ring, but it matches the
"active — you are here" legend colour closely enough to misread; worth a
one-line source check.
