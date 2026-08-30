#!/usr/bin/env python3
"""check_complexity.py — the stdlib cognitive-complexity + SLOC census.

Measures SonarSource Cognitive Complexity (CognitiveComplexity.pdf v1.7) and
SLOC per function, plus a per-module public-symbol count (reported, never
gated — the Ousterhout depth proxy). Stdlib only: a shipped check must not make
every adopter install a linter, which is why this exists beside — and not on
top of — the ruff C901 ratchet. Because the counting rules live in this
docstring rather than in a third-party tool, the baseline is a property of the
code, not of a tool version: a linter upgrade cannot silently invalidate it.

REPORT-ONLY as shipped: no `[step:]` is wired into `docs/stack.ini`, so nothing
runs this as a gate. The enforce capability exists (`--mode enforce`, exercised
by the tests) but arming it is an opt-in act — a `[step:complexity]` step, of
the shape below:

    [step:complexity]
    command = {py} project-trajectory/scripts/check_complexity.py --root .

CENSUS UNIT. One row per module-level function and per method. A nested `def`
or `lambda` is scored INTO its enclosing function (Sonar charges the nesting
increment for it, never a base increment) and never gets its own row: the
reward for decomposition is a SIBLING function or a new module, not an inner
one, and a second row for the inner def would double-count it in the census.

BASELINE. `docs/complexity-baseline`, TSV, LF-only, sorted by path then
function, one row per over-threshold function: path, function, cognitive, sloc,
reason. Its own header states that it is a DEBT STATEMENT, not an approval. TSV
for one reason — the minimum merge-conflict surface when two concurrent
sessions re-stamp; it matches the extension-less house data files under `docs/`
(`docs/coverage-floors`). There is NO inline suppression pragma and there must
never be one; the escape hatch is this one reviewed central file, because a
scattered opt-out self-replicates as new code copies it.

Implements: SR-183, LLR-206
"""

import argparse
import ast
import sys
from pathlib import Path

from kitlib.config import utf8_console

DEFAULT_THRESHOLD = 15
BASELINE = "docs/complexity-baseline"
DEFAULT_INCLUDE = ("project-trajectory/scripts/**/*.py",)
COLUMNS = ("path", "function", "cognitive", "sloc", "reason")
HEADER = "# " + "\t".join(COLUMNS)
DEBT_NOTE = (
    "# docs/complexity-baseline — one row per function over the cognitive-"
    "complexity threshold when stamped.\n"
    "# A row is a DEBT STATEMENT, NOT AN APPROVAL: the reason column records "
    "why it is carried, and the\n"
    "# baseline only ever tightens — re-stamp DOWNWARD or delete a row, never "
    "up to clear a finding.\n"
)
PYCACHE = "__pycache__"
FIXES = (
    "  named escapes: decompose OUTWARD (a sibling function or a new module, "
    "never a nested def); express the branches as a data table "
    "(check.py::steps is 670 lines at cognitive 14); define the error out of "
    "existence so the branch disappears."
)

_LOOPS = (ast.For, ast.AsyncFor, ast.While)
_COMPS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef)


def _kids(node, nesting, ctx):
    return sum(_visit(c, nesting, ctx) for c in ast.iter_child_nodes(node))


def _seq(stmts, nesting, ctx):
    return sum(_visit(s, nesting, ctx) for s in stmts)


def _h_if(node, nesting, ctx):
    return (
        1
        + nesting
        + _visit(node.test, nesting, ctx)
        + _seq(node.body, nesting + 1, ctx)
        + _h_orelse(node, nesting, ctx)
    )


