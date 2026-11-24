# WI-1024 slice 3: the record

The third of the five slices the plan ([plan.md](plan.md), section 4) sets
out: the population of the interfaces CMP-008 owns, for sittings C1 and C2.
Built on `maint/wi-1024` at `d7e3a57df` (slice 1 merged as `6ed2cfc28`, slice
2 as `88e589103`), from the confirmed plan and the coordinator's answers to
slice 1's four questions (the brief, after the eighth sitting's verdict,
[001-ADJUDICATE-fbd50be.md](../../reviews/wi-1068-adjudicate-eighth-sitting/001-ADJUDICATE-fbd50be.md)).
It also carries the two items slice 2 handed on (IF-049 and IF-144, its
section 6) and, in its own commit, the answer to the ninth sitting's LLR-014
disposition (section 8). The spec stays in `docs/work/queued/` until slice 5
(D10); this file stands in for the Deliverable until then, as
[slice-1.md](slice-1.md) and [slice-2.md](slice-2.md) do. Review round 1's
fixes are folded into the sections below and recorded in section 7.

Registries and tests only: no shipped file changed, so no RESYNC entry.

The judging was split by surface over five parallel passes in one worktree,
each drafting its rows, clause accounting and tests from the same brief; the
builder integrated them, applied the registry changes once and ran the module
set over the whole (section 2).

## 1. What changed, against the Done-when

