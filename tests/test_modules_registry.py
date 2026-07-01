"""trace.py's optional coordinator module registry (Thread 20, MULTI_REPO.md):
MOD-### rows live off the SN->SR->LLR->TC spine (the multi-repo layer) but stay
traceable *within the coordinator repo* — each DelegatedSRs value back-links a
real coordinator SR, and a malformed MOD id or a dangling delegation fails
--strict. The registry is optional and coordinator-only: it is NOT scaffolded by
bootstrap, an absent file is a no-op, and a leftover MOD-000 never blocks a gate.
An external/reused part referenced only via the IF-### catalog may delegate
nothing, so an empty back-link is allowed here (unlike PB).
"""

from conftest import make_minimal_project, run_py

MOD_HEADER = "MOD-ID,Module,Repo,DelegatedSRs,Version,Type,Owner,Notes\n"
ROW = "{mid},widget,https://example.com/org/widget,{delegated},v1,owned,Integration,note\n"


def mod_path(root):
    return root / "docs" / "requirements" / "modules.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_modules(root, *rows):
    mod_path(root).write_text(MOD_HEADER + "".join(rows), encoding="utf-8")


def test_registry_not_scaffolded_and_absent_file_is_noop(scaffold):
    # modules.csv is the coordinator-only multi-repo layer: bootstrap does not lay
    # it down, and a single-repo project's trace run must ignore its absence.
    make_minimal_project(scaffold)
    assert not mod_path(scaffold).exists()
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "modules=" not in proc.stdout


def test_clean_module_delegating_real_sr_passes(scaffold):
    make_minimal_project(scaffold)
    write_modules(scaffold, ROW.format(mid="MOD-001", delegated="SR-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "modules=1 module-findings=0" in proc.stdout


def test_module_delegating_unknown_sr_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_modules(scaffold, ROW.format(mid="MOD-001", delegated="SR-999"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "MOD MOD-001 delegates unknown SR-999" in report_of(scaffold)


def test_module_with_empty_delegation_passes(scaffold):
    # An external/reused part referenced only via the interface catalog delegates
    # no functional SR, so an empty DelegatedSRs is allowed (unlike PB's Refs).
    make_minimal_project(scaffold)
    write_modules(scaffold, ROW.format(mid="MOD-001", delegated=""))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "modules=1 module-findings=0" in proc.stdout


def test_malformed_mod_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_modules(scaffold, ROW.format(mid="MOD-XX", delegated="SR-001"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "MOD id 'MOD-XX' is malformed" in report_of(scaffold)


def test_placeholder_module_row_is_inert(scaffold):
    # A MOD-000 example row (the template's placeholder) must never block a gate,
    # even under --no-placeholders, the same stance as interfaces.csv / PB-000.
    make_minimal_project(scaffold)
    write_modules(scaffold, ROW.format(mid="MOD-000", delegated="SR-000"))
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # With no real MOD rows, no module section/counts are emitted at all.
    assert "modules=" not in proc.stdout


def test_optional_columns_do_not_break_strict_schema(scaffold):
    # The Delegated/ParentRef markers and the modules registry are schema-safe: a
    # coordinator SR carrying an optional Delegated column still passes
    # --strict-schema (the optional-column tolerance, like Area/Lifecycle/PB).
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    text = srs.read_text(encoding="utf-8")
    header, row = text.splitlines()[0], text.splitlines()[1]
    srs.write_text(header + ",Delegated\n" + row + ",MOD-001\n", encoding="utf-8")
    write_modules(scaffold, ROW.format(mid="MOD-001", delegated="SR-001"))
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
