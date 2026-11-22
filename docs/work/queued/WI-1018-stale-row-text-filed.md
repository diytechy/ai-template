+++
id = "WI-1018"
title = "Row text a lane leaves behind its code is filed as work, and the first set of stale LLRs is brought up to the code"
workstream = "process"
sr_refs = ["SR-186"]
specref = "docs/archive/work/complete/WI-1017-llrs-yield-to-design.md"
buildtier = "medium"
safety_class = "ordinary"
needs = ["WI-1028"]
priority = 3
+++

## Context

Filed on trunk at WI-1017's landing (2026-11-21), from the evidence sample
in its Deliverable ("Causes outside the guidance", row 1; cases B1 to B9).

A lane that finds an LLR's text stale after its gate leaves it: the rule
that a MINOR after the gate never moves the gated tip (`coordinator-cycle`
recipes §3, wi-935 D-005), and the cost of re-sitting or re-accepting a row,
send the finding to `docs/status.md`'s unfiled follow-ups or to nowhere.
Of the nine cases sampled, only B5 has been fixed since (by WI-1010).

The first set, from the sample: LLR-273's `module` (B1), LLR-150 (B2),
LLR-123's rationale (B3), LLR-362 (B4), LLR-153's label (B6), LLR-312 (B7),
and LLR-172 with TC-166 (B9). Most are `Accepted`, so their amendments are
text only and drift for the operator's re-accept.

WI-1015 clears the drift between LLR CodeSymbol cells and the code, and
variant F (the review-churn plan's pointer rules, ruled and unbuilt) retires
the `module` and `code_symbol` cells. Whichever lands first takes the cases
it covers (B1, B7 and B9's symbol) out of this row's set.

**Added at F-3's merge (2026-11-22).** F-3 (WI-1023) removed the cells, so
B1, B7 and B9's symbol leave the set. Its review found one more stale row it did
not amend: SR-221 (`Accepted`) still says "for a module a design row names",
though design rows now name no module; the files realizing a row are read
from the code's back-links. It joins the first set.

## Done-when

- [ ] A stale-row finding a lane does not fix is filed as a queued row, or
      named in the work item of the next lane that touches the row, so it
      cannot lapse; the coordinator's recipe says so where the post-gate
      rule is stated.
- [ ] The first set above is amended to the code, each `Accepted` row's
      text only, for the operator's re-accept; a case another row has
      already fixed is named and skipped.
