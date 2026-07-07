#!/usr/bin/env python3
"""The check harness — one command that runs every quality gate locally and in CI.

Stack-agnostic kit, **Python reference implementation**. This is the runnable
version of the "harness contract" in `process.md §7`: format · lint · tests ·
coverage · traceability · doc-navigability · perf-budgets · architecture-map
freshness. Wire it to your stack in ONE declared file, `docs/stack.ini`: swap
the format/lint/test commands + `src`/`tests` paths (the "EDIT FOR YOUR STACK"
block just under the imports is the identical built-in fallback), and add any
project-specific gate as a `[step:<name>]` section (see extra_steps) — so this
file stays take-wholesale across a kit re-sync. The contract is the *gates and
exit code*, not the specific tools. For a non-Python project, replace the
format/lint/test commands with your own (or drop the ones you don't have); keep
the traceability/flows/doc-navigability/perf-budgets/arch-map steps — they're
stdlib-only and stack-agnostic.

Design choices that keep it honest and CI-friendly:
    - **Never a false green.** Any failing required step makes the whole run exit
      nonzero. We print the real command output; we do not summarize it away.
    - **Missing tool != pass.** If a step's required module isn't importable, or
      its command's executable can't be found (a rewired non-Python toolchain
      that isn't installed), the step is reported SKIP(missing) and (outside
      --lenient) fails the run, so CI can't silently skip linting.
    - **One interpreter.** Tools run as `python -m ruff` / `python -m pytest` with
      the same interpreter running this script, so the launchers' venv python is
      enough — no activated venv or PATH entry required.
    - **Gate-scoped.** `--gate G2` runs only what that gate needs (e.g. G2 needs
      traceability + a runnable harness; G3 needs the full suite). Default runs all.
    - **Tiered tests.** `--tier smoke` runs only the fast subset so you can check
      every iteration; `release` runs everything including slow/hardware tests.
      Tiers map to pytest markers (`-m`); the `Tier` column in test-cases.csv is
      the registry source of truth. An **unmarked test runs in `full` and above**,
      so a forgotten marker can never drop a test from the pre-merge suite. The
      coverage threshold applies at `full`/`release` only — the smoke subset alone
      isn't expected to meet it. CI typically runs `smoke` on push, `full` on PR,
      and `release`/`all` on a release tag.
    - **Non-interactive.** No prompts; deterministic exit codes for automation.

Usage:
    python scripts/check.py [--gate G1|G2|G3|all] [--tier smoke|full|release|all]
                            [--coverage N] [--phase LIST] [--lenient] [--list]

    --gate      Which gate's checks to run. Default: the repo's **active gate**
                from the one-line `docs/gate` file (bootstrap starts it at G1;
                closing a gate = the human bumps it in a reviewed commit), else
                `all` when no gate file exists. This is what keeps a young
                project's CI green-and-honest: it enforces the bar the project
                is actually at, not the end-state bar. G3 (and all) also
                requires every Verification=Test SR to be Status=Verified
                (trace.py --require-verified).
    --tier      Which test tier to run (default: all). Mark fast critical-path
                tests @pytest.mark.smoke and expensive ones @pytest.mark.release
                (markers registered in pytest.ini); leave ordinary tests unmarked —
                they run in the full/release tiers automatically.
    --coverage  Line-coverage threshold percent (default: 80; see COVERAGE_THRESHOLD).
                Enforced for the full/release/all tiers, not smoke.
    --lenient   Treat missing tools as SKIP instead of failure (local dev only).
    --list      Print the step plan for the gate and exit; each step is tagged
                [process] (kit-owned, stdlib, identical everywhere) or [product]
                (language-specific — you wire it to your stack). See process.md
                §7 "process vs product checks".
    --run-step  Run just one named step (e.g. `format`) and exit with its
                status; a missing tool is SKIP (exit 0), a real failure exit 1.
                The pre-commit hook uses it to source its format check from the
                declared profile rather than restating the command.

The product toolchain (format/lint/test commands, src/tests paths, tier
expressions, coverage threshold) is declared ONCE in `docs/stack.ini` when it
exists — CI, the pre-commit hook, and setup.* delegate there instead of each
restating a command. Absent that file, the built-in Python-reference defaults
below apply (identical values), so a profile-less repo is unchanged.
"""

