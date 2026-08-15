+++
id = "WI-141"
title = "[v3] dev slice: SR-051-rev interface-wired render + descend-a-layer"
workstream = "dashboard"
sr_refs = ["SR-070"]
needs = ["WI-135", "WI-145"]
order = 140
+++

## Deliverable

Two commits (When roadmap + How-SW containment): replaced the tiered views' in-place <details> expand with a shared Simulink-style drill renderer (DRILL_STYLE/DRILL_SCRIPT/_drill_layer_svg/_render_drill in gen_trajectory.py) — each tier is an SVG block diagram with input/output ports, seams/edges wire OUT->IN ports (deduped union aggregated to the container boundary), a container block double-clicks (or Enter/Space on focus) to DESCEND one layer, and a self-contained breadcrumb restores any ancestor. When view: phase->workstream->effort->work-item layers, per-phase accent, <=3/<=3 fallback to the flat SVG DAG byte-identical. How-SW: component/module/external block layers, one layer_edges helper generalizing the WI-073 cross/intra/boundary split; no-CMP vacuity + TOP_VIEW_MAX bound unchanged. Byte-deterministic; --check stable. SR-051/LLR-052/TC-052 Planned->Verified (phase v2 rejoins G3; v3 held at G2 until WI-142..144). Tests: 3 named TC-052 cases + reworked WI-087/WI-073 tiering cases; full suite 728 passed.
