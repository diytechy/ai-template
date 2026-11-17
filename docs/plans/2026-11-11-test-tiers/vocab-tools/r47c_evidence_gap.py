"""HANDOFF 4.5.3 (ruled 2026-11-16): a "red TC" is an **evidence gap**.

A test case that is not accepted although every requirement it verifies is
cited by a work item recorded done. The census that finds them is already the
gap census, so the names follow it.

- `git mv` first: `prompts/adjudicate-red-tc.template.md` ->
  `prompts/adjudicate-evidence-gap.template.md` (regenerate the catalogue).
- The brief kind `red-tc` is `evidence-gap`, with the prompt-map key
  `ADJUDICATE-EVIDENCE-GAP`, in code, templates and tests. It is stored in
  `docs/process.toml` `[adjudicator] retain_for`, which this file skips: the
  migrator's `POLICY_ITEMS` respells it there (`h47f_migrator.py`), as it did
  `first-approval`. Old verdict files and bindings keep the kind (D15).
- The census line grammar (`"red TC "`, `"red assumption TC "`) is printed
  and parsed live, never stored, so it moves by hand (`h47f.py`) with the
  sentences around it.

Not this file: "red" for a failing check run (4.5.6).
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
    # the stored brief kind moves through the migrator
    "docs/process.toml",
]

TOKENS = {
    "red_tc_census": "evidence_gap_census",
    "parse_red_tc": "parse_evidence_gap",
    "red_tc_values": "evidence_gap_values",
    "RED_TC_PREFIX": "EVIDENCE_GAP_PREFIX",
    "RED_ASSUMPTION_TC_PREFIX": "ASSUMPTION_GAP_PREFIX",
    "ADJUDICATE_RED_TC": "ADJUDICATE_EVIDENCE_GAP",
    "_TC_NOT_RED": "_GAP_EXEMPT_STATUSES",
    "_RED_TC_RE": "_EVIDENCE_GAP_RE",
    "_red_assumption_census": "_assumption_gap_census",
    "_red_tc_line": "_evidence_gap_line",
    "_red_tc_draft": "_evidence_gap_draft",
    "_red_tc_context": "_evidence_gap_context",
    # tests: helpers and fixtures
    "_red_tc_repo": "_evidence_gap_repo",
    "RED_TC_ROW": "EVIDENCE_GAP_ROW",
    "red_tc": "evidence_gap",
    # tests (D4), with the evidence cells that cite them
    "test_a_red_tc_under_a_closed_row_is_named": "test_an_evidence_gap_under_a_closed_row_is_named",
    "test_parse_red_tc_returns_None_for_every_other_census_line":
        "test_parse_evidence_gap_returns_None_for_every_other_census_line",
    "test_the_red_tc_census_rides_the_gap_census_seam":
        "test_the_evidence_gap_census_rides_the_gap_census_seam",
    "test_the_red_tc_line_grammar_round_trips": "test_the_evidence_gap_line_grammar_round_trips",
    "test_a_minted_red_tc_row_reaches_the_FRONTIER": "test_a_minted_evidence_gap_row_reaches_the_FRONTIER",
    "test_a_red_tc_mints_an_ADJUDICATION_row_not_an_ordinary_gap_row":
        "test_an_evidence_gap_mints_an_ADJUDICATION_row_not_an_ordinary_gap_row",
    "test_a_red_tc_rows_session_receives_the_red_tc_brief":
        "test_an_evidence_gap_rows_session_receives_the_evidence_gap_brief",
    "test_the_red_tc_brief_carries_the_live_census_and_the_obligation_it_covers":
        "test_the_evidence_gap_brief_carries_the_live_census_and_the_obligation_it_covers",
    "test_the_red_tc_brief_names_all_three_readings_without_choosing":
        "test_the_evidence_gap_brief_names_all_three_readings_without_choosing",
    "test_the_red_tc_draft_declares_NO_planmode": "test_the_evidence_gap_draft_declares_NO_planmode",
    "test_the_red_tc_tier_is_ESTIMATED_from_breadth_not_defaulted":
        "test_the_evidence_gap_tier_is_ESTIMATED_from_breadth_not_defaulted",
    "test_a_partial_close_never_makes_a_tc_red": "test_a_partial_close_never_makes_an_evidence_gap",
    "test_a_tc_verifying_a_MIX_of_claimed_and_unclaimed_is_not_red":
        "test_a_tc_verifying_a_MIX_of_claimed_and_unclaimed_is_no_evidence_gap",
    "test_an_OPEN_row_never_makes_a_tc_red": "test_an_OPEN_row_never_makes_an_evidence_gap",
    "test_the_three_exempt_statuses_are_never_red": "test_the_three_exempt_statuses_are_never_an_evidence_gap",
}

PARTS = {
    # the brief kind, the prompt file's name and the prompt-map key
    "red-tc": "evidence-gap",
    "RED-TC": "EVIDENCE-GAP",
}

REGEX = [
    # prose: the hyphenated form is an adjective ("the red-TC census"), the
    # spaced form a noun ("a red TC"); an article before either takes "an"
    (r"\b([Aa]) red-TC\b", r"\1n evidence-gap"),
    (r"\b([Aa]) red TC\b", r"\1n evidence gap"),
    (r"\bred-TC\b", "evidence-gap"),
    (r"\bred TCs\b", "evidence gaps"),
    (r"\bred TC's\b", "evidence gap's"),
    (r"\bred TC\b(?! TC-)", "evidence gap"),
    (r"\bTHE RED-TC\b", "THE EVIDENCE-GAP"),
    (r"\ba red test case\b", "an evidence gap"),
]

PROTECT = list(_PROTECT) + [
    # census lines quoted in tests: the grammar moves by hand with its producer
    r"\"red TC TC-[^\"]*\"",
    r"red assumption TC ",
]
