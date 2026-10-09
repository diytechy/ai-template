# WI-860 — combined adjudication at ba1dc19 (first-approval, second re-sit)

Independent adjudicator, one sitting. I re-read SR-233, LLR-311 and TC-332 as
shown in the brief, against SN-006, WI-860's Done-when, PROCESS_OPTIONS.md
"Delegated decisions record", the built §6 paragraph (`0928481f`) and the
reworked test.

The cited test passes as built (`1 passed, 47 deselected in 0.12s`). I then
deleted the parenthesis "(and in the delegated-decisions record too, when the
run keeps one)" from the §6 paragraph in my working tree and re-ran it. It still
passed (`1 passed, 47 deselected in 0.12s`). PROCESS.md was restored with
`git checkout`, and the tree is clean.

The second rework answers the re-sit's point:
- The dismissal now has a home that always exists, the response to the review verdict.
- The delegated-decisions record is now conditional on the run keeping one.
- §6 states both.
- The test pins the ruling party and the always-present home, and enumerates the finding-judging briefs (`FINDING_JUDGING_BRIEFS`, with a comment saying a later one joins it).

One clause of the parents still has no verifying assertion.

## first-approval

- [RETURN] SR-233 -> the delivered review process must limit findings to defects reachable in a normal working environment, with: one authoritative definition that excludes compromised- or contrived-host reproductions; whoever rules such a finding recording its dismissal in one line in the response to the review verdict, and in the delegated-decisions record too when the run keeps one, never with code; and each enumerated finding-judging brief (today, the reviewer brief) citing the definition without its examples -> UPWARD, it is honestly derived from SN-006 through UNATTENDED-OPS. SIDEWAYS, it no longer conflicts with the dial-gated delegated-decisions record, and the actor and both homes are named. DOWNWARD, TC-332 asserts every clause except the conditional second home: removing "(and in the delegated-decisions record too, when the run keeps one)" from §6 leaves TC-332 green (observed above). So one acceptance condition this row carries has no verifying case, and its `Verification: Test` claim does not yet cover it -> not ready, by that one clause. The rest of the text I would bless as written. Returned: WI-860 spec `## Dispositions`, draft 1.
- [RETURN] LLR-311 -> the §6 bold-lead paragraph must carry the in-scope classes, the exclusion, and the ruling party's one-line dismissal in the response to the review verdict (and in the delegated-decisions record when the run keeps one), without code; each enumerated finding-judging brief must cite the bold lead without copying examples -> UPWARD, it follows SR-233 clause for clause, and the built paragraph now says what the Detail says. DOWNWARD, TC-332, its only TestRef, leaves the delegated-decisions clause unasserted, as shown above -> not ready, by the same one clause. Otherwise blessable as written. Returned: WI-860 spec `## Dispositions`, draft 1.
- [RETURN] TC-332 -> it must assert: the lead occurs once; the paragraph carries the nine named clauses; each member of `FINDING_JUDGING_BRIEFS` cites `§6 "Review threat model"`; and no shipped prompt carries the four examples -> DOWNWARD, the Method and Expected match the test exactly, with no over-claim. But the case claims to verify SR-233 and LLR-311, and it asserts neither the delegated-decisions half of their recording clause nor its condition ("when the run keeps one") -> not ready. Add that clause to the asserted list, and name it in Method and Expected. Returned: WI-860 spec `## Dispositions`, draft 1.

OUTCOME: RETURN rows=3

SITTING: JUDGED kinds=first-approval
