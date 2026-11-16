"""HANDOFF 4.3 / 10.4: the role uses of "owner" inside the interface files.

r43b_owner.py skips these files whole, because there "the owner" is nearly
always an interface row's providing side. This file reaches only them, and only
through phrases that name the role and nothing else: a dated citation of a
ruling, the role's queue, surface and decision view, the renamed symbols. The
remaining role sentences are hand edits (h43c.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import PROTECT  # noqa: E402,F401
from r43b_owner import INTERFACE_FILES  # noqa: E402

SKIP = ["*"]
EXTRA = list(INTERFACE_FILES)

TOKENS = {
    "owner_cards": "operator_cards",
    "owner_state": "operator_state",
    # named in IF rows' data cells (found by a scan of r43b's TOKENS here)
    "OWNER_KEY": "OPERATOR_KEY",
    "OWNER_VALUES": "OPERATOR_VALUES",
}

PARTS = {
    "owner-ruled": "operator-ruled",
    "owner-registry": "operator-registry",
}

REGEX = [
    (r"\b([Oo])wner (rulings?|directives?|decision (?:view|queue|registry)|queue|surface)\b",
     lambda m: ("O" if m[1] == "O" else "o") + "perator " + m[2]),
    (r"\bOWNER RULING", "OPERATOR RULING"),
    (r"the owner's own addition", "the operator's own addition"),
    (r"The owner's ruled typing", "The operator's ruled typing"),
]
