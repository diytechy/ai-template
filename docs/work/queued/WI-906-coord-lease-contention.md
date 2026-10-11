+++
id = "WI-906"
title = "A coordinator-lease hook that meets store-lock contention never leaves the lease with an ended session"
workstream = "process"
specref = "docs/work/README.md"
sr_refs = ["SR-229", "SR-230"]
needs = ["WI-858"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-11 (coordinator-2026-10-11
D-003), split from WI-858's check of `coordinator_guard`'s lock sites as a
sibling of its class. The coordinator lease (`out/` lease store, the same
`dir_lock` primitive with a ten-second wait) has no expiry, so contention
there never retires a healthy holder, which is WI-858's harm. It can leave the
lease held until a human releases it:

- `session_end` (the exit hook) acquires the relaunch request under the lock;
  a `StoreBusy` there is caught and printed by `_hook_main`, so the successor
  is not launched, `relaunch.json` stays, and the ended session keeps the
  lease. Every later `take` and every non-holder claim is refused until the
  owner runs `release`.
- `on_session_start` installs a successor's take under the lock; a
  `StoreBusy` loses the take, so the old holder keeps the lease and the
  successor's claims are refused.
- `hand_back` and `release` are CLI calls: a `StoreBusy` exits with a
  traceback and the lease stays, but the caller sees it and can rerun.

## Done-when

- A contended exit or session-start hook does not lose the relaunch
  request or the successor's take: either is recorded durably and applied by
  the next locked access, or the hook waits it out within a stated bound, as
  the scope critique's Trust section rules.
- `hand_back` and `release` under contention fail with a one-line message
  naming the rerun, not a traceback.
- Tests: the lease lock held across `session_end` and across
  `on_session_start`; the lease ends with the successor, not the ended
  session.
- LLR-300 and LLR-301's details and their TCs say this, and those rows pass
  in-lane adjudication.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.

The row owes its scope critique and a `## Trust` section (the lease store's
producers, consumers and a ruling per consumer) before its claim.
