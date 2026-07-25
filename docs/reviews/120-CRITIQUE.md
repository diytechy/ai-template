# 120-CRITIQUE — dashboard accessibility/uniformity/usability (SR-052/053/054), fresh render after WI-294/295/299

**Trigger:** WI-294/295/299 (ring-ink token, shared legend component, Process-tab
type-scale tokens) all touch `gen_trajectory.py`, re-dating the perceptual
evidence past `119-CRITIQUE.md`. Re-judges all three SRs cold against the
current render, one pass.

**Critic:** a fresh Claude Opus subagent (Anthropic family) — a **DEGRADED**
same-family dispatch per SR-084/SR-085's actual contract (preferred, not
required — see wrap-up-plan.md §2 and `agent_route.py:50-53,608-653`). A
genuinely different provider remains the preferred, stronger-corroboration path
and should be reached for again when access allows. Dispatched into an isolated
sandbox holding only the three rubrics, the SN/SR intent brief, and 14 PNGs —
no build transcript, no self-assessment, no repo access. This round's critic
independently decoded the PNGs with a stdlib PNG reader and sampled pixels
directly rather than eyeballing colors — every hex/contrast/geometry claim
below is measured, not estimated.

**Artifact:** `PROJECT_STATE.html` as generated post-WI-294/295/299, 14 renders
— all 5 tabs at 1280px both themes, plus the 390px mobile fold (landing) and
390px full (How-SW) both themes.

**Rubrics:** [dashboard-accessibility.md](../rubrics/dashboard-accessibility.md)
(A1-A4), [dashboard-uniformity.md](../rubrics/dashboard-uniformity.md) (U1-U5),
[dashboard-usability.md](../rubrics/dashboard-usability.md) (T1-T8).

**Corroboration with 119-CRITIQUE.** The A4/T5 descend-affordance contrast
BLOCKER and the U1/U3 legend-styling MINORs from 119-CRITIQUE are gone —
confirms WI-299's per-fill ring ink and WI-294/295's token fixes landed as
intended (this round measures A4 worst pair at 4.98:1, was 1.00:1; T5 clean in
both themes). T1 (no next-work surface) reconfirms 119-CRITIQUE's finding
independently, now filed as **WI-305**. T8's port-fan crossing clusters
reconfirm the pre-existing, already-tracked WI-253 gap the usability rubric's
T8 anchor itself names as a known open finding. **New this round:** U5 residue
the exact-hex-collision check (WI-292/LLR-102) was explicitly scoped NOT to
catch — near-duplicate (not identical) hues reused across the phase/status/type
vocabularies, e.g. three distinct greens (`#4d7c0f` phase-3, `#047857` done,
`#0f766e` Test Case) that still read as one concept at a glance. This is
exactly the perceptual residue LLR-102's own scope note anticipated staying
under SR-053's coarse critique TC.

---

## Anchor verdicts

**A1 — Keyboard reachability:** CANNOT JUDGE from static screenshots — no shot captures a focused control.

**A2 — Accessible names:** PASS (visible evidence) — every control/node carries visible text; no icon-only control in the 14 shots. `<title>`/`aria-label` unverifiable from a raster.

**A3 — No information by colour alone:** PASS (visible evidence) — phase/spine labels are all printed as text; hard vs advisory edges distinguished by solid vs dashed. Caveat: no status-coloured node in this shot set (0 active items).

**A4 — Text contrast:** PASS (measured) — worst pair white-on-slate-500 `#64748b` = 4.81:1; muted body 4.55:1; white-on-lime-700 (phase 3) 4.98:1. All clear 4.5:1 in both themes.

**U1 — One type scale and spacing rhythm:** PASS — node title bands 13-14px, sub-labels 9-13px across all three SVG emitters and the Process cards.

**U2 — One status/phase/type colour vocabulary:** PASS — SN/SR/LLR/TC hexes byte-identical between icicle and Knowledge graph; `done` matches the EXECUTION meter; every hex identical light/dark.

**U3 — Uniform node/edge/legend/detail-panel styling:** PASS — shape, corner radius, port rings, edge stroke, legend row, and detail panel identical across `dag_svg`/`sw_graph`/the OKF graph; the SW "component" unfilled-swatch difference is a declared, meaningful distinction, not drift.

