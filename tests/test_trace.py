"""trace.py: orphan detection and the --require-verified G3 criterion."""

from conftest import make_minimal_project, run_py

ORPHAN_SR = """SR-ID,Title,UN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,UN-001,"The system shall add two numbers.","Realizes UN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Orphaned,UN-001,"The system shall do something untested.","Demo orphan.","n/a",,M,Test,Draft
"""


def test_happy_chain_is_orphan_free(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout


def test_orphan_sr_fails_strict(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        ORPHAN_SR, encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no LLR" in report
    assert "SR SR-002 has no test (TC)" in report


def test_require_verified_flags_unverified_test_sr(scaffold):
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Verified", ",M,Test,Implemented"
        ),
        encoding="utf-8",
    )
    # Without the flag: still a clean trace (status is a G3 concern).
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # With the flag: the unverified Test SR fails the gate.
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "G3 requires Verified" in report
