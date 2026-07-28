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

import ast
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
# This is the guard that stops that growing back — and it is the SECOND version.
#
# The first scanned for two literal historical reason strings, and an adversarial
# review drove it: a brand-new inline probe with a reason it had never seen walked
# straight past, as did the fourteen `which("git")` probes that existed at the
# time. That is the 129-REVIEW-A shape — a guard advertising a property it lacks —
# so this one asserts the actual invariant instead, over the AST rather than the
# text: **a `shutil.which` result for a gated tool must never decide a skip.**
# Using `which` to LOCATE a tool after the gate has run is fine and common; what
# is banned is re-deciding, because a skip decided anywhere else is a skip the
# banner cannot predict and the summary cannot count.
GATED_TOOLS = frozenset({"sh", "bash", "git"})


def _which_calls_for_gated_tools(node):
    """Every `...which("sh"|"bash"|"git")` call inside `node`."""
    found = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name != "which" or not child.args:
            continue
        arg = child.args[0]
        if isinstance(arg, ast.Constant) and arg.value in GATED_TOOLS:
            found.append(child)
    return found


def _skip_calls(node):
    """Every `pytest.skip(...)` / bare `skip(...)` call inside `node`."""
    out = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name == "skip":
            out.append(child)
    return out


def _skipif_conditions(tree):
    """The condition expression of every `pytest.mark.skipif(...)` in the tree."""
    out = []
    for child in ast.walk(tree):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        if isinstance(func, ast.Attribute) and func.attr == "skipif" and child.args:
            out.append(child.args[0])
    return out


def _hand_rolled_gate_probes(path):
    """Findings for one test module: a gated-tool probe deciding a skip."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    findings = []

    for condition in _skipif_conditions(tree):
        for call in _which_calls_for_gated_tools(condition):
            findings.append(
                "{}:{} a skipif CONDITION probes {!r} directly".format(
                    path.name, call.lineno, call.args[0].value
                )
            )

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        probes = _which_calls_for_gated_tools(node)
        if probes and _skip_calls(node):
            findings.append(
                "{}:{} `{}` both probes {!r} and calls skip()".format(
                    path.name,
                    probes[0].lineno,
                    node.name,
                    probes[0].args[0].value,
                )
            )
    return findings


def test_no_test_decides_a_skip_from_its_own_tool_probe():
    from conftest import ROOT

    offenders = []
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        if path.name == "test_env_gates.py":  # this module IS the guard
            continue
        offenders.extend(_hand_rolled_gate_probes(path))
    assert not offenders, (
        "these decide a skip from their own tool probe instead of the declared "
        "gate, so their skips are uncounted and unexplained (WI-326) — use "
        "conftest.skip_without_env_gates / env_gate_skipif:\n  "
        + "\n  ".join(offenders)
    )


def test_the_guard_catches_a_freshly_invented_probe(tmp_path):
    """The mutation the first version of this guard FAILED. A reviewer wrote a
    new inline skip with a reason string this repo had never used, and the
    string-matching guard passed it. This one is driven against that exact shape
    plus its skipif twin, and against a legitimate post-gate `which` that must
    NOT be flagged — so it can fail in both directions."""
    bad_runtime = tmp_path / "test_bad_runtime.py"
    bad_runtime.write_text(
        "import shutil, pytest\n"
        "def test_x():\n"
        "    if not shutil.which('sh'):\n"
        "        pytest.skip('requires a POSIX shell')\n",
        encoding="utf-8",
    )
    bad_mark = tmp_path / "test_bad_mark.py"
    bad_mark.write_text(
        "import shutil, pytest\n"
        "pytestmark = pytest.mark.skipif(not shutil.which('git'), reason='anything')\n"
        "def test_x():\n    pass\n",
        encoding="utf-8",
    )
    ok = tmp_path / "test_ok.py"
    ok.write_text(
        "import shutil\n"
        "from conftest import skip_without_env_gates\n"
        "def test_x():\n"
        "    skip_without_env_gates('posix-shell')\n"
        "    assert shutil.which('sh')\n",
        encoding="utf-8",
    )
    assert _hand_rolled_gate_probes(bad_runtime), "runtime probe not caught"
    assert _hand_rolled_gate_probes(bad_mark), "skipif probe not caught"
    assert not _hand_rolled_gate_probes(ok), "post-gate which() must be allowed"


def test_the_guard_ignores_an_ungated_tool(tmp_path):
    """`which('pwsh')` is not a declared gate, so it is nobody's business here —
    otherwise the guard would grow into a ban on `shutil.which`."""
    other = tmp_path / "test_other.py"
    other.write_text(
        "import shutil, pytest\n"
        "def test_x():\n"
        "    if not shutil.which('pwsh'):\n"
        "        pytest.skip('no powershell')\n",
        encoding="utf-8",
    )
    assert not _hand_rolled_gate_probes(other)
