#!/usr/bin/env python3
"""Per-module coverage floors: stop the global floor hiding weak high-risk modules.

The global line-coverage floor (`docs/stack.ini` `[coverage] threshold`, enforced
by pytest-cov `--cov-fail-under`) is ONE aggregate number, so a heavily tested
generator can subsidize thin coverage in a security/process boundary while the
headline percentage still passes (repo-review 2026-07-22 M-4). This check adds
per-module MINIMUMS for the modules that must not be subsidized — initially at
honest current baselines, raised as focused behavioral tests land — and keeps the
global `--cov-fail-under` floor as the backstop rather than the only measure.

It splits along the same process/product line as `check_perf.py` (process.md §7):
**measuring** coverage is *product* work the project wires (pytest-cov emits a
JSON report); **comparing** each module against its declared floor is *process*
work the kit owns — this script, stdlib-only (arithmetic over JSON) and
stack-agnostic. Swap the JSON producer for your stack; the comparator is yours.

Inputs (a missing one degrades safely, never a false failure):
    --report  coverage.json         the coverage.py JSON report (pytest-cov
              `--cov-report=json`), keyed by source file with a per-file
              `summary.percent_covered`. ABSENT means coverage was not measured
              this run (e.g. the smoke tier, which the global floor also skips)
              => SKIP, the check_perf.py posture.
    --floors  docs/coverage-floors   one `<repo-relative module> <min percent>`
              per line — the docs/dupes-allow census idiom: `#` comments and
              blank lines are ignored, so each floor can carry a why-note.

Exit code is nonzero when any declared module is below its floor, OR is absent
from the report (a declared floor whose module vanished from measurement must
FAIL — never quietly pass), OR the floors file is malformed (a broken
declaration is loud, the same fail-closed stance check.py takes on a bad
profile). Exit 0 when every floor holds, when no floors are declared, or when
the report is absent (an unmeasured run).

Usage:
    python scripts/check_coverage.py [--report coverage.json]
                                     [--floors docs/coverage-floors]

Wired via `docs/stack.ini` as a `[step:module-coverage]` gate step, so it runs
AFTER `tests+coverage` produces the JSON (check.py's plan orders extra steps
after the test step). Opt-in like the dup-code gate: a repo without the step and
the floors file pays nothing.

Contracts: IF-069, IF-070 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import json
import sys
from pathlib import Path


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII module path or a `<`/`>=` glyph can't raise UnicodeEncodeError on a
    legacy Windows cp1252 console. Python 3.7+ streams expose `.reconfigure`;
    guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def load_floors(path):
    """Parse the floors census into `[(module, floor, lineno)]`. Each non-comment
    line is `<repo-relative module path> <min percent>`; blank lines and `#`
    comments (whole-line or trailing) are ignored, so a floor can carry a
    why-note. A malformed line — wrong field count, a non-numeric or
    out-of-range percent — raises ValueError naming the line: a broken
    declaration is a loud failure, never a silently dropped floor (the
    fail-closed stance check.py takes on a malformed profile)."""
    if not path.exists():
        return []
    out = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(
                "coverage-floors line {}: expected '<module> <percent>', "
                "got {!r}".format(i, raw.strip())
            )
        module, pct_s = parts
        try:
            pct = float(pct_s)
        except ValueError:
            raise ValueError(
                "coverage-floors line {}: {!r} is not a number".format(i, pct_s)
            )
        if not 0 <= pct <= 100:
            raise ValueError(
                "coverage-floors line {}: floor {} out of range 0..100".format(i, pct)
            )
        out.append((module.replace("\\", "/"), pct, i))
    return out


def load_report(path):
    """The coverage.py JSON report as `{normalized-file-path: percent_covered}`,
    or None when the file is absent (the 'not measured this run' signal, like
    check_perf's absent metrics). Paths are normalized to forward slashes so a
    Windows-separated report key matches a repo-relative floor. Malformed JSON
    raises (a corrupt report is loud, not a silent pass)."""
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for key, info in data.get("files", {}).items():
        pct = info.get("summary", {}).get("percent_covered")
        if isinstance(pct, bool) or not isinstance(pct, (int, float)):
            continue
        out[key.replace("\\", "/")] = float(pct)
    return out


def module_percent(percents, module):
    """The measured percent for `module` (a normalized repo-relative path), or
    None when no report key matches. A key matches when it equals the module or
    ends with `/<module>` — absolute-vs-relative and either path separator fold
    together, and the `/` boundary keeps `agent_session.py` from matching a
    hypothetical `my_agent_session.py`."""
    if module in percents:
        return percents[module]
    suffix = "/" + module
    for key, pct in percents.items():
        if key.endswith(suffix):
            return pct
    return None


def evaluate(floors, percents):
    """`[(module, floor, measured_or_None, status)]` for each declared floor,
    status in OK / FAIL (below floor) / MISSING (no report match)."""
    results = []
    for module, floor, _lineno in floors:
        measured = module_percent(percents, module)
        if measured is None:
            status = "MISSING"
        elif measured < floor:
            status = "FAIL"
        else:
            status = "OK"
        results.append((module, floor, measured, status))
    return results


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--report",
        default="coverage.json",
        help="coverage.py JSON report (default: coverage.json)",
    )
    ap.add_argument(
        "--floors",
        default="docs/coverage-floors",
        help="per-module floor census (default: docs/coverage-floors)",
    )
    args = ap.parse_args()

    try:
        floors = load_floors(Path(args.floors))
    except ValueError as exc:
        print("check_coverage: FAIL - {}".format(exc))
        sys.exit(1)

    if not floors:
        print(
            "check_coverage: OK - no per-module coverage floors declared ({})".format(
                args.floors
            )
        )
        return

    percents = load_report(Path(args.report))
    if percents is None:
        print(
            "check_coverage: SKIP - {} floor(s) declared but no coverage report "
            "at {} (coverage not measured this run - e.g. the smoke tier, where "
            "the global --cov-fail-under floor is likewise skipped)".format(
                len(floors), args.report
            )
        )
        return

    results = evaluate(floors, percents)
    for module, floor, measured, status in results:
        if status == "OK":
            print("  OK    {:6.2f} >= {:5.1f}  {}".format(measured, floor, module))
        elif status == "FAIL":
            print("  FAIL  {:6.2f} <  {:5.1f}  {}".format(measured, floor, module))
        else:  # MISSING
            print(
                "  FAIL  (no measurement)  floor {:5.1f}  {} - absent from {} "
                "(module vanished or was excluded from coverage)".format(
                    floor, module, args.report
                )
            )
    fails = [r for r in results if r[3] in ("FAIL", "MISSING")]
    n = len(results)
    if fails:
        print(
            "check_coverage: FAIL - {}/{} module floor(s) breached "
            "(the global --cov-fail-under floor stays the backstop)".format(
                len(fails), n
            )
        )
        sys.exit(1)
    print("check_coverage: OK - all {} module floor(s) hold".format(n))


if __name__ == "__main__":
    main()
