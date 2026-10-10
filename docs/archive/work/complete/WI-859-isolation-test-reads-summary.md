+++
id = "WI-859"
title = "The conftest isolation test reads pytest's summary line, not the run's last line"
workstream = "process"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

`tests/test_conftest_isolation.py` finds the inner run's pytest summary line
wherever the conftest's notices fall. The check still fails on a non-zero
exit, an ImportError, a collection error, an error beside passes, or a
missing summary. A regression supplies the job-object notice after a clean
summary; it is red on the old last-line reading. Gate: Codex 6.1 Sol's fresh
full-lane review `docs/reviews/wi-859/001-REVIEW-A-043ce2a.md`, APPROVE with
0 findings. In the full unfiltered suite on the lane's tip (5d8c3714:
1 failed, 5632 passed, 21 skipped), the isolation test passes. The one
failure is the session kill's taskkill latency, filed separately
(coordinator-2026-10-10 D-006, D-007).

## Context

Filed by hand by the coordinator on 2026-10-08. The full unfiltered suite at
`24160bc0` (detached worktree, fixed basetemp) gave 1 failed, 5392 passed,
17 skipped in 1037 s. The one failure,
`tests/test_conftest_isolation.py::test_a_module_importing_kitlib_collects_on_its_own`,
is deterministic in this environment and environment-caused: the shell now
runs inside a Windows job object, so the suite's conftest prints its notice
"this run is already inside another job object … capped at 50% ON ITS OWN"
after the inner run's summary. The test takes the output's last line as the
summary, so it fails although the inner run reported `4 passed`. The previous
session's full suite (`e806682a`) passed it; the workstation's OS build
changed during this session.

The defect is the test's: a notice the conftest legitimately prints can
follow the summary. Surfaced, not tooled around (owner rule).

## Done-when

- The test finds pytest's own summary line (the one naming passed, failed or
  error counts) wherever the conftest's notices fall, and still fails on an
  ImportError, a collection error or a non-zero exit.
- A test runs the check with the job-object notice following the summary and
  passes; the full unfiltered suite is green on the job-object workstation.
- Review bar: A (one cross-family REVIEW-A).
