+++
id = "WI-858"
title = "A finished call's bookkeeping survives store-lock contention without retiring a healthy session"
workstream = "process"
specref = "docs/work/README.md"
sr_refs = ["SR-227"]
needs = ["WI-846"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand by the coordinator on 2026-10-08 from WI-846's review sweep
(stop item 1, a defect outside that row's surface, reported and not built).
WI-846's narrow Codex Sol review found that store-lock contention on an
authentication failure's lease release leaves the lease behind; once it
expires, the next call retires the session ("lease expired unreleased") and
mints afresh. WI-846 ends that for release-only paths with a lockless release
marker (the tombstone protocol `keep_abandon` already uses, in a release-only
mode).

The same class remains on the ordinary path. `session_keep.keep_bookkeep`
takes the store lock to fold a finished call in, apply the reset rules and
release the lease. Under contention `StoreBusy` escapes, the call's
observation is lost, and the lease stays to expire, so a healthy retained
session is retired later. Making it durable means the marker carries the
call's observation and its drain or retire decision, a wider change to the
store protocol than WI-846's.

`coordinator_guard.py` uses the same `dir_lock` primitive with a ten-second
wait for a different store (the coordinator lease); what a failed release
leaves there was not checked. Check it as a sibling site of this class.

WI-800 replaces the session store (`out/sessions/store.toml`); if it lands
first, this row's rule moves with the store.

## Done-when

- A finished call's bookkeeping under store-lock contention is not lost: the
  observation, the reset decision and the lease release are recorded durably
  without waiting on the lock, and applied by the next locked read before any
  expired-lease retirement.
- A healthy session whose bookkeeping met contention is resumed, not retired,
  by the next call.
- `coordinator_guard`'s lock sites are checked for the same class, and either
  fixed here or shown not to leave a lease behind.
- Tests: the store lock held across a successful call leaves no lease, keeps
  the call's observation, and the next call resumes the same session; the
  same with a call that should drain the session.
- LLR-270's detail and its TCs say this, and those rows pass in-lane
  adjudication.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
