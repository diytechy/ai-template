#!/usr/bin/env python3
"""The check harness — one command that runs every quality gate locally and in CI.

Stack-agnostic kit, **Python reference implementation**. This is the runnable
version of the "harness contract" in `process.md §7`: format · lint · tests ·
coverage · derived-gate freshness · traceability · doc-navigability · perf-budgets
· architecture-map freshness. Wire it to your stack in ONE declared file, `docs/stack.ini`: swap
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
      --lenient) fails the run, so CI can't silently skip linting. On the hook
      path, where the skip is deliberately allowed (`--run-step`/`--run-steps`
      run lenient so a not-yet-set-up repo can commit), a SKIPped PRODUCT-layer
      step — one whose command this repo itself declared in docs/stack.ini —
      also raises `missing_tool_banner`, because a dim SKIP line repeated on
      every commit of a branch is how two of this kit's four late defects hid.
    - **One interpreter.** Tools run as `python -m ruff` / `python -m pytest` with
      the same interpreter running this script, so the launchers' venv python is
      enough — no activated venv or PATH entry required.
    - **Gate-scoped.** `--gate DevStg-Tests` runs only what that gate needs (e.g. DevStg-Tests needs
      traceability + a runnable harness; DevStg-Impl needs the full suite). Default runs all.
    - **Tiered tests.** `--tier smoke` runs only the fast subset so you can check
      every iteration; `release` runs everything including slow/hardware tests.
      Tiers map to pytest markers (`-m`); the `Tier` field in test-cases.toml is
      the registry source of truth. An **unmarked test runs in `full` and above**,
      so a forgotten marker can never drop a test from the pre-merge suite. The
      coverage threshold applies at `full`/`release` only — the smoke subset alone
      isn't expected to meet it. CI typically runs `smoke` on push, `full` on PR,
      and `release`/`all` on a release tag.
    - **Lane-aware freshness.** The generated-artifact freshness gates are the
      TRUNK lane's (concurrency-restructure.md §5.2). On a claimed work branch —
      one with a `docs/work/active/<branch>/` spec directory — each is reported
      SKIP with its reason instead of running. Fail-closed: off git, on a
      detached HEAD, or unclaimed, the full bar applies. See
      `_TRUNK_FRESHNESS_STEPS`. `--trunk-lane` forces them ON: the station
      refresh (`integrate.py refresh`) regenerates on the branch and then bars
      it, and that tree IS the tree that becomes trunk, so the branch stands in
      the trunk lane for exactly that one run.
    - **Non-interactive.** No prompts; deterministic exit codes for automation.

Usage:
    python scripts/check.py [--gate DevStg-Reqs|DevStg-Tests|DevStg-Impl|all] [--tier smoke|full|release|all]
                            [--coverage N] [--phase LIST] [--lenient] [--list]
                            [--jobs N] [--run-step NAME] [--run-steps A,B,...]

    --gate      Which gate's checks to run. Default: the repo's **derived gate**
                from `docs/gate` — the gate it must next PASS (a fresh scaffold
                derives DevStg-Reqs), computed by derive_gate.py, never hand-set;
                closing a gate = ratifying artifacts in a reviewed commit +
                regenerating. Else `all` when no gate file exists. This keeps a young
                project's CI green-and-honest: it enforces the bar the project
                is working toward, not the end-state bar. DevStg-Impl (and all) also
                requires every Verification=Test SR to be Status=Approved
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
                An explicit --gate builds the step AT that gate (else "all").
    --run-steps Run several named steps concurrently with --run-step's lenient
                semantics, reporting EVERY step's result (exit 1 if any FAILs) —
                the pre-commit hook's batched freshness/integrity floor, one
                interpreter spawn instead of a chain that stops at the first
                stale artifact.
    --jobs      Run the plan's steps on N concurrent workers (0 = one per
                step; default 1 = sequential, streamed output, byte-identical
                to the historical behavior). Parallel-safe by construction:
                steps are read-only or write disjoint artifacts, and the two
                trace.py steps that share docs/test/report.md run chained in
                one lane. Output is captured per step and printed whole, so
                nothing interleaves.

The product toolchain (format/lint/test commands, src/tests paths, tier
expressions, coverage threshold) is declared ONCE in `docs/stack.ini` when it
exists — CI, the pre-commit hook, and setup.* delegate there instead of each
restating a command. Absent that file, the built-in Python-reference defaults
below apply (identical values), so a profile-less repo is unchanged.

Contracts: IF-013, IF-022, IF-040 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import configparser
import importlib.util
import os
import re
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

# The conventional coverage.py JSON report: `--cov-report=json` writes
# `coverage.json` at the cwd and check_coverage.py reads it there by default.
# It is gitignored and SURVIVES BETWEEN RUNS, so main() clears a stale copy
# before any plan that runs the tests+coverage step (run-scoping the report —
# repo-review 2026-07-22 REVIEW-A). Without this, a smoke-tier run (which emits
# no JSON) would leave the previous full-tier file on disk for a
# [step:module-coverage] consumer to grade as a current PASS instead of the
# correct SKIP; a covered tier rewrites it fresh, so this only ever removes a
# report the current run did not produce.
COVERAGE_JSON = Path("coverage.json")

# The built-in plan's own step names. A project-declared `[step:<name>]` in
# docs/stack.ini may not shadow one — that would silently append a second step
# under a kit name, not replace the kit step. Keep in sync with steps() below.
BUILTIN_STEP_NAMES = frozenset(
    {
        "format",
        "lint",
        "tests+coverage",
        "derived-gate",
        "registry-integrity",
        "traceability",
        "vocabulary",
        "need-form",
        "privacy",
        "doc-navigability",
        "perf-budgets",
        "design-flows",
        "trajectory",
        "arch-map",
        "trajectory-map",
        "status-map",
        "open-items",
        "okf",
        "ratify-fresh",
        "skills-sync",
        "skills-index",
        "prompt-catalog",
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
        # utf-8-sig + replace: a Notepad BOM must not surface as a confusing
        # configparser "malformed" error, and a stray byte degrades (C8).
        cp.read_string(
            path.read_text(encoding="utf-8-sig", errors="replace"), source=str(path)
        )
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


def _split_template(template):
    """Whitespace-split a command template WITHOUT posix backslash-escaping, so a
    Windows path value in a stack.ini command (`.venv\\Scripts\\eslint`) keeps
    its separators — a bare shlex.split (posix escaping) would eat them to
    `.venvScriptseslint`. Same tokenizer agent_loop.split_cmd uses; kept a small
    duplicated helper per the F5 rule."""
    lex = shlex.shlex(template, posix=True)
    lex.whitespace_split = True
    lex.escape = ""
    return list(lex)


def _expand(template, subs):
    """Split a command TEMPLATE into argv, THEN substitute {py}/{src}/{tests}/
    {coverage}/{tier} per token. Splitting first keeps a Windows interpreter path
    (spaces, backslashes) intact — substituting into the raw string and then
    splitting would mangle it."""
    argv = []
    for tok in _split_template(template):
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


def _step_sections(profile):
    """Yield `(section, name)` for each `[step:<name>]` in the profile (name
    stripped, possibly empty — the caller validates). A None profile yields
    nothing. The single place the step-section scan lives, shared by extra_steps
    and extra_step_lanes so neither restates the loop prologue."""
    if profile is None:
        return
    for section in profile.sections():
        if section.startswith("step:"):
            yield section, section[len("step:") :].strip()


def extra_steps(profile, subs):
    """Project-declared additional gate steps, from `docs/stack.ini`
    `[step:<name>]` sections — the home for product-specific gates (license-lint,
    capability-integrity, …) so a project extends the plan WITHOUT
    hand-editing this take-wholesale file. A re-sync then overwrites check.py
    cleanly; the steps live in the declared profile, like the rest of the
    toolchain. Each section:

        [step:capability-integrity]
        command = {py} scripts/check_capabilities.py {src}   # required
        gates   = DevStg-Tests DevStg-Impl                                # optional, default DevStg-Impl
        layer   = product                             # optional, default product
        lane    = tests+coverage                       # optional (see below)

    `{py}/{src}/{tests}/{coverage}/{tier}` expand as in every other command, and
    the required-import set is auto-derived from the argv (a `{py} -m <mod>` step
    declares <mod>; any other executable's absence is caught by run_step's PATH
    guard) — the author declares nothing extra. An optional `lane = <step>`
    serializes this step into another step's lane so `--jobs>1` runs it AFTER,
    not concurrently — for a step that CONSUMES another's output (e.g. a
    coverage-floor check reading the tests+coverage JSON); `lane` is parsed by
    extra_step_lanes() and validated in main(). Malformed entries fail LOUDLY,
    never silently dropped, like every other profile error."""
    out = []
    for section, name in _step_sections(profile):
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
        # `gates =` IS AN ADOPTER-AUTHORED VALUE, so the retired `G1|G2|G3` tags  check_vocab: allow
        # translate on read (OI-21 contract break 2) — SILENTLY here, deliberately:
        # check_vocab.py sees this same file, can name the offending line, and
        # warns once per file instead of once per step per run. The shipped
        # template authors the new vocabulary; an adopter's existing file keeps
        # working until their re-sync updates it.
        gates = set()
        for tok in (
            profile.get(section, "gates", fallback=BAR_RELEASE)
            .replace(",", " ")
            .split()
        ):
            tok = RETIRED_BAR_ALIASES.get(tok, tok)
            if tok not in BAR_ORDER:
                sys.exit(
                    "check: docs/stack.ini [{}] gates has {!r}; expected a "
                    "space/comma list of {}".format(section, tok, "|".join(BAR_ORDER))
                )
            gates.add(tok)
        if not gates:
            gates = {BAR_RELEASE}
        layer = profile.get(section, "layer", fallback="product").strip() or "product"
        if layer not in ("process", "product"):
            sys.exit(
                "check: docs/stack.ini [{}] layer is {!r}; expected "
                "process|product".format(section, layer)
            )
        out.append((name, _requires(cmd), cmd, gates, layer))
    return out


def extra_step_lanes(profile):
    """`{step-name: lane}` for `[step:<name>]` sections declaring `lane = <other>`
    — the parallel-run serialization hint for a step that CONSUMES another step's
    output. Under `--jobs>1` every step runs in its own lane (concurrently)
    unless mapped here; a step reading the tests+coverage JSON report (the
    per-module coverage floor) must not race its producer, so it declares
    `lane = tests+coverage` and the runner puts it in that lane, executed AFTER
    it in plan order. Absent = own lane (the default). The lane is validated
    against the real plan in main(), so a typo fails loudly instead of silently
    re-racing the step."""
    out = {}
    for section, name in _step_sections(profile):
        lane = profile.get(section, "lane", fallback="").strip()
        if name and lane:
            out[name] = lane
    return out


def _resolve_lane_map(profile, coverage, tier, phase):
    """The parallel-run lane map: the built-in write-write lanes plus each
    `[step:]` `lane = <producer>` declaration (extra_step_lanes). A declared lane
    must name a REAL step (resolved at gate "all" so a lane onto another gate's
    step still maps), so a typo fails LOUDLY here instead of silently re-racing
    the step under --jobs>1 (a false green)."""
    lane_map = dict(_SHARED_OUTPUT_LANES)
    declared = extra_step_lanes(profile)
    if declared:
        all_names = {s[0] for s in steps(coverage, tier, "all", phase, profile)}
        for step_name, lane in declared.items():
            if lane not in all_names:
                sys.exit(
                    "check: docs/stack.ini [step:{}] lane = {!r} names no known "
                    "step to serialize after".format(step_name, lane)
                )
            lane_map[step_name] = lane
    return lane_map


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
    # {tier} exposes the run's selected tier to any declared step command, so a
    # tier-sensitive [step:] (the per-module coverage floor, which SKIPs when the
    # tier measures no coverage) reads it without check.py special-casing it.
    subs = {
        "py": sys.executable,
        "src": src,
        "tests": tests,
        "coverage": str(coverage),
        "tier": tier,
    }
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
    # The traceability step only runs at DevStg-Tests/DevStg-Impl, where placeholder rows must be
    # gone, so --no-placeholders is always on here (a fresh scaffold is exempt
    # only because nothing past DevStg-Reqs runs against it). --html also regenerates the
    # scalable full-graph view (a gitignored composite artifact) every run.
    trace_cmd = [
        sys.executable,
        str(_SCRIPTS / "trace.py"),
        "--strict",
        "--no-placeholders",
        "--html",
    ]
    if gate in (
        BAR_RELEASE,
        "all",
    ):  # DevStg-Impl criterion: test-verifiable SRs are Approved
        trace_cmd.append("--require-verified")
        trace_cmd.append(
            "--strict-schema"
        )  # DevStg-Impl: required fields + valid enums
        if (
            phase
        ):  # phased delivery: close DevStg-Impl for this phase only (process.md §4)
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
    # The trajectory validator gains --strict at DevStg-Tests/DevStg-Impl — the gates promote the
    # status↔registry coherence rules R-B…R-E from WARN to ERROR (R-A always
    # fails). "all" is deliberately EXCLUDED so the pre-commit floor, which runs
    # this step with NO --gate (so _step_gate resolves it to "all"), stays
    # warn-first: a plain commit must not block on status.md/SpecRef drift, only
    # on the R-A handoff-incoherence rule (process-options.md "Trajectory /
    # work-items layer").
    # The retired-vocabulary enforcer (OI-21) rides check_trajectory's severity
    # ladder EXACTLY — same condition, same `if`, deliberately not a second one.
    # The reason is the same too: a repo mid-conversion must SEE every remaining
    # site without being blocked by it, while a repo past its requirements bar has
    # no excuse. "all" is excluded so the pre-commit floor (which passes no
    # --gate) stays warn-first for both.
    traj_cmd = [sys.executable, str(_SCRIPTS / "check_trajectory.py")]
    vocab_cmd = [sys.executable, str(_SCRIPTS / "check_vocab.py"), "--root", "."]
    if gate in (BAR_TESTS, BAR_RELEASE):
        traj_cmd.append("--strict")
        vocab_cmd.append("--strict")
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
    # Cross-agent skill-sync drift gate (S7): byte-compare each per-agent skill
    # copy (.claude/.gemini/.agents) to the ONE neutral source. gen_skills_index
    # is a KIT-only script (it needs the neutral skills/ source, which only the
    # kit repo hosts — a scaffold has no source to drift from), so downstream it
    # isn't beside check.py; the step then runs a vacuous no-op so the hook's
    # `--run-step skills-sync` still resolves (never `no step named`) and passes
    # for free. Where the generator IS present (this kit's own repo) it runs the
    # real byte-identity check, deriving source + per-agent dirs itself.
    skills_gen = _SCRIPTS / "gen_skills_index.py"
    skills_sync_cmd = (
        [sys.executable, str(skills_gen), "--check-agents"]
        if skills_gen.exists()
        else [sys.executable, "-c", "pass"]  # kit-only generator absent: vacuous
    )
    # The generator's OTHER half, and a DIFFERENT property (WI-427): is
    # skills/INDEX.csv — a declared `[generated]` artifact — still what the
    # SKILL.md frontmatter says? `--check-agents` above cannot answer that; it
    # compares hand-authored copies to hand-authored source and never reads the
    # index. Hence its own step: different input, different fix
    # (gen_skills_index.py vs bootstrap.py --sync), different gate set.
    #   `--skills` IS PASSED EXPLICITLY, derived from this script's location and
    # never left to its CWD-relative `skills` default — in the kit's own repo the
    # source is at project-trajectory/skills, so the default finds nothing and
    # the generator exits 0 with "no skills dir": a step that cannot fail, the
    # SN-008 failure this row exists to remove.
    #   Both new commands take the kit-only shape of skills_sync_cmd above
    # (vacuous no-op where the generator isn't beside check.py), and both
    # generators resolve their artifact from their OWN location, so neither step
    # depends on the CWD.
    skills_index_cmd = (
        [
            sys.executable,
            str(skills_gen),
            "--skills",
            str(_SCRIPTS.parent / "skills"),
            "--check",
        ]
        if skills_gen.exists()
        else [sys.executable, "-c", "pass"]  # kit-only generator absent: vacuous
    )
    catalog_gen = _SCRIPTS / "gen_prompt_catalog.py"
    prompt_catalog_cmd = (
        [sys.executable, str(catalog_gen), "--check"]
        if catalog_gen.exists()
        else [sys.executable, "-c", "pass"]  # kit-only generator absent: vacuous
    )
    return [
        # --- product checks: language-specific, declared in docs/stack.ini -----
        ("format", _requires(fmt_cmd), fmt_cmd, {BAR_RELEASE}, "product"),
        ("lint", _requires(lint_cmd), lint_cmd, {BAR_RELEASE}, "product"),
        ("tests+coverage", _requires(test_cmd), test_cmd, {BAR_RELEASE}, "product"),
        # --- project-declared product steps: docs/stack.ini [step:<name>] ------
        # Product-specific gates a project adds (dup-code, license-lint, …) live
        # in the declared profile, NOT hand-edited into this take-wholesale file
        # (see extra_steps above). They slot in here with the other product steps.
        *extra_steps(profile, subs),
        # Optional PRODUCT-layer detector, not wired into the required floor:
        # `scripts/check_stubs.py` is the Python-reference tripwire for the DevStg-Impl
        # no-stub / substance criterion (process.md §4). It is warn-first and
        # language-specific (a stub's shape differs per stack), so — like the perf
        # *meters* — a project opts in. Prefer a docs/stack.ini `[step:no-stubs]`
        # section (survives re-sync) over hand-editing a step in here, e.g.:
        #   [step:no-stubs]
        #   command = {py} scripts/check_stubs.py --strict
        # (drop --strict to warn instead of fail). A non-Python stack swaps or
        # drops it. Left out of the default plan to keep the floor honest.
        # --- process checks: kit-owned, stdlib-only, identical everywhere -----
        # Registry integrity floor at DevStg-Reqs: the traceability step below already
        # fails on integrity findings via --strict, but it only runs from DevStg-Tests —
        # so a structurally broken registry CSV (unquoted commas misaligning
        # every later column) or a duplicated/malformed id would pass the DevStg-Reqs
        # gate and hide until DevStg-Tests/DevStg-Impl. This runs trace.py's always-valid subset
        # (duplicate/malformed ids + CSV column structure) at the first gate;
        # the pre-commit hook runs the same command on every commit. Listed
        # before traceability so at --gate all the fuller report.md wins.
        (
            "registry-integrity",
            (),
            [sys.executable, str(_SCRIPTS / "trace.py"), "--strict-integrity"],
            {BAR_REQS},
            "process",
        ),
        # Derived-gate freshness (docs/archive/specs/derived-gate-model.2026-07-20.md §5): docs/gate is
        # now GENERATED from artifact states by derive_gate.py, not hand-set —
        # `--check` recomputes and fails if the cache drifted (the arch-map/OKF/
        # dashboard freshness idiom, applied to the gate marker itself). Runs at
        # every gate: resolve_gate reads the cached value to pick the plan, so the
        # cache must be fresh whenever check.py runs, and this catches a stale one
        # (a legacy hand-set gate with no `# basis:` line is compared value-only,
        # so a not-yet-migrated repo stays green — the smooth-transition path).
        (
            "derived-gate",
            (),
            [sys.executable, str(_SCRIPTS / "derive_gate.py"), "--check"],
            {BAR_REQS, BAR_TESTS, BAR_RELEASE},
            "process",
        ),
        ("traceability", (), trace_cmd, {BAR_TESTS, BAR_RELEASE}, "process"),
        # Retired-vocabulary enforcer (OI-21). AT EVERY BAR, deliberately: the
        # whole point is that the retired tags cannot grow back, and the surface
        # they grow back into (registries, briefs, status prose) is authored
        # hardest at the LOWEST bar — a DevStg-Impl-only step would not run in
        # this kit's own CI for the whole of its requirements phase, which is
        # exactly the window the drift it guards against happened in. The
        # severity, not the wiring, is what stays warn-first.
        (
            "vocabulary",
            (),
            vocab_cmd,
            {BAR_REQS, BAR_TESTS, BAR_RELEASE},
            "process",
        ),
        # Need-form check (SN-033's declared checker, WI-454): each SN `need`
        # cell is scanned for internal paths, implementation-only identifiers
        # and process citations against the reviewed exception list in
        # docs/need-form-allow (ships empty). At every bar, like vocabulary —
        # the need registry is authored hardest at the LOWEST bar — but
        # WARN-FIRST ALWAYS: no `--strict` promotion here, deliberately unlike
        # vocab_cmd/traj_cmd. Promoting a form heuristic over ratified
        # stakeholder prose to a gate is an owner ruling that has not been
        # made (WI-454's scope guard); the severity ladder stops at WARN until
        # it is.
        (
            "need-form",
            (),
            [
                sys.executable,
                str(_SCRIPTS / "check_need_form.py"),
                "--root",
                ".",
            ],
            {BAR_REQS, BAR_TESTS, BAR_RELEASE},
            "process",
        ),
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
            {BAR_REQS, BAR_TESTS, BAR_RELEASE},
            "process",
        ),
        # Doc navigability (process.md §3 "Reviewability"): broken intra-repo
        # links fail; orphans warn; the README vision tag + SN inventory are
        # checked. Runs from DevStg-Reqs on (docs exist early). --stale adds the
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
                # The docs/work/ registry is DATA, not navigable prose: each
                # spec's body is a verbatim historical record (its Deliverable
                # cell), so link-checking it would force edits to history.
                # Registry integrity (id/filename agreement, frontmatter parse,
                # R-A/R-E) is check_trajectory's job, not this checker's.
                "--ignore",
                "docs/work/*",
                # SR-144's per-close reports: same posture, same reason (an
                # immutable generated record, not navigable prose).
                "--ignore",
                "docs/handbacks/*",
                "--stale",
            ],
            {BAR_REQS, BAR_TESTS, BAR_RELEASE},
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
            {BAR_RELEASE},
            "process",
        ),
        # Authored runtime-flow diagrams (process.md §3 "Design-time runtime
        # flows"): required from DevStg-Tests on, so reviewers verify behavior from the
        # diagrams, not from registry rows.
        (
            "design-flows",
            (),
            [sys.executable, str(_SCRIPTS / "check_flows.py"), "--no-placeholders"],
            {BAR_TESTS, BAR_RELEASE},
            "process",
        ),
        # Work-item trajectory (process-options.md "Trajectory / work-items
        # layer"): validates the execution DAG in docs/requirements/work-items.csv
        # — id integrity, resolvable predecessors, an acyclic graph (SR refs warn)
        # — plus the status.md↔registry SSOT rules (R-A Deliverable-iff-done, a
        # hard error always; R-B…R-E status coherence + SpecRef resolution, warn
        # here and ERROR under --strict, added at DevStg-Tests/DevStg-Impl via traj_cmd above).
        # An OPT-OUT layer: an absent or placeholder-only registry passes
        # vacuously and [checks] trajectory_check = false silences it, so a repo that
        # never adopts it pays nothing (the docs/secrets-scan floor's posture).
        # From DevStg-Tests on, where execution planning has begun.
        (
            "trajectory",
            (),
            traj_cmd,
            {BAR_TESTS, BAR_RELEASE},
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
            {BAR_RELEASE},
            "process",
        ),
        # Trajectory dashboard freshness (process-options.md "Trajectory /
        # work-items layer"): the generated-artifact freshness gate for
        # the root PROJECT_STATE.html — gen_trajectory.py --check regenerates in memory
        # and byte-compares, exactly like arch-map. DevStg-Impl only (like arch-map — the
        # generated view churns while the plan is still forming). Vacuous on an
        # absent/placeholder-only registry and silent under
        # [checks] trajectory_check = false, so a repo without work items pays nothing.
        (
            "trajectory-map",
            (),
            [sys.executable, str(_SCRIPTS / "gen_trajectory.py"), "--check"],
            {BAR_RELEASE},
            "process",
        ),
        # status.md derived-snapshot freshness (WI-202): the generated
        # `<!-- BEGIN GENERATED STATUS -->` block in docs/status.md carries only
        # derived facts (spine + derived gate + the open-items one-liners);
        # gen_trajectory.py --status --check regenerates in memory and
        # byte-compares, exactly like arch-map/trajectory-map. This is the
        # freshness successor to the WI-200 forward-only token guard, which stands
        # its rule down once the marker is present (check_trajectory). Vacuous when
        # status.md is absent or carries no marker pair (the opt-in posture), so a
        # repo that never adopts the block pays nothing. DevStg-Impl only, like the sibling
        # generated-artifact gates.
        (
            "status-map",
            (),
            [
                sys.executable,
                str(_SCRIPTS / "gen_trajectory.py"),
                "--status",
                "--check",
            ],
            {BAR_RELEASE},
            "process",
        ),
        # Owner decision-surface freshness (WI-322, OI-10 ruled option (b)):
        # docs/open-items.html is generated from docs/requirements/open-items.toml
        # plus the spine's Drafted/Modified rows — the surface that replaced the
        # hand-maintained docs/open-items.md. Same generated-artifact contract
        # as its siblings — a pure function of the committed tree since the
        # machine-local advisory region retired with the dispatcher
        # (concurrency-restructure Phase 5). Vacuous — exit 0 — when a repo
        # carries neither the registry nor the view, so a non-adopter pays
        # nothing.
        (
            "open-items",
            (),
            [sys.executable, str(_SCRIPTS / "gen_open_items.py"), "--check"],
            {BAR_RELEASE},
            "process",
        ),
        # OKF knowledge-bundle freshness (Thread 48): docs/okf/ is a generated
        # export of the spine registries (never a parallel source of truth) —
        # gen_okf.py --check regenerates in memory and byte-compares like
        # arch-map/trajectory-map. On by default, opt-out via
        # [checks] okf_export = false; vacuous on placeholder-only/absent
        # registries, so a fresh scaffold and a non-adopter pay nothing.
        (
            "okf",
            (),
            [sys.executable, str(_SCRIPTS / "gen_okf.py"), "--check"],
            {BAR_RELEASE},
            "process",
        ),
        # Re-attestation brief freshness (WI-325). Every other generated surface
        # here is freshness-gated; docs/ratify/*.md is generated the same way and
        # was gated by nothing, so it silently drifted behind the registry it
        # summarizes — twice in one day, both times caught only by a human
        # noticing. It fails CLOSED because a stale brief is read by a HUMAN
        # ABOUT TO ATTEST: a short brief means an owner blesses rows they were
        # never shown. The comparison uses the baseline the brief itself
        # DECLARES, never a re-derived one (re-deriving is the WI-322 BLOCKER,
        # where a regeneration collapsed 43 chain-row diffs to 18 while a
        # --check certified the loss).
        #
        # BUILT-IN rather than a docs/stack.ini `[step:]` — 130-REVIEW-A found
        # that shipping the hook while the step lived in a project-owned
        # stack.ini BLOCKS EVERY COMMIT for an adopter whose stack.ini predates
        # WI-325 ("check: no step named 'ratify-fresh'", exit 1). Its siblings
        # above are all built-in for exactly this reason: check.py and the hook
        # ship together, so a step declared here can never be missing from under
        # the hook that calls it. Doubly self-arming, so a non-adopter pays
        # nothing: silent with no docs/ratify/ brief, and silent when no SR is
        # Modified (the window is closed, so the brief is a record).
        (
            "ratify-fresh",
            (),
            [
                sys.executable,
                str(_SCRIPTS / "trace.py"),
                "--ratify",
                "modified",
                "--check",
            ],
            {BAR_TESTS, BAR_RELEASE},
            "process",
        ),
        # Cross-agent skill-sync freshness (S7): every per-agent skill copy
        # (.claude/.gemini/.agents) must stay byte-identical to the ONE neutral
        # source — the same generated-artifact gate as arch-map/trajectory-map/
        # okf. A drifted copy fails with a one-command fix (bootstrap.py --sync).
        # Vacuous when a repo has no neutral source or no per-agent dir (a
        # scaffold: the generator isn't beside check.py, so skills_sync_cmd is a
        # no-op). DevStg-Impl only, like the other generated-artifact freshness gates.
        (
            "skills-sync",
            (),
            skills_sync_cmd,
            {BAR_RELEASE},
            "process",
        ),
        # skills/INDEX.csv freshness against the SKILL.md frontmatter, and
        # prompts/CATALOG.md freshness against the shipped templates (WI-427,
        # IF-098). Both are declared generated in docs/stack.ini `[generated]`
        # (`skillsindex`, `promptcatalog`), both had a working `--check`, and
        # grep found neither in a step table, a hook or a workflow — so a stale
        # one passed every gate. SN-010 states the freshness contract as a
        # UNIVERSAL over generated artifacts, and a universal is false at one
        # instance.
        #
        # AT EVERY GATE, not {DevStg-Impl} like the siblings above. That family
        # (arch-map / trajectory-map / status-map / open-items / okf) is DevStg-Impl-only
        # for a stated reason — those are views of the project's own evolving
        # spine and "churn while the plan is still forming", so gating them early
        # reds a repo for drift in an artifact whose inputs are still being
        # written. These two have the opposite input profile: they index the
        # APPARATUS (the kit's skill library, the loop's prompt templates), which
        # does not move as a downstream plan matures, so there is no early-stage
        # churn to protect. Their consumers are live from the first session — an
        # agent reads INDEX.csv to decide whether a skill applies; an operator
        # reads CATALOG.md to join a session log's `# prompt-sha:` back to the
        # template that produced it, i.e. while debugging a session that already
        # behaved oddly. That is `derived-gate`'s shape (an artifact the
        # machinery's own honesty rests on), not the dashboards'. Concretely:
        # this kit's own docs/gate reads DevStg-Reqs while its ratification window is
        # open, so a {DevStg-Impl} step would not run in the kit's own CI for the whole
        # duration of that window — the gap, re-created.
        (
            "skills-index",
            (),
            skills_index_cmd,
            {BAR_REQS, BAR_TESTS, BAR_RELEASE},
            "process",
        ),
        (
            "prompt-catalog",
            (),
            prompt_catalog_cmd,
            {BAR_REQS, BAR_TESTS, BAR_RELEASE},
            "process",
        ),
    ]


# --- THE BAR VOCABULARY (OI-21) -------------------------------------------------
# The three CLEARABLE stages, lowest first — a strict subset of the eight-rung
# ladder, each named for the rung it CLOSES OUT (owner ruling 2026-08-18: one
# vocabulary, the VERB carries the axis — a repo is IN a stage and CLEARS a
# stage, never a second `DevBar-` spelling). Duplicated from derive_gate.py per the F5
# independently-copyable-script rule and pinned equal by tests/test_rule_sync.py:
# check.py must stay a wholesale drop-in that never imports a sibling.
#
#     clearing DevStg-Reqs   closes Needs, Boundary, Reqs
#     clearing DevStg-Tests  closes Arch, LLReqs, Tests
#     clearing DevStg-Impl   closes Impl  (DevStg-Release is OUTSIDE this range)
BAR_REQS, BAR_TESTS, BAR_RELEASE = "DevStg-Reqs", "DevStg-Tests", "DevStg-Impl"
BAR_ORDER = [BAR_REQS, BAR_TESTS, BAR_RELEASE]
GATES = BAR_ORDER + ["all"]

# THE RETIRED-TAG ALIASES (check_vocab: allow-file is NOT used — only these
# declaration lines are marked). `--gate G2` is a string an adopter's hook  check_vocab: allow
# and CI workflow pass LITERALLY, so refusing it would break every adopter's
# pipeline at the re-sync — and this kit's own rule is that a breaking change to
# a downstream-visible CLI needs a migration, not a cliff. So the retired tags
# are ACCEPTED here and WARNED about (`_resolve_bar_alias` prints the canonical
# form to stderr once per run).
#
# WHY WARNED RATHER THAN SILENT OR REFUSED. Silent acceptance is how the retired
# vocabulary grows back — the tags would live in adopters' hooks forever with
# nothing ever telling anyone. Refusal breaks working pipelines for a vocabulary
# change. A warning is the only posture that both keeps the pipeline green and
# guarantees the operator is told; it costs one stderr line per run and it stops
# the moment the hook is updated. The AUTHORED surfaces (docs/stack.ini `gates=`,
# a WI's `bar:` frontmatter) translate SILENTLY instead, because check_vocab.py
# can see those files and name the offending line — a far better message than a
# reader could produce.
RETIRED_BAR_ALIASES = {  # check_vocab: allow
    "G1": BAR_REQS,  # check_vocab: allow
    "G2": BAR_TESTS,  # check_vocab: allow
    "G3": BAR_RELEASE,  # check_vocab: allow
    # The `DevBar-*` prefix, retired 2026-08-18. `DevBar-Release` resolves to
    # `DevStg-Impl`, NOT to `DevStg-Release`: that bar never certified the
    # Release rung, and the alias carries the correction.
    "DevBar-Reqs": BAR_REQS,  # check_vocab: allow
    "DevBar-Tests": BAR_TESTS,  # check_vocab: allow
    "DevBar-Release": BAR_RELEASE,  # check_vocab: allow
}


def bar_ord(name):
    """The ladder position of a bar name; RAISES on anything else.

    EVERY COMPARISON BETWEEN BARS ROUTES THROUGH HERE. The retired vocabulary let
    this module compare gate names as raw strings, which was correct only because
    `G1 < G2 < G3` happens to alphabetize (check_vocab: allow) — a form that looks
    ordered while being
    ordered by accident. The new names are NOT alphabetical (`DevStg-Impl`
    sorts before `DevStg-Reqs` before `DevStg-Tests`), so the accident is gone and
    a lexical comparison is now obviously, loudly wrong instead of quietly right.
    tests/test_stage_ladder.py greps the kit's scripts to keep it that way."""
    try:
        return BAR_ORDER.index(name)
    except ValueError:
        raise ValueError(
            "check: {!r} is not a runnable bar — expected one of {}".format(
                name, "|".join(BAR_ORDER)
            )
        ) from None


