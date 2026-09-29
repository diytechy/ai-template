+++
id = "WI-727"
title = "Bound the real-scale wire-routing tests: one test_traj_graph case takes 790 s alone and sets the full suite's critical path"
workstream = "process"
specref = "tests/test_traj_graph.py"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by WI-721, whose Done-when asked that a regression large enough to
explain the full suite's wall-time jump be fixed or filed.

- **The full suite:** at e86cae4f plus WI-721 it ran `4816 passed, 15
  skipped in 4998.50s (1:23:18)` under load. The wave-5 close measured 111
  minutes, and the suite was recorded at about 10 minutes before that.
- **The slowest tests** (`--durations=30`):
  - `tests/test_traj_graph.py::test_meta_knowledge_and_when_wires_avoid_unrelated_boxes`
    at 1160.6 s;
  - `test_fallback_dag_and_sw_graph_wires_avoid_unrelated_boxes` at 392.7 s;
  - `tests/test_prereq_toolchain.py::test_a_gate_closed_run_announces_itself_at_both_ends`
    at 291.1 s.
- **Run alone** on a mostly quiet box, the first takes **790.5 s** of call
  time (`1 passed in 965.37s`). No parallelism can finish the suite faster
  than that one test.
- **The likely cause is growth, not a code change.** Both graph tests route
  wires over diagrams built from this repository's LIVE registries (the
  test's own comment: "same spine, same scale"). `rendering/traj_graph.py`
  has not changed since cde260dd (2026-09-06), while the spine and work
  registry have kept growing, so the router's cost grows super-linearly with
  them. That is unmeasured; the first step is to confirm it.

## Done-when

- **Profile** the router on the live meta Knowledge and When graphs, and
  name what dominates: node count, wire count, the obstacle search, or the
  through-box check.
- **Fix** that cost where it is a real inefficiency (the dashboard
  generator pays it too, on every regeneration); otherwise bound the tests.
  Keep the T8 through-box invariant exercised at a real scale, for example
  with a pinned snapshot of the live graph sized to catch the regression
  class. Do not simply drop it to a toy graph.
- **Measure:** the case runs in under 120 s alone on this box, and the full
  suite's slowest-30 list is re-measured and recorded.
- **Also look at** `test_prereq_toolchain`'s 291 s case, and fix it or
  explain it.
