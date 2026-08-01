+++
id = "WI-371"
title = "shoot.mjs destroys any BEFORE baseline a session stored under shots/: it rmSync(OUT, {recursive:true}) on every run, so the natural move of copying the pristine shots into shots/before/ before an edit silently deletes the baseline on the next shoot (hit twice in the 2026-07-30 render session; both builders lost their first baseline and re-shot from a worktree). Either scope the clean to the harness's own deterministic *.png names (leaving subdirectories alone) or make the README state loudly that baselines must live OUTSIDE shots/ - the first is one line and preserves the no-stale-shots property for the files the harness owns."
workstream = "dashboard"
specref = ""
buildtier = "quick"
priority = 3
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-30, the spec's first option. `shoot.mjs`'s pre-run clean now
removes only the harness's own top-level `*.png` (every shot it ever
writes is one), leaving subdirectories — a session's `shots/before/`
baseline — alone; the final listing likewise prints only PNGs, and the
README states the contract. The no-stale-shots property is preserved for
the files the harness owns. Verified live rather than by pytest (meta-only
Node dev tooling with no test harness; adding one for a one-line
clean-scope change would be a new toolchain step): a marker file planted
in a session subdirectory of the gitignored shots output survived a full
36-shot run that regenerated every declared PNG (the reviewer repeated
the probe with a stale top-level PNG added, which was deleted as owed).
