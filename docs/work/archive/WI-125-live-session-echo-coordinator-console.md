+++
id = "WI-125"
title = "Live session echo - coordinator console shows progress during a session"
workstream = "unattended"
needs = ["WI-124"]
order = 124
+++

## Deliverable

Owner-directed 2026-07-13 ('the feedback would be nice to have during a run'): the coordinator console previously printed nothing between the session banner and the outcome line - a 30-minute BUILD was 30 silent minutes. run_session reopened from subprocess.run to Popen + a reader thread (the same pump shape run() uses internally, so the capture/timeout/OSError/WinError-2-resolution contract is unchanged) with each line echoed as it arrives via echo_session_line: stream-json events render compact one-liners (assistant text '  > ...', tool calls '  * <name>'; result/system/user events suppressed - the coordinator prints its own outcome line and tool results re-echo file contents), plain-text CLIs (opencode) pass through, every echoed line truncated to 240 chars; the FULL stream is still captured to the session log + out/run-logs. --no-session-echo silences the console, never the capture. The claude CmdTemplates (agents.csv 3 ANTHROPIC rows + both launcher AGENT_CMD fallbacks) move json -> stream-json --verbose so events exist to stream; the final result event carries the same WI-119/124 telemetry - parse_json_result hardened to PREFER a type:result line so a trailing non-result event (killed stream) never shadows the result. Live-verified against the real CLI before the config switch: sonnet one-liner through build_argv+run_session echoed '  > OK' and parsed type=result/turns/cost. Tests: stream-done fake-agent action (result deliberately NOT last) - echo renders compact + tokens/turns parse from the result event; --no-session-echo silences console but the log keeps the stream. PROCESS_OPTIONS iteration-logs paragraph names the echo.
