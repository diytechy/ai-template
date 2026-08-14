"""The depth-0 FRAME registry (WI-442, sitting-2 §1R): `external.toml`.

Three tiers on one path — entities (`EXT-###`), boundary crossings (`B-##`) and
external-to-external relationships (`REL-###`) — plus the directional tie-back an
`IF-###` row carries when it REALIZES a crossing.

The frame's *content* is a human ruling and nothing here judges it. What is
mechanized, and what this module pins, is the joining: a crossing names a
declared entity, a relationship names two, a tie-back names a declared crossing,
and every row carries the one maturity field the boundary rung reads
(`derive_gate.boundary_incomplete` — its own tests live in
tests/test_ratification_level.py).
"""

import tomllib

from conftest import (
    ROOT,
    load_script,
    make_minimal_project,
    record_ids,
    run_py,
)

CARRIER = load_script("spine_carrier")
TRACE = load_script("trace")

LIVE = ROOT / "docs" / "requirements" / "external.toml"

# A complete, resolving frame — the fixture every mutation below starts from.
CLEAN_FRAME = """
[entity.EXT-001]
name = "Downstream adopter"
class = "operational"
description = "The team that adopts the package."
approval = "draft"

[boundary.B-01]
entity = "EXT-001"
direction = "out"
carries = "the delivered package"
approval = "draft"

[relationship.REL-001]
from = "EXT-001"
to = "EXT-001"
kind = "hands-off"
flow = "a flow this system is not a party to"
approval = "draft"
"""


def _frame(scaffold, text=CLEAN_FRAME):
    (scaffold / "docs" / "requirements" / "external.toml").write_text(
        text, encoding="utf-8"
    )


def _run(scaffold, *args):
    record_ids(scaffold)
    return run_py(["scripts/trace.py", *args], cwd=scaffold)


# --- the carrier: three tiers, ONE path ---------------------------------------


def test_the_three_tiers_load_off_one_path_without_a_new_loader():
    """The whole reason the carrier keys registries by ID COLUMN rather than by
    path. `external.toml` is the first file to carry more than one tier, and it
    needed no loader change at all — `load(path, "B-ID")` returns exactly the
    crossings because the tier, not the file, is what the key names."""
    for id_col, table in (
        ("EXT-ID", "entity"),
        ("B-ID", "boundary"),
        ("REL-ID", "relationship"),
    ):
        assert CARRIER.REGISTRY_TABLE[id_col] == table
        rows = CARRIER.load(LIVE, id_col)
        assert rows, id_col
        assert all(r[id_col] for r in rows)
    # ...and the three do not bleed into each other.
    ext_ids = {r["EXT-ID"] for r in CARRIER.load(LIVE, "EXT-ID")}
    bif_ids = {r["B-ID"] for r in CARRIER.load(LIVE, "B-ID")}
    assert not (ext_ids & bif_ids)


def test_the_live_frame_is_the_LOCKED_one():
    """5 entities, 6 crossings, 3 relationships — sitting-2 §1R.7, ruled
    2026-08-13o and amended at 13u when B-03 was removed. A count is a weak
    assertion about most registries and a strong one here, because this frame was
    closed by a ruling: a row appearing or vanishing without a sitting is the
    defect, not a growth curve."""
    tables = tomllib.loads(LIVE.read_text(encoding="utf-8"))
    assert len(tables["entity"]) == 5
    assert len(tables["boundary"]) == 6
    assert len(tables["relationship"]) == 3
    # B-03 is ABSENT on purpose (removed 13u) and the gap is load-bearing: it
    # keeps id and frame name aligned 1:1 rather than renumbering a locked table.
    assert "B-03" not in tables["boundary"]


def test_every_frame_row_carries_the_approval_element():
    """D12's requirement, from the file's FIRST commit: a frame with no approval
    element is un-ratifiable, and the rung that reads it would have nothing
    honest to read. Checked over every row of every tier, because a single
    unapproved-by-omission crossing is what would silently clear rung 1."""
    tables = tomllib.loads(LIVE.read_text(encoding="utf-8"))
    for table in ("entity", "boundary", "relationship"):
        for rid, row in tables[table].items():
            assert row.get("approval") in ("draft", "approved"), (table, rid)


def test_nothing_in_the_live_frame_is_approved_yet():
    """The flip authority, asserted rather than asked for. `process.toml`'s
    `human_ratification_through` covers the SPINE tiers only; until sitting-3
    §3.6 rules the mechanized extension, an `approval` cell here is the OWNER's
    to flip in a reviewed commit. Nothing this program builds may set one.

    This test is expected to be EDITED by that ratification — deliberately. It
    is the tripwire that makes a loop-authored approval a red test rather than a
    quiet line in a diff."""
    tables = tomllib.loads(LIVE.read_text(encoding="utf-8"))
    approvals = {
        row.get("approval")
        for table in ("entity", "boundary", "relationship")
        for row in tables[table].values()
    }
    assert approvals == {"draft"}


