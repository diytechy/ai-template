# WI-852 — dispute adjudication at cb444fd (findings A, B)

Independent adjudicator. I read `project-trajectory/PROCESS.md` §6 "Review
threat model" as written, and judged each finding on the code at
`a0cb7226..e3be3eec` (`project-trajectory/scripts/review_brief.py` as of
`03693add`). Each stated reproduction was run in process against that code; I
report what I observed, not either party's account.

**Finding A.** It reproduces exactly. `review_brief.review_refusal` returns None (accept) for all three of the reviewer's verdicts.

- With a second line `verdict: CHANGES-REQUESTED findings=0`, the filer accepts the review as APPROVE, while `score_reviews.parse_verdict` (the reader the rollup and scoring use) reads the same file as CHANGES-REQUESTED. The filed record therefore says one verdict and is reported as the other.
- With `VERDICT: APPROVE findings=0 CHANGES-REQUESTED`, the filer accepts.
- With `VERDICT: APPROVE findings=0 findings = 7`, the filer accepts.

This is in scope. The reproduction is model-written repository content, the very class §6 keeps in scope ("the content agents write into the repository (the gates exist to check it)"), and it needs nothing of the host. It also contradicts SR-235's approved acceptance ("a verdict that is unbound, malformed or count-mismatched is refused with no record"). The coordinator's diagnosis holds on the evidence: three rounds each patched the instance that round found (prefix match, duplicated field, now case and extra tokens), because `_machine_line` checks selected tokens of a line chosen by the shared lenient reader. The fix that ends the class is a whole-grammar check at this one boundary:
- exactly one line whose keyword, compared case-insensitively, is `VERDICT`;
- that line must fullmatch the canonical form `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>` and nothing else;
- any other line naming that keyword in any case refuses.

The shared reader's own laxity stays with WI-870, as the reviewer says.

**Finding B.** It reproduces exactly. In a temporary root, `file_review(root, "rollup", <valid APPROVE review>, sha, "full")` wrote `docs/reviews/rollup/001-REVIEW-A-bbbbbbb.md`. The round-reader read-back accepts it, because `rollup` is one directory level. `gen_verdict_rollup.targets` then listed nothing, and `gen_verdict_rollup.main` printed `wrote 0 rollup(s) under docs/reviews/rollup, pruned 1.` and deleted the accepted record.

The coordinator argues this is out of scope as contrived. The bound as written excludes a reproduction that needs the host compromised or contrived (a fake binary, a working-directory-dependent shim, a mid-call environment change, a tampered tool). This one needs none of that. It needs only a valid git branch named `rollup`, and `lane_commits` takes the lane from `git branch --show-current` on whatever branch the attended launcher runs in. The claim mints `wi-NNN`, but nothing in this command requires that. So it is an unusual input on a supported path, not a contrived host, and `out-of-scope` does not apply. It is unlikely, but its outcome is the worst class this change admits: silent loss of an accepted review record, which SR-235 exists to keep. The fix is a few lines in the same function the lane is already changing for finding A: refuse a lane whose scope is the rollup generator's own output directory, derived from `gen_verdict_rollup.ROLLUP_DIR` so it has one owner and is not restated, plus one test. That is far below the defect's cost, so `not-worth-cost` does not apply either.

RULING: A FIX the attended filing boundary accepts a second case-variant VERDICT line, extra tokens and a repeated spaced field, filing a record the rollup reads as a different verdict; replace the token checks with one whole-grammar check (exactly one case-insensitive VERDICT line, fullmatching the canonical form)
RULING: B FIX filing on a valid branch named rollup writes into the rollup generator's owned directory and the next regeneration prunes the accepted record; refuse that scope, derived from gen_verdict_rollup.ROLLUP_DIR, before writing
