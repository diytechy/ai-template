+++
id = "WI-887"
title = "The loop's reviewer resumes within a lane, and the final reviewer is configurable, fresh or persisted"
workstream = "process"
sr_refs = ["SR-227"]
specref = "docs/work/queued/WI-884-reviewer-retention-and-gate.md"
needs = ["WI-884"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Context

Split from WI-884 by the coordinator on 2026-10-10 after its scope critique
(decision D-012 in `coordinator-2026-10-10.toml`). WI-884 wires the narrow
rounds and binds a fresh, full-lane final review at the merge gate. This
row adds retention on top of that gate contract: the loop's REVIEW role
resumes its session within one lane's iteration, and the owner's
requirement (D-008) that **the final reviewer is configurable**, either a
fresh session or a persisted independent final reviewer, retained only for
final gates so it never judges a round it reviewed while the lane iterated.

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
   resumed, and the reviewed range. (Committed: see Done-when.)

WI-800 replaces the session store. If it lands first, the scope keying
moves into its store, as WI-858's rule does (decision D-010).

Landing order: one lane after WI-884. Retention and the persisted final
reviewer share the scope keying, and a persisted reviewer without scoped
records could resume an iteration reviewer's transcript.

## Trust

The row gives two files authority (`project-trajectory/PROCESS.md` §3,
"When a guard is owed"). The ruling was written for WI-847 before the
split (D-003, for the owner to confirm or overrule) and extended for the
persisted final reviewer:

- **A retained reviewer's store record** decides which transcript a REVIEW
  call resumes. Its producer is `session_keep` under `store_lock`, which
  writes the record whole through a temporary file and a replace; a failed
  write leaves the previous record or none, and `StoreBusy` surfaces as an
  error. Its consumers (found by grep):
  `project-trajectory/scripts/session_keep.py`,
  `project-trajectory/scripts/session_service.py`,
  `project-trajectory/scripts/dispatch.py`,
  `project-trajectory/scripts/coordinator_adjudicate.py` and
  `project-trajectory/scripts/coordinator_guard.py` (the lease directory).
  Ruling: an absent, unreadable or malformed record, or one naming another
  family, route or scope, is no record, so the call mints a fresh session.
  A malformed dial reads as off. No review is ever resumed on doubt.
- **The merge-gating review's verdict file** keeps WI-884's filing and
  failure contract, its consumers, its claim-base-to-tip binding and its
  rejection rules, with one mode-dependent change to "a session minted for
  that review". In fresh mode (the default) that requirement is unchanged.
  In persisted mode the gate instead accepts a session resumed from the
  persisted final reviewer's own scope, and still never an iteration
  reviewer's session or scope. Every consumer WI-884 lists applies this
  same ruling; none keeps the fresh-only rule in persisted mode.

## Done-when

- The loop's REVIEW role can resume its session within one lane's
  iteration, through the keep operation, the store and the lease, keyed so
  no lane or phase resumes another's transcript. The dial ships off.
- The final reviewer is configurable, fresh or persisted independent, with
  fresh as the default. Either way it reviews the full lane, claim base to
  tip, and never resumes an iteration reviewer's session.
- Each REVIEW session log records whether the session was minted fresh or
  resumed, its scope, and the reviewed range (base and tip). The log is an
  audit record: no gate or scheduler reads it, so it carries no authority.
  The gate's evidence that a verdict came from the final reviewer's scope
  is the verdict file itself, under WI-884's filing contract.
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
