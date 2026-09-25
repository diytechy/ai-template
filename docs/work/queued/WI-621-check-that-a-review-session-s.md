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
first. Related: WI-607 (routing on an uncommitted verdict) and WI-608 (a later
session rewriting an earlier round).

## Done-when

- A REVIEW session whose recorded range adds anything but its verdict file is
  refused right after the session, naming the paths.
- The merge ladder re-derives the same check from the committed session logs
  and refuses by name.
- A dirty tree right after a review session fails the draw, and the review
  re-runs clean.
- Tests drive a clean review, an extra file, a dirty tree, and a merge whose
  log records a bad range.
