+++
id = "WI-107"
title = "Unattended enablement - routing maps + agents registry + run-phase + guardrails-policy + single-ratify gate authority"
workstream = "unattended"
needs = ["~WI-106"]
order = 106
+++

## Deliverable

WI-107 (2026-07-12, owner-directed; the WI-106 sitting's main event): the meta-repo's walk-away loop wired for a managed, consent-explicit run with one human attest per phase batch. (1) docs/gate-policy attended->single-ratify + the deviation register docs/gate-policy.md (the bootstrap --gate-policy single-ratify shape + a meta-context note; DRAFT until the owner reviews this landing commit = the single attest). (2) docs/agents.csv seeded 3 ANTHROPIC pair rows (ANTHROPIC-OPUS strong / -SONNET medium / -HAIKU weak; CmdTemplate = the launcher's `claude ... --dangerously-skip-permissions`; Env ambient; same Family, so review rounds run the documented degraded-legal same-family mode per agent_route.select). (3) docs/agents-enabled (the 3 ids in preference order) - its PRESENCE turns managed routing ON; absent = byte-for-byte legacy. (4) docs/run-phase=BUILD. (5) docs/guardrails-policy=off with the reason recorded (no vendored docs/guardrails/core.md here - owner-ruled upstream), avoiding the every-run no-core warning; flip to `haiku` once the core is vendored. (6) launcher twins agent-resume.sh/.cmd: AGENT_MODEL_MAP (PLAN/BUILD/DESIGN-CHECK/CRITIQUE=opus, REVIEW-A/B=sonnet) + AGENT_TIER_MAP=BUILD=strong filled + exported (AGENT_CMD_MAP left empty - single-provider). Verified via agent_route on the REAL config: registry parses 3/3 (0 errors), enable-list resolves 3/3 (0 errors), BUILD/PLAN/CRITIQUE->opus(strong), REVIEW-A/B->sonnet(medium, degraded-legal), guardrails off+not-inert, banner reads '3 enabled of 3 registry models'; the only sandbox-gated preflight check (CmdTemplate CLI 'claude' on PATH) passes wherever Claude Code is installed. Config layer only - NO spine change, derived gate stays G3. Gate bar green (check.py --gate G3 --jobs 0); commit bar pytest -n auto + check_docs --stale exit 0. Needs owner: the single-ratify enablement review (single attest), filed in status.md Needs <human>.
