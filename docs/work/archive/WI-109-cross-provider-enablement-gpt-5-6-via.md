+++
id = "WI-109"
title = "Cross-provider enablement - GPT-5.6 via opencode + agent-CLI dev tools + routing failure context"
workstream = "unattended"
sr_refs = ["SR-045"]
needs = ["WI-107", "WI-059"]
order = 108
+++

## Deliverable

WI-109 (2026-07-12, owner-directed; the sitting after WI-107). (1) docs/agents.csv +3 OPENAI pair rows - OPENAI-SOL/-TERRA/-LUNA (gpt-5.6-sol/-terra/-luna, Version 5.6; strong/medium/weak - the GA 2026-07-09 GPT-5.6 family, ids verified against the release docs) routed via `opencode run --model openai/{model} {prompt}`; reviews now select CROSS-FAMILY (REVIEW->gpt-5.6-terra after an ANTHROPIC build, CRITIQUE->gpt-5.6-sol; same-family stays the degraded-legal fallback). (2) ANTHROPIC rows pin CLAUDE_CODE_EFFORT_LEVEL=high via Env (owner: high/very-high balance; high = the documented Opus 4.8 default, declared against drift; env-var over flag so older CLIs no-op instead of failing; xhigh dial-up + mechanized selection = WI-110 deferred). (3) docs/agents-enabled -> 6 ids, ANTHROPIC-preferred per tier. (4) Meta scripts/dev-setup.{sh,ps1}: claude + opencode named required dev tools with install+sign-in hints (report-only --check stays exit-0; loop preflight is the hard gate; kit templates untouched). (5) Failure context (kit code): registry Notes = the declared install/sign-in hint home, echoed at the 3 failure points - managed-preflight missing CLI, the previously-SILENT ERROR/TIMEOUT cooldown (now `route: <id> outcome=... (exit N); cooled ~Ns - <notes>`), and the NEEDS-HUMAN no-routable page which renders the whole enabled pool per row (tier/family/cooling/Notes) via new agent_route.pool_context(). No spine change (message surface within SR-045's selection-logging claim; config = the WI-075/107 precedent). PROCESS_OPTIONS routing bullet +1 sentence (Notes-as-failure-context). Verified on the real config: 6/6 resolve, BUILD->opus with effort env merged, reviews cross-family. Tests: test_agent_route (pool_context), test_agent_loop_review (no-routable page + preflight hint), test_onboard_devsetup (CLI rows). Spec: docs/specs/WI-109.md.
