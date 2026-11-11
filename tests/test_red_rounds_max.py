"""`[build] stop_lane_after_consecutive_commit_check_failures`, the commit-check
failure cap's one reader, in-process.

The reader's table lives here, in the per-commit tier, rather than beside the
hook-driven `docs/process.toml` contract in `test_process_config` (a slow
module): it is a pure unit of `kitlib.config.red_rounds_max` over a temp file,
and the review-gate family's subprocess cases call the same reader through the
real loop.
"""

import pytest
from conftest import load_script

# `load_script` puts scripts/ on sys.path; the reader is imported after it.
load_script("agent_common")
from kitlib import config as kconfig  # noqa: E402

_TRUNK = '[policies]\ntrunk = "main"\n'
KEY = "stop_lane_after_consecutive_commit_check_failures"
# The key's name before the rename: refused where it is still declared.
RETIRED_KEY = "red_rounds_max"


def write_toml(root, text):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    with (root / "docs" / "process.toml").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write(text)


def _build(value, key=KEY):
    """A `[build]` table declaring `key = value`, on the file's fifth line."""
    return "\n[build]\n{} = {}\n".format(key, value)


@pytest.mark.parametrize(
    "body, value",
    [
        # The shipped default for an absent table or key. Green on the stub
        # too, which answers the shipped 3; the adequacy witness is a reader
        # that answers anything else, or refuses, for a file that is silent.
        pytest.param("", 3, id="absent-table"),
        pytest.param("\n[build]\n", 3, id="absent-key"),
        # A declared value is the one read: a reader that still looked the
        # retired name up would answer the shipped 3 here.
        pytest.param(_build(5), 5, id="declared"),
        pytest.param(_build(0), None, id="0"),
        pytest.param(_build(-1), None, id="-1"),
        pytest.param(_build("true"), None, id="true"),
        pytest.param(_build('"3"'), None, id="string"),
        pytest.param(_build(3.0), None, id="float"),
    ],
)
def test_red_rounds_max_reads_3_when_absent_and_refuses_each_bad_value(
    tmp_path, body, value
):
    """Implements: TC-382"""
    # TC-382. An absent `[build]` table or key reads the shipped 3; a value
    # that is not an int, is a bool, or is below 1 is refused, naming the
    # file, its line and the key.
    write_toml(tmp_path, _TRUNK + body)
    got, refusal = kconfig.red_rounds_max(tmp_path)
    if value is not None:
        assert (got, refusal) == (value, None)
        return
    assert got is None, got
    assert refusal and "docs/process.toml:5" in refusal, refusal
    assert "[build] {} = ".format(KEY) in refusal


@pytest.mark.parametrize(
    "body",
    [
        pytest.param(_build(5, RETIRED_KEY), id="alone"),
        # Beside the new key too: the old line is a dial somebody believes
        # is set, so it is never passed over for the one that is read.
        pytest.param(
            _build(5, RETIRED_KEY) + "{} = 4\n".format(KEY), id="beside-the-new"
        ),
    ],
)
def test_the_retired_key_is_refused_naming_the_new_one(tmp_path, body):
    """Implements: TC-382"""
    # TC-382. The key was renamed. A file still declaring the old name is
    # refused, naming its line, the old name and the name to rename it to: a
    # renamed dial read as absent would silently restore the shipped 3.
    write_toml(tmp_path, _TRUNK + body)
    got, refusal = kconfig.red_rounds_max(tmp_path)
    assert got is None, got
    assert refusal.startswith(
        "docs/process.toml:5: [build] {} was renamed {}; rename the key".format(
            RETIRED_KEY, KEY
        )
    ), refusal
