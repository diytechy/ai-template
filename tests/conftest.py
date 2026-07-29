"""Shared fixtures/helpers for the kit's self-tests.

The kit scripts must stay stdlib-only (downstream repos run them without pip);
this suite is meta-repo dev tooling, so pytest/ruff are fair game here. The
tests exercise the scripts the way a downstream user would: bootstrap a real
scaffold in a temp dir and run the actual commands.
"""

import collections
import importlib.util
import os
import shutil
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
        # Heavy end-to-end session/integrator modules — real subprocesses
        # driving live git repos, the same heavy-integration class as the
        # hook/scaffold runs above. (The v4 parallel-dispatch e2e modules that
        # anchored this group retired with the dispatcher at
        # concurrency-restructure Phase 5.)
        "test_dual_plan_round",  # the dual-plan round end-to-end (WI-199)
        "test_integrate",  # local integrator: real git repos + a real check.py bar
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
        # The toolchain prereq, re-tiered on the SAME precedent as test_session_stdin
        # directly above: it is DESIGNED to red on a below-floor checkout, so leaving
        # it in the bar would make the commit bar unpassable on such a machine — a
        # developer could then never commit the very fix that installs the floor.
        # Nothing is weakened: the `pytest_sessionstart` banner still fires on EVERY
        # run including `-m smoke`, so the commit bar keeps the loud warning and
        # loses only the hard stop; the hard failure lands at slice/phase close and
        # in CI, which is where a gate result is claimed.
        "test_prereq_toolchain",  # designed to red below the declared Python floor
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


# --- The interpreter-floor preflight -----------------------------------------
# The kit declares ONE Python floor (`agent_common.MIN_PYTHON`) and dev-setup
# provisions ./.venv to satisfy it. Run this suite under a BELOW-floor
# interpreter and dozens of tests fail deep inside machinery that is working
# exactly as designed (dev-setup's PATH probe finds no 3.11+ to offer, and the
# toolchain-dependent fixtures build from *this* process's base). Those
# reds read like branch defects but are purely environmental — measured
# 2026-07-25 on a CLT-Python 3.9.6 .venv: 49 failures, a byte-identical set on a
# clean tree. The guards below turn that into one loud, correct diagnosis plus
# honest skips. The floor itself is READ from the source of truth, never
# restated here, so a floor bump flows through untouched.


def declared_python_floor():
    """The kit's declared interpreter floor as a `(major, minor)` tuple, read
    from `agent_common.MIN_PYTHON` — the same constant the dispatcher preflight
    and dev-setup enforce."""
    return tuple(load_script("agent_common").MIN_PYTHON)


def floor_shortfall(exe=None):
    """A one-line "running X, floor is Y" string when `exe` (default: this
    process) is below the declared floor, else None.

    The single predicate every floor guard and the prereq test share, so they can
    never disagree about what "below floor" means. Probing is delegated to
    `agent_common.interpreter_version`, which reads `sys.version_info` for this
    process and RUNS any other path — so a stale .venv reports its own version.
    Returns None (not a shortfall) when a foreign interpreter cannot be run at
    all; that shape is the dispatcher preflight's to report, not this one's."""
    floor = declared_python_floor()
    ver = load_script("agent_common").interpreter_version(exe)
    if ver is None or ver >= floor:
        return None
    return "running Python {} but the kit's declared floor is {}+".format(
        ".".join(str(p) for p in ver), ".".join(str(p) for p in floor)
    )


def skip_below_floor(what):
    """`pytest.skip` with the shortfall and the remedy when this interpreter
    cannot satisfy the declared floor; a no-op otherwise.

    For tests whose PRECONDITION is a floor-satisfying toolchain — not tests that
    merely happen to fail without one. Skipping is the honest verdict there: the
    behaviour under test genuinely cannot be exercised, so a red would be
    reporting the environment as a defect. `test_prereq_toolchain.py` fails hard
    in the same run, so a below-floor session can never read as green."""
    short = floor_shortfall()
    if short:
        pytest.skip(
            "{} — {}. Run `scripts/dev-setup --install` to provision a "
            "floor-satisfying ./.venv (see test_prereq_toolchain.py).".format(
                what, short
            )
        )


