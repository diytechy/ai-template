+++
id = "WI-746"
title = "Let a work item wait on an open item: a queued row with an unruled open item is blocked, not schedulable, and says why"
workstream = "process"
specref = ""
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

A queued work item can wait on an open item, and says so: the open-item registry
owns the block (the owner's 2026-10-02 design), and the work-item row format is
unchanged.

- **Rule (IF-073, IF-054):** a queued row named in the `wi_refs` of an open item
  whose `status` is `pending` is not offered by the shared readiness
  (`schedule.hard_preds_satisfied`, mutex candidacy included); dispatch, integrate,
  the status snapshot and `agent_brief` all read it through `schedule._load`. Ruling
  the open item releases the row with no edit to it.
- **Surfaces:** the status snapshot lists open items and blocked rows apart from the
  ready frontier, each beside its gating open item's title and `open-items.html`
  anchor; `agent_brief` returns a blocked notice; `check_trajectory` reports a
  `wi_refs` entry naming no work item (ruled rows included, archived rows seen).
- **Writer:** intake keeps the raising row in `wi_refs` and no longer adds an
  open-item id to `needs`; the shipped disposition prompt says so. The existing
  reader for open-item ids in `needs` is kept, because approved TC-253 requires it;
  retiring it is an adjudicated amendment of TC-253, IF-176 and LLR-058 (owner's
  call, not filed).
- **Rows:** IF-054 and IF-073 amended (Drafted); IF-264, IF-265, LLR-288, LLR-289,
  TC-301, TC-302 added Drafted. OI-98 (WI-684) and OI-99 (WI-688) filed pending;
  the hand-written do-not-claim note removed from `docs/status.md`.
- **Docs:** stated once in IF-073 and IF-054; PROCESS.md (+131 bytes),
  `docs/work/README.md` and the templates link to it; a RESYNC_PACK entry.
- **Reviews:** Sonnet 5.5, NOT YET SOUND at 56503928 (a stale shipped prompt), SOUND
  at acc1e195; composed onto trunk the smoke tier then failed three tests the lane
  caused (a `gates` name the ladder guard reads, two new deferred imports, the
  dashboard past its byte budget), fixed at d1681906 and confirmed SOUND
  (`docs/reviews/2026-10-02-wave7/sonnet-wi746-r1.md` to `-r3.md`).

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

## Design (ruled by the owner 2026-10-02)

The open-item registry owns the block; the work-item row format does not change.
Every open item already carries `wi_refs` (IF-073). The rule:

- A queued work item named in the `wi_refs` of an open item whose `status` is
  `pending` is BLOCKED: the scheduler's readiness (IF-054) and `agent_brief` do not
  offer it, and it is reported as blocked BY that open item. When the open item is
  ruled, the block lifts with no edit to the work item.
- `wi_refs` therefore changes meaning from "related to, or raised by" to "waits on
  this ruling". A pending open item that only mentions a work item for context
  must not list it there. State this once, in IF-073's contract, and link to it.
- The generated ready frontier drops a blocked row. A generated "Blocked" list
  names each blocked row beside the open item that gates it (the open item's title
  and its `open-items.html` anchor), so a reader goes straight to the context
  needed to unblock it.
- `needs` stays work-item to work-item only. No `needs = ["OI-..."]` edge and no
  new `blocked_by` key.
- A gate on a person's act (WI-684's re-sync, WI-688's hold) is filed as a pending
  open item that lists the row in `wi_refs`, so it is blockable the same way.

## Done-when

- A queued row named in a pending open item's `wi_refs` is not offered by the
  scheduler's readiness, with a test; the same row is offered once that open item
  is ruled, with no edit to the row.
- The generated frontier and status snapshot show blocked rows apart from ready
  ones, each with its gating open item; the dashboard and roadmap still read status
  from the directory (no second statement of state).
- A `wi_refs` entry that resolves to no work item is a `check_trajectory` finding.
- The rule is stated once, in IF-073's contract (the `wi_refs` cell's meaning) and
  IF-054's readiness, and `docs/work/README.md`, `PROCESS.md` and the open-item
  template link to it rather than restate it; the work-item row format (IF-023,
  `WI-000-example.md`) does not change. A RESYNC entry covers the shipped scripts
  and templates that change.
- Existing ruled open items' `wi_refs` are left as history (a ruled item blocks
  nothing). Every row still held by hand when this lands gets a pending open item
  that lists it in `wi_refs`, consolidating where one already covers the gate, and
  the hand-written "do not claim" note in `docs/status.md` is removed.
- The commit bar passes.
