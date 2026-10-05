7cb6b1d7 NOT YET SOUND

## BLOCKER

none

## MAJOR

1. **The shared filter suppresses a finding that the former reader reported.** project-trajectory/scripts/check_trajectory.py:2887; project-trajectory/scripts/kitlib/spine.py:304.

   Confirmed with a CSV registry containing two pending `OI-001` rows: the first says `Approve the [p]-[DevStg-Reqs] batch` without a hierarchy-view link; the second says `Unrelated decision`. Previously, `approval_brief_findings` returned one warning. It now returns `[]`, because `open_items_at` overwrites the first row in its dictionary. The carrier preserves duplicate CSV rows, but the new shared stage discards them before linting. Both added open-item pins use unique IDs and miss this regression. Preserve the sequence semantics of this reader and pin this case.

2. **D-001 raises a baseline the spec expressly requires to move downward.** docs/stack.ini:1018; docs/decisions/wi-821.toml:7.

   The measured burn-down is correct: `5/5/52 → 2/2/32`. The committed baseline, however, changes from `0/0/0 → 2/2/32`. On the same residual duplicates, the former baseline reports growth; the replacement reports `OK`. The WI explicitly requires a downward re-stamp, and the census’s standing convention is downward-only. Recording the stale stamp and two residual groups explains the proposed exception; it does not authorize it. Keep the warning baseline or obtain an explicit ruling permitting this upward correction.

## MINOR

1. **D-002 changes visible output despite the unchanged-behavior requirement.** project-trajectory/scripts/trace.py:2862; tests/test_rule_sync.py:1629; docs/decisions/wi-821.toml:14.

   For `IF-101` with `Notes = "Minted 2026-08-15."`, the advisory changes from “states the seam” to “states the system” and loses its trailing period. A filter matching the former phrase consequently stops matching. Detection remains equivalent in this case, but the added test compares the wrapper with the engine it directly calls; it cannot preserve the former wording. Preserve that output or explicitly approve the exception to the Done-when.

## Verified

The commissioning rule delegates correctly to `shared_spec`: distinct sections separate, identical sections and whole-file references pair, and the open-item edge remains intact. The section-separation assertion fails on the former implementation and passes on the new one; the live WI-797–WI-818 population has zero commissioning pairs. LLR-210 describes the rule in the correct direction. New back-links resolve to their owning modules and symbols. Registry changes comprise eight LLR rows and ten TC evidence cells, with no IDs or statuses changed and no SR amendment violating R2. The RESYNC entry is anchored at trunk-history commit `eae1f486`. The deferred-import count is 32, with the new edge explaining the window increase. Fragment rebasing matched the former implementation across 16 edge cases, including CRLF. The worktree remains clean.

## Commands

All Python commands used `C:/Projects/ai-template/.venv/Scripts/python.exe`, with `PYTHONDONTWRITEBYTECODE=1`; required checks also used the supplied `GIT_CEILING_DIRECTORIES`.

- `Get-Content` and `rg` — inspected CLAUDE.md, applicable skills, the full WI and research plan, relevant PROCESS rules, builder/Terra reports, decisions, changed implementations and registry cells.
- `git diff eae1f486..7cb6b1d7` and targeted/stat variants — reviewed the complete change range.
- `git show`, `git log --oneline -4`, `git branch --contains eae1f486`, `git merge-base --is-ancestor eae1f486 refactor_again` — checked former implementations and anchor history; ancestor check exited 0.
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-821 tests/test_consolidate.py tests/test_rule_sync.py tests/test_plan_coverage.py tests/test_trunk_step.py tests/test_spec_move.py` — **211 passed in 7.88s**.
- `python project-trajectory/scripts/check_trajectory.py --strict` — **exit 0**, clean summary with advisories.
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-821 tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_check_stubs.py tests/test_check_dupes_census.py` — **29 passed in 18.18s**.
- `python C:/Projects/ai-template.wt/review-tmp/wi821_review_probes.py` — final run exited 0; confirmed the regression, old/new behavior comparisons, census readings and unchanged statuses. Earlier inline/probe attempts encountered setup errors, corrected before this completed run.
- `python project-trajectory/scripts/check_dupes_census.py --root . --strict` — **exit 0**, `2/2/32`, unchanged from replacement baseline.
- `python project-trajectory/scripts/check_complexity.py --root . --mode enforce` — **exit 0**, 194 over-threshold rows unchanged from baseline.
- `git diff --check eae1f486..7cb6b1d7` — clean.
- `git status --short` — clean before and after review.