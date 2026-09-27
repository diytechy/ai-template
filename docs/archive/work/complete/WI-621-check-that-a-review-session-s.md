+++
id = "WI-621"
title = "Review and Done-when integrity: a review session adds only its verdict file, no later session rewrites a round, and a lane's Done-when is fixed at claim"
workstream = "unattended"
specref = ""
buildtier = "medium"
priority = 4
safety_class = "ordinary"
needs = []
supersedes = "WI-608;WI-622"
+++

## Deliverable

The record a merge judges stays as its authors committed it (squash of
build/wi-621: 58535a4c, 57bdae19 and c49146a3, rebased onto 9ecb934f from
a7124fed). Codex Sol reviewed three rounds: NOT YET SOUND twice
(`sol-wi621.md`, `sol-wi621-fix.md`), then SOUND (`sol-wi621-fix2.md`).
Wave-4 rulings 16 and 17.

- **WI-608 (absorbed), reproduced then closed.** A later session rewriting
  an earlier round's verdict file cleared the gate; a test drove it red. No
  new refusal was added. `kitlib/verdict.logged_rounds` reads each round at
  the end of its session's recorded range, only when that range changed the
  file. Session logs are append-only evidence: each is read as the commit that
  added it recorded it, and the merge rung refuses by name any lane commit
  that modifies or deletes one. An end-to-end regression shows a rewritten log
  cannot launder a rewritten verdict.
- **WI-621.** A REVIEW session whose recorded range adds anything but its
  verdict file stops the run with NEEDS-HUMAN, naming the paths, and the merge
  ladder re-derives the same check (`_review_scope_refusal`). New dirt after a
  REVIEW or CRITIQUE session fails the draw, with the leftovers stashed. A
  stash that fails stops for a human with nothing redrawn, driven end to end
  through the fake-agent loop. `read_verdict` reads the committed blob in
  both the review and critique arms, so the loop never routes on an
  uncommitted verdict (review pack C3, reproduced).
- **WI-622 (absorbed).** `kitlib/done_when.py` (IF-242). A claim WARNS on a
  missing Done-when. It does not refuse, because every minted row today is
  filed without one: 28 of the 74 completed rows since WI-550. The refusal
  waits on the mint writing one, or on the owner ruling minted adjudications
  exempt. At merge, a Done-when item changed since claim (a tick and the
  convention's evidence form stripped; appended prose is not evidence) is
  flagged in the reviewer brief and mints a brief-less adjudication row.

Drafted rows owing a first approval in the next spine-acts batch: LLR-262,
TC-257 (Full) and TC-259 (Smoke). IF-242 is Drafted and off-spine. No
approved row was touched. Size ratchet: agent_loop, integrate, intake and
bootstrap re-measured on the merged tree, with reasons; `check_complexity`
is unchanged. Recorded limit: `— DONE except on Windows` still reads as
evidence.

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
