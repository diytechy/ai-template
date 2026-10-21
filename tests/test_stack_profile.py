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
import functools
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
    # The one declared difference is the readability report's step (SR-216),
    # which is a `[step:]` by design and so exists only where it is declared;
    # the test below pins that it is the ONLY one.
    reference = _profile((KIT / "stack.ini.template").read_text(encoding="utf-8"))
    for tier in ("smoke", "full", "release", "all"):
        for gate in ("DevStg-Reqs", "DevStg-Impl", "all"):
            builtin = check.steps(80, tier, gate)
            profiled = check.steps(80, tier, gate, None, reference)
            profiled = [s for s in profiled if s[0] != "readability"]
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
    # printed plan is identical to the one the reference profile produces —
    # but for the declared readability step (SR-216), which exists only where
    # the profile declares it.
    with_profile = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    assert with_profile.returncode == 0, with_profile.stdout + with_profile.stderr
    (scaffold / "docs" / "stack.ini").unlink()
    without = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    assert without.returncode == 0, without.stdout + without.stderr
    declared = [
        line
        for line in with_profile.stdout.splitlines()
        if not line.startswith("  - readability ")
    ]
    assert len(declared) == len(with_profile.stdout.splitlines()) - 1
    assert without.stdout.splitlines() == declared


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
        ["scripts/check.py", "--gate", "DevStg-Impl", "--tier", "full", "--list"],
        cwd=scaffold,
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
        ["scripts/check.py", "--gate", "DevStg-Impl", "--tier", "full", "--list"],
        cwd=scaffold,
    )
    assert "--cov-fail-under=55" in proc.stdout
    # An explicit --coverage on the CLI still wins over the profile threshold.
    proc = run_py(
        [
            "scripts/check.py",
            "--gate",
            "DevStg-Impl",
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
        ["scripts/check.py", "--gate", "DevStg-Impl", "--tier", "full", "--list"],
        cwd=scaffold,
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
        "[step:dup-code]\ncommand = {py} -m duplo {src}\nfrom-stage = DevStg-Arch\n"
        "[step:license-lint]\ncommand = npx license-checker\n"
    )
    plan = check.steps(80, "all", "all", None, prof)
    dup = next(s for s in plan if s[0] == "dup-code")
    assert dup[1] == ("duplo",)  # `{py} -m duplo` declares the module
    assert dup[2][-1] == "src"  # {src} expanded
    # ONE RUNG, not a set of bars (WI-498 slice 2): the declared value is the
    # rung the step becomes relevant at, and selection is AT OR ABOVE it — which
    # is asserted as behaviour here rather than as a sorted list, because the
    # ordering that list existed to pin now lives in `at_or_above`.
    assert dup[3] == "DevStg-Arch"
    assert check.at_or_above("DevStg-Tests", dup[3])
    assert not check.at_or_above("DevStg-Reqs", dup[3])
    assert dup[4] == "product"
    lic = next(s for s in plan if s[0] == "license-lint")
    assert lic[1] == ()  # non-`-m` command declares no import (PATH guard covers it)
    assert lic[3] == "DevStg-Impl"  # the default rung


def test_a_retired_gates_value_in_stack_ini_TRANSLATES():
    """TWO retirements, one reader, applied in order.

    `gates =` is a value the ADOPTER authors, so the retired `G1|G2|G3` tags  # check_vocab: allow
    still translate on read (OI-21 break 2). Since WI-498 slice 2 the `gates =`
    MEMBERSHIP LIST is itself retired in favour of a single `from-stage` rung, so
    the translated list is then folded to the rung it effectively meant. An
    adopter's stack.ini from either era keeps working until their re-sync.

    THE FOLD IS NOT THE SPAN FLOOR, which is the part worth pinning: the
    DevStg-Tests BAR was a MIN over every row and so was reached only by a fully
    decomposed spine — the DevStg-Impl RUNG — while the DevStg-Reqs bar is the
    floor every repo already sits at, so it folds to DevStg-Needs and the step
    keeps running always."""
    prof = _profile(
        "[step:dup-code]\ncommand = {py} -m duplo {src}\ngates = G2 G3\n"  # check_vocab: allow
        "[step:legacy-mixed]\ncommand = npx thing\ngates = G1, DevStg-Impl\n"  # check_vocab: allow
    )
    check._LEGACY_GATES_WARNED.clear()
    plan = check.steps(80, "all", "all", None, prof)
    dup = next(s for s in plan if s[0] == "dup-code")
    assert dup[3] == "DevStg-Impl"
    mixed = next(s for s in plan if s[0] == "legacy-mixed")
    assert mixed[3] == "DevStg-Needs"


def test_extra_step_is_stage_scoped(scaffold):
    # A [step:] declared from DevStg-Arch on must not run below that rung, and
    # must show at EVERY rung at or above it — the at-or-above half is what a
    # membership set could not express.
    (scaffold / "docs" / "stack.ini").write_text(
        "[step:cap-integrity]\ncommand = {py} scripts/check_caps.py\n"
        "from-stage = DevStg-Arch\n",
        encoding="utf-8",
    )
    below = run_py(
        ["scripts/check.py", "--stage", "DevStg-Reqs", "--list"], cwd=scaffold
    )
    assert "cap-integrity" not in below.stdout, below.stdout
    for stage in ("DevStg-Arch", "DevStg-Release"):
        at = run_py(["scripts/check.py", "--stage", stage, "--list"], cwd=scaffold)
        assert at.returncode == 0, at.stdout + at.stderr
        line = next(ln for ln in at.stdout.splitlines() if "cap-integrity" in ln)
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
        "[step:foo]\ngates = DevStg-Impl\n", encoding="utf-8"
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


def test_reference_profile_declares_only_the_readability_step():
    # The shipped stack.ini's [step:] examples are COMMENTED, so the reference
    # profile still equals the built-in plan (guards the byte-identity contract
    # above against a stray uncommented example line). Its one active step is
    # the per-change readability report (SR-216), part of the delivered harness.
    reference = _profile((KIT / "stack.ini.template").read_text(encoding="utf-8"))
    declared = check.extra_steps(
        reference, {"py": "py", "src": "s", "tests": "t", "coverage": "80"}
    )
    assert [s[0] for s in declared] == ["readability"]
    assert declared[0][2] == ["py", "scripts/check_readability.py", "--root", "."]


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


# --- [arch-map] mode: the declared inventory mode -----------------------------
# (The committed-map freshness step retired at WI-455; the mode now gates the
# AST-inventory readers, and check.py keeps validating it loudly.)


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
    # profile, telling the AST-inventory readers (WI-455) there is no Python
    # source to scan — their layers stay dormant, not vacuously green — and
    # the fresh repo's harness floor is green on day one.
    dest = tmp_path / "repo"
    proc = run_py(
        [SCRIPTS / "bootstrap.py", "--dest", dest, "--stack", "node"], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    ini = (dest / "docs" / "stack.ini").read_text(encoding="utf-8")
    assert "mode = files" in ini
    assert "mode = symbols" not in ini
    assert not (dest / "docs" / "architecture.md").exists()
    chk = run_py(["scripts/check.py", "--run-step", "trajectory"], cwd=dest)
    assert chk.returncode == 0, chk.stdout + chk.stderr


# --- Every reader of docs/stack.ini keeps its outcome (WI-915) -----------------
# Thirteen functions read the profile, all through `kitlib.config`'s one
# reader. Each is driven here through its real entry point over the same nine
# input classes, and its outcome is pinned: its key case, its defaults and its
# failure rule. `today` is the outcome each site gave before the shared reader;
# `ruled` holds the cells a ruled read change moved, with their outcome now
# (Q1: one decode rule, UTF-8 with an optional BOM and a stray byte read as
# U+FFFD; Q2: a path that exists but cannot be read is an error, denied by
# default). A site that ends on an uncaught error is pinned to raise, never to
# a particular exception type.

_CLASSES = (
    "absent",
    "empty",
    "valid",
    "bom",
    "stray",
    "parse",
    "upper",
    "twin",
    "directory",
)
_STRAY = b"[notes]\ntext = caf\xff\n"  # one non-UTF-8 byte inside a value
_RAISES = ("raises",)
_RAISES_VALUE_ERROR = ("raises", "ValueError")
_EXIT = ("exit", "is malformed")
_Q1 = "Q1: one decode rule, the BOM accepted and a stray byte replaced"
_Q2 = "Q2: a path that exists but cannot be read is the error outcome"


@functools.lru_cache(maxsize=None)
def _script(name):
    """One import per kit script for the whole grid, not one per cell."""
    return load_script(name)


_TESTS_FOR_LLRS = """[design.LLR-001]
sr_refs = ["SR-001"]
module = "src/m.py"
status = "Approved"
"""
_TESTS_FOR_TCS = """[test.TC-001]
verifies = ["LLR-001"]
tier = "Smoke"
evidence = "tests/test_m.py; spec/test_m.py"
status = "Approved"
"""


def _value(outcome):
    return ("value", outcome)


def _parsed(cp, section, option):
    """A parsed profile as a comparable value: None when the site returned
    none, else the one option the site's callers read from it."""
    return None if cp is None else ("parsed", cp.get(section, option, fallback=None))


def _drive(call, value_error_is_the_contract=False):
    """The site's outcome: its value, its "is malformed" exit, or a raise."""
    try:
        return _value(call())
    except SystemExit as exc:
        code = str(exc.code)
        return ("exit", "is malformed") if "is malformed" in code else ("exit", code)
    except Exception as exc:  # noqa: BLE001 - the outcome under test is "raises"
        if value_error_is_the_contract and isinstance(exc, ValueError):
            return _RAISES_VALUE_ERROR
        return _RAISES


def _write_class(ini, cls, site):
    ini.parent.mkdir(parents=True, exist_ok=True)
    if cls == "absent":
        return
    if cls == "directory":
        ini.mkdir()
        return
    text = {
        "empty": "",
        "valid": site["valid"],
        "bom": site["valid"],
        "stray": site["valid"],
        "parse": "a line before any section header\n" + site["valid"],
        "upper": site["upper"],
        "twin": site["twin"],
    }[cls]
    data = text.encode("utf-8")
    if cls == "bom":
        data = b"\xef\xbb\xbf" + data
    if cls == "stray":
        data += _STRAY
    ini.write_bytes(data)


def _smoke_budget_module():
    spec = importlib.util.spec_from_file_location(
        "check_smoke_budget_under_test", ROOT / "scripts" / "check_smoke_budget.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tests_for(docs):
    """`trace._cmd_tests_for` over a one-row spine whose case names a test
    under `tests/` and one under `spec/`: the printed path is the test root."""
    import contextlib
    import io

    trace = _script("trace")
    (docs / "requirements").mkdir(parents=True, exist_ok=True)
    (docs / "test").mkdir(parents=True, exist_ok=True)
    (docs / "requirements" / "low-level-requirements.toml").write_text(
        _TESTS_FOR_LLRS, encoding="utf-8"
    )
    (docs / "test" / "test-cases.toml").write_text(_TESTS_FOR_TCS, encoding="utf-8")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = trace._cmd_tests_for(docs, "src/m.py")
    return rc, out.getvalue().splitlines()


def _sites():
    """Each site: its driver, its three file texts, and its outcome per class
    (`ruled` maps a class to its new outcome and the ruled change's reason)."""
    paths_src = ("[paths]\nsrc = lib\n", "[paths]\nSRC = lib\n")
    paths_twin = "[paths]\nsrc = lib\nSRC = other\n"
    scan = "[arch-map]\nmode = files\n"
    gen = (
        "[generated]\ndocs/stage = stage\n",
        "[generated]\nPROJECT_STATE.html = html\n",
        "[generated]\nreadme.md = md\nREADME.md = md\n",
    )
    lib = _value(("parsed", "lib"))
    scan_v, scan_d = _value(("lib", "files")), _value(("src", "symbols"))
    return [
        {
            "name": "check.load_profile",
            "call": lambda root, ini, mp: _parsed(
                _script("check").load_profile(ini), "paths", "src"
            ),
            "valid": paths_src[0],
            "upper": paths_src[1],
            "twin": paths_twin,
            "today": {
                "absent": _value(None),
                "empty": _value(("parsed", None)),
                "valid": lib,
                "bom": lib,
                "stray": lib,
                "parse": _EXIT,
                "upper": lib,
                "twin": _EXIT,
                "directory": _RAISES,
            },
            "ruled": {"directory": (_EXIT, _Q2)},
        },
        {
            "name": "check._generated_census",
            "call": lambda root, ini, mp: _script("check")._generated_census(root),
            "valid": gen[0],
            "upper": gen[1],
            "twin": gen[2],
            "today": {
                "absent": _value([]),
                "empty": _value([]),
                "valid": _value(["docs/stage"]),
                "bom": _value(["docs/stage"]),
                "stray": _value(["docs/stage"]),
                "parse": _value([]),
                "upper": _value(["PROJECT_STATE.html"]),
                "twin": _value(["readme.md", "README.md"]),
                "directory": _value([]),
            },
            "ruled": {},
        },
        {
            "name": "agent_common._declared_test_command",
            "call": lambda root, ini, mp: _script(
                "agent_common"
            )._declared_test_command(ini, py="PY"),
            "value_error_is_the_contract": True,
            "valid": "[product]\ntest = pytest -q\n",
            "upper": "[product]\nTEST = pytest -q\n",
            "twin": "[product]\ntest = pytest -q\nTEST = other\n",
            "today": {
                "absent": _RAISES_VALUE_ERROR,
                "empty": _value(None),
                "valid": _value(["pytest", "-q"]),
                "bom": _value(["pytest", "-q"]),
                "stray": _value(["pytest", "-q"]),
                "parse": _RAISES_VALUE_ERROR,
                "upper": _value(["pytest", "-q"]),
                "twin": _RAISES_VALUE_ERROR,
                "directory": _RAISES_VALUE_ERROR,
            },
            "ruled": {},
        },
        {
            "name": "agent_policy.read_agent_loop_config",
            "call": lambda root, ini, mp: _script(
                "agent_policy"
            ).read_agent_loop_config(ini.parent),
            "valid": "[agent-loop]\njobs = 2\n",
            "upper": "[agent-loop]\nJOBS = 2\n",
            "twin": "[agent-loop]\njobs = 2\nJOBS = 3\n",
            "today": {
                "absent": _value({}),
                "empty": _value({}),
                "valid": _value({"jobs": "2"}),
                "bom": _value({}),
                "stray": _value({}),
                "parse": _value({}),
                "upper": _value({"jobs": "2"}),
                "twin": _value({}),
                "directory": _value({}),
            },
            "ruled": {
                "bom": (_value({"jobs": "2"}), _Q1),
                "stray": (_value({"jobs": "2"}), _Q1),
            },
        },
        {
            "name": "check_doc_refs._scan_profile",
            "call": lambda root, ini, mp: _script("check_doc_refs")._scan_profile(root),
            "valid": paths_src[0] + scan,
            "upper": paths_src[1] + scan,
            "twin": paths_twin + scan,
            "today": {
                "absent": scan_d,
                "empty": scan_d,
                "valid": scan_v,
                "bom": scan_d,
                "stray": scan_v,
                "parse": scan_d,
                "upper": scan_v,
                "twin": scan_d,
                "directory": _RAISES,
            },
            "ruled": {"bom": (scan_v, _Q1), "directory": (scan_d, _Q2)},
        },
        {
            "name": "check_dupes_census._load_baseline",
            "call": lambda root, ini, mp: _script("check_dupes_census")._load_baseline(
                root
            ),
            "valid": "[dupes-census]\ngroups = 2\ncopies = 2\nlines = 32\n",
            "upper": "[dupes-census]\nGROUPS = 2\ncopies = 2\nlines = 32\n",
            "twin": "[dupes-census]\ngroups = 2\nGROUPS = 3\ncopies = 2\nlines = 32\n",
            "today": {
                "absent": _value(None),
                "empty": _value(None),
                "valid": _value((2, 2, 32)),
                "bom": _RAISES,
                "stray": _RAISES,
                "parse": _RAISES,
                "upper": _value((2, 2, 32)),
                "twin": _RAISES,
                "directory": _value(None),
            },
            "ruled": {
                "bom": (_value((2, 2, 32)), _Q1),
                "stray": (_value((2, 2, 32)), _Q1),
                "directory": (_RAISES, _Q2),
            },
        },
        {
            "name": "integrate._generated_table",
            "call": lambda root, ini, mp: _script("integrate")._generated_table(root),
            "valid": gen[0],
            "upper": gen[1],
            "twin": gen[2],
            "today": {
                "absent": _value({}),
                "empty": _value({}),
                "valid": _value({"docs/stage": "stage"}),
                "bom": _value({"docs/stage": "stage"}),
                "stray": _value({"docs/stage": "stage"}),
                "parse": _value({}),
                "upper": _value({"PROJECT_STATE.html": "html"}),
                "twin": _value({"readme.md": "md", "README.md": "md"}),
                "directory": _value({}),
            },
            "ruled": {},
        },
        {
            "name": "kitlib.evidence.source_paths",
            "call": lambda root, ini, mp: [
                declared for declared, _path in _kit_evidence().source_paths(root)
            ],
            "valid": "[paths]\nsrc = lib\ntests = tests\n",
            "upper": "[paths]\nSRC = lib\ntests = tests\n",
            "twin": "[paths]\nsrc = lib\nSRC = other\ntests = tests\n",
            "today": {
                "absent": _value([]),
                "empty": _value([]),
                "valid": _value(["lib", "tests"]),
                "bom": _value(["lib", "tests"]),
                "stray": _value(["lib", "tests"]),
                "parse": _value([]),
                "upper": _value(["lib", "tests"]),
                "twin": _value([]),
                "directory": _value([]),
            },
            "ruled": {},
        },
        {
            "name": "run_menu.load_capabilities",
            "call": lambda root, ini, mp: _script("run_menu").load_capabilities(ini),
            "valid": "[run]\nserve = python -m app\n",
            "upper": "[run]\nServe = python -m app\n",
            "twin": "[run]\nserve = python -m app\nServe = python -m other\n",
            "today": {
                "absent": _value([]),
                "empty": _value([]),
                "valid": _value([("serve", "python -m app", "")]),
                "bom": _EXIT,
                "stray": _RAISES,
                "parse": _EXIT,
                "upper": _value([("Serve", "python -m app", "")]),
                "twin": _value(
                    [
                        ("serve", "python -m app", ""),
                        ("Serve", "python -m other", ""),
                    ]
                ),
                "directory": _RAISES,
            },
            "ruled": {
                "bom": (_value([("serve", "python -m app", "")]), _Q1),
                "stray": (_value([("serve", "python -m app", "")]), _Q1),
                "directory": (_EXIT, _Q2),
            },
        },
        {
            "name": "trace._cmd_tests_for",
            "call": lambda root, ini, mp: _tests_for(ini.parent),
            "valid": "[paths]\ntests = spec\n",
            "upper": "[paths]\nTESTS = spec\n",
            "twin": "[paths]\ntests = spec\nTESTS = other\n",
            "today": {
                "absent": _value((0, ["tests/test_m.py"])),
                "empty": _value((0, ["tests/test_m.py"])),
                "valid": _value((0, ["spec/test_m.py"])),
                "bom": _value((0, ["spec/test_m.py"])),
                "stray": _RAISES,
                "parse": _RAISES,
                "upper": _value((0, ["spec/test_m.py"])),
                "twin": _RAISES,
                "directory": _value((0, ["tests/test_m.py"])),
            },
            "ruled": {
                "stray": (_value((0, ["spec/test_m.py"])), _Q1),
                "directory": (_RAISES, _Q2),
            },
        },
        {
            "name": "trajectory_arch._stack_ini_get",
            "call": lambda root, ini, mp: _script("trajectory_arch")._arch_scan_profile(
                root
            ),
            "valid": paths_src[0] + scan,
            "upper": paths_src[1] + scan,
            "twin": paths_twin + scan,
            "today": {
                "absent": scan_d,
                "empty": scan_d,
                "valid": scan_v,
                "bom": scan_d,
                "stray": scan_v,
                "parse": scan_d,
                "upper": scan_v,
                "twin": scan_d,
                "directory": _RAISES,
            },
            "ruled": {"bom": (scan_v, _Q1), "directory": (scan_d, _Q2)},
        },
        {
            "name": "trunk_step._profile",
            "call": lambda root, ini, mp: _parsed(
                _script("trunk_step")._profile(root), "paths", "src"
            ),
            "valid": paths_src[0],
            "upper": paths_src[1],
            "twin": paths_twin,
            "today": {
                "absent": _value(None),
                "empty": _value(("parsed", None)),
                "valid": lib,
                "bom": lib,
                "stray": lib,
                "parse": _value(None),
                "upper": lib,
                "twin": _value(None),
                "directory": _RAISES,
            },
            "ruled": {"directory": (_value(None), _Q2)},
        },
        {
            "name": "check_smoke_budget._profile",
            "call": _smoke_budget_limits,
            "valid": _SMOKE_LIMITS,
            "upper": _SMOKE_LIMITS_UPPER,
            "twin": _SMOKE_LIMITS + "CPU-SECONDS = 950\n",
            "today": {
                "absent": _RAISES,
                "empty": _RAISES,
                "valid": _value(_SMOKE_LIMITS_VALUE),
                "bom": _value(_SMOKE_LIMITS_VALUE),
                "stray": _RAISES,
                "parse": _RAISES,
                "upper": _value(_SMOKE_LIMITS_VALUE),
                "twin": _RAISES,
                "directory": _RAISES,
            },
            "ruled": {"stray": (_value(_SMOKE_LIMITS_VALUE), _Q1)},
        },
    ]


def _kit_evidence():
    from kitlib import evidence

    return evidence


_SMOKE_LIMITS = (
    "[smoke-budget]\ncpu-seconds = 900\nwall-seconds = 600\nmax-tests = 3000\n"
)
_SMOKE_LIMITS_UPPER = (
    "[smoke-budget]\nCPU-SECONDS = 900\nWALL-SECONDS = 600\nMAX-TESTS = 3000\n"
)
_SMOKE_LIMITS_VALUE = (900.0, 600.0, 3000)


def _smoke_budget_limits(root, ini, monkeypatch):
    budget = _smoke_budget_module()
    monkeypatch.setattr(budget, "STACK_INI", ini)
    return tuple(budget.declared_limits(budget._profile()))


def _cells():
    for site in _sites():
        for cls in _CLASSES:
            yield pytest.param(site, cls, id="{}-{}".format(site["name"], cls))


@pytest.mark.parametrize("site, cls", list(_cells()))
def test_each_stack_ini_reader_keeps_its_outcome(site, cls, tmp_path, monkeypatch):
    root = tmp_path / "repo"
    ini = root / "docs" / "stack.ini"
    _write_class(ini, cls, site)
    want = site["ruled"][cls][0] if cls in site["ruled"] else site["today"][cls]
    got = _drive(
        lambda: site["call"](root, ini, monkeypatch),
        site.get("value_error_is_the_contract", False),
    )
    assert got == want


def test_the_ruled_read_changes_move_exactly_seventeen_cells():
    # Seventeen cells moved under Q1 and Q2, every site states all nine
    # classes, and no cell is an expected failure any more.
    ruled = [(s["name"], c) for s in _sites() for c in s["ruled"]]
    assert len(ruled) == 17, ruled
    assert all(set(s["today"]) == set(_CLASSES) for s in _sites())
    assert not [p for p in _cells() if p.marks], "a cell is still marked"


# --- The one reader ------------------------------------------------------------


def _kit_config():
    from kitlib import config

    return config


def _ini(tmp_path, data):
    path = tmp_path / "stack.ini"
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    return path


def test_the_reader_answers_none_for_an_absent_path(tmp_path):
    assert _kit_config().read_stack_ini(tmp_path / "stack.ini") is None


def test_the_reader_folds_keys_unless_told_not_to(tmp_path):
    config = _kit_config()
    folded = config.read_stack_ini(_ini(tmp_path, "[paths]\nSRC = lib\n"))
    assert folded.get("paths", "src") == "lib"
    path = _ini(tmp_path, "[generated]\nPROJECT_STATE.html = html\n")
    as_written = config.read_stack_ini(path, fold_keys=False)
    assert as_written.options("generated") == ["PROJECT_STATE.html"]


def test_the_reader_accepts_a_bom_and_replaces_a_stray_byte(tmp_path):
    path = _ini(tmp_path, b"\xef\xbb\xbf[notes]\ntext = caf\xff\n")
    profile = _kit_config().read_stack_ini(path)
    assert profile.get("notes", "text") == "caf�"


def test_the_reader_keeps_percent_and_inline_semicolons_literal(tmp_path):
    profile = _kit_config().read_stack_ini(_ini(tmp_path, "[x]\na = 50% ; note\n"))
    assert profile.get("x", "a") == "50% ; note"


def test_the_reader_inherits_default_keys(tmp_path):
    path = _ini(tmp_path, "[DEFAULT]\nshared = yes\n[paths]\nsrc = lib\n")
    assert _kit_config().read_stack_ini(path).get("paths", "shared") == "yes"


def test_a_parse_error_is_the_one_error_and_names_the_file(tmp_path):
    config = _kit_config()
    path = _ini(tmp_path, "a line before any section header\n")
    with pytest.raises(config.StackIniError) as caught:
        config.read_stack_ini(path)
    assert repr(str(path)) in str(caught.value)  # the parser quotes the name


def test_a_directory_at_the_path_is_the_one_error(tmp_path):
    config = _kit_config()
    path = tmp_path / "stack.ini"
    path.mkdir()
    with pytest.raises(config.StackIniError):
        config.read_stack_ini(path)


def test_a_duplicate_key_is_the_one_error_only_when_folded(tmp_path):
    config = _kit_config()
    path = _ini(tmp_path, "[run]\nserve = a\nServe = b\n")
    with pytest.raises(config.StackIniError):
        config.read_stack_ini(path)
    assert config.read_stack_ini(path, fold_keys=False).options("run") == [
        "serve",
        "Serve",
    ]


def test_the_stack_ini_parse_is_one_home():
    # The parser and its options are named in the reader's module and nowhere
    # else under the kit's scripts or this repo's own tools, so a fourteenth
    # parse fails here rather than waiting for the next census.
    home = (SCRIPTS / "kitlib" / "config.py").resolve()
    tokens = (
        "ConfigParser(",
        "import configparser",
        "from configparser",
        "interpolation=None",
        "optionxform",
    )
    offenders = []
    for tree in (SCRIPTS, ROOT / "scripts"):
        for path in sorted(tree.rglob("*.py")):
            if path.resolve() == home:
                continue
            text = path.read_text(encoding="utf-8")
            offenders += [
                "{}: {}".format(path.relative_to(ROOT).as_posix(), tok)
                for tok in tokens
                if tok in text
            ]
    assert offenders == []
