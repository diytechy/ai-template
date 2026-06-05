#!/usr/bin/env python3
"""Generate the module/function map for `architecture.md` from the source tree.

Stack-agnostic kit, **Python reference implementation** (stdlib only — uses
`ast`, no pip installs). It keeps `architecture.md` honest: the hand-written
overview stays, and everything between the GENERATED markers is regenerated
here so it cannot drift from the code. Swap this script for an equivalent in
your stack (e.g. `tsc`/ts-morph for TypeScript, `go doc` for Go) — the contract
is only the marker block it fills.

What it emits per public symbol (top-level, non-underscore) in each package:
    - module path, symbol name + signature, one-line docstring summary
    - any `Implements: SR-###, LLR-###` back-links found in the symbol's source
      (so reviewers and agents can see the requirement coverage inline)

This doubles as the **AI/human code map**: a single screen that tells an agent
where each capability lives and which requirement it implements, so it edits the
right place instead of re-deriving the layout.

Usage:
    python scripts/gen_arch_map.py [--src SRC ...] [--doc docs/architecture.md] [--check]

    --src     One or more source roots to scan (default: src). Repeatable.
    --doc     Architecture doc to update in place (default: docs/architecture.md).
    --check   Do not write; exit 1 if the doc is out of date (use in CI/harness).

The doc must contain these markers (the template ships with them):
    <!-- BEGIN GENERATED MODULE MAP -->
    <!-- END GENERATED MODULE MAP -->
"""
import argparse
import ast
import re
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN GENERATED MODULE MAP -->"
END = "<!-- END GENERATED MODULE MAP -->"
IMPLEMENTS_RE = re.compile(r"\b(?:SR|LLR|UN|TC)-\d+\b")


def first_line(text):
    """First non-empty line of a docstring, trimmed."""
    for line in (text or "").strip().splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def signature(node):
    """Render a function/method signature from its AST args (names only)."""
    a = node.args
    parts = [p.arg for p in (a.posonlyargs + a.args)]
    if a.vararg:
        parts.append("*" + a.vararg.arg)
    if a.kwonlyargs:
        if not a.vararg:
            parts.append("*")
        parts += [p.arg for p in a.kwonlyargs]
    if a.kwarg:
        parts.append("**" + a.kwarg.arg)
    return "({})".format(", ".join(parts))


def implements(node, source_lines):
    """Collect requirement ids annotated near a symbol (docstring + the few
    comment lines just above its definition)."""
    ids = set()
    doc = ast.get_docstring(node) or ""
    ids.update(IMPLEMENTS_RE.findall(doc))
    start = node.lineno - 1  # 0-based line of the def
    for i in range(max(0, start - 4), start):
        line = source_lines[i]
        if "Implements" in line or line.lstrip().startswith("#"):
            ids.update(IMPLEMENTS_RE.findall(line))
    return sorted(ids)


def scan_module(path, root):
    """Return (rel_module, [rows]) for one .py file; rows describe public items."""
    text = path.read_text(encoding="utf-8")
    source_lines = text.splitlines()
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:  # surface, don't crash the whole run
        rel = path.relative_to(root).as_posix()
        return rel, [(":parse-error:", "", str(exc), [])]
    rel = path.relative_to(root).with_suffix("").as_posix().replace("/__init__", "")
    rows = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            rows.append((node.name, signature(node),
                         first_line(ast.get_docstring(node)),
                         implements(node, source_lines)))
        elif isinstance(node, ast.ClassDef):
            if node.name.startswith("_"):
                continue
            methods = [n.name for n in node.body
                       if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                       and not n.name.startswith("_")]
            sig = " · ".join(methods)
            rows.append((node.name + " (class)", "", first_line(ast.get_docstring(node)),
                         implements(node, source_lines)))
            if sig:
                rows.append(("  methods", "", sig, []))
    return rel, rows


def build_map(src_roots):
    out = ["| Module | Public item | Summary | Implements |",
           "|---|---|---|---|"]
    any_rows = False
    for root in src_roots:
        root = Path(root)
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            if any(part.startswith((".", "__pycache__")) for part in path.parts):
                continue
            rel, rows = scan_module(path, root.parent if root.name else root)
            for name, sig, summary, ids in rows:
                any_rows = True
                impl = ", ".join(ids) if ids else ""
                out.append("| `{}` | `{}{}` | {} | {} |".format(
                    rel, name, sig, summary.replace("|", "\\|"), impl))
    if not any_rows:
        out.append("| _(no source scanned)_ | | | |")
    note = ("_Generated by `scripts/gen_arch_map.py` from the source tree. "
            "Do not edit by hand; run the check harness to refresh._")
    return note + "\n\n" + "\n".join(out)


def splice(doc_text, generated):
    if BEGIN not in doc_text or END not in doc_text:
        raise SystemExit(
            "architecture doc is missing the GENERATED MODULE MAP markers:\n"
            "  {}\n  {}".format(BEGIN, END))
    pre = doc_text.split(BEGIN)[0]
    post = doc_text.split(END)[1]
    return "{}{}\n{}\n{}{}".format(pre, BEGIN, generated, END, post)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", action="append", default=None,
                    help="source root to scan (repeatable; default: src)")
    ap.add_argument("--doc", default="docs/architecture.md",
                    help="architecture doc to update (default: docs/architecture.md)")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if the doc is stale")
    args = ap.parse_args()

    src_roots = args.src or ["src"]
    doc = Path(args.doc)
    if not doc.exists():
        raise SystemExit("architecture doc not found: {}".format(doc))

    generated = build_map(src_roots)
    current = doc.read_text(encoding="utf-8")
    updated = splice(current, generated)

    if args.check:
        if updated != current:
            print("architecture map is STALE: run `python scripts/gen_arch_map.py`",
                  file=sys.stderr)
            sys.exit(1)
        print("architecture map up to date.")
        return

    if updated != current:
        doc.write_text(updated, encoding="utf-8")
        print("architecture map regenerated -> {}".format(doc))
    else:
        print("architecture map already up to date.")


if __name__ == "__main__":
    main()
