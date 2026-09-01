+++
wi = "WI-508"
branch = "wi508-architectural-remap"
claimed_outcome = "partial"
reason = "OI-71 RULED (c): the wi508 lane ran 19 review rounds and stopped at round 019's three MAJORs (two trunk-side renderer defects since fixed by WI-554; one the SR-163 tension ruled by OI-72). The owner ruled it closes PARTIAL through the kit's own path — nothing discarded, the evidence preserved in history, a successor re-lands the reviewed spine content from the preserved record."
commit_range = "ff29fef8f9..6ba2711078"
suggested_tier = "strong"
keep_commits = []
discard_commits = []
split_decided_by = "adjudicator"
+++

## What happened

Lane `wi508-architectural-remap` closed `WI-508` as **partial**: OI-71 RULED (c): the wi508 lane ran 19 review rounds and stopped at round 019's three MAJORs (two trunk-side renderer defects since fixed by WI-554; one the SR-163 tension ruled by OI-72). The owner ruled it closes PARTIAL through the kit's own path — nothing discarded, the evidence preserved in history, a successor re-lands the reviewed spine content from the preserved record.

The work so far is in trunk, not on a branch — the lane merges like any
other. Read it with `git log --oneline ff29fef8f9..6ba2711078` / `git diff ff29fef8f9..6ba2711078`.

## Delivered

The four Drafted slice-1 spine rows for SR-163's DELIVERED arms (~4 lines of low-level-requirements.toml, ~10 of test-cases.toml, auto-merging clean per handoff §1.4), plus 19 rounds of review evidence and the compiled rollup `docs/reviews/WI-508-REVIEW-A.md` — all preserved in the commit range and on `origin/wi508-architectural-remap-HELD-for-owner-verdict`.

## Not delivered

The SR-163 direct-TC shape (ruled by OI-72; owned by the re-scoped WI-543) and a fresh reviewer round on a refreshed tree. The successor re-lands the LIVE registry edits and REGENERATES docs/archive/last_approved/ via intake.py snapshot at its own approval commit — never copied from the branch's snapshot bytes (the ruling's degradation-risk condition).

## Keep / discard

- **keep**: (none)
- **discard**: (none)
- **decided by**: adjudicator

The closing party could not judge this work — a dispatcher closing a lane whose worker exited or crashed has no view of it. The split is therefore OWED, and the disposition row minted for this close is what owes it: read the commit range, decide which commits survive, and mint a corrective successor for anything that should not.
