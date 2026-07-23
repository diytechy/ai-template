"""Per-module coverage floors (WI-279; repo-review 2026-07-22 M-4).

check_coverage.py is the kit-owned, stdlib-only comparator that stops the global
--cov-fail-under floor from hiding a thin high-risk module behind well-tested
ones. It reads coverage.py's JSON report (pytest-cov --cov-report=json) and the
docs/coverage-floors census, and fails when a declared module is below its floor
or absent from the report; a missing report SKIPs (an unmeasured run, e.g. the
smoke tier), and no floors is a clean no-op.

These tests exercise the pure functions in-process and drive the CLI end-to-end
over crafted report/floors files, plus prove the step wires into the harness.
"""

import json

from conftest import SCRIPTS, load_script, make_minimal_project, run_py

check = load_script("check_coverage")

MOD = "project-trajectory/scripts/agent_session.py"
GATE = "project-trajectory/scripts/subagent_gate.py"


def _report(path, files, sep="/"):
    """Write a minimal coverage.py JSON report: {relpath: percent}. `sep`
    controls the path separator in the keys so the Windows-vs-POSIX and
    absolute-vs-relative matching can be exercised."""
    keyed = {
        k.replace("/", sep): {"summary": {"percent_covered": v}}
        for k, v in files.items()
    }
    data = {"files": keyed, "totals": {"percent_covered": 0.0}}
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _floors(path, text):
    path.write_text(text, encoding="utf-8")
    return path


# --- pure functions -----------------------------------------------------------
def test_load_floors_parses_and_ignores_comments(tmp_path):
    f = _floors(
        tmp_path / "floors",
        "# per-module floors\n"
        "\n"
        "  project-trajectory/scripts/agent_session.py   74   # security boundary\n"
        "project-trajectory/scripts/subagent_gate.py 40\n",
    )
    floors = check.load_floors(f)
    assert [(m, p) for m, p, _ln in floors] == [(MOD, 74.0), (GATE, 40.0)]


def test_load_floors_absent_file_is_empty(tmp_path):
    assert check.load_floors(tmp_path / "nope") == []


def test_load_floors_rejects_malformed_lines(tmp_path):
    import pytest

    for bad, needle in (
        ("mod 12 extra\n", "expected"),
        ("mod notanumber\n", "not a number"),
        ("mod 140\n", "out of range"),
        ("mod -3\n", "out of range"),
        ("lonelytoken\n", "expected"),
    ):
        with pytest.raises(ValueError) as exc:
            check.load_floors(_floors(tmp_path / "f", bad))
        assert needle in str(exc.value)


def test_load_report_absent_is_none_and_parses_percent(tmp_path):
    assert check.load_report(tmp_path / "nope.json") is None
    r = _report(tmp_path / "c.json", {MOD: 74.3, GATE: 40.0})
    percents = check.load_report(r)
    assert percents[MOD] == 74.3 and percents[GATE] == 40.0


def test_module_percent_matches_exact_suffix_and_backslash(tmp_path):
    # exact relative key, an absolute POSIX key (suffix match), and a
    # Windows-separator key all resolve to the same repo-relative module.
    for sep, prefix in (("/", ""), ("/", "/abs/root/"), ("\\", "C:\\abs\\root\\")):
        keys = {prefix.replace("/", sep) + MOD.replace("/", sep): 74.0}
        # load_report normalizes separators; emulate by building the map directly.
        percents = {k.replace("\\", "/"): v for k, v in keys.items()}
        assert check.module_percent(percents, MOD) == 74.0
    # a partial-name near-miss must NOT match on the '/' boundary
    percents = {"project-trajectory/scripts/my_agent_session.py": 99.0}
    assert check.module_percent(percents, MOD) is None


