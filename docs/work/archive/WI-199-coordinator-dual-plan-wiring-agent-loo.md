+++
id = "WI-199"
title = "Coordinator dual-plan wiring - agent_loop recognizes the declared trigger via the schedule frontier and runs the full round unattended through the existing session path (DP-001 selected plan P6)"
workstream = "unattended"
needs = ["WI-194", "WI-195", "WI-196", "WI-197", "WI-198"]
buildtier = "strong"
order = 195
+++

## Deliverable

WI-199 (2026-07-17, fable): agent_loop runs the dual-plan round unattended. TRIGGER: a WI row's PlanMode=dual cell (declared at filing, never by flag); the worker --wi path REFUSES a dual row fail-closed (never a direct BUILD, pointing at the entry), and `agent_loop --dual-plan WI-x` is the round's early path. RUNNER (run_dual_plan_round): drives plan_round through the existing build_argv/run_session machinery (every hat inherits S8 per-session limits) - planner x2 routed via agent_route.planner_pair when routing is opted in (one planner_fallback on runtime nonresponse, then page; ambient template both hats = the recorded routing-off degraded mode), coverage via plan_coverage_step (clean report to briefs, raw FAIL lines - a new stdout key on its result - to the one mechanical-repair bounce), cross-critique by the OTHER hat's route, one revision each, arbiter x2 with swapped anonymized labels de-anonymized before recording (the agreement rule compares TRUE plans), artifacts + selected-row filing via plan_artifacts (queued WIs hanging off the parent), PAGE mapped per gate-policy (attended writes NEEDS-HUMAN run-state + stop banner). 5 end-to-end fixture tests (SLOW_MODULES class) incl. the position-biased-arbiter PAGE and the real check_trajectory pass. RESIDUALS RECORDED: repo-cwd sessions (brief-allowlist redaction; empty-cwd is stronger) + --jobs auto-dispatch = WI-201's ruling. Spine LLR-076/TC-076 under SR-061 (provisional); PROCESS_OPTIONS layer tail updated (+ budget re-stamp); IF-059/060 notes de-staled.