import argparse
import configparser
import importlib.util
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Resolve sibling scripts relative to *this file*, not the cwd. A repo whose
# existing directory is named "Scripts/" (NTFS case-preserving, POSIX case-
# sensitive) would break the old "scripts/trace.py" cwd-relative strings on
# Linux CI even though Windows never notices the mismatch.
_SCRIPTS = Path(__file__).resolve().parent


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII step name / path / child-process banner can't raise
    UnicodeEncodeError on a legacy Windows cp1252 console. Python 3.7+ streams
    expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# ============================ EDIT FOR YOUR STACK ============================
# PREFER `docs/stack.ini` (Thread 30): declaring the toolchain there keeps CI,
# the hook, and setup.* reading one source. The constants + built-in command
# templates below are the FALLBACK used when no profile file exists — a
# profile-less repo runs exactly these. Keep them and the scaffolded stack.ini
# in step: the reference profile declares these same values. The traceability,
# design-flows, and arch-map steps are stdlib-only and stack-agnostic (kept
# as-is either way).
SRC = "src"  # source root ([paths] src)
TESTS = "tests"  # test root ([paths] tests)
COVERAGE_THRESHOLD = 80  # line-coverage %, enforced at full/release (process.md)

# The declared product toolchain (Thread 30), read at repo root when present.
PROFILE_FILE = Path("docs/stack.ini")

# Built-in Python-reference commands, used when docs/stack.ini is absent (or for
# any section/key it doesn't override). {py}/{src}/{tests}/{coverage} expand the
# same way the profile's do (see load_profile / _expand). The scaffolded
# stack.ini declares these same strings, so a fresh scaffold and a profile-less
# repo build byte-identical plans.
BUILTIN_PRODUCT = {
    "format": "{py} -m ruff format --check {src} {tests}",
    "lint": "{py} -m ruff check {src} {tests}",
    "test": "{py} -m pytest -q",
}
BUILTIN_COVERAGE_ARGS = (
    "--cov={src} --cov-report=term-missing --cov-fail-under={coverage}"
)
# ============================================================================

# Tier -> pytest marker expression. Tiers are cumulative, and the safe default
# is opt-OUT: an unmarked test runs in `full` and `release`, so forgetting a
# marker can't silently drop a test from the pre-merge suite. `smoke` is opt-in
# (mark the fast critical paths); marking `release` opts a test out of pre-merge.
TIERS = {
    "smoke": "smoke",
    "full": "not release",
    "release": None,
    "all": None,
}

# Tiers whose pytest run must meet the coverage threshold. Smoke runs only a
# subset of the tests, so holding it to the full-suite threshold would fail the
# cheap gate for the wrong reason.
COVERAGE_TIERS = ("full", "release", "all")

# The built-in plan's own step names. A project-declared `[step:<name>]` in
# docs/stack.ini may not shadow one — that would silently append a second step
# under a kit name, not replace the kit step. Keep in sync with steps() below.
BUILTIN_STEP_NAMES = frozenset(
    {
        "format",
        "lint",
        "tests+coverage",
        "registry-integrity",
        "traceability",
        "privacy",
        "doc-navigability",
        "perf-budgets",
        "design-flows",
        "arch-map",
    }
)


def load_profile(path=PROFILE_FILE):
    """Parse the declared product toolchain (docs/stack.ini) if present, else
    None. A malformed profile fails LOUDLY — never silently ignored — so a typo
    can't quietly drop the format/lint/test gate. `interpolation=None` keeps the
    command values literal (a `%` in a command needs no escaping)."""
    if not path.exists():
        return None
    cp = configparser.ConfigParser(interpolation=None)
    try:
        cp.read_string(path.read_text(encoding="utf-8"), source=str(path))
    except configparser.Error as exc:
        sys.exit("check: {} is malformed: {}".format(path, exc))
    return cp


