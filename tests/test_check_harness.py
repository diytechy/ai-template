"""check.py end-to-end: the documented flow must be green on a minimal project,
and the tier/coverage wiring must not silently skip tests."""

import os

from conftest import (
    SCRIPTS,
    SRS,
    augment_env,
    load_script,
    make_minimal_project,
    pin_autocrlf,
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
    # (No docs/architecture.md exists to regenerate since WI-455 — the module
    # inventory derives live from src/, exercised by the trajectory step above.)


def test_off_root_fails_loudly(tmp_path):
    # M2 / WI-100: check.py reads docs/stage + docs/stack.ini
    # relative to CWD. Run it where there is no docs/ tree and it must FAIL loudly
    # rather than silently fall back to the built-in commands and gate `all` (a
    # different, weaker plan). tmp_path has no docs/, so this stands in for "off
    # the repo root". SCRIPTS is absolute, so check.py is still found to run.
    proc = run_py([SCRIPTS / "check.py", "--gate", "DevStg-Reqs"], cwd=tmp_path)
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
    proc = run_py(
        ["scripts/check.py", "--gate", "DevStg-Impl", "--tier", "full"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "2 passed" in proc.stdout  # the smoke test AND the unmarked one


def test_smoke_tier_runs_only_smoke_and_skips_coverage_gate(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_unmarked.py").write_text(
        '"""An ordinary test with no tier marker."""\n\n\n'
        "def test_unmarked_runs():\n    assert True\n",
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check.py", "--gate", "DevStg-Impl", "--tier", "smoke"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 passed" in proc.stdout  # only the @pytest.mark.smoke test


def test_failing_test_fails_the_harness(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "tests" / "test_broken.py").write_text(
        '"""Deliberately failing test."""\n\n\ndef test_broken():\n    assert False\n',
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/check.py", "--gate", "DevStg-Impl", "--tier", "full"], cwd=scaffold
    )
    assert proc.returncode != 0
    assert "RESULT: FAIL" in proc.stdout


def test_backlink_coverage_step_is_wired_at_the_right_bars(tmp_path):
    """THE WIRING NOBODY PINNED (2026-08-20, the batch review's MINOR-20). Every
    other part of the reverse-coverage layer has a test — the grammar, the
    percentage, the dial reader, the report's vacuity — while the fact that
    `check.py` runs it AT ALL was pinned by nothing. A step nothing invokes is a
    measurement nobody takes, and the whole ruling was "ship the measurement".

    Two facts, both driven off the real step table: the step's THRESHOLD is the
    DevStg-Impl rung and not below (which is also why the shipped template must
    not claim it warns at a plain run — below that rung it does not run), and
    `--strict-backlinks` rides exactly the rungs that promote it.

    The threshold moved to Impl at WI-498 slice 2, and the reason is in the step
    table: what this grades is a literal `Implements:` declaration IN SOURCE, so
    below the rung where source exists it would grade an artifact that does not.
    The retired `{DevStg-Tests, DevStg-Impl}` tag named BARS, and the DevStg-Tests
    bar was itself only reached by a fully decomposed spine — the Impl rung — so
    this is where the step effectively always ran."""
    check = load_script("check")
    ladder = check._kitladder

    def step(stage):
        return next(
            (s for s in check.steps(80, "full", stage) if s[0] == "backlink-coverage"),
            None,
        )

    at_reqs = step(ladder.STAGE_REQS)
    assert at_reqs is not None, "the step vanished from the table entirely"
    _name, requires, cmd, threshold, layer = at_reqs
    assert layer == "process" and requires == ()  # kit-owned, stdlib-only
    assert "--backlink-coverage" in cmd, cmd
    # WHERE IT RUNS: the threshold is the step table's own answer, and a repo at
    # the requirements rung is NOT at or above it — so a plain run does not warn,
    # it does not run the step at all. (The shipped template claimed otherwise
    # until 2026-08-20.)
    assert threshold == ladder.STAGE_IMPL, threshold
    assert not check.at_or_above(ladder.STAGE_REQS, threshold)
    # ...and below its rung it is never promoted, so a stray invocation cannot
    # gate on a dial the repo has not reached.
    assert "--strict-backlinks" not in cmd, cmd
    for stage in (ladder.STAGE_IMPL, ladder.STAGE_RELEASE):
        found = step(stage)
        assert found is not None, "no backlink-coverage step at {}".format(stage)
        assert check.at_or_above(stage, found[3])
        assert "--strict-backlinks" in found[2], (
            "at {} the step must promote a below-minimum reading to a failure; "
            "without the flag the dial can never gate at any rung".format(stage)
        )


def test_step_plan_wiring():
    # Unit-level checks on the step table, without spawning tools.
    check = load_script("check")
    assert check.TIERS["full"] == "not release"  # unmarked tests run pre-merge

    def cmd_of(plan, name):
        return next(s[2] for s in plan if s[0] == name)

    smoke = check.steps(80, "smoke", "DevStg-Impl")
    full = check.steps(80, "full", "all")
    smoke_pytest = cmd_of(smoke, "tests+coverage")
    full_pytest = cmd_of(full, "tests+coverage")
    # Coverage threshold applies to full/release, never to the smoke subset.
    assert not any(a.startswith("--cov-fail-under") for a in smoke_pytest)
    assert "--cov-fail-under=80" in full_pytest
    # DevStg-Impl/all adds the SR status criterion to traceability.
    assert "--require-verified" in cmd_of(full, "traceability")
    assert "--require-verified" not in cmd_of(
        check.steps(80, "all", "DevStg-Tests"), "traceability"
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
    # includes derived-stage, the docs/stage freshness guard — it was
    # derived-gate over docs/gate until WI-498 slice 5 retired that axis).
    make_minimal_project(scaffold)
    proc = run_py(
        [
            "scripts/check.py",
            "--run-steps",
            "okf,trajectory-map,trajectory,registry-integrity,derived-stage,skills-sync",
        ],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for name in (
        "okf",
        "trajectory-map",
        "registry-integrity",
        "derived-stage",
    ):
        assert name in proc.stdout


def test_derived_stage_step_wired_at_every_rung_and_runs(scaffold):
    # check.py consumes the derived STAGE: the derived-stage freshness step is a
    # process-layer step at every rung. RE-KEYED at WI-498 slice 5 — the same
    # claim was made about `derived-gate` over `docs/gate` until that step and
    # the three-value BAR axis it guarded were retired; the concern (the derived
    # spine state's freshness is gated everywhere, from stdlib, with no tool
    # requirement) survives intact on the successor.
    check = load_script("check")
    for stage in check._kitladder.STAGE_ORDER:
        plan = check.resolve_plan(stage, 80, "full", None, None)
        match = [s for s in plan if s[0] == "derived-stage"]
        assert match, "derived-stage missing at {}".format(stage)
        assert match[0][4] == "process" and match[0][1] == ()  # stdlib, no tool
    # End-to-end: on a DevStg-Impl-complete project (docs/stage regenerated to
    # DevStg-Impl) the step passes; un-approving an SR without regenerating
    # docs/stage makes it FAIL.
    make_minimal_project(scaffold)
    ok = run_py(["scripts/check.py", "--run-step", "derived-stage"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    sr = scaffold / "docs" / "requirements" / "system-requirements.csv"
    sr.write_text(
        sr.read_text(encoding="utf-8").replace(",Test,Approved", ",Test,Drafted"),
        encoding="utf-8",
    )
    bad = run_py(["scripts/check.py", "--run-step", "derived-stage"], cwd=scaffold)
    assert bad.returncode != 0
    assert "STALE" in bad.stdout + bad.stderr


def test_run_steps_reports_every_failure(scaffold):
    # Unlike a `set -e` chain of single --run-step calls (which stops at the
    # first stale artifact), the batch names ALL failures in one pass: stale
    # the OKF bundle AND duplicate a registry id, and both steps must FAIL in
    # the same run.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "okf" / "index.md").write_text("# stale\n", encoding="utf-8")
    sr = scaffold / "docs" / "requirements" / "system-requirements.csv"
    sr.write_text(
        sr.read_text(encoding="utf-8") + SRS.splitlines()[1] + "\n", encoding="utf-8"
    )
    proc = run_py(
        ["scripts/check.py", "--run-steps", "okf,registry-integrity"],
        cwd=scaffold,
    )
    assert proc.returncode != 0
    lines = proc.stdout.splitlines()
    assert any("FAIL" in ln and "okf" in ln for ln in lines), proc.stdout
    assert any("FAIL" in ln and "registry-integrity" in ln for ln in lines), proc.stdout


def test_step_stage_honours_an_explicit_stage(scaffold):
    # WI-355: --run-step/--run-steps used to resolve their plan at "all"
    # unconditionally, so `--stage DevStg-Impl --run-steps trajectory` ran the
    # WARN-first command while `--stage DevStg-Impl --list` advertised the
    # --strict one. _step_stage is the explicit-vs-defaulted sentinel: an
    # explicitly passed --stage builds the command AT that rung; a defaulted one
    # (argparse default=None — what the pre-commit hook passes) stays ALL and
    # must NEVER consult the derived stage, or the commit floor would arm
    # --strict (see the trajectory step's comment).
    check = load_script("check")
    ladder = check._kitladder
    assert check._step_stage(ladder.STAGE_IMPL) == ladder.STAGE_IMPL
    assert check._step_stage(ladder.STAGE_REQS) == ladder.STAGE_REQS
    assert check._step_stage(None) == check.ALL
    assert check._step_stage("") == check.ALL

    # And the sentinel really changes the command built for the step that carries
    # the R-B..R-E promotions — the only step keying on the Impl rung for its
    # SEVERITY rather than for its selection.
    def traj_cmd(stage):
        match = [s for s in check.steps(80, "full", stage) if s[0] == "trajectory"]
        assert match, "no trajectory step at stage {}".format(stage)
        return match[0][2]

    assert "--strict" in traj_cmd(ladder.STAGE_IMPL)
    assert "--strict" in traj_cmd(ladder.STAGE_RELEASE)
    # Below the promotion rung it stays warn-first — and so does ALL, which is
    # the whole point of the sentinel (the hook's floor must not block a commit
    # on status.md drift).
    assert "--strict" not in traj_cmd(ladder.STAGE_TESTS)
    assert "--strict" not in traj_cmd(check.ALL)
    # Name lookup stays unfiltered at any rung: `format`'s threshold is the Impl
    # rung but the hook resolves it with no --stage, so it must still be findable
    # at ALL...
    assert [s for s in check.steps(80, "full", check.ALL) if s[0] == "format"]
    # ...and at an explicit LOW rung too (WI-360, WI-355-REVIEW-A MINOR 2). The
    # ALL assertion alone would stay green if steps() started filtering its
    # returned table, and DevStg-Reqs is the case that would break, so pin it.
    # `steps()` BUILDS the table; `resolve_plan` is what selects from it.
    assert [s for s in check.steps(80, "full", ladder.STAGE_REQS) if s[0] == "format"]
    assert not [
        s
        for s in check.resolve_plan(ladder.STAGE_REQS, 80, "full", None, None)
        if s[0] == "format"
    ]


def test_run_steps_unknown_name_fails_loudly(scaffold):
    proc = run_py(["scripts/check.py", "--run-steps", "okf,nope"], cwd=scaffold)
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
        return (name, (), [sys.executable, "-c", code], {"DevStg-Impl"}, "product")

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
    proc = run_py(["scripts/check.py", "--gate", "DevStg-Impl", "--list"], cwd=scaffold)
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
        plan = check.steps(80, tier, "DevStg-Impl", None, cp)
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
        "gates = DevStg-Impl\nlayer = product\nlane = tests+coverage\n"
    )
    stack.write_text(text, encoding="utf-8")
    (scaffold / "docs" / "coverage-floors").write_text(
        "src/demo.py 50\n", encoding="utf-8"
    )

    # Full tier: coverage.json is produced and the floor is graded and holds.
    full = run_py(
        [
            "scripts/check.py",
            "--gate",
            "DevStg-Impl",
            "--tier",
            "full",
            "--jobs",
            "0",
        ],
        cwd=scaffold,
    )
    assert full.returncode == 0, full.stdout + full.stderr
    assert (scaffold / "coverage.json").exists()
    assert "module floor(s) hold" in full.stdout

    # Smoke tier: the stale full report is cleared before the (no-coverage) run,
    # the step SKIPs instead of grading it, and the run stays honest-green.
    smoke = run_py(
        [
            "scripts/check.py",
            "--gate",
            "DevStg-Impl",
            "--tier",
            "smoke",
            "--jobs",
            "0",
        ],
        cwd=scaffold,
    )
    assert smoke.returncode == 0, smoke.stdout + smoke.stderr
    assert "module floor(s) hold" not in smoke.stdout  # not graded
    assert "check_coverage: SKIP" in smoke.stdout  # the tier-skip fired
    assert not (scaffold / "coverage.json").exists()  # run-scoped away


def test_the_default_stage_comes_from_the_derived_stage_file(scaffold):
    """check.py without --stage reads the repo's DERIVED effective stage, so CI
    enforces the rung the project is actually on — a fresh scaffold must be
    green, not red-until-Impl (the day-one false-red regression).

    THE SOURCE FILE CHANGED AT WI-498 slice 2: `docs/gate` (a bar) → `docs/stage`
    (a rung), read through `kitlib.stage.read_stage` rather than by scraping a
    line. Three properties move with it and are pinned below: a fresh scaffold
    still resolves the floor and still passes; an explicit --stage still wins;
    and a hand-edited value that is not a rung fails LOUDLY instead of selecting
    a silently wrong plan. The retired-vocabulary refusal keeps its ruling
    (OI-21 break 5 — the file is GENERATED, so a retired value there means the
    cache predates the conversion and the fix is one regenerate, not a reader
    that accepts both spellings forever); it is now enforced by
    `kitlib.stage.require_rung`, which refuses everything off the ladder rather
    than only the tags someone remembered to list."""
    stage_file = scaffold / "docs" / "stage"
    proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # A fresh scaffold ships the placeholder, so the reader DERIVES: an empty
    # spine earns nothing and the selection floor applies.
    assert "Plan at stage DevStg-Reqs" in proc.stdout
    # And that plan actually passes on the untouched scaffold (the CI path).
    proc = run_py(["scripts/check.py", "--tier", "smoke", "--lenient"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT: PASS" in proc.stdout

    # A REAL derived record is read back rather than re-derived (the fingerprint
    # fast path), and an explicit --stage always wins over it.
    assert (
        run_py([SCRIPTS / "derive_stage.py", "--root", "."], cwd=scaffold).returncode
        == 0
    )
    recorded = stage_file.read_text(encoding="utf-8")
    assert "stage = DevStg-Reqs" in recorded
    proc = run_py(
        ["scripts/check.py", "--stage", "DevStg-Release", "--list"], cwd=scaffold
    )
    assert "Plan at stage DevStg-Release" in proc.stdout

    # A hand-edited non-rung fails loudly, and the two cases differ: `banana` is
    # not rung-shaped at all, while a retired gate tag is the value an
    # un-regenerated cache would actually carry. Both are refused. The tag below
    # is the INPUT under test, not a live citation.
    for bad in ("banana", "G2"):  # check_vocab: allow
        stage_file.write_text(
            recorded.replace("stage = DevStg-Reqs", "stage = " + bad),
            encoding="utf-8",
        )
        proc = run_py(["scripts/check.py", "--list"], cwd=scaffold)
        assert proc.returncode != 0, bad
        assert bad in proc.stdout + proc.stderr, bad
        assert "stage ladder" in proc.stdout + proc.stderr, bad


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


# --- OI-31: the staged-vs-worktree divergence detector -----------------------
# The step is not a tenth freshness gate: it reads the SAME docs/stack.ini
# `[generated]` census the nine gates are wired from (the census's own rules are
# held in tests/test_generated_freshness_wiring.py) and asks the question none
# of them can — is the artifact on disk the one about to be COMMITTED?
#
# The gap it closes (OI-31, ruled option (b) 2026-08-18): every freshness step
# resolves its artifact from the filesystem, so an author who regenerates and
# forgets to `git add` gets an honest green over a stale commit. Measured at
# 3b8d306d, where PROJECT_STATE.html was modified in the worktree, absent from
# the index, and the committed tree failed the very gate that guarded it.
#
# HERE rather than beside the census, which is the more natural home: these
# cases build real git repos, and that module is in the SMOKE tier, whose
# membership budget (docs/stack.ini [smoke-budget]) is a shared dial this lane
# did not own. They run at slice close and in CI with the rest of this module.


def _git(repo, *args):
    import subprocess

    subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    )


# A census that is deliberately NOT the kit's own: the step must read whatever
# docs/stack.ini declares (that is the whole point of reading rather than
# copying the list), so the fixture declares a name no kit script knows, a
# prefix row, and a marker-pair row — the three shapes §5.2 admits.
FIXTURE_CENSUS = """[generated]
HOUSE_DASHBOARD.html = trajectory
docs/bundle/ = okf
docs/status.md = status | <!-- BEGIN GENERATED STATUS --> | <!-- END GENERATED STATUS -->
"""


def _divergence_repo(tmp_path):
    """A tiny git repo whose committed tree matches its declared census."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(FIXTURE_CENSUS, encoding="utf-8")
    (tmp_path / "HOUSE_DASHBOARD.html").write_text("<p>v1</p>\n", encoding="utf-8")
    (tmp_path / "docs" / "bundle").mkdir()
    (tmp_path / "docs" / "bundle" / "sn.md").write_text("v1\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("hand-written\n", encoding="utf-8")
    _git(tmp_path, "init", "-q")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "T")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def _divergence(repo, *extra):
    return run_py([SCRIPTS / "check.py", "--staged-divergence", *extra], cwd=repo)


def test_divergence_step_reports_a_regenerated_but_unstaged_artifact(tmp_path):
    # THE POSITIVE CASE, and the one the whole ruling turns on: regenerate a
    # declared artifact, do not stage it, and the step must name it. Proved
    # three ways so a passing assertion cannot be a printed string that happens
    # to contain the path:
    #   1. the path is named and the census's OTHER rows are not;
    #   2. an undeclared dirty file (notes.md) is NOT named — the census filter
    #      is doing work, so the step is not just echoing `git diff`;
    #   3. --strict turns the same finding into exit 1, so the detection is a
    #      decision the code reached, not a message it always prints.
    repo = _divergence_repo(tmp_path)
    (repo / "HOUSE_DASHBOARD.html").write_text("<p>v2</p>\n", encoding="utf-8")
    (repo / "notes.md").write_text("edited too\n", encoding="utf-8")
    proc = _divergence(repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, (
        "the BARE detector still reports-only — the severity moved to the plan "
        "step's --strict, not to this entry point"
    )
    assert "WARN" in out and "HOUSE_DASHBOARD.html" in out, out
    assert "docs/bundle" not in out, "an unmodified declared artifact was named"
    assert "notes.md" not in out, "an UNDECLARED dirty file was reported: " + out
    # The census is READ, not copied: this repo declares a name no kit script
    # knows, so a hardcoded artifact list could not have produced that finding.
    # And the honest gap is stated in the step's own message, not only in a doc.
    assert "STAGED WHILE STALE" in out, "the message must state what it misses"
    assert "option (a)" in out, "the message must name where that case is closed"
    strict = _divergence(repo, "--strict")
    assert strict.returncode == 1, (
        "the ruled promotion path must be reachable: " + strict.stdout + strict.stderr
    )


# The census Sol's CRITICAL is driven against: a `docs/stage` row, because the
# derived stage is the artifact whose staleness the WI-498 program is named for.
_STAGE_CENSUS = """[generated]
docs/stage = stage
"""


def _stale_stage_repo(tmp_path):
    """Sol's scenario, byte for byte (ROUND-SOL-RAW finding 1): a registry edit
    STAGED, and the regenerated `docs/stage` left in the worktree."""
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "stack.ini").write_text(_STAGE_CENSUS, encoding="utf-8")
    (tmp_path / "docs" / "stage").write_text("stage: DevStg-Needs\n", encoding="utf-8")
    reg = tmp_path / "docs" / "requirements" / "system-requirements.toml"
    reg.write_text('[req.SR-001]\nstatus = "Drafted"\n', encoding="utf-8")
    _git(tmp_path, "init", "-q")
    pin_autocrlf(tmp_path)
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "T")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "base")
    # The edit that moves the derived stage, STAGED …
    reg.write_text('[req.SR-001]\nstatus = "Approved"\n', encoding="utf-8")
    _git(tmp_path, "add", "docs/requirements/system-requirements.toml")
    # … and the regeneration that answers it, NOT staged.
    (tmp_path / "docs" / "stage").write_text("stage: DevStg-Impl\n", encoding="utf-8")
    return tmp_path


def test_the_PLAN_STEP_refuses_a_regenerated_but_unstaged_derived_stage(tmp_path):
    # THE CRITICAL THIS CLOSES (OI-31's ruled promotion, taken at the WI-498
    # close). Before it, this exact tree — the one Sol drove — passed the whole
    # commit bar: `derived-stage --check` reads the WORKING TREE and sees the
    # fresh bytes, the divergence detector warned and exited 0, and the commit
    # landed the edited registry beside the OLD derived stage.
    #
    # Driven through `--run-steps`, NOT the bare `--staged-divergence` flag,
    # because the defect was never in the detector: it was in the WIRING, which
    # did not pass --strict. A test of the flag alone would have stayed green
    # through the entire defect (it did — the old positive case asserted the
    # promotion was *reachable*, never that it was *taken*).
    repo = _stale_stage_repo(tmp_path)
    proc = run_py([SCRIPTS / "check.py", "--run-steps", "staged-divergence"], cwd=repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, (
        "the bar must REFUSE a commit whose derived stage is regenerated but "
        "unstaged — this is the exact tree that used to pass: " + out
    )
    assert "FAIL" in out and "docs/stage" in out, out


def test_the_PLAN_STEP_passes_once_the_regeneration_is_staged(tmp_path):
    # The other half, so the refusal above is a decision and not a step that
    # reds on every tree: stage the regeneration — the correct workflow — and
    # the same bar goes green.
    repo = _stale_stage_repo(tmp_path)
    _git(repo, "add", "docs/stage")
    proc = run_py([SCRIPTS / "check.py", "--run-steps", "staged-divergence"], cwd=repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "FAIL" not in out, out


def test_divergence_step_is_silent_on_a_clean_tree(tmp_path):
    # The negative that keeps the step from being a warning people learn to
    # ignore: nothing modified, nothing reported.
    repo = _divergence_repo(tmp_path)
    proc = _divergence(repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "WARN" not in out, out
    assert "HOUSE_DASHBOARD.html" not in out, out


def test_divergence_step_is_silent_when_the_artifact_is_staged(tmp_path):
    # THE CASE THAT DEFINES THE STEP. The same edit as the positive test, staged
    # — which is the correct workflow — must be silent. A step that fired on
    # every regenerated artifact regardless of the index would be reporting
    # "you regenerated something", which is not a finding.
    repo = _divergence_repo(tmp_path)
    (repo / "HOUSE_DASHBOARD.html").write_text("<p>v2</p>\n", encoding="utf-8")
    (repo / "docs" / "bundle" / "sn.md").write_text("v2\n", encoding="utf-8")
    _git(repo, "add", "HOUSE_DASHBOARD.html", "docs/bundle/sn.md")
    proc = _divergence(repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "WARN" not in out, "a STAGED regeneration is the correct state: " + out


def test_divergence_step_skips_cleanly_outside_a_git_checkout(tmp_path):
    # The degradation that keeps it on the floor. The scaffold suites bootstrap
    # temp directories that are not git repos, and a detector that crashed or
    # failed there would be pulled out of the hook — the same outcome as never
    # having written it. So: no index to read => SKIP, with the reason named,
    # exit 0.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(FIXTURE_CENSUS, encoding="utf-8")
    (tmp_path / "HOUSE_DASHBOARD.html").write_text("<p>v1</p>\n", encoding="utf-8")
    proc = _divergence(tmp_path)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "SKIP" in out and "not a git checkout" in out, out
    # And a repo declaring no census skips too, rather than inventing a list.
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\n", encoding="utf-8"
    )
    bare = _divergence(tmp_path)
    assert bare.returncode == 0
    assert "no [generated] artifacts" in (bare.stdout + bare.stderr)


def test_strict_is_refused_without_the_detector(tmp_path):
    # `--strict` is the detector's promotion switch and nothing else's. Refused
    # loudly rather than ignored, so nobody reads a bare `--strict` as "make the
    # whole plan strict" and gets a silently unchanged run.
    repo = _divergence_repo(tmp_path)
    proc = run_py([SCRIPTS / "check.py", "--strict", "--list"], cwd=repo)
    assert proc.returncode != 0
    assert "--strict applies only to --staged-divergence" in (proc.stdout + proc.stderr)
