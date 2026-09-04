+++
id = "WI-589"
title = "Two verified defects around the one verdict definition: agent_loop's unpinned REVIEW_PHASES duplicate with its magic clamp, and IF-175's requestor list omitting scripts/score_reviews"
workstream = "process"
specref = ""
buildtier = "strong"
priority = 3
safety_class = "spine"
bar = "DevStg-Tests"
+++

## Deliverable

Shipped in session 001 of the batch lane (`05f6bb26`, `b8e445ae`; trailer
`WI: WI-589`). Defect 1: `agent_loop.py`'s byte-identical `REVIEW_PHASES`
tuple is deleted (not aliased) and its two use sites plus the reviewer-dial
clamp read `kverdict.REVIEW_PHASES`, so a third phase added to the verdict leaf
cannot land in one home and be dropped by the other; behaviour is identical at
today's span of 2. Defect 2: `IF-175.requestors` names `scripts/score_reviews`,
its notes state which half of the seam it reads (the declared phase span, not
round evidence), and the span crossing is recorded in the row's notes rather
than its data cell. Module-size ratchet re-stamped downward 2587 -> 2586. Log
fragment: `docs/log.d/WI-589-one-verdict-definition.md`. The row's spec was
closed by the supervising session on 2026-09-03 after the batch's APPROVE
round: the per-session walk moved past this row on its trailer before the C6
close ritual ran, leaving the spec in `active/` and the branch unfinished.

## Context

Drafted by WI-586 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

VERDICT THIS CONTINUES:
`docs/reviews/wi-586-adjudicate-llr-207-llr-208/009-ADJUDICATE-082b9e1.md`.
Neither defect is a fault in the four rows adjudicated there, so neither could be
cured by returning them; both were verified while reading their chain, and they
are queued rather than narrated because a finding recorded only in a file under
`docs/reviews/` is read by nothing — `gen_verdict_rollup` takes that file's
ordinal, phase, sha, verdict word and finding COUNT, never its content.

1. `agent_loop.py:317` declares `REVIEW_PHASES = ("REVIEW-A", "REVIEW-B")`, a
   byte-identical duplicate of `kitlib/verdict.py:157`, pinned by nothing; and
   `_clamped_review_rounds` (`:4160-4170`) clamps with a magic `min(2, rp_int)`
   whose `2` is that tuple's length restated as a literal. `IF-175`'s own notes
   argue the shared-definition case in as many words — "there is exactly one
   definition, and a second reader of round evidence anywhere else is a finding
   against this row". Import the constant and derive the clamp from its length,
   so a third phase cannot be added in one home and silently ignored in the
   other. This is the kit's own settled remedy (LLR-182's rationale: "drift is
   better made unrepresentable than detected").
2. `IF-175.requestors` is `["scripts/integrate", "scripts/agent_loop",
   "scripts/gen_verdict_rollup"]`, but `scripts/score_reviews.py:72` holds a
   hard `from kitlib.verdict import declared_phases` and calls it at `:429`.
   By the row's own sentence that omission is "a finding against this row".
   Add the requestor, and state in the notes which half of the seam it reads
   (the declared phase span, not the round evidence) so the addition does not
   read as a fourth reader of the verdict.
