"""The OI-12 carrier converter: `.md` + `.csv` registries -> one TOML carrier.

The conversion's whole claim is that it is LOSSLESS, so the tests that matter
are the ones proving the loss detector can actually fail. A round-trip check
that cannot report a dropped cell is worth nothing, and a green from it would
be exactly the "a green never hides a skipped check" failure SN-008 forbids —
so every corruption class is driven here, not just the happy path.
"""

import tomllib

import pytest
from conftest import ROOT, load_script

mc = load_script("migrate_carrier")

HEADER = ["SR-ID", "Title", "Requirement", "SN-Refs", "Phase", "Permutations"]
ROW = {
    "SR-ID": "SR-001",
    "Title": "Addition",
    "Requirement": "The system shall add two numbers.",
    "SN-Refs": "SN-001 SN-002",
    "Phase": "3",
    "Permutations": "",
}


def _expected(rows, header=HEADER, id_col="SR-ID"):
    return {
        (r.get(id_col) or "").strip(): {
            mc.KEY.get(c, c): (r.get(c) or "").strip()
            for c in header
            if c != id_col and (r.get(c) or "").strip()
        }
        for r in rows
    }


def _convert(rows=None):
    rows = rows or [ROW]
    text = mc.rows_to_toml("requirement", "SR-ID", rows, HEADER)
    return text, _expected(rows)


def test_a_clean_conversion_reports_nothing():
    text, expected = _convert()
    assert mc.compare("f", "requirement", expected, text) == []


def test_the_emitted_toml_parses_and_keys_on_the_prefixed_id():
    text, _ = _convert()
    parsed = tomllib.loads(text)
    # `[requirement.SR-001]` — bare key, prefix retained. The prefix is what
    # ~6,400 hand-authored citations grep for, so the registry has to stay
    # findable by the same token every commit message and log entry uses.
    assert list(parsed["requirement"]) == ["SR-001"]
    assert "[requirement.SR-001]" in text


def test_refs_become_a_typed_array_and_phase_an_int():
    text, _ = _convert()
    row = tomllib.loads(text)["requirement"]["SR-001"]
    # The typed array is what retires refs()'s split-on-whitespace rule, and
    # with it the `SN-001 and SN-002` -> "`and` is an orphan" defect.
    assert row["sn_refs"] == ["SN-001", "SN-002"]
    assert row["phase"] == 3 and isinstance(row["phase"], int)


def test_an_empty_cell_becomes_an_absent_key_not_an_empty_string():
    text, _ = _convert()
    # "unset" and "set to empty" stop being the same value — a distinction CSV
    # cannot carry at all.
    assert "permutations" not in tomllib.loads(text)["requirement"]["SR-001"]


def test_a_duplicate_id_is_a_PARSE_error_rather_than_a_check():
    text, expected = _convert()
    findings = mc.compare("f", "requirement", expected, text + text)
    assert findings and "twice" in findings[0]


@pytest.mark.parametrize(
    "corrupt,needle",
    [
        (lambda t: t.replace('title = "Addition"\n', ""), "title"),
        (lambda t: t.replace("add two numbers", "add three numbers"), "requirement"),
        (lambda t: t.replace('["SN-001", "SN-002"]', '["SN-001"]'), "sn_refs"),
        (lambda t: t.replace("phase = 3", "phase = 4"), "phase"),
    ],
    ids=["dropped-cell", "mangled-prose", "lost-ref", "changed-int"],
)
def test_the_loss_detector_actually_bites(corrupt, needle):
    text, expected = _convert()
    findings = mc.compare("f", "requirement", expected, corrupt(text))
    assert findings, "corruption of {} went unreported".format(needle)
    assert needle in findings[0]


def test_a_missing_row_is_reported():
    text, expected = _convert()
    expected["SR-999"] = {"title": "never emitted"}
    findings = mc.compare("f", "requirement", expected, text)
    assert any("SR-999" in f for f in findings)


def test_a_prose_cell_with_quotes_commas_and_a_pipe_survives():
    # The cells CSV fights: a literal `|` (which the SN markdown tables cannot
    # hold at all), embedded quotes, and commas.
    row = dict(ROW, Requirement='He said "a|b", then left.')
    text, expected = _convert([row])
    assert mc.compare("f", "requirement", expected, text) == []
    assert (
        tomllib.loads(text)["requirement"]["SR-001"]["requirement"]
        == 'He said "a|b", then left.'
    )


def test_the_meta_repos_own_registries_convert_losslessly():
    """The dogfood: the real spine, not a fixture. Reads only — `write=False`."""
    findings, written = mc.convert(ROOT, write=False)
    assert findings == [], findings[:5]
    assert written == []


def test_sn_edge_rows_keep_their_native_fields():
    """The edge-case table has its own columns, and the carrier keeps them.

    `traj_parse._sn_fields` folds an edge row onto the core four for the
    generated exports (its Scenario reads as the need). That fold is a
    PRESENTATION rule the markdown table forced; baking it into the carrier
    would make the export's reading the only reading there is.
    """
    needs = mc.read_sn(ROOT / "docs" / "requirements" / "stakeholder-needs.md")
    kinds = {kind for _, kind, _ in needs}
    assert kinds == {"core", "draft", "edge"}
    edge = next(f for _, kind, f in needs if kind == "edge")
    assert set(edge) == {"lifecycle", "scenario", "expected"}
    parsed = tomllib.loads(mc.sn_to_toml(needs))["need"]
    assert all("kind" in row for row in parsed.values())