**U4 — One interaction idiom per structure:** PASS (available evidence) — every view declares and offers the identical descend/breadcrumb/detail idiom. Hover/click behavior unverifiable from a static PNG.

**U5 — One concept per colour:** FAIL — the phase palette draws from the same hue families as the type/status palettes; six measured near-duplicate collisions (distinct hexes, same perceived hue), two co-rendered in one viewport.

**T1 — Task findability:** FAIL — "find the project state" and "find how the parts connect" pass; "find the next work" has no one-switch surface (WI-305).

**T2 — Default-density legibility:** PASS — every view opens collapsed (8 phase blocks, 5 component boxes, 6 type blocks) — no wall of nodes.

**T3 — Detail in context:** PASS (available evidence) — persistent detail panel beside every graph. No descended/breadcrumb state was captured to verify the return path.

**T4 — Label legibility:** PASS — no clipped/overlapping text; container-edge clips carry an explicit scroll affordance.

**T5 — Interactive-control legibility, both themes:** PASS for visible controls in both themes (4.55-7.34:1). Focus-ring half unverifiable — no shot captures a focused state.

**T6 — Theme-lock:** PASS — all tabs render fully in the selected theme in both light/dark captures; no mid-view inversion.

**T7 — Viewport fit at declared widths:** PASS — the 390px landing reflows cleanly, nothing clipped past the viewport at the initial view.

**T8 — Edge routing legibility:** FAIL — no through-box edges (verified clean), but crossings cluster inside port fans rather than open space (pre-existing, WI-253-tracked).

## Findings

- [BLOCKER] T8 -> The 8-node top-level roadmap produces 11 crossing clusters landing on port fans: one between the phase-"2" box's two right ports (505, 2523); three at the "unphased" box's right-port fan (1219-1225, 2536-2594); three more in the shared exit lane of the "2"/"2+3"/"4" right ports (510-524, 2602-2723) — `1280px-light-dag-full.png`. A reader cannot attribute which wire leaves which port at those points. (No through-box edges found in any of the three graphs — that half of T8 is clean.) -> Widen the port exit lane and route crossings into open vertical gutters so no crossing falls within ~40px of a port fan. -> @owner
- [MAJOR] U5 -> Six near-duplicate (not identical) hue collisions across vocabularies: `#4d7c0f` (phase 3) / `#047857` (done) / `#0f766e` (Test Case) all read as "green"; `#155e75` (phase 2) vs `#0e7490` (SR); `#7e22ce` (unphased) vs `#7c3aed` (Interface); `#1e40af` (phase 1+2) vs `#2563eb` (module) vs `#4338ca` (Stakeholder Need); `#991b1b` (phase 1+3) vs `#9a3412` (Process Guide); `#94a3b8` (queued) vs `#64748b` (LLR/edge stroke). `done`'s green (the EXECUTION meter, every tab) and Test Case's teal co-render on `1280px-light-know-full.png`. -> Move the phase accents onto a hue family the status/type palettes do not use (a single warm ramp, or one hue at eight lightness steps), reserving green exclusively for `done`. -> @owner
- [MAJOR] T1 -> "Find the next work" has no one-switch surface: the Process tab's resume-loop panel names no WI, and the When tab's status legend advertises "active — you are here" while 0 nodes carry a status colour and the header reads 0 active — reaching a real next WI needs phase -> workstream -> work-item, three nested expands (the anchor's own bad case). -> Add a next-ready-WI surface reachable in one switch (filed as WI-305). -> @owner

## Notes

A2/A3/A4/U1/U2/U3/U4/T2/T3/T4/T5/T6/T7 all hold on available evidence; A1 and
the focus-ring half of T5 are unjudgeable from static screenshots (no focused
state was captured), and A3's status-cue / T3's breadcrumb need a descended
view outside this shot set. One sub-floor observation not rising to a finding:
the `queued` swatch at 2.45:1 against the light page background is below the
3:1 graphical floor but carries a redundant text label, so it fails neither A4
nor T5 as currently used — worth re-checking if `queued` is ever used as a node
fill with white text.

VERDICT: CHANGES-REQUESTED findings=3