def _has(profile, section, option):
    """profile.has_option raises NoSectionError on a missing section; guard it."""
    return (
        profile is not None
        and profile.has_section(section)
        and profile.has_option(section, option)
    )


def _pget(profile, section, option, fallback):
    """A profile value if declared, else the built-in fallback (so a partial
    stack.ini that overrides only [paths] still uses the reference commands)."""
    return profile.get(section, option) if _has(profile, section, option) else fallback


def _expand(template, subs):
    """Split a command TEMPLATE into argv, THEN substitute {py}/{src}/{tests}/
    {coverage} per token. Splitting first keeps a Windows interpreter path
    (spaces, backslashes) intact — substituting into the raw string and then
    splitting would mangle it."""
    argv = []
    for tok in shlex.split(template):
        for key, val in subs.items():
            tok = tok.replace("{" + key + "}", val)
        argv.append(tok)
    return argv


def _requires(argv):
    """The importable modules a product command needs, derived from its argv so
    a profile author declares nothing extra: `{py} -m <mod>` needs <mod>, and a
    pytest `--cov*` flag needs the pytest-cov plugin (loaded by flag, not
    import). A non-`-m` command (npx, cargo, go) needs no import — its
    executable's absence is caught by run_step's PATH guard instead."""
    reqs = []
    if len(argv) >= 3 and argv[0] == sys.executable and argv[1] == "-m":
        reqs.append(argv[2])
    if any(tok.startswith("--cov") for tok in argv):
        reqs.append("pytest_cov")
    return tuple(dict.fromkeys(reqs))


def extra_steps(profile, subs):
    """Project-declared additional gate steps, from `docs/stack.ini`
    `[step:<name>]` sections — the home for product-specific gates (dup-code,
    license-lint, capability-integrity, …) so a project extends the plan WITHOUT
    hand-editing this take-wholesale file. A re-sync then overwrites check.py
    cleanly; the steps live in the declared profile, like the rest of the
    toolchain. Each section:

        [step:dup-code]
        command = {py} scripts/check_dupes.py {src}   # required
        gates   = G2 G3                                # optional, default G3
        layer   = product                             # optional, default product

    `{py}/{src}/{tests}/{coverage}` expand as in every other command, and the
    required-import set is auto-derived from the argv (a `{py} -m <mod>` step
    declares <mod>; any other executable's absence is caught by run_step's PATH
    guard) — the author declares nothing extra. Malformed entries fail LOUDLY,
    never silently dropped, like every other profile error."""
    if profile is None:
        return []
    out = []
    for section in profile.sections():
        if not section.startswith("step:"):
            continue
        name = section[len("step:") :].strip()
        if not name:
            sys.exit("check: docs/stack.ini has a [step:] section with an empty name")
        if name in BUILTIN_STEP_NAMES:
            sys.exit(
                "check: docs/stack.ini [step:{0}] shadows a built-in step name; "
                "rename it (it would append a second '{0}', not replace the kit "
                "step)".format(name)
            )
        if not profile.has_option(section, "command"):
            sys.exit(
                "check: docs/stack.ini [{}] needs a `command =` line".format(section)
            )
        cmd = _expand(profile.get(section, "command"), subs)
        gates = set()
        for tok in (
            profile.get(section, "gates", fallback="G3").replace(",", " ").split()
        ):
            if tok not in ("G1", "G2", "G3"):
                sys.exit(
                    "check: docs/stack.ini [{}] gates has {!r}; expected a "
                    "space/comma list of G1|G2|G3".format(section, tok)
                )
            gates.add(tok)
        if not gates:
            gates = {"G3"}
        layer = profile.get(section, "layer", fallback="product").strip() or "product"
        if layer not in ("process", "product"):
            sys.exit(
                "check: docs/stack.ini [{}] layer is {!r}; expected "
                "process|product".format(section, layer)
            )
        out.append((name, _requires(cmd), cmd, gates, layer))
    return out


