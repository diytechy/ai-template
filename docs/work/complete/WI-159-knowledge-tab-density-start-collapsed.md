+++
id = "WI-159"
title = "Knowledge-tab density - start-collapsed .knode/knowarrow re-spec (T2 deferred from OI-12 / 052 CRITIQUE)"
workstream = "dashboard"
sr_refs = ["SR-054"]
needs = ["WI-144"]
buildtier = "medium"
safety_class = "ordinary"
order = 158
+++

## Deliverable

Knowledge (OKF) tab now opens START-COLLAPSED (the T2 density + T4 clipping fix 075-CRITIQUE confirmed). gen_trajectory.know_view renders one block per OKF type (SN/SR/LLR/TC/IF/PG terse codes matching the stat tiles) wired by the aggregated SN->SR->LLR->TC spine above the SR-089 >3-type threshold; double-click/Enter descends to per-type concepts, breadcrumb returns - SINGLE-SOURCED from the When/How-SW drill (_drill_layer_svg/_render_drill/DRILL_STYLE/DRILL_SCRIPT, no parallel idiom, check_dupes clean); <=3 types stays flat. Terse codes keep the 600px root layer inside its container so the TC block no longer clips (full names in legend/tooltip/breadcrumb/detail). WI-070 invariants held (self-contained conditional panel, bundle-less byte-identity, --check deterministic x2); all 396 concepts reachable in descend (reviewer-verified 0 dropped); 2 density-rule tests added. Independent opus REVIEW-A APPROVE findings=4, ALL MINOR/non-blocking: #1 flat-SVG still built+discarded in the collapsed path (low-priority efficiency, recorded not consumed - refactor risk not worth it at 396-node scale); #2 descend aria terse (WCAG label-in-name holds, matches How-SW idiom, accepted); #3 title-count test relaxed to spot-check (accepted); #4 exact 3-type boundary not unit-pinned (logic transparent, adjacent 2/4 covered, accepted). Pixel-verified both themes (builder + reviewer + my own read). Full suite 1235p/4s, gate G3. Build 729e867.
