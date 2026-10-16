+++
id = "WI-932"
title = "adjudicate: LLR-069, LLR-311, LLR-313, LLR-314, SR-233, SR-234, SR-236, TC-069, TC-332, TC-333, TC-334 - approved/routed cell(s) amended on merged trunk 962921f..247dc36 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-233", "SR-234", "SR-236"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-069", "LLR-311", "LLR-313", "LLR-314", "SR-233", "SR-234", "SR-236", "TC-069", "TC-332", "TC-333", "TC-334"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-233 `AcceptanceCriteria`: 'The review scope includes repository content agents write, supported configurations, and regressions of supported behav…' -> 'The review scope includes repository content agents write, supported configurations, and regressions of supported behav…'
- SR-234 `AcceptanceCriteria`: 'A composed adjudication carries exactly the requested findings, each finding and held position verbatim, change-range f…' -> 'A composed adjudication carries exactly the requested findings, each finding and held position verbatim, change-range f…'
- SR-234 `Requirement`: 'Where a review finding is contested by the builder or coordinator, or recurs for a third review round, the delivered ad…' -> 'Where a review finding is contested by the builder or coordinator, or recurs for a third review round, the delivered ad…'
- SR-236 `AcceptanceCriteria`: 'A review verdict or a declared F# findings input produces one ordered clause per finding; dispatch is refused while any…' -> 'A review verdict or a declared F# findings input produces one ordered clause per finding; dispatch is refused while any…'
- SR-236 `Rationale`: 'A DERIVED requirement, and labelled so. SN-024 requires an independent critical eye to drive rework, but does not say h…' -> 'A DERIVED requirement, and labelled so. SN-024 requires an independent critical eye to drive rework, but does not say h…'
- SR-236 `Requirement`: 'When a reviewed change requires rework, the delivered review workflow shall dispatch that rework only after its plan co…' -> 'When a reviewed change requires rework, the delivered review workflow shall dispatch that rework only after its plan co…'
- LLR-069 `Detail`: 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…' -> 'Uses one plan-table grammar for dual goal and single item runs. Resolves clause, SR, TC and interface references; valid…'
- LLR-311 `Detail`: 'The §6 bold-lead paragraph `Review threat model` defines the review scope: normal-environment defects include repositor…' -> 'The §6 bold-lead paragraph `Review threat model` defines the review scope: normal-environment defects include repositor…'
- LLR-314 `Detail`: 'kitlib.dispute accepts one TOML findings file with only a non-empty `range` and a non-empty `[[finding]]` list. Each fi…' -> 'kitlib.dispute accepts one TOML findings file with only a non-empty `range` and a non-empty `[[finding]]` list. Each fi…'
- LLR-313 `Detail`: 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…' -> 'Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file, and…'
- TC-069 `Expected`: 'A review verdict yields ordered F# clauses for its declared-severity findings only; a bracketed non-severity bullet yie…' -> 'A review verdict yields ordered F# clauses for its declared-severity findings only; a bracketed non-severity bullet yie…'
- TC-069 `Method`: 'Run dual and single plan coverage, reference, graph, exclusion, review-verdict finding, dispute-ruling, SR/TC-diff, abs…' -> 'Run dual and single plan coverage, reference, graph, exclusion, review-verdict finding, dispute-ruling, SR/TC-diff, abs…'
- TC-332 `Expected`: 'The `Review threat model` bold lead occurs once; its paragraph contains `the content agents write into the repository`,…' -> 'The `Review threat model` bold lead occurs once; its paragraph contains `the content agents write into the repository`,…'
- TC-332 `Method`: 'Run test_the_reviewer_brief_links_the_review_threat_model_and_restates_nothing: it reads the §6 bold-lead paragraph, as…' -> 'Run test_the_reviewer_brief_links_the_review_threat_model_and_restates_nothing: it reads the §6 bold-lead paragraph, as…'
- TC-334 `Expected`: 'A dispute brief contains every requested finding and position verbatim with independently derived range facts and a rev…' -> 'A dispute brief contains every requested finding and position verbatim with independently derived range facts and a rev…'
- TC-334 `Method`: 'Run the dispute tests that compose a brief carrying every finding, held position, range fact and review-scope link; ref…' -> 'Run the dispute tests that compose a brief carrying every finding, held position, range fact and review-scope link; ref…'
- TC-334 `Tier`: 'Smoke' -> 'Full'
- TC-333 `Expected`: 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…' -> 'A complete attended review or critique brief has no unfilled slot and carries the shipped review clauses, lane facts or…'
- TC-333 `Method`: 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…' -> 'Run test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts, test_a_narrow_round_names_the_findings_it_…'

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
- LLR-069 [project-trajectory/scripts/plan_coverage.py :: parse_goal/finding_clauses/parse_plan/check_plan/find_cycle/format_report/parse_excludes/verifying_tcs/ref_problem/_covers_findings/_interfaces_findings/check_excludes/ruling_problem/_finding_key/_tree_text/_tree_tomls/_ruled_texts/_correspondence_problem/resolution_findings/gap_findings/spine_diff/diff_findings/_plan_section/_malformed/_read/_declared/load_item/_parse_args/_check_one/_load_gate] tests: (see TC-069) — Plan coverage gate
- LLR-311 [project-trajectory/PROCESS.md;project-trajectory/prompts/reviewer.template.md;project-trajectory/prompts/adjudicate-dispute.template.md :: Review threat model;REVIEWER;ADJUDICATE-DISPUTE] tests: TC-332 — Review threat-model definition and reviewer reference
- LLR-314 [project-trajectory/scripts/kitlib/dispute.py :: BRIEF/RULINGS/DISMISS_REASONS/HELD_BY/read_findings/request_line/requested_ids/parse] tests: TC-334 — Dispute findings and verdict grammar is parsed once
- LLR-315 [project-trajectory/scripts/adjudicate_brief.py :: DISPUTE/BRIEF_PROMPTS/dispute_values/_render_finding] tests: TC-334 — Dispute brief assembly carries bounded findings to the adju…
- TC-069 -> tests/test_plan_coverage.py::test_the_shared_step_turns_a_real_verdict_into_F_clauses; tests/test_plan_coverage.py::test_a_bracketed_word_that_is_not_a_severity_never_shifts_the_F_ids; tests/test_plan_coverage.py::test_a_findings_file_mixing_both_shapes_is_malformed; tests/test_plan_coverage.py::test_an_uncovered_review_finding_refuses_the_dispatch; tests/test_plan_coverage.py::test_covered_or_excluded_review_findings_pass; tests/test_plan_coverage.py::test_a_dismissed_dispute_citing_its_ruling_passes; tests/test_plan_coverage.py::test_a_dispute_ruling_cited_by_its_own_id_passes; tests/test_plan_coverage.py::test_a_dismissal_of_an_unrelated_finding_refuses; tests/test_plan_coverage.py::test_a_dismissal_from_another_round_under_the_same_id_refuses; tests/test_plan_coverage.py::test_a_dismissal_whose_finding_cannot_be_shown_refuses; tests/test_plan_coverage.py::test_a_ruling_of_the_same_finding_passes_through_typographic_drift; tests/test_plan_coverage.py::test_a_cited_ruling_that_does_not_dismiss_refuses; tests/test_plan_coverage.py::test_a_real_dispute_verdict_ruling_FIX_refuses_its_exclusion; tests/test_plan_coverage_step.py::test_an_unexcluded_gap_in_plan_a_alone_bounces_only_a;tests/test_plan_coverage.py::test_a_successor_ruling_citing_its_verdict_passes;tests/test_plan_coverage.py::test_a_successor_ruling_of_another_finding_refuses
- TC-332 -> tests/test_prompts.py::test_the_reviewer_brief_links_the_review_threat_model_and_restates_nothing;tests/test_prompts.py::test_the_dispute_brief_offers_successor_and_never_for_a_convergence_class_finding;tests/test_prompts.py::test_the_reviewer_brief_ties_severity_to_reachability_and_classifies_out_of_set_inputs;tests/test_prompts.py::test_the_reviewer_brief_states_the_convergence_stance;tests/test_prompts.py::test_the_convergence_render_excludes_every_record_of_earlier_findings;tests/test_prompts.py::test_the_review_threat_model_dismisses_contrived_scenarios_and_gates_every_class;tests/test_prompts.py::test_a_spec_promise_reaches_only_what_supported_routes_produce

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-060 scripts/plan_coverage -> scripts/plan_coverage_step: exit-code 0 clean | 1 findings, including unexplained clause gaps or SINGLE SR/TC misses | 2 malformed input, including…
- IF-152 scripts/plan_coverage <- scripts/plan_coverage_step: cli --goal | --item [--findings], --root, --out, then the plan paths
- IF-153 scripts/plan_coverage -> scripts/plan_coverage_step: file the --out coverage report: coverage and exclusions per plan, a SINGLE SR/TC diff, and a pairwise diff over tw…
- IF-057 docs/requirements/interfaces.toml -> scripts/plan_coverage;external:downstream adopter: file one table per seam, keyed by IF id; cells per the file header
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/dispatch;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict;scripts/plan_coverage;scripts/review_brief: call parse_verdict: typed verdict findings, where a finding is a bullet whose bracket names one of the module's de…
