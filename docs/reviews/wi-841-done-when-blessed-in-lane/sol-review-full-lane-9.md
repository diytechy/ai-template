263e22d2 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/agent_loop.py:902 — The blessing hold does not cover every BUILD dispatch. Confirmed two states with a committed, unblessed Done-when edit:
   - A completed `WI:` trailer plus substantive uncommitted residue skips `build_hold` and returns through the dirty-tree arm at line 913.
   - A resumed lane with a `Blocked-WI:` trailer returns at line 891 on its first iteration, also skipping the hold.

   In both scratch reproductions, `build_hold` returned `(7, HELD)`, yet `run_iteration` reached routing with BUILD as the next phase. This violates the spec’s next-build hold and LLR-309. Apply the blessing rule to the selected build dispatch, including these resume paths.

**MINOR**

none

**Verified**

The eighth-pass findings are closed: the loop binds and accepts combined requests, RESYNC includes `session_service.py`, and the all-return test now asserts RETURN with no approval act. Reviewed the fixed range, full spec, D-001..D-027, amended cells, holds, parser, acts and minting. R2 is satisfied; all 68 changed-function back-links resolve; existing Status values are unchanged. The RESYNC anchor is a trunk ancestor. Product and test files still matched the fixed tip after adjudicator commits advanced HEAD.

**Commands**

- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final9 tests/test_done_when_blessing.py tests/test_snapshot_readers.py tests/test_acceptance_record.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py tests/test_agent_loop_worker.py tests/test_verdict_record.py` — **379 passed in 240.39s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean trajectory with advisory warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-final9-checks.py` — confirmed both dispatch bypasses; combined-loop regression was red against pre-fix `159819d6`; back-link, Status and anchor checks passed.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -` — inline cell audits and preliminary reproductions; one routing-state probe required corrected constructor arguments, incorporated in the saved script.
- Read-only `git diff`, `git show`, `git log --oneline`, `git status --short`, `git rev-parse --short HEAD`, `rg -n`, and `Get-Content` commands — inspected the fixed range, governing documents, cells, implementation, tests and shipping entry. Final worktree status was clean.