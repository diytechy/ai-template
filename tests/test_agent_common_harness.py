"""agent_common's harness plumbing — the shared resolvers the bar runs on.

Relocated at concurrency-restructure Phase 5 from the retired dispatcher test
modules (test_agent_dispatch_decisions.py, test_agent_loop_integrate.py): these
tests cover agent_common.py functions that survive the train-machinery
deletion — `_failure_tail`, `venv_python`, `harness_python`,
`interpreter_version`, `_declared_test_command` — and lived in dispatcher
modules only because the dispatcher was their first consumer.
"""

import os
import sys

from conftest import load_script

agent_common = load_script("agent_common")
_failure_tail = agent_common._failure_tail


# --- WI-240: park/quarantine details carry the FAILING step, not the head -------

# The exact WI-229 field string: a commit-hook `check.py --run-steps` output
# whose FIRST banner is a PASSING `=== derived-gate : <long python.exe cmd> ===`
# and whose real failure is a later `trajectory` step. The old `out[:200]` head
# cut kept the derived-gate banner and dropped the error; the helper must invert
# that.
WI229_HOOK_OUT = (
    "\n=== arch-map : python check.py --run-step arch-map ===\n"
    "  PASS  arch-map         0.2s\n"
    "\n=== derived-gate : C:/Users/x/.venv/Scripts/python.exe derive_gate.py "
    "--check --root . ===\n"
    "  PASS  derived-gate     0.1s\n"
    "\n=== trajectory : C:/Users/x/.venv/Scripts/python.exe check_trajectory.py "
    "--root . ===\n"
    "check_trajectory: ERROR - blocked-ref WI-229: status=blocked but BlockRef "
    "is empty\n"
    "  FAIL  trajectory       exit 1 (0.3s)\n"
)


def test_failure_tail_extracts_failing_step_not_first_banner():
    tail = _failure_tail(WI229_HOOK_OUT)
    # Names the failing step and its error line ...
    assert "  FAIL  trajectory" in tail
    assert "blocked-ref WI-229: status=blocked but BlockRef is empty" in tail
    # ... and DROPS the earlier passing banner that the [:200] head kept.
    assert "derived-gate" not in tail
    assert "arch-map" not in tail
    assert len(tail) <= 600


def test_failure_tail_single_line_passes_through():
    line = "fatal: nothing to commit, working tree clean"
    assert _failure_tail(line) == line


def test_failure_tail_no_fail_marker_is_bounded_tail_not_head():
    body = "FIRSTLINE\n" + "\n".join("row %d" % i for i in range(300))
    tail = _failure_tail(body, budget=40)
    assert "FIRSTLINE" not in tail  # never the head
    assert "row 299" in tail  # the tail survives
    assert len(tail) <= 40
    # Empty / None degrade to "", never crash a journal call.
    assert _failure_tail("") == ""
    assert _failure_tail(None) == ""


# --- the interpreter resolvers (WI-285/WI-286's surviving halves) ---------------


def _stub_venv(tmp_path):
    """A .venv layout whose interpreter is a text file (resolvable, not
    runnable)."""
    if os.name == "nt":
        d = tmp_path / ".venv" / "Scripts"
        exe = d / "python.exe"
    else:
        d = tmp_path / ".venv" / "bin"
        exe = d / "python"
    d.mkdir(parents=True)
    exe.write_text("stub interpreter\n", encoding="utf-8")
    return exe


def test_venv_python_finds_native_layout_else_none(tmp_path):
    assert agent_common.venv_python(tmp_path) is None  # no .venv
    exe = _stub_venv(tmp_path)
    assert agent_common.venv_python(tmp_path) == exe


def test_harness_python_prefers_venv_else_sys_executable(tmp_path):
    # No .venv -> this process's own interpreter is the DEFENSIVE fallback.
    # (The dispatcher-era fail-closed floor gate that refused a venv-less root
    # up front retired with the dispatcher at concurrency-restructure Phase 5;
    # the resolver's own contract — prefer the pinned .venv, degrade to the
    # running interpreter — stands on its own.)
    assert agent_common.harness_python(tmp_path) == sys.executable
    exe = _stub_venv(tmp_path)
    assert agent_common.harness_python(tmp_path) == str(exe)


def test_interpreter_version_reads_self_and_fails_soft_on_a_broken_exe(tmp_path):
    # None and this process's own executable short-circuit to sys.version_info
    # (no subprocess); a garbage/non-runnable path returns None, not a crash.
    assert agent_common.interpreter_version(None) == sys.version_info[:2]
    assert agent_common.interpreter_version(sys.executable) == sys.version_info[:2]
    garbage = _stub_venv(tmp_path)  # a text file named python(.exe) cannot run
    assert agent_common.interpreter_version(garbage) is None


# --- the declared-bar resolver (WI-285) -----------------------------------------


def test_declared_test_command_substitutes_the_given_py(tmp_path):
    ini = tmp_path / "stack.ini"
    ini.write_text("[product]\ntest = {py} -m pytest\n", encoding="utf-8")
    assert agent_common._declared_test_command(ini, "/opt/venv/python") == [
        "/opt/venv/python",
        "-m",
        "pytest",
    ]
    # Default (no py) stays this interpreter — the WI-285 contract is unchanged.
    assert agent_common._declared_test_command(ini)[0] == sys.executable


def test_declared_test_command_resolution(tmp_path):
    # The shared resolver directly: [product] expands {py}/{src}/{tests} exactly
    # as check.py fills them; [stack] is tokenized RAW (quotes group as one
    # token); NEITHER key -> None (stackless) while a present-but-EMPTY command
    # -> [] (declared) so the caller fail-closes rather than skipping.
    ini = tmp_path / "stack.ini"
    ini.write_text(
        "[paths]\nsrc = lib\ntests = t\n[product]\ntest = {py} -m pytest {src} {tests}\n",
        encoding="utf-8",
    )
    assert agent_common._declared_test_command(ini) == [
        sys.executable,
        "-m",
        "pytest",
        "lib",
        "t",
    ]
    ini.write_text('[stack]\ntest = mytool --run "a b"\n', encoding="utf-8")
    assert agent_common._declared_test_command(ini) == ["mytool", "--run", "a b"]
    ini.write_text("[paths]\nsrc = s\n", encoding="utf-8")
    assert agent_common._declared_test_command(ini) is None
    ini.write_text("[product]\ntest =\n", encoding="utf-8")
    assert agent_common._declared_test_command(ini) == []
