#!/usr/bin/env python3
"""flag_axis.py — the flag-axis count: boolean switches that could be one state.

WHAT IT COUNTS, PER MODULE. Two readings, both candidates for packing mutually
exclusive booleans into one enum state:

- a FLAG FUNCTION takes two or more boolean parameters: a parameter annotated
  `bool` or defaulting to `True`/`False`, keyword-only ones included. Two flags
  are four combinations, and a function that is fused from unrelated behaviours
  behind a mode switch shows up here, which is the cheap way to lower a
  duplicate or an operation count;
- a BOOLEAN-LITERAL CALL SITE passes `True` or `False` POSITIONALLY, where the
  reader cannot tell what the literal switches. A literal passed by keyword is
  named at the call and is not counted: the flag parameter behind it is already
  counted where it is defined, and most keyword literals are a library's own
  signature (`mkdir(parents=True)`, `run(check=True)`) that no project can
  change. On this kit the keyword form is eight times the positional one and
  almost all of it is that noise.

Functions are named as the complexity census names them
(`check_complexity.functions`: module-level functions and `Class.method`, a
nested `def` belonging to its enclosing function), so one function has one name
across both measures. Call sites are counted everywhere in the module.

A MEASURE OF THE PER-CHANGE REPORT, NEVER A GATE. `check_readability.py` runs it
as its `flag-axis` measure over the modules a change touches, against the
stamped per-module reading in `docs/flag-axis-baseline`, and lists a rise as a
WARN beside every other worsening. It is report-only by its own contract: the
report refuses to gate it even when a profile declares it gating, because a
count of candidates is a prompt to look, and many a two-flag function is the
right shape. Run directly, this module prints every counted module and the
totals against the stamped rows, and it always exits 0.

BASELINE. `docs/flag-axis-baseline`, TSV, LF-only, sorted by path, one row per
module whose reading is not zero: path, flag functions, boolean-literal call
sites. DOWNWARD-ONLY BY CONVENTION: re-stamp with `--restamp` after a module
sheds a flag, and never to quiet a warning. Nothing mechanizes the direction,
because the measure refuses nothing to enforce it with.

Contracts: IF-239, IF-240 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-239: the flag-axis measure's own parts, which the per-change
    readability report calls instead of copying. `reading(tree)` is one
    module's `Reading`: `functions`, one `(name, flags)` per flag function in
    census order, and `sites`, one `(line, callee)` per boolean-literal call
    site. `compare(now, row)` is None unless a count rose above the stamped
    `(functions, sites)` row (None reads as `(0, 0)`), and otherwise the delta
    text naming each count that rose. `read_baseline(path)` reads the stamped
    rows as `{path: (functions, sites)}`, empty when unstamped. `BASELINE` is
    the carrier path.

Contract IF-240: the flag-axis report's command line. `--root` (default the
    working directory), `--include GLOB` (repeatable; default the complexity
    census's surface), `--baseline PATH` (default `docs/flag-axis-baseline`)
    and `--restamp`, which rewrites the baseline from the current reading.
    It prints one SKIP line per included file it cannot read or parse and
    goes on. Without `--restamp` it prints one line per counted module, then one total
    line against the stamped rows, then one WARN line per module above its row
    or one OK line. It exits 0 in every case; argparse's own exit 2 for a
    malformed command line is the one other code.

Implements: SR-216, LLR-261
"""

import argparse
import ast
import sys
from collections import namedtuple
from pathlib import Path

import check_complexity
from kitlib.config import utf8_console

# Implements: SR-216, LLR-261
BASELINE = "docs/flag-axis-baseline"
MIN_FLAGS = 2
COLUMNS = ("path", "flag_functions", "literal_call_sites")
NOTE = (
    "# docs/flag-axis-baseline — the flag-axis reading of each counted module when "
    "stamped (flag_axis.py).\n"
    "# DOWNWARD-ONLY BY CONVENTION: re-stamp after a module sheds a flag or a "
    "literal, never to quiet a warning.\n"
)

Reading = namedtuple("Reading", "functions sites")


def _is_bool(node):
    return isinstance(node, ast.Constant) and isinstance(node.value, bool)


def _is_flag(arg, default):
    note = arg.annotation
    annotated = getattr(note, "id", None) == "bool" or (
        isinstance(note, ast.Constant) and note.value == "bool"
    )
    return annotated or _is_bool(default)


def flags(fn):
    """The boolean parameters of `fn`, in signature order. Defaults align to
    the END of the positional list; a keyword-only parameter carries its own
    default (None when it has none)."""
    a = fn.args
    positional = a.posonlyargs + a.args
    defaults = [None] * (len(positional) - len(a.defaults)) + list(a.defaults)
    pairs = list(zip(positional, defaults)) + list(zip(a.kwonlyargs, a.kw_defaults))
    return tuple(arg.arg for arg, default in pairs if _is_flag(arg, default))