def _resolve_bar_alias(value, what):
    """Translate a retired `G1`/`G2`/`G3` tag to a canonical bar, warning once.  check_vocab: allow
    Anything else passes through untouched for the caller's own validation."""
    v = (value or "").strip()
    if v in RETIRED_BAR_ALIASES:
        canonical = RETIRED_BAR_ALIASES[v]
        print(
            "check: {} {!r} uses the RETIRED gate vocabulary — reading it as {!r}. "
            "The tags retired at OI-21; update to the stage-ladder bar names "
            "({}).".format(what, v, canonical, "|".join(BAR_ORDER)),
            file=sys.stderr,
        )
        return canonical
    return v


# The machine-readable derived bar (process.md §4/§7). One line, e.g. "DevStg-Reqs".
GATE_FILE = Path("docs/gate")

# `derive_gate.py` writes its inputs into a `# basis:` comment above the value.
# The two counts below say whether the bar is SUPPRESSED by an open ratification
# window rather than reflecting the project's real maturity.
# `drafted=` (was `drafts=`) SINCE D-9 MIGRATION STEP 5 — moved in the SAME
# commit as `derive_gate.basis_line`, which is the whole point: a producer rename
# that leaves this regex behind blinds the window detector and twelve gate steps
# stop running silently (the measured 2026-07-26/27 precedent below). The
# producer-consumer round-trip pin in `tests/test_derive_gate.py` is what makes
# the next such edit fail loudly.
_BASIS_RE = re.compile(r"#\s*basis:.*\bdrafted=(\d+)\b.*\bmodified=(\d+)\b")
# The other two fields the window test needs: the raw computed level (may be
# `DevStg-Below`, unlike the runnable value on the line below it) and the
# per-phase breakdown, which is what distinguishes "drafts are holding a MATURE
# spine down" from "this project is simply early".
_COMPUTED_RE = re.compile(r"\bcomputed=(DevStg-\w+)\b")
_PER_PHASE_RE = re.compile(r"\bper-phase=(\S+)")
# The level the spine would compute with the DRAFT rows removed (WI-341). This
# is the direct answer to "are the drafts the only thing holding this bar
# down?", and unlike the per-phase breakdown a draft cannot erase it: the rows
# it did not touch are still there. Absent from gate files written before
# WI-341 — the per-phase fallback below covers those until they regenerate.
_EX_DRAFT_RE = re.compile(r"\bex-draft=(DevStg-\w+)\b")


