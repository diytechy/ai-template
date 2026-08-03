## 2026-08-02 — WI-412: the banner counts WIs, and names both surfaces

**Summary.** Closed the three WI-381 REVIEW-A findings the intake minted this
row for. The independent REVIEW-A (cross-family, OpenAI `gpt-5.6-sol`) returned
**REWORK** with one BLOCKING finding, and it was right on all three counts; what
shipped is the reworked shape.

**Finding 3 — first an undercount, then the wrong unit.** The `admit-exclusive`
arm drains finished residue so the spine batch runs as the sole toucher of
trunk, but never credited those merges. Round 1 credited them. Review then drove
the deeper defect: the banner promises "N WI(s) integrated" while the code
counted **branches** — `_poll` incremented once per lane, and the residue credit
used `len(finished_branches)`. A spine batch is one branch carrying several WIs,
which is the very admission path the barrier exists for, so the banner still
lied. Now counted in WI ids everywhere: `_poll` credits `len(ln.wi_ids)`, both
drains credit `_residue_wi_count`, which sums `integrate._claimed_wi_ids` — the
same evidence the merge slot reads, so the two cannot disagree about a branch's
payload.

**Finding 1 — judged, reviewed, re-judged.** `max(cards, surfaced)` mislabeled
rather than merely over-reported: a queued gate row with zero projected cards
pointed the owner at `open-items.html`, which rendered "None — no durable owner
action is pending". Round 1 made the arms exclusive, on the argument that the
two populations overlap and two numbers would report one row twice. Review drove
the cost: one unrelated card **suppressed** two genuinely queued attestation
rows. The overlap argument justifies never *summing* the reads; it does not
justify hiding one. Shipped: both named, separately labelled, never added, with
the overlap stated in the line. The cards-only arm keeps the amendment's exact
wording.

**Finding 4 — the byte re-stamp.** `PROCESS_OPTIONS.md` measured 169,138 bytes
against a 169,125 stamp. Re-stamped +13 with the layer-table reason across all
three tracked `byte-budget-guard` copies; they remain byte-identical.

**What the review changed, kept honest.** Two of the three review findings were
about reasoning rather than syntax — the wrong counting unit and a rationalized
judgment — and neither would have been caught by a green suite. The round-1
banner unit test passed against the *old* code and so pinned nothing; it was
replaced. The regression fixture now carries a two-WI residue branch **and** a
two-WI spine batch, and mutation runs confirm it: reverting either `_poll` to
per-lane or the residue credit to `len(finished_branches)` fails it.

**Deviation (recorded).** Round 1 was built in the PRIMARY checkout rather than a
lane worktree, so `test_check_lane.py::test_the_primary_checkout_is_not_a_work_branch`
failed while the branch was open — the guard working correctly, on the builder
rather than the code. Round 2 moved to a real lane worktree via
`integrate.lane_worktree`, which is the shape the rest of this drain follows.

**Verification** (lane worktree, round-2 rework):

dispatch suites: 38 passed in 22.19s
<!-- fig: cmd="python -m pytest -q tests/test_dispatch.py tests/test_dispatch_admission.py" rev=1520dd59 -->
full suite: 1965 passed / 6 skipped / 0 failed in 340.84s (0:05:40)
<!-- fig: cmd="python -m pytest -q -n auto" rev=1520dd59 -->
mutation: `_poll` per-lane → the residue regression FAILS;
`len(finished_branches)` residue credit → the same test FAILS.
`gen_skills_index.py --check-agents` — OK, 12 per-agent copies match source.
