+++
id = "WI-162"
title = "Parallel WI dispatch across coordinator lanes - design spec (actionability scan x overlap guard x lane lifecycle)"
workstream = "unattended"
needs = ["WI-025", "~WI-149"]
buildtier = "strong"
order = 161
+++

## Deliverable

Documentation-only design exploration (no dispatcher code shipped): the initial opt-in --track-lane design in docs/specs/parallel-wi-dispatch.md - deterministic hard-predecessor + lowest-gate actionability scan, conservative off-spine overlap guard, central dispatcher/worktree ownership, per-lane review, serialized gated integration, telemetry projection, five implementation slices. SUPERSEDED by the WI-176 redesign (parallel-by-default dispatcher); the original five-slice plan is retained only as history.
