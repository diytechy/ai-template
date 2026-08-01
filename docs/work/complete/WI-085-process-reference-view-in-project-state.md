+++
id = "WI-085"
title = "Process reference view in PROJECT_STATE.html"
workstream = "scripts"
sr_refs = ["SR-050"]
needs = ["WI-039", "WI-070", "WI-117"]
order = 84
+++

## Deliverable

Process tab shipped (2026-07-12, phase v2 dev slice 1 of 2). gen_trajectory.py gains process_panel() + _gate_value/_process_doc (the WI-070 Knowledge-tab conditional-panel idiom): (1) artifact lifecycle x gates - live tier counts joined from the spine registries, the current derived gate read from docs/gate and the stages it spans highlighted; (2) the resume loop in the real agent_loop phase vocabulary (PLAN/BUILD/REVIEW-A/B/CRITIQUE-dashed-conditional/INTEGRATE plus the DESIGN-CHECK and page-human escalation edges); (3) slices -> phase -> gates - the commit-bar/gate-bar cadence with live counts joined from work-items.csv. Data-derived where a canonical home exists; links out to the process docs (scaffolded docs/process*.md downstream, the kit masters in this meta-repo); in-view restatement bounded to the relationships no single doc states (the WI-085 anti-duplication ruling). Tab omitted without docs/gate so a gate-less repo renders byte-identically (round-trip proven); byte-deterministic, no new --check exclusion. New seam IF-052 (gen_trajectory Consumes docs/gate, the derive_gate cache contract). Generated-first ruling honored: SR-050 Verified via TC-051 as a Test TC (7 pinned pytest node paths in tests/test_gen_trajectory.py incl. the meta smoke proving every link-out resolves); LLR-051 Implemented; derived gate v2 stays G2 until SR-051 verifies (WI-087 next). Spec archived to docs/archive/specs/WI-085.2026-07-12.md.
