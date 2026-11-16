"""HANDOFF 10.5 pass 3, residue: the act-sense forms r45c's parts could not see.

Read off the leftovers after r45c/r45d (trap 28): uppercase verbs outside the
first-acceptance grammar rules ("the rows the verdict APPROVES", "AN OPERATOR
STILL APPROVES"), words with no part edge (`deapproved`, `DEAPPROVAL`,
`APPROVES` and `APPROVABLE` inside test names), and the adjective
"approvable", which has no direct twin: a tier an act accepts rows on is an
"acceptance tier"; a rung declared for the machine is "machine-acceptable".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT, RECORDS  # noqa: E402,F401
from r45c_accept import OTHER_APPROVALS, REVIEW_FILES  # noqa: E402

SKIP = RECORDS + HAND_ONLY + REVIEW_FILES + OTHER_APPROVALS + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
]

TOKENS = {
    "test_a_held_rung_APPROVE_row_owes_no_act": "test_a_held_rung_ACCEPT_row_owes_no_act",
    "test_an_explicit_APPROVES_ref_authorises_it_and_is_RECORDED": "test_an_explicit_ACCEPTS_ref_authorises_it_and_is_RECORDED",
    "test_the_four_APPROVABLE_rungs_answer_exactly_as_they_did_before_the_ladder": "test_the_four_ACCEPTANCE_rungs_answer_exactly_as_they_did_before_the_ladder",
    "deapproved_id": "deaccepted_id",
    "_deapproved": "_deaccepted",
}

PARTS = {
    "DEAPPROVAL": "DEACCEPTANCE",
}

REGEX = [
    (r"\b(An?|AN) OPERATOR STILL APPROVES\b", r"\1 OPERATOR STILL ACCEPTS"),
    (r"\bverdict APPROVES\b", "verdict ACCEPTS"),
    (r"\bsection APPROVES\b", "section ACCEPTS"),
    (r"\bapprovable (TIERS|tiers?|fold)\b", r"acceptance \1"),
    (r"\bAPPROVABLE(-TIER| tiers)\b", r"ACCEPTANCE\1"),
    (r"\bmachine-approvable\b", "machine-acceptable"),
    (r"\belement is un-approvable,", "element can never be accepted,"),
]
