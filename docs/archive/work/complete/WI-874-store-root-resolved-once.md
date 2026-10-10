+++
id = "WI-874"
title = "The runtime store's primary checkout is resolved once per operation, not by a git spawn on every store access"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

`session_keep.primary_out_dir` memoizes the git common directory per absolute
root for the process's life, so one store operation (a keep, a bookkeeping
release, the coordinator lease's take or release) spawns the lookup at most
once. Its signature (IF-272) and every store caller are unchanged, and a
lane's worktree still resolves to the primary checkout's `out/`. A red-first
test counts the spawns and pins the lane's store and lease to the primary's.
No spine row was made untrue. Quiet re-measure, three runs, beside WI-869's:
`docs/log.d/2026-10-10-wi-874-store-lookup-measurement.md` (summed per-test
time 29.3 s against 123.2 s across the four modules). Gate: Codex 6.1 Sol's
fresh full-lane review `docs/reviews/wi-874/001-REVIEW-A-6b8cf4e.md`, APPROVE
with 0 findings.

## Context

Filed by the coordinator on 2026-10-09 from WI-869's measurement (docs/log.d/2026-10-09-wi-869-smoke-tier-measurement.md; docs/decisions/wi-869.toml D-003). `session_keep.primary_out_dir` runs `git rev-parse --path-format=absolute --git-common-dir` on every call, with no caching, and `store_dir` (and through it `store_lock` and `dedicated_home`) and `coordinator_guard.lease_dir` call it on each store access. The builder counted about 1,260 git spawns in `tests/test_session_keep.py` alone and 255 to 330 each in `test_coordinator_adjudicate`, `test_adjudicator_token` and `test_coordinator_guard`. Those in-process smoke modules are among the tier's heaviest after WI-869's re-tier (53.0, 33.9, 16.0 and 14.1 s summed per-test time). At about 20 ms a spawn on this workstation, the cost is the same in the live loop: every keep, lease and bookkeeping write pays it again.

## Done-when

- One store operation (a keep, a lease take or release, a bookkeeping write) resolves the primary checkout's `out/` once and passes it down, or the lookup is memoized per root for the life of the process; a lane's worktree still shares the primary checkout's store (the lookup's reason to exist).
- The change is red-first: a test counts the git spawns of one store operation, and fails before the change.
- `tests/test_session_keep.py`, `test_coordinator_adjudicate`, `test_adjudicator_token` and `test_coordinator_guard` are re-measured (summed per-test time, `--durations=0`, three quiet runs) and the figures are stated in the log beside WI-869's.
- No behaviour other than the spawn count changes; the spine rows that state the store's location (LLR-270's chain) are re-read and amended only where their text becomes untrue.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit (a shipped script changes).
