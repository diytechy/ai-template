#!/usr/bin/env python3
"""WI-281 — the smoke commit bar's wall-clock budget check (CI-facing).

The per-commit smoke tier (docs/stack.ini [tiers] smoke) must run within the
seconds budget declared in docs/stack.ini [smoke-budget] — a smoke test answers
"is it basically alive?", not "re-run most of the full suite". WI-281 split the
budget in two: the ALWAYS-ON deterministic membership ratchet
(tests/test_smoke_budget.py) is the machine-independent floor; THIS is the
wall-clock half. It defaults to `--mode warn` for LOCAL convenience (a breach
prints a WARNING, exit 0). CI runs it with `--mode enforce` (exit 1 on breach):
the re-tiered tier is startup-dominated, not core-bound — measured ~7.5 s at 24
cores, ~8.1 s at 4, ~10.5 s at 2 (WI-281 rework, 2026-07-23, 3.11.9) — so the
60 s budget keeps ~5x headroom on any real runner and a breach means the tier
stopped being a smoke test (a heavy module slipped back in), not runner noise.

Usage:
  # time a fresh smoke run and compare (local convenience, or a CI lane):
  python scripts/check_smoke_budget.py [--mode warn|enforce]
  # evaluate an already-measured elapsed time (CI times the step, feeds it here):
  python scripts/check_smoke_budget.py --elapsed 42.5 [--mode warn|enforce]

Stdlib-only, cross-platform (a meta-repo dev/CI tool, like scripts/dev-setup).
"""

import argparse
import configparser
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STACK_INI = ROOT / "docs" / "stack.ini"


def _profile():
    # Mirror check.py's parser: interpolation=None keeps command values literal
    # (a `%` needs no escaping), utf-8-sig tolerates a Notepad BOM.
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(STACK_INI, encoding="utf-8-sig")
    return cp


def declared_seconds(cp):
    return float(cp["smoke-budget"]["seconds"])


def smoke_argv(cp):
    """The declared smoke command: [product] test + the [tiers] smoke selector,
    with {py} bound to this interpreter — so this times exactly the bar sessions
    run (`python -m pytest -q -n auto -m smoke`), read from the single source."""
    test = cp.get("product", "test", fallback="{py} -m pytest -q -n auto")
    tier = cp.get("tiers", "smoke", fallback="-m smoke")
    argv = shlex.split(test) + shlex.split(tier)
    return [sys.executable if tok == "{py}" else tok for tok in argv]


def _annotate(level, message):
    """A GitHub Actions annotation when running in CI; harmless plain text else."""
    if os.environ.get("GITHUB_ACTIONS"):
        print("::{}::{}".format(level, message))


def evaluate(elapsed, budget, mode):
    """Report the verdict and return an exit code. warn -> always 0 (a WARNING
    line on breach); enforce -> 1 on breach."""
    over = elapsed > budget
    verdict = "OVER" if over else "within"
    print(
        "smoke wall-clock budget: {:.1f}s vs {:.0f}s budget -> {}".format(
            elapsed, budget, verdict
        )
    )
    if not over:
        return 0
    msg = (
        "smoke tier took {:.1f}s, over its {:.0f}s budget (docs/stack.ini "
        "[smoke-budget]). Re-tier a heavy module into conftest.SLOW_MODULES, or "
        "re-stamp the budget with the reason in the log.".format(elapsed, budget)
    )
    if mode == "enforce":
        _annotate("error", msg)
        print("FAIL (enforce): " + msg, file=sys.stderr)
        return 1
    _annotate("warning", msg)
    print("WARN: " + msg)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Smoke-tier wall-clock budget check.")
    ap.add_argument(
        "--elapsed",
        type=float,
        default=None,
        help="evaluate this already-measured wall time (seconds) instead of "
        "running the smoke tier.",
    )
    ap.add_argument(
        "--mode",
        choices=("warn", "enforce"),
        default="warn",
        help="warn (default): report only; enforce: exit 1 when over budget.",
    )
    args = ap.parse_args(argv)
    cp = _profile()
    budget = declared_seconds(cp)

    if args.elapsed is not None:
        elapsed = args.elapsed
    else:
        cmd = smoke_argv(cp)
        print("timing: " + " ".join(shlex.quote(c) for c in cmd))
        start = time.perf_counter()
        proc = subprocess.run(cmd, cwd=str(ROOT))
        elapsed = time.perf_counter() - start
        if proc.returncode != 0:
            # A red smoke tier is a separate failure from a slow one; surface it
            # but do not let a broken run masquerade as a budget verdict.
            print(
                "note: smoke tier exited {} (test failures are not a budget "
                "breach; fix them separately)".format(proc.returncode),
                file=sys.stderr,
            )

    return evaluate(elapsed, budget, args.mode)


if __name__ == "__main__":
    sys.exit(main())
