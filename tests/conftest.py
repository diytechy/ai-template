"""Shared fixtures/helpers for the kit's self-tests.

The kit scripts must stay stdlib-only (downstream repos run them without pip);
this suite is meta-repo dev tooling, so pytest/ruff are fair game here. The
tests exercise the scripts the way a downstream user would: bootstrap a real
scaffold in a temp dir and run the actual commands.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "project-trajectory"
SCRIPTS = KIT / "scripts"


def load_script(name):
    """Import a kit script as a module (scripts/ is intentionally not a package).

    scripts/ is put on sys.path first so a script that imports a sibling — e.g.
    gen_trajectory's sanctioned `import check_trajectory` — resolves in-process
    too. Run as a subprocess the sibling resolves via sys.path[0], but
    importlib.exec_module does not add scripts/ itself, so the next author writing
    an in-process test of a sibling-importing script would otherwise hit a bare
    ImportError (THREAD_52_REVIEW.md F5)."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def augment_env(env):
    """Add subprocess-coverage wiring to `env` (a dict) when pytest-cov is
    measuring the parent (it exports `COV_CORE_DATAFILE`); a no-op otherwise.

    Most of the suite runs the kit scripts as subprocesses, which coverage does
    not see unless each child starts it (IMPROVEMENT_PLAN.md Thread 47 phase 6).
    Shared by run_py AND any test that builds its own subprocess env
    (test_check_privacy.lint_env, test_pre_push_hook.run_hook), so coverage is
    measured *uniformly* regardless of which helper a test uses — routing only
    run_py children left the privacy suite invisible and its module reading a
    misleadingly-low %. Points the child at `.coveragerc` +
    `tests/_cov/sitecustomize.py` (which calls `coverage.process_startup()`) and
    shares pytest-cov's datafile so the parallel data lands in one place for the
    session-end combine; `.coveragerc`'s [paths] remaps the temp-scaffold script
    copies back to the source tree. NB: `tests/_cov` is prepended to PYTHONPATH,
    so it would shadow any environment-provided `sitecustomize` during a measured
    run — harmless here (none exists; gated on an active pytest-cov)."""
    datafile = os.environ.get("COV_CORE_DATAFILE")
    if not datafile:
        return env
    env = dict(env)
    env["COVERAGE_PROCESS_START"] = str(ROOT / ".coveragerc")
    env["COVERAGE_FILE"] = datafile
    covdir = str(ROOT / "tests" / "_cov")
    env["PYTHONPATH"] = covdir + os.pathsep + env.get("PYTHONPATH", "")
    return env


def run_py(args, cwd):
    """Run `python <args>` in cwd, capturing output.

    stdin is closed (DEVNULL) so a script that *would* prompt on a TTY (e.g.
    bootstrap's agent-selection question) runs non-interactively and takes its
    default instead of blocking — the CI-safe path the tests must exercise.
    """
    return subprocess.run(
        [sys.executable] + [str(a) for a in args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=augment_env(dict(os.environ)),
    )


@pytest.fixture
def scaffold(tmp_path):
    """A fresh repo bootstrapped from the kit (the documented quick-start)."""
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return tmp_path


# --- A minimal but complete downstream project -------------------------------
# One pure function, one traced SN->SR->LLR->TC chain, one marked smoke test.
# Used by the harness tests; written ruff-format-clean on purpose.

DEMO_SRC = '''"""Demo pure core for the kit self-test. Pure — no I/O."""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a + b
'''

DEMO_TEST_CONFTEST = '''"""Make src/ importable for the tests (no install step needed)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
'''

DEMO_TEST = '''"""Verifies SR-001/LLR-001 (TC-001)."""

import pytest
from demo import add


@pytest.mark.smoke
def test_add_sr001():
    assert add(1, 2) == 3
'''

STAKEHOLDER_NEEDS = """# Stakeholder Needs (SN-###)

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Add two numbers. | Demo. | M | add(1,2) gives 3. |
"""

SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
"""

LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Implemented
"""

TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,Verified
"""


def make_minimal_project(root):
    """Fill a scaffold with the demo project + a fully traced registry chain,
    then refresh the generated arch map so the harness starts from truth."""
    (root / "src" / "demo.py").write_text(DEMO_SRC, encoding="utf-8")
    (root / "tests" / "conftest.py").write_text(DEMO_TEST_CONFTEST, encoding="utf-8")
    (root / "tests" / "test_demo.py").write_text(DEMO_TEST, encoding="utf-8")
    req = root / "docs" / "requirements"
    (req / "stakeholder-needs.md").write_text(STAKEHOLDER_NEEDS, encoding="utf-8")
    (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(TCS, encoding="utf-8")
    # A G2-complete project replaces the template's placeholder Runtime-flows
    # citations (SR-000/LLR-000) with its real ids, so the harness's
    # check_flows --no-placeholders step is satisfied.
    arch = root / "docs" / "architecture.md"
    arch.write_text(
        arch.read_text(encoding="utf-8")
        .replace("SR-000", "SR-001")
        .replace("LLR-000", "LLR-001"),
        encoding="utf-8",
    )
    # A G1-complete project's README cites its real need (the opt-out
    # need-coverage gate: every Must/Should SN is cited), replacing the -000 stub.
    readme = root / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "- **_(capability)_** — _(one line: what a user can do)_ (SN-000)",
            "- **Addition** — add two numbers (SN-001)",
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/gen_arch_map.py"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return root
