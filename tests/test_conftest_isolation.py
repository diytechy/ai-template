"""The shared conftest makes `kitlib` importable at collection, in any order.

A test module's top-level `from kitlib import ...` runs when the module is
collected. When scripts/ reached sys.path only inside the first `load_script`
call, that import resolved only if some earlier-collected module had loaded a
script, so an xdist worker handed one such module alone failed to collect it.
A run of the whole suite hides the defect (some module always loads a script
first); only a run of the module on its own shows it, which is why the pin is a
subprocess that collects one module and nothing else.
"""

import importlib.util
import os
import subprocess
import sys

from conftest import ROOT, SCRIPTS, _put_scripts_on_path

# The cheapest of the modules that import kitlib before any load_script call:
# four in-memory tests, so the subprocess costs little more than its startup.
ISOLATED_MODULE = "tests/test_kitlib_station.py"


def _same_path(entry):
    return bool(entry) and os.path.normcase(os.path.abspath(entry)) == (
        os.path.normcase(os.path.abspath(SCRIPTS))
    )


def test_a_module_importing_kitlib_collects_on_its_own():
    """One xdist worker, not a serial run: a serial run hides the defect,
    because `pytest_sessionstart` loads a script (its interpreter-floor check)
    before collection on the controller, and a worker skips that hook. A
    single worker is the cheapest run that collects the module the way the
    failing runs did."""
    args = [sys.executable, "-X", "utf8", "-m", "pytest", "-q", "-n", "1"]
    args += ["-p", "no:cacheprovider"]
    if importlib.util.find_spec("pytest_randomly") is not None:
        args += ["-p", "no:randomly"]
    # The outer run's own pytest variables must not steer the inner one.
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTEST_")}
    proc = subprocess.run(
        [*args, ISOLATED_MODULE],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        encoding="utf-8",
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "ImportError" not in out, out
    summary = out.strip().splitlines()[-1]
    assert "passed" in summary and "error" not in summary, out


def test_scripts_lands_first_exactly_once(monkeypatch):
    """scripts/ must sit at index 0, where a subprocess finds its siblings: the
    kit's `trace.py` has to shadow the stdlib's for the scripts that import it
    by that name, so an entry further down (another spelling, left by some other
    path juggling) is moved rather than kept."""
    other = str(ROOT)
    elsewhere = str(SCRIPTS / "kitlib" / "..")  # the same directory, spelled apart
    monkeypatch.setattr(sys, "path", [other, elsewhere])

    _put_scripts_on_path()
    assert sys.path[0] == str(SCRIPTS)
    assert sum(_same_path(p) for p in sys.path) == 1
    assert other in sys.path

    before = list(sys.path)
    _put_scripts_on_path()
    assert sys.path == before, "a second call must leave sys.path as it is"