def _window_ord(name):
    """A basis-line level as a comparable ordinal, with `DevStg-Below` sitting
    UNDER every runnable bar. Separate from `bar_ord` because the basis line
    legitimately carries the below-the-floor sentinel that `--gate` never can, and
    an unreadable value reads as the floor so a malformed cache never manufactures
    a window."""
    if name == "DevStg-Below":
        return -1
    try:
        return BAR_ORDER.index(name)
    except ValueError:
        return -1


# Steps kept OUT of the advisory pass, by name and with the reason — an
# unexplained exclusion list is how a warn tier quietly stops covering things.
#
# `tests+coverage` is excluded because it is NOT a blind spot: a developer runs
# the suite directly on every commit (the smoke bar) and unfiltered at slice
# close, so its failures surface immediately with or without this pass. Adding it
# would re-run the whole suite plus coverage on EVERY gate run for the life of a
# window — measured 55.8 s at the smoke tier and ~11 min unfiltered on a
# 24-thread box — which buys no signal and would train people to skip the gate.
# The steps that ARE included (lint, the freshness gates, the DevStg-Impl traceability
# criterion) are cheap, read-only, and genuinely stop running.
#
# `module-coverage` follows its PRODUCER out (127-REVIEW-A MAJOR 6). It grades
# `coverage.json`, which only `tests+coverage` writes — and `_clear_stale_coverage_report`
# only deletes a stale report when the GATING plan contains that producer. Left
# in, the advisory pass would either grade a coverage report from some earlier,
# unrelated run as if it were this run's evidence, or report a missing-data
# failure every time. Stale evidence reported as current is worse than no
# evidence: it is the failure mode this whole ruling exists to prevent. If the
# producer is ever cheap enough to include, this exclusion should go with it.
ADVISORY_EXCLUDE = {"tests+coverage", "module-coverage"}