def _h_orelse(node, nesting, ctx):
    """TRAP 1. Python parses `elif` as an `If` nested in `orelse`, so a naive
    recursion both double-counts and over-nests every ladder in the tree. An
    `elif` is HYBRID: +1 flat, NO nesting increment, body one level deeper. A
    written-out `else:` is +1 flat with its body one deeper. The discriminator
    is the column — a real `elif` starts at the parent `if`'s column."""
    tail = node.orelse
    if not tail:
        return 0
    head = tail[0]
    chained = len(tail) == 1 and isinstance(head, ast.If)
    if chained and head.col_offset == node.col_offset:
        return (
            1
            + _visit(head.test, nesting, ctx)
            + _seq(head.body, nesting + 1, ctx)
            + _h_orelse(head, nesting, ctx)
        )
    return _h_else(tail, nesting, ctx)


def _h_else(stmts, nesting, ctx):
    """`else` — on an `if`, and equally on Python's loop-`else`, which is a
    break in linear flow and a famously misread one: +1 flat, body one deeper.
    The spec has no loop-`else` (no Java analogue); the reference Python
    implementation charges it, and so does this."""
    return (1 + _seq(stmts, nesting + 1, ctx)) if stmts else 0


def _h_loop(node, nesting, ctx):
    head = node.test if isinstance(node, ast.While) else node.iter
    return (
        1
        + nesting
        + _visit(head, nesting, ctx)
        + _seq(node.body, nesting + 1, ctx)
        + _h_else(node.orelse, nesting, ctx)
    )


def _h_ifexp(node, nesting, ctx):
    return (
        1
        + nesting
        + _visit(node.test, nesting, ctx)
        + _visit(node.body, nesting + 1, ctx)
        + _visit(node.orelse, nesting + 1, ctx)
    )


def _h_except(node, nesting, ctx):
    """A catch is +1 however many types it names; `try`, `else` and `finally`
    are ignored altogether (spec, "Catches") — they fall through to `_kids`."""
    return 1 + nesting + _seq(node.body, nesting + 1, ctx)


def _h_match(node, nesting, ctx):
    """A `switch` and ALL its cases combined is ONE structural increment (spec,
    "Switches"): it is read at a glance, unlike an if/elif ladder that may
    compare any number of variables against anything. A `case ... if guard`
    adds +1 flat — the guard is the extra comparison a switch cannot express."""
    total = 1 + nesting + _visit(node.subject, nesting, ctx)
    for case in node.cases:
        if case.guard is not None:
            total += 1 + _visit(case.guard, nesting, ctx)
        total += _seq(case.body, nesting + 1, ctx)
    return total


def _h_boolop(node, nesting, ctx):
    """TRAP 2. +1 per RUN of like operators, not per operator: `a and b and c`
    is +1, `a and b or c` is +2. Python's parser already groups a run into one
    BoolOp with n values, so counting BoolOp NODES is counting runs."""
    return 1 + _kids(node, nesting, ctx)


def _h_lambda(node, nesting, ctx):
    return _kids(node, nesting + 1, ctx)


def _h_comp(node, nesting, ctx):
    """A comprehension is its own scope: nesting increment, no base increment
    (like a lambda). Each `if` clause is a real condition: +1 + inner nesting."""
    inner = nesting + 1
    clauses = sum(1 for gen in node.generators for _ in gen.ifs)
    return _kids(node, inner, ctx) + clauses * (1 + inner)


def _h_def(node, nesting, ctx):
    """A nested def takes the nesting increment and no base increment — unless
    Appendix A's Python-decorator exception exempts it."""
    return _kids(node, nesting + (0 if id(node) in ctx[1] else 1), ctx)


def _h_call(node, nesting, ctx):
    """Direct recursion is +1 per recursive call site: a bare `name(...)` or a
    `self`/`cls`-qualified `self.name(...)`. Anything else qualified is a
    DELEGATION, not recursion — `RoutingState.cool` calling `agent_route.cool`
    is the case that a bare attribute-name match gets wrong. Indirect recursion
    (the spec's "recursion cycle") needs a whole-program call graph and is out
    of scope."""
    func = node.func
    owner = getattr(func, "value", None)
    same = getattr(owner, "id", None) in ("self", "cls")
    hit = (
        func.id
        if isinstance(func, ast.Name)
        else (getattr(func, "attr", None) if same else None)
    )
    return (1 if hit == ctx[0] else 0) + _kids(node, nesting, ctx)


