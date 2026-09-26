+++
id = "WI-621"
title = "Check that a review session's commits add only its verdict file, after the session and again at merge (S9)"
workstream = "unattended"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#33-fewer-tools-per-role-and-skills-handled-mechanically-note-1"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

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
