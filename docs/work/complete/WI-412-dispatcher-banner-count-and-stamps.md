+++
id = "WI-412"
title = "Dispatcher banner counts and the missed byte re-stamp (WI-381 REVIEW-A findings 1, 3, 4, minted trunk-side at intake per the R3 invariant). FINDING 3, the fix: residue branches merged at barrier-open are dropped from the drained banner's integrated count - driven: a hand-finished lane plus a queued spine row both merge but the banner says 1 WI(s) integrated; regresses the twice-reviewed banner-count contract trunk's drive.py honored. Count every WI integrated in the tick, whatever admission path merged it; pin with the reviewer's two-branch fixture (docs/reviews/WI-381-REVIEW-A.md finding 3). FINDING 4, the hygiene: PROCESS_OPTIONS.md moved 169,125 to 169,138 (+13, the layer-table row) and the byte-budget-guard skill copies were not re-stamped per the skill's own rule - re-stamp all three homes with the WI-381 reason. FINDING 1, the judged rider: _surface_banner's max(pending_cards, surfaced) floor can OVER-report (a queued gate row with zero pending cards banners 1 ratification waiting while pending_block renders None) - the builder recorded the judgment and over-reporting is the safe direction; JUDGE whether making the banner name the two sources separately (N card(s), M queued attestation row(s)) reads more honestly than the max, take it only if it stays one line each side, else re-record the judgment with the driven example. Scope: dispatch.py banner arithmetic + tests, the three skill-copy stamps."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 1520dd59. All three WI-381 REVIEW-A findings
closed; the judged rider was judged and its answer is the interesting part.

FINDING 3 — the undercount. The `admit-exclusive` arm settles finished residue
so the spine batch runs as the sole toucher of trunk, but never credited what
that drain merged. The count is now taken BEFORE the drain and added to
`state["merged"]` after it succeeds, which is exactly how `_station_exit` has
counted since REVIEW-A round 1 — the same contract, on the other admission
path. Taking it before is forced, not stylistic: after the drain those
branches have merged and are no longer residue, so the number is
unrecoverable. Pinned by the reviewer's own two-branch drive
(`test_residue_settled_at_barrier_open_is_counted_in_the_drained_banner`): a
hand-finished `wi-777` plus a queued spine `WI-501`, all three specs landing
in `complete/`, banner 2 → 3. The test was written first and failed on the
undercount before the fix went in.

FINDING 1 — the judged rider, DECLINED AS FLOATED. `_surface_banner`'s
`max(cards, surfaced)` was not merely an over-report: it MISLABELED, sending
the owner to `open-items.html` to read "None — no durable owner action is
pending" whenever a gate row was queued with zero projected cards. The WI
floated naming both sources ("N card(s), M queued attestation row(s)"). That
was judged and declined, because the two populations OVERLAP —
`_pending_cards` yields blocked rows with a BlockRef plus Draft/Modified spine
rows, `surfaced` yields queued gate/attestation frontier rows, and a single
row can be both, which is precisely the docstring's "common case" of the two
reads agreeing. Two numbers would report one waiting row twice: an over-count
traded for a double-count, plus a second way to disagree with the owner
surfaces. Taken instead: the arms are made EXCLUSIVE. Cards are the authority
the ruled amendment names, so when any exist the banner is byte-identical to
before; only when that shared read is empty is the queued row named in its own
words, pointing nowhere. Neither arm can disagree with `pending_block`, no row
is counted twice, one line each side. The existing attended-ratification test
already sat on the reviewer's zero-card corner and now pins the honest text; a
companion unit pins the no-double-count property directly.

FINDING 4 — the hygiene. `PROCESS_OPTIONS.md` is 169,138 bytes against a
169,125 stamp; re-stamped +13 with the layer-table reason across all three
tracked `byte-budget-guard` copies, which remain byte-identical.

DEVIATION, recorded rather than tidied away: this row was built in the PRIMARY
checkout instead of a lane worktree, so while it was open trunk transiently
carried a `docs/work/active/` claim and
`test_check_lane.py::test_the_primary_checkout_is_not_a_work_branch` failed —
the guard doing its job, on the builder rather than on the code. Nothing in
this change causes it and it clears when the primary checkout returns to
trunk; the station's own worker seam uses `integrate.lane_worktree`, which is
the shape the remaining rows follow.
