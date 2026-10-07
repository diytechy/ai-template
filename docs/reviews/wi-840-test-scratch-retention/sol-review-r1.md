3908ca6a NOT YET SOUND

## BLOCKER

none

## MAJOR

- docs/decisions/wi-840.toml:23 — Required completion measurements remain outstanding. The builder report supplies smoke-tier leftover sizes and explicitly owes the full-run result; its smoke timing was measured under load. The spec requires full-run before/after leftover sizes and a quiet-box smoke measurement at docs/work/active/wi-840/WI-840-test-scratch-retention.md:26 and :32. Concrete scenario: a passing `tmp_path_factory` test still leaves its directory under literal `--basetemp`, as my probe confirmed. The smoke measurement therefore cannot establish full-suite retention. Record both required measurements before accepting completion.

## MINOR

- pytest.ini:21 — “a failing test’s stays for the post-mortem” overstates retention. Concrete reproduction: a test body passes, then a fixture teardown assertion fails; pytest reports an error, but the diagnostic directory has already been deleted. With the previous `all` policy it survives. Qualify the comment to describe call-phase failure retention and best-effort cleanup.

## Verified

The requested policy is enabled. A before/after probe confirmed passing-directory removal, call-failure retention, and factory-directory persistence. Skill mirrors match the source; bootstrap excludes this `this-repo` skill from adopters, so no RESYNC entry is owed. No requirement, design, test-case, Status cell, or `Implements:` tag changed. The worktree remained clean.

## Commands

All Python runs disabled bytecode writes; pytest caching was disabled.

- `git status --short` — clean before and after checks.
- `git log --oneline 6b1e85c0..3908ca6a` — one lane commit.
- `git diff 6b1e85c0..3908ca6a`, including `--stat`, `--name-only`, and file-scoped reads — reviewed all five changed files; no spine changes.
- `git diff --check 6b1e85c0..3908ca6a` — passed.
- `Get-Content` and `rg` — inspected the complete spec, builder report, repo guide, relevant PROCESS rules, skills, decisions, configs, tests, fixtures, bootstrap filter, and RESYNC rules.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-840 tests/test_skills_sync.py tests/test_dogfood_sync.py` — **56 passed, 1 skipped in 4.71s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean, with advisory warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/gen_skills_index.py --check-agents` — 18 copies match source.
- Python source inspection of pytest 9.1.1’s temporary-directory fixture and hooks — confirmed cleanup uses call-phase results.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B -` — scratch-only retention probe, running pytest with the literal basetemp above, first with `-o tmp_path_retention_policy=all`, then with the committed configuration. Probe assertions passed; teardown-error diagnostics survived before and were deleted after.

Neither the full suite nor the smoke tier was run, as instructed.