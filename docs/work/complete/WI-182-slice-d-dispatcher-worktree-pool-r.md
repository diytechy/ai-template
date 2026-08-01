+++
id = "WI-182"
title = "Slice D - dispatcher + worktree pool + reservations"
workstream = "unattended"
sr_refs = ["SR-061"]
needs = ["WI-179", "WI-181"]
buildtier = "strong"
order = 181
+++

## Deliverable

Slice D (2026-07-16): agent_loop.py --jobs N|auto (AGENT_JOBS env) launches the parallel dispatcher - reconcile -> gate -> build-out. Frontier + classification via schedule.py (sanctioned sibling import; IF-055 seam; unclassified fails closed per WI); pack_traincars clusters ordinary unary hard-chains (cap 4) with spine/gate/attestation/protected never joining a multi-WI car; reserve_traincar = ONE commit-tree metadata commit ({train,wis,base} JSON) + ONE update-ref --stdin zero-old-value transaction creating the train branch + every refs/llm/reservations/WI-### ref all-or-none (bytes stdin - Windows text mode would CRLF-mangle the transaction); worktree pool at ../<repo>-trains/<id> (lease_worktree reuses a recovered checkout); Slice-C workers spawned per train up to the ceiling with rescan-on-every-exit dynamic refill; spine-class trains run whole-project-serial (drain first, nothing beside); reconcile stage parks built trains ready-to-integrate/blocked and resumes incomplete ones from durable reservations (never re-reserving); pause = no new reservations at the boundary; blackout = no new worker; out/dispatch/ journal (events.jsonl + atomic manifest + trains/*.json) is cache never authority; root run-state generated (RUNNING|BLOCKED|DONE|NEEDS-HUMAN). Legacy resume loop untouched without --jobs/AGENT_JOBS (launchers flip at H). tests/test_agent_loop_dispatch.py (10 fixtures incl. rendezvous overlap proof + all-or-none + --jobs 1 peak-concurrency-1). PROCESS_OPTIONS dispatcher contract. SR-061/LLR-062/TC-062 Verified (autonomous single-agent adversarial review).
