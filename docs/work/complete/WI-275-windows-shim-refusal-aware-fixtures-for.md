+++
id = "WI-275"
title = "Windows shim-refusal-aware fixtures for the two SR-026 launch tests: test_agent_loop.py::test_cmd_shim_cli_spawns_on_windows + test_session_stdin.py::test_run_session_codex_reads_last_message_not_transcript build .cmd batch shims the H-4 prompt-transport refusal (272a6e8) now correctly rejects - route each fixture through the stdin prompt path (product untouched; WI-120 spawn + WI-217 capture assertions survive verbatim); fronts the queue: the unpushed branch would turn CI's Windows legs red on push"
workstream = "quality"
sr_refs = ["SR-026"]
buildtier = "quick"
priority = 1
safety_class = "ordinary"
order = 272
+++

## Deliverable

Integrated from train 1-g3-WI-275-dfea @ 551c41f: WI-275: route Windows shim launch tests through the stdin prompt path
