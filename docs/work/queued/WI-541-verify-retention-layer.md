+++
id = "WI-541"
title = "Verify the retention layer on this box before the dial is turned: windows, compaction ceiling, occupancy, TTLs, replay"
specref = "docs/plans/2026-08-29-adjudicator-session-retention-plan.md#5-sequenced-work-each-a-wi-none-starts-while--exists"
workstream = "process"
sr_refs = []
needs = ["WI-620"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

`needs` re-pointed 2026-08-31: this row waited on `WI-540`, which closed
`partial` (terminal), stranding it — the gap `docs/handoff-2026-08-31.md` §2
names. `WI-551` supersedes `WI-540` and builds the retention layer this row
verifies (as the session service's keep operation, after WI-620), so the edge
follows the successor. (`WI-552` makes this strand
class visible at mint time.)

## Done-when

- The context window each routed family reports on this machine is recorded
  beside the configured fallback, and a mismatch is logged rather than guessed.
- A retained session driven toward the compaction ceiling (the auto-compact
  window set low) is observed and recorded: the kit's reset fires before the
  provider compacts, or the compaction is logged on the session's row.
- Occupancy on a real multi-step, tool-using adjudication is checked against
  the latest request's prompt size, the rule the reset trusts, and any
  disagreement is recorded.
- The codex and opencode cache TTLs and the resume replay time at 100k–700k
  tokens are measured.
- Each reading is in the log fragment with its producing command under `fig:`,
  and the retention dial in `docs/process.toml` is left at 0: turning it on is
  the owner's act.
