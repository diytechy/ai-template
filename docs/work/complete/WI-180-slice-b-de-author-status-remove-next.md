+++
id = "WI-180"
title = "Slice B - de-author status + remove next-wi"
workstream = "unattended"
sr_refs = ["SR-148"]
needs = ["WI-179"]
buildtier = "medium"
order = 179
+++

## Deliverable

Slice B (2026-07-16, owner ruled 'full literal B' - docs/log.md): retired docs/next-wi + docs/run-phase and every live dependency. agent_loop drops all next-wi reading (build_tier_pin/batch_advisories/_next_wi_ids/queued_wi/scope_pointer) and the docs/run-phase FILE - the managed review/critique/design-check phase is carried in-process (next_phase local), so the S8 loop still routes WITHIN a run while the persistent file + its cross-session/cross-crash wiring are gone (activity-routing + {phase}-{gate} branch land in Slice D); DEFAULT_PROMPT/docstring/track-preamble/arg-help de-run-phased. check_trajectory retires R-B/R-C/R-D + gate_first_findings + the STATUS_MD/NEXT_WI/WI_TOKEN_RE consts (R-A floor + R-E SpecRef kept); gen_trajectory drops the next-wi Resume-loop projection; check_docs re-frames the status-lint off 'forward-only'. Launchers x4 + templates (work-items/PLAN/tracks-README/review-policy) + session-protocol skill x3 + READMEs + ADOPTING + PROCESS_OPTIONS de-referenced; PROCESS_OPTIONS gains the generated-root-status CONTRACT (integrator-generated, freshness-gated snapshot; the R-B/C/D retirement) - the generator itself is Slice F. Meta docs/next-wi + docs/run-phase deleted; docs/run-state set RUNNING with a forward note. Tests: deleted the build_tier_pin/batch cluster + the two run-phase-file routing tests + 3 gate_first + the R-D test; rewrote guardrails/wi-label/rework/critique-design-check to the in-process model; interfaces IF-041 reworded + arch-map/PROJECT_STATE/okf regenerated. SR-059/LLR-060/TC-060 stay Planned: the generation half (integrator-generated status.md + dispatcher-derived run-state, 'only on the integration branch') lands with Slices D/F and verifies then. Known follow-up: --model-map/--cmd-map legacy per-phase routing is now inert (legacy phase='').
