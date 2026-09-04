+++
id = "WI-548"
title = "Stall guard: a reviewer outage never closes a lane partial (the 2026-08-30 plan's C1-C7)"
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 1
+++

## Deliverable

The seven stall-guard changes (C1-C7 of
`docs/plans/2026-08-30-stall-guard-plan.md`), built by hand on this claim
branch under the tracked pause and verified by tests AND on a bootstrapped
scaffold:

- **C1** `agent_loop.RoutingState` splits the builder's stall streak from
  review-draw failures (`note_session(judging=)`, `note_review_draw_failure`,
  reset on any recorded verdict) — three reviewer outages are no longer the
  builder "not building".
- **C2** `EXIT_REVIEW_OWED = 9`: a committed build whose review ladder is
  exhausted parks the lane (banner + `out/review-owed` marker); the
  dispatcher resumes it like a crash, the resumed worker schedules the owed
  round FIRST, a completed round clears the marker. Never a `partial` close
  of finished work.
- **C3** `agent_session.run_session(idle_timeout=)`: a silent child is killed
  ~`idle_timeout` s after its last output line (engine default 900;
  `AGENT_SESSION_IDLE_TIMEOUT` slot in all four launchers,
  `--session-idle-timeout`, forwarded by `lane.worker_argv`; typed
  `timeout: wall|idle` telemetry key).
- **C4** `probe_route`/`select_with_probe`: a route cooled earlier this run
  answers a 30 s `OK` probe on its own CmdTemplate (verbatim) before another
  real session is spent on it; clean routes are never probed.
- **C5** the same-family reviewer fallback rung: exhausted cross-family
  ladder -> relaxed retry; ANY same-family review draw is recorded three ways
  (`-relaxed` verdict filename, `heterogeneity=relaxed` round line, typed
  telemetry key).
- **C6** the close rituals in `worker.template.md` and
  `adjudicate-disposition.template.md` (the adjudicator closes its OWN row;
  draft shape pinned: this spec's `## Dispositions`, top-level keys, title
  <= 120), and `integrate` unload sheds the loop's own `out/run-logs/`
  streams + the `out/review-owed` marker as declared residue (two shipped
  pins deliberately overturned, the overturn stated in the rewritten tests).
- **C7** the reviewer brief's reading scope: exact three-dot diff against the
  CURRENT trunk with telemetry/record/generated exclusions, summary-only
  harness reads, cited-rows-only registry reads, and `{trunk}` /
  `{process_doc}` as loop-rendered slots (`trunk_name`, `process_doc_path`) —
  proven both ways: the meta-repo renders `project-trajectory/PROCESS.md`,
  the bootstrapped scaffold renders `docs/process.md`. The TERRA row carries
  `-c model_reasoning_effort=medium` as the measured item-5 experiment.

Adopter compatibility per the plan's §6: exit 9 appended at the end of the
alphabet and documented in PROCESS_OPTIONS.md "Unattended operation"; the
launcher slot landed in template + live launchers in the same commit
(test_dogfood_sync parity); RESYNC_PACK.md carries this change set's entry
PLUS the two entries the previous run owed (the check_docs HTML-comment fix,
opencode `--dir .`).

Verification: full suite 3175 passed, 16 skipped in 861.84s (fig: cmd="python -m pytest -q -n auto" rev=777bbbfe on the lane, loaded box); guard suites 107 + 121 passed; scaffold drive: bootstrap from this branch's kit ->
one managed `--wi` session end to end (build + review), the brief rendering
the scaffold-side slot values. Module-size ratchet re-stamped with reasons
(agent_loop 3622 -> 3924, agent_common 2660 -> 2678, integrate 2626 -> 2646).

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
