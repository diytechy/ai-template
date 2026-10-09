# WI-860 — combined adjudication at 3e3af5e (first-approval, third re-sit)

Independent adjudicator, one sitting. I re-read SR-233, LLR-311 and TC-332 as
shown in the brief, against SN-006, WI-860's Done-when, PROCESS_OPTIONS.md
"Delegated decisions record", the built §6 paragraph and the test. The test
passes as built (`1 passed, 47 deselected in 0.12s`). I then repeated the
previous sitting's probe: I deleted "(and in the delegated-decisions record too,
when the run keeps one)" from §6 in my working tree. The test now fails
(`tests\test_prompts.py:187: AssertionError`, `1 failed, 47 deselected in 0.20s`).
PROCESS.md was restored with `git checkout`, and the tree is clean.

The only change since the second re-sit (`f43007a7`, `3e3af5ea`) is the one
asserted phrase that sitting's draft named, plus TC-332's Method and Expected
naming it. SR-233, LLR-311 and PROCESS.md are unchanged since that sitting judged
them blessable apart from this gap.

## first-approval

- [APPROVE] SR-233 -> the delivered review process must limit findings to defects reachable in a normal working environment, with: one authoritative definition that excludes compromised- or contrived-host reproductions; whoever rules such a finding recording its dismissal in one line in the response to the review verdict, and in the delegated-decisions record too when the run keeps one, never with code; and each enumerated finding-judging brief (today, only the reviewer brief) citing the definition without its examples -> UPWARD, it is honestly labelled DERIVED from SN-006 through UNATTENDED-OPS, with the feedback to the need stated. SIDEWAYS, the recording homes no longer conflict with the dial-gated delegated-decisions record, and the actor is named; it overlaps no other SR (SR-154 keeps routing and escalation). DOWNWARD, TC-332 now asserts every acceptance clause: the in-scope classes, the exclusion, the ruling party, both homes with the condition, no code response, the enumerated briefs' citation, and the absence of all four examples. Removing the last clause that was unverified now fails it (observed) -> ready. A closed, observable obligation with a verifying case for each clause.
- [APPROVE] LLR-311 -> the §6 bold-lead paragraph must carry SR-233's scope, exclusion and recording rule, and each enumerated finding-judging brief must cite the bold lead without copying examples -> UPWARD, it decomposes SR-233 clause for clause into its two modules, PROCESS.md and the reviewer template. DOWNWARD, the built paragraph says what the Detail says, the reviewer brief cites `§6 "Review threat model"`, and TC-332, its only TestRef, pins each clause -> ready.
- [APPROVE] TC-332 -> one test must assert: the lead occurs once; the paragraph carries the ten named clauses; each member of `FINDING_JUDGING_BRIEFS = (pr.REVIEWER,)` cites `§6 "Review threat model"`; and no shipped prompt carries the four boundary examples -> DOWNWARD, the Method and Expected match the test's asserted lists exactly, with no over-claim, and together they cover every clause of SR-233's acceptance and LLR-311's Detail. The enumerated set and its in-code note that a later finding-judging brief joins it answer how WI-865's brief will be held -> ready.

OUTCOME: APPROVE rows=3

SITTING: JUDGED kinds=first-approval
