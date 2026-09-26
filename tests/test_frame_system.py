"""A boundary crossing's system of interest, driven through `trace.py` (TC-212).

Each crossing of the depth-0 frame belongs to one of two systems of interest:
the system in OPERATION, or the system that builds and DELIVERS it (SR-187).
The `system` cell carries that from a closed pair. What this module pins is the
checker-level contract: a value outside the pair joins the frame class that
fails `--strict`, a missing value is an advisory that never moves the exit code,
and a project with no crossing (or no frame at all) hears nothing.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: every case bootstraps a
scaffold and runs the checker as a subprocess. The pure rules are in
`tests/test_frame_rules.py`, in the per-commit tier.
"""

import tomllib

from conftest import KIT, ROOT, load_script, make_minimal_project, record_ids, run_py
from test_dogfood_sync import _toml_keys, registry_key_drift

CARRIER = load_script("spine_carrier")

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

[boundary.B-02]
entity = "EXT-001"
direction = "out"
carries = "the delivered package"
system = "delivery"
status = "Drafted"
"""


def _frame(scaffold, text=FRAME):
    (scaffold / "docs" / "requirements" / "external.toml").write_text(
        text, encoding="utf-8"
    )


def _run(scaffold, *args):
    record_ids(scaffold)
    return run_py(["scripts/trace.py", *args], cwd=scaffold)


def _system_lines(stdout):
    return [line for line in stdout.splitlines() if "System" in line]


def test_crossings_declaring_operation_and_delivery_produce_no_frame_finding(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold)
    proc = _run(scaffold, "--strict")
    assert _system_lines(proc.stdout) == [], proc.stdout
    assert "FINDING (frame)" not in proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_a_value_outside_the_pair_fails_the_strict_run_naming_the_crossing(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold, FRAME.replace('system = "delivery"', 'system = "staging"'))
    proc = _run(scaffold, "--strict")
    failing = [
        line
        for line in proc.stdout.splitlines()
        if line.startswith("FINDING (frame)") and "B-02" in line
    ]
    assert failing and "staging" in failing[0], proc.stdout
    assert proc.returncode == 1


def test_a_crossing_declaring_nothing_is_one_advisory_and_the_strict_exit_stays_0(
    scaffold,
):
    make_minimal_project(scaffold)
    _frame(scaffold, FRAME.replace('system = "operation"\n', ""))
    proc = _run(scaffold, "--strict")
    advisories = [
        line
        for line in proc.stdout.splitlines()
        if line.startswith("WARNING (advisory)") and "B-01" in line and "System" in line
    ]
    assert len(advisories) == 1, proc.stdout
    assert "FINDING (frame)" not in proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_a_frame_file_with_no_crossing_is_vacuous(scaffold):
    make_minimal_project(scaffold)
    _frame(scaffold, "# nothing declared yet\n")
    proc = _run(scaffold, "--strict")
    assert _system_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_a_project_with_no_frame_file_is_vacuous(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "external.toml").unlink()
    proc = _run(scaffold, "--strict")
    assert _system_lines(proc.stdout) == [], proc.stdout
    assert proc.returncode == 0, proc.stdout


def test_the_shipped_example_crossing_carries_the_cell():
    template = tomllib.loads(
        (KIT / "registries" / "external.template.toml").read_text(encoding="utf-8")
    )
    assert template["boundary"]["B-000"]["system"] == "operation"


def test_the_three_leg_key_comparison_passes_with_the_key_on_every_leg(scaffold):
    """The dogfood rule's three legs, with `system` present on all of them: the
    schema states it, the template ships it, and a frame that uses it (the
    scaffold's, written above) invents nothing the schema does not state."""
    _frame(scaffold)
    live = _toml_keys(scaffold / "docs" / "requirements" / "external.toml", "boundary")
    tmpl = _toml_keys(KIT / "registries" / "external.template.toml", "boundary")
    schema = set(CARRIER.REGISTRY_KEYS["B-ID"])
    assert "system" in live and "system" in tmpl and "system" in schema
    assert registry_key_drift(tmpl, live, schema, CARRIER.REGISTRY_COLUMN) is None
    # ...and this repository's own frame, which gains the cell only at the C1
    # sitting commit (LLR-211: the live frame changes by ruling), still passes
    # the same comparison without it. WI-643, which writes those cells, turns
    # this into `assert "system" in own`.
    own = _toml_keys(ROOT / "docs" / "requirements" / "external.toml", "boundary")
    assert registry_key_drift(tmpl, own, schema, CARRIER.REGISTRY_COLUMN) is None