def window_open(gate_file=None):
    """True when an open `Drafted`/`Modified` window is holding the derived gate
    below what the artifacts otherwise support.

    Why this exists (owner ruling 2026-07-27): a window drops the gate, and the
    plan below then drops every step tagged for the higher gate — so `lint` and
    `--require-verified` simply STOP RUNNING for the duration. That
    is not a relaxed bar, it is a blind spot: twelve commits went green over
    those steps during the 2026-07-26/27 window and the debt surfaced in one
    lump when the window closed (WI-333/WI-334 — that debt was the duplication
    census's, and the census itself was torn down later, D-7/WI-426; the ruling
    is about the blind spot, not about which step fell into it).

    Deliberately NOT "any gate below DevStg-Impl": a project genuinely at DevStg-Reqs has not
    earned those steps and should not be told about them on every run. The
    signal is specifically that the gate was *suppressed*.

    The two counts are not equally good evidence of that, which the first cut
    got wrong (127-REVIEW-A MAJOR 5 — it fired on `drafted>0`, ordinary DevStg-Below/DevStg-Reqs
    state, contradicting the very claim above):

      * `modified>0` IS conclusive on its own. `Modified` is *defined* as a
        post-approval amendment (derive_gate's model, WI-316), so the row can
        only exist in a spine that has already been ratified. Something that was
        `Approved` is pending again — that is a window by construction.
      * `drafted>0` is ambiguous. A `Drafted` row reads DevStg-Below, so drafts drop the gate in a
        mature repo starting a new phase AND in a project that has never
        ratified anything. The counts cannot tell those apart — `ex-draft` can,
        by answering the question directly: it is the level the same arithmetic
        computes with the draft rows REMOVED. If that clears DevStg-Tests and sits above
        the level the drafts produced, then the spine has demonstrably climbed
        and the drafts are the only thing holding it down. A window.

    `ex-draft` replaced a per-phase heuristic that read the phase breakdown for
    the same evidence (WI-341). The heuristic could not see a SINGLE-phase
    repo's maturity at all: a `Drafted` row added there drops that phase to DevStg-Below, so no
    phase remains above `computed` and the mature repo reads exactly like a new
    one — the very blind spot this tier exists to close, reopened by one row
    (128-REVIEW-A MAJOR 3). It is kept below ONLY as the fallback for a gate
    file written before `ex-draft` existed, and it keeps its own DevStg-Tests floor,
    which fixed the mirror-image false positive on an early multi-phase repo.

    Both routes are conservative when the evidence is missing (no `ex-draft`
    and no per-phase breakdown => ordinary): the cost of a false positive is a
    warn tier people learn to ignore, and the case that motivated the ruling —
    the 2026-07-26/27 re-attestation — is a `modified` window, caught
    unconditionally."""
    path = Path(gate_file) if gate_file else GATE_FILE
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    m = _BASIS_RE.search(text)
    if not m:
        return False  # a hand-written or pre-derived gate file: no opinion
    drafts, modified = int(m.group(1)), int(m.group(2))
    if modified > 0:
        return True
    if drafts == 0:
        return False
    computed = _COMPUTED_RE.search(text)
    if not computed:
        return False
    ex_draft = _EX_DRAFT_RE.search(text)
    if ex_draft:
        # Two conditions, not one: the drafts-removed level must clear the bar
        # the advisory tier reports on (DevStg-Tests+), and it must actually be ABOVE what
        # the drafts produced — otherwise the drafts are not what is holding the
        # gate down and there is nothing being suppressed.
        return _window_ord(ex_draft.group(1)) >= _window_ord(BAR_TESTS) and (
            _window_ord(ex_draft.group(1)) > _window_ord(computed.group(1))
        )
    # Fallback for a pre-WI-341 gate file (no `ex-draft`), with its own DevStg-Tests floor.
    per_phase = _PER_PHASE_RE.search(text)
    if not per_phase or per_phase.group(1) == "(none)":
        return False
    levels = re.findall(r"=(DevStg-\w+)", per_phase.group(1))
    if not levels:
        return False
    top = max(_window_ord(v) for v in levels)
    return top >= _window_ord(BAR_TESTS) and top > _window_ord(computed.group(1))


