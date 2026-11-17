"""HANDOFF 4.5.2 (ruled 2026-11-16 with 12.4's change): the work-item key `bar`
becomes `checks_stage`, the stage a row pins its landing checks to.

The key itself (frontmatter `bar`, row column `Bar`, the drafted-row key in a
`## Dispositions` block) is a quoted string in a handful of places, so it moves
by hand (`h47a.py`); the stored values move by the migrator's `work item` step.
This file renames the identifiers named after the key, and the tests named for
it (D4), with the evidence cells that cite them.

Not this file:
- `_RETIRED_WI_BARS` (intake.py) and `_RETIRED_BARS` (integrate.py): readers of
  the retired `G1`..`G3` and `DevBar-*` values, kept under the retired word
  until D11's change, as 4.5.5 says for every such table.
- "bar" for running checks (`_run_bar`, `_refresh_bar`, the no-bar arm):
  10.7's later concept.
- Python locals and parameters named `bar` (`pyname.py`, `n47a_names.py`).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
    # ratchet histories: each entry quotes the names of its day
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
    "docs/complexity-baseline",
]

TOKENS = {
    # the key's value vocabulary, one copy in each reader (F5)
    "WI_BARS": "WI_CHECKS_STAGES",
    "_BAR_GATES": "_CHECKS_STAGES",
    "normalize_bar": "normalize_checks_stage",
    "_normalize_bar": "_normalize_checks_stage",
    # integrate.py: the claimed row's say over the landing checks, and the
    # refusal when no check suite is declared to run
    "_lane_bar_directives": "_lane_checks_directives",
    "_declared_bar_or_refusal": "_declared_checks_or_refusal",
    "bar_gate": "checks_stage",
    # tests (D4), with the evidence cells that cite them
    "test_the_bar_key_reaches_check_gate": "test_the_checks_stage_key_reaches_check_py",
    "test_without_a_bar_key_the_refresh_passes_no_stage":
        "test_without_a_checks_stage_key_the_refresh_passes_no_stage",
    "test_a_malformed_bar_value_refuses_the_refresh": "test_a_malformed_checks_stage_refuses_the_refresh",
    "test_the_bar_cell_round_trips_and_a_context_body_is_read_past":
        "test_the_checks_stage_cell_round_trips_and_a_context_body_is_read_past",
    "test_the_bar_key_is_carried_by_every_reader": "test_the_checks_stage_key_is_carried_by_every_reader",
}

PROTECT = list(_PROTECT)
