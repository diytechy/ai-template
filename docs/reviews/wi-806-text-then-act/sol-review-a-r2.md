98142025 NOT YET SOUND

## BLOCKER

- project-trajectory/scripts/acceptance_record.py:2287 — **The squash exemption admits newly combined requirement text that no judged commit carried.** I reproduced trunk and lane each changing different, separated lines inside one multiline `Requirement` cell, committing text and copy separately. Every individual commit passes. Git cleanly squashes them into a third cell value containing both edits, updating live and recorded registries identically. The ordinary staged guard, comparison against both tips, and an ordinary merge commit all refuse that value; the squash guard returns `[]`, and the actual `text-then-act` step exits 0. The mirror also passes. This is another bypass, independent of abandoned-squash residue: equality to Git’s merge result does not prove the resulting cells were committed and judged. docs/requirements/low-level-requirements.toml:3163 codifies this overly broad exemption, and docs/test/test-cases.toml:1745 lacks this case. Require the landing to introduce no new cell values beyond the judged trees, or require a refreshed lane tip containing the final result.

## MAJOR

- project-trajectory/scripts/acceptance_record.py:2317 — **The disputed direct-trunk exemption remains.** After abandoning a valid squash while retaining `SQUASH_MSG`, retyping its exact registries and record as a direct mixed commit still returns `[]`; the current regression explicitly demonstrates this. Byte equality bounds the content risk, but it does not satisfy Q-8’s explicit requirement that other direct trunk commits separate text and act. I retain this finding pending the independent adjudicator’s ruling on docs/decisions/wi-806.toml:32. It is distinct from the newly combined-cell BLOCKER above.

## MINOR

none

## Verified

The original missing-row BLOCKER is fixed: cell values are compared against every parent, including absence. Its regression and the nonidentical stale-squash regression are red on `78d90c70` and green here. Both original MINORs are corrected. LLR-245 accurately states the absorption invariant; changed function tags match their LLR bindings. Existing statuses are unchanged, LLR-302 remains Drafted, and no SR requirement cell changed. IF-129’s current contract contains no retired guidance. The RESYNC anchor is a trunk ancestor. The worktree was clean before and after review.

## Commands

- `Get-Content` inspections of `CLAUDE.md`, the antidote/session-protocol skills, the full WI, governing design ruling and chapter, PROCESS, decisions, builder commit reports, adjudications, earlier reviews, affected code, rows and tests — checked scope, instructions and implementation.
- `rg -n` / `rg --files` inspections of those governing and implementation surfaces — located contracts, bindings, rulings and finding lines.
- `git diff --stat 78d90c70..98142025`; scoped `git diff 78d90c70..98142025 -- project-trajectory tests`; scoped `git diff cde27048..98142025 -- docs/requirements docs/test` — reviewed round-two changes and final spine cells.
- `git diff --name-only cde27048..98142025`; additional scoped diffs; `git log --oneline cde27048..98142025`; `git show --format=fuller --no-patch` for the two new commits — checked supporting changes and builder reports.
- With `$env:GIT_CEILING_DIRECTORIES = "C:/Projects/ai-template.wt"`:  
  `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-806 tests/test_text_then_act.py tests/test_baseline_snapshot.py tests/test_acceptance_record.py tests/test_integrate_admission.py` — **218 passed, 1 failed in 189.92s**. The failure was shallow-clone setup: Git’s `sh.exe` reported the identified sandbox Win32 error 5.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — clean, warnings only.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -` scratch probes — confirmed the combined-cell bypass, ordinary merge refusal, and named refusal for a concrete commit with a missing parent; checked regression behavior, TOML statuses, AST back-links and byte deltas. Initial probe-helper errors were corrected.
- From the scratch reproduction: `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/wi-806/project-trajectory/scripts/check.py --run-steps text-then-act` — **exit 0 on the bypass**. An initial relative-path invocation failed to locate the script.
- `git diff --check cde27048..98142025` — passed.
- `git merge-base --is-ancestor 883b3edf cde27048`; `git show -s --format='%h %s' 883b3edf` — anchor exists and is a trunk ancestor.
- `git status --short`; `git status --porcelain=v1 --untracked-files=all` — clean.