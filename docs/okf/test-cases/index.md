---
type: "Index"
title: "test-cases"
description: "tier index"
tags: []
resource: "generated"
---
> **GENERATED — a reference copy, not the source of truth.** Derived from docs/test/test-cases.csv by scripts/gen_okf.py; edit the registry/doc, then rerun it (docs/okf-export: off silences the layer).

# test-cases — index

| id | summary |
|---|---|
| [TC-001](TC-001.md) | Run the trace suite; a linked chain is orphan-free and an injected orphan fails --strict. |
| [TC-002](TC-002.md) | Run the registry-checks suite; duplicate/malformed ids and mis-columned rows fail --stric… |
| [TC-003](TC-003.md) | Run the registry-checks suite; leftover -000 rows, empty/out-of-vocab fields, and (once t… |
| [TC-004](TC-004.md) | Run the acceptance-criteria advisory suite; an unpinned comparative warns without changin… |
| [TC-005](TC-005.md) | Run the off-spine registry suites; back-link findings fire and -000 rows are ignored. |
| [TC-006](TC-006.md) | Run the check-harness suite; gate steps run and a missing required tool fails with SKIP(m… |
| [TC-007](TC-007.md) | Run the stack-profile suite; commands and tiers/coverage/arch-map resolve from stack.ini. |
| [TC-008](TC-008.md) | Run the stack-profile suite; malformed/non-integer/missing-binary profiles fail loudly. |
| [TC-009](TC-009.md) | Run the profile suite; a non-Python profile omits Python-only files and seeds files-mode … |
| [TC-010](TC-010.md) | Run the bootstrap suite; a fresh scaffold's harness runs green. |
| [TC-011](TC-011.md) | Run the bootstrap suite; a re-run leaves existing files unchanged, --force overwrites, an… |
| [TC-012](TC-012.md) | Run the check-docs suite; a broken link or missing vision tag fails --stale. |
| [TC-013](TC-013.md) | Run the check-flows suite; a conformant flow passes and a malformed one fails. |
| [TC-014](TC-014.md) | Run the check-perf suite; a within-tolerance metric passes and a regression fails. |
| [TC-015](TC-015.md) | Run the perf-budgets suite; an unresolvable or empty PB Refs is a finding. |
| [TC-016](TC-016.md) | Run the check-stubs suite; a stub at the declared gate fails and clean source passes. |
| [TC-017](TC-017.md) | Run the check-privacy suite; a staged secret is blocked with privacy-check off. |
| [TC-018](TC-018.md) | Run the check-privacy suite; PII/identity classes fire only with privacy-check on and hon… |
| [TC-019](TC-019.md) | Run the pre-commit-hook suite; a failing integrity/secrets check blocks the commit. |
| [TC-020](TC-020.md) | Run the pre-push-hook suite; a secret/identity in the push range blocks the push. |
| [TC-021](TC-021.md) | Run the hook suites' python-probe cases; a missing/aliased python3 reports clearly withou… |
| [TC-022](TC-022.md) | Run the check-vendored suite; a drifted vendored copy is a finding. |
| [TC-023](TC-023.md) | Run the gen-arch-map suite; --check fails on a stale map and regeneration rewrites only t… |
| [TC-024](TC-024.md) | Run the gen-cases suite; the spec grammar expands to the expected case set. |
| [TC-025](TC-025.md) | Run the skills-index suite; INDEX.csv regenerates from the SKILL.md frontmatter. |
| [TC-026](TC-026.md) | Run the agent-loop suite; the dispatcher and its workers resume headless (registry + rese… |
| [TC-027](TC-027.md) | Run the agent-loop suite; preflight exits a typed code on a non-git dir / missing CLI / p… |
| [TC-028](TC-028.md) | Run the agent-loop suite; a zero-commit repo is guarded and an all-ERROR region reads as … |
| [TC-029](TC-029.md) | Run the agent-loop suite's lock tests (ported from the retired tracks suite, WI-210): a h… |
| [TC-030](TC-030.md) | Run the agent-loop suite's lock tests (ported from the retired tracks suite, WI-210): a s… |
| [TC-031](TC-031.md) | Run the gate-policy and push-policy suites; each reader returns the first declared line. |
| [TC-032](TC-032.md) | Run the onboard/dev-setup suite; the scaffolded scripts run to a green setup and dev-setu… |
| [TC-033](TC-033.md) | Run gen_release_checklist.py over a warn-tier PB budget; assert the generated checklist l… |
| [TC-034](TC-034.md) | Run the stdlib-only suite; an AST scan asserts every kit script's top-level imports resol… |
| [TC-035](TC-035.md) | Analyze the CI matrix result across Linux/Windows/macOS x Python 3.8/latest. |
| [TC-036](TC-036.md) | Inspect a re-sync done per ADOPTING.md section 6 against the docs/kit-version diff — kit-… |
| [TC-037](TC-037.md) | Run the trajectory-validator suite; a well-formed registry passes, and a malformed WI id,… |
| [TC-038](TC-038.md) | Run the dashboard suite; the generated root HTML is one offline file (no external hosts/C… |
| [TC-039](TC-039.md) | Run the check-dupes suite; a seeded copy-pasted helper fails naming both file:line locati… |
| [TC-040](TC-040.md) | Run the agent-loop suite; a REVIEW-B-mapped phase invokes the second fake CLI and not the… |
| [TC-041](TC-041.md) | Run the doc-refs suite; a dangling path warns then gates under --strict, non-path backtic… |
| [TC-042](TC-042.md) | Run the gen-okf suite; typed linked concepts generate, Process Guide concepts emit for pr… |
| [TC-043](TC-043.md) | Run the subagent-gate suite; a Task/Agent spawn under deny is refused (permissionDecision… |
| [TC-044](TC-044.md) | Run the interface-connectivity suite: trace.py flags a malformed/duplicate IF id and an e… |
| [TC-045](TC-045.md) | Run the skills-sync suite: a hand-edited per-agent copy fails gen_skills_index --check-ag… |
| [TC-046](TC-046.md) | Run the heterogeneous-scheduling suite: agent_route selection honors enable-list order, t… |
| [TC-047](TC-047.md) | Run the run-menu suite: --list prints name<TAB>desc for each declared capability in decla… |
| [TC-048](TC-048.md) | Run the critique-loop suite: the loop schedules CRITIQUE exactly when a committing build'… |
| [TC-049](TC-049.md) | Run the top-view suite: an inventory over 10 modules with no containing CMPs warns plain … |
| [TC-050](TC-050.md) | derive the gate from fixture states across every per-artifact rule and guard the cache; -… |
| [TC-051](TC-051.md) | Run the dashboard suite; the Process tab renders its three panels from the live registrie… |
| [TC-052](TC-052.md) | Run the dashboard suite; with fixture registries exceeding the tier thresholds the When/H… |
| [TC-053](TC-053.md) | A fresh, family-heterogeneous CRITIQUE session (SR-047 loop) adjudicates the generated PR… |
| [TC-054](TC-054.md) | A fresh, family-heterogeneous CRITIQUE session (SR-047 loop) adjudicates the generated PR… |
| [TC-055](TC-055.md) | A fresh, family-heterogeneous CRITIQUE session (SR-047 loop) adjudicates the generated PR… |
| [TC-056](TC-056.md) | Run the dashboard suite; the Process tab renders both loop panels (intake loop A + human-… |
| [TC-057](TC-057.md) | Run the dashboard suite; the tiered decomposition views render one horizontal parent->chi… |
| [TC-058](TC-058.md) | Run schedule.py against a fixture registry; the ready frontier, the exclusions with reaso… |
| [TC-059](TC-059.md) | Drive the pure safety classifier over each SafetyClass + review-policy input including mi… |
| [TC-060](TC-060.md) | Exercise the migration on a fixture scaffold: next-wi/run-phase absent, no live surface r… |
| [TC-061](TC-061.md) | Run two concurrent workers from explicit --wi/--train/worktree assignments; assert no lan… |
| [TC-062](TC-062.md) | Launch the dispatcher with independent ready WIs; assert up-to-ceiling concurrency in sep… |
| [TC-063](TC-063.md) | Drive a unary chain, a fork, a join, a cap, and an early end; assert the continuation/sto… |
| [TC-064](TC-064.md) | Compose overlapping trains through the integrator; assert the combined bar always runs, a… |
| [TC-065](TC-065.md) | Inject termination at each lifecycle boundary (reservation txn, both CAS points, the publ… |
| [TC-066](TC-066.md) | Run a parallel session + a downstream-migration fixture; assert reason-coded telemetry ag… |
| [TC-067](TC-067.md) | Run the cross-CMP suite: an import edge between two components with no covering IF row wa… |
| [TC-068](TC-068.md) | Run the spec-interface suite: an unarmed spec (no ## Interfaces section) is vacuous; a se… |
| [TC-069](TC-069.md) | Run plan_coverage.py over a goal brief + rival plan tables: two commensurable plans emit … |
| [TC-070](TC-070.md) | Drive plan_round with injected fake step results: the happy path selects with the 8-sessi… |
| [TC-071](TC-071.md) | Assemble each hat brief over a fixture repo whose status.md/log.md carry a sentinel and r… |
| [TC-072](TC-072.md) | Drive planner_pair/planner_fallback against docs/agents.csv-shaped fixtures: a two-family… |
| [TC-073](TC-073.md) | Drive plan_coverage_step end-to-end with the real plan_round machine and the real plan_co… |
| [TC-074](TC-074.md) | Build a fixture repo (work-items.csv with the round's parent WI, a selected plan carrying… |
| [TC-075](TC-075.md) | Run the status.md forward-only suite: a done id echoed in a hand-edited status.md warns p… |
| [TC-076](TC-076.md) | Run the real agent_loop --dual-plan over a fixture repo (PlanMode=dual WI, C#-claused goa… |
