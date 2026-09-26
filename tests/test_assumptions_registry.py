"""The assumptions registry, driven through `trace.py` on scaffolds (TC-217).

`docs/requirements/assumptions.toml` holds two tiers beside the frame: the
domain assumptions a requirement's argument relies on (`[assumption.DA-###]`,
SR-191) and the stand-ins that answer for an outside party in tests
(`[surrogate.SUR-###]`, SR-192). What this module pins is the checker-level
contract: an incomplete or out-of-vocabulary assumption row fails `--strict`
naming the row and the cell, a spent id is never issued again, the shipped
template arrives as an inert blank form, and a project that declares no frame
hears nothing from the registry at all. The pure rules are pinned on
in-memory rows in `tests/test_assumption_rules.py`.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: every case bootstraps a
scaffold and runs the checker as a subprocess.
"""

import pytest

from conftest import KIT, make_minimal_project, record_ids, run_py

REGISTRY_REL = "docs/requirements/assumptions.toml"

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

ASSUMPTION = """
[assumption.DA-001]
effect_at = ["B-01"]
assumption = "An adopter reads the shipped guide before running the scaffold."
holds_when = "The adopter installs from the published package."
obstacle = "The adopter copies the scripts without the guide."
falsifier = "A support request asking what the scaffold is for."
realized_by = "SUR-001"
status = "Drafted"
standing = "active"
"""

SURROGATE = """
[surrogate.SUR-001]
name = "Scripted adopter"
emulates = ["EXT-001"]
description = "A fresh scaffold in a temporary directory, driven by the suite."
status = "Drafted"
"""

# Each defect, in turn, on the one assumption row: the text edit that plants it
# and the cell the strict finding must name. A missing cell is its key's line
# removed; the three vocabulary and resolution defects rewrite a value.
DEFECTS = [
    ("effect_at", "effect_at = ", "", "EffectAt"),
    ("assumption", "assumption = ", "", "Assumption"),
    ("holds_when", "holds_when = ", "", "HoldsWhen"),
    ("obstacle", "obstacle = ", "", "Obstacle"),
    ("status", "status = ", "", "Status"),
    ("standing", "standing = ", "", "Standing"),
    ("status value", 'status = "Drafted"', 'status = "Bananas"', "Bananas"),
    ("standing value", 'standing = "active"', 'standing = "doubtful"', "doubtful"),
    ("landing", 'effect_at = ["B-01"]', 'effect_at = ["B-09"]', "B-09"),
]


def _without_line(text, prefix):
    """`text` with the one line starting `prefix` removed (a whole-line drop:
    every value here is single-line)."""
    lines = text.split("\n")
    kept = [line for line in lines if not line.startswith(prefix)]
    assert len(kept) == len(lines) - 1, "fixture: no single line starts " + prefix
    return "\n".join(kept)


def _plant(old, new):
    if new == "":
        return _without_line(ASSUMPTION, old)
    assert old in ASSUMPTION, "fixture: " + old
    return ASSUMPTION.replace(old, new, 1)


def _project(scaffold, registry=ASSUMPTION + SURROGATE):
    """The minimal traced project with a declared frame and the given
    assumptions registry (None keeps the scaffold's shipped blank form)."""
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "external.toml").write_text(FRAME, encoding="utf-8")
    if registry is not None:
        (req / "assumptions.toml").write_text(registry, encoding="utf-8")


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


def _tier_lines(stdout):
    return [line for line in stdout.splitlines() if "DA-" in line or "SUR-" in line]


def test_a_complete_assumption_row_passes(scaffold):
    """The row is read, and nothing in it fails: the one line naming it is the
    advisory that no requirement cites it yet."""
    _project(scaffold)
    proc = _run(scaffold, "--strict")
    findings = [line for line in _tier_lines(proc.stdout) if line.startswith("FINDING")]
    assert findings == [], proc.stdout
    assert _lines(proc.stdout, "WARNING (advisory)", "DA-001"), proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_each_defect_fails_the_strict_run_naming_the_row_and_the_cell(scaffold):
    """One scaffold, one defect at a time: each run's registry differs from the
    complete row by exactly the planted defect, so each red is that defect's."""
    _project(scaffold)
    record_ids(scaffold)
    registry = scaffold / REGISTRY_REL
    missed = []
    for label, old, new, cell in DEFECTS:
        registry.write_text(_plant(old, new) + SURROGATE, encoding="utf-8")
        proc = _run(scaffold, "--strict", bump=False)
        if proc.returncode != 1 or not _lines(
            proc.stdout, "FINDING (frame)", "DA-001", cell
        ):
            missed.append((label, proc.returncode, _tier_lines(proc.stdout)))
    assert missed == [], missed


