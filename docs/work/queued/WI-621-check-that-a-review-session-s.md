+++
id = "WI-621"
title = "Review and Done-when integrity: a review session adds only its verdict file, no later session rewrites a round, and a lane's Done-when is fixed at claim"
workstream = "unattended"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#33-fewer-tools-per-role-and-skills-handled-mechanically-note-1"
buildtier = "medium"
priority = 4
safety_class = "ordinary"
needs = []
supersedes = "WI-608;WI-622"
+++

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-608 (Stop a later session rewriting an earlier review round's verdict file: reproduce first, then fix (review pack C4)), WI-622 (Require a Done-when before claim, and flag a lane that changes its own Done-when at merge (S13)). Each keeps the record a merge judges from being changed by the lane it judges: a reviewer's extra commits (WI-621), a later session rewriting an earlier round's verdict (WI-608), a builder rewriting its own Done-when (WI-622). All three sit in the claim and merge ladder. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

WI-608 reproduces first; its fix should fall out of this row's per-session range record (a round read as its session committed it) rather than add a refusal.

Ruled by the owner: S9 (2026-09-23, "verify, don't isolate") and its
mechanism (2026-09-24, review pack B2), sister plan §3.3 and §5.

Reviewers keep committing their own verdicts (OI-76 unchanged). Nothing on a
commit reliably names its role, but the coordinator records each session's
phase and exact commit range in its session log (`# phase:`, `# commits:
before..after`: the range is taken at `agent_loop.py:3906-3909`, the fields
assembled at `:3295-3343`, the header written at `agent_common.py:2565-2585`).
The check keys on that record, not on authors, subjects or trailers. It runs
right after each review session and again in the merge ladder
(`_merge_refusal`), re-derived from the committed session logs. A dirty tree
right after a review session fails the draw through the existing failed-draw
path, so the review re-runs clean. On a build lane with no Drafted rows, the
merge ladder is the final pass. S11's single-commit plan rewrites the
lane-to-trunk path this sits on, so design it with that plan if the plan lands
first. Related: WI-608 (a later session rewriting an earlier round).

ABSORBED from WI-607 (the routing side): `read_verdict`
(`agent_loop.py` ~1072) parses the verdict file on disk whether or not the
reviewer committed it, while the merge gate reads committed round files at
the branch tip, so the loop can route (approve, re-route, re-critique) on a
verdict the gate cannot see. The dirty-tree arm above is the mechanism: an
uncommitted verdict fails the draw, so it is never read. Apply it to the
critique arm too, which also calls `read_verdict`, rather than adding a
second check.

## Done-when

- A REVIEW session whose recorded range adds anything but its verdict file is
  refused right after the session, naming the paths.
- The merge ladder re-derives the same check from the committed session logs
  and refuses by name.
- A dirty tree right after a review session fails the draw, and the review
  re-runs clean.
- The loop routes on a verdict only as committed on the lane, in both the
  review and the critique arms; an uncommitted verdict file is treated as no
  verdict (the failed-draw path).
- Tests drive a clean review, an extra file, a dirty tree, a merge whose
  log records a bad range, and a review and a critique session that each
  write but do not commit their verdict, showing the loop does not route on
  it.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-608 (Done-when, verbatim)

- A test reproduces the rewrite, or shows it cannot happen, in which case this
  row closes with that evidence.
- If reproduced: a round's verdict is read as its review session committed
  it, so a later edit cannot change what the gate counts; prefer that to a
  new refusal (the antidote question).
- If a refusal is still needed, it names the round file and the commit that
  touched it.

### From WI-622 (Done-when, verbatim)

- A work item without a `## Done-when` is not claimable: warn-first until the
  open items lacking one are backfilled, then the claim refuses by name.
- At merge, each Done-when item's text at claim is compared with its text at
  merge, ticks and trailing evidence stripped, and any change is flagged to the
  reviewer and the adjudicator.
- Tests: a tick with evidence does not flag; a reworded item does; a work item
  with no Done-when warns (and later refuses).
