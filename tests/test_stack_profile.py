"""The declared product toolchain (Thread 30, process.md §7).

`docs/stack.ini` is the single home for the format/lint/test commands, the
src/tests paths, the tier expressions, and the coverage threshold. check.py
reads it; the pre-commit hook delegates its format step to it. The properties
pinned here are the thread's own acceptance tests: the scaffolded profile
behaves byte-identically to check.py's built-in defaults, `--list` reflects the
profile, a malformed profile fails loudly, tier expressions thread through to
the test step, and a profile naming a missing binary hits the run_step guard.
"""

import configparser
import importlib.util

import pytest
from conftest import KIT, load_script, make_minimal_project, run_py

check = load_script("check")


def _plan_sig(plan):
    """A comparable signature for a step plan: name, requires, argv, gates, layer."""
    return [(n, tuple(req), tuple(cmd), tuple(sorted(g)), lay) for n, req, cmd, g, lay in plan]


def _profile(text):
    cp = configparser.ConfigParser(interpolation=None)
    cp.read_string(text)
    return cp


# --- The reference profile == the built-in defaults ---------------------------


def test_scaffolded_profile_equals_the_template_bytes(scaffold):
    # bootstrap copies the profile verbatim (a non-.md file), so the repo's
    # docs/stack.ini is the reference template byte-for-byte.
    got = (scaffold / "docs" / "stack.ini").read_bytes()
    want = (KIT / "stack.ini.template").read_bytes()
    assert got == want


def test_reference_profile_matches_builtin_plan_every_tier():
    # The scaffolded stack.ini declares check.py's own built-in commands, so a
    # profile-driven plan and the built-in (profile=None) plan are identical for
    # every gate/tier — the "profile-absent behavior is byte-identical" contract.
    reference = _profile((KIT / "stack.ini.template").read_text(encoding="utf-8"))
    for tier in ("smoke", "full", "release", "all"):
        for gate in ("G1", "G3", "all"):
            builtin = check.steps(80, tier, gate)
            profiled = check.steps(80, tier, gate, None, reference)
            assert _plan_sig(builtin) == _plan_sig(profiled), (tier, gate)


def test_absent_profile_list_matches_reference_profile(scaffold):
    # End-to-end: deleting docs/stack.ini falls back to the built-ins, and the
    # printed plan is identical to the one the reference profile produces.
    with_profile = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    assert with_profile.returncode == 0, with_profile.stdout + with_profile.stderr
    (scaffold / "docs" / "stack.ini").unlink()
    without = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    assert without.returncode == 0, without.stdout + without.stderr
    assert without.stdout == with_profile.stdout


# --- --list reflects the profile ----------------------------------------------


def test_list_reflects_a_swapped_command(scaffold):
    ini = scaffold / "docs" / "stack.ini"
    ini.write_text(
        "[product]\nlint = npx eslint {src}\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The swapped lint command shows in the plan; the untouched format/test steps
    # fall back to the built-in ruff/pytest reference (partial profile merges).
    assert "npx eslint src" in proc.stdout
    assert any("format" in ln and "ruff format" in ln for ln in proc.stdout.splitlines())


def test_tier_expression_threads_through_to_the_test_step(scaffold):
    # A3: a non-pytest stack declares its tiers here. The [tiers] full expression
    # is appended to the test command verbatim.
    (scaffold / "docs" / "stack.ini").write_text(
        "[product]\ntest = npm test\n[tiers]\nfull = --run smoke-and-full\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check.py", "--gate", "G3", "--tier", "full", "--list"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    test_line = next(
        ln for ln in proc.stdout.splitlines() if "tests+coverage" in ln
    )
    assert "npm test" in test_line
    assert "--run smoke-and-full" in test_line


def test_coverage_threshold_comes_from_the_profile(scaffold):
    (scaffold / "docs" / "stack.ini").write_text(
        "[coverage]\nthreshold = 55\n"
        "args = --cov={src} --cov-fail-under={coverage}\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check.py", "--gate", "G3", "--tier", "full", "--list"], cwd=scaffold
    )
    assert "--cov-fail-under=55" in proc.stdout
    # An explicit --coverage on the CLI still wins over the profile threshold.
    proc = run_py(
        ["scripts/check.py", "--gate", "G3", "--tier", "full", "--coverage", "90",
         "--list"],
        cwd=scaffold,
    )
    assert "--cov-fail-under=90" in proc.stdout


# --- Failure modes ------------------------------------------------------------


def test_malformed_profile_fails_loudly(scaffold):
    # A malformed profile must never be silently ignored (that would drop the
    # format/lint/test gate). check.py exits nonzero naming the file.
    (scaffold / "docs" / "stack.ini").write_text(
        "this is not a section header\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert proc.returncode != 0
    assert "malformed" in (proc.stdout + proc.stderr)
    assert "stack.ini" in (proc.stdout + proc.stderr)


def test_non_integer_coverage_threshold_fails_loudly(scaffold):
    (scaffold / "docs" / "stack.ini").write_text(
        "[coverage]\nthreshold = eighty\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "full", "--list"],
                  cwd=scaffold)
    assert proc.returncode != 0
    assert "threshold" in (proc.stdout + proc.stderr)


def test_profile_missing_binary_hits_the_run_step_guard():
    # A non-Python profile naming a tool that isn't installed must be a designed
    # FAIL (Thread 29's guard), not a false green — the command flows from the
    # profile through steps() into run_step's PATH check.
    prof = _profile("[product]\nlint = no-such-tool-t30 {src}\n")
    plan = check.steps(80, "smoke", "all", None, prof)
    lint = next(s for s in plan if s[0] == "lint")
    assert lint[2][0] == "no-such-tool-t30"  # profile command threaded through
    assert lint[1] == ()  # non-`-m` command declares no import; PATH guard catches it
    status, detail = check.run_step(lint[0], lint[1], lint[2], lenient=False)
    assert status == "FAIL"
    assert "not found" in detail


# --- --run-step (the hook's format delegation) --------------------------------


def _ruff_available():
    return importlib.util.find_spec("ruff") is not None


def test_run_step_format_passes_clean_and_fails_unformatted(scaffold):
    if not _ruff_available():
        pytest.skip("ruff not importable by this interpreter")
    make_minimal_project(scaffold)
    ok = run_py(["scripts/check.py", "--run-step", "format"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # An unformatted source file must make the delegated step FAIL (exit 1) so
    # the hook blocks the commit.
    (scaffold / "src" / "bad.py").write_text("x=1\n", encoding="utf-8")
    bad = run_py(["scripts/check.py", "--run-step", "format"], cwd=scaffold)
    assert bad.returncode == 1, bad.stdout + bad.stderr
    assert "FAIL" in bad.stdout


def test_run_step_missing_tool_is_skip_not_block(scaffold):
    # The hook must not wedge a not-yet-set-up repo: a missing format tool is
    # SKIP (exit 0), so the commit proceeds. A real failure (above) still blocks.
    (scaffold / "docs" / "stack.ini").write_text(
        "[product]\nformat = no-such-formatter-t30 {src}\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--run-step", "format"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SKIP" in proc.stdout


def test_run_step_unknown_name_errors(scaffold):
    proc = run_py(["scripts/check.py", "--run-step", "no-such-step"], cwd=scaffold)
    assert proc.returncode != 0
    assert "no step named" in (proc.stdout + proc.stderr)