def run_advisory(advisory, jobs, lane_map):
    """Run the warn-only tier and return its results ([] when there is none).

    Split out of `main()` to hold the complexity ratchet: the advisory feature
    added branches to a function already at its baseline, and the ratchet's rule
    is to decompose rather than re-stamp."""
    if not advisory:
        return []
    print(
        "\n### ADVISORY — a ratification window is open, so the gate is "
        "below what these steps belong to. They run WARN-ONLY: findings are\n"
        "### reported, the exit code is not affected. Clearing the window "
        "restores them to the bar (owner ruling 2026-07-27)."
    )
    return run_plan(advisory, True, jobs or len(advisory), lane_map)


def advisory_plan(gate, plan, steps_at):
    """Steps a HIGHER gate requires, while an open ratification window holds this
    gate down. They run advisory: reported, never gating (owner ruling
    2026-07-27).

    Without this a window is a blind spot rather than a lower bar — the step
    stops running, so the commit that breaks it says nothing and the debt lands
    in one lump whenever the window closes.

    Built by ASKING `steps()` for each higher gate's own plan (`steps_at`), not
    by filtering this gate's. That distinction is the whole of 127-REVIEW-A
    BLOCKER 4: the step table is *specialized to the gate it was built for*, so
    `traceability` built at DevStg-Tests carries no `--require-verified`, and no filter
    over it could ever produce the stronger variant — which the owner explicitly
    ruled IN (an unapproved-but-decomposed row "also fails it, and that is real
    signal" — the owner's words named `Planned`, which folded into `Approved` at
    D-9 step 5; the point survives the word). The
    first cut filtered, so it silently ran neither the DevStg-Impl command nor anything
    in its place, while a test asserted traceability was *not* advisory and
    entrenched it.

    A step already in the gating plan is skipped only when its command is
    IDENTICAL. When the higher gate's form differs, that stronger form runs
    advisory alongside the weaker gating one — the same step name legitimately
    appears in both tiers, which is why the summary marks the advisory rows.

    A named function rather than an inline comprehension for two reasons: it kept
    `main()` under the complexity ratchet, and it gives the guards something to
    CALL. The first version of the test re-implemented this filter and therefore
    asserted against its own copy of the rule — a guard that cannot observe the
    code it names.
    """
    if gate == "all" or not window_open():
        return []
    gating = {}
    for name, _requires, cmd, _gates, _layer in plan:
        gating.setdefault(name, []).append(list(cmd))
    out, seen = [], set()
    # HIGHEST gate first, and one entry per step name: a step required at both
    # DevStg-Tests and DevStg-Impl gets its DevStg-Impl form, which is the stronger one. Ascending order ran
    # `traceability` twice at DevStg-Reqs — once without `--require-verified` and once
    # with — which is pure duplication, since the stronger form subsumes it.
    higher_bars = [g for g in BAR_ORDER if bar_ord(g) > bar_ord(gate)]
    for higher in sorted(higher_bars, key=bar_ord, reverse=True):
        for step in steps_at(higher):
            name, _requires, cmd, gates, _layer = step
            if higher not in gates or name in ADVISORY_EXCLUDE or name in seen:
                continue
            if list(cmd) in gating.get(name, []):
                seen.add(name)  # already running in exactly this form
                continue
            seen.add(name)
            out.append(step)
    return out