def _callee(call):
    func = call.func
    return getattr(func, "attr", None) or getattr(func, "id", None) or "<expr>"


def reading(tree):
    """One module's `Reading`: its flag functions and its positional
    boolean-literal call sites.

    Implements: SR-216, LLR-261
    """
    named = [(name, flags(fn)) for name, fn in check_complexity.functions(tree)]
    sites = sorted(
        (node.lineno, _callee(node))
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and any(_is_bool(a) for a in node.args)
    )
    return Reading([(n, f) for n, f in named if len(f) >= MIN_FLAGS], sites)


def _signature(functions):
    return ", ".join("{}({})".format(name, ", ".join(f)) for name, f in functions)


def compare(now, row):
    """None unless a count of `now` rose above the stamped `(functions,
    sites)` row, else the delta naming each count that rose. A fall is not a
    worsening, and re-stamping it down is the maintainer's act.

    Implements: SR-216, LLR-261
    """
    was_fns, was_sites = row or (0, 0)
    parts = []
    if len(now.functions) > was_fns:
        parts.append(
            "flag functions {} -> {} (+{}: {})".format(
                was_fns,
                len(now.functions),
                len(now.functions) - was_fns,
                _signature(now.functions),
            )
        )
    if len(now.sites) > was_sites:
        parts.append(
            "boolean-literal call sites {} -> {} (+{})".format(
                was_sites, len(now.sites), len(now.sites) - was_sites
            )
        )
    return "; ".join(parts) or None


def census(root, includes):
    """`({path: Reading}, [(path, why)])`: every module under `root` with a
    non-zero reading, paths POSIX and relative to `root`, over the complexity
    census's own file walk, and each included file that could not be read or
    parsed. An unreadable file is reported rather than raised, because the
    report's promise is to exit 0 and one bad file must not hide the rest."""
    out, skipped = {}, []
    for rel, path in check_complexity.source_paths(root, includes):
        try:
            found = reading(ast.parse(path.read_text(encoding="utf-8")))
        except (OSError, SyntaxError, UnicodeDecodeError, ValueError) as exc:
            skipped.append((rel, type(exc).__name__))
            continue
        if found.functions or found.sites:
            out[rel] = found
    return out, skipped


def read_baseline(path):
    """`{path: (flag functions, literal call sites)}`; empty when unstamped.

    Implements: SR-216, LLR-261
    """
    path = Path(path)
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = line.split("\t")
        if line.startswith("#") or len(cells) < 3:
            continue
        out[cells[0]] = (int(cells[1]), int(cells[2]))
    return out


def write_baseline(path, found):
    text = [NOTE + "# " + "\t".join(COLUMNS)]
    for rel, r in sorted(found.items()):
        text.append("\t".join((rel, str(len(r.functions)), str(len(r.sites)))))
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(text) + "\n")


def _module_line(rel, r):
    sites = ", ".join("line {} {}".format(n, c) for n, c in r.sites)
    return "flag_axis: {} - {} flag function(s){}; {} boolean-literal call site(s){}".format(
        rel,
        len(r.functions),
        ": " + _signature(r.functions) if r.functions else "",
        len(r.sites),
        ": " + sites if sites else "",
    )


def _report(found, stamped, baseline):
    """The per-module lines, the totals and the comparison, as text lines."""
    lines = [_module_line(rel, r) for rel, r in sorted(found.items())]
    lines.append(
        "flag_axis: total - {} flag function(s) and {} boolean-literal call "
        "site(s) in {} module(s); stamped {} and {} in {}".format(
            sum(len(r.functions) for r in found.values()),
            sum(len(r.sites) for r in found.values()),
            len(found),
            sum(row[0] for row in stamped.values()),
            sum(row[1] for row in stamped.values()),
            baseline,
        )
    )
    worse = [
        (rel, compare(r, stamped.get(rel)))
        for rel, r in sorted(found.items())
        if compare(r, stamped.get(rel))
    ]
    lines += [
        "flag_axis: WARN - {} above its stamped reading: {}".format(rel, delta)
        for rel, delta in worse
    ]
    if not worse:
        lines.append("flag_axis: OK - no module above its stamped reading")
    return lines


def main(argv=None):
    """The flag-axis report and stamp; always exits 0.

    Implements: SR-216, LLR-261
    """
    utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("--include", action="append", default=None, metavar="GLOB")
    ap.add_argument("--baseline", default=BASELINE)
    ap.add_argument("--restamp", action="store_true", help="rewrite the baseline")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    found, skipped = census(
        root, tuple(args.include or check_complexity.DEFAULT_INCLUDE)
    )
    for rel, why in skipped:
        print("flag_axis: SKIP - cannot read or parse {} ({})".format(rel, why))
    if args.restamp:
        write_baseline(root / args.baseline, found)
        print("flag_axis: re-stamped {} row(s) -> {}".format(len(found), args.baseline))
        return 0
    stamped = read_baseline(root / args.baseline)
    print("\n".join(_report(found, stamped, args.baseline)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
