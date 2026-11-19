"""The requirement field in the forms the first rule set missed: as a Python
keyword argument, in the messages that name it, in prose that writes
`Verification=Critique`, and as a TOML key inside a Python string literal.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
]

REGEX = [
    (r"\bVerification(==?)", r"VerificationMethod\1"),
    (r"(['\"]|\\n)verification = (\\?\")", r"\1verification_method = \2"),
    (r"\b(whose|[Ii]ts|unless its) Verification (is|says)\b", r"\1 verification method \2"),
    (r"\bunless Verification is\b", "unless the verification method is"),
    (r"\bwhile Verification is\b", "while VerificationMethod is"),
    (r"\bVerification to Critique\b", "VerificationMethod to Critique"),
    (r"\bSR Verification methods\b", "SR verification methods"),
    (r"\bSR Verification\b", "SR VerificationMethod"),
    (r"\bVerification/Tier\b", "VerificationMethod/Tier"),
    (r"\(not Verification\)", "(not VerificationMethod)"),
]
