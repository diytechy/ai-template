"""HANDOFF 10.5 pass 3, correction: `is_approved` waits for pass 4.

r45c renamed the predicate with every other name on "approved". But
tests/test_rule_sync.py derives each status predicate's name from the status
word (`"is_" + value.lower()`), so the predicate and the status `Approved`
must move together, in pass 4. This puts the name back; it did not exist as
`is_accepted` before r45c (checked: zero uses at the pass-2 commit).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
]

TOKENS = {
    "is_accepted": "is_approved",
    "test_is_accepted_agrees": "test_is_approved_agrees",
}
