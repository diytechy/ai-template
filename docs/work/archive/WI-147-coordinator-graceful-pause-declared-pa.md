+++
id = "WI-147"
title = "Coordinator graceful pause - declared pause request wraps to a clean stop"
workstream = "unattended"
needs = ["WI-024", "WI-145"]
order = 146
+++

## Deliverable

agent_loop.py honors docs/pause (pause_reason helper + top-of-loop boundary check, exit 8): launch-time refusal, graceful stop after the in-flight session, delete-to-resume (run-state untouched); per-lane like run-state. PROCESS_OPTIONS unattended section documents it (+650 B, baseline re-stamped 136,099). 4 tests.
