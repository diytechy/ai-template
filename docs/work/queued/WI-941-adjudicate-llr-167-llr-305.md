+++
id = "WI-941"
title = "adjudicate: LLR-167, LLR-305, LLR-306, LLR-310, SR-231, TC-161, TC-192, TC-308, TC-321, TC-322 - approved/routed cell(s) amended on merged trunk 702ce85..5604f0f (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-227", "SR-231"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-167", "LLR-305", "LLR-306", "LLR-310", "SR-231", "TC-161", "TC-192", "TC-308", "TC-321", "TC-322"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-231 `AcceptanceCriteria`: 'At every retention-dial value, a coordinator adjudication from the primary checkout, an unclaimed worktree or outside a…' -> 'At every retention-dial value, a coordinator adjudication from the primary checkout, an unclaimed worktree or outside a…'
- SR-231 `Rationale`: 'A DERIVED requirement, and labelled so. SN-025 asks that a configured agent progress without a human curating what come…' -> 'A DERIVED requirement, and labelled so. SN-025 asks that a configured agent progress without a human curating what come…'
- SR-231 `Requirement`: 'The delivered coordinator adjudication entry point shall, regardless of the declared adjudicator retention dial, run on…' -> 'The delivered coordinator adjudication entry point shall, regardless of the declared adjudicator retention dial, run on…'
- LLR-167 `Detail`: 'The route reads `Brief` and `Adjudicates` through the same normalization the merge uses, so a spelling or scope accepte…' -> 'The route reads `Brief` and `Adjudicates` through the same normalization the merge uses, so a spelling or scope accepte…'
- LLR-305 `Detail`: 'REQUEST. AdjudicationRequest carries root, brief, the selected route row, work item, role, prompt-template overrides an…' -> 'REQUEST. AdjudicationRequest carries root, brief, the selected route row, work item, role, prompt-template overrides an…'
- LLR-306 `Detail`: 'ENTRY. coordinator_adjudicate runs only from a claimed lane worktree and otherwise refuses before launch through IF-284…' -> 'ENTRY. coordinator_adjudicate runs only from a claimed lane worktree and otherwise refuses before launch through IF-284…'
- LLR-306 `SR-Refs`: 'SR-227;SR-231' -> 'SR-227;SR-231;SR-209'
- LLR-310 `Detail`: 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…' -> 'A combined class accepts only amendment:<id>, first-approval:<id> and done-when:<id> Adjudicates tokens; it composes ea…'
- TC-161 `Expected`: 'Satisfies SR-146 AcceptanceCriteria' -> 'Satisfies SR-146 AcceptanceCriteria: judging briefs order no act and identify the later act turn.'
- TC-161 `Method`: 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…' -> 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…'
- TC-192 `Method`: 'gen_prompt_catalog.render is exercised directly rather than read. test_the_catalogue_lists_every_shipped_prompt_with_it…' -> 'gen_prompt_catalog.render is exercised directly rather than read. test_the_catalogue_lists_every_shipped_prompt_with_it…'
- TC-308 `Method`: 'Compose a first-approval brief scoped to a Drafted assumption-only case; assert its assumption statement, falsifier and…' -> 'Compose a first-approval brief scoped to a Drafted assumption-only case; assert its assumption statement, falsifier and…'
- TC-321 `Expected`: 'Only a claimed lane worktree launches and writes one attributed session log per call; a second coordinator-route adjudi…' -> 'Only a claimed lane worktree launches and writes one attributed session log per call; a second coordinator-route adjudi…'
- TC-321 `Method`: 'Run test_a_second_coordinator_adjudication_resumes_the_first, test_the_coordinator_route_writes_one_session_log_per_cal…' -> 'Run test_a_second_coordinator_adjudication_resumes_the_first, test_the_coordinator_route_writes_one_session_log_per_cal…'
- TC-321 `Tier`: 'Smoke' -> 'Full'
- TC-321 `Verifies`: 'SR-227;SR-231;LLR-306;IF-283;IF-284;IF-285' -> 'SR-227;SR-231;LLR-306;IF-283;IF-284;IF-285;SR-209'
- TC-322 `Method`: 'Run the existing retained-class identity cases and test_a_retained_reviewers_identity_is_its_own_template. Assert the r…' -> 'Run the existing retained-class identity cases and test_a_retained_reviewers_identity_is_its_own_template. Assert the r…'

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
- LLR-269 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/plan_runner.py :: Call/act/record/call;launch_session;_dp_session] tests: (see TC-265) — One session service launches and records every model call
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py;project-trajectory/scripts/kitlib/config.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/primary_out_dir/store_lock/dir_lock/store_load/load_honoured/is_lease_only/store_remove/keep_release/APPLY_WAIT/_compaction_seen/_marker_name/keep_marker/publish_marker/Pending/_pending/_parse_marker/fold_marker/fold_markers/_released/_landing/Honoured/_folded/_busy/_observation/due_routes/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/retire_after_blackout/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/_prepare_warm/_warm_candidates/_warm_keep/take_warm_lease/scoped_route/retire_scope/review_retention/ReviewRetention/_record_name/_read_record/_variant/_nonempty_str/_conforms;cli_version/plan_keep/KeepWarmer/KeepWarmer._ping/KeepWarmer._record_finished/KeepWarmer._raise_unended/KeepWarmer.finish/_pings_one_turn/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error/auth_failed;adjudication_keep/review_keep_scope/review_keep_templates/draw_session_route;run;reviewer_dials] tests: (see TC-266, TC-267, TC-268, TC-322, TC-329, TC-330) — The keep operation retains adjudicator and loop reviewer se…
- LLR-290 [project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/session_keep.py :: CodexAdapter.compaction;_observe_compaction] tests: TC-303 — Record reported and inferred codex compaction within a reta…
- LLR-305 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_keep.py;project-trajectory/scripts/adjudicate_brief.py :: AdjudicationRequest/adjudication_keep/SigninRefused/SIGNIN_PROBES/TOKEN_VARIABLES/COMPETING_CREDENTIALS/RUNNER_REFUSAL/_read_token/_token_refusal/launch_credential/refuse_competing/_CASE_INSENSITIVE/_name_key/Prepared/prepare_launch/_resolve_executable/probe_env/compose_env/_compose/_runner_argv/_as_prepared/_launch_env/_redactor/signin_status/require_signin/route_env;dedicated_home;governing_templates/_add_act_template] tests: (see TC-322, TC-323, TC-324, TC-330) — Coordinator adjudication shares the keep request and refuse…
- LLR-306 [project-trajectory/scripts/coordinator_adjudicate.py :: DEFAULT_ROUTE/resolve_route/lane_refusal/reserve_verdict/bind_requested/_release/_launched/_call/adjudicate/REVIEWS/_status_paths/_act_inputs/_reviews_written/_act_report/act/signin/main] tests: (see TC-321) — Coordinator adjudication entry attributes a current verdict…
- LLR-338 [project-trajectory/scripts/adjudicate_act.py :: ACTABLE/NONE_OWED/NO_ACT/RETIRE/_verdict_rel/_unaccepted_reason/_accepted/_tier/_held/_arm/_authorized/_Rows/_claims_approval/_retirement/_state/_odd/owed_acts/_recorded/_grouped/_derive/left_owed/bound_brief/_amendment_text/_approval_text/act_values/compose_act] tests: TC-368 — Act assembly from a committed accepted verdict

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-061 scripts/plan_artifacts <- scripts/plan_runner: call allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-064 scripts/agent_session <- scripts/agent_loop;scripts/session_service;scripts/plan_runner: call build_argv, run_session, parse_json_result and the console renderers
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
