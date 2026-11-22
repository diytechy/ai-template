+++
id = "WI-1054"
title = "The flat How-SW graph's legend names the component nodes it draws"
workstream = "scripts"
sr_refs = ["SR-169"]
needs = []
specref = "docs/archive/work/complete/WI-1048-answer-wi-1047-verdict.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, from
WI-1048's Deliverable. Since F-2 (WI-1022) the flat How-SW graph draws
component nodes, but its legend lists only module, file and external actor
(`rendering/traj_views.py`, the legend spans near lines 960 and 1315). A
reader meets a node kind the key does not name.

## Done-when

- [ ] The flat graph's legend names every node kind it draws, the
      component node among them, with the swatch the node uses taken from
      the same token or class (no second copy of a colour).
- [ ] A test fails when the graph draws a node kind its legend omits.