# Each step: name, the third-party module(s) it needs (importable by THIS
# interpreter; () = stdlib-only), the command, the set of gates that require it,
# and its layer — "process" (kit-owned, stdlib-only, identical in every project:
# traceability / design-flows / arch-map) or "product" (language-specific, you
# wire it to your stack: format / lint / tests). The empty-vs-nonempty `requires`
# tuple already implies the split; the layer tag formalizes and surfaces it (see
# process.md §7 "process vs product checks"). Edit commands to fit your stack;
# keep the gate tags and layers.
def steps(coverage, tier, gate, phase=None, profile=None):
    # --- product commands: the declared profile (docs/stack.ini) or the built-in
    # Python-reference defaults -------------------------------------------------
    # `profile` is a parsed docs/stack.ini (or None). Every product command flows
    # through the same _expand path, so an ABSENT profile is byte-identical to
    # the historical hard-coded plan. Tools run as `{py} -m <mod>` via this
    # interpreter (the launcher's venv python is enough — no PATH/venv dance);
    # _requires derives the module a step imports from its argv, so a missing
    # tool is reported SKIP(missing) and (outside --lenient) fails rather than
    # passing. EDIT the commands in docs/stack.ini, not here.
    src = _pget(profile, "paths", "src", SRC)
    tests = _pget(profile, "paths", "tests", TESTS)
    subs = {"py": sys.executable, "src": src, "tests": tests, "coverage": str(coverage)}
    fmt_cmd = _expand(
        _pget(profile, "product", "format", BUILTIN_PRODUCT["format"]), subs
    )
    lint_cmd = _expand(_pget(profile, "product", "lint", BUILTIN_PRODUCT["lint"]), subs)
    test_cmd = _expand(_pget(profile, "product", "test", BUILTIN_PRODUCT["test"]), subs)
    if tier in COVERAGE_TIERS:
        test_cmd += _expand(
            _pget(profile, "coverage", "args", BUILTIN_COVERAGE_ARGS), subs
        )
    # Tier selector appended to the test command: the profile's [tiers] value
    # (a stack-native expression), else the built-in marker map. Empty = run all.
    if _has(profile, "tiers", tier):
        test_cmd += _expand(profile.get("tiers", tier), subs)
    else:
        marker = TIERS.get(tier)
        if marker:
            test_cmd += ["-m", marker]
    # The traceability step only runs at G2/G3, where placeholder rows must be
    # gone, so --no-placeholders is always on here (a fresh scaffold is exempt
    # only because nothing past G1 runs against it). --html also regenerates the
    # scalable full-graph view (a gitignored composite artifact) every run.
    trace_cmd = [
        sys.executable,
        str(_SCRIPTS / "trace.py"),
        "--strict",
        "--no-placeholders",
        "--html",
    ]
    if gate in ("G3", "all"):  # G3 criterion: test-verifiable SRs are Verified
        trace_cmd.append("--require-verified")
        trace_cmd.append("--strict-schema")  # G3: required fields + valid enums
        if phase:  # phased delivery: close G3 for this phase only (process.md §4)
            trace_cmd += ["--phase", phase]
    # Arch-map mode from the profile ([arch-map] mode = symbols|files): a
    # non-Python stack declares `files` for the stack-neutral fallback instead
    # of hand-editing this take-wholesale file (the downstream delta WI-1.25
    # absorbed). Invalid values fail loudly, like every other profile error.
    arch_mode = _pget(profile, "arch-map", "mode", "symbols")
    if arch_mode not in ("symbols", "files"):
        sys.exit(
            "check: docs/stack.ini [arch-map] mode is {!r}; expected "
            "symbols|files".format(arch_mode)
        )
    arch_cmd = [
        sys.executable,
        str(_SCRIPTS / "gen_arch_map.py"),
        "--check",
        "--strict-parse",
        "--src",
        src,
        "--doc",
        "docs/architecture.md",
    ]
    if arch_mode == "files":
        arch_cmd += ["--mode", "files"]
        # Optional: whitespace-separated comment tokens whose first line is a
        # file's summary (gen_arch_map's default already covers # // --).
        for tok in _pget(profile, "arch-map", "comment-prefixes", "").split():
            arch_cmd += ["--comment-prefix", tok]
    return [
        # --- product checks: language-specific, declared in docs/stack.ini -----
        ("format", _requires(fmt_cmd), fmt_cmd, {"G3"}, "product"),
        ("lint", _requires(lint_cmd), lint_cmd, {"G3"}, "product"),
        ("tests+coverage", _requires(test_cmd), test_cmd, {"G3"}, "product"),
        # --- project-declared product steps: docs/stack.ini [step:<name>] ------
        # Product-specific gates a project adds (dup-code, license-lint, …) live
        # in the declared profile, NOT hand-edited into this take-wholesale file
        # (see extra_steps above). They slot in here with the other product steps.
        *extra_steps(profile, subs),
        # Optional PRODUCT-layer detector, not wired into the required floor:
        # `scripts/check_stubs.py` is the Python-reference tripwire for the G3
        # no-stub / substance criterion (process.md §4). It is warn-first and
        # language-specific (a stub's shape differs per stack), so — like the perf
        # *meters* — a project opts in. Prefer a docs/stack.ini `[step:no-stubs]`
        # section (survives re-sync) over hand-editing a step in here, e.g.:
        #   [step:no-stubs]
        #   command = {py} scripts/check_stubs.py --strict
        # (drop --strict to warn instead of fail). A non-Python stack swaps or
        # drops it. Left out of the default plan to keep the floor honest.
        # --- process checks: kit-owned, stdlib-only, identical everywhere -----
        # Registry integrity floor at G1: the traceability step below already
        # fails on integrity findings via --strict, but it only runs from G2 —
        # so a structurally broken registry CSV (unquoted commas misaligning
        # every later column) or a duplicated/malformed id would pass the G1
        # gate and hide until G2/G3. This runs trace.py's always-valid subset
        # (duplicate/malformed ids + CSV column structure) at the first gate;
        # the pre-commit hook runs the same command on every commit. Listed
        # before traceability so at --gate all the fuller report.md wins.
        (
            "registry-integrity",
            (),
            [sys.executable, str(_SCRIPTS / "trace.py"), "--strict-integrity"],
            {"G1"},
            "process",
        ),
        ("traceability", (), trace_cmd, {"G2", "G3"}, "process"),
        # Secrets + privacy sweep (process-options.md "Commit identity &
        # privacy"): every tracked text file is swept for the always-on
        # secrets floor (key/token shapes, all repos) plus — when
        # docs/privacy-check is `true` — the privacy/identity-leak classes,
        # catching what slipped in before the gate was enabled or past
        # --no-verify. Runs at every gate (a leak is wrong at any stage); the
        # script exits 0 fast only when both layers are off (privacy-check off +
        # docs/secrets-scan off).
        (
            "privacy",
            (),
            [sys.executable, str(_SCRIPTS / "check_privacy.py"), "--repo"],
            {"G1", "G2", "G3"},
            "process",
        ),
        # Doc navigability (process.md §3 "Reviewability"): broken intra-repo
        # links fail; orphans warn; the README vision tag + SN inventory are
        # checked. Runs from G1 on (docs exist early). --stale adds the
        # git-gated, warn-only "lying map" heuristic (degrades to a clean skip
        # off-git). The generated, gitignored trace report is dropped.
        (
            "doc-navigability",
            (),
            [
                sys.executable,
                str(_SCRIPTS / "check_docs.py"),
                "--ignore",
                "docs/test/report.md",
                "--stale",
            ],
            {"G1", "G2", "G3"},
            "process",
        ),
        # Performance budgets (process.md §9): the kit-owned *comparator* (stdlib,
        # metric-agnostic) checks the project's measured perf-metrics.json against
        # the budgets registry + committed baseline. Tier-threaded so size-class
        # budgets gate at full and noisy runtime ones warn at release; absent
        # metrics/budgets skip. The *measurement* that emits perf-metrics.json is
        # a PRODUCT step you wire to your stack (see EDIT FOR YOUR STACK above).
        (
            "perf-budgets",
            (),
            [sys.executable, str(_SCRIPTS / "check_perf.py"), "--tier", tier],
            {"G3"},
            "process",
        ),
        # Authored runtime-flow diagrams (process.md §3 "Design-time runtime
        # flows"): required from G2 on, so reviewers verify behavior from the
        # diagrams, not from registry rows.
        (
            "design-flows",
            (),
            [sys.executable, str(_SCRIPTS / "check_flows.py"), "--no-placeholders"],
            {"G2", "G3"},
            "process",
        ),
        # Add `--doc AGENTS.md` / `--doc CLAUDE.md` to route the map there too, and
        # `--flow <entry>` to also check the generated high-level flow.
        # The mode (symbols vs the stack-neutral files fallback) comes from
        # docs/stack.ini [arch-map] — see arch_cmd above.
        (
            "arch-map",
            (),
            arch_cmd,
            {"G3"},
            "process",
        ),
    ]


