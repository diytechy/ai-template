# WI-853 adjudication sitting at 0b94f3c

## amendment

- [MEANING] LLR-069 Detail -> one plan-table grammar for dual/single runs; a findings file's clauses are whatever `F#` lines it declares; any reasoned exclusion resolves a clause; unexplained gaps / uncited item SRs / unnamed TCs exit 1, malformed input exits 2 -> same, plus: a findings input may instead be a review verdict whose finding lines become ordered F1..Fn through `finding_clauses`; mixing declared and verdict forms is malformed (exit 2); an `F#` exclusion that cites a dispute verdict must cite an accepted DISMISS for that finding (or the cited ruling id), otherwise it is a finding -> not the same: a new accepted input form, a new malformed case, and a new finding condition on exclusions. An old-correct implementation would reject a verdict-shaped findings file and would pass an `F#` exclusion citing a FIX/ESCALATE ruling, so it fails the new text.
- [MEANING] TC-069 Expected, Method -> the test checks reasoned exclusions pass, clean plans emit coverage, and bad refs/graphs, clause gaps, bad exclusions, uncited item SRs and unnamed TCs exit 1; malformed input and missing Done-when exit 2 -> it now also checks that a review verdict yields ordered F# clauses; that an uncovered finding exits 1; that an F# exclusion citing a FIX, ESCALATE, non-accepted, mismatched or missing dispute verdict exits 1; and that a mixed declared/verdict findings file exits 2. Method adds review-verdict finding and dispute-ruling cases -> not the same: the acceptance conditions grew, and a test that met the old Expected would not exercise or pass the new cases. Expected is the cell that changes the obligation; the Method change follows from it.

I would bless both rows. The new text is coherent and testable, and it matches what was built: `plan_coverage.finding_clauses` and `ruling_problem`, the latter accepting only an accepted dispute binding that rules DISMISS. The FIX, ESCALATE, pending and mismatched-id cases are tested in `tests/test_plan_coverage.py`. The rung is released, so I re-attest both rows in a separate act commit.

VERDICT: MEANING rows=2

SITTING: JUDGED kinds=amendment
