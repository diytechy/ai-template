+++
id = "WI-160"
title = "OpenAI provider-CLI swap (opencode -> codex exec) + builder preference Codex Sol"
workstream = "unattended"
needs = ["WI-059"]
order = 159
+++

## Deliverable

Owner directive 2026-07-14b executed in-session (log.md Decisions): the 3 OPENAI rows in docs/agents.csv now ride codex exec --model {model} --dangerously-bypass-approvals-and-sandbox (opencode sometimes unresponsive); Notes carry install (npm i -g @openai/codex) + codex login; AGENT_TIER_MAP=BUILD=strong in both launchers + OPENAI-SOL heads docs/agents-enabled so BUILD draws Sol first. Side effect owner-accepted: PLAN/DESIGN-CHECK strong draws also move to Sol until WI-161; CRITIQUE keeps Fable via heterogeneity. codex not on PATH at execution - cooldown self-heals BUILD onto Fable until the owner installs/authenticates. Supersedes-for-now: WI-121 BUILD-medium relax; WI-110's opencode --variant note (now codex -c model_reasoning_effort). FOLLOW-UP same day (owner question re dev-setup): scripts/dev-setup.{sh,ps1} swapped their stale opencode row/offer to codex (@openai/codex + codex login; test_onboard_devsetup.py pins updated) and a new scripts/dev-setup.cmd Windows double-click shim added (-Check then offered -Install; the WI-051 .command pattern) - the template twin is WI-166.
