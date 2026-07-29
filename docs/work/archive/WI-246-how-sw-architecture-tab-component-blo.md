+++
id = "WI-246"
title = "How (SW architecture) tab: component-block labels truncate with an ellipsis - widen or wrap so the full CMP name reads at default zoom (T4, 075-CRITIQUE)"
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "quick"
safety_class = "ordinary"
order = 243
+++

## Deliverable

CMP component-block labels in the containerized drill view (_drill_layer_svg, not the flat sw_graph fallback the finding pointed at) now wrap ID-Name onto an id line over a name line (a new _drill_block_label helper, the arch_icicle id/name idiom) instead of truncating - all 5 CMP names read in full at 1280px ('Unattended loop & floor' included), both themes. Built as one traincar with WI-247/248 (dd170fc); REVIEW-A opus APPROVE on this finding (0 issues); 077-CRITIQUE.md confirms in the re-rendered PNGs.
