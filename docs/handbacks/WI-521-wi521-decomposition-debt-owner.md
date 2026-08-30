+++
wi = "WI-521"
branch = "wi521-decomposition-debt-owner"
claimed_outcome = "partial"
reason = "worker exit 4"
commit_range = "efcde754aa..378e90005b"
suggested_tier = "medium"
keep_commits = []
discard_commits = []
split_decided_by = "adjudicator"
+++

## What happened

Lane `wi521-decomposition-debt-owner` closed `WI-521` as **partial**: worker exit 4

The work so far is in trunk, not on a branch — the lane merges like any
other. Read it with `git log --oneline efcde754aa..378e90005b` / `git diff efcde754aa..378e90005b`.

## Delivered

_(the close named nothing as delivered)_

## Not delivered

The worker exited 4 before moving its specs out of active/wi521-decomposition-debt-owner/, so nothing in this row's Done-when can be assumed met. Read the commit range above.

## Keep / discard

- **keep**: (none)
- **discard**: (none)
- **decided by**: adjudicator

The closing party could not judge this work — a dispatcher closing a lane whose worker exited or crashed has no view of it. The split is therefore OWED, and the disposition row minted for this close is what owes it: read the commit range, decide which commits survive, and mint a corrective successor for anything that should not.
