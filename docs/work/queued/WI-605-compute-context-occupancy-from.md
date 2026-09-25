+++
id = "WI-605"
title = "Compute context occupancy from the latest request's prompt, not the session's cumulative usage (review pack C1)"
workstream = "unattended"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

Found by the 2026-09-24 telemetry research; filed by the owner from the
review pack's Part C.

`family_context_telemetry` (`agent_loop.py:3253`) sums the stream-json
result's four usage counters (input + cache read + cache creation + output)
and divides by the window. Those counters are cumulative over every model call
in the session, so `docs/iteration_index.md`'s "Ctx %" column shows readings up
to 34,836%. Context occupancy is the latest request's prompt size over the
window. WI-541 verifies occupancy on this machine and reads this value.

The owner's S8 ruling (sister plan §3.2, 2026-09-24) keeps billed tokens and
context occupancy in separate columns; this row fixes the occupancy formula
only. NOT IN SCOPE: the OTel schema (S7's record step), and rewriting
historical logs, which stay as recorded.

## Done-when

- Occupancy is computed from the final model call's prompt tokens (its
  input plus cache read plus cache write), not the result's cumulative
  counters, and the docstring names the source field.
- A test pins it with a recorded multi-call stream where the cumulative and
  last-request values differ.
- No newly written session log reports occupancy above 100%; the fix's log
  fragment names the first session recorded under the corrected meaning.
