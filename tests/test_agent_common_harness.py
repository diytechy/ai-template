"""agent_common's harness plumbing — the shared resolvers the bar runs on.

Relocated at concurrency-restructure Phase 5 from the retired dispatcher test
modules (test_agent_dispatch_decisions.py, test_agent_loop_integrate.py): these
tests cover agent_common.py functions that survive the train-machinery
deletion — `_failure_tail`, `venv_python`, `harness_python`,
`interpreter_version`, `_declared_test_command` — and lived in dispatcher
modules only because the dispatcher was their first consumer.

WI-361 added `harness_floor_failures` to that list: the WI-286 fail-closed floor,
re-homed here as a public agent_common helper with an arming boundary, refused at
integrate.py's bar seam (see tests/test_integrate.py for the wired half).
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


# --- WI-398: the refusal carries the failing STEP's output, never the summary ---

# A full `check.py --jobs 0` red, the `_run_bar` shape: each step's captured
# output prints under the lane lock with its own inline status line, and then
# the closing summary block RE-prints every step's status after a `====` rule.
# The WI-240 anchor (LAST `  FAIL` line) always landed in that summary copy, so
# the window walked back to the LAST step's banner and the refusal carried
# summary rows instead of the failing step's own output — the WI-387 refresh
# red cost three lost diagnoses of one failure exactly this way.
WI398_JOBS_BAR_OUT = (
    "\n=== format : python -m ruff format --check . ===\n"
    "74 files already formatted\n"
    "  PASS  format           0.4s\n"
    "\n=== tests+coverage : .venv/bin/python -m pytest -q -m smoke ===\n"
    "..F..F.\n"
    "=========================== short test summary info ===========================\n"
    "FAILED tests/test_refresh.py::test_the_lost_diagnosis - AssertionError: gone\n"
    "FAILED tests/test_refresh.py::test_the_other_red - AssertionError\n"
    "2 failed, 5 passed in 3.2s\n"
    "  FAIL  tests+coverage   exit 1 (3.4s)\n"
    "\n=== trajectory : python check_trajectory.py --root . ===\n"
    "check_trajectory: OK (58 rows)\n"
    "  PASS  trajectory       0.3s\n"
    "\n" + "=" * 56 + "\n"
    "Check summary (gate DevBar-Release, tier smoke):\n"
    "  PASS  format           0.4s\n"
    "  FAIL  tests+coverage   exit 1 (3.4s)\n"
    "  PASS  trajectory       0.3s\n" + "=" * 56 + "\n"
    "RESULT: FAIL (1 step(s) failed)\n"
)


def test_failure_tail_extracts_the_failing_steps_own_output_not_the_summary():
    tail = _failure_tail(WI398_JOBS_BAR_OUT)
    # The step's OWN output — the failing test names a re-run had to recover.
    assert "FAILED tests/test_refresh.py::test_the_lost_diagnosis" in tail
    assert "FAILED tests/test_refresh.py::test_the_other_red" in tail
    # ... still names the failing step and its exit ...
    assert "  FAIL  tests+coverage" in tail
    # ... and NEVER the summary re-print or a later passing step's window.
    assert "Check summary" not in tail
    assert "RESULT: FAIL" not in tail
    assert "check_trajectory: OK" not in tail


# The same red at `--jobs 1`: step output STREAMS with no inline status line, so
# the only `  FAIL` markers in the whole output are the summary rows. The window
# must still be the failing step's own banner-to-end block (found by the NAME the
# summary row carries), with that row appended so the refusal names the step.
WI398_SEQ_BAR_OUT = (
    "\n=== format : python -m ruff format --check . ===\n"
    "74 files already formatted\n"
    "\n=== tests+coverage : .venv/bin/python -m pytest -q -m smoke ===\n"
    "..F.\n"
    "FAILED tests/test_refresh.py::test_the_lost_diagnosis - AssertionError: gone\n"
    "1 failed, 3 passed in 2.1s\n"
    "\n=== trajectory : python check_trajectory.py --root . ===\n"
    "check_trajectory: OK (58 rows)\n"
    "\n" + "=" * 56 + "\n"
    "Check summary (gate DevBar-Release, tier smoke):\n"
    "  PASS  format           0.4s\n"
    "  FAIL  tests+coverage   exit 1 (2.3s)\n"
    "  PASS  trajectory       0.3s\n" + "=" * 56 + "\n"
    "RESULT: FAIL (1 step(s) failed)\n"
)


def test_failure_tail_reaches_the_step_output_when_statuses_only_print_in_summary():
    tail = _failure_tail(WI398_SEQ_BAR_OUT)
    assert "FAILED tests/test_refresh.py::test_the_lost_diagnosis" in tail
    assert "  FAIL  tests+coverage" in tail  # the anchoring row rides along
    assert "Check summary" not in tail
    assert "check_trajectory: OK" not in tail


# --- WI-405: KNOWN LIMIT — bar-shaped text EMBEDDED in a step's own output ------

# WI-398 REVIEW-A finding 1's three constructed shapes, pinned AS THE KNOWN
# LIMIT, not as designed behavior: both anchors trust line SHAPE, so bar-shaped
# text embedded in a step's own captured output silently misanchors the window
# onto a passing step's text. The remedy stays inside WI-398's scope guard (no
# parsing machinery): the limit is documented in `_own_step_window`'s docstring
# and, on the refresh path, the kept full log
# (out/run-logs/refresh-refused-<branch>.log) is the authority. The
# outermost-banner preference was JUDGED AND DECLINED: knowing which banner is
# outermost means knowing which lines sit inside another step's section — a
# structural parser — and a first-to-last-match swap merely mirrors the hole
# (it would break the symmetric shape, a failing step whose banner a LATER
# passing step quotes, that first-match handles). These tests pin the current
# wrong-window outcomes so the choice stays explicit; if one reds, the anchor
# changed and the docstring's limit clause is stale.

# Shape 1: a PASSING tests+coverage step's output quotes an old
# `  FAIL  tests+coverage` log row at line start (a pasted log in test output);
# the real red is lint (F401). The quoted row is the FIRST FAIL line, so the
# window is the passing step's own banner section.
WI405_QUOTED_FAIL_ROW_BAR = (
    "\n=== tests+coverage : .venv/bin/python -m pytest -q -m smoke ===\n"
    "all good\n"
    "  FAIL  tests+coverage   exit 1 (3.4s)\n"
    "4 passed in 1.0s\n"
    "  PASS  tests+coverage   1.1s\n"
    "\n=== lint : python -m ruff check . ===\n"
    "scripts/x.py:3:8: F401 `os` imported but unused\n"
    "  FAIL  lint             exit 1 (0.5s)\n"
    "\n" + "=" * 56 + "\n"
    "Check summary (gate DevBar-Release, tier smoke):\n"
    "  PASS  tests+coverage   1.1s\n"
    "  FAIL  lint             exit 1 (0.5s)\n" + "=" * 56 + "\n"
    "RESULT: FAIL (1 step(s) failed)\n"
)


def test_known_limit_a_quoted_fail_row_hijacks_the_window_onto_a_passing_step():
    tail = _failure_tail(WI405_QUOTED_FAIL_ROW_BAR)
    # PINNED LIMIT: the window is the passing quoter's section ...
    assert "all good" in tail
    assert "  PASS  tests+coverage" in tail
    # ... with zero bytes of the real red.
    assert "F401" not in tail
    assert "  FAIL  lint" not in tail


# Shape 2: a passing format step quotes a MOCK banner for the step that later
# genuinely fails. The FIRST `=== tests+coverage : ` match is the quoted line,
# so the window carries the quoting step's text; only the appended anchoring
# FAIL row names the right step.
WI405_QUOTED_MOCK_BANNER_BAR = (
    "\n=== format : python -m ruff format --check . ===\n"
    "=== tests+coverage : stub pytest -q ===\n"
    "fixture tail\n"
    "  PASS  format           0.4s\n"
    "\n=== tests+coverage : .venv/bin/python -m pytest -q -m smoke ===\n"
    "FAILED tests/test_x.py::test_y - AssertionError: REAL ERROR\n"
    "1 failed, 3 passed in 1.0s\n"
    "  FAIL  tests+coverage   exit 1 (1.2s)\n"
    "\n" + "=" * 56 + "\n"
    "Check summary (gate DevBar-Release, tier smoke):\n"
    "  PASS  format           0.4s\n"
    "  FAIL  tests+coverage   exit 1 (1.2s)\n" + "=" * 56 + "\n"
    "RESULT: FAIL (1 step(s) failed)\n"
)


def test_known_limit_a_quoted_mock_banner_carries_the_quoting_steps_text():
    tail = _failure_tail(WI405_QUOTED_MOCK_BANNER_BAR)
    # PINNED LIMIT: anchored on the quoted mock banner, quoter's text carried ...
    assert "=== tests+coverage : stub pytest -q ===" in tail
    assert "fixture tail" in tail
    # ... the real error line never reached ...
    assert "REAL ERROR" not in tail
    # ... though the appended anchoring row still names the failing step.
    assert "  FAIL  tests+coverage" in tail


# Shape 3 (the realistic one for THIS repo): a RED tests+coverage whose pytest
# output embeds a nested scaffold bar (captured stdout of a failing
# integrate/check test — the STUB_CHECK_RED shape) whose FAIL row names a
# DIFFERENT step. The nested `  FAIL  format` is the FIRST FAIL line, so the
# window becomes the passing format step's own output — an actively wrong
# attribution, silent. (When the nested row names the SAME step as the outer
# red — the common stub shape — the window is correct; REVIEW-A drove that.)
WI405_NESTED_BAR_OTHER_STEP = (
    "\n=== format : python -m ruff format --check . ===\n"
    "146 files already formatted\n"
    "  PASS  format           0.2s\n"
    "\n=== tests+coverage : .venv/bin/python -m pytest -q -m smoke ===\n"
    "..F\n"
    "=== format : stub ruff format --check ===\n"
    "  FAIL  format           exit 1 (0.1s)\n"
    "FAILED tests/test_integrate.py::test_red_bar - AssertionError: OUTER REAL\n"
    "1 failed, 2 passed in 0.9s\n"
    "  FAIL  tests+coverage   exit 1 (1.0s)\n"
    "\n" + "=" * 56 + "\n"
    "Check summary (gate DevBar-Release, tier smoke):\n"
    "  PASS  format           0.2s\n"
    "  FAIL  tests+coverage   exit 1 (1.0s)\n" + "=" * 56 + "\n"
    "RESULT: FAIL (1 step(s) failed)\n"
)


def test_known_limit_a_nested_bar_naming_another_step_misattributes_the_window():
    tail = _failure_tail(WI405_NESTED_BAR_OTHER_STEP)
    # PINNED LIMIT: the passing format step's output plus the nested FAIL row ...
    assert "146 files already formatted" in tail
    assert "  FAIL  format" in tail
    # ... and the truly failing step is never named, its error never carried.
    assert "OUTER REAL" not in tail
    assert "tests+coverage" not in tail


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
    # No .venv -> this process's own interpreter is the DEFENSIVE fallback. The
    # resolver's contract — prefer the pinned .venv, degrade to the running
    # interpreter — stands on its own; tmp_path declares no pinned toolchain, so
    # the WI-361 floor below is unarmed here and the fallback is the real answer.
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


# --- the harness floor (WI-286, re-homed by WI-361) -----------------------------

# Ported from the deleted dispatcher module (test_agent_dispatch_decisions.py @
# 31ad569^) onto the public `agent_common.harness_floor_failures`, plus the two
# tests for the arming boundary WI-361 added: the floor guards only a repo that
# DECLARES the pinned toolchain (requirements-dev.txt at its root), so the
# venv-less fixtures the rest of this fleet builds keep today's ambient fallback.


def _declare_toolchain(tmp_path):
    """Arm the floor: the pinned-toolchain declaration this repo shape opts in
    with."""
    (tmp_path / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")


def test_harness_floor_clears_with_a_floor_satisfying_venv(tmp_path, monkeypatch):
    # A root whose OWN .venv interpreter reports >= the floor clears the guard.
    _declare_toolchain(tmp_path)
    monkeypatch.setattr(agent_common, "venv_python", lambda root: tmp_path / "py")
    monkeypatch.setattr(
        agent_common, "interpreter_version", lambda exe: agent_common.MIN_PYTHON
    )
    assert agent_common.harness_floor_failures(tmp_path) == []


def test_harness_floor_refuses_a_below_floor_venv(tmp_path, monkeypatch):
    _declare_toolchain(tmp_path)
    monkeypatch.setattr(agent_common, "venv_python", lambda root: tmp_path / "py")
    monkeypatch.setattr(agent_common, "interpreter_version", lambda exe: (3, 8))
    fails = agent_common.harness_floor_failures(tmp_path)
    assert len(fails) == 1
    assert ".venv is Python 3.8" in fails[0] and "below the 3.11 floor" in fails[0]


def test_harness_floor_refuses_a_missing_venv(tmp_path, monkeypatch):
    # REVIEW-A MAJOR: a missing (or incomplete-layout) root .venv fails CLOSED —
    # the harness must not fall back to the ambient interpreter, whose pinned dev
    # tools may be absent even at a satisfying version (a false green).
    _declare_toolchain(tmp_path)
    monkeypatch.setattr(agent_common, "venv_python", lambda root: None)
    fails = agent_common.harness_floor_failures(tmp_path)
    assert len(fails) == 1
    assert "no runnable ./.venv" in fails[0] and "false green" in fails[0]
    # The message points at the surviving remedy, not the retired dispatcher.
    assert "dev-setup --install" in fails[0]


def test_harness_floor_refuses_no_venv_even_when_ambient_is_at_floor(tmp_path):
    # The exact hole REVIEW-A named: NO ./.venv but the ambient interpreter (this
    # very test process) is >= the floor. It must FAIL closed and never consult the
    # ambient version. No monkeypatch — the REAL resolver sees no .venv under
    # tmp_path and refuses before ambient is read.
    _declare_toolchain(tmp_path)
    fails = agent_common.harness_floor_failures(tmp_path)
    assert len(fails) == 1 and "no runnable ./.venv" in fails[0]


def test_harness_floor_fails_closed_on_an_unrunnable_venv(tmp_path, monkeypatch):
    # A .venv present but its interpreter cannot report a version -> fail closed
    # (never treat an unverifiable interpreter as floor-satisfying). Built from the
    # real layout: `_stub_venv` writes a text file named python(.exe), which
    # resolves but cannot run.
    _declare_toolchain(tmp_path)
    _stub_venv(tmp_path)
    fails = agent_common.harness_floor_failures(tmp_path)
    assert len(fails) == 1 and "could not be run" in fails[0]


def test_the_floor_is_unarmed_without_the_pinned_toolchain_declaration(
    tmp_path, monkeypatch
):
    # The boundary, negative side: no requirements-dev.txt -> no refusal, whatever
    # the .venv looks like. The declaration is checked FIRST, so an absent venv and
    # even a below-floor one are both silent here — such a repo keeps
    # `harness_python`'s ambient fallback, which is its whole contract.
    assert agent_common.harness_floor_failures(tmp_path) == []
    monkeypatch.setattr(agent_common, "venv_python", lambda root: tmp_path / "py")
    monkeypatch.setattr(agent_common, "interpreter_version", lambda exe: (3, 8))
    assert agent_common.harness_floor_failures(tmp_path) == []


def test_the_declaration_alone_arms_the_floor_on_the_same_root(tmp_path):
    # The boundary, positive side: the SAME venv-less root flips from silent to
    # refusing the moment the declaration lands. Nothing else about the root
    # changes, so the declaration is provably the arming input.
    assert agent_common.harness_floor_failures(tmp_path) == []
    _declare_toolchain(tmp_path)
    assert len(agent_common.harness_floor_failures(tmp_path)) == 1


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
