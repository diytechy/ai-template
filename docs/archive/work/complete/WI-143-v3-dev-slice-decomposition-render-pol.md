+++
id = "WI-143"
title = "[v3] dev slice: decomposition render polish (columns/arrows/hover)"
workstream = "dashboard"
sr_refs = ["SR-070"]
needs = ["WI-135", "WI-145"]
order = 142
+++

## Deliverable

SR-056 shipped in gen_trajectory.py: right-sized tier columns (declared MAX_TIER_COL bound; narrower where content allows), one horizontal parent->child containment arrow per descend edge (class=cedge), and a persistent last-hovered highlight keyed to data-node (no flash-on-exit). Folded OI-10: leaf wi_block hover title now carries the delivery Phase, and the SR-051/LLR-052/TC-052 threshold wording reconciled (>3 = When-view tiers; How-SW = WI-073 containerization bounded at TOP_VIEW_MAX). LLR-057/TC-057 Verified; 3 TC-057 cases + 1 OI-10 leaf-phase case.
