+++
id = "WI-080"
title = "Decompose agent_loop.py main() behind test seams"
workstream = "scripts"
needs = ["WI-024"]
buildtier = "strong"
order = 79
+++

## Deliverable

WI-080 (2026-07-16, five slices A-E, behavior-preserving): agent_loop.py main() decomposed from a ~1,657-line god function to orchestration-only (323 lines of wiring). A: golden net first — 8 e2e tests pinning the previously-unpinned loop transitions (swap-implementer applied to the next BUILD, tier-up-never-down after a swap, managed rate-limit/ERROR/no-verdict cool+re-route, model-map parse + missing-{model} preflights). B: session_model/session_template/compose_session_prompt extracted to module level taking explicit state (+ L3 fold-in: parse_model_map -> parse_map; LLR-037 text + arch-map + OKF synced). C: RoutingState — the ~24 mutable locals of the S8 managed-routing/WI-068 critique/stall-guard cluster behind 18 pure transition methods (mutate the object, return decisions; all I/O stays with the caller) + 18 direct unit tests; recorded deviation: complete_round's append/clear stays split in the loop (the worker-rework handler reads round_verdicts between escalation and the clear). D: classify_outcome(outcome ladder) + worker_endstate/worker_exit_banner as module functions + unit matrix. E: run_iteration(ctx,i) composed from route_session (plan-or-exit) + session_bookkeeping (None/exit/reroute), setup extracted (parse_args, map_preflight, build_worker_assignment, track_preamble_text, run_interactive, print_run_banner, LoopContext); the continue-path semantics (skip stall + pause sleep) preserved exactly; recorded deviation: main() is 323 lines vs the spec's ~150 target (uncompressed wiring). Golden net green throughout with zero existing-test edits beyond one mechanical rename; FULL suite at close: 927 passed, 3 skipped. Commits b032ff0/437ba8b/759d7f5/3ff0560/d61e95a.
