## 2026-09-02 — WI-569: the WI-508 spine reseal — one clean cross-family round, and the two routed BLOCKERs ruled

Worker lane `wi-569-wi-508-spine-reseal-one-clean`, integration base `2f660cb7`.
Successor to the closed `WI-508`, drafted by the `WI-568` adjudication.

**Scope as it actually stood, not as the row was minted.** The row was minted
carrying a baseline arm — regenerate `docs/archive/last_approved/` under the
owner's `OI-78` ruling. Two merged predecessors removed that arm from this
lane before it started, and the spec's `## Context` records the supersession:

- `WI-571` scoped `baseline_snapshot.copy_live` to the act, so a bare
  `intake.py snapshot` on a lane that flips no `Status` copies **zero**
  registries — this row flips none.
- `WI-572` ruled the approval act (every `Status` flip and every
  `docs/archive/last_approved/` write) the adjudicator's alone, on trunk, and
  wired a merge-slot refusal by name against any work lane whose delta performs
  one.

So this lane ran the two arms that remained: **(1)** the one clean cross-family
reviewer round on current trunk confirming the four rows stand in their
reviewed state, and **(2)** a ruling on the two `5175065` BLOCKERs the WI-508
close left on no queue.

Deferred open items: none — `OI-78` was ruled STAND by the owner on
2026-09-01 and this lane owes no further decision.

_(Session in progress; verdict and figures land in this fragment and in the
row's `## Deliverable` at close.)_
