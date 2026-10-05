5361b3e4 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. **Git-quoted paths bypass both overrule coupling and fail-closed parsing.** project-trajectory/scripts/acceptance_record.py:2142 filters raw `git diff --name-only` output without decoding Git’s quoted paths. With `core.quotePath=true`, `docs/decisions/owner-é.toml` appears as `"docs/decisions/owner-\303\251.toml"` and is skipped. I reproduced both a valid overrule without citing work and an overrule followed by `broken = [`: staged synchronization returned `[]`, and merge synchronization returned `None`. Thus D-005’s refusal still has a degenerate path. Read filenames losslessly, for example through NUL-delimited Git output.

2. **Valid run names can produce citations the coupling cannot recognize.** project-trajectory/scripts/kitlib/decisions.py:148 restricts filenames to `[\w.-]+`, while `record_path` at line 157 preserves `+` and `@`. For the valid Git branch names `owner+cleanup` and `owner@cleanup`, I amended a queued specification with the exact generated citation in the overrule commit. Both staged and merge admission incorrectly reported no citing work. The otherwise identical `owner-cleanup` case passed. The path producer and citation reader need the same alphabet.

**MINOR**

1. **Migration deletes trailing comments.** project-trajectory/scripts/kitlib/decisions.py:465 and project-trajectory/scripts/kitlib/decisions.py:469 discard the assignment’s comment when dropping or replacing it. `reviewed = true # Owner confirmed after discussing the rollback` becomes only `owner = "confirmed"`; the corresponding false assignment loses its comment too. This contradicts the explicit comment-preservation promise in project-trajectory/scripts/migrate_decisions.py:13. The parsed-data check cannot detect comment loss.

2. **NaN makes an unchanged, valid record fail migration.** project-trajectory/scripts/kitlib/decisions.py:504 uses ordinary Python equality for re-parse equivalence. A complete record containing an unrelated `extra = nan`, with no retired key, yields no format findings but raises the migration’s “differs … in more than the verdict keys” error. The CLI’s `--check` consequently exits 1 on this already-clean record. I reproduced the same behavior for `+nan` and `-nan`.

**Verified**

D-003’s revised surface/coupling distinction is sound. D-005’s unparseable-parent treatment correctly charges a repair for every overrule it shows; ordinary-path malformed commits remain refused despite a later repair. SR-225 now distinguishes conditional record-writing from unconditional coupling and names no concrete carrier in its requirement cell. The amended rows retain their statuses, and changed back-links match their module/symbol rows. The new regression tests match their claimed cases; selected regressions were red on `ddf9f026`. Scanner probes preserved escapes, multiline strings, quoted keys, arrays, comments containing quotes and CRLF; unsupported forms were safely refused. The migration preserved all 100 original entries’ fields and notes. RESYNC_PACK is anchored at trunk commit `eae1f486`. The worktree remains clean.

**Commands**

Execution environment: `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`; `PYTHONDONTWRITEBYTECODE=1`.

- `Get-Content`, `rg`, scoped `git diff ddf9f026..HEAD`, and `git diff eae1f486..ddf9f026` — inspected rules, full WI, decisions, earlier review, code, rows, tests and shipping changes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-818 tests/test_decisions_to_review.py tests/test_decision_overrule.py tests/test_decision_record.py tests/test_ruling_sync.py tests/test_gen_open_items.py` — **169 passed in 24.75s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean, with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi818-review-probes.py` — original failures corrected; migration preservation and unchanged statuses verified.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi818-round2-probes.py` — scanner matrix, round-one regression replay and all four findings reproduced.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/migrate_decisions.py --check` — exit 0; no repository record carries the retired key.
- `git check-ref-format --branch owner+cleanup` and `git check-ref-format --branch owner@cleanup` — both valid.
- `git diff --check ddf9f026..HEAD` and `git diff --check ddf9f026..5361b3e4` — clean.
- `git worktree list --porcelain`; `git merge-base --is-ancestor eae1f486 refactor_again` — trunk anchor verified; ancestry exit 0.
- `git log -8 --oneline`, commit metadata inspection, `git ls-files --eol`, `git rev-parse HEAD`, and `git status --short` / `--porcelain` — reviewed commits, LF source files, correct tip and clean worktree.