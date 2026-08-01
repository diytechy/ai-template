+++
id = "WI-124"
title = "Session-shape telemetry - boot latency + context volume + speed dials per session"
workstream = "unattended"
needs = ["WI-119"]
order = 123
+++

## Deliverable

Owner-directed 2026-07-13 (the 'CLI feels slower than the IDE' question): WI-119 said how long a session took; this says WHY. The log header gains six fields parsed from the CLI JSON / launch env - ttft-secs (boot-to-first-token, the initial context-ingest latency), cache-read + cache-create (context tokens carried per turn / ingested fresh at session start - the 'initial information complexity' signal), effort (CLAUDE_CODE_EFFORT_LEVEL from the launched env - coordinator-known even when the CLI reports no JSON), fast (fast_mode_state - every 2026-07-12 session ran off), prompt-chars (the composed instruction's size). iteration_index gains two DERIVED columns computed at regeneration: s/turn (api-secs/turns - the like-for-like pace number across sessions of different lengths) and Ctx/turn (cache-read/turns humanized - what the totals hide); old logs render em-dash. read_log_meta headroom 24->32. This is the WI-110 un-defer evidence stream (effort/fast dials now measurable per row: dial down effort or try fast-mode on opus and READ the s/turn delta instead of guessing). Historical baseline from the 2026-07-12 run's stored JSON: fable BUILD 12.7 and 11.3 s/turn at ~91k/77k ctx/turn effort=high fast=off; opus reviews 15.5/11.6 s/turn - the CLI's per-turn pace matches interactive; the felt slowness is 100-turn batches + zero streaming output + cold ~190k ingest per session. Tests: fake agent emits ttft_ms/cache/fast fields; done-exit test asserts all six header keys + the derived index columns (8.7 s/turn, 10k ctx/turn from the fixture numbers). PROCESS_OPTIONS sizing-sensor + index prose extended.