_HANDLERS = {
    ast.If: _h_if,
    ast.IfExp: _h_ifexp,
    ast.ExceptHandler: _h_except,
    ast.BoolOp: _h_boolop,
    ast.Lambda: _h_lambda,
    ast.Call: _h_call,
}
_HANDLERS.update({t: _h_loop for t in _LOOPS})
_HANDLERS.update({t: _h_comp for t in _COMPS})
_HANDLERS.update({t: _h_def for t in _DEFS})
if hasattr(ast, "Match"):
    _HANDLERS[ast.Match] = _h_match


def _visit(node, nesting, ctx):
    if node is None:
        return 0
    handler = _HANDLERS.get(type(node))
    return handler(node, nesting, ctx) if handler else _kids(node, nesting, ctx)


def _is_docstring(stmt):
    return (
        isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant)
        and isinstance(stmt.value.value, str)
    )


def _wrapped_def(node):
    """The inner `def` of Appendix A's Python-decorator shape — a body of
    nothing but an optional docstring, one nested def, and a `return` OF THAT
    DEF. Else None. The paper says "only a nested function and a return
    statement"; requiring the return to name the def is the narrow reading it
    asks for, and it is what stops a plain `def helper(): ...; return
    (helper(a), helper(b))` from claiming a decorator's exemption."""
    body = [s for s in node.body if not _is_docstring(s)]
    if (
        len(body) != 2
        or not isinstance(body[0], _DEFS)
        or not isinstance(body[1], ast.Return)
    ):
        return None
    return body[0] if getattr(body[1].value, "id", None) == body[0].name else None


def _exempt(fn):
    out, node = set(), _wrapped_def(fn)
    while node is not None:
        out.add(id(node))
        node = _wrapped_def(node)
    return out


def cognitive(fn):
    """The Sonar cognitive complexity of `fn`, nested defs and lambdas
    included."""
    return _seq(fn.body, 0, (fn.name, _exempt(fn)))


def _doc_lines(tree):
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef) + _DEFS) and node.body:
            head = node.body[0]
            if _is_docstring(head):
                out.update(range(head.lineno, head.end_lineno + 1))
    return out


def sloc(node, lines, doc_lines):
    """Non-blank, non-comment, non-docstring physical lines of `node`. Half the
    kit-scripts tree is prose by house style, so a raw line count would be
    measuring documentation."""
    live = [i for i in range(node.lineno, node.end_lineno + 1) if i not in doc_lines]
    body = [lines[i - 1].strip() for i in live]
    return sum(1 for text in body if text and not text.startswith("#"))


def _collect(node, prefix, out):
    """Every module-level function and method, qualified `Class.method`."""
    for field in ("body", "orelse", "finalbody", "handlers"):
        for child in getattr(node, field, None) or []:
            if isinstance(child, ast.ClassDef):
                _collect(child, prefix + child.name + ".", out)
            elif isinstance(child, _DEFS):
                out.append((prefix + child.name, child))
            elif isinstance(child, (ast.If, ast.Try, ast.With)):
                _collect(child, prefix, out)


def _public(tree):
    names = []
    for node in tree.body:
        if isinstance(node, (ast.ClassDef,) + _DEFS):
            names.append(node.name)
        elif isinstance(node, ast.Assign):
            names += [t.id for t in node.targets if isinstance(t, ast.Name)]
    return [n for n in names if not n.startswith("_")]


def _paths(root, includes):
    seen = set()
    for pattern in includes:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if PYCACHE not in path.parts and path.is_file() and rel not in seen:
                seen.add(rel)
                yield rel, path


