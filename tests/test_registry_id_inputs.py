"""A registry row id as an observation case's declared input (TC-276).

An observation case may name a registry row by its id (`SR-184`) instead of a
file, and what its judgment reads is then that row's cells. Two readers must
agree on that, and this module pins both on a small registry under tmp_path
(no scaffold, no git: the link set is handed in):

- the re-judge checkpoint's support paths (`rejudge._support_paths`) read the
  registry directories for an id, never a file named after the id;
- the writer's digest (`record_observation.inputs_digest`) follows the named row
  alone, so an edit to another row leaves it unchanged and an edit to the named
  row moves it.

The declaration half (an id is never an escaping path) is pinned beside the
other input rules in `tests/test_assumption_rules.py`.
"""

from conftest import load_script

WRITER = load_script("record_observation")
REJUDGE = load_script("rejudge")

SRS = """[requirement.SR-184]
title = "The inspected row"
requirement = "The delivered record shall name its rubric."
status = "Approved"

[requirement.SR-185]
title = "Its neighbour"
requirement = "The delivered review shall name its counterpart."
status = "Approved"
"""


def _repo(tmp_path):
    reqs = tmp_path / "docs" / "requirements"
    reqs.mkdir(parents=True)
    (reqs / "system-requirements.toml").write_text(SRS, encoding="utf-8")
    return tmp_path


def _digest(root, names):
    return WRITER.inputs_digest(root, names, links=frozenset())


def test_a_row_id_selects_the_registry_support_paths_not_a_file():
    paths = REJUDGE._support_paths(["SR-184"])
    assert "SR-184" not in paths
    assert set(WRITER.REGISTRY_DIRS) <= set(paths)
    # A path input is its own support path, and adds no registry directory.
    assert REJUDGE._support_paths(["docs/test/inspection-procedures.md"]) == [
        "docs/test/inspection-procedures.md"
    ]


def test_changing_only_the_named_row_changes_its_digest(tmp_path):
    root = _repo(tmp_path)
    srs = root / "docs" / "requirements" / "system-requirements.toml"
    before = _digest(root, ["SR-184"])
    # The id resolves to the row, not to an absent file of that name.
    assert before != _digest(root, ["SR-999"])
    # Another row's edit leaves the named row's digest alone...
    srs.write_text(
        srs.read_text(encoding="utf-8").replace("its counterpart", "its partner"),
        encoding="utf-8",
    )
    assert _digest(root, ["SR-184"]) == before
    # ...and the named row's own edit moves it.
    srs.write_text(
        srs.read_text(encoding="utf-8").replace("its rubric", "its written rubric"),
        encoding="utf-8",
    )
    assert _digest(root, ["SR-184"]) != before
