+++
id = "WI-646"
title = "Scope the amendment brief to its own rows, and stamp the anchor copy per registry"
workstream = "scripts"
specref = ""
sr_refs = ["SR-146", "SR-148"]
needs = ["WI-645"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

- The amendment mint (`intake._amendment_drafts`) writes the rows it routes
  as a typed `Adjudicates` cell; `adjudicate_brief.amendment_values`
  intersects `trace.reattest_model` with that scope, renders a row under
  several SRs once, and refuses an unscoped row and a scope none of whose rows
  still differs, naming the rows.
- `baseline_snapshot.stamp(root, registry=None)` answers per registry; the
  brief's anchor line names each shown registry's own copy commit.
- Amended, left Approved for the joint adjudication: LLR-167 `detail`, TC-161
  `method` (its tier was already Full from WI-645).
- Tests in `tests/test_adjudicate_brief.py`, seen failing first; the review
  follow-up pinned the settled-row refusal on a live identical scoped row and
  the two-registry anchor with differently dated copies.

## Context

Found by the WI-641, WI-601 and WI-603 adjudications (2026-09-25), each of
whose briefs rendered the same twenty rows although each work item named one.
Two defects in the evidence the amendment brief carries:

1. **The brief renders the whole tree, not the row's scope.**
   `adjudicate_brief.amendment_values` renders every drifted approved row from
   `trace.reattest_model`, and `intake._amendment_drafts` writes no typed
   `Adjudicates` cell, so there is nothing to filter by. Every verdict then has
   to count its own scope by hand and list the rest as excluded (the rule
   WI-566's review corrected its own verdict to, and WI-573 applied). The same
   seventeen SR rows have been rendered to four adjudications.
2. **The anchor stamp names the newest write anywhere in the snapshot
   directory.** `baseline_snapshot.stamp()` returned cde260dd (2026-09-06),
   which copied `stakeholder-needs.toml` alone; the rows judged were measured
   against the requirements copy written at 27a30842 and the design-row copy
   written at 2e1197fd. A judge reading the stamp is told the wrong provenance
   for the text under judgement.

IN SCOPE: the amendment mint writes a typed `Adjudicates` cell from the rows it
routes, as the first-approval mint does; `amendment_values` intersects the
re-attestation model with that scope and refuses an empty one, mirroring
`first_approval_values`' WI-572 rule; the template's `{rows}` note says the
listing is scope-bounded; the baseline line names the copy each shown
registry was last written at. Tests pin that a one-row mint renders one row,
that an unscoped amendment row refuses, and that the stamp is per registry.
Recorded in the arbitration of the three verdicts' scoping (Fable, 2026-09-25).

NOT IN SCOPE: the seam WI-593 recorded, that a CLARITY verdict never re-anchors
the record so the same rows resurface until an approval act copies their
registry. That is a separate question about who re-anchors on CLARITY.

## Done-when

- A new amendment row carries its `Adjudicates` scope, and its brief shows only
  those rows; an amendment row with no scope refuses, naming why.
- The baseline line names, for each registry shown, the commit that last wrote
  its copy.
- Each change is driven by a test seen failing first, and the design row that
  describes `amendment_values` says so (an amendment of an approved row, left
  for adjudication).
- The commit bar and `trace.py --strict-integrity` pass.
