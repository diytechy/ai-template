"""OI-130 re-score, step 2: exact-clone function bodies (4+ lines) and top-level function names defined in
more than one module under project-trajectory/scripts/. Run from the repo root: python census.py"""

import ast, hashlib, collections
from pathlib import Path

S = Path("project-trajectory/scripts")


def key(p):
    return p.relative_to(S).with_suffix("").as_posix().replace("/__init__", "")


def body(n):
    b = n.body
    if (
        b
        and isinstance(b[0], ast.Expr)
        and isinstance(b[0].value, ast.Constant)
        and isinstance(b[0].value.value, str)
    ):
        b = b[1:]
    return b


clones = collections.defaultdict(list)
names = collections.defaultdict(list)
for p in sorted(S.rglob("*.py")):
    if "__pycache__" in p.parts:
        continue
    t = ast.parse(p.read_bytes())
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            b = body(n)
            L = n.end_lineno - n.lineno + 1
            if b and L >= 4:
                clones[
                    hashlib.sha1("\n".join(map(ast.dump, b)).encode()).hexdigest()
                ].append((key(p), n.name, L))
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names[n.name].append((key(p), n.end_lineno - n.lineno + 1))
d = [v for v in clones.values() if len(v) > 1]
print(
    "EXACT CLONES groups",
    len(d),
    "copies",
    sum(len(v) - 1 for v in d),
    "lines",
    sum(sum(x[2] for x in v[1:]) for v in d),
)
for v in sorted(d, key=lambda v: -len(v)):
    print("  ", v)
skip = {
    "main",
    "_parse_args",
    "parse_args",
    "build_parser",
    "_build_parser",
    "emit",
    "render",
    "load",
    "esc",
    "rel",
    "digest",
    "_main",
}
multi = {k: v for k, v in names.items() if len(v) > 1 and k not in skip}
print("DUP TOP-LEVEL NAMES", len(multi))
for k, v in sorted(multi.items(), key=lambda kv: -len(kv[1])):
    print("  ", k, v)
