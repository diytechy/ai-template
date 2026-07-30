+++
id = "WI-359"
title = "Integrator unload is incomplete while a worker worktree holds the merged branch: integrate_one's git branch -d fails silently (checked out elsewhere) and nothing removes the worker worktree, so the §5.6 drained-and-unloaded stop needs hand cleanup. The integrator should report the still-held branch by name (loud, not swallowed) and own or delegate worker-worktree GC - the old dispatcher's no-GC gap (36 stale worktrees) must not regrow here."
workstream = "scripts"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-29 (adversarially reviewed; the review's MAJOR fixed before landing). `integrate_one` never swallows the unload: `_unload_branch` resolves the holder via `git worktree list --porcelain`; the dirt read is `git status --porcelain --ignored=matching` and FAILS CLOSED (a failing read counts as dirty) because the review proved the tracked-only read waved through worktrees whose only unique content was git-ignored (out/run-logs/ — the class that exists nowhere else) and the GC destroyed it. A clean holder is removed (never --force) and the delete retried; a dirty one is reported with paths + exact commands; the MAIN checkout is recognized and never removed. An incomplete unload now exits NONZERO with a STILL HELD summary (merges stand; the stop is not 'drained and unloaded' until clear) — the 36-stale-worktree pathology cannot regrow silently. 50 tests in tests/test_integrate.py incl. two e2e runs against the real bar.
