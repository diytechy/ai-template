"""trace.py's optional purchased/external parts registry (WI-1.3,
process-options.md "purchased parts"): PART-### rows live off the
SN->SR->LLR->TC spine and record parts the project buys rather than builds. Each
row's IF-Ref names the interface row that is its owner-of-record (MULTI_REPO.md
§3.3), but trace.py never reads the IF-### tier, so PART is integrity-checked
only (malformed/duplicate id) — deliberately minimal, "no more than PB". The
registry is optional: an absent file is a no-op and the bootstrapped PART-000
placeholder never blocks a gate.
"""

from conftest import make_minimal_project, run_py

PART_HEADER = "PART-ID,Name,IF-Ref,Vendor,Cost,Status,Quantity,Notes\n"
ROW = "{pid},SO-101 arm,{ifref},https://example.com/vendor,199,ordered,2,note\n"


def part_path(root):
    return root / "docs" / "requirements" / "procurement.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_parts(root, *rows):
    part_path(root).write_text(PART_HEADER + "".join(rows), encoding="utf-8")


def test_clean_part_row_passes(scaffold):
    make_minimal_project(scaffold)
    write_parts(scaffold, ROW.format(pid="PART-001", ifref="IF-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "parts=1" in proc.stdout


def test_malformed_part_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_parts(scaffold, ROW.format(pid="PART-XX", ifref="IF-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "PART id 'PART-XX' is malformed" in report_of(scaffold)


def test_duplicate_part_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_parts(
        scaffold,
        ROW.format(pid="PART-001", ifref="IF-001"),
        ROW.format(pid="PART-001", ifref="IF-002"),
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "PART id PART-001 is duplicated" in report_of(scaffold)


def test_part_with_empty_if_ref_passes(scaffold):
    # IF-Ref is NOT resolved (trace.py never reads the IF-### tier), so an empty
    # or unknown IF-Ref is not an integrity error — the minimal, "no more than
    # PB" stance. A part is only rejected for a malformed/duplicate id.
    make_minimal_project(scaffold)
    write_parts(scaffold, ROW.format(pid="PART-001", ifref=""))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "parts=1" in proc.stdout


def test_placeholder_part_registry_is_inert(scaffold):
    # The bootstrapped PART-000 placeholder must never block a gate for a project
    # that buys nothing (same stance as interfaces.csv / PB-000): it survives even
    # --no-placeholders, which the spine does not.
    make_minimal_project(scaffold)
    assert part_path(scaffold).exists()  # bootstrap laid down the registry
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # With no real PART rows, no parts count is emitted at all.
    assert "parts=" not in proc.stdout
