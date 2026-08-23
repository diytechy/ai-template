+++
id = "WI-268"
title = "--dual-plan flag path honors autonomous (pause-free STALL, not NEEDS-HUMAN); widen SR-108 to both dual-plan PAGE entries"
workstream = "unattended"
sr_refs = ["SR-155"]
needs = ["~WI-209"]
buildtier = "strong"
safety_class = "ordinary"
order = 265
+++

## Deliverable

agent_loop --dual-plan PAGE branches on plan_round.page_action: attended keeps NEEDS-HUMAN + EXIT_NEEDS_HUMAN (exit 7); autonomous/single-ratify writes run-state RUNNING + an attention banner and returns EXIT_STALL (exit 4) - the pause-free attention end state the dispatcher's dual-paged route-on reaches (agent_dispatch._terminal_decision). No design-check session spawned (Residual). SR-108/LLR-096/TC-098 widened to cover both dual-plan PAGE entries (LLR-095 multi-site precedent); spine counts unchanged. Regression tests/test_agent_loop_dualplan.py::test_arbiter_disagreement_autonomous_stalls_not_pages (proven to bite pre-fix). Adversarial 113-REVIEW-A APPROVE f=0 (regression-bite + fail-open + run-state-clobber + exit-code-contract hunts survived); check.py --gate G3 RESULT: PASS (1366 passed, cov 91.53%).