# --- the join rules ------------------------------------------------------------


def test_a_clean_frame_produces_no_finding(scaffold):
    """The fixture floor every mutation below stands on: if a resolving frame
    already reported something, none of the bite-proofs would mean anything."""
    make_minimal_project(scaffold)
    _frame(scaffold)
    proc = _run(scaffold, "--strict")
    assert "FINDING (frame)" not in proc.stdout
    assert "references unknown" not in proc.stdout
    # ...and the report's frame section reads out the clean counts, so a silently
    # SKIPPED section cannot masquerade as a clean one.
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "## The depth-0 frame" in report
    assert "1 entity, 1 boundary-crossing and 1 relationship row(s)" in report


def test_a_crossing_naming_an_undeclared_entity_is_a_FINDING(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold, CLEAN_FRAME.replace('entity = "EXT-001"', 'entity = "EXT-009"'))
    proc = _run(scaffold, "--strict")
    assert "boundary B-01 Entity references unknown EXT-009" in proc.stdout
    assert proc.returncode == 1


def test_a_relationship_naming_an_undeclared_entity_is_a_FINDING(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold, CLEAN_FRAME.replace('to = "EXT-001"', 'to = "EXT-009"'))
    proc = _run(scaffold, "--strict")
    assert "relationship REL-001 To references unknown EXT-009" in proc.stdout
    assert proc.returncode == 1


def test_an_IF_tieback_naming_an_undeclared_crossing_is_a_FINDING(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'direction = "Provides"\n'
        'this_project = "src/demo"\n'
        'counterpart = "downstream adopter"\n'
        'contract = "the package"\n'
        'signal = "discrete"\n'
        'sr_refs = ["SR-001"]\n'
        'version = "v1"\n'
        'approval = "draft"\n'
        'interface_to_external = "B-99"\n',
        encoding="utf-8",
    )
    proc = _run(scaffold, "--strict")
    assert "IF IF-001 InterfaceToExternal references unknown crossing B-99" in (
        proc.stdout
    )
    assert proc.returncode == 1


def test_the_frame_rules_are_VACUOUS_without_the_registry(scaffold):
    """The applies-when, at the checker tier. A project that declares no boundary
    has no `external.toml`, and every rule above must then say nothing at all —
    not "no entities declared", which would make the frame mandatory by the back
    door for every adopter who never wanted it."""
    make_minimal_project(scaffold)
    # bootstrap SCAFFOLDS the file (inert, `-000` rows only). Deleting it is what
    # "a project that never adopts the tier" actually looks like — the same act
    # ADOPTING.md tells an adopter to take for any registry they do not want.
    (scaffold / "docs" / "requirements" / "external.toml").unlink()
    proc = _run(scaffold, "--strict")
    assert "FINDING (frame)" not in proc.stdout
    assert "depth-0 frame" not in (
        scaffold / "docs" / "test" / "report.md"
    ).read_text(encoding="utf-8")


def test_a_tieback_is_vacuous_when_no_crossing_is_declared(scaffold):
    """Narrower than the case above and a different failure: the frame file
    exists but declares no crossings, so a tie-back names nothing that COULD
    resolve. That is a schema question (why is there a tie-back at all?), not a
    resolution one, and reporting it as a dangling reference would blame the IF
    row for the frame's emptiness."""
    make_minimal_project(scaffold)
    _frame(scaffold, '[entity.EXT-001]\nname = "A"\nclass = "operational"\n')
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'direction = "Provides"\n'
        'this_project = "src/demo"\n'
        'counterpart = "downstream adopter"\n'
        'contract = "the package"\n'
        'signal = "discrete"\n'
        'sr_refs = ["SR-001"]\n'
        'version = "v1"\n'
        'approval = "draft"\n'
        'interface_to_external = "B-99"\n',
        encoding="utf-8",
    )
    proc = _run(scaffold, "--strict")
    assert "references unknown crossing" not in proc.stdout


# --- SN-037's SR -> boundary rule, at its two severities -----------------------


def _srs(scaffold, extra_keys=""):
    # `make_minimal_project` writes the CSV carrier; the dual-home refusal is
    # deliberate and hard, so the legacy file goes when the TOML one arrives.
    csv = scaffold / "docs" / "requirements" / "system-requirements.csv"
    if csv.exists():
        csv.unlink()
    (scaffold / "docs" / "requirements" / "system-requirements.toml").write_text(
        "[requirement.SR-001]\n"
        'title = "Addition"\n'
        'sn_refs = ["SN-001"]\n'
        "{}"
        'requirement = "The system shall add two numbers."\n'
        'rationale = "Realizes SN-001."\n'
        'acceptance_criteria = "add(1,2) == 3"\n'
        'priority = "M"\n'
        'verification = "Test"\n'
        'status = "Verified"\n'.format(extra_keys),
        encoding="utf-8",
    )


