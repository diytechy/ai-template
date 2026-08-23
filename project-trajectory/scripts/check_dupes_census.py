#!/usr/bin/env python3
"""check_dupes_census.py — the WI-448 duplication census, standing (WI-507,
OI-58 (a)+(b)).

WARN-FIRST FOREVER: this never fails a gate, not even under `--strict` (the
flag is accepted only for the `[step:]` convention's uniform command shape).
That is deliberate and narrower than what it replaces: `[step:dupes]` GATED on
an unbounded population and 93% of its findings were accepted idioms, so the
owner tore it down (D-7, 2026-08-10) and ruled F5 duplication UNBOUNDED. OI-58
(2026-08-22) re-arms the MEASUREMENT, not the gate — a burn-down number beside
the module-size and smoke-budget ratchets, never a new floor. Do not add
`--strict` teeth here without bringing that case to the owner, per D-7.

Measures duplicated FUNCTION BODIES over `project-trajectory/scripts/**/*.py`
(bodies >= 4 lines, docstring stripped, `__pycache__` excluded): each
function's body AST is hashed and identical hashes group as one duplicate
class. This is the exact WI-448 producing command — previously a `python -c`
one-liner re-typed into every log fragment that measured it, which is the
very restatement this doctrine's 0->A->B rule targets — now one named function
two callers (this script's `main`, and any future caller) share instead of
each re-deriving the AST walk.

Baseline lives in `docs/stack.ini` `[dupes-census]`, hand-maintained like the
module-size ratchet and the smoke-budget ceiling: DOWNWARD-ONLY by convention
(a reviewed re-stamp, reason in the log), never a mechanized rewrite — the
baseline six lines up have narrative for the same reason those two do.

    [step:dupes-census]
    command = {py} project-trajectory/scripts/check_dupes_census.py --root .

Stdlib only.

Implements: SR-182, LLR-195
"""

import argparse
import ast
import configparser
import hashlib
import sys
from pathlib import Path

from kitlib.config import utf8_console as _utf8_console

PYCACHE = "__pycache__"
MIN_BODY_LINES = 4
STACK_INI = "docs/stack.ini"
SECTION = "dupes-census"


def _stripped_body(node):
    """A function's body with its docstring removed, if it has one — matching
    the WI-448 producing command's `B` lambda so this census reads the same
    population it always has."""
    body = node.body
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        return body[1:]
    return body


def measure(scripts_dir):
    """`(groups, copies, lines)`: duplicated function-body groups, redundant
    copies (each group's size minus one, summed), and redundant lines (each
    group's members after the first, summed) — over every `*.py` under
    `scripts_dir`, excluding `__pycache__`."""
    by_hash = {}
    for path in sorted(Path(scripts_dir).rglob("*.py")):
        if PYCACHE in path.parts:
            continue
        tree = ast.parse(path.read_bytes())
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            body = _stripped_body(node)
            if not body:
                continue
            n_lines = node.end_lineno - node.lineno + 1
            if n_lines < MIN_BODY_LINES:
                continue
            digest = hashlib.sha1(
                "\n".join(ast.dump(n) for n in body).encode("utf-8")
            ).hexdigest()
            by_hash.setdefault(digest, []).append(n_lines)
    dupe_groups = [v for v in by_hash.values() if len(v) > 1]
    groups = len(dupe_groups)
    copies = sum(len(v) - 1 for v in dupe_groups)
    lines = sum(sum(v[1:]) for v in dupe_groups)
    return groups, copies, lines


def _load_baseline(root):
    """`(groups, copies, lines)` from `docs/stack.ini` `[dupes-census]`, or
    `None` when no baseline is stamped yet (a fresh/scaffolded repo)."""
    cp = configparser.ConfigParser(interpolation=None)
    cp.read(Path(root) / STACK_INI, encoding="utf-8")
    if not cp.has_section(SECTION):
        return None
    return (
        cp.getint(SECTION, "groups"),
        cp.getint(SECTION, "copies"),
        cp.getint(SECTION, "lines"),
    )


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="accepted for the [step:] convention's uniform shape; never "
        "changes the exit code — this check is warn-first forever (D-7)",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()
    scripts_dir = root / "project-trajectory" / "scripts"
    if not scripts_dir.is_dir():
        print("check_dupes_census: OK - no project-trajectory/scripts/ here.")
        return 0

    groups, copies, lines = measure(scripts_dir)
    baseline = _load_baseline(root)
    if baseline is None:
        print(
            "check_dupes_census: {} group(s) / {} redundant copy/copies / {} "
            "redundant line(s) — no baseline stamped (docs/stack.ini "
            "[dupes-census])".format(groups, copies, lines)
        )
        return 0

    b_groups, b_copies, b_lines = baseline
    worse = groups > b_groups or copies > b_copies or lines > b_lines
    better = groups < b_groups or copies < b_copies or lines < b_lines
    measured = "{} group(s) / {} redundant copy/copies / {} redundant line(s)".format(
        groups, copies, lines
    )
    baselined = "{} / {} / {}".format(b_groups, b_copies, b_lines)
    if worse:
        print(
            "check_dupes_census: WARN - {} vs the stamped baseline {} — "
            "duplication grew. Not a gate (D-7): investigate whether the new "
            "duplicate pairs a fix that wants a shared stage (0->A->B), then "
            "re-stamp deliberately with the reason, in "
            "docs/stack.ini [dupes-census].".format(measured, baselined),
            file=sys.stderr,
        )
    elif better:
        print(
            "check_dupes_census: {} vs the stamped baseline {} — the census "
            "improved. Re-stamp docs/stack.ini [dupes-census] downward in "
            "this commit, per its own rule.".format(measured, baselined),
            file=sys.stderr,
        )
    else:
        print("check_dupes_census: OK - {}, unchanged from baseline.".format(measured))
    return 0


if __name__ == "__main__":
    sys.exit(main())
