+++
id = "WI-371"
title = "shoot.mjs destroys any BEFORE baseline a session stored under shots/: it rmSync(OUT, {recursive:true}) on every run, so the natural move of copying the pristine shots into shots/before/ before an edit silently deletes the baseline on the next shoot (hit twice in the 2026-07-30 render session; both builders lost their first baseline and re-shot from a worktree). Either scope the clean to the harness's own deterministic *.png names (leaving subdirectories alone) or make the README state loudly that baselines must live OUTSIDE shots/ - the first is one line and preserves the no-stale-shots property for the files the harness owns."
workstream = "dashboard"
specref = "scripts/dashboard-shots/README.md"
buildtier = "quick"
priority = 3
safety_class = "ordinary"
+++
