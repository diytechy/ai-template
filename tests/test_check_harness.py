"""check.py end-to-end: the documented flow must be green on a minimal project,
and the tier/coverage wiring must not silently skip tests."""

import os

from conftest import (
    DEMO_SRC,
    SCRIPTS,
    SRS,
    augment_env,
    load_script,
    make_minimal_project,
    run_py,
)


def test_subprocess_coverage_wiring_survives_pytest_cov_7():
    # pytest-cov < 7 exported COV_CORE_DATAFILE and augment_env keyed on it;
    # pytest-cov 7 dropped the whole COV_CORE_* env contract, so keying on it
    # alone silently unwires every child and the harness coverage floor reads
    # a fraction of reality (observed: 29% vs the 80 floor on a fresh
    # toolchain). Under an active coverage run, augment_env must still wire.
    import pytest

    import coverage

    if os.environ.get("COV_CORE_DATAFILE"):
        pytest.skip("legacy pytest-cov env contract active; nothing to prove")
    if coverage.Coverage.current() is None:
        pytest.skip("not a coverage-measured run")
    env = augment_env(dict(os.environ))
    assert "COVERAGE_PROCESS_START" in env, (
        "augment_env did not wire the child under an active coverage session"
    )


def test_minimal_project_is_green(scaffold):
    # The full documented flow: scaffold -> code + traced registries -> harness.
    # This is the regression test for "fresh clone fails": check.py must find
    # ruff/pytest via the running interpreter, not a PATH that lacks the venv.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/check.py", "--gate", "all", "--tier", "all"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT: PASS" in proc.stdout
    # The regenerated architecture doc carries the Mermaid dependency diagram.
    arch = (scaffold / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "```mermaid" in arch
    assert "src/demo" in arch


def test_off_root_fails_loudly(tmp_path):
    # M2 / WI-100: check.py reads docs/gate + docs/stack.ini + docs/architecture.md
    # relative to CWD. Run it where there is no docs/ tree and it must FAIL loudly
    # rather than silently fall back to the built-in commands and gate `all` (a
    # different, weaker plan). tmp_path has no docs/, so this stands in for "off
    # the repo root". SCRIPTS is absolute, so check.py is still found to run.
    proc = run_py([SCRIPTS / "check.py", "--gate", "G1"], cwd=tmp_path)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "must run at the repo root" in (proc.stdout + proc.stderr)


def test_step_env_strips_ambient_coverage_vars(monkeypatch):
    # check.py must not let a parent coverage session (a CI wrapper, or the kit's
    # own meta-suite measuring check.py under --cov) corrupt the project's own
    # `pytest --cov` step: the COVERAGE_*/COV_CORE_* orchestration vars are
    # stripped from a spawned step's env, while ordinary vars pass through.
    check = load_script("check")
    monkeypatch.setenv("COVERAGE_PROCESS_START", "/x/.coveragerc")
    monkeypatch.setenv("COVERAGE_FILE", "/x/.coverage")
    monkeypatch.setenv("COV_CORE_DATAFILE", "/x/.coverage")
    monkeypatch.setenv("KEEP_ME", "yes")
    env = check._step_env()
    assert "COVERAGE_PROCESS_START" not in env
    assert "COVERAGE_FILE" not in env
    assert "COV_CORE_DATAFILE" not in env
    assert env.get("KEEP_ME") == "yes"


def test_unmarked_test_runs_in_full_tier(scaffold):
    # An unmarked test must run pre-merge (tier full); the old opt-in marker
    # scheme silently deselected it.
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_unmarked.py").write_text(
        '"""An ordinary test with no tier marker."""\n\n\n'
        "def test_unmarked_runs():\n    assert True\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "full"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "2 passed" in proc.stdout  # the smoke test AND the unmarked one


def test_smoke_tier_runs_only_smoke_and_skips_coverage_gate(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_unmarked.py").write_text(
        '"""An ordinary test with no tier marker."""\n\n\n'
        "def test_unmarked_runs():\n    assert True\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "smoke"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 passed" in proc.stdout  # only the @pytest.mark.smoke test


def test_failing_test_fails_the_harness(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_broken.py").write_text(
        '"""Deliberately failing test."""\n\n\ndef test_broken():\n    assert False\n',
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--tier", "full"], cwd=scaffold)
    assert proc.returncode != 0
    assert "RESULT: FAIL" in proc.stdout


def test_step_plan_wiring():
    # Unit-level checks on the step table, without spawning tools.
    check = load_script("check")
    assert check.TIERS["full"] == "not release"  # unmarked tests run pre-merge

    def cmd_of(plan, name):
        return next(s[2] for s in plan if s[0] == name)

    smoke = check.steps(80, "smoke", "G3")
    full = check.steps(80, "full", "all")
    smoke_pytest = cmd_of(smoke, "tests+coverage")
    full_pytest = cmd_of(full, "tests+coverage")
    # Coverage threshold applies to full/release, never to the smoke subset.
    assert not any(a.startswith("--cov-fail-under") for a in smoke_pytest)
    assert "--cov-fail-under=80" in full_pytest
    # G3/all adds the SR status criterion to traceability.
    assert "--require-verified" in cmd_of(full, "traceability")
    assert "--require-verified" not in cmd_of(
        check.steps(80, "all", "G2"), "traceability"
    )
    # Tools run via this interpreter (-m), not a bare PATH lookup.
    assert full_pytest[1:3] == ["-m", "pytest"]
    assert cmd_of(full, "lint")[1:3] == ["-m", "ruff"]

    # Each step declares a process/product layer (process.md §7). Process steps
    # are kit-owned and stdlib-only (requires == ()); product steps name the
    # tool(s) they need — the layer formalizes that already-implied split.
    layer_of = {s[0]: s[4] for s in full}
    assert layer_of["traceability"] == "process"
    assert layer_of["design-flows"] == "process"
    assert layer_of["arch-map"] == "process"
    assert layer_of["format"] == "product"
    assert layer_of["lint"] == "product"
    assert layer_of["tests+coverage"] == "product"
    assert {s[4] for s in full} == {"process", "product"}
    for name, requires, _cmd, _gates, layer in full:
        if layer == "process":
            assert requires == (), name  # stdlib-only, no tool to wire
        else:
            assert requires, name  # product steps declare their toolchain

    # Process-layer steps must resolve kit scripts via an absolute path so the
    # commands work even when the repo's scripts directory is capitalised
    # differently (e.g. "Scripts/" on an NTFS case-preserving system that also
    # runs on case-sensitive Linux CI).  The path is the second element of the
    # command list (after sys.executable).
    import os

    process_steps = [s for s in full if s[4] == "process"]
    for name, _req, cmd, _gates, _layer in process_steps:
        script_arg = cmd[1]  # first arg after the interpreter
        if script_arg.endswith(".py"):
            assert os.path.isabs(script_arg), (
                "process step {!r} uses a relative script path {!r}; "
                "use _SCRIPTS / 'name.py' so it resolves correctly when "
                "the repo scripts dir is capitalised differently".format(
                    name, script_arg
                )
            )


def test_missing_command_is_designed_failure():
    # A rewired step ("swap the format/lint/test commands for your toolchain")
    # names an executable the module guard can't see (npx, cargo, ...). Its
    # absence must be a designed FAIL with guidance — not a raw
    # FileNotFoundError traceback — and --lenient downgrades it to SKIP,
    # exactly like the module guard.
    import sys

    check = load_script("check")
    status, detail = check.run_step(
        "demo", (), ["no-such-tool-t29", "--check"], lenient=False
    )
    assert status == "FAIL"
    assert "no-such-tool-t29" in detail
    assert "not found" in detail
    status, detail = check.run_step("demo", (), ["no-such-tool-t29"], lenient=True)
    assert status == "SKIP"
    # The reference plan is unaffected: sys.executable is a real path, so the
    # guard resolves it without a PATH lookup.
    status, _detail = check.run_step(
        "noop", (), [sys.executable, "-c", "pass"], lenient=False
    )
    assert status == "PASS"


def test_run_steps_batch_passes_on_clean_project(scaffold):
    # The pre-commit hook's batched floor: several independent steps in one
    # interpreter spawn, run concurrently, each reported. Green on a fully
    # traced, freshly mapped project. Mirrors the shipped hook's batch (which
    # now includes derived-gate, the docs/gate freshness guard).
    make_minimal_project(scaffold)
    proc = run_py(
        [
            "scripts/check.py",
            "--run-steps",
            "arch-map,okf,trajectory-map,trajectory,registry-integrity,derived-gate,skills-sync",
        ],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for name in (
        "arch-map",
        "okf",
        "trajectory-map",
        "registry-integrity",
        "derived-gate",
    ):
        assert name in proc.stdout


def test_derived_gate_step_wired_at_every_gate_and_runs(scaffold):
    # check.py consumes the derived gate (docs/specs/derived-gate-model.md §5):
    # the derived-gate freshness step is a process-layer step at every gate.
    check = load_script("check")
    for gate in ("G1", "G2", "G3"):
        plan = [s for s in check.steps(80, "full", gate) if gate in s[3]]
        match = [s for s in plan if s[0] == "derived-gate"]
        assert match, "derived-gate missing at {}".format(gate)
        assert match[0][4] == "process" and match[0][1] == ()  # stdlib, no tool
    # End-to-end: on a G3-complete project (docs/gate regenerated to G3) the step
    # passes; un-verifying an SR without regenerating docs/gate makes it FAIL.
    make_minimal_project(scaffold)
    ok = run_py(["scripts/check.py", "--run-step", "derived-gate"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    sr = scaffold / "docs" / "requirements" / "system-requirements.csv"
    sr.write_text(
        sr.read_text(encoding="utf-8").replace(",Test,Verified", ",Test,Implemented"),
        encoding="utf-8",
    )
    bad = run_py(["scripts/check.py", "--run-step", "derived-gate"], cwd=scaffold)
    assert bad.returncode != 0
    assert "STALE" in bad.stdout + bad.stderr


def test_run_steps_reports_every_failure(scaffold):
    # Unlike a `set -e` chain of single --run-step calls (which stops at the
    # first stale artifact), the batch names ALL failures in one pass: stale
    # the code map AND duplicate a registry id, and both steps must FAIL in
    # the same run.
    make_minimal_project(scaffold)
    (scaffold / "src" / "demo.py").write_text(
        DEMO_SRC + "\n\ndef extra():\n    return 0\n", encoding="utf-8"
    )
    sr = scaffold / "docs" / "requirements" / "system-requirements.csv"
    sr.write_text(
        sr.read_text(encoding="utf-8") + SRS.splitlines()[1] + "\n", encoding="utf-8"
    )
    proc = run_py(
        ["scripts/check.py", "--run-steps", "arch-map,registry-integrity"],
        cwd=scaffold,
    )
    assert proc.returncode != 0
    lines = proc.stdout.splitlines()
    assert any("FAIL" in ln and "arch-map" in ln for ln in lines), proc.stdout
    assert any("FAIL" in ln and "registry-integrity" in ln for ln in lines), proc.stdout


def test_step_gate_honours_an_explicit_gate(scaffold):
    # WI-355: --run-step/--run-steps used to resolve their plan at gate "all"
    # unconditionally, so `--gate G3 --run-steps trajectory` ran the WARN-first
    # command while `--gate G3 --list` advertised the --strict one. _step_gate is
    # the explicit-vs-defaulted sentinel: an explicitly passed --gate builds the
    # command AT that gate; a defaulted one (argparse default=None — what the
    # pre-commit hook passes) stays "all" and must NEVER consult docs/gate, or
    # the commit floor would arm --strict (see the trajectory step's comment).
    check = load_script("check")
    assert check._step_gate("G3") == "G3"
    assert check._step_gate("G1") == "G1"
    assert check._step_gate(None) == "all"
    assert check._step_gate("") == "all"

    # And the sentinel really changes the command built for the step that carries
    # the R-B..R-E promotions — the only step keying on gate in ("G2","G3").
    def traj_cmd(gate):
        match = [s for s in check.steps(80, "full", gate) if s[0] == "trajectory"]
        assert match, "no trajectory step at gate {}".format(gate)
        return match[0][2]

    assert "--strict" in traj_cmd("G3")
    assert "--strict" in traj_cmd("G2")
    assert "--strict" not in traj_cmd("all")
    # Name lookup stays unfiltered at any gate: `format` is a G3-only step but the
    # hook resolves it with no --gate, so it must still be findable at "all".
    assert [s for s in check.steps(80, "full", "all") if s[0] == "format"]


def test_run_steps_unknown_name_fails_loudly(scaffold):
    proc = run_py(["scripts/check.py", "--run-steps", "arch-map,nope"], cwd=scaffold)
    assert proc.returncode != 0
    assert "nope" in proc.stdout + proc.stderr


def test_jobs_parallel_plan_matches_sequential(scaffold):
    # --jobs 0 runs the plan's steps concurrently with captured (never
    # interleaved) output; the result set and exit semantics must match the
    # sequential default. Smoke tier keeps the test cheap.
    make_minimal_project(scaffold)
    par = run_py(
        ["scripts/check.py", "--gate", "all", "--tier", "smoke", "--jobs", "0"],
        cwd=scaffold,
    )
    assert par.returncode == 0, par.stdout + par.stderr
    assert "RESULT: PASS" in par.stdout
    # Every step of the sequential plan is present in the parallel summary.
    seq = run_py(
        ["scripts/check.py", "--gate", "all", "--tier", "smoke", "--list"],
        cwd=scaffold,
    )
    for ln in seq.stdout.splitlines():
        if ln.strip().startswith("- "):
            name = ln.strip().split()[1]
            assert name in par.stdout, name
    # And a failure still fails the parallel run (never a false green).
    (scaffold / "tests" / "test_broken.py").write_text(
        '"""Deliberately failing test."""\n\n\n'
        "import pytest\n\n\n"
        "@pytest.mark.smoke\ndef test_broken():\n    assert False\n",
        encoding="utf-8",
    )
    bad = run_py(
        ["scripts/check.py", "--gate", "all", "--tier", "smoke", "--jobs", "0"],
        cwd=scaffold,
    )
    assert bad.returncode != 0
    assert "RESULT: FAIL" in bad.stdout


# --- WI-279: a [step:] may declare `lane =` to serialize a data-dependent step
# (the per-module coverage floor reads the tests+coverage JSON) after its
# producer under --jobs>1, instead of racing it and finding no output yet.
def test_extra_step_lanes_reads_declared_lane():
    import configparser

    check = load_script("check")
    cp = configparser.ConfigParser(interpolation=None)
    cp.read_string(
        "[step:module-coverage]\ncommand = {py} x.py\nlane = tests+coverage\n\n"
        "[step:dupes]\ncommand = {py} y.py\n"  # no lane -> own lane, omitted
    )
    assert check.extra_step_lanes(cp) == {"module-coverage": "tests+coverage"}


def test_declared_lane_serializes_a_dependent_step_under_jobs(tmp_path):
    import sys

    check = load_script("check")
    order = tmp_path / "order.txt"

    def step(name, token, sleep):
        code = (
            "import time,pathlib;time.sleep({s});"
            "p=pathlib.Path('{f}');"
            "p.write_text((p.read_text() if p.exists() else '')+'{t}')"
        ).format(s=sleep, f=order.as_posix(), t=token)
        return (name, (), [sys.executable, "-c", code], {"G3"}, "product")

    # The producer sleeps; an un-laned consumer would win the race under jobs=2.
    # Sharing the producer's lane forces the consumer to run AFTER it, in plan
    # order, so the file reads "PC" deterministically (the coverage-floor case).
    plan = [step("producer", "P", 0.4), step("consumer", "C", 0.0)]
    check.run_plan(plan, lenient=False, jobs=2, lane_map={"consumer": "producer"})
    assert order.read_text() == "PC"


def test_bad_lane_fails_loudly(scaffold):
    # A [step:] whose `lane` names no real step must fail LOUDLY at plan time,
    # never silently re-race the step (a false green under --jobs>1).
    make_minimal_project(scaffold)
    stack = scaffold / "docs" / "stack.ini"
    stack.write_text(
        stack.read_text(encoding="utf-8")
        + "\n[step:floors]\ncommand = {py} scripts/check_coverage.py\n"
        + "lane = no-such-step\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/check.py", "--gate", "G3", "--list"], cwd=scaffold)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "names no known step" in proc.stdout + proc.stderr


def test_tier_substitution_available_to_declared_steps():
    # {tier} exposes the run's tier to any [step:] command (the tier-sensitive
    # per-module coverage floor reads it) — it expands like {py}/{src}/... .
    import configparser

    check = load_script("check")
    cp = configparser.ConfigParser(interpolation=None)
    cp.read_string("[step:cov]\ncommand = {py} c.py --tier {tier}\n")
    for tier in ("smoke", "full"):
        plan = check.steps(80, tier, "G3", None, cp)
        cov = next(s for s in plan if s[0] == "cov")
        assert "--tier" in cov[2] and tier in cov[2], (tier, cov[2])


def test_module_coverage_full_then_smoke_run_scopes_the_report(scaffold):
    # REVIEW-A regression: the module-coverage floor must NOT grade a stale
    # full-tier coverage.json as a current PASS after a no-coverage smoke run.
    # check.py run-scopes the report (clears it before the plan) and the step is
    # told smoke measures no coverage, so smoke SKIPs and the file is gone.
    make_minimal_project(scaffold)
    stack = scaffold / "docs" / "stack.ini"
    text = stack.read_text(encoding="utf-8").replace(
        "--cov-report=term-missing",
        "--cov-report=term-missing --cov-report=json",
    )
    text += (
        "\n[step:module-coverage]\n"
        "command = {py} scripts/check_coverage.py --tier {tier} --skip-tiers smoke\n"
        "gates = G3\nlayer = product\nlane = tests+coverage\n"
    )
    stack.write_text(text, encoding="utf-8")
    (scaffold / "docs" / "coverage-floors").write_text(
        "src/demo.py 50\n", encoding="utf-8"
    )

    # Full tier: coverage.json is produced and the floor is graded and holds.
    full = run_py(
        ["scripts/check.py", "--gate", "G3", "--tier", "full", "--jobs", "0"],
        cwd=scaffold,
    )
    assert full.returncode == 0, full.stdout + full.stderr
    assert (scaffold / "coverage.json").exists()
    assert "module floor(s) hold" in full.stdout

    # Smoke tier: the stale full report is cleared before the (no-coverage) run,
    # the step SKIPs instead of grading it, and the run stays honest-green.
    smoke = run_py(
        ["scripts/check.py", "--gate", "G3", "--tier", "smoke", "--jobs", "0"],
        cwd=scaffold,
    )
    assert smoke.returncode == 0, smoke.stdout + smoke.stderr
    assert "module floor(s) hold" not in smoke.stdout  # not graded
    assert "check_coverage: SKIP" in smoke.stdout  # the tier-skip fired
    assert not (scaffold / "coverage.json").exists()  # run-scoped away


def test_default_gate_comes_from_gate_file(scaffold):
    # check.py without --gate reads the committed docs/gate (bootstrap writes
    # G1), so CI enforces the bar the project is actually at — a fresh scaffold
    # must be green, not red-until-G3 (the day-one false-red regression).
    gate_file = scaffold / "docs" / "gate"
    assert gate_file.read_text(encoding="utf-8").strip() == "G1"
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Plan for gate G1" in proc.stdout
    # And the G1 plan actually passes on the untouched scaffold (the CI path).
    proc = run_py(["scripts/check.py", "--tier", "smoke", "--lenient"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT: PASS" in proc.stdout

    # Bumping the gate raises the bar; an explicit --gate always wins; garbage
    # in the file fails loudly rather than running a silently wrong plan.
    gate_file.write_text("G2\n", encoding="utf-8")
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert "Plan for gate G2" in proc.stdout
    proc = run_py(["scripts/check.py", "--gate", "G1", "--list"], cwd=scaffold)
    assert "Plan for gate G1" in proc.stdout
    gate_file.write_text("banana\n", encoding="utf-8")
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert proc.returncode != 0
    assert "docs/gate" in proc.stdout + proc.stderr

    # Comment lines are tolerated — every declared-policy file shares one
    # parse rule (first non-empty, non-comment line): a docs/gate annotated
    # like the sibling gate-policy/push-policy files must still resolve.
    gate_file.write_text("# active gate (see process.md §7)\nG2\n", encoding="utf-8")
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Plan for gate G2" in proc.stdout


def test_list_tags_process_and_product_layers(scaffold):
    # A newcomer running --list must see which steps are kit-owned (process) and
    # which they have to localize (product).
    proc = run_py(["scripts/check.py", "--gate", "all", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "[process]" in proc.stdout
    assert "[product]" in proc.stdout
    # The layer must line up with the step it tags.
    lines = proc.stdout.splitlines()
    assert any("traceability" in ln and "[process]" in ln for ln in lines)
    assert any("format" in ln and "[product]" in ln for ln in lines)