def test_a_surrogate_status_outside_the_vocabulary_fails_the_integrity_floor(scaffold):
    _project(scaffold, ASSUMPTION + SURROGATE.replace('"Drafted"', '"Bananas"'))
    proc = _run(scaffold, "--strict-integrity")
    assert _lines(proc.stdout, "FINDING (integrity)", "SUR-001", "Bananas"), proc.stdout
    assert proc.returncode == 1


def test_an_id_above_its_watermark_mark_is_refused(scaffold):
    _project(scaffold)
    record_ids(scaffold)
    marks = (scaffold / "docs" / "id-watermark").read_text(encoding="utf-8")
    assert "\nDA = 1\n" in marks and "\nSUR = 1\n" in marks, marks
    registry = scaffold / REGISTRY_REL
    registry.write_text(
        registry.read_text(encoding="utf-8")
        + ASSUMPTION.replace("DA-001", "DA-005")
        + SURROGATE.replace("SUR-001", "SUR-005"),
        encoding="utf-8",
    )
    proc = _run(scaffold, "--strict-integrity", bump=False)
    assert _lines(proc.stdout, "FINDING (integrity)", "DA-005", "watermark"), (
        proc.stdout
    )
    assert _lines(proc.stdout, "FINDING (integrity)", "SUR-005", "watermark"), (
        proc.stdout
    )
    assert proc.returncode == 1


def test_a_fresh_scaffold_receives_the_blank_form_and_passes_strict(scaffold):
    """The scaffold mapping ships the template verbatim; its `-000` example
    rows are inert, so the strict check passes and names neither of them."""
    shipped = (KIT / "registries" / "assumptions.template.toml").read_bytes()
    assert (scaffold / REGISTRY_REL).read_bytes() == shipped
    marks = (scaffold / "docs" / "id-watermark").read_text(encoding="utf-8")
    assert "\nDA = 0\n" in marks and "\nSUR = 0\n" in marks, marks
    for flag in ("--strict", "--strict-integrity"):
        proc = run_py(["scripts/trace.py", flag], cwd=scaffold)
        assert _tier_lines(proc.stdout) == [], proc.stdout
        assert proc.returncode == 0, proc.stdout


def test_the_example_rows_are_inert_beside_a_declared_frame(scaffold):
    """The template's rows land on `B-000` and emulate `EXT-000`, which no
    declared frame carries: inert, they name nothing and fail nothing."""
    _project(scaffold, registry=None)
    shipped = (KIT / "registries" / "assumptions.template.toml").read_bytes()
    assert (scaffold / REGISTRY_REL).read_bytes() == shipped
    proc = _run(scaffold, "--strict")
    assert _tier_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout


@pytest.mark.parametrize("flag", ["--strict", "--strict-integrity"])
def test_a_project_with_no_frame_file_hears_nothing_from_the_registry(scaffold, flag):
    """Without a declared frame there is no crossing for an assumption to land
    on, so the tier does not apply: the same registry that fails beside a frame
    is silent once the frame file is gone."""
    broken = _plant('effect_at = ["B-01"]', 'effect_at = ["B-09"]').replace(
        'status = "Drafted"', 'status = "Bananas"'
    ) + SURROGATE.replace("EXT-001", "EXT-404")
    _project(scaffold, registry=broken)
    framed = _run(scaffold, flag)
    assert framed.returncode == 1 and _tier_lines(framed.stdout), framed.stdout
    (scaffold / "docs" / "requirements" / "external.toml").unlink()
    proc = _run(scaffold, flag, bump=False)
    assert _tier_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout
