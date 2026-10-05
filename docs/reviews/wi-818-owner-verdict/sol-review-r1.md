ddf9f026 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. **D-005 permits an unchecked overrule through both admission paths.** project-trajectory/scripts/kitlib/decisions.py:271 substitutes empty entries for unparseable TOML; project-trajectory/scripts/acceptance_record.py:2147 consequently finds no obligation. I staged `owner = "overruled"` followed by `broken = [` without a citing WI: staged synchronization returned `[]`, and merge synchronization returned `None`. A subsequent commit repairing the syntax while removing the verdict also passed. Thus the promised later coupling need never occur. This is a degenerate fail-open path under the owner’s standing prohibition; reporting malformed disclosure fields does not authorize treating an unreadable verdict as no verdict.

2. **The forced migrator corrupts valid multiline TOML.** project-trajectory/scripts/kitlib/decisions.py:405 scans physical lines without tracking string boundaries. With a multiline `review` containing the literal line `reviewed = true`, plus an actual `reviewed = true` key, migration changes that line inside the owner’s note to `owner = "confirmed"`. Separately, a valid recognized value written as `reviewed = """\ntrue\n"""` produces invalid TOML because only its opening line is replaced. This contradicts the note-preservation requirement and LLR-304’s preservation claim at docs/requirements/low-level-requirements.toml:3174. Transform complete TOML assignments without rewriting string contents.

3. **D-003 implements the opposite of the retired-key acceptance rule.** project-trajectory/scripts/kitlib/decisions.py:294 counts an entry carrying both `owner = "confirmed"` and `reviewed = true` as confirmed; the reproduced queue was `([], [], 1)`. The WI’s first Done-when bullet and docs/requirements/system-requirements.toml:1671 require a retired key to be reported **and read as not yet seen**. tests/test_decisions_to_review.py:123 instead pins the contradictory behavior. Reconcile the implementation, design text and test with the governing instruction.

4. **SR-225 incorrectly makes the new coupling conditional on the recording dial.** docs/requirements/system-requirements.toml:1669 places the overrule refusal inside “Where the declared decision-recording dial asks for a record”; line 1671 also says an off or undeclared dial judges a closing lane by nothing here. The implementation enforces coupling unconditionally. In a scratch repository without `docs/process.toml`, a valid overrule without a citer was refused at both staged and merge synchronization. The code follows the WI’s unconditional coupling rule; the SR must distinguish that rule from the conditional obligation to write a delegated-run record.

**MINOR**

1. **TC-320 claims migration coverage its evidence does not provide.** docs/test/test-cases.toml:3193 says the tests exercise a retired line beside an existing owner. Neither evidence test at tests/test_decision_overrule.py:230 or tests/test_decision_overrule.py:246 supplies an owner key. Removing the `_migrated_line` branch that drops such a line would leave those tests green. Add the claimed case and preservation cases covering the confirmed multiline failures.

**Verified**

D-001 correctly reuses the existing staged and per-commit merge synchronization paths. D-004 correctly requires a changed queued or active citer; untouched and archived citers fail. The actual migration preserved every parsed field and note across all 100 original entries in 10 records. Amended row statuses stayed unchanged, the new back-links match their module/symbol rows, and SR-225’s requirement contains no concrete carrier names. The RESYNC entry is anchored at `eae1f486`, the trunk checkout’s commit. A baseline replay confirmed that missing-citer refusal was absent before this change. The worktree remains clean.

**Commands**

Environment for execution: `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`; `PYTHONDONTWRITEBYTECODE=1`.

- `git diff eae1f486..ddf9f026` and scoped diffs, `Get-Content`, `rg` — inspected the WI, rulings, reports, code, rows, tests and shipping changes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-818 tests/test_decisions_to_review.py tests/test_decision_overrule.py tests/test_decision_record.py tests/test_ruling_sync.py tests/test_gen_open_items.py` — **162 passed in 20.36s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean, with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi818-review-probes.py` — reproduced the four major findings; verified migration preservation, unchanged statuses and baseline behavior.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/migrate_decisions.py --check` — exit 0; no record carries the retired key.
- `git diff --check eae1f486..ddf9f026` — clean.
- `git merge-base --is-ancestor eae1f486 main` — exit 1; `main` is not the current trunk.
- `git worktree list --porcelain`, branch/ref inspection, and `git merge-base --is-ancestor eae1f486 refactor_again` — identified the trunk checkout and verified the anchor; ancestry exit 0.
- `git status --short` / `git status --porcelain` — clean before and after review.