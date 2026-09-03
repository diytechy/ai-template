# WI-578 — REVIEW-A rollup

Compiled by the supervising session (2026-09-03) from the round files under
`docs/reviews/wi-578-adjudicate-llr-158-llr-203/`, time-ordered, governing
line last. No mechanized round exists for an adjudication lane until WI-579
lands (the round-scheduling half it absorbed from WI-559); both rounds were
drawn by the supervisor through an independent Opus reviewer with a hostile
brief, rendered from the kit's own reviewer template for this lane.
`001-ADJUDICATE-921f947.md` is the adjudicator's own verdict (`VERDICT:
MEANING rows=3` over LLR-158, LLR-203, LLR-204; the re-anchor found REFUSED
by drift in registries the act never writes; no approval act taken; one
successor drafted), not a round.

### Round 002 — `002-REVIEW-A-c3ae6ba-supervisor.md` — CHANGES-REQUESTED findings=2

Upheld: the absolute constraint (no Status flip, no `last_approved/` byte, driven
at both diff scopes); all five cells' MEANING rulings re-derived from
`baseline_snapshot.refresh_ledger`; the blocked re-anchor reproduced in-process
with the same ledger (SR 17 / LLR 7 / TC 3 absorbed, no flips) and the
writer-vs-gate contradiction confirmed in source; the no-act decision judged
correct; scope clean; harness `integrity=0`, one inherited ERROR. Findings, both
on the drafted successor: [MAJOR] its closing step re-anchored the LLR
registry, an act a `spine` worker lane is refused by construction
(`lane_approval_refusal`); [MINOR] its title was 140 characters.
Reworked at `f51281cc`: the re-anchor restated as the successor condition the
trunk-side amendment-adjudication rung takes after the row lands; title 76.

### Round 003 — `003-REVIEW-A-f51281c-supervisor.md` — APPROVE findings=1

Both findings verified fixed: the diff since `c3ae6ba0` is the round file and
the spec only; `parse_dispositions` returns one draft, no refusal; the title
measures 76; a token sweep of the scope finds no instruction to write
`SNAPSHOT_DIR` or flip a Status; the (a) acceptance test cannot re-introduce the
act (every `copy_live` caller in the suite takes a scaffold root); harness
unchanged. One MINOR for clarity — `safety_class = "spine"` no longer stated its
reason — addressed in the commit before this rollup: the row changes
`refresh_refusal`, the gate every approval act consults, so it runs alone and
first.

VERDICT: APPROVE findings=1
