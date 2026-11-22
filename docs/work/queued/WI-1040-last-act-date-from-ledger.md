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
planmode = "single"
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
      added it. With no ledger, or an empty one, it says no act is recorded
      instead of guessing. When the newest entry is present but the commit
      that added it is not in the readable history (a shallow clone, the
      limit IF-217 already states), the heading gives the entry's recorded
      date and says its commit is not in the available history; it never
      falls back to another commit. The promise covers supported workflows
      and the ledger as the kit writes it; a hand-edited ledger is outside
      it.
- [ ] A test covers each of those states, and one shows that a row addition
      or a new draft after the last act no longer moves the heading's date,
      failing on today's code.
- [ ] The audit note's site 1 is marked resolved by this row.
