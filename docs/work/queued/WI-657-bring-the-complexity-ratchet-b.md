+++
id = "WI-657"
title = "Bring the complexity ratchet back to green: re-stamp the improvements, argue or undo the growth, drop the moved paths"
workstream = "quality"
specref = "project-trajectory/scripts/check_complexity.py"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

`check_complexity.py --mode enforce` fails at b14d1808, so the
`[step:complexity]` step is red at any gate run. It first failed at 76a235bb.
Three kinds of finding:

- growth: `route_session` cognitive 37 -> 38, `trace.load_registries` 39 ->
  42, and a new unbaselined `tests/test_bookkeeping._whole_tree_git_calls`
  (25) (measured at HEAD by the backlog audit);
- improvements the ratchet wants re-stamped downward in the commit that made
  them (for example `agent_loop.run_iteration` 18 -> 16,
  `baseline_snapshot.refresh_ledger` 23 -> 21, `dispatch._advance` 20 -> 18);
- rows whose function is gone from the path the baseline names
  (`integrate._claim_refusal`, and the `traj_graph.py`, `traj_panels.py`,
  `traj_render.py` and `traj_views.py` rows left behind when those modules
  moved under `rendering/`).

IN SCOPE: re-stamp the improvements downward; re-point or delete the rows
whose function moved or went; for each growth (`route_session`, `load_registries`,
`_whole_tree_git_calls`), either reduce it or re-stamp it upward with a reason a reader can argue with, and record
which in the log. Find why the per-commit bar did not catch the drift (the
ratchet test's tier, or a step the bar skips) and say so in the Deliverable.

NOT IN SCOPE: refactoring other functions to lower their numbers.

## Done-when

- `python project-trajectory/scripts/check_complexity.py --mode enforce`
  passes at the landing commit, and the Deliverable pastes its output.
- Every upward re-stamp carries its reason at the baseline entry.
- The commit bar passes.
