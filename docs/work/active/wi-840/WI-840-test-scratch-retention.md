+++
id = "WI-840"
title = "Test and review scratch no longer accumulates: passing tests' temp dirs are removed, and runs share a dated root"
workstream = "tooling"
specref = "docs/log.d/2026-10-06-wave17-coordinator.md"
buildtier = "quick"
safety_class = "ordinary"
priority = 9
+++

## Context

Filed by hand by the wave-17 coordinator on 2026-10-06, at the owner's
question. Pytest never deletes a literal `--basetemp` after a run; it empties
the directory only at the start of the next run with the same name. Its
retention policy (the last three runs) applies only to its own default root.
Review and full-suite runs point `--basetemp` into `review-tmp`, the one root the
Codex sandbox may write to, under a fresh name each round, and reviewers'
reproduction scripts add randomly named directories. 137 stale directories
(6.6 GB) were deleted on 2026-10-06. Wave 16 ran the disk down to 42 MB, and a
full suite failed in a burst that looked like test failures.

## Done-when

- `pytest.ini` declares `tmp_path_retention_policy = failed`, so a passing
  test's temp directory is removed as the test finishes. Measured: one full run's
  leftover size, before and after.
- The session-protocol skill (source, then the mirrors via `bootstrap.py
  --sync`) directs each session's review and full-suite runs to one dated root,
  `review-tmp/<date>-<session>/`, removed once the session's results are
  recorded, instead of a fresh name per round.
- The smoke budget still holds, measured on a quiet box.
- Review bar: A (one cross-family REVIEW-A).
