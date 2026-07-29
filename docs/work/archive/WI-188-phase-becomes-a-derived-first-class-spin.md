+++
id = "WI-188"
title = "Phase becomes a derived first-class spine property; retire the grouping concept"
workstream = "self-adoption"
sr_refs = ["SR-003", "SR-049"]
needs = ["~WI-141"]
buildtier = "strong"
order = 187
+++

## Deliverable

Made phase first-class and DERIVED, retiring the old per-WI grouping vocabulary (external plan splendid-hopping-pike). Slice 1: Phase back-filled onto SR (blank->1, v2/3/4->2/3/4) + LLR (parent-SR phase) + TC (max-verified) + their templates + EXAMPLE.md; both in_phase filters keep the foundation (min) phase always in scope (fixed the gen_release_checklist second-script bug); derive_gate gained phase_num() + the derived current phase (max ratified) on the basis line + --print (phase=4); PROCESS.md/PROCESS_OPTIONS 'Phased delivery' updated + the 6 [vN]-[g*] WI titles renumbered to [N]. Slice 2: trace.phase_ratified_findings joins --strict-schema (a ratified non-Draft SR/LLR/TC whose Phase does not digit-parse is a finding, vacuous-until-armed, a downstream vN passes); LLR-003/050 + TC-003/050 detail extended; predicate + integration tests. Slice 3: the grouping column dropped from work-items.csv + template; the check_trajectory field removed; gen_trajectory retired the grouping-binned When view and collapsed when_view to phase>workstream>work-item (Process Panel 3 = slices>phase>gates); spine text SR-050/051/055/063 + LLR-051 + TC-051 re-attested; the 6 agent_loop + schedule/trajectory/gen_trajectory fixtures updated. Slice 4: the retired word scrubbed from all live prose (PROCESS_OPTIONS 'Phase cadence' renamed from the old grouping-ruling section, session-protocol x3, CLAUDE/README/launchers/status/open-items/rubrics/specs) + ADOPTING sec 6 migration note; docs/repo-review-2026-07-12b.md preserved as history (a review verdict). Byte deltas: PROCESS.md 60169, PROCESS_OPTIONS.md 151921, baselines re-stamped. Close: full suite + check.py --gate G3 PASS; acceptance grep-zero over the live set.
