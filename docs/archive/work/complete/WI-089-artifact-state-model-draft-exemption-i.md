+++
id = "WI-089"
title = "Artifact-state model + Draft-exemption in trace"
workstream = "scripts"
needs = ["WI-088"]
order = 88
+++

## Deliverable

Foundation of the derived-gate effort (spec §3/§10.1). trace.py gains a Draft artifact state: is_draft(row) keys on the open-vocab Status value `Draft`, and the orphan pass exempts Draft rows from the CHILD-COMPLETENESS rules only - a Draft SR needs no LLR/TC, a Draft LLR needs no TC - so a requirement lives in the live spine while being drafted requirement-first (retiring the -000/off-spine workaround). Parent-linkage (a Draft SR still links an SN) and every integrity rule still apply; a Draft SR is also skipped by --require-verified (pre-ratification, below G1). Draft rows are surfaced auditable: a metrics-table count, a `## Draft artifacts (decomposition-exempt)` report section listing them, and a `drafts=N` stdout token. Migrated three existing fixtures that used Status=Draft casually to mean an in-progress orphan (ORPHAN_SR->Planned, PHASED_SRS->Implemented) so they still exercise orphan/phase scoping. Runs under today's monolithic gate; no meta-spine row change (spine reconciliation is WI-096). Tests: 4 new in test_trace.py (SR exempt, LLR exempt, --require-verified exempt, SN+integrity still apply).
