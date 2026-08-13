## 2026-08-12 — Bounded orthogonal dependency wires

**Why.** The selected-state pixels after WI-434 exposed four defects the first
pass's tests did not bind: a How route reached `y=-9.1` outside a y=0 viewBox,
incoming paths visually fused at one centre port, duplicate marker ids hid
arrowheads, and curved lane transitions formed acute roadmap cusps. The finding
and its rendered baselines are recorded in
[WI-435](../work/complete/WI-435-orthogonal-bounded-drill-wires.md).

**What changed.** [The generated dashboard](../../PROJECT_STATE.html) now draws
When/How drill dependencies as obstacle-checked orthogonal paths, exposes one
connector circle per edge on a shared node side, reserves routing gutters for
backward edges, scopes arrow markers per SVG layer, and pads viewBoxes on all
four sides. Focused blue-in/amber-out behavior, exact relationship text,
drill-down, keyboard operation, and the offline single-file contract remain.
No external dependency or interface-registry change was needed.

**Verification.** Renderer/view/panel suite: **107 passed**; focused routing
family: **16 passed**; the final declared render matrix writes **36 shots** and
the selected `CMP-004` Playwright check reports zero duplicate marker ids.
<!-- fig: cmd="python -m pytest -q tests/test_traj_render.py tests/test_traj_views.py tests/test_traj_panels.py" rev=this-worktree -->
<!-- fig: cmd="python -m pytest -q tests/test_traj_graph.py -k 'route or port_fan or svg or t8 or orthogonal'" rev=this-worktree -->
<!-- fig: cmd="node scripts/dashboard-shots/shoot.mjs" rev=this-worktree -->

**Deviations / budgets.** None. No budget-watched file changed.
