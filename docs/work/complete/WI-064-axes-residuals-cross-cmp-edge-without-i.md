+++
id = "WI-064"
title = "AXES residuals: cross-CMP-edge-without-IF check (+ IF tag validation)"
workstream = "scripts"
sr_refs = ["SR-044"]
buildtier = "strong"
order = 63
+++

## Deliverable

WI-064 (2026-07-16, four slices A-D per docs/specs/WI-064.md): the AXES ratified model's enforceability ruling mechanized. A: the meta-repo's architecture.md gains the DEPENDENCY DIAGRAM block the shipped template already carried (imports + dotted IF seams, freshness-gated). B: check_trajectory.cross_component_findings — an import edge between two different CMP-### components with no covering interfaces.csv row is a finding, wired as component_findings' third rule (WARN plain / ERROR under --strict, docs/components-check opt-out, vacuous when any input absent); edge source = the committed MODULE MAP's Imports (internal): lines via the extended arch_inventory (recorded improvement over the spec's diagram-parse). C: IF rows join trace.py's Component-tag membership sweep (the stale off-the-read-set comment predated WI-056). D: the check's first live finding — the sanctioned sibling import gen_trajectory (CMP-002) -> check_trajectory (CMP-001) — declared as IF-056; LLR-067 + TC-067 under SR-044 (Verified); LLR-041/TC-044 text extended; PROCESS_OPTIONS 'Component layer' gains the check contract (+614 B flagged, baseline re-stamped x3). Spine SR=65 LLR=67 TC=67 IF=56. Gated residuals (typed IF contracts, consumes/effort, cyclic renderer, engine extraction, CAD extractor) recorded with applies-when in spec section 2 -> successor row WI-187. 9 new tests; phase-close check.py --gate G3 evidence in log.md.
