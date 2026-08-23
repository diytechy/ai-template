+++
id = "WI-239"
title = "Completion supersedes a Blocked-WI trailer - a cured blocker must be survivable without discarding finished work (2026-07-19 field finding)"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["~WI-238"]
buildtier = "medium"
safety_class = "high-risk"
order = 236
+++

## Deliverable

latest trailer wins per WI so a newer WI: completion supersedes an older Blocked-WI: (shared agent_common.latest_trailer_evidence folds BOTH the worker-side train_evidence and the dispatcher-side train_branch_evidence into disjoint built/blocked buckets); reconcile gives a reserved blocked train ONE resume per integration-head advance via a durable refs/llm/blocked/<train> record (record/read/clear_blocked + _blocked_recovery_state) rather than short-circuiting to the disposition - keyed on the integration head (not the tip) so a re-block never loops; a resumed worker's first session is no longer short-circuited by its OWN pre-existing block (worker_endstate allow_block_exit) so a green re-run commits WI: and integrates; spec parallel-wi-dispatch.md §9 documents block->cure->supersede->integrate. 5 regressions in test_agent_loop_recovery.py.
