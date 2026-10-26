+++
id = "WI-982"
title = "Both adjudication routes widen a sitting's hats by the authoring work item's tags: the minted first-approval and amendment rows carry the merged lane's tags"
workstream = "process"
sr_refs = ["SR-161"]
specref = "docs/reviews/wi-976/004-ADJUDICATE-81e623b.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand by headless leg 23 (2026-10-26) at WI-976's landing, from
the SUCCESSOR ruling of WI-976's dispute sitting 004
(`docs/reviews/wi-976/004-ADJUDICATE-81e623b.md`, RB1-F1, accepted; its
duplicate RB3-F1 was dismissed by sitting 010, and the post-rebase round's
REVIEW-B re-raised the same class, `docs/decisions/wi-976.toml` D-028).

What is true: a decomposition round's hats are widened by the tags of the
row the sitting composer is handed. The coordinator's in-lane route hands
it the authoring lane's own row. The unattended route hands it the
merge-minted adjudication row, whose Workstream is always `process` and
whose SafetyClass is `adjudication` (it routes the row), so the authoring
work item's tags are lost and the hat set differs by route. The defect is
in the minted row's provenance, outside WI-976's declared surface.

The ruling, verbatim: "make both routes widen a sitting's parent needs by
the authoring work item's declared tags: carry the merged lane's
Workstream and SafetyClass (in a cell other than the routing SafetyClass)
or a link to it onto every minted first-approval and amendment row,
resolve the branchless sweep, state in LLR-360 that the authoring work
item's tags widen, and add a test that composes the minted row shape and
the in-lane shape for one SR and asserts one hat set".

Its scope critique runs before its claim (the `coordinator-cycle` skill,
section 1).

## Done-when

- [ ] Every minted first-approval and amendment row carries the merged
      lane's Workstream and SafetyClass, or a link to the authoring work
      item, in a cell other than the routing SafetyClass.
- [ ] The branchless sweep's case is resolved and stated.
- [ ] Both routes widen a sitting's parent needs by the authoring work
      item's declared tags, and LLR-360 states that it is the authoring
      work item's tags that widen.
- [ ] A test composes the minted row shape and the in-lane shape for one
      SR and asserts one hat set.
- [ ] The commit bar is green, and both strict lints are clean on the
      landing tip.
