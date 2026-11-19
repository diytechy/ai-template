"""HANDOFF 4.2 / 10.5 pass 2: the kind and the class.

- The brief kind `first-approval` becomes `first-acceptance` everywhere live,
  with `FIRST-APPROVAL`, `ADJUDICATE_FIRST_APPROVAL`, every snake name built
  on `first_approval` (test names included, and the evidence cells that cite
  them), and the prompt file `adjudicate-first-approval.template.md` (moved
  with `git mv` after this file is applied; its references move here).
- The work-item safety class `attestation` (VOCABULARY.md 3, S5) becomes
  `acceptance`: a row that closes an acceptance window. Only its own forms
  move (`attestation`/`gate`, the pipe lists, `"attestation"` as a kind in
  the scheduler, dispatcher and their tests, "attestation row(s)"). Other
  senses of "attestation" in the same files wait: the passed-checks record
  (S1) for 10.6, the act itself (S6) for pass 3.

NOT in this pass:
- Two-word prose "first approval": pass 3, where `approval` becomes
  `acceptance` everywhere at once.
- `docs/process.toml`: its `[adjudicator] retain_for` holds the kind as a
  stored value, which the migrator rewrites (its prose waits for pass 3).
- Records keep the kind as written (D15): `kinds = ...first-approval` in the
  bindings and the verdict files under docs/reviews, `brief = "first-approval"`
  in archived work items. None of them is on the live surface.
- `bootstrap.py`'s `_migrate_dial_key_name` passes the string "attestation"
  as a TABLE name, a form the dial concept missed (it is split over lines):
  that is a hand edit to "authority" (h45b), not this class.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/process.toml",
]

PARTS = {
    "first-approval": "first-acceptance",
    "first_approval": "first_acceptance",
    "First-approval": "First-acceptance",
    "FIRST-APPROVAL": "FIRST-ACCEPTANCE",
    "FIRST_APPROVAL": "FIRST_ACCEPTANCE",
}

# The safety class, in the files that hold it (found by inventory: the
# scheduler, the dispatcher, their tests, the templates that list the classes,
# and the registry rows describing the dispatcher).
_CLASS_FILES = [
    "project-trajectory/scripts/schedule.py",
    "project-trajectory/scripts/dispatch.py",
    "project-trajectory/scripts/agent_policy.py",
    "project-trajectory/README.md",
    "project-trajectory/work/WI-000.template.md",
    "project-trajectory/registries/work-items.template.csv",
    "docs/requirements/low-level-requirements.toml",
    "docs/test/test-cases.toml",
    "tests/test_schedule.py",
    "tests/test_dispatch.py",
    "tests/test_dispatch_admission.py",
    "tests/test_approval_level.py",
    # found after the first apply: frontier fixtures of the dispatcher's order
    "tests/test_loop_order.py",
]

_CLASS_RULES = [
    # the declared vocabulary, as a pipe list
    (r"\bgate\|attestation\|", "gate|acceptance|"),
    # the kind as a Python string: the scheduler's tables, the dispatcher's
    # arm, and the tests' frontier fixtures
    (r"(?<![A-Za-z0-9_])\"attestation\"(?=[,:)])", '"acceptance"'),
    # prose naming the class
    (r"`attestation`/`gate`", "`acceptance`/`gate`"),
    (r"\battestation/gate\b", "acceptance/gate"),
    (r"\bgate/attestation\b", "gate/acceptance"),
    (r"\battestation, gate\b", "acceptance, gate"),
    (r"\battestation or gate row", "acceptance or gate row"),
    (r"\battestation (rows?\b|row\(s\))", r"acceptance \1"),
    (r"\battestation still drains", "acceptance row still drains"),
]

SCOPED = [(glob, pat, repl) for glob in _CLASS_FILES for pat, repl in _CLASS_RULES]
