# 042 — CRITIQUE: PROJECT_STATE.html vs SR-052/053/054 rubrics

Independent critique session. I regenerated the artifact myself
(`python project-trajectory/scripts/gen_trajectory.py` → `PROJECT_STATE.html`,
676,685 bytes) and judged the **emitted** HTML/CSS/JS: DOM structure, event
wiring, and programmatically computed WCAG contrast ratios of the actual
text/fill pairs. **Proxy disclosure:** this is a static-markup + computed-color
inspection, not a visual render — anchors that need pixel-level judgment (T4
overlap/clipping at default zoom) are assessed from layout markup only and are
not the basis of any finding below.

Method notes for T1 (tasks done cold): landing tab is "What (SR breakdown)";
project state = 1 tab switch (When roadmap legend "active — you are here", or
Process lifecycle panel); next work = 1 tab switch (Process resume-loop panel /
When active node); how parts connect = 1 tab switch (How (SW architecture)).
T1 satisfied. T2 satisfied for the When/How drill views (layers ship `hidden`,
root-only on open, `>3` tiering present) but not for Knowledge (below). A1/A2
largely sound: tabs are native labelled `<button>`s, every descendable drill
block carries `tabindex` + Enter/Space handler, all 249 knowledge nodes and 194
spine cells are `tabindex="0"` with `<title>` names, edges carry `<title>`s,
focus mirrors hover for highlight+detail where detail exists.

## Findings

- [BLOCKER] U4 (also T3, A1) -> When tab: the detail aside `#dag-detail` promises "Click a work item to read its detail" but the wiring targets `#dag .wi` and the emitted When view contains zero `.wi` nodes (it renders drill `.block` nodes, which have no click handler) — the panel never populates for mouse users, and keyboard users have no path to WI detail at all (the only detail conduit left is the mouse-only `<title>` tooltip); the identical structure (SVG node + `.detail` aside) works click/focus-for-detail in the What and Knowledge tabs -> rewire the drill emitter's blocks (single-click + focus) to `renderDetail(#dag-detail, wiDetails[id], …)`, or emit the `.wi` wiring the JS expects -> @owner
- [BLOCKER] A4 -> SVG label text falls below the rubric's declared 4.5:1 normal-text floor across most node fills: `#fff` on `#059669` done-green = **3.77** (132 blocks, 11px bold ⇒ normal-size), `#fff` on `#0891b2` SR-cyan = **3.68**, `#fff` on `#d97706` amber = **3.19**, `#fff` on `#6366f1` SN-indigo = **4.47**; the `.sub`/`.bsub` sublabels (8.5px at opacity .85/.9) drop further to **2.72–3.95** on five of six fills (passing pairs do exist: `#0f172a` on queued-gray = 6.96, `#fff` on `#7c3aed` = 5.70) -> darken the fills (e.g. done `#059669`→`#047857`-or-darker, cyan/amber similarly) or switch node style to dark text on light tints, and remove the sub-label opacity discount -> @owner
- [MAJOR] A3 -> When/How drill blocks encode WI status by fill hue alone: the visible label is only `WI-nnn` + truncated title (e.g. `WI-067 run capability menu…`); the word "(done)" exists only in the hover-only `<title>` tooltip, and the legend still requires perceiving the color to match node→swatch -> add a redundant visible cue on the block (a ✓/●/○ status glyph or the status word beside the WI id), matching the phase pattern which already pairs its swatch with a text label -> @owner
- [MAJOR] T2 -> Knowledge tab opens as a wall of nodes: one flat SVG (`#knowgraph`) renders all 249 concept nodes at once on tab open, with no start-collapsed grouping — the `>3` rule applied in the When/How drill views is absent here -> group the knowledge graph by concept type (SN/SR/LLR/TC/IF/Guide) into start-collapsed tiers or reuse the drill emitter -> @owner
- [MAJOR] U3 -> the How-SW drill view ships with neither a legend nor a detail panel while its sibling When drill view has both: sw blocks use tier fills `#0891b2`/`#64748b`/`#7c3aed` that are explained nowhere in the How tab (the `tierlegend` exists only in the When panel), and there is no `.detail` aside in `#sw` at all -> emit the tier legend and a `#sw-detail` aside in the sw_graph panel using the shared `.legend`/`.detail` styling -> @owner
- [MAJOR] U2 -> proposed new anchor **U5 — one color, one meaning** (accumulation rule: U2 as written only covers the same concept rendered *differently*; this artifact fails the converse): the same hue carries different meanings across and even within tabs — `#059669` = "done" (When status legend) = phase "v3" (the same When panel's tierlegend) = "Test Case" (Knowledge legend); `#d97706` = "active" = phase "v2+v3" = "Process Guide"; `#0891b2` = "System Requirement" (What) = "unphased" (When) = a sw tier (How) -> give phases their own hue family distinct from the status vocabulary and de-collide the per-tab type palettes; add U5 to docs/rubrics/dashboard-uniformity.md -> @owner
- [MINOR] U1 -> primary node-label type sizes are per-emitter rather than one shared set: knowledge `.knode text` 9px, What `.cell text` 10px, drill `.blab` 11px (subs uniform at 8.5px) — three sizes for the same role (an SVG node's name) across the three emitters -> pick one node-label size (and one sub size) in shared CSS and drop the per-emitter overrides -> @owner

## TC-HARDEN proposals (route via change-intake, process.md §5)

- [TC-HARDEN] A4 is mechanizable: add a TC that parses every emitted `<text>`/effective-fill pair (including opacity-composited sub-labels) from PROJECT_STATE.html and asserts WCAG ratio ≥ 4.5 (≥ 3.0 for ≥18.66px-bold text) — exactly the computation used above.
- [TC-HARDEN] the dead `#dag .wi` wiring was silently vacuous: add a TC asserting every `querySelectorAll` selector in the emitted scripts matches ≥ 1 element in the same document (or that each `.detail` aside has ≥ 1 wired trigger).
- [TC-HARDEN] add a TC asserting every SVG emitter that uses > 1 categorical fill also emits a legend naming each fill in that panel.

VERDICT: CHANGES-REQUESTED findings=7
