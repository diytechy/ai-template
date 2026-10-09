9cbf1a59557602f9d1666f71aa4f8eff91c7faa9 NOT YET SOUND

## BLOCKER

none

## MAJOR

- project-trajectory/scripts/plan_coverage.py:485 — Separate dispute rounds contaminate each other when they reuse finding IDs. Confirmed: an accepted dismissal of the current review’s F2, with its matching findings file beside the verdict, passes with exit 0. Retaining an earlier round’s findings file and accepted verdict in that same lane directory, also requesting F2 but concerning another issue, changes the current plan’s result to exit 1. `_ruled_texts` gathers both rounds’ text; `_correspondence_problem` at line 510 rejects their disagreement. This blocks a valid dismissal during ordinary repeated review rounds, contrary to SR-236’s acceptance and Done-when’s resolved-dispute pass condition. The cited verdict needs correspondence to its particular findings input; shared IDs do not establish that relationship.

## MINOR

none

## Verified

Read the full spec, prior reports, dispute ruling and approval sitting, and reviewed the full lane range. SR-236 supplies the missing parent and satisfies owner ruling R2. New Implements tags match LLR-069’s module and symbols; existing approved rows retain their statuses. IF-046’s merged contract accurately describes the parser. The skill mirrors match, and the RESYNC entry has a trunk-ancestor anchor. The requested tests pass without vacuous new assertions; five meaningful regression assertions fail against their respective earlier implementations. The worktree remained clean.

## Commands

- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-853 tests/test_plan_coverage.py tests/test_plan_coverage_step.py tests/test_score_reviews.py` — **73 passed in 5.58s**; used the prescribed ceiling and disabled bytecode writes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — **exit 0**, clean with advisory warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi-853-last-review.py` — confirmed the multi-round failure: **exit 0 → exit 1**; checked five baseline-red assertions.
- Scratch copies of `plan_coverage.py` at `0b550da9` and `49d5a9a6`, invoked with the reproduction’s `--item`, `--root`, `--findings` and plan paths — confirmed baseline malformed verdict input and the earlier unrelated-dismissal acceptance.
- `git diff 0b550da9..9cbf1a59557602f9d1666f71aa4f8eff91c7faa9`, scoped diffs and `--stat` — reviewed authored changes.
- `git diff --check 0b550da9..9cbf1a59557602f9d1666f71aa4f8eff91c7faa9` — clean.
- `git merge-base --is-ancestor c5076d62 0b550da9` — exit 0.
- `git show`, `git log --oneline`, `Get-Content`, `rg` and `Get-FileHash` — inspected rules, records, implementations, baseline code and skill mirrors.
- `git status --short` — clean before and after review.