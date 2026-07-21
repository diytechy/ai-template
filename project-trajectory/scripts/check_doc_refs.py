#!/usr/bin/env python3
"""Doc reference validation — prose that names dead files or symbols (Thread 49).

`check_docs.py` proves a markdown *link* resolves; this closes the two rot
classes links can't see, with false-positive control as the design center
(validate precise shapes, never every backticked word):

  1. PATH TIER (aggressive — low ambiguity, high value): a backticked token
     shaped like a repo path (contains "/" and ends in a known source/doc
     extension, or starts with a conventional top-level dir) must exist on
     disk. A renamed or deleted file named in prose is one of the commonest
     real rots. URLs, globs, and `{placeholder}` shapes are skipped; a line
     carrying `path-ok` is exempt (the `privacy-ok` idiom) for deliberate
     examples naming files that don't exist here.
  2. SYMBOL TIER (opt-in convention — no heuristic storm): only references
     written `sym:<module>.<name>` are checked, against the generated module
     map in architecture.md (the arch-map inventory is the oracle — reuse the
     artifact, don't re-parse the AST). You *assert* a symbol exists and the
     check holds you to it. No module map / no symbols -> the tier skips
     cleanly (a files-mode or non-Python stack degrades gracefully).

Ships WARN-FIRST and product-layer like check_stubs.py: exit 0 with warnings
unless --strict; NOT wired into check.py's required floor. Opt in per repo:

    [step:doc-refs]
    command = {py} scripts/check_doc_refs.py --strict

Scan surface = root *.md + docs/**/*.md (the check_docs surface). Stdlib only.

Contracts: IF-008, IF-028 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import re
import sys
from pathlib import Path

# A backticked token is path-shaped when it has a separator AND either a known
# extension or a conventional top-level prefix — the bounded rule that keeps
# `off`, `type`, shell snippets and other repos' names out of scope.
PATH_EXTS = (
    ".py",
    ".md",
    ".csv",
    ".ini",
    ".yml",
    ".yaml",
    ".sh",
    ".ps1",
    ".cmd",
    ".command",
    ".json",
    ".html",
    ".toml",
    ".cfg",
    ".txt",
)
PATH_PREFIXES = (
    "scripts/",
    "docs/",
    "src/",
    "tests/",
    ".githooks/",
    ".github/",
    "registries/",
    "skills/",
    "ci/",
    "hooks/",
)
BACKTICK = re.compile(r"`([^`\n]+)`")
SYM = re.compile(r"\bsym:([A-Za-z_][\w.]*)\.(\w+)\b")
MOD_HEAD = re.compile(r"^### `([^`]+)`")
SYM_ROW = re.compile(r"^\| `(\w+)[(`]")


def is_path_shaped(token):
    token = token.strip()
    if not token or "://" in token or any(c in token for c in "*{}<>$ "):
        return False
    # `::` is a pytest node id (tests/x.py::test_name — the kit's sanctioned
    # Evidence form, a real file plus a selector), and `;`/`,` join a list of
    # paths; none is a single filesystem path, so they are out of the path
    # tier's scope (false-positive control is the point).
    if "::" in token or ";" in token or "," in token:
        return False
    if "/" not in token:
        return False
    return token.rstrip("/").endswith(PATH_EXTS) or token.startswith(PATH_PREFIXES)


def _generated_prefixes(root):
    """Directory prefixes marked `linguist-generated` in .gitattributes (e.g.
    `docs/okf/`), so the tool never lints its own generated output — the same
    "don't lint generated" stance the GENERATED marker-block skip already
    encodes for inline blocks."""
    ga = root / ".gitattributes"
    prefixes = []
    if not ga.exists():
        return prefixes
    for line in ga.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "linguist-generated" not in line:
            continue
        glob = line.split()[0]
        # `docs/okf/**` / `docs/okf/*` -> `docs/okf/`
        prefix = glob.rstrip("*").rstrip("/")
        if prefix:
            prefixes.append(prefix + "/")
    return prefixes


def doc_files(root):
    seen = sorted(root.glob("*.md")) + sorted((root / "docs").rglob("*.md"))
    skip = _generated_prefixes(root)
    out = []
    for p in seen:
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if any(rel.startswith(pre) for pre in skip):
            continue  # generated tree — its freshness is the generator's --check
        out.append(p)
    return out


def load_symbol_oracle(arch_path):
    """{module-tail: {symbols}} parsed from the generated module map, or {}."""
    if not arch_path.exists():
        return {}
    oracle, current = {}, None
    for line in arch_path.read_text(
        encoding="utf-8-sig", errors="replace"
    ).splitlines():
        m = MOD_HEAD.match(line)
        if m:
            current = m.group(1).replace("\\", "/").split("/")[-1]
            oracle.setdefault(current, set())
            continue
        s = SYM_ROW.match(line)
        if s and current:
            oracle[current].add(s.group(1))
    return {k: v for k, v in oracle.items() if v}


def findings_for(doc, root, oracle):
    out = []
    rel = doc.relative_to(root).as_posix()
    in_generated = False
    for n, line in enumerate(
        doc.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1
    ):
        # Generated marker blocks (the module map, flow diagrams) are not
        # hand-authored prose — their freshness is the generator's --check
        # contract, and their tokens (module names like `src/demo`) are not
        # disk paths. The rot this tool hunts lives outside them.
        if "<!-- BEGIN GENERATED" in line:
            in_generated = True
        if "<!-- END GENERATED" in line:
            in_generated = False
            continue
        if in_generated:
            continue
        if "path-ok" in line:
            continue  # deliberate example naming a path that isn't here
        for token in BACKTICK.findall(line):
            if (
                is_path_shaped(token)
                and not (root / token.strip().rstrip("/")).exists()
            ):
                out.append(
                    "{}:{}: `{}` does not exist in the repo".format(rel, n, token)
                )
        for mod, name in SYM.findall(line):
            if not oracle:
                continue  # no inventory -> the symbol tier skips (docstring)
            tail = mod.split(".")[-1]
            known = oracle.get(tail)
            if known is None:
                out.append(
                    "{}:{}: sym:{}.{} — module {!r} is not in the module map".format(
                        rel, n, mod, name, tail
                    )
                )
            elif name not in known:
                out.append(
                    "{}:{}: sym:{}.{} — symbol {!r} is not in module {!r}'s "
                    "public inventory".format(rel, n, mod, name, name, tail)
                )
    return out


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII path / title / registry cell can't raise UnicodeEncodeError on a
    legacy Windows cp1252 console (verbatim across the
    kit). Python 3.7+ streams expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--arch",
        default="docs/architecture.md",
        help="module-map doc holding the symbol inventory (the sym: oracle)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 on findings (default: warn-first, exit 0)",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()
    oracle = load_symbol_oracle(root / args.arch)
    if not oracle:
        print(
            "check_doc_refs: no symbol inventory in {} — the sym: tier is "
            "skipped (path tier still runs).".format(args.arch)
        )
    findings = []
    for doc in doc_files(root):
        findings += findings_for(doc, root, oracle)
    for f in findings:
        print("check_doc_refs: WARN - " + f, file=sys.stderr)
    if findings:
        print(
            "check_doc_refs: {} dangling reference(s){}.".format(
                len(findings), "" if args.strict else " (warn-first; --strict gates)"
            )
        )
        return 1 if args.strict else 0
    print("check_doc_refs: OK - no dangling path or sym: references.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
