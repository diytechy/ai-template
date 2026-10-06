+++
id = "WI-838"
title = "A route's first retained mint takes the lease, so two first calls cannot both mint"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/log.d/2026-10-06-wave17-coordinator.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 9
+++

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
