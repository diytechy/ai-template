+++
id = "WI-759"
title = "An open item's wi_refs naming the example WI-000 is inert: the scaffold's commit floor is red since WI-746"
workstream = "process"
specref = "project-trajectory/scripts/check_trajectory.py"
sr_refs = ["SR-148"]
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Context

Found 2026-10-03 by the coordinator. Two slow-tier hook tests fail on trunk since
WI-746 (9dbb5103):

    tests/test_pre_commit_hook.py::test_hook_trajectory_step_is_the_ra_floor
    tests/test_pre_commit_hook.py::test_run_steps_gate_promotes_the_warn_first_floor
    AssertionError: R-E must warn, not block, at the commit floor
    ... check_trajectory: ERROR - OI-2: wi_refs names unknown work item WI-000

In a bootstrapped scaffold an open item's `wi_refs` names the example `WI-000`, and
WI-746's `check_trajectory.open_item_wi_ref_findings` (LLR-289) reports it as
dangling, because example `-000` work rows are excluded from the registry it
resolves against. The check skips `-000` OPEN ITEMS but not `-000` REFERENCES. An
adopter's freshly scaffolded repo therefore fails its commit floor. The module is
slow-tier, so the per-commit smoke tier did not see it.

## Done-when

- A `wi_refs` entry naming a `-000` example work item is inert (no finding), the same
  way `-000` rows are elsewhere; a test in `tests/test_open_item_readiness.py` covers
  it, and the two hook tests above pass.
- If LLR-289's or TC-302's text needs to say so, amend it in place (both Approved;
  status left Approved for the merge's adjudication).
- The smoke tier and `tests/test_pre_commit_hook.py tests/test_meta_repo_hook.py`
  pass.
