+++
id = "WI-242"
title = "Dogfood-sync: adopt the 7 missing template registry columns + structural drift gate for launchers/dev-setup/stack.ini (owner directive 2026-07-19)"
workstream = "quality"
needs = ["~WI-238"]
buildtier = "medium"
safety_class = "high-risk"
order = 239
+++

## Deliverable

Widened work-items.csv 10->17 cols in TEMPLATE ORDER (option (a) full-width rewrite: 240 rows, every original cell remapped under its template-ordered column, the 6 new scheduler cols + PlanMode empty, SafetyClass relocated idx 9->15; CRLF + minimal-quoting preserved). Field-preservation proof: 240 rows x 10 original cols, 0 mismatches; behavior-neutrality proven identical across schedule.evaluate/simulate, check_trajectory.ssot_findings, agent_loop.critique_control, plan_runner.wi_plan_mode (empty new cell == absent column, every consumer DictReader-guarded). tests/test_dogfood_sync.py pins the structural surfaces and each assertion bites under temporary scratch mutation: every live registry header is an ordered superset of its template (SR's live-only SupersededBy is a legal extension); agent-resume.{sh,cmd,command} engine-invocation line normalized for the meta-repo project-trajectory/ prefix + --root . self-application, plus the exported AGENT_* variable-NAME set as template-subset-of-live (values free); stack.ini declares every template SECTION. dev-setup ruled value/bespoke (each variant is a meta-repo rewrite, no shared structural contract to pin without false positives). Spec deviation: rows are field-preserving not byte-identical - interleaved column insertion cannot be expressed by the WI-238 header-only ragged growth for width-stable rows, so option (a) rewrites every row for positional correctness (csv round-trip proven field-wise).
