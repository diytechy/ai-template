# WI-852 — combined adjudication at 53c653c (amendment)

Independent adjudicator, one sitting. I judged the amended cells given in the
brief against the anchor `docs/archive/last_approved` (design and test-case copies
at 42c916bf). To check what the new clause describes and what its test observes,
I read `review_brief.file_review` (the `kitlib.verdict.round_file` read-back added
in `03693add`) and
`tests/test_review_brief_git.py::test_filing_a_review_exits_zero_and_writes_only_the_round_file`.

Runs:
- `tests/test_review_brief.py` and `tests/test_review_brief_git.py` pass as built (`25 passed in 4.15s`).
- Each of TC-333's fourteen Evidence entries resolves to a defined test.

## amendment

- [MEANING] LLR-313 Detail -> before: `file_review` writes only an accepted verdict as the lane's next round record -> after: the same, and only when the round reader reads the written lane path back as that lane's scope -> not the same: a refusal case was added. An implementation of the old text would file a review on a branch such as `feature/wi-900` into a nested directory that `round_file` never reads, and that fails the new text. BLESSED: the clause states exactly what the code does. `file_review` parses its own target with `kverdict.round_file` and refuses unless the parsed scope equals the lane, before anything is written. It is closed and observable.
- [MEANING] TC-333 Expected + Method -> before: the refusal list ends with malformed or unbound verdicts, and filing is exercised on a readable lane -> after: a lane branch the round reader cannot read as a review scope is added to the refusals, and the Method attempts filing on such a branch -> not the same: a case was added in both cells. BLESSED: the cited test checks out `feature/wi-900`, asserts exit 2, and asserts the tree still holds only the earlier `001-REVIEW-A` round, so no requested record is written. That is exactly what the Expected claims. The case rides an Evidence entry already listed, and every other clause is unchanged from the text approved at 42c916bf.

VERDICT: MEANING rows=2

SITTING: JUDGED kinds=amendment
