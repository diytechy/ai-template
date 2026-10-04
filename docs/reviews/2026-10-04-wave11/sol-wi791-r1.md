523d576a NOT YET SOUND

## BLOCKER

none

## MAJOR

1. **The held-rung guard reads an obsolete dial.** project-trajectory/scripts/acceptance_record.py:1022 reads the merge base’s dial, supplied by project-trajectory/scripts/integrate.py:1189. Concrete scenario: a lane re-attests without a verdict while released; the owner subsequently holds that rung on trunk. The actual merge-slot reader returns `None`, although reading current trunk refuses the act. project-trajectory/scripts/integrate.py:2936 checks admission before refreshing and does not repeat that check afterward. The lane can therefore land a re-attestation without the verdict current authority requires.

2. **LLR-158 still specifies the opposite amendment universe.** docs/requirements/low-level-requirements.toml:1598 says `staged_spine_amendments` reads exactly `SPINE_CSVS`, excludes needs, and shares that universe with the warning and intake mint. The amended symbol cell now names `AMENDMENT_CSVS`, and the code walks SN/DA/SUR too. An approved SN amendment demonstrably produces an amendment record and adjudication row where this design text says it remains outside the walk. Update the detail alongside the symbol.

3. **The amended design and associated test case still claim scripted approval.** docs/requirements/low-level-requirements.toml:1538 says `flip_verified` flips under single-approve/autonomous; docs/test/test-cases.toml:1459 claims the tests demonstrate those flips. A released-rung Drafted row instead reaches the permanent refusal in project-trajectory/scripts/intake.py:2914. The tests cover that refusal, rather than the claimed enactment. These cells contradict both the implementation and OI-45.

## MINOR

1. **Windows verdict paths are accepted by snapshot but rejected at merge.** project-trajectory/scripts/baseline_snapshot.py:1211 accepts `docs\reviews\v.md` as an existing file and records it unchanged. project-trajectory/scripts/acceptance_record.py:994 passes that spelling to `git show`, which cannot resolve it as the committed path. I reproduced a valid CLARITY act being refused. Normalize the recorded path to repository-relative forward-slash form.

2. **SR-228’s first-draft acceptance condition is not enforced.** docs/requirements/system-requirements.toml:1726 says a first draft is not re-attested under this allowance. With an existing snapshot containing Drafted SR-001, a scoped amendment claim and a CLARITY verdict, snapshot records SR-001 in `reattested`, and `merge_approval_refusal` returns `None`. Its Status remains Drafted, so this does not approve it, but the acceptance text overstates the implemented restriction. No new test exercises this condition.

## Verified

Read the full WI, OI-100 ruling, both reports, PROCESS.md, and both commits. SN/DA/SUR amendments route through the existing mint; need briefs show before/after text; ordinary held-rung missing/MEANING verdicts refuse and CLARITY permits the act. Gap 3 remains coupled. New back-links resolve, existing row Status values do not change, and SR-228 contains no concrete implementation name. The RESYNC entry is anchored at trunk commit 484b411c. No autonomous approval path was added. The worktree remains clean.

## Commands

- `Get-Content`, `rg`, and bounded `Select-Object` reads of the spec, reports, rules, changed source, registries and tests — inspected both implementations and authored cells.
- `git status --short` — clean before and after.
- `git log --oneline 484b411c..523d576a` — confirmed the builder and Terra commits.
- `git diff --stat 484b411c..523d576a`, scoped `git diff 484b411c..523d576a -- …`, and `git diff --numstat …` — reviewed the complete change surface, including generated views.
- `git branch --all --contains 484b411c`, `git branch --list`, `git show -s --format='%H %P %s' 484b411c`, the equivalent read for `refactor_again`, and `git merge-base --is-ancestor 484b411c refactor_again` — confirmed the RESYNC anchor is on trunk.
- `git diff --check 484b411c..523d576a` — passed.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt` and bytecode writes disabled:

  ```powershell
  C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-791 tests/test_acceptance_record.py tests/test_baseline_snapshot.py tests/test_snapshot_readers.py tests/test_intake.py tests/test_adjudicate_brief.py tests/test_gen_open_items_render.py tests/test_trajectory_staged.py
  ```

  **396 passed in 184.99s.**

- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0 with advisories.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi-791-review-probes.py` — reproduced the stale-dial admission, Drafted-row re-attestation and Windows-path refusal.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi-791-export-before.py`, scratch-only `Copy-Item` commands, and inline Python archive extraction — exported the base kit and supplied current test fixtures.
- Repeated the seven-module pytest command in that scratch export with:

  ```text
  -k "amendment_walk_covers or amended_approved_need_mints or amended_approved_assumption_and_surrogate or need_scoped_amendment_row or held_rung_CLARITY_verdict or amendment_brief_reanchors or ledger_entry_may_name or reattesting_act_records or approved_needs_amendment_is_recorded or verdict_reattestation_stays_listed"
  ```

  Initial scratch runs exposed missing fixture inputs; after supplying them, the final run with `--tb=short` produced **10 expected failures in 3.19s** against 484b411c.

- Inline Python TOML comparisons — confirmed only the listed rows/cells changed and no existing Status flipped; reran with explicit UTF-8 after correcting the inspection command’s decoding.