"""trace.py acceptance-criteria testability advisory (WI-1.16, warn-only).

Gilbert's SR-013 shipped an AC saying a consumer "cannot distinguish source by
schema" — a comparative with no named predicate — and it sailed through G1.
The advisory flags comparative/absolute terms in AcceptanceCriteria cells that
lack a nearby pinned predicate. It is a heuristic, so it WARNS and never joins
any failure set: the G1 consistency review (process.md §4) makes the call.
"""

from conftest import make_minimal_project, run_py


def sr_path(root):
    return root / "docs" / "requirements" / "system-requirements.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def swap_ac(root, new_ac):
    csv = sr_path(root)
    csv.write_text(
        csv.read_text(encoding="utf-8").replace('"add(1,2) == 3"', '"' + new_ac + '"'),
        encoding="utf-8",
    )


def test_unpinned_comparative_term_warns_but_never_fails(scaffold):
    make_minimal_project(scaffold)
    # The Gilbert shape: a comparative ("schema-identical", "cannot
    # distinguish") with no predicate named anywhere in the cell.
    swap_ac(scaffold, "Consumer cannot distinguish source; output schema-identical")
    proc = run_py(
        ["scripts/trace.py", "--strict", "--strict-integrity", "--strict-schema"],
        cwd=scaffold,
    )
    # Warn-only: loud on stdout, in the report, but exit 0 under every flag.
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARNING" in proc.stdout
    assert "ac-advisories=1" in proc.stdout
    report = report_of(scaffold)
    assert "Acceptance-criteria advisories" in report
    assert "SR-001" in report
    assert "predicate" in report


def test_pinned_comparative_term_is_not_flagged(scaffold):
    make_minimal_project(scaffold)
    # Same comparative, but the predicate is named ("i.e. ..." pins it).
    swap_ac(
        scaffold,
        "Output identical to the simulator's, i.e. same field names and dtypes",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ac-advisories" not in proc.stdout
    assert "None." in report_of(scaffold).split("Acceptance-criteria advisories")[1]


def test_plain_measurable_ac_is_not_flagged(scaffold):
    # The minimal project's own AC ("add(1,2) == 3") must never warn — the
    # advisory only bites on comparative terms, not on ordinary criteria.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ac-advisories" not in proc.stdout


def test_advisory_surfaces_at_g1_via_registry_integrity_step(scaffold):
    # The G1 harness run must show the warning (Gilbert's AC passed G1 unseen)
    # while the gate itself stays green — warn, not fail.
    make_minimal_project(scaffold)
    swap_ac(scaffold, "Behaves the same as the reference implementation")
    proc = run_py(["scripts/check.py", "--gate", "G1", "--lenient"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT: PASS" in proc.stdout
    assert "WARNING" in proc.stdout and "ac-advisories=1" in proc.stdout
