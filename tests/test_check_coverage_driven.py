"""The per-module coverage step wired into `check.py`, on a bootstrapped scaffold.

Split out of `test_check_coverage.py`, whose pure-function and CLI cases stay
in the per-commit smoke tier. This case takes the `scaffold` fixture (a real
`bootstrap.py` subprocess) and drives `check.py` twice, so it is registered in
`tests/conftest.py`'s `SLOW_MODULES` and runs at slice/phase close and in CI.
"""

from conftest import make_minimal_project, run_py


def test_module_coverage_step_wires_into_the_harness(scaffold):
    # The opt-in step slots into check.py's plan as a DevStg-Impl product step with no
    # kit-script edit (the extra_steps contract), and passes as a no-op until a
    # docs/coverage-floors census is authored.
    make_minimal_project(scaffold)
    stack = scaffold / "docs" / "stack.ini"
    stack.write_text(
        stack.read_text(encoding="utf-8")
        + "\n[step:module-coverage]\n"
        + "command = {py} scripts/check_coverage.py\n"
        + "gates = DevStg-Impl\nlayer = product\n",
        encoding="utf-8",
    )
    listed = run_py(
        ["scripts/check.py", "--gate", "DevStg-Impl", "--list"], cwd=scaffold
    )
    assert listed.returncode == 0, listed.stdout + listed.stderr
    assert "module-coverage" in listed.stdout

    ran = run_py(["scripts/check.py", "--run-step", "module-coverage"], cwd=scaffold)
    assert ran.returncode == 0, ran.stdout + ran.stderr
    assert "no per-module coverage floors declared" in ran.stdout
