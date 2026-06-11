"""check_flows.py: the authored Runtime-flows section is present, diagrammed,
and cites only real requirement ids (process.md §3 'Design-time runtime flows')."""

from conftest import make_minimal_project, run_py

FLOWS_OK = """
## Runtime flows (authored at G2)

```mermaid
sequenceDiagram
    participant UI as src/demo (LLR-001)
    Note over UI: SR-001 - add two numbers
    UI->>UI: add(a, b)
```
"""

FLOWS_NO_IDS = """
## Runtime flows (authored at G2)

```mermaid
sequenceDiagram
    participant UI
    UI->>UI: does something untraceable
```
"""

FLOWS_UNKNOWN_ID = FLOWS_OK.replace("SR-001", "SR-099")


def arch_path(root):
    return root / "docs" / "architecture.md"


def test_fresh_scaffold_template_section_passes(scaffold):
    # The copied ARCHITECTURE template ships a placeholder flow (ids ending
    # -000) and must start green, like every other template artifact.
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "check_flows: OK" in proc.stdout


def test_real_flow_with_known_ids_passes(scaffold):
    make_minimal_project(scaffold)
    arch_path(scaffold).write_text("# Architecture\n" + FLOWS_OK, encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_missing_section_fails(scaffold):
    make_minimal_project(scaffold)
    arch_path(scaffold).write_text("# Architecture\nno flows here\n", encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert 'no "Runtime flows" heading' in proc.stdout


def test_diagram_without_ids_fails(scaffold):
    make_minimal_project(scaffold)
    arch_path(scaffold).write_text("# Architecture\n" + FLOWS_NO_IDS, encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert "cites no SR/LLR id" in proc.stdout


def test_unknown_id_fails(scaffold):
    make_minimal_project(scaffold)
    arch_path(scaffold).write_text(
        "# Architecture\n" + FLOWS_UNKNOWN_ID, encoding="utf-8"
    )
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert "unknown id cited: SR-099" in proc.stdout


def test_harness_runs_design_flows_at_g2(scaffold):
    # check.py --gate G2 must include and enforce the design-flows step.
    make_minimal_project(scaffold)
    arch_path(scaffold).write_text("# Architecture\nno flows\n", encoding="utf-8")
    proc = run_py(["scripts/check.py", "--gate", "G2"], cwd=scaffold)
    assert proc.returncode != 0
    assert "design-flows" in proc.stdout
    assert "RESULT: FAIL" in proc.stdout
