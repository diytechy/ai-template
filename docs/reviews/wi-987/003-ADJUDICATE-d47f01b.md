# WI-987 checkpoint sitting at d47f01b

## amendment

Two approved rows moved against their copies (anchor dc7e2a5cf). Both carry WI-987's one change: the owner's open-items page now lists the stakeholder needs and stakeholders that owe an act. It reads the same detector that the re-attestation brief reads.

What I checked:
- **The parent.** SR-178 asks that the kit "report any recorded artifact whose text has moved ... stakeholder needs included". The page is one of the kit's reporting surfaces, so the new clause is decomposition SR-178 calls for, not new scope.
- **The page code.** `gen_open_items._need_cards` takes `needs_owing`'s rows in the detector's order and shows each row's reason verbatim. A drifted row (one carrying moved cells) is shown as before/after, with the rest of the row collapsed. Any other row, `Drafted` or Status-less, is shown whole and unclipped. So the page holds no second opinion of what owes, matching the Done-when.
- **The tests.** `pytest tests/test_snapshot_readers.py -k "need or stakeholder or open_items or empty_attestation"`: 13 passed, including the three page tests now cited in TC-269's evidence. Both reviewers' red-before runs found the three page tests failing on the pre-change renderer.
- **The lint.** `trace.py --strict` exits 0.
- **Naming.** The new sentences name no code carrier. "The owner's open-items page" is a shipped generated surface, which the LLR and TC tiers may name. The traced `module`/`code_symbol`/`evidence` additions are trace homes, as the brief says, and REVIEW-B 002's MAJOR asked for exactly them.

Both rows are MEANING, because each adds an obligation (the page's needs listing) that a correct implementation of the old text did not have to meet. I would bless both.

- [MEANING+BLESS] LLR-271 Detail -> before: the need and stakeholder tiers are compared, owing rows are derived by the one owing rule, they are briefed in the re-attestation brief (drifted cells before and after, other rows in full), recorded by the act ledger, held by the refresh refusal, and reported by the unanchored rule -> after: the same, plus the owner's open-items page lists the same owing need and stakeholder rows as the brief, a drifted row with its moved cells before and after and a first-approval row with its cells in full -> not the same: a reporting surface is added. Ready to bless:
  - It decomposes SR-178's "report ... stakeholder needs included" onto the owner's surface.
  - "the same owing ... rows as the re-attestation brief" binds the page to the one detector, so no second owing rule can appear.
  - TC-269 verifies both page arms.
- [MEANING+BLESS] TC-269 Method, Expected -> before: the drifted need and stakeholder are reported and briefed; the act ledger names an approved stakeholder; the snapshot is refused until re-attested -> after: the same, plus the open-items page shows a drifted owing need with its moved cells before and after, shows a first-approval need and stakeholder with their cells in full, and includes owing rows in its count -> not the same: page arms are added to the verified set. Ready to bless. It matches LLR-271's new clause arm for arm, and its three new evidence nodes exist and pass.

**Notes, not findings.**
- **The count arm has no LLR home.** TC-269's method also asserts the page's count includes the owing rows (Done-when item 2), which LLR-271's new sentence does not state. So the count has a verifying test but no stated design obligation. This is extra verification, not a false claim, and it does not hold either row. A later amendment could add "and its counts include them" to LLR-271, or state it in LLR-118.
- **LLR-118's list is out of date.** LLR-118, the page's own composition row, unamended, still lists the page's sections and sources without the needs section. It does not say the page shows only those sections, so it is not contradicted, but its list is now incomplete. The section's empty message (Done-when item 2) is likewise held by `test_empty_attestation_state_names_only_what_it_checked`, under no LLR clause. Both are for the lane to weigh; they are not this sitting's rows.

**What the act needs.** The rung is released, so the later act turn re-attests LLR-271 and TC-269. No row here is on a held rung.

VERDICT: MEANING rows=2

SITTING: JUDGED kinds=amendment
