#!/usr/bin/env python3
"""Coverage step adapter: run the dual-plan coverage pre-pass headless and turn
its exit/report contract into the round state machine's typed step outcome
(DP-001 selected plan P4 / WI-197; the protocol is process-options.md "Dual-plan
decomposition").

Stack-agnostic, standard-library only (Python 3.8+, Windows/POSIX). This is the
thin seam between two shipped, unchanged pieces:

  * `plan_coverage.py` (IF-057, WI-190) — the mechanical commensurability
    checker. Exit-code contract: `0` clean, `1` reference/structure findings,
    `2` malformed inputs (no clauses / no plan table / missing file). Findings
    print as `plan_coverage: FAIL - <planfile>: ...` lines; the per-plan +
    pairwise report is printed and, with `--out`, written to a file.

  * `plan_round.py` (IF-058, WI-194) — the pure round lifecycle. Its
    STEP_COVERAGE record contract is `findings=bool` plus `plans=[implicated
    true plan keys]` (absent/empty means both), driving the one-repair bounce
    and, on a repeat, the DISP_PAGE.

`run_coverage()` invokes the checker as a subprocess, captures the report as the
payload P2's critic/arbiter briefs embed (returned, never printed), and maps the
exit status to a typed result dict. `to_record_kwargs()` projects that dict onto
the `record(state, STEP_COVERAGE, ...)` kwargs. This module never mutates round
state — it produces the kwargs and lets the coordinator call `record`; keeping
the adapter side-effect-free (the `plan_round`/`schedule` shape) means a caller
can brief, log, or persist the result before recording it.

Exit 2 (malformed) is preserved as its own outcome (`malformed=True`) so the
coordinator can tell a bad-inputs bounce from a real-findings bounce; both bounce
the round (`to_record_kwargs` folds malformed into `findings`), and with no
parseable FAIL line the implicated set is empty, so the machine re-runs both
plans — the fail-closed default.

Usage (the CLI is a documentation aid; plans map to A/B in argument order):

    python scripts/plan_coverage_step.py --goal GOAL.md PLAN_A.md PLAN_B.md \
        [--root .] [--out coverage.md]

Contracts: IF-060 — the interface seam this module declares (process.md §8; rows
of record in docs/requirements/interfaces.csv).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# A finding line names the plan by its file basename: `plan_coverage: FAIL -
# <planfile>: <message>` (plan_coverage.check_plan formats every finding as
# "<name>: ..."). The basename is captured up to the first colon.
FAIL_RE = re.compile(r"^plan_coverage: FAIL - (.+?):")


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check.py guard)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _implicated_plans(stdout, plan_key_of):
    """The true plan keys ("A"/"B") named by the FAIL lines, de-duplicated in
    first-seen order. `plan_key_of` maps a plan file basename to its true key;
    an unmapped basename (None) is dropped so a stray line cannot invent a plan."""
    keys = []
    for line in stdout.splitlines():
        m = FAIL_RE.match(line)
        if not m:
            continue
        key = plan_key_of(m.group(1).strip())
        if key and key not in keys:
            keys.append(key)
    return keys


def run_coverage(goal, plan_paths, root, out_path, plan_key_of):
    """Run `plan_coverage.py` headless over `goal` + `plan_paths` and return the
    typed result the round consumes:

        {"exit": int, "findings": bool, "malformed": bool,
         "implicated": [true plan keys], "report": str}

    `plan_coverage.py` is located relative to this module (siblings in
    scripts/), invoked with `sys.executable`, and given `--out out_path` so the
    clean report (no FAIL/OK/note noise) lands in a file. `report` is that file
    when it was written (exit 0/1); on a malformed run (exit 2) no report file
    is produced, so the captured stdout — carrying the ERROR line — is returned
    instead. The report is the payload the critic/arbiter briefs embed; it is
    returned here, never printed.

    Exit mapping: 0 -> clean (findings=False, malformed=False); 1 -> findings
    (implicated parsed from the FAIL lines); 2 -> malformed (its own flag, empty
    implicated -> both plans bounce by the record contract's default)."""
    script = Path(__file__).resolve().parent / "plan_coverage.py"
    out_path = Path(out_path)
    argv = [
        sys.executable,
        str(script),
        "--goal",
        str(goal),
        "--root",
        str(root),
        *[str(p) for p in plan_paths],
        "--out",
        str(out_path),
    ]
    proc = subprocess.run(
        argv,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    exit_code = proc.returncode
    findings = exit_code == 1
    malformed = exit_code == 2
    # A malformed run (exit 2) writes no fresh report — a leftover out_path
    # from an earlier stage must not masquerade as this run's (repo-review
    # 2026-07-21 L-28).
    report = (
        out_path.read_text(encoding="utf-8")
        if out_path.exists() and not malformed
        else proc.stdout
    )
    implicated = _implicated_plans(proc.stdout, plan_key_of) if findings else []
    return {
        "exit": exit_code,
        "findings": findings,
        "malformed": malformed,
        "implicated": implicated,
        "report": report,
        # The raw checker stdout: on a findings run it carries the
        # `plan_coverage: FAIL - ...` lines the report file deliberately
        # omits — the payload a mechanical-repair prompt needs (WI-199).
        "stdout": proc.stdout,
    }


def to_record_kwargs(result):
    """The `plan_round.record(state, STEP_COVERAGE, ...)` kwargs for a result:
    `{"findings": bool, "plans": [...]}`. A malformed run bounces exactly like a
    findings run (fail-closed), so `findings` folds in `malformed`; `plans`
    carries the implicated true plan keys (empty => the machine re-runs both)."""
    return {
        "findings": bool(result["findings"] or result["malformed"]),
        "plans": list(result["implicated"]),
    }


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description="dual-plan coverage step adapter (see module docstring)"
    )
    ap.add_argument("plans", nargs="+", metavar="PLAN.md", help="plan file(s)")
    ap.add_argument("--goal", required=True, help="the goal brief (C# clauses)")
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--out", default="coverage.md", help="report file (default: coverage.md)"
    )
    args = ap.parse_args()
    # The demo maps plans to true keys by argument order (A, B, ...).
    order = {name: chr(ord("A") + i) for i, name in enumerate(args.plans)}
    result = run_coverage(
        args.goal,
        args.plans,
        args.root,
        args.out,
        lambda basename: order.get(basename) or order.get(Path(basename).name),
    )
    briefed = {k: v for k, v in result.items() if k != "report"}
    briefed["record_kwargs"] = to_record_kwargs(result)
    print(json.dumps(briefed, indent=2))


if __name__ == "__main__":
    main()
