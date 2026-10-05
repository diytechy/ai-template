246f2d1d NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. **The delimiter fix creates another record-identity collision.** project-trajectory/scripts/kitlib/decisions.py:165 and project-trajectory/scripts/kitlib/decisions.py:184 map both Git-valid branches `owner#cleanup` and `owner-cleanup` to `docs/decisions/owner-cleanup.toml`. Their paths were distinct before round 4. I reproduced a first run recording a coupled overrule, followed by the second run overwriting its decision at the shared path without changing any citing specification. Staged synchronization returned `[]`, committed synchronization returned `[]`, and merge admission returned `None`: the retained `overruled` value disguises the second run’s different decision as an existing verdict. This also falsifies the amended “two lanes never write one file” claim at project-trajectory/decisions.template.toml:8.

**MINOR**

none

**Verified**

The original ambiguous-citation and Unicode-space probes now pass. Non-UTF-8 records are refused at staged, committed and merge checks; unread non-UTF-8 source and specification paths remain accepted. Deleting or renaming a pre-existing non-UTF-8 record is refused, exactly as D-014 discloses at docs/decisions/wi-818.toml:103; D-014 is marked high risk. Changed back-links resolve, registry statuses remain unchanged, and SR-225’s requirement cell names no concrete carrier. The RESYNC entry covers the shipped changes and has a verified trunk anchor. The worktree remains clean.

**Commands**

Environment: `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`; Python commands used `PYTHONDONTWRITEBYTECODE=1`.

- `Get-Content`, numbered reads and `rg` — inspected the full WI, guide, applicable skills, process rules, previous review, changed code, rows, tests and shipping entry.
- `git log --oneline 9f787441..HEAD`; `git diff --stat 9f787441..HEAD`; `git diff --name-only 9f787441..HEAD`; full and scoped `git diff 9f787441..HEAD` — reviewed only the requested changes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-818 tests/test_decisions_to_review.py tests/test_decision_overrule.py tests/test_decision_record.py tests/test_ruling_sync.py` — **161 passed in 19.70s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi818-round3-probes-r4.py` — reran the round-3 probes, omitting obsolete `git_paths`/`git_show` body comparisons and reversing the corrected collision assertion; exit 0.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi818-round4-extra-probes.py` — confirmed the new collision, meaningful red regression replays, path refusals, unread-path acceptance, disclosed deletion/rename edge and unchanged statuses; final exit 0. Earlier runs stopped on scratch-harness issues, subsequently corrected.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -` — created/adapted scratch probes and investigated unusual UTF-8 paths. Git for Windows did not add tab, newline, backslash, quote or wildcard paths, so those cases were not exercised.
- `git show -s --format=fuller eae1f486`; `git worktree list --porcelain`; `git merge-base --is-ancestor eae1f486 2feab680` — verified the trunk anchor; ancestry exit 0. The initial ancestry check against `main` returned 1; `main` was not the identified trunk tip.
- `git ls-files --eol` on changed source/test files; `git diff --check 9f787441..246f2d1d`; `git rev-parse HEAD`; `git status --short` / `--porcelain` — LF files, clean diff, correct tip and clean worktree.

Actual shallow-clone test: **not run under the sandbox**. The focused suite’s simulated shallow-boundary and missing-parent tests passed.