"""check.py end-to-end: the documented flow must be green on a minimal project,
and the tier/coverage wiring must not silently skip tests."""

from conftest import load_script, make_minimal_project, run_py


def test_minimal_project_is_green(scaffold):
    # The full documented flow: scaffold -> code + traced registries -> harness.
    # This is the regression test for "fresh clone fails": check.py must find
    # ruff/pytest via the running interpreter, not a PATH that lacks the venv.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/check.py", "--gate", "all", "--tier", "all"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT: PASS" in proc.stdout
    # The regenerated architecture doc carries the Mermaid dependency diagram.
    arch = (scaffold / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "```mermaid" in arch
    assert "src/demo" in arch


def test_unmarked_test_runs_in_full_tier(scaffold):
    # An unmarked test must run pre-merge (tier full); the old opt-in marker
    # scheme silently deselected it.
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_unmarked.py").write_text(
        '"""An ordinary test with no tier marker."""\n\n\n'
        "def test_unmarked_runs():\n    assert True\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "2 passed" in proc.stdout  # the smoke test AND the unmarked one


def test_smoke_tier_runs_only_smoke_and_skips_coverage_gate(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_unmarked.py").write_text(
        '"""An ordinary test with no tier marker."""\n\n\n'
        "def test_unmarked_runs():\n    assert True\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "smoke"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 passed" in proc.stdout  # only the @pytest.mark.smoke test


def test_failing_test_fails_the_harness(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_broken.py").write_text(
        '"""Deliberately failing test."""\n\n\ndef test_broken():\n    assert False\n',
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "full"], cwd=scaffold)
    assert proc.returncode != 0
    assert "RESULT: FAIL" in proc.stdout


def test_step_plan_wiring():
    # Unit-level checks on the step table, without spawning tools.
    check = load_script("check")
    assert check.TIERS["full"] == "not release"  # unmarked tests run pre-merge

    def cmd_of(plan, name):
        return next(s[2] for s in plan if s[0] == name)

    smoke = check.steps(80, "smoke", "G3")
    full = check.steps(80, "full", "all")
    smoke_pytest = cmd_of(smoke, "tests+coverage")
    full_pytest = cmd_of(full, "tests+coverage")
    # Coverage threshold applies to full/release, never to the smoke subset.
    assert not any(a.startswith("--cov-fail-under") for a in smoke_pytest)
    assert "--cov-fail-under=80" in full_pytest
    # G3/all adds the SR status criterion to traceability.
    assert "--require-verified" in cmd_of(full, "traceability")
    assert "--require-verified" not in cmd_of(
        check.steps(80, "all", "G2"), "traceability"
    )
    # Tools run via this interpreter (-m), not a bare PATH lookup.
    assert full_pytest[1:3] == ["-m", "pytest"]
    assert cmd_of(full, "lint")[1:3] == ["-m", "ruff"]
