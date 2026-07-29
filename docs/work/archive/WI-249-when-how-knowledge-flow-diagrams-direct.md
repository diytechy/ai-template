+++
id = "WI-249"
title = "When/How/Knowledge flow diagrams: directed-edge arrowheads were invisible (near-white --border fill / sub-pixel stroke-scaled markers) and multi-edge ports bunched into a knot - route every graph edge through one shared userSpaceOnUse arrow marker on theme tokens, trim edge ends clear of the port ring, and fan multi-edge ports across a small band"
workstream = "dashboard"
sr_refs = ["SR-052", "SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 246
+++

## Deliverable

New _arrow_markers() emits a shared <defs> marker (userSpaceOnUse so the triangle stays a fixed legible size regardless of a wire's stroke-width; classed, never inline-filled, so it follows --muted/--accent in both themes) adopted by dag_svg, sw_graph, know_graph and every _drill_layer_svg wire. dag_svg's .arrowhead moved off the near-white --border token to --muted; sw_graph/know_graph dropped their hardcoded #94a3b8 fills (now theme-aware .swedge/.kedge). New _port_fan() spreads wires sharing one port across a <=0.6*row_h band ordered by the far endpoint's row, killing the fan-in/out knot; wire ends trimmed PORT_R+2 px short of the target port ring so the arrowhead renders in the clear gap rather than under the later-painted port circle. Re-shot the When/How/Knowledge matrix (light+dark, 390/1280/1680) to confirm; full suite green.
