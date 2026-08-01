+++
id = "WI-110"
title = "Effort-level selection for agent sessions (per-phase/tier; xhigh experiment)"
workstream = "unattended"
needs = ["~WI-109", "WI-145"]
order = 109
+++

## Deliverable

WI-110 (2026-07-14, owner directive intake item 2 'opus implementation → extra high'; supersedes the deferral). STATIC PIN executed: (1) docs/agents.csv ANTHROPIC-OPUS Env high→xhigh - one cell; FABLE/SONNET stay high; parse_env merges it at launch, WI-124 telemetry effort field reads it back so every OPUS BUILD row now logs effort=xhigh. (2) Default question resolved: live claude 2.1.201 ambient effort resolves to `high` with no pin (WI-109's record holds), so xhigh is a genuine dial-up not a no-op; xhigh valid live (owner ~/.claude/settings.json already effortLevel=xhigh; ladder low/medium/high/xhigh/max). (3) Before/after via WI-124 s/turn: BEFORE baseline opus reviews 15.5/11.6 s/turn at high (WI-124 log); AFTER captured automatically on the next OPUS session (effort=xhigh + its s/turn/Ctx/turn) - this WI arms the sensor, does not fabricate an after it did not run. (4) OpenAI answered: opencode 1.17.18 exposes reasoning effort as `opencode run --variant <low|medium|high|max|minimal>` (a CLI flag → CmdTemplate, NOT an Env cell - corrects the intake draft's config-file guess); left UNWIRED - no s/turn telemetry parity to measure an OpenAI dial-up, so it's a follow-up gated on parity not this directive. Per-phase effort map (#2) + computed selection (#3) stay deferred (spec un-defer triggers unchanged). No spine change (config only, WI-075/107/109 precedent); no test change (tests use synthetic registries; test_agent_loop asserts the effort key present regardless of value). PROCESS_OPTIONS untouched (the general Per-phase-effort paragraph already frames the knob; the pin lives in agents.csv Notes + spec). Spec: docs/specs/WI-110.md.
