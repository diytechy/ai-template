## 2026-08-02 — WI-412: the banner counts what it merged, and names the right surface

**Summary.** Closed the three WI-381 REVIEW-A findings the intake minted this
row for. Two were arithmetic and hygiene; the third was a judgment call the row
was explicitly asked to make, and the answer was to decline the fix as floated.

**Finding 3 — residue settled at barrier-open was uncounted.** The
`admit-exclusive` arm drains finished residue so the spine batch runs as the
sole toucher of trunk, but never credited those merges to `state["merged"]`.
The reviewer's two-branch drive is now a test: a hand-finished `wi-777` plus a
queued spine `WI-501` both merge, all three specs land in `complete/`, and the
run used to end `2 WI(s) integrated this run.` The count must be taken *before*
the drain — afterwards those branches have merged and are no longer residue, so
the number is gone — which is how `_station_exit` has counted since REVIEW-A
round 1. This is that same twice-reviewed contract applied to the other
admission path. The test was written first and observed failing on the
undercount.

**Finding 1 — the judged rider, declined as floated.** `_surface_banner`'s
`max(cards, surfaced)` floor did not merely over-report, it *mislabeled*: a
queued gate row with zero projected cards produced `1 ratification(s) waiting
in open-items.html` while that page rendered "None — no durable owner action is
pending", the exact disagreement the ruled amendment forbids. The row floated
naming both sources separately. Declined, because the populations **overlap**:
`_pending_cards` yields blocked rows with a BlockRef plus Draft/Modified spine
rows, `surfaced` yields queued gate/attestation frontier rows, and one row can
be both — the docstring's own "common case" of the two reads agreeing. Two
numbers would report a single waiting row twice, trading an over-count for a
double-count and inventing a second way to disagree with the owner surfaces.
Taken instead: **exclusive arms**. Cards are the authority the amendment names,
so when any exist the banner is byte-identical to before; only when that shared
read is empty is the queued row named in its own words, pointing nowhere.
Neither arm can disagree with `pending_block`, no row is counted twice, one
line each side as the row required.

**Finding 4 — the byte re-stamp.** `PROCESS_OPTIONS.md` measured 169,138 bytes
against a 169,125 stamp. Re-stamped +13 with the layer-table reason across all
three tracked `byte-budget-guard` copies; they remain byte-identical.

**Deviation (recorded, not tidied away).** This row was built in the PRIMARY
checkout rather than a lane worktree, so while it was open the primary checkout
carried the claim and
`test_check_lane.py::test_the_primary_checkout_is_not_a_work_branch` failed —
the guard working correctly, on the builder rather than on the code. It reads
the claim from branch history as well as the working tree, so it stays red
until the primary checkout returns to trunk; nothing in this change causes it.
The authoritative bar for this branch is therefore the station's own §A2
refresh, which runs in a lane worktree where the guard is green by
construction. The remaining rows in this drain follow the worktree shape.

**Verification** (branch, work commit `1520dd59`):

dispatch suites: 38 passed in 22.83s
<!-- fig: cmd="python -m pytest -q tests/test_dispatch.py tests/test_dispatch_admission.py" rev=1520dd59 -->
full suite: 1961 passed / 9 skipped / 1 failed in 337.37s — the single failure
is the primary-checkout guard described above
<!-- fig: cmd="python -m pytest -q -n auto" rev=1520dd59 -->
`gen_skills_index.py --check-agents` — OK, 12 per-agent skill copies match
source. `check_docs.py` (harness ignore globs) — 371 doc(s), 1024 intra-repo
link(s), 0 broken.
