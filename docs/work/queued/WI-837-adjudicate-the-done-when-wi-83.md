+++
id = "WI-837"
title = "adjudicate the Done-when WI-835 changed in its own lane wi-835 - does the close still answer the row as claimed? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = "docs/archive/work/complete/WI-835-coordinator-retained-adjudication.md"
buildtier = "medium"
safety_class = "adjudication"
+++

## Context

`docs/archive/work/complete/WI-835-coordinator-retained-adjudication.md` closed with a Done-when that differs from the one it was claimed with (ticks and trailing evidence already set aside). A reviewer maps coverage against that list, so a change made by the lane it judges is the goalposts moving:

- at claim, no longer present as written: 'the governing template identity;'
- added since claim: "the operator's template overrides, from which the keep operation derives the governing template identity over every retained class, so a switch between retained classes is not a rule change (owner-confirmed scope, 2026-10-06, after the first live run);"
- added since claim: "This repo's `[adjudicator] retain_for` gains `first-approval`, so the coordinator's in-lane first approvals use the retained session too (owner, 2026-10-05, overruling docs/decisions/wi-835.toml#D-007). The shipped template's list is unchanged."

Judge whether each change only clarifies or moves the scope. A moved scope is a successor row, never a reversal - the merge stands.
