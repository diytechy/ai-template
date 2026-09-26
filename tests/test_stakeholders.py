"""The stakeholder list and each need's references into it, driven through
`trace.py` (TC-215).

A needs file may carry a `[stakeholder.STK-##]` table beside its needs: who
owns an outcome, and which declared entity of the frame they are (SR-189). Each
need names its stakeholders in `stakeholder_refs`. What this module pins is the
checker-level contract on a scaffold: a dangling reference or an incomplete
stakeholder fails `--strict` naming the row, a stakeholder status outside the
spine's vocabulary fails the always-on integrity floor, a need naming nobody is
one advisory, and the stakeholder rows never leak into the need universe.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: every case bootstraps a
scaffold and runs the checker as a subprocess.
"""

import tomllib

import pytest

from conftest import KIT, load_script, make_minimal_project, record_ids, run_py
from test_dogfood_sync import TOML_REGISTRIES, _toml_keys, registry_key_drift

CARRIER = load_script("spine_carrier")
import kitlib.spine as SPINE  # noqa: E402  (after the load above puts scripts/ on the path)

NEEDS_REL = "docs/requirements/stakeholder-needs.toml"

FRAME = """
[entity.EXT-001]
name = "Downstream adopter"
class = "operational"
description = "The team that adopts the package."
status = "Drafted"

[boundary.B-01]
entity = "EXT-001"
direction = "in"
carries = "the adopter's request"
system = "operation"
status = "Drafted"
"""

STAKEHOLDERS = """
[stakeholder.STK-01]
name = "Adopting team"
description = "A team that adds the package to its own work."
party = "EXT-001"
status = "Approved"
"""

NEED = """
[need.SN-001]
status = "Approved"
need = "Add two numbers."
why = "Demo."
priority = "M"
acceptance = "Adding one and two gives three."
stakeholder_refs = ["STK-01"]
"""


def _project(scaffold, needs=STAKEHOLDERS + NEED, frame=FRAME):
    """The minimal traced project, its needs moved onto the TOML carrier with
    the given text (the fixture writes the legacy markdown one)."""
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "stakeholder-needs.md").unlink()
    (req / "stakeholder-needs.toml").write_text(needs, encoding="utf-8")
    (req / "external.toml").write_text(frame, encoding="utf-8")


def _run(scaffold, *args, bump=True):
    if bump:
        record_ids(scaffold)
    return run_py(["scripts/trace.py", *args], cwd=scaffold)


def _lines(stdout, prefix, *needles):
    return [
        line
        for line in stdout.splitlines()
        if line.startswith(prefix) and all(n in line for n in needles)
    ]


def _stakeholder_lines(stdout):
    return [
        line for line in stdout.splitlines() if "STK-" in line or "stakeholder" in line
    ]


def test_a_declared_stakeholder_and_a_need_citing_it_are_clean(scaffold):
    _project(scaffold)
    proc = _run(scaffold, "--strict")
    assert _stakeholder_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_a_need_citing_an_undeclared_stakeholder_fails_naming_the_need(scaffold):
    _project(scaffold, STAKEHOLDERS + NEED.replace('["STK-01"]', '["STK-09"]'))
    proc = _run(scaffold, "--strict")
    assert _lines(proc.stdout, "FINDING (frame)", "SN-001", "STK-09"), proc.stdout
    assert proc.returncode == 1


def test_a_need_citing_a_stakeholder_with_no_list_at_all_fails_naming_it(scaffold):
    """No stakeholder table at all: the advisory for a need naming nobody stays
    silent, but a reference still has to resolve, so a need citing a
    stakeholder the file never declares fails naming the need."""
    _project(scaffold, NEED)
    proc = _run(scaffold, "--strict")
    assert _lines(proc.stdout, "FINDING (frame)", "SN-001", "STK-01"), proc.stdout
    assert proc.returncode == 1


