+++
id = "WI-113"
title = "Tier rename (weak->quick) + Claude re-lineup (Fable/Opus/Sonnet) + full model re-verification"
workstream = "unattended"
sr_refs = ["SR-154", "SR-155"]
needs = ["WI-109", "WI-112"]
order = 112
+++

## Deliverable

Owner-ruled 2026-07-12: Fable=strong / Opus=medium / Sonnet=quick, and the tier vocabulary renamed strong/medium/QUICK (was weak). KIT (never-breaking): agent_route.TIER_ORDER=(quick,medium,strong) + new normalize_tier() - legacy `weak` reads as `quick` (the Provider->Family precedent) - applied at load_registry, select(), agent_loop.phase_tier and the tier-map preflight; --tier-map help + module docstrings + guardrails prose updated; agents.template.csv example row weak->quick + vocab sentence; PROCESS_OPTIONS guardrails line. META: docs/agents.csv re-lineup (ANTHROPIC-FABLE claude-fable-5/5/strong ADDED and leads; OPUS->medium; SONNET->quick; HAIKU row dropped per the ruled lineup; SOL/TERRA/LUNA strong/medium/quick), agents-enabled reordered (FABLE,SOL,OPUS,TERRA,SONNET,LUNA), launcher twins' fallback maps re-pointed (AGENT_MODEL=claude-fable-5; PLAN/BUILD/DESIGN-CHECK/CRITIQUE=claude-fable-5, REVIEW-A/B=opus), guardrails-policy comment haiku->sonnet/quick. RE-VERIFICATION (both CLIs now installed+authed: claude 2.1.207 on PATH, opencode OpenAI oauth): mechanical - 6/6 rows parse, 6/6 enabled resolve, preflight exe checks ALL PASS, routing PLAN/BUILD->FABLE, REVIEW-A->TERRA (cross-family), REVIEW-B->OPUS (degraded-legal), CRITIQUE->SOL, banner '6 enabled of 6'; LIVE through the loop's own build_argv+parse_env+run_session from a scratchpad cwd - fable(8.0s)/opus(2.2s)/sonnet(2.8s) with CLAUDE_CODE_EFFORT_LEVEL=high merged + sol(2.9s)/terra(2.4s) ALL replied the asked-for 'OK' exit 0; gpt-5.6-luna HANGS today (id valid - present in `opencode models`; 2 attempts 240s/60s, zero output; provider/plan-side, not config) - runtime impact bounded: TIMEOUT->cooldown->re-route, quick tier still routes SONNET; retry later or owner-rule gpt-5.6-luna-fast as an alternate row. Tests: test_weak_is_a_legacy_alias_for_quick (TIER_ORDER, normalize, legacy registry row loads as quick, select('weak') works, phase_tier normalizes); legacy-weak rows in existing tests kept deliberately as alias proofs; 91 routing/loop tests green. No spine text carries the tier vocab (grep-verified) - no re-attestation impact.
