+++
id = "WI-606"
title = "Record codex and opencode token usage, and fix Claude's blank reasoning-tokens and reported-model (review pack C2)"
workstream = "unattended"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

Found by the 2026-09-23 telemetry research; filed by the owner from the
review pack's Part C.

On a successful codex call `run_session` replaces the captured stream with
the `-o` text (`agent_session.py:536-538`, `:617-621`), so every usage field is
blank: 27 of 188 codex logs hold any token line, and none is from a successful
call under the current capture. The opencode route requests no structured
output. For Claude, `reasoning-tokens` reads a field no CLI emits, and
`reported-model` goes blank when a background model appears beside the main
one.

The owner's S8 ruling (sister plan §3.2, 2026-09-24) adds `exec --json` to the
codex route (it works together with `-o`) and `run --format json` to the
opencode route; the OTel GenAI field names land in S7's record step. IN SCOPE:
capture and parse parity on today's recorded fields. NOT IN SCOPE: the OTel
schema itself.

## Done-when

- A successful codex session's log carries its token usage, parsed from
  `exec --json`, while its final text still comes from `-o`.
- An opencode session's log carries its token usage from `run --format json`.
- Claude's `reasoning-tokens` is read from a field the CLI actually emits, or
  removed; `reported-model` names the main model when a background model also
  appears.
- Each route is pinned by a test over a recorded fixture of that CLI's
  output.
