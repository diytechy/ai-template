4dca7543 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

- project-trajectory/scripts/plan_coverage.py:442 — An item SR can be excluded instead of cited. Removing `SR-001` from the SINGLE fixture’s rows and adding `Excludes: SR-001 — deferred to another item.` exits 0 and reports `SR-001: excluded`. Chapter 3 §4.5 requires every item SR to be cited by a row; its exclusion allowance applies to TCs. Require SR citation and align the module’s contract text with that rule.

- project-trajectory/scripts/plan_coverage.py:644 — The DUAL gap policy conflicts with the approved design. A goal declaring C1/C2 and a plan covering only C1, without exclusions, exits 0. Chapter 3 §4.5 says an unexplained clause gap fails, without limiting that rule to SINGLE. D-001 records the conflicting compatibility interpretation, and docs/requirements/low-level-requirements.toml:672 embeds it in the amended design text. Resolve this conflict through a reviewed ruling or implement the stated gate; preserving the pairwise diff alone does not settle it.

**MINOR**

- docs/stack.ini:846 — The restamp incorrectly calls the nine new cases “in-process” and says “no subprocess.” Every case uses `write_single` or `run`, which calls `tests/conftest.py:825`’s subprocess-based `run_py`. Someone assessing smoke membership from this record receives the wrong execution classification. Correct the explanation; this finding does not dispute the measured timing.

**Verified**

The targeted tests pass. The eight new SINGLE tests fail against the pre-change script; the 13 DUAL tests, including byte identity, pass there. All 19 new back-links match LLR-069’s module and symbols. No SR cells or statuses changed, so R2 is respected. The RESYNC entry exists, and `97b5e041` is a trunk ancestor. The worktree remained clean.

**Commands**

All Python commands used `PYTHONDONTWRITEBYTECODE=1`; gate/test runs also used the requested Git ceiling.

- `Get-Content` and `rg -n` inspections of the guides, full WI spec, design/ruling, decisions, earlier review, implementation, tests and amended registries — reviewed.
- `git diff --stat 883b3edf..4dca7543`, `git diff --numstat 883b3edf..4dca7543`, and scoped `git diff 883b3edf..4dca7543` calls — inspected authored and generated changes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-803 tests/test_plan_coverage.py tests/test_plan_coverage_step.py tests/test_dual_plan_round.py tests/test_complexity_ratchet.py` — **35 passed in 16.52s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean, with warnings.
- Inline Python baseline pytest runner, using `883b3edf`’s script and the literal required basetemp — **8 failed, 13 passed in 3.08s**, as expected.
- Inline Python reproduction and AST/TOML checks — confirmed both gap-policy findings, baseline report identity, 19 matching back-links and zero status flips.
- `git merge-base --is-ancestor 97b5e041 883b3edf` — exit 0.
- `git log -4 --format='%h %s'` and `git show --no-patch --format='%h %s' 97b5e041` — confirmed history and anchor.
- `git status --short` — empty before and after review.