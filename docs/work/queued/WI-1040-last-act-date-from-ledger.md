+++
id = "WI-1040"
title = "The re-acceptance brief dates the last acceptance from the act ledger, not from the newest status-line diff"
workstream = "process"
sr_refs = []
needs = []
specref = "docs/reviews/2026-11-history-readers/README.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, class (c)
site 1 (`docs/reviews/2026-11-history-readers/README.md`).

The re-acceptance brief's heading names when the last acceptance act
happened. Today the date is recomputed from history: the newest commit
whose diff adds or removes a `status =` line in a snapshotted registry. The
function's own docstring grants that this also matches a row addition or a
new draft, so the heading can name a commit that accepted nothing. The rule
it breaks: a decision is recorded at its event and read from that record,
never recomputed (PROCESS.md §3; the review-churn plan's item 2).

The record already exists. An act made through `intake.py snapshot` appends
an entry to the act ledger (`docs/archive/last_accepted/acts.toml`) with its
date, and the commit that added the entry is the act's own commit, read the
way the accepted-risk reader already reads it (class (b) in the audit). No
LLR names the function, so no accepted row changes.

## Done-when

- [ ] The brief's heading reads the newest ledger entry and the commit that
      added it; with no ledger, or an empty one, it says no act is recorded
      instead of guessing.
- [ ] A test shows a row addition or a new draft after the last act no
      longer moves the heading's date, and fails on today's code.
- [ ] The audit note's site 1 is marked resolved by this row.
