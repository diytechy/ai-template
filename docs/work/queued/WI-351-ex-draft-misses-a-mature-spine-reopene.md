+++
id = "WI-351"
title = "`ex-draft` misses a mature spine reopened by flipping an EXISTING child to Draft, and the obvious fix creates the mirror false positive (129-REVIEW-A MAJOR 2, plus a counter-measurement taken while triaging it). The reviewer drove a real spine - Verified SR, one TC, its SOLE LLR changed to Draft - and got `computed=G0 ex-draft=G1 window=False`: excluding the Draft LLR also removes the structural evidence that the SR is decomposed, so the counterfactual calls a mature G3 chain undecomposed. Confirmed here on the shipped code. BUT the correction the review proposes - keep the Draft child's structural role while dropping its maturity contribution - was measured too, on the same shipped functions, and it fires on an EARLY project: a ratified-but-unverified SR (Planned) with a drafted LLR and a TC reads ALT `ex-draft=G2` against `computed=G0`, i.e. window=True, which is exactly the nag that 127-REVIEW-A MAJOR 5 ruled out. So this is NOT a one-line fix and must not be treated as one; this branch has already shipped two corrections that were wrong in the opposite direction. A lead worth testing: in the mature case the SR is `Verified` and in the early case it is `Planned`, so the two are separable by SR maturity rather than by structure - but check what that does to the multi-phase G2 cases before adopting it. Whatever lands must pin BOTH spines above as producer and consumer tests, each mutation-proven."
workstream = "scripts"
specref = "docs/reviews/129-REVIEW-A.md"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
order = 348
+++
