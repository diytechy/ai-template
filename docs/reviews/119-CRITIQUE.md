# 119-CRITIQUE — dashboard accessibility/uniformity/usability (SR-052/053/054), fresh render at `79a29f8`

**Trigger:** correcting the wrap-up plan's family-heterogeneous mandate wording
(this session) touched no render surface, but `gen_trajectory.py` postdates
`118-CRITIQUE.md`, so `check_trajectory --strict` still returns the fail-closed
`perceptual-stale SR-052;SR-053;SR-054` from the last render-surface edit
(WI-296). This re-dates the perceptual evidence past that change and re-judges
all three SRs cold in one pass.

**Critic:** a fresh Claude Opus subagent (Anthropic family) — a **DEGRADED**
same-family dispatch per SR-084/SR-085's actual contract
(`project-trajectory/scripts/agent_route.py:50-53,608-653`): family-heterogeneity
is *preferred, not required*, and "fresh context, never the authoring session"
(SN-024) is the real invariant. No non-Anthropic critic was available this
session; a genuinely different provider remains the preferred, stronger-
corroboration path and should be reached for again when access allows. Dispatched
via the Agent tool into an isolated sandbox holding only the three rubrics, the
SN/SR intent brief, and 14 PNGs — no build transcript, no self-assessment, no
repo access.

**Artifact:** `PROJECT_STATE.html` as generated at HEAD `79a29f8`, 14 renders —
all 5 tabs (Architecture/landing, When, Knowledge, Process, How-SW) at 1280px
both themes, plus the 390px mobile fold (landing) and 390px full (How-SW, for
overflow) both themes.

**Rubrics:** [dashboard-accessibility.md](../rubrics/dashboard-accessibility.md)
(A1-A4), [dashboard-uniformity.md](../rubrics/dashboard-uniformity.md) (U1-U5),
[dashboard-usability.md](../rubrics/dashboard-usability.md) (T1-T8) — all three
SRs judged in one pass since they share a render surface and staleness fires on
all three together.

**Corroboration with prior critiques.** U5 collisions and the A4/T5
`--accent`-on-phase-3 contrast failure reconfirm 117/118's already-filed
WI-292/294/295/299 (all still `queued`, unbuilt) — same hexes, same locations.
**New this round**, not covered by any open WI: the T1 "find the next work" task
has no surface at all; T2 the landing (What) tab opens fully exploded with an
unlabelled TC lane; T7 the How-SW graph and the What icicle both clip/force
sideways scroll at their declared widths; U1/U3 the When tab's phase-accent
legend diverges in size, placement and styling from the other four legends in
the document. A1/A2 were ruled unjudgeable from static screenshots (no focused
state captured; ARIA is invisible in a raster) rather than guessed at.

---

## Anchor verdicts

**A1 — Keyboard reachability:** UNJUDGEABLE from static screenshots — no shot captures a focused state.

**A2 — Accessible names:** UNJUDGEABLE from static screenshots — `<title>`/`aria-label` are invisible in a raster; visible text is present on every tab/legend/node except the 104 unlabelled TC blocks in the What icicle and the icon-only "—" descend glyph.

**A3 — No information by color alone:** PASS — every status/phase/type swatch pairs with visible text; the Process lifecycle highlight adds a border change alongside the hue change.

**A4 — Text contrast:** FAIL — the "—" descend affordance is `#4f46e5` on saturated node fills: 1.00:1 on the phase-3 block (identical color on identical color), 1.04-1.32:1 on every other container node in light theme, against the 3:1 UI-boundary floor. Also the `queued` swatch `#94a3b8` on white is 2.56:1.

**U1 — One type scale and spacing rhythm:** FAIL — the When tab's status-legend labels render at ~10px where all four other legends in the document render at ~13px.

**U2 — One status/phase/type color vocabulary:** PASS — SN/SR/LLR/TC hexes are byte-identical between the legends and the node fills across tabs; phase accents match between the legend and the roadmap nodes.

**U3 — Uniform node/edge/legend/detail-panel styling:** FAIL — the When tab's phase-accent legend uses 18x16px swatches placed inside the graph card with an inline "Phase accent:" prefix, where all four other legends use 26x26px swatches placed below the card with no prefix.

**U4 — One interaction idiom per structure:** PASS — all three wired emitters (roadmap, module graph, knowledge graph) share the identical descend/breadcrumb/detail-panel idiom.

**U5 — One concept per colour:** FAIL — four confirmed cross-vocabulary collisions: `#047857` = `done` and `Test Case`/`TC`; `#b45309` = `active` and `Process Guide`; `#0e7490` = `SR` and `module`; `#7c3aed` = `Interface` and `file (shared-contract hub)`.

**T1 — Task findability:** FAIL — "find the project state" (0-1 switch) and "find how the parts connect" (1 switch) pass; "find the next work" has no path — with 0 active items, nothing marks "you are here," and the only route to a queued item is drilling through nested blocks.

**T2 — Default-density legibility:** FAIL — the landing (What) tab opens fully exploded (~340 icicle blocks) while the three wired tabs correctly start collapsed; the TC lane renders with no labels at all and clips at both the right and bottom card edges.

