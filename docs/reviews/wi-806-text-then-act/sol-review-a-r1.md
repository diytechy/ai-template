78d90c70 NOT YET SOUND

## BLOCKER

- project-trajectory/scripts/acceptance_record.py:2234 — **Intersecting change labels hides newly authored text.** When SR-003 exists only in the second parent, editing its Title and approving/copying it during a merge produces `added` against the first parent and `Title` against the second. Their intersection is empty. I reproduced the staged guard returning `[]`, the committed guard returning `[]`, and the landing rung returning `None`; the mirror check also passed. The same defect admits an edited squash of a lane that introduced SR-003. Compare resulting cell values across the parent trees, including missing-row states, rather than intersecting these incompatible labels. This violates LLR-302’s promise at docs/requirements/low-level-requirements.toml:3163.

## MAJOR

- project-trajectory/scripts/check.py:1998 — **A stale SQUASH_MSG grants an exemption to a direct trunk commit.** Squash a valid two-commit lane, then cancel its staged changes with `git restore --staged .` and `git restore .`. I confirmed the worktree becomes clean while SQUASH_MSG remains. Subsequently stage a direct mixed text-and-copy commit matching that abandoned lane’s spine changes: the plain guard refuses it, but the hook step exits 0 because acceptance_record.py:2279 adds the stale tip as a comparison base. This contradicts Q-8’s direct-trunk rule and D-004’s claim that stale SQUASH_MSG “never removes” judgement.

## MINOR

- tests/test_text_then_act.py:227 — **The negative merge assertion never exercises a merge.** The preceding merge already incorporated main. Merging main again creates no MERGE_HEAD; I reproduced `None` for its lookup. The assertion at line 231 therefore checks an ordinary staged commit, leaving the claimed merge-specific refusal untested.

- docs/requirements/low-level-requirements.toml:1777 — **LLR-173’s new unconditional wording omits implemented exceptions.** It says the copy’s commit adds/removes no approval-act rows and records previously committed text. The permitted root commit can introduce both rows and their record; the exempt squash can combine text and act. Qualify this sentence consistently with LLR-302 and the owner’s squash ruling.

## Verified

The prescribed tests passed on rerun: **215 passed in 184.40s**. Strict trajectory checking passed with warnings. Changed function back-links match their LLR modules and code symbols; existing row Status values remain unchanged, and no SR requirement cell was amended. The RESYNC entry’s anchor, 883b3edf, is a trunk ancestor. The refusal-text regression fails against the base implementation and passes on this head. The worktree remained untouched.

## Commands

- `git diff cde27048..78d90c70`, including scoped diffs, `--stat` and `--name-only` — reviewed all 23 changed files.
- `Get-Content` / `rg` inspections of the guide, skills, full WI, decisions, Terra report, design ruling and chapters, PROCESS, affected code, rows and tests — checked governing text and implementation.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-806 tests/test_text_then_act.py tests/test_baseline_snapshot.py tests/test_acceptance_record.py tests/test_integrate_admission.py` — first run: 205 passed, 2 failures and 8 errors involving disappearing scratch directories.
- Same pytest command with `--tb=short` and scratch-log redirection — **215 passed in 184.40s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — clean, warnings only.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -` scratch probes — confirmed the merge/squash bypass, stale-message bypass, and missing MERGE_HEAD in the negative test.
- Python TOML/AST comparison — no existing Status flips; all changed tagged functions matched their LLR bindings.
- Python base-versus-head regression probe — refusal-text assertion red on cde27048, green on 78d90c70.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check.py --run-steps cli-reference` — skipped as designed on a work branch.
- `git show -s --format='%h %s' 883b3edf`; `git merge-base --is-ancestor 883b3edf cde27048` — anchor exists and is a trunk ancestor.
- `git diff --check cde27048..78d90c70` — passed.
- `git status --short` — clean before and after review.