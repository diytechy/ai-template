+++
id = "WI-838"
title = "A route's first retained mint takes the lease, so two first calls cannot both mint"
workstream = "process"
sr_refs = ["SR-227"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

## Deliverable

A route's first retained call now writes a lease-only record (`family`, `route_id`, `lease`) under the store lock before it launches, so a second first call meets the lease, waits up to `lease_wait`, and runs unretained, as it does for a held session; two first calls can no longer both mint. A mint lands only while the record still carries its own lease, so a late first mint never replaces the record of the call that took its lease over, whether that call still runs or has finished (D-002). An abandoned first mint removes its lease-only record; a crashed one's lease expires and is retired as an unreleased lease is. Dial 0 writes nothing. Rows: LLR-270 re-attested after adjudication 002 (MEANING, blessed; 001 returned it for two dropped general clauses, answered in the lane), TC-329 approved (003); IF-247 (Drafted) names the record file and its three shapes. Codex 6.1 Sol: three rounds, the third SOUND (`01d21b26`). Decisions: `docs/decisions/wi-838.toml`.

## Context

Filed by hand by the wave-17 coordinator on 2026-10-06, from the first live run
of the coordinator's adjudication entry point. `session_keep._hold` writes the
route's lease only when a record already exists (`if record is not None`). On a
route's first retained call, nothing records that a mint is in flight, so two
calls starting together both mint, and the second bookkeeping replaces the
first session's record. SR-227 requires that no two calls use one retained
session at once. A pair of first calls is the case the lease leaves open. This
gap predates WI-835 (LLR-270's mint path).

## Done-when

- A covered call on a route with no record writes a record holding only the
  lease under the store lock, before it launches. A second call meeting that
  lease waits and then runs unretained, as it does for a held session today.
  `keep_bookkeep` and `keep_abandon` complete or remove the record.
- Tests: two concurrent first calls produce one minted session and one
  unretained call; a crashed first call's lease expires and is retired as an
  unreleased lease is today. Dial 0 still writes nothing.
- LLR-270's rows state it and pass adjudication on the one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.

## Adjudication follow-ups, answered in this lane

Adjudication 001 (`docs/reviews/wi-838-first-mint-takes-a-lease/001-ADJUDICATE-1e1e27c.md`) returned LLR-270 and drafted its follow-up as a `## Dispositions` block. Under the owner's ruling of 2026-10-06 (a returned row is answered in the lane, not minted), it is answered here:

- LLR-270 `detail` states the general lease wait (keep_for waits up to lease_wait on any lease another call holds, then runs unretained saying why) and the release (keep_bookkeep and keep_abandon release the lease) again, beside the first-mint text, with no behaviour change (`16ecfd7e`). The re-sit judges it.
