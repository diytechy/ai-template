+++
id = "WI-857"
title = "A verdict records its judging session, and an act backed by the authoring session's verdict is refused"
workstream = "process"
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
sr_refs = ["SR-178", "SR-156"]
needs = ["WI-849", "WI-801"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Context

Split out of WI-849 by the owner on 2026-10-08 ("Split it out"), when WI-849's
first build round found the part it could not build. Ruling 6 of 2026-10-07
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`) lets an independent
adjudicator take the approval act in the authoring lane. WI-849 lands the
merge slot's rung on today's route-established independence: an accepted
binding is written only by the adjudication route
(`adjudicate_brief.record_outcome`), after it launches its own separate
session. A hand-written binding is the honest bound `kitlib/evidence.py`
already states.

What no record holds today, from WI-849's round-1 evidence:
- the binding (`kitlib.sitting.render_requested`) records the brief, the kinds
  and the outcome, but no session id; the judging session's id lives only in
  call telemetry and the keep store;
- no record the merge reads names the session that authored a row. Lane
  commits carry `Loop-Session`, which the builder and adjudicator share, and
  the coordinator's spine authoring runs from launch scripts outside the kit.

This row waits on WI-801 (one labelled entry point for model calls, after
WI-852 renders the coordinator's briefs), so that every authoring and judging
call is launched by the kit and can be recorded by it.

## Done-when

- The binding records the judging call's session id, written by the one
  route that records its outcome; a binding with no session id reads as no
  independent verdict for this rule.
- Each authoring call (spine text, code) leaves a record the merge slot reads
  naming its session, written by the kit's launch path, never by hand.
- The approval-act rung refuses an act whose backing verdict was judged by a
  session that authored any row the act flips or re-attests, naming the act,
  the row and both sessions.
- Tests: an act backed by an independent session's verdict merges; refused
  each: a verdict from the authoring session, and a binding with no session
  id. Nothing that merged before is refused.
- The rows it amends (SR-178's chain as WI-849 left it) are authored as one
  change set and judged in one combined sitting.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