GATES = ["G1", "G2", "G3", "all"]

# The machine-readable active gate (process.md §7). One line, e.g. "G1".
GATE_FILE = Path("docs/gate")


def resolve_gate(explicit):
    """The gate to run: an explicit --gate wins; else the docs/gate file (the
    project's recorded active gate); else 'all' (a repo without the file gets
    the full bar, never a silently weaker one). The file is parsed by the
    declared-policy rule every reader shares (hooks, check_privacy.py,
    agent_loop.py): the first non-empty, non-comment line."""
    if explicit:
        return explicit
    if GATE_FILE.exists():
        val = ""
        for ln in GATE_FILE.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                val = ln
                break
        if val not in GATES:
            sys.exit(
                "check: docs/gate contains {!r}; expected one of {}".format(
                    val, "|".join(GATES)
                )
            )
        return val
    return "all"


# coverage.py orchestration vars that must NOT leak into the steps this harness
# spawns: the `tests+coverage` step runs the project's own `pytest --cov`, and if
# a *parent* process is itself running under coverage (a CI that wraps the whole
# run, or the kit's own meta-suite measuring check.py), the inherited COVERAGE_*
# / COV_CORE_* would redirect this project's coverage data file and config,
# corrupting the authoritative run. Stripping them makes check.py's coverage step
# self-contained. A no-op when no such parent exists.
_COVERAGE_ENV_VARS = (
    "COVERAGE_PROCESS_START",
    "COVERAGE_FILE",
    "COV_CORE_SOURCE",
    "COV_CORE_CONFIG",
    "COV_CORE_DATAFILE",
    "COV_CORE_BRANCH",
    "COV_CORE_CONTEXT",
)


