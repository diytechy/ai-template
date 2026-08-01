+++
id = "WI-279"
title = "Per-module coverage floors for the security/process boundaries — add a per-module minimum (initially at honest current baselines) so the global 85 floor stops letting well-tested generators subsidize thin coverage in agent_session.py/subagent_gate.py/plan_runner.py; keep the global floor as a backstop"
workstream = "scripts"
needs = ["~WI-105"]
buildtier = "medium"
safety_class = "ordinary"
order = 276
+++

## Deliverable

Integrated from train p0-g3-WI-279-b5fa @ f23385b: WI-279: fix REVIEW-A — run-scope the coverage report + reject a corrupt one
