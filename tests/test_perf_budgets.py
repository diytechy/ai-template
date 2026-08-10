"""trace.py's optional performance-budgets hook (Thread 10): PB-### rows live off
the SN->SR->LLR->TC spine but stay traceable — each back-links a real
SR/LLR/Module, and a malformed PB id or a dangling ref fails --strict. The
registry is optional, so its -000 placeholder never blocks a gate.
"""

from conftest import make_minimal_project, run_py, record_ids

PB_HEADER = "PB-ID,Metric,Refs,Budget,Unit,Tolerance,Direction,Tier,Gate,Owner,Notes\n"
ROW = "{pid},Peak RAM,{refs},256,MiB,10%,lower-better,Release,warn,Integration,note\n"


def pb_path(root):
    return root / "docs" / "requirements" / "performance-budgets.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_budgets(root, *rows):
    pb_path(root).write_text(PB_HEADER + "".join(rows), encoding="utf-8")
    record_ids(root)


def test_clean_budget_linked_to_sr_passes(scaffold):
    make_minimal_project(scaffold)
    write_budgets(scaffold, ROW.format(pid="PB-001", refs="SR-001;LLR-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "budgets=1 budget-findings=0" in proc.stdout


def test_budget_referencing_unknown_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_budgets(scaffold, ROW.format(pid="PB-001", refs="SR-999"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "PB PB-001 references unknown SR-999" in report_of(scaffold)


def test_budget_may_back_link_a_module_path(scaffold):
    # Refs resolve against SR/LLR ids OR an LLR Module path (the demo LLR's
    # Module is src/demo), so a budget can bound a whole module.
    make_minimal_project(scaffold)
    write_budgets(scaffold, ROW.format(pid="PB-001", refs="src/demo"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_budget_with_empty_refs_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_budgets(scaffold, ROW.format(pid="PB-001", refs=""))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "PB PB-001 back-links nothing" in report_of(scaffold)


def test_malformed_pb_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_budgets(scaffold, ROW.format(pid="PB-XX", refs="SR-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "PB id 'PB-XX' is malformed" in report_of(scaffold)


def test_placeholder_budget_registry_is_inert(scaffold):
    # The bootstrapped PB-000 placeholder must never block a gate for a project
    # that uses real spine rows but no budgets (same stance as interfaces.csv):
    # it survives even --no-placeholders, which the spine does not.
    make_minimal_project(scaffold)
    assert pb_path(scaffold).exists()  # bootstrap laid down the registry
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # With no real PB rows, no budget section/counts are emitted at all.
    assert "budgets=" not in proc.stdout
