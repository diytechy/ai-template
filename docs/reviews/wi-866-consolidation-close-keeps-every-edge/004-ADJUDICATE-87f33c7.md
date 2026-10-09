# WI-866 — combined adjudication at 87f33c7 (amendment, third re-sit)

Independent adjudicator, one sitting. I judged the one amended cell given in
the brief against the anchor `docs/archive/last_approved` (commit 79928ac8).
To check which window the clause's cited test actually drives, I read
`tests/test_consolidate_close.py::test_a_row_claimed_between_close_and_merge_refuses_the_whole_mint`.
It closes, then merges (`_merge`), THEN claims WI-402, then runs the successor
mint (`intake.intake_after_merge`). So the hand claim lands after the merge and
before the mint.

## amendment

- [MEANING] TC-254 Method -> before: a hand claim landing between the close and the merge refuses the successor mint whole (names the claimed row, archives nothing, leaves the other absorbed rows queued) -> after: the same refusal for a hand claim landing after the close and before the successor mint -> not the same. The window that triggers the refusal moved: it now ends at the successor mint instead of at the merge, so it also covers the post-merge, pre-mint interval. An implementation that refused only for claims before the merge would satisfy the old text and fail the new one. The Method cell carries the change; no other cell moved. BLESSED: the new window is the one the cited test drives (claim after `_merge`, before `intake_after_merge`), so the clause now describes what is verified, where the old text named a window the test never exercises. Every other clause is byte-identical to the text this lane's previous sitting blessed. Re-attested by this sitting.

VERDICT: MEANING rows=1

SITTING: JUDGED kinds=amendment
