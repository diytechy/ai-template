+++
id = "WI-116"
title = "[2]-[g1] Dashboard-views requirement structuring"
workstream = "self-adoption"
sr_refs = ["SR-050", "SR-051"]
needs = ["WI-096"]
order = 115
+++

## Deliverable

Phase v2 opened under the derived-gate model - its first live use (2026-07-12). SR-050 (process reference view, WI-085) + SR-051 (tiered drill-down views, WI-087) drafted in the LIVE spine (Status=Draft, Phase=v2, under SN-010;SN-021 - no -000/off-spine workaround) then ratified Draft->Planned by the G1 LLM-gate review in this reviewed Status-change commit (single-ratify: owner batch ratification queued at the [v2]-[g2] close). Verdict: no contradiction with the existing 49 SRs - SR-038 stays the umbrella dashboard SR, these are facet SRs per the owner's explicit new-SR ruling (WI-085 spec); acceptance criteria deterministic/testable. Provisional rulings recorded (log.md 2026-07-12): WI-087's four open questions (Phase>Workstream>WI tiers with grouping kept as the bottom-tier WI-074 container; grouping-primary phase encoding + color accent; in-place details-expand, no zoom nav; >3 governs start-collapsed, TOP_VIEW_MAX=10 unchanged) + WI-085 generated-first render mode (Test TC; Critique only on static fallback, per the owner's recorded ruling). docs/gate derived: runnable G1, per-phase (default)=G3;v2=G1; anchors [v2]-[g1]=WI-116 / [v2]-[g2]=WI-117.
