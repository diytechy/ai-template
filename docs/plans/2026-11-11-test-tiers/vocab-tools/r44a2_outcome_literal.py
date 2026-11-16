"""The outcome value as a bare string literal in tests (positional arguments,
parametrize ids, tuples). Every "accepted" literal under tests/ was read on
2026-11-11 and each is the binding's outcome value."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS

SCOPED = [
    ("tests/*.py", r'"accepted"', '"recorded"'),
]
