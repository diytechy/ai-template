# WI-860 — combined adjudication at 7f72102 (first-approval, re-sit)

Independent adjudicator, one sitting. I re-read SR-233, LLR-311 and TC-332 as
shown in the brief, together with SN-006, WI-860's Done-when and the owner's
2026-10-08 ruling. To check what the rows claim about the delivered text and
what TC-332 can observe, I read the built PROCESS.md §6 paragraph (unchanged
since `d885d0c4`), the reworked test (`5c170072`), and PROCESS_OPTIONS.md
"Delegated decisions record". `trace.py --strict-integrity`, last line:
`Traceability: SN=31 SR=125 LLR=290 TC=301 orphans=0 integrity=0 ... form-findings=1 paraphrase-advisories=3`
(the form finding is LLR-292's, not this chain's). It reports SR-233 as
"unclassified" (advisory), as it does for SR-224 through SR-232.

The rework answers three of the four points the first sitting raised:
- SR-233's false Coincident cell is gone.
- LLR-311 names its home by its real form, the bold-lead paragraph.
- TC-332 now pins the paragraph's content and all four boundary examples.

The fourth point is the new dismissal-record clause, and it is not sound yet.

## first-approval

- [RETURN] SR-233 -> the delivered review process must limit findings to defects reachable in a normal working environment, with: one authoritative definition that excludes compromised- or contrived-host reproductions; the ruling party recording each such dismissal in the lane's delegated-decisions record, without a code response; and the reviewer brief and every brief that judges a review finding citing the definition without restating its examples -> UPWARD, the row is honestly derived from SN-006 through UNATTENDED-OPS, and dropping the Coincident waiver leaves it advisory-unclassified like its recent siblings, which is acceptable. SIDEWAYS, the new dismissal-record clause conflicts with an existing delivered rule. PROCESS_OPTIONS.md "Delegated decisions record" applies only "when a run acts on the owner's behalf while the owner is away", under a dial that ships `"off"`. So in an attended review, or in any adopter on the shipped default, the record this AC names does not exist, and the obligation cannot be met. Yet this SR binds "the delivered review process" without scoping. DOWNWARD, the built §6 paragraph says only "dismissed in one recorded line". It names neither the ruling party nor the delegated-decisions record, and TC-332 asserts neither. "Every delivered brief that judges a review finding" is also unverified: the test checks the reviewer brief alone and does not record that the set is otherwise empty today -> not ready. One acceptance clause is unsatisfiable under the shipped default and appears in no delivered text and no verifying case. Returned: WI-860 spec `## Dispositions`, draft 1.
- [RETURN] LLR-311 -> the §6 bold-lead paragraph must carry the in-scope classes, the exclusion, and the ruling party recording a one-line dismissal in the lane's delegated-decisions record without code; the reviewer brief and every finding-judging brief must cite that bold lead and copy no example -> UPWARD, it follows SR-233 faithfully, including SR-233's defective clause. DOWNWARD, its Detail describes the §6 paragraph as stating the ruling party and the delegated-decisions record, but the paragraph does not say that (the module and the row disagree), and TC-332 does not check it. The "every delivered brief" clause is unverified as above -> not ready. It inherits the parent's unsatisfiable clause and claims text the module does not carry. Returned: WI-860 spec `## Dispositions`, draft 1.
- [RETURN] TC-332 -> the test must assert: the lead occurs once; the paragraph carries the seven named clauses; the reviewer brief cites `§6 "Review threat model"`; and no shipped prompt carries any of the four examples -> DOWNWARD, the Method and Expected are now closed and exact, and they match the reworked test line for line. But the case verifies SR-233 and LLR-311, and it checks neither the ruling party's record nor any finding-judging brief beyond the reviewer's. Both are in the acceptance and the Detail it claims to verify -> not ready. It must cover whatever recording clause the parents settle on, and either assert each finding-judging brief or state that the reviewer brief is the only one today. Returned: WI-860 spec `## Dispositions`, draft 1.

OUTCOME: RETURN rows=3

SITTING: JUDGED kinds=first-approval
