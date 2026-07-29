+++
id = "WI-253"
title = "Dashboard edge routing: wires still cross and pass through unrelated node boxes in the When/How/Knowledge/drill diagrams - route wires around node rects with deterministic detours + minimize crossings; acceptance = new rubric anchor T8 (dashboard-usability), which blocks critique APPROVE until the render passes (2026-07-20 owner finding)"
workstream = "dashboard"
sr_refs = ["SR-052", "SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 250
+++

## Deliverable

Obstacle-aware wire router _route_edges single-sourced across all four layered emitters (dag_svg, sw_graph, know_graph, _drill_layer_svg): a wire whose direct cubic clears every non-endpoint box keeps its legacy path byte-for-byte; a blocked wire detours through the clear horizontal lane nearest the endpoint midline, entering ports on short stubs in the inter-column corridor (Liang-Barsky hit test + cubic sampling + nearest-free-band search - deterministic, stdlib-only, new helpers C901<=10, --check byte-stable). 0 through-box wires across every rendered panel, mechanized: meta scans (containerized How-SW / Knowledge / tiered When) + the fallback dag_svg/sw_graph scan with non-vacuity floors. The 078 findings fixed in pixels: When long wires lane around blocks, the How-SW CMP-001 port-cluster X and CMP-003 graze gone, remaining crossings in open space. Opus build 30ed4c9; independent opus 110-REVIEW-A APPROVE f=3 all MINOR (fallback-scan MINOR consumed 5ebc3b0; the 2 render-surface MINORs filed as WI-255 to build with a bundled critique); fresh independent 079-CRITIQUE APPROVE f=0 - T1-T8 all PASS, T8 verified in magnified wire-hotspot crops both themes, perceptual evidence re-dated past the render change (WI-243 gate cleared).
