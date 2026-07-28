"""The environment-gate machinery (WI-326).

`test_prereq_toolchain.py` owns the hard stop — "this machine satisfies every
required gate" — and is SLOW-tiered so it lands at close and in CI. This module
owns the MACHINERY, is in-process and fast, and therefore stays in the smoke
tier: the helpers must keep working on every commit, not only at the gate.

Everything here CONSTRUCTS the condition it measures rather than inheriting the
runner's. A guard that merely re-reads the host's real PATH would pass on a
provisioned box no matter what the code did — the vacuous shape this repo has
now paid for six times. Each helper is therefore driven against a synthetic
gate that is unsatisfied by construction, and against its satisfied twin, so the
guard can fail in both directions.
"""

import shutil
import types

import pytest
from conftest import (
    ENV_GATE_SKIP_PREFIX,
    ENV_GATES,
    EnvGate,
    env_gate_banner,
    env_gate_skip_reason,
    env_gate_skipif,
    env_gate_shortfalls,
    env_gated_skip_count,
    skip_without_env_gates,
    unreachable_posix_shell,
)
import conftest

SATISFIED = EnvGate(
    name="always-there",
    required=True,
    probe=lambda: True,
    cost="nothing — this gate holds",
    remedy=lambda: "no action",
)
ABSENT = EnvGate(
    name="never-there",
    required=True,
    probe=lambda: False,
    cost="the synthetic tests SKIP",
    remedy=lambda: "install the synthetic tool",
)
OPTIONAL_ABSENT = ABSENT._replace(name="optional-absent", required=False)


@pytest.fixture
def gates(monkeypatch):
    """Replace the declared table with a constructed one: one gate that holds,
    one that does not. Returns a setter so a test can choose its own table."""

    def use(*table):
        monkeypatch.setattr(conftest, "ENV_GATES", tuple(table))
        return table

    use(SATISFIED, ABSENT)
    return use


# --- the declaration itself ---------------------------------------------------


def test_the_shipped_table_is_well_formed():
    """Every declared gate carries the four things a reader needs: a probe that
    returns a bool, a cost, and a remedy that renders to a non-empty string."""
    assert ENV_GATES, "no environment gates declared"
    for gate in ENV_GATES:
        assert isinstance(gate.probe(), bool), gate.name
        assert gate.cost.strip(), gate.name
        assert gate.remedy().strip(), gate.name
        assert isinstance(gate.required, bool), gate.name


def test_shortfalls_names_the_absent_gate_and_omits_the_present_one(gates):
    missing = env_gate_shortfalls()
    assert [g.name for g in missing] == ["never-there"]


def test_shortfalls_restricts_to_the_named_gates(gates):
    """A caller asking only about a gate it does not depend on gets nothing —
    otherwise every test would skip on any unsatisfied gate anywhere."""
    assert env_gate_shortfalls(("always-there",)) == []
    assert [g.name for g in env_gate_shortfalls(("never-there",))] == ["never-there"]


def test_shortfalls_is_empty_when_every_gate_holds(gates):
    """The mutation twin: with the absent gate removed the same call must return
    nothing, so a passing run above is evidence and not an accident."""
    gates(SATISFIED)
    assert env_gate_shortfalls() == []


# --- the two skip forms -------------------------------------------------------


def test_skip_helper_skips_on_an_absent_gate_and_carries_the_remedy(gates):
    with pytest.raises(pytest.skip.Exception) as caught:
        skip_without_env_gates("never-there")
    message = str(caught.value)
    assert ENV_GATE_SKIP_PREFIX in message
    assert "never-there" in message
    assert "install the synthetic tool" in message


def test_skip_helper_is_a_no_op_when_the_gate_holds(gates):
    """The direction that makes the test above meaningful: a satisfied gate must
    NOT skip, or every gated test would vanish silently."""
    skip_without_env_gates("always-there")


def test_skipif_form_carries_the_identical_reason(gates):
    """Both forms must produce the same string, because the terminal-summary
    count finds them with one substring test — two spellings would under-count
    exactly the module-level suites (pre-push) that skip that way."""
    mark = env_gate_skipif("never-there")
    assert mark.args[0] is True
    assert mark.kwargs["reason"] == env_gate_skip_reason([ABSENT])
    assert ENV_GATE_SKIP_PREFIX in mark.kwargs["reason"]


def test_skipif_form_is_inert_when_the_gate_holds(gates):
    mark = env_gate_skipif("always-there")
    assert mark.args[0] is False


def test_skip_reason_dedupes_a_shared_remedy(gates):
    """Two gates closed by the same action must not print that action twice."""
    twin = ABSENT._replace(name="never-there-2")
    reason = env_gate_skip_reason([ABSENT, twin])
    assert reason.count("install the synthetic tool") == 1
    assert "never-there" in reason and "never-there-2" in reason


