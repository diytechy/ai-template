+++
id = "WI-939"
title = "adjudicate: LLR-026, SR-238, TC-026 - approved/routed cell(s) amended on merged trunk 3a11f46..ab16614 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-238"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-026", "SR-238", "TC-026"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-931's in-lane checkpoint sitting
`docs/reviews/wi-931/003-ADJUDICATE-4dbd3bd.md` blessed SR-238, LLR-026 and TC-026
as MEANING, and act seq 125 re-attested them. At the landing ab16614fa the
system, low-level and test registries are byte-equal to their approved
snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-238 `AcceptanceCriteria`: "At a wall deadline, an idle deadline, or a coordinator interruption once the platform's process creation has returned t…" -> 'At a wall deadline, an idle deadline, or a coordinator interruption while the coordinator supervises a launched session…'
- SR-238 `Rationale`: 'A descendant can outlive the direct session child and keep editing the worktree handed to the next session. Ending only…' -> 'A descendant can outlive the direct session child and keep editing the worktree handed to the next session. Ending only…'
- LLR-026 `Detail`: 'Runs the agent CLI headless: build_argv substitutes {model} into argv and, when a CmdTemplate carries no {prompt} place…' -> 'Runs the agent CLI headless: build_argv substitutes {model} into argv and, when a CmdTemplate carries no {prompt} place…'
- LLR-026 `Rationale`: 'A large prompt passed as argv dies at the OS command-line cap (8191 characters through a Windows .CMD shim, 32767 via C…' -> 'A large prompt passed as argv dies at the OS command-line cap (8191 characters through a Windows .CMD shim, 32767 via C…'
- TC-026 `Expected`: 'Satisfies SR-026 AcceptanceCriteria; the bounded descendants have ended when the coordinator continues, with no grace p…' -> 'Satisfies SR-026 AcceptanceCriteria; the bounded descendants have ended when the coordinator continues, with no grace p…'
- TC-026 `Method`: 'Run the agent-loop suite; the dispatcher and its workers resume headless (registry + reservations + explicit assignment…' -> 'Run the agent-loop suite; the dispatcher and its workers resume headless (registry + reservations + explicit assignment…'

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
- LLR-026 [project-trajectory/scripts/agent_session.py;project-trajectory/scripts/session_adapters.py :: build_argv/run_session/_codex_lastmsg_setup/_win32/_contain_in_job/_spawn_session/_start_session_io/_feed_stdin/TreeNotEnded/_kill_tree/_end_job_tree/_end_group_tree/_terminate_job/_open_job_members/_close_handles/_job_active_processes/_job_survivors/_group_survivors/_await_tree_end] tests: (see TC-026) — Headless session launch
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py;project-trajectory/scripts/kitlib/config.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/primary_out_dir/store_lock/dir_lock/store_load/load_honoured/is_lease_only/store_remove/keep_release/APPLY_WAIT/_compaction_seen/_marker_name/keep_marker/publish_marker/Pending/_pending/_parse_marker/fold_marker/fold_markers/_released/_landing/Honoured/_folded/_busy/_observation/due_routes/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/retire_after_blackout/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/_prepare_warm/_warm_candidates/_warm_keep/take_warm_lease/scoped_route/retire_scope/review_retention/ReviewRetention/_record_name/_read_record/_variant/_nonempty_str/_conforms;cli_version/plan_keep/KeepWarmer/KeepWarmer._ping/KeepWarmer._record_finished/KeepWarmer._raise_unended/KeepWarmer.finish/_pings_one_turn/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error/auth_failed;adjudication_keep/review_keep_scope/review_keep_templates/draw_session_route;run;reviewer_dials] tests: (see TC-266, TC-267, TC-268, TC-322, TC-329, TC-330) — The keep operation retains adjudicator and loop reviewer se…
- TC-026 -> tests/test_agent_loop.py; tests/test_session_stdin.py::test_a_deadline_kill_ends_the_grandchild; tests/test_session_stdin.py::test_an_interruption_ends_the_grandchild; tests/test_session_stdin.py::test_an_uncontainable_child_errors_before_it_runs; tests/test_session_stdin.py::test_a_tree_not_ended_within_the_bound_raises; tests/test_session_stdin.py::test_a_member_the_kill_cannot_open_makes_it_raise; tests/test_session_stdin.py::test_an_ordinary_launch_error_still_returns_the_session_error; tests/test_session_stdin.py::test_run_session_idle_deadline_kills_a_silent_child
- TC-266 -> tests/test_session_keep.py
- TC-267 -> tests/test_session_keep.py::test_a_bookkept_call_under_contention_keeps_its_observation_and_resumes;tests/test_session_keep.py::test_a_draining_call_under_contention_drains_and_is_not_retired;tests/test_session_keep.py::test_an_auth_failure_release_under_contention_never_retires_the_session;tests/test_session_keep.py::test_a_keep_warm_ping_under_contention_leaves_no_lease_and_stays_warm;tests/test_session_keep.py::test_a_release_marker_never_makes_keep_warm_skip_the_record;tests/test_session_keep.py::test_a_reader_that_saw_expiry_after_a_release_was_published_does_not_retire;tests/test_session_keep.py::test_a_reader_never_deletes_a_marker_it_did_not_apply;tests/test_session_keep.py::test_retire_scope_under_contention_retires_on_the_next_read;tests/test_session_keep.py::test_a_retire_marker_spares_a_newer_session_and_a_lease_it_does_not_hold;tests/test_session_keep.py::test_a_malformed_marker_is_deleted_with_one_line_and_read_as_absent;tests/test_session_keep.py::test_an_unreadable_marker_stays_and_holds_back_the_expired_lease;tests/test_session_keep.py::test_a_failed_publication_raises_to_the_caller;tests/test_session_keep.py::test_a_replayed_bookkeep_marker_never_frees_a_newer_holders_lease;tests/test_session_keep.py::test_after_a_failed_unlink_two_competing_resumed_calls_get_one_session;tests/test_session_keep.py::test_a_replayed_release_is_inert;tests/test_session_keep.py::test_a_replayed_retire_is_inert;tests/test_session_keep.py::test_a_replayed_scope_retirement_spares_the_next_reviewer;tests/test_session_keep.py::test_an_overrun_calls_late_bookkeep_never_frees_its_successors_lease;tests/test_adjudicator_token.py::test_an_auth_failure_records_the_call_failed_and_keeps_the_session;tests/test_adjudicator_token.py::test_an_auth_failure_on_a_first_mint_leaves_no_record;tests/test_adjudicator_token.py::test_another_failure_still_retires_the_session;tests/test_blackout_window.py::test_the_first_keep_call_after_a_window_retires_by_the_predicate;tests/test_blackout_window.py::test_a_draining_sessions_chain_does_not_survive_the_window;tests/test_blackout_window.py::test_a_wrap_up_inside_the_window_resumes_the_retained_session;tests/test_blackout_window.py::test_no_keep_warm_ping_fires_inside_the_window;tests/test_blackout_window.py::test_a_keep_warm_tick_first_after_the_window_retires_and_never_refreshes;tests/test_session_keep.py::test_a_lock_create_refused_once_as_access_denied_is_retried_and_taken;tests/test_session_keep.py::test_a_lock_create_refused_as_access_denied_past_the_wait_is_busy_and_named;tests/test_session_keep.py::test_any_other_lock_create_refusal_is_raised_at_once
- TC-329 -> tests/test_session_keep.py::test_two_concurrent_first_calls_mint_one_session_and_run_one_unretained;tests/test_session_keep.py::test_a_crashed_first_calls_lease_expires_and_is_retired;tests/test_session_keep.py::test_a_late_first_mint_never_replaces_the_session_that_took_its_lease_over;tests/test_session_keep.py::test_a_first_mint_that_raises_removes_its_lease_only_record;tests/test_session_keep.py::test_at_dial_zero_a_first_call_writes_no_lease;tests/test_session_keep.py::test_a_first_call_whose_lock_create_is_refused_as_access_denied_runs_unretained

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-245 scripts/session_adapters <- scripts/session_service: call USAGE_KEYS, OTEL_SEMCONV; adapter_for(argv) -> adapter; adapter.prepare, final_text, raw_usage, usage, context
- IF-266 scripts/session_adapters -> scripts/session_service;scripts/session_keep: call compaction(stream, env, session_id) -> {reported: bool, prompts: list[int], totals: list[int]} for codex, els…
