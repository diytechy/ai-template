"""WI-281 — the smoke wall-clock budget check (scripts/check_smoke_budget.py).

Exercises the wall-clock half of the smoke budget without a real suite run, so
this stays a fast smoke test: via `--elapsed`, the warn default reports but
never fails and `--mode enforce` fails only on breach; in process, the timed
form runs a stand-in tier and exits with a red tier's own code. The always-on
deterministic half is tests/test_smoke_budget.py.
"""

import importlib.util
import subprocess
import sys

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


def _load_script():
    spec = importlib.util.spec_from_file_location("check_smoke_budget", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _stand_in_tier(monkeypatch, exit_code, budget=None):
    """The script with a trivial interpreter command as its smoke tier, and
    optionally a stood-in budget, so `main` times a run that costs nothing."""
    module = _load_script()
    tier = [sys.executable, "-c", "import sys; sys.exit({})".format(exit_code)]
    monkeypatch.setattr(module, "smoke_argv", lambda cp: tier)
    if budget is not None:
        monkeypatch.setattr(module, "declared_seconds", lambda cp: budget)
    return module


def test_a_red_tier_exits_with_its_own_code_and_still_reports_its_time(
    monkeypatch, capsys
):
    module = _stand_in_tier(monkeypatch, 3)
    for mode in ("warn", "enforce"):
        assert module.main(["--mode", mode]) == 3, mode
        out, err = capsys.readouterr()
        assert "smoke wall-clock budget:" in out, mode
        assert "note: smoke tier exited 3" in err, mode


def test_a_green_tier_within_budget_exits_zero(monkeypatch, capsys):
    module = _stand_in_tier(monkeypatch, 0)
    assert module.main(["--mode", "enforce"]) == 0
    out, err = capsys.readouterr()
    assert "-> within" in out
    assert "note: smoke tier exited" not in err


def test_a_red_tier_over_budget_reports_both_and_exits_with_its_code(
    monkeypatch, capsys
):
    module = _stand_in_tier(monkeypatch, 4, budget=0.0)
    assert module.main(["--mode", "enforce"]) == 4
    out, err = capsys.readouterr()
    assert "-> OVER" in out
    assert "FAIL (enforce):" in err
    assert "note: smoke tier exited 4" in err
