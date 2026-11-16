"""HANDOFF 4.2 / 10.5 pass 1: re-attest becomes re-accept.

The act repeated after an amendment. Names (`reattest_model`, `reattest_lines`,
`parse_reattests`, `reattested_between`, `_REATTEST_*_H`, the in-memory kind
"reattest", the flag `--reattests`), test names, prose ("re-attestation
brief") and printed labels (`RE-ATTESTED:`) move together.

NOT in this pass:
- The bare token `reattested`: it is the act ledger's stored key in
  `docs/archive/last_approved/acts.toml` (`reattested = [...]`, read as
  `act["reattested"]`), and the variables beside the ledger code carry its
  name. All of it moves in pass 4, with the record and a migrator step, so it
  is protected here. Names that merely contain it (`_reattested_ids`, a test
  name ending `_is_reattested`) are not the key, and move.
- `--approves` and the in-memory kind "approve": pass 3, with every other
  "approve" (`args.approves` and the flag move in one rule there).
- `RE-ATTESTATION-PENDING`: a retired commit-message convention, named as it
  was spelled.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
]

# Snake and kebab parts (underscore and hyphen are edges), so test names and
# compound identifiers move with the word.
PARTS = {
    "reattestations": "reacceptances",
    "reattestation": "reacceptance",
    "reattesting": "reaccepting",
    "reattests": "reaccepts",
    "reattested": "reaccepted",
    "reattest": "reaccept",
    "Reattestation": "Reacceptance",
    "Reattest": "Reaccept",
    "REATTEST": "REACCEPT",
    "re_attestation": "re_acceptance",
    "re_attested": "re_accepted",
}

REGEX = [
    (r"\b([Rr])e-attestations\b", r"\1e-acceptances"),
    (r"\b([Rr])e-attestation\b", r"\1e-acceptance"),
    (r"\b([Rr])e-attesting\b", r"\1e-accepting"),
    (r"\b([Rr])e-attests\b", r"\1e-accepts"),
    (r"\b([Rr])e-attested\b", r"\1e-accepted"),
    (r"\b([Rr])e-attest\b", r"\1e-accept"),
    (r"\bRE-ATTESTATIONS\b", "RE-ACCEPTANCES"),
    (r"\bRE-ATTESTATION\b", "RE-ACCEPTANCE"),
    (r"\bRE-ATTESTED\b", "RE-ACCEPTED"),
    (r"\bRE-ATTEST\b", "RE-ACCEPT"),
]

PROTECT = list(_PROTECT) + [
    # the ledger key and its namesakes: pass 4
    r"(?<![A-Za-z0-9_])reattested(?![A-Za-z0-9_])",
    # ...and after an escape inside a string literal (trap 20): a TOML fixture
    # in test_baseline_snapshot writes the ledger as "...\nreattested = []\n"
    r"(?<=\\n)reattested(?![A-Za-z0-9_])",
    r"RE-ATTESTATION[ -]PENDING",
]
