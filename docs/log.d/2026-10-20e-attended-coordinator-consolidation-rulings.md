## 2026-10-20 — attended: the owner's consolidation rulings on the WI-788 rows; WI-963 filed

After headless leg 06 closed the overnight run (`--max-legs 6 reached`),
the owner asked why the trunk mint said WI ids mint only on trunk, and
whether the queue needed consolidating before lanes open up. A read-only
consolidation drill checked the WI-788 lane-lifecycle rows (WI-799 to
WI-817, filed 2026-10-04) against the review-churn rulings of 2026-10-11
to 2026-10-16 and the rows landed since: almost none is built, and
revisions 31 and 33 and ruling 9 contradict large parts of WI-804,
WI-807, WI-809, WI-810 and WI-813. None of this was an open item; the
drill produced the calls.

- **Owner rulings** (coordinator-2026-10-20 D-008 to D-011): WI-902's
  plan-cap FIX goes to a third plan revision with one confirming
  critique (WI-953 carries the route); WI-810 is split, its settled-
  amendment filter filed as WI-963 (54 rows had been closed "as already
  settled") and the rest cancelled, with the question whether the WI
  space rides item 16's carrier left for P5's filing; WI-807 is
  cancelled into WI-808's fenced landing lock; WI-817 is deferred into
  item 10's config program.
- **Edges** (D-012): WI-812 and WI-813 drop WI-810. The drill's other
  re-scopes wait for the owner's review.
- **Correction recorded for the reader:** revision 27 put WI ids on the
  carrier and revision 33 narrowed it back to spine ids; "a work branch
  never mints a WI id" is the current ruling, not a leftover.

Commit `08fc2fb2f`; bar: both strict lints clean, 2969 passed, 3 skipped,
budget 403.1 s vs 60 s (load, records only).

### Round 2: two reviews, a queue audit, the owner's second rulings

Codex Sol and a fresh Claude Opus (both medium, one brief, independent)
reviewed `08fc2fb2f`/`e70a2c48b`: CHANGES-REQUESTED, 4 and 6 findings, all
verified and adopted (D-013). Both found that WI-953's Owner route never
reached its sitting (the disposition composer reads only the closed spec,
report and commit facts), so the recipes gain the append step; Sol found
WI-963 refusing on an absent ledger (a fresh adopter's normal state) and
missing a cell restored after its act; Opus found WI-963's anchor, its
warn/mint invariant and its producers, and stale prose in WI-800, WI-813
and WI-851. A queue audit of every other open row found the runner's real
hazard: after the first three rows, the handoff sent legs to the
2026-10-11 "leg 03's rows" table, whose first row was WI-906. The owner
ruled (D-014 to D-019): no bar fails on the smoke tier's seconds, the run
menu's audit judges them, and WI-940 is re-scoped to carry it ahead of
WI-957; WI-906 cancelled as contrived; sixteen rows deferred for review of
their re-scopes (WI-857 behind WI-801); WI-832 and WI-833 kept; WI-795
needs WI-820; WI-910 split, its Mac run filed as WI-964; owner-held rows
listed as never claimed by a leg. The handoff's queue is now an explicit
list that stops when nothing in it can move.
