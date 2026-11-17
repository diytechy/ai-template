"""HANDOFF 10.7 item 1 with 9.10's leftovers: "bar" where it names a run of
checks, in code names and test names (D4); and the few live names where
"bar" is a stage (4.5.5) or a threshold (4.5.7). The glossary already says
which word replaced which: the commit bar and the review bar are the
**commit checks**, the landing bar the **landing checks**, the gate bar the
**gate checks**, a bar in general the **required checks**.

Kept, each named for the retired thing it reads or records (4.5.5): the
retired bar axis and everything named for it (`_LEGACY_BAR_THRESHOLD`,
`_RETIRED_BARS`, `_RETIRED_WI_BARS`, `RETIRED = "bars"` and the `[bars]`
section, `DevBar-*`, "bar-era", "bar-only wording", "vacuous-lowest-bar",
`bar_failures: 0` quoted from a run's output, `test_a_retired_bars_section_*`).
Visual bars stay bars (`tracebar`, `stbar`, progress bars, a rule of `=`).

Prose: `r47e_checks_prose.py` and `h47g*.py`. Locals that share a spelling
with retired-axis history elsewhere (`bar_label`, `BARS`) move by token in
`n47e_names.py`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
    "docs/complexity-baseline",
    "docs/handoff-*",
]

TOKENS = {
    # --- integrate.py, review_brief.py, agent_loop.py
    "_run_bar": "_run_landing_checks",
    "_refresh_bar": "_refresh_checks",
    "_run_review_bar": "_run_commit_checks",
    "_bar_refusal": "_checks_refusal",
    "_review_bar_refusal": "_commit_checks_refusal",
    "skip_bar": "skip_checks",
    "run_bar": "run_checks",
    "record_bar_result": "record_checks_result",
    # --- dashboard panel 3
    "bar_lis": "check_lis",
    # --- test fixtures: the stand-in check suite and its switches
    "declare_review_bar": "declare_commit_checks",
    "bar_runs": "check_runs",
    "_bar_ran": "_checks_ran",
    "bar_red": "checks_fail",
    "bar_plan": "checks_plan",
    "BAR-FAIL-MARKER": "CHECKS-FAIL-MARKER",
    "bar-cache": "checks-cache",
    "LONG_BAR": "LONG_CHECKS",
    "long_bar": "long_checks",
    "WI398_JOBS_BAR_OUT": "WI398_JOBS_CHECKS_OUT",
    "WI398_SEQ_BAR_OUT": "WI398_SEQ_CHECKS_OUT",
    "WI405_NESTED_BAR_OTHER_STEP": "WI405_NESTED_CHECKS_OTHER_STEP",
    "WI405_QUOTED_FAIL_ROW_BAR": "WI405_QUOTED_FAIL_ROW_CHECKS",
    "WI405_QUOTED_MOCK_BANNER_BAR": "WI405_QUOTED_MOCK_BANNER_CHECKS",
    # --- tests (D4), with the evidence cells that cite them
    "test_the_shipped_default_holds_a_bar_advance": "test_the_shipped_default_holds_a_stage_advance",
    "test_known_limit_a_nested_bar_naming_another_step_misattributes_the_window":
        "test_known_limit_a_nested_check_run_naming_another_step_misattributes_the_window",
    "test_red_bar_draws_no_review_records_a_red_round_and_rebuilds_with_the_tail":
        "test_failed_checks_draw_no_review_record_a_failed_round_and_rebuild_with_the_tail",
    "test_worker_brief_names_the_one_turn_close_bar_scratch_and_amendments":
        "test_worker_brief_names_the_one_turn_close_checks_scratch_and_amendments",
    "test_backlink_coverage_step_is_wired_at_the_right_bars":
        "test_backlink_coverage_step_is_wired_at_the_right_stages",
    "test_the_lints_are_the_declared_commit_bars_own_and_none_is_the_tier_step":
        "test_the_lints_are_the_declared_commit_checks_own_and_none_is_the_tier_step",
    "test_neither_bar_fails_on_seconds": "test_neither_route_fails_on_seconds",
    "test_a_red_tier_still_fails_each_bar": "test_a_failing_tier_still_fails_each_route",
    "test_the_shipped_table_is_the_documented_human_bar":
        "test_the_shipped_table_is_the_documented_set_of_checks",
    "test_a_red_handback_is_reverted_to_a_bar_inert_artefact_and_merges":
        "test_a_failing_handback_is_reverted_to_a_checks_inert_artefact_and_merges",
    "test_drive_stops_on_a_red_refresh_bar": "test_drive_stops_on_failing_landing_checks",
    "test_a_declared_test_command_passes_the_bar_declaration_check":
        "test_a_declared_test_command_passes_the_checks_declaration_check",
    "test_a_declared_toolchain_without_its_venv_refuses_the_bar":
        "test_a_declared_toolchain_without_its_venv_refuses_the_checks",
    "test_a_scaffold_that_declares_no_toolchain_still_runs_the_bar":
        "test_a_scaffold_that_declares_no_toolchain_still_runs_the_checks",
    "test_a_red_review_bar_commits_nothing_and_leaves_branch_and_index":
        "test_failing_commit_checks_commit_nothing_and_leave_branch_and_index",
    "test_record_checks_refuses_a_dirty_worktree_before_running_the_bar":
        "test_record_checks_refuses_a_dirty_worktree_before_running_the_checks",
    "test_record_checks_refuses_a_missing_review_bar_key_naming_it":
        "test_record_checks_refuses_a_missing_commit_checks_key_naming_it",
    "test_the_named_tests_run_after_the_review_bar_under_the_lanes_basetemp":
        "test_the_named_tests_run_after_the_commit_checks_under_the_lanes_basetemp",
    "test_a_bar_that_edits_a_tracked_file_records_nothing":
        "test_checks_that_edit_a_tracked_file_record_nothing",
    "test_a_bar_that_stages_an_edit_leaves_the_index_as_staged":
        "test_checks_that_stage_an_edit_leave_the_index_as_staged",
    "test_record_checks_refuses_below_the_harness_floor_before_the_bar":
        "test_record_checks_refuses_below_the_harness_floor_before_the_checks",
    "test_a_message_file_carrying_the_label_is_refused_before_the_bar":
        "test_a_message_file_carrying_the_label_is_refused_before_the_checks",
    "test_a_derivation_refusal_runs_no_bar_and_leaves_branch_and_index":
        "test_a_derivation_refusal_runs_no_checks_and_leaves_branch_and_index",
    "test_record_checks_runs_the_review_bar_then_the_derived_files":
        "test_record_checks_runs_the_commit_checks_then_the_derived_files",
    "test_a_row_touching_no_code_runs_the_bar_alone": "test_a_row_touching_no_code_runs_the_check_suite_alone",
    "test_the_refresh_merges_trunk_in_regenerates_bars_then_commits":
        "test_the_refresh_merges_trunk_in_regenerates_checks_then_commits",
    "test_the_bar_residue_the_refresh_created_is_shed_but_the_lanes_is_not":
        "test_the_checks_residue_the_refresh_created_is_shed_but_the_lanes_is_not",
    "test_an_adjudication_lane_runs_no_bar": "test_an_adjudication_lane_runs_no_checks",
    "test_a_product_touching_adjudication_lane_fails_toward_the_bar":
        "test_a_product_touching_adjudication_lane_fails_toward_the_checks",
    "test_a_lane_whose_one_row_is_ordinary_runs_the_bar": "test_a_lane_whose_one_row_is_ordinary_runs_the_checks",
    "test_a_red_refresh_bar_commits_nothing_and_leaves_the_branch_clean":
        "test_failing_landing_checks_commit_nothing_and_leave_the_branch_clean",
    "test_the_queue_refuses_to_land_a_forged_passed_checks_record_unbarred":
        "test_the_queue_refuses_to_land_a_forged_passed_checks_record_unchecked",
    "test_a_directory_the_bar_itself_created_is_pruned":
        "test_a_directory_the_checks_themselves_created_is_pruned",
    "test_integrate_refuses_and_holds_the_trunk_when_the_bar_is_undeclared":
        "test_integrate_refuses_and_holds_the_trunk_when_the_checks_are_undeclared",
    "test_bar_step_count_is_by_distinct_name_not_by_echoed_line":
        "test_checks_step_count_is_by_distinct_name_not_by_echoed_line",
    "test_the_refresh_trailer_names_the_landing_bar": "test_the_refresh_trailer_names_the_landing_checks",
    "test_the_declared_residue_set_is_exactly_the_bars_own_leavings":
        "test_the_declared_residue_set_is_exactly_the_checks_own_leavings",
    "test_a_lane_holding_the_bars_html_report_unloads_clean":
        "test_a_lane_holding_the_checks_html_report_unloads_clean",
    "test_the_worker_close_bar_points_at_its_homes_instead_of_restating_it":
        "test_the_worker_close_checks_point_at_their_homes_instead_of_restating_them",
    "test_the_worker_brief_points_at_the_spine_linked_tests_and_the_bar":
        "test_the_worker_brief_points_at_the_spine_linked_tests_and_the_checks",
    "test_record_checks_refuses_each_undeclared_state_before_the_bar":
        "test_record_checks_refuses_each_undeclared_state_before_the_checks",
    "test_refresh_refuses_each_undeclared_state_before_the_bar":
        "test_refresh_refuses_each_undeclared_state_before_the_checks",
    "test_the_backlink_bar_is_type_checked_where_its_reader_stays_quiet":
        "test_the_backlink_minimum_is_type_checked_where_its_reader_stays_quiet",
    "test_require_verified_bar_matches_sr_gate_regardless_of_method":
        "test_require_verified_at_impl_matches_sr_gate_regardless_of_method",
    "test_adopter_facing_checks_meet_the_shipped_bar": "test_adopter_facing_checks_meet_the_shipped_standard",
    "test_bar_catches_a_coordinator_tier_import": "test_the_standard_catches_a_coordinator_tier_import",
    "test_bar_catches_an_unruled_shipped_import": "test_the_standard_catches_an_unruled_shipped_import",
    "test_bar_catches_an_undeclared_import": "test_the_standard_catches_an_undeclared_import",
    "test_the_declared_commit_bar_runs_the_strict_lints_before_its_budget":
        "test_the_declared_commit_checks_run_the_strict_lints_before_their_budget",
    "test_critique_staleness_warns_at_commit_bar_when_render_surface_newer":
        "test_critique_staleness_warns_at_commit_checks_when_render_surface_newer",
}

PARTS = {
    "no-bar": "no-checks",
    "NO-BAR": "NO-CHECKS",
    "bar-inert": "checks-inert",
    "Bar-inert": "Checks-inert",
    "BAR-INERT": "CHECKS-INERT",
    "commit-bar": "commit-check",
    "review-bar": "commit-check",
    "gate-bar": "gate-check",
    "check-bar": "gate-check",
    "bar-shaped": "harness-shaped",
    "real-bar": "real-checks",
}

PROTECT = list(_PROTECT) + [
    r"bar_failures: 0",
]
