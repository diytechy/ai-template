+++
wi = "WI-484"
branch = "wi484-concern-refs-component-view"
claimed_outcome = "partial"
reason = "worker exit 3"
commit_range = "9ab30d641c..0bc7902f6d"
suggested_tier = "medium"
keep_commits = []
discard_commits = []
split_decided_by = "adjudicator"
+++

## What happened

Lane `wi484-concern-refs-component-view` closed `WI-484` as **partial**: worker exit 3

The work so far is in trunk, not on a branch — the lane merges like any
other. Read it with `git log --oneline 9ab30d641c..0bc7902f6d` / `git diff 9ab30d641c..0bc7902f6d`.

## Delivered

_(the close named nothing as delivered)_

## Not delivered

The worker exited 3 before moving its specs out of active/wi484-concern-refs-component-view/, so nothing in this row's Done-when can be assumed met. Read the commit range above.

## Keep / discard

- **keep**: (none)
- **discard**: (none)
- **decided by**: adjudicator

The closing party could not judge this work — a dispatcher closing a lane whose worker exited or crashed has no view of it. The split is therefore OWED, and the disposition row minted for this close is what owes it: read the commit range, decide which commits survive, and mint a corrective successor for anything that should not.
