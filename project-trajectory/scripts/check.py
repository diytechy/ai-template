#!/usr/bin/env python3
"""The check harness — one command that runs every quality gate locally and in CI.

Stack-agnostic kit, **Python reference implementation**. This is the runnable
version of the "harness contract" in `process.md §7`: format · lint · tests ·
coverage · traceability · architecture-map freshness. Wire it to your stack by
editing the `STEPS` table below (swap `ruff`/`pytest` for your toolchain); the
contract is the *gates and exit code*, not the specific tools.

Design choices that keep it honest and CI-friendly:
    - **Never a false green.** Any failing required step makes the whole run exit
      nonzero. We print the real command output; we do not summarize it away.
    - **Missing tool != pass.** If a required tool isn't installed the step is
      reported SKIP(missing) and (outside --lenient) fails the run, so CI can't
      silently skip linting.
    - **Gate-scoped.** `--gate G2` runs only what that gate needs (e.g. G2 needs
      traceability + a runnable harness; G3 needs the full suite). Default runs all.
    - **Tiered tests.** `--tier smoke` runs only the fast subset so you can check
      every iteration; `release` runs everything including slow/hardware tests.
      Tiers map to pytest markers (`-m`); the `Tier` column in test-cases.csv is
      the registry source of truth. CI typically runs `smoke` on push, `full` on
      PR, and `release`/`all` on a release tag.
    - **Non-interactive.** No prompts; deterministic exit codes for automation.

Usage:
    python scripts/check.py [--gate G1|G2|G3|all] [--tier smoke|full|release|all]
                            [--coverage N] [--lenient] [--list]

    --gate      Which gate's checks to run (default: all).
    --tier      Which test tier to run (default: all). Requires tests to be marked
                @pytest.mark.smoke / .full / .release and the markers registered in
                pytest.ini, e.g.:
                    [pytest]
                    markers =
                        smoke: fast checks safe to run every iteration
                        full: full pre-merge suite
                        release: slow / hardware / manual-adjacent, run at release
    --coverage  Line-coverage threshold percent (default: 80; see COVERAGE_THRESHOLD).
    --lenient   Treat missing tools as SKIP instead of failure (local dev only).
    --list      Print the step plan for the gate and exit.
"""
import argparse
import shutil
import subprocess
import sys
import time

COVERAGE_THRESHOLD = 80  # keep in sync with process.md
SRC = "src"              # source root (edit to match your layout)
TESTS = "tests"          # test root

# Tier -> pytest marker expression. `all` runs everything (no -m filter); the
# others select cumulatively so a smoke test always runs in the higher tiers.
TIERS = {
    "smoke": "smoke",
    "full": "smoke or full",
    "release": "smoke or full or release",
    "all": None,
}

# Each step: name, the tool executable that must exist, the command, and the set
# of gates that require it. Edit commands to fit your stack; keep the gate tags.
def steps(coverage, tier):
    pytest_cmd = ["pytest", "-q",
                  "--cov=" + SRC, "--cov-report=term-missing",
                  "--cov-fail-under=" + str(coverage)]
    marker = TIERS.get(tier)
    if marker:
        pytest_cmd += ["-m", marker]
    return [
        ("format", "ruff",
         ["ruff", "format", "--check", SRC, TESTS], {"G3"}),
        ("lint", "ruff",
         ["ruff", "check", SRC, TESTS], {"G3"}),
        ("tests+coverage", "pytest", pytest_cmd, {"G3"}),
        ("traceability", sys.executable,
         [sys.executable, "scripts/trace.py", "--strict"], {"G2", "G3"}),
        ("arch-map", sys.executable,
         [sys.executable, "scripts/gen_arch_map.py", "--check",
          "--src", SRC, "--doc", "docs/architecture.md"], {"G3"}),
    ]

GATES = ["G1", "G2", "G3", "all"]


def run_step(name, tool, cmd, lenient):
    """Run one step. Returns (status, detail) where status in PASS/FAIL/SKIP."""
    if shutil.which(tool) is None and tool != sys.executable:
        status = "SKIP" if lenient else "FAIL"
        return status, "required tool '{}' not installed".format(tool)
    start = time.time()
    print("\n=== {} : {} ===".format(name, " ".join(cmd)), flush=True)
    proc = subprocess.run(cmd)
    secs = time.time() - start
    if proc.returncode == 0:
        return "PASS", "{:.1f}s".format(secs)
    return "FAIL", "exit {} ({:.1f}s)".format(proc.returncode, secs)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gate", choices=GATES, default="all")
    ap.add_argument("--tier", choices=list(TIERS), default="all")
    ap.add_argument("--coverage", type=int, default=COVERAGE_THRESHOLD)
    ap.add_argument("--lenient", action="store_true",
                    help="treat missing tools as SKIP (local dev only)")
    ap.add_argument("--list", action="store_true", help="print the plan and exit")
    args = ap.parse_args()

    plan = [s for s in steps(args.coverage, args.tier)
            if args.gate == "all" or args.gate in s[3]]

    if args.list:
        print("Plan for gate {} (tier {}):".format(args.gate, args.tier))
        for name, tool, cmd, gates in plan:
            print("  - {:16} [{}]  {}".format(name, ",".join(sorted(gates)),
                                              " ".join(cmd)))
        return

    if not plan:
        print("No checks defined for gate {}.".format(args.gate))
        return

    results = []
    for name, tool, cmd, _gates in plan:
        status, detail = run_step(name, tool, cmd, args.lenient)
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
