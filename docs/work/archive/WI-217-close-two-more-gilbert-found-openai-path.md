+++
id = "WI-217"
title = "Close two more gilbert-found OpenAI-path gaps - claude stdin + codex output-last-message"
workstream = "unattended"
sr_refs = ["SR-026"]
buildtier = "strong"
order = 214
+++

## Deliverable

WI-217 (2026-07-17): closed two more gilbert-found gaps my WI-215/216 left open (owner chose the broad scope for both). Gap 1 (gilbert 4e9b705): WI-216 routed only codex via stdin, but the round's later briefs (repair ~35k, critic ~70k with the rival plan embedded) exceed even the 32767-char CreateProcess cap, so CLAUDE sessions ALSO died at launch as apparent nonresponse - dropped {prompt} from ALL claude rows (agents.csv + agents.template.csv) so every claude session delivers its prompt via stdin (verified live: claude -p piped a prompt returned PONG). Gap 2 (gilbert 9add15b): codex echoes its banner + the whole prompt into stdout, so plan_coverage.parse_plan read the echoed brief not the plan; WI-215's parse_json_result (claude stream-json) does not catch this - run_session now injects codex's own -o/--output-last-message file for EVERY codex session and reads it back as the deterministic result (_codex_lastmsg_setup/_read; verified -o/--output-last-message exists + a fake-codex integration test proving the transcript is discarded). tests/test_session_stdin.py +5 (codex helpers + read-back). LLR-026 amended; no new SR (robustness under SR-026/SN-016). NOT pure replication of WI-216 - each commit exposed a real gap. Sits on WI-215/216 (same thread).
