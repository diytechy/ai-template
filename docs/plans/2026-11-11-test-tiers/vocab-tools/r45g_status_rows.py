"""HANDOFF 10.5 pass 4: r45f's rules inside the live registries only.

The rows' text (an `Approved` row, `last_approved`, the ledger's keys named
in IF data, `is_approved` in code-symbol cells) moves with the code. The
`status` cell of each row is a stored value: `migrate_vocabulary.py` rewrites
it, proved by a re-parse, so that this repository's migration exercises the
same step an adopter's does. It is protected here.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from r45f_status import LIVE_REGISTRIES, PARTS, PROTECT as _PROTECT  # noqa: E402,F401

SKIP = ["*"]
# The registries check_vocab reads as live, named one by one: EXTRA bypasses
# that scope, and `open-items.toml` is a record of rulings (exempt there), so
# a glob would reach it. Found the hard way in the first dry run.
EXTRA = [
    "docs/requirements/assumptions.toml",
    "docs/requirements/components.derived.toml",
    "docs/requirements/components.toml",
    "docs/requirements/external.toml",
    "docs/requirements/hats.toml",
    "docs/requirements/interfaces.toml",
    "docs/requirements/low-level-requirements.toml",
    "docs/requirements/performance-budgets.csv",
    "docs/requirements/stakeholder-needs.toml",
    "docs/requirements/system-requirements.toml",
    "docs/test/test-cases.toml",
]

PROTECT = list(_PROTECT) + [
    r"(?<=status = \")Approved(?=\")",
]