# --- WI-326: the environment gates ------------------------------------------
# Preconditions that are not the BRANCH's business but silently change what the
# suite RUNS. Measured 2026-07-26 on Windows (the account is in docs/log.md):
# the same tree, the same commit, run twice — 1540 passed / 54 skipped without
# `Git\bin` on PATH, 1587 passed / 7 skipped with it. Forty-seven tests were
# never asked, 26 of them the two hook suites guarding the commit floor, and BOTH
# printed a green. That is SN-008's dishonest-green shape one level up: not a
# skipped check, but a skipped check-of-the-check.
#
# Declared ONCE here because the skip guards and the gate must read the same
# fact. A gate names its probe, what its absence costs, and whether a run
# missing it may still be called a gate result. Tests skip through the helpers
# below rather than re-probing, so the number the terminal summary reports and
# the reason an individual test skipped cannot drift into two figures — which is
# exactly how 47 went uncounted: `shutil.which("sh")` was copied inline into
# four modules and no one owned the total.
#
# Deliberately NOT done, per the row: auto-prepending the directory to PATH. A
# harness that silently repairs its own environment hides the identical fact one
# layer down — the same standing rule that forbids reaching for a
# `docs/dupes-allow` sanction to green a step.
#
# The declaration lives here rather than in docs/stack.ini (where [smoke-budget]
# sits) because only this suite reads it: stack.ini is what the KIT SCRIPTS
# parse, and tests/ is not shipped downstream.

EnvGate = collections.namedtuple("EnvGate", "name required probe cost remedy")

ENV_GATE_SKIP_PREFIX = "environment gate"


