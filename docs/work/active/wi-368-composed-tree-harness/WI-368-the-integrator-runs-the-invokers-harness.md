+++
id = "WI-368"
title = "The integrator folds the trunk step with the INVOKER'S harness, not the composed tree's: _run_trunk_step runs SCRIPTS/trunk_step.py (resolved from the running integrate.py — the trunk checkout), so the §5.2 regen executes trunk-version generators against the candidate; a work branch that changes a generator (first hit: WI-366's gen_trajectory.py port harness) is then refused by the merge commit's own freshness floor, which runs the MERGED generator and finds the old renderer's artifact stale. Reproduced deterministically 2026-07-30: trunk trunk_step.py against the merged candidate -> 'project-state dashboard STALE in PROJECT_STATE.html'; the candidate's own trunk_step.py against the same tree -> clean, floor and bar green. _run_bar shares the seam (SCRIPTS/check.py — its step commands already resolve against the candidate, but the orchestrator itself is the invoker's version). Fix: when the invoker's SCRIPTS directory sits inside --root and the candidate carries the same relative path, run the COMPOSED tree's copy (fallback to the invoker's copy otherwise) — §4's 'required checks on the composed tree' applied to the checker itself. Latent until now because the grind sessions committed attended-serial (RULING-8) rather than through the queue; the queue path had never merged a generator change."
workstream = "scripts"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
+++
