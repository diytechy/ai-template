"""check_flows.py: the authored Runtime-flows section is present, diagrammed,
and cites only real requirement ids (process.md §3 'Design-time runtime flows')."""

from conftest import make_minimal_project, run_py

# Every fixture below is written as a REAL flows doc: a document title, then the
# "Runtime flows" SECTION inside it. The title must never be the thing the check
# latches onto (see test_titled_runtime_flows_with_deleted_section_fails), so the
# positive fixtures must not be shaped as title-only docs either - a fixture whose
# H1 *is* the section cannot expose that bug.
DOC_TITLE = "# Runtime flows — demo project (authored at DevStg-Tests)\n"

FLOWS_OK = """
## Runtime flows

```mermaid
sequenceDiagram
    participant UI as src/demo (LLR-001)
    Note over UI: SR-001 - add two numbers
    UI->>UI: add(a, b)
```
"""

FLOWS_NO_IDS = """
## Runtime flows

```mermaid
sequenceDiagram
    participant UI
    UI->>UI: does something untraceable
```
"""

FLOWS_UNKNOWN_ID = FLOWS_OK.replace("SR-001", "SR-099")

# The adversarial-review scenario (M1): the document is still TITLED "Runtime
# flows", a valid, id-citing mermaid block still sits in the doc - but the
# Runtime-flows section itself is gone. Before the fix the title heading was
# selected as the section and ran to EOF, so this passed.
TITLED_BUT_SECTION_DELETED = (
    DOC_TITLE
    + """
## Shape of the product

```mermaid
sequenceDiagram
    participant UI as src/demo (LLR-001)
    Note over UI: SR-001 - a diagram OUTSIDE any Runtime flows section
    UI->>UI: add(a, b)
```
"""
)


def flows_path(root):
    return root / "docs" / "runtime-flows.md"


def test_fresh_scaffold_template_section_passes(scaffold):
    # The copied RUNTIME_FLOWS template ships a placeholder flow (ids ending
    # -000) and must start green, like every other template artifact.
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "check_flows: OK" in proc.stdout


def test_scaffold_template_section_is_not_the_document_title(scaffold):
    # The shipped template must not be born with the shadow: deleting its
    # Runtime-flows section has to break the gate even though line 1 still
    # names the doc "Runtime flows".
    doc = flows_path(scaffold)
    lines = doc.read_text(encoding="utf-8").splitlines()
    heads = [ln for ln in lines if ln.startswith("#")]
    assert heads[0].lower().startswith("# runtime flows")  # still the title
    assert "## Runtime flows" in heads[1:], heads  # ...and a real section below


def test_real_flow_with_known_ids_passes(scaffold):
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text(DOC_TITLE + FLOWS_OK, encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # Counts distinct ids (SR-001 + LLR-001), not id kinds.
    assert "2 requirement id(s) cited" in proc.stdout


def test_missing_section_fails(scaffold):
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text("# Doc\nno flows here\n", encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert 'no "Runtime flows" section heading' in proc.stdout


def test_titled_runtime_flows_with_deleted_section_fails(scaffold):
    """REGRESSION (adversarial review M1): a doc TITLED "Runtime flows" whose
    flows section was deleted must FAIL, even though a valid, id-citing mermaid
    block survives elsewhere in it. The old rule matched the first heading whose
    title merely *started with* "runtime flows" at any level, so the H1 title
    shadowed the H2 section and, with no later H1, its "section" was the whole
    file - the DevStg-Tests gate could not fail on any doc named for it."""
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text(TITLED_BUT_SECTION_DELETED, encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert 'no "Runtime flows" section heading' in proc.stdout


def test_exact_section_heading_wins_over_a_longer_prefix_match(scaffold):
    # Two candidates below the title: the diagram-less "Runtime flows summary"
    # comes first, but the exact "Runtime flows" heading is the section.
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text(
        DOC_TITLE + "\n## Runtime flows summary\n\nprose only\n" + FLOWS_OK,
        encoding="utf-8",
    )
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 flow diagram(s)" in proc.stdout


def test_section_under_an_unrelated_document_title_passes(scaffold):
    # An adopter whose flows doc is titled anything else: the section is found
    # normally, and content in other sections is outside it.
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text(
        "# Architecture narrative\n\nintro\n" + FLOWS_OK + "\n## Notes\n\nafter\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 flow diagram(s)" in proc.stdout


def test_diagram_without_ids_fails(scaffold):
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text(DOC_TITLE + FLOWS_NO_IDS, encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert "cites no SR/LLR id" in proc.stdout


def test_unknown_id_fails(scaffold):
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text(DOC_TITLE + FLOWS_UNKNOWN_ID, encoding="utf-8")
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 1
    assert "unknown id cited: SR-099" in proc.stdout


def test_harness_runs_design_flows_at_g2(scaffold):
    # check.py --gate DevStg-Tests must include and enforce the design-flows step.
    make_minimal_project(scaffold)
    flows_path(scaffold).write_text("# Doc\nno flows\n", encoding="utf-8")
    proc = run_py(["scripts/check.py", "--gate", "DevStg-Tests"], cwd=scaffold)
    assert proc.returncode != 0
    assert "design-flows" in proc.stdout
    assert "RESULT: FAIL" in proc.stdout
