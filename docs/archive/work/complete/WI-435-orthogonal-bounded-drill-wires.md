+++
id = "WI-435"
title = "Replace the focused When/How drill wires with bounded orthogonal routes and explicit connectors. The owner-supplied 2026-08-12 renders show a selected How edge leaving through the top of the SVG, two incoming paths visually merging before CMP-004, arrowheads disappearing at the port layer, and roadmap routes forming diagonal cusps at lane turns. First harden the tests: inspect both axes of every routed path against its viewBox, require drill routes to use only rectilinear segments, require distinct per-edge connector positions when a port is shared, and keep a visible direction marker outside the destination connector. Then render square/orthogonal wires with round joins, individual connector circles, reserved routing gutters, and complete viewBox containment. Preserve focused blue-in/amber-out semantics, exact Needs/Unlocks text, keyboard interaction, offline single-file output, obstacle avoidance, and the existing hierarchy."
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Completed 2026-08-12. The shared drill view now retains the obstacle-aware
router's clear corridors but emits them as orthogonal `M/L` paths with rounded
stroke joins. When several edges share a node side, each terminates at its own
blue input or amber output connector circle instead of collapsing into one
centre-port wedge. Focused direction markers are 12px and use a unique id per
SVG layer; the prior document emitted 50 copies of `drillarrow-out`, so a
visible path could resolve its marker through a hidden layer's duplicate id.

Backward edges receive a bounded top/bottom routing gutter. The SVG frame now
measures path ink on all four sides rather than only left/right, closing the
exact `CMP-004 → CMP-002` vertical clip (`y=-9.1` against a `y=0` viewBox).
Square bend candidates are checked against unrelated boxes; when a midpoint
elbow would create a new crossing, the router chooses a clear obstacle boundary.
The interface registry is unchanged: these circles represent rendered
connections on the existing producer-to-consumer seams, not new interfaces.

Verification:

- The renderer/view/panel regression set passed: 107 passed.
  <!-- fig: cmd="python -m pytest -q tests/test_traj_render.py tests/test_traj_views.py tests/test_traj_panels.py" rev=this-worktree -->
- The focused geometry family passed: 16 passed, including vertical viewBox
  containment, shared-port separation, orthogonal vocabulary, marker uniqueness,
  and the existing no-through-box sweep.
  <!-- fig: cmd="python -m pytest -q tests/test_traj_graph.py -k 'route or port_fan or svg or t8 or orthogonal'" rev=this-worktree -->
- Playwright selected `CMP-004` and confirmed three distinct incoming blue
  connectors, two outgoing amber connectors, visible arrowheads, and zero
  duplicate marker ids. The selected roadmap uses complete 90-degree routes.
- The declared 36-shot light/dark desktop/mobile matrix is the final perceptual
  verification recipe.
  <!-- fig: cmd="node scripts/dashboard-shots/shoot.mjs" rev=this-worktree -->

No package, external runtime, dependency-ledger row, or interface-definition
change was added.

## Context

Follow-up to WI-434 after reading the selected-state pixels rather than only the
default screenshot matrix. The owner-supplied How screenshot selects `CMP-004`:
the amber `CMP-004 → CMP-002` wraparound reaches y=-9.1 while the SVG viewBox
still begins at y=0; the blue `CMP-002/CMP-005 → CMP-004` paths converge into a
small wedge at one centre port; and no arrowhead remains visually attributable.
The selected roadmap screenshot shows the same cubic router producing acute
diagonal-to-lane cusps. These are geometry and visual-contract defects, not a
reason to change the interface registry.

Baseline reproduction belongs under
`scripts/dashboard-shots/shots/before/WI-435-*.png`; the declared matrix remains
`node scripts/dashboard-shots/shoot.mjs`.
