+++
id = "WI-196"
title = "Two-family planner routing with runtime nonresponse fallback - agent_route planner-pair selection + degraded rule at selection AND launch time with recorded reasons (DP-001 selected plan P3)"
workstream = "unattended"
needs = ["WI-190"]
buildtier = "medium"
order = 192
+++

## Deliverable

WI-196 (2026-07-16, opus build / fable integrate): agent_route.py gains planner_pair()/planner_fallback() - pure two-hat selection composing select(), no launching, seams stay IF-044/IF-045 (contract amended). planner_pair: second hat prefers a different Family (PAIR_TWO_FAMILY, not degraded); one-family pool degrades AT SELECTION to two fresh same-family sessions (PAIR_SINGLE_FAMILY); empty pool PAIR_NO_MODEL. planner_fallback (runtime nonresponse after failure_action() retries exhausted) HARD-excludes the dead family - the key catch: select()'s exclude_families only DEPRIORITIZES and would degrade back to the dark family - returning two fresh sessions from the responding family (PAIR_RUNTIME_FALLBACK) or PAIR_NO_RESPONDER. Freshness = object identity (PlannerSession/PlannerPair; reasons as data). 6 new tests (39 total in test_agent_route.py). Spine LLR-072/TC-072 under SR-045 Phase 1 (corrected from the proposed 4 - rows match their SR's phase).
