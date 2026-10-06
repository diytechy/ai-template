+++
id = "WI-843"
title = "adjudicate: LLR-300, SR-229, TC-316, TC-318 - approved/routed cell(s) amended on merged trunk dc1d285..f9265d9 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-229"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-300", "SR-229", "TC-316", "TC-318"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-842's in-lane adjudicator, through the retained session, ruled SR-229, LLR-300, TC-316 and TC-318 MEANING and blessed them (verdict `docs/reviews/wi-842-coordinator-hands-back-lease/001-ADJUDICATE-b6c13a8.md`, act seq 41). The low-level, system and test-case registries are byte-identical to their anchors under `docs/archive/last_approved/` at the landing.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-229 `AcceptanceCriteria`: 'With the guard off, admission proceeds without reading or writing guard state; with it on, the holder below the thresho…' -> 'With the guard off, admission proceeds without reading or writing guard state; with it on, the holder below the thresho…'
- SR-229 `Requirement`: 'Where the declared coordinator context guard is enabled, the delivered work-item admission, on every route but the unat…' -> 'Where the declared coordinator context guard is enabled, the delivered work-item admission, on every route but the unat…'
- LLR-300 `Detail`: 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…' -> 'guard_config reads the declared coordinator threshold and window: a non-positive, out-of-range or malformed threshold i…'
- TC-316 `Expected`: 'Exactly one coordinator owns admission, a claim without its lease refuses naming the recovery action, and the drain sta…' -> 'Exactly one coordinator owns admission, a claim without its lease refuses naming the recovery action, and the drain sta…'
- TC-316 `Method`: 'Drive holder, other-session and subagent hook payloads and guarded claims with controlled transcript readings and lease…' -> 'Drive holder, other-session and subagent hook payloads and guarded claims with controlled transcript readings and lease…'
- TC-318 `Method`: "Drive relaunch requests and session-end payloads with a stub launcher, and the guard's command line. Assert holder and …" -> "Drive relaunch requests and session-end payloads with a stub launcher, and the guard's command line. Assert holder and …"

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
- LLR-300 [project-trajectory/scripts/coordinator_guard.py;project-trajectory/scripts/integrate.py :: GuardConfig/guard_config/Occupancy/read_occupancy/lease_dir/take/release/clear/hand_back/record_event/latch_reading/claim_refusal/on_monitored/on_session_start/on_pre_compact/classify_compaction/hook;claim] tests: TC-315;TC-316;TC-317 — Coordinator context occupancy, lease, and drain latch
- TC-315 -> tests/test_coordinator_guard.py::test_occupancy_counts_input_cache_read_and_cache_creation;tests/test_coordinator_guard.py::test_a_branched_transcript_reads_the_live_branch;tests/test_coordinator_guard.py::test_a_sidechain_record_is_never_the_live_tip;tests/test_coordinator_guard.py::test_after_compaction_only_usage_after_the_last_boundary_counts;tests/test_coordinator_guard.py::test_the_recorded_compaction_fixture_is_claude_code_2_1_289;tests/test_coordinator_guard.py::test_a_recorded_compaction_reads_the_reply_after_the_boundary;tests/test_coordinator_guard.py::test_a_recorded_compaction_never_reads_a_preserved_messages_old_usage;tests/test_coordinator_guard.py::test_after_a_resume_the_newest_usage_counts_whatever_session_wrote_it;tests/test_coordinator_guard.py::test_malformed_and_partial_usage_is_skipped_to_the_newest_valid;tests/test_coordinator_guard.py::test_no_valid_usage_reads_unknown_never_zero;tests/test_coordinator_guard.py::test_a_mismatched_window_is_flagged_with_its_percent;tests/test_coordinator_guard.py::test_admission_compares_unrounded_occupancy;tests/test_coordinator_guard.py::test_the_reader_reads_the_tail_and_widens_only_to_resolve
- TC-316 -> tests/test_coordinator_guard.py::test_a_subagent_and_another_sessions_hook_calls_are_no_ops;tests/test_coordinator_guard.py::test_a_claim_names_its_caller_by_claude_code_session_id;tests/test_coordinator_guard.py::test_with_no_lease_held_a_claim_refuses_naming_the_take;tests/test_coordinator_guard.py::test_a_non_holders_claim_refuses_naming_the_holder_and_the_release;tests/test_coordinator_guard.py::test_the_holders_claim_below_threshold_passes;tests/test_coordinator_guard.py::test_a_silent_live_holder_keeps_the_lease_however_long_it_is_quiet;tests/test_coordinator_guard.py::test_the_owners_release_frees_the_lease_and_is_recorded;tests/test_coordinator_guard.py::test_the_relaunched_successor_takes_the_lease_at_session_start;tests/test_coordinator_guard.py::test_the_latch_holds_after_a_compaction_drops_the_reading;tests/test_coordinator_guard.py::test_the_latch_survives_a_resumed_session_and_is_restated;tests/test_coordinator_guard.py::test_only_the_owners_recorded_clear_or_the_successor_unlatches;tests/test_coordinator_guard.py::test_the_instruction_comes_once_at_the_latch_then_bounded_reminders;tests/test_coordinator_guard.py::test_pre_compact_records_trigger_occupancy_and_guard_state;tests/test_coordinator_guard.py::test_the_handoff_classifies_each_compaction;tests/test_coordinator_guard.py::test_the_holders_hand_back_frees_the_lease_for_the_next_take;tests/test_coordinator_guard.py::test_another_sessions_or_a_promptless_hand_back_is_refused;tests/test_coordinator_guard.py::test_a_drained_holder_hands_back_and_the_next_take_is_unlatched;tests/test_coordinator_guard.py::test_a_hand_back_with_a_relaunch_requested_is_refused;tests/test_coordinator_guard.py::test_a_previous_holders_request_never_blocks_the_current_holders_hand_back
- TC-317 -> tests/test_coordinator_guard.py::test_off_means_off_claims_pass_and_hooks_do_nothing;tests/test_coordinator_guard.py::test_a_malformed_threshold_leaves_the_guard_off;tests/test_coordinator_guard.py::test_the_crossing_replys_claim_refuses_via_the_pre_tool_use_reading;tests/test_coordinator_guard.py::test_the_crossing_replys_claim_refuses_with_no_hook_run;tests/test_coordinator_guard.py::test_the_live_dispatchers_claim_route_is_untouched;tests/test_coordinator_guard.py::test_only_the_claim_consults_the_guard_so_close_out_passes;tests/test_coordinator_guard.py::test_a_draining_pre_tool_use_never_denies_a_close_out_command;tests/test_coordinator_guard_e2e.py::test_the_cli_claim_refuses_while_draining;tests/test_coordinator_guard_e2e.py::test_a_wrapper_importing_integrate_is_refused;tests/test_coordinator_guard_e2e.py::test_close_out_git_operations_pass_while_draining;tests/test_coordinator_guard_e2e.py::test_the_hook_cli_reads_stdin_and_prints_its_output;tests/test_coordinator_guard_e2e.py::test_a_lane_worktree_shares_the_primary_checkouts_lease;tests/test_session_keep.py::test_the_store_lock_excludes_a_second_holder;tests/test_coordinator_guard.py::test_with_the_guard_off_a_hand_back_reads_and_writes_nothing

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
- IF-055 scripts/schedule <- scripts/integrate: call frontier over the loaded rows, in deterministic order
- IF-065 scripts/agent_common <- scripts/agent_loop;scripts/integrate;scripts/session_service;scripts/session_keep: call END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_config, load_wi_registry…
