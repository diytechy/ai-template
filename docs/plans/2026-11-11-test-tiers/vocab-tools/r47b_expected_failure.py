"""HANDOFF 4.5.4 (ruled 2026-11-16): the reader of the two declared values the
commit checks need, and the commit-check failure cap's reader.

- `git mv` first: `kitlib/red_mark.py` -> `kitlib/expected_failure.py`,
  `tests/test_red_mark.py` -> `tests/test_expected_failure.py`,
  `tests/test_red_mark_lane.py` -> `tests/test_expected_failure_lane.py`,
  `tests/test_red_rounds_max.py` -> `tests/test_commit_check_failure_cap.py`.
- Then this file: the module's path and import names, `Bars` ->
  `CommitCheckSettings`, `read_bars` -> `read_commit_check_settings`, the
  `RED_ROUNDS_*` constants, the test modules and the tests named for the old
  words (D4), with the evidence cells that cite them.

Not this file:
- `red_rounds_max`, which is also the retired key's spelling inside strings
  (`FAILURE_CAP_RETIRED_KEY = "red_rounds_max"`, the tests' `RETIRED_KEY`):
  renamed by token with `pyname.py` (`n47b_names.py`), so the strings keep it.
- The fields `review` and `red_mark` of the settings, and the `bars` locals:
  `n47b_names.py`. The cause keys and refusal arguments that name the fields
  as strings, and the retired `[bars]` key names that stay: `h47d.py`.
- `RETIRED = "bars"` and `_RETIRED_*` tables: readers of the retired spelling.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
    "docs/test/observations/*",
    "tests/test_module_size_ratchet.py",
    "tests/test_complexity_ratchet.py",
    "docs/complexity-baseline",
    # dated coordinator handoffs: their "**Bars:**" headings are records
    "docs/handoff-*",
]

TOKENS = {
    "Bars": "CommitCheckSettings",
    "read_bars": "read_commit_check_settings",
    "_kitredmark": "_kitexpected",
    "krm": "kef",
    "RED_ROUNDS_KEY": "FAILURE_CAP_KEY",
    "RED_ROUNDS_RETIRED_KEY": "FAILURE_CAP_RETIRED_KEY",
    "RED_ROUNDS_MAX_DEFAULT": "FAILURE_CAP_DEFAULT",
    # the tests' fixture values
    "BARS_RED_MARK": "MARKER_DECLARATION",
    "RED_MARK": "EXPECTED_FAILURE_MARKER",
    # test modules, and the evidence cells and pins that name them
    "test_red_mark_lane": "test_expected_failure_lane",
    "test_red_mark": "test_expected_failure",
    "test_red_rounds_max": "test_commit_check_failure_cap",
    # tests (D4)
    "test_red_rounds_max_reads_3_when_absent_and_refuses_each_bad_value":
        "test_the_failure_cap_reads_3_when_absent_and_refuses_each_bad_value",
    "test_a_bad_red_rounds_max_refuses_before_any_session":
        "test_a_bad_failure_cap_refuses_before_any_session",
    "test_the_bar_and_the_mark_come_from_one_parse":
        "test_the_commit_checks_and_the_marker_come_from_one_parse",
    "test_the_hand_landing_checks_the_staged_squash_for_a_red_mark":
        "test_the_hand_landing_checks_the_staged_squash_for_an_expected_failure_marker",
}

REGEX = [
    (r"kitlib/red_mark\.py", "kitlib/expected_failure.py"),
    (r"kitlib\.red_mark\b", "kitlib.expected_failure"),
    (r"\bfrom kitlib import red_mark as\b", "from kitlib import expected_failure as"),
]

PROTECT = list(_PROTECT)
