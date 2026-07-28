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
        "\nversus 1587 passed / 7 skipped with it — 47 tests never asked, 36 of them"
        "\nthe guards on the commit floor itself. A pass total from a machine in this"
        "\nstate is NOT comparable with one from a fully-gated machine."
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

    `tests/test_env_gates.py` unit-tests the helpers; nothing there proves the
    two pytest HOOKS are wired, and a banner that is never printed is exactly the
    defect WI-326 exists to fix. So this constructs the unprovisioned box — PATH
    reduced to one empty directory, which makes `shutil.which` return None for
    every tool on every platform — rather than inheriting whatever the runner
    happens to have, and asserts both ends fire: the predicted banner on stderr
    before the first test, and the measured count on stdout after the last.

    `test_pre_push_hook.py` is the subject because it skips at MODULE level, so
    the run costs no fixtures — and it is the skipif form, the one a substring
    count under-reads first if the two skip helpers ever drift apart.
    """
    empty = tmp_path / "nothing"
    empty.mkdir()
    env = dict(os.environ, PATH=str(empty), PYTEST_CPU_CAP="off")
    env.pop("PYTEST_ADDOPTS", None)
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:xdist",
            "tests/test_pre_push_hook.py",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=env,
    )
    combined = proc.stdout + proc.stderr
    assert "ENVIRONMENT GATE:" in proc.stderr, combined
    assert "posix-shell" in proc.stderr, combined
    assert "ENVIRONMENT-GATED SKIPS:" in proc.stdout, combined

    # The count is the point, so read it rather than trusting the label.
    counted = int(
        re.search(r"ENVIRONMENT-GATED SKIPS: (\d+) test", proc.stdout).group(1)
    )
    reported_skips = int(re.search(r"(\d+) skipped", proc.stdout).group(1))
    assert counted == reported_skips > 0, combined

    # And the mutation twin: the same command on THIS (provisioned) machine must
    # print neither line, or the assertions above would pass on any run at all.
    clean = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:xdist",
            "--collect-only",
            "tests/test_pre_push_hook.py",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env=dict(os.environ, PYTEST_CPU_CAP="off"),
    )
    assert "ENVIRONMENT-GATED SKIPS:" not in clean.stdout, clean.stdout + clean.stderr
    assert "ENVIRONMENT GATE:" not in clean.stderr, clean.stdout + clean.stderr
