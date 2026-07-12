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
import os
import subprocess
import sys

import pytest
from conftest import KIT, ROOT, SCRIPTS, load_script, make_minimal_project, run_py

check = load_script("check")


def _plan_sig(plan):
    """A comparable signature for a step plan: name, requires, argv, gates, layer."""
    return [
        (n, tuple(req), tuple(cmd), tuple(sorted(g)), lay)
        for n, req, cmd, g, lay in plan
    ]


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


def test_meta_repo_declares_parallel_test_command_but_template_opts_out():
    # WI-075: the meta-repo's OWN docs/stack.ini opts into pytest-xdist, so its
    # gate/CI test command parallelizes (`-n auto`); the shipped TEMPLATE keeps
    # the plain command with the opt-in COMMENTED (a downstream suite may not be
    # xdist-safe). Guards the wiring, the opt-in posture, and that `-n auto`
    # composes as two contiguous argv tokens through _expand (not a fused `-nauto`
    # from a quoting/split slip).
    meta = check.load_profile(ROOT / "docs" / "stack.ini")
    assert meta is not None, "meta repo docs/stack.ini is missing"
    meta_test = next(
        s[2]
        for s in check.steps(80, "all", "all", None, meta)
        if s[0] == "tests+coverage"
    )
    assert "-n" in meta_test and meta_test[meta_test.index("-n") + 1] == "auto", (
        meta_test
    )

    template = _profile((KIT / "stack.ini.template").read_text(encoding="utf-8"))
    tmpl_test = next(
        s[2]
        for s in check.steps(80, "all", "all", None, template)
        if s[0] == "tests+coverage"
    )
    assert "-n" not in tmpl_test, "template must keep the -n auto opt-in commented"


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
    assert any(
        "format" in ln and "ruff format" in ln for ln in proc.stdout.splitlines()
    )


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
    test_line = next(ln for ln in proc.stdout.splitlines() if "tests+coverage" in ln)
    assert "npm test" in test_line
    assert "--run smoke-and-full" in test_line


