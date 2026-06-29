#!/usr/bin/env python3
"""The check harness — one command that runs every quality gate locally and in CI.

Stack-agnostic kit, **Python reference implementation**. This is the runnable
version of the "harness contract" in `process.md §7`: format · lint · tests ·
coverage · traceability · architecture-map freshness. Wire it to your stack by
editing the step list the `steps()` function returns below — and the
`SRC`/`TESTS`/tool names in the "EDIT FOR YOUR STACK" block just under the
imports (swap `ruff`/`pytest` for your toolchain); the contract is the *gates and
exit code*, not the specific tools. For a non-Python project, replace the
format/lint/test commands with your own (or drop the ones you don't have); keep
the traceability/flows/arch-map steps — they're stdlib-only and stack-agnostic.

Design choices that keep it honest and CI-friendly:
    - **Never a false green.** Any failing required step makes the whole run exit
      nonzero. We print the real command output; we do not summarize it away.
    - **Missing tool != pass.** If a step's required module isn't importable the
      step is reported SKIP(missing) and (outside --lenient) fails the run, so CI
      can't silently skip linting.
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

    --gate      Which gate's checks to run (default: all). G3 (and all) also
                requires every Verification=Test SR to be Status=Verified
                (trace.py --require-verified).
    --tier      Which test tier to run (default: all). Mark fast critical-path
                tests @pytest.mark.smoke and expensive ones @pytest.mark.release
                (markers registered in pytest.ini); leave ordinary tests unmarked —
                they run in the full/release tiers automatically.
    --coverage  Line-coverage threshold percent (default: 80; see COVERAGE_THRESHOLD).
                Enforced for the full/release/all tiers, not smoke.
    --lenient   Treat missing tools as SKIP instead of failure (local dev only).
    --list      Print the step plan for the gate and exit.
"""

import argparse
import importlib.util
import subprocess
import sys
import time

# ============================ EDIT FOR YOUR STACK ============================
# The stack-specific knobs live here. For a non-Python project: point SRC/TESTS
# at your layout, then swap the format/lint/tests commands in steps() (search
# "EDIT FOR YOUR STACK" again) for your toolchain — or drop a step you don't
# have. The traceability, design-flows, and arch-map steps are stdlib-only and
# stack-agnostic; keep them as-is.
SRC = "src"  # source root
TESTS = "tests"  # test root
COVERAGE_THRESHOLD = 80  # line-coverage %, enforced at full/release (process.md)
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


# Each step: name, the third-party module(s) it needs (importable by THIS
# interpreter; () = stdlib-only), the command, and the set of gates that require
# it. Edit commands to fit your stack; keep the gate tags.
def steps(coverage, tier, gate, phase=None):
    # --- EDIT FOR YOUR STACK: the format/lint/test commands -------------------
    # `pytest_cmd` (assembled here because it varies by tier/coverage) and the
    # `ruff` format/lint entries in the returned list are the Python-reference
    # toolchain. Replace them with your stack's equivalents — or drop a step you
    # don't have — but keep each step's gate tags. Tools run as `python -m <mod>`
    # via this interpreter, so the launcher's venv python is enough (no PATH/venv
    # dance). `pytest_needs` lists the modules a step imports, so a missing tool
    # is reported SKIP(missing) and (outside --lenient) fails rather than passing.
    pytest_cmd = [sys.executable, "-m", "pytest", "-q"]
    pytest_needs = ("pytest",)
    if tier in COVERAGE_TIERS:
        pytest_cmd += [
            "--cov=" + SRC,
            "--cov-report=term-missing",
            "--cov-fail-under=" + str(coverage),
        ]
        pytest_needs = ("pytest", "pytest_cov")
    marker = TIERS.get(tier)
    if marker:
        pytest_cmd += ["-m", marker]
    # The traceability step only runs at G2/G3, where placeholder rows must be
    # gone, so --no-placeholders is always on here (a fresh scaffold is exempt
    # only because nothing past G1 runs against it).
    trace_cmd = [sys.executable, "scripts/trace.py", "--strict", "--no-placeholders"]
    if gate in ("G3", "all"):  # G3 criterion: test-verifiable SRs are Verified
        trace_cmd.append("--require-verified")
        trace_cmd.append("--strict-schema")  # G3: required fields + valid enums
        if phase:  # phased delivery: close G3 for this phase only (process.md §4)
            trace_cmd += ["--phase", phase]
    return [
        (
            "format",
            ("ruff",),
            [sys.executable, "-m", "ruff", "format", "--check", SRC, TESTS],
            {"G3"},
        ),
        (
            "lint",
            ("ruff",),
            [sys.executable, "-m", "ruff", "check", SRC, TESTS],
            {"G3"},
        ),
        ("tests+coverage", pytest_needs, pytest_cmd, {"G3"}),
        ("traceability", (), trace_cmd, {"G2", "G3"}),
        # Authored runtime-flow diagrams (process.md §3 "Design-time runtime
        # flows"): required from G2 on, so reviewers verify behavior from the
        # diagrams, not from registry rows.
        (
            "design-flows",
            (),
            [sys.executable, "scripts/check_flows.py", "--no-placeholders"],
            {"G2", "G3"},
        ),
        # Add `--doc AGENTS.md` / `--doc CLAUDE.md` to route the map there too, and
        # `--flow <entry>` to also check the generated high-level flow.
        (
            "arch-map",
            (),
            [
                sys.executable,
                "scripts/gen_arch_map.py",
                "--check",
                "--strict-parse",
                "--src",
                SRC,
                "--doc",
                "docs/architecture.md",
            ],
            {"G3"},
        ),
    ]


GATES = ["G1", "G2", "G3", "all"]


def run_step(name, requires, cmd, lenient):
    """Run one step. Returns (status, detail) where status in PASS/FAIL/SKIP."""
    missing = [m for m in requires if importlib.util.find_spec(m) is None]
    if missing:
        status = "SKIP" if lenient else "FAIL"
        return status, "module(s) {} not importable by {} — run scripts/setup".format(
            ", ".join(missing), sys.executable
        )
    start = time.time()
    print("\n=== {} : {} ===".format(name, " ".join(cmd)), flush=True)
    proc = subprocess.run(cmd)
    secs = time.time() - start
    if proc.returncode == 0:
        return "PASS", "{:.1f}s".format(secs)
    return "FAIL", "exit {} ({:.1f}s)".format(proc.returncode, secs)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--gate", choices=GATES, default="all")
    ap.add_argument("--tier", choices=list(TIERS), default="all")
    ap.add_argument("--coverage", type=int, default=COVERAGE_THRESHOLD)
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
    ap.add_argument("--list", action="store_true", help="print the plan and exit")
    args = ap.parse_args()

    plan = [
        s
        for s in steps(args.coverage, args.tier, args.gate, args.phase)
        if args.gate == "all" or args.gate in s[3]
    ]

    if args.list:
        print("Plan for gate {} (tier {}):".format(args.gate, args.tier))
        for name, _requires, cmd, gates in plan:
            print(
                "  - {:16} [{}]  {}".format(
                    name, ",".join(sorted(gates)), " ".join(cmd)
                )
            )
        return

    if not plan:
        print("No checks defined for gate {}.".format(args.gate))
        return

    results = []
    for name, requires, cmd, _gates in plan:
        status, detail = run_step(name, requires, cmd, args.lenient)
        results.append((name, status, detail))

    print("\n" + "=" * 56)
    print("Check summary (gate {}, tier {}):".format(args.gate, args.tier))
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
