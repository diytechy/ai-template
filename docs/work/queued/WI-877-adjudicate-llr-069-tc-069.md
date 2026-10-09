+++
id = "WI-877"
title = "adjudicate: LLR-069, TC-069 - approved/routed cell(s) amended on merged trunk 0b550da..c6a2eab (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-155"]
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-069", "TC-069"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-069 `Detail`: 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…' -> 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…'
- LLR-069 `SR-Refs`: 'SR-155' -> 'SR-155;SR-236'
- TC-069 `Expected`: 'A reasoned exclusion passes and clean plans emit per-plan and pairwise coverage; a bad reference or plan graph, an unex…' -> 'A review verdict yields ordered F# clauses; a covered or reasoned-excluded finding passes; an uncovered finding, bad re…'
- TC-069 `Method`: 'Run dual and single plan coverage, reference, graph, exclusion, SR/TC-diff, absent-registry, and malformed-input cases.' -> 'Run dual and single plan coverage, reference, graph, exclusion, review-verdict finding, dispute-ruling, SR/TC-diff, abs…'
- TC-069 `Verifies`: 'SR-155;LLR-069' -> 'SR-155;SR-236;LLR-069'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-069 [project-trajectory/scripts/plan_coverage.py :: parse_goal/finding_clauses/parse_plan/check_plan/find_cycle/format_report/parse_excludes/verifying_tcs/ref_problem/_covers_findings/_interfaces_findings/check_excludes/ruling_problem/_finding_key/_ruled_texts/_correspondence_problem/resolution_findings/gap_findings/spine_diff/diff_findings/_plan_section/_malformed/_read/_declared/load_item/_parse_args/_check_one/_load_gate] tests: (see TC-069) — Plan coverage gate
- LLR-070 [project-trajectory/scripts/plan_round.py :: new_round/ready_steps/record/disposition/page_action] tests: (see TC-070) — Typed dual-plan round lifecycle
- LLR-071 [project-trajectory/scripts/plan_briefs.py :: build_surface/assemble/load_template/strip_dispatcher_block/HAT_KEYS] tests: (see TC-071) — Allowlist-only dual-plan briefs
- LLR-072 [project-trajectory/scripts/agent_route.py :: planner_pair/planner_fallback] tests: (see TC-072) — Dual-plan planner pair and fallback
- LLR-073 [project-trajectory/scripts/plan_coverage_step.py :: run_coverage/to_record_kwargs/_implicated_plans] tests: (see TC-073) — Coverage-step result adapter
- LLR-074 [project-trajectory/scripts/plan_artifacts.py :: allocate_round_dir/write_stage/file_selected_wis/append_log_summary/parse_plan_wis] tests: (see TC-074) — Dual-plan artifact persistence and filer

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-059 docs/requirements/ -> scripts/plan_briefs;external:downstream adopter: file SR id, title, requirement; IF id, owner, far side, channel, data
- IF-060 scripts/plan_coverage -> scripts/plan_coverage_step: exit-code 0 clean | 1 findings, including unexplained clause gaps or SINGLE SR/TC misses | 2 malformed input, including…
