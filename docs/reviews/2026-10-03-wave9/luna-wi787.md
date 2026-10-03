da2037a7 NOT YET SOUND

## BLOCKER

- `docs/ratify/CURRENT.md:657` lists SR-222 and SR-227 as “Waiting for automated adjudication.” There is no WI-787 adjudication act in the lane. If this change lands as-is, the amended Approved LLR cells have no required re-attestation.

## MAJOR

- `project-trajectory/scripts/session_adapters.py:573` resolves the default home from the process environment via `Path.home()`, even though the adapter receives the launch environment in `env`. If a route overrides `HOME` but leaves `CODEX_HOME` unset, Codex writes its rollout under that launch home while the adapter looks under the service process home; occupancy and compaction stay blank. The new tests redirect the process home, but do not cover a launch `HOME` that differs from it.

## MINOR

none

**Verified:** The exact-thread rollout lookup is preserved, and an explicit non-empty `CODEX_HOME` takes precedence. The two amended cells are LLR rows; their module and code-symbol links match the adapter methods, and the SR cells were not changed. No Status flips were present. The RESYNC_PACK entry is anchored at `e78204b4`.

**Commands**

- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/build-wi-787 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py` — **128 passed in 15.85s**.
- `python project-trajectory/scripts/check_trajectory.py --strict` — **exit 0**, with warnings.