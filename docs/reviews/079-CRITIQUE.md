# 079-CRITIQUE — dashboard render, post-WI-253 (T8 re-judged in pixels)

**Trigger:** the WI-243 perceptual re-fire — the render surface changed at
commit `30ed4c9` (WI-253, dashboard edge routing, delivering SR-052/SR-053;
spec [WI-253](../specs/WI-253.md)). 078-CRITIQUE ruled CHANGES-REQUESTED on
**T8** (When-DAG corridor crossings; the How-SW X at CMP-001's port cluster).
This fresh session re-judges the full `T1…T8` anchor set
([dashboard-usability.md](../rubrics/dashboard-usability.md)) and re-dates the
perceptual evidence past the 30ed4c9 render change.

**Artifact:** `node scripts/dashboard-shots/shoot.mjs` on commit `30ed4c9` —
the full declared matrix (36 PNGs: 390/1280/1680 × light/dark × 5 tabs, full +
landing folds; the render's as-of stamp reads `2aa9b10`, the last spine-input
commit at generation — `gen_trajectory` reported already-up-to-date).
Judged shots read directly: `1280px-light-dag-full`, `1280px-dark-dag-full`,
`1280px-light-sw-full`, `1280px-dark-sw-full`, `1680px-dark-know-full`,
`1280px-light-process-full`, `1280px-light-arch-full`, `390px-light-arch-full`,
`390px-light-dag-full`, `390px-light-process-full`, `390px-light-arch-fold` —
plus magnified crops of every wire hotspot, and (because T8 names the drill
views, which the declared matrix does not cover) four supplementary drill
captures taken with the same pinned Playwright at 1280 via focus+Enter descent:
When›unphased (light), How›CMP-004 (light), Knowledge›IF (light + dark). The
declared matrix in `shoot.mjs` was not modified.

## Anchor verdicts

- **T1 (task findability) — PASS.** Done as a first-time reviewer: project
  state = 1 tab switch (When, or Process's gate panel); next work = 1 tab
  switch (Process resume-loop; the landing header already shows 240/252 · 0
  active); how the parts connect = 1 tab switch (How-SW). All entry points are
  labelled tabs.
- **T2 (default density) — PASS.** When opens as the tiered roadmap (8 phase
  blocks); Knowledge opens start-collapsed at 6 OKF type blocks (WI-159
  holding); How-SW opens at 5 components; descent is opt-in per the `>3` rule.
- **T3 (detail in context) — PASS** (re-verified interactively this session,
  not just statically: focus+Enter descent into When›unphased returns the
  `Roadmap › unphased` breadcrumb plus the PHASE detail panel; Knowledge›IF
  shows the "65 Interface concept(s)" context panel).
- **T4 (label legibility) — PASS.** No colliding or clipped-without-affordance
  labels in any judged shot; long names truncate with an ellipsis and the
  documented click-to-read affordance (icicle SN cells, How-SW drill module
  names). WI-246 (How-SW truncation polish) remains valid as filed polish.
- **T5 (control contrast, both themes) — PASS.** Tabs + active accent, legends,
  breadcrumb, and detail-panel text clear their backgrounds in light and dark
  across all judged tabs and the dark drill view. Tracked: the phase-accent
  legend's neighbouring hues (1+2 vs unphased, 2+3 vs 4) sit close — already
  filed as WI-247; blocks carry text labels so nothing relies on hue alone.
- **T6 (theme-lock) — PASS.** No mid-view inversion anywhere, including the
  drill layers under dark; every panel follows the page theme.
- **T7 (viewport fit) — PASS.** 390px landing is a clean single-column stack
  with no page-level horizontal scroll; wide graphs sit in their own scroll
  container with an explicit "↔ Scroll sideways" hint at 390; the header band
  bisecting 390 `-full` shots was confirmed against the `-fold` shots as the
  documented fullPage sticky-header capture artifact. Tracked imperfection
  (passes the anchor's letter — nothing crosses the *viewport* edge at the
  initial above-the-fold view — but worth a WI, see below): the What-icicle's
  fixed 848px SVG clips inside its card at **every** width (measured
  clientWidth 742 vs scrollWidth 867 at both 1280 and 1680; the `TC` lane
  header lands past the visible edge — right 866 vs 844 visible at 1280,
  1066 vs 1044 at 1680), and unlike 390 the desktop widths show **no scroll
  affordance**, so the TC lane reads as unlabeled green bars cut mid-bar.
  The same silent card-edge clip appears in wide drill layers at 1280
  (When›unphased cuts the "Docs / process…" block mid-label with its right
  port invisible; How›CMP-004 cuts its rightmost column).
- **T8 (edge routing) — PASS.** The 078 failures are fixed, confirmed in
  magnified pixels:
  - *When DAG (both themes):* long-range wires now travel two horizontal
    lanes in the open corridors above/below the middle row and bend around
    block `1`'s far side; no wire enters any unrelated block. The remaining
    crossings sit in open space: the fan-out at phase-`2`'s port crosses only
    its own same-source wires; the X above block `4`'s port lies mid-corridor,
    clear of labels; the lane-descent into `1`'s left port converges without
    crossing the `unphased→1` pair under the port.
  - *How-SW (both themes):* the X immediately left of CMP-001's port cluster
    is gone — CMP-002's wire now drops vertically right of CMP-003's box and
    enters CMP-001's port from above, and CMP-003/CMP-004's wires converge
    fan-like without crossing; the single remaining crossing (CMP-002's drop
    over the CMP-001→CMP-002 return lane) is mid-corridor.
  - *Knowledge (collapsed):* the SR→TC spine wire visibly detours **under**
    the LLR block instead of through it.
  - *Drill views (When›unphased, How›CMP-004, Knowledge›IF):* wires thread
    the corridors between columns (dashboard→Docs runs beneath the tooling
    box, not through it); crossings land between blocks; Knowledge type
    layers are unwired columns. Minor, attributable edge-of-idiom: two steep
    wires terminate at a block's top edge near the corner (unphased's left
    edge; block `4`'s top edge) rather than at the port circle — they do not
    pass through any box and their endpoints stay unambiguous.

## Verdict

`VERDICT: APPROVE findings=0` — every anchor passes; the WI-253 lane/detour
routing renders correctly in both themes, at all three widths, and in the
drill layers, so the owner's T8 acceptance is met and this critique re-dates
the perceptual evidence past the 30ed4c9 render change (the WI-243 staleness
re-fire clears). Tracked-but-passing imperfections the orchestrator may want
as follow-up WIs: (1) the desktop icicle clip — TC lane header hidden behind
an affordance-less card scroll edge at 1280/1680 (extends WI-248's 390px
finding; measurements above); (2) the same silent card-edge clip in wide
drill layers at 1280; (3) the already-filed WI-246 (How-SW truncation) and
WI-247 (phase-accent hue separation) remain valid; (4) steep wires ending on
a block edge instead of a port — cosmetic idiom polish only.
