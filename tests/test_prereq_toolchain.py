"""The toolchain prereq the rest of this suite assumes.

Runs in the SMOKE tier (so the per-commit bar carries it, not just CI) and is the
one place a below-floor interpreter is reported as what it is: an environment
shortfall, named once and loudly, rather than ~50 downstream reds that read like
branch defects.

Division of labour with the guards in `conftest.py`:

- `skip_below_floor` marks the toolchain-DEPENDENT tests as skipped, because
  their preconditions genuinely cannot be met;
- this module FAILS, so a below-floor session can never be mistaken for green.

Both read the floor from `agent_common.MIN_PYTHON` — the same constant the
dispatcher's WI-286 harness gate and `scripts/dev-setup.sh` enforce — so a floor
bump lands in one place and flows here untouched.
"""

import sys
from pathlib import Path

from conftest import ROOT, declared_python_floor, floor_shortfall, load_script


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
