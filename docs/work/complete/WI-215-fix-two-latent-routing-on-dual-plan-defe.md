+++
id = "WI-215"
title = "Fix two latent routing-ON dual-plan defects found downstream in gilbert"
workstream = "unattended"
sr_refs = ["SR-066"]
buildtier = "medium"
order = 212
+++

## Deliverable

WI-215 (2026-07-17): fixed two latent kit defects in the routing-ON dual-plan path that gilbert (a downstream adopter) hit the first time it ran the round with real --output-format stream-json templates - both flagged latent at kit@42a30bc+HEAD in gilbert's log. (1) _dp_routes and the mid-round planner fallback passed resolve_enabled's (ids, errors) tuple straight into planner_pair/planner_fallback, which iterated it as the pool and crashed (TypeError: unhashable list) before any session launched - the routing-ON dual-plan path had never worked; unpacked both callsites, unresolvable ids now PAGE loudly (the main dispatcher path already unpacked). (2) _dp_session returned the raw json/stream-json event transcript instead of the result text, so plan_coverage's line parser got garbage rows and the {{PLAN}}/{{CRITIQUE}} briefs would have leaked thinking+model-names; now reduces to the result-event text via parse_json_result (plain-text passes through unchanged). Coverage gap: TC-076's fixture ran a plain-text, routing-off fake CLI so neither path fired. Added tests/test_dual_plan_routing.py (6 unit regressions, proven to fail without the fix) on TC-076 Evidence. No new spine (code under LLR-076/SR-066). Ported from gilbert 92acd07 + 4a9faf5.
