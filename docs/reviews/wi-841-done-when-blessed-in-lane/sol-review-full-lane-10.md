82d78a26 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/kitlib/sitting.py:220 — The parser accepts malformed machine lines. Confirmed both:
   - `DONE-WHEN:` followed by `BLESSED changes=2 digest=<current digest>` on the next line.
   - A complete matching line followed by a bare second `DONE-WHEN:` at EOF.

   The regex crosses line boundaries and ignores a keyword without a label. Both shapes were recorded ACCEPTED and released dispatch, staged close and merge. Combined verdicts also accept them. This contradicts LLR-308/LLR-310’s complete-line grammar and TC-326’s incomplete-verdict refusal. Count incomplete keyword lines and validate within physical lines.

**MINOR**

1. project-trajectory/scripts/coordinator_adjudicate.py:50 — Contract IF-285 promises verdict output for calls exiting 0 within their deadline. Confirmed an exit-0, non-timeout result with `is_error=true` prints “its verdict is not read” instead. The implementation correctly rejects the failed call; the authoritative contract needs that condition.

**Verified**

D-028 closes both ninth-pass bypasses: actual `run_iteration` stops before launch for dirty completed lanes and first-iteration blocked resumes; both reproductions reach launch on pre-fix `263e22d2`. Reviewed the full spec, D-001..D-028, amended cells, parsing, acts, holds and minting. R2 is satisfied, all 69 changed-function back-links resolve, existing Status values are unchanged, and the RESYNC anchor is a trunk ancestor. Tested product files matched the fixed tip despite subsequent adjudication commits. No worktree files were edited.

**Commands**

- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final10 tests/test_done_when_blessing.py tests/test_agent_loop_worker.py tests/test_snapshot_readers.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py` — **290 passed in 174.46s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with advisory warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-final10-checks.py` — confirmed dispatch closure, pre-fix failures, malformed-verdict releases, back-links, Status invariants and anchor. Initial fixture omitted its verdict commit; corrected replay passed.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -` — inline cell audits, parser probes and IF-285 reproduction.
- Read-only `git diff`, `git show`, `git log --oneline`, `git status --short`, `git rev-parse`, `rg -n`, and `Get-Content` — inspected the fixed range and governing sources; final worktree status clean.