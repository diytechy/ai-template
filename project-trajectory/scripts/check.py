#!/usr/bin/env python3
"""The check harness — one command that runs every quality gate locally and in CI.

Stack-agnostic kit, **Python reference implementation**. This is the runnable
version of the "harness contract" in `process.md §7`: format · lint · tests ·
coverage · derived-stage freshness · traceability · doc-navigability · perf-budgets
· work-item trajectory. Wire it to your stack in ONE declared file, `docs/stack.ini`: swap
the format/lint/test commands + `src`/`tests` paths (the "EDIT FOR YOUR STACK"
block just under the imports is the identical built-in fallback), and add any
project-specific gate as a `[step:<name>]` section (see extra_steps) — so this
file stays take-wholesale across a kit re-sync. The contract is the *gates and
exit code*, not the specific tools. For a non-Python project, replace the
format/lint/test commands with your own (or drop the ones you don't have); keep
the traceability/flows/doc-navigability/perf-budgets steps — they're
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
    - **Stage-scoped, at or above.** `--stage DevStg-Tests` runs every step whose
      declared threshold that rung is at or above. The default is the repo's
      DERIVED effective stage (`docs/stage`), which is computed over the SETTLED
      spine — so drafting a requirement can never drop a check that was running.
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
    python scripts/check.py [--stage DevStg-Needs|...|DevStg-Release|all] [--tier smoke|full|release|all]
                            [--coverage N] [--phase LIST] [--lenient] [--list]
                            [--jobs N] [--run-step NAME] [--run-steps A,B,...]
                            [--staged-divergence [--strict]]

    --stage     The rung the repo is IN. Every step whose declared threshold
                this rung is AT OR ABOVE runs — "when is it relevant to run
                these checks", not "what did I pass that permits them" (OI-51).
                Default: the repo's **derived effective stage** from
                `docs/stage`, computed by derive_stage.py over the SETTLED spine
                and never hand-set; `all` when no stage file exists. This keeps a
                young project's CI green-and-honest: it enforces what the project
                has reached, not the end-state. From DevStg-Impl on, traceability
                also requires every Verification=Test SR to be Status=Approved
                (trace.py --require-verified). `--gate` is the accepted prior
                spelling; `--stage-cleared` is accepted and warns.
    --tier      Which test tier to run (default: all). Mark fast critical-path
                tests @pytest.mark.smoke and expensive ones @pytest.mark.release
                (markers registered in pytest.ini); leave ordinary tests unmarked —
                they run in the full/release tiers automatically.
    --coverage  Line-coverage threshold percent (default: 80; see COVERAGE_THRESHOLD).
                Enforced for the full/release/all tiers, not smoke.
    --lenient   Treat missing tools as SKIP instead of failure (local dev only).
    --list      Print the step plan for the stage and exit; each step is tagged
                [process] (kit-owned, stdlib, identical everywhere) or [product]
                (language-specific — you wire it to your stack). See process.md
                §7 "process vs product checks".
    --run-step  Run just one named step (e.g. `format`) and exit with its
                status; a missing tool is SKIP (exit 0), a real failure exit 1.
                The pre-commit hook uses it to source its format check from the
                declared profile rather than restating the command.
                An explicit --stage builds the step AT that rung (else `all`).
    --run-steps Run several named steps concurrently with --run-step's lenient
                semantics, reporting EVERY step's result (exit 1 if any FAILs) —
                the pre-commit hook's batched freshness/integrity floor, one
                interpreter spawn instead of a chain that stops at the first
                stale artifact.
    --staged-divergence
                Run only the OI-31 detector: which declared `[generated]`
                artifact is modified in the worktree but absent from the index?
                Every freshness step here reads the tree ON DISK, so a
                regenerated-but-unstaged artifact passes them all and lands
                stale. Warn-only (exit 0) unless --strict; skips cleanly off
                git. It does NOT catch an artifact staged while stale.
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
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# THE SHIPPED SHARED-HELPER PACKAGE (owner ruling D-8, `OI-16`, executed
# WI-448): the best-effort-off-git subprocess pattern this module used to spell
# out itself. Run as a subprocess this script's own dir is sys.path[0] so a
# plain import resolves; the guard covers an in-process import (a test) whose
# sys.path does not yet carry scripts/.
try:
    from kitlib import git as _kitgit
    from kitlib import ladder as _kitladder
    from kitlib import stage as _kitstage
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import git as _kitgit
    from kitlib import ladder as _kitladder
    from kitlib import stage as _kitstage

# Resolve sibling scripts relative to *this file*, not the cwd. A repo whose
# existing directory is named "Scripts/" (NTFS case-preserving, POSIX case-
# sensitive) would break the old "scripts/trace.py" cwd-relative strings on
# Linux CI even though Windows never notices the mismatch.
_SCRIPTS = Path(__file__).resolve().parent


# ============================ EDIT FOR YOUR STACK ============================
# PREFER `docs/stack.ini` (Thread 30): declaring the toolchain there keeps CI,
# the hook, and setup.* reading one source. The constants + built-in command
# templates below are the FALLBACK used when no profile file exists — a
# profile-less repo runs exactly these. Keep them and the scaffolded stack.ini
# in step: the reference profile declares these same values. The traceability,
# design-flows steps are stdlib-only and stack-agnostic (kept
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
        "derived-stage",
        "registry-integrity",
        "traceability",
        "vocabulary",
        "need-form",
        "privacy",
        "doc-navigability",
        "perf-budgets",
        "design-flows",
        "trajectory",
        "backlink-coverage",
        "trajectory-map",
        "status-map",
        "open-items",
        "okf",
        "ratify-fresh",
        "skills-sync",
        "skills-index",
        "prompt-catalog",
        "staged-divergence",
        "ratify-immutable",
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
        command    = {py} scripts/check_capabilities.py {src}  # required
        from-stage = DevStg-Impl                      # optional, default DevStg-Impl
        layer      = product                          # optional, default product
        lane       = tests+coverage                   # optional (see below)

    `from-stage` is the rung the step becomes RELEVANT at and the step runs
    whenever the repo is at or above it (see _step_threshold; the retired
    `gates =` membership list still translates).

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
        threshold = _step_threshold(profile, section)
        layer = profile.get(section, "layer", fallback="product").strip() or "product"
        if layer not in ("process", "product"):
            sys.exit(
                "check: docs/stack.ini [{}] layer is {!r}; expected "
                "process|product".format(section, layer)
            )
        out.append((name, _requires(cmd), cmd, threshold, layer))
    return out


# THE LEGACY `gates =` TRANSLATION, and it preserves an adopter's effective
# behavior rather than the tag's face value (WI-498 slice 2). A `gates =` list
# named the BARS a step ran at, and the bar was a MIN over every in-scope row:
# `DevStg-Reqs` is the floor every repo sits at, while `DevStg-Tests` was reached
# only by a spine already fully decomposed and TC'd — which is the DevStg-Impl
# RUNG — and `DevStg-Impl` was never reached at all under the OI-30 D2 ceiling.
# So the rung that reproduces each listed bar under an at-or-above rule is:
_LEGACY_BAR_THRESHOLD = {
    _kitladder.STAGE_REQS: _kitladder.STAGE_NEEDS,
    _kitladder.STAGE_TESTS: _kitladder.STAGE_IMPL,
    _kitladder.STAGE_IMPL: _kitladder.STAGE_IMPL,
}

# Sections already warned about, so the notice is ONCE PER RUN as promised and
# not once per `steps()` call — the plan is built two or three times in a single
# invocation (the lane map resolves at ALL; `--list` and the run each rebuild),
# and a migration notice repeated per rebuild reads as a malfunction.
_LEGACY_GATES_WARNED = set()


def _step_threshold(profile, section):
    """The rung a declared `[step:<name>]` becomes relevant at.

    `from-stage = <rung>` is the declared spelling: any of the eight ladder rungs,
    and the step runs whenever the repo is AT OR ABOVE it. Default `DevStg-Impl`,
    unchanged in value from the retired `gates =` default — a project-specific
    gate grades a built thing.

    `gates = <space/comma list>` IS ACCEPTED AND TRANSLATED, with one stderr line
    per run. It is the retired membership spelling, and unlike the `--stage` CLI
    aliases the FILE can be named here, so the notice says which section to fix
    rather than leaving an adopter to guess. The lowest listed bar picks the rung
    (`_LEGACY_BAR_THRESHOLD`); the retired `G1|G2|G3` tags translate first,  check_vocab: allow
    exactly as they always did. Both spellings at once is an authoring error and
    fails LOUDLY, like every other profile error — silently preferring one would
    make a step's real threshold unreadable from the file."""
    has_new = profile.has_option(section, "from-stage")
    has_old = profile.has_option(section, "gates")
    if has_new and has_old:
        sys.exit(
            "check: docs/stack.ini [{}] declares both `from-stage` and the "
            "retired `gates` — keep `from-stage` and delete `gates`".format(section)
        )
    if has_new:
        value = profile.get(section, "from-stage").strip()
        if value not in _kitladder.LADDER_RUNGS:
            sys.exit(
                "check: docs/stack.ini [{}] from-stage is {!r}; expected one of "
                "{}".format(section, value, "|".join(_kitladder.STAGE_ORDER))
            )
        return value
    if not has_old:
        return _kitladder.STAGE_IMPL
    bars = []
    for tok in profile.get(section, "gates").replace(",", " ").split():
        tok = RETIRED_STAGE_ALIASES.get(tok, tok)
        if tok not in _LEGACY_BAR_THRESHOLD:
            sys.exit(
                "check: docs/stack.ini [{}] gates has {!r}; expected a "
                "space/comma list of {}".format(
                    section, tok, "|".join(_LEGACY_BAR_THRESHOLD)
                )
            )
        bars.append(tok)
    if not bars:
        return _kitladder.STAGE_IMPL
    threshold = min((_LEGACY_BAR_THRESHOLD[b] for b in bars), key=_kitladder.stage_ord)
    if section not in _LEGACY_GATES_WARNED:
        _LEGACY_GATES_WARNED.add(section)
        print(
            "check: docs/stack.ini [{}] uses the RETIRED `gates =` membership "
            "list — reading it as `from-stage = {}`. Selection is now AT OR "
            "ABOVE one rung (OI-51); update the section to say so.".format(
                section, threshold
            ),
            file=sys.stderr,
        )
    return threshold


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
# traceability / design-flows) or "product" (language-specific, you
# wire it to your stack: format / lint / tests). The empty-vs-nonempty `requires`
# tuple already implies the split; the layer tag formalizes and surfaces it (see
# process.md §7 "process vs product checks"). Edit commands to fit your stack;
# keep the gate tags and layers.
# Implements: SR-006, LLR-006, SR-170, LLR-141
def steps(coverage, tier, stage, phase=None, profile=None):
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
    # The traceability step runs from the DevStg-Impl rung on, where a spine's
    # every SR is decomposed and TC'd and placeholder rows must be gone, so
    # --no-placeholders is always on here (a fresh scaffold is exempt because
    # nothing above the floor runs against it). --html also regenerates the
    # scalable full-graph view (a gitignored composite artifact) every run.
    trace_cmd = [
        sys.executable,
        str(_SCRIPTS / "trace.py"),
        "--strict",
        "--no-placeholders",
        "--html",
    ]
    if at_or_above(
        stage, _kitladder.STAGE_IMPL
    ):  # the Impl criterion: test-verifiable SRs are Approved
        trace_cmd.append("--require-verified")
        trace_cmd.append(
            "--strict-schema"
        )  # DevStg-Impl: required fields + valid enums
        if (
            phase
        ):  # phased delivery: close DevStg-Impl for this phase only (process.md §4)
            trace_cmd += ["--phase", phase]
    # Arch-map mode from the profile ([arch-map] mode = symbols|files): a
    # non-Python stack declares `files`, which tells the AST-inventory readers
    # (check_trajectory / the dashboard / check_doc_refs' sym: tier — WI-455)
    # there is no Python source to scan, so their layers stay dormant instead
    # of passing vacuously. Invalid values fail loudly, like every other
    # profile error, even though no step here consumes the mode directly
    # anymore (the committed-map freshness step retired with
    # docs/architecture.md).
    arch_mode = _pget(profile, "arch-map", "mode", "symbols")
    if arch_mode not in ("symbols", "files"):
        sys.exit(
            "check: docs/stack.ini [arch-map] mode is {!r}; expected "
            "symbols|files".format(arch_mode)
        )
    # The trajectory validator gains --strict from the DevStg-Impl rung on — it
    # promotes the status↔registry coherence rules R-B…R-E from WARN to ERROR
    # (R-A always fails). ALL is deliberately EXCLUDED so the pre-commit floor,
    # which runs this step with NO --stage (so _step_stage resolves it to ALL),
    # stays warn-first: a plain commit must not block on status.md/SpecRef drift,
    # only on the R-A handoff-incoherence rule (process-options.md "Trajectory /
    # work-items layer").
    #   WHY THE RUNG IS Impl AND NOT Arch (WI-498 slice 2, recorded because the
    # mechanical translation of the retired tag gives the wrong answer). The old
    # condition was the DevStg-Tests/DevStg-Impl BAR, and the bar was a MIN over
    # every in-scope row — so it was reached ONLY by a spine already fully
    # decomposed and TC'd, which on the stage ladder is the Impl rung, not the
    # Arch rung that opens the bar's span. Keying on Arch would PROMOTE A
    # SEVERITY the owner ruled warn-first-until-mature, which is a policy change
    # and not a re-key. The rung the promotion has always effectively meant is
    # the rung it now names.
    # The retired-vocabulary enforcer (OI-21) rides check_trajectory's severity
    # ladder EXACTLY — same condition, same `if`, deliberately not a second one.
    # The reason is the same too: a repo mid-conversion must SEE every remaining
    # site without being blocked by it, while a repo past its requirements bar has
    # no excuse. "all" is excluded so the pre-commit floor (which passes no
    # --gate) stays warn-first for both.
    traj_cmd = [sys.executable, str(_SCRIPTS / "check_trajectory.py")]
    vocab_cmd = [sys.executable, str(_SCRIPTS / "check_vocab.py"), "--root", "."]
    # Reverse back-link coverage (OI-42 ruled (e), WI-486) rides the SAME
    # severity ladder, third of three, for the same reason: the number must be
    # visible at every commit and gate only where a repo past its requirements
    # bar has no excuse. It is vacuous while `[checks] backlink_coverage_min`
    # is 0, which is what the kit ships — the step then reports the percentage
    # and can never fail.
    backlink_cmd = [
        sys.executable,
        str(_SCRIPTS / "gen_arch_map.py"),
        "--backlink-coverage",
        "--root",
        ".",
        "--src",
        src,
    ]
    if stage != ALL and at_or_above(stage, _kitladder.STAGE_IMPL):
        traj_cmd.append("--strict")
        vocab_cmd.append("--strict")
        backlink_cmd.append("--strict-backlinks")
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
        ("format", _requires(fmt_cmd), fmt_cmd, _kitladder.STAGE_IMPL, "product"),
        ("lint", _requires(lint_cmd), lint_cmd, _kitladder.STAGE_IMPL, "product"),
        (
            "tests+coverage",
            _requires(test_cmd),
            test_cmd,
            _kitladder.STAGE_IMPL,
            "product",
        ),
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
            _kitladder.STAGE_NEEDS,
            "process",
        ),
        # THE FRESHNESS CONTRACT FOR THE DERIVED STAGE (WI-498 slice 1). Same
        # tags, same layer and the same trunk-lane stand-down as the registry
        # step above: `docs/stage` is derived from the registry rows by the
        # predicates in `spine_rules`, so a repo where the rows are guarded and
        # the cache is not would be a repo where the two can silently disagree.
        # It arrived beside a twin step over `docs/gate`, held in step so the
        # transitional dual state could not diverge; slice 5 deleted that file,
        # its readers and its `derived-gate` step, leaving this one alone.
        (
            "derived-stage",
            (),
            [sys.executable, str(_SCRIPTS / "derive_stage.py"), "--check"],
            _kitladder.STAGE_NEEDS,
            "process",
        ),
        # THE THRESHOLD IS THE Impl RUNG, AND IT IS NOT A CHOICE (WI-498 slice 2).
        # `--strict` fails on ORPHANS, and the two orphan rules — "SR has no LLR"
        # and "SR has no test" — are LITERALLY the predicates that hold a repo at
        # the LLReqs and Tests rungs (spine_rules.spine_stage). So this step
        # cannot be green below DevStg-Impl by construction: running it lower
        # would demand the output of the very rung the repo is standing on. The
        # retired tag said "from the DevStg-Tests BAR on", which under the bar's
        # min-fold meant a fully decomposed spine — the same repo, named by its
        # rung instead of by the bar that implied it.
        ("traceability", (), trace_cmd, _kitladder.STAGE_IMPL, "process"),
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
            _kitladder.STAGE_NEEDS,
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
            _kitladder.STAGE_NEEDS,
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
            _kitladder.STAGE_NEEDS,
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
            _kitladder.STAGE_NEEDS,
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
            _kitladder.STAGE_IMPL,
            "process",
        ),
        # Authored runtime-flow diagrams (process.md §3 "Design-time runtime
        # flows"): required from the DevStg-Tests RUNG on, so reviewers verify
        # behavior from the diagrams, not from registry rows.
        #   RUNG RESTORED TO WHAT THE STEP ALWAYS CLAIMED (WI-498 slice 2). The
        # comment has always said "from DevStg-Tests on" and the retired tag has
        # always MEANT something else — the bar's min-fold put this step's real
        # arrival at the Impl rung, one later. What the diagrams answer to is a
        # SETTLED decomposition, which is exactly what leaving the LLReqs rung
        # means, so the rung the author named is the honest one. A deliberate
        # one-rung widening, recorded rather than smuggled.
        (
            "design-flows",
            (),
            [sys.executable, str(_SCRIPTS / "check_flows.py"), "--no-placeholders"],
            _kitladder.STAGE_TESTS,
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
        # From the DevStg-Tests RUNG on, where execution planning has begun —
        # the same one-rung restoration as design-flows above, and for the same
        # reason: the tag named a bar that arrived a rung later than the sentence
        # beside it promised. Warn-first here; the --strict promotion keeps its
        # own, higher rung (see traj_cmd).
        (
            "trajectory",
            (),
            traj_cmd,
            _kitladder.STAGE_TESTS,
            "process",
        ),
        # Reverse back-link coverage (OI-42 ruled (e), WI-486): the share of
        # LIVE LLR rows named by a literal `Implements:` declaration under
        # [paths] src. The percentage is the progress bar a back-link campaign
        # has otherwise never had — it measures ADHERENCE rather than policing
        # the links that exist. REPORT-ONLY as shipped (the dial is 0), vacuous
        # on a repo with no LLR rows, and language-agnostic: it reads comment
        # TEXT, so it costs no parser in any stack.
        #   THE RUNG IS Impl, WHICH DIVERGES FROM THE OLD PLACEMENT ARGUMENT
        # ("beside the other spine-coherence steps") ON PURPOSE (WI-498 slice 2).
        # The artifact this step grades is not in the registries at all — it is a
        # literal `Implements:` declaration IN SOURCE. Source is what the Impl
        # rung means, so below it the percentage grades an artifact that does not
        # exist yet, and the declared minimum becomes a floor nobody could have
        # met. Adjacency in this table was never a reason to run.
        (
            "backlink-coverage",
            (),
            backlink_cmd,
            _kitladder.STAGE_IMPL,
            "process",
        ),
        # (The `arch-map` committed-map freshness step retired at WI-455:
        # the module map is DERIVED live from the source AST by its readers,
        # so there is no committed docs/architecture.md block left to drift.
        # gen_arch_map stays shipped for the opt-in AGENTS.md/CLAUDE.md map
        # routing; --strict-parse's parse tripwire rides your lint/test steps.)
        # Trajectory dashboard freshness (process-options.md "Trajectory /
        # work-items layer"): the generated-artifact freshness gate for
        # the root PROJECT_STATE.html — gen_trajectory.py --check regenerates in memory
        # and byte-compares. DevStg-Impl only (the
        # generated view churns while the plan is still forming). Vacuous on an
        # absent/placeholder-only registry and silent under
        # [checks] trajectory_check = false, so a repo without work items pays nothing.
        (
            "trajectory-map",
            (),
            [sys.executable, str(_SCRIPTS / "gen_trajectory.py"), "--check"],
            _kitladder.STAGE_IMPL,
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
            _kitladder.STAGE_IMPL,
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
            _kitladder.STAGE_IMPL,
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
            _kitladder.STAGE_IMPL,
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
        #   AT EVERY RUNG SINCE WI-498 slice 2, and the re-derivation is the
        # clearest case in the table. The question this step asks — "is the brief
        # a human is about to attest FROM still the brief the registry supports?"
        # — is asked at the moment of an ATTESTATION, and attestation happens at
        # every rung of the ladder, not only near the end of it. The old
        # `{DevStg-Tests, DevStg-Impl}` tag put it out of reach for exactly the
        # repos that attest most often: an early one, whose derived bar sits at
        # the floor for the whole of its requirements work. Doubly self-arming
        # already, so a repo with no brief still pays nothing.
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
            _kitladder.STAGE_NEEDS,
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
            _kitladder.STAGE_IMPL,
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
        # behaved oddly. That is `derived-stage`'s shape (an artifact the
        # machinery's own honesty rests on), not the dashboards'. The concrete
        # case this was written against — a repo pinned at the lowest reading for
        # the whole duration of a ratification window, so a `DevStg-Impl` step
        # never ran in its own CI — is the collapse `docs/stage` removes by
        # deriving over the SETTLED spine; the ARGUMENT for the tag survives it.
        (
            "skills-index",
            (),
            skills_index_cmd,
            _kitladder.STAGE_NEEDS,
            "process",
        ),
        (
            "prompt-catalog",
            (),
            prompt_catalog_cmd,
            _kitladder.STAGE_NEEDS,
            "process",
        ),
        # Staged-vs-worktree divergence (OI-31, ruled option (b) 2026-08-18):
        # every step above asks whether the artifact ON DISK matches its
        # regeneration; this one asks whether the artifact on disk is the one
        # about to be COMMITTED — see staged_divergence() for the detector, its
        # degradation, and the gap it does NOT close. Three WIRING decisions,
        # which live here because nothing else records them:
        #   PROMOTED TO AN ERROR by the `--strict` below (WI-498 close), on
        # OI-31's own trigger — "once it has run clean for a program". It ran
        # clean for this one, and the close's review measured what warn-only
        # costs (ROUND-SOL-RAW 1, CRITICAL): stage a registry edit, regenerate
        # `docs/stage`, forget the `git add`, and every freshness step passes on
        # bytes the commit does not contain. So the bar now vouches for the tree
        # being COMMITTED. The bare `--staged-divergence` stays warn-only: the
        # severity lives at the WIRING, where the ruling put it. Adopter-visible
        # and deliberate — a partially-staged commit that leaves a regenerated
        # artifact behind is refused (RESYNC_PACK entry, this program).
        #   AT EVERY BAR, like vocabulary/need-form: the question is about the
        # commit in front of you, which a DevStg-Reqs repo makes exactly as often
        # as a DevStg-Impl one. Deliberately NOT in _TRUNK_FRESHNESS_STEPS either:
        # that stand-down exists because a work branch must not COMMIT a
        # regenerated artifact, and this step never demands one — it reports
        # what the tree already diverges on, which is as true on a branch.
        (
            "staged-divergence",
            (),
            [
                sys.executable,
                str(_SCRIPTS / "check.py"),
                "--staged-divergence",
                "--strict",
            ],
            _kitladder.STAGE_NEEDS,
            "process",
        ),
        # Re-attestation brief immutability (WI-503). A sibling of
        # staged-divergence above, same shape and same reason for AT EVERY BAR
        # / NOT in _TRUNK_FRESHNESS_STEPS: it reads the staged tree rather than
        # a regenerated artifact's freshness, so it is as true on a work branch
        # as on trunk, and it never demands a regeneration — only that an
        # already-committed dated brief stays byte-identical. Fail-closed with
        # no --strict switch: unlike staged-divergence, there is no honest
        # warn-first state for "a historical record just got rewritten".
        (
            "ratify-immutable",
            (),
            [
                sys.executable,
                str(_SCRIPTS / "check.py"),
                "--ratify-immutable",
            ],
            _kitladder.STAGE_NEEDS,
            "process",
        ),
    ]


# --- THE STAGE AXIS: SELECTION IS AT-OR-ABOVE (OI-51, ruled 2026-08-21) --------
# THE OWNER'S RULE, and this module is what it re-keys: a step runs because the
# repo IS AT OR ABOVE the rung that step becomes relevant at — *"when is it
# relevant for me to run these checks"* — never because some earlier bar was
# cleared. The eight-rung vocabulary is `kitlib.ladder`'s (one home since WI-498
# slice 0) and the EFFECTIVE stage is `docs/stage`'s (slice 1), so this module
# declares NEITHER. It declares only the CLI's one extra token and the comparison
# every selection routes through.
#
# WHAT RETIRED HERE, AND WHY IT WAS NOT A RELABEL. `BAR_REQS`/`BAR_TESTS`/
# `BAR_RELEASE`, `BAR_ORDER`, `GATES` and `bar_ord` are gone with the set-
# MEMBERSHIP rule they served. The bar was a MIN over every in-scope row, so
# `DevStg-Tests` was only ever reached by a spine that was ALREADY fully
# decomposed and TC'd, and `DevStg-Impl` was never reached at all under the OI-30
# D2 ceiling — which is why the three product steps tagged for it never ran from
# a derived value. That is OI-51's defect. Keying on a rung a settled spine
# actually reaches is what fixes it; the per-step thresholds and the reasoning
# for each are in `steps()`.
ALL = "all"

# The CLI's one non-rung token: run EVERY step whatever the repo's stage. It is
# not a rung and never compares as one (`at_or_above` short-circuits on it), so
# it can neither be written to `docs/stage` nor sorted onto the ladder.
STAGES = list(_kitladder.STAGE_ORDER) + [ALL]

# THE RETIRED-TAG ALIASES (check_vocab: allow-file is NOT used — only these
# declaration lines are marked). `--gate G2` is a string an adopter's hook  check_vocab: allow
# and CI workflow pass LITERALLY, so refusing it would break every adopter's
# pipeline at the re-sync — and this kit's own rule is that a breaking change to
# a downstream-visible CLI needs a migration, not a cliff. So the retired tags
# are ACCEPTED here and WARNED about (`_resolve_stage_alias` prints the canonical
# form to stderr once per run).
#
# WHY WARNED RATHER THAN SILENT OR REFUSED. Silent acceptance is how the retired
# vocabulary grows back — the tags would live in adopters' hooks forever with
# nothing ever telling anyone. Refusal breaks working pipelines for a vocabulary
# change. A warning is the only posture that both keeps the pipeline green and
# guarantees the operator is told; it costs one stderr line per run and it stops
# the moment the hook is updated. The AUTHORED surface (docs/stack.ini's
# per-step threshold) translates with its own one-line notice instead, because
# there the FILE can be named.
#
# A THIRD ALIAS GENERATION IS NOT OWED, which the census expected to be. The
# three bar spellings are all rungs on the ladder, so an adopter passing
# `DevStg-Tests` keeps a legal value — what changed is the READING (the repo is
# at that rung, rather than that bar must next be cleared), and a reading is
# migrated by the RESYNC note, not by a translation table.
# THE VALUES ARE ARRIVAL RUNGS, BY MEANING — never the same-spelled rung
# (corrected at the WI-498 close, ROUND-OPUS 8). A retired tag names a BAR the
# repo had CLEARED, and the bar was a MIN over every in-scope row, so the rung a
# repo at that bar had actually reached is what the tag translates to. That is
# the same by-meaning rule `_LEGACY_BAR_THRESHOLD` states for `gates =` lists
# and the same one the phase-anchor grammar uses; this table was the one place
# taking the SPELLING.
#
# WHAT IT COST, driven: `--gate G2` resolved to `DevStg-Tests` and produced a
# 12-step plan where the equivalent arrival (`DevStg-Impl`) produces 26. The 14
# steps that silently dropped out included `traceability`, `tests+coverage`,
# `lint`, `format` and `backlink-coverage` — so an adopter's CI passing
# `--gate G2` literally (the exact case the silent-`--gate` concession exists to
# protect) stayed green while quietly stopping most of its checks.
#
# COMPOSITION IS UNCHANGED for `gates =` step lists: `_step_threshold` maps
# through this table and then through `_LEGACY_BAR_THRESHOLD`, and every entry
# below lands on the same threshold it did before (Impl -> Impl, Reqs -> Needs).
# Only the CURRENT-STAGE direction moves, which is the one that was wrong.
RETIRED_STAGE_ALIASES = {  # check_vocab: allow
    # The Reqs bar IS the floor every repo sits at.
    "G1": _kitladder.STAGE_REQS,  # check_vocab: allow
    # The Tests bar was reached ONLY by a spine already fully decomposed and
    # TC'd, which on the ladder is the DevStg-Impl RUNG — three above the word
    # it shares with the bar.
    "G2": _kitladder.STAGE_IMPL,  # check_vocab: allow
    "G3": _kitladder.STAGE_IMPL,  # check_vocab: allow
    # The `DevBar-*` prefix, retired 2026-08-18. `DevBar-Release` resolves to
    # `DevStg-Impl`, NOT to `DevStg-Release`: that bar never certified the
    # Release rung, and the alias carries the correction.
    "DevBar-Reqs": _kitladder.STAGE_REQS,  # check_vocab: allow
    "DevBar-Tests": _kitladder.STAGE_IMPL,  # check_vocab: allow
    "DevBar-Release": _kitladder.STAGE_IMPL,  # check_vocab: allow
}


def at_or_above(current, threshold):
    """THE ONE COMPARISON EVERY SELECTION IN THIS MODULE ROUTES THROUGH: is a
    repo at rung `current` at or above the rung `threshold` becomes relevant at?

    `ALL` is above everything BY DEFINITION rather than by ordinal — it is the
    CLI's "run the lot", not a rung, and ordering it would mean putting it on a
    ladder it is not on. Both rung arguments go through
    `kitlib.ladder.stage_ord`, which RAISES on an unknown label instead of
    degrading to a default: an unrecognized rung means the ladder moved under a
    cached value, and a silent default here would silently change which checks
    run."""
    if current == ALL:
        return True
    return _kitladder.stage_ord(current) >= _kitladder.stage_ord(threshold)


def _resolve_stage_alias(value, what):
    """Translate a retired `G1`/`G2`/`G3` tag to a canonical rung, warning once.  check_vocab: allow
    Anything else passes through untouched for the caller's own validation.

    THE WARNING NAMES THE TRANSLATION'S DIRECTION, because the value moving is
    the thing an operator most needs to see (ROUND-OPUS 8): the tag translates
    BY MEANING, so a bar-era value can resolve to a rung several above the word
    it shares with the ladder, and the plan the run executes changes with it.
    The old text reported only the re-reading and said nothing about the plan,
    so an adopter's pipeline could shrink by fourteen steps behind one line of
    reassurance."""
    v = (value or "").strip()
    if v in RETIRED_STAGE_ALIASES:
        canonical = RETIRED_STAGE_ALIASES[v]
        note = (
            ""
            if canonical == v.replace("DevBar-", "DevStg-")
            else (
                " NOTE: that is NOT the same-spelled rung — a retired tag named "
                "a BAR the repo had CLEARED, and the bar was a MIN over every "
                "in-scope row, so it translates to the rung a repo at that bar "
                "had actually REACHED. The plan is the one for {!r}, which runs "
                "every step at or above it; `--list` shows exactly which."
            ).format(canonical)
        )
        print(
            "check: {} {!r} uses the RETIRED gate vocabulary — reading it as {!r}. "
            "The tags retired at OI-21; update to the stage-ladder rung names "
            "({}).{}".format(
                what, v, canonical, "|".join(_kitladder.STAGE_ORDER), note
            ),
            file=sys.stderr,
        )
        return canonical
    return v


# The one prior flag spelling that makes a CLAIM about the axis, and therefore
# the one that warns (`--gate` does not — see the argparse block for why the two
# postures differ). argparse records only the DEST, never which spelling reached
# it, so this reads argv directly; both `--stage-cleared X` and
# `--stage-cleared=X` forms count.
_RETIRED_FLAG = "--stage-cleared"


def _warn_retired_flag_spelling(argv=None):
    """One stderr line when the run was invoked with `--stage-cleared`."""
    args = sys.argv[1:] if argv is None else argv
    if not any(a == _RETIRED_FLAG or a.startswith(_RETIRED_FLAG + "=") for a in args):
        return False
    print(
        "check: `{0}` names the RETIRED bar reading — reading it as `--stage`, "
        "the rung the repo is IN, which selects every step at or above it "
        "(OI-51). Update the flag; the value spellings are unchanged.".format(
            _RETIRED_FLAG
        ),
        file=sys.stderr,
    )
    return True


# --- THE DERIVED STAGE, READ THROUGH THE COMMON READER ------------------------
# `docs/stage` is the stage axis's committed record (WI-498 slice 1) and
# `kitlib.stage.read_stage` is the ONE reader the ruled plan §3 puts every
# consumer behind: it recomputes the fingerprint of the declared derivation
# inputs on every call, returns the recorded record only while it still holds,
# and otherwise derives fresh IN MEMORY. So this module can no longer select a
# plan from a stale value — including on a claimed work branch, where the
# freshness step is deliberately stood down (`_TRUNK_FRESHNESS_STEPS`) and a
# green run over a stale cache used to be reachable.
#
# `docs/gate` IS GONE (WI-498 slice 5). The file, its producer's writer half,
# its `derived-gate` freshness step and the three-value BAR axis it carried are
# all deleted, and the count of its readers went 6 -> 4 -> 0 across slices 2, 4
# and 5. The last four were the three DISPLAY readers (`traj_parse`,
# `traj_panels`, `traj_status`), which now render the stage vocabulary, and
# `agent_common.spine_stage_of` — not display at all, but the input to
# `human_holds`, i.e. RATIFICATION AUTHORITY — which now comes through the common
# reader above. That one is why the freshness step could not retire earlier: a
# stale value there decides who may ratify.
STAGE_FILE = Path(_kitstage.STAGE_FILE)


def _derive_stage(root):
    """The deriver `kitlib.stage.read_stage` calls on a fingerprint miss.

    The mechanism moved to `kitlib.stage.derive_via_subprocess` at slice 5, when
    `agent_common.spine_stage_of` became its second caller; what stays here is
    this module's FAILURE POLICY, which is the half that differs. A CLI that
    cannot establish the stage exits rather than selecting a guessed plan."""
    try:
        return _kitstage.derive_via_subprocess(_SCRIPTS, root)
    except _kitstage.DerivationError as exc:
        sys.exit("check: {} — or pass --stage explicitly".format(exc))


def resolve_stage(explicit, root="."):
    """The rung this invocation selects at: an explicit `--stage` wins; else the
    repo's derived EFFECTIVE stage; else `ALL`.

    `ALL` WHEN THERE IS NO `docs/stage` — never a silently weaker rung. A repo
    that has not adopted the file gets the full plan, which is the same
    fail-closed direction the retired `resolve_gate` took for a missing
    `docs/gate`."""
    if explicit:
        return explicit
    if not (Path(root) / STAGE_FILE).exists():
        return ALL
    try:
        record = _kitstage.read_stage(Path(root), _derive_stage)
    except ValueError as exc:  # a hand-edited or cross-ladder value: fail loudly
        sys.exit("check: {}".format(exc))
    return record["stage"]


def resolve_plan(stage, coverage, tier, phase, profile):
    """Every step this invocation will run: the steps whose threshold this repo's
    stage is AT OR ABOVE.

    ONE TIER, WHERE THERE WERE THREE (WI-498 slice 2). The gating plan used to be
    followed by a PRODUCT-REGRESSION FLOOR (`floor_plan`, WI-473) that put back
    the product steps a drafted row had knocked out, and then by an ADVISORY tier
    (`advisory_plan`, owner ruling 2026-07-27) that re-ran warn-only whatever a
    ratification window had suppressed. Both existed for ONE reason: the derived
    BAR was a min over every in-scope row, so a single ordinary draft dropped it
    to what a fresh scaffold reads and steps silently stopped running.

    THE EFFECTIVE STAGE ABSORBS BOTH, by construction rather than by compensation.
    `docs/stage`'s headline value is derived over the SETTLED rows — drafts
    excluded, and a phase that has earned nothing ignored rather than folded in
    (`derive_stage`, slice 1) — so drafting a row cannot lower selection at all,
    for ANY step rather than only the product ones the floor covered. There is
    nothing left for the floor to restore and nothing left for the advisory tier
    to report on, so both retire here with the axis that needed them. What the
    advisory tier bought (a suppressed step still gets SEEN) the new selection
    delivers strictly more strongly: the step is not suppressed, so it GATES.

    Kept as its own function rather than folded back into `main()` for the stated
    reason it was extracted: `main()`'s C901 complexity is pinned to the digit by
    tests/test_complexity_ratchet.py, and this repo's rule is to decompose rather
    than re-stamp the ratchet."""
    plan = steps(coverage, tier, stage, phase, profile)
    return [s for s in plan if at_or_above(stage, s[3])]


def _print_steps(plan):
    """One `--list` line per step: name, layer, the rung it becomes relevant at,
    and the exact command.

    The threshold is printed as `>=DevStg-Arch` rather than as a bare label so a
    reader cannot mistake it for "this step belongs to that rung ALONE" — which is
    exactly what the retired membership tags meant, and the misreading the
    at-or-above rule exists to remove."""
    for name, _requires, cmd, threshold, layer in plan:
        print(
            "  - {:16} [{:7}] [>={}]  {}".format(name, layer, threshold, " ".join(cmd))
        )


def _step_stage(explicit):
    """The stage that BUILDS a --run-step/--run-steps command: an explicit
    --stage is honoured (so `--stage DevStg-Impl --run-steps trajectory` really
    gates), but a DEFAULTED one resolves to ALL, never the derived stage — the
    pre-commit hook passes no --stage and its floor must stay warn-first (see the
    trajectory step's comment). Name lookup stays unfiltered, so `format` is
    findable whatever rung the repo is on.

    A SECOND REASON SINCE THE RE-KEY, worth stating because it is a cost this
    default avoids: resolving the derived stage can now cost a subprocess
    (`_derive_stage`, on a fingerprint miss), and the hook's floor would pay it on
    every commit for a value it never consults."""
    return explicit or ALL


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
    "derived-stage trajectory-map status-map open-items okf ratify-fresh".split()
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


# stdout of a git command under `root`, or None on ANY failure (no git binary,
# not a repo, unknown rev/path, non-zero exit) — the house best-effort-off-git
# pattern. ONE HOME since WI-448 (`kitlib.git`): it was written out three times,
# in check.py, trace.py and trunk_step.py, each docstring pointing at the others
# as though one of them were the original. Kept under its own long-standing
# private name so no call site below moves.
_git_out = _kitgit.git_out


# --- staged-vs-worktree divergence (OI-31, ruled option (b) 2026-08-18) --------
# The gap this closes, in one sentence: the nine regenerate-and-byte-compare
# steps all resolve their artifact from the FILESYSTEM under --root, so their
# honest claim is "the artifact on disk matches its regeneration" while every
# reader takes it to mean "the artifact about to be committed does". Those
# diverge exactly when an author regenerates and forgets to `git add`.
# THE MEASURED INSTANCE: at 3b8d306d, PROJECT_STATE.html was modified in the
# worktree and absent from the index; the hook was honestly green on the tree on
# disk and the committed tree failed the very gate that guarded it — undetected
# until an adversarial review re-measured a log fragment's claim.


def _generated_census(root="."):
    """The `docs/stack.ini` `[generated]` paths — a READ of the §5.2 declaration,
    never a second copy of it.

    The artifact list this detector needs already exists and is already load-
    bearing (tests/test_generated_freshness_wiring.py reads this same section to
    prove every declared artifact has an enforcer), so copying it here would rot
    the day a tenth artifact is declared — the one real cost the ruling names
    against option (b), paid off by reading rather than restating.

    Keys are PATHS, so `optionxform = str`: configparser's default lowercasing
    would make `PROJECT_STATE.html` unmatchable — the same read, for the same
    reason, as integrate.py's `_generated_paths`. An absent or malformed profile
    declares nothing: this is a detector, and one that crashed on a file every
    other step tolerates would be a worse failure than the one it reports."""
    ini = Path(root) / "docs" / "stack.ini"
    if not ini.exists():
        return []
    cp = configparser.ConfigParser(interpolation=None)
    cp.optionxform = str
    try:
        cp.read_string(ini.read_text(encoding="utf-8-sig", errors="replace"))
    except (configparser.Error, OSError):
        return []
    if not cp.has_section("generated"):
        return []
    return [k.strip() for k in cp.options("generated") if k.strip()]


def _declared_generated(path, census):
    """True when `path` IS, or sits under, a declared `[generated]` entry — a
    trailing "/" marks a prefix row (docs/okf/, docs/ratify/), exactly as §5.2
    defines it. A marker-pair row (docs/status.md) matches on the FILE: the
    markers narrow which region is generated, not which file is committed."""
    return any(
        path.startswith(entry) if entry.endswith("/") else path == entry
        for entry in census
    )


def staged_divergence(root=".", strict=False):
    """Report every DECLARED generated artifact that is modified in the working
    tree but absent from the index, and return the exit code.

    THE HONEST GAP, stated here rather than discovered later: this does **not**
    catch an artifact that was STAGED WHILE STALE. The freshness steps read the
    working tree, so a stale blob added to the index passes them AND passes
    this. Closing that case needs the gates themselves to read the staged tree —
    OI-31 option (a), recorded as the destination and deliberately not taken now
    (it would convert nine scripts whose contract is "a pure function of a
    directory" into git-object readers, which is what makes the whole freshness
    tier testable against a temp scaffold). This step covers the shape that
    actually happened — a forgotten `git add` — and leaves the rarer one open.

    SEVERITY LIVES AT THE WIRING, not here: this entry point reports and exits
    0 unless `strict`, and the PLAN STEP passes `--strict` (steps(), OI-31's
    promotion taken at the WI-498 close). So the bare
    `check.py --staged-divergence` stays the detector an author runs mid-work,
    while the bar — hook floor and CI alike — refuses.

    DEGRADES, never crashes and never fails: no git binary, not a checkout, a
    root that is not the checkout's top level, or a failing git call each SKIP
    with the reason named. A detector that died in a scaffold would be removed
    from the floor, which is the same outcome as not having it."""
    census = _generated_census(root)
    if not census:
        print(
            "  SKIP  staged-divergence  docs/stack.ini declares no [generated] "
            "artifacts — nothing to compare against the index."
        )
        return 0
    top = _git_out(root, ["rev-parse", "--show-toplevel"])
    if top is None or not top.strip():
        print(
            "  SKIP  staged-divergence  no git, or {} is not a git checkout — "
            "there is no index to compare the worktree against.".format(
                Path(root).resolve()
            )
        )
        return 0
    try:
        at_top = Path(top.strip()).resolve() == Path(root).resolve()
    except OSError:  # pragma: no cover - an unresolvable path reads as "not top"
        at_top = False
    if not at_top:
        print(
            "  SKIP  staged-divergence  {} is not the top level of its git "
            "checkout ({}), so [generated] paths do not resolve against this "
            "index.".format(Path(root).resolve(), top.strip())
        )
        return 0
    # -z: NUL-separated and UNQUOTED, so a path with an unusual byte is compared
    # as itself rather than as git's C-quoted rendering of it (which would match
    # no census row and under-report silently).
    diff = _git_out(root, ["diff", "--name-only", "-z"])
    if diff is None:
        print(
            "  SKIP  staged-divergence  `git diff --name-only` failed — the "
            "worktree/index comparison could not be made."
        )
        return 0
    hits = sorted({p for p in diff.split("\0") if p and _declared_generated(p, census)})
    if not hits:
        print(
            "  ok    staged-divergence  none of the {} declared generated "
            "artifact paths is modified-but-unstaged.".format(len(census))
        )
        return 0
    print(
        "  {}  staged-divergence  {} declared generated artifact(s) modified in "
        "the working tree but NOT staged — the freshness steps just passed on "
        "bytes this commit will not contain:".format(
            "FAIL" if strict else "WARN", len(hits)
        )
    )
    for path in hits:
        print("      {}".format(path))
    print(
        "    Fix: `git add` them, then re-commit — or revert them. Leaving\n"
        "    them out is not free: the PLAN step runs --strict (OI-31's ruled\n"
        "    promotion, WI-498 close), so the bar vouches for the tree being\n"
        "    COMMITTED. This bare detector reports only.\n"
        "    GAP, so this is not read as a guarantee: it does NOT catch an\n"
        "    artifact that was STAGED WHILE STALE. The freshness gates read the\n"
        "    working tree, so a stale blob in the index passes them and passes\n"
        "    this. That case needs the staged-tree read (OI-31 option (a))."
    )
    return 1 if strict else 0


# --- WI-503: the re-attestation brief's immutability enforcer -----------------
# The defect this closes: `docs/ratify/<date>-*.md` is read as the record of
# what a human was shown at a sitting, but a regeneration used to find and
# rewrite whichever dated file was newest — ten rewrites on one file, none of
# them about the WI it was named for. The split (`current_ratify_brief`,
# `mint_ratify_brief` in trace.py) makes `docs/ratify/CURRENT.md` the only
# file a regeneration ever touches and `--mint-ratify-brief` the only thing
# that ever creates a dated one — but a CONVENTION with no enforcer rots the
# way the byte baselines did (the spec's own words). This is the enforcer: it
# reads the STAGED tree (what the commit is about to contain, exactly like
# `ratify_immutability`'s sibling `staged_divergence` reads the unstaged one)
# and refuses any status other than a plain ADD on an existing dated name.

_RATIFY_EXEMPT_NAMES = frozenset({"current.md", "readme.md"})


def _is_dated_ratify_brief(path):
    """True for a `docs/ratify/*.md` path that is neither the live surface
    (`CURRENT.md`) nor the directory's own README — i.e. a dated brief that,
    once committed, must never change again."""
    posix = path.replace("\\", "/")
    if not posix.startswith("docs/ratify/"):
        return False
    name = posix.rsplit("/", 1)[-1]
    return name.lower() not in _RATIFY_EXEMPT_NAMES


def ratify_immutability(root=".", strict=True):
    """Refuse a commit whose STAGED diff modifies or deletes an
    already-committed dated re-attestation brief. Returns the exit code.

    Reads `git diff --cached --name-status --no-renames -z` — the tree this
    commit is about to contain, not the working tree `staged_divergence`
    reads. `--no-renames` keeps a delete-and-recreate legible as its own two
    honest halves (D + A) rather than a single R that could hide a rewrite
    behind a fresh-looking status; a plain ADD (a brand-new dated filename,
    what `trace.py --mint-ratify-brief` ever produces) is the ONLY status this
    permits on a dated brief. `docs/ratify/CURRENT.md` and `README.md` are
    exempt — the live surface and the directory's own reference doc, neither
    of them history.

    FAIL-CLOSED BY DEFAULT (`strict=True`), unlike `staged_divergence`: there
    is no warn-first promotion path here, because the property this guards —
    "a dated brief never changes after the sitting it recorded" — has no
    honest partial-compliance state to warn through; every rewrite it lets
    through undermines the same "what did the human see" question the split
    exists to answer.

    DEGRADES like `staged_divergence`, for the same reason: no git, no
    checkout, wrong root, or a failing git call each SKIP with the reason
    named. A detector that died in a scaffold would be pulled off the floor,
    the same outcome as never having written it."""
    top = _git_out(root, ["rev-parse", "--show-toplevel"])
    if top is None or not top.strip():
        print(
            "  SKIP  ratify-immutable  no git, or {} is not a git checkout — "
            "there is no index to compare against.".format(Path(root).resolve())
        )
        return 0
    try:
        at_top = Path(top.strip()).resolve() == Path(root).resolve()
    except OSError:  # pragma: no cover - an unresolvable path reads as "not top"
        at_top = False
    if not at_top:
        print(
            "  SKIP  ratify-immutable  {} is not the top level of its git "
            "checkout ({}), so docs/ratify/ does not resolve against this "
            "index.".format(Path(root).resolve(), top.strip())
        )
        return 0
    diff = _git_out(root, ["diff", "--cached", "--name-status", "--no-renames", "-z"])
    if diff is None:
        print(
            "  SKIP  ratify-immutable  `git diff --cached` failed — the "
            "staged tree could not be inspected."
        )
        return 0
    tokens = [t for t in diff.split("\0") if t]
    # `--name-status -z` pairs a status token with a path token, in order.
    violations = []
    i = 0
    while i + 1 < len(tokens):
        status, path = tokens[i], tokens[i + 1]
        i += 2
        if not _is_dated_ratify_brief(path):
            continue
        if status != "A":
            violations.append((status, path))
    if not violations:
        print(
            "  ok    ratify-immutable  no staged change touches an existing "
            "dated docs/ratify/ brief."
        )
        return 0
    print(
        "  FAIL  ratify-immutable  {} dated re-attestation brief(s) staged "
        "with a change other than a plain add — a dated brief is IMMUTABLE "
        "once minted:".format(len(violations))
    )
    for status, path in violations:
        print("      {}  {}".format(status, path))
    print(
        "    Fix: revert the change to the existing dated file (`git restore "
        "--staged --worktree -- <path>`); regenerate the LIVE surface at "
        "`docs/ratify/CURRENT.md` instead (`trace.py --ratify modified --out "
        "docs/ratify/CURRENT.md`); mint a NEW dated brief with `trace.py "
        "--mint-ratify-brief SLUG` rather than editing an old one."
    )
    return 1 if strict else 0


def _ratify_immutable_mode(args):
    """The `--ratify-immutable` entry point, the same shape as
    `_divergence_mode`: EXIT with the detector's code when the flag selects
    it, else return and let main() build the ordinary plan."""
    if not args.ratify_immutable:
        return
    sys.exit(ratify_immutability("."))


def _divergence_mode(args):
    """The `--staged-divergence` entry point: EXIT with the detector's code when
    the flag selects it, else return and let main() build the ordinary plan.

    It runs before any plan is built — the detector reads docs/stack.ini itself
    (keys are paths, see _generated_census) and needs neither a gate nor a
    profile. `--strict` alone is REFUSED rather than ignored, so nobody reads a
    bare `--strict` as "make the whole plan strict" and gets a silently
    unchanged run.

    A helper rather than two `if`s in main() because main() sits at its
    complexity baseline and the ratchet's rule is to decompose, not re-stamp
    (tests/test_complexity_ratchet.py)."""
    if not args.staged_divergence:
        if args.strict:
            sys.exit(
                "check: --strict applies only to --staged-divergence today (the "
                "plan's severity comes from --stage)"
            )
        return
    sys.exit(staged_divergence(".", strict=args.strict))


def _claimed_work_branch(root):
    """The uncached answer behind `_work_branch` — see it for the contract.

    Implements: SR-006, SR-170, LLR-141
    """
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
    Returns (status, detail) where status in PASS/FAIL/SKIP.

    Implements: SR-006, LLR-006
    """
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
    # `--stage` IS THE CANONICAL SPELLING (OI-51, ruled 2026-08-21): the value is
    # the rung the repo is IN, and every step whose threshold that rung is at or
    # above runs. Two prior spellings stay accepted, with DIFFERENT postures for
    # a stated reason:
    #   `--gate` — SILENT, unchanged. It is the flag name an adopter's hooks, CI
    # and launchers pass literally (and, measured this slice, the only spelling
    # anything in this repo actually passes); the word "gate" was never retired
    # where it means a check that can fail; `spine_rules.py` keeps its name by
    # that same ruling (`docs/gate` did too, until slice 5 deleted the file).
    #   `--stage-cleared` — WARNS. Unlike `--gate` it makes a CLAIM about the
    # axis, and the claim is now the wrong one: it says the value is a bar being
    # cleared. That is the exact vocabulary trap OI-51 retires (it survived
    # inside the 2026-08-18 rename that was meant to remove it), so leaving it
    # silent would let the retired reading live on in adopters' pipelines with
    # nothing ever saying so. It keeps working — the three bar spellings are all
    # ladder rungs, so the value stays legal — and it says once per run what it
    # is now read as.
    ap.add_argument(
        "--stage",
        "--stage-cleared",
        "--gate",
        dest="stage",
        choices=STAGES + list(RETIRED_STAGE_ALIASES),
        metavar="{" + ",".join(STAGES) + "}",
        default=None,
        help="the rung the repo is IN: every step whose threshold this rung is "
        "AT OR ABOVE runs (default: the derived effective stage in docs/stage, "
        "else all). Drafting a row cannot lower it — the derivation reads the "
        "SETTLED spine — so there is no dial that turns product checks off by "
        "opening a ratification window. The retired G1/G2/G3 and DevBar-* "  # check_vocab: allow
        "value spellings are accepted as aliases and warn; `--gate` is accepted "
        "silently as the prior flag name, `--stage-cleared` warns.",
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
        help="run the named steps (comma-separated, e.g. 'okf,trajectory-map') "
        "concurrently with the same lenient semantics as --run-step, reporting "
        "every step's result — so a commit with several stale artifacts names "
        "them all in one pass (the pre-commit hook's batched floor); exits 1 "
        "if any step FAILs",
    )
    ap.add_argument(
        "--staged-divergence",
        action="store_true",
        help="run ONLY the staged-vs-worktree divergence detector and exit "
        "(OI-31): report every declared [generated] artifact modified in the "
        "worktree but absent from the index. Warn-only — exit 0 — unless "
        "--strict. This is the self-invoked body of the 'staged-divergence' "
        "step, not a separate contract",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="with --staged-divergence: exit 1 on a divergent artifact instead "
        "of warning. The ruled promotion path (OI-31: error 'once it has run "
        "clean for a program'); the step itself does NOT pass it today",
    )
    ap.add_argument(
        "--ratify-immutable",
        action="store_true",
        help="run ONLY the re-attestation-brief immutability enforcer and exit "
        "(WI-503): refuse a STAGED change (other than a plain add) to an "
        "existing docs/ratify/<date>-*.md. Fail-closed by default — no "
        "--strict, no warn mode. This is the self-invoked body of the "
        "'ratify-immutable' step, not a separate contract",
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
    # check.py resolves docs/stage and docs/stack.ini relative to the CWD
    # (unlike the sibling scripts, which take --root). Run it anywhere but the
    # repo root and it would silently see no profile and no stage — falling back
    # to the built-in commands and stage `all`, i.e. a different,
    # stricter-or-weaker plan rather than an error. Anchor that invariant loudly:
    # the whole plan assumes a docs/ tree at CWD, so refuse to run without one
    # instead of diverging quietly (deep-review-2026-07-12b M2 / WI-100).
    if not Path("docs").is_dir():
        sys.exit(
            "check: must run at the repo root — no docs/ directory in {} "
            "(the stage and stack-profile reads are CWD-relative)".format(Path.cwd())
        )
    _divergence_mode(args)  # exits when --staged-divergence selects it
    _ratify_immutable_mode(args)  # exits when --ratify-immutable selects it
    # Translate a retired `--stage G2` (warning once) before anything consumes  check_vocab: allow
    # it, so `resolve_stage` and `_step_stage` both see only canonical rungs.
    args.stage = (
        _resolve_stage_alias(args.stage, "--stage") if args.stage else args.stage
    )
    _warn_retired_flag_spelling()
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
    # unfiltered plan so a stage-scoped step (format's threshold is the Impl
    # rung) is still found,
    # and be lenient about a missing tool so a not-yet-set-up repo can commit —
    # a real failure still exits nonzero.
    step_stage = _step_stage(args.stage)  # explicit --stage gates; defaulted = ALL
    if args.run_step:
        all_steps = steps(coverage, args.tier, step_stage, args.phase, profile)
        match = [s for s in all_steps if s[0] == args.run_step]
        if not match:
            sys.exit("check: no step named {!r}".format(args.run_step))
        name, requires, cmd, _threshold, _layer = match[0]
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
        all_steps = steps(coverage, args.tier, step_stage, args.phase, profile)
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

    # RESOLVED HERE, not at the top of main(): --run-step/--run-steps exit above
    # without ever consulting it, and resolving it can now cost a subprocess
    # (`_derive_stage`, on a fingerprint miss). The pre-commit hook takes exactly
    # those two paths, so the floor no longer pays for a value it never reads.
    stage = resolve_stage(args.stage)
    plan = resolve_plan(stage, coverage, args.tier, args.phase, profile)

    if args.list:
        print("Plan at stage {} (tier {}):".format(stage, args.tier))
        _print_steps(plan)
        return

    if not plan:
        print("No checks defined at stage {}.".format(stage))
        return

    # Run-scope the coverage report before the plan (see the helper): a stale,
    # gitignored coverage.json must never be graded as this run's output.
    _clear_stale_coverage_report(plan)

    jobs = args.jobs if args.jobs is not None else 1
    if jobs == 0:
        jobs = len(plan)
    results = run_plan(plan, args.lenient, jobs, lane_map)

    print("\n" + "=" * 56)
    print("Check summary (stage {}, tier {}):".format(stage, args.tier))
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
