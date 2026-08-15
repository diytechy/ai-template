+++
id = "WI-065"
title = "Active-seam TC citation - reconcile trace Verifies vocabulary"
workstream = "scripts"
sr_refs = ["SR-159"]
needs = ["WI-056"]
safety_class = "spine"
order = 64
+++

## Deliverable

Ruled: the TC's own `Verifies` cell is the ONE home for a seam citation (Verifies=SR-074;IF-009), not a second column. trace.py now joins IF-### tokens against interfaces.csv exactly as it joins SR/LLR ids, so a documented Active-seam citation passes trace --strict AND satisfies check_trajectory's seam-TC warn — the two checks had disagreed about the vocabulary, making the rule unsatisfiable. Two rules keep the widened vocabulary honest: an unresolvable IF token is still 'references unknown', and a TC citing ONLY seam ids is a new orphan finding (a seam citation supplements the spine citation, never replaces it). Guards: tests/test_trace.py::test_seam_citation_satisfies_trace_and_check_trajectory_together (runs BOTH checkers on one scaffold — a single-checker test is what let them disagree), plus test_unknown_seam_id_in_verifies_is_still_an_orphan and test_tc_citing_only_seam_ids_is_an_orphan; all verified to fail against the pre-fix behaviour. Ruled cell documented in PROCESS_OPTIONS.md 'Intra-repo interfaces & the architecture graph' (+561 bytes).
