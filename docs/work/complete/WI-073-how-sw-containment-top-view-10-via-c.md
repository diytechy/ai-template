+++
id = "WI-073"
title = "How-SW containment - top view <=10 via CMP + right-sizing rule"
workstream = "scripts"
sr_refs = ["SR-048"]
needs = ["WI-039", "WI-056"]
order = 72
+++

## Deliverable

FB5 (owner-feedback-2026-07-11, 2026-07-11): the How-SW top view is bounded at 10 items and containerized by component. check_trajectory.py gains component_top_view (the ONE home for the module->CMP join: arch_inventory modules x load_cmps CMP rows x module_components LLR Component tags; _cmp_roots resolves PartOf to top-level roots, cycle-guarded) + component_findings (top-level components that contain a module + uncontained modules > TOP_VIEW_MAX=10 -> WARN plain / ERROR --strict G2+), opt-out docs/components-check (no scaffolded file, absence on - the interfaces-check precedent), vacuous below the bound or with no arch-map inventory. gen_trajectory.sw_containment imports that derivation to render the containerized native-<details> top view (expandable members + nested children + boundary-aggregated cross-component seams deduped to one edge per crossing pair; intra/boundary seams inside the expansion; flat fallback byte-identical when no CMP contains a module); build_html routes software CMPs to How-SW and non-software CMPs to the How-physical table. Meta dogfood: authored docs/requirements/components.csv (5 right-sized software components CMP-001..005) + the Component column/tags on all 48 meta LLR rows -> meta top view 23 modules -> 5 components, 0 uncontained; trace components=5 findings=0, check_trajectory --strict green. Spine +SR-048 (under SN-023/SN-012) + LLR-049 + TC-049; SR-038 minimally clarified (containerized-when-CMP-layer / non-software component table). Regenerated arch-map + okf (230 files) + PROJECT_STATE.html. Rides the pending G3 re-attestation. Tests in test_trajectory.py + test_gen_trajectory.py.
