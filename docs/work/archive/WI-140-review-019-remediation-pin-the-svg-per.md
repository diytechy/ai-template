+++
id = "WI-140"
title = "Review 019 remediation - pin the SVG per-node title tooltip contract"
workstream = "scripts"
needs = ["WI-102"]
order = 139
+++

## Deliverable

WI-140 (2026-07-14, review 019's MINOR, driver-remediated with WI-139 - the round was left dangling by the NEEDS-HUMAN sittings that followed it): WI-102 added a <title> tooltip/a11y child to every SVG node across the four emitters, but the only changed assertion made the title OPTIONAL in a regex, so a regression removing the labels from any emitter stayed green. New tests/test_gen_trajectory.py::test_svg_nodes_carry_escaped_title_tooltips (smoke tier by default): one integration render over a fixture whose SR title, WI title, and IF counterpart carry markup-hostile characters (& <), pinning per emitter - arch_icicle (every cell has a title; SR tip escaped), dag_svg (every WI node; id-title-status tip escaped), sw_graph (kind-suffixed module + external tips escaped), know_graph (every knode; id-title-type tip escaped via the gen_okf bundle round-trip). No script change - test-only; the WI-102 contract is now regression-pinned.
