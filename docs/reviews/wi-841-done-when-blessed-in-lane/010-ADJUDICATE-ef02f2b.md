# WI-841 amendment adjudication at ef02f2b

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchors copied at 793cd196 (LLR) and 3ad2eb4f (TC).

- [MEANING] LLR-262 Detail -> at merge, a SUCCESSOR part that is ambiguous (no or repeated section, a DONE-WHEN line under another heading, or repeated Dispositions) or supplies no draft is REFUSED -> only repeated Dispositions inside a valid done-when section, or a part supplying no draft, refuses. A sitting with no or repeated done-when section, or a DONE-WHEN line under another heading, is invalid, covers nothing, and the uncovered arm MINTS the goalposts row -> an outcome changed: a misplaced or missing section used to refuse the mint and now produces one. An intake correct under the old text (refusing) fails the new one (minting)
- [MEANING] TC-328 Expected, Method -> an ambiguous or draftless SUCCESSOR part, or an unreadable claim, refuses -> refusal only for repeated Dispositions in a valid section, a draftless part, or an unreadable claim. A SUCCESSOR line outside its section invalidates the sitting and the uncovered arm mints, driven by the new `test_at_merge_a_successor_line_outside_its_section_blesses_nothing` -> the acceptance condition for the misplaced-line case flipped from refuse to mint, carried by both cells
- [MEANING] LLR-307 Detail -> covering: ANY DONE-WHEN line under review records carrying CLARITY/BLESSED/SUCCESSOR and the digest covers it -> only a valid single-kind Done-when verdict, or a combined sitting that passes the sitting validator with the line in its own `## done-when` section, covers -> the cover set narrowed. A covering reader correct under the old text accepts the line from a rejected sitting or from another kind's section, and so releases a hold the new text keeps
- [MEANING] TC-326 Expected, Method -> a verdict or owner ruling binding the digest releases; an unseen or retired-key ruling does not -> only a VALID verdict releases; a rejected sitting, or a sitting with an unrequested section, does not, driven by two new tests (`test_a_rejected_combined_sitting_blesses_nothing`, `test_a_valid_sitting_with_an_unrequested_section_blesses_nothing`) -> two new non-release cases enter the acceptance condition, carried by both cells
- [MEANING] TC-327 Method -> a combined sitting presents exactly its requested kinds and refuses an invalid section -> the same, and it also refuses an UNREQUESTED section, driven by the new `test_an_unrequested_section_refuses_the_combined_verdict` -> a new refusal case the old Method neither ran nor asserted
- [MEANING] LLR-310 Detail -> the verdict carries exactly one heading per requested kind, each section passing its own grammar -> exactly one kind-form lower-case heading per requested kind and NO OTHER kind-form heading; and the Done-when holds use this same validator, accepting a Done-when line only from a valid verdict and its own section -> two new obligations: an extra unrequested `## <kind>` section now refuses, and the hold side is bound to the sitting validator. A validator correct under the old text could accept a `## red-tc` section beside the requested one

All six rows are MEANING, and the LLR and TC tiers' rung is RELEASED, so the blessing is the adjudicator's to give. I would bless each new text:

- The six cells state one consistent rule: a sitting that fails the validator covers nothing at either the holds or the merge, and an uncovered change falls to the goalposts mint, which fails safe.
- The rule matches the code and tests landed in `c34e12b2`. `kdone.covering` excludes a rejected sitting's line. `ab.verdict_refusal("combined", ...)` names an unrequested `red-tc` section. A SUCCESSOR line under `## amendment` leaves intake minting one `brief = "done-when"` row without the stray draft. Two Dispositions inside a valid `## done-when` section still refuse as ambiguous.
- Each TC's run list names exactly the tests its Evidence needs to produce the outcomes it asserts.

The re-attestation is taken in its own act.

VERDICT: MEANING rows=6
