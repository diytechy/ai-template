+++
id = "WI-609"
title = "Point the reviewer brief at the work item's own spec, not the empty docs/specs folder (review pack C5)"
workstream = "process"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

## Context

Found by the 2026-09-24 code-facts research; filed by the owner from the
review pack's Part C.

`prompts/reviewer.template.md:39` sends reviewers to "the docs/specs
spec-of-record for the open work item", but `docs/specs/` here holds only its
README and example: specs now live in the work-item files under `docs/work/`.
The same brief already maps coverage against the work items' Done-when. The
brief is shipped, so check whether the change needs a RESYNC entry.

## Done-when

- The reviewer brief names the work item's own spec file (and its `specref`,
  where that points elsewhere) as the spec of record.
- No shipped prompt still points at `docs/specs` as where open work lives
  (grep evidence quoted).
- The prompt and byte-budget tests stay green.
