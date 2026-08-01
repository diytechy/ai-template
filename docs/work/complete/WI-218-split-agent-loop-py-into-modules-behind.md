+++
id = "WI-218"
title = "Split agent_loop.py into modules behind the declared seams (verbatim-move)"
workstream = "scripts"
needs = ["~WI-080"]
buildtier = "strong"
safety_class = "high-risk"
order = 215
+++

## Deliverable

WI-218 (2026-07-18, slices A-E, behavior-preserving): agent_loop.py split 6,336 -> 2,863 lines into four sibling modules by mechanized VERBATIM AST extraction (normalized-identity checked per slice): agent_session.py (346 - build_argv/run_session/codex capture/console renderers; IF-041 re-homed, IF-064 minted), agent_common.py (927 - exit codes, git wrappers, declared reads+blackout, the kernel lock [held descriptor lives ONLY there], worker-assignment readers, parse_map, preflight, session-log family, run-state write; IF-037 re-homed, IF-065 minted), plan_runner.py (460 - wi_plan_mode/_dp_routes/_dp_session/run_dual_plan_round; IF-058/061 counterparts re-homed, IF-066 minted), agent_dispatch.py (2,125 - reservations/traincars/journal, CAS integrator, migration gate, telemetry, dispatch_run; IF-055 re-homed, IF-067 minted). agent_loop binds every historical name (public surface unchanged; mutable lock internals deliberately NOT re-bound). Two sanctioned non-verbatim edits, both spec'd: spawn_worker's engine path became the explicit _ENGINE sibling (hazard 1: __file__ would have named agent_dispatch) and the WI-068 critique banner stayed with the critique layer rather than riding _SPLIT_RE. Tests re-targeted where they patch moved internals (plan_runner.run_session; agent_loop.agent_common._take_os_lock - the canonical imported instance; the fault-point source grep). LLR-026..030/060/062/064/065/066/076 Modules+CodeSymbols re-homed; scaffold surface synced (bootstrap MAPPING + docstring inventory, kit README rows, test_bootstrap lists). NO compaction (spec: total grew +385 lines for seams). Suite + full G3 gate green at close (totals in log.md).