def test_a_party_naming_an_undeclared_entity_fails_naming_the_stakeholder(scaffold):
    _project(scaffold, STAKEHOLDERS.replace("EXT-001", "EXT-009") + NEED)
    proc = _run(scaffold, "--strict")
    assert _lines(proc.stdout, "FINDING (frame)", "STK-01", "EXT-009"), proc.stdout
    assert proc.returncode == 1


@pytest.mark.parametrize("cell", ["name", "description", "status"])
def test_a_stakeholder_missing_a_required_cell_fails_naming_it(scaffold, cell):
    body = "\n".join(
        line for line in STAKEHOLDERS.split("\n") if not line.startswith(cell + " =")
    )
    _project(scaffold, body + NEED)
    proc = _run(scaffold, "--strict")
    assert _lines(proc.stdout, "FINDING (frame)", "STK-01", cell), proc.stdout
    assert proc.returncode == 1


def test_a_need_citing_no_stakeholder_is_one_advisory_and_never_fails(scaffold):
    _project(
        scaffold, STAKEHOLDERS + NEED.replace('stakeholder_refs = ["STK-01"]\n', "")
    )
    proc = _run(scaffold, "--strict")
    advisories = _lines(proc.stdout, "WARNING (advisory)", "SN-001", "stakeholder")
    assert len(advisories) == 1, proc.stdout
    assert "FINDING (frame)" not in proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_a_stakeholder_with_no_party_is_valid(scaffold):
    _project(scaffold, STAKEHOLDERS.replace('party = "EXT-001"\n', "") + NEED)
    proc = _run(scaffold, "--strict")
    assert _stakeholder_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_a_status_outside_the_vocabulary_fails_the_integrity_floor(scaffold):
    _project(scaffold, STAKEHOLDERS.replace('"Approved"', '"Bananas"', 1) + NEED)
    proc = _run(scaffold, "--strict-integrity")
    assert _lines(proc.stdout, "FINDING (integrity)", "STK-01", "Bananas"), proc.stdout
    assert proc.returncode == 1
    # ...and under the full strict run it ALSO fails the frame class, where the
    # stakeholder rules put it: each of the two approved rows asking for it
    # holds, and removing either finding reds this test.
    proc = _run(scaffold, "--strict", bump=False)
    assert _lines(proc.stdout, "FINDING (integrity)", "STK-01", "Bananas"), proc.stdout
    assert _lines(proc.stdout, "FINDING (frame)", "STK-01", "Bananas"), proc.stdout
    assert proc.returncode == 1


def test_a_stakeholder_id_above_the_watermark_is_refused_as_unallocated(scaffold):
    _project(scaffold)
    record_ids(scaffold)
    marks = (scaffold / "docs" / "id-watermark").read_text(encoding="utf-8")
    assert "\nSTK = 1\n" in marks, marks  # the space is marked, at the live max
    req = scaffold / "docs" / "requirements" / "stakeholder-needs.toml"
    req.write_text(
        req.read_text(encoding="utf-8")
        + STAKEHOLDERS.replace("STK-01", "STK-05").replace("Adopting team", "Owner"),
        encoding="utf-8",
    )
    proc = _run(scaffold, "--strict-integrity", bump=False)
    assert _lines(proc.stdout, "FINDING (integrity)", "STK-005", "watermark"), (
        proc.stdout
    )
    assert proc.returncode == 1


def test_a_need_id_quoted_in_a_stakeholder_description_is_not_a_need(scaffold):
    quoted = STAKEHOLDERS.replace(
        "own work.", "own work, and first raised the request SN-777 records."
    )
    _project(scaffold, quoted + NEED)
    proc = _run(scaffold, "--strict")
    assert "SN-777" not in proc.stdout, proc.stdout
    assert "Traceability: SN=1 " in proc.stdout, proc.stdout
    assert proc.returncode == 0, proc.stdout
    # The scrape itself, on the same text: the stakeholder's prose is not read.
    text = (scaffold / NEEDS_REL).read_text(encoding="utf-8")
    assert SPINE.sn_all_ids(text, ".toml") == {"SN-001"}


