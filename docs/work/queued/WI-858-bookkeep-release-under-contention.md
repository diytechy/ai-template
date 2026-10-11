+++
id = "WI-858"
title = "Every lease release and bookkeeping write survives store-lock contention without retiring a healthy session"
workstream = "process"
specref = "docs/work/README.md"
sr_refs = ["SR-227"]
needs = ["WI-846", "WI-887"]
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

**Owner ruling, 2026-10-08** ("Move it to WI-858"): store-lock contention
lives here for every path. WI-846's lockless release marker drew race
findings in three Codex Sol rounds running (the last: a reader deleting a
newer marker it never applied), so WI-846 drops it and releases its lease
under the lock; an authentication failure's release and the keep-warm skip
under contention are this row's, with the ordinary path, in one design.
The three rounds' findings are the design's test list; they are quoted in
`docs/decisions/wi-846.toml` (D-003 and D-005) once WI-846 lands.

WI-800 replaces the session store (`out/sessions/store.toml`); if it lands
first, this row's rule moves with the store.

## Deliverables and order

Written before the claim, answering the scope critique's S1 (coordinator
2026-10-11 D-003). This row has one landable deliverable: the session store
(`session_keep`, `out/adjudicator/`) keeps every call's bookkeeping and every
lease release through store-lock contention. The coordinator lease
(`coordinator_guard`, its own `dir_lock` store) was checked as a sibling site
and is not the same class: that lease has no `until` and nothing retires it,
so contention there never retires a healthy session. It does leave a lease
held until a human releases it (a contended `session_end` hook loses the
successor's launch and keeps the ended holder; a contended
`on_session_start` loses the successor's take), a different harm with
different consumers (the claim gate and the relaunch). That is filed as
WI-906 and lands after this row; this row does not change `coordinator_guard`.

## Trust

Durable bookkeeping gives a file authority over a lease's release and over a
session's retirement, so this section states the carrier, its producers, its
consumers and a ruling per consumer (coordinator 2026-10-11 D-004, for the
owner to confirm or overrule).

**One carrier.** A *store marker* is a JSON file written whole beside a
record (`_write_whole`: a temporary file, then a replace), in the store
directory under a suffix no record glob (`*.json`, `ANTHROPIC-*.json`)
matches. It names one record identity (family, route id, scope), the call's
lease holder, the session id and generation the call held (`Keep`), and one
kind: `bookkeep` (the call's raw observation: the outcome's usable flag, the
metrics `keep_bookkeep` reads, the compaction observation and the judged WI),
`release` (lease release only) or `retire` (the tombstone's reason). The
existing `.retire` tombstone becomes this carrier's `retire` kind: one
carrier, one reader. A marker's file name carries the record's stem and a
hash of its holder, so each call's marker has its own identity: a marker is
written once, never overwritten, and deleted only by name by the locked
reader that applied it (the WI-846 round 3 finding: a reader deleting a newer
release it never applied). The reset decision is not in the marker: it is
computed when the marker is applied, under the lock, by the code that
computes it today (`_landing`, `_observe`, `_retire`, `drain_reason`).

**Producers and write route.** Every lease release and bookkeeping write
publishes its marker FIRST, with no lock, then applies it under the lock if
the lock is had within a short wait: one route for every path, not a
fallback beside the locked one (the pattern `keep_abandon` already uses).
The producers are `keep_bookkeep` (ordinary and drain paths),
`keep_release` (an authentication failure, and a blackout refusal's release
in `session_service.act`), `keep_abandon` (a launch that raised), the
keep-warm ping's bookkeeping and release (through `act`), and
`retire_scope` (a lane's gating round retires its iteration reviewer). A
failed write is an `OSError` before the replace: no marker exists (a
leftover `*.tmp` matches no glob), the producer raises it to its caller, and
the lease follows the expiry rule. A partial marker cannot be observed (the
replace is whole). Contention on the apply is not a failure: the marker
stands for the next locked read.

**Consumers and rulings.**

- **Locked readers** (`load_honoured`, so `keep_for`, `keep_release`,
  `keep_bookkeep`, `keep_abandon`, `retire_scope` and `take_warm_lease`):
  read the clock first, then list the record's markers, apply each in
  publication order, then run `retire_stale_lease`, so no reader retires a
  lease whose release was published before it observed the lease expired
  (WI-846 round 2, finding 5). A marker applies under `_landing`'s rule: a
  resumed session's observation lands only on the record still holding that
  session, a mint's only while the record still carries that holder's lease;
  a marker that no longer lands releases its holder's lease, if still held,
  and is otherwise spent. Each applied or spent marker is deleted by name.
  An unreadable marker (an `OSError`, such as a sharing violation during a
  replace) is left in place, and the reader does not retire that record's
  expired lease on this read; a malformed one (unparseable, a missing field,
  or an identity that disagrees with its file name) is deleted with one
  stderr line and read as absent.
- **Lockless readers** (`due_routes` and its `_warm_candidates`,
  `scoped_route`, `_scoped_records`): fold the record's markers with the
  same pure function the locked reader applies, never deleting one, and
  decide on the folded record. A pending `bookkeep` or `release` marker
  never makes a record skipped; only a fold that retires it does (WI-846
  round 2, finding 4: a release marker made keep-warm skip the record, so
  nothing ever applied it). An unreadable or malformed marker is read as
  absent here.
- **The call's caller** (`session_service.act`, so `coordinator_adjudicate`,
  `agent_loop` and the keep-warm `_ping`): bookkeeping no longer raises
  `StoreBusy`, so the outcome returns and a blackout refusal surfaces as
  `BlackoutRefused`. When the apply was deferred, the row's `reset-reason`
  column reads `pending` and its `session-gen` is the call's own; telemetry
  readers take `pending` as not yet known.
- **The coordinator by hand** (the recipes' read of
  `out/adjudicator/*.json`): a record can lag its pending markers until the
  next locked read; the recipe says so.

**What the authority binds to.** A marker binds to one record identity, one
lease holder (minted per call: `<role>:<uuid>` in `keep_for`,
`keep-warm:<uuid>` in the warmer) and the session id and generation that
call held. It releases only that holder's lease and lands its observation
only on that session; it never authorizes a lease, a session or a record it
does not name.

## Done-when

- A finished call's bookkeeping under store-lock contention is not lost: the
  observation, the reset decision and the lease release are recorded durably
  without waiting on the lock, and applied by the next locked read before any
  expired-lease retirement.
- A healthy session whose bookkeeping met contention is resumed, not retired,
  by the next call.
- The same holds for every release-only path: an authentication failure's
  lease release (WI-846) and a keep-warm skip. No reader drops a release it
  has not applied, and no reader retires a lease whose release was published
  before it observed the lease expired.
- `coordinator_guard`'s lock sites are checked for the same class, and either
  fixed here or shown not to leave a lease behind. Checked before the claim
  (2026-10-11, `## Deliverables and order`): the coordinator lease has no
  expiry, so no site there retires a healthy holder; the lease a contended
  hook leaves held until a human releases it is WI-906's.
- Tests: the store lock held across a successful call leaves no lease, keeps
  the call's observation, and the next call resumes the same session; the
  same with a call that should drain the session.
- LLR-270's detail and its TCs say this, and those rows pass in-lane
  adjudication.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
