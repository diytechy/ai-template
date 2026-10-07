# WI-840 measurement: one full run's leftover size, before and after

Taken by the wave-18 coordinator on 2026-10-06, answering Sol round 1's MAJOR.

## After (this lane, tmp_path_retention_policy = failed)

The full unfiltered suite on the lane tip `11735c66`, from a detached worktree,
`python -m pytest -q -n auto -p no:cacheprovider --basetemp <fixed>`:

- 2 failed, 5277 passed, 17 skipped, in 815.6 s (816 s wall; the box was loaded
  by two parallel builders and Codex reviews).
- The basetemp left **193 MB** in 1,210 directories at depth 1-2.

Neither failure is this lane's:

- `test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans`: seven
  coordinator handoffs lost their path from an entry root when the wave-17
  handoff cited wave 16 only inside its prompt. Fixed on trunk (`dc1d2851`).
- `test_conftest_isolation.py::test_a_module_importing_kitlib_collects_on_its_own`:
  the test reads the child run's last line, which here was the conftest's
  job-object notice (the run was launched from a background shell, itself a job
  object). This is the wave-14 unfiled follow-up, not a retention effect.

## Before (trunk, the default `all` policy)

Not re-run, to spare the disk: wave 16 recorded about 4 GB per full-run
basetemp on this box (three finished runs left 12 GB under `review-tmp`;
`docs/handoff-2026-10-05-wave16-coordinator.md`, "Corrections learned"). The
lane's own smoke-tier pair (same box, same day) fell from 29 MB to 2.5 MB.

## Quiet-box smoke budget

On the lane rebased onto trunk `f4b13f50` (tip `c733abc6`), with no builder, reviewer or adjudicator running, two consecutive runs of `python -m pytest -q -n auto -m smoke -p no:cacheprovider --basetemp <fixed>` then `python scripts/check_smoke_budget.py --mode enforce`:

- 2274 passed, 2 skipped in 36.66 s; budget 37.0 s vs 60 s, within.
- 2274 passed, 2 skipped in 39.72 s; budget 38.3 s vs 60 s, within.

The basetemp held 2.5 MB after the second run.