| Done-when | Slice 3 |
|---|---|
| 1. The cells | Unchanged (slice 1). |
| 2. The derived check | Unchanged; its count line moves (section 3.3). |
| 3. The repeat check | Unchanged; it now reports one repeated name, TC-301's IF-264 (section 6, item 9). |
| 4. Every interface reached | CMP-008: 71 of its 76 interfaces now reached through a constraining design row; the other five carried (section 6, items 3 and 4), each reached through its naming test cases. IF-049 (slice 2's) linked. IF-144 measured, a proposal for the coordinator (section 6, item 2). 135 of 239 overall. |
| 5. Strict, OI-43 retired | Not in this slice (slice 5). |
| 6. The readers | Unchanged. |
| 7. RESYNC | None owed: no shipped file changed. |
| 8. Checks and tests | Section 2. |

The registry changes: 45 accepted design rows gain `constrains`, 35 of them
with `detail` amended under rule 1 and answers 1 and 5 (every recorded clause
kept, code names scrubbed, and the behaviour across the named interface written
in and tested where the text did not yet state it) and 10 a link only;
review round 1 (section 7) amended one of the ten, LLR-339, so 36 amend
`detail` and nine are links only. No `title` changed; round 1 amended one
`rationale` (LLR-306) and added a parent to two requirements cells
(LLR-137 gains SR-173, LLR-301 SR-229, both routed). Of the 45,
four are rows slices 1 and 2 linked and the ninth sitting re-accepted on
trunk (LLR-031, LLR-040, LLR-047, LLR-247), each gaining a further routed
link (LLR-040 a sentence too). No new row and no id minted: every CMP-008
interface whose behaviour a row could state already had a row stating it
(answer 2), so the brief's ranges (LLR-496 to LLR-510, TC-589 to TC-605) are
unused and there was no mint for `trace.py --bump-ids` to follow. 25 test
cases gain tagged tests in `evidence` (traced, no act owed), and round 1
tagged more for TC-028, TC-046, TC-058, TC-321 and TC-369 and amended
TC-028's `method` and `expected`. No `dimensions` or
`out_of_domain` cell (answer 4).

In its own commit, the ninth sitting's LLR-014 disposition: LLR-014's
`detail` and TC-014's `method` and `expected` amended, three tests of
`tests/test_check_perf.py` added and two extended (section 8).

## 2. The tests added and run

**Added for a kept or new clause no named test drove** (answer 1), each shown
to fail against a deliberate breakage of the behaviour and to pass restored:
a scratch runner replaced the code byte-exact, ran the one test by node id and
restored the file in the same process (`git status` clean after each). The
failing line each breakage drew is quoted.

| Test | Row, clause | Breakage it caught |
|---|---|---|
| `tests/test_guardrails_payload.py::test_an_unreadable_chosen_payload_reads_as_no_core_and_the_session_runs_past_it` | LLR-280, an unreadable chosen payload reads as no core, reported once | the reader falling back to the default core on a read error: `AssertionError: assert 'DEFAULT-CORE' is None` |
| `tests/test_guardrails_payload.py::test_equal_length_substrings_fall_to_name_order` | LLR-280, then by name | the tie ordered by reverse name: `AssertionError: assert 'SONNET-PAYLOAD' == 'CLAUDE-PAYLOAD'` |
| `tests/test_trajectory_forward_only.py::test_an_unknown_id_and_an_absent_status_page_draw_no_finding` | LLR-075, unknown ids and an absent status page | (a) the absent-page guard removed: `FileNotFoundError: [Errno 2] No such file or directory: '...docs\\status.md'`; (b) every id named, not only done ones: `assert (2 == 1)` |
| `tests/test_trunk_step.py::test_the_step_runs_the_operations_it_is_asked_for_compile_first` | LLR-137, the invocation forms, compile first, exit 1 on a failed compile with no regeneration | (a) the regeneration run whatever was asked: `AssertionError: assert ('would append 1 fragment(s)' in ... and 'regen' not in ...)`; (b) a failed compile not stopping the step: `AssertionError: assert 0 == 1`; (c) the regeneration run before the compile: `AssertionError: assert 968 < 12` |
| `tests/test_trunk_step.py::test_fragments_added_by_one_commit_fold_in_file_name_order` | LLR-137, the file name breaking a tie | the tie sorted by reverse name: `AssertionError: assert 82 < 65` |
| `tests/test_trunk_step.py::test_fragments_are_appended_through_the_shared_log_appender` | LLR-137, through the shared appender | a direct append to the log: `AssertionError: assert [] == ['## WI-14 — shared appender\n']` |
| `tests/test_trunk_step.py::test_the_log_compile_never_commits_the_caller_owns_the_commit` | LLR-137, never commits | a commit after the delete: `AssertionError: assert 'e6a998c6a228...' == 'f843051589eb...'` |
| `tests/test_schedule.py::test_cli_prints_the_frontier_and_the_simulation_as_text_lines` | LLR-058, text lines | the simulation printing JSON whatever the format: `assert ['{', '  "job...'] == ['round 1   (... (1): WI-002']` |
| `tests/test_schedule.py::test_a_generated_view_projects_the_frontier_and_omits_it_without_the_scheduler` | LLR-058, the status page's frontier block, in order, absent without the scheduler | (a) the absent-scheduler guard removed: `AttributeError: 'NoneType' object has no attribute '_load'`; (b) the block re-sorted by id: `AssertionError: assert (217 < 193)` |
| `tests/test_integrate_station.py::test_the_queue_restricted_to_named_branches_merges_only_those` (new, tagged TC-145) | LLR-151, the queue's restriction to named branches | the restriction dropped, every finished branch queued: the merge refused the branch the restriction left out (`AssertionError: integrate: wi-401 is not merge-ready ...`), `1 failed in 9.25s` |
| `tests/test_done_when_blessing.py::test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close` (extended: `capsys`, the printed refusal and its digest; tagged TC-132 beside TC-325) | LLR-140, the Done-when hold command prints its refusal and exits nonzero | the command returning 1 without printing: `assert ('integrate: REFUSED' in '')`, `1 failed in 3.76s` |
| `tests/test_dispute.py::test_a_findings_text_keeps_its_spaces_and_drops_only_its_edge_newlines` | LLR-314, clause 3 | the reader stripping all whitespace, not newlines: `assert 'indented fir...  second line' == '  indented f...second line  '`, `1 failed in 0.26s` |
| `tests/test_dispute.py::test_the_first_request_and_findings_file_lines_are_the_ones_read` | LLR-314, clauses 4 and 5 | (a) the last request line read: `assert ('F9',) == ('F1', 'R2')`; (b) the last findings-file line read: `assert 'other.toml' == 'findings.toml'`; (c) an empty line supplying an empty path: `assert '' is None`; each `1 failed` (0.28s, 0.26s, 0.27s) |
| `tests/test_plan_filing.py::test_the_dispute_findings_file_is_never_written_over_an_existing_one` | LLR-313, clause 17 | the existence check and the exclusive open both removed: `assert 0 == 2`, `1 failed in 3.62s` |
| `tests/test_plan_gate.py::test_the_gate_command_prints_fail_and_exits_1_then_ok_and_exits_0` | LLR-337, added sentence | (a) the step always exiting 0: the held run's exit asserted 1, `1 failed in 2.29s`; (b) `ok` reworded `pass`: `assert 'pass' == 'ok'`, `1 failed in 6.38s` |
| `tests/test_rejudge.py::test_the_release_command_names_its_count_and_a_refused_mint_exits_1` | LLR-255, added sentence | (a) the refusal dropped from the command's ending: `assert 0 == 1`, `1 failed in 3.18s`; (b) the count dropped from its line: `assert 're-judge at release: minted 1 row(s).' in '... re-judge at release: minted rows.'`, `1 failed in 4.90s` |
| `tests/test_rejudge.py::test_the_cadence_reads_one_history_per_result_commit` | LLR-293, clause 6 | the per-commit cache bypassed: `AssertionError: ['log', 'diff', 'log', 'diff']`, `1 failed in 3.50s` |
| `tests/test_intake.py::test_a_history_sweep_naming_a_branch_labels_its_commit_and_runs_no_done_when_check` | LLR-265, clause 7 | every sweep handing the check the branch as a claim identity: `assert not True` (a Done-when row minted), `1 failed in 6.96s` |
| `tests/test_prompts.py::test_an_operator_override_is_loaded_in_place_of_the_shipped_template` | LLR-162, clause 1 | the override ignored: `assert 'You are a wo...er, and stop.' == "the operator...brief, {slot}"`, `1 failed in 0.42s` |
| `tests/test_prompts.py::test_the_catalogue_rows_give_each_prompt_its_file_slots_and_digest_in_key_order` | LLR-162, added sentence | the row's file given as its key: `assert 'ADJUDICATE-ACT' == 'adjudicate-act.template.md'`, `1 failed in 0.33s` |
| `tests/test_decision_record.py::test_the_decisions_library_imports_only_the_standard_library_and_the_kernel` | LLR-283, clause 1 | an `os` import added: `assert {'os', 're', 'tomllib'} <= {'re', 'tomllib'}`, `1 failed in 0.33s` |
| `tests/test_decision_record.py::test_each_queued_entry_carries_its_id_hoist_fields_and_raw_operator_value` | LLR-283, clause 11 | the operator value normalized instead of raw: `assert ('D-001', False, None) == ('D-001', False, 'maybe')`, `1 failed in 0.37s` |
| `tests/test_decision_record.py::test_the_newly_overruled_entries_come_in_id_order_whatever_else_they_carry` | LLR-283, clauses 14 and 15 | (a) a lexical sort: `assert ['D-10', 'D-9'] == ['D-9', 'D-10']`, `1 failed in 0.33s`; (b) a blank note suppressing the overrule: `assert ['D-10'] == ['D-9', 'D-10']`, `1 failed in 0.44s` |
| `tests/test_decision_record.py::test_the_missing_record_refusal_names_the_run_the_path_and_the_dial` | LLR-283, clause 17 | the dial dropped from the refusal: `assert "'escalate-first'" in 'wi-401-x closed without its decisions record ...'`, `1 failed in 0.38s` |
| `tests/test_decision_record.py::test_the_session_note_names_the_path_only_under_a_recording_dial` (four assertions added) | LLR-283, clause 18 | the "not an exit" sentence dropped: `assert 'The record is not an exit' in 'DECISIONS RECORD ...'`, `1 failed in 0.33s` |
| `tests/test_adoption_record.py::test_a_malformed_record_is_refused_and_the_commit_dropping_it_is_not` | LLR-345, clause 5 | (a) the tree under judgement read leniently: `assert [] != []`, `1 failed in 4.82s`; (b) a parent read strictly: `assert ['commit c59a...w through it'] == []`, `1 failed in 5.07s` |
| `tests/test_adoption_record.py::test_the_step_prints_fail_or_ok_with_its_exit` | LLR-345, added sentence | (a) `FAIL` reworded `WARN`: `AssertionError:   WARN  adoption-record  WI-401: ...`, `1 failed in 4.43s`; (b) the step always exiting 0: `assert 0 == 1`, `1 failed in 4.16s` |
| `tests/test_session_service.py::test_only_the_service_calls_the_headless_or_attached_launch` | LLR-269, no other module calls the headless or attached session launch | a call of the headless launch appended to the scheduler module: `E AssertionError: assert {'schedule.py': [973]} == {}`, `1 failed in 0.94s`; restored `1 passed in 0.91s` |
| `tests/test_session_service.py::test_no_gate_or_scheduler_names_the_session_mode_or_keep_scope_column` | LLR-269, the audit columns no gate or scheduler reads | a read of the session-mode column appended to the scheduler module: `E AssertionError: assert {'schedule.py...ession-mode']} == {}`, `1 failed in 0.97s`; restored `1 passed in 0.84s` |
| `tests/test_adjudicator_token.py::test_a_route_declaring_a_competing_credential_is_refused_before_launch[CLAUDE_CODE_OAUTH_TOKEN]` (a case added) | LLR-305, a token account may not declare its token variable | the token variable removed from the claude runner's competing names: `E Failed: DID NOT RAISE SigninRefused`, `1 failed in 0.41s`; restored `1 passed in 0.32s` |
| `tests/test_accounts.py::test_only_a_token_accounts_template_is_refused_for_the_bare_flag` | LLR-305, only a token account's template may not carry the bare-mode flag | the flag refused for every account: `E session_service.SigninRefused: launch [WORK]: refused before launch: the route or the account declares --bare, ...`, `1 failed in 0.35s`; restored `1 passed in 0.20s` |
| `tests/test_coordinator_guard_e2e.py::test_the_posix_launcher_checks_the_window_on_its_first_floor_interpreter` | LLR-301: first 3.11+ candidate, the window check on it, nothing started on a refusal, a new terminal on a pass, guidance when none resolves | (a) the window-check line dropped from the POSIX launcher; (b) the floor test dropped (the first candidate that runs taken). Each: `assert ['terminal', ...nch.sh'", ...] == ['python', 'D...window-check']`, `1 failed in 0.52s` / `1 failed in 0.53s` |
| `tests/test_coordinator_guard_e2e.py::test_the_windows_launcher_checks_the_window_on_its_interpreter_before_starting` | LLR-301: the window check on the resolved interpreter before the token, then the prompt-file step on the same interpreter; guidance when none resolves | the window-check line dropped from the Windows launcher: `assert ['exec-claude...\\prompt.txt'] == ['--root', 'D...window-check']`, `1 failed in 0.55s` |
| `tests/test_coordinator_guard.py::test_a_relaunch_request_whose_write_fails_leaves_no_request` | LLR-301: the request written atomically | the request written in place: `Failed: DID NOT RAISE OSError`, `1 failed in 1.04s` |
| `tests/test_coordinator_adjudicate.py::test_an_undecodable_brief_is_refused_with_the_usage_exit` (assertion added) | LLR-306: an unreadable brief refused | the read error no longer caught: `FileNotFoundError: [Errno 2] No such file or directory: ...brief.md'`, `1 failed in 2.83s` |
| `tests/test_coordinator_adjudicate.py::test_a_call_refused_before_launch_releases_its_reservation` (assertions added) | LLR-306: a refusal leaves the directory it created | the release also removing the directory: `assert (False)` / `where False = is_dir()`, `1 failed in 2.90s` |
| `tests/test_coordinator_act.py::test_a_retained_act_turn_whose_account_is_not_signed_in_is_refused_apart` | LLR-306: the act turn's sign-in refusal reports its distinct result | the sign-in refusal returning the pre-launch code: `assert 2 == 7`, `1 failed in 6.27s` |
| `tests/test_done_when_blessing.py::test_the_entry_point_commits_its_recorded_binding_in_its_own_telemetry_commit` | LLR-306: the binding committed in its own telemetry commit; LLR-310: the recorder's commit path | the recorder's commit removed: `assert (False)` where `False = startswith('telemetry: ')`, `1 failed in 6.02s` |
| `tests/test_adjudicate_brief.py::test_the_one_review_line_reader_takes_only_the_exact_form` (4 cases) | LLR-310: the one review-line reader, the filing boundary, the merge reader | two VERDICT lines taken: `AssertionError: Reviewed: aaaa... VERDICT: APPROVE findings=0`, `4 failed in 0.49s` |
| `tests/test_adjudicate_brief.py::test_a_single_kind_verdict_carries_no_kind_section` | LLR-310: a single-kind verdict carries no kind section | the section check disabled: `TypeError: argument of type 'NoneType' is not iterable`, `1 failed in 0.32s` |
| `tests/test_adjudicate_brief.py::test_the_loops_binding_carries_its_findings_file_and_identities_through_the_outcome` | LLR-310: the loop route's dispute binding, the outcome rewrite carrying the findings file and the identity cell, none bound when none named | (a) the rewrite dropping the findings file: `assert None == 'docs/reviews/wi-1/002-DISPUTE-findings.toml'`, `1 failed in 0.36s`; (b) dropping the identity cell: `assert (None, 'the b...dentity cell') == ({'LLR-001': ...bcdef'}, None)`, `1 failed in 0.72s` |
| `tests/test_blackout_window.py::test_an_absent_window_answers_neither_question` | LLR-316: an absent declaration is disabled | an absent key read as a default window: `assert (True, dateti...'12:00-19:00') == (False, None, '')`, `1 failed in 0.31s` |
| `tests/test_blackout_window.py::test_with_no_instant_given_the_reading_is_taken_now` | LLR-316: the current UTC instant | no instant read as midnight: `assert (datetime.datetime(2026, 7, 13, 0, 0) == datetime.datetime(2026, 7, 13, 14, 0))`, `1 failed in 0.97s` |

**Tagged** (a test docstring's `Implements:` line; the `evidence` cells
regenerated by `trace.py --root . --regen-evidence`, which rewrote 25:
TC-046, TC-056, TC-058, TC-075, TC-130, TC-132, TC-145, TC-248, TC-257,
TC-261, TC-265, TC-290, TC-293, TC-303, TC-306, TC-318, TC-321, TC-322,
TC-327, TC-333, TC-334, TC-335, TC-362, TC-367, TC-383):

- TC-046: `tests/test_agent_route.py::test_enable_list_is_ordered_and_skips_comments`, `::test_absent_registry_and_enable_list_are_empty`, `::test_select_prefers_a_different_provider_but_degrades`, `::test_select_none_when_all_cooled`, `::test_resolve_token_unresolvable`; `tests/test_agent_loop_env.py::test_pair_row_env_is_merged_into_the_launch`, `::test_empty_env_inherits_the_ambient_environment`; `tests/test_agent_loop_review.py::test_absent_enable_list_keeps_legacy_behavior` (beside TC-082).
- TC-056: `tests/test_traj_panels.py::test_process_tab_is_byte_deterministic_and_check_stable` (beside TC-051).
- TC-075: `tests/test_trajectory.py::test_generated_marker_exempts_only_the_block`; the new forward-only test.
- TC-130: `tests/test_trunk_step.py::test_no_fragments_is_a_clean_idempotent_noop`, `::test_second_run_is_idempotent`, `::test_relative_links_are_rebased_out_of_log_d`, `::test_uncommitted_fragment_is_a_loud_error`, `::test_a_merge_staged_fragment_compiles_from_merge_head_history`, `::test_missing_heading_is_rejected`, `::test_reserved_section_headings_are_rejected`, `::test_one_bad_fragment_blocks_the_whole_batch`, `::test_dry_run_plans_both_operations_without_writing`, `::test_the_directorys_readme_is_its_declaration_home_not_a_fragment`, `::test_regen_fails_loudly_on_a_broken_generator` (beside TC-135); the four new trunk tests.
- TC-058 and TC-290: the new tests in their modules (`test_schedule.py` already carries TC-058 at module level).
- `tests/test_integrate_station.py::test_the_queue_restricted_to_named_branches_merges_only_those`: `Implements: TC-145`.
- `tests/test_done_when_blessing.py::test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close`: `TC-325` -> `TC-325, TC-132`.
- `tests/test_done_when_blessing.py::test_the_loop_route_records_its_verdicts_outcome`, `::test_the_loop_records_a_failed_calls_verdict_failed`, `::test_a_failed_loop_call_keeps_its_obligation_and_reads_no_verdict`: `TC-326` -> `TC-326, TC-257`; `::test_the_loop_route_takes_a_combined_sitting_on_its_bound_kinds`: `TC-326, TC-327` -> `TC-326, TC-327, TC-257`.
- TC-293 on eight `tests/test_decision_overrule.py` tests (beside TC-319): `test_the_run_name_alphabet_is_what_git_refuses_plus_two_delimiters`, `test_a_run_name_carrying_the_citation_delimiter_has_no_record`, `test_the_citation_reads_every_run_name_the_record_path_writes`, `test_the_citation_reader_takes_no_surrounding_prose`, `test_a_citation_of_another_entry_does_not_match`, `test_a_repair_of_an_unparseable_parent_owes_every_overrule_it_shows`, `test_a_record_that_does_not_parse_is_refused_at_the_commit_and_the_merge_slot`, `test_an_entry_already_overruled_owes_nothing_again`.
- TC-261 on `tests/test_intake.py::test_a_range_sweep_run_twice_mints_nothing_the_second_time` (it had no tag).
- TC-248 on `tests/test_import_layers.py::test_a_view_never_imports_a_lifecycle_service` (beside TC-177, TC-183, TC-194).
- Each new test carries its row's test case's tag: TC-334 (two), TC-333, TC-367, TC-248, TC-306, TC-261, TC-293 (three new, the note test already module-tagged), TC-383 (two); the two prompt tests sit in TC-157's module-tagged `tests/test_prompts.py`.
- `tests/test_session_adapters.py::test_codex_occupancy_falls_back_to_codexs_default_home`:
  a docstring `Implements: TC-303` (LLR-290 clause 2).
- `tests/test_session_keep.py::test_a_review_rounds_brief_and_identity_share_one_template_read`:
  `Implements: TC-351` -> `Implements: TC-351, TC-322` (LLR-305 clause 24).
- The two new `tests/test_session_service.py` tests carry `Implements: TC-265`;
  the new `tests/test_accounts.py` test carries `Implements: TC-362`.
- `tests/test_run_devsetup.py::test_each_run_launcher_searches_what_its_dev_setup_searches`: TC-318 (LLR-301's candidate order).
- `tests/test_blackout_window.py::test_reopening_the_same_session_with_both_drains_needs_the_operators_clear`: TC-318 (LLR-301's operator clear).
- `tests/test_done_when_blessing.py::test_a_call_reporting_an_error_is_failed_on_both_routes`: TC-321, TC-327.
- `tests/test_done_when_blessing.py::test_a_refused_reservation_leaves_a_binding_it_does_not_own`: TC-321.
- `tests/test_done_when_blessing.py::test_the_entry_point_binds_the_requested_kinds_beside_the_verdict`: TC-321.
- `tests/test_done_when_blessing.py::test_at_merge_a_combined_successor_mints_the_done_when_sections_own_draft`: TC-327.
- `tests/test_done_when_blessing.py::test_a_failed_loop_call_keeps_its_obligation_and_reads_no_verdict`: TC-327.
- `tests/test_coordinator_adjudicate.py::test_a_dispute_binding_records_its_findings_file_through_the_outcome`: TC-321.
- The added tests carry their own tags: TC-318 (the three LLR-301 tests),
  TC-321 (the act sign-in and the two adjudicate assertions sit in TC-321
  tests), TC-321 and TC-327 (the telemetry commit), TC-327 (the three
  `tests/test_adjudicate_brief.py` tests), TC-335 (the two blackout tests).

**The tests run** (builder rule 5): the modules holding the tests every test
case verifying a touched row names (76 test cases), every test module this
slice edited, `tests/test_trunk_step_plan.py` beside TC-130's, the four named
ratchet and sync modules and the stage test, 94 modules, `-n 6`:

```
1 failed, 3868 passed, 20 skipped in 4061.75s (1:07:41)
```

The one failure, `tests/test_agent_loop.py::test_budget_ceiling`, was the
session loop's own restart guard: `agent_loop: RESTART - coordinator Python
changed after this process imported it`, exit 11 where 6 was asserted. LLR-014's
breakage runs (section 8) edited the budget comparator for about ten seconds
each while this run was going, and the loop saw a kit file change under it. Run
alone with the tree restored: `1 passed in 43.81s`. The parallel passes'
own breakage windows had all closed before this run started.

After this run the commit hook's format step refused eight of the edited test
modules on layout; the formatter rewrote them (layout only) and the build
commit took them. With LLR-014's commit, those eight modules, LLR-014's
`tests/test_check_perf.py`, the four ratchet and sync modules and the stage
test ran again, `-n 6`: `601 passed, 1 skipped in 1177.73s (0:19:37)`.

- `trace.py --root . --strict`, at the build commit and again at LLR-014's:
  exit 0, no finding (slice 2's base red, LLR-484's, resolved with slice 2's
  merge): `Traceability: SN=31 SR=141 LLR=372 TC=448 orphans=0 integrity=0
  ... interfaces=239 interface-findings=0 ac-advisories=1
  paraphrase-advisories=1`.
- `check_trajectory.py --root . --strict`: `check_trajectory: clean (1070
  work item(s), 941 done (88%), 37 cancelled, graph acyclic).`
- The views were regenerated (`trunk_step.py --root . --regen`) before each
  commit; the derived stage is unchanged but for its fingerprint. The build
  commit's first attempt was refused at the hook's format step (the eight test
  modules above); its second, and LLR-014's commit, passed the hook.
- `run_menu.py smoke`, once, after LLR-014's commit: exit 0.
  `check_docs: OK - 3711 doc(s), 3840 intra-repo link(s), 0 broken.`;
  `check_resync: OK, no shipped path changed (base d7e3a57df...)`; the tier
  `3954 passed, 3 skipped, 17 warnings in 233.56s (0:03:53)`; `smoke budget:
  CPU 735.0 s vs 540 s cpu-seconds; wall 235.7 s vs 600 s wall-seconds; meter
  windows-job; 24 logical CPUs -> OVER`, a warning the checks do not fail on
  (the known over-budget tier, re-tier row WI-1039).

## 3. The population

### 3.1 The measure, re-taken at `d7e3a57df`

The 76 live interfaces CMP-008 owns, as [candidates.md](candidates.md)
counted them at `bba30552f`. None was constrained before this slice. The
test cases naming each, re-taken at the tip, are the ones candidates.md
recorded for every one of the 76; the tier and candidate column is
candidates.md's (tiers as the plan's section 3 defines them), which the judged
table below supersedes. Grouped as the sittings take them (section 3.2).

| Interface | Channel | Case naming it today | Tier and candidate |
|---|---|---|---|
| IF-015 | git | none | 6: LLR-028, LLR-045, LLR-061, LLR-132, LLR-174, LLR-175 +7 |
| IF-253 | file | TC-290 | 3: LLR-280 |
| IF-037 | file | TC-031 | 3: LLR-031 |
| IF-038 | file | none | 7: text names its file: LLR-018, LLR-034, LLR-039, LLR-040 |
| IF-045 | file | none | 7: text names its file: LLR-044, LLR-176 |
| IF-162 | file | none | 7: text names its file: LLR-044 |
| IF-163 | file | none | 7: text names its file: LLR-026, LLR-056, LLR-061, LLR-075 |
| IF-071 | call | none | 2: LLR-058, LLR-123, LLR-288 |
| IF-085 | call | none | 6: LLR-058, LLR-059, LLR-089, LLR-123, LLR-131, LLR-152 +1 |
| IF-171 | cli | none | 6: LLR-058, LLR-059, LLR-089, LLR-123, LLR-131, LLR-152 +1 |
| IF-172 | stdout | none | 6: LLR-058, LLR-059, LLR-089, LLR-123, LLR-131, LLR-152 +1 |
| IF-264 | call | TC-301 | 1: LLR-288 |
| IF-093 | call | TC-056 | 3: LLR-056 |
| IF-094 | call | TC-056 | 3: LLR-056 |
| IF-081 | exit-code | none | 6: LLR-060, LLR-124, LLR-137, LLR-142 |
| IF-155 | cli | none | 6: LLR-060, LLR-124, LLR-137, LLR-142 |
| IF-156 | file | none | 7: none |
| IF-168 | file | none | 7: none |
| IF-080 | exit-code | TC-425 | 1: LLR-368 |
| IF-154 | cli | TC-417, TC-424 | 1: LLR-207, LLR-368 |
| IF-175 | call | TC-205 | 1: LLR-207, LLR-262 |
| IF-186 | call | TC-145 | 1: LLR-151 |
| IF-179 | call | TC-369 | 3: LLR-339 |
| IF-189 | call | TC-249, TC-369 | 1: LLR-339 |
| IF-194 | call | TC-242 | 1: LLR-247, LLR-248 |
| IF-224 | call | TC-147, TC-252 | 2: LLR-061, LLR-339 |
| IF-242 | call | TC-257, TC-259 | 1: LLR-262 |
| IF-286 | call | TC-325, TC-326, TC-328 | 1: LLR-262, LLR-307 |
| IF-326 | call | TC-461 | 2: LLR-307 |
| IF-297 | call | TC-370 | 1: LLR-340 |
| IF-046 | call | TC-333 | 3: LLR-313 |
| IF-047 | file | TC-333 | 3: LLR-313 |
| IF-160 | file | none | 5: LLR-046 |
| IF-288 | cli | TC-333, TC-371, TC-419 | 1: LLR-313, LLR-341 |
| IF-289 | exit-code | TC-333, TC-371 | 1: LLR-313, LLR-341 |
| IF-290 | call | TC-334 | 1: LLR-314 |
| IF-322 | file | TC-334 | 1: LLR-314 |
| IF-309 | call | TC-415 | 1: LLR-367 |
| IF-295 | exit-code | TC-367 | 1: LLR-337 |
| IF-228 | call | TC-247 | 1: LLR-254 |
| IF-229 | cli | TC-248 | 1: LLR-255 |
| IF-243 | cli | TC-260 | 1: LLR-264 |
| IF-244 | cli | TC-261 | 1: LLR-265 |
| IF-269 | call | TC-306, TC-307, TC-311 | 1: LLR-293, LLR-294 |
| IF-098 | call | none | 2: LLR-162 |
| IF-255 | file | TC-294, TC-319 | 1: LLR-303 |
| IF-256 | call | TC-293 | 1: LLR-283 |
| IF-294 | call | TC-360 | 1: LLR-335 |
| IF-303 | call | TC-383 | 1: LLR-345 |
| IF-304 | exit-code | TC-383 | 1: LLR-345 |
| IF-245 | call | TC-262, TC-386, TC-387, TC-391 | 1: LLR-266, LLR-347, LLR-348, LLR-352, LLR-353 |
| IF-246 | call | TC-265, TC-384, TC-387, TC-389, TC-390, TC-392, TC-393 | 1: LLR-269, LLR-346 |
| IF-247 | file | TC-267, TC-303, TC-329, TC-351 | 1: LLR-270, LLR-290 |
| IF-248 | call | TC-266, TC-267, TC-303, TC-341, TC-351 | 1: LLR-270, LLR-290 |
| IF-266 | call | TC-303 | 1: LLR-290 |
| IF-272 | call | TC-317 | 2: LLR-270 |
| IF-273 | call | TC-267, TC-317 | 1: LLR-270 |
| IF-282 | call | TC-322, TC-323, TC-324, TC-330 | 1: LLR-270, LLR-305 |
| IF-305 | cli | TC-391, TC-394 | 1: LLR-353, LLR-355 |
| IF-306 | stdout | TC-391 | 1: LLR-353, LLR-355 |
| IF-307 | exit-code | TC-394 | 1: LLR-353, LLR-355 |
| IF-271 | call | TC-317, TC-339 | 1: LLR-300 |
| IF-274 | cli | TC-316, TC-317, TC-339 | 1: LLR-300 |
| IF-275 | stdout | TC-316, TC-317, TC-339 | 1: LLR-300 |
| IF-278 | env | TC-318 | 1: LLR-301 |
| IF-279 | cli | TC-318 | 1: LLR-301 |
| IF-280 | cli | TC-318, TC-340 | 1: LLR-301 |
| IF-281 | exit-code | TC-318, TC-340 | 1: LLR-301 |
| IF-283 | cli | TC-321, TC-323 | 1: LLR-306 |
| IF-284 | exit-code | TC-321 | 1: LLR-306 |
| IF-285 | stdout | TC-321, TC-323 | 1: LLR-306 |
| IF-321 | file | TC-321 | 1: LLR-306 |
| IF-115 | call | TC-308, TC-309, TC-327 | 1: LLR-295, LLR-308, LLR-310 |
| IF-287 | call | TC-327, TC-331, TC-398 | 1: LLR-310, LLR-359 |
| IF-296 | call | TC-368, TC-398 | 1: LLR-338, LLR-359 |
| IF-291 | call | TC-335 | 1: LLR-316 |

IF-049 (CMP-007's, carried from slice 2): file, named by TC-431, tier 3
candidate LLR-370 at `bba30552f`; slice 2 judged LLR-047 its row.

### 3.2 The judged table, in the two halves the sittings take

One row per interface; a row constraining several interfaces of one surface
constrains them all. "Link" means only `constrains` changed; "amended" means
the row's `detail` changed too: its code names scrubbed (rule 1, every clause
kept, answer 1) and, where the text did not yet state the behaviour across the
interface, that behaviour written in and tested (answer 5). The full per-row
clause accounting is section 4.

The halves are by surface, about equal in rows (section 5): **C1**, the agent
loop's outcome codes and payloads, the policy and routing files, the status
blackboard, the scheduler and station vocabulary, the trunk step and its log
fragments, then the integrator, the verdict record, the bookkeeping commit,
the trunk helpers, loop provenance, the Done-when library and the hooks
refusal (30 CMP-008 interfaces, with IF-049 and LLR-014's answer); **C2**, the
review briefs, scorer, disputes, plan gate and review set, the intake
commands, re-judge cadence, prompt catalogue, decisions and adoption records,
then the session service, adapters, keep store and usage ingest, then the
coordinator guard, the coordinator adjudication entry, the adjudication brief,
sitting record and act, and the blackout reading (46 interfaces).

#### C1

**The loop, policy files, scheduler, station and trunk step**

| Interface | Channel | Constraining row | Change | Clause-to-test |
|---|---|---|---|---|
| IF-015 | git | LLR-028 | amended `detail` (one sentence appended) | the coordinator stops with the exit code assigned to its end state: TC-028 (module tag on `tests/test_agent_loop.py`) `test_blocked_exit` 3, `test_stall_guard_aborts_after_no_commit_sessions` 4, `test_limit_hit_backs_off_without_counting_stall` 5, `test_budget_ceiling` 6; the other codes' tests tagged to TC-028, whose `method` and `expected` now state every code (round 1) |
| IF-037 | file | LLR-031 | link (routed; slice 2's row) | the privacy keys read outside and inside the policies table, one parse, an unreadable file refused: TC-031 `tests/test_process_config.py` tests by name |
| IF-038 | file | LLR-040 | amended `detail` (slice 2's row; one sentence added) | off or none declared allows, ask asks, deny refuses, any other value asks, an unparseable configuration asks or keeps a legacy deny: TC-043 `tests/test_subagent_gate.py` tests by name |
| IF-045, IF-162 | file, file | LLR-044 | amended `detail` | the pair rows, the enable list in preference order as the consent surface, entries and qualified entries: TC-046 `tests/test_agent_route.py` tests by name, five tagged; two `tests/test_agent_loop_env.py` tests and one `tests/test_agent_loop_review.py` test tagged; an existing unreadable enable list refused (round 1): `tests/test_accounts.py::test_an_unreadable_enable_list_is_an_error_and_an_absent_one_is_routing_off`, tagged TC-046 |
| IF-163 | file | LLR-075 | amended `detail` | done ids in the hand-authored part warn plain and fail strict; the generated block, open and unknown ids, the opt-out and an absent page stand down: TC-075 tests by name; one new test, one tagged |
| IF-253 | file | LLR-280 | amended `detail` | longest substring, then name order, the policy's matcher, the default core, the KIT CORE block, an unreadable chosen payload read as no core and reported once: TC-290 tests by name; two new tests |
| IF-071, IF-085, IF-171, IF-172 | call, call, cli, stdout | LLR-058 | amended `detail` | the command's frontier, explanation and simulation as text or JSON, the worker-count refusal, the status page's frontier block drawn from the derivation and omitted without the scheduler: TC-058 (module tag) tests by name; two new tests; no command prints the usage and exits 2, an empty text answer says so (round 1): `test_no_command_prints_the_usage_and_an_empty_text_answer_says_so` (new) |
| IF-093, IF-094 | call, call | LLR-056 | amended `detail` | the outcome cards and their directories from the outcome vocabulary, the refresh card's passed-checks label, the spine barrier's exclusive kinds in rank order: TC-056 `tests/test_traj_panels.py` tests by name; one tagged |
| IF-264 | call | LLR-288 | link | each row's holding items with their titles in its readiness record: TC-301 `tests/test_open_item_readiness.py` (file level) |
| IF-081, IF-155, IF-156, IF-168 | exit-code, cli, file, file | LLR-137 | amended `detail`; `sr_refs` gains SR-173 (round 1) | the fragment grammar and order, the all-or-nothing compile, the invocation forms and dry run, the exit and the name on the error stream: TC-130 `tests/test_trunk_step.py` tests by name (eleven tagged), four new tests |
| IF-049 | file | LLR-047 | link (routed; slice 1's row, WI-1071's restored text) | the run section read into name, command and description in declaration order, no interpolation, each name's case kept, a description row attached and an orphan or empty one dropped: TC-047 `tests/test_run_menu.py::test_list_is_stable_name_tab_desc`, `::test_the_run_section_reads_values_literally_and_keeps_a_names_case`, `::test_an_orphan_description_and_an_empty_command_are_dropped` |

**The integrator, verdict record, bookkeeping, trunk helpers, provenance, Done-when and hooks refusal**

| Interface | Channel | Constraining row | Change | Clause-to-test |
|---|---|---|---|---|
| IF-080, IF-154 | exit-code, cli | LLR-140 | amended `detail` | every recorded clause kept in contract terms (TC-132 file-level, TC-205, TC-317, TC-370 by name); added: the command line's six commands, each refusing with its reason printed and a nonzero exit: `test_a_lowercase_wi_id_is_normalized_before_any_rung_runs` (claim), `test_the_refresh_cli_is_the_lane_side_entry_point`, `test_the_record_checks_cli_is_the_route_a_builder_calls`, `test_integrate_refuses_and_holds_the_trunk_when_the_checks_are_undeclared`, `test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close` (extended, tagged TC-132), `test_audit_flags_a_non_merge_trunk_commit_touching_product_paths` |
| IF-175 | call | LLR-207 | amended `detail` | every clause kept, code names scrubbed: TC-205's named tests (section below), TC-132, TC-417, TC-424 |
| IF-186 | call | LLR-151 | amended `detail` | every recorded clause kept (TC-145, `tests/test_integrate.py` by name; the queue restriction by a new test); added: the shared bookkeeping commit's planning, isolation, drift, install and clean-up contract, `tests/test_bookkeeping.py` (TC-145) by name |
| IF-179, IF-189 | call, call | LLR-339 | amended `detail` (round 1) | the declared trunk read and refused naming the declaration; a lane's integration base its merge base with the declared trunk: TC-369 `tests/test_trunk_name.py` tests, `test_default_base_keeps_the_trunk_boundary_after_a_single_checkout_resume`, `test_default_base_lets_an_undeclared_trunk_refusal_through`; with no merge base the checkout's own tip, with no commit none (round 1): `test_default_base_is_the_tip_without_a_merge_base_and_none_with_no_commit` (new) |
| IF-194 | call | LLR-247 | link (routed; slice 2's row) | the trailer key, the marker, rendering, parsing (last trailer wins) and the refusal naming the subject: TC-242 `tests/test_loop_provenance.py` (file-level), `test_format_and_parse_round_trip`, `test_the_last_trailer_wins`, `test_a_missing_trailer_is_refused_naming_the_subject` |
| IF-224 | call | LLR-259 | amended `detail` | the brief asks the shared acceptance-dial predicate per spine tier and sets apart the released chains: TC-252 `tests/test_trace_briefs.py` by name |
| IF-242 | call | LLR-262 | amended `detail` | every clause kept, code names scrubbed; the Done-when items and the comparison: TC-259 `tests/test_done_when.py` (file-level); four existing tests tagged TC-257 for the loop's adjudication-call clause |
| IF-286, IF-326 | call, call | LLR-307 | amended `detail` | every clause kept, code names scrubbed; the blessing digest's `sha256:` and 16 hex characters: TC-325 `test_the_merge_refusal_names_the_digest_and_the_changes`; cover, hold and staged-change clauses: TC-325, TC-326 by name |
| IF-297 | call | LLR-340 | amended `detail` (one phrase) | the hooks refusal and its three repairs: TC-370 `tests/test_commit_hooks.py` tests by name |

#### C2

**Review briefs, scorer, disputes, plan gate, review set, intake commands, cadence, prompts, decisions and adoption**

| Interface | Channel | Constraining row | Change | Clause-to-test |
|---|---|---|---|---|
| IF-046, IF-047, IF-160 | call, file, file | LLR-046 | amended `detail` | the finding rule and the strict verdict read: TC-083 `test_a_bracketed_word_that_is_not_a_severity_is_prose`, `test_every_declared_severity_reads_as_a_finding`, `test_the_gate_reads_a_malformed_verdict_line_as_no_verdict`; the verdict line and the count tripwire (added): `test_parse_verdict_reads_machine_line_and_findings`, `test_tripwire_count_mismatch`; recording a round (added): `test_scoreboard_roundtrip_and_decay` |
| IF-288, IF-289 | cli, exit-code | LLR-313 | amended `detail` | every subcommand's render, filing and refusal: TC-333's named tests (section below); the exit (added): `test_a_review_render_exits_zero_and_writes_only_the_brief`, `test_filing_a_review_exits_zero_and_writes_only_the_round_file`, `test_the_command_line_refuses_a_lane_the_git_reads_reject`, `test_a_filed_critique_exits_zero_and_writes_only_its_record`, `test_the_pass_form_refuses_while_head_lacks_the_critique_it_cites`, `test_the_dispute_findings_file_refuses_ids_other_than_the_blocking_ones`; one new test |
| IF-290, IF-322 | call, file | LLR-314 | amended `detail` | the findings file, the request and findings-file lines, the RULING grammar: TC-334 `tests/test_dispute.py` tests by name; two new tests |
| IF-309 | call | LLR-367 | link | the set, the listed evidence, the gaps and the named refusals: TC-415's eight tests |
| IF-295 | exit-code | LLR-337 | amended `detail` (one sentence appended) | the step line and exit: TC-367 `test_a_build_without_a_pass_record_is_refused_at_the_hook_and_the_landing`; one new test |
| IF-228 | call | LLR-254 | amended `detail` | each clause: TC-247 `tests/test_rejudge.py` tests by name |
| IF-229 | cli | LLR-255 | amended `detail` | the two command entries, the merge refusal, the checklist item, the staging, the exit (added): TC-248 tests by name; one new test, one tag |
| IF-243 | cli | LLR-264 | amended `detail` | each clause: TC-260's four tests |
| IF-244 | cli | LLR-265 | amended `detail` | each clause and the exit (added): TC-261's tests; one new test, one tag |
| IF-269 | call | LLR-293 and LLR-294 | amended `detail` (both) | the cadence: TC-306 `tests/test_rejudge.py` tests by name, one new test; the rubric advisory: TC-307 `tests/test_rejudge_rubric.py`, TC-311 `test_trajectory_rubric_warning_survives_strict_and_no_work_items` |
| IF-098 | call | LLR-162 | amended `detail` | the loader, fill, digest, preflight, fragments, catalogue and fingerprint: TC-157 and TC-192 tests by name; the catalogue's rows (added); two new tests |
| IF-255, IF-256 | file, call | LLR-283 | amended `detail` | each clause: TC-293 `tests/test_decision_record.py`, `tests/test_decisions_to_review.py` tests by name, eight TC-319 tests tagged; four new tests, one test extended |
| IF-294 | call | LLR-335 | link | the block, the disposed row, the successor validation, the record pair: TC-360 tests by name |
| IF-303, IF-304 | call, exit-code | LLR-345 | amended `detail` | each clause and the step's exit (added): TC-383 tests by name; two new tests |

IF-269 is constrained by two rows because its form carries two calls, the
cadence decision (LLR-293) and the rubric advisory (LLR-294), and each row
states one; neither restates the other (answer 2).

**The session service, adapters, keep store and usage ingest**

| Interface | Channel | Constraining row | Change | Clause-to-test |
|---|---|---|---|---|
| IF-245 | call | LLR-347 | link | the transcript reader's once-per-message usage, finality, open last message, partial count, the usage sum, model, cli and provider: TC-386, TC-387, TC-388 tests by name (`tests/test_claude_transcripts.py`, `tests/test_usage_ingest.py`) |
| IF-246 | call | LLR-269 | amended `detail` | launch, accounting, record, call step, the caller's step between launch and record, the one launch path, the audit columns, lane commit or spool, the report: TC-265 (`tests/test_session_service.py`, file level and by name; two new tests), TC-384 and TC-351 tests by name |
| IF-247, IF-248, IF-266 | file, call, call | LLR-290 | amended `detail` | the codex rollout read (exact thread, launch or default home), the exec totals, the compacted flag and source in the call's columns and the retained record, reported over inferred, the cursor and baseline, the legacy record, the kit reset: TC-303 (`tests/test_session_keep.py` file level and by name; one test tagged) |
| IF-272 | call | none: carried (section 6, item 4) | LLR-270 is the only row stating it | reached by its naming case TC-317 |
| IF-273 | call | none: carried (section 6, item 4) | LLR-270 is the only row stating it | reached by its naming cases TC-267, TC-317 |
| IF-282 | call | LLR-305 | amended `detail` | the request, preparation, the sign-in readings, the token refusal, the competing-credential check, composition, the one executable, the probe environment, redaction, the OpenCode base, the governing identity: TC-322, TC-323, TC-324, TC-330, TC-362, TC-365 tests by name; one new test, one test extended, one tagged |
| IF-305, IF-306, IF-307 | cli, stdout, exit-code | LLR-355 | link | the optional session and root, the seven outcome lines and their prefix, the shape refusal's file and field, exits 0, 1 and 2: TC-389, TC-390, TC-391, TC-394 tests by name |

**The coordinator guard, adjudication entry, brief, sitting, act and blackout**

| Interface | Channel | Constraining row | Change | Clause-to-test |
|---|---|---|---|---|
| IF-271 | call | none: carried, LLR-300 the only row (section 6, item 3) | stays reached through its naming cases TC-317, TC-339 | |
| IF-274 | cli | none: carried, LLR-300 the only row (section 6, item 3) | stays reached through TC-316, TC-317, TC-339 | |
| IF-275 | stdout | none: carried, LLR-300 the only row (section 6, item 3) | stays reached through TC-316, TC-317, TC-339 | |
| IF-278, IF-279, IF-280, IF-281 | env, cli, cli, exit-code | LLR-301 | amended `detail`; `sr_refs` gains SR-229 (round 1) | the launcher exporting the successor token, its root, prompt file and token arguments, the command line's dispatch and exits: TC-318 tests by name; three new tests, one assertion-free tag pair |
| IF-283, IF-284, IF-285, IF-321 | cli, exit-code, stdout, file | LLR-306 | amended `detail` (three code names; round 1, the printed reading), `rationale` (round 1) | the lane admission, the refusals, the exclusive reservation and binding, the outcomes, the readings, the act turn: TC-321 and TC-365 tests by name; two new tests, two assertions added, four tags; the reading (round 1): `test_the_adjudicate_reading_names_the_keep_the_exit_and_the_verdict` (new) and an act-turn exit assertion |
| IF-115, IF-287 | call, call | LLR-310 | amended `detail` (seven code names) | the combined composition, the one parser, the review-line reader, the binding and its outcome rewrite, the recorded-verdict and blessed-row readers: TC-327, TC-331, TC-368 tests by name; four new tests, three tags |
| IF-296 | call | LLR-338 | link | the act derivation, its refusals, the brief in full or not at all, the later-act report, the retained class: TC-368 tests by name |
| IF-291 | call | LLR-316 | amended `detail` (one code name) | the one reader, the reading at an instant, disabled forms, weekdays, the wrap: TC-335 tests by name; two new tests |

Why LLR-310 rather than a smaller row for IF-115 and IF-287: LLR-308 (the
Done-when brief) and LLR-295 (assumption-only briefs) each state the
composer's behaviour for one brief class; LLR-310 states the combined
composition (each kind composed, refused whole), the outcome recorder
(outcome and reason, accepted only on a successful call and a valid verdict)
and every cell and reader IF-287 lists. The all-or-nothing rule for every
shipped brief is LLR-167's (WI-1070's, untouched), so IF-115 is reached
without it and is not the brief's stop.

**No new row.** Every interface whose behaviour a row this slice may touch
could state already had a row stating it, so answer 2 asked for amendments,
not focused rows. The five interfaces no such row states are carried
(section 6, items 3 and 4), not given rows beside the large row that states
them.

### 3.3 By channel, and the tip's lines

The warn-first companion line at the tip, slices 1 to 3 together (every pair
is "without"; slice 3's own pairs in brackets, IF-269 counted once for each of
its two rows):

| Channel | Constrained pairs | With both companion cells | Without |
|---|---:|---:|---:|
| bytes | 3 (0) | 0 | 3 |
| call | 39 (34) | 0 | 39 |
| cli | 17 (11) | 0 | 17 |
| env | 3 (1) | 0 | 3 |
| exit-code | 32 (8) | 0 | 32 |
| file | 30 (15) | 0 | 30 |
| git | 2 (1) | 0 | 2 |
| stdout | 11 (3) | 0 | 11 |

No companion cells (answer 4): the counts are the evidence for the later
strictness call. The line reads `85 design row(s) constrain an interface
without both a Dimensions and an OutOfDomain cell`.

The tip's lines: `placement: 152 design row(s) placed, 220 unplaced`;
`interface coverage: 239 interface(s): 135 through a constraining design row,
0 through a constraining requirement, 51 through a naming test case, 0 by
observation alone, 53 unreached`; one repeated name reported (TC-301's
IF-264, section 6, item 9). Against slice 2's tip (63, 0, 108, 0, 68), the 72
interfaces this slice links moved into the first count: 57 from the
naming-case count, 15 from unreached. Every CMP-008 interface is now reached.
<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="cb5ed0c7f" -->

## 4. The clause accounting (answer 1)

Per amended row, each clause of the recorded text and where it went, then the
clauses added to state the behaviour across the interface, then the rule-3
check against its parent. A test named bare sits in the row's own test case's
module; "file-level" is the test case's module-level `Implements` tag (answer
3). "Verbatim" means the clause's words are unchanged; "kept" means kept in
contract terms with its code names removed. For a link-only row, the words
that state the behaviour across the interface and the tests that drive them.

### C1

**LLR-028** (SR-028; TC-028, `tests/test_agent_loop.py`, whose module docstring
tags TC-028).
1. "Sites SR-028's obligation in the coordinator loop as three mechanisms": verbatim.
2. "the outcome ladder that resolves every session end state to one typed code": verbatim; `test_error_session_reads_error_not_no_commit`, `test_plain_text_nonzero_exit_reads_error`, `test_limit_hit_backs_off_without_counting_stall`.
3. "the zero-commit HEAD guard": verbatim; `test_zero_commit_repo_is_guarded`.
4. "the stall fork whose all-ERROR verdict is an unavailable agent rather than a work stall": verbatim; `test_all_error_stall_names_an_agent_error`, `test_mixed_no_commit_and_error_stall_stays_generic`.
- Added: "The coordinator stops with the exit code assigned to the end state it reached, so its caller reads why it stopped from the code alone": `test_blocked_exit` (3), `test_stall_guard_aborts_after_no_commit_sessions` (4), `test_limit_hit_backs_off_without_counting_stall` (5), `test_budget_ceiling` (6). The row names no code (the alphabet is IF-015's form); the other codes (2, 7, 8, 9, 11, 12) are driven in `test_agent_loop_worker.py`, `test_agent_loop_review.py`, `test_agent_loop_review_gate.py`, `test_dispatch.py` and `test_coordinator_code_drift.py`, none tagged TC-028.
- Round 1: the other codes' tests are tagged TC-028: done, `tests/test_agent_loop_worker.py::test_worker_builds_assignment_and_exits_done`; preflight, `test_cmd_map_broken_entry_fails_preflight` (already in the module); needs operator, `tests/test_agent_loop_review.py::test_two_top_tier_failures_page_the_operator`; paused, the dispatcher's `tests/test_dispatch.py::test_a_pause_with_nothing_in_flight_exits_paused_at_once`; review owed, `tests/test_agent_loop_review.py::test_reviewer_outage_parks_review_owed_then_resume_draws_the_round`; restart, `tests/test_coordinator_code_drift.py::test_worker_rechecks_after_a_blackout_wait`; check-failure cap, `tests/test_agent_loop_review_gate.py::test_the_failure_count_survives_a_resume_to_the_cap_and_exits_12`. TC-028's `method` and `expected` now state each end state and its code (section 7).
- Rule 3: SR-028 "shall end each session in a typed outcome code", its criterion "every declared end state returns its assigned outcome code": the added sentence is that, at the coordinator's exit.

**LLR-031** (SR-031; TC-031; slice 2's row, re-accepted by the ninth sitting). Link only, the recorded text
verbatim. "All policy enforcers ... obtain a declared policy answer from one
parsed representation", "A privacy gate declaration the parse holds outside the
policies table reads as gate on ...; a privacy reviewer declaration it holds
there reads as reviewer required" and "An unreadable or unparseable declaration
is a distinct outcome, never a default" state IF-037's reading (its data cell:
"a privacy gate key outside [policies] reads as gate on, and a reviewer key
there as review required"). Driven by `tests/test_process_config.py::test_valid_toml_policy_shapes_reach_every_reader`,
`::test_a_privacy_key_under_another_table_fails_closed_in_every_reader`,
`::test_an_unreadable_policy_file_is_refused`.

**LLR-040** (SR-043; TC-043, `tests/test_subagent_gate.py`, file level; slice
2's row, re-accepted by the ninth sitting). Every clause of the recorded text (slice 2's amendment) kept
verbatim, its slice-2 tests unchanged. One sentence added, the dial's alphabet,
which is IF-038's form:
- "The dial off, or no dial declared in either home, allows a spawn": `test_off_and_absent_allow`, `test_hook_allows_when_off`.
- "ask asks for acceptance; deny refuses it": `test_ask_policy_defers_to_acceptance`, `test_deny_policy_refuses_a_spawn`, `test_hook_denies_and_exits_2`.
- "any other value asks": `test_unrecognized_policy_asks_never_harder_than_deny`, `test_garbled_policy_value_asks_and_is_never_a_quiet_off`.
- "a process configuration that is present but does not parse asks, or refuses where the legacy declaration denies": `test_corruption_with_no_legacy_file_asks`, `test_corruption_keeps_an_explicit_legacy_deny`, `test_corruption_does_not_let_a_legacy_off_reopen_the_gate`.
- Rule 3: SR-043 states the dial "(off|ask|deny; absent=off; the legacy one-word file is still read through the migration window)"; the sentence decomposes it. The unparseable arm is a reading of the declared dial, not an error of the gate, so SR-043's "fail open on any error" is not contradicted (section 6, item 7).

**LLR-044** (SR-154; TC-046, `tests/test_agent_route.py`).
1. "Parses pair rows and enable tokens": kept ("the agent registry's pair rows and the enable list's tokens"); `test_load_registry_parses_columns_not_the_id`, `test_enable_list_is_ordered_and_skips_comments` (tagged).
2. "resolves versions": verbatim; `test_resolve_versionless_newest_skips_preview`.
3. "merges Env": kept ("merges a row's environment entries into its launch"); `test_family_column_and_env_parse`, `tests/test_agent_loop_env.py::test_pair_row_env_is_merged_into_the_launch`, `::test_empty_env_inherits_the_ambient_environment` (both tagged).
4. "selects by tier, family, cooldown, and order": verbatim; `test_select_honors_preference_order_and_tier`, `test_select_reviewer_heterogeneity_wins_over_phase_preference`, `test_acct2_row_cools_down_independently`.
5. "with legacy Provider compatibility": kept as what the code does, "a legacy provider column reading as the family"; `test_load_registry_parses_columns_not_the_id` (its fixture carries the legacy header).
6. "Selection tiers up and never down": verbatim; `test_select_tiers_up_never_down`.
7. "honors family preference with documented fallback": verbatim; `test_select_prefers_a_different_provider_but_degrades` (tagged), `test_select_reviewer_heterogeneity_wins_over_phase_preference`.
8. "resolves a version-less token deterministically": verbatim; `test_resolve_versionless_newest_skips_preview`.
9. "reports no available route honestly rather than guessing": verbatim; `test_select_none_when_all_cooled`, `test_resolve_token_unresolvable` (both tagged), `test_select_tiers_up_never_down`.
10. "The pair rows are docs/agents.toml's": "the agent registry's"; `test_load_registry_parses_columns_not_the_id`.
11. "the consent surface whose presence turns managed selection on is docs/agents-enabled": "is the enable list"; `test_absent_registry_and_enable_list_are_empty` (tagged), `tests/test_agent_loop_review.py::test_absent_enable_list_keeps_legacy_behavior` (tagged TC-046 beside TC-082).
12. "Each enable-list line is one entry": verbatim, "in preference order" added; `test_enable_list_is_ordered_and_skips_comments`, `test_select_honors_preference_order_and_tier`.
13. "selection, preference and cooldowns carry that entry rather than its bare route id, and a registry row is read only through the entry's route": verbatim; `test_selection_and_preference_return_entries`, `test_cooldowns_key_on_the_entry_not_its_route`.
14. "An unqualified entry key is its route id; a qualified entry key is ROUTE@ACCOUNT": kept, the spelling said in words ("the route id joined to an account id by an at sign"); `test_an_unqualified_entry_is_keyed_by_its_route_id`, `test_acct2_row_cools_down_independently`.
- Added (round 1, IF-162): "An absent enable list holds no entry, so managed selection is off; one that exists but cannot be read is refused as an error rather than read as absent": `tests/test_accounts.py::test_an_unreadable_enable_list_is_an_error_and_an_absent_one_is_routing_off` (an absent list reads as no entry, a directory in its place raises the refusal; tagged TC-046 beside TC-361).
- Rule 3: SR-154 names the registry's pair rows and the consent surface whose presence turns managed selection on; nothing added beyond it.

**LLR-056** (SR-168; TC-056, `tests/test_traj_panels.py`).
1. "Extends LLR-051's process_panel with the station cycle as one linked flow panel": kept ("LLR-051's process panel"); `test_process_tab_renders_the_station_cycle`.
2. "the ring stations ... drawn as a single directed closed cycle in one self-contained SVG": verbatim; `test_process_tab_renders_the_station_cycle`.
3. "the three terminal-outcome cards (merged/cancelled/handback, derived from integrate.OUTCOME_DIRS) fanning out of Lane build and fanning back in to Station refresh": kept, the derivation in contract terms ("read from the outcome vocabulary by which the merge slot classifies a finished lane"), the card list corrected to what that derivation yields (merged, cancelled, partial; section 6, item 6); `test_station_outcomes_derive_from_the_integrator`.
4. "Each stage links to its canonical home (status.md, the WI registry (docs/work/), open-items.html, log.md)": narrowed to the homes the panel links (the work-item registry, the log, the operator's open-items page; section 6, item 6); `test_station_links_resolve`.
5. "data-derived where a canonical source exists": verbatim; `test_station_outcomes_derive_from_the_integrator`, `test_station_refresh_pins_the_passed_checks_record`, `test_station_barrier_and_admission_arms_pin_to_the_dispatcher`.
6. "a data-less repo renders byte-identically": verbatim; `test_station_byte_identical_without_data`.
7. "--check unchanged (the trajectory-map step)": "the generated view's freshness check is unchanged"; `test_process_tab_is_byte_deterministic_and_check_stable` (tagged TC-056 beside TC-051).
8. "Every stage link resolves to its canonical doc": verbatim; `test_station_links_resolve`.
9. "generation is byte-deterministic": verbatim; `test_process_tab_is_byte_deterministic_and_check_stable` (tagged).
10. "the station panel is part of the generated project-state view ... across B-09": verbatim; `test_process_tab_renders_the_station_cycle`.
- Added: "the status directory each names" (from the vocabulary): `test_station_outcomes_derive_from_the_integrator` (its last loop); "The refresh card names the passed-checks record by the label the station refresh and the merge slot share": `test_station_refresh_pins_the_passed_checks_record`; "the spine-barrier note lists the exclusive kinds read from the scheduler's classification tables, in rank order": `test_station_barrier_and_admission_arms_pin_to_the_dispatcher`.
- Rule 3: SR-168, one state view showing work and its flow; within it.

**LLR-058** (SR-148; TC-058, `tests/test_schedule.py`, module tag).
1. "Derives the dependency-ready frontier from the WI registry, the states of the open items its rows cite and the dispatcher reservations, never from prose": kept ("work-item registry"); `test_hard_pred_satisfied_by_done_predecessor`, `test_oi_edge_pending_holds_the_wi_blocked`, `test_deferred_reserved_excluded_with_reason_codes`; "never from prose" file level.
2. "excludes terminally closed, deferred, reserved, protected and exclusive-conflicting work with reason codes": verbatim; `test_cancelled_wi_is_terminal_never_ready`, `test_deferred_reserved_excluded_with_reason_codes`, `test_shared_exclusive_key_serializes`, `test_the_frontier_orders_one_concurrency_group_by_rank`.
3. "exposes ready --explain, --format json and simulate --jobs N": kept in contract terms, with the outputs and the worker-count refusal spelled out; `test_cli_ready_json_matches_library`, `test_cli_explain_reports_every_wi_and_reasons`, `test_cli_explain_text_formats_reason_lists`, `test_cli_simulate_serial_and_parallel`, `test_cli_simulate_refuses_a_jobs_ceiling_below_one`; the plain frontier's and the simulation's text lines had no test, `test_cli_prints_the_frontier_and_the_simulation_as_text_lines` added.
4. "The ready set contains exactly the work items whose hard work-item predecessors are done and whose OI-### edges name only items present in the open-items registry and not pending": kept ("open-item edges"); `test_oi_edge_satisfied_once_ruled`, `test_absent_oi_edge_fails_closed`, `test_mixed_wi_and_oi_edges_both_gate`, `test_hard_pred_satisfied_by_done_predecessor`.
5. "A lane stopped early leaves the frontier through its terminal partial move": verbatim; `test_partial_predecessor_is_a_dead_edge_with_its_own_reason` (the partial row is not ready).
- Added: "The status page's generated frontier block is drawn from this derivation, in its order, and a generator that finds no scheduler renders no frontier block rather than failing": `test_a_generated_view_projects_the_frontier_and_omits_it_without_the_scheduler` (new).
- Added (round 1, IF-171 and IF-172): "Given no command, it prints its usage and exits 2, and a text answer with nothing in it is one line saying so: that no work item is ready, that the registry is empty, or that there is nothing to schedule": `test_no_command_prints_the_usage_and_an_empty_text_answer_says_so` (new, section 7).
- Rule 3: SR-148 asks the ordering and exclusion reasons exposed for replay and the status surface generated; the added clauses are those.

**LLR-075** (SR-157; TC-075, `tests/test_trajectory.py`, `tests/test_trajectory_forward_only.py`).
1. "Finds done WI tokens only in hand-edited status.md": kept ("the ids of done work items in the hand-authored part of the status page, outside its generated block"); `test_done_id_in_status_warns_plain_errors_strict`, `test_clean_status_has_no_forward_only_finding`, `test_generated_marker_exempts_only_the_block` (tagged), `test_forward_only_unit_over_the_real_meta_repo`.
2. "with plain/strict severity": kept ("a warning in the plain check and an error that fails the strict check"); `test_done_id_in_status_warns_plain_errors_strict`.
3. "stands down for the generated marker": kept ("inside the generated block"); `test_generated_marker_stands_the_rule_down`, `test_generated_marker_exempts_only_the_block`.
4. "open/unknown ids": kept; open, `test_open_ids_in_status_are_not_a_finding`; unknown, no test drove it, `test_an_unknown_id_and_an_absent_status_page_draw_no_finding` added.
5. "opt-out": verbatim ("under the check's opt-out"); `test_forward_only_opt_out_silences`.
6. "absent status": kept ("when there is no status page"); no test drove it, the same new test.
- Rule 3: SR-157, a declared rule reported with its row, advisory plain and failing strict at its gate, an absent optional input vacuous; within it.

**LLR-137** (SR-170; TC-130, `tests/test_trunk_step.py`, `tests/test_rule_sync.py`).
1. "Compiles docs/log.d/*.md into docs/log.md": kept ("the session log fragments into the log"); `test_fragments_compile_in_git_order_and_are_deleted`.
2. "via plan_artifacts.append_log_summary": kept ("through the log's shared appender"); no test drove it, `test_fragments_are_appended_through_the_shared_log_appender` added.
3. "in (git add-time, filename) order": kept ("in the order of the commits that added them, oldest first, with the file name breaking a tie"); the commit order, `test_fragments_compile_in_git_order_and_are_deleted`; the tie had no test, `test_fragments_added_by_one_commit_fold_in_file_name_order` added.
4. "all fragments validated first (name shape": kept; `test_one_bad_fragment_blocks_the_whole_batch` (tagged).
5. "## heading": kept ("an opening second-level heading"); `test_missing_heading_is_rejected` (tagged).
6. "reserved section headings refused": kept; `test_reserved_section_headings_are_rejected` (tagged).
7. "an adding commit required - on HEAD, or on MERGE_HEAD during the integrator's merge composition)": kept in contract terms ("on the checked-out history or, while the integrator composes a merge, on the branch being merged"); `test_uncommitted_fragment_is_a_loud_error`, `test_a_merge_staged_fragment_compiles_from_merge_head_history` (both tagged).
8. "relative links rebased from docs/log.d/ to docs/": kept ("from the fragment directory to the log's"); `test_relative_links_are_rebased_out_of_log_d` (tagged), `tests/test_rule_sync.py::test_the_fragment_link_rebase_is_the_spec_moves`.
9. "fragments deleted after append": verbatim; `test_fragments_compile_in_git_order_and_are_deleted`.
10. "all-or-nothing on any validation error": kept, with what a refusal leaves ("the log unchanged and every fragment in place"); `test_one_bad_fragment_blocks_the_whole_batch`, `test_uncommitted_fragment_is_a_loud_error`.
11. "Never commits; the caller owns the commit": verbatim; no test drove it for the compile (TC-170's drives the regeneration's), `test_the_log_compile_never_commits_the_caller_owns_the_commit` added.
12. "The artifact-regen half is LLR-142": verbatim (a pointer; TC-135 and TC-170 drive it).
13. "A fragment-free run is a clean idempotent no-op": verbatim; `test_no_fragments_is_a_clean_idempotent_noop`, `test_second_run_is_idempotent` (both tagged).
- Added (IF-168): "Dotfiles and the directory's own readme are not fragments and are never removed": `test_fragments_compile_in_git_order_and_are_deleted` (the marker stays), `test_the_directorys_readme_is_its_declaration_home_not_a_fragment` (tagged).
- Added (IF-155): the compile, the regeneration or neither (both, compile first) and the dry run writing nothing: `test_the_step_runs_the_operations_it_is_asked_for_compile_first` (new), `test_dry_run_plans_both_operations_without_writing` (tagged).
- Added (IF-081): "exits 0 when every selected operation finished or found nothing to do, and 1 on any failure, naming the offending fragment or generator on its error stream; a failed compile stops the step before the regeneration": `test_no_fragments_is_a_clean_idempotent_noop` (0), `test_uncommitted_fragment_is_a_loud_error` and `test_missing_heading_is_rejected` (1, the fragment named on the error stream), `test_the_step_runs_the_operations_it_is_asked_for_compile_first` (the step exits 1 naming the fragment, no regeneration), `test_regen_fails_loudly_on_a_broken_generator` (1, `regen FAILED at okf`; tagged TC-130 beside TC-135).
- Rule 3: SR-170 (the shared records written only by the serial step) and, since round 1, SR-173 (ordered regeneration, stopping at the first failure, committing no partial set), which the added order and failure clauses decompose and the compile's code already cited; nothing added exceeds either.

**LLR-280** (SR-223; TC-290, `tests/test_guardrails_payload.py`).
1. "guardrails_core(root, model) lists the vendored core.<substring>.md payloads beside docs/guardrails/core.md": kept ("The guardrails payload reader lists the payloads a repository vendors beside its default guardrails core, each a core file named for a model-name substring"); `test_the_longest_matching_substring_selects_the_payload`.
2. "orders their substrings longest first and then by name": verbatim; longest, `test_the_longest_matching_substring_selects_the_payload`; the name order had no test, `test_equal_length_substrings_fall_to_name_order` added.
3. "reads the first one that guardrails_apply matches against the model name": kept ("the guardrails policy's own matcher"); `test_the_longest_matching_substring_selects_the_payload`.
4. "reading core.md when none matches or no model is named": kept ("the default core"); `test_the_longest_matching_substring_selects_the_payload`, `test_the_kit_ships_no_payload_so_every_model_gets_the_default_core`.
5. "The KIT CORE block is extracted from the chosen file as from the core": kept ("The block between the KIT CORE markers"); `test_the_longest_matching_substring_selects_the_payload` (the narrow payload's block without its noise; the broad payload, carrying no block, read whole).
6. "an unreadable chosen file returns None, which compose_session_prompt already reports once and runs past": kept ("reads as no core, which the session prompt's composition reports once and runs past without one"); no test drove it, `test_an_unreadable_chosen_payload_reads_as_no_core_and_the_session_runs_past_it` added.
7. "Whether a session is guarded stays compose_session_prompt's call on the policy, made before the payload is read": kept ("that composition's call"); `test_a_guarded_session_carries_its_payload_and_the_policy_still_decides`.
- Rule 3: SR-223's criterion (longest wins, the default core for none, the policy alone deciding); the unreadable case adds no obligation beyond "receives that payload and not the default core".

**LLR-288** (SR-148; TC-301). Link only, the recorded text verbatim: "Attach to
each work row the id and title of every open item its needs cite ... such a row
reads blocked ... and its record lists exactly the holding items with their
titles" states IF-264 ("readiness records carrying unmet item ids and
titles"); `tests/test_open_item_readiness.py` (file level, TC-301's evidence).

**LLR-140** (SR-156; TC-132 file-level over `tests/test_integrate.py`,
`tests/test_integrate_admission.py`, `tests/test_integrate_station.py`,
`tests/test_integrate_record_checks.py`; TC-205; TC-317; TC-370). Title and
rationale unchanged (both clean).
1. "claim: when the coordinator context guard is enabled and the claim does not hold the dispatch lock ..., a guard refusal comes first (no coordinator lease, a caller other than the lease holder, or a latched or threshold-crossing holder)": kept; TC-317 `tests/test_coordinator_guard_e2e.py::test_the_cli_claim_refuses_while_draining`, `tests/test_coordinator_guard.py::test_the_live_dispatchers_claim_route_is_untouched`, `::test_off_means_off_claims_pass_and_hooks_do_nothing`.
2. "then §2.3 steps 1+2 with the refusal ladder, cheapest first (...) before anything is written": the ladder kept rung by rung ("tracked pause via agent_common.tracked_pause" as a tracked pause, "SpecRef" as a spec reference, "docs/status.md's hand prose" as the status page's hand-authored prose); the design-document pointer "§2.3 steps 1+2" dropped (a section reference, not an obligation; the move and the branch cut it names are clause 3). `test_claim_refuses_while_the_tracked_pause_is_present`, `test_claim_refuses_when_the_branch_already_exists`, `test_a_branch_carrying_work_is_a_collision_the_claim_still_refuses`, `test_claim_refuses_a_branch_name_that_is_not_a_flat_claim_dir`, `test_claim_refuses_a_spec_without_a_specref`, `test_claim_refuses_a_specref_that_does_not_resolve`, `test_claim_refuses_when_status_md_hand_prose_names_the_claimed_id`, `test_claim_refuses_a_wi_that_is_not_on_the_ready_frontier`; one file with readable frontmatter, file-level (`tests/test_integrate.py`).
3. "The trunk commit goes through bookkeeping.commit, under that helper's contract (IF-186) for isolation and install, scoped to ... : a dirty path in that scope refuses by name before any step or checkout write, and the branch is cut before trunk advances": kept as "the shared bookkeeping commit, under that helper's isolation and install contract" (the interface id dropped from the text; the helper's contract is now stated by LLR-151, which constrains IF-186); `test_claim_refuses_a_dirty_path_it_must_write`, `test_claim_runs_the_link_aware_move_ritual`, `test_claim_moves_the_spec_commits_the_trunk_and_cuts_the_branch`.
4. "finished_branches: a claimed branch whose tip holds no spec under active/<branch>/": kept; `test_finished_is_the_move_to_complete_not_a_state_file`, `test_a_claim_dir_with_no_matching_branch_is_ignored`.
5. "integrate_one: --no-ff --no-commit merge, trunk_step.py folded into the merge commit ..., check.py --jobs 0 at the declared tier on the composed tree read fail-closed (nonzero exit OR any SKIP line refuses), verdict gate per [policies] review_rounds ... a narrow round and a retained full round never admit": kept in contract terms; `test_claim_build_and_integrate_end_to_end`, `test_run_trunk_step_executes_the_branch_trees_copy`, `test_checks_step_count_is_by_distinct_name_not_by_echoed_line`, `test_verdict_is_not_required_at_review_policy_zero`, `test_a_required_verdict_absent_from_the_branch_refuses_by_name`; the scope arms, TC-205 `test_a_lane_with_only_narrow_rounds_does_not_clear_the_gate`, `test_a_full_round_from_a_retained_session_does_not_clear_the_gate`, `test_a_final_round_clears_the_gate_only_with_both_dials_on`; the concurrent steps and the SKIP refusal, file-level (`tests/test_integrate_station.py`).
6. "The gate is governed by TREE IDENTITY: ... an unreadable claim commit holds by name, a narrow-only lane never clears, and a phase whose latest round is invalid evidence holds by name": kept; TC-205 `test_a_logged_reviewer_round_naming_this_tree_clears_the_gate`, `test_a_round_that_judged_an_earlier_tree_does_not_count`, `test_a_lane_with_no_claim_commit_holds_and_names_it`, `test_a_partial_or_refusable_round_file_does_not_clear_the_gate`.
7. "whether an adjudication lane owes a verdict at all is [authority] adjudication_review, read through the one function ...; ... a single declared precedence (terminal first ...)": kept, the dial named as the process configuration's adjudication-review dial; TC-205 `test_the_dial_decides_when_an_adjudication_owes_a_round`, `test_an_unreadable_dial_falls_to_when_minting_not_to_never`, `test_the_scheduler_and_the_gate_read_one_spec_copy`.
8. "The trailer is a cross-check over the newest trailer ... never on one below it - ...": verbatim but for capitals; TC-205 `test_a_trailer_contradicting_the_rounds_refuses`, `test_a_trailer_OVERSTATING_the_governing_round_count_refuses`, `test_a_trailer_UNDERSTATING_the_governing_round_count_does_not`, `test_the_newest_trailer_at_a_tree_governs_the_cross_check`.
9. "ff-only trunk advance, branch deleted on a pass, candidate parked on a failure": kept; `test_claim_build_and_integrate_end_to_end`, `test_integrate_refuses_and_holds_the_trunk_when_the_checks_are_undeclared`.
10. "audit: git log --first-parent --no-merges over --since..HEAD; paths outside docs/work/, docs/log.d/, docs/log.md and the stack.ini [generated] set flag the commit": kept in contract terms; `test_audit_flags_a_non_merge_trunk_commit_touching_product_paths`, `test_audit_passes_a_window_of_bookkeeping_commits_only`, `test_audit_allows_product_changes_that_arrive_by_a_no_ff_merge`, `test_audit_passes_a_trunk_commit_of_every_regen_output_under_the_shipped_list`.
11. "A missing stack.ini or an empty [product] test declaration refuses the merge": kept; `test_an_absent_stack_ini_is_a_refusal`, `test_a_stack_ini_without_a_product_test_key_is_a_refusal`, `test_a_declared_but_empty_test_command_is_a_refusal`.
12. "failing checks parks the candidate and stops the queue rather than composing past it": verbatim; file-level (`tests/test_integrate_station.py`), `test_integrate_refuses_and_holds_the_trunk_when_the_checks_are_undeclared` for the held trunk.
13. "The shared commit-floor refusal precedes even that first guard refusal and the dispatch lock": verbatim; TC-370 `tests/test_hooks_on_routes.py` tests and its route census.
- Added (IF-080, IF-154): the command line runs one command against the root given or the working directory, a claim (one id and a branch), a refresh (a branch, a tier), record checks (a branch, the commit check set), integrate (a tier), the Done-when hold, the audit (the base revision); each, refusing, prints the reason and exits nonzero. Driven: claim `test_a_lowercase_wi_id_is_normalized_before_any_rung_runs` (exit 1, the reason printed) and, for one id, `test_a_multi_item_claim_refuses_before_any_state_change`, `test_an_empty_claim_refuses_before_the_lock`; refresh `test_the_refresh_cli_is_the_lane_side_entry_point` (run from the working directory, no root given; nonzero, "cannot refresh wi-999"); record checks `test_the_record_checks_cli_is_the_route_a_builder_calls` (exit 1 naming the loose file; another check set refused), `test_record_checks_takes_no_tests_argument`; integrate `test_integrate_refuses_and_holds_the_trunk_when_the_checks_are_undeclared` (nonzero, the reason printed); Done-when hold `tests/test_done_when_blessing.py::test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close` (extended to assert the printed refusal and its digest; tagged TC-132); audit `test_audit_flags_a_non_merge_trunk_commit_touching_product_paths` (exit 1, the commit and path printed). The 0 exits are not stated: an integrate run that merged a branch it could not unload exits 1 while refusing nothing, and no test drives that summary's exit (stated so the row does not over-claim, answer 6).
- Rule 3: SR-156 asks for one serial, fail-closed seam that parks a failing candidate and stops the queue loudly; the exit-on-refusal clause states that loudness at the command line. Nothing added exceeds it.

**LLR-151** (SR-156; TC-145, file-level over `tests/test_integrate.py` and `tests/test_bookkeeping.py`). Title and rationale unchanged (clean).
1. "The §A4.1 authority flip's integrator half (docs/concurrency-v2.md §A4.1)": kept as "The integrator's half of the dispatcher's authority flip" (the design document's path and section dropped; a pointer, not an obligation).
2. "_claim_refusal's safety_class != ordinary arm is DELETED (admission is the dispatcher's decision)": kept as "the claim no longer refuses a work item whose safety class is not ordinary"; `test_a_spine_claim_succeeds_on_an_idle_station`.
3. "the claim REQUIRES the dispatch lock (..., the lock a live dispatcher holds for its process lifetime), acquired at ONE site (... mirroring ... the merge slot's own lock)": kept, the lock's path and the function names dropped; `test_a_hand_claim_during_live_lanes_is_unrepresentable`; the one site, file-level.
4. "with the ladder run before it (the ladder carries no clean-trunk rung: the claim commits through bookkeeping.commit, which refuses by name a dirty path the claim must write and never stages the lock's own file)": kept; `test_claim_refuses_a_dirty_path_it_must_write`, `tests/test_bookkeeping.py::test_a_dirty_path_the_claim_must_write_refuses_by_name`; the lock file never staged, `test_claims_and_mints_commit_only_what_they_wrote` (file-level otherwise).
5. "a hand claim on an idle station works, a hand claim during live lanes is unrepresentable, and the dispatcher's in-process claim passes dispatch_lock_held=True": kept, the parameter as "declares that it already holds the lock"; `test_a_spine_claim_succeeds_on_an_idle_station`, `test_a_hand_claim_during_live_lanes_is_unrepresentable`.
6. "a claim commit moves one queued spec": verbatim; `test_the_claim_subject_composes_one_id_only`, `test_claim_moves_the_spec_commits_the_trunk_and_cuts_the_branch`.
7. "empty or multi-item input refuses before any move, commit, branch or worktree": verbatim; `test_a_multi_item_claim_refuses_before_any_state_change`, `test_an_empty_claim_refuses_before_the_lock`.
8. "historical multi-item claim commits stay readable and are neither split nor re-claimed": verbatim; `test_a_historical_joined_claim_still_reads_as_a_claim`.
9. "integrate() takes an optional branches= restriction so the dispatcher merges each lane's branch as its own refresh completes": kept as "the merge queue takes an optional restriction to named branches"; no test drove the queue's own restriction (the dispatcher's test replaces the queue), `tests/test_integrate_station.py::test_the_queue_restricted_to_named_branches_merges_only_those` added, tagged TC-145.
- Added (IF-186, the helper's contract; TC-145's method already states it): plans over the committed tree, an uncommitted edit neither narrowing nor widening the plan, `test_an_uncommitted_link_to_the_spec_does_not_widen_the_claim`, `test_an_uncommitted_edit_hiding_a_committed_link_refuses_by_name`; a dirty in-scope path refused by name before writing, `test_a_dirty_path_the_claim_must_write_refuses_by_name`, `test_a_dirty_path_the_mint_must_write_refuses_by_name`; step and regeneration in a scratch worktree, the committed copy where the repository carries the kit, `test_the_regeneration_runs_the_committed_kit_not_an_uncommitted_edit`, `test_an_uncommitted_generator_input_stays_out_of_the_committed_artifacts`; exactly the changed in-scope paths plus the regeneration, `test_claims_and_mints_commit_only_what_they_wrote`, `test_no_bookkeeping_path_keeps_a_whole_tree_git_write`; after the pre-advance step, drift or a moved trunk refused by name with nothing installed, `test_an_operator_edit_while_the_regeneration_is_blocked_survives_and_refuses`, `test_the_drift_check_runs_after_before_advance`, `test_a_trunk_that_moved_while_the_step_ran_refuses_before_installing`; the install's restore naming an edit made there, `test_a_refusal_inside_the_install_restores_it_and_leaves_an_edit_made_there`; the scratch removed on success, refusal and crash and one that will not remove named, `test_a_raising_step_leaves_the_checkout_untouched_and_says_so`, `test_a_scratch_worktree_that_will_not_remove_is_named`. The helper's inactive-floor refusal and its held-status refusal under the loop marker are not restated: LLR-340 and LLR-246 state them.
- Rule 3: SR-156's isolated lanes and "never a half-integrated authoritative state" are what the helper's isolation and compare-and-swap install decompose.

**LLR-207** (SR-156; TC-205 by name, TC-132, TC-417, TC-424). Title and rationale unchanged (both clean). The recorded `detail` (at `d7e3a57df`), clause by clause, in its order; a test named bare sits in `tests/test_verdict_record.py`. The two record lines (`Checks-Passed: ...`, `Review-Verdict: ...`) are markers the code writes and stay.
1. "tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/iteration/, and returns a 64-hex SHA-256 identity": kept ("The tree identity folds the raw NUL-delimited recursive tree listing after dropping the review-record, log-fragment and iteration-record directories, and is a 64-hex SHA-256 identity"); `test_the_identity_ignores_every_record_path`, `test_the_identity_notices_work_and_notices_docs_work`.
2. "fold_listing accepts bytes and preserves every path byte so display quoting or decoding cannot merge distinct work trees": kept ("Its fold takes the listing as bytes and preserves every path byte, ..."); `test_a_record_path_is_excluded_whatever_characters_it_holds`, `test_distinct_invalid_utf8_work_paths_have_distinct_identities`.
3. "A passed-checks record is exactly one column-0 label line, `Checks-Passed: ...`": verbatim; `tests/test_passed_checks.py::test_two_label_lines_are_not_a_passed_checks_record`, `::test_a_trailer_quoted_mid_line_is_not_a_passed_checks_record`, `::test_a_line_in_the_earlier_trailer_form_is_not_a_passed_checks_record`.
4. "its verifier returns fields only when tree and work equal the commit's own tree and first parent and its `checks` field is in that set": kept ("its checks field", backticks dropped); `tests/test_passed_checks.py::test_a_trailer_naming_its_own_tree_and_parent_verifies_for_each_check_set`, `::test_a_wrong_tree_is_not_a_passed_checks_record`, `::test_a_wrong_parent_is_not_a_passed_checks_record`, `::test_an_unknown_check_set_is_not_a_passed_checks_record`.
5. "tests carries none for an empty named test-path set": kept ("The tests field carries none ..."); `tests/test_passed_checks.py::test_a_trailer_without_tests_is_not_a_passed_checks_record`; the empty set's none, file-level (`tests/test_passed_checks.py`, TC-205).
6. "otherwise it carries the SHA-256 of that set after path separators and leading ./ are normalized, duplicates are removed, and the paths are joined in sorted order": kept ("a leading current-directory prefix" for "leading ./"); `tests/test_passed_checks.py::test_the_tests_digest_is_the_same_for_the_same_set_in_any_order`.
7. "Thus one set in any order or spelling has one value, and a different set has a different value": verbatim; `tests/test_passed_checks.py::test_the_tests_digest_is_the_same_for_the_same_set_in_any_order`, `::test_the_tests_digest_differs_for_a_different_set`.
8. "refresh_passed_checks admits a refresh subject only with that verified record and checks `landing` or `none`, so work_tip never peels a commit record as a refresh": kept ("The refresh check admits ... a checks field of landing or none, so the reset path's tip peel never peels a commit record as a refresh"); `tests/test_passed_checks.py::test_work_tip_never_peels_a_commit_checks_record`, `::test_a_verified_refresh_still_peels_under_the_new_grammar`.
9. "the read-only identity walk still steps through any commit whose non-record identity equals its parent, including an empty commit record": verbatim; `tests/test_passed_checks.py::test_governing_rev_never_peels_a_commit_checks_record`, `test_the_empty_carrier_commits_its_own_paths_and_never_the_index`.
10. "One producer writes every passed-checks record: it fixes the staged tree before the checks, refuses failing checks or one that leaves the index or worktree off that tree, and restores the index on every failed write": verbatim; `tests/test_integrate_station.py::test_the_refresh_and_record_checks_commit_through_one_producer`, `tests/test_integrate_record_checks.py::test_failing_commit_checks_commit_nothing_and_leave_branch_and_index`, `::test_checks_that_edit_a_tracked_file_record_nothing`, `::test_checks_that_stage_an_edit_leave_the_index_as_staged` (TC-132).
11. "its line joins the message's final trailer block": verbatim; `tests/test_integrate_record_checks.py::test_the_passed_checks_record_joins_a_message_files_trailer_block` (TC-132).
12. "The record-checks route refuses before the checks when commit hooks are off, the primary checkout holds the branch, the worktree is dirty (including untracked files), the commit-check declaration is absent or empty, the message carries the label, or the harness floor refuses": verbatim; TC-132 `tests/test_integrate_record_checks.py::test_record_checks_refuses_a_dirty_worktree_before_running_the_checks`, `::test_record_checks_counts_untracked_files_whatever_status_shows`, `::test_record_checks_refuses_the_branch_the_main_checkout_holds`, `::test_record_checks_refuses_a_missing_commit_checks_key_naming_it`, `::test_a_message_file_carrying_the_label_is_refused_before_the_checks`, `::test_record_checks_refuses_below_the_harness_floor_before_the_checks`; hooks off, file-level (`tests/test_integrate_record_checks.py`, TC-132).
13. "it reads the commit checks and derived test set from the lane's own declarations, with no default, and refuses before the checks when derivation refuses": verbatim; `tests/test_integrate_record_checks.py::test_record_checks_runs_the_declarations_staged_in_the_lane_not_the_primarys` (TC-132), `::test_a_derivation_refusal_runs_no_checks_and_leaves_branch_and_index` (TC-417).
14. "a refusal leaves the branch and index unchanged": verbatim; `tests/test_integrate_record_checks.py::test_a_derivation_refusal_runs_no_checks_and_leaves_branch_and_index` (TC-417), `::test_a_hook_refused_record_checks_commit_leaves_branch_and_index` (TC-132).
15. "On the record-checks route the producer runs the commit checks then the derived files, records their digest in the unchanged grammar, and prints the set, listed evidence and reported gaps": verbatim; TC-417 `tests/test_integrate_record_checks.py::test_record_checks_runs_the_commit_checks_then_the_derived_files`, `::test_record_checks_prints_the_set_and_the_listed_evidence`, `::test_record_checks_prints_the_gaps_a_row_touching_no_code_reports`.
16. "A trailer without a `checks` field is not read": kept ("a checks field", backticks dropped); `tests/test_passed_checks.py::test_a_trailer_without_checks_is_not_a_passed_checks_record`.
17. "work_tip peels only a verified refresh at the tip for the reset path": kept ("The reset path's tip peel removes only a verified refresh at the tip"); `tests/test_integrate_station.py::test_a_work_commit_that_quotes_the_trailer_is_never_peeled_away`.
18. "governing_rev is read-only and walks across commits whose non-record identity equals their first parent's, peeling any DISPOSABLE commit it meets ..., and ending at the first commit whose identity differs ... or at its absent-parent and depth bounds": kept ("the read-only identity walk walks across ..."); `test_a_station_refresh_owes_no_round_and_the_two_readers_agree`, `test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel`; the bounds, file-level (`tests/test_verdict_record.py`, TC-205).
19. "TWO commit classes are disposable and the read-only walk peels BOTH: the station's REFRESH, admitted by refresh_passed_checks, and the machinery's OWN adjudication close, admitted by mechanical_close_peel against exactly one parent and a no-renames changed-path stream lying wholly under docs/work/": kept ("admitted by the refresh check", "admitted by the mechanical-close check", "wholly under the work registry"); `test_a_station_refresh_owes_no_round_and_the_two_readers_agree`, `test_the_mechanical_close_does_not_stale_the_round_it_follows`, `test_a_close_that_reached_outside_docs_work_does_not_peel`.
20. "That stream must pair deleted specs from exactly ONE docs/work/active/<branch>/ with additions of the same filenames under docs/work/complete/, and ONLY the move itself may create or destroy: ...": kept ("from exactly one branch's active directory", "under the completed directory"); `test_a_close_reaching_into_a_second_lanes_claims_does_not_peel`, `test_a_close_that_smuggles_a_new_spec_in_does_not_peel`, `test_a_close_that_destroys_an_archived_record_does_not_peel`.
21. "Modifications ride along unrestricted, because a close's inbound relink rewrites other rows in place and only ever modifies": verbatim; `tests/test_handback.py::test_the_close_the_writer_lands_is_one_the_verifier_peels`, `test_the_peel_still_refuses_a_close_whose_relink_leaves_docs_work`.
22. "A mechanical close admits exactly one moved row": verbatim; `test_a_mechanical_close_moving_two_rows_does_not_peel`.
23. "any other shape declines to peel toward more review": verbatim; `test_a_mechanical_close_moving_two_rows_does_not_peel`, `test_a_two_row_close_under_the_one_id_subject_does_not_peel`.
24. "Its subject must equal the writer's composed subject exactly, so a public prefix/suffix with a forged middle is not a passed-checks record": kept ("a public prefix and suffix"); `test_only_the_machinerys_own_close_subject_peels`, `test_a_forged_mechanical_close_middle_does_not_peel`.
25. "The one-row clause refuses an empty close, which has no deletion, and every multi-row close": verbatim; `test_an_empty_close_is_refused_and_the_walk_covers_it_regardless`, `test_a_mechanical_close_moving_two_rows_does_not_peel`.
26. "one deletion implies one source branch": verbatim; `test_a_close_reaching_into_a_second_lanes_claims_does_not_peel`.
27. "the subject composer takes a single id and refuses anything else, so no empty-id subject is ever composed": verbatim; `test_a_two_row_close_under_the_one_id_subject_does_not_peel`; the composer's refusal, file-level (`tests/test_verdict_record.py`, TC-205).
28. "One property admits the two classes and it is not two rules: both are machine-authored end to end, ... docs/work/ is deliberately inside the identity ...": kept ("the work registry is deliberately inside the identity"); `test_the_identity_notices_work_and_notices_docs_work`, `test_the_mechanical_close_does_not_stale_the_round_it_follows`.
29. "Every arm of both verifications fails toward REVIEW, ... on the empty close the refused commit is identity-preserving, ... the refusal guards this function's contract rather than any answer the gate gives": kept ("fails toward review", "a later revision", "guards the mechanical-close check's contract"); `test_an_empty_close_is_refused_and_the_walk_covers_it_regardless`.
30. "The two peels are NOT the same peel: work_tip calls refresh_passed_checks directly rather than through the shared disposable test, so a mechanical close is never removed by the destructive reset path ...": kept ("the reset path's tip peel asks the refresh check directly"); `tests/test_integrate_station.py::test_a_work_commit_that_quotes_the_trailer_is_never_peeled_away`, `test_the_mechanical_close_does_not_stale_the_round_it_follows`.
31. "governing_identity composes governing_rev and tree_identity for the branch tip or an explicit revision, including a round's reviewed commit and a trailer's carrier": kept ("The governing identity composes the read-only walk and the tree identity ..."); `test_a_round_drawn_after_a_refresh_is_visible_to_both_readers`, `test_a_trailer_riding_a_commit_that_changed_the_work_is_not_read`.
32. "the branch argument is a branch NAME, because the peel verifies a refresh commit against the branch it names and no refresh subject names HEAD": kept ("the branch is given by its name, ..."); `test_a_station_refresh_owes_no_round_and_the_two_readers_agree`; file-level (`tests/test_verdict_record.py`, TC-205).
33. "format_scope records a REVIEW session scope as full, narrow or final base..sha": kept ("A review session's scope is recorded as full, narrow or final base..sha"); `test_the_session_log_records_the_review_scope`, `test_only_a_full_round_drawn_under_the_final_stage_records_the_final_kind`.
34. "gating_span admits a fresh full scope in either mode, or a final scope only where reviewer retention is on and final_reviewer is persisted": kept ("the gating span admits ...", "the final reviewer is persisted"); `test_a_final_round_clears_the_gate_only_with_both_dials_on`, `test_in_persisted_mode_the_final_reviewers_resumed_round_clears_the_gate`.
35. "a narrow scope and a retained full scope never admit": verbatim; `test_a_lane_with_only_narrow_rounds_does_not_clear_the_gate`, `test_a_full_round_from_a_retained_session_does_not_clear_the_gate`, `test_a_retained_full_round_never_clears_the_gate_in_persisted_mode`.
36. "logged_rounds joins branch-scoped round files to coordinator session logs by train and ordinal, and each round's review phase is the JOINED LOG's declared phase ...": kept ("The logged rounds join ..."); `test_one_session_cannot_serve_a_phase_its_log_does_not_declare`, `test_an_implementer_authored_file_in_the_review_path_is_not_a_round`.
37. "a joined key whose logs declare more than one review phase yields no round": verbatim; `test_two_logs_at_one_key_declaring_two_phases_serve_no_round`.
38. "It retains only a gating span whose base equals the caller's claim base and whose reviewed sha the round file names": kept ("They retain ... whose reviewed commit the round file names"); `test_a_lane_with_no_claim_commit_holds_and_names_it`, `test_the_gate_range_survives_a_trunk_refresh`.
39. "round_entries retains only rounds whose reviewed revision governs the identity under judgement and emits phase, ordinal and verdict entries through an injected parser": kept ("The round entries ... through a verdict parser the caller supplies"); `test_a_round_that_judged_an_earlier_tree_does_not_count`, `test_a_record_only_commit_after_the_round_leaves_it_governing`.
40. "filing_refusal applies one filing check: the first physical line is exactly the Reviewed full-sha opener (a CR ending is allowed; no leading blank or whitespace is), exactly one canonical VERDICT line, a finding count matching the file, and a change request naming a finding": kept ("One filing check applies: ..."); `test_the_filing_check_is_the_one_the_gate_applies`.
41. "An unreadable or refused round is an entry with no verdict, so it is the phase's latest word rather than an older verdict being used": verbatim; `test_a_partial_or_refusable_round_file_does_not_clear_the_gate`, `test_an_invalid_round_file_at_the_tip_raises_no_page_either`.
42. "tree_already_judged is true only for an entry carrying a verdict and false with no base": kept ("A tree reads as already judged only for an entry carrying a verdict, and never with no base"); `test_with_no_base_nothing_is_judged_and_only_a_verdict_judges`.
43. "declared_phases clamps the configured independent-review count to the available review phases": kept ("The declared phases clamp ..."); `test_the_declared_phase_span_is_read_the_same_length_by_both_readers`.
44. "phases_owed returns declared phases whose latest entry is missing or invalid evidence": kept ("The phases owed are the declared phases ..."); `test_a_half_drawn_round_owes_its_missing_phase_and_only_that`, `test_the_review_owed_derivation_and_the_gate_share_one_definition`.
45. "a dissent is served": verbatim; `test_the_review_owed_derivation_and_the_gate_share_one_definition`; file-level (`tests/test_verdict_record.py`, TC-205).
46. "round_count returns the largest per-phase entry count at one governing identity, so a multi-phase review cycle counts once and changed work starts a new count": kept ("The round count is the largest ..."); `test_round_count_counts_cycles_not_reviewers`, `test_the_trailer_count_is_derived_at_the_governing_tree`.
47. "format_trailer and parse_trailer carry `Review-Verdict: APPROVE|CHANGES-REQUESTED rounds=<N> tree=<64 hex>`": kept ("The trailer, written and read by one pair, carries `Review-Verdict: ...`"); `test_the_trailer_round_trips_and_the_last_one_governs`, `test_a_malformed_trailer_is_no_trailer`.
48. "branch_trailers verifies each carrier against its governing identity and returns the ordered trailer sequence per tree": kept ("The branch's trailers are each verified against their carrier's governing identity ..."); `test_a_trailer_riding_a_commit_that_changed_the_work_is_not_read`, `test_the_newest_trailer_at_a_tree_governs_the_cross_check`.
49. "Readers treat unavailable repository answers according to their own fail-closed contract": verbatim; `test_a_lane_with_no_claim_commit_holds_and_names_it`; file-level (`tests/test_verdict_record.py`, TC-205).
50. "The record-checks route reads the declared expected-failure mark with the commit checks from one parse of the lane's declarations, with no default, and refuses before either checks when either required declaration is unavailable or its mark transition is refused under LLR-368": verbatim; TC-424 `tests/test_expected_failure_lane.py` record-checks tests by name (`test_record_checks_reads_the_mark_its_lane_stages_not_the_primarys`, `test_record_checks_refuses_a_removal_the_set_does_not_name`, `test_record_checks_passes_an_added_mark_the_set_names`).
- Nothing added; nothing cut. Rule 3: the meaning under SR-156 is unchanged.

**LLR-259** (SR-139; TC-252, `tests/test_trace_briefs.py`, file-level and by name). Title and rationale unchanged (clean).
1. "released_tiers(root) asks agent_common.operator_accepts_spine once per spine tier (SR, LLR, TC), each tier's registry taken from SPINE_FILES, and returns the tiers the declared acceptance level releases": kept as the brief asking the shared acceptance-dial predicate per tier, the registry list unnamed; `test_a_released_rungs_chain_renders_in_full_collapsed_under_its_label`, `test_the_shipped_default_dial_holds_every_chain_and_collapses_none`.
2. "no rung table is held in trace.py": kept as "the brief holds no rung table of its own"; file-level.
3. "dial_releases_chain(entry, released) is true when a chain of reaccept_model has ... ; one owing row on a held tier, or no owing row at all, keeps the chain held": kept, the names dropped; `test_a_released_rungs_chain_renders_in_full_collapsed_under_its_label` (the pairing with a Drafted requirement), `test_the_shipped_default_dial_holds_every_chain_and_collapses_none`.
4. "reaccept_lines renders every owing chain: ...": kept, the renderer unnamed; `test_a_dial_releasing_every_rung_leaves_the_operator_a_stated_empty_ask`, `test_a_released_rungs_re_acceptance_renders_its_diff_in_the_collapsed_block`.
5. "The page's title claims no operator act ...": verbatim; `test_a_released_rungs_chain_renders_in_full_collapsed_under_its_label`.
6. "At a level that releases no spine tier, no collapsed block renders ...": verbatim; `test_the_shipped_default_dial_holds_every_chain_and_collapses_none`.
- Nothing added: the row already states the crossing IF-224 exists for (the brief reading the one predicate). Rule 3: SR-139 unchanged in reach.

**LLR-262** (SR-154, SR-156; TC-205, TC-257, TC-259, TC-328). Title and rationale unchanged (both clean). The recorded `detail` (at `d7e3a57df`), clause by clause, in its order. The session-log header markers `# commits: before..after` and `# review-scope: base..sha` are lines the coordinator writes and stay.
1. "The coordinator's session log records each session's phase and its exact commit range (`# commits: before..after`), and records a REVIEW session's full or narrow scope (`# review-scope: base..sha`)": kept ("a review session's"); TC-205 `tests/test_verdict_record.py::test_the_session_log_records_the_review_scope`; the range header, TC-259 `tests/test_review_scope.py` (file-level).
2. "session_range and parse_range read the range, review_logs yields the gating span with it, and range_paths lists the paths the range changed with renames split": kept ("the range is read back from the log, the review logs yield the gating span with it, and the paths the range changed are listed with renames split"); TC-259 `tests/test_review_scope.py` (file-level: the range parses from a log header, an empty range and the loop's placeholders parse as none); the gating span, TC-205 `tests/test_verdict_record.py::test_the_gate_range_survives_a_trunk_refresh`.
3. "scope_offenders names every changed path other than the REVIEW session's own verdict file, the round file named for the session's train, ordinal and logged phase under any reviewed sha and tag": kept ("The scope rule names ... under any reviewed commit and tag"); TC-259 `tests/test_review_scope.py` (file-level: only the session's own verdict file, with and without the relaxed tag, names no offender).
4. "record paths are not exempt": verbatim; TC-259 `tests/test_review_scope.py` (file-level: a log fragment, a scoreboard and another phase's round files are each named).
5. "Right after a REVIEW session the loop asks scope_offenders of the range it just took and, on any offender, stops the run needing an operator with the paths named": kept ("asks the scope rule"); TC-257 `tests/test_agent_loop_review.py::test_a_review_session_committing_beside_its_verdict_is_refused_by_name`, `::test_a_clean_review_session_passes`.
6. "a session log is append-only evidence, so every reader takes each log as the commit that ADDED it recorded it (log_history, review_logs), never at the branch tip, and the merge ladder's review-scope rung first refuses by name any commit in the lane that modified or deleted a session log, then asks the same function of every REVIEW session log the branch committed (review_scope_refusal) and refuses the merge by name, an unreadable log or range refusing too": kept, the function names dropped ("asks the same rule of every review session log"); TC-257 `tests/test_verdict_record.py::test_a_later_session_rewriting_a_session_log_cannot_launder_its_round`, `::test_the_merge_ladder_refuses_a_review_range_beyond_its_verdict`; the unreadable arm, file-level (`tests/test_verdict_record.py`, TC-205).
7. "After a REVIEW or CRITIQUE session, uncommitted changes not present before it, other than the coordinator's own session log, fail the draw through the existing failed-draw path - the route cooled and the same phase re-drawn - with those paths stashed under one entry named for the session, so the re-drawn session starts clean": kept ("a review or critique session"); TC-257 `tests/test_agent_loop_review.py::test_a_dirty_tree_after_a_review_fails_the_draw_and_it_reruns_clean`.
8. "when that stash fails the run stops needing an operator with the paths and the failure named, and nothing is re-drawn": verbatim; TC-257 `tests/test_agent_loop_review.py::test_a_failed_stash_stops_for_the_operator_and_redraws_nothing`, `::test_a_review_whose_leftovers_cannot_be_stashed_stops_and_is_not_redrawn`.
9. "read_verdict reads the verdict blob as committed at HEAD in both arms, so an uncommitted verdict is never routed on": kept ("The loop reads the verdict as committed at HEAD in both arms"); TC-257 `tests/test_agent_loop_review.py::test_an_uncommitted_review_verdict_is_never_routed_on`, `tests/test_agent_loop_critique.py::test_an_uncommitted_critique_verdict_is_never_routed_on`.
10. "session_body binds an adjudication's composed request beside its verdict before the loop calls it": kept ("The loop binds an adjudication's composed request beside its verdict before it calls it"); no test LLR-262's cases named drove it: `tests/test_done_when_blessing.py::test_the_loop_route_takes_a_combined_sitting_on_its_bound_kinds` tagged TC-257 (it stays TC-326's and TC-327's).
11. "after the call, run_iteration records the loop call's success from call_succeeded in plan, and adjudication_bookkeeping calls record_outcome against those bound kinds and uses its returned why as the completion obligation: a failed call is recorded failed, keeps that obligation and does not read its verdict": kept ("after the call it records whether the call succeeded, and its bookkeeping records the call's outcome against those bound kinds and takes the reason that record returns as the completion obligation: ..."); no test LLR-262's cases named drove it: `tests/test_done_when_blessing.py::test_the_loop_route_records_its_verdicts_outcome`, `::test_the_loop_records_a_failed_calls_verdict_failed`, `::test_a_failed_loop_call_keeps_its_obligation_and_reads_no_verdict` tagged TC-257 (they stay TC-326's).
12. "logged_rounds reads each round at the end of its session's recorded range, and only when that range changed the round file: a later commit rewriting the file changes nothing the gate counts, a file its session never committed is no round, and a key whose logs record different phases or ranges yields none": kept ("The logged rounds read each round ..."); TC-257 `tests/test_verdict_record.py::test_a_later_session_rewriting_a_round_cannot_change_what_the_gate_counts`, `::test_a_verdict_its_session_did_not_commit_is_not_a_round`; TC-205 `::test_two_logs_at_one_key_declaring_two_phases_serve_no_round`.
13. "done_when.items reads a spec's Done-when section, through kitlib.registry.done_when_section, as items: a list item with its continuation lines, or a prose paragraph, across subsections": kept ("A spec's Done-when section, read through the registry's one Done-when heading rule, is a list of items: ..."); TC-259 `tests/test_done_when.py` (file-level: subsections and continuation lines; no or an empty section has none; a prose criterion counts).
14. "changes compares a claim-time text with a later one after stripping ticks, strikethrough and whitespace": kept ("The comparison reads a claim-time text against a later one after stripping ..."); TC-259 `tests/test_done_when.py` (file-level: a tick and a strikethrough flag nothing).
15. "a later item carries a claim-time one when it equals it or extends it with evidence in the form closed specs use - appended text opening with an evidence separator (...) and carrying an evidence token (...) - while any other appended text, after closing punctuation or not, is a change": verbatim; TC-259 `tests/test_done_when.py` (file-level: the closed-spec evidence form flags nothing; appended prose flags with or without closing punctuation).
16. "and every claim-time item not carried is reported as changed and every later item carrying none as added": verbatim; TC-259 `tests/test_done_when.py` (file-level: a reworded, narrowed, deleted or added item flags).
17. "The claim warns by name on stderr for each claimed row with no Done-when item and still claims": kept ("on standard error"); TC-257 `tests/test_integrate.py::test_a_claim_of_a_row_with_no_done_when_warns_by_name`, `::test_a_claim_of_a_row_with_a_done_when_is_silent_about_it`.
18. "When a review round is composed, the brief gains a block quoting each change between the spec under active/<train>/ at the lane's base and the lane's own copy": kept ("the spec in the lane's active directory"); TC-257 `tests/test_agent_loop_review.py::test_the_reviewer_is_told_the_lane_reworded_its_done_when`, `::test_a_lane_that_only_ticked_its_done_when_tells_the_reviewer_nothing`.
19. "At merge, intake evaluates each claimed non-adjudication row": verbatim; TC-328 `tests/test_done_when_blessing.py::test_at_merge_an_uncovered_close_mints_the_goalposts_row`; TC-257 `tests/test_intake.py::test_a_lane_that_rewords_its_own_done_when_mints_an_adjudication`.
20. "An unreadable claim refuses the merge-time mint, naming why": verbatim; TC-328 `tests/test_done_when_blessing.py::test_at_merge_an_unreadable_claim_refuses_the_mint`.
21. "the merge itself stands and recovery is a trunk-side fix": verbatim; TC-328 `tests/test_done_when_blessing.py::test_at_merge_an_unreadable_claim_refuses_the_mint` (the mint refused, the merge not undone); file-level otherwise.
22. "For an absent claim, intake emits its stderr line that the Done-when check did not run and mints nothing": kept ("its standard-error line"); TC-328 `tests/test_done_when_blessing.py::test_at_merge_an_absent_claim_mints_nothing_and_says_so`.
23. "For a readable claim whose closed Done-when changed against trunk's pre-merge copy under active/<branch>, intake proceeds through the existing arms: when no verdict line or operator ruling in the merged tree binds the closed text's digest, it mints one brief-bearing done-when adjudication row, titled per row and branch so a re-run dedupes, with Adjudicates naming the closed work item and Context quoting each change": kept ("trunk's pre-merge copy in the branch's active directory"); TC-328 `tests/test_done_when_blessing.py::test_at_merge_an_uncovered_close_mints_the_goalposts_row`, `::test_at_merge_a_covered_close_mints_nothing`, `::test_at_merge_a_blessed_cover_mints_nothing`; TC-257 `tests/test_intake.py::test_a_lane_that_rewords_its_own_done_when_mints_an_adjudication`, `::test_a_lane_that_only_ticks_its_done_when_with_evidence_mints_nothing`.
24. "when a covering SUCCESSOR verdict carries Dispositions drafts, it mints the Done-when part's own drafts instead - the whole single-kind verdict or its one ## done-when section - and refuses repeated Dispositions inside that valid section or one supplying no draft": verbatim; TC-328 `tests/test_done_when_blessing.py::test_at_merge_a_successor_verdict_mints_its_own_draft`, `::test_at_merge_a_combined_successor_mints_the_done_when_sections_own_draft`, `::test_at_merge_an_ambiguous_successor_section_refuses`, `::test_at_merge_a_successor_verdict_with_no_draft_refuses`.
25. "A sitting with no or repeated done-when section, or a DONE-WHEN line under another heading, is invalid, covers nothing, and leaves the uncovered arm to mint the goalposts row": verbatim; TC-328 `tests/test_done_when_blessing.py::test_at_merge_a_successor_line_outside_its_section_blesses_nothing`, `::test_at_merge_an_ambiguous_successor_section_refuses`.
26. "review_logs reads the resolved final-reviewer mode once per call through reviewer_dials and passes it to every REVIEW log's gating_span, so all readers apply one mode": kept ("The review logs read the resolved final-reviewer mode once per call and pass it to every review log's gating span"; the dial reader's name dropped); TC-205 `tests/test_verdict_record.py::test_in_persisted_mode_the_final_reviewers_resumed_round_clears_the_gate`, `::test_a_final_round_clears_the_gate_only_with_both_dials_on`; once per call, file-level (`tests/test_verdict_record.py`, TC-205).
- Nothing added; nothing cut. Clauses 13 to 16 state IF-242's two functions (the items and the comparison). Rule 3: the meaning under SR-154 and SR-156 is unchanged.

**LLR-307** (SR-156; TC-325, TC-326 by name in `tests/test_done_when_blessing.py`). Title and rationale unchanged (clean).
1. "bound_items reads ...; digest binds the work-item id and those items as sha256:<16 hex>": kept, the function names dropped; the width (IF-326), `test_the_merge_refusal_names_the_digest_and_the_changes` (asserts `sha256:` and 16 characters); ticks read as the claimed item, `test_an_unchanged_or_only_ticked_done_when_holds_nothing`.
2. "covering reads verdict lines ... only through the one recorded-verdict reader ...": kept; TC-326 `test_a_covering_verdict_releases_the_dispatch_and_the_close`, `test_a_failed_calls_verdict_releases_nothing`, `test_a_recorded_calls_verdict_releases`, `test_an_unbound_sitting_blesses_nothing`, `test_another_brief_classes_verdict_covers_nothing_and_never_raises`.
3. Operator entries cover; unseen or retired key does not: `test_an_operator_ruling_binding_the_digest_releases_and_an_unseen_one_does_not`, `test_a_confirmed_ruling_still_carrying_the_retired_reviewed_key_does_not_release`.
4. "claim_copy returns absent ...; unreadable ...; unreadable_reason makes that a named hold ...": kept as the claim-copy read's answers; `test_an_absent_claim_is_released_at_every_hold_point`, `test_an_unreadable_claim_is_held_naming_why`, `test_at_merge_an_unreadable_claim_refuses_the_mint` (TC-328, beside).
5. "_copy_at gives both claim and current reads found, absent, or unreadable forms": kept; `test_an_unreadable_current_spec_is_held_naming_why`, `test_an_unreadable_claim_is_held_naming_why`.
6. "blessing_owed owes ...; deleting its Done-when section reports every claimed item changed": kept; `test_an_edit_with_no_verdict_holds_the_dispatch_and_the_close`, `test_a_lane_that_deletes_its_done_when_section_owes_a_blessing`.
7. Absent releases only for a never-claimed row; unreadable and gone hold naming why: verbatim; `test_an_absent_claim_is_released_at_every_hold_point`, `test_a_claimed_row_whose_spec_is_gone_from_the_lane_is_held`.
8. "spec_at returns path, text and why, and lane_hold compares ...; the terminal homes are docs/archive/work/complete, partial or cancelled, or the legacy docs/work equivalent": kept, the directories named in contract terms; `test_a_hand_close_into_any_terminal_home_is_held`, `test_the_hold_points_share_one_predicate`.
9. Staged entries, the close, a lone addition: verbatim; `test_the_staged_delta_classifies_each_claim_copy_change`.
10. The exact relink exemption: verbatim; `test_a_squash_landing_that_relinks_another_claims_done_when_link_is_not_held`, `test_a_squash_landing_with_a_real_edit_beside_the_relink_is_held`, `test_a_relink_with_no_move_in_the_same_delta_is_still_a_change`.
11. Which base, by branch: verbatim; `test_a_linked_worktree_on_the_declared_trunk_holds_an_unblessed_done_when_change`, `test_a_single_checkout_on_a_branch_not_named_for_its_claim_does_not_judge_a_non_close_change`, `test_a_trunk_amendment_of_a_claimed_done_when_is_held_and_one_that_changes_none_is_not`.
12. The trunk read once; undeclared holds: verbatim; `test_an_undeclared_trunk_refuses_each_caller_naming_the_key`, `test_a_commit_touching_no_claim_copy_is_not_refused_over_the_key`.
13. Unreadable delta or branch holds; off a work tree nothing judged: verbatim; `test_an_index_delta_git_cannot_list_holds_naming_why`, `test_a_branch_identity_git_cannot_read_holds_naming_why`.
14. Lossless listing: verbatim; `test_a_claim_copy_whose_path_git_quotes_is_judged_like_any_other`.
15. Compared with HEAD: verbatim; `test_a_two_commit_landing_is_held_at_its_first_commit_until_blessed`.
16. "The routes outside ... are stated once, as residue, in the shipped hook's `done-when-blessed` comment": kept, the step named as the pre-commit hook's Done-when blessing step; TC-325's inspection (its method: "Inspect the shipped hook's done-when-blessed comment"), `test_the_shipped_hooks_floor_holds_an_unblessed_hand_close`.
- Nothing added. IF-326: clause 1 states the 16-character cut the blessing digest owns; the acceptance record's reading of that width is LLR-359's statement (not touched).
- Rule 3: unchanged meaning under SR-156.

**LLR-340** (SR-240; TC-370). One phrase: "the checkout's or primary checkout's .githooks directory" reads "the hooks directory at the top of the checkout or of the primary checkout" (a directory name scrubbed; the module defines it so). Every other word verbatim; `tests/test_commit_hooks.py::test_a_relative_githooks_is_on`, `::test_an_absolute_githooks_is_on`, `::test_a_linked_worktree_is_on_with_a_tracked_relative_githooks`, `::test_another_directory_is_not_on`, `::test_unset_hooks_path_is_not_on`, `::test_a_missing_hook_is_not_on`, `::test_a_non_executable_hook_is_not_on`, `::test_an_unanswering_git_is_not_on`; the routes, `tests/test_hooks_on_routes.py` by name. It already stated IF-297's call: none when the hooks are on, else the cause and its repair.

**LLR-339** (SR-156; TC-369). A link in the slice's build; in round 1 one clause added (below). The recorded text states both crossings: "an absent, non-text or empty declaration, or one that names no local branch, is refused naming the declaration by every reader that judges or writes against the trunk" (IF-179's trunk name; `tests/test_trunk_name.py::test_a_repository_with_the_key_reads_it_and_one_without_refuses`, `::test_each_undeclared_shape_is_refused_naming_the_key`, `::test_the_reader_reads_no_worktree_list_and_no_current_branch`) and "A lane's integration base is its merge base with the declared trunk, in a single checkout as in a linked worktree" with "the readability report skips each declared measure naming the declaration" (IF-189's base; `test_default_base_keeps_the_trunk_boundary_after_a_single_checkout_resume`, `test_default_base_lets_an_undeclared_trunk_refusal_through`, `test_an_undeclared_trunk_on_a_claimed_lane_skips_naming_the_declaration`). IF-179's plain git runner (code and output) and IF-189's two fallbacks (an unrelated history, an unborn checkout) are form, not stated.
- Added (round 1, IF-189's fallbacks): "with no merge base, as on a history sharing no commit with the trunk, it is the checkout's own tip, and a checkout with no commit has none": `tests/test_agent_loop_review.py::test_default_base_is_the_tip_without_a_merge_base_and_none_with_no_commit` (new, tagged TC-369). Read in the code: the tip is named by its abbreviated id, the merge base by a full one (section 6, item 16). Rule 3: SR-156's one trunk boundary; nothing beyond it.

**LLR-247** (SR-209; TC-242; slice 2's row, re-accepted by the ninth sitting). Link only, a routed change; the recorded text states IF-194's vocabulary: the trailer key and the marker ("declares the commit-message trailer Loop-Session and the loop marker"), rendering ("rendered as one trailer line"), parsing ("returns its last trailer's session or none"), the refusal ("names the commit's subject when the trailer is missing, malformed, or names another session") and the marking ("set the marker in their own process environment once per run"); TC-242 `tests/test_loop_provenance.py` (file-level), `test_format_and_parse_round_trip`, `test_the_last_trailer_wins`, `test_a_missing_trailer_is_refused_naming_the_subject`, `test_a_child_the_dispatcher_starts_sees_the_marker`. The lane window and loop-writer commit IF-194 also carries are stated by LLR-248 (not touched).

**LLR-047** (SR-046; TC-047, TC-342; slice 1's row as WI-1071 restored it). A
link only, the recorded text verbatim: "The run menu reads the run section of
the stack profile into a list of name, command and description in
declaration order, with no interpolation, so a percent sign in a value is
literal, and keeping each name's case; a name's description row attaches to
its command, and a description row naming no command, or a command with an
empty value, is dropped" states IF-049's form (one name and command line per
capability, plus a description line), driven by TC-047's
`tests/test_run_menu.py::test_list_is_stable_name_tab_desc` (name, tab, description, in declaration order),
`::test_the_run_section_reads_values_literally_and_keeps_a_names_case` and
`::test_an_orphan_description_and_an_empty_command_are_dropped`. TC-431 still names
IF-049 and verifies LLR-370, which does not constrain it, so the name is no
repeat.

### C2

**LLR-046** (SR-154; TC-083, `tests/test_score_reviews.py`, module-tagged TC-083). The recorded text named no code; every clause verbatim, two sentences appended.
1. "Computes advisory substance components and decay history": `test_substance_is_mean_of_available_components_length_never_positive`, `test_anchored_precision_penalizes_unresolved_anchor`, `test_actionability_rate`, `test_scoreboard_roundtrip_and_decay`.
2. "treats tripwires as gates and never rewards length": `test_fired_tripwires_aggregates`, `test_cli_exit_1_on_tripwire`, `test_substance_is_mean_of_available_components_length_never_positive`.
3. "Severity hygiene rides the same non-scored gate path as the anti-gaming tripwires": file-level (the module, tagged TC-083, whose docstring states it), `test_tripwire_count_mismatch`.
4. "corroboration feeds the component scores": `test_corroboration_weights_cross_family_above_same`.
5. "the declared severity set makes a bullet a finding only when its bracket names one of its members, without regard to case, and another bracketed word is prose": `test_a_bracketed_word_that_is_not_a_severity_is_prose`, `test_every_declared_severity_reads_as_a_finding`.
6. "Verdict parsing takes its word and declared count from the shared strict review-line reader, returning no verdict when that reader refuses": `test_the_gate_reads_a_malformed_verdict_line_as_no_verdict`, `test_parse_verdict_reads_machine_line_and_findings`.
7. "scoreboard round trips are deterministic": `test_scoreboard_roundtrip_and_decay`.
- Added (IF-047): the verdict line reads VERDICT:, APPROVE or CHANGES-REQUESTED and findings= with the declared count, `test_parse_verdict_reads_machine_line_and_findings` (CHANGES-REQUESTED, 2), `test_merge_verdict_mechanical_no_debate` (APPROVE, 0); a count differing from the finding lines fires the count-mismatch tripwire, `test_tripwire_count_mismatch`.
- Added (IF-160): recording a round reads the standing tallies, decays the tally of each provider the round scores by the declared factor before adding its substance, appends the round and rewrites the scoreboard, `test_scoreboard_roundtrip_and_decay` (0.8 x 0.7 + 0.5 = 1.06 over two rounds, two rounds read back, the second's fields). Read from the code: a provider the round does not score keeps its tally undecayed, so the text says "each provider the round scores", not "each provider".
- Rule 3: SR-154's review routing holds the scorer as advisory state; the added sentences state the record form and the scoreboard the row already named. Within the parent.

**LLR-313** (SR-146, SR-154, SR-235; TC-333, named tests only, in `tests/test_review_brief.py`, `tests/test_review_brief_git.py`, `tests/test_plan_filing.py`, `tests/test_plan_pass.py`). Six function names removed; every clause kept; one sentence appended.
1. "Round accepts only a full-lane review with no prior findings or a narrow review that names the prior findings file": kept as "A review round accepts ..." (the leading word was the round type's name); `test_a_narrow_round_names_the_findings_it_answers`, `test_a_narrow_round_without_findings_and_a_full_one_with_them_are_refused`.
2. "[the review render] strictly fills the shipped reviewer template with the work-item specification, lane range, scratch location, optional review rubric and verdict destination": kept; `test_a_rendered_review_brief_carries_the_kit_clauses_and_the_lane_facts`.
3. "an empty derived set is a valid round, renders no test command, and states that the row touches no code": verbatim; `test_an_empty_set_renders_no_pytest_line_and_says_why`.
4. "listed evidence and reported gaps render beside the test command": verbatim; `test_the_sets_notes_render_beside_its_test_command`.
5. "[the critique render] strictly fills the shipped critique template with the work-item specification and named rubric": kept; `test_the_scope_critique_carries_ruling_twos_questions_and_its_rubric`.
6. "Both refuse a missing specification, unreadable or empty named input, or unfilled template slot before a brief is written": verbatim; `test_the_critique_render_refuses_a_missing_spec`, `test_an_empty_or_missing_named_input_refuses`, `test_a_named_input_that_is_not_there_refuses`, `test_an_unfilled_slot_refuses_and_no_brief_is_written`.
7. "[the filing check] accepts only a verdict bound to the reviewed full commit after the shared review-line reader accepts exactly one line whose keyword, in any case, is VERDICT, in exactly the canonical form `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`, whose count matches ... and whose changes request names a finding": kept as "Filing accepts only ...", the form kept as the output marker grammar it is (its backticks dropped); `test_a_malformed_review_is_refused_and_nothing_is_filed`, `test_a_bracketed_word_that_is_not_a_severity_never_refuses_a_filing`, `tests/test_plan_filing.py::test_a_critique_outside_the_verdict_format_is_refused_and_nothing_is_written` (unbound, malformed, count-mismatched, changes-without-findings).
8. "[the round chooser] chooses the next ordinal lane round filename": kept as "A filed round takes the lane's next ordinal round file name"; `test_filing_a_review_exits_zero_and_writes_only_the_round_file` (`001-REVIEW-A-<sha7>.md`), `test_a_filed_coordinator_review_appears_in_the_rollup`.
9. "[the filer] writes only a recorded verdict as that round record when the round reader reads its lane path back as that lane's scope": kept; `test_filing_a_review_exits_zero_and_writes_only_the_round_file` (a `feature/wi-900` branch exits 2 and files nothing).
10. "[the lane resolver] resolves commits on a branch and requires the base to be an ancestor of the reviewed commit": kept; `test_the_command_line_refuses_a_lane_the_git_reads_reject` (detached, not a commit, not an ancestor).
11. "A first plan critique is bound to its named lane commit, includes coverage over the Done-when alone, opens with that commit, and refuses a missing rubric, plan or specification, a missing or beyond delta, a coverage failure, or a third round": verbatim; `test_the_plan_critique_renders_over_the_committed_plan_and_its_coverage`, `test_the_plan_critique_refuses_a_missing_input_and_writes_nothing` (rubric, plan, spec, beyond delta). The render's delta, cap and coverage refusals are three shared refusals the filing and second-round paths call too, and those tests drive them: a missing delta, `test_a_plan_with_a_missing_or_beyond_delta_is_never_filed`; a third round, `test_at_the_cap_a_recorded_dismissal_of_every_blocking_finding_passes` (a third critique exits 2); a coverage failure, `test_the_second_critique_refuses_a_revision_that_misses_a_first_finding` (the render's coverage refusal, exit 2, no brief).
12. "A second plan critique ... refuses a revision that leaves a first-critique finding neither covered nor excluded": verbatim; `test_the_second_plan_critique_is_in_convergence_and_never_sees_the_first`, `test_the_second_critique_refuses_a_revision_that_misses_a_first_finding`.
13. "A single-plan brief strictly fills the shipped single-plan template ...; a revision additionally labels ... as claims under judgement": verbatim; `test_the_planner_brief_carries_the_clauses_the_contract_and_the_delta_question`, `test_the_revision_brief_asks_the_delta_question_again_and_labels_its_inputs`, `test_the_planner_brief_names_each_input_by_its_registry`.
14. "It refuses a missing specification, Done-when, plan or critique, or an unfilled slot": verbatim; `test_the_planner_brief_refuses_a_missing_input`, `test_the_planner_brief_refuses_an_unfilled_slot`, `test_the_command_writes_nothing_when_the_brief_refuses`.
15. "A critique record is filed only when it is bound to an ancestor that holds the plan and has the verdict form": verbatim; `test_a_critique_outside_the_verdict_format_is_refused_and_nothing_is_written`, `test_a_plan_with_a_missing_or_beyond_delta_is_never_filed`, `test_a_filed_critique_exits_zero_and_writes_only_its_record`.
16. "a pass record is written only from committed cited records, passing plan coverage, and a passing delta, after an acceptance or an accepted dismissal of every blocking and major second-round finding": verbatim; `test_the_pass_form_refuses_while_head_lacks_the_critique_it_cites`, `test_the_pass_form_reads_a_committed_critique_through_line_ending_conversion`, `test_a_plan_the_coverage_gate_fails_never_passes`, `test_a_minor_only_change_request_passes`, `test_a_first_change_request_allows_one_revision_and_never_passes`, `test_at_the_cap_a_recorded_dismissal_of_every_blocking_finding_passes`, `test_at_the_cap_anything_but_a_recorded_dismissal_is_refused`, `test_at_the_cap_two_blocking_findings_with_one_dismissed_are_refused`, `test_at_the_cap_an_uncommitted_dispute_verdict_is_refused`, `test_at_the_cap_a_successor_ruling_never_passes`.
17. "At the cap, a dispute findings file is written only from the committed second critique, giving ... a declared position; it refuses another identifier set or an existing file": verbatim; `test_at_the_cap_a_major_after_a_minor_is_disputed_under_its_own_number`, `test_the_dispute_findings_file_refuses_ids_other_than_the_blocking_ones`; no test drove "an existing file", `tests/test_plan_filing.py::test_the_dispute_findings_file_is_never_written_over_an_existing_one` added.
18. "The second plan critique's brief never carries the first critique's verdict or any finding's text": verbatim; `test_the_second_plan_critique_is_in_convergence_and_never_sees_the_first`.
19. "A review round is ordinary by default or convergence: ... refuses a narrow scope or unknown stance before writing a brief": verbatim; `test_an_absent_stance_renders_the_ordinary_round`, `test_a_convergence_round_renders_the_one_fixed_stance_line`, `test_a_narrow_round_refuses_the_convergence_stance` (narrow and `wild`), `test_a_convergence_brief_carries_the_stance_and_its_marking`.
20. "An ordinary review reading scope reads the delegated-decisions record and filed plan critiques, while a convergence scope excludes both": verbatim; `test_only_a_convergence_brief_leaves_the_decisions_record_and_critiques_out_of_its_reading_scope`, `test_an_ordinary_review_reads_the_decisions_record`.
21. "a convergence render refuses a reviewer template whose reading-scope command does not carry the review-record exclusion exactly once": verbatim; `test_only_a_convergence_brief_leaves_the_decisions_record_and_critiques_out_of_its_reading_scope` (its `exactly once` refusal), `test_the_reading_scope_never_shows_a_record_of_earlier_findings`.
22. "The scope critique names the component and interface registries, derived architecture, runtime flows, and dependency ledger, marking an absent registry": verbatim; `test_the_scope_critique_names_the_registries_beside_the_spec`.
23. "the single-plan brief and scope critique render their registry lines from one declared set": verbatim; `test_the_scope_rubric_names_every_registry_the_critique_brief_renders`, `test_the_planner_brief_names_each_input_by_its_registry`.
24. "A plan critique ties every severity class to a normal-use-reachable defect ...": verbatim; `test_the_plan_critique_brief_ties_severity_to_reachability`.
25. "Its confirming round treats a new finding as BLOCKER or MAJOR only when ...": verbatim; `test_the_second_plan_critique_is_in_convergence_and_never_sees_the_first` (the convergence classes' sentence).
26. "A finding line bearing the convergence-class tag defined by LLR-311 is filed and counted as one finding": verbatim; `test_a_convergence_tagged_finding_files_with_its_count_unchanged`.
- Added (IF-289): exit 0 when it writes a brief or files a review, a critique, a dispute findings file or a pass record, 2 when it refuses, a refusal writing no requested brief or record: `test_a_review_render_exits_zero_and_writes_only_the_brief`, `test_filing_a_review_exits_zero_and_writes_only_the_round_file`, `test_a_filed_critique_exits_zero_and_writes_only_its_record`, `test_the_dispute_findings_file_refuses_ids_other_than_the_blocking_ones` (2 then 0), `test_the_pass_form_refuses_while_head_lacks_the_critique_it_cites` (2 then 0), `test_the_command_line_refuses_a_lane_the_git_reads_reject` (2, no file, clean repository), `test_the_plan_critique_refuses_a_missing_input_and_writes_nothing` (2, no brief).
- Rule 3: SR-235 asks a malformed or unbound verdict refused without a record and SR-146 that a refused render write no brief; the exit sentence states those outcomes as codes. Within the parents.

**LLR-314** (SR-234; TC-334, `tests/test_dispute.py` and three other modules by name).
1. "kitlib.dispute accepts one TOML findings file with only a non-empty `range` and a non-empty `[[finding]]` list": kept as "The shared dispute grammar accepts ... a non-empty range and a non-empty list of findings"; `test_a_malformed_findings_file_refuses_the_brief` (bad range, unknown key, no finding, not TOML).
2. "Each finding has exactly a unique letter-led id, held_by `builder` or `coordinator`, and non-empty finding and position text": kept ("the party holding its position, builder or coordinator"); same test (duplicate id, bad id, bad holder, empty position, an extra or a missing key).
3. "which the reader keeps verbatim apart from every leading and trailing newline character; spaces and interior lines are kept": verbatim; `test_the_dispute_brief_carries_each_finding_its_position_range_and_scope_link` for verbatim; no test told the newline trim from a whitespace trim, `test_a_findings_text_keeps_its_spaces_and_drops_only_its_edge_newlines` added.
4. "request_line writes the composed request, and requested_ids reads its first DISPUTE findings line": kept; `test_the_dispute_brief_carries_each_finding_its_position_range_and_scope_link` (the `DISPUTE: findings=F1;R2-3` line read back); no test drove "first", `test_the_first_request_and_findings_file_lines_are_the_ones_read` added.
5. "The composed brief's findings-file line names the findings file the brief was composed over; its first such line supplies the path, and no line or an empty one supplies none": verbatim; `test_the_dispute_brief_names_the_findings_file_it_was_composed_over` (the line, and no line), and the added test for "first" and "an empty one".
6. "parse reads RULING lines one physical line at a time and accepts only one FIX, SUCCESSOR, DISMISS, or ESCALATE ruling with a reason for every requested id": kept as "The verdict reader reads ..."; `test_a_well_formed_verdict_is_read_and_parsed`, `test_a_malformed_or_incomplete_verdict_is_refused` (a reason on the next line, a prefixed line).
7. "DISMISS additionally takes only out-of-scope, refuted, or not-worth-cost and a reason": verbatim; same two tests.
8. "Missing, duplicate, unrequested, malformed, or incomplete content refuses; no value is defaulted": verbatim; `test_a_malformed_or_incomplete_verdict_is_refused`, `test_a_verdict_judged_against_no_requested_findings_is_refused`.
9. "SUCCESSOR takes a reason and no reason class": verbatim; `test_a_successor_ruling_is_read_and_parsed`, `test_a_malformed_or_incomplete_verdict_is_refused`.
10. "an unknown ruling refusal names FIX, SUCCESSOR, DISMISS, and ESCALATE in that order": verbatim; `test_an_unknown_ruling_is_refused_naming_the_four_rulings`.
- Rule 3: unchanged meaning under SR-234.

**LLR-367** (SR-241; TC-413 to TC-420, TC-563). Link only, the recorded text verbatim. The words stating IF-309's behaviour: "It returns the sorted union of tagged test files, lists a tagged test case's non-test evidence and declared non-executable evidence without running it, and returns every gap", "refuses by name / refuses partial naming every gap / refuses empty", and "set printing" among its covered behaviour; TC-415 (which names IF-309) drives the refusals and gaps, `test_a_code_touching_row_naming_no_sr_is_refused_by_name`, `test_partial_names_every_gap_and_outranks_empty`, `test_empty_is_refused_only_with_no_gap_and_no_tagged_file`, `test_gaps_on_a_row_touching_no_code_are_reported_never_refused`; the set and the listed evidence are driven by TC-419's `tests/test_review_brief_git.py::test_the_render_lists_the_derived_files`.

**LLR-337** (SR-154; TC-367). The recorded text named no code; every sentence verbatim, driven by TC-367's named tests as its method lists them (`tests/test_plan_gate.py`, `tests/test_plan_pass.py`). One sentence appended (IF-295): run as the plan-gate step over the commit being made, it prints one step line, FAIL with each hold or ok, and exits 1 when a commit is held and 0 otherwise: `test_a_build_without_a_pass_record_is_refused_at_the_hook_and_the_landing` (exit 1 through the harness, `FAIL  plan-gate`), and, since no test ran the step itself or drove its ok and 0, `test_the_gate_command_prints_fail_and_exits_1_then_ok_and_exits_0` added. Rule 3: SR-154 refuses build output at its making until a pass record binds; the step's exit is that refusal.

**LLR-254** (SR-215; TC-247, `tests/test_rejudge.py`, module-tagged TC-247).
1. "A sibling of consolidate.py imported by intake": kept as "sits beside the consolidation census, and the intake imports it"; file-level, and `test_the_release_subcommand_mints_for_an_expired_result_once` (the intake's command reaching the decision).
2. "observation_test_cases(root, rev) reads observation cases at a revision": kept; `test_the_observation_cases_are_read_at_the_revision`.
3. "checkpoint_for(root, rev, tc) returns the case's Trigger when it names the release or stage-gate checkpoint, else merge": kept; `test_checkpoint_for_maps_explicit_triggers` (and a missing case reads merge).
4. "due_cases(root, rev, now, checkpoint) reads committed inputs and records and uses the cadence decision to apply the configured closed-WI floor and declared trigger": kept; `test_inputs_are_read_at_the_revision_not_the_working_tree`, `test_trigger_waits_for_closed_work_floor`.
5. "A case with no record is due at once, and an expired record is due at once; neither waits for the floor": verbatim; `test_first_judgement_and_expiry_bypass_trigger_and_floor`, `test_a_case_with_no_result_gets_one_draft`, `test_an_expired_result_gets_one_draft`.
6. "Without a trigger, a changed input digest is due subject to the floor; without inputs, only absence and expiry make a case due": verbatim; `test_trigger_waits_for_closed_work_floor` (the empty-trigger case), `test_floor_alone_does_not_fire_trigger`, `test_a_case_declaring_no_inputs_is_judged_by_expiry_and_absence_alone`.
7. "checkpoint_drafts drafts each due case once, suppressing an open item by its typed Brief and Adjudicates cells, never by title": kept; `test_an_open_item_found_by_its_typed_cells_suppresses_a_second_draft`.
8. "A draft names the case, the reason, the rubric and the changed inputs or the fired trigger, and its title carries the case id and the inputs-digest prefix": verbatim; `test_a_changed_input_gets_one_draft_naming_the_case_and_the_input`, `test_trigger_waits_for_closed_work_floor` (trigger and rubric lines), `test_an_expired_result_gets_one_draft`.
9. "Committed links are excluded by the observation writer's own link predicate": verbatim; `test_a_committed_link_is_not_content`.
10. "No model runs": verbatim; `test_no_agent_command_is_spawned`.
- Rule 3: unchanged meaning under SR-215.

**LLR-255** (SR-215; TC-248, `tests/test_rejudge.py`, `tests/test_intake.py`, both module-tagged TC-248, and one named test).
1. "intake_after_merge adds rejudge.checkpoint_drafts(root, after, "merge") to its drafts inside the held merge slot, so the check runs once per merged work item": kept; `tests/test_intake.py::test_a_merge_changing_an_observation_input_mints_one_rejudge_item`.
2. "mint_rejudge(root, rev, checkpoint) files them through _mint": kept as "The re-judge mint files them through the mint path"; `test_the_release_mint_runs_the_mint_checks`.
3. "`intake.py rejudge --checkpoint release` is the release-preparation entry and `... --checkpoint stage-gate` the stage-gate-preparation entry, and the command refuses a merge checkpoint": kept; `test_the_release_subcommand_mints_for_an_expired_result_once`, `test_stage_gate_trigger_is_filed_through_the_cli_not_at_merge`, `test_the_cli_refuses_a_manual_merge_checkpoint`.
4. "Release and stage-gate preparation are a person's acts, so each is prompted where that person works": verbatim; realized by clauses 5 and 6 and their tests.
5. "The release checklist, a view that may not import intake, carries a required item from _rejudge_checklist_line naming the release command and the count ..., read through rejudge's pure decision": kept; `test_the_release_checklist_carries_the_required_rejudge_item`; "may not import" is driven by `tests/test_import_layers.py::test_a_view_never_imports_a_lifecycle_service` (a generated view never imports the intake), tagged TC-248.
6. "The shipped gate-advance skill names the stage-gate command as a required step before a rung is signed": verbatim; `tests/test_skills_index.py::test_gate_advance_names_the_stage_gate_rejudge_step`.
7. "The minted row's brief and verdict entries are added where its kind requires them": verbatim; `test_a_minted_rejudge_row_composes_its_brief_and_demands_its_verdict`.
8. "Filing goes through the mint path's staging, which has to stage and restore only what it wrote ...": verbatim; `test_a_pre_staged_unrelated_edit_survives_the_release_mint`.
- Added (IF-229): exit 0 naming the count or that nothing is due; a mint refusal mints nothing, prints its reason on standard error and exits 1: no test asserted the count line or the command's exit 1, `test_the_release_command_names_its_count_and_a_refused_mint_exits_1` added.
- Rule 3: SR-215 files one item per due case at a release; the exit states the outcome. Within the parent.

**LLR-264** (SR-220; TC-260's four tests in `tests/test_intake.py`).
1. "`intake.py consolidate` runs consolidate.census_draft over the checkout's registry": kept; all four tests.
2. "When the census proposes nothing it prints the census's reason on stdout and exits 0, because ...": kept ("standard output"); `test_the_consolidation_census_says_why_it_proposes_nothing`, `test_the_consolidation_census_mints_one_row_then_says_why_not_again` (second run).
3. "Otherwise it prints the candidate set, its Digests pair and each pre-filter finding, then mints the one row through _mint, the one allocator of a work-item id, as one bookkeeping commit, and exits 0": kept; `test_the_consolidation_census_mints_one_row_then_says_why_not_again`.
4. "a mint refusal prints on stderr and exits 1": kept; `test_a_refused_consolidation_mint_says_why_on_stderr_and_exits_1`.
5. "`--dry-run` prints the same census and mints nothing": kept as "Its dry run ..."; `test_the_consolidation_census_dry_run_names_the_cluster_and_mints_nothing`.
- Rule 3: unchanged meaning under SR-220.

**LLR-265** (SR-215; TC-261, named tests in `tests/test_intake.py`).
1. "`intake.py sweep --before <sha> --after <sha> --branch <lane> --merged WI-###[;WI-###]` runs intake_after_merge over the range with an outcomes map holding exactly the named rows": kept; `test_merged_mints_what_the_named_rows_owe_and_nothing_else`.
2. "merged_outcomes reads each one's outcome from the one terminal folder holding its spec (complete, partial or cancelled)": kept; same test (partial), `test_merged_mints_every_arm_the_slot_would_have_for_a_hand_merge` (complete).
3. "so the early-close dispositions, the clean-close spot checks and the drafts a merged adjudication row names ... are minted for those rows and no others": verbatim; both tests above.
4. "beside the range's diff triggers (the amendment and first-acceptance rows) and the merge checkpoint's re-judge drafts at `--after`": kept ("at the range's later end"); `test_merged_mints_what_the_named_rows_owe_and_nothing_else` (amendment), `test_merged_mints_every_arm_the_slot_would_have_for_a_hand_merge` (first acceptance), `test_a_sweep_after_a_hand_merge_runs_the_merge_checkpoint`.
5. "`--merged` judges one merge, so _merged_shape_refusal refuses it without both range ends, when the two name one commit, and without `--branch`": kept; `test_merged_needs_a_real_range_and_the_lane_branch`.
6. "The branch is the claim identity the Done-when check reads: a named row whose claim is under `active/<branch>/` at `--before` is checked against it, and one whose claim is not there gets one stderr line naming the row, the branch and why the check did not run": kept; `test_merged_mints_every_arm_the_slot_would_have_for_a_hand_merge`, `test_merged_says_by_name_when_the_done_when_arm_cannot_run`.
7. "`--branch` names the mint commit either way, and a range or history sweep hands the check no claim identity": kept; no TC-261 test drove either half, `test_a_history_sweep_naming_a_branch_labels_its_commit_and_runs_no_done_when_check` added.
8. "A named row in no terminal folder, or in more than one, refuses the whole sweep by name and mints nothing": verbatim; `test_merged_refuses_a_row_no_terminal_folder_holds`, `test_merged_refuses_a_row_two_terminal_folders_hold`.
9. "`--merged` and `--with-terminal` are mutually exclusive; the range shape without either still judges no close, and the bare sweep still judges every close on file": kept; `test_merged_and_with_terminal_are_one_question_asked_two_ways`, `test_a_range_sweep_mints_the_range_and_touches_no_terminal_folder`, `test_a_bare_sweep_still_walks_the_terminal_folders`.
10. "Idempotent by the mint's exact-title dedup, like every sweep": verbatim; `test_merged_mints_what_the_named_rows_owe_and_nothing_else` (second run).
- Added (IF-244): a sweep that mints exits 0 naming the count, one with nothing to mint exits 0 saying so, `test_a_range_sweep_mints_the_range_and_touches_no_terminal_folder` (`sweep minted 1 row(s).`), `test_a_range_sweep_run_twice_mints_nothing_the_second_time` (`nothing to mint.`, tagged TC-261); a refusal of a named-row sweep for its range, its branch or a row's terminal folder mints nothing and exits 1 with its reason on standard error, `test_merged_needs_a_real_range_and_the_lane_branch`, `test_merged_refuses_a_row_no_terminal_folder_holds`, `test_merged_refuses_a_row_two_terminal_folders_hold`. The mutual exclusion is the command line's own refusal (exit 2), so the exit sentence does not cover it.
- Rule 3: SR-215's merge checkpoint and the slot's rows; within the parent.

**LLR-293** (SR-215; TC-306, `tests/test_rejudge.py`, module-tagged TC-306).
1. "Cadence reads the process policy at the committed checkpoint": kept; `test_an_uncommitted_policy_change_moves_nothing`.
2. "and counts distinct terminal archived WI IDs added since the commit that added the latest observation record": kept; `test_trigger_waits_for_closed_work_floor`, `test_raised_floor_and_bookkeeping_do_not_count`, `test_existing_archive_edits_do_not_count_as_new_closed_work`, `test_trigger_reads_committed_revision_and_new_result_resets_floor`.
3. "eligible applies the greater of default and case floors": kept; `test_case_floor_can_raise_but_not_lower_default`.
4. "then file globs, the files whose Component header declares the component in the checked-out tree, release or stage-gate triggers": kept; `test_trigger_waits_for_closed_work_floor`, `test_floor_alone_does_not_fire_trigger`, `test_component_trigger_reads_no_interface_row`.
5. "An omitted trigger leaves input-digest comparison to rejudge": kept; the empty-trigger cases of the two trigger tests.
6. "History is cached per result commit": verbatim; no test drove the cache, `test_the_cadence_reads_one_history_per_result_commit` added.
7. "malformed policy, an unknown trigger and unreadable history raise ValueError": kept ("each raise an error"); `test_cadence_refuses_what_it_cannot_read`.
8. "Zero explicitly disables the default floor": verbatim; `test_a_zero_policy_floor_disables_the_default`.

**LLR-294** (SR-215; TC-307 `tests/test_rejudge_rubric.py`, TC-311).
1. "observation_rubric_findings returns one warning for each real observation case omitting Rubric, naming the case": kept; `tests/test_rejudge_rubric.py::test_missing_observation_rubric_warns`.
2. "Automated and example cases are excluded": verbatim; same test.
3. "check_trajectory prints the warnings before its no-WI return and never promotes them under strict": kept; `tests/test_rejudge.py::test_trajectory_rubric_warning_survives_strict_and_no_work_items`.
- Rule 3 for both: SR-215 asks a warning, never a failure, for a case citing no criteria; unchanged.

**LLR-162** (SR-146; TC-157 `tests/test_prompts.py`, `tests/test_routing_and_prompts.py`, module-tagged; TC-192 by name).
1. "`load` reads a shipped template (or an operator override) and raises a named `PromptError`": kept; `test_an_unknown_key_refuses_by_name`; no test in its modules loaded an override, `test_an_operator_override_is_loaded_in_place_of_the_shipped_template` added.
2. "`fill` refuses an unknown slot and an unfilled declared slot": kept; `test_fill_is_strict_in_both_directions`.
3. "`digest` normalizes line endings before hashing": kept; `test_digest_is_stable_across_line_endings`, `test_a_line_ending_difference_in_the_home_is_not_an_edit`.
4. "`preflight` turns a missing template into a launch-time refusal": kept; `test_preflight_is_clean_and_bites_on_a_missing_file`.
5. "`KIT_FRAGMENTS` declares each composed fragment and its slot": kept; `test_an_edit_to_the_composed_question_home_stales_the_catalogue`.
6. "`fragment_rows` reads each through the shared `_read_body`, digests its normalized text, and raises `PromptError` when it is absent, unreadable or empty ...": kept; `test_an_unreadable_home_fails_generation_and_the_check` (absent, undecodable, empty).
7. "`gen_prompt_catalog.py` renders the catalogue with a `--check` freshness gate": kept; `test_the_catalogue_on_disk_is_FRESH`, `test_a_template_edit_moves_its_digest_and_so_the_catalogue`.
8. "and `agent_common.prompt_fingerprint` records the rendered result per session beside the template's own name": kept; `test_the_session_log_records_which_template_and_what_it_rendered_to`, `test_the_fingerprint_identifies_the_text_and_folds_nothing_else`.
- Added (IF-098): the prompt rows, sorted by key, give key, file, slots and digest, and the fragment rows file, slot and digest: `test_the_catalogue_lists_every_shipped_prompt_with_its_digest` asserts keys and digests only, so `test_the_catalogue_rows_give_each_prompt_its_file_slots_and_digest_in_key_order` added.
- Rule 3: SR-146's catalogue lists every shipped prompt with its digest; within it.

**LLR-283** (SR-225; TC-293, `tests/test_decision_record.py` and `tests/test_decisions_to_review.py`, both module-tagged TC-293). Every clause kept but the first, narrowed.
1. "kitlib/decisions.py imports nothing and reads no file, git or environment": NARROWED to "imports only the standard library and the shared kernel's id reading, and reads no file, git or environment". Read from the code: it imports `re`, `tomllib` and the shared kernel's id-number reader, so "imports nothing" no longer holds; the no-read half does. No test drove either half: `test_the_decisions_library_imports_only_the_standard_library_and_the_kernel` added.
2. "record_path(run) is DECISIONS_DIR/<run>.toml under docs/decisions, the run's / becoming - and no other character rewritten": kept; `test_the_record_path_is_one_file_per_run`.
3. "a run name carrying any other character outside the shared run-name alphabet raises ValueError naming the run and each such character": kept ("is refused, naming ..."); `tests/test_decision_overrule.py::test_the_run_name_alphabet_is_what_git_refuses_plus_two_delimiters`, `::test_a_run_name_carrying_the_citation_delimiter_has_no_record` (tagged TC-293).
4. "That alphabet excludes /, # and exactly the characters git refuses ...": verbatim; `test_the_run_name_alphabet_is_what_git_refuses_plus_two_delimiters`.
5. "citations(text) recognizes every character that record_path keeps ...; its path ends at the first # after docs/decisions/, so each citation has one parse": kept; `::test_the_citation_reads_every_run_name_the_record_path_writes`, `::test_the_citation_reader_takes_no_surrounding_prose`, `::test_a_run_name_carrying_the_citation_delimiter_has_no_record` (tagged).
6. "operator_state(value) returns confirmed, overruled, the empty string for an absent operator value, or None for any other value; its strings are exact": kept; `tests/test_decisions_to_review.py::test_the_shipped_template_entry_leaves_the_operator_key_unset`, `::test_an_unrecognized_value_reads_as_not_yet_seen_and_is_reported` (`"Confirmed"` is not confirmed).
7. "record_findings(text) parses the text as TOML, returning one finding when it does not parse, and otherwise one finding per defect: ...": kept, the required keys named in words; `test_an_unparseable_record_is_one_finding`, `test_a_decision_key_that_is_not_a_table_is_reported`, `test_an_entry_id_outside_the_numbering_is_reported`, `test_a_non_table_entry_is_reported`, `test_each_missing_required_key_is_reported_by_entry`, `test_each_required_key_holding_non_text_is_reported`, `test_each_required_key_left_blank`, `test_an_unrecognized_value_reads_as_not_yet_seen_and_is_reported`, `test_the_retired_reviewed_key_is_a_finding_and_never_read`, `test_an_overrule_with_a_blank_note_is_a_format_finding`, `test_a_malformed_hoist_is_reported`, `test_a_missing_hoist_is_reported`, `test_a_hoist_naming_an_absent_entry_is_reported`.
8. "an id ending -000 is skipped wherever it appears, and other entry keys are not judged": verbatim; `test_a_000_entry_is_inert`, `test_000_is_never_counted_or_judged`, `test_extra_keys_on_an_entry_are_not_judged`.
9. "It does not raise": kept ("The findings never raise"); `test_the_findings_never_raise`.
10. "review_queue(text) returns (unseen, overruled, confirmed_count): ...": kept; `test_confirmed_and_overruled_are_not_counted_and_are_sound`, `test_an_unrecognized_value_reads_as_not_yet_seen_and_is_reported`, `test_the_retired_reviewed_key_is_a_finding_and_never_read`, `test_an_all_confirmed_state_counts_zero`.
11. "Each list holds dictionaries with id, high_risk, fields and the raw operator value, orders hoisted entries first and then by id, excludes -000, and is empty for a text that does not parse without raising": kept; `test_review_queue_lists_hoisted_first_then_by_id`, `test_the_shipped_template_entry_leaves_the_operator_key_unset` (-000), `test_an_unparseable_record_is_reported_and_counts_nothing`; no test read the entry's fields or raw value, `test_each_queued_entry_carries_its_id_hoist_fields_and_raw_operator_value` added.
12. "citation(rel, id) returns <rel>#<id>": kept; `::test_the_citation_reads_every_run_name_the_record_path_writes` (tagged).
13. "citations(text) returns the set of docs/decisions/<run>.toml#D-<digits> tokens whose id is not followed by a digit": kept; `::test_the_citation_reader_takes_no_surrounding_prose`, `::test_a_citation_of_another_entry_does_not_match` (a following digit; tagged).
14. "newly_overruled(before, after) returns, in id order, entries ... raising ValueError naming a parse error when after does not parse": kept ("refused, naming the parse error"); `::test_an_entry_already_overruled_owes_nothing_again`, `::test_a_repair_of_an_unparseable_parent_owes_every_overrule_it_shows`, `::test_a_record_that_does_not_parse_is_refused_at_the_commit_and_the_merge_slot` (tagged); no test drove "in id order", `test_the_newly_overruled_entries_come_in_id_order_whatever_else_they_carry` added.
15. "A retired key or blank review note does not suppress this transition reading": verbatim; the added test (D-9 carries both), and `tests/test_decision_overrule.py::test_an_overrule_beside_the_retired_key_still_owes_its_work` (TC-319).
16. "owed(mode, outcomes) is true for mode record or escalate-first with at least one outcome, whatever the outcome, a partial close included": kept; `test_which_closes_owe_a_record`.
17. "missing_record_refusal(mode, run) returns the merge slot refusal of an owed close with no record: naming the run, record_path(run) and the dial, or, for a refused run name, naming the run and the ValueError; each ends nothing was merged": kept; the merge tests (TC-294) assert the path and the ending but not the run or the dial, `test_the_missing_record_refusal_names_the_run_the_path_and_the_dial` added.
18. "session_note(mode, run) returns the empty string for off and otherwise the instruction naming ...": kept; `test_the_session_note_names_the_path_only_under_a_recording_dial` (extended: a call the session is unsure of, the record not an exit, escalate-first's prefer-the-exits sentence asserted by their words), `test_the_session_note_names_the_routing_home_and_the_two_kinds_it_leaves`, `test_the_routing_home_and_the_template_leave_out_spine_stated_and_conduct`.
19. "pending.decision_records counts the unseen entries ..., prefixes a record's findings with its file, and answers no records where the directory is absent": kept; `test_records_are_summed_and_their_findings_named_by_file`, `test_no_decisions_directory_has_nothing_unseen`.
20. "gen_open_items.record_findings_block renders those findings, by file and entry, as a notice closing the pending operator actions, and nothing when there is none; no entry is listed ...": kept; `test_the_findings_notice_closes_section_three`, `test_sound_records_and_no_records_put_no_notice_on_the_page`, `test_the_page_lists_no_entry_and_has_no_decisions_section`.
- Rule 3: SR-225's acceptance criteria state the record's fields, verdicts, hoist, citation token and the close refusal; the row decomposes them. The narrowing (clause 1) moves nothing the SR states.

**LLR-335** (SR-148; TC-360). Link only, the recorded text verbatim. The words stating IF-294's calls: "A disposition adoption is a fenced TOML block containing exactly one distinct, well-formed successor id" (the block parse: `test_an_adoption_block_is_parsed_apart_from_the_drafts`, `test_a_malformed_adoption_block_is_a_parse_refusal`, `test_a_repeated_adoption_is_a_parse_refusal`); "The disposed row is resolved from the title's one event token" (`test_the_disposed_row_is_read_from_either_minted_title_form`); "validation accepts exactly one ... specification that is open in draft, queued or active state ... refuses every other state ..." (the row refusal over a supplied listing: `test_validity_is_read_against_the_registry_with_distinct_refusals`); "refuses a request without a record, a record without a request, unequal request and record, a malformed record" (the record read and the record-change judgement: `test_the_record_reader_accepts_only_a_list_of_distinct_ids`, `test_the_record_change_table`), all in `tests/test_disposition_adoption.py`.

**LLR-345** (SR-148; TC-383, named tests in `tests/test_adoption_record.py` and three others).
1. "A commit that changes an adoption record or moves a requesting specification into docs/work/complete or docs/archive/work/complete is admitted only when it is the close's own commit or carries an existing record with its request unchanged in some parent": kept (the folders in contract terms); `test_the_closes_own_commit_passes`, `test_a_later_commit_carrying_the_record_unchanged_passes`, `test_a_requesting_spec_moved_into_complete_without_a_record_is_refused`. "Admitted only when" is a necessary condition of this rule, recorded so, not a claim that such a commit passes every step.
2. "A merge is judged only on the changes absent from every parent, under that same rule": verbatim; `test_a_refresh_merge_carrying_trunks_record_passes`.
3. "The close's own commit has one readable parent, paired moves from one docs/work/active branch to docs/work/complete, ... each changed path outside docs/work exactly the inbound relink ...": kept; `test_a_real_close_relinking_a_file_outside_docs_work_passes_the_rider_and_the_squash_hook`, `test_a_hand_written_record_beside_the_same_relink_is_refused`, `test_a_hand_close_writing_a_record_is_refused`, `tests/test_disposition_adoption.py::test_the_close_shape_admits_outside_paths_only_through_the_oracle`.
4. "its record equals its request and every adopted id is valid in the parent tree": verbatim; `test_a_close_shaped_commit_whose_record_differs_from_the_request_is_refused`, `test_a_close_shaped_commit_whose_adoption_fails_in_the_parent_tree_is_refused`.
5. "The tree under judgement is read strictly; a parent's specification whose front matter or record does not parse holds no record, while a parent git cannot read is refused and named": verbatim; `test_a_parent_behind_a_shallow_boundary_is_refused_by_name` for the last half; no test drove the first two, `test_a_malformed_record_is_refused_and_the_commit_dropping_it_is_not` added.
6. "Every other record change, a carried record whose request changed or was removed, or a requesting move without a record is refused": verbatim; `test_a_record_changed_later_is_refused`, `test_a_record_removed_later_is_refused`, `test_a_request_rewritten_under_a_carried_record_is_refused`, `test_a_requesting_spec_moved_into_complete_without_a_record_is_refused`, `test_a_record_written_in_a_lane_commit_is_refused_at_the_slot`.
7. "The rule applies to the lane-commit walk and staged commit check, including their squash handling": verbatim; `test_the_record_rule_rides_the_lane_commit_walk`, `test_the_pre_commit_hook_runs_the_adoption_record_step`, `test_a_record_staged_on_trunk_is_refused_by_the_hook_step`, `test_a_rebased_lanes_squash_landing_is_admitted`, `test_a_squash_whose_index_edits_the_tips_record_is_refused`, `test_a_squash_landing_is_judged_through_the_shared_walk`.
- Added (IF-304): run as the adoption-record step it prints one step line, FAIL with each refusal or ok, and exits 1 when it refuses a record change and 0 otherwise: the exit was asserted (`test_a_record_staged_on_trunk_is_refused_by_the_hook_step`, `test_a_rebased_lanes_squash_landing_is_admitted`), the line's words were not, `test_the_step_prints_fail_or_ok_with_its_exit` added.
- Rule 3: SR-148 holds the adoption record rule; the step's exit is its refusal. Within the parent.

**LLR-347** (SR-244; TC-386, TC-387, TC-388, TC-389). Link only; the recorded
text is unchanged and clean. IF-245 carries the transcript reader's usage call
(the contract's transcript usage of a run of counted messages); the row's
words stating it: "The transcript reader accepts usage only from assistant
message usage" (`tests/test_claude_transcripts.py::test_each_invocation_usage_is_its_unique_message_sum`,
`::test_the_parents_tool_result_summary_is_never_read`); "orders messages by
first appearance, and takes each message id's last record"
(`::test_a_repeated_record_adds_nothing`); the three finality arms and "A
session's own transcript is never finished by a notice" (TC-388's
`::test_a_message_without_a_stop_record_is_final_once_a_later_message_follows`,
`::test_a_background_agents_task_notice_makes_its_last_message_final`,
`::test_an_agent_with_no_evidence_of_finishing_keeps_its_last_message_open`,
`::test_no_finish_notice_finishes_the_sessions_own_last_message`); "Only a
transcript's last message may remain open; it is named and is neither counted
nor crossed by a cursor" (`::test_an_open_last_message_is_named_and_not_counted`,
`tests/test_usage_ingest.py::test_an_open_message_is_recorded_once_final_and_the_contributions_equal_the_completed_transcript`);
"counted at its last record as partial"
(`::test_a_finished_agents_unstopped_hand_back_is_counted_at_its_last_record`);
"reasoning is empty unless every counted message reports it"
(`::test_each_invocation_usage_is_its_unique_message_sum`); the sum, "the last
non-synthetic counted model", the cli and provider
(`::test_the_response_model_is_the_last_counted_model_not_named_synthetic`,
`tests/test_usage_ingest.py::test_one_ingest_records_four_logs_with_the_usage_vocabulary`).

**LLR-355** (SR-244; TC-389, TC-390, TC-391, TC-394). Link only; the recorded
text is unchanged and clean (its "the stdout form IF-306 declares" names an
interface id, not code). Every clause states the behaviour across the three
interfaces: "accepts an optional session identity and root" (IF-305;
`tests/test_usage_ingest.py::test_the_ambient_session_id_is_ingested_when_none_is_named`,
and every `--session`/`--root` ingest); "recorded, unchanged, open" with "each
invocation's line naming its role, agent type and agent id" (IF-306;
`::test_recorded_unchanged_and_open_lines_name_each_invocations_role_type_and_id`);
"skipped" (`::test_a_service_recorded_session_skips_its_main_transcript`);
"refused" (`::test_a_torn_earlier_log_refuses_that_invocation_naming_it`,
`::test_an_unknown_shape_exits_nonzero_and_records_nothing_for_that_transcript`);
"absent" (`::test_an_absent_transcript_is_named`); "unresolved-parent"
(`::test_an_unresolved_parent_is_named_on_its_agents_lines`); "a transcript
refused for its shape is named by its file and field"
(`::test_an_unknown_shape_exits_nonzero_and_records_nothing_for_that_transcript`
asserts the file name and the field in the refused line); exit zero
(`::test_recorded_unchanged_and_open_lines_name_each_invocations_role_type_and_id`,
`::test_a_service_recorded_session_skips_its_main_transcript`), one on a
refusal, an absence or a refused record commit (IF-307;
`::test_an_unknown_shape_exits_nonzero_and_records_nothing_for_that_transcript`,
`::test_an_absent_transcript_is_named`,
`tests/test_usage_ingest_git.py::test_a_refused_record_commit_exits_one_and_names_the_refusal`),
two with no session (`::test_no_session_is_a_usage_error`).

**LLR-290** (SR-227; TC-303, file level `tests/test_session_keep.py`).
Title and rationale unchanged (clean).
1. "The codex adapter reads compacted entries and per-request input counts from
   the exact thread rollout under the launch CODEX_HOME": kept, the variable
   named as "the codex home the launch environment names";
   `test_codex_reported_rollout_compaction_takes_precedence` (a compacted
   entry), `test_codex_rollout_prompt_drop_labels_inference` (per-request
   counts), `test_codex_unrelated_rollout_cannot_report_compaction` (exactly
   the call's thread), `test_codex_context_and_compaction_receive_same_ambient_environment`
   (the launch environment's home).
2. "or codex's own default home when that is unset": kept ("when it names
   none"); `tests/test_session_adapters.py::test_codex_occupancy_falls_back_to_codexs_default_home`,
   which asserts the compaction prompts are read through the default home,
   now tagged TC-303.
3. "and turn.completed running input totals from exec": kept as "the running
   input totals of the exec stream's completed turns";
   `test_codex_multiple_exec_totals_without_rollout_cannot_infer`,
   `test_codex_multi_request_exec_turn_then_smaller_turn_cannot_infer`, and the
   stored total `test_codex_legacy_record_learns_running_total_before_inference`
   removes (it raises if absent).
4. "Retained bookkeeping records compacted and compaction-source in the call
   row and compacted and compaction_source in the store": kept as "the
   compacted flag and its source in the call's compacted and
   compaction-source columns and in the retained record" (the two column names
   are the session log's printed header keys; the store's key is dropped);
   `test_codex_rollout_prompt_drop_labels_inference` (the call's columns, the
   record's flag, and the written log's `compacted: True` and
   `compaction-source: inferred`), `test_codex_reported_rollout_compaction_takes_precedence`
   (the record's source).
5. "reported for a rollout entry, otherwise inferred from any decrease across
   consecutive new rollout requests, starting with the stored request_prompt
   baseline and the first new request": kept ("the stored latest prompt
   baseline"); `test_codex_reported_rollout_compaction_takes_precedence`,
   `test_codex_scans_every_new_rollout_request_from_stored_baseline`,
   `test_codex_rollout_request_drop_is_inferred_without_reported_entry`,
   `test_codex_equal_prompt_is_not_compaction`.
6. "Only rollout per-request prompts drive inference; without a readable
   rollout there is no new inference, and exec turn sums are retained only as a
   running-total baseline": verbatim; the two exec tests of clause 3.
7. "The rollout request cursor and latest prompt baseline live in the retained
   record, so old requests are not rechecked and a kit reset starts a new
   comparison": verbatim; `test_codex_reported_replaces_inferred_and_holds_on_new_drop`
   (cursor and baseline asserted in the record),
   `test_codex_legacy_rollout_learns_baseline_without_rechecking_old_drop`,
   `test_codex_kit_reset_discards_prompt_comparison`.
8. "a resumed legacy record lacking a rollout cursor first learns the latest
   prompt and cursor before inferring": verbatim;
   `test_codex_legacy_rollout_learns_baseline_without_rechecking_old_drop`,
   `test_codex_legacy_record_learns_running_total_before_inference`.
9. "Reported evidence takes precedence over inferred evidence": verbatim;
   `test_codex_reported_replaces_inferred_and_holds_on_new_drop`.
10. "Once recorded, compacted and its source hold for every later call ...":
    verbatim but "the compacted flag"; `test_codex_inferred_compaction_holds_on_later_rising_requests`.
11. "a reported entry replaces an inferred source, and an inferred drop never
    replaces a reported one": verbatim; `test_codex_reported_replaces_inferred_and_holds_on_new_drop`.
- Added: nothing. The row now states the behaviour across IF-266 (what the
  codex compaction call reads and returns) and the compaction half of IF-247
  (the record carries the flag, source, cursor and baseline) and IF-248 (the
  bookkeeping that folds them). It does not state IF-266's empty answer for
  other runners; no test drives it, so it is left to the form.
- Rule 3: SR-227 asks that a retained session's state and calls be recorded;
  the row is unchanged in meaning.

**LLR-269** (SR-222, SR-227, SR-239, SR-243; TC-265 file level
`tests/test_session_service.py`, TC-351, TC-384). Title and rationale
unchanged (clean).
1. "A role hands a Call its data (root, role, the route's template, model and
   prompt, provider, tier, route id, source event, attempt id, further
   attribution, env, deadlines, console renderer, attached) and nothing else":
   kept, narrowed in form: the list is "including" (the call now also carries
   a retained session, a one-turn bound, a work item, an unretained resume
   thread and an injectable runner, so the recorded list was no longer
   exhaustive), and "nothing else" is "the service owns every launch and
   record step", driven with clause 7. `test_act_launches_through_the_adapter_and_accounts_the_call`
   (the call's data accounted). Reported in section 6, item 6.
2. "act builds the argv (agent_session.build_argv), lets the launched runner's
   adapter prepare it, launches it headless through run_session or attached
   through run_attached, reads the final text through the adapter": kept in
   contract terms; `test_act_launches_through_the_adapter_and_accounts_the_call`
   (the codex adapter's last-message text), `test_a_ctrl_c_in_an_attached_sitting_persists_a_complete_record`
   (attached).
3. "and fills the accounting: invocation id and timestamps, wall seconds, exit
   code and timeout kind, the adapter's usage record with usage-source and
   usage-status (known ..., partial ..., else unavailable), and the latest
   request's session id and context occupancy": kept;
   `test_act_launches_through_the_adapter_and_accounts_the_call` (ids,
   timestamps, known), `test_a_timeout_keeps_partial_usage_and_its_kind`
   (timeout kind, partial), `test_a_failed_spawn_is_accounted_with_unavailable_usage`
   (unavailable, wall seconds), `test_each_call_gets_a_new_invocation_id`
   (session id), `test_call_records_one_log_with_the_usage_record_and_the_raw_stream`
   (occupancy).
4. "a launch that raises is accounted with unavailable usage and re-raised":
   verbatim; `test_a_runner_exception_is_accounted_then_reraised`.
5. "record writes one session log from the caller's row overlaid by that
   accounting, with the whole captured stream as its transcript, the raw stream
   to raw_dir/raw_name when given, and its own telemetry commit": kept, the raw
   file as "the file the caller names when it names one";
   `test_call_records_one_log_with_the_usage_record_and_the_raw_stream`,
   `test_the_worker_record_takes_the_callers_row_and_the_raw_stream_file`.
6. "call is act then record with the standard call_<invocation-id> row,
   recording an interrupted or failed launch too": kept ("the standard call
   row, named for the call's invocation id");
   `test_call_records_one_log_with_the_usage_record_and_the_raw_stream`,
   `test_a_ctrl_c_in_an_attached_sitting_persists_a_complete_record`.
7. "The worker loop (launch_session, then record with the row it composed), the
   hands-on sitting, the route probe and the dual-plan hats (_dp_session) all
   launch through it; nothing else calls run_session, run_attached or the
   session-log writer": kept in contract terms. The writer half:
   `test_only_the_service_writes_a_session_log`. The launch half had no driving
   test (the provider-launch guard catches a process launch of a provider
   argv, not a call of the service's launches):
   `test_only_the_service_calls_the_headless_or_attached_launch` added. The
   roles' routes: TC-384's `tests/test_session_stdin.py::test_an_interactive_sitting_on_the_primary_checkout_spools_its_log`,
   `tests/test_agent_loop_routing.py::test_a_probe_from_the_primary_checkout_spools_its_log_and_commits_nothing`,
   `tests/test_dual_plan_routing.py::test_a_hat_rooted_at_the_primary_checkout_spools_its_log`.
8. "The service identity row accounts every call with session-mode, resumed
   only when its keep resumes a session, and keep-scope, the keep scope or
   empty": narrowed to what the code does, "its session mode, fresh unless its
   retained session resumes one or it resumes an unretained thread" (the
   recorded "only" was contradicted by the row's own clause 14, and the code
   marks either resumed); `tests/test_session_keep.py::test_an_unretained_call_logs_a_fresh_unscoped_session`,
   `::test_two_iteration_rounds_resume_one_review_session` (resumed, scope),
   `test_a_resumed_call_launches_the_resume_form_and_logs_resumed`
   (unretained). Reported in section 6, item 6.
9. "write_session_log records these as audit columns that no gate or scheduler
   reads": kept ("the session log records these"); the header lines
   `tests/test_session_keep.py::test_an_unretained_call_logs_a_fresh_unscoped_session`;
   no test drove "no gate or scheduler reads":
   `test_no_gate_or_scheduler_names_the_session_mode_or_keep_scope_column`
   added.
10. "The record operation commits a log only from a claimed linked worktree,
    including ... close ...; from the shared checkout, a detached checkout, or
    an unclaimed branch, it writes the log to the primary checkout's spool and
    commits nothing": verbatim but "the record step";
    `test_a_call_outside_a_lane_spools_its_log_and_commits_nothing`,
    `tests/test_codex_call_git.py::test_lane_ness_follows_the_written_predicate_and_the_close_first_case`,
    `::test_a_call_outside_a_lane_spools_and_changes_nothing`.
11. "An unreadable claim read adds no claim; it spools only when neither
    readable tree establishes the linked worktree's claim": verbatim;
    `test_an_unreadable_lane_reading_spools`.
12. "A spool write failure raises without a commit": verbatim;
    `test_an_unwritable_spool_raises_and_commits_nothing`.
13. "a refused telemetry commit is reported to the caller": verbatim;
    `test_a_refused_telemetry_commit_is_reported_to_the_caller`.
14. "a non-empty resumed thread identifier is refused with retained-session
    input before accounting": verbatim;
    `test_a_call_with_both_keep_and_resume_is_refused_before_accounting`.
15. "A non-empty unretained resume identifier records the resumed session mode
    without retaining that identifier": verbatim;
    `test_a_resumed_call_launches_the_resume_form_and_logs_resumed` (no
    retained store written).
16. "Standard call-log names remain distinct from gate-log names": verbatim;
    `test_the_standard_call_log_name_is_never_a_gate_log_name`.
- Added (the behaviour across IF-246's call and record signatures): a step
  the caller hands the call step runs with the launch's outcome, or none when
  the launch raised, after the launch and before the log is written,
  `test_call_runs_the_callers_seam_between_act_and_record`; the record step
  hands a caller that asks the log's path, whether it was spooled or
  committed, and the commit's refusal,
  `test_a_call_outside_a_lane_spools_its_log_and_commits_nothing`,
  `test_a_refused_telemetry_commit_is_reported_to_the_caller` (both assert the
  whole report).
- Rule 3: the added clauses decompose SR-243's "record its log without
  committing ... a refused record commit is reported" and "judge the call's
  changes against its starting state" (the caller's step is where the
  coordinator call judges); SR-222's one record. Nothing beyond the parents.

**LLR-305** (SR-227, SR-239; TC-322, TC-323, TC-324, TC-330, TC-362, TC-365).
Title and rationale unchanged (clean).
1. "AdjudicationRequest carries root, brief, the selected route row, work
   item, role, prompt-template overrides and deadline" with the later
   "AdjudicationRequest also carries scope and account": merged into one
   sentence; `tests/test_coordinator_adjudicate.py::test_the_loop_composes_the_same_keep_request_as_before`
   (route, role, brief, scope, account, work item, the overrides' texts, the
   deadline's lease).
2. "Both callers compose that request once": verbatim; the loop,
   `::test_the_loop_composes_the_same_keep_request_as_before`; the
   coordinator, `::test_the_coordinator_route_refuses_a_retained_launch_not_signed_in`
   (its request reaches the shared keep step's sign-in refusal).
3. "adjudication_keep derives governing templates, then plans with the selected
   row": kept ("the shared keep step"); `::test_the_loop_composes_the_same_keep_request_as_before`.
4. "prepare_launch reads no registry: from that row and the selected entry
   account it derives family, template, model, tier, route environment,
   account environment, account home and launch credential": kept ("Launch
   preparation"); `tests/test_adjudicator_token.py::test_a_row_changed_after_selection_launches_the_selected_row`,
   `tests/test_accounts.py::test_two_accounts_of_one_cli_launch_under_two_homes`,
   `::test_a_token_account_home_is_created_empty_and_carries_the_token`.
5. "A token account is signed-in exactly when the file its
   token_file_variable names is present, readable and nonempty; its probe runs
   no command": kept ("its declared token-file variable");
   `tests/test_adjudicator_token.py::test_the_claude_probe_reads_the_token_file_and_runs_nothing`,
   `tests/test_accounts.py::test_the_signin_probe_reads_a_token_account_from_its_file_only`.
6. "A login-account home resolves without being created": verbatim;
   `tests/test_coordinator_adjudicate.py::test_the_probe_resolves_the_home_without_creating_it`.
7. "For a login account home, only documented command-run pairs count: Codex
   accepts exactly one Logged in using <method> line at exit 0 or exactly Not
   logged in at exit 1, apart from blank lines and its PATH-alias warning;
   Claude without a token accepts exactly one JSON object with boolean loggedIn
   true at exit 0 or false at exit 1; another answer, failure or timeout is
   unknown": kept; the codex status command's two printed lines kept as
   observable markers, the JSON key as "its logged-in flag", "PATH-alias" as
   "path-alias"; `::test_the_probe_reports_signed_in_missing_or_unknown`
   (the warning before Not logged in included),
   `::test_an_undocumented_probe_answer_is_unknown`,
   `::test_a_probe_that_fails_or_times_out_reports_unknown`,
   `tests/test_accounts.py::test_the_claude_status_reader_takes_only_its_documented_pairs`.
8. "An absent, unreadable or empty token file refuses before a lease, naming
   the declared variable and the setup step but never its path or value":
   verbatim; `tests/test_adjudicator_token.py::test_a_token_that_cannot_be_read_refuses_before_launch`
   (four arms; the variable named, the path absent, no record),
   `tests/test_accounts.py::test_a_token_account_whose_token_cannot_be_read_is_refused_before_its_home`.
9. "refuse_competing checks every declared account: its route or account
   environment may not declare a credential source ranked above its account
   home": kept ("The competing-credential check covers every declared
   account ... its runner ranks above"); `tests/test_adjudicator_token.py::test_a_route_declaring_a_competing_credential_is_refused_before_launch`,
   `::test_a_route_declaring_the_ambient_value_is_still_refused`,
   `tests/test_accounts.py::test_a_login_account_whose_route_or_account_declares_a_competing_source_is_refused`,
   `::test_a_gemini_login_account_whose_route_declares_a_vertex_source_is_refused`.
10. "a token account also may not declare its token variable": verbatim; no
    test drove it: `test_a_route_declaring_a_competing_credential_is_refused_before_launch`
    gains the token variable as a fourth declared case.
11. "and only a token account's template may not carry --bare": kept ("the
    runner's bare-mode flag"); the token arm `::test_a_route_declaring_a_competing_credential_is_refused_before_launch[--bare]`,
    `::test_keep_warm_with_a_bare_route_is_refused_before_any_lease`; no test
    drove "only" (a login account's template carrying it is not refused):
    `tests/test_accounts.py::test_only_a_token_accounts_template_is_refused_for_the_bare_flag`
    added.
12. "names compare under platform case rules": verbatim;
    `::test_the_name_key_folds_case_on_windows_semantics_only`.
13. "settings-file credential sources are outside this boundary": verbatim. A
    stated bound on clause 9's absolute, not a behaviour: nothing to drive.
14. "compose_env builds the launch environment by removing names the launch
    sets and competing credential names, then applying route pairs, account
    pairs, home and token as the launch's one environment credential": kept
    ("The launch environment is composed by ...");
    `::test_competing_ambient_credentials_never_reach_the_retained_launch`,
    `tests/test_accounts.py::test_a_qualified_login_launch_withholds_every_ambient_credential_its_cli_ranks_above_the_home`,
    `::test_a_token_account_launch_carries_only_its_own_token`.
15. "Prepared carries the template's first token after normal substitution,
    resolved once to an absolute executable on that environment's PATH;
    failure refuses before a lease and names the runner and declared or ambient
    PATH": kept ("the prepared launch", "search path");
    `::test_the_runner_resolves_after_the_template_substitution`,
    `::test_a_runner_not_on_the_launch_path_is_refused_before_any_lease`
    (both arms, no record).
16. "cli_version and the retained launch run that executable": kept ("The
    runner-version probe"); `::test_the_probe_and_the_launch_run_the_one_prepared_executable`.
17. "_as_prepared makes act launch and account the selected row rather than
    caller copies": kept ("the launch step launches and accounts the selected
    row rather than the caller's copies");
    `::test_a_retained_call_launches_its_prepared_route_not_the_callers`.
18. "probe_env composes the prepared environment with the launch credential
    withheld": kept ("The probe environment is ...");
    `::test_the_version_probe_never_receives_the_credential`,
    `::test_the_version_probe_runs_under_the_prepared_environment`.
19. "act redacts each verbatim occurrence of the credential value from physical
    output lines and captured stream before result, usage, logs or records
    consume it": kept ("The launch step"); `::test_an_echoed_token_is_redacted_from_every_sink`,
    `::test_the_token_is_read_at_launch_and_never_logged`.
20. "escaped, encoded and line-split representations are outside that bound":
    verbatim; the stated bound of clause 19, nothing to drive.
21. "For a qualified OpenCode account, the environment starts from its declared
    platform and network-transport base plus kit-owned names, then route
    pairs, account pairs and home, never ambient environment": verbatim but
    articles; `tests/test_accounts.py::test_a_qualified_opencode_launch_starts_from_the_declared_base`,
    `::test_a_qualified_opencode_launch_keeps_the_kit_owned_names`,
    `::test_a_key_declared_for_a_qualified_opencode_launch_is_carried`.
22. "OPENCODE_AUTH_CONTENT is refused": kept ("an OpenCode account declaring
    its auth-content variable is refused");
    `::test_a_qualified_opencode_entry_declaring_its_auth_content_is_refused`.
23. "No registry reread, fallback or automatic sign-in occurs": verbatim;
    `::test_a_row_changed_after_selection_launches_the_selected_row` (no
    reread), `tests/test_coordinator_adjudicate.py::test_the_coordinator_route_refuses_a_retained_launch_not_signed_in`,
    `::test_the_loop_route_refuses_a_retained_launch_not_signed_in` (no
    fallback, no sign-in).
24. "governing_templates receives the request role: for REVIEW it returns the
    once-resolved reviewer template text used by the brief, and for ADJUDICATE
    it keeps the retained-class identity; adjudication_keep passes that role":
    kept ("The governing-template step", "for a review", "for an
    adjudication", "the shared keep step"); `::test_a_retained_reviewers_identity_is_its_own_template`;
    "used by the brief" (one read for both) was driven only under TC-351:
    `tests/test_session_keep.py::test_a_review_rounds_brief_and_identity_share_one_template_read`
    tagged TC-322.
25. "The governing identity of a retained set holding amendment,
    first-acceptance, or combined also covers the act brief, by its wired
    override text when present and otherwise by its shipped text": verbatim;
    `::test_the_identity_covers_the_act_brief_for_an_actable_retained_class`.
- Added: nothing. The text already states IF-282's behaviour (the request,
  preparation, composition, probe environment, competing check, credential,
  sign-in and its refusal).
- Rule 3: no clause's meaning moved; SR-227's credential and sign-in
  refusals and SR-239's shared retention request are what the row
  decomposes.

**LLR-301** (SR-230; TC-318, TC-340; `tests/test_coordinator_guard.py`,
`tests/test_coordinator_guard_e2e.py`, `tests/test_blackout_window.py`).
1. "session_prompt extracts the one fenced session prompt from a handoff,
   preserving headings inside that fence as prompt text": kept, the reading
   named in contract terms; `test_the_session_prompt_is_the_fenced_block_under_its_heading`,
   `test_a_heading_inside_the_prompt_fence_is_prompt_text`.
2. "request_relaunch refuses inside a blackout window": kept;
   `tests/test_blackout_window.py::test_no_relaunch_is_written_inside_the_window`.
   "and otherwise accepts only the lease holder and an existing handoff":
   verbatim; `test_only_the_holder_requests_a_relaunch_naming_a_real_handoff`.
   "then writes a same-session request atomically": verbatim; the request's
   session, `tests/test_coordinator_guard_e2e.py::test_the_guard_cli_takes_requests_releases_and_clears`;
   no test drove "atomically", `test_a_relaunch_request_whose_write_fails_leaves_no_request` added.
3. "The hook's on_blackout SessionEnd dispatch calls blackout_session_end to
   cancel a pending request and record blackout inside a window": kept in
   contract terms ("Inside a blackout window the hook's session-end handling
   cancels a pending request and records blackout");
   `tests/test_blackout_window.py::test_a_pending_relaunch_at_session_end_inside_the_window_is_cancelled`.
4. "otherwise session_end acts only for a true exit by that holder in its
   declared repository": kept ("the session-end handling");
   `test_clear_and_resume_never_launch`, `test_a_non_holders_or_subagents_end_never_launches`,
   `test_an_exit_launches_once_in_the_declared_root_with_the_prompt`. "rejects a
   foreign request": verbatim; `test_a_foreign_request_is_refused_and_reported`.
   "atomically renames one request to acquire it": verbatim;
   `test_two_concurrent_end_handlers_launch_once`. "holds the store lock ...
   so restoration never waits on the lock": verbatim;
   `test_a_failed_launch_restores_while_another_handler_wants_the_lock`.
5. "It writes a fresh successor token ... invokes the platform launcher
   detached in the declared root with that file and token": verbatim;
   `test_an_exit_launches_once_in_the_declared_root_with_the_prompt`,
   `test_the_launcher_runs_detached_in_the_repo_root`,
   `test_the_successor_takes_the_lease_through_pt_coordinator_take`. "and on any
   failure before launch confirmation restores the request and removes the
   successor token and the prompt file": verbatim;
   `test_a_failed_launch_restores_the_request`, `test_a_failed_token_save_restores_the_request`,
   `test_a_failed_prompt_write_restores_the_request`,
   `test_a_launch_failing_with_any_error_restores_the_request`.
6. "launch_command selects the Windows or POSIX launcher; launch_detached
   waits through its grace period and confirms only a still-running launcher
   or one that exits zero": kept ("The launch selects ..., waits ... and
   confirms ..."); `test_the_launcher_runs_detached_in_the_repo_root` (both
   platforms; an exit 0 confirms, an exit 42 refuses),
   `test_a_launcher_that_exits_non_zero_restores_the_request`.
7. "Each launcher enters the declared root": verbatim;
   `tests/test_coordinator_guard_e2e.py::test_the_posix_launcher_runs_claude_in_the_root_with_the_prompt`,
   `::test_the_windows_launcher_runs_the_guards_claude_step_in_the_root`.
   "resolves one interpreter by running its virtual-environment candidate
   followed by the candidates from its dev-setup's ordinary runtime search":
   kept ("development setup's");
   `tests/test_run_devsetup.py::test_each_run_launcher_searches_what_its_dev_setup_searches`
   (both relaunch launchers are in its pairs; tagged). "and takes the first
   that reports Python 3.11 or later as its executable path": verbatim; no
   test drove it, `tests/test_coordinator_guard_e2e.py::test_the_posix_launcher_checks_the_window_on_its_first_floor_interpreter`
   added (a silent sub-floor candidate is passed over for the next that
   reports). "it exits nonzero with guidance when none resolves": verbatim;
   no test drove it, both added launcher tests assert it. "runs window_check
   on that interpreter": kept ("runs the guard's blackout window check on that
   interpreter"); no test drove it, both added launcher tests assert it.
   "exports the token as PT_COORDINATOR_TAKE for the successor's SessionStart
   take": kept ("exports the token in the successor-token variable for the
   successor's session-start take"; the variable's spelling is IF-278's form);
   the two existing launcher tests, the added Windows test (no token during
   the check, the token on the prompt-file step), and
   `test_the_successor_takes_the_lease_through_pt_coordinator_take`. "and
   starts claude with the prompt as one argument: the POSIX one in a new
   terminal, the Windows one through exec_claude, which invokes claude with
   the extracted prompt": kept ("the agent command-line tool", "the guard's
   prompt-file step"); the existing POSIX inner-step test and the added POSIX
   test (a passing check opens a new terminal running the inner step),
   `test_the_windows_launcher_runs_the_guards_claude_step_in_the_root`,
   `test_exec_claude_passes_the_prompt_as_one_argument`.
8. "main dispatches the guard operations": kept ("The guard's command line
   dispatches the guard operations");
   `tests/test_coordinator_guard_e2e.py::test_the_guard_cli_takes_requests_releases_and_clears`,
   `test_the_hand_back_command_line_maps_its_result_to_the_exit_code`.
   "reopening a session with the context latch still set needs the operator
   recorded clear": verbatim;
   `tests/test_blackout_window.py::test_reopening_the_same_session_with_both_drains_needs_the_operators_clear`
   (tagged).
- Added: "starting nothing when it refuses" (the window check), both added
  launcher tests. The command line's exits: "the lease take, release, clear,
  relaunch request, hand-back and status operations exit 0 when they succeed,
  and one that refuses prints its reason on standard error after the guard's
  own prefix and exits 1; a usage error exits 2, and the hook operation exits
  0 whatever it reads": `test_the_guard_cli_takes_requests_releases_and_clears`
  (take 0 and a refused take 1 with the prefix; relaunch request 1 for another
  session and 0 for the holder; clear 0, and 1 with nothing held; status 0;
  release without a reason 2, with one 0),
  `test_the_hand_back_command_line_maps_its_result_to_the_exit_code` (1 with
  the prefix, then 0), `tests/test_coordinator_guard_e2e.py::test_the_hook_cli_reads_stdin_and_prints_its_output`
  (0 for a parsed event and for an unparsable one). The window check's and
  the hooks report's exits are not restated (LLR-300 states the window
  check's; section 6, item 8).
- Rationale unchanged (no code name).
- Rule 3: SR-230's request, acquisition, launch and blackout cancellation are
  what clauses 1 to 7 decompose; "starting nothing when it refuses"
  decomposes SR-230's "Inside the window, no relaunch is requested or
  launched". Round 1: the exit sentence's lease take, release, clear and
  status operations serve SR-229, which the requirements cell now names
  beside SR-230 (section 7); no row under SR-229 this slice may touch states
  those operations (LLR-300 is WI-1071's, LLR-423 states the caller alone).

**LLR-306** (SR-227, SR-231, SR-209; TC-321, TC-365;
`tests/test_coordinator_adjudicate.py`, `tests/test_coordinator_act.py`,
`tests/test_accounts.py`). Three code names scrubbed; every clause kept.
1. "ENTRY. coordinator_adjudicate runs only from a claimed lane worktree and
   otherwise refuses before launch through IF-284": kept ("The coordinator's
   adjudication entry point"); `test_a_primary_checkout_root_is_refused_before_launch`,
   `test_a_worktree_whose_branch_holds_no_claim_is_refused`,
   `test_a_root_outside_any_repository_is_refused`.
2. "It also refuses an unusable route, invalid account, registry error, or
   unreadable or undecodable brief through that interface": verbatim;
   `test_an_unknown_route_or_one_off_the_enable_list_is_refused`,
   `tests/test_accounts.py::test_the_adjudicator_refuses_a_registry_error_an_undeclared_account_or_an_unreadable_list`,
   `test_an_undecodable_brief_is_refused_with_the_usage_exit`; no test drove
   the unreadable half, an assertion added to that test (a missing brief file
   exits 2 naming it).
3. "its sign-in reading identifies the adjudicator entry's account":
   verbatim; `tests/test_accounts.py::test_the_signin_probe_reads_a_token_account_from_its_file_only`,
   `::test_the_signin_probe_reads_a_login_account_from_its_own_home`,
   `::test_the_signin_probe_names_an_ambient_or_unresolved_entry`.
4. "As its last pre-launch checks it creates the verdict path's missing
   parent directories and then the path itself, empty and exclusively":
   verbatim; `test_a_verdict_path_under_a_missing_directory_is_reserved_and_launches`,
   `test_a_call_whose_session_writes_into_its_reservation_succeeds`,
   `test_two_calls_naming_one_verdict_path_never_share_its_verdict`.
5. "and creates its requested-kinds binding beside it exclusively, so an
   existing or concurrently reserved path or binding, or one whose parent
   cannot be created, also refuses": verbatim;
   `test_a_failed_call_reusing_a_verdict_path_does_not_return_success`
   (existing path), `test_two_calls_naming_one_verdict_path_never_share_its_verdict`
   (concurrent), `test_a_verdict_path_that_cannot_be_reserved_is_refused`
   (parent); the binding half `tests/test_done_when_blessing.py::test_the_entry_point_binds_the_requested_kinds_beside_the_verdict`
   and `::test_a_refused_reservation_leaves_a_binding_it_does_not_own` (both
   tagged).
6. "its exclusive binding is made through the shared bind_pending request
   binder": kept ("the shared request binder"); the entry point's binding
   carries what the shared binder writes, the findings-file record,
   `test_a_dispute_binding_records_its_findings_file_through_the_outcome`
   (tagged), and the requested kinds,
   `tests/test_done_when_blessing.py::test_the_entry_point_binds_the_requested_kinds_beside_the_verdict`.
7. "a pre-launch refusal removes only the reservation and binding this call
   created and leaves any directory it created": verbatim;
   `test_a_call_refused_before_launch_releases_its_reservation`,
   `tests/test_done_when_blessing.py::test_a_refused_reservation_leaves_a_binding_it_does_not_own`;
   no test drove "leaves any directory it created", assertions added to the
   first (a refused reservation under a new directory is removed with its
   binding, and the directory stays).
8. "Otherwise it composes the shared request, plans the keep, launches and
   records an ADJUDICATE call with coordinator attribution": kept ("an
   adjudication call"); `test_the_coordinator_route_writes_one_session_log_per_call`,
   `test_a_second_coordinator_adjudication_resumes_the_first`,
   `test_a_session_at_the_dial_drains_and_retires_at_the_next_clear_point`.
9. "then validates the verdict and records accepted only when that
   validation and a successful call - exit 0, in deadline, and no reported
   error result - both hold, otherwise failed": verbatim;
   `test_a_call_whose_session_writes_into_its_reservation_succeeds`,
   `test_a_missing_or_malformed_verdict_is_reported_and_fails`,
   `test_a_nonzero_exit_or_a_timeout_fails_whatever_file_exists`; the
   reported error result, `tests/test_done_when_blessing.py::test_a_call_reporting_an_error_is_failed_on_both_routes`
   (tagged).
10. "and commits that binding in its own telemetry commit": verbatim; no test
    drove it (this module's fixture stubs the commit),
    `tests/test_done_when_blessing.py::test_the_entry_point_commits_its_recorded_binding_in_its_own_telemetry_commit`
    added.
11. "and prints the IF-285 reading": restated in round 1 as the reading it
    prints: the call's retention (a fresh session, a retained session minted
    or one resumed) and its exit, then, for a successful call, the verdict
    with its validity or that it wrote none, and, for a failed call, that its
    verdict is not read; `test_the_adjudicate_reading_names_the_keep_the_exit_and_the_verdict`
    (new), with `test_a_missing_or_malformed_verdict_is_reported_and_fails`,
    `test_two_calls_naming_one_verdict_path_never_share_its_verdict`,
    `test_a_failed_call_reusing_a_verdict_path_does_not_return_success`.
12. "A non-zero exit, timeout or reported error result returns the
    failed-call outcome through IF-284 without reading the verdict":
    verbatim; `test_a_nonzero_exit_or_a_timeout_fails_whatever_file_exists`
    (a valid verdict on file, exit 1, never read as valid), and the error
    result as in 9.
13. "after a successful call, an empty reservation is a missing verdict
    recorded failed": verbatim; `test_two_calls_naming_one_verdict_path_never_share_its_verdict`.
14. "A launched call leaves its verdict file, empty or written, for
    inspection": verbatim; the same test (empty) and
    `test_a_verdict_path_under_a_missing_directory_is_reserved_and_launches` (written).
15. "The adjudicator act turn runs under the resolved entry's declared
    account, the same account as its judging turn, so a retained act
    continues that session": verbatim;
    `tests/test_coordinator_act.py::test_an_act_turn_on_the_default_entry_launches_under_its_accounts_environment`,
    `::test_an_act_turn_resumes_the_session_its_sitting_keyed_under_the_entrys_account`.
16. "The default route and every command outcome are declared by IF-283 and
    IF-284": verbatim; `test_the_shipped_entry_point_defaults_to_the_strong_anthropic_route`,
    `test_the_adjudicator_resolves_its_enabled_entry`, and the exit tests above.
17. "and the command also exposes a sign-in reading": verbatim;
    `tests/test_run_devsetup.py::test_the_sign_in_is_reported_signed_in_missing_or_off`,
    `tests/test_accounts.py::test_the_signin_probe_names_an_ambient_or_unresolved_entry`.
18. "An act invocation from a claimed clean lane derives a complete
    later-turn brief ... without reserving a verdict or recording an
    outcome": verbatim; `tests/test_coordinator_act.py::test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict`,
    `::test_the_act_turn_writes_no_binding_and_reserves_no_path`.
19. "It refuses before launch for a lane, route, uncommitted lane change, or
    act-derivation refusal, naming the relevant input": verbatim;
    `::test_the_act_command_refuses_each_trust_input_before_launch`.
20. "it succeeds only after a successful call leaves no authorized act owed
    and no changed verdict record, otherwise fails": verbatim;
    `::test_the_act_turn_reports_success_only_when_no_listed_act_is_left`,
    `::test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed`.
21. "and a sign-in refusal reports its distinct result": verbatim; no test
    drove the act turn's, `tests/test_coordinator_act.py::test_a_retained_act_turn_whose_account_is_not_signed_in_is_refused_apart`
    added.
22. "Under the loop marker, each prompt it launches ends with loop
    provenance after its binding is read": verbatim;
    `::test_under_the_loop_marker_every_launched_prompt_ends_with_the_loop_session_line`,
    `::test_without_the_marker_no_prompt_carries_the_line`.
23. "The fresh verdict reservation, validation, and deadline conditions
    above apply to the judging turn; the act turn instead uses the later
    completion conditions stated here": verbatim (the scope of 4 to 14 and 18
    to 21); `::test_the_act_turn_writes_no_binding_and_reserves_no_path`.
- Added (round 1): the act turn "prints the call's retention and exit, then
  the acts still owed after the call and the review records the call
  changed, or that the act is complete";
  `tests/test_coordinator_act.py::test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict`
  (a fresh session and a minted one, the exit, asserted in round 1, and
  completion), `::test_an_act_turn_resumes_the_session_its_sitting_keyed_under_the_entrys_account`
  (a resumed one), `::test_the_act_turn_reports_success_only_when_no_listed_act_is_left`
  and `::test_an_act_turn_that_leaves_a_waiting_flip_owes_it_and_does_not_read_complete`
  (the acts still owed), `::test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed`
  (the changed review records).
- Rationale (round 1): its sentence "IF-283, IF-284 and IF-285 each own the
  command contract they expose; copying those contracts here was rejected
  because two homes for the same route or exit condition would drift" now
  reads "The command's interfaces state its form, its default route and its
  exit codes, and this row states the behaviour a caller observes across
  them: the refusals, the recorded outcome and the reading it prints", which
  is what the `constrains` cell beside it asserts. The rest is unchanged.
- Rule 3: no meaning moved; SR-231's lane admission, exclusive reservation,
  in-deadline success and act-turn conditions, SR-227's sign-in and SR-209's
  provenance are what the clauses decompose.

**LLR-310** (SR-232; TC-327, TC-331, TC-368; `tests/test_done_when_blessing.py`,
`tests/test_adjudicate_brief.py`, `tests/test_integrate_admission.py`,
`tests/test_adjudicate_act.py`, `tests/test_coordinator_adjudicate.py`). Seven
code names scrubbed; every clause kept.
1. "A combined class accepts only amendment:<id>, first-acceptance:<id> and
   done-when:<id> Adjudicates tokens": verbatim (scope tokens of the
   Adjudicates cell); `tests/test_integrate_admission.py::test_a_combined_row_with_only_malformed_tokens_is_refused`,
   `test_a_combined_rows_tokens_scope_each_kinds_act`.
2. "it composes each named class through compose with that section's
   verdict path in fixed amendment, first-acceptance, done-when order": kept
   ("the shared brief composer"); `test_a_combined_sitting_composes_each_kind_from_its_own_brief`,
   `test_the_coordinator_reads_the_requested_kinds_from_the_composed_brief`.
3. "and refuses whole if any section cannot compose": verbatim;
   `test_a_combined_sitting_refuses_whole_when_a_section_cannot_compose`.
4. "One parser reads machine lines one physical line at a time ... a bare,
   split, bad-label or field-missing line invalidates": verbatim;
   `test_a_malformed_machine_line_invalidates_the_verdict`,
   `test_the_done_when_verdict_grammar`,
   `tests/test_adjudicate_brief.py::test_an_unusable_verdict_is_refused_and_says_which_way`.
5. "The same module's review_line is the one reader of a review VERDICT
   line: exactly one case-insensitive VERDICT keyword line is accepted only
   as `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`; the filing
   boundary refuses every other form and the merge reader treats it as no
   verdict": kept ("The same grammar's review-line reader"; the line form is
   an output marker); the drivers were LLR-046's and the review-brief rows'
   tests, none named by LLR-310's cases:
   `tests/test_adjudicate_brief.py::test_the_one_review_line_reader_takes_only_the_exact_form`
   added (both labels taken; another case of the keyword, a label outside
   the pair, a non-digit count, more on the line, and two lines each
   refused by the reader, by the filing boundary and read as no verdict by
   the merge gate's round reader).
6. "A combined sitting names exactly the kinds bound at reservation in
   <verdict>.requested, has exactly one kind-form lower-case section per
   bound kind and none other, and has across the whole file exactly one
   complete line per bound kind and one SITTING line, and no line for
   another kind": kept ("the requested-kinds binding beside its verdict");
   `test_a_combined_verdict_must_judge_exactly_the_kinds_its_sitting_requested`,
   `test_an_unrequested_section_refuses_the_combined_verdict`,
   `test_a_combined_verdict_is_parsed_section_by_section`,
   `test_a_machine_keyword_outside_every_section_invalidates_a_sitting`.
7. "a single-kind verdict has no kind-form section and exactly one complete
   line for its kind": verbatim; the one-line half,
   `test_a_malformed_machine_line_invalidates_the_verdict`; no test drove the
   no-section half, `tests/test_adjudicate_brief.py::test_a_single_kind_verdict_carries_no_kind_section`
   added.
8. "One binding records pending before either route calls: the coordinator
   entry point binds the request exclusively at reservation, and the loop
   binds its composed request at composition": verbatim;
   `test_the_entry_point_binds_the_requested_kinds_beside_the_verdict`,
   `test_the_loop_route_takes_a_combined_sitting_on_its_bound_kinds`, and the
   added `tests/test_adjudicate_brief.py::test_the_loops_binding_carries_its_findings_file_and_identities_through_the_outcome`.
9. "write_binding is its one writer and record_outcome its one route
   recorder and commit path, returning its `(outcome, why)` decision and
   recording accepted only when call_succeeded has derived exit 0, no timeout
   and no reported error result, and validation passes": kept ("the binding
   writer", "the outcome recorder", "its outcome with the reason for it",
   "the shared call-success derivation has found");
   `test_a_failed_call_is_recorded_failed_without_reading_its_verdict` (the
   outcome and reason returned), `test_a_call_reporting_an_error_is_failed_on_both_routes`
   (tagged: exit, timeout and error result), the bindings both routes write
   read back by the one reader in the tests of 8; the commit path, no test
   drove it, `test_the_entry_point_commits_its_recorded_binding_in_its_own_telemetry_commit` added.
10. "A dispute binding also records the findings file its composed brief
    names. It is written by the one writer in the same call as the requested
    ids, on either route": verbatim; the coordinator's route,
    `tests/test_coordinator_adjudicate.py::test_a_dispute_binding_records_its_findings_file_through_the_outcome`;
    no test drove the loop's route, the added carried-cells test.
11. "The outcome rewrite carries it unchanged, as it carries the identity
    cell": verbatim; the findings file, the same two tests; the identity
    cell had only LLR-359's test case driving it, the added carried-cells
    test asserts it.
12. "A brief that names none binds none, which every reader reads as
    absent": verbatim; `test_a_dispute_binding_records_its_findings_file_through_the_outcome`,
    the added carried-cells test.
13. "call_succeeded is derived once and shared by both routes": kept ("The
    call-success derivation is made once ..."); `test_a_call_reporting_an_error_is_failed_on_both_routes` (tagged).
14. "a failed call is recorded failed without its verdict being read":
    verbatim; `test_a_failed_call_is_recorded_failed_without_reading_its_verdict`.
15. "and the loop consumes that same why as its completion obligation": kept
    ("that same reason"); `test_a_failed_loop_call_keeps_its_obligation_and_reads_no_verdict` (tagged).
16. "The coordinator validates its pending binding before recording its
    outcome, while the loop records against the kinds read back from its
    bound request": verbatim; `test_the_coordinator_reads_the_requested_kinds_from_the_composed_brief`,
    `test_the_loop_route_takes_a_combined_sitting_on_its_bound_kinds`.
17. "later consumers use the recorded-verdict reader, which returns only an
    accepted, bound, valid verdict and each part's row rulings": verbatim;
    `test_a_combined_verdicts_done_when_section_is_acted_on`,
    `tests/test_integrate_admission.py::test_an_in_lane_act_whose_verdict_failed_is_refused`,
    `tests/test_adjudicate_act.py::test_each_unrecorded_or_unreadable_verdict_is_refused_naming_why`.
18. "Every row an adjudication merge act flips needs an ACCEPT ruling ... and
    a named verdict must authorize each row its act re-accepts in the same
    way": verbatim; `tests/test_integrate_admission.py::test_an_in_lane_act_backed_by_a_recorded_verdict_merges_at_the_slot`,
    `::test_an_in_lane_act_with_no_verdict_is_refused`,
    `::test_an_in_lane_act_whose_verdict_judged_other_rows_is_refused`,
    `::test_an_unbacked_ledger_only_acceptance_is_refused_by_name`.
19. "Failed, pending, unbound or other-class verdicts cover nothing":
    verbatim; `tests/test_adjudicate_act.py::test_each_unrecorded_or_unreadable_verdict_is_refused_naming_why`
    (unbound, pending, failed; a Done-when and a disposition verdict owe no
    act), `tests/test_integrate_admission.py::test_an_in_lane_act_whose_verdict_failed_is_refused`.
20. "Ordinary and mixed lanes consume the same claimed-row reader at the
    merge ...": verbatim; `tests/test_integrate_admission.py::test_a_mixed_lane_keeps_its_adjudication_rows_scope`,
    `::test_the_route_and_the_merge_read_one_scope_cell_alike`,
    `::test_a_brief_spelled_unlike_its_kind_still_bounds_the_lane`,
    `::test_a_ledger_only_acceptance_outside_the_scope_is_refused`,
    `::test_a_backed_ledger_only_acceptance_on_an_ordinary_lane_is_admitted`.
21. "Token and section parsing are shared by composition, validation, act
    scopes and merge-time minting": verbatim; `test_a_combined_rows_tokens_scope_each_kinds_act`,
    `tests/test_integrate_admission.py::test_the_route_and_the_merge_read_one_scope_cell_alike`,
    `test_at_merge_a_combined_successor_mints_the_done_when_sections_own_draft` (tagged).
22. "the class is routed and retainable through BRIEF_PROMPTS": kept ("the
    declared brief-prompt table"); `test_both_new_classes_are_accepted_by_the_coordinator_entry_point`,
    `test_this_repo_retains_both_new_classes`.
23. "An amendment verdict's `- [MEANING+BLESS]` row tag reads MEANING to every
    rulings reader, and a dedicated reader returns only rows so marked ...":
    verbatim (the tag is an output marker); `tests/test_adjudicate_act.py::test_a_MEANING_BLESS_row_reads_MEANING_and_blessed`,
    `::test_an_unmarked_MEANING_row_is_not_blessed`, `::test_a_row_tagged_both_ways_is_not_blessed`.
24. "One reader of the rows a recorded verdict authorizes, a MEANING row only
    when so marked, serves both the merge and the act assembler": verbatim;
    `::test_the_bless_mark_has_one_reader_shared_by_the_merge_and_the_act`,
    `::test_judged_rows_admits_an_amendment_MEANING_row_only_with_its_bless_mark`.
- Rationale unchanged (no code name).
- Rule 3: no meaning moved; SR-232 asks for one sitting preserving each kind's
  scope, evidence and grammar, refused when a section is missing, extra,
  repeated or invalid, which clauses 1 to 7 decompose; the binding, recorder
  and reader clauses carry the scope through to the act and the merge.

**LLR-316** (SR-237; TC-335; `tests/test_blackout_window.py`).
1. "blackout_at is the sole reader of the declared blackout value": kept ("The
   blackout reading"); `test_the_window_function_is_the_only_reader_of_the_dial`.
2. "At a supplied or current UTC instant it returns the declared value,
   whether the instant is inside an enabled interval, that interval's
   exclusive end, and the most recent interval end at or before the
   instant": verbatim; `test_the_end_minute_is_exclusive_and_the_last_end_inclusive`,
   `test_a_disabled_window_answers_neither_question` (the declared value
   returned); no test of this case drove the current-instant arm,
   `test_with_no_instant_given_the_reading_is_taken_now` added.
3. "It treats absent, malformed and equal endpoints as disabled": verbatim;
   `test_a_disabled_window_answers_neither_question` (empty, equal, garbage,
   out of range); no test drove an absent declaration,
   `test_an_absent_window_answers_neither_question` added (no key, no file).
4. "starts intervals only on weekdays": verbatim;
   `test_a_sunday_night_window_does_not_exist`.
5. "and assigns a midnight-wrapping interval to its start weekday": verbatim;
   `test_a_friday_night_window_runs_into_saturday`.
- Title and rationale unchanged. Rule 3: SR-237's "the end is exclusive, a
  wrapping interval belongs to its weekday start", unchanged meaning.

**LLR-338** (SR-231, SR-232; TC-368; `tests/test_adjudicate_act.py`). A link
only, the recorded text verbatim (it carries no code name). It states the
behaviour across IF-296's surface: "the act assembler derives every
authorized act that the revision's committed registries and records do not
carry in full" (the owed-acts call; `test_a_held_rung_CLARITY_row_is_reaccepted_naming_its_verdict`,
`test_a_combined_verdict_lists_the_amendment_act_before_the_first_acceptance_act`);
"any unrecognized state or unmatched tier refuses the whole derivation naming
the row" and "An uncommitted, unbound, non-accepted or invalid verdict ...
refuses the whole derivation naming why" (its refusal arm;
`test_each_unrecorded_or_unreadable_verdict_is_refused_naming_why`,
`test_a_ruled_row_no_compared_tier_holds_is_refused_naming_it`); "their brief
is filled in full or not at all" (the act brief's composition;
`test_the_composed_act_brief_names_its_verdict_and_trailer`); "the later-act
derivation reports the acts a verdict still owes, marking each waiting flip
... or its refusal, and reports no outstanding act only when every authorized
act is taken" (the left-owed call; `test_the_later_act_derivation_reports_a_waiting_flip_as_owed_and_marked_never_taken`,
`test_a_completed_act_owes_none_and_is_refused`); "It identifies the retained
class from an accepted actable verdict binding" (the bound-brief call;
`tests/test_coordinator_act.py::test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict`
is TC-321's, so file-level here through TC-368's act tests); "A re-accept of a
row absent from the committed registries is a retirement" (the retires part;
`test_a_retired_row_ruled_CLARITY_beside_a_first_acceptance_is_listed_in_the_reaccepts`,
`test_a_retirement_on_a_held_rung_owes_no_act`); the waiting flips and the
all-waiting refusal (`test_a_flip_under_a_returned_parent_waits_and_the_listed_flips_pass_the_parent_first_check`,
`test_a_verdict_whose_only_remaining_act_waits_is_refused_naming_each_row_and_parent`).
IF-296 also lists the held-text identity refusal, which LLR-359 states
(WI-1070's row, untouched); LLR-338 does not, and needs not for the link.

## 5. Acts owed to sittings C1 and C2

Amended accepted rows keep `Accepted` and show as drift; "routed" marks the
`constrains` cell, a routed traced change. Every design row below amends
`detail` alone where it amends text.

**Sitting C1**

| Row | Accepted cells amended | Routed traced change |
|---|---|---|
| LLR-028 | `detail` | `constrains` IF-015 |
| LLR-031 | none | `constrains` IF-037, beside slice 2's IF-298 |
| LLR-040 | `detail` (one sentence) | `constrains` IF-038, beside slice 2's four |
| LLR-044 | `detail` | `constrains` IF-045, IF-162 |
| LLR-047 | none | `constrains` IF-049, beside slice 1's three |
| LLR-056 | `detail` | `constrains` IF-093, IF-094 |
| LLR-058 | `detail` | `constrains` IF-071, IF-085, IF-171, IF-172 |
| LLR-075 | `detail` | `constrains` IF-163 |
| LLR-137 | `detail` | `constrains` IF-081, IF-155, IF-156, IF-168; `sr_refs` gains SR-173 (round 1) |
| LLR-280 | `detail` | `constrains` IF-253 |
| LLR-288 | none | `constrains` IF-264 |
| LLR-140 | `detail` | `constrains` IF-080, IF-154 |
| LLR-151 | `detail` | `constrains` IF-186 |
| LLR-207 | `detail` | `constrains` IF-175 |
| LLR-247 | none | `constrains` IF-194, beside slice 2's IF-197 |
| LLR-259 | `detail` | `constrains` IF-224 |
| LLR-262 | `detail` | `constrains` IF-242 |
| LLR-307 | `detail` | `constrains` IF-286, IF-326 |
| LLR-339 | `detail` (round 1) | `constrains` IF-179, IF-189 |
| LLR-340 | `detail` (one phrase) | `constrains` IF-297 |
| LLR-014 | `detail` | none (its slice-2 `constrains` IF-004, IF-147, IF-167 stays owed with it) |
| TC-014 | `method`, `expected` | none |
| TC-028 | `method`, `expected` (round 1) | none (its `evidence` gains the other codes' tests, traced) |

23 rows: 21 design rows (20 with a routed `constrains` change, one with a
routed `sr_refs` change, 17 with `detail` amended, four link only) and two
test cases. LLR-014 is the ninth sitting's
MEANING row, owed until its answer (section 8) is judged; TC-014 is amended
with it.

**Sitting C2**

| Row | Accepted cells amended | Routed traced change |
|---|---|---|
| LLR-046 | `detail` | `constrains` IF-046, IF-047, IF-160 |
| LLR-313 | `detail` | `constrains` IF-288, IF-289 |
| LLR-314 | `detail` | `constrains` IF-290, IF-322 |
| LLR-367 | none | `constrains` IF-309 |
| LLR-337 | `detail` (one sentence appended) | `constrains` IF-295 |
| LLR-254 | `detail` | `constrains` IF-228 |
| LLR-255 | `detail` | `constrains` IF-229 |
| LLR-264 | `detail` | `constrains` IF-243 |
| LLR-265 | `detail` | `constrains` IF-244 |
| LLR-293 | `detail` | `constrains` IF-269 |
| LLR-294 | `detail` | `constrains` IF-269 |
| LLR-162 | `detail` | `constrains` IF-098 |
| LLR-283 | `detail` | `constrains` IF-255, IF-256 |
| LLR-335 | none | `constrains` IF-294 |
| LLR-345 | `detail` | `constrains` IF-303, IF-304 |
| LLR-347 | none | `constrains` IF-245 |
| LLR-355 | none | `constrains` IF-305, IF-306, IF-307 |
| LLR-290 | `detail` | `constrains` IF-247, IF-248, IF-266 |
| LLR-269 | `detail` | `constrains` IF-246 |
| LLR-305 | `detail` | `constrains` IF-282 |
| LLR-301 | `detail` | `constrains` IF-278, IF-279, IF-280, IF-281; `sr_refs` gains SR-229 (round 1) |
| LLR-306 | `detail`, `rationale` (round 1) | `constrains` IF-283, IF-284, IF-285, IF-321 |
| LLR-310 | `detail` | `constrains` IF-115, IF-287 |
| LLR-316 | `detail` | `constrains` IF-291 |
| LLR-338 | none | `constrains` IF-296 |

25 design rows, 25 routed `constrains` changes and one routed `sr_refs`
change, 20 with `detail` amended (LLR-306 its `rationale` too), five link
only.

**No new `Drafted` row** is owed a first acceptance. The 25 test cases whose
`evidence` gained tests (section 2) changed a traced cell only: no act owed.

Both sittings' total: 48 rows (46 design rows and two test cases), each new to
its sitting.

## 6. For the coordinator, before slice 4

1. **IF-049 is linked to LLR-047** (slice 2's item, as the brief's 2a set it).
   LLR-047 as WI-1071 restored it states the run section's form: the section
   read into name, command and description in declaration order, with no
   interpolation, each name's case kept, a description row attached to its
   command and an orphan description or an empty command dropped (section 4,
   C1). A routed change on a row the ninth sitting re-accepted, owed to C1.
2. **IF-144, measured; a proposal, nothing built** (slice 2's item, as the
   brief's 2b set it). A read-only pass over the worktree, its drivers kept
   outside the repository, measured what slice 2's section 6 asked:
   - (a) **The checkers claiming the protocol are 18, not the 14 IF-144's
     notes count**: the 17 `check_*` scripts and the traceability check. The
     notes' figures come from the OI-64 checker-uniformity census at
     `fc8a0edc` (2026-08-25); four checkers have shipped since (the
     complexity census, the test-first and readability reports, the
     assumption gate). No checker cites IF-144; only the harness's contract
     comment states it. The four dispositions are spelled with thirteen labels
     in the census's own table (its text says twelve): passed `OK`, `clean`;
     not applicable `SKIP`, `skipped`; advisory `WARN`, `WARNING (advisory)`,
     `ADVISORY`, `UNTRACED`, `note`, `hint`; gate `FAIL`, `ERROR`,
     `FINDING (<class>)`. All are still printed.
   - (b) **Per part, whether a census test over the 18 can drive it on every
     one:**
     1. *A finding names its location unless population-level*: **no**. One
        planted finding per checker exercises one of about 158 emission
        sites; a test of every site needs a fixture per site, or a static scan
        with a hand-kept exception list, which is a ratchet, not a drive.
        Only the readability report enforces a location mechanically. The
        six thin sites the census named are still there (in the flows check,
        the trajectory check twice, the seam check, the documents check
        twice), two of which read as located (a module pair; an SN id).
     2. *A finding carries one of the four severities*: **only by freezing the
        spellings**, which IF-144's rationale declines to fix. The label does
        not reliably match the outcome: the reference and figure checks
        print `WARN` under their strict flag and exit 1; the complexity
        census prints `FAIL` in its default warn mode and exits 0 (read in
        the code: its failure lines print, and it returns 1 only in its
        enforce mode); the traceability check prints `FINDING (...)` and
        exits 0 without strict; the privacy scan's findings carry no severity
        word.
     3. *An advisory never reaches the exit code; a declared strict flag is
        the only promotion*: **partly**. One planted advisory per checker
        drives the class planted, not every class; it is vacuous for the
        coverage, flows and privacy checks, which have no advisory class; and
        the assumption gate, readability report and budget comparator promote
        through configuration or a per-row gate cell, not a flag. Each
        checker's own tests already drive its promotion.
     4. *An absent optional input exits 0 and names the absence*: **yes, and
        cheaply**: an empty directory and a table of 18 command lines and the
        phrase each prints. 14 of the 18 already have a test asserting their
        absence message (by a grep of the test modules, not a run).
   - (c) **What a census test would fail on today.** Carve-outs the code
     argues: the flows check fails on an absent runtime-flows document (the
     document is what it checks, required from DevStg-Tests); the traceability
     check fails without the id watermark ("fails loud", and the scaffold
     writes one); the privacy scan's staged, range, message and author modes
     exit 2 outside git (never a clean verdict over nothing; its repository
     sweep, which the harness runs, exits 0); the test-first report fails on
     unreadable history only under its strict flag, which the harness never
     passes. Defects, each cheap: the complexity census does not name an
     absent baseline (it prints a cognitive change from none) and prints
     `FAIL` in warn mode; the assumption gate names its setting but not the
     absent registries.
   - **Proposal:** a new design row with a census test, narrowed to parts 3
     and 4, over every `check_*` script and the traceability check found by
     glob (so a new checker joins by default), with a three-entry carve-out
     table (the flows document, the id watermark, the privacy scan's
     git-only modes); and IF-144 amended to state parts 1 and 2 as judged at
     review rather than tested, its notes corrected from 14 checkers to 18.
     Retiring the row would drop the two parts a test can hold cheaply, one
     of which (part 4) has already drifted in the complexity census. The two
     complexity-census defects would be the census test's red, fixed in the
     same row. Not built; the coordinator's call.
   - **The coordinator's answer (review round 1):** IF-144 becomes WI-1075,
     filed on trunk at `e12781779`. Nothing is built for it here.
3. **Carried, LLR-300 the only row: IF-271, IF-274, IF-275** (the claim
   refusal call, the hook event read from standard input, the hook's JSON
   answer). Every behaviour across them is LLR-300's (the claim refusal's
   window-first order and lease ownership, the hook events it reads, the
   denials and injected instructions). LLR-322 states only the hooks'
   installation state and LLR-301 only the session-end handling; LLR-140
   states the integrator's side of the claim refusal but omits the blackout
   refusal that runs at every dial, so it is not a clean row for IF-271 as
   worded. LLR-300 is WI-1071's and this slice may not touch it, and a
   focused row beside it is barred by answer 2, so nothing was built. Each
   stays reached through its naming test cases (TC-316, TC-317, TC-339).
   For LLR-300's next amendment: no row states IF-274's "input that does not
   parse is reported on standard error and answered with nothing" (driven by
   `tests/test_coordinator_guard_e2e.py::test_the_hook_cli_reads_stdin_and_prints_its_output`).
   **The coordinator's answer (review round 1):** the three stay reached
   through their naming test cases, and IF-274's unstated parse failure goes
   to LLR-300's next amendment.
4. **Carried, LLR-270 the only row: IF-272, IF-273** (the primary checkout's
   output directory, the keep store's directory lock and its busy refusal).
   LLR-270 resolves the directory from the git common directory and names the
   lock, its stale time and its busy refusal; no other row states them, so a
   focused row would restate LLR-270's clauses (answer 2). Rewriting LLR-270
   under rule 1 is about 11,400 characters of `detail` and 1,500 of
   `rationale`, about 80 code-shaped tokens, about 70 clauses to account and
   eight test cases (TC-266, TC-267, TC-268, TC-322, TC-329, TC-341, TC-351,
   TC-364): one row the size of a sitting's quarter. Held, not built, for the
   coordinator: (a) rewrite LLR-270 in slice 4 (or its own row) and link
   IF-247, IF-248, IF-272 and IF-273 there; or (b) leave the two reached
   through their naming cases (TC-317; TC-267, TC-317) until LLR-270's next
   amendment. Under (a), IF-247 and IF-248 move from LLR-290 (item 5).
   **The coordinator's answer (review round 1):** option (b). IF-272 and
   IF-273 stay reached through their naming cases until LLR-270's next
   amendment, and IF-247 and IF-248 stay on LLR-290.
5. **IF-247 and IF-248 rest on LLR-290, a partial statement.** LLR-290 states
   the compaction flag, source, cursor and baseline the retained record
   carries and the bookkeeping that folds them; the record's name, identity,
   lease and lock are LLR-270's. One row is enough under the plan, and TC-303
   already names both interfaces for LLR-290, so a sitting asking "does the
   interface carry what the row constrains" is answered yes; a sitting asking
   whether the row states the whole form is answered by item 4.
6. **Clauses narrowed to what the code does; none cut.** Each is a MEANING
   change for the sitting, with its code evidence in section 4:
   - LLR-056: the outcome cards are merged, cancelled and partial (the
     outcome vocabulary's three), not "handback"; the station panel links
     the work-item registry, the log and the open-items page, and has linked
     no status page since `56dc580d0`, so the status page leaves the list.
   - LLR-044: "legacy Provider compatibility" is what the code gives, a
     legacy provider column read as the family.
   - LLR-269: the session mode is "fresh unless its retained session
     resumes one or it resumes an unretained thread" (the recorded "resumed
     only when its keep resumes a session" was contradicted by its own later
     clause and the code); the list of a call's data reads "including" (the
     call now carries more); "nothing else" is carried by "the service owns
     every launch and record step" with a new guard test.
   - LLR-283: "imports nothing" reads "imports only the standard library and
     the shared kernel's id reading" (the module imports the kernel's
     id-number reader); the no-file, no-git, no-environment half holds, with a
     new test.
   - LLR-140 and LLR-151 lose a design-document pointer each ("§2.3 steps
     1+2"; the concurrency document's section), pointers rather than
     obligations. LLR-140's added exit clause states the refusal side only:
     an integrate run that merged a branch it could not unload exits 1 while
     refusing nothing, and no test drives that.
7. **Rule-3 judgement calls a sitting may raise.** Round 1 resolved the
   first two (section 7): LLR-301's requirements cell now names SR-229
   beside SR-230, and LLR-137's names SR-173 beside SR-170.
   - LLR-301's added exit sentence gives the lease take, release, clear and
     status operations' exits, which serve SR-229, beside LLR-301's parent
     SR-230. TC-318, accepted and verifying SR-230 and LLR-301, already
     asserts those codes and the recorded row already said the command line
     dispatches the guard operations. The alternative states only the
     relaunch request's and hand-back's exits, leaving IF-281 partly
     unstated.
   - LLR-137's code cites SR-173 while its `sr_refs` names SR-170 alone; its
     added failure and order clauses sit under SR-173's partial-result arm as
     much as SR-170's. Adding SR-173 would be a routed change not made here.
   - LLR-040's unparseable-dial arm (asks, or keeps a legacy deny) beside
     SR-043's "fail open on any error": the gate treats the arm as a reading
     of the dial, not an error, and the row says so.
8. **Overlaps a sitting may read as one decision** (none states one decision
   twice; recorded so the question is answered before it is asked):
   - LLR-140 (a dirty path in the claim's scope refuses by name) and LLR-151
     (the claim commits through the bookkeeping commit, which refuses by name
     a dirty path the claim must write): both said so before this slice;
     LLR-151 now states the helper's whole contract (IF-186) and LLR-140
     points at it.
   - LLR-301's exit sentence leaves the window check's exit to LLR-300 ("The
     guard's window check exits nonzero inside an armed window"), so it keeps
     one home; LLR-301's lease-operation exits sit beside LLR-300's statement
     of what those operations refuse.
   - IF-175 is a bundle LLR-207 states most of; the failed-checks record and
     failed-round count (LLR-343) and the commit-record review walk (LLR-344)
     are stated elsewhere, not linked. IF-224's trunk-name call is LLR-339's
     statement and its one-id parse LLR-151's; LLR-259 states the crossing
     the bundle exists for. IF-245's adapter selection, occupancy and usage
     mapping (LLR-266 to LLR-268) and IF-246's coordinator call (LLR-346)
     are stated by rows not linked; the clean rows were preferred.
   - LLR-307 states the blessing digest's 16-character cut (IF-326); LLR-359
     (WI-1070's) states that the acceptance record takes the width from
     there. IF-326 is therefore not the brief's stop.
9. **The repeat check reports one name**: TC-301 names IF-264 and verifies
   only LLR-288, which now constrains it. This is one of the plan's four
   slice-5 strips (TC-253, TC-301, TC-308, TC-309): IF-264's only case
   citation, so it waits for slice 5 while OI-43's direct check stands.
10. **Cross-component candidates for slice 4, not linked here:** LLR-288 also
    states CMP-006's IF-054 (a pending open item blocks its citer) and IF-073
    (pending or ruled, a ruling releasing the row), both named by TC-301; each
    of those registry forms carries much else, so whether LLR-288 is their row
    is slice 4's judgement (a link only, if so). LLR-075's checker sits in
    CMP-006, but its one link is CMP-008's IF-163, so it is now placed at
    CMP-008.
11. **Interface rows found stale, not this slice's to amend:** IF-229's form
    names only the release checkpoint, while the command also takes the
    stage-gate checkpoint (LLR-255 states both); IF-256's notes say the
    decisions library imports nothing (item 6); IF-144's notes count 14
    checkers (item 2).
12. **Parts of a form no row states, left to the form** (none is a row clause
    today; each would need a test before a row could say it): IF-162's draw
    weights; IF-171's "no write, no spawn, no git"; IF-172's sorted JSON
    keys; IF-179's plain git runner; IF-266's empty answer for other
    runners; IF-296's held-text identity refusal (LLR-359's, untouched);
    IF-043's third code, as slice 2 left it. Round 1 wrote four that the
    first build had listed here into their rows, each with its test: IF-162's
    unreadable enable list (LLR-044), IF-171's no-command exit 2 and IF-172's
    empty-answer sentences (LLR-058), and IF-189's two fallbacks (LLR-339).
13. **Shared test modules.** `tests/test_done_when_blessing.py` carries tags
    for TC-132, TC-257 (the integrator's surface) and TC-321, TC-327 (the
    coordinator's), one docstring line holding both surfaces' tags;
    `tests/test_import_layers.py` gains one TC-248 tag (the release
    checklist's no-import clause), a population tag on a ratchet module's
    test, which can be dropped and the test cited untagged if the coordinator
    prefers; `tests/test_run_devsetup.py` gains one TC-318 tag.
14. **The parallel passes' breakage windows overlapped.** Each pass held a
    shipped file broken for one test run while the others ran their own
    tests; one pass saw one unrelated failure while another's window was
    open, which passed on rerun. The module run in section 2 ran after every
    window had closed, over the integrated tree.
15. **Ids:** none minted; the brief's ranges are untouched.
16. **Found in round 1, not fixed here (a design smell, surfaced):** the
    lane's integration base names the tip by its abbreviated id when there is
    no merge base, and by a full id otherwise (the merge-base answer is the
    full id git prints, the fallback the short tip id). A caller that hands
    the base to git as a revision is unaffected; one comparing bases as text
    would see two spellings of one kind of value. Readers not audited here.
    LLR-339 states the tip without naming the spelling.

## 7. Review record

**Round 1**, in five sessions: Gemini Hydrogen `APPROVE findings=0` on C1 and
on C2; OpenAI Sol, the code half over C1 and C2, seven distinct MINORs, all
adopted by the coordinator and fixed in one commit, `42d9c8bac`, every
recorded clause kept and the three row rules held:

1. **LLR-137's parent.** Its compile-first and stop-on-failure clauses sit
   under SR-173 (ordered regeneration, stopping at the first failure,
   committing no partial set), which its code already cited, while its
   requirements cell named SR-170 alone. The cell now names SR-170 and
   SR-173, a routed change. SR-173 is Accepted, so parent-first holds
   (`trace.py --strict`: `integrity=0`).
2. **LLR-301's parent.** Its added exit sentence covers the lease take,
   release, clear and status operations, which serve SR-229, beyond SR-230's
   successor relaunch. SR-229 is added to its requirements cell (routed),
   rather than the sentence moved: the rows under SR-229 are LLR-300, which
   states those operations but is WI-1071's and this slice may not touch, and
   LLR-423, which states the caller identification alone. SR-229 is Accepted.
3. **LLR-044 and IF-162's unreadable file.** The row now states "An absent
   enable list holds no entry, so managed selection is off; one that exists
   but cannot be read is refused as an error rather than read as absent".
   The test that drives it exists,
   `tests/test_accounts.py::test_an_unreadable_enable_list_is_an_error_and_an_absent_one_is_routing_off`
   (TC-361's), now tagged TC-046 beside it.
4. **LLR-339 and IF-189's fallbacks.** The row now states "with no merge
   base, as on a history sharing no commit with the trunk, it is the
   checkout's own tip, and a checkout with no commit has none". No test drove
   either: `tests/test_agent_loop_review.py::test_default_base_is_the_tip_without_a_merge_base_and_none_with_no_commit`
   (tagged TC-369) is added. Writing it found that the fallback names the tip
   by its abbreviated id (section 6, item 16); the test resolves both ids.
5. **LLR-058 and the scheduler's command line.** The row now states "Given
   no command, it prints its usage and exits 2, and a text answer with
   nothing in it is one line saying so: that no work item is ready, that the
   registry is empty, or that there is nothing to schedule".
   `tests/test_schedule.py::test_no_command_prints_the_usage_and_an_empty_text_answer_says_so`
   (tagged TC-058) is added. IF-172's sorted JSON keys and IF-171's "no write,
   no spawn, no git" stay form (section 6, item 12).
6. **TC-028 and the exit codes.** The tests driving the codes outside its
   module are tagged TC-028 (done, needs operator, paused through the
   dispatcher, review owed, restart, check-failure cap; preflight sits in its
   module already), and its `method` and `expected` now state each end state
   and its code: an accepted-cell amendment, owed to C1. Its recorded content
   is kept: the zero-commit guard, the all-ERROR region read as an
   unavailable agent, and its satisfying SR-028's acceptance criteria; "the
   agent-loop suite" (a module's name) is scrubbed.
7. **LLR-306 and IF-285.** "and prints the IF-285 reading" named an
   interface rather than stating the behaviour. The row now states the
   judging turn's reading (the call's retention, a fresh session, a retained
   session minted or one resumed, and its exit, then, for a successful call,
   the verdict with its validity or that it wrote none, and, for a failed
   call, that its verdict is not read) and the act turn's (its retention and
   exit, then the acts still owed and the review records changed, or that
   the act is complete). Its rationale's sentence giving the interfaces the
   command contract now says the interfaces state the form, the default route
   and the exit codes, and the row the behaviour a caller observes across
   them. `tests/test_coordinator_adjudicate.py::test_the_adjudicate_reading_names_the_keep_the_exit_and_the_verdict`
   (tagged TC-321) is added, and the act turn's exit line is asserted in
   `tests/test_coordinator_act.py::test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict`.

**Breakage runs.** Each new test or assertion failed against a deliberate
breakage of the code and passed restored, by a scratch runner outside the
repository (byte-exact replace, one test by node id, restore in the same
process, `git status` clean after each):

| Breakage | Test that caught it | Failing assertion (`1 failed` each) |
|---|---|---|
| no merge base read as none | the base fallback test | `TypeError: expected str, bytes or os.PathLike object, not NoneType`, `1 failed in 1.84s` |
| a checkout with no commit falling back to the trunk's name | the same | `AssertionError: assert 'main' is None`, `1 failed in 1.13s` |
| no command exiting 0 | the scheduler test | `AssertionError: assert 0 == 2`, `1 failed in 0.22s` |
| an empty frontier printing an empty line | the same | `assert [''] == ['schedule: n...y work items']`, `1 failed in 0.48s` |
| an empty simulation printing an empty line | the same | `assert [''] == ['schedule: n... to schedule']`, `1 failed in 0.35s` |
| the judging turn's retention line dropped | the adjudicate reading test | `assert 'keep: minting a retained session' in [...]`, `1 failed in 3.19s` |
| its exit line dropped | the same | `assert 'adjudicate: exit 0' in [...]`, `1 failed in 3.12s` |
| the failed call's line dropped | the same | `assert 'adjudicate: the call failed; its verdict is not read' in [...]`, `1 failed in 2.55s` |
| the missing verdict's line dropped | the same | the missing line absent from the output, `1 failed in 3.19s` |
| the act turn's exit line dropped | the act turn test | `assert 'act: exit 0' in 'keep: minting a retained session\nact: complete\n'`, `1 failed in 18.11s` |

The first pass of the two scheduler cases ran over stale bytecode (each
breakage left the module the same size within the same second, so the
interpreter kept the first's compiled copy); both reran with the bytecode
cleared, and those are the lines above.

**Round 1's tests:** the modules holding the tests of every test case
verifying the seven rows, with every test module the fix touched, the four
ratchet and sync modules and the stage test, 31 modules, `-n 6`, with a
short `--basetemp` outside the repository: `1480 passed, 17 skipped in 1598.86s
(0:26:38)`. `trace.py --root . --strict`: exit 0, `Traceability: SN=31
SR=141 LLR=372 TC=448 orphans=0 integrity=0 ... interfaces=239
interface-findings=0 ac-advisories=1 paraphrase-advisories=1`, the same
advisories as the build's tip, the coverage and placement lines unchanged
(135, 0, 51, 0, 53; 152 placed). `check_trajectory.py --root . --strict`:
`check_trajectory: clean (1070 work item(s), 941 done (88%), 37 cancelled,
graph acyclic).` The views and the `evidence` cells were regenerated before
the fix commit, which the hook passed.

## 8. The ninth sitting's LLR-014 disposition, answered

The ninth sitting (WI-1074,
`docs/reviews/wi-1074-adjudicate-ninth-sitting/001-ADJUDICATE-ee3f528.md`, on
trunk) re-accepted every slice-1 and slice-2 row but LLR-014, which it ruled
MEANING, not blessed: slice 2's text contradicted IF-004 on the unmeasured
fail-level budget and left out IF-147's baseline-update refusal and IF-167's
report. Its disposition asked three things; the coordinator added: read the
code for each clause, keep every clause of the accepted text, drive each
restated clause with a test (red against a deliberate breakage where new), and
check that the verifying test case states each clause. Answered in its own
commit, `728ffff89`; owed to sitting C1 (section 5).

**What the code does** (the budget comparator, read for each clause): a
failing or warning in-tier budget prints `check_perf: <FAIL|WARN> - <budget
id> <metric>: <reason>`; an in-tier fail-level budget with no measurement
keeps the SKIP status and prints `check_perf: WARN - <id> <metric>: Gate=fail
but no measurement this run - budget not checked (SKIP)`, counted in the
summary's skips; a warn-level one prints nothing and is counted there too; the
last line is `check_perf: OK - ...` or `check_perf: FAIL - ...` counting the
in-tier budgets, failures, warnings and skips, exiting 1 only on a FAIL. The
baseline-update arm runs before the budgets are read: with no metrics (none
read, or none in the file) it prints `check_perf: cannot update baseline - no
metrics at <path>` and exits 1; otherwise it merges the metrics into the
baseline, prints the changes and exits 0. The no-budgets and no-metrics arms
print their one line and return, exit 0. Only a run that reaches the
comparison writes the report: one table row per in-tier budget (status, id,
metric, measured, baseline, delta, budget, direction, gate), then a findings
list naming the reason for each FAIL and each WARN.

**The disposition's three points:**

1. The unmeasured fail-level budget: "reported on its own line as a skip"
   now reads "prints a WARN line naming it and marked as a skip, rather than
   passing in silence, and is counted among the summary's skips, not its
   warnings", which is IF-004's WARN and the code's line.
2. IF-147's baseline-update refusal is stated: "The baseline update compares
   nothing: it merges the current metrics into the baseline and exits 0, and
   with no metrics to write from it prints that it cannot update the
   baseline, naming where the metrics were expected, and exits 1."
3. The report sentence now matches IF-167: "A run that reaches a comparison
   writes the performance report: one table row per in-tier budget giving its
   status, budget id, metric, measured value, baseline, delta against the
   baseline, budget, direction and gate, then a findings list naming the
   reason for each failing and each warning budget; the no-budgets,
   no-metrics and baseline-update runs write no report."

**The clause accounting** (LLR-014, SR-006 and SR-167; TC-014,
`tests/test_check_perf.py`, module-tagged). The accepted text's four clauses
first, then slice 2's owed additions:

1. "Compares measured metrics (the metrics file) to declared budgets and the
   committed baseline (the baseline file)": kept as slice 2 worded it;
   `test_within_tolerance_regression_passes`,
   `test_regression_beyond_tolerance_fails_when_gate_fail`.
2. "fails beyond tolerance at the row's block/warn level": kept;
   `test_absolute_breach_fails_when_gate_fail`,
   `test_absolute_breach_only_warns_when_gate_warn`.
3. "the baseline update flag is the reviewed acceptance path for an intended
   regression": kept as "the baseline update"; `test_update_baseline_writes_file`,
   `test_update_baseline_merges_and_preserves`.
4. "The step is wired into the harness at DevStg-Impl, per its declared gates
   in the stack profile file": kept; `test_harness_runs_perf_at_g3`,
   `test_perf_step_is_process_layer_in_list`.
5. (slice 2) "Each in-tier budget that fails or warns prints a line naming its
   status and its budget id": kept, the line's metric and reason added (what
   it prints); `test_absolute_breach_fails_when_gate_fail`,
   `test_absolute_breach_only_warns_when_gate_warn`, and
   `test_the_report_rows_each_in_tier_budget_and_names_each_fail_and_warn_reason`
   (new: the two lines asserted whole).
6. (slice 2) "a fail-level budget with no measurement this run is reported on
   its own line as a skip rather than passing in silence": restated, point 1;
   `test_gated_skip_prints_per_row_warn_line`,
   `test_an_unmeasured_budget_gets_its_own_line_only_when_fail_level`
   (extended: the line begins `check_perf: WARN - PB-001` and ends `(SKIP)`,
   and the summary counts `0 warn, 2 skip`).
7. (slice 2) "while a warn-level budget with no measurement prints no line of
   its own and is counted among the skips": verbatim;
   `test_an_unmeasured_budget_gets_its_own_line_only_when_fail_level`.
8. (slice 2) "The run prints an OK or FAIL summary counting the failures,
   warnings and skips": kept as "closes on an OK or FAIL summary line counting
   the in-tier budgets, the failures, the warnings and the skips";
   `test_an_unmeasured_budget_gets_its_own_line_only_when_fail_level` (the
   last line), `test_the_report_rows_each_in_tier_budget_and_names_each_fail_and_warn_reason`.
9. (slice 2) "a project with no budget rows printing an OK line saying so":
   kept; `test_no_real_budgets_passes`,
   `test_the_no_budgets_no_metrics_and_baseline_update_runs_write_no_report`.
10. (slice 2) "budgets with no metrics file a SKIP line": kept, "naming where
    the metrics were expected"; `test_budgets_present_but_no_metrics_skips`
    (extended: the metrics path named).
11. (slice 2) "A comparison exits 1 only when an in-tier budget fails, and 0
    for every other outcome, warnings and skips included": verbatim;
    `test_tier_scopes_which_budgets_gate`, `test_absolute_breach_*`,
    `test_malformed_metric_value_*`, `test_gated_skip_prints_per_row_warn_line`.
12. (slice 2) "A run that reaches a comparison writes the performance report,
    naming each failing budget's reason": restated, point 3;
    `test_the_report_rows_each_in_tier_budget_and_names_each_fail_and_warn_reason`
    and `test_the_no_budgets_no_metrics_and_baseline_update_runs_write_no_report`
    (both new), with `test_absolute_breach_fails_when_gate_fail`,
    `test_regression_beyond_tolerance_fails_when_gate_fail`,
    `test_malformed_metric_value_fails_hard_gated_row` (each failure's reason
    in the report).
- Added (point 2): the baseline update's merge and exit 0,
  `test_update_baseline_writes_file`, `test_update_baseline_merges_and_preserves`;
  its refusal with no metrics, `test_update_baseline_with_no_metrics_refuses_and_writes_nothing`
  (new); "compares nothing", the update run in
  `test_the_no_budgets_no_metrics_and_baseline_update_runs_write_no_report`
  (no report).
- Rule 3: SR-167 asks that an unmeasured hard-gated row be "a per-row
  reported skip, never silent", which the WARN line marked as a skip is, and
  that a reviewed baseline update be the acceptance path; SR-006 the step
  plan. The added refusal and report clauses decompose those; nothing beyond
  either parent.

**TC-014** (verifies SR-006, SR-167, LLR-014) stated none of these clauses
("Run the check-perf suite; a within-tolerance metric passes and a regression
fails"; expected "Satisfies the acceptance folded into LLR-014 ..."). Its
`method` and `expected` now state each, every observable asserted by a test in
its module: the vacuous runs' lines and exits, the FAIL and WARN lines and
exits, the regression arm, the tier scope, the non-numeric metric, the
unmeasured budgets' lines and the summary's count, the report's rows and
findings and the out-of-tier budget's absence, the baseline update and its
refusal, no report on the three arms, and the harness's DevStg-Impl run and
step listing. Its recorded content is kept: the within-tolerance pass and the
regression failure, and its satisfying SR-167's breach verdict and SR-006's
step plan through LLR-014. "The check-perf suite" (a module's name) is
scrubbed. Owed to sitting C1 with LLR-014.

**The tests** (`tests/test_check_perf.py`): three added
(`test_update_baseline_with_no_metrics_refuses_and_writes_nothing`,
`test_the_report_rows_each_in_tier_budget_and_names_each_fail_and_warn_reason`,
`test_the_no_budgets_no_metrics_and_baseline_update_runs_write_no_report`) and
two extended (`test_budgets_present_but_no_metrics_skips`,
`test_an_unmeasured_budget_gets_its_own_line_only_when_fail_level`). Each new
or extended assertion failed against a deliberate breakage of the comparator,
restored at once by a scratch runner outside the repository:

| Breakage | Test that caught it | Failing assertion (`1 failed` each) |
|---|---|---|
| the unmeasured fail-level line printed as `SKIP -` | `test_an_unmeasured_budget_gets_its_own_line_only_when_fail_level` | `AssertionError: ['check_perf: SKIP - PB-001 Metric PB-001: Gate=fail but no measurement this run - budget not checked (SKIP)']`, `1 failed in 7.98s` |
| the no-metrics SKIP line without the metrics path | `test_budgets_present_but_no_metrics_skips` | `AssertionError: check_perf: SKIP - 1 budget(s) but no metrics at the declared path (wire the product measurement step that emits it)`, `1 failed in 9.01s` |
| the baseline update with no metrics returning 0 | `test_update_baseline_with_no_metrics_refuses_and_writes_nothing` | the exit asserted 1, `1 failed in 12.42s` |
| the refusal without the metrics path | the same | `AssertionError: check_perf: cannot update baseline - no metrics at the declared path`, `1 failed in 7.89s` |
| the console line without its reason | `test_the_report_rows_each_in_tier_budget_and_names_each_fail_and_warn_reason` | `assert 'check_perf: FAIL - PB-001 Metric PB-001: exceeds budget 500MiB; regressed vs baseline 400MiB' in ['check_perf: FAIL - PB-001 Metric PB-001', ...]`, `1 failed in 14.05s` |
| the findings naming FAIL only | the same | the WARN finding absent from the report, `1 failed in 9.29s` |
| the table row without its gate | the same | the two rows' gate cells empty where `fail` and `warn` were asserted, `1 failed in 10.75s` |
| the no-budgets run writing a report | `test_the_no_budgets_no_metrics_and_baseline_update_runs_write_no_report` | `assert not True` (`exists()`), `1 failed in 7.76s` |
| the no-metrics run writing a report | the same | `assert not True`, `1 failed in 11.68s` |
| the baseline update writing a report | the same | `assert not True`, `1 failed in 10.18s` |

The module, restored: `24 passed in 177.49s (0:02:57)`.
