+++
id = "WI-434"
title = "Replace the When/How overview spaghetti with focused dependency tracing: the 2026-08-12 render matrix reproduces crossing and wraparound wires at 1680/1280px, while 390px scales both diagrams below comfortable reading size. The root cause is not just routing: every aggregated relationship is exposed simultaneously, so even a better layout engine would leave the overview visually dense. Keep the drill hierarchy and offline deterministic artifact, but make one selected node's incoming and outgoing neighbourhood the primary view, distinguish both directions without relying on colour alone, preserve keyboard interaction, and give the reader explicit source/destination labels. Judge the visual result from fresh light/dark desktop/mobile screenshots, not source inspection. Research candidate external engines (ELK/elkjs, Dagre, Cytoscape.js, Graphviz/WASM) and record why the chosen dependency posture fits the shipped install-nothing dashboard."
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Completed 2026-08-12. The shared drill renderer now gives the When and How
overviews a focused dependency mode: one deterministic default card is selected;
incoming prerequisites render blue, outgoing dependents amber, unrelated cards
and routes recede, and the summary names the exact `Needs` and `Unlocks`
endpoints. Hover, click and keyboard focus move the selection; double-click and
Enter keep their existing drill-down meaning. What and Knowledge remain outside
the focused mode even though they reuse the same renderer.

The dashboard remains a deterministic, dependency-free, single-file offline
artifact. Research found ELK/elkjs the best escalation if a future change needs
a full layout-engine replacement because it supports layered layout, ports and
hierarchical nodes and ships a browser-ready bundle. Dagre would leave routing
and drill integration local; Cytoscape.js is a broader interactive viewer than
this read-only surface needs; Graphviz/WASM adds a larger runtime boundary.

Verification:

- The full declared 36-shot width/theme/tab matrix was regenerated and visually
  read at desktop and mobile sizes; the selected source/destination paths are
  traceable in both themes and no longer compete with every background route.
  <!-- fig: cmd="node scripts/dashboard-shots/shoot.mjs" rev=this-worktree -->
- The renderer/view regression set passed: 70 passed.
  <!-- fig: cmd="python -m pytest -q tests/test_traj_render.py tests/test_traj_views.py" rev=this-worktree -->
- A real Playwright interaction check moved the When selection from `1+3` to
  `unphased`, updated the exact relationship summary, and moved the How selection
  from `CMP-005` to `CMP-003`; the What drill carried no focused-trace marker.

No external dependency or dependency-ledger row was added. The prior
`origin/FlowDiagramUpdates` branch was inspected, not merged: it diverges at
`95a3b0d8`, its useful hierarchy/drill ideas are already superseded on trunk,
and its remaining registry/gate changes are obsolete.

## Context

Baseline evidence is the declared `scripts/dashboard-shots/shoot.mjs` matrix
generated from commit `db34b072` on 2026-08-12, especially:

- `scripts/dashboard-shots/shots/1680px-light-dag-full.png`
- `scripts/dashboard-shots/shots/1680px-light-sw-full.png`
- `scripts/dashboard-shots/shots/390px-dark-dag-full.png`
- `scripts/dashboard-shots/shots/390px-dark-sw-full.png`

The prior `origin/FlowDiagramUpdates` branch diverges at `95a3b0d8` and is not a
merge candidate. Its WI-087 hierarchy/drill ideas already entered and were
superseded on trunk; its remaining diff includes obsolete CSV registry and gate
changes.

Candidate engine references:

- ELK: https://eclipse.dev/elk/ — layered layout, explicit ports and hierarchical
  nodes; strongest technical fit if the native renderer is replaced.
- Dagre: https://github.com/dagrejs/dagre — smaller directed-layout library, but
  it would still leave obstacle routing and drill integration here.
- Cytoscape.js: https://js.cytoscape.org/ — capable compound interactive viewer,
  broader and heavier than the dashboard's read-only need.
- Graphviz/WASM: https://hpcc-systems.github.io/hpcc-js-wasm/ — mature static
  layout at the cost of a larger WASM/runtime surface and weaker integration with
  the existing SVG drill interaction.

The implementation should first remove the all-edges-at-once presentation. If
focused tracing still renders poorly, ELK/elkjs is the preferred escalation; a
layout dependency must be vendored or embedded so `PROJECT_STATE.html` remains
fully usable offline and must receive a `docs/dependencies.md` ledger row.
