+++
id = "WI-548"
title = "Stall guard: a reviewer outage never closes a lane partial (the 2026-08-30 plan's C1-C7)"
specref = "docs/plans/2026-08-30-stall-guard-plan.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 1
+++

## Context

The plan of record is `docs/plans/2026-08-30-stall-guard-plan.md`, written at
the owner's request after the 2026-08-30 unattended run (its evidence rows:
decisions 14, 17, 21, 23, 29, 30 of `docs/decisions-for-review-2026-08-31.md`).
The owner's direction: *"If both openai and opencode are unavailable, I would
expect the fallback to be an independent opus reviewer, not a partial WI"* —
and these changes land FIRST, by hand on a claim branch, before the frontier
unpauses (the tracked `docs/work/pause` holds it).

Scope is the plan's C1-C7, one row (the plan's §3 offered one or two rows;
folded into one so the pause lifts after a single reviewed merge):

- C1 route-aware stall accounting (`agent_loop.RoutingState` splits the build
  stall from review draw failures).
- C2 "review owed" as a parked state (`EXIT_REVIEW_OWED`, not a decided
  handback; persisted so a resumed worker schedules the round).
- C3 an idle deadline in `agent_session.run_session` (launcher/env slot,
  dogfood-sync parity on the launchers).
- C4 a pre-dispatch liveness probe on routes with an unclean history this run.
- C5 the same-family reviewer fallback rung, `heterogeneity=relaxed` recorded
  on the verdict path, the round line and the telemetry.
- C6 the worker/adjudicator close ritual in the shipped briefs, and
  `integrate.unload` shedding the loop's own `out/run-logs/` streams.
- C7 the review brief's reading scope (three-dot diff against the current
  trunk with telemetry/generated exclusions, summary-not-transcript harness
  reads, cited registry rows only, `{trunk}`/`{process_doc}` rendered as slots
  because this meta-repo has no `docs/process.md` while every adopter does).

Adopter compatibility is the plan's §6: the new exit code lands at the END of
the alphabet with a `RESYNC_PACK.md` entry, the launcher slot lands in template
and live launcher in the same commit (test_dogfood_sync parity), prompt paths
render as slots, and the probe/relaxed rung stay policy-visible prose in
PROCESS_OPTIONS.md. Verify on a bootstrapped scaffold as well as by tests.
