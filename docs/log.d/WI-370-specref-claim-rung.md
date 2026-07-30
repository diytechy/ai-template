## 2026-07-30 — WI-370: the claim refuses a spec without a resolving SpecRef

R-E hoisted to claim time, the WI-358 shape again: the 2026-07-30 drain
measured that an intake filed without a SpecRef claims cleanly against the
warn-first floor and then reds `--strict` on every composed tree that sees
it open — from a file the closing branch cannot amend, because open wants
the ref and terminal wants it cleared, so trunk-side repair rename-merges
the ref into the archived copy and trips R-F instead. The claim is the
last moment the debt is a one-line trunk commit.

- **Deliverable:** `_specref_refusal` in
  [integrate.py](../../project-trajectory/scripts/integrate.py) (empty ref
  and unresolving-path refusals, path-part-only per R-E; anchors stay
  check_trajectory's) + three rung tests and shape-explicit fixtures in
  tests/test_integrate.py (queued specs carry a resolving ref, the e2e
  close clears it). Spec archived:
  [WI-370](../work/archive/WI-370-claim-refuses-a-spec-without-a-specref.md).
- **Deviations from spec:** none in scope; the rung was extracted to its
  own helper after the C901 census flagged the inline form (complexity 11)
  — extraction over baseline stamp.
- **Suite:** full `pytest -q -n auto` (posix-shell gate satisfied):
  1689 passed / 7 skipped / 1 failed — the sole failure the standing
  WI-357 work-branch conditional, re-green on trunk.
  `check_trajectory.py --strict` exit 0.
