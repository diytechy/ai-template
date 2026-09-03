# WI-586 — REVIEW-A rollup

Compiled by the supervising session (2026-09-03) from the round files under
`docs/reviews/wi-586-adjudicate-llr-207-llr-208/`, time-ordered, governing
line last. Every round below was a mechanized, logged reviewer session drawn
by the loop under `review_rounds = 1` and `[attestation] adjudication_review =
"when-minting"` (the verdict drafts spine successors, so a round is owed); all
six rounds were cross-family (Terra/Opus reviewers alternating against the
Opus/Sol adjudicator sessions). This rollup exists only because the mechanical
close (`6b066486`, `active/` -> `complete/`) moved the non-record tree from
`1da2cb20` to `7c01dec9` AFTER the APPROVE round that named `1da2cb20`, so no
logged round names the tree the merge slot judges; the rounds and their
verdicts are unchanged. `001-ADJUDICATE-d7ffb41.md` is the adjudicator's own
verdict (`OUTCOME: RETURN` over LLR-207, LLR-208, TC-205, TC-206 after the
rework of round 002; no approval act taken; three successors drafted), not a
round.

### Round 002 — `002-REVIEW-A-9c563df.md` (gpt-5.6-terra) — CHANGES-REQUESTED findings=1

[BLOCKER] the second `## Dispositions` draft could not mint: `parse_dispositions`
rejects its `depends_on` key and then `safety_class = "adjudication"`, and the
all-or-nothing parser would have returned zero drafts. Verified by the
supervisor against `intake._DRAFT_KEYS` and the `safety_class` refusal arm.
Reworked at `3c7764c5` (Sol): all four rows returned, both drafts `spine`.

### Round 004 — `004-REVIEW-A-3c7764c.md` (claude-opus-5) — CHANGES-REQUESTED findings=3

[BLOCKER] draft 1's scope asserted LLR-208/TC-206 were APPROVED although the
same act returned them; [MAJOR] both drafts declared `bar = "DevStg-Reqs"`
while delivering new tests; [MINOR] a reproduction step omitted its branch
name. Reworked at `aeefcb2b` (Opus).

### Round 006 — `006-REVIEW-A-aeefcb2.md` (gpt-5.6-terra) — CHANGES-REQUESTED findings=1

[MINOR] the disposition counted five continued findings but enumerated six.
Reworked at `082b9e1b` (Sol).

### Round 008 — `008-REVIEW-A-082b9e1.md` (claude-opus-5) — CHANGES-REQUESTED findings=3

[BLOCKER] draft 2's remedy edited TC-206 only, stranding LLR-208 with no queued
approver (driven in a throwaway worktree against the delta-driven mint);
[MAJOR] three verified live defects were narrated in the verdict's closing
section, which no minter reads, instead of being queued; [MINOR] a "whole
suite" count named two modules. Reworked at `397d4b12` (Opus, DESIGN-CHECK
after the page-human degrade): draft 2 names `LLR-208.detail`, a third
disposition block queues the three defects, bars set to `DevStg-Tests`.

### Round 010 — `010-REVIEW-A-397d4b1.md` (gpt-5.6-terra) — CHANGES-REQUESTED findings=1

[MINOR] a mutation-evidence sentence cited 27 passed where 20 was observed.
Reworked at `51fb3e86` (Sol, DESIGN-CHECK).

### Round 012 — `012-REVIEW-A-51fb3e8.md` (claude-opus-5) — APPROVE findings=1

All prior findings verified fixed; every measured claim re-driven, all three
mutation claims reproduced; `parse_dispositions` returns three `spine` drafts
with no refusal. One MINOR for clarity on how draft 3's IF-175 finding is
justified, left for the successor.

VERDICT: APPROVE findings=1
