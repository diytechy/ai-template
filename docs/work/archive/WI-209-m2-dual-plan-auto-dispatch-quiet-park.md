+++
id = "WI-209"
title = "M2: dual-plan auto-dispatch + quiet-park auto-page - wire the WI-201 ruling: schedule.classify derives the single-WI-traincar class from PlanMode=dual itself (never a second cell; a contradicting SafetyClass quarantines unclassified); the --jobs build-out auto-runs run_dual_plan_round for a selected dual row (reserve -> round -> SELECT files children / PAGE per plan_round.page_action, pause-free under autonomous); the serial driver pages naming --dual-plan when only dual rows are actionable (no silent park on either path); SR-066 deferral clauses dropped + AC extended with its TC in the same commit"
workstream = "unattended"
sr_refs = ["SR-066"]
needs = ["WI-208"]
buildtier = "strong"
order = 208
+++

## Deliverable

PlanMode=dual auto-dispatch wired end-to-end (the WI-201 ruling): schedule.classify derives single-wi:dual-plan from the PlanMode signal itself (a contradicting declared SafetyClass quarantines unclassified); the --jobs dispatcher auto-runs the round for a dual frontier row as ONE serialized docs-only disposition onto the integration ref (dual_plan_disposition: SELECT closes the parent done + files the children; PAGE commits the evidence and maps plan_round.page_action onto gate-policy, pause-free under autonomous; attended parks NEEDS-HUMAN with the ask); the serial driver pages the --dual-plan ask when only dual rows are dependency-actionable (dual_only_frontier_ask); SR-066/LLR-076/TC-076 amended in the same commit; 6 new tests