def unreachable_posix_shell():
    """A directory holding an `sh` that EXISTS on this machine but is not on
    PATH, or None (including whenever `sh` is already reachable).

    Git for Windows installs `sh.exe` under both `Git\\bin` and `Git\\usr\\bin`
    but puts only `Git\\cmd` on PATH, so the shell is *installed and
    unreachable* — the default Windows developer state, not an exotic one.
    Naming the directory turns an unactionable "no POSIX shell" into a one-line
    remedy the reader can paste."""
    if shutil.which("sh"):
        return None
    bases = [os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")]
    for base in [b for b in bases if b]:
        for sub in ("Git\\bin", "Git\\usr\\bin"):
            candidate = Path(base) / sub
            if (candidate / "sh.exe").is_file():
                return candidate
    return None


def _posix_shell_remedy():
    found = unreachable_posix_shell()
    if found:
        return (
            "put {} on PATH — sh.exe is already installed there; Git for "
            "Windows puts only Git\\cmd on PATH".format(found)
        )
    return "install a POSIX shell (Git for Windows ships one) and put it on PATH"


ENV_GATES = (
    EnvGate(
        name="posix-shell",
        required=True,
        probe=lambda: shutil.which("sh") is not None,
        cost=(
            "every shell-driven test SKIPS — the pre-commit (8) and pre-push (18) "
            "hook suites that guard the commit floor itself, the dev-setup "
            "install path, and the commit-msg trailer hook"
        ),
        remedy=_posix_shell_remedy,
    ),
    EnvGate(
        name="git",
        required=True,
        probe=lambda: shutil.which("git") is not None,
        cost="every test that drives a real repository SKIPS",
        remedy=lambda: "install git and put it on PATH",
    ),
)


# A test that needs to observe the SATISFIED half of this machinery cannot get
# there by running on a provisioned machine — that inherits the runner's
# environment, which is the thing under test. `KIT_ENV_GATES_SATISFIED` lets a
# child process construct that half, the same way an empty PATH constructs the
# unsatisfied one. Deliberately NOT an opt-out: it forces gates to read
# satisfied, so setting it in anger would make the suite claim MORE ran, not
# less, and `test_prereq_toolchain` still fails on the real probes.
ENV_GATES_SATISFIED_VAR = "KIT_ENV_GATES_SATISFIED"


def env_gate_shortfalls(names=None):
    """The declared gates this machine does NOT satisfy, in declaration order.

    `names` restricts the answer to the gates a caller depends on; None means
    all of them. Returns EnvGate records, so a caller can report the cost and
    the remedy without re-deriving either."""
    if os.environ.get(ENV_GATES_SATISFIED_VAR):
        return []
    return [
        g for g in ENV_GATES if (names is None or g.name in names) and not g.probe()
    ]


def env_gate_skip_reason(missing):
    """The one skip-reason string, shared by both skip forms so the terminal
    summary can count them with a single substring test."""
    remedies = list(dict.fromkeys(g.remedy() for g in missing))
    return "{} unsatisfied: {} — {}".format(
        ENV_GATE_SKIP_PREFIX, ", ".join(g.name for g in missing), "; ".join(remedies)
    )


def skip_without_env_gates(*names):
    """`pytest.skip` when any NAMED declared gate is unsatisfied; a no-op
    otherwise. The runtime form, for a guard inside a test or fixture."""
    missing = env_gate_shortfalls(names)
    if missing:
        pytest.skip(env_gate_skip_reason(missing))


def env_gate_skipif(*names):
    """The module-level `pytest.mark.skipif` form of `skip_without_env_gates`,
    carrying the identical reason string so both forms are counted alike."""
    missing = env_gate_shortfalls(names)
    return pytest.mark.skipif(
        bool(missing), reason=env_gate_skip_reason(missing) if missing else ""
    )


def env_gate_banner():
    """The stderr announcement, or None when every declared gate is satisfied.

    Predicted from the probes, so it lands BEFORE the first test rather than
    behind a scrollback of skips — the same belt-and-braces role the toolchain
    banner plays for the interpreter floor."""
    missing = env_gate_shortfalls()
    if not missing:
        return None
    lines = [
        "",
        "!! ENVIRONMENT GATE: {} of {} declared gates unsatisfied on this "
        "machine.".format(len(missing), len(ENV_GATES)),
    ]
    for gate in missing:
        lines.append(
            "     {}{}: {}".format(
                gate.name, " (REQUIRED)" if gate.required else "", gate.cost
            )
        )
        lines.append("       remedy: {}".format(gate.remedy()))
    lines.append(
        "   Those tests will SKIP, so this run is PARTIAL — a green here is not"
    )
    lines.append(
        "   a gate result. test_prereq_toolchain.py FAILS on a required gate at"
    )
    lines.append("   slice close and in CI, where a gate result is actually claimed.")
    lines.append("")
    return "\n".join(lines)


def env_gated_skip_count(terminalreporter):
    """How many tests skipped THIS run because a declared environment gate was
    unsatisfied — the MEASURED number, as opposed to the banner's prediction.

    It reads the reason string the shared helpers emit, so a hand-rolled inline
    `shutil.which` skip elsewhere would be invisible here — which is safe only
    because `test_env_gates` bans one over the AST. The first version of that
    guard matched two literal reason strings and let a fresh probe through, so
    "invisible BY DESIGN" was, for one commit, just invisible.

    The `(path, lineno, reason)` longrepr shape is what pytest actually hands
    back for a skip, and it SURVIVES xdist: measured under `-n 2` with the gates
    closed, both skip forms round-trip the 3-tuple intact and the count read 51.
    The defensive non-tuple branch stays for plugins that wrap it, but the
    earlier claim that "xdist hands back a bare string" was wrong — it was
    reasoned about rather than measured."""
    counted = 0
    for report in terminalreporter.stats.get("skipped", []):
        longrepr = getattr(report, "longrepr", None)
        reason = (
            longrepr[2] if isinstance(longrepr, tuple) and len(longrepr) == 3 else ""
        )
        if ENV_GATE_SKIP_PREFIX in str(reason):
            counted += 1
    return counted


def pytest_sessionstart(session):
    """Announce a below-floor interpreter and any unsatisfied environment gate on
    stderr before a single test runs, on the xdist CONTROLLER only (workers set
    `workerinput`, and one banner per worker would be noise). Belt-and-braces for
    the prereq test: under `-q` a failure summary can scroll far behind ~50
    skips, and this lands first."""
    if hasattr(session.config, "workerinput"):
        return
    short = floor_shortfall()
    if short:
        print(
            "\n!! TOOLCHAIN PREREQ: {} — the toolchain-dependent tests will SKIP "
            "and test_prereq_toolchain.py will FAIL. This is the environment, "
            "not the branch. Remedy: scripts/dev-setup --install\n".format(short),
            file=sys.stderr,
        )
    banner = env_gate_banner()
    if banner:
        print(banner, file=sys.stderr)


def pytest_terminal_summary(terminalreporter):
    """Report the MEASURED environment-gated skip count once the run is over.

    The session-start banner predicts from the probes; this states what actually
    happened. It is the line whose absence let two sessions record `1579 passed,
    7 skipped` and `1540 passed, 54 skipped` as comparable greens — the count was
    always one `-rs` flag away, and nobody passes `-rs`."""
    if hasattr(terminalreporter.config, "workerinput"):
        return
    counted = env_gated_skip_count(terminalreporter)
    missing = env_gate_shortfalls()
    if not counted and not missing:
        return
    terminalreporter.write_line("")
    terminalreporter.write_line(
        "ENVIRONMENT-GATED SKIPS: {} test(s) did not RUN because {} of {} "
        "declared gates are unsatisfied ({}).".format(
            counted,
            len(missing),
            len(ENV_GATES),
            ", ".join(g.name for g in missing) or "none",
        ),
        yellow=True,
        bold=True,
    )
    for gate in missing:
        terminalreporter.write_line(
            "  remedy ({}): {}".format(gate.name, gate.remedy())
        )
    terminalreporter.write_line(
        "  A pass total measured here is NOT comparable with one measured on a "
        "fully-gated machine.",
        yellow=True,
    )


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


# (seed_venv — the end-to-end dispatch fixtures' floor-satisfying ./.venv
# builder — retired with the dispatcher's WI-286 harness-floor preflight at
# concurrency-restructure Phase 5; no surviving fixture drives that gate.)


# --- The agent_loop work-item registry fixture builder -----------------------
# ONE implementation for the six agent_loop suites (worker/dispatch/train/
# integrate/recovery/migration), each of which used to carry a near-verbatim
# copy of the header constant, the row maker, and the CSV writer. The three
# real variants are parameters, not copies:
#   - `sr`: each suite tags its rows with the SR it verifies (SR-060..SR-065);
#   - `columns`: the registry SHAPES the suites exercise are prefixes of one
#     canonical column list — worker's 9 (a registry predating SafetyClass),
#     the four dispatcher-era suites' 10, and integrate's 11 (+BlockRef, the
#     column the integrator adopts). Slicing one list is what makes them
#     provably prefixes rather than three hand-kept constants.
# Each suite keeps its own module-level `HEADER`/`_wi_row`/`_write_registry`
# name bound to a partial of these, so its ~250 call sites read unchanged.

WI_REGISTRY_COLUMNS = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "BuildTier",
    "SafetyClass",
    "BlockRef",
]


def wi_registry_header(columns=10):
    """The first `columns` work-item registry columns, as a fresh list."""
    return list(WI_REGISTRY_COLUMNS[:columns])


def wi_row(wid, preds="", safety="ordinary", status="queued", sr="SR-061", columns=10):
    """One work-item row, `columns` wide, as a fresh mutable list (callers
    patch cells in place — e.g. integrate's `_wi_row_srrefs`)."""
    return [
        wid,
        "Work " + wid,
        "ws",
        sr,
        preds,
        status,
        "shipped" if status == "done" else "",
        "docs/specs/thing.md",
        "medium",
        safety,
        "",
    ][:columns]


def write_wi_registry(repo, rows, header=None):
    """Write the fixture WI registry in its one home, `docs/work/` spec files
    (Phase 5 — the CSV home retired). The signature is unchanged: `rows` are
    header-ordered cell lists exactly as the CSV era wrote them, mapped here
    through the format's single writer (wi_convert), so the ~250 call sites
    across the session-engine suites read as before. Re-writing an id
    replaces its spec (fixtures re-seed freely); the file for a previous
    status is removed first so status = directory stays single-homed."""
    wc = load_script("wi_convert")
    cols = wi_registry_header() if header is None else header
    work = Path(repo) / "docs" / "work"
    work.mkdir(parents=True, exist_ok=True)
    for n, cells in enumerate(rows, 1):
        row = {c: "" for c in wc.COLUMNS}
        row.update({col: (cell or "") for col, cell in zip(cols, cells)})
        row["Status"] = row.get("Status") or "queued"
        if row["Status"] == "done" and not row.get("Deliverable"):
            row["Deliverable"] = "shipped"
        wid = row["WI-ID"]
        for old in work.glob("*/{}-*.md".format(wid)):
            old.unlink()
        for old in work.glob("active/*/{}-*.md".format(wid)):
            old.unlink()
        wc.write_spec_file(work, row, order=n)


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
