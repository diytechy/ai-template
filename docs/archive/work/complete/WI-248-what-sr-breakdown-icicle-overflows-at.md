+++
id = "WI-248"
title = "What (SR breakdown) icicle overflows at 390px - LLR/TC need horizontal scroll; add a reflow/scroll affordance at mobile width (T7, 075-CRITIQUE)"
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "quick"
safety_class = "ordinary"
order = 245
+++

## Deliverable

NO CODE CHANGE - honest re-verification. This finding carried forward from WI-189 marked 'not independently re-verified'; rendering the arch tab at 390px (both themes) shows the WI-219 _hscroll/SCROLL_CUE idiom already working: the scroll cue renders above the icicle, the .view container clips at the SR column's right edge, LLR/TC reachable by horizontal scroll, page body does not overflow. Confirmed independently by the builder, REVIEW-A, and this critic (077-CRITIQUE.md) - three independent renders, same conclusion.
