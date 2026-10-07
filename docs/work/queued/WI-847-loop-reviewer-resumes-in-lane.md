+++
id = "WI-847"
title = "The loop's reviewer resumes within a lane's iteration, and the merge-gating review is always fresh and full-lane"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/log.d/2026-10-06-wave18-coordinator.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by the wave-18 coordinator on 2026-10-07. The owner confirmed it for the
hand path that day: narrow rounds resume the reviewer while a lane iterates,
and the last review before a landing is a fresh, full-lane review from the
lane's trunk base to its tip. Today the loop's reviewer is never retained
(`session_keep.keep_for` covers only ADJUDICATE). Every loop review round is
a fresh, full-lane session, so the merge gate is already right, but each round
pays the full context cost again. On WI-841 the hand path's fresh Sol rounds
cost 115k to 160k tokens each, mostly re-reading the same context, and they
hit the Codex plan limit twice.

## Done-when

- The loop's REVIEW role can resume its session within one lane's review
  chain, through the same keep operation, the store and the lease
  (`retain_for` gains the review class behind its own dial; shipped off).
- The review that gates a merge is always a fresh session over the full lane
  (claim base to tip), never a resumed one.
- Tests: two iteration rounds resume one session; the merge-gating round mints
  fresh and covers the claim base to the tip; dial off changes nothing.
- SR-227's rows state it and pass adjudication on the one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
