e7865b82 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. **Citation parsing can discharge the wrong record.** project-trajectory/scripts/kitlib/decisions.py:166 admits `#` in run names but stops at the first `.toml#D-<digits>`. Git accepts the branch `owner.toml#D-002`. Its generated citation, `docs/decisions/owner.toml#D-002.toml#D-002`, is parsed as `docs/decisions/owner.toml#D-002`. I reproduced both outcomes: correctly citing the longer filename is refused, while citing it incorrectly discharges an overrule in `owner.toml`. Staged, committed and merge checks agree. This also contradicts the round-trip claim in docs/requirements/low-level-requirements.toml:2927.

2. **The new normalization collides valid branch names and changes existing paths.** project-trajectory/scripts/kitlib/decisions.py:160 uses Unicode `\s`, whereas Git permits U+00A0. `git check-ref-format --branch` accepts both `owner\u00a0cleanup` and `owner-cleanup`; `record_path` now maps both to `docs/decisions/owner-cleanup.toml`. Before round 3 their paths differed. An existing record retaining U+00A0 also cannot satisfy coupling through its exact citation. D-010’s unchanged-path claim and the amended LLR-283 description are therefore false.

3. **NUL delimiters still leave a lossy path reader that bypasses coupling.** project-trajectory/scripts/kitlib/git.py:105 reads through `git_out`, which decodes UTF-8 with replacement. Using scratch-only Git index plumbing, I staged and committed an uncited overrule at the raw path `docs/decisions/owner-\xff.toml`. `git_paths` returned a different path containing U+FFFD; `git_show` treated that replacement path as absent. Staged and committed synchronization returned `[]`, and merge admission returned `None`. The promised lossless reader still permits a listed decisions record to disappear from judgment.

**MINOR**

1. **The new constant backlink does not resolve to its row’s symbol list.** project-trajectory/scripts/kitlib/decisions.py:159 tags `_RUN_EXCLUDED` with LLR-283, but docs/requirements/low-level-requirements.toml:2926 omits that symbol. `check_trajectory.py --strict` emits the corresponding backlink warning when scanning this declaration.

**Verified**

All four round-2 findings are corrected for their original probes. The moved bodies match `23a90c97` after the reader and name substitutions; I found no hidden behavioral change in the decomposition. `git_show` now correctly names LLR-303, whose module and symbol cells include it. Changed registry statuses remain unchanged, SR-225 has no concrete carrier in its requirement cell, and representative new regressions are red against `ee424b3c`. The RESYNC_PACK entry includes both moved modules and is anchored at trunk ancestor `eae1f486`. The worktree remains clean.

**Commands**

Environment: `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`; Python runs used `PYTHONDONTWRITEBYTECODE=1`.

- `Get-Content`, `rg`, and numbered reads — inspected the guide, applicable skills, full WI, round-2 review, process rules, code, rows, tests and shipping entry.
- `git log --oneline ee424b3c..HEAD`, `git diff --stat ee424b3c..HEAD`, and scoped `git diff ee424b3c..HEAD` — reviewed the requested range.
- `git show 23a90c97:project-trajectory/scripts/acceptance_record.py` and scoped `git diff 23a90c97..81da4832` — inspected the decomposition.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-818 tests/test_decisions_to_review.py tests/test_decision_overrule.py tests/test_decision_record.py tests/test_ruling_sync.py` — **154 passed in 16.71s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi818-round2-probes.py` — stopped at its obsolete pre-rebase registry comparison.
- The same command with `wi818-round2-probes-r3.py` — adapted comparison to `ee424b3c`; completed, confirming the original fixes and unchanged statuses.
- The same command with `wi818-round3-probes.py` — confirmed all three MAJOR scenarios, red regression replays and normalized AST equivalence of moved bodies.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/migrate_decisions.py --check` — exit 0; no retired keys.
- `git diff --check ee424b3c..HEAD` — clean.
- `git show -s --format=fuller eae1f486`, `git worktree list --porcelain`, and `git merge-base --is-ancestor eae1f486 2feab680` — trunk anchor verified; ancestry exit 0.
- Scoped `git ls-files --eol`, `git rev-parse HEAD`, and `git status --short` / `--porcelain` — LF source files, correct tip and clean worktree.

Actual shallow-clone test: **not run under the sandbox**. The prescribed suite’s simulated shallow-boundary and missing-object tests passed.