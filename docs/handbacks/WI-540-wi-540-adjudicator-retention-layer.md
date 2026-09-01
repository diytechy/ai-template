+++
wi = "WI-540"
branch = "wi-540-adjudicator-retention-layer"
claimed_outcome = "partial"
reason = "worker exit 4"
commit_range = "9abdb5d982..a83418f58c"
suggested_tier = "medium"
keep_commits = []
discard_commits = []
split_decided_by = "adjudicator"
+++

## What happened

Lane `wi-540-adjudicator-retention-layer` closed `WI-540` as **partial**: worker exit 4

The work so far is in trunk, not on a branch — the lane merges like any
other. Read it with `git log --oneline 9abdb5d982..a83418f58c` / `git diff 9abdb5d982..a83418f58c`.

## Delivered

_(the close named nothing as delivered)_

## Not delivered

The worker exited 4 before moving its specs out of active/wi-540-adjudicator-retention-layer/, so nothing in this row's Done-when can be assumed met. Read the commit range above.

## Keep / discard

- **keep**: (none)
- **discard**: (none)
- **decided by**: adjudicator

The closing party could not judge this work — a dispatcher closing a lane whose worker exited or crashed has no view of it. The split is therefore OWED, and the disposition row minted for this close is what owes it: read the commit range, decide which commits survive, and mint a corrective successor for anything that should not.
