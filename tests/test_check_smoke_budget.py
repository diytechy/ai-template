"""WI-281 — the smoke wall-clock budget check (scripts/check_smoke_budget.py).

Exercises the CI-facing wall-clock half of the smoke budget via `--elapsed` (no
real suite run, so this stays a fast smoke test), plus fresh runs with a stubbed
child: warn softens only timing, while test failures always propagate. The
always-on deterministic half is tests/test_smoke_budget.py.
"""

import subprocess
import sys
import runpy

import pytest

from conftest import ROOT

SCRIPT = ROOT / "scripts" / "check_smoke_budget.py"


def _run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        encoding="utf-8",
    )


def test_within_budget_passes_both_modes():
    for mode in ("warn", "enforce"):
        proc = _run("--elapsed", "5", "--mode", mode)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "within" in proc.stdout


def test_over_budget_warns_but_does_not_fail():
    # The default (and warn mode) reports a breach but exits 0 — the repo's
    # warn-first stance for noisy runtime metrics; the deterministic ratchet is
    # the enforced floor.
    proc = _run("--elapsed", "99999")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OVER" in proc.stdout
    assert "WARN" in proc.stdout


def test_over_budget_enforce_fails():
    proc = _run("--elapsed", "99999", "--mode", "enforce")
    assert proc.returncode == 1
    assert "OVER" in proc.stdout


def test_reads_declared_budget_from_stack_ini():
    # The verdict cites the declared [smoke-budget] seconds (single source of
    # truth), so a budget re-stamp flows through without touching the script.
    import configparser

    cp = configparser.ConfigParser(interpolation=None)
    cp.read(ROOT / "docs" / "stack.ini", encoding="utf-8-sig")
    budget = int(float(cp["smoke-budget"]["seconds"]))
    proc = _run("--elapsed", "1")
    assert "{}s budget".format(budget) in proc.stdout, proc.stdout


@pytest.mark.parametrize("mode", ["warn", "enforce"])
@pytest.mark.parametrize(
    "child_code,elapsed", [(0, 1), (1, 1), (5, 1), (1, 99999), (0, 99999)]
)
def test_fresh_run_preserves_test_failure_and_reports_budget(
    monkeypatch, capsys, mode, child_code, elapsed
):
    script = runpy.run_path(str(SCRIPT))
    clock = iter((0, elapsed))
    monkeypatch.setattr(script["time"], "perf_counter", lambda: next(clock))
    monkeypatch.setattr(
        script["subprocess"],
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], child_code),
    )
    expected = child_code or int(elapsed > 90 and mode == "enforce")
    assert script["main"](["--mode", mode]) == expected
    out = capsys.readouterr()
    assert "smoke wall-clock budget:" in out.out
    assert ("OVER" if elapsed > 90 else "within") in out.out
