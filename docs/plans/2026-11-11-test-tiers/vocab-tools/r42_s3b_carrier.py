"""The CSV-to-TOML converter and its tests: the current header and key.

migrate_carrier.py converts a registry between the kit's two live carriers, so
it knows the current column name. Knowledge of the earlier one lives in
migrate_vocabulary.py alone.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import PROTECT  # noqa: E402,F401

_FILES = ("project-trajectory/scripts/migrate_carrier.py", "tests/test_migrate_carrier.py")

SCOPED = []
for _f in _FILES:
    SCOPED += [
        (_f, r'"Verification": "verification"', '"VerificationMethod": "verification_method"'),
        (_f, r'(["\'])Verification\1', r"\1VerificationMethod\1"),
        (_f, r"(?m)^(\s*)verification(\s*=\s*\")", r"\1verification_method\2"),
        (_f, r",Verification(?=,|\"|\\n|$)", ",VerificationMethod"),
        (_f, r"\| Verification \|", "| VerificationMethod |"),
        (_f, r"`Verification`", "`VerificationMethod`"),
        (_f, r'"Attest"', '"Vouch"'),
        (_f, r",Attest,", ",Vouch,"),
        (_f, r"`Attest`", "`Vouch`"),
    ]
