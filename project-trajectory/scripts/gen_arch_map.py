#!/usr/bin/env python3
"""Generate the module/function map for `architecture.md` from the source tree.

Stack-agnostic kit, **Python reference implementation** (stdlib only — uses
`ast`, no pip installs). It keeps `architecture.md` honest: the hand-written
overview stays, and everything between the GENERATED markers is regenerated
here so it cannot drift from the code. Swap this script for an equivalent in
your stack (e.g. `tsc`/ts-morph for TypeScript, `go doc` for Go) — the contract
is only the marker block it fills.

What it emits, per module (one section each):
    - the module's one-line **summary** (its module docstring) — so an agent
      grasps each file's job without opening it;
    - **internal coupling**: which other in-tree modules it imports (best-effort)
      — makes layering/dependency invariants visible (e.g. "Common must not
      import Engine") and tells an agent the blast radius of a change;
    - each public symbol's **signature**, one-line docstring summary, and any
      `Implements: SR-###, LLR-###` back-links found near it.

This is the **AI/human code map**: a current, greppable index of where each
capability lives, what it depends on, and which requirement it implements — so an
agent edits the right place instead of re-deriving the layout. It is harvested
from your docstrings/headers, which is one more reason to comment for humans
(see CLAUDE.template.md "Comment for humans — and the map").

Routing: `--doc` is repeatable, so the same generated block can be spliced into
`docs/architecture.md` AND the agent's primary file (`AGENTS.md` / `CLAUDE.md`) —
wherever the marker pair lives. Embed it where agents actually read.

Usage:
    python scripts/gen_arch_map.py [--src SRC ...] [--doc FILE ...] [--check]

    --src     One or more source roots to scan (default: src). Repeatable.
    --doc     File(s) to update in place (default: docs/architecture.md).
              Repeatable — each must contain the marker pair below.
    --check   Do not write; exit 1 if any target is out of date (use in CI/harness).

Each target file must contain these markers (the templates ship with them):
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


def internal_imports(tree, internal_names):
    """In-tree modules this file imports (best-effort: relative imports, or an
    absolute import whose first segment names a scanned module/package)."""
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level:  # relative import -> always internal
                found.add("." * node.level + (node.module or ""))
            elif node.module and node.module.split(".")[0] in internal_names:
                found.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in internal_names:
                    found.add(alias.name)
    return sorted(found)


def scan_module(path, root, internal_names):
    """Return (rel_module, summary, imports, rows) for one .py file."""
    text = path.read_text(encoding="utf-8")
    source_lines = text.splitlines()
    rel = path.relative_to(root).with_suffix("").as_posix().replace("/__init__", "")
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:  # surface, don't crash the whole run
        return rel, "PARSE ERROR: {}".format(exc), [], []
    summary = first_line(ast.get_docstring(tree))
    imports = internal_imports(tree, internal_names)
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
            rows.append((node.name + " (class)", "", first_line(ast.get_docstring(node)),
                         implements(node, source_lines)))
            if methods:
                rows.append(("  methods", "", " · ".join(methods), []))
    return rel, summary, imports, rows


def _module_files(src_roots):
    """Yield (path, root_parent) for every scanned .py file, with the set of
    internal module/package names (for coupling detection)."""
    files = []
    names = set()
    for root in src_roots:
        root = Path(root)
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            if any(part.startswith((".", "__pycache__")) for part in path.parts):
                continue
            files.append((path, root.parent if root.name else root))
            names.add(path.stem)
            for part in path.relative_to(root).parts[:-1]:
                names.add(part)
    return files, names


def build_map(src_roots):
    files, internal_names = _module_files(src_roots)
    note = ("_Generated by `scripts/gen_arch_map.py` from the source tree (AST). "
            "Do not edit by hand; run the check harness to refresh. Summaries and "
            "`Implements:` come from your docstrings/comments._")
    if not files:
        return note + "\n\n_(no source scanned)_"
    sections = [note]
    for path, root_parent in files:
        rel, summary, imports, rows = scan_module(path, root_parent, internal_names)
        if not (summary or imports or rows):
            continue  # skip empty modules (e.g. bare __init__.py) — no noise
        sections.append("\n### `{}`".format(rel))
        if summary:
            sections.append("_{}_".format(summary.replace("|", "\\|")))
        if imports:
            sections.append("Imports (internal): {}".format(
                ", ".join("`{}`".format(i) for i in imports)))
        if rows:
            sections.append("\n| Public item | Summary | Implements |\n|---|---|---|")
            for name, sig, summ, ids in rows:
                sections.append("| `{}{}` | {} | {} |".format(
                    name, sig, summ.replace("|", "\\|"),
                    ", ".join(ids) if ids else ""))
        else:
            sections.append("_(no public items)_")
    return "\n".join(sections)


def splice(doc_text, generated, target):
    if BEGIN not in doc_text or END not in doc_text:
        raise SystemExit(
            "{} is missing the GENERATED MODULE MAP markers:\n"
            "  {}\n  {}".format(target, BEGIN, END))
    pre = doc_text.split(BEGIN)[0]
    post = doc_text.split(END)[1]
    return "{}{}\n{}\n{}{}".format(pre, BEGIN, generated, END, post)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", action="append", default=None,
                    help="source root to scan (repeatable; default: src)")
    ap.add_argument("--doc", action="append", default=None,
                    help="file(s) to update; repeatable (default: docs/architecture.md). "
                         "Point at AGENTS.md / CLAUDE.md too to route the map there.")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if any target is stale")
    args = ap.parse_args()

    src_roots = args.src or ["src"]
    docs = [Path(d) for d in (args.doc or ["docs/architecture.md"])]
    generated = build_map(src_roots)

    stale = False
    for doc in docs:
        if not doc.exists():
            raise SystemExit("target file not found: {}".format(doc))
        current = doc.read_text(encoding="utf-8")
        updated = splice(current, generated, doc)
        if args.check:
            if updated != current:
                stale = True
                print("code map STALE in {}: run `python scripts/gen_arch_map.py`"
                      .format(doc), file=sys.stderr)
        elif updated != current:
            doc.write_text(updated, encoding="utf-8")
            print("code map regenerated -> {}".format(doc))
        else:
            print("code map already up to date -> {}".format(doc))

    if args.check:
        if stale:
            sys.exit(1)
        print("code map up to date.")


if __name__ == "__main__":
    main()