def _print_steps(plan):
    """One `--list` line per step: name, layer, the gates that require it, and
    the exact command. Extracted rather than repeated for the advisory tier: the
    two tiers print the SAME line, so one printer is the only way the formats
    cannot drift apart. (Historically the duplication census flagged the second
    copy the moment it appeared; that census was torn down in D-7/WI-426, so the
    extraction now stands on its own reason rather than on a tool's verdict.)"""
    for name, _requires, cmd, gates, layer in plan:
        # Sorted by LADDER POSITION, not lexically: `DevStg-Impl` alphabetizes
        # FIRST, so an unkeyed sort here printed the step's bars in nonsense order
        # the moment the vocabulary changed. Caught by tests/test_stage_ladder.py's
        # grep, which is exactly the class of accidentally-right code OI-21 banned.
        print(
            "  - {:16} [{:7}] [{}]  {}".format(
                name, layer, ",".join(sorted(gates, key=bar_ord)), " ".join(cmd)
            )
        )


def resolve_gate(explicit):
    """The gate to run: an explicit --gate wins; else the docs/gate file (the
    project's derived gate); else 'all' (a repo without the file gets the full bar,
    never a silently weaker one). The file is parsed by the declared-policy rule
    every reader shares (hooks, check_privacy.py, agent_loop.py): the first
    non-empty, non-comment line — which is now DERIVED by derive_gate.py from the
    artifact states (docs/archive/specs/derived-gate-model.2026-07-20.md), not hand-set. The read is
    unchanged (the derived value sits on that same first non-comment line, with the
    derivation basis in `#` comments above it); the `derived-gate` step guards the
    cache against drift, so a --gate resolved here is a fresh computed value."""
    if explicit:
        return explicit
    if GATE_FILE.exists():
        val = ""
        for ln in GATE_FILE.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():  # errors="replace": degrade a stray byte, don't crash (C8)
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


def _step_gate(explicit):
    """The gate that BUILDS a --run-step/--run-steps command: an explicit --gate
    is honoured (so `--gate DevStg-Impl --run-steps trajectory` really gates), but a
    DEFAULTED one resolves to "all", never docs/gate — the pre-commit hook passes
    no --gate and its floor must stay warn-first (see the trajectory step's
    comment). Name lookup stays unfiltered, so `format` is findable at any gate."""
    return explicit or "all"


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
    "COVERAGE_RCFILE",
    "COV_CORE_SOURCE",
    "COV_CORE_CONFIG",
    "COV_CORE_DATAFILE",
    "COV_CORE_BRANCH",
    "COV_CORE_CONTEXT",
)


# --- The trunk lane: generated-artifact freshness is not a work branch's job ----
# concurrency-restructure.md §5.2: work branches NEVER commit generated artifacts
# — the trunk regenerates them in one serial step after each merge. Gating a
# branch on their freshness would red every branch for drift it is forbidden to
# fix, and would push workers to commit exactly the artifacts whose conflicts
# this restructure exists to delete. Reads are unaffected: a branch-local check
# reads a generated artifact as-of-base, and the composed tree re-derives at the
# queue. Deliberately NOT here: `skills-sync` (both sides of that gate are
# hand-authored SOURCE, so a branch editing a skill fixes its copies on the
# branch), registry-integrity, trajectory, doc-navigability, and every product
# step — those grade the branch's own edits, not the trunk's derived views.
#   `skills-index` and `prompt-catalog` (WI-427) also stay out, and the reason is
# the asymmetry docs/stack.ini `[generated]` records: `trunk_step.py --regen`
# re-derives six DOCUMENT families and neither of these is among them. Standing
# them down on a branch would leave the artifact ungated on the only side that
# can fix it (the branch editing the SKILL.md / prompt template) and unfixable on
# the side that gates it — the trunk would red with no mechanical regen to run.
# The `[generated]` section declares OWNERSHIP, not lane; this set encodes which
# owners the trunk can actually regenerate.
_TRUNK_FRESHNESS_STEPS = frozenset(
    "derived-gate arch-map trajectory-map status-map open-items okf "
    "ratify-fresh".split()
)

# `_work_branch` shells out to git; unmemoized it would run once per step. Keyed
# by resolved root, so a test moving between fixtures gets its own answer.
_WORK_BRANCH_CACHE = {}

# Set by `--trunk-lane`. The stand-down above rests on "a work branch never
# commits a generated artifact", which the station refresh (concurrency-v2.md
# §A2) makes false for exactly one commit: it merges trunk in, runs trunk_step
# ON the branch and bars the result — a tree byte-identical to the one the merge
# produces, so it owes the trunk lane's gates. Without the flag those seven
# steps SKIP, and the integrator reads any SKIP as a refusal, so the refresh
# could never go green: the flag is what MAKES the mechanical bar possible, not
# a rescue from a false pass (REVIEW-A round 1 — the first version of this
# comment had the failure direction backwards). Opt-IN all the same, so a
# caller that forgets it gets the stricter-for-trunk answer.
_FORCE_TRUNK_LANE = False


def _git_out(root, args):
    """stdout of a git command under `root`, or None on ANY failure (no git
    binary, not a repo, detached HEAD) — the house best-effort-off-git pattern
    (trace.py `_git_out`, derive_gate.py `_git`)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def _claimed_work_branch(root):
    """The uncached answer behind `_work_branch` — see it for the contract."""
    out = _git_out(root, ["symbolic-ref", "--short", "HEAD"])
    branch = (out or "").strip()
    if not branch:
        return None  # no git, not a repo, or a detached HEAD => full checks
    # A branch name is used here as a relative PATH. git's own ref rules already
    # forbid `..` and `\`, but this decides whether a gate runs, so it refuses
    # rather than trusts — loudly, because a name that reaches here is either a
    # git that stopped enforcing its rules or something feeding us a fake ref.
    if ".." in branch or "\\" in branch or branch.startswith("/"):
        print(
            "check: ignoring implausible branch name '{}' — running the full "
            "checks (concurrency-restructure §5.2)".format(branch),
            file=sys.stderr,
        )
        return None
    active = Path(root) / "docs" / "work" / "active"
    spec_dir = active / branch
    try:
        # Belt-and-braces containment: whatever the name, the claim directory
        # must sit UNDER docs/work/active/ for this to be a claimed branch.
        spec_dir.resolve().relative_to(active.resolve())
    except (OSError, ValueError):
        return None
    if spec_dir.is_dir():
        return branch
    # WI-357: the working tree alone cannot answer this. §2.3 step 3 closes a WI by
    # MOVING the claim out of active/, so from the close commit on the tree holds no
    # claim and the freshness gates re-arm inside the very commit that closes it,
    # demanding artifacts §5.2 forbids the branch to commit. History outlives the
    # move: the base commit that cut the branch added the directory, and that add
    # stays reachable. One path-limited git call, stopped at the first hit.
    # FAIL-DIRECTION: no git, a failing git or an empty answer all read as the TRUNK
    # lane and its STRICT bar, because a false positive would switch the freshness
    # gates off on the trunk — the one branch that owns regenerating them, where
    # nothing else would catch the drift. Residual (review-confirmed breadth): ANY
    # branch whose name ever appeared under docs/work/active/ in reachable history
    # reads as claimed forever — a retired WI branch re-cut, or a throwaway reusing
    # its name; that relaxes a BRANCH, never the trunk, and bounding the walk would
    # need a configured trunk name this rule deliberately has not. Cost note: on
    # the trunk the pathspec never matches, so the -1 walk pays full history —
    # measured ~0.05 ms/commit (61 ms at 1.2k commits), once per process via the
    # cache below; a very large adopter repo that feels it should bound with
    # --since rather than name its trunk.
    log = _git_out(
        root, ["log", "-1", "--format=%H", "--", "docs/work/active/" + branch]
    )
    return branch if (log or "").strip() else None


def _work_branch(root="."):
    """The current branch name IF it is a CLAIMED work branch, else None.

    The claim is the Phase 2c registry model (concurrency-restructure §2.1/§2.3):
    a claimed branch's work-item specs live in `docs/work/active/<branch>/`, moved
    there by the serial trunk commit that cut the branch. So the branch itself
    carries the evidence — no ref namespace, no reservation file — in its working
    tree, or once the close moves the specs to their terminal directory, in
    its own history.

    Fail-CLOSED by construction: off git, on a detached HEAD, or with neither a
    matching `active/` directory nor a claim in history the answer is None and the
    STRICT bar applies. The trunk is simply the branch nobody claimed a work item
    on."""
    key = str(Path(root).resolve())
    if key not in _WORK_BRANCH_CACHE:
        _WORK_BRANCH_CACHE[key] = _claimed_work_branch(root)
    return _WORK_BRANCH_CACHE[key]


def _work_branch_skip(name, root="."):
    """(status, detail, notice) when `name` is a trunk-lane freshness step and we
    are on a claimed work branch, else None.

    The skip happens HERE, at execution, not by dropping rows from the step table:
    `--list` and the summary must still name the step, or the plan would lie about
    what the gate covers. A skipped step never affects the exit code (SKIP is not
    FAIL — the same status the missing-tool guard uses)."""
    if name not in _TRUNK_FRESHNESS_STEPS or _FORCE_TRUNK_LANE:
        return None
    branch = _work_branch(root)
    if not branch:
        return None
    detail = (
        "work branch '{}' — generated freshness is the trunk lane's, "
        "concurrency-restructure §5.2".format(branch)
    )
    return "SKIP", detail, "{}: skipped ({})".format(name, detail)


def _step_env():
    """The environment for a spawned step, minus any ambient coverage-orchestration
    vars (see _COVERAGE_ENV_VARS) so the project's own coverage run is authoritative."""
    env = dict(os.environ)
    for var in _COVERAGE_ENV_VARS:
        env.pop(var, None)
    return env


