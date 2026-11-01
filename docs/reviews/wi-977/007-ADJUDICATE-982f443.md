# WI-977 checkpoint sitting at 982f443

## amendment

This sitting re-judges the two rows that sitting 006 (`006-ADJUDICATE-e49def4.md`) returned: LLR-207 and TC-205.

How I checked:
- I word-diffed both cells against their anchor (2aaf9f66f).
- The only changed text is the batch clause, replaced by its one-row account, and the empty-close and second-lane explanations.
- The base words the pointer-word ban had displaced ("unchanged", "stated", "retains", the unchanged-rework page) are back verbatim. No other hunk remains.
- Neither registry holds a U+FFFD character.
- `trace.py --strict` exits 0.
- The new account matches the code: `_closed_wi_ids` refuses any shape whose `active/` deletions number other than one (`len(deleted) != 1`), and the subject composer takes a single id and raises on anything else.
- The two test comments the lane corrected now say the same (`tests/test_verdict_record.py`, `_claim_commit` and `test_an_empty_close_is_refused_and_the_walk_covers_it_regardless`).
- `pytest tests/test_verdict_record.py -k close`: 11 passed. That includes the two-row arms under both subjects, the second-lane close and the empty close.

Both rows are MEANING, because the mechanical-close peel narrows from a sorted multi-row batch to exactly one row. I would bless both.

- [MEANING+BLESS] LLR-207 Detail -> before: the moved rows' ids are ordered by the shared key and composed into the subject, so a multi-row batch close cannot fail on a sorting; the empty commit is refused "by that pairing ... its empty id list composes a subject no real close carries" -> after: a mechanical close admits exactly one moved row, and any other shape declines to peel toward more review; the subject must equal the writer's composed subject exactly; the one-row clause refuses the empty close and every multi-row close; one deletion implies one source branch; the composer takes a single id, so no empty-id subject is composed. Every other clause is verbatim -> not the same: the peel admits one row instead of a sorted batch. Ready to bless:
  - The detail is the spec's LLR-207 target.
  - It answers REVIEW-A 004's MINOR and both of sitting 006's returns.
  - It names nothing new.
  - TC-205 verifies every arm it states.
- [MEANING+BLESS] TC-205 Method -> before: a two-row close seeded out of order peels under the shared ordering; the second-lane close and the empty close are refused by a one-source-branch requirement, the empty close also by an empty-id subject -> after: a two-row close does not peel, under the historical joined subject and under the current one-item subject; the second-lane close moves two rows, so the one-row clause refuses it; the one-row clause owns the empty close's refusal and no empty-id subject is composed. Every other arm is verbatim -> not the same: the verified peel changes. Ready to bless. It matches LLR-207 arm for arm, and its cited cases exist and pass. Note, not a finding: the empty-close sentence keeps "no third non-emptiness clause ... where these two already had". That still reads correctly, the two being the one-row clause and the composer's refusal.

**What the act needs.**
- The rung is released, so the later act turn re-attests LLR-207 and TC-205.
- No row here is on a held rung.
- With these two, all 23 rows of WI-977's spine change are now judged ready across sittings 005, 006 and 007:
  - 005 blessed SR-144, SR-148, SR-156 and TC-146, and found LLR-058 CLARITY;
  - 006 blessed sixteen rows;
  - 007 blesses LLR-207 and TC-205.

VERDICT: MEANING rows=2

SITTING: JUDGED kinds=amendment
