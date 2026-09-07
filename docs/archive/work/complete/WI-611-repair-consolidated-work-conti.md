+++
id = "WI-611"
title = "Repair consolidated-work continuation and stale primary test evidence"
workstream = "process"
sr_refs = ["SR-144", "SR-156", "SR-157"]
buildtier = "strong"
safety_class = "spine"
+++

## Deliverable

Implemented the reviewed distinction between ordinary terminal continuation and reconsolidation, with protection inherited through typed lineage. Corrected TC-205 Evidence and its stale Full-tier explanation; no Status or snapshot changes. Red/green regressions, current cited tests and the commit/strict checks are recorded in docs/reviews/wi610-prerequisites/. WI-610 retains the full scope and this hard predecessor. Supervised execution without a lane claim; no semantic acceptance, batch-code deletion, coordinator/control window, push or main merge.

## Context

Supervised prerequisite for the owner-authorized combined adjudication in WI-610, while the coordinator and tracked pause remain stopped. The actual intake preflight rejects a normal disposition successor of a terminal consolidated WI as reabsorption. Distinguish an ordinary terminal continuation from reconsolidation using existing typed draft/status data, and retain consolidation protection through existing Supersedes ancestry. Keep live-owner, restructured-source and actual reconsolidation refusals intact. Do not change primary approval/publication verification or weaken scope, absorption or provenance checks.

Repair TC-205's stale trace after the prior primary-publication rewrite: ten cited test functions no longer exist. Replace those Evidence entries with the current primary proof tests, and remove the stale numeric module count from the Full-tier rationale in Method. Retain every other Method obligation and the Full tier. This is source authoring, not acceptance; WI-610 retains its exact 52-row scope and judges the cumulative TC-205 text and actual per-use coverage. Do not duplicate that ownership.

Done when red-then-green continuation/protection regressions, the existing intake/consolidation and actual TC-205 evidence tests, smoke/budget and strict trace/trajectory/docs checks pass; independent review accepts the implementation correction and authoring boundary; all Status/snapshot bytes remain unchanged, no new scope is absorbed, and WI-610 waits for this completed prerequisite. Record the supervised execution honestly without an ordinary claim while paused. No batch-code deletion, coordinator/control window, push or main merge.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-001 [project-trajectory/scripts/trace.py :: main] tests: (see TC-001) — SN->SR->LLR->TC join + orphan set
- LLR-002 [project-trajectory/scripts/trace.py :: integrity_findings/structure_findings/triangle_findings] tests: (see TC-002) — Id + registry-CSV-structure + citation integrity
- LLR-003 [project-trajectory/scripts/trace.py :: placeholder_findings/schema_findings/phase_approved_findings] tests: (see TC-003) — Placeholder + schema checks
- LLR-004 [project-trajectory/scripts/trace_text.py :: ac_advisories] tests: (see TC-004) — Comparative-term advisory
- LLR-005 [project-trajectory/scripts/trace.py :: integrity_findings/module_findings] tests: (see TC-005) — Off-spine integrity + back-links
- LLR-034 [project-trajectory/scripts/check_trajectory.py :: load_wis/validate] tests: (see TC-037) — WI dependency-DAG validation

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-009 scripts/check_trajectory -> scripts/check: exit-code 0 clean · 1 hard error · 2 usage
- IF-021 docs/requirements/ -> scripts/trace;external:downstream adopter: file id-keyed TOML, one file per spine tier; ids are the table keys
