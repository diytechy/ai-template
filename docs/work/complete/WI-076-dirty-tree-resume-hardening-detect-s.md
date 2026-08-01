+++
id = "WI-076"
title = "Dirty-tree resume hardening - detect + surface + stale-lock recheck"
workstream = "unattended"
needs = ["WI-024"]
order = 75
+++

## Deliverable

P3 - loop surfaces a loop-start dirty tree: working_tree_dirty() porcelain reader + a one-line stderr log + RESUME_RECONCILE_NOTE prepended to the FIRST session's prompt only (once-at-start, NOT per-iteration - the coordinator's own tracked-but-lagging docs/iteration bookkeeping would false-positive every later pass); surface-only, never stash/clean/block (WI-060 stays deferred). Protocol text: session-protocol skill 'check git status first' rule + byte-identical fan-out; PROCESS_OPTIONS unattended sentence. Stale-lock recheck: SAFE - the kernel advisory lock is OS-released on holder death (crash/SIGKILL), already covered by test_lock_auto_released_when_holder_dies; recorded in log.md, no fix needed. No spine change (prompt composition inside the existing session contract). +3 tests (dirty-inject+log, clean byte-identical, rename/untracked parse).
