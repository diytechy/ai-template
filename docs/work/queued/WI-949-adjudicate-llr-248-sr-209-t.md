+++
id = "WI-949"
title = "adjudicate: LLR-248, SR-209, TC-242 - approved/routed cell(s) amended on merged trunk 0b009fe..b2bea0d (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-209"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-248", "SR-209", "TC-242"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-209 `AcceptanceCriteria`: 'Every process the loop starts carries a marker the commit floor reads, so a commit made from a loop-started process is …' -> 'Every process the loop starts carries a marker the commit floor reads, so a commit made from a loop-started process is …'
- LLR-248 `Detail`: 'The claim, refresh, merge, bookkeeping, handback-close and telemetry writers append format_loop_trailer to their messag…' -> 'The claim, refresh, merge, bookkeeping, handback-close and telemetry writers append format_loop_trailer to their messag…'
- TC-242 `Expected`: "Satisfies SR-209's acceptance: every loop-started process carries the marker; a loop commit without a valid trailer is …" -> "Satisfies SR-209's acceptance: every loop-started process carries the marker; a loop commit without a valid trailer is …"
- TC-242 `Method`: 'The trailer helpers unit-tested: format and parse round-trip, a session the grammar refuses cannot be formatted, the tr…' -> 'The trailer helpers unit-tested: format and parse round-trip, a session the grammar refuses cannot be formatted, the tr…'

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
- LLR-247 [project-trajectory/scripts/kitlib/provenance.py;project-trajectory/scripts/dispatch.py;project-trajectory/scripts/agent_loop.py :: LOOP_TRAILER/LOOP_SESSION_ENV/format_loop_trailer/parse_loop_trailer/loop_trailer_refusal] tests: - — The loop provenance trailer and the loop marker
- LLR-248 [project-trajectory/scripts/integrate.py;project-trajectory/scripts/intake.py;project-trajectory/scripts/handback.py;project-trajectory/scripts/agent_common.py;project-trajectory/hooks/commit-msg;project-trajectory/scripts/bookkeeping.py;project-trajectory/scripts/kitlib/provenance.py :: _claim_locked/_mint/commit_telemetry/_loop_trailer_refusal/_commit_object/LOOP_WRITER_SUBJECTS/loop_writer_commit/loop_lane_window/reclaim_subject/_reclaim] tests: - — Every loop writer carries the trailer, and the floor checks…
- LLR-306 [project-trajectory/scripts/coordinator_adjudicate.py :: DEFAULT_ROUTE/resolve_route/lane_refusal/reserve_verdict/bind_requested/_release/_launched/_call/adjudicate/REVIEWS/_status_paths/_act_inputs/_reviews_written/_act_report/act/signin/main] tests: (see TC-321) — Coordinator adjudication entry attributes a current verdict…
- TC-242 -> tests/test_loop_provenance.py; tests/test_pre_commit_hook.py
- TC-321 -> tests/test_coordinator_adjudicate.py::test_a_second_coordinator_adjudication_resumes_the_first;tests/test_coordinator_adjudicate.py::test_the_coordinator_route_writes_one_session_log_per_call;tests/test_coordinator_adjudicate.py::test_a_session_at_the_dial_drains_and_retires_at_the_next_clear_point;tests/test_coordinator_adjudicate.py::test_an_unknown_route_or_one_off_the_enable_list_is_refused;tests/test_coordinator_adjudicate.py::test_a_missing_or_malformed_verdict_is_reported_and_fails;tests/test_coordinator_adjudicate.py::test_a_failed_call_reusing_a_verdict_path_does_not_return_success;tests/test_coordinator_adjudicate.py::test_a_nonzero_exit_or_a_timeout_fails_whatever_file_exists;tests/test_coordinator_adjudicate.py::test_an_undecodable_brief_is_refused_with_the_usage_exit;tests/test_coordinator_adjudicate.py::test_two_calls_naming_one_verdict_path_never_share_its_verdict;tests/test_coordinator_adjudicate.py::test_a_call_whose_session_writes_into_its_reservation_succeeds;tests/test_coordinator_adjudicate.py::test_a_call_refused_before_launch_releases_its_reservation;tests/test_coordinator_adjudicate.py::test_a_verdict_path_that_cannot_be_reserved_is_refused;tests/test_coordinator_adjudicate.py::test_a_verdict_path_under_a_missing_directory_is_reserved_and_launches;tests/test_coordinator_adjudicate.py::test_a_primary_checkout_root_is_refused_before_launch;tests/test_coordinator_adjudicate.py::test_a_worktree_whose_branch_holds_no_claim_is_refused;tests/test_coordinator_adjudicate.py::test_a_root_outside_any_repository_is_refused;tests/test_coordinator_adjudicate.py::test_the_shipped_entry_point_defaults_to_the_strong_anthropic_route;tests/test_blackout_window.py::test_the_coordinators_adjudication_reports_a_refusal;tests/test_coordinator_act.py::test_the_act_command_refuses_each_trust_input_before_launch;tests/test_coordinator_act.py::test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict;tests/test_coordinator_act.py::test_a_combined_act_commits_its_amendment_act_before_its_first_approval_act;tests/test_coordinator_act.py::test_the_act_turn_reports_success_only_when_no_listed_act_is_left;tests/test_coordinator_act.py::test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed;tests/test_coordinator_act.py::test_an_act_interrupted_between_flip_and_snapshot_is_refused_dirty_then_rerun_in_full;tests/test_coordinator_act.py::test_a_combined_act_interrupted_between_commits_reruns_with_only_its_first_approval_act;tests/test_coordinator_act.py::test_the_act_turn_writes_no_binding_and_reserves_no_path;tests/test_coordinator_act.py::test_under_the_loop_marker_every_launched_prompt_ends_with_the_loop_session_line;tests/test_coordinator_act.py::test_without_the_marker_no_prompt_carries_the_line

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-015 scripts/agent_loop -> external:downstream adopter: git 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paused · 9 REVIEW-OWED …
- IF-170 scripts/subagent_gate -> scripts/agent_loop;external:downstream adopter: file one tab-separated line per non-deferred decision - tool, decision, reason - appended best-effort to the gate …
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-044 scripts/agent_route <- scripts/agent_loop;scripts/session_service: call select() -> the chosen row plus its reason; load_registry(path) -> {id: row}, errors; parse_env(cell) -> {nam…