def census(root, includes):
    """`(rows, modules)` — every function as `(path, name, cognitive, sloc)`
    and every module as `(path, public_symbols, lines)`. Paths are POSIX and
    relative to `root`, so a baseline is byte-identical on Windows and POSIX."""
    rows, modules = [], []
    for rel, path in _paths(root, includes):
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        lines, docs = text.splitlines(), _doc_lines(tree)
        found = []
        _collect(tree, "", found)
        rows += [(rel, n, cognitive(f), sloc(f, lines, docs)) for n, f in found]
        modules.append((rel, len(_public(tree)), len(lines)))
    return sorted(rows), sorted(modules)


def read_baseline(path):
    """`{(path, function): (cognitive, sloc, reason)}`; empty when unstamped."""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        cells = line.split("\t")
        if len(cells) < 4:
            continue
        reason = cells[4] if len(cells) > 4 else ""
        out[(cells[0], cells[1])] = (int(cells[2]), int(cells[3]), reason)
    return out


def write_baseline(path, rows, old):
    text = [DEBT_NOTE + HEADER]
    for rel, name, cog, lines in rows:
        reason = old.get((rel, name), ("", "", ""))[2]
        text.append("\t".join((rel, name, str(cog), str(lines), reason)))
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(text) + "\n")


def compare(over, old):
    """`(grew, improved)` as `[(path, function, was, now)]` — rows that rose
    above the baseline (or are new to it), and rows that fell below it (or
    vanished, reported as `now=None`)."""
    now = {(rel, name): cog for rel, name, cog, _ in over}
    grew, improved = [], []
    for key, score in sorted(now.items()):
        was = old[key][0] if key in old else None
        if was is None or score > was:
            grew.append(key + (was, score))
    for key, entry in sorted(old.items()):
        if now.get(key, -1) < entry[0]:
            improved.append(key + (entry[0], now.get(key)))
    return grew, improved


def _fail(grew, improved):
    for rel, name, was, score in grew:
        print(
            "check_complexity: FAIL - {}::{} cognitive {} -> {}. SIMPLIFY; a "
            "bump is a reviewed baseline edit whose reason lands in the log, "
            "never a drive-by.\n{}".format(rel, name, was, score, FIXES),
            file=sys.stderr,
        )
    for rel, name, was, score in improved:
        print(
            "check_complexity: FAIL - {}::{} cognitive {} -> {}. RE-STAMP "
            "DOWNWARD (or delete the row) in this same commit, so the ratchet "
            "only ever tightens; `--restamp` writes it.".format(rel, name, was, score),
            file=sys.stderr,
        )


def _report(rows, modules, threshold):
    print("# " + "\t".join(COLUMNS[:4]))
    for row in rows:
        print("\t".join(str(cell) for cell in row))
    for cut in sorted({threshold, 25, 50}):
        print("# over {}: {}".format(cut, sum(1 for r in rows if r[2] > cut)))
    for rel, public, lines in modules:
        print("# module\t{}\t{}\t{}".format(rel, public, lines))


def main(argv=None):
    utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("--mode", choices=("report", "warn", "enforce"), default="warn")
    ap.add_argument("--report", action="store_true", help="alias for --mode report")
    ap.add_argument("--restamp", action="store_true", help="rewrite the baseline")
    ap.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    ap.add_argument("--include", action="append", default=None, metavar="GLOB")
    ap.add_argument("--baseline", default=BASELINE)
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    rows, modules = census(root, tuple(args.include or DEFAULT_INCLUDE))
    if args.report or args.mode == "report":
        _report(rows, modules, args.threshold)
        return 0

    over = [r for r in rows if r[2] > args.threshold]
    path = root / args.baseline
    old = read_baseline(path)
    if args.restamp:
        write_baseline(path, over, old)
        print(
            "check_complexity: re-stamped {} row(s) -> {}".format(
                len(over), args.baseline
            )
        )
        return 0

    grew, improved = compare(over, old)
    if not grew and not improved:
        print(
            "check_complexity: OK - {} row(s) over {}, unchanged from baseline.".format(
                len(over), args.threshold
            )
        )
        return 0
    _fail(grew, improved)
    return 1 if args.mode == "enforce" else 0


if __name__ == "__main__":
    sys.exit(main())
