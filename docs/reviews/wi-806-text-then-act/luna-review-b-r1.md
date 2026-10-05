78d90c70 NOT YET SOUND

## BLOCKER

none

## MAJOR

- `docs/requirements/interfaces.toml:1650` — The WI requires IF-129 to be amended, and the design matrix says its contract must lose the “re-attest it in this commit” guidance. IF-129 is unchanged in this lane; the builder’s report confirms no amendment. The required interface-row change and its adjudication are therefore missing.

## MINOR

- `project-trajectory/scripts/acceptance_record.py:2212` — The WI defines the check against a commit’s first parent, but this implementation intersects changes across every parent. A merge that changes the snapshot and a non-Status spine cell relative to its first parent, while matching its second parent on those paths, passes this check. That is the multi-parent rule described by LLR-302, but it differs from the WI’s stated first-parent rule.

## Verified

The new tests cover mixed commits, the two-commit sequence, no-verify lane commits, refresh merges, and squash landings. The targeted suite passed. The strict trajectory check reported a clean result with warnings, and the RESYNC_PACK anchor is an ancestor of trunk tip `cde27048`.

## Commands

- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-806 tests/test_text_then_act.py tests/test_baseline_snapshot.py tests/test_acceptance_record.py tests/test_integrate_admission.py` — `215 passed in 179.49s`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — `clean (821 work item(s), 725 done (88%), 26 cancelled, graph acyclic).` Warnings were reported.
- `git diff --check cde27048..78d90c70` — no whitespace errors.
- `git merge-base --is-ancestor 883b3edf cde27048` — exit code 0.