+++
id = "WI-884"
title = "The loop's reviewer resumes within a lane, and the merge gate binds its final reviewer, fresh or persisted"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/log.d/2026-10-06-wave18-coordinator.md"
needs = ["WI-847"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Context

Split from WI-847 by the owner on 2026-10-10 (attended; decisions
`coordinator-2026-10-10.toml` D-008). WI-847 lands the narrow round's brief
render. This row carries the rest: the loop's REVIEW role resumes its
session within one lane's iteration, and the review that gates a merge is
bound. The owner added one requirement: **the final reviewer is
configurable**, either a fresh session or a persisted independent final
reviewer. The persisted reviewer is retained only for final gates, so it
never judges a round it reviewed while the lane iterated.

The cost case is WI-847's. On WI-841 the hand path's fresh Sol rounds cost
115k to 160k tokens each, mostly re-reading the same context, and they hit
the Codex plan limit twice.

WI-847's builder (2026-10-10) found that this needs a store identity beyond
today's family and route key. Its proposal, unadjudicated, is the starting
design:

1. The record gains a verbatim `scope` (lane plus review phase), and its
   file name hashes the route id plus the scope. An empty scope keeps the
   adjudicator's file name, so existing records still load. A record naming
   another scope reads as no record.
2. `applies` admits REVIEW under its own dial, shipped off, and `keep_for`
   takes the scope.
3. A narrow round pins the lane's retained reviewer route. Keep-warm never
   pings a reviewer record. The lane's iteration record retires when the
   gating round is drawn.
4. The gating round runs either unretained, or on the persisted final
   reviewer under its own scope, per the configuration.
5. REVIEW session logs record whether the session was minted fresh or
   resumed, and the reviewed range.

It also found three gate hazards this row must close:

- At review policy 1, when only narrow rounds exist, the gate's filtered
  set is empty and falls through to the legacy hand-rollup window. That is
  a fallback to an older verdict.
- `agent_loop`'s `tree_already_judged` page would fire when a narrow
  APPROVE already sits at the tree the gating round must judge.
- The gate's base is the merge-base with trunk, which moves after a
  refresh, so "claim base to tip" needs the lane's claim base recorded.

Gate readers found by grep: `integrate._verdict_gate`, `_round_refusal` and
`_legacy_window_refusal`; `agent_loop.review_owed_by_evidence` and the
`tree_already_judged` page; `dispatch._round_owed`; `kitlib/verdict.py`
(`review_logs`, `logged_rounds`, `round_entries`, `branch_entries`,
`phases_owed`); and `score_reviews.latest_phase_verdicts`.

WI-800 replaces the session store. If it lands first, the scope keying
moves into its store, as WI-858's rule does (decision D-010).

## Trust

The row gives two files authority (`project-trajectory/PROCESS.md` §3,
"When a guard is owed"). The ruling was written for WI-847 before the
split (D-003, for the owner to confirm or overrule). It is extended here
for the persisted final reviewer:

- **A retained reviewer's store record** decides which transcript a REVIEW
  call resumes. Its producer is `session_keep` under `store_lock`, which
  writes the record whole through a temporary file and a replace; a failed
  write leaves the previous record or none, and `StoreBusy` surfaces as an
  error. Its consumers: `session_keep.py`, `session_service.py`,
  `dispatch.py`, `coordinator_adjudicate.py` and `coordinator_guard.py`
  (the lease directory). Ruling: an absent, unreadable or malformed record,
  or one naming another family, route or scope, is no record, so the call
  mints a fresh session. A malformed dial reads as off. No review is ever
  resumed on doubt.
- **The merge-gating review's verdict file** decides whether a lane may
  land. Its producer is the review session, filed through `review_brief.py
  file`. Its consumers are the gate readers above. Ruling: the gate accepts
  only a verdict from the configured final reviewer whose range runs from
  the lane's claim base to its tip. In fresh mode, that means a session
  minted for that review. In persisted mode, it means the final reviewer's
  own scope, never an iteration reviewer's. Any other verdict, an absent or
  unreadable one, or one lacking those facts does not clear the gate. The
  merge holds, with no fallback to an older verdict.

## Done-when

- The loop's REVIEW role can resume its session within one lane's
  iteration, through the keep operation, the store and the lease, keyed so
  no lane or phase resumes another's transcript. The dial ships off.
- The loop schedules its narrow iteration rounds through
  `agent_brief.narrow_reviewer_prompt`, which WI-847 landed unwired
  (decisions coordinator-2026-10-10 D-011).
- The final reviewer is configurable, fresh or persisted independent, with
  fresh as the default. Either way it reviews the full lane, claim base to
  tip, and never resumes an iteration reviewer's session.
- The three gate hazards above are closed: no fallback to the legacy
  window, no unchanged-rework page on a narrow APPROVE, and the claim base
  recorded and used.
- Tests: two iteration rounds resume one session; a second lane on the same
  route does not resume it; the gating round in fresh mode mints fresh; in
  persisted mode it resumes only the final reviewer's scope; a resumed
  iteration session's verdict does not clear the gate; with the dial off,
  nothing changes.
- SR-227 amended to cover the review class and the final reviewer's
  configuration, or a new SR. Its rows state it and pass adjudication on the
  one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
