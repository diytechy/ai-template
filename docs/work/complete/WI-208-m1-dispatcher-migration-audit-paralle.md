+++
id = "WI-208"
title = "M1: dispatcher-migration audit + parallel-default flip - add the SafetyClass column and deliberately classify EVERY open row (queued/active/blocked + deferred, so an un-defer needs no second audit; done rows stay blank history), disposition every open soft edge (confirm advisory or promote to hard), sign docs/archive/history/parallel-ready per parallel-wi-dispatch.md section 14, flip the three launchers to AGENT_JOBS=2 (--jobs 1 stays the escape), and prove one real boot to the dispatcher banner with zero unclassified rows"
workstream = "unattended"
needs = ["WI-204"]
buildtier = "strong"
order = 207
+++

## Deliverable

Added and audited SafetyClass for all 15 then-open rows; confirmed all three open soft edges advisory; signed docs/archive/history/parallel-ready; enabled AGENT_JOBS=2 in all launchers; real paused/no-work dispatcher boots proved ceiling 2, banner, and telemetry.
