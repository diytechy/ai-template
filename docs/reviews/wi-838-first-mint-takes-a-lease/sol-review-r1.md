909c901f NOT YET SOUND

**BLOCKER**

none

**MAJOR**

- project-trajectory/scripts/session_keep.py:753 — An expired first mint can still overwrite its completed replacement. Confirmed sequence: A takes the first lease; A’s lease expires; B takes over, mints and completes bookkeeping; A then finishes. Because B released its lease, `_landing` replaces B’s session with A’s, increments generation from 1 to 2, and returns an empty reset reason instead of `store moved on`. This contradicts LLR-270’s promise to preserve a replacement session and TC-329’s expected result. tests/test_session_keep.py:583 checks only the case where B still holds its lease, missing this ordering.

**MINOR**

- docs/requirements/interfaces.toml:2302 — IF-247’s amended record shapes omit a reachable state. When a first caller’s lease expires, the record gains `state` and `reset_reason`, so it is no longer lease-only, but still lacks the `session_id`, `generation`, `judged`, and occupancy fields listed under “otherwise.” The new expiry test itself produces this shape. The cell also drops the common identity fields and optional lease from the completed-record description.

**Verified**

The initial lease is written under the store lock, concurrent first calls receive one retained keep, abandonment removes the lease-only record and tombstone, and dial zero writes nothing. New backlinks resolve to LLR-270; approved-row edits are scoped and no Status changes occur. No SR cell was amended. The RESYNC entry exists and its anchor is on trunk. The worktree remained clean.

**Commands**

- Read-only `Get-Content`, `rg -n`, and Git diff/history inspections — read the complete spec and notes, relevant PROCESS rules, changed cells, implementation, tests, and callers.
- `git diff --check 88e28250..909c901f` — passed.
- `git merge-base --is-ancestor 88e28250 refactor_again` — exit 0; RESYNC anchor is on trunk.
- `git status --short` — clean before and after review.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt` and bytecode writes disabled:  
  `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-838-sol tests/test_session_keep.py tests/test_session_service.py tests/test_coordinator_adjudicate.py` — **166 passed in 55.21s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi838-sol-probe.py before` — three new behavior tests failed against the base implementation; dial-zero passed.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi838-sol-probe.py takeover` — confirmed the completed replacement session was overwritten by the late first mint.