+++
id = "WI-068"
title = "Critique verification + subjective-quality critique loop"
workstream = "unattended"
sr_refs = ["SR-154", "SR-157"]
needs = ["WI-059"]
order = 66
+++

## Deliverable

C2 (2026-07-11): Critique joins the Verification vocabulary (trace.py ENUM_FIELDS + registry-hygiene skill + PROCESS.md §4). LLR-exemption decision: a Critique SR is NOT exempt - its artifact is produced by code and only acceptance is subjective, so it keeps its LLR like Demonstration/Manual (a truly code-less subjective requirement is an Attest). New docs/rubrics/ scaffold (README + inert rubric-000; numbered G#/B# anchors derived from SN/SR intent not the possibly-lax TC, accumulating at rework). agent_loop managed mode gains the CRITIQUE run-phase: a committing build whose commit-subject WI (build_scope_srs, joined through work-items.csv) touches a Critique SR schedules a fresh provider-heterogeneous critic (strong tier) with a redacted critique_brief (rubric text + SN/SR intent + TC artifact recipe, never the self-assessment); verdict at docs/reviews/NNN-CRITIQUE.md; BUILD<->CRITIQUE bounded by AGENT_CRITIQUE_MAX (default 3, env) then agent_route.failure_action(gate-policy) pages the human. check_trajectory --staged gains the lax-TC ratchet (a Critique WI closing under a CHANGES-REQUESTED verdict with no TC/tests/docs-rubrics delta warns). PROCESS_OPTIONS 'Critique verification & the critique loop' subsection. Spine +SN-024/SR-047/LLR-048/TC-048 (rides the pending G3 re-attestation). Absent enable-list or any Critique SR = byte-for-byte legacy behavior. Tests: test_agent_loop_critique.py, test_trajectory.py (ratchet), test_trace.py (vocab/exemption).
