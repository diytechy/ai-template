+++
id = "WI-084"
title = "Reviewer requirement-consistency sweep (Option A)"
workstream = "unattended"
sr_refs = ["SR-045"]
needs = ["WI-059"]
order = 83
+++

## Deliverable

Owner-ruled Option A (2026-07-12): the embedded REVIEWER_PROMPT (agent_loop.py - SR-045's reviewer surface) gains a directed requirement-consistency sweep - when a diff adds/changes SN/SR/TC rows the reviewer cross-checks them against the existing registries (new AND historical rows) for contradiction/overlap/attribute-limit conflict, raising each as a finding (MINOR 'for clarity' where sharper SN/SR/TC language would resolve a wording ambiguity, per the owner's future-clarity goal). Operationalizes PROCESS.md 3's existing 'the reviewer is well-suited to a first-pass contradiction sweep' line within the existing reviewer capability - no new SR, no PROCESS/SR text change, byte-budgeted files untouched. Test: test_agent_loop_review.py::test_reviewer_prompt_carries_requirement_consistency_sweep.