# --- the banner ---------------------------------------------------------------


def test_banner_is_none_when_every_gate_holds(gates):
    gates(SATISFIED)
    assert env_gate_banner() is None


def test_banner_names_the_gate_its_cost_and_its_remedy(gates):
    banner = env_gate_banner()
    assert banner is not None
    assert "never-there" in banner
    assert "the synthetic tests SKIP" in banner
    assert "install the synthetic tool" in banner
    assert "REQUIRED" in banner


def test_banner_marks_only_required_gates_as_required(gates):
    gates(OPTIONAL_ABSENT)
    banner = env_gate_banner()
    assert "optional-absent" in banner
    assert "REQUIRED" not in banner


# --- the measured count -------------------------------------------------------


def _reporter(*reasons):
    """A minimal stand-in for pytest's terminalreporter carrying skip reports
    with the given reasons, in the (path, lineno, reason) longrepr shape pytest
    actually uses for a skip."""
    reports = [types.SimpleNamespace(longrepr=("t.py", 1, r)) for r in reasons]
    return types.SimpleNamespace(stats={"skipped": reports})


def test_count_counts_env_gated_skips():
    reason = "Skipped: " + env_gate_skip_reason([ABSENT])
    assert env_gated_skip_count(_reporter(reason, reason)) == 2


def test_count_ignores_an_unrelated_skip():
    """The mutation that matters: a platform skip (`needs a POSIX shell + exec
    bit` on Windows) has no remedy, so counting it would turn the number into
    noise. Only a DECLARED gate contributes."""
    assert env_gated_skip_count(_reporter("Skipped: needs a POSIX shell")) == 0
    assert env_gated_skip_count(_reporter("Skipped: no ./.venv in this checkout")) == 0


def test_count_is_zero_on_a_run_with_no_skips():
    assert env_gated_skip_count(types.SimpleNamespace(stats={})) == 0


def test_count_survives_a_report_with_no_longrepr_tuple():
    """xdist and some plugins hand back a bare string longrepr; the counter must
    not raise mid-summary and lose the whole report."""
    odd = types.SimpleNamespace(
        stats={"skipped": [types.SimpleNamespace(longrepr=None)]}
    )
    assert env_gated_skip_count(odd) == 0


# --- the remedy probe ---------------------------------------------------------


def test_unreachable_shell_is_none_when_sh_is_on_path(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda tool: "/usr/bin/" + tool)
    assert unreachable_posix_shell() is None


def test_unreachable_shell_names_the_git_directory_holding_it(monkeypatch, tmp_path):
    """The finding that made WI-326 actionable: Git for Windows installs sh.exe
    under Git\\bin but puts only Git\\cmd on PATH, so the shell is installed AND
    unreachable. Constructed here rather than probed, so this runs identically on
    POSIX."""
    monkeypatch.setattr(shutil, "which", lambda tool: None)
    monkeypatch.setenv("ProgramFiles", str(tmp_path))
    bin_dir = tmp_path / "Git" / "bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "sh.exe").write_text("", encoding="utf-8")
    assert unreachable_posix_shell() == bin_dir
    assert str(bin_dir) in conftest._posix_shell_remedy()


def test_unreachable_shell_is_none_when_nothing_is_installed(monkeypatch, tmp_path):
    monkeypatch.setattr(shutil, "which", lambda tool: None)
    monkeypatch.setenv("ProgramFiles", str(tmp_path))
    monkeypatch.delenv("ProgramFiles(x86)", raising=False)
    assert unreachable_posix_shell() is None
    assert "install a POSIX shell" in conftest._posix_shell_remedy()


# --- the anti-drift guard -----------------------------------------------------

# The original defect was not a missing feature, it was four inline copies of
# `shutil.which("sh")` with no owner: the skips were real, the count was nobody's.
# This is the guard that keeps that from growing back — a new shell-gated test
# added with its own inline probe would be invisible to the banner and the count,
# and the suite would quietly go back to hiding tests.
LEGACY_REASONS = ("needs a POSIX shell and git on PATH", "no POSIX shell on PATH")


def test_no_test_skips_on_a_hand_rolled_shell_probe():
    from conftest import ROOT

    offenders = []
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        if path.name == "test_env_gates.py":  # this module quotes them on purpose
            continue
        text = path.read_text(encoding="utf-8")
        for reason in LEGACY_REASONS:
            if reason in text:
                offenders.append("{}: {!r}".format(path.name, reason))
    assert not offenders, (
        "these skip through an inline probe instead of the declared gate, so "
        "their skips are uncounted and unexplained (WI-326) — use "
        "conftest.skip_without_env_gates / env_gate_skipif:\n  "
        + "\n  ".join(offenders)
    )
