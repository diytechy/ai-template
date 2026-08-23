+++
id = "WI-087"
title = "Hierarchical phase-aware When & How drill-down views"
workstream = "scripts"
sr_refs = ["SR-070"]
needs = ["WI-073", "WI-074", "WI-117"]
order = 86
+++

## Deliverable

Tiered drill-down views shipped (2026-07-13, phase v2 dev slice 2 of 2; v2 -> G3). gen_trajectory.py gains when_view()/_wi_phases() + shared _campboxes/_wi_row/_wi_table helpers (extracted from the When-view binner, byte-identical): the When roadmap tiers phase -> workstream -> work item, a tier collapsing into native <details> blocks only when its LOCAL group count exceeds 3 (flat at or below - the owner >3 rule, ruling Q4), grouping containers kept as the WI-074 bottom tier (Q1), each WI carrying a per-phase color accent (grouping-primary encoding, Q2), every rendered tier drawing one deduped parent-to-parent edge per crossing pair aggregated from the union of child edges (the FB5 boundary idiom per tier); in-place <details> expand, no zoom nav (Q3). A WI phase is derived from the Phase column of the SRs it delivers (work-items.csv carries none) - a blank cell = the default phase, distinct from unphased (delivers no SR). The How-SW view (sw_containment) starts top components EXPANDED at <=3 and COLLAPSED at >3 (TOP_VIEW_MAX bound unchanged). A registry with <=3 phases AND <=3 workstreams returns None (the flat SVG DAG) byte-identically, so a small project stays flat (the feature is earned by scale); the meta now tiers into 4 workstream blocks (3 phases (default)/unphased/v2, flat). No new seam (gen_trajectory already consumes the SR registry via spine_stats). SR-051 Verified via TC-052 (9 pinned pytest nodes in tests/test_gen_trajectory.py), LLR-052 Implemented; derived gate v2 -> G3 (both v2 SRs Verified; runnable docs/gate G3, per-phase (default)=G3;v2=G3). Spec archived to docs/archive/specs/WI-087.2026-07-13.md.
