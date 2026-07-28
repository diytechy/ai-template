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


def _any_which_call(node):
    """Every `...which(x)` call inside `node`, whatever the argument.

    Deliberately not restricted to a constant gated tool: 130-REVIEW-A's bypass
    passed the tool name through a VARIABLE, so a rule keyed on the literal
    cannot see it."""
    out = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name == "which":
            out.append(child)
    return out


def _imports_the_declared_gate(tree):
    """Whether the module imports the declared-gate helpers at all."""
    wanted = {"skip_without_env_gates", "env_gate_skipif"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if wanted & {a.name for a in node.names}:
                return True
    return False


def _hand_rolled_gate_probes(path):
    """Findings for one test module: a tool probe that could decide a skip.

    THREE rules, widening outward, because 130-REVIEW-A drove the first two:

    1. a `skipif` CONDITION that probes a gated tool directly;
    2. one FUNCTION that both probes a gated tool and calls `skip()`;
    3. a MODULE that probes with `which` at all AND skips at all, while importing
       neither declared-gate helper.

    Rule 3 is what the reviewer's bypass needed: it split the probe and the skip
    across two module-level helpers and passed the tool through a variable, so
    neither of the first two could see it. A module that genuinely probes a
    NON-gated tool (`pwsh`) and skips is exempted by importing the helpers, which
    every such module here already does — the exemption is cheap and explicit,
    which is the point: the guard now asks a module to declare that it has
    thought about this, rather than trying to infer it.

    **What this still cannot see, recorded rather than papered over**
    (`docs/enforcement-audit.md`, Reviewer tier): a probe in module A deciding a
    skip in module B; a probe that shells out (`subprocess.run(["git", ...])`)
    instead of using `which`; and a skip conditioned on a probe's result stored in
    a module constant at import time. Those are semantic, not structural, and a
    guard that claimed them would be advertising a property it does not hold —
    which is the exact defect this rule replaced."""
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

    probes = _any_which_call(tree)
    if probes and _skip_calls(tree) and not _imports_the_declared_gate(tree):
        findings.append(
            "{}:{} the module probes with which() and skips, but imports neither "
            "`skip_without_env_gates` nor `env_gate_skipif` — split across "
            "helpers, that is an uncounted gated skip".format(
                path.name, probes[0].lineno
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


def test_an_ungated_tool_is_not_a_NAMED_finding(tmp_path):
    """`which('pwsh')` is not a declared gate, so neither of the two NAMED rules
    fires on it — the guard must not grow into "any `which` is a defect".

    Rule 3 does ask such a module to import the declared helpers, and that is
    deliberate: after 130-REVIEW-A it is the only structural way to tell a
    legitimate ungated probe from a gated one smuggled through a variable. The
    cost is one import; the alternative was a guard that could be bypassed."""
    other = tmp_path / "test_other.py"
    body = (
        "import shutil, pytest\n"
        "{}"
        "def test_x():\n"
        "    if not shutil.which('pwsh'):\n"
        "        pytest.skip('no powershell')\n"
    )
    other.write_text(body.format(""), encoding="utf-8")
    findings = _hand_rolled_gate_probes(other)
    assert findings and "imports neither" in findings[0], findings
    assert not any("probes 'pwsh'" in f for f in findings), (
        "an ungated tool must never be named as a gated-probe finding"
    )

    other.write_text(
        body.format("from conftest import skip_without_env_gates  # noqa: F401\n"),
        encoding="utf-8",
    )
    assert _hand_rolled_gate_probes(other) == []


def test_the_guard_catches_the_helper_indirection_bypass(tmp_path):
    """130-REVIEW-A BLOCKER 2, reproduced exactly.

    The reviewer split the probe and the skip across two module-level helpers and
    passed the tool name through a VARIABLE, so neither the skipif rule nor the
    same-function rule could see it, and the shipped guard reported nothing. The
    module rule catches it; the exempt twin proves the exemption is what makes
    the difference, not something incidental about the file."""
    bypass = tmp_path / "test_bypass.py"
    bypass.write_text(
        "import shutil, pytest\n"
        "def _probe(tool):\n"
        "    return shutil.which(tool)\n"
        "def _need(tool):\n"
        "    if not _probe(tool):\n"
        "        pytest.skip('requires ' + tool)\n"
        "def test_x():\n"
        "    _need('git')\n"
        "    assert True\n",
        encoding="utf-8",
    )
    findings = _hand_rolled_gate_probes(bypass)
    assert findings, "the reviewer's bypass still walks past the guard"
    assert "imports neither" in findings[0], findings

    exempt = tmp_path / "test_exempt.py"
    exempt.write_text(
        "import shutil, pytest\n"
        "from conftest import skip_without_env_gates\n"
        "def _pwsh():\n"
        "    return shutil.which('pwsh')\n"
        "def test_x():\n"
        "    skip_without_env_gates('posix-shell')\n"
        "    if not _pwsh():\n"
        "        pytest.skip('no powershell')\n",
        encoding="utf-8",
    )
    assert _hand_rolled_gate_probes(exempt) == [], (
        "a module that DECLARES the gate must stay exempt, or every legitimate "
        "probe of an ungated tool becomes a finding"
    )


def test_the_guards_residue_is_recorded_not_claimed():
    """What the AST cannot see is written down where the enforcement tiers live,
    rather than left implied by a guard that would otherwise advertise a property
    it does not hold — the defect this rule replaced."""
    from conftest import ROOT

    audit = (ROOT / "docs" / "enforcement-audit.md").read_text(encoding="utf-8")
    assert "WI-326" in audit and "cross-module" in audit, (
        "the Reviewer-tier residue of the environment-gate rule is not recorded "
        "in docs/enforcement-audit.md"
    )
