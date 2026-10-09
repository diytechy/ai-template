e72e3a2db43725351eb54f60a931874e95f10629 NOT YET SOUND

## BLOCKER

none

## MAJOR

- docs/decisions/wi-870.toml:15 — The required migration inventory is missing. D-002 says the affected historical files are listed in this lane’s log fragment, but no such fragment or enumerated list exists at this tip. For example, `docs/reviews/WI-277-REVIEW-A.md` previously supplied a verdict and now supplies none. The owner cannot inspect the promised inventory of lost readings, so the spec’s migration Done-when remains unmet. Record the affected paths and their before/after readings without rewriting the reviews.

## MINOR

none

## Verified

Both consumers use the shared strict reader. All five new gate cases fail against the baseline implementation and pass against the reviewed implementation; malformed verdicts remain fail-closed through the gate’s phase map. Duplicate fields are refused by the shared adjudication reader. All 34 bound adjudication records retain their previous parsing results. Registry changes preserve IDs and statuses, add no SR artifact names, and match the implementation. Added back-links resolve correctly. The RESYNC entry is anchored at trunk ancestor `c5076d62`. The worktree remains clean.

## Commands

- `Get-Content` and `rg` over the specified rules, spec, reports, code, registries and review records — inspected contracts, back-links, assertions and migration disclosure.
- `git status --short` — clean before and after review.
- `git diff c5076d62..e72e3a2db43725351eb54f60a931874e95f10629`, including `--stat`, `--name-only` and `--numstat` — inspected the complete change range.
- `git diff --check c5076d62..e72e3a2db43725351eb54f60a931874e95f10629` — clean.
- `git log --oneline` for the range; `git show -s` and `git branch --contains c5076d62`; `git merge-base --is-ancestor c5076d62 refactor_again` — confirmed history and trunk anchoring. The initial ancestry probe against nonexistent local `main` exited 1.
- With `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt` and bytecode writes disabled:  
  `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-870 tests/test_score_reviews.py tests/test_review_brief.py tests/test_adjudicate_brief.py tests/test_dispute.py tests/test_done_when_blessing.py` — **233 passed in 69.23s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean summary with warnings.
- In-memory `python -` comparison probes — five new gate cases red before/green after; duplicate-field refusal confirmed; historical parsing and registry changes compared. An initial baseline-module import failed; the corrected package-aware import succeeded.