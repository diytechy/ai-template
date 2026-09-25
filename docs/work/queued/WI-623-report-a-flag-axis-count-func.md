+++
id = "WI-623"
title = "Report a flag-axis count: functions taking two or more boolean parameters, and bool-literal call sites (S14)"
workstream = "scripts"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#41-minimizing-the-number-of-expressed-operations-note-3"
buildtier = "quick"
priority = 3
safety_class = "ordinary"
+++

## Context

Ruled by the owner 2026-09-24 (sister plan S14, §4.1): pursued, re-scoped
from cycles to structure. The aim is less complexity and right-sized modules,
with mutually exclusive boolean flags packed into enum states.

The flag-axis count is the part built now: stdlib `ast`, warn-only, a reported
burn-down number beside the size and complexity caps, like
`check_dupes_census.py`, and never a gate. It also counters the gaming move of
fusing unrelated functions behind a mode flag, which would lower a duplicate
count. Duplicated-stage detection is a separate research item.

## Done-when

- A stdlib check reports, per module, the functions taking two or more boolean
  parameters and the call sites passing boolean literals, with totals.
- It never fails a gate, even under `--strict`; its baseline sits beside the
  census's, downward-only by convention.
- Tests pin a two-flag function, a one-flag function (not counted) and a
  boolean-literal call site.
