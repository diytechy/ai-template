+++
id = "WI-672"
title = "Tie a test case's tier to the smoke tier's membership, and settle the older Smoke cases whose evidence sits in slow modules"
workstream = "quality"
specref = "tests/conftest.py"
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Found by WI-652's re-tier and its codex review (arbitration ruling 4(ii) of
`docs/reviews/2026-09-26-wave3/ARBITRATION.md`). An approved test case's
`tier` cell says whether its evidence runs in the per-commit smoke tier
(Smoke) or only at close (Full); D31 of the spine map puts each Smoke case in
a fast in-memory module and each Full one in a module registered in
`tests/conftest.py` `SLOW_MODULES`. Nothing checks it. WI-652 settled the
cases its own re-tier moved (six amended to Full, two kept Smoke with fast
evidence), but thirteen evidence modules for Smoke-tier cases were already
slow before it, among them `test_bootstrap`, `test_trace`,
`test_trajectory`, `test_trajectory_staged`, `test_handback` and
`test_baseline_snapshot`.

IN SCOPE: (1) a check that reads each approved test case's `tier` and
`evidence` node ids and reports a Smoke case none of whose evidence runs in
the smoke tier (`conftest.smoke_tier_for`), and a Full case none of whose
evidence is slow (advisory, since the Full tier runs everything); decide
whether it lives in `check_trajectory` or `trace` and whether it gates.
(2) Settle the older mismatches the check reports: per case, split its
in-memory clauses into a fast module and move the traced `evidence` pointer,
or amend `tier` to Full in place (left Approved) and file the adjudication.

## Done-when

- The check exists, is tested (a Smoke case with slow-only evidence is
  reported; one with fast evidence is not), and runs in the declared bar.
- Every approved test case it reports is settled by a pointer move or an
  adjudicated tier amendment; the commit bar passes.
