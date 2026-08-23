+++
id = "WI-185"
title = "Slice G - recovery + fault injection"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["WI-182", "WI-184"]
buildtier = "strong"
order = 184
+++

## Deliverable

Slice G (2026-07-16): the crash matrix + reconcile hardening. AGENT_FAULT_POINT hook (_fault -> os._exit(86), a REAL crash - no cleanup/atexit) wired at six lifecycle boundaries: reserve-pre-txn / reserve-post-txn / pre-integration-cas / post-integration-cas / post-intent / post-dev-cas (a coverage-guard test asserts every named point stays wired). Reconcile hardening (the two missing spec-11 table rows): (1) already-integrated restore - a train whose WIs are all done on llm/integration restores 'integrated' + finishes the pending reservation release, NEVER re-integrates (proven: one session total, one integration commit, across the post-CAS crash); (2) unprovable-ownership quarantine - a train branch claiming a WI outside its reservation set quarantines that train only (nothing deleted; branch + commit + reservation survive for a human), disjoint proven work proceeds. tests/test_agent_loop_recovery.py (9 fixtures, TC-065): each matrix point crashes a live dispatcher run then relaunches clean and asserts exactly-one-owner / no-double-run (worker session count) / no-false-done / llm/integration atomically before-or-after / the three recoverable publication states via the intent / out/dispatch/ FULLY DELETED still reconstructs from Git alone / stale-lock liveness (kernel locks, existing evidence). SR-064/LLR-065/TC-065 Verified (autonomous single-agent adversarial review).
