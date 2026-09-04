# WI-590 — REVIEW-A rollup

Compiled by the supervising session (2026-09-04) from the round files under
`docs/reviews/wi-590-adjudicate-llr-207-llr-208/`, time-ordered, governing
line last. Rounds 005, 008 and 010 were mechanized, logged reviewer sessions
drawn by the loop under `review_rounds = 1` and `[attestation]
adjudication_review = "when-minting"` (the verdict drafts successors, so a
round is owed); rounds 011–013 were drawn by the supervisor through an
independent Opus reviewer with the kit's own reviewer brief, after the merge
slot refused the lane as a reroll-until-green (rounds 008 and 010 judged one
tree, because the Opus rework between them changed only a record path) and
after the lane, finished and closed, could draw no further round through the
loop (a finished branch is integrated before any worker resumes). Every
round was cross-family or supervisor-independent of the session it judged.
`004-ADJUDICATE-774ef35.md` is the adjudicator's own verdict (`OUTCOME:
RETURN rows=4`: LLR-208 and TC-206 approved and anchored at `a1d80c6f`,
LLR-207 and TC-205 returned with a successor drafted), not a round.

### Round 005 — `005-REVIEW-A-*.md` (gpt-5.6-terra) — CHANGES-REQUESTED findings=1

[MAJOR] LLR-208's Detail claims a work branch never writes the rollup, but
the generator wrote `docs/reviews/rollup/` on a claimed branch and returned
0. The Sol rework at `9671078a` returned LLR-207/TC-205 again and did not
address it. Closed on the TRUNK at `7ea3cce7` (`gen_verdict_rollup`
refuses off-trunk writes; `trunk_step` passes `--trunk-step`; driven by
`test_a_work_branch_cannot_write_the_rollup_but_the_trunk_step_can`).

### Round 008 — `008-REVIEW-A-*.md` (claude-opus-5) — CHANGES-REQUESTED findings=1

[MAJOR] the whole-file anchoring copy at `a1d80c6f` re-blessed 14 drifted
Approved rows (10 LLR, 4 TC) nothing named. The Opus rework at `6fba20e7`
declined it as owner-owed and changed only its record. Remedied by the
supervisor's rework at `075acc78`: draft 2 enumerates the 14 rows with the
verdict that judged each (13 judged by WI-566/573/578/585; LLR-197 unjudged,
its adjudication minted as WI-593) and queues the absorb-ledger successor.

### Round 010 — `010-REVIEW-A-*.md` (gpt-5.6-terra) — APPROVE findings=0

An empty approval at the tree round 008 had judged; the merge slot refused
it as a reroll-until-green. Not the governing verdict.

### Round 011 — `011-REVIEW-A-7b72d2f-supervisor.md` (claude-opus-5, supervisor-drawn) — CHANGES-REQUESTED findings=2

[MAJOR] LLR-208's Approved Detail and code_symbol, and TC-206's Method and
Evidence, no longer describe `_off_trunk_refusal`, the mechanism that now
enforces the clause, and neither draft carried that debt; [MINOR] draft 1
ignored WI-594, the queued adjudication over the same rows. Reworked at
`5ee77bdf`: draft 1 widened to "LLR-207/TC-205 return and LLR-208/TC-206
amendment", both mechanisms in the Detail, the symbol added, the guard's
test cited.

### Round 012 — `012-REVIEW-A-5ee77bd-supervisor.md` (claude-opus-5, supervisor-drawn) — CHANGES-REQUESTED findings=2

[MAJOR] `needs = ["WI-594"]` ordered the overlap the wrong way — WI-594's
first-approval brief, driven, presented LLR-207/TC-205 as awaiting approval
with none of this lane's returns in it; [MINOR] the bundling ground
contradicted the ordering paragraph. Reworked at `98908416` (the `needs`
dropped, the paragraph restated) and on the trunk at `bfe2bda7` (WI-594
narrowed to LLR-209 and TC-207, the two rows only its range authored).

### Round 013 — `013-REVIEW-A-9890841-supervisor.md` (claude-opus-5, supervisor-drawn) — CHANGES-REQUESTED findings=1

Overlap gone (WI-594's brief driven on the merged tree names none of the four
rows), both drafts mint, scope clean. [MAJOR] draft 2's closing sentence
still ordered the amendment behind WI-594 and pointed at "the FIRST draft
above", which mints verbatim into its own row. Reworked at `1715ae78`.

### Round 014 — `014-REVIEW-A-1715ae7-supervisor.md` (claude-opus-5, supervisor-drawn) — APPROVE findings=2

Round 013's finding discharged: both drafts minted in a scratch clone (WI-595,
WI-596) and read end to end as their builders would, with no dangling or
false sentence; WI-594's brief names none of the four rows; parse, mint,
check.py PASS, rollup refusal, absorb ledger and scope all re-driven clean.
Two MINORs left to the successor: three test line numbers in draft 1 item 3
staled by the refresh (the ::names beside them are correct), and draft 2's
"needs no ordering against any other row" is wider than its evidence (WI-594
only).

VERDICT: APPROVE findings=2

(Re-noted 2026-09-04 after the hand refresh onto trunk bfe2bda7 — the generated dashboard resolved to the trunk side and regenerated; the rounds and the governing line above are unchanged.)
