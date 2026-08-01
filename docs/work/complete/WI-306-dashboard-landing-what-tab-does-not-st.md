+++
id = "WI-306"
title = "Dashboard landing (What) tab does not start-collapsed (119-CRITIQUE T2) - unlike the three wired tabs (When/How-SW/Knowledge, which correctly open at a summary layer per the SR-089 '>3' rule), the What tab's icicle renders all four lanes fully exploded (~340 blocks in this repo). Two visible consequences: the TC lane compresses to unlabelled 1-unit bars fading into a right-edge gradient, and the card clips the last row mid-block with only a sideways-scroll hint that says nothing about the vertical cut. Fix: apply the same start-collapsed threshold to the icicle (open at the SN lane, descend on click), or cap the rendered depth so the landing view is a summary; add a vertical affordance if it stays scrollable. Re-affirmed 2026-07-26 against the amended SR-054 (the T1/T3 ruling touches T1 and T3 only; T2 stays a live critique anchor and this defect is unaffected)."
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "medium"
safety_class = "ordinary"
order = 303
+++

## Deliverable

Delivered 2026-07-26. The landing What icicle now earns its tiering by scale: above the SR-089 >3 SN rule it renders a start-collapsed drill - one block per SN, descend-on-click into that SN's subtree - reusing _drill_layer_svg/_render_drill so the descend/breadcrumb idiom stays single-sourced with the When/How-SW/Knowledge views (U4 holds by construction). Capping DEPTH was rejected, with the reason stated at the branch: height is leaf-proportional, so stopping at the SR lane still stacks one unit per SR (~110). At or below 3 SNs the flat icicle renders BYTE-IDENTICALLY. Bound by widening LLR-099/TC-102 (T2's core) to the What view. Guards mutation-proven: disabling the tiering reds test_t2_what_icicle_starts_collapsed_above_the_sn_threshold, whose load-bearing assertion is that NO leaf cell appears in the opening layer - the wall itself. Ratchets re-stamped (5112->5156; arch_icicle complexity 20->23).