def _step_guard(requires, cmd, lenient):
    """The missing-tool guards shared by both step runners. Returns
    ((status, detail), None) when the step must not run, else (None, exe) with
    the RESOLVED executable to exec.

    Module guard: a `{py} -m <mod>` step whose module this interpreter can't
    import. Command guard: a rewired step ("swap the format/lint/test commands
    for your toolchain") names an executable the module guard can't see —
    resolve it the way the OS would (a path, or PATH lookup — shutil.which
    honors PATHEXT on Windows) and fail by design instead of crashing with a
    raw FileNotFoundError. The resolved path (not the bare name) is what gets
    exec'd: Windows CreateProcess applies no PATHEXT, so a bare `npx` that
    shutil.which found as npx.cmd would still crash with WinError 2
    (downstream field report, WI-1.25)."""
    missing = [m for m in requires if importlib.util.find_spec(m) is None]
    if missing:
        status = "SKIP" if lenient else "FAIL"
        detail = "module(s) {} not importable by {} — run scripts/setup".format(
            ", ".join(missing), sys.executable
        )
        return (status, detail), None
    exe = cmd[0] if Path(cmd[0]).exists() else shutil.which(cmd[0])
    if not exe:
        status = "SKIP" if lenient else "FAIL"
        detail = (
            "command {!r} not found — wire your stack's toolchain "
            "(see the EDIT FOR YOUR STACK block)".format(cmd[0])
        )
        return (status, detail), None
    return None, exe


def missing_tool_banner(skipped):
    """The SILENT-SKIP GUARD (WI-460): a boxed stderr banner naming every
    PRODUCT-layer step that SKIPped because its tool is not installed.

    Why a banner and not a refusal. The hook path (`--run-step` /
    `--run-steps`) runs every step LENIENT on purpose — a missing tool is SKIP,
    exit 0 — so a not-yet-set-up repo can still commit. That leniency is right
    and it has a measured cost: a lane worktree with no `ruff` SKIPped `format`
    on EVERY commit of a nine-commit branch, and two unformatted files rode to
    the merge. Nothing was hidden — one dim `SKIP format ...` line printed each
    time, in the middle of a twelve-step batch, and a dim line repeated nine
    times is a line nobody reads. So the smallest honest fix is to make the
    same fact unmissable, not to change what the commit is allowed to do.

    PRODUCT layer only, and that is the whole selector. A product step's command
    is the one the repo WROTE DOWN in docs/stack.ini (`[product] format/lint/
    test`, and each `[step:*]` declaring `layer = product`) — declaring it is
    the repo saying it wants that tool run. Process-layer steps are kit-owned
    and stdlib-only, so they have no third-party tool to go missing, and the
    trunk-lane freshness skips (`_TRUNK_FRESHNESS_STEPS`) are all process-layer
    — a DELIBERATE, already-explained skip must never be dressed as a defect.

    Refusal was weighed and left to the owner: making a declared-but-absent tool
    FAIL on the hook path is the stronger guard, and it breaks every adopter
    whose contributor has not run dev-setup yet — a migration this session has
    no authority to impose. Recorded in the log rather than taken quietly."""
    if not skipped:
        return
    sys.stdout.flush()  # the banner is the LAST thing on screen, deterministically
    print("", file=sys.stderr)
    print("!" * 72, file=sys.stderr)
    print(
        "!! A DECLARED CHECK DID NOT RUN — this commit was NOT graded by it.",
        file=sys.stderr,
    )
    for name, detail in skipped:
        print("!!   {:16} {}".format(name, detail), file=sys.stderr)
    print(
        "!! These steps come from docs/stack.ini, so this repo declares them.",
        file=sys.stderr,
    )
    print(
        "!! Install the toolchain (scripts/dev-setup) — a step that skips on",
        file=sys.stderr,
    )
    print(
        "!! every commit of a branch is a bar that is not being run.", file=sys.stderr
    )
    print("!" * 72, file=sys.stderr)


def _skipped_product_steps(results, by_name):
    """[(name, detail)] for the results whose step is PRODUCT-layer and SKIPped.
    `by_name` maps a step name to its plan tuple (name, requires, cmd, gates,
    layer)."""
    return [
        (name, detail)
        for name, status, detail in results
        if status == "SKIP" and (by_name.get(name) or (None,) * 5)[4] == "product"
    ]


def run_step(name, requires, cmd, lenient):
    """Run one step, streaming its output live (the sequential path).
    Returns (status, detail) where status in PASS/FAIL/SKIP."""
    lane_skip = _work_branch_skip(name)
    if lane_skip:
        print(lane_skip[2], flush=True)
        return lane_skip[0], lane_skip[1]
    guard, exe = _step_guard(requires, cmd, lenient)
    if guard:
        return guard
    start = time.time()
    print("\n=== {} : {} ===".format(name, " ".join(cmd)), flush=True)
    proc = subprocess.run([exe] + list(cmd[1:]), env=_step_env())
    secs = time.time() - start
    if proc.returncode == 0:
        return "PASS", "{:.1f}s".format(secs)
    return "FAIL", "exit {} ({:.1f}s)".format(proc.returncode, secs)


def run_step_captured(name, requires, cmd, lenient):
    """run_step with the child's output captured instead of streamed — the
    parallel path, where concurrent children writing one console would
    interleave. Returns (status, detail, output)."""
    lane_skip = _work_branch_skip(name)
    if lane_skip:
        # The notice rides out as the step's OUTPUT so the parallel path prints
        # it under the same lock as every other step's banner.
        return lane_skip[0], lane_skip[1], lane_skip[2] + "\n"
    guard, exe = _step_guard(requires, cmd, lenient)
    if guard:
        return guard[0], guard[1], ""
    start = time.time()
    proc = subprocess.run(
        [exe] + list(cmd[1:]),
        env=_step_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    secs = time.time() - start
    out = proc.stdout or ""
    if proc.returncode == 0:
        return "PASS", "{:.1f}s".format(secs), out
    return "FAIL", "exit {} ({:.1f}s)".format(proc.returncode, secs), out


# Steps that must not run concurrently share a *lane* (run serially, in plan
# order). Two reasons a step joins another's lane:
#   - WRITE-WRITE: BOTH trace.py invocations — registry-integrity's
#     --strict-integrity floor and the full traceability join — rewrite
#     docs/test/report.md every run, so they chain in one "trace-report" lane.
#   - READ-AFTER-WRITE: a project step that CONSUMES another's output declares
#     `lane = <producer>` in its [step:] section (extra_step_lanes) — e.g. the
#     per-module coverage floor reading the tests+coverage JSON must run after
#     it, not race it. Those declarations are merged onto this base map in main().
# Every other step is read-only (the --check freshness gates, the lints,
# privacy) or writes a distinct target, so it parallelizes freely.
_SHARED_OUTPUT_LANES = {
    "registry-integrity": "trace-report",
    "traceability": "trace-report",
}


def run_plan(plan, lenient, jobs, lane_map=None):
    """Execute the plan's steps; returns [(name, status, detail)] in plan order.

    jobs == 1 streams each step's output live, one at a time — byte-identical
    to the historical behavior, and the default. jobs > 1 runs the steps
    concurrently in *lanes* (see _SHARED_OUTPUT_LANES and a step's declared
    `lane =`), capturing each step's output and printing it whole under a lock
    when the step finishes, so output never interleaves; the summary and exit
    semantics are unchanged (never a false green — an unexpected runner
    exception propagates). `lane_map` (name -> lane) defaults to the built-in
    write-write map; main() passes it merged with the profile's `lane =`
    declarations."""
    if lane_map is None:
        lane_map = _SHARED_OUTPUT_LANES
    if jobs <= 1 or len(plan) <= 1:
        return [
            (name, *run_step(name, requires, cmd, lenient))
            for name, requires, cmd, _gates, _layer in plan
        ]
    import concurrent.futures
    import threading

    lanes = {}
    for idx, step in enumerate(plan):
        lanes.setdefault(lane_map.get(step[0], step[0]), []).append((idx, step))
    lock = threading.Lock()
    results = {}

    def run_lane(lane_steps):
        for idx, (name, requires, cmd, _gates, _layer) in lane_steps:
            status, detail, output = run_step_captured(name, requires, cmd, lenient)
            with lock:
                print("\n=== {} : {} ===".format(name, " ".join(cmd)), flush=True)
                if output:
                    print(output, end="" if output.endswith("\n") else "\n", flush=True)
                print("  {:5} {:16} {}".format(status, name, detail), flush=True)
                results[idx] = (name, status, detail)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=min(jobs, len(lanes))
    ) as pool:
        for future in [pool.submit(run_lane, ls) for ls in lanes.values()]:
            future.result()  # propagate, never swallow, a runner failure
    return [results[i] for i in sorted(results)]


