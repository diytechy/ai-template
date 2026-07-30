## 2026-07-30 — WI-368: the integrator runs the composed tree's own harness

The first queue merge of a generator change (WI-366's renderer) was refused
by the merge commit's own freshness floor: `_run_trunk_step` executed
`SCRIPTS/trunk_step.py` — the *running* integrate.py's directory, i.e. the
trunk checkout — so the §5.2 regen wrote the candidate's artifacts with
trunk-vintage generators, and the floor (running the merged vintage)
correctly called them stale. Reproduced deterministically in both
directions before fixing: trunk step against the merged candidate → STALE;
the candidate's own step against the same tree → floor and bar green.
Latent until now because the grind sessions committed attended-serial
(RULING-8); the queue had never merged a generator change.

- **Deliverable:** `_composed_tree_script(wt, root, name)` in
  [integrate.py](../../project-trajectory/scripts/integrate.py) — the
  invoker's root-relative layout joined onto the candidate first, then the
  known layouts, falling back to the invoker's copy — used by BOTH
  `_run_trunk_step` and `_run_bar` (§4's "required checks on the composed
  tree" applied to the checker itself; discovery mirrors the shipped hook's
  scripts-dir probe). Spec archived:
  [WI-368](../work/archive/WI-368-the-integrator-runs-the-invokers-harness.md).
- **Tests:** tests/test_integrate.py §4b — the three resolution shapes plus
  a seam test non-vacuous against the pre-fix wiring (the invoker's copy
  exits 3, the composed copy writes a sentinel).
- **Deviations from spec:** none.
- **Suite:** full `pytest -q -n auto` (posix-shell gate satisfied):
  1670 passed / 11 skipped / 2 failed. One failure is the standing
  work-branch conditional (`test_this_repo_is_not_a_work_branch`, red
  branch-wide by WI-357 design, re-greens on trunk). The other —
  `test_scaffold_omissions_list_is_current` — is NOT this branch's and does
  not re-green at close: the declared absence `docs/work/active/`
  materializes whenever ANY claim is outstanding, so the honesty test reds
  every tree (and every composed-tree bar) while the §2.3 parallel-claims
  model is in use. Filed as its own item (WI-369) rather than papered over
  here. `check_trajectory.py --strict` exit 0.
