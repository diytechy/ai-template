4e8f2079 SOUND

## BLOCKER

none

## MAJOR

none

## MINOR

none

## Verified

All four round-3 findings are fixed. The contention regression fails against `ea3e6688` with a stranded request and passes at this tip, including successful retry. A Windows process probe confirmed successor SessionStart waits through the five-second grace period and takes the lease; concurrent claim and hook calls completed without StoreBusy. No reentrant acquisition was found.

IF-281 separates exit codes from IF-280’s arguments; TC-318 cites both restoration regressions; all 24 added back-links resolve to the correct modules and symbols. Amended design/test text matches the implementation. SR requirement cells comply with R2. No approved rows changed or Status flipped in this range. The RESYNC entry’s `176b6aef` anchor is on trunk’s first-parent history. Worktree and index remained unchanged.

## Commands

Repeated reads and searches are grouped.

- `Get-Content`, numbered reads, and `rg -n` / `rg --files` — inspected rules, skills, full WI/spec, adjudications, prior review, decisions, code, tests, launchers, settings and registry cells.
- `git diff --stat ea3e6688..4e8f2079`, `git diff --name-status ea3e6688..4e8f2079`, scoped `git diff`, and `git log --oneline ea3e6688..4e8f2079` — confirmed the narrow change inventory.
- `git show`, `git rev-parse HEAD`, branch/ref inventory, `git merge-base --is-ancestor`, and first-parent log searches — confirmed reviewed tip and trunk RESYNC anchor.
- `$env:GIT_CEILING_DIRECTORIES = "C:/Projects/ai-template.wt"`; `$env:PYTHONDONTWRITEBYTECODE = "1"` — constrained discovery and disabled bytecode writes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-822 tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_frame_context.py` — **79 passed, 1 failed in 13.22s**. Git Bash failed with `CreateFileMapping` error 5 before POSIX launcher assertions, matching round 3’s environment failure.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; **clean, 821 work items, graph acyclic**, with warnings.
- Scratch-only `Set-Content` / `WriteAllText` and inline Python inspection — prepared probes and corrected a scratch-harness UTF-8 comparison error.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi822-r4-probes.py` — passed regression, Windows successor/concurrent-call and registry checks.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi822-r3-lock-probe.py` — request restored, zero consumed requests, token cleared, retry succeeded.
- `git diff --check ea3e6688..4e8f2079`; `git diff --quiet`; `git diff --cached --quiet`; `git status --porcelain` — checks passed; final status clean.