def test_a_need_id_named_only_in_a_toml_comment_is_not_a_need(scaffold):
    """Both readers of the need universe, the checker and the stage derivation,
    tell the carrier from the FILE they resolved, so a TOML needs file is read
    as TOML even where its text alone would not say so. Here the file holds a
    comment naming SN-777 and one real need: the comment is not a need."""
    _project(scaffold, "# first raised as SN-777\n" + STAKEHOLDERS + NEED)
    proc = _run(scaffold, "--strict")
    assert "SN-777" not in proc.stdout, proc.stdout
    assert "Traceability: SN=1 " in proc.stdout, proc.stdout
    assert proc.returncode == 0, proc.stdout
    docs = scaffold / "docs"
    assert load_script("spine_rules").load_spine(docs)["sn_ids"] == {"SN-001"}
    # A needs file holding ONLY comments declares no need at all, to either
    # reader: its text parses to nothing, and read by sniffing it took the
    # markdown carrier's whole-text scrape and counted the comment.
    (scaffold / NEEDS_REL).write_text("# first raised as SN-777\n", encoding="utf-8")
    assert load_script("spine_rules").load_spine(docs)["sn_ids"] == set()
    assert load_script("trace").load_registries(docs).sn_ids == set()


def test_the_dogfood_key_comparison_covers_the_stakeholder_table(scaffold):
    """The three-leg rule reaches the new tier: it is registered on the needs
    path under its own table, the shipped template states exactly the schema's
    keys, a scaffold's own table passes, and a planted defect on either side is
    named."""
    assert TOML_REGISTRIES["STK-ID"] == (
        NEEDS_REL,
        "registries/stakeholder-needs.template.toml",
        "stakeholder",
    )
    _project(scaffold)
    schema = set(CARRIER.REGISTRY_KEYS["STK-ID"])
    assert schema == {"name", "description", "party", "status"}
    template = KIT / "registries" / "stakeholder-needs.template.toml"
    tmpl = _toml_keys(template, "stakeholder")
    live = _toml_keys(scaffold / NEEDS_REL, "stakeholder")
    assert registry_key_drift(tmpl, live, schema, CARRIER.REGISTRY_COLUMN) is None
    # (1) a live stakeholder invents a key nobody shipped.
    drift = registry_key_drift(
        tmpl, live | {"owner_hat"}, schema, CARRIER.REGISTRY_COLUMN
    )
    assert drift is not None and "owner_hat" in drift
    # (2) the template stops shipping `party`.
    drift = registry_key_drift(tmpl - {"party"}, live, schema, CARRIER.REGISTRY_COLUMN)
    assert drift is not None and "party" in drift
    # ...and the need tier's own leg carries the reference column.
    assert "stakeholder_refs" in _toml_keys(template, "need")
    assert "stakeholder_refs" in CARRIER.REGISTRY_KEYS["SN-ID"]


def test_the_shipped_template_cites_its_example_stakeholder():
    template = tomllib.loads(
        (KIT / "registries" / "stakeholder-needs.template.toml").read_text(
            encoding="utf-8"
        )
    )
    assert set(template["stakeholder"]) == {"STK-000"}
    assert template["need"]["SN-000"]["stakeholder_refs"] == ["STK-000"]


def test_a_fresh_scaffold_with_the_example_rows_is_clean(scaffold):
    """The template's example stakeholder and the example need citing it are
    placeholders: they produce no finding and no advisory."""
    proc = _run(scaffold, "--strict-integrity")
    assert _stakeholder_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_a_needs_file_with_no_stakeholder_table_produces_none_of_these(scaffold):
    _project(scaffold, NEED.replace('stakeholder_refs = ["STK-01"]\n', ""))
    proc = _run(scaffold, "--strict")
    assert _stakeholder_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout
    proc = _run(scaffold, "--strict-integrity", bump=False)
    assert _stakeholder_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout
