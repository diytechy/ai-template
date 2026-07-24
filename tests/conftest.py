"""Shared fixtures/helpers for the kit's self-tests.

The kit scripts must stay stdlib-only (downstream repos run them without pip);
this suite is meta-repo dev tooling, so pytest/ruff are fair game here. The
tests exercise the scripts the way a downstream user would: bootstrap a real
scaffold in a temp dir and run the actual commands.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "project-trajectory"
SCRIPTS = KIT / "scripts"

# Hermeticity: a coordinator-launched session (agent-resume.* -> agent_loop.py ->
# the agent CLI running this suite as the commit bar) inherits the launcher's
# AGENT_* routing contract (AGENT_CMD, AGENT_MODEL_MAP, AGENT_TIER_MAP, ...).
# The agent_loop tests build their own scaffolds and env, but an *ambient*
# AGENT_TIER_MAP (e.g. BUILD=strong) re-routes their subprocess loops and fails
# 8 of them — so the unattended layer could never produce a green commit bar
# (WI-118, found live 2026-07-12). Scrub the whole namespace at import, before
# any test copies os.environ; tests that need these vars set them explicitly.
for _k in [k for k in os.environ if k.startswith("AGENT_")]:
    del os.environ[_k]


# --- WI-122 + WI-281: the meta commit-bar smoke tier --------------------------
# The per-commit bar runs the fast SMOKE tier (docs/stack.ini [tiers]
# smoke = -m smoke); the FULL suite runs at slice/phase close and in CI
# (PROCESS_OPTIONS.md phased-delivery cadence). Tiering is OPT-OUT: every
# collected test is `smoke` UNLESS its module is listed below, so a NEW test is
# in the commit bar by default ("never a false green" by omission) and a test
# leaves the bar only by being named here. `smoke` and `slow` PARTITION the
# suite (every test gets exactly one) — test_smoke_tier.py guards the invariant
# and that each name below is a real test module.
#
# WI-281 re-tiered this set to a BUDGET. A smoke test answers "is it basically
# alive?", so the commit bar must run <= 60 s wall at -n auto (owner directive
# 2026-07-23). At 1378 tests the WI-122 opt-out default had inverted its own
# purpose: 1088/1378 (79%) ran per commit at ~6 min wall (measured 351 s), so
# the "smoke" bar re-ran most of the full suite every commit. The line below is
# the MECHANICAL boundary the measured module-wall ranking drew (recorded in
# docs/specs/WI-281.md): a module whose cost is dominated by driving the heavy
# scripts (gen_trajectory / trace / check* / agent_loop) or bootstrapping a
# scaffold through conftest.run_py as SUBPROCESSES runs at close + CI, not per
# commit; the in-process unit modules stay in the bar. Nothing is deleted or
# weakened — everything cut still runs at slice/phase close + CI. The runtime is
# its OWN budget item now (declared seconds + a deterministic membership ratchet
# that bites if this set shrinks the bar back toward the full suite) — see
# docs/stack.ini [smoke-budget] and tests/test_smoke_budget.py.
SLOW_MODULES = frozenset(
    {
        # WI-122: heavy end-to-end integration — full hook / gate /
        # scaffold-bootstrap runs the commit hook re-exercises live and the
        # close/CI gate re-runs wholesale, so per commit they are redundant.
        "test_pre_push_hook",  # full pre-push hook end-to-end
        "test_pre_commit_hook",  # full pre-commit hook end-to-end
        "test_bootstrap",  # full scaffold bootstraps
        "test_onboard_devsetup",  # dev-setup.sh on a bootstrapped scaffold
        "test_profile",  # scaffold-profile byte-compare
        "test_stack_profile",  # scaffold-profile byte-compare
        "test_check_perf",  # perf gate step on a scaffold
        "test_check_flows",  # design-flow gate step on a scaffold
        "test_meta_repo_hook",  # meta pre-commit hook integration
        # The v4 parallel-dispatch end-to-end modules (WI-186): each spawns real
        # dispatcher + worker subprocesses driving live git worktrees/reservations
        # — the same heavy-integration class as the hook/scaffold runs above, so
        # the commit bar drops them and the full suite + CI exercise them.
        "test_agent_loop_dispatch",  # dispatcher fan-out end-to-end
        "test_agent_loop_dualplan",  # the dual-plan round end-to-end (WI-199)
        "test_agent_loop_train",  # traincar continuation / fork / join
        "test_agent_loop_integrate",  # atomic integrator end-to-end
        "test_agent_loop_recovery",  # fault-injected crash matrix
        "test_agent_loop_migration",  # telemetry + downstream migration
        # WI-281: subprocess/scaffold-heavy modules moved to slow to hold the
        # <= 60 s commit-bar budget. Each is dominated by run_py subprocesses
        # (running gen_trajectory / trace / check* / agent_loop) or the scaffold
        # fixture's full bootstrap — the same heavy class as above, just not
        # "end-to-end" in name. Ordered by measured module-wall cost (the
        # ranking is the close deliverable in docs/specs/WI-281.md). All still
        # run at slice/phase close + CI.
        "test_gen_trajectory",  # gen_trajectory.py subprocesses (the #1 cost)
        "test_agent_loop_review",  # review-tail subprocess rounds
        "test_agent_loop",  # agent_loop.py subprocess loops
        "test_trace",  # trace.py subprocess runs
        "test_check_docs",  # check_docs on bootstrapped scaffolds
        "test_registry_checks",  # registry gates on scaffolds
        "test_check_privacy",  # privacy lint on scaffolds
        "test_agent_loop_critique",  # critique-round subprocesses
        "test_check_harness",  # check.py harness on scaffolds
        "test_trajectory",  # trajectory registry on scaffolds
        "test_components_registry",  # components gate on scaffolds
        "test_derive_gate",  # derive_gate on scaffolds
        "test_gen_okf",  # gen_okf on scaffolds
        "test_gen_trajectory_pending",  # pending-state gen_trajectory subprocesses
        "test_modules_registry",  # modules gate on scaffolds
        "test_agent_loop_worker",  # worker-leg subprocesses
        "test_ac_advisory",  # AC-advisory on scaffolds
        "test_check_stubs",  # stub gate on scaffolds
        "test_perf_budgets",  # perf-budget gen/compare on scaffolds
        "test_procurement",  # procurement gate on scaffolds
        "test_gen_release_checklist",  # release-checklist gen on scaffolds
        "test_assets",  # assets gate on scaffolds
        "test_gen_arch_map",  # gen_arch_map on scaffolds
        "test_trace_golden",  # trace.py golden subprocess runs
        "test_gate_policy",  # gate-policy on scaffolds
        "test_run_menu",  # run-menu subprocesses
        "test_agent_loop_env",  # agent_loop env-routing subprocesses
        # WI-281 rework (review A, finding 1): the run_session subprocess/shim
        # transport module. It drives real CLI subprocesses through run_session
        # (including Windows .cmd/.bat shim launchers), and it HOSTS the known
        # Windows batch-shim reds that are WI-275's open subject — one of which
        # (test_run_session_codex_reads_last_message_not_transcript) still fails
        # on a Windows checkout and would red the per-commit bar there. It runs at
        # slice/phase close + CI (where the full suite exposes those reds for
        # WI-275 to fix); holding it out of the commit bar keeps that bar green on
        # every supported OS until WI-275 lands. No test deleted or weakened — the
        # module is re-tiered whole (module-granular, like every entry here), so
        # its healthy in-process units still run at close + CI. The reviewer named
        # this the in-scope alternative to landing WI-275's fix from this WI.
        "test_session_stdin",  # run_session subprocess/shim transport (WI-275 reds)
    }
)


def smoke_tier_for(module_stem):
    """The tier a test module belongs to: 'slow' for the heavy end-to-end
    modules in SLOW_MODULES, else 'smoke'. Total by construction — one test
    maps to exactly one tier, so nothing lands outside both (the invariant the
    smoke commit bar leans on)."""
    return "slow" if module_stem in SLOW_MODULES else "smoke"


def pytest_collection_modifyitems(config, items):
    for item in items:
        stem = Path(item.nodeid.split("::", 1)[0]).stem
        item.add_marker(smoke_tier_for(stem))


def load_script(name):
    """Import a kit script as a module (scripts/ is intentionally not a package).

    scripts/ is put on sys.path first so a script that imports a sibling — e.g.
    gen_trajectory's sanctioned `import check_trajectory` — resolves in-process
    too. Run as a subprocess the sibling resolves via sys.path[0], but
    importlib.exec_module does not add scripts/ itself, so the next author writing
    an in-process test of a sibling-importing script would otherwise hit a bare
    ImportError (THREAD_52_REVIEW.md F5)."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _active_cov_datafile():
    """The measuring session's coverage datafile, or None when unmeasured.

    pytest-cov 7 removed the COV_CORE_* env contract (there is no
    COV_CORE_DATAFILE anymore), so ask the in-process coverage object pytest-cov
    drives (Coverage.current()) for its configured path. The kit pins pytest-cov
    7.x for all supported Pythons (requirements-dev.txt / WI-262), so this is the
    single measuring path — the pre-7 env-var fallback (WI-105) is gone."""
    try:
        import coverage
    except ImportError:  # plain pytest without pytest-cov: unmeasured run
        return None
    cov = coverage.Coverage.current()
    if cov is None:
        return None
    datafile = getattr(cov.config, "data_file", None)
    # Children run in temp cwds, so a rootdir-relative path must be anchored.
    return str(Path(datafile).resolve()) if datafile else None


def augment_env(env):
    """Add subprocess-coverage wiring to `env` (a dict) when pytest-cov is
    measuring the parent (see `_active_cov_datafile`); a no-op otherwise.

    Most of the suite runs the kit scripts as subprocesses, which coverage does
    not see unless each child starts it (IMPROVEMENT_PLAN.md Thread 47 phase 6).
    Shared by run_py AND any test that builds its own subprocess env
    (test_check_privacy.lint_env, test_pre_push_hook.run_hook), so coverage is
    measured *uniformly* regardless of which helper a test uses — routing only
    run_py children left the privacy suite invisible and its module reading a
    misleadingly-low %. Points the child at `.coveragerc` +
    `tests/_cov/sitecustomize.py` (which calls `coverage.process_startup()`) and
    shares pytest-cov's datafile so the parallel data lands in one place for the
    session-end combine; `.coveragerc`'s [paths] remaps the temp-scaffold script
    copies back to the source tree. NB: `tests/_cov` is prepended to PYTHONPATH,
    so it would shadow any environment-provided `sitecustomize` during a measured
    run — harmless here (none exists; gated on an active pytest-cov)."""
    datafile = _active_cov_datafile()
    if not datafile:
        return env
    env = dict(env)
    env["COVERAGE_PROCESS_START"] = str(ROOT / ".coveragerc")
    env["COVERAGE_FILE"] = datafile
    covdir = str(ROOT / "tests" / "_cov")
    env["PYTHONPATH"] = covdir + os.pathsep + env.get("PYTHONPATH", "")
    return env


def run_py(args, cwd):
    """Run `python <args>` in cwd, capturing output.

    stdin is closed (DEVNULL) so a script that *would* prompt on a TTY (e.g.
    bootstrap's agent-selection question) runs non-interactively and takes its
    default instead of blocking — the CI-safe path the tests must exercise.
    """
    # encoding="utf-8" (not text=True): the kit scripts emit UTF-8 via
    # _utf8_console, and a bare text=True decodes captured output with the
    # console codepage on Windows, mojibaking em-dashes into the goldens (WI-192).
    return subprocess.run(
        [sys.executable] + [str(a) for a in args],
        cwd=str(cwd),
        capture_output=True,
        encoding="utf-8",
        stdin=subprocess.DEVNULL,
        env=augment_env(dict(os.environ)),
    )


def seed_venv(repo):
    """Give an end-to-end dispatch fixture a real, floor-satisfying `./.venv` so
    the parallel dispatcher's WI-286 harness-floor preflight
    (`agent_dispatch._harness_floor_failures`) passes.

    That gate FAILS CLOSED when the root `.venv` is absent (REVIEW-A): a venv-less
    repo must never fall back to the ambient interpreter, whose pinned dev tools
    may be missing even at a satisfying version (a false green). So every fixture
    that drives the dispatcher (`agent_loop.py --jobs`) end-to-end needs one.
    Built with `venv.create(with_pip=False)` — a genuine ≥3.11 interpreter (this
    process's own base), created in ~0.3 s with no network/pip cost. It is
    deliberately tool-less: the fixtures stand in the real pytest bar with a fake
    worker, so only the interpreter VERSION the preflight probes must be real (a
    tool-less child's coverage `sitecustomize` import failure is a non-fatal stderr
    warning, so the version probe and the trivial `{py} -c` bar still return 0).
    Callers gitignore `.venv` (a local, per-checkout toolchain, never committed —
    a leased worktree shares the primary's by absolute path, the WI-286 design), so
    it stays out of `git add` and the porcelain the dispatcher/integrator read."""
    import venv

    venv.create(str(Path(repo) / ".venv"), with_pip=False)


@pytest.fixture
def scaffold(tmp_path):
    """A fresh repo bootstrapped from the kit (the documented quick-start)."""
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return tmp_path


# --- A minimal but complete downstream project -------------------------------
# One pure function, one traced SN->SR->LLR->TC chain, one marked smoke test.
# Used by the harness tests; written ruff-format-clean on purpose.

DEMO_SRC = '''"""Demo pure core for the kit self-test. Pure — no I/O."""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a + b
'''

DEMO_TEST_CONFTEST = '''"""Make src/ importable for the tests (no install step needed)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
'''

DEMO_TEST = '''"""Verifies SR-001/LLR-001 (TC-001)."""

import pytest
from demo import add


@pytest.mark.smoke
def test_add_sr001():
    assert add(1, 2) == 3
'''

STAKEHOLDER_NEEDS = """# Stakeholder Needs (SN-###)

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Add two numbers. | Demo. | M | add(1,2) gives 3. |
"""

SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
"""

LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Implemented
"""

TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Verified
"""


def make_minimal_project(root):
    """Fill a scaffold with the demo project + a fully traced registry chain,
    then refresh the generated arch map so the harness starts from truth."""
    (root / "src" / "demo.py").write_text(DEMO_SRC, encoding="utf-8")
    (root / "tests" / "conftest.py").write_text(DEMO_TEST_CONFTEST, encoding="utf-8")
    (root / "tests" / "test_demo.py").write_text(DEMO_TEST, encoding="utf-8")
    req = root / "docs" / "requirements"
    (req / "stakeholder-needs.md").write_text(STAKEHOLDER_NEEDS, encoding="utf-8")
    (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(TCS, encoding="utf-8")
    # A G2-complete project replaces the template's placeholder Runtime-flows
    # citations (SR-000/LLR-000) with its real ids, so the harness's
    # check_flows --no-placeholders step is satisfied.
    arch = root / "docs" / "architecture.md"
    arch.write_text(
        arch.read_text(encoding="utf-8")
        .replace("SR-000", "SR-001")
        .replace("LLR-000", "LLR-001"),
        encoding="utf-8",
    )
    # A G1-complete project's README cites its real need (the opt-out
    # need-coverage gate: every Must/Should SN is cited), replacing the -000 stub.
    readme = root / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "- **_(capability)_** — _(one line: what a user can do)_ (SN-000)",
            "- **Addition** — add two numbers (SN-001)",
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/gen_arch_map.py"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # Same "start from truth" for the OKF bundle: with real registry rows the
    # on-by-default export exists and is fresh (its hook/G3 --check passes).
    proc = run_py(["scripts/gen_okf.py"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The derived gate (docs/specs/derived-gate-model.md): this is a full G3 chain,
    # so docs/gate is regenerated from the artifact states — the scaffold shipped
    # the fresh-repo G1, and ratifying artifacts up to a G3-complete spine is what
    # advances the derived gate. Keeps the derived-gate freshness step green.
    proc = run_py(["scripts/derive_gate.py"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return root
