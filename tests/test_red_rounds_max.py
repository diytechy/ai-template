"""`[build] red_rounds_max`, the red-round cap's one reader, in-process.

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


def write_toml(root, text):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    with (root / "docs" / "process.toml").open(
        "w", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write(text)


@pytest.mark.parametrize(
    "body, value",
    [
        # The shipped default for an absent table or key. Green on the stub
        # too, which answers the shipped 3; the adequacy witness is a reader
        # that answers anything else, or refuses, for a file that is silent.
        pytest.param("", 3, id="absent-table"),
        pytest.param("\n[build]\n", 3, id="absent-key"),
        pytest.param("\n[build]\nred_rounds_max = 0\n", None, id="0"),
        pytest.param("\n[build]\nred_rounds_max = -1\n", None, id="-1"),
        pytest.param("\n[build]\nred_rounds_max = true\n", None, id="true"),
        pytest.param('\n[build]\nred_rounds_max = "3"\n', None, id="string"),
        pytest.param("\n[build]\nred_rounds_max = 3.0\n", None, id="float"),
    ],
)
def test_red_rounds_max_reads_3_when_absent_and_refuses_each_bad_value(
    tmp_path, body, value
):
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
    assert "red_rounds_max" in refusal
