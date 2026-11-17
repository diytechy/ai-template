"""HANDOFF 4.5.6 (ruled 2026-11-16) with 9.10's leftover, test names (D4): a
run of checks passes or fails; "red" and "green" are not used for either.
The tests named for a red or green run, with the evidence cells that cite
them, and three fake test names inside fixture output (`test_red`,
`test_the_other_red`, `test_red_bar`) that stand for a failing test.

Not this file: "red" and "green" in comments, docstrings and messages
(9.11 lists what is left); colours in the dashboard and its tests; the red,
green, refactor cycle `process.md` names.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
    "docs/complexity-baseline",
    "docs/handoff-*",
]

TOKENS = {
    "test_a_freshly_scaffolded_repo_is_GREEN_on_the_placeholder":
        "test_a_freshly_scaffolded_repo_PASSES_on_the_placeholder",
    "test_every_profile_permutation_scaffolds_green": "test_every_profile_permutation_scaffolds_and_passes",
    "test_a_GREEN_run_writes_a_record_that_HOLDS": "test_a_PASSING_run_writes_a_record_that_HOLDS",
    "test_a_RED_run_does_not_overwrite_an_existing_record": "test_a_FAILING_run_does_not_overwrite_an_existing_record",
    "test_a_RED_run_writes_NOTHING": "test_a_FAILING_run_writes_NOTHING",
    "test_a_long_red_summary_keeps_its_cause_and_its_final_diagnostic":
        "test_a_long_failure_summary_keeps_its_cause_and_its_final_diagnostic",
    "test_an_interrupted_red_is_rechecked_once_at_the_draw_and_counted_once":
        "test_an_interrupted_failure_is_rechecked_once_at_the_draw_and_counted_once",
    "test_minimal_project_is_green": "test_minimal_project_passes",
    "test_old_kit_scaffold_syncs_forward_to_a_green_harness":
        "test_old_kit_scaffold_syncs_forward_to_a_passing_harness",
    "test_red_count_survives_a_resume_and_a_green_resets_it":
        "test_the_failure_count_survives_a_resume_and_a_pass_resets_it",
    "test_red_count_survives_a_resume_to_the_cap_and_exits_12":
        "test_the_failure_count_survives_a_resume_to_the_cap_and_exits_12",
    "test_regen_failure_after_green_steps_commits_nothing": "test_regen_failure_after_passing_steps_commits_nothing",
    "test_the_check_py_STEP_goes_red_on_a_stale_cache": "test_the_check_py_STEP_fails_on_a_stale_cache",
    "test_the_green_holds_only_because_the_old_checkers_survived":
        "test_the_pass_holds_only_because_the_old_checkers_survived",
    "test_a_PENDING_AMENDMENT_leaves_the_committed_mirror_GREEN":
        "test_a_PENDING_AMENDMENT_leaves_the_committed_mirror_PASSING",
    "test_a_SCOPED_refresh_leaves_the_UNTOUCHED_offspine_mirror_GREEN":
        "test_a_SCOPED_refresh_leaves_the_UNTOUCHED_offspine_mirror_PASSING",
    "test_a_conflict_only_on_declared_generated_paths_refreshes_green":
        "test_a_conflict_only_on_declared_generated_paths_refreshes_and_passes",
    "test_a_green_tier_with_a_failed_reading_exits_two": "test_a_passing_tier_with_a_failed_reading_exits_two",
    "test_a_red_refusal_carries_the_steps_own_output_and_names_the_kept_log":
        "test_a_failure_refusal_carries_the_steps_own_output_and_names_the_kept_log",
    "test_a_red_tier_exits_with_its_own_code_and_the_verdict_line":
        "test_a_failing_tier_exits_with_its_own_code_and_the_verdict_line",
    "test_a_red_tier_over_max_tests_keeps_its_code_and_names_the_count":
        "test_a_failing_tier_over_max_tests_keeps_its_code_and_names_the_count",
    "test_a_red_tier_with_a_failed_reading_names_both": "test_a_failing_tier_with_a_failed_reading_names_both",
    "test_check_py_gate_red_on_seeded_leak": "test_check_py_gate_fails_on_seeded_leak",
    "test_cli_mapping_purpose_is_green_over_the_real_repo": "test_cli_mapping_purpose_passes_over_the_real_repo",
    "test_coherent_sr_llr_pairs_stay_green": "test_coherent_sr_llr_pairs_pass",
    "test_default_scaffold_is_fully_green_including_warnings":
        "test_default_scaffold_passes_fully_including_warnings",
    "test_force_resync_installs_current_checkers_and_the_tree_cannot_false_green":
        "test_force_resync_installs_current_checkers_and_the_tree_cannot_falsely_pass",
    "test_quarantine_refuses_when_the_red_is_not_the_lanes_own_code":
        "test_quarantine_refuses_when_the_failure_is_not_the_lanes_own_code",
    "test_quoted_comma_control_stays_green": "test_quoted_comma_control_passes",
    "test_repo_sweep_fresh_scaffold_green_then_seeded_leak_red":
        "test_repo_sweep_fresh_scaffold_passes_then_seeded_leak_fails",
    "test_restamp_then_enforce_is_green": "test_restamp_then_enforce_passes",
    "test_scaffold_with_agents_still_green": "test_scaffold_with_agents_still_passes",
    "test_staged_home_dir_paths_red_placeholders_and_marker_green":
        "test_staged_home_dir_paths_fail_placeholders_and_marker_pass",
    "test_two_plans_green_with_coverage_diff": "test_two_plans_pass_with_coverage_diff",
    # fake test names inside fixture output, standing for a failing test
    "test_the_other_red": "test_the_other_failing",
    "test_red_bar": "test_failing_checks",
    "test_red": "test_failing",
}

PROTECT = list(_PROTECT)
