"""`Hat-Refs` end to end: an undeclared hat reaches trace.py's exit code.

Split out of `test_trace_hats.py`, whose rule, vacuity, coverage and
derivation cases call trace.py's functions in-process and stay in the
per-commit smoke tier. This case bootstraps a scaffold and runs `trace.py
--strict` as a subprocess twice, so it is registered in `tests/conftest.py`'s
`SLOW_MODULES` and runs at slice/phase close and in CI.
"""

from conftest import make_minimal_project, run_py
from test_trace_hats import write_roster


def test_an_undeclared_hat_reds_a_real_run_under_strict(scaffold):
    make_minimal_project(scaffold)
    write_roster(scaffold)
    csv = scaffold / "docs" / "requirements" / "system-requirements.csv"
    text = csv.read_text(encoding="utf-8").splitlines()
    # Append the column to the header and a bad value to the first data row.
    text[0] += ",Hat-Refs"
    text[1] += ",SECRUITY"
    csv.write_text("\n".join(text) + "\n", encoding="utf-8")

    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FINDING (hat)" in proc.stdout, proc.stdout
    assert "SECRUITY" in proc.stdout

    # And it is non-vacuous in the other direction: the SAME tree with the name
    # spelled correctly exits zero.
    text[1] = text[1].replace("SECRUITY", "SECURITY")
    csv.write_text("\n".join(text) + "\n", encoding="utf-8")
    ok = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "FINDING (hat)" not in ok.stdout
