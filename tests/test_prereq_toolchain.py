"""The toolchain prereq the rest of this suite assumes.

Runs in the SLOW tier (`conftest.SLOW_MODULES`), so the hard stop lands at slice
close and in CI — where a gate result is actually claimed — while the per-commit
bar stays passable on a machine that has not been provisioned yet. It is the one
place an environment shortfall is reported as what it is: named once and loudly,
rather than ~50 downstream skips-and-reds that read like branch defects. The
`pytest_sessionstart` banner in `conftest.py` still fires on EVERY run including
`-m smoke`, so the commit bar keeps the warning and loses only the failure.

Two shortfalls live here, on the same division of labour with `conftest.py`:

- the **interpreter floor** — `skip_below_floor` marks the toolchain-DEPENDENT
  tests skipped, because their preconditions genuinely cannot be met, and this
  module FAILS so a below-floor session can never be mistaken for green;
- the **environment gates** (WI-326) — `skip_without_env_gates` /
  `env_gate_skipif` mark the shell- and git-driven tests skipped, and this module
  FAILS on any gate declared `required`.

The floor is read from `agent_common.MIN_PYTHON` — the same constant the
dispatcher's WI-286 harness gate and `scripts/dev-setup.sh` enforce — and the
gates from `conftest.ENV_GATES`, so each is declared once and flows here
untouched.

**One thing here is NOT verified, and is recorded as unverified rather than
claimed.** The environment gate hard-fails wherever the full suite runs, which
includes CI's `windows-latest` lane. Whether that runner puts `sh.exe` on PATH
could not be determined from the runner-images documentation, and this branch has
never been pushed, so there is no CI evidence either way. If it does not, the
first push turns a *silent* skip of ~250 tests into a red cell — which is this
check working, not a regression, and the remedy is one PATH line in the workflow.
The branch has already been wrong twice about what an OS permits, in opposite
directions (127- and 128-REVIEW-A), so the rule stands: one machine is one data
point, and an unmeasured claim is stated as unmeasured.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

from conftest import (
    ENV_GATES,
    ROOT,
    declared_python_floor,
    env_gate_shortfalls,
    floor_shortfall,
    load_script,
)


def _floor_str():
    return ".".join(str(p) for p in declared_python_floor())


def _diagnosis(subject, short, remedy_extra=""):
    """The loud message. Names the shortfall, the interpreter it came from, what
    it costs, and the remedy — so a reader who has never seen this failure can
    act on it without opening a single source file."""
    return (
        "\n"
        "\n=============================== TOOLCHAIN PREREQ ==============================="
        "\n{subject}: {short}."
        "\n"
        "\n  interpreter : {exe}"
        "\n  root .venv  : {venv}"
        "\n  declared floor: Python {floor}+  (agent_common.MIN_PYTHON — the same"
        "\n                  constant the dispatcher preflight and dev-setup enforce)"
        "\n"
        "\nWhat this costs: every test whose precondition is a floor-satisfying"
        "\ntoolchain SKIPS (the agent_loop dispatch/integrate/train/recovery/"
        "\nmigration/dualplan modules and the dev-setup install path). The suite's"
        "\nremaining result is therefore PARTIAL — it is not a gate result, and a"
        "\nfull-suite green cannot be produced on this machine."
        "\n"
        "\nRemedy: install a Python {floor}+ interpreter, then recreate the venv:"
        "\n    scripts/dev-setup --install{extra}"
        "\n================================================================================"
        "\n"
    ).format(
        subject=subject,
        short=short,
        exe=sys.executable,
        venv=load_script("agent_common").venv_python(ROOT) or "(absent)",
        floor=_floor_str(),
        extra=remedy_extra,
    )


def test_interpreter_meets_the_declared_floor():
    """The RUNNING interpreter clears the floor.

    This is the precondition `seed_venv` depends on: it builds each dispatch
    fixture's `.venv` from this process's own base, so a below-floor runner hands
    the dispatcher a venv its own preflight must refuse.
    """
    short = floor_shortfall()
    assert short is None, _diagnosis("the interpreter running this suite", short)


def test_root_venv_meets_the_declared_floor():
    """The repo's own `./.venv` — what dev-setup provisions — clears the floor.

    Distinct from the test above: `agent_dispatch._harness_floor_failures` probes
    the ROOT .venv, not the running interpreter, so an ambient-but-modern Python
    running a stale .venv still refuses at dispatch. Absent .venv is not this
    test's business (CI runs the suite without one, and the dispatcher's own
    fail-closed gate owns that shape) — so it skips rather than inventing a red.
    """
    venv_py = load_script("agent_common").venv_python(ROOT)
    if venv_py is None:
        import pytest

        pytest.skip(
            "no ./.venv in this checkout — the dispatcher preflight owns that case"
        )
    short = floor_shortfall(venv_py)
    assert short is None, _diagnosis(
        "the repo's ./.venv at {}".format(Path(venv_py)),
        short,
        remedy_extra="   # offers to recreate a below-floor ./.venv",
    )


def _gate_diagnosis(missing):
    """The loud message for an unsatisfied environment gate. Same shape as
    `_diagnosis`: name the shortfall, what it costs, and the remedy, so a reader
    who has never seen this failure can act on it without opening a source
    file."""
    body = []
    for gate in missing:
        body.append("\n  {}: {}".format(gate.name, gate.cost))
        body.append("\n      remedy: {}".format(gate.remedy()))
    return (
        "\n"
        "\n=============================== ENVIRONMENT GATE ==============================="
        "\n{n} of {total} declared environment gates are unsatisfied on this machine."
        "{body}"
        "\n"
        "\nWhat this costs: the tests gated on them do not RUN, and the suite still"
        "\nprints a green — the dishonest-green shape SN-008 forbids, one level up"
        "\n(not a skipped check, but a skipped check-OF-the-check). Measured"
        "\n2026-07-26 on Windows: 1540 passed / 54 skipped without Git\\bin on PATH"
        "\nversus 1587 passed / 7 skipped with it. Re-measured 2026-07-28 once the"
        "\ngit gate had an owner too: with BOTH gates closed, 250 tests across the"
        "\nsuite do not run — 26 of them the two hook suites that guard the commit"
        "\nfloor itself. A pass total from a machine in this state is NOT comparable"
        "\nwith one from a fully-gated machine."
        "\n"
        "\nThis failure is the ENVIRONMENT, not the branch. It is deliberately not"
        "\nrepaired automatically: a harness that silently prepends a PATH entry hides"
        "\nthe identical fact one layer down."
        "\n================================================================================"
        "\n"
    ).format(n=len(missing), total=len(ENV_GATES), body="".join(body))


def test_every_required_environment_gate_is_satisfied():
    """Every environment gate declared `required` in `conftest.ENV_GATES` holds.

    WI-326's "announce always, gate at the gate": the session banner warns on
    every run, and this is the hard stop — reached only in the full suite, which
    is what `check.py`'s `tests+coverage` step runs at the gate and what CI runs
    on all three platforms.
    """
    missing = [g for g in env_gate_shortfalls() if g.required]
    assert not missing, _gate_diagnosis(missing)


def test_a_gate_closed_run_announces_itself_at_both_ends(tmp_path):
    """Drive a REAL pytest run on a box with no gate satisfied, and read what it
    printed.

    `tests/test_env_gates.py` unit-tests the helpers; nothing there proves the two
    pytest HOOKS are wired, and a banner that is never printed is exactly the
    defect WI-326 exists to fix. So this constructs the unprovisioned box — PATH
    reduced to one empty directory, which makes `shutil.which` return None for
    every tool on every platform (`shutil.which` reads `os.environ["PATH"]` when
    set, with no `os.defpath` fallback) — and asserts both ends fire: the
    predicted banner on stderr before the first test, and the measured count on
    stdout after the last.

    `test_pre_push_hook.py` is the subject because it skips at MODULE level, so
    the run costs no fixtures — and it is the `skipif` form, the one a substring
    count under-reads first if the two skip helpers ever drift apart.

    The SATISFIED twin is constructed too, via `KIT_ENV_GATES_SATISFIED` (read by
    `conftest.env_gate_shortfalls`), rather than by running on this machine and
    hoping it is provisioned. The first version of this test inherited the
    runner's PATH for that half, so it PASSED here and would have RED on exactly
    the unprovisioned Windows box WI-326 targets — an adversarial review measured
    it. It also ran `--collect-only`, so zero tests ran and the count path was
    never exercised at all; both halves now run the real thing.
    """
    empty = tmp_path / "nothing"
    empty.mkdir()
    base = dict(os.environ, PYTEST_CPU_CAP="off")
    base.pop("PYTEST_ADDOPTS", None)
    base.pop("KIT_ENV_GATES_SATISFIED", None)
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:xdist",
        "tests/test_pre_push_hook.py",
    ]

    closed = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=dict(base, PATH=str(empty)),
    )
    combined = closed.stdout + closed.stderr
    assert "ENVIRONMENT GATE:" in closed.stderr, combined
    assert "posix-shell" in closed.stderr, combined
    assert "ENVIRONMENT-GATED SKIPS:" in closed.stdout, combined

    # The count is the point, so read it rather than trusting the label.
    counted = int(
        re.search(r"ENVIRONMENT-GATED SKIPS: (\d+) test", closed.stdout).group(1)
    )
    reported = int(re.search(r"(\d+) skipped", closed.stdout).group(1))
    assert counted == reported > 0, combined

    # The twin: gates declared satisfied, same command, same machine. Neither
    # line may appear — otherwise every assertion above would pass on any run.
    satisfied = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=dict(base, PATH=str(empty), KIT_ENV_GATES_SATISFIED="1"),
    )
    both = satisfied.stdout + satisfied.stderr
    assert "ENVIRONMENT-GATED SKIPS:" not in satisfied.stdout, both
    assert "ENVIRONMENT GATE:" not in satisfied.stderr, both
