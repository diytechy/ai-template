+++
id = "WI-039"
title = "PROJECT_STATE.html - unified state artifact"
workstream = "scripts"
sr_refs = ["SR-070"]
needs = ["WI-031", "WI-038"]
order = 38
+++

## Deliverable

AXES artifact spec landed (WI-1.52, 2026-07-10): root PROJECT_STATE.html replaces docs/trajectory.html (Q10 default confirmed: replace); What = icicle, When = WI DAG, How-SW = module-map view parsed from architecture.md's generated block (omitted without a symbol inventory), How-physical = CMP table when rows exist (graph render stays deferred-on-need per ratification); git-derived as-of stamp visible on open, excluded from the --check byte-compare (design decision: gating on the stamp would force a follow-up regen commit after every source commit). SR-038/LLR-035/TC-038 extended -> re-attestation pending (R4).
