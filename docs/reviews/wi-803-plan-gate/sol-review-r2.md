eec8ac3c NOT YET SOUND

**BLOCKER**

none

**MAJOR**

none

**MINOR**

- project-trajectory/scripts/plan_coverage.py:134 — A bold exclusion label is rejected despite the supported bold grammar documented at docs/decisions/wi-803.toml:35. With C1/C2 declared, a row covering C1 and `**Excludes:** C2 — deliberately deferred.`, the CLI exits 1 with `unparseable ref '**'`. The regex’s first alternative leaves the closing bold marker in the reference list. Changing only the label to `Excludes:` exits 0. Consume the closing marker and add a regression test.

**Verified**

Both round-1 MAJOR findings and the smoke-classification MINOR are fixed. The amended rows state the gate rules correctly; all 19 new back-links match LLR-069’s module and symbols. No SR cells or statuses changed. Original DUAL fixtures remain unchanged, and the report-byte assertion passes. The RESYNC entry describes the migration and anchors to `97b5e041` on the base’s first-parent history. The worktree remained clean.

**Commands**

Python runs used `PYTHONDONTWRITEBYTECODE=1`; test/gate runs used the requested Git ceiling.

- `Get-Content` and `rg -n` inspections of the guides, full WI spec, design/ruling, earlier reviews, decisions, implementation, tests and registries — reviewed.
- `git diff --stat 883b3edf..eec8ac3c` and scoped `git diff 883b3edf..eec8ac3c` calls — inspected the complete lane change.
- `git show --stat 60ef4dd9` and `git show --stat eec8ac3c` — checked fix scopes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-803 tests/test_plan_coverage.py tests/test_plan_coverage_step.py tests/test_dual_plan_round.py` — **38 passed in 18.62s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean, with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-803 tests/test_plan_briefs.py tests/test_hats.py tests/test_complexity_ratchet.py` — **107 passed in 1.86s**.
- Inline Python baseline pytest runner, using scratch script copies and the literal required basetemp — **8 expected failures against `883b3edf`; 3 expected round-2 regression failures against `4dca7543`**.
- Inline Python parser/CLI reproductions and AST/TOML checks — confirmed the bold-label defect, matching back-links, unchanged fixtures, and zero status flips.
- Inline Python inspection of generated HTML differences — no authored change identified.
- `git diff --check 883b3edf..eec8ac3c` — exit 1; only Markdown hard-break whitespace in `terra-spine-r2.md`.
- `git merge-base --is-ancestor 97b5e041 883b3edf`, `git show --no-patch --format='%h %s' 97b5e041`, and inline first-parent verification — anchor confirmed.
- `git status --short` — empty before and after review.