# WI-956 adjudication: plan critique 2, finding F1

Range: `72c81fcdb3144109c8505cf7cb4c5e4f56ad7a80..39c6a4828c3a7771b9f65a4c002a9813523ac933`
(plan, critiques 1 and 2). Ruled against PROCESS.md §6 "Review threat model",
the WI-956 spec's Done-when, and `kitlib/verdict.py` at this range.

## F1: `governing_rev` walks through an empty review carrier

**What I observed.** I built a scratch repo: a work commit W, then a verified
refresh R on top of it (the current grammar), then an empty
`attest: lane bar=review` commit E carrying a `Bar-Green: ... bar=review
tests=none` trailer whose tree and parent check out. At this range:
`_peel_target(E)` is `None`, so the review commit is not peeled.
`governing_rev` returns W and not E, and `governing_identity(tip)` equals
`tree_identity(W)` and not `tree_identity(R)`. I swapped E for a plain empty
telemetry commit and got the same result. So the finding describes the walk's
behaviour correctly. An empty review carrier is walked through, and the refresh
beneath it is peeled.

**Why that is not a Done-when gap.** In this module, "peel" and "walk" are two
different steps. `governing_rev`'s docstring defines the peel as "the one step
that does move the identity", allowed only after `_peel_target` verifies the
commit. A walk step is taken only when a commit's non-record identity equals its
parent's, so a walk step can never change the answer. The Done-when says
"`work_tip` and `governing_rev` never peel a verified `review` attestation".
Deliverable 2 names how: `refresh_attestation` is narrowed to `bar` in
{landing, no-bar}, and `_peel_target` keeps calling it. That is exactly what P2
delivers. An empty review commit is not peeled. It is walked through, and that
step cannot change the governing identity, because the commit carries no work.

**Peeling the refresh beneath is correct.** It is the OI-76 fix this function
exists for. A refresh is disposable, and an identity-neutral commit stacked on
it must not hide it. Otherwise an APPROVE served before the refresh would stop
governing, and the slot would refuse "no logged review round names its current
tree".

**The proposed fix would cause a regression.** Stopping the walk at a review
carrier would shift the identity of tip E from W's tree to R's composed tree. A
commit that changes nothing would then stale an honest pre-refresh verdict.

**The finding's second scenario has no effect.** That scenario is "returns the
parent rather than the review commit", with no refresh beneath. The only caller
of `governing_rev` is `governing_identity`. It reads only the identity, and the
walk's step condition makes the parent's identity equal the carrier's.

Finally, a review attestation that carries a work change, the case where peeling
would let unreviewed work through, is the case P2's
`test_governing_rev_never_peels_a_review_attestation` already pins. The finding
is accurate about the mechanics but wrong that they are a defect.

RULING: F1 DISMISS refuted — an empty review carrier is walked through, not peeled. That step leaves the identity unchanged by construction, and `governing_identity`, the only consumer, reads only the identity. Peeling the refresh beneath is the intended OI-76 behaviour, and a stop at the carrier would stale an honest pre-refresh verdict.
