+++
id = "WI-359"
title = "Integrator unload is incomplete while a worker worktree holds the merged branch: integrate_one's git branch -d fails silently (checked out elsewhere) and nothing removes the worker worktree, so the §5.6 drained-and-unloaded stop needs hand cleanup. The integrator should report the still-held branch by name (loud, not swallowed) and own or delegate worker-worktree GC - the old dispatcher's no-GC gap (36 stale worktrees) must not regrow here."
workstream = "scripts"
specref = "docs/log.md"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
+++
