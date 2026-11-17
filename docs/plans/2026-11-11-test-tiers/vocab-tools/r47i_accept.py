"""HANDOFF 10.7 item 3 (4.4's last paragraph): plain "accept" where a reader
could take it for the act (accepting a row). The candidates 10.7 noted are
test names: a verdict, a ruling, a typed line, an adoption record, an open
item's table, a review session, a sitting and a record each "accepted" by a
reader or a check, which in this kit now reads as the operator's act. Each
says what happens instead: it is read, it passes, it is valid, it is taken.

Left as they are: "accept" for a value a parser or reader takes (`a quoted
rev value is accepted`, `a padded value is accepted as the reader reads it`,
`large weight is accepted`), which no reader takes for the act, and every
name about accepting rows, which is the act.
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
    "test_a_well_formed_verdict_is_accepted_and_parsed": "test_a_well_formed_verdict_is_read_and_parsed",
    "test_a_successor_ruling_is_accepted_and_parsed": "test_a_successor_ruling_is_read_and_parsed",
    "test_a_well_formed_typed_line_is_accepted_for_every_brief":
        "test_a_well_formed_typed_line_is_read_for_every_brief",
    "test_a_clean_review_session_is_accepted": "test_a_clean_review_session_passes",
    "test_the_typed_open_item_table_is_accepted_whole": "test_the_typed_open_item_table_is_read_whole",
    "test_the_same_ruling_with_the_done_when_updated_is_accepted":
        "test_the_same_ruling_with_the_done_when_updated_passes",
    "test_a_row_closed_in_the_ruling_commit_is_accepted": "test_a_row_closed_in_the_ruling_commit_passes",
    "test_an_adoption_that_is_not_accepted_refuses_the_close": "test_an_invalid_adoption_refuses_the_close",
    "test_acceptance_is_read_against_the_registry_with_distinct_refusals":
        "test_validity_is_read_against_the_registry_with_distinct_refusals",
    "test_the_loop_route_accepts_a_combined_sitting_on_its_bound_kinds":
        "test_the_loop_route_takes_a_combined_sitting_on_its_bound_kinds",
    "test_the_review_render_accepts_what_record_checks_writes":
        "test_the_review_render_reads_what_record_checks_writes",
    "test_the_entry_point_accepts_the_dispute_class": "test_the_entry_point_takes_the_dispute_class",
    "test_the_worker_preflight_accepts_the_resumed_finished_lane":
        "test_the_worker_preflight_passes_the_resumed_finished_lane",
}

PROTECT = list(_PROTECT)