def test_an_SR_naming_an_undeclared_crossing_is_a_HARD_finding(scaffold):
    """The half of SN-037 that can be true today, and the only half that is an
    error: a dangling reference, exactly like an SR citing a deleted SN."""
    make_minimal_project(scaffold)
    _frame(scaffold)
    _srs(scaffold, 'boundary_refs = ["B-99"]\n')
    proc = _run(scaffold, "--strict")
    assert "SR SR-001 Boundary-Refs references unknown crossing B-99" in proc.stdout
    assert proc.returncode == 1


def test_an_SR_naming_a_DECLARED_crossing_is_clean(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold)
    _srs(scaffold, 'boundary_refs = ["B-01"]\n')
    proc = _run(scaffold, "--strict")
    assert "Boundary-Refs references unknown" not in proc.stdout
    # ...and the crossing is no longer reported as named by nobody.
    assert "named by NO requirement" not in proc.stdout


def test_SR_boundary_COVERAGE_is_a_summary_advisory_and_never_an_error(scaffold):
    """The other half, and the severity split is the point. "Every SR references
    a declared interface" is SN-037's wording, but enforcing it the day the column
    ships would red every row in the registry for work the re-tier campaign owns
    — and under a form rule that is itself a guideline with recorded waivers. A
    gate that is 100% red on day one is a gate someone turns off.

    So: ONE line carrying the count the campaign has to move, on the advisory
    pipe, with the exit code untouched."""
    make_minimal_project(scaffold)
    _frame(scaffold)
    _srs(scaffold)  # no boundary_refs at all
    proc = _run(scaffold, "--strict")
    assert "SR->boundary coverage: 1 of 1 requirement(s) name no crossing" in (
        proc.stdout
    )
    assert proc.returncode == 0
    # One summary line, not one per row — the ergonomic rule the seam-TC warn
    # already learned.
    assert len([ln for ln in proc.stdout.splitlines() if "->boundary" in ln]) == 1


def test_the_realization_gap_is_REPORTED_and_never_gated(scaffold):
    """Decision 6's question — a crossing with no realizing IF row — deferred BY
    RULING to post-schema. It is visible (a deferral nobody can see is a
    deferral nobody honours) and it changes no exit code, which is the same
    restraint that keeps `boundary_incomplete` reading approval rather than
    realization coverage."""
    make_minimal_project(scaffold)
    _frame(scaffold)
    _srs(scaffold, 'boundary_refs = ["B-01"]\n')
    proc = _run(scaffold, "--strict")
    assert "boundary crossing(s) realized by NO interface row: B-01" in proc.stdout
    assert proc.returncode == 0


def test_the_SR_boundary_rule_is_vacuous_without_a_frame(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "external.toml").unlink()
    _srs(scaffold, 'boundary_refs = ["B-99"]\n')
    proc = _run(scaffold, "--strict")
    assert "Boundary-Refs" not in proc.stdout
    assert "->boundary coverage" not in proc.stdout


# --- the schema tier (warn-first, like IF/CMP) ---------------------------------


def test_an_out_of_vocabulary_frame_value_WARNS_and_never_fails(scaffold):
    """The frame tiers join the ADVISORY schema tier, the same ruled warn-first
    sequencing IF and CMP got at WI-443 — a vocabulary is closed the moment it is
    stated, and promotion to ERROR is a later, separate decision. The resolution
    rules above are hard; a typo in a vocabulary cell is not."""
    make_minimal_project(scaffold)
    _frame(scaffold, CLEAN_FRAME.replace('class = "operational"', 'class = "vendor"'))
    proc = _run(scaffold, "--strict")
    assert "EXT EXT-001 has Class='vendor'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout
    # ...and it did not join the failure set.
    assert "FINDING (frame)" not in proc.stdout


def test_an_empty_required_frame_field_WARNS(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold, CLEAN_FRAME.replace('carries = "the delivered package"\n', ""))
    proc = _run(scaffold, "--strict")
    assert "B B-01 has empty required field Carries" in proc.stdout


def test_the_example_rows_are_inert(scaffold):
    """The `-000` convention, applied to a registry whose ids are NOT three
    digits. `B-000` and `EXT-000` must be skipped exactly like `IF-000`, or a
    freshly bootstrapped repo reports findings against the template it just
    copied — and the crossing example, which points at `EXT-000`, would resolve
    against nothing."""
    make_minimal_project(scaffold)
    template = (
        ROOT / "project-trajectory" / "registries" / "external.template.toml"
    ).read_text(encoding="utf-8")
    _frame(scaffold, template)
    proc = _run(scaffold, "--strict")
    assert "FINDING (frame)" not in proc.stdout
    assert "EXT-000" not in proc.stdout
    assert TRACE.is_example("B-000") and TRACE.is_example("EXT-000")
