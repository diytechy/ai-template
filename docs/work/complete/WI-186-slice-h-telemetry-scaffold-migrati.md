+++
id = "WI-186"
title = "Slice H - telemetry + scaffold + migration + dogfood"
workstream = "unattended"
sr_refs = ["SR-065", "SR-059"]
needs = ["WI-180", "WI-183", "WI-184", "WI-185"]
buildtier = "medium"
order = 185
+++

## Deliverable

Slice H (2026-07-16, the effort join): telemetry + downstream migration + scaffold flip + generated surfaces, closing v4 G2->G3. TELEMETRY (SR-065): every journal event carries a per-launch run id (<utc>-<pid>-<rand>), so aggregation is by (run, train, WI, session) with no cross-run collision; a change-gated one-line banner reports lanes/frontier/integration-queue/ceiling; telemetry_summary writes out/dispatch/telemetry.json with the required measurements (reservation->integration counts, overlap/conflict/re-review/rework rates, recovery reconciles, quarantines, bar-failures-after-green). MIGRATION (SR-065, spec 14): resolve_ceiling gates the two-worker promotion - a repo holds at --jobs 1 until BOTH assess_migration audits pass (SafetyClass: every open WI classified, one unclassified holds the repo; soft-edge: every ~ edge signed via docs/archive/history/parallel-ready), a fresh scaffold passing by construction, the flip recorded (parallel-enabled event); reconcile_legacy returns legacy active rows to queued (logged finding) + flags docs/tracks/*; a non-adopting repo (no --jobs/AGENT_JOBS) keeps the byte-unchanged legacy loop. SCAFFOLD/SR-059: agent-resume.template.{sh,cmd} ship AGENT_JOBS=2 parallel-by-default; a fresh scaffold carries no next-wi/run-phase; generate_status is marker-gated (a hand-authored status.md is never clobbered) - the integrator-generated status.md + dispatcher-generated run-state complete SR-059's generation half; the launch reconcile now fast-forwards the integration ref to absorb human-added WIs on the dev branch (spec 9 'reconciles from the development branch' - the gap D/F left), classifying dev-ahead vs integration-ahead vs diverged before acting so a publish never discards new work. downstream-resync skill + ADOPTING 6 + PROCESS_OPTIONS document the migration. tests/test_agent_loop_migration.py (9 fixtures, TC-060+TC-066). SR-059/SR-065 + LLR-060/066 + TC-060/066 Verified (autonomous single-agent adversarial review). phase-v4 effort COMPLETE - all of SR-057..065 Verified; derived gate v4 G2->G3.
