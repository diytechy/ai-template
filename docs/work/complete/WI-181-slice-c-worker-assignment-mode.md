+++
id = "WI-181"
title = "Slice C - worker assignment mode"
workstream = "unattended"
sr_refs = ["SR-026"]
needs = ["WI-179"]
buildtier = "strong"
order = 180
+++

## Deliverable

Slice C (2026-07-16): agent_loop.py explicit worker assignment - --wi/--train/--worktree/--base/--rework run one dispatcher-assigned traincar on branch llm/train/<id>. Worker prompt assembled from AGENTS.md + WI row + SpecRef + predecessor context + train diff + rework finding (never status.md/next-wi); NO lane files (run-state never read/written - the three NEEDS-HUMAN page writes gated off; pause dispatcher-owned; iteration_index regeneration skipped - integrator-owned); result = committed evidence (WI/Train/Base trailers; Blocked-WI + BlockRef -> exit 3; evidence-first DONE check gives spec-11 recovery semantics: a relaunched worker with complete evidence exits without a session). Collision-safe evidence: session logs docs/iteration/<train>-NNN-*.log (train-scoped numbering) + review verdicts docs/reviews/<train>/NNN-<PHASE>-<sha7>.md naming the exact reviewed head + train-scoped scoreboard. Per-WI BuildTier pin restored from the reserved WI row (managed mode); assignment-scoped rework replaces the lane rework-wi pointer in worker mode; --track deprecated for one compatibility window (old behavior intact, warned). Preflight fails closed: pair/slug/branch-guard/unknown-or-done-WI. tests/test_agent_loop_worker.py (22 fixtures, incl. two concurrent workers in linked worktrees + exact-reviewed-commit naming). PROCESS_OPTIONS 'Worker assignment (parallel dispatch)' contract (+1,113 B). SR-060/LLR-061/TC-061 Verified (autonomous single-agent adversarial self-review).
