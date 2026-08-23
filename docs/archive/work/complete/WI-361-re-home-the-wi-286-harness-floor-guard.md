+++
id = "WI-361"
title = "Re-home the WI-286 harness-floor guarantee at a surviving seam, or retire it with a recorded reason. The fail-closed ≥3.11-pinned-venv preflight (_harness_floor_failures + _activate_root_venv) had exactly one enforcement point — the parallel dispatcher's dispatch_run — and was deleted with it at concurrency-restructure Phase 5 item 1 (nothing surviving ever called it, so no surviving flow lost a guarantee it had). The exposure it guarded is still real: a worker session or the integrator's composed-tree bar launched in a worktree without the pinned .venv resolves the ambient interpreter, which can clear the version floor yet lack the pinned dev tools (the 20260723 run inherited Python 3.8; an ambient-modern Python is the FALSE-GREEN half, REVIEW-A on WI-286). Candidate seams, to be DESIGNED not assumed: agent_loop.map_preflight (would newly refuse venv-less repos — the test fleet's fixtures run venv-less, so this changes the contract, which is why the silent port was refused at Phase 5); integrate.py's bar runner (harness_python already prefers the venv; the floor would make absence a named refusal instead of a silent ambient run). Decide the seam against the post-deletion loaders, port the ~70 lines + the five floor tests from git history (agent_dispatch.py@31ad569^), or retire the guarantee with the reason in this row."
workstream = "scripts"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
order = 361
+++

## Deliverable

DONE 2026-07-29 — RE-HOMED as a fail-closed refusal (owner ruled refusal over warn in-session: warns get ignored). agent_common.harness_floor_failures (ported from the deleted dispatcher, all three shapes: no runnable .venv / unrunnable interpreter / below-floor) refuses integrate.py's bar BEFORE the candidate worktree and merge. Arming boundary — the WI's design decision: the floor arms only where requirements-dev.txt declares the pinned toolchain; an undeclared repo (fresh scaffold, fixture, non-Python adopter) keeps the ambient fallback and never sees the refusal, so it is never a contract the repo didn't opt into. Downstream adopters on other stacks owe their own analogous environment validation (owner's framing, recorded here). Tests in test_agent_common_harness.py (five floor shapes + both boundary directions) and test_integrate.py (declared-without-venv refuses; undeclared runs).
