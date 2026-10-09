# WI-852 — combined adjudication at 8ef07c3 (amendment)

Independent adjudicator, one sitting. I judged the amended cells given in the
brief against the anchor `docs/archive/last_approved` (design and test-case copies
at 089e3116). The cells state the two refusals the dispute sitting (`006`) ruled
FIX, so I checked them against the code that applies them (`7c7b643d`) and
against its tests.

Runs:
- `tests/test_review_brief.py` and `tests/test_review_brief_git.py` pass as built (`25 passed in 4.59s`).
- In process, `review_refusal` now refuses all three of finding A's verdicts. A case-variant second line refuses as "2 VERDICT lines". The extra token and the spaced repeated field refuse as "is not exactly" the canonical form.
- `file_review(root, "rollup", <valid review>, …)` refuses, naming the rollup generator's directory, and creates no `docs/reviews/rollup/`.
- Probing past the stated cases: a bulleted or bold second `VERDICT` line is accepted by the filer, and `score_reviews.VERDICT_RE` (anchored `^\s*VERDICT:`) ignores it too. Every line the scorer reads as a verdict is one the filer counts, so the filed record and the reported verdict can no longer disagree.

## amendment

- [MEANING] LLR-313 Detail -> before: `review_refusal` accepts a bound verdict with exactly one VERDICT line whose count matches; `file_review` writes an accepted verdict when the round reader reads the lane path back as the lane's scope -> after: exactly one line whose keyword, in any case, is VERDICT, and that line exactly `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`; and `file_review` also refuses when the record's directory is the rollup generator's own -> not the same: two refusal cases were added. An implementation of the old text filed a review carrying a lowercase second verdict line or an extra token, and filed into `docs/reviews/rollup/`; both fail the new text. BLESSED: `_machine_line` counts every physical line whose pre-colon head, case-folded, is `verdict`, requires exactly one, and fullmatches it against a regex built from the one `REVIEW_GRAMMAR` declaration. `file_review` refuses when the record's parent equals `kitlib.verdict.ROLLUP_DIR`, now the directory's single owner. Both are stated exactly and observable.
- [MEANING] TC-333 Expected + Method -> before: the refusals included a malformed or unbound verdict and an unreadable branch scope -> after: the malformed case is defined as lacking exactly one case-insensitive VERDICT line in the canonical form, a lane whose scope is the rollup generator's directory is added to the refusals, and the Method attempts filing on such a branch -> not the same: the oracle sharpened and a case was added, in both cells. BLESSED:
  - `test_a_filed_coordinator_review_appears_in_the_rollup` now drives five non-canonical lines, including the case-variant second line, the extra token and the spaced field.
  - `test_a_malformed_review_is_refused_and_nothing_is_filed` keeps its cases under the new reasons.
  - `test_filing_a_review_exits_zero_and_writes_only_the_round_file` checks out `rollup` and asserts exit 2 with nothing new filed.
  - Each Expected clause is driven by an Evidence entry already listed.

VERDICT: MEANING rows=2

SITTING: JUDGED kinds=amendment
