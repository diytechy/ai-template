# Luna review — WI-781 (build/wi-781 at 9134b0fa)

Reviewer: Codex Luna (gpt-6-luna, high), through `luna_review.sh` (lane unchanged). Builder: Claude Opus (kit-builder rules). The one MINOR was fixed by the coordinator at 3dc73563 (the first `Method:` must follow the case header).

9134b0fa NOT YET SOUND

**BLOCKER**

none

**MAJOR**

none

**MINOR**

- `tests/test_assumption_observation_briefs.py:77` — The TC-309 method also requires the assumption chain to appear above the observation Method, but the new ordering assertion checks only that the chain appears before the case header. If the Method were rendered before the chain while the case header stayed below it, these assertions would pass. The row making that claim is `docs/test/test-cases.toml:3136`.

**Verified**

The TC-309 edits are limited to `method` and `expected`; TC-310’s cells and all statuses remain unchanged. The production scripts are untouched, and no RESYNC entry is required for this test-only change. The scoped tests passed, the trajectory check ended cleanly, and the strict trace reported only the pre-existing LLR-292 finding.

**Commands**

- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/build-wi-781 tests/test_assumption_observation_briefs.py tests/test_release_assumptions.py` — `8 passed in 0.79s`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — `check_trajectory: clean`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/trace.py --strict` — exited 1 with the pre-existing LLR-292 “minimal” finding.
- `git diff --check 1273a994..9134b0fa` — passed.