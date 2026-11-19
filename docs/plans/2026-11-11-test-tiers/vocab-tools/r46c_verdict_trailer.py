"""HANDOFF 10.6: the `Review-Verdict:` trailer in tests/test_verdict_record.py.

That module called the verdict trailer an "attestation" throughout. It is a
script-written trailer naming the tree a round judged, and the code's own word
for it is "trailer"; with the passed-checks record renamed, "attestation" would
otherwise be left naming only this. Its two "attestor"s are the mechanical-close
peel (`mechanical_close_peel`). One file only: every other file outside it is
skipped.
"""

import fnmatch
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import PROTECT as _PROTECT  # noqa: E402

ONLY = ["tests/test_verdict_record.py"]
_TRACKED = subprocess.run(
    ["git", "-C", "C:/Projects/ai-template-wt-vocabulary", "ls-files"],
    capture_output=True, text=True, encoding="utf-8", check=True,
).stdout.splitlines()
SKIP = [rel for rel in _TRACKED if not any(fnmatch.fnmatch(rel, g) for g in ONLY)]

REGEX = [
    (r"\bAn attestation\b", "A trailer"),
    (r"\ban attestation\b", "a trailer"),
    (r"\battestations\b", "trailers"),
    (r"\battestation\b", "trailer"),
    (r"\ban attestor\b", "a peel"),
    (r"\battestor\b", "peel"),
]

PROTECT = list(_PROTECT)