def test_evaluate_ok_fail_and_missing():
    floors = [(MOD, 74.0, 1), (GATE, 40.0, 2), ("gone.py", 50.0, 3)]
    percents = {MOD: 74.0, GATE: 39.9}  # gate just below, MOD exactly at floor
    results = {
        m: (measured, status)
        for m, _f, measured, status in check.evaluate(floors, percents)
    }
    assert results[MOD] == (74.0, "OK")  # exactly at floor is OK
    assert results[GATE][1] == "FAIL"
    assert results["gone.py"] == (None, "MISSING")


# --- CLI end-to-end -----------------------------------------------------------
def _run(tmp_path, report=None, floors=None):
    args = [SCRIPTS / "check_coverage.py"]
    if report is not None:
        args += ["--report", str(report)]
    if floors is not None:
        args += ["--floors", str(floors)]
    return run_py(args, cwd=tmp_path)


def test_cli_passes_when_all_floors_hold(tmp_path):
    report = _report(tmp_path / "c.json", {MOD: 80.0, GATE: 45.0})
    floors = _floors(tmp_path / "f", MOD + " 74\n" + GATE + " 40\n")
    proc = _run(tmp_path, report, floors)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "all 2 module floor(s) hold" in proc.stdout


def test_cli_fails_on_a_breach(tmp_path):
    report = _report(tmp_path / "c.json", {MOD: 73.9, GATE: 45.0})
    floors = _floors(tmp_path / "f", MOD + " 74\n" + GATE + " 40\n")
    proc = _run(tmp_path, report, floors)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "1/2 module floor(s) breached" in proc.stdout
    assert "agent_session.py" in proc.stdout


def test_cli_fails_when_declared_module_absent_from_report(tmp_path):
    # A declared floor whose module vanished from measurement must FAIL loudly,
    # never quietly pass — the whole point is to keep watching that module.
    report = _report(tmp_path / "c.json", {GATE: 45.0})
    floors = _floors(tmp_path / "f", MOD + " 74\n" + GATE + " 40\n")
    proc = _run(tmp_path, report, floors)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "absent from" in proc.stdout


def test_cli_skips_when_report_absent(tmp_path):
    # No coverage.json (e.g. the smoke tier, where the global floor is also
    # skipped): SKIP, not a false failure — the check_perf.py posture.
    floors = _floors(tmp_path / "f", MOD + " 74\n")
    proc = _run(tmp_path, report=tmp_path / "missing.json", floors=floors)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SKIP" in proc.stdout


def test_cli_noop_when_no_floors_declared(tmp_path):
    proc = _run(tmp_path, report=tmp_path / "missing.json", floors=tmp_path / "missing")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no per-module coverage floors declared" in proc.stdout


def test_cli_fails_loudly_on_malformed_floors(tmp_path):
    floors = _floors(tmp_path / "f", MOD + " notanumber\n")
    proc = _run(tmp_path, report=tmp_path / "missing.json", floors=floors)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "not a number" in proc.stdout


# --- harness wiring -----------------------------------------------------------
def test_module_coverage_step_wires_into_the_harness(scaffold):
    # The opt-in step slots into check.py's plan as a G3 product step with no
    # kit-script edit (the extra_steps contract), and passes as a no-op until a
    # docs/coverage-floors census is authored.
    make_minimal_project(scaffold)
    stack = scaffold / "docs" / "stack.ini"
    stack.write_text(
        stack.read_text(encoding="utf-8")
        + "\n[step:module-coverage]\n"
        + "command = {py} scripts/check_coverage.py\n"
        + "gates = G3\nlayer = product\n",
        encoding="utf-8",
    )
    listed = run_py(["scripts/check.py", "--gate", "G3", "--list"], cwd=scaffold)
    assert listed.returncode == 0, listed.stdout + listed.stderr
    assert "module-coverage" in listed.stdout

    ran = run_py(["scripts/check.py", "--run-step", "module-coverage"], cwd=scaffold)
    assert ran.returncode == 0, ran.stdout + ran.stderr
    assert "no per-module coverage floors declared" in ran.stdout
