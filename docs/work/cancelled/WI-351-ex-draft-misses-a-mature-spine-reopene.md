+++
id = "WI-351"
title = "`ex-draft` misses a mature spine reopened by flipping an EXISTING child to Draft, and the obvious fix creates the mirror false positive (129-REVIEW-A MAJOR 2, plus a counter-measurement taken while triaging it). The reviewer drove a real spine - Verified SR, one TC, its SOLE LLR changed to Draft - and got `computed=G0 ex-draft=G1 window=False`: excluding the Draft LLR also removes the structural evidence that the SR is decomposed, so the counterfactual calls a mature G3 chain undecomposed. Confirmed here on the shipped code. BUT the correction the review proposes - keep the Draft child's structural role while dropping its maturity contribution - was measured too, on the same shipped functions, and it fires on an EARLY project: a ratified-but-unverified SR (Planned) with a drafted LLR and a TC reads ALT `ex-draft=G2` against `computed=G0`, i.e. window=True, which is exactly the nag that 127-REVIEW-A MAJOR 5 ruled out. So this is NOT a one-line fix and must not be treated as one; this branch has already shipped two corrections that were wrong in the opposite direction. A lead worth testing: in the mature case the SR is `Verified` and in the early case it is `Planned`, so the two are separable by SR maturity rather than by structure - but check what that does to the multi-phase G2 cases before adopting it. Whatever lands must pin BOTH spines above as producer and consumer tests, each mutation-proven."
workstream = "scripts"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
order = 348
+++

## Deliverable

RETIRED 2026-07-29, concurrency-restructure Phase 5 item 7, per the 2026-07-28
audit ruling (handoff-2026-07-28c §3: won't-fix the oracle). The row's own
record shows why: the reviewer's fix and its mirror were BOTH measured wrong in
opposite directions, on a branch that had already shipped two such corrections
— `ex-draft` is an oracle whose false negative (a mature spine reopened by
flipping an existing child to Draft) costs a delayed advisory, not a wrong
gate, and every candidate correction re-opened the early-project nag that
127-REVIEW-A MAJOR 5 ruled out. The honest core the audit asked to absorb into
WI-355 is standing practice: WI-355 made an explicit `--gate` genuinely gate,
and the recorded habit is to run `check_trajectory.py --strict` directly,
unfiltered, before claiming anything done — the strict bar is never inferred
from the warn-first floor. This row stays in the archive as the measured
record of both wrong directions.
