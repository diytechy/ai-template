"""HANDOFF 4.2 / 10.5 pass 4: the status, the record and the ledger.

The status a row holds once accepted, `Approved`, becomes `Accepted`, and
with it every form the earlier passes held back: the constant `APPROVED`
(`SPINE_APPROVED_CELLS`, `_APPROVED_TEXT`, `BIF_APPROVED`), the predicate
`is_approved`, every quoted "approved" (the status read case-folded, the act
ledger's key and the cell class: all three become "accepted"), the
backticked `approved`, the lowercase status in CSV fixtures, the record's
directory `last_approved` (and its README template `last-approved-README`),
and the ledger's keys `approved` / `reattested` (`reaccepted`).

Stored values are the migrator's, not this file's: the status cells of the
live registries (r45g leaves them for it), the record directory itself and
its ledger, which the migrator moves and re-keys.

NOT in this pass:
- The review-round modules (r45c's REVIEW_FILES) stay skipped: their
  "approved" is a reviewer's (D12). Two status fixtures in one of them are
  hand edits (h45g).
- The retired off-spine column `Approval` and its values, as history notes
  spell them (`Approval == "approved"`, `` `draft`/`approved` ``).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402
from r45c_accept import OTHER_APPROVALS, REVIEW_FILES  # noqa: E402

LIVE_REGISTRIES = [
    "docs/requirements/*.toml",
    "docs/requirements/*.csv",
    "docs/test/*.toml",
    "docs/test/*.csv",
]

SKIP = RECORDS + HAND_ONLY + REVIEW_FILES + OTHER_APPROVALS + LIVE_REGISTRIES + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
]

PARTS = {
    "Approved": "Accepted",
    "APPROVED": "ACCEPTED",
    "approved": "accepted",
    "unapproved": "unaccepted",
    "reattested": "reaccepted",
}

PROTECT = list(_PROTECT) + [
    r"\bwi-?\d+[a-z]?-[A-Za-z0-9_-]+",
    r"human_approval_through",
    r"single[-_]approv\w*",
    # the retired column's values, as history notes spell them
    r"[Aa]pproval\s*==?\s*\"approved\"",
    r"`draft`/`approved`",
    r"both became `approved`",
    # an external skill's own review status
    r"unapproved external review copy",
    # a reviewer's or a critic's approval (D12)
    r"review round approved",
    r"rounds had approved",
    r"honestly-approved",
    r"approved lane",
    r"approved perceptual stamp",
    r"approved deviation register",
]
