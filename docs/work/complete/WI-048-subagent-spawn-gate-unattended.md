+++
id = "WI-048"
title = "Subagent spawn gate (unattended)"
workstream = "unattended"
sr_refs = ["SR-043"]
needs = ["WI-024", "~WI-025"]
order = 47
+++

## Deliverable

ClaudeGuardChecks integration Phase 4 - the one code adoption (commit 73b5bd0; spec docs/archive/INTEGRATION_PLAN.md Phase 4). scripts/subagent_gate.py = a Claude PreToolUse deny-by-default fan-out gate for unattended runs (policy docs/subagent-gate off|ask|deny absent=off; launcher-held SUBAGENT_GATE=allow override; fail-open with a paper trail to docs/subagent-gate.log). Materialized Claude-only via the agent-hooks example; agent-neutral floor untouched. SR-043/LLR-040/TC-043 mechanized by tests/test_subagent_gate.py. Adapted (stdlib) from brefledev/stop-subagent-fanout (MIT).
