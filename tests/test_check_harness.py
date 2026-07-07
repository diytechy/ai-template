"""check.py end-to-end: the documented flow must be green on a minimal project,
and the tier/coverage wiring must not silently skip tests."""

from conftest import load_script, make_minimal_project, run_py


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
