b2f39dec NOT YET SOUND

**BLOCKER**

none

**MAJOR**

none

**MINOR**

- docs/requirements/interfaces.toml:2302 — IF-247 now describes the retired-first shape, but drops the record’s filename convention entirely. A reader locating a particular route learns only `out/adjudicator/`, without the family/hash naming rule or `.json` extension. The writer still uses `<FAMILY>-<route hash>.json` at project-trajectory/scripts/session_keep.py:254. Restore that pattern in the data cell.

**Verified**

The round-1 MAJOR is closed: late first mints preserve both in-flight and completed replacements. The new regression test fails against `909c901f` and passes against `b2f39dec`. The round-1 shape omission is corrected. D-002 and LLR-270 agree with the implementation; TC-329’s added assertions are meaningful. Backlinks remain valid, no SR cells or Status values changed, and the RESYNC anchor is on trunk. The worktree remained clean.

**Commands**

- Read-only `Get-Content`, `rg -n`, `Get-ChildItem`, and Git diff/history inspections — checked the complete spec, earlier review, builder reports, amended cells, relevant PROCESS rules, implementation and tests.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt` and `PYTHONDONTWRITEBYTECODE=1`:  
  `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-838-sol2 tests/test_session_keep.py tests/test_coordinator_adjudicate.py` — **128 passed in 27.93s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi838-sol2-probe.py` — baseline regression red, revised implementation green; four landing probes passed. Initial run hit a scratch-harness constructor error, corrected before rerunning.
- `git diff --check 909c901f..b2f39dec` — flagged only the intentional Markdown hard-break spaces in the committed round-1 review.
- `git merge-base --is-ancestor 88e28250 refactor_again` — exit 0.
- `git status --short` — clean before and after review.