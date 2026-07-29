+++
id = "WI-319"
title = "Next-work card truncates its WI title with no reveal affordance (T4, 121-CRITIQUE MINOR) - the landing next-work surface WI-305 delivered renders the title as `...tiering expo...`, cut mid-word, and nothing visible tells a reader how to see the rest. Observed in 390px-light-arch-fold.png and 390px-dark-arch-fold.png AND at 1680px-light-arch-full.png, where the card has ample width left, so the budget is being applied regardless of available space rather than as a fit constraint. Note the T4 anchor text: truncated-WITHOUT-AFFORDANCE is the failure; an ellipsis that a reader can act on is not. Three honest fixes, cheapest first: let the title wrap, widen the budget to the space actually available, or make the card an operable control that opens the detail aside (which already exists for the graph views). Whichever is chosen, the guard belongs with WI-305's TC-120 next-work tests. RE-AFFIRMED against the amended SR-054 (2026-07-26, WI-321's prompt): the amendment removed the row's restatement of which critique anchors are live, moving that to the rubric alone. The requirement text this finding is judged against is unchanged, and the rubric still carries the anchor, so the finding stands as scoped."
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "quick"
safety_class = "ordinary"
order = 316
+++

## Deliverable

The landing next-work card stopped budgeting by CHARACTER COUNT: the WI Title's leading clause is emitted whole and the card's own width does the fitting (HTML already fits text to available space - the fixed 60 was the only thing preventing it). _NEXT_WORK_TITLE now bounds ONE item's height, measured over 320 rows (median 44, p90 126, max 609), and where it bites the remainder discloses through a NATIVE <details> cut at a word, so head and remainder rejoin continuously when opened - operable by pointer and keyboard with no script, which is what makes the affordance assertable from the markup. Bound into LLR-119/TC-124 as T4's second mechanized half; the document-wide truncated-WITHOUT-AFFORDANCE clause stays critique residue.