**T3 — Detail in context:** PASS (caveat: no descended/breadcrumb state was captured in this shot set, so the return path itself is unverified) — every graph tab pairs the diagram with a persistent detail panel.

**T4 — Label legibility:** PASS (caveat: truncated labels end in an explicit "…"; whether a tooltip backs them is unverified from a static capture) — no overlapping or box-overflowing text found.

**T5 — Interactive-control legibility in both themes:** FAIL — same root cause as A4: the descend affordance fails differently per theme (1.00-1.32:1 light, 1.60-2.65:1 dark), never clearing 3:1 in either; tab controls themselves pass in both themes (4.55-7.34:1).

**T6 — Theme-lock:** PASS — dark captures hold `#0b1120`/`#0f172a` page/card colors across every tab; no panel renders on the opposite theme.

**T7 — Viewport fit at declared widths:** FAIL — the How-SW graph is sliced mid-label at 390px forcing sideways scroll; the What icicle's TC lane is clipped at the card's right edge even at the desktop 1280px width.

**T8 — Edge routing legibility:** PASS (caveat: only top-tier collapsed views were captured; the drill views WI-253 also names were not re-tested) — no edge enters the top/bottom of any node box in the When DAG, How-SW, or Knowledge graphs.

## Findings

- [BLOCKER] A4 -> The "—" descend affordance drawn top-right on every collapsed container node is `#4f46e5` painted on the node's own fill: 1.00:1 on the phase-3 block (`1280px-light-dag-full.png`, bbox x606-854 y2497-2590), 1.04-1.32:1 on every other container node in light theme (phase 1/2/4, IF, TC, LLR fills). Also the `queued` swatch `#94a3b8` on white is 2.56:1 (same file, y~2968 x660-686). -> Give the affordance glyph a fill computed against its host node (e.g. white on all six saturated fills >= 4.7:1) instead of a fixed brand indigo, and darken the `queued` swatch to >=3:1 on white. -> @owner
- [BLOCKER] U5 -> Four hues each carry two different meanings across the document: `#047857` = `done` (When status legend) and `Test Case`/`TC` (Knowledge type legend, What legend); `#b45309` = `active` and `Process Guide`; `#0e7490` = `SR` and `module`; `#7c3aed` = `Interface` and `file (shared-contract hub)`. All four pairs are byte-identical. -> Split the palettes so no status colour is reachable from the type/phase palettes; regenerate the legends from the single declared palette so a collision is impossible by construction. -> @owner
- [MAJOR] T1 -> "Find the next work" is not reachable on any tab: with 0 active items nothing is marked "you are here," the Process tab's resume loop is a static method diagram with no data, and the only route to a queued item is When -> double-click a phase -> double-click a workstream -> scan for a queued node. -> Add a next-work surface reachable in one switch — the ready/queued WIs derived from the DAG, named, with their blocking predecessor. -> @owner
- [MAJOR] T2 -> The landing tab opens fully exploded (~340 icicle blocks across four lanes) while the three wired tabs correctly start collapsed. The TC lane renders with no labels at all and dissolves into a right-edge gradient; the card clips the last row mid-block. -> Apply the same `>3` start-collapsed rule to the icicle, or cap the rendered depth so the landing view is a summary. -> @owner
- [MAJOR] T5 -> The descend affordance fails the contrast floor differently per theme: light `#4f46e5` on node fills 1.00-1.32:1; dark `#818cf8` on node fills 1.60-2.65:1 — never clearing 3:1 in either theme, the anchor's stated both-themes bad case. -> Derive the affordance colour per theme *and* per host fill and assert >=3:1 in the generator. -> @owner
- [MAJOR] T7 -> SVG emitters don't reflow at the declared widths: at 390px the How-SW CMP-002 node is sliced by the viewport edge, forcing sideways scroll; at the desktop 1280px width the What icicle's TC lane is clipped at the card's right edge. -> Make the SVG viewBox responsive (scale-to-fit or re-layout under a width threshold) so narrow/wide content reflows; keep the sideways-scroll hint only as fallback. -> @owner
- [MINOR] U1 -> The When tab's status-legend labels render at ~10px type where its own phase-accent legend, and every other legend in the document (Knowledge, How-SW, What), render at ~13px. -> Emit all legend labels from the one shared legend type token. -> @owner
- [MINOR] U3 -> The When tab's phase-accent legend uses 18x16px swatches placed inside the graph card with an inline "Phase accent:" prefix, where every other legend (status legend on the same tab, Knowledge, How-SW, What) uses 26x26px swatches placed below the card with no prefix. -> Render the phase-accent legend through the same legend component as the other four. -> @owner

## Notes

U2/U4/A3/T3/T4/T6/T8 hold; the wired-tab interaction idiom, color vocabulary,
color-independent encoding, and theme-lock are solid. The defects cluster in two
places: the descend-affordance glyph (A4/T5, one root cause, two anchors) and the
When tab's from-scratch phase-accent legend (U1/U3, one root cause not shared
with the other four legends that were built from a common component). T1/T2/T7
are usability gaps not previously filed under any open WI.

VERDICT: CHANGES-REQUESTED findings=8