def test_coverage_threshold_comes_from_the_profile(scaffold):
    (scaffold / "docs" / "stack.ini").write_text(
        "[coverage]\nthreshold = 55\nargs = --cov={src} --cov-fail-under={coverage}\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check.py", "--gate", "G3", "--tier", "full", "--list"], cwd=scaffold
    )
    assert "--cov-fail-under=55" in proc.stdout
    # An explicit --coverage on the CLI still wins over the profile threshold.
    proc = run_py(
        [
            "scripts/check.py",
            "--gate",
            "G3",
            "--tier",
            "full",
            "--coverage",
            "90",
            "--list",
        ],
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
    proc = run_py(
        ["scripts/check.py", "--gate", "G3", "--tier", "full", "--list"], cwd=scaffold
    )
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


# --- [step:<name>] project-declared extra gate steps (WI-1.28) ----------------


def test_extra_step_joins_the_plan_with_derived_requires():
    # A domain gate declared in the profile appears in the plan as a product
    # step; its required-import set is auto-derived from the argv (a `{py} -m
    # <mod>` step declares <mod>; a bare executable declares nothing).
    prof = _profile(
        "[step:dup-code]\ncommand = {py} -m duplo {src}\ngates = G2 G3\n"
        "[step:license-lint]\ncommand = npx license-checker\n"
    )
    plan = check.steps(80, "all", "all", None, prof)
    dup = next(s for s in plan if s[0] == "dup-code")
    assert dup[1] == ("duplo",)  # `{py} -m duplo` declares the module
    assert dup[2][-1] == "src"  # {src} expanded
    assert sorted(dup[3]) == ["G2", "G3"]
    assert dup[4] == "product"
    lic = next(s for s in plan if s[0] == "license-lint")
    assert lic[1] == ()  # non-`-m` command declares no import (PATH guard covers it)
    assert sorted(lic[3]) == ["G3"]  # default gate


def test_extra_step_is_gate_scoped(scaffold):
    # A [step:] declared for G2/G3 must not run at G1, and must show at its gates.
    (scaffold / "docs" / "stack.ini").write_text(
        "[step:cap-integrity]\ncommand = {py} scripts/check_caps.py\ngates = G2,G3\n",
        encoding="utf-8",
    )
    at_g1 = run_py(["scripts/check.py", "--gate", "G1", "--list"], cwd=scaffold)
    assert "cap-integrity" not in at_g1.stdout, at_g1.stdout
    at_g2 = run_py(["scripts/check.py", "--gate", "G2", "--list"], cwd=scaffold)
    assert at_g2.returncode == 0, at_g2.stdout + at_g2.stderr
    line = next(ln for ln in at_g2.stdout.splitlines() if "cap-integrity" in ln)
    assert "[product]" in line and "check_caps.py" in line


def test_extra_step_runs_via_run_step(scaffold):
    # --run-step finds a project step by name (so the hook / CLI can drive one),
    # and it executes: a trivial command exits 0 -> PASS.
    (scaffold / "docs" / "stack.ini").write_text(
        '[step:hello]\ncommand = {py} -c "print(1)"\n', encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--run-step", "hello"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout and "hello" in proc.stdout


def test_every_builtin_step_name_is_guarded_against_shadowing(scaffold):
    # REVIEW_GRIND_FULL C1: the shadow guard must protect EVERY built-in step
    # name, not one hardcoded example — `okf` was a real step missing from
    # BUILTIN_STEP_NAMES, so a downstream [step:okf] silently duplicated. Iterate
    # the guard set AND the actual plan so the two can never drift apart again.
    check = load_script("check")
    plan_names = {s[0] for s in check.steps(80, "full", "all")}
    assert plan_names <= check.BUILTIN_STEP_NAMES, (
        "steps() emits names absent from BUILTIN_STEP_NAMES (shadow-guard hole): "
        + str(sorted(plan_names - check.BUILTIN_STEP_NAMES))
    )
    ini = scaffold / "docs" / "stack.ini"
    for name in sorted(check.BUILTIN_STEP_NAMES):
        ini.write_text(
            "[step:{}]\ncommand = {{py}} x.py\n".format(name), encoding="utf-8"
        )
        proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
        assert proc.returncode != 0, "[step:{}] must be rejected".format(name)
        assert "shadows a built-in step" in (proc.stdout + proc.stderr)


def test_stack_ini_command_preserves_windows_backslash_path(scaffold):
    # C2: a native Windows path in a stack.ini command value must survive the
    # split intact — a posix-escaping shlex.split would eat the backslashes to
    # `.venvScriptseslint`, so run_step's PATH probe would never resolve it.
    check = load_script("check")
    ini = scaffold / "docs" / "stack.ini"
    ini.write_text(
        "[product]\nlint = .venv\\Scripts\\eslint --fix {src}\n", encoding="utf-8"
    )
    profile = check.load_profile(ini)
    raw = check._pget(profile, "product", "lint", check.BUILTIN_PRODUCT["lint"])
    argv = check._expand(raw, {"src": "src", "py": "python"})
    assert argv[0] == ".venv\\Scripts\\eslint", argv


def test_extra_step_without_command_fails_loudly(scaffold):
    (scaffold / "docs" / "stack.ini").write_text(
        "[step:foo]\ngates = G3\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert proc.returncode != 0
    assert "needs a `command =` line" in (proc.stdout + proc.stderr)


def test_extra_step_bad_gate_and_layer_fail_loudly(scaffold):
    ini = scaffold / "docs" / "stack.ini"
    ini.write_text("[step:foo]\ncommand = {py} x.py\ngates = G9\n", encoding="utf-8")
    bad_gate = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert bad_gate.returncode != 0
    assert "gates" in (bad_gate.stdout + bad_gate.stderr) and "G9" in (
        bad_gate.stdout + bad_gate.stderr
    )
    ini.write_text("[step:foo]\ncommand = {py} x.py\nlayer = weird\n", encoding="utf-8")
    bad_layer = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert bad_layer.returncode != 0
    assert "layer" in (bad_layer.stdout + bad_layer.stderr)


def test_reference_profile_has_no_active_extra_step():
    # The shipped stack.ini's [step:] example is COMMENTED, so the reference
    # profile still equals the built-in plan (guards the byte-identity contract
    # above against a stray uncommented example line).
    reference = _profile((KIT / "stack.ini.template").read_text(encoding="utf-8"))
    assert (
        check.extra_steps(
            reference, {"py": "py", "src": "s", "tests": "t", "coverage": "80"}
        )
        == []
    )


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


def test_run_step_executes_the_resolved_path(scaffold):
    # WI-1.25 (downstream field report): run_step resolved cmd[0] with
    # shutil.which for the guard but executed the UNRESOLVED argv. On Windows,
    # CreateProcess applies no PATHEXT, so a bare `npx`-style .cmd shim passed
    # the guard and then crashed the exec with WinError 2 — the exact raw
    # FileNotFoundError the guard's comment claims to avoid. The step must run
    # the resolved path; this exercises the real path on Windows CI (a .cmd
    # shim) and stays a live regression guard on POSIX (a shell script).
    bindir = scaffold / "toolbin"
    bindir.mkdir()
    if os.name == "nt":
        (bindir / "fake-fmt-wi125.cmd").write_text(
            "@echo fake formatter ok\r\n@exit /b 0\r\n", encoding="utf-8"
        )
    else:
        tool = bindir / "fake-fmt-wi125"
        tool.write_text("#!/bin/sh\necho fake formatter ok\nexit 0\n", encoding="utf-8")
        tool.chmod(0o755)
    (scaffold / "docs" / "stack.ini").write_text(
        "[product]\nformat = fake-fmt-wi125\n", encoding="utf-8"
    )
    env = dict(os.environ)
    env["PATH"] = str(bindir) + os.pathsep + env.get("PATH", "")
    proc = subprocess.run(
        [sys.executable, "scripts/check.py", "--run-step", "format"],
        cwd=str(scaffold),
        capture_output=True,
        text=True,
        env=env,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout, proc.stdout


# --- [arch-map] mode: the stack-neutral fallback declared in the profile ------


def test_arch_map_mode_files_comes_from_the_profile(scaffold):
    # WI-1.25: a non-Python repo declares the file-level map in stack.ini
    # instead of hand-editing the take-wholesale check.py (the downstream
    # MODIFIED-FROM-KIT delta this absorbs).
    (scaffold / "docs" / "stack.ini").write_text(
        "[arch-map]\nmode = files\ncomment-prefixes = ;; --\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    arch_line = next(ln for ln in proc.stdout.splitlines() if "arch-map" in ln)
    assert "--mode files" in arch_line
    assert "--comment-prefix ;;" in arch_line
    # The default (or an explicit symbols) keeps the historical symbol-map plan.
    (scaffold / "docs" / "stack.ini").write_text(
        "[arch-map]\nmode = symbols\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    arch_line = next(ln for ln in proc.stdout.splitlines() if "arch-map" in ln)
    assert "--mode" not in arch_line


def test_arch_map_invalid_mode_fails_loudly(scaffold):
    (scaffold / "docs" / "stack.ini").write_text(
        "[arch-map]\nmode = banana\n", encoding="utf-8"
    )
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert proc.returncode != 0
    assert "arch-map" in (proc.stdout + proc.stderr)
    assert "banana" in (proc.stdout + proc.stderr)


def test_non_python_stack_seeds_files_mode_and_starts_fresh(tmp_path):
    # bootstrap --stack node seeds [arch-map] mode = files in the scaffolded
    # profile AND initializes architecture.md in that same mode, so the fresh
    # non-Python repo's freshness gate is real (not vacuous) and green on
    # day one — generator and checker must agree on the mode.
    dest = tmp_path / "repo"
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", dest, "--stack", "node"], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    ini = (dest / "docs" / "stack.ini").read_text(encoding="utf-8")
    assert "mode = files" in ini
    assert "mode = symbols" not in ini
    arch = (dest / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "--mode files" in arch  # the generated block's byline names the mode
    chk = run_py(["scripts/check.py", "--run-step", "arch-map"], cwd=dest)
    assert chk.returncode == 0, chk.stdout + chk.stderr
    assert "PASS" in chk.stdout
