+++
id = "WI-1019"
title = "An LLR states WI-1001's rule that an accepted automated test case no test tag names is a finding"
workstream = "process"
sr_refs = ["SR-157"]
specref = "docs/archive/work/complete/WI-1017-llrs-yield-to-design.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk at WI-1017's landing (2026-11-21), from the evidence sample
in its Deliverable ("Causes outside the guidance", row 2; case B10).

WI-1001 built the rule that an accepted automated TC no test tag names is a
finding. No LLR states it: TC-428 and TC-429 verify SR-157 directly. Its
builder stopped at the accepted row, since whether LLR-366 is amended or a
new LLR is minted was the operator's call, and nothing filed the gap.

## Done-when

- [ ] The scope critique chooses between amending LLR-366 (`Accepted`; text
      only, drifting for the operator's re-accept) and minting a `Drafted`
      LLR under SR-157, and the chosen row states the rule as built.
- [ ] TC-428 and TC-429 verify that LLR, and `trace.py --strict` stays clean.
