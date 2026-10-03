+++
id = "WI-746"
title = "Let a work item wait on an open item: a queued row with an unruled open item is blocked, not schedulable, and says why"
workstream = "process"
specref = "project-trajectory/scripts/agent_common.py"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed 2026-10-02 at the owner's direction. Today a row can be blocked only by a
`needs` edge to another WORK ITEM, satisfied only by an integrated `done`
predecessor (IF-054). A row that waits on the owner's ruling or on a person's act
has no predecessor row, so it reads as ready: WI-667's own Context says "no
`needs` target or open item carries that gate, so the row reads claimable while it
cannot be built", and the wave-6 handoff and `docs/status.md` carry a hand-written
list of rows not to claim (WI-541's remaining parts, WI-657, WI-667, WI-684,
WI-688, WI-697). WI-713 had to swap `needs = ["OI-96"]` for `WI-722` because an
open-item id is not an accepted edge.

The owner's idea: a queued work item that has associated open items is, mechanically,
BLOCKED (not actively schedulable), and the block ties back to the open item's
details and context, which is where the unblocking decision lives. This needs no new
status directory: status stays the directory, and "blocked" is derived from the
edge.

## Design to confirm (the owner's call)

Preferred: let `needs` accept an open-item id (`needs = ["OI-96"]`) as a hard edge
satisfied only once that open item's `status` is `ruled` (not `pending`). Then:
- the scheduler's readiness (IF-054) and `agent_brief` treat an unruled OI edge as
  unsatisfied, so the row is not claimable and is reported as blocked BY that OI;
- the generated ready frontier drops it and a generated "Blocked" list names each
  row beside the OI that gates it (the OI's title and `open-items.html` anchor), so a
  reader goes straight to the context needed to unblock it;
- `check_trajectory` fails an OI id that resolves to no open item, and keeps the
  acyclicity check over the mixed graph;
- when the OI is ruled the edge is satisfied with no edit to the row, and the row
  is claimable again.

Alternative to weigh: derive the block from an association field instead of `needs`
(for example a `blocked_by` key), keeping `needs` for work-item predecessors only.
Prefer the first unless the readiness code treats `needs` as work-item-only in too
many places.

A gate on a person's act (WI-684's re-sync, WI-688's producer before its re-run) is
filed as an open item too, so it is blockable the same way: say so in the design.

## Done-when

- A queued row whose `needs` names a pending open item is not offered by the
  scheduler's readiness, with a test; the same row is offered once the open item is
  ruled.
- The generated frontier and status snapshot show blocked rows apart from ready
  ones, each with its gating open item; the dashboard and roadmap read status from
  the directory still (no second statement of state).
- A dangling open-item edge is a `check_trajectory` finding; a cycle through one is
  still an error.
- The contracts that state the rule (IF-054's readiness, IF-023's row format,
  `docs/work/README.md`, `WI-000-example.md`, `PROCESS.md` where it describes `needs`)
  say it once and link, not restate; a RESYNC entry covers the shipped scripts and
  templates if they change.
- The rows now waiting by hand (WI-541's remainder, WI-657, WI-667, WI-684, WI-688,
  WI-697) are re-pointed at an open item each (filed or existing, consolidating
  rather than adding where one already covers the gate), and the hand-written "do
  not claim" note in `docs/status.md` is removed.
- The commit bar passes.
