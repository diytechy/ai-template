+++
id = "WI-412"
title = "Dispatcher banner counts and the missed byte re-stamp (WI-381 REVIEW-A findings 1, 3, 4, minted trunk-side at intake per the R3 invariant). FINDING 3, the fix: residue branches merged at barrier-open are dropped from the drained banner's integrated count - driven: a hand-finished lane plus a queued spine row both merge but the banner says 1 WI(s) integrated; regresses the twice-reviewed banner-count contract trunk's drive.py honored. Count every WI integrated in the tick, whatever admission path merged it; pin with the reviewer's two-branch fixture (docs/reviews/WI-381-REVIEW-A.md finding 3). FINDING 4, the hygiene: PROCESS_OPTIONS.md moved 169,125 to 169,138 (+13, the layer-table row) and the byte-budget-guard skill copies were not re-stamped per the skill's own rule - re-stamp all three homes with the WI-381 reason. FINDING 1, the judged rider: _surface_banner's max(pending_cards, surfaced) floor can OVER-report (a queued gate row with zero pending cards banners 1 ratification waiting while pending_block renders None) - the builder recorded the judgment and over-reporting is the safe direction; JUDGE whether making the banner name the two sources separately (N card(s), M queued attestation row(s)) reads more honestly than the max, take it only if it stays one line each side, else re-record the judgment with the driven example. Scope: dispatch.py banner arithmetic + tests, the three skill-copy stamps."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commits `1520dd59` (round 1) and the round-2 rework
below. REVIEW-A returned **REWORK** with one BLOCKING finding; the shipped
shape is the reworked one, and the round-1 reasoning is recorded here only
where the correction is the interesting part.

FINDING 3 — the undercount, and then the WRONG UNIT. The `admit-exclusive` arm
settles finished residue so the spine batch runs as the sole toucher of trunk,
but never credited what that drain merged. Round 1 credited it and stopped
there. Review drove the deeper defect: the banner says "N WI(s) integrated",
and the code was counting BRANCHES — both in `_poll` (one increment per lane)
and in the residue credit (`len(finished_branches)`). A spine batch is one
branch carrying several WIs, which is precisely the admission path the barrier
exists for, so the banner still lied. Now counted in WI ids on every path:
`_poll` credits `len(ln.wi_ids)`, and both drains credit `_residue_wi_count`,
which sums `integrate._claimed_wi_ids` — the same evidence the merge slot
reads, so banner and merge cannot disagree about a branch's payload. The count
is still taken BEFORE the drain because afterwards those branches have merged
and the number is unrecoverable.

FINDING 1 — the judged rider, judged twice. `max(cards, surfaced)` did not
merely over-report, it MISLABELED: a queued gate row with zero projected cards
sent the owner to `open-items.html` to read "None — no durable owner action is
pending", the disagreement the ruled amendment forbids. Round 1 made the arms
exclusive (cards if any, else the queued rows), reasoning that the populations
overlap and two numbers would double-report one row. Review drove the cost of
that: one unrelated card silently SUPPRESSED two genuinely queued attestation
rows. The overlap argument justifies never SUMMING the two reads; it does not
justify hiding one. Shipped: both named, separately labelled, never added, with
the possible overlap stated in the line itself. The cards-only arm is
byte-identical to the original wording.

FINDING 4 — the hygiene. `PROCESS_OPTIONS.md` measured 169,138 bytes against a
169,125 stamp; re-stamped +13 with the layer-table reason across all three
tracked `byte-budget-guard` copies, which remain byte-identical.

TESTS PIN THE UNITS, PROVEN BY MUTATION. The regression fixture carries a
two-WI residue branch AND a two-WI spine batch, so neither counting path can be
satisfied by counting branches; reverting either `_poll` to per-lane or the
residue credit to `len(finished_branches)` fails it. The round-1 banner unit
test was replaced: it passed against the old code and therefore pinned nothing.

DEVIATION, recorded. Round 1 was built in the PRIMARY checkout instead of a
lane worktree, so `test_check_lane.py::test_the_primary_checkout_is_not_a_work_branch`
failed while the branch was open — the guard working correctly, on the builder
rather than the code. Round 2 moved to a real lane worktree
(`integrate.lane_worktree`), where the full suite is green at 1965 passed / 6
skipped / 0 failed.
