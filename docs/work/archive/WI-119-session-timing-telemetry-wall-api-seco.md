+++
id = "WI-119"
title = "Session timing telemetry - wall/API seconds + turns in the iteration surface"
workstream = "unattended"
needs = ["WI-024"]
order = 118
+++

## Deliverable

Owner-directed 2026-07-12 (slow-run triage): the per-session time signal existed only inside the JSON transcript (duration_ms / duration_api_ms / num_turns) - invisible in the log header and iteration_index, so a slow run could not be read at a glance. agent_loop.py now measures wall seconds around run_session on the coordinator's own clock (present even for ERROR / non-JSON sessions) and parses api-secs + turns from the CLI JSON result when present; write_session_log's header gains wall-secs / api-secs / turns (read_log_meta line headroom 16->24); regenerate_index gains Wall s / API s / Turns columns (older logs render the em-dash fallback like every optional cell). PROCESS_OPTIONS 'sizing sensor' + iteration-index prose extended to name the new fields. Tests: the fake agent emits duration_api_ms/num_turns; the done-exit test asserts the header keys and index columns. Evidence need: the interrupted 2026-07-12 run read BUILD=2288s(1367s API/108 turns)+1721s(1066s/94) vs reviews ~540s each - derivable only by opening each log's JSON.
