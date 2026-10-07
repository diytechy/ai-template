# WI-841 amendment adjudication at efc4c77

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchor copied at 793cd196.

- [MEANING] TC-326 Method -> run three tests and assert: each covering verdict outcome and a seen matching owner ruling release; an unseen ruling does not; a later text change owes a fresh blessing -> run four tests, adding `test_a_confirmed_ruling_still_carrying_the_retired_reviewed_key_does_not_release`, and also assert that a retired-key ruling does not release -> a new acceptance case: a run that met the old Method (three tests, no retired-key case) fails the new one, and an implementation that let an owner-confirmed entry carrying the retired key release would pass the old Method but not the new one

The row is MEANING, and the TC tier's rung is RELEASED, so the blessing is the adjudicator's to give. I would bless the new text. It closes the coverage gap adjudication 007 recorded against LLR-307 ("a retired reviewed key does not [cover]"). The cited test exists in `tests/test_done_when_blessing.py` and asserts exactly the new clause: the digest is absent from `covering`, the dispatch hold names it, and the merge refuses. The row's Evidence already cites the test, so the Method's run list and its Evidence agree. The Expected ("only a verdict or owner ruling that binds the current digest releases") still holds, because a retired-key entry reads as unseen. The re-attestation is taken in its own act.

VERDICT: MEANING rows=1
