"""HANDOFF 4.1 / 10.6: the passed-checks record, with 4.5.1 (the failed-checks record).

S1 of VOCABULARY.md 3: a script's record that a named set of checks passed on
a named tree. The trailer `Bar-Green: tree= work= bar=<review|landing|no-bar>
tests= <summary>` becomes `Checks-Passed: tree= work= checks=<commit|landing|none>
tests= <summary>`; `integrate.py attest --bar review` becomes `integrate.py
record-checks --checks commit`; the loop's log phase `ATTEST` (labels `ATTEST
GREEN|RED`) becomes `CHECKS` (`CHECKS PASSED|FAILED`). With it, 4.5.1 (D16):
the session-log headers `# bar-red:` / `# bar-summary:` become
`# checks-failed:` / `# checks-summary:`, and the record's names follow
(`red_rounds` -> `failed_rounds`, `format_red_record`, `parse_red_record`,
`red_record`, `EXIT_RED_CAP` -> `EXIT_CHECK_FAILURE_CAP`, `red_cap_check` ->
`failure_cap_check`).

Write and read the new form only (D3): no reader of the earlier trailer or
headers is kept.

Not this file:
- Python locals (`attested`, the field and parameter `bar`): `pyname.py` with
  `n46a_names.py`, by token, so prose and strings are not touched.
- Sentences: `h46*.py`.
- Other senses of the same words, left as they are: "bar" as a generic word
  for running checks and the work-item `bar` key (4.5.2 to 4.5.7, 10.7);
  `red_rounds_max` and `RED_ROUNDS_*` (4.5.4); the S3 method leftovers
  (`make_attest_project`, "critique or attestation", "gate-attested"); retired
  names spelled as they were (`_attested_baseline`, `attestation-baseline`,
  `RE-ATTESTATION-PENDING`, the retired `intake.py attest` subcommand);
  `ctl/bar_red`, a test fixture's switch for a failing check suite.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
    # ratchet histories: each entry quotes the names of its day
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
    "docs/complexity-baseline",
]

TOKENS = {
    # --- the record: kitlib/station.py, kitlib/verdict.py
    "BAR_GREEN": "CHECKS_PASSED",
    "BAR_NAMES": "CHECK_SETS",
    "LANDING_BARS": "LANDING_CHECK_SETS",
    "_ATTEST_RE": "_PASSED_CHECKS_RE",
    "BarAttestation": "PassedChecks",
    "bar_attestation": "passed_checks",
    "read_bar_attestation": "read_passed_checks",
    "format_bar_green": "format_passed_checks",
    "refresh_attestation": "refresh_passed_checks",
    "review_attestation": "commit_passed_checks",
    # Reads no checks record: it peels the machinery's own close commit. The
    # name station.py's comment already gives it (decision in HANDOFF 9.10).
    "mechanical_close_attestation": "mechanical_close_peel",
    # named for the trailer's value `review`, now `commit`
    "_review_record_answer": "_commit_record_answer",
    "last_review_record": "last_commit_record",
    "_last_review_green": "_last_commit_passed",
    # --- the failed-checks record (4.5.1)
    "RED_KEYS": "FAILED_KEYS",
    "_BAR_RED_RE": "_CHECKS_FAILED_RE",
    "_BAR_SUMMARY_RE": "_CHECKS_SUMMARY_RE",
    "format_red_record": "format_failed_record",
    "parse_red_record": "parse_failed_record",
    "red_record": "failed_record",
    "red_rounds": "failed_rounds",
    "RedCount": "FailedCount",
    "_logged_red": "_logged_failure",
    "EXIT_RED_CAP": "EXIT_CHECK_FAILURE_CAP",
    "red_cap_check": "failure_cap_check",
    "_red_cap_close": "_failure_cap_close",
    # --- integrate.py, agent_loop.py, kitlib/red_mark.py, review_brief.py
    "_attest_commit": "_record_checks_commit",
    "_attest_message": "_record_checks_message",
    "_attest_preflight": "_record_checks_preflight",
    "_AttestPlan": "_RecordChecksPlan",
    "attest_build": "record_build_checks",
    "attest_refusal": "record_checks_refusal",
    "_ATTEST_STEP": "_RECORD_CHECKS_STEP",
    # --- tests: files, fixtures, helpers
    "test_bar_attestation": "test_passed_checks",
    "test_integrate_attest": "test_integrate_record_checks",
    "attest_repo": "checks_repo",
    "ATTEST_STACK_INI": "CHECKS_STACK_INI",
    "ATTEST_SUITE": "CHECKS_SUITE",
    "ATTEST_FILES": "CHECKS_FILES",
    "_attest": "_record_checks",
    "_attest_tip": "_passed_checks_tip",
    "_malformed_attest_tip": "_malformed_record_tip",
    "_attested_line": "_record_line",
    "red_capped_worker": "failure_capped_worker",
    # --- tests: names (D4), with the evidence cells that cite them
    "test_a_trailer_naming_its_own_tree_and_parent_verifies_for_each_bar":
        "test_a_trailer_naming_its_own_tree_and_parent_verifies_for_each_check_set",
    "test_a_wrong_tree_is_not_an_attestation": "test_a_wrong_tree_is_not_a_passed_checks_record",
    "test_a_wrong_parent_is_not_an_attestation": "test_a_wrong_parent_is_not_a_passed_checks_record",
    "test_a_trailer_without_bar_is_not_an_attestation":
        "test_a_trailer_without_checks_is_not_a_passed_checks_record",
    "test_an_unknown_bar_is_not_an_attestation": "test_an_unknown_check_set_is_not_a_passed_checks_record",
    "test_a_trailer_without_tests_is_not_an_attestation":
        "test_a_trailer_without_tests_is_not_a_passed_checks_record",
    "test_a_trailer_quoted_mid_line_is_not_an_attestation":
        "test_a_trailer_quoted_mid_line_is_not_a_passed_checks_record",
    "test_two_label_lines_are_not_an_attestation": "test_two_label_lines_are_not_a_passed_checks_record",
    "test_work_tip_never_peels_a_review_attestation": "test_work_tip_never_peels_a_commit_checks_record",
    "test_governing_rev_never_peels_a_review_attestation":
        "test_governing_rev_never_peels_a_commit_checks_record",
    "test_a_hook_refused_attest_commit_leaves_branch_and_index":
        "test_a_hook_refused_record_checks_commit_leaves_branch_and_index",
    "test_a_rewritten_attest_commit_is_undone_by_the_self_check":
        "test_a_rewritten_record_checks_commit_is_undone_by_the_self_check",
    "test_a_bar_that_edits_a_tracked_file_attests_nothing": "test_a_bar_that_edits_a_tracked_file_records_nothing",
    "test_the_attestation_joins_a_message_files_trailer_block":
        "test_the_passed_checks_record_joins_a_message_files_trailer_block",
    "test_the_attest_cli_is_the_route_a_builder_calls": "test_the_record_checks_cli_is_the_route_a_builder_calls",
    "test_the_review_render_accepts_what_attest_writes": "test_the_review_render_accepts_what_record_checks_writes",
    "test_merge_ready_refuses_a_tip_carrying_only_a_review_attestation":
        "test_merge_ready_refuses_a_tip_carrying_only_a_commit_checks_record",
    "test_a_deliberately_forged_attestation_is_a_STATED_limit_not_a_defence":
        "test_a_deliberately_forged_passed_checks_record_is_a_STATED_limit_not_a_defence",
    "test_a_forged_bar_green_trailer_does_not_make_a_branch_merge_ready":
        "test_a_forged_checks_passed_trailer_does_not_make_a_branch_merge_ready",
    "test_a_landing_attestation_refuses_naming_both_bars": "test_a_landing_record_refuses_naming_both_check_sets",
    "test_a_matching_review_attestation_renders_and_names_it":
        "test_a_matching_commit_checks_record_renders_and_names_it",
    "test_a_plain_commit_removal_then_an_empty_attest_is_judged":
        "test_a_plain_commit_removal_then_an_empty_record_checks_commit_is_judged",
    "test_a_review_attestation_for_other_tests_refuses_naming_both_digests":
        "test_a_commit_checks_record_for_other_tests_refuses_naming_both_digests",
    "test_a_tip_with_no_attestation_refuses_naming_the_attest_command":
        "test_a_tip_with_no_passed_checks_record_refuses_naming_the_record_checks_command",
    "test_a_work_commit_above_the_attested_one_refuses": "test_a_work_commit_above_the_recorded_one_refuses",
    "test_amending_a_refresh_commit_revokes_its_attestation":
        "test_amending_a_refresh_commit_revokes_its_passed_checks_record",
    "test_an_attestation_that_does_not_name_the_tip_refuses_naming_the_cause":
        "test_a_passed_checks_record_that_does_not_name_the_tip_refuses_naming_the_cause",
    "test_attest_phase_is_inert_to_every_phase_reader": "test_checks_phase_is_inert_to_every_phase_reader",
    "test_green_bar_attests_once_then_draws_the_review": "test_passed_commit_checks_are_recorded_once_then_the_review_is_drawn",
    "test_merge_ready_needs_the_ancestor_relation_AND_the_attestation":
        "test_merge_ready_needs_the_ancestor_relation_AND_the_passed_checks_record",
    "test_post_narrow_and_adjudication_rounds_draw_only_over_a_verified_attestation":
        "test_post_narrow_and_adjudication_rounds_draw_only_over_a_verified_passed_checks_record",
    "test_record_only_commits_above_the_attested_one_render": "test_record_only_commits_above_the_recorded_one_render",
    "test_red_cap_exits_with_its_own_code_and_one_fewer_does_not":
        "test_failure_cap_exits_with_its_own_code_and_one_fewer_does_not",
    "test_a_red_cap_exit_closes_the_lane_partial_with_typed_fields_and_the_drain_quarantines_it":
        "test_a_failure_cap_exit_closes_the_lane_partial_with_typed_fields_and_the_drain_quarantines_it",
    "test_a_derivation_refusal_counts_toward_the_red_cap": "test_a_derivation_refusal_counts_toward_the_failure_cap",
    "test_red_rounds_counts_an_unreadable_log_and_answers_none_for_no_history":
        "test_failed_rounds_counts_an_unreadable_log_and_answers_none_for_no_history",
    "test_red_rounds_counts_distinct_red_builds_and_a_green_attestation_resets_it":
        "test_failed_rounds_counts_distinct_failed_builds_and_a_passed_checks_record_resets_it",
    "test_red_rounds_counts_one_build_recorded_twice_once": "test_failed_rounds_counts_one_build_recorded_twice_once",
    "test_resumed_round_on_an_unattested_tip_runs_the_producer_once":
        "test_resumed_round_on_an_unrecorded_tip_runs_the_producer_once",
    "test_station_refresh_pins_the_bar_attestation": "test_station_refresh_pins_the_passed_checks_record",
    "test_the_adjudication_refresh_names_no_bar": "test_the_adjudication_refresh_names_no_checks",
    "test_the_close_the_writer_lands_is_one_the_attestor_peels":
        "test_the_close_the_writer_lands_is_one_the_verifier_peels",
    "test_the_cycle_reviews_only_an_attested_tip": "test_the_cycle_reviews_only_a_recorded_tip",
    "test_the_queue_refuses_to_land_a_forged_attestation_unbarred":
        "test_the_queue_refuses_to_land_a_forged_passed_checks_record_unbarred",
    "test_the_refresh_and_attest_commit_through_one_producer":
        "test_the_refresh_and_record_checks_commit_through_one_producer",
    "test_the_refresh_attests_the_bar_to_the_sha_it_produced":
        "test_the_refresh_records_the_checks_for_the_sha_it_produced",
    "test_the_refusal_hint_names_attest_without_tests": "test_the_refusal_hint_names_record_checks_without_tests",
    # the Review-Verdict trailer, which the code calls a trailer
    "test_an_attestation_riding_a_commit_that_changed_the_work_is_not_read":
        "test_a_trailer_riding_a_commit_that_changed_the_work_is_not_read",
    "test_the_newest_attestation_at_a_tree_governs_the_cross_check":
        "test_the_newest_trailer_at_a_tree_governs_the_cross_check",
}

REGEX = [
    # --- test names: the route's own prefix (test_attest_refuses_..., ...)
    (r"\btest_attest_", "test_record_checks_"),
    # the default commit subject, before its `bar=review` moves below
    (r"\battest: \{\} bar=review", "record-checks: {} checks=commit"),
    # --- the trailer's grammar and values (a name after `\n` in a literal too)
    (r"(?:\b|(?<=\\n))Bar-Green\b", "Checks-Passed"),
    (r"\bbar=<review\|landing\|no-bar>", "checks=<commit|landing|none>"),
    (r"\bbar=<review\\\|landing\\\|no-bar>", r"checks=<commit\\|landing\\|none>"),
    (r"\bbar=<bar>", "checks=<checks>"),
    (r"\bbar=review\b", "checks=commit"),
    (r"\bbar=landing\b", "checks=landing"),
    (r"\bbar=no-bar\b", "checks=none"),
    (r"\bbar=\(\\S\+\)", r"checks=(\\S+)"),
    (r"\bbar=\{\}", "checks={}"),
    (r'"bar=" \+ bar\b', '"checks=" + bar'),
    (r"`bar=`", "`checks=`"),
    # --- the failed-checks headers
    (r"\bbar-red\b", "checks-failed"),
    (r"\bbar-summary\b", "checks-summary"),
    # --- the route on the command line
    (r"\battest --branch\b", "record-checks --branch"),
    (r"--bar review\b", "--checks commit"),
    (r'"--bar", "review"', '"--checks", "commit"'),
    (r'"attest", "--branch"', '"record-checks", "--branch"'),
    (r"\bintegrate\.py attest\b", "integrate.py record-checks"),
    (r'"\$SCRIPTS/integrate\.py" attest\b', '"$SCRIPTS/integrate.py" record-checks'),
    (r'(--root "\$REPO") attest\b', r"\1 record-checks"),
    (r"\b(integ|integrate|kv|kverdict)\.attest\b", r"\1.record_checks"),
    (r'\.record_checks\((.*?), "review"', r'.record_checks(\1, "commit"'),
    (r"`attest`", "`record-checks`"),
    (r"\ban `record-checks`", "a `record-checks`"),
    (r"-attest-message\b", "-checks-message"),
    (r'"\{\}-attest-\{\}"', '"{}-record-checks-{}"'),
    # --- the loop's log phase and its labels
    (r'phase="ATTEST"', 'phase="CHECKS"'),
    (r'"ATTEST " \+', '"CHECKS " +'),
    (r'== "ATTEST"', '== "CHECKS"'),
    (r'\(repo, 2, "ATTEST",', '(repo, 2, "CHECKS",'),
    (r"# phase: ATTEST\\n", r"# phase: CHECKS\\n"),
    (r"`ATTEST`", "`CHECKS`"),
    (r"\bATTEST (GREEN|RED)\b", lambda m: "CHECKS " + {"GREEN": "PASSED", "RED": "FAILED"}[m[1]]),
    (r"\ban ATTEST (log|record)\b", r"a CHECKS \1"),
    (r"\bthe ATTEST log\b", "the CHECKS log"),
    (r"\bown ATTEST log\b", "own CHECKS log"),
    # --- the values in code: `review` -> `commit`, `no-bar` -> `none`
    # (TOKENS run first, so these name the new constants)
    (r'\bCHECK_SETS = \("review", "landing", "no-bar"\)', 'CHECK_SETS = ("commit", "landing", "none")'),
    (r'\bLANDING_CHECK_SETS = \("landing", "no-bar"\)', 'LANDING_CHECK_SETS = ("landing", "none")'),
    (r'\.bar (==|!=) "review"', r'.bar \1 "commit"'),
    (r'\bbar="review"', 'bar="commit"'),
    (r'\bbar="no-bar" if skip_bar\b', 'bar="none" if skip_bar'),
    (r'(format_passed_checks\(tree, work), "review",', r'\1, "commit",'),
    (r'^(\s+tree, parent), "review", (kv\.tests_digest)', r'\1, "commit", \2'),
    (r'parametrize\("bar", \["review", "landing", "no-bar"\]\)', 'parametrize("bar", ["commit", "landing", "none"])'),
    (r'parametrize\("(bar|arm)", \["landing", "no-bar"\]\)', r'parametrize("\1", ["landing", "none"])'),
    (r'\.tests\) == \("review", "none"\)', '.tests) == ("commit", "none")'),
    (r'\.tests\) == \("no-bar", "none"\)', '.tests) == ("none", "none")'),
    (r"`landing` (or|and) `no-bar`", r"`landing` \1 `none`"),
    (r"`landing` / `no-bar`", "`landing` / `none`"),
    # --- prose naming the record
    (r"\b[Nn]o-bar attestation\b", "`checks=none` record"),
    (r"(?<![-\w])[Bb]ar[- ]attestation\b", "passed-checks record"),
    (r"\bcommit[- ]checks attestation\b", "commit-checks record"),
    (r"\bcommit checks' attestation\b", "commit checks' record"),
    (r"\b(the|a|its) `review` attestation\b", r"\1 `commit` record"),
    (r"\bverified `review` attestation\b", "verified `commit` record"),
    (r"\b(a|an) `bar=review` attestation\b", "a `checks=commit` record"),
    (r"`checks=commit` attestation\b", "`checks=commit` record"),
    (r"\breview-attestation walk\b", "commit-record walk"),
]

# The trailer's `bar` as a bare name, in the one module where it is only that
# (test_check_smoke_budget's `bar == "review"` is another thing).
SCOPED = [
    ("project-trajectory/scripts/integrate.py", r'\bbar (==|!=) "review"', r'bar \1 "commit"'),
]

PROTECT = list(_PROTECT) + [
    # the S3 method and retired names, spelled as they were
    r"make_attest_project",
    r"_attested_baseline",
    r"attestation-baseline",
    r"test_attestation_(?:digest|ledger)",
    r"RE-ATTESTATION[ -]PENDING",
    r"critique or attestation",
    r"an attestation, a demonstration",
    r"a rubric or an attestation",
    r"gate-attested",
    r"retired `attest` subcommand",
    r"`_cmd_attest` and the `attest` subparser",
    # `BAR_NAMES` had an earlier home: the retired stage axis (kitlib/ladder.py)
    r"`BAR_\*` ordinals, `BAR_NAMES`",
    r"`BAR_NAMES`/`BAR_ORDER`",
    r'"BAR_ORDER", "BAR_NAMES"',
    # 4.5.4: the cap's setting keeps its name until 10.7
    r"red_rounds_max",
    r"RED_ROUNDS_\w+",
]