def _clear_stale_coverage_report(plan):
    """Run-scope the coverage report: if this plan runs the tests+coverage step,
    the coverage.json it may (re)write is THIS run's output, so clear a stale copy
    first (COVERAGE_JSON). At a covered tier tests+coverage rewrites it fresh; at
    the smoke tier (no --cov-report=json) it stays absent, so a
    [step:module-coverage] consumer correctly SKIPs instead of grading a stale
    full-tier measurement (repo-review 2026-07-22 REVIEW-A). A locked/undeletable
    stale report is a LOUD failure — it must not silently survive into a consumer
    as a false green (the fail-closed stance)."""
    if not any(s[0] == "tests+coverage" for s in plan):
        return
    try:
        COVERAGE_JSON.unlink(missing_ok=True)
    except OSError as exc:
        sys.exit(
            "check: could not clear stale coverage report {}: {}".format(
                COVERAGE_JSON, exc
            )
        )


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # THE CLI CONTRACT, OI-21 break 1. `choices=` deliberately lists the retired
    # tags TOO, because argparse rejects an out-of-choices value before any code of
    # ours runs — so an adopter's `--gate G2` dies with a bare argparse usage  check_vocab: allow
    # error naming no migration. Listing them lets `_resolve_bar_alias` translate
    # and explain instead. The `metavar` keeps `--help` teaching only the canonical
    # form, so the aliases are reachable without being advertised.
    # `--stage-cleared` is the canonical spelling (owner ruling 2026-08-18): the
    # VALUE is a stage token on the one vocabulary, so the FLAG has to say which
    # reading of that token it means — the stage being CLEARED, not the stage the
    # repo is in. `--gate` stays accepted, unadvertised and silent: it is a flag
    # name an adopter's hooks, CI and launchers pass literally, the word "gate"
    # was never retired where it means a check that can fail, and `docs/gate` /
    # `derive_gate.py` keep their names by the same ruling.
    ap.add_argument(
        "--stage-cleared",
        "--gate",
        dest="gate",
        choices=GATES + list(RETIRED_BAR_ALIASES),
        metavar="{" + ",".join(GATES) + "}",
        default=None,
        help="the stage whose bar to run — the stage being CLEARED, not the one "
        "in work (default: the derived value in docs/gate, else all). The "
        "retired G1/G2/G3 and DevBar-* spellings are accepted as aliases and "  # check_vocab: allow
        "warn; `--gate` is accepted silently as the prior flag name.",
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
        help="delivery phase(s) in scope, e.g. v1 or v1,v2 — scopes the DevStg-Impl "
        "approval criterion to that phase (process.md §4 'Phased delivery')",
    )
    ap.add_argument(
        "--lenient",
        action="store_true",
        help="treat missing tools as SKIP (local dev only)",
    )
    ap.add_argument(
        "--trunk-lane",
        action="store_true",
        help="run the generated-artifact freshness gates even on a claimed "
        "work branch — the station refresh's bar (integrate.py refresh), where "
        "the branch tree IS the tree that becomes trunk",
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
    ap.add_argument(
        "--run-steps",
        metavar="NAMES",
        default=None,
        help="run the named steps (comma-separated, e.g. 'arch-map,okf') "
        "concurrently with the same lenient semantics as --run-step, reporting "
        "every step's result — so a commit with several stale artifacts names "
        "them all in one pass (the pre-commit hook's batched floor); exits 1 "
        "if any step FAILs",
    )
    ap.add_argument(
        "--jobs",
        type=int,
        default=None,
        metavar="N",
        help="run the plan's steps concurrently on N workers (0 = one per "
        "step); every step is read-only or writes a distinct artifact, except "
        "the two trace.py steps, which share a lane. Default 1: sequential, "
        "with each step's output streamed live exactly as before",
    )
    args = ap.parse_args()
    global _FORCE_TRUNK_LANE
    _FORCE_TRUNK_LANE = args.trunk_lane
    # check.py resolves docs/gate, docs/stack.ini, and docs/architecture.md
    # relative to the CWD (unlike the sibling scripts, which take --root). Run it
    # anywhere but the repo root and it would silently see no profile and no gate
    # — falling back to the built-in commands and gate `all`, i.e. a different,
    # stricter-or-weaker plan rather than an error. Anchor that invariant loudly:
    # the whole plan assumes a docs/ tree at CWD, so refuse to run without one
    # instead of diverging quietly (deep-review-2026-07-12b M2 / WI-100).
    if not Path("docs").is_dir():
        sys.exit(
            "check: must run at the repo root — no docs/ directory in {} "
            "(the gate, stack profile, and arch-map reads are CWD-relative)".format(
                Path.cwd()
            )
        )
    # Translate a retired `--gate G2` (warning once) before anything consumes it,  check_vocab: allow
    # so `resolve_gate` and `_step_gate` both see only canonical bar names.
    args.gate = (
        _resolve_bar_alias(args.gate, "--stage-cleared") if args.gate else args.gate
    )
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

    # Parallel-run lane map: built-in write-write lanes + each [step:] `lane =`
    # declaration, validated (a typo fails loudly, never silently re-races a step
    # under --jobs>1). Factored out to keep main() under its complexity baseline.
    lane_map = _resolve_lane_map(profile, coverage, args.tier, args.phase)

    # Run one named step and exit (the hook's format delegation). Search the
    # unfiltered plan so a gate-scoped step (format is DevStg-Impl-only) is still found,
    # and be lenient about a missing tool so a not-yet-set-up repo can commit —
    # a real failure still exits nonzero.
    step_gate = _step_gate(args.gate)  # explicit --gate gates; defaulted = "all"
    if args.run_step:
        all_steps = steps(coverage, args.tier, step_gate, args.phase, profile)
        match = [s for s in all_steps if s[0] == args.run_step]
        if not match:
            sys.exit("check: no step named {!r}".format(args.run_step))
        name, requires, cmd, _gates, _layer = match[0]
        status, detail = run_step(name, requires, cmd, lenient=True)
        print("  {:5} {:16} {}".format(status, name, detail))
        missing_tool_banner(
            _skipped_product_steps([(name, status, detail)], {name: match[0]})
        )
        sys.exit(1 if status == "FAIL" else 0)

    # The batch form of --run-step (the hook's floor in ONE interpreter spawn):
    # resolve each name from the full plan, run them concurrently (they are
    # independent freshness/integrity checks), and — unlike a `set -e` chain of
    # single steps — report EVERY failure, so a commit with several stale
    # artifacts names them all at once instead of one per attempt. Same lenient
    # semantics as --run-step (a missing tool is SKIP, exit 0).
    if args.run_steps:
        names = [t.strip() for t in args.run_steps.split(",") if t.strip()]
        if not names:
            sys.exit("check: --run-steps got no step names")
        all_steps = steps(coverage, args.tier, step_gate, args.phase, profile)
        by_name = {s[0]: s for s in all_steps}
        unknown = [n for n in names if n not in by_name]
        if unknown:
            sys.exit("check: no step named {}".format(", ".join(map(repr, unknown))))
        jobs = args.jobs if args.jobs is not None else 0
        results = run_plan(
            [by_name[n] for n in names],
            lenient=True,
            jobs=jobs or len(names),
            lane_map=lane_map,
        )
        missing_tool_banner(_skipped_product_steps(results, by_name))
        sys.exit(1 if any(status == "FAIL" for _n, status, _d in results) else 0)

    all_for_gate = steps(coverage, args.tier, gate, args.phase, profile)
    plan = [s for s in all_for_gate if gate == "all" or gate in s[3]]
    # The higher gate's OWN table, not a filter of this one — see advisory_plan.
    advisory = advisory_plan(
        gate, plan, lambda g: steps(coverage, args.tier, g, args.phase, profile)
    )

    if args.list:
        print("Plan for gate {} (tier {}):".format(gate, args.tier))
        _print_steps(plan)
        # The advisory tier is part of what this invocation WILL run, so --list
        # must show it or the option lies (128-REVIEW-A MINOR 5: a real window
        # listed only the weaker DevStg-Tests traceability while the run executed the DevStg-Impl
        # one). Marked, and separated, so it cannot be read as the bar.
        if advisory:
            print(
                "\nAdvisory during the open ratification window "
                "(reported, NOT gating — the exit code is not affected):"
            )
            _print_steps(advisory)
        return

    if not plan:
        print("No checks defined for gate {}.".format(gate))
        return

    # Run-scope the coverage report before the plan (see the helper): a stale,
    # gitignored coverage.json must never be graded as this run's output.
    _clear_stale_coverage_report(plan)

    jobs = args.jobs if args.jobs is not None else 1
    if jobs == 0:
        jobs = len(plan)
    results = run_plan(plan, args.lenient, jobs, lane_map)

    advisory_results = run_advisory(advisory, jobs, lane_map)

    print("\n" + "=" * 56)
    print("Check summary (gate {}, tier {}):".format(gate, args.tier))
    # One loop over both tiers. Advisory rows carry their marker in the DETAIL
    # column — never the bare status word, because an "ADVISORY FAIL" that reads
    # like a FAIL in a scanned log is how a warn-only tier is mistaken for the bar.
    for name, status, detail in list(results) + [
        (n, st, "{} [advisory — not gating]".format(d)) for n, st, d in advisory_results
    ]:
        print("  {:5} {:16} {}".format(status, name, detail))
    failed = [r for r in results if r[1] == "FAIL"]
    print("=" * 56)
    if failed:
        print("RESULT: FAIL ({} step(s) failed)".format(len(failed)))
        sys.exit(1)
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
