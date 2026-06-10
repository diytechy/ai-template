"""Bootstrap must produce a scaffold that is green out of the box."""

from conftest import SCRIPTS, run_py


def test_scaffold_contains_expected_files(scaffold):
    for rel in [
        "CLAUDE.md",
        ".gitignore",
        "pytest.ini",
        "docs/process.md",
        "docs/status.md",
        "docs/architecture.md",
        "docs/requirements/system-requirements.csv",
        "docs/test/test-cases.csv",
        "scripts/check.py",
        "scripts/gen_cases.py",
        ".github/workflows/check.yml",
        "src/.gitkeep",
        "tests/.gitkeep",
    ]:
        assert (scaffold / rel).exists(), "missing from scaffold: " + rel


def test_fresh_scaffold_passes_archmap_check_and_trace(scaffold):
    # Bootstrap runs the generators itself, so --check must pass immediately —
    # a fresh repo must not start with a failing harness.
    proc = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout


def test_scaffold_architecture_has_generated_diagram_block(scaffold):
    arch = (scaffold / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "BEGIN GENERATED DEPENDENCY DIAGRAM" in arch
    # Empty src at bootstrap time -> the spliced placeholder, not the template's.
    assert "(no source scanned)" in arch


def test_dry_run_writes_nothing(tmp_path):
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", tmp_path / "repo", "--dry-run"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert not (tmp_path / "repo").exists()


def test_rerun_skips_existing_files(scaffold):
    (scaffold / "CLAUDE.md").write_text("customized", encoding="utf-8")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", scaffold], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (scaffold / "CLAUDE.md").read_text(encoding="utf-8") == "customized"