def _step_env():
    """The environment for a spawned step, minus any ambient coverage-orchestration
    vars (see _COVERAGE_ENV_VARS) so the project's own coverage run is authoritative."""
    env = dict(os.environ)
    for var in _COVERAGE_ENV_VARS:
        env.pop(var, None)
    return env


def run_step(name, requires, cmd, lenient):
    """Run one step. Returns (status, detail) where status in PASS/FAIL/SKIP."""
    missing = [m for m in requires if importlib.util.find_spec(m) is None]
    if missing:
        status = "SKIP" if lenient else "FAIL"
        return status, "module(s) {} not importable by {} — run scripts/setup".format(
            ", ".join(missing), sys.executable
        )
    # Same guarantee for the command itself: a rewired step ("swap the
    # format/lint/test commands for your toolchain") names an executable this
    # interpreter knows nothing about, so the module guard above can't see its
    # absence. Resolve it the way the OS would (a path, or PATH lookup —
    # shutil.which honors PATHEXT on Windows) and fail by design instead of
    # crashing with a raw FileNotFoundError.
    exe = cmd[0] if Path(cmd[0]).exists() else shutil.which(cmd[0])
    if not exe:
        status = "SKIP" if lenient else "FAIL"
        return status, (
            "command {!r} not found — wire your stack's toolchain "
            "(see the EDIT FOR YOUR STACK block)".format(cmd[0])
        )
    start = time.time()
    print("\n=== {} : {} ===".format(name, " ".join(cmd)), flush=True)
    # Run the RESOLVED path, not the bare name: Windows CreateProcess applies
    # no PATHEXT, so a bare `npx`/`eslint` that shutil.which found as npx.cmd
    # would still crash the exec with WinError 2 — resolving for the guard
    # but running unresolved was exactly the crash this block claims to
    # avoid (downstream field report, WI-1.25).
    proc = subprocess.run([exe] + list(cmd[1:]), env=_step_env())
    secs = time.time() - start
    if proc.returncode == 0:
        return "PASS", "{:.1f}s".format(secs)
    return "FAIL", "exit {} ({:.1f}s)".format(proc.returncode, secs)


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--gate",
        choices=GATES,
        default=None,
        help="gate to run (default: the active gate in docs/gate, else all)",
    )
    ap.add_argument("--tier", choices=list(TIERS), default="all")
    ap.add_argument(
        "--coverage",
        type=int,
        default=None,
        help="line-coverage threshold %% (default: docs/stack.ini [coverage] "
        "threshold, else {})".format(COVERAGE_THRESHOLD),
    )
    ap.add_argument(
        "--phase",
        default=None,
        help="delivery phase(s) in scope, e.g. v1 or v1,v2 — scopes the G3 "
        "Verified criterion to that phase (process.md §4 'Phased delivery')",
    )
    ap.add_argument(
        "--lenient",
        action="store_true",
        help="treat missing tools as SKIP (local dev only)",
    )
    ap.add_argument(
        "--list",
        action="store_true",
        help="print the plan (with [process]/[product] layer tags) and exit",
    )
    ap.add_argument(
        "--run-step",
        metavar="NAME",
        default=None,
        help="run just the named step (e.g. 'format') and exit with its status; "
        "a missing tool is SKIP (exit 0), a real failure exits 1 (the pre-commit "
        "hook uses this to source its format check from docs/stack.ini)",
    )
    args = ap.parse_args()
    gate = resolve_gate(args.gate)
    profile = load_profile()

    # --coverage wins; else the profile's declared threshold; else the built-in.
    coverage = args.coverage
    if coverage is None:
        coverage = COVERAGE_THRESHOLD
        if _has(profile, "coverage", "threshold"):
            try:
                coverage = int(profile.get("coverage", "threshold").strip())
            except ValueError:
                sys.exit(
                    "check: docs/stack.ini [coverage] threshold must be an integer"
                )

    # Run one named step and exit (the hook's format delegation). Search the
    # unfiltered plan so a gate-scoped step (format is G3-only) is still found,
    # and be lenient about a missing tool so a not-yet-set-up repo can commit —
    # a real failure still exits nonzero.
    if args.run_step:
        all_steps = steps(coverage, args.tier, "all", args.phase, profile)
        match = [s for s in all_steps if s[0] == args.run_step]
        if not match:
            sys.exit("check: no step named {!r}".format(args.run_step))
        name, requires, cmd, _gates, _layer = match[0]
        status, detail = run_step(name, requires, cmd, lenient=True)
        print("  {:5} {:16} {}".format(status, name, detail))
        sys.exit(1 if status == "FAIL" else 0)

    plan = [
        s
        for s in steps(coverage, args.tier, gate, args.phase, profile)
        if gate == "all" or gate in s[3]
    ]

    if args.list:
        print("Plan for gate {} (tier {}):".format(gate, args.tier))
        for name, _requires, cmd, gates, layer in plan:
            print(
                "  - {:16} [{:7}] [{}]  {}".format(
                    name, layer, ",".join(sorted(gates)), " ".join(cmd)
                )
            )
        return

    if not plan:
        print("No checks defined for gate {}.".format(gate))
        return

    results = []
    for name, requires, cmd, _gates, _layer in plan:
        status, detail = run_step(name, requires, cmd, args.lenient)
        results.append((name, status, detail))

    print("\n" + "=" * 56)
    print("Check summary (gate {}, tier {}):".format(gate, args.tier))
    for name, status, detail in results:
        print("  {:5} {:16} {}".format(status, name, detail))
    failed = [r for r in results if r[1] == "FAIL"]
    print("=" * 56)
    if failed:
        print("RESULT: FAIL ({} step(s) failed)".format(len(failed)))
        sys.exit(1)
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
