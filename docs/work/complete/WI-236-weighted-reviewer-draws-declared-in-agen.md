+++
id = "WI-236"
title = "Weighted reviewer draws declared in agents-enabled annotations (owner-selected shape 2026-07-19; deterministic rotation within tier + heterogeneity rules)"
workstream = "unattended"
buildtier = "medium"
safety_class = "high-risk"
order = 233
+++

## Deliverable

agent_route per-phase draw-weight grammar + deterministic weighted rotation keyed on the per-train session counter (select/_weighted_rotation/_pick + load_enabled_entries/resolved_weights/phase_weights); wired through agent_loop main/route_session; 9 regressions; grammar in PROCESS_OPTIONS routing + docs/agents-enabled
