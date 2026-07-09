"""trace.py's optional domain-neutral component registry (the AXES/CMP layer,
process-options.md "Component layer"): CMP-### rows live off the SN->SR->LLR->TC
spine as the set-grained knowledge + lifecycle home. Structure is derived, never
restated on the CMP row — membership is a `Component` tag on the primitive rows —
so what trace.py checks is exactly the joins: PartOf / SupersededBy must name real
CMP ids, a primitive's Component tag must resolve to a real CMP row, a malformed
CMP id fails --strict, and a leftover CMP-000 placeholder never blocks a gate.
"""

from conftest import make_minimal_project, run_py

CMP_HEADER = "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
ROW = "{cid},arm,physical,docs/knowledge/arm,{state},{sup},{partof},,note\n"


def cmp_path(root):
    return root / "docs" / "requirements" / "components.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_cmps(root, *rows):
    cmp_path(root).write_text(CMP_HEADER + "".join(rows), encoding="utf-8")


def row(cid, state="planned", sup="", partof=""):
    return ROW.format(cid=cid, state=state, sup=sup, partof=partof)


def test_scaffolded_placeholder_is_inert(scaffold):
    # bootstrap lays components.csv down with only the CMP-000 example row; the
    # placeholder never blocks a gate, even under --no-placeholders (the
    # interfaces.csv / PB-000 / MOD-000 stance).
    make_minimal_project(scaffold)
    assert cmp_path(scaffold).exists()
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "components=" not in proc.stdout  # no real rows -> no counts emitted


def test_clean_component_rows_pass(scaffold):
    make_minimal_project(scaffold)
    write_cmps(
        scaffold,
        row("CMP-001"),
        row("CMP-002", partof="CMP-001", sup=""),
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "components=2 component-findings=0" in proc.stdout


def test_partof_must_name_a_real_cmp(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001", partof="CMP-999"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CMP CMP-001 PartOf references unknown CMP-999" in report_of(scaffold)


def test_supersededby_must_name_a_real_cmp(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001", state="deprecated", sup="CMP-777"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CMP CMP-001 SupersededBy references unknown CMP-777" in report_of(scaffold)


def test_llr_component_tag_must_resolve(scaffold):
    # The membership join, checked from the primitive side: an LLR tagged with a
    # phantom component is a finding once a real CMP registry exists.
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    text = llr.read_text(encoding="utf-8").rstrip("\n").splitlines()
    text[0] += ",Component"
    text[1] += ",CMP-404"
    llr.write_text("\n".join(text) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "Component tag references unknown CMP-404" in report_of(scaffold)


def test_llr_component_tag_resolving_passes(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    text = llr.read_text(encoding="utf-8").rstrip("\n").splitlines()
    text[0] += ",Component"
    text[1] += ",CMP-001"
    llr.write_text("\n".join(text) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "component-findings=0" in proc.stdout


def test_malformed_cmp_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-XX"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CMP id 'CMP-XX' is malformed" in report_of(scaffold)
