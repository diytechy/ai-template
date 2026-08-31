+++
id = "WI-541"
title = "Verify the retention layer on this box before the dial is turned: windows, compaction ceiling, occupancy, TTLs, replay"
specref = "docs/plans/2026-08-29-adjudicator-session-retention-plan.md#5-sequenced-work-each-a-wi-none-starts-while--exists"
workstream = "process"
sr_refs = []
needs = ["WI-551"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

`needs` re-pointed 2026-08-31: this row waited on `WI-540`, which closed
`partial` (terminal), stranding it — the gap `docs/handoff-2026-08-31.md` §2
names. `WI-551` supersedes `WI-540` and re-lands the retention layer this row
verifies, so the edge follows the successor. (`WI-552` makes this strand
class visible at mint time.)
