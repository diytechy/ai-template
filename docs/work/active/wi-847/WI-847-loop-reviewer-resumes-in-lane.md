+++
id = "WI-847"
title = "The loop's reviewer resumes within a lane's iteration, and the merge-gating review is always fresh and full-lane"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/log.d/2026-10-06-wave18-coordinator.md"
needs = ["WI-852", "WI-834"]
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

Landing order (scope critique, 2026-10-10; decisions
`coordinator-2026-10-10.toml` D-002): one row, built in this order inside
its lane. The narrow round's brief, rendered through `prompts.py`, comes
first; it stands alone, because every session is still fresh. Reviewer
retention and the merge gate's freshness binding come next, together: a
resumed reviewer without the binding could clear a merge, which is the
defect this row must not open.

## Trust

The row gives two files authority (decision D-003, for the owner to
confirm or overrule; `project-trajectory/PROCESS.md` §3, "When a guard is
owed"):

- **The retained reviewer's store record** decides which transcript a REVIEW
  call resumes. Its producer is `session_keep` under `store_lock`, the same
  route as the adjudicator's records. The record is written whole through a
  temporary file and a replace, so a failed write leaves the previous record
  or none, and `StoreBusy` surfaces as an error. Its consumers, found by
  grepping `session_keep`: `session_keep.py`, `session_service.py`,
  `dispatch.py`, `coordinator_adjudicate.py` and `coordinator_guard.py`
  (the lease directory). Ruling: an absent, unreadable or malformed record,
  or one naming another family or route, is no record, so the call mints a
  fresh session. A malformed dial reads as off. Either way, no review is
  ever resumed on doubt.
- **The merge-gating review's verdict file** decides whether a lane may
  land. Its producer is the review session, filed through `review_brief.py
  file`. Its gate consumers are `agent_loop.py`, `integrate.py` and
  `kitlib/verdict.py`; the builder confirms that list by grep before the
  build. Ruling: the gate accepts only a verdict whose session was minted
  fresh for that review and whose range runs from the claim base to the
  tip. A verdict that is absent, unreadable, lacks either fact, or comes
  from a resumed session does not clear the gate. The merge holds, with no
  fallback to an older verdict.

## Done-when

- The loop's REVIEW role can resume its session within one lane's review
  chain, through the same keep operation, the store and the lease
  (`retain_for` gains the review class behind its own dial; shipped off).
- The review that gates a merge is always a fresh session over the full lane
  (claim base to tip), never a resumed one.
- Tests: two iteration rounds resume one session; the merge-gating round mints
  fresh and covers the claim base to the tip; dial off changes nothing.
- The narrow round's reading scope (the round's delta) is a render of
  `prompts/reviewer.template.md` through `prompts.py`, the same render the
  coordinator's reviews use.
- SR-227 amended to cover the review class, or a new SR; its rows state it and
  pass adjudication on the one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
