"""Each new cell's class — traced or approved — driven through the amendment
classifier over real git trees (TC-222, LLR-225).

The cells the assumption tier and its neighbours introduce, each on an
APPROVED row whose one change is that cell, compared across two committed
trees. A traced cell is a pointer at another row: moving it reports no drift
from the recorded copy. An approved cell is a statement the row makes: moving
it is drift owed a re-attestation.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: its fixture builds and
commits a real git repository, which the per-commit tier does not run.
"""

import subprocess

import pytest
from conftest import load_script, pin_autocrlf

acceptance_record = load_script("acceptance_record")
baseline_snapshot = load_script("baseline_snapshot")

# The TOML key is the carrier's (`migrate_carrier.KEY`) where the carrier maps
# the cell today, and the column name itself where the cell's carrier key lands
# with its own tier: the classifier is keyed by the column, which is what is
# under test.

MIGRATE = load_script("migrate_carrier")

_SR = ("docs/requirements/system-requirements.toml", "SR-ID")
_TC = ("docs/test/test-cases.toml", "TC-ID")
_SN = ("docs/requirements/stakeholder-needs.toml", "SN-ID")
_STK = ("docs/requirements/stakeholder-needs.toml", "STK-ID")
_IF = ("docs/requirements/interfaces.toml", "IF-ID")
_B = ("docs/requirements/external.toml", "B-ID")
_EXT = ("docs/requirements/external.toml", "EXT-ID")
_DA = ("docs/requirements/assumptions.toml", "DA-ID")

# (registry, id column, row id, column, class)
CELL_CLASSES = [
    (*_SR, "SR-001", "DA-Refs", "traced"),
    (*_SR, "SR-002", "Coincident", "approved"),
    (*_SR, "SR-003", "Form", "approved"),
    (*_TC, "TC-001", "Assumption-Refs", "traced"),
    (*_TC, "TC-002", "Inputs", "approved"),
    (*_TC, "TC-003", "MaxAge", "approved"),
    (*_TC, "TC-004", "Sampling", "approved"),
    (*_TC, "TC-005", "SampleSize", "approved"),
    (*_TC, "TC-006", "AcceptanceRule", "approved"),
    (*_SN, "SN-001", "Stakeholder-Refs", "traced"),
    (*_SN, "SN-002", "Source", "traced"),
    (*_STK, "STK-01", "Name", "approved"),
    (*_STK, "STK-02", "Description", "approved"),
    (*_STK, "STK-03", "Party", "approved"),
    (*_IF, "IF-001", "BridgedBy", "traced"),
    (*_IF, "IF-002", "Coincident", "approved"),
    (*_B, "B-01", "System", "approved"),
    (*_EXT, "EXT-001", "Mediates", "approved"),
    (*_DA, "DA-001", "ObstacleHats", "traced"),
]


def _cell_rows(value):
    """Each registry's text: one APPROVED row per case, carrying its cell at
    `value`. Rows sharing a file (needs and stakeholders; the frame's tiers)
    land in that one file under their own tables."""
    carrier = load_script("spine_carrier")
    files = {}
    for rel, id_col, rid, column, _cls in CELL_CLASSES:
        files.setdefault(rel, []).append(
            '[{}.{}]\n{} = "{}"\nstatus = "Approved"\n'.format(
                carrier.REGISTRY_TABLE[id_col],
                rid,
                MIGRATE.KEY.get(column, column),
                value,
            )
        )
    return {rel: "\n".join(blocks) for rel, blocks in files.items()}


@pytest.fixture(scope="module")
def amended_cells(tmp_path_factory):
    """A git repository whose second commit moves every case's one cell."""
    root = tmp_path_factory.mktemp("cell-classes")

    def git(*args):
        subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            stdin=subprocess.DEVNULL,
        )

    def write(value):
        for rel, text in _cell_rows(value).items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode("utf-8"))

    git("init")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    git("config", "user.email", "loop@example.com")
    git("config", "user.name", "Loop Test")
    write("recorded")
    git("add", "-A")
    git("commit", "-q", "-m", "the recorded copy")
    write("moved")
    git("add", "-A")
    git("commit", "-q", "-m", "one cell moves on each row")
    return root


@pytest.mark.parametrize(
    "rel,id_col,rid,column,cls",
    [pytest.param(*case, id=case[3] + "@" + case[1]) for case in CELL_CLASSES],
)
def test_each_new_cell_is_classed_traced_or_approved(
    amended_cells, rel, id_col, rid, column, cls
):
    before = acceptance_record._spine_rows_at(amended_cells, "HEAD~1:", rel, id_col)
    after = acceptance_record._spine_rows_at(amended_cells, "HEAD:", rel, id_col)
    split = acceptance_record.split_changed_cells(rel, id_col, before[rid], after[rid])
    assert split[cls] == {column: ("recorded", "moved")}, split
    other = "approved" if cls == "traced" else "traced"
    assert split[other] == {}, split
    # The recorded copy is the first tree: a traced move is no drift, an
    # approved one is drift owed a re-attestation.
    drifted = baseline_snapshot.drifted_cells(rel, id_col, after[rid], before)
    assert drifted == ({column: ("recorded", "moved")} if cls == "approved" else {})
    assert baseline_snapshot.is_drifted(rel, id_col, after[rid], before) is (
        cls == "approved"
    )


def test_off_spine_registries_have_a_traced_half_now():
    """Before this table every off-spine cell counted as approved: the residual
    rule reads a cell no table names as approved, and no table named an
    off-spine registry. The traced half is two pointers, and every other cell
    stays the fail-safe approved."""
    assert acceptance_record.OFFSPINE_TRACED_CELLS == {
        "docs/requirements/interfaces.toml": frozenset({"BridgedBy"}),
        "docs/requirements/assumptions.toml": frozenset({"ObstacleHats"}),
    }
    for rel, cells in acceptance_record.OFFSPINE_TRACED_CELLS.items():
        for column in cells:
            assert acceptance_record.spine_cell_class(rel, column) == "traced"
        assert acceptance_record.spine_cell_class(rel, "Notes") == "approved"
