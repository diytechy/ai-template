+++
id = "WI-884"
title = "The loop schedules narrow review rounds, and the merge gate binds a fresh full-lane final review"
workstream = "process"
sr_refs = ["SR-154"]
specref = "docs/log.d/2026-10-06-wave18-coordinator.md"
needs = ["WI-847"]
buildtier = "strong"
safety_class = "ordinary"
priority = 5
+++

## Context

Split from WI-847 by the owner on 2026-10-10 (attended; decisions
`coordinator-2026-10-10.toml` D-008). WI-847 lands the narrow round's brief
render. Its step 2 was filed here whole: the loop's REVIEW role resumes its
session within one lane's iteration, and the review that gates a merge is
bound, with the owner's added requirement that **the final reviewer is
configurable**, a fresh session or a persisted independent final reviewer.

The scope critique of 2026-10-10 found four independently landable parts.
The coordinator split them in two (decision D-012 in
`coordinator-2026-10-10.toml`), first deliverable first:

1. **This row:** the loop schedules its narrow iteration rounds, and the
   merge gate binds a fresh, full-lane final review, closing the three gate
   hazards below. It lands value at once (narrow briefs are cheaper than
   full ones) and settles the gate contract the persisted reviewer must
   meet.
2. **WI-887**, which needs this row: REVIEW retention within a lane, keyed
   by lane and phase in the store, and the configurable persisted
   independent final reviewer. WI-858's store-keying need moves there.

The cost case is WI-847's. On WI-841 the hand path's fresh Sol rounds cost
115k to 160k tokens each, mostly re-reading the same context, and they hit
the Codex plan limit twice.

WI-847's builder (2026-10-10) found three gate hazards this row must close:

- At review policy 1, when only narrow rounds exist, the gate's filtered
  set is empty and falls through to the legacy hand-rollup window. That is
  a fallback to an older verdict.
- `agent_loop`'s `tree_already_judged` page would fire when a narrow
  APPROVE already sits at the tree the gating round must judge.
- The gate's base is the merge-base with trunk, which moves after a
  refresh, so "claim base to tip" needs the lane's claim base recorded.

## Trust

The merge-gating review's verdict file decides whether a lane may land
(`project-trajectory/PROCESS.md` §3, "When a guard is owed"). The ruling was
written for WI-847 before the split (D-003, for the owner to confirm or
overrule):

- **Producer:** a fresh review session, filed through
  `project-trajectory/scripts/review_brief.py file`, which refuses a review
  that does not open with `Reviewed: <full sha>` or lacks exactly one
  `VERDICT:` line whose count matches its findings, and then writes nothing.
  A failed write after the checks (an exclusive create, so never over
  another round) can leave a partial round file.
- **Consumers** (found by grep): `project-trajectory/scripts/integrate.py`
  (`_verdict_gate`, `_round_refusal`, `_legacy_window_refusal`),
  `project-trajectory/scripts/agent_loop.py` (`review_owed_by_evidence`, the
  `tree_already_judged` page), `project-trajectory/scripts/dispatch.py`
  (`_round_owed`), `project-trajectory/scripts/kitlib/verdict.py`
  (`review_logs`, `logged_rounds`, `round_entries`, `branch_entries`,
  `phases_owed`) and `project-trajectory/scripts/score_reviews.py`
  (`latest_phase_verdicts`).
- **Ruling:** the gate accepts only a full-scope verdict from a session
  minted for that review, whose range runs from the lane's recorded claim
  base to its tip. A narrow round's verdict, an absent, unreadable or
  partial round file, one the filing check would refuse, or one lacking any
  of those facts does not clear the gate. The merge holds, with no fallback
  to an older verdict or the legacy window. Per consumer:
  - `integrate.py` holds the merge and names the missing fact.
  - `agent_loop.py` and `dispatch.py` treat the full-lane review as still
    owed and schedule it. Their unchanged-rework page fires only for a
    qualifying full-scope verdict already at the tree, never for a narrow
    APPROVE or an invalid file.
  - `kitlib/verdict.py` reports an unreadable, partial or refusable round
    file as invalid evidence, never as a verdict of either kind.
  - `score_reviews.py` leaves invalid evidence out of its scores and
    reports it.
  - `project-trajectory/scripts/gen_verdict_rollup.py` (the human-facing
    rollup) skips an unreadable round file and shows an unparseable one
    without a verdict. The rollup has no merge authority.
  A narrow verdict steers iteration (another round, or rework) and never
  carries gate authority.

The **claim base** is the second fact the gate binds to. Its carrier
already exists: the claim commit `integrate.claim` writes on trunk before it
cuts the branch (subject `claim: <ids> -> active/<branch> (bookkeeping)`),
read by `agent_common.claim_base` (`project-trajectory/scripts/agent_common.py`).
It is git history, so a failed claim leaves no claim commit and no branch.
The gate reads the claim base through `claim_base` alone and reads no
merge-base. When the claim commit is absent (a manual or pre-claim lane) or
its history is unreadable, the gate holds. A trunk refresh leaves the claim
commit an ancestor of the lane, so the binding survives it.

## Done-when

- The loop schedules its narrow iteration rounds through
  `agent_brief.narrow_reviewer_prompt`, which WI-847 landed unwired
  (decisions coordinator-2026-10-10 D-011). Reviewers stay fresh sessions.
- The merge-gating round is a fresh session over the full lane, from the
  recorded claim base to the tip.
- The three gate hazards above are closed: no fallback to the legacy
  window, no unchanged-rework page on a narrow APPROVE, and the claim base
  recorded at the claim and used by the gate.
- Tests: a lane with only narrow rounds does not clear the gate; a narrow
  APPROVE at the tip does not raise the unchanged-rework page; the gate's
  range survives a trunk refresh; a partial or refusable round file does not
  clear it.
- The rows the change makes untrue or incomplete (SR-154's chain) state it
  and pass adjudication on the one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
