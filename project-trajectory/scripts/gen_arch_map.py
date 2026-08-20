#!/usr/bin/env python3
"""The module/function AST walk behind the DERIVED architecture (WI-455).

Stack-agnostic kit, **Python reference implementation** (stdlib only — uses
`ast`, no pip installs). `scan_inventory()` is the ONE walk the derived
architecture reads — the dashboard's How-SW tab, check_trajectory's
coverage/containment rules and check_doc_refs' sym: oracle all consume it
live, so the picture cannot drift from the code. The CLI additionally splices
the RENDERED map into opt-in `--doc` marker blocks (an agent guide, a doc you
keep); swap it for an equivalent in your stack (e.g. `tsc`/ts-morph for
TypeScript, `go doc` for Go) — there the contract is only the marker block it
fills. (The scaffolded `docs/architecture.md` default target retired at
WI-455, sitting-2 decision 8.)

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
(see AGENTS.template.md "Comment for humans — and the map").

Routing: `--doc` is repeatable, so the same generated block can be spliced into
several files — wherever the marker pair lives (`AGENTS.md` / `CLAUDE.md`, a
kept doc). Embed it where agents actually read.

Program flow (`--flow ENTRY`): emit the **ordered internal calls** an entry/
orchestrator function makes, each with the callee's one-line summary, into a
GENERATED FLOW block. This makes the high-level flow readable at a glance AND
acts as a tripwire: a thin orchestrator yields a clean numbered flow; one that
inlines logic instead of delegating shows up as a short, uninformative list.
(Control flow — loops/branches — is not represented; keep the overview prose for
that.)

Dependency diagram: the same internal imports the map lists, rendered as a
Mermaid `graph LR` and spliced into the DEPENDENCY DIAGRAM markers wherever a
--doc has them. Output is plain text —
GitHub/GitLab and the VS Code Markdown preview render mermaid fences natively,
so the kit needs no diagram toolchain — and layering violations (e.g. an arrow
from `common` into `engine`) are visible at a glance.

A syntax-broken module is rendered as a `PARSE ERROR` summary rather than
crashing the run (so the rest of the map still generates). That keeps the error
*visible*, but `--check` alone would still pass once the PARSE ERROR text is
written; pass `--strict-parse` to also *fail* on any unparseable module — for a
non-Python stack where this map is the only parse signal, or to belt-and-braces
the lint/test steps.

Stack-neutral fallback (`--mode files`): when no parser for your language is
handy, fill the same MODULE MAP block with **one row per source file** — its
path plus the first comment line as a summary — instead of symbol-level rows.
The freshness contract is identical: a file added/removed/renamed, or a
summary-line edit, refreshes the map and so trips `--check`. Coarser than the
symbol-level default, but it restores a real drift check for *any* stack without
porting a generator (see ADOPTING.md). `--comment-prefix` sets the comment
tokens scanned (default `#`, `//`, `--`). `--flow` and the dependency diagram
are symbol-mode only (they need a parser).

Usage:
    python scripts/gen_arch_map.py --doc FILE [--src SRC ...] [--flow ENTRY]
                                   [--mode symbols|files] [--comment-prefix TOK ...]
                                   [--check] [--strict-parse]

    --src            One or more source roots to scan (default: src). Repeatable.
    --doc            File(s) to update in place (required; repeatable) — each
                     must contain the MODULE MAP marker pair.
    --flow           Entry function (e.g. `run` or `module:run`) whose call
                     sequence is spliced into the FLOW markers of any --doc.
    --mode           `symbols` (default; Python-AST symbol map + diagram/flow) or
                     `files` (stack-neutral file-level fallback; see above).
    --comment-prefix Comment token(s) whose first occurrence yields a file's
                     summary in `--mode files` (repeatable; default `#`,`//`,`--`).
    --check          Do not write; exit 1 if any target is out of date (CI/harness).
    --strict-parse   Exit 1 if any scanned module fails to parse (independent of
                     --check staleness).

Marker pairs (the templates ship with them):
    <!-- BEGIN GENERATED MODULE MAP -->  ... <!-- END GENERATED MODULE MAP -->   (required per --doc)
    <!-- BEGIN GENERATED FLOW -->        ... <!-- END GENERATED FLOW -->          (optional; used by --flow)
    <!-- BEGIN GENERATED DEPENDENCY DIAGRAM --> ... <!-- END GENERATED DEPENDENCY DIAGRAM -->  (optional)

Contracts: IF-010, IF-025 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import ast
import re
import sys
from pathlib import Path

# Sibling: the registry CARRIER. Run as a subprocess this script's own dir is
# sys.path[0] so a plain import resolves; the guard covers an in-process import
# (a test) whose sys.path does not yet carry scripts/ — the sanctioned-sibling
# idiom trace.py uses for trace_text and check_trajectory for this same module.
# Taken at WI-443, when `interfaces` moved to the TOML carrier: the alternative
# was a SECOND home for the IF column vocabulary inside this file, which is the
# exact drift `spine_carrier`'s one-home rule exists to prevent, and bootstrap
# already ships `spine_carrier.py` into every scaffold.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is. Kit
    scripts print non-ASCII (an em-dash WARNING, `§` refs) that a legacy Windows
    cp1252 console raises UnicodeEncodeError on — wedging the run, not just
    mojibaking. Python 3.7+ streams expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


BEGIN = "<!-- BEGIN GENERATED MODULE MAP -->"
END = "<!-- END GENERATED MODULE MAP -->"
BEGIN_FLOW = "<!-- BEGIN GENERATED FLOW -->"
END_FLOW = "<!-- END GENERATED FLOW -->"
BEGIN_DIAGRAM = "<!-- BEGIN GENERATED DEPENDENCY DIAGRAM -->"
END_DIAGRAM = "<!-- END GENERATED DEPENDENCY DIAGRAM -->"
IMPLEMENTS_RE = re.compile(r"\b(?:SR|LLR|SN|TC)-\d+\b")
# Interface-seam ids a module declares via a `Contracts: IF-###, ...` line
# (process.md §8) — harvested like Implements, but module-level (WI-056).
CONTRACTS_RE = re.compile(r"\bIF-\d+\b")
IF_ID_RE = re.compile(r"IF-\d+")
# Source-file extensions stripped when normalizing a module path, so a diagram
# node (`scripts/check`) and an IF endpoint written with the full repo path
# (`project-trajectory/scripts/check.py`) collapse to one key. Kept in sync with
# trace.py / check_trajectory (a small stable helper duplicated per the F5 rule).
_MODULE_EXTS = (".py", ".sh", ".ps1", ".ts", ".js", ".go", ".rs", ".cmd")
# Comment tokens the file-level fallback (--mode files) reads a summary from.
# The three most common line-comment markers; override with --comment-prefix.
DEFAULT_COMMENT_PREFIXES = ("#", "//", "--")


def load_interfaces(path):
    """The rows of the IF-### seam registry as dicts, or [] when the registry is
    absent under either carrier — an unused/absent registry adds no IF edges
    (vacuous). Read through `spine_carrier`, so a repo that has not migrated off
    `interfaces.csv` still resolves."""
    return spine_carrier.load(Path(path), "IF-ID")


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


def module_bindings(tree):
    """Every name a module BINDS at module scope, plus class-level `def` names.

    The rendered map is deliberately a PUBLIC-API view — `scan_module` drops
    `_`-prefixed names and never lists a module constant — so the map cannot
    answer "does this name exist here". A spine consumer needs that question
    answered: measured at WI-429, 41 of the kit's 149 live LLR `CodeSymbol`
    cells name a private helper (`_ring_ink`), a module constant
    (`STATUS_FILL`) or a class method, all of which are real code and none of
    which the rendered table can see.

    So the binding set lives HERE, next to the walk that renders the map, and
    not in the consumer: a second AST symbol parser in a second script is the
    D-6/F5 hazard — a copy that has not learned a node type does not fail
    loudly, it silently reports "that symbol does not exist". Two walks inside
    ONE file is the residual cost, and it is pinned rather than trusted:
    `tests/test_arch_map.py` asserts every public item `scan_module` renders is
    in this set, for every module in the repo.

    Module scope only, by design. A local variable inside a function is not a
    name the module offers, and treating one as a binding would make the
    consumer's answer meaningless (the census found `budget_findings` and
    `tier_legend` cited as symbols when both are function locals)."""
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.ClassDef):
            names.add(node.name)
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    names.add(sub.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


class ContractsGrammarError(ValueError):
    """A module's `Contracts:` block declares an IF-### id only on a
    continuation line that opens with a bare id token (WI-478) — the
    ambiguous wrapped-list shape a comma-separated `Contracts: X (...), Y
    (...), ...` enumeration produces when it line-wraps mid-list. A
    marker-line-only grammar cannot silently accept that shape; move the id
    onto the line carrying the literal word `Contracts` instead of letting it
    wrap onto its own line."""


# The marker-line-only Contracts grammar (WI-478): every id a module declares
# belongs on the line carrying the word `Contracts`. A later, unindented line
# in the same paragraph/comment run may still MENTION an id already found
# there — ordinary explanatory prose, common across the kit's own modules
# (`adjudicate_brief.py`, `agent_loop.py`, ...) — but a line that OPENS with a
# bare `IF-###` token no earlier line declared reads as a new list item, not a
# mid-sentence aside: that shape is refused rather than silently dropped.
_LEADING_ID_RE = re.compile(r"^(IF-\d+)\b")


def _refuse_ambiguous_continuation(lines, ids):
    """Raise ContractsGrammarError if any `lines` (the text following a
    Contracts marker line, up to the first blank line) opens with a bare
    `IF-###` token not already in `ids`. Never adds to `ids` itself — a
    continuation line is prose, not a second declaration site."""
    for line in lines:
        if not line.strip():
            return  # blank line ends the paragraph/comment run
        m = _LEADING_ID_RE.match(line.strip())
        if m and m.group(1) not in ids:
            raise ContractsGrammarError(
                "Contracts: {} is declared only on a continuation line "
                "({!r}) — WI-478's marker-line grammar requires every "
                "declared id on the line carrying the word `Contracts`; move "
                "it there.".format(m.group(1), line.strip())
            )


def module_contracts(tree, source_lines):
    """The IF-### seam ids this module declares via a `Contracts: IF-###, ...`
    line in its module docstring or a top-of-file comment (WI-056). Restricted to
    lines carrying the word `Contracts`, so an IF id merely mentioned in prose is
    not mistaken for a declaration.

    Grammar (WI-478): the declared ids are the ones on that marker line, full
    stop — `_refuse_ambiguous_continuation` hard-fails rather than silently
    missing an id a wrapped enumeration pushed onto its own line (dispatch.py's
    real defect: IF-088/IF-089 read as undeclared because they opened
    continuation lines the old harvester never scanned)."""
    ids = set()
    doc = ast.get_docstring(tree) or ""
    doc_lines = doc.splitlines()
    for i, line in enumerate(doc_lines):
        if "Contracts" in line:
            ids.update(CONTRACTS_RE.findall(line))
            _refuse_ambiguous_continuation(doc_lines[i + 1 :], ids)
    for i, line in enumerate(source_lines[:8]):
        if "Contracts" in line and line.lstrip().startswith("#"):
            ids.update(CONTRACTS_RE.findall(line))
            _refuse_ambiguous_continuation(source_lines[i + 1 : 8], ids)
    return sorted(ids)


def _norm_module(path):
    """A module path reduced to a naming-convention-neutral key (strip a leading
    `project-trajectory/`, any source extension, `/__init__`) so an IF endpoint
    and a diagram node match regardless of which form the author used."""
    p = (path or "").strip().replace("\\", "/")
    if p.startswith("project-trajectory/"):
        p = p[len("project-trajectory/") :]
    for ext in _MODULE_EXTS:
        if p.endswith(ext):
            p = p[: -len(ext)]
            break
    if p.endswith("/__init__"):
        p = p[: -len("/__init__")]
    return p


def internal_imports(tree, internal_names):
    """In-tree modules this file imports (best-effort: relative imports, or an
    absolute import whose first segment names a scanned module/package).

    `from pkg import mod` is recorded as `pkg.mod` when `mod` names a scanned
    module — the real dependency is the submodule, not the package — except
    when the imported name shadows the module it comes from (`from .util
    import util`), where the module itself is the right target."""
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level or (
                node.module and node.module.split(".")[0] in internal_names
            ):
                prefix = "." * node.level + (node.module or "")
                last = (node.module or "").split(".")[-1]
                submodules = [
                    a.name
                    for a in node.names
                    if a.name in internal_names and a.name != last
                ]
                if submodules:
                    sep = "." if node.module else ""
                    for sub in submodules:
                        found.add(prefix + sep + sub)
                else:
                    found.add(prefix)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in internal_names:
                    found.add(alias.name)
    return sorted(found)


def scan_module(path, root, internal_names):
    """Return (rel_module, summary, imports, contracts, rows) for one .py file."""
    text = path.read_text(encoding="utf-8")
    source_lines = text.splitlines()
    rel = path.relative_to(root).with_suffix("").as_posix().replace("/__init__", "")
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:  # surface, don't crash the whole run
        return rel, "PARSE ERROR: {}".format(exc), [], [], []
    summary = first_line(ast.get_docstring(tree))
    imports = internal_imports(tree, internal_names)
    contracts = module_contracts(tree, source_lines)
    rows = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            rows.append(
                (
                    node.name,
                    signature(node),
                    first_line(ast.get_docstring(node)),
                    implements(node, source_lines),
                )
            )
        elif isinstance(node, ast.ClassDef):
            if node.name.startswith("_"):
                continue
            methods = [
                n.name
                for n in node.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not n.name.startswith("_")
            ]
            rows.append(
                (
                    node.name + " (class)",
                    "",
                    first_line(ast.get_docstring(node)),
                    implements(node, source_lines),
                )
            )
            if methods:
                rows.append(("  methods", "", " · ".join(methods), []))
    return rel, summary, imports, contracts, rows


def _module_files(src_roots):
    """Yield (path, root_parent) for every scanned .py file, with the set of
    internal module/package names (for coupling detection)."""
    files = []
    names = set()
    for root, base, path in _walk_roots(src_roots, "*.py"):
        files.append((path, base))
        names.add(path.stem)
        for part in path.relative_to(root).parts[:-1]:
            names.add(part)
    return files, names


def _is_hidden_rel(rel):
    """Whether a path RELATIVE TO ITS SCAN ROOT is hidden (a dot- or
    `__pycache__` part) and so not source.

    Root-relative is load-bearing, not incidental: the same test against the
    path's *absolute* parts made every repo whose checkout sits under a
    dot-prefixed directory (`~/.local/src`, a CI cache, a dot-prefixed pytest
    temp root) scan to an empty map with exit 0 (WI-363). Where the caller keeps
    the repo is not the caller's hidden-file intent; only what is inside the
    root they pointed at is."""
    return any(part.startswith((".", "__pycache__")) for part in rel.parts)


def _walk_roots(src_roots, pattern):
    """Yield `(root, base, path)` for every non-hidden `pattern` match under each
    existing root, sorted. `base` is the rel-path base (`root.parent`, or `root`
    itself for a bare name).

    The "which files count as source" rule — skip anything with a dot- or
    `__pycache__` path part — lived in both collectors below and is stated here
    once (WI-347). Both arms are in this one file, so the cross-script F5
    sanction never covered them."""
    for root in src_roots:
        root = Path(root)
        if not root.exists():
            continue
        base = root.parent if root.name else root
        for path in sorted(root.rglob(pattern)):
            if _is_hidden_rel(path.relative_to(root)):
                continue
            yield root, base, path


def _warn_hidden_swallow(src_roots, pattern, what):
    """Emit the sharper zero-scan warning when hidden dirs ate the whole map.

    Split out of main() so the conditional lives here, not in main's C901
    budget; `what` names the counted unit honestly per mode ("modules" for
    symbols, "source files" for files)."""
    hidden = _hidden_dirs_swallowing_source(src_roots, pattern)
    if hidden:
        print(
            "gen_arch_map: WARNING - the scan found zero {}, yet {} "
            "hold(s) matching files that were skipped as hidden. The "
            "dot-prefixed skip applies only to paths INSIDE a --src root "
            "(a dot-prefixed parent of the checkout is not filtered), so "
            "if that is real source, rename the directory or pass it as "
            "its own --src root.".format(what, ", ".join(hidden)),
            file=sys.stderr,
        )


def _hidden_dirs_swallowing_source(src_roots, pattern):
    """Dot-prefixed directories INSIDE a scan root, as `<root>/<reldir>` strings,
    that hold `pattern` files the hidden-skip dropped.

    Only meaningful when the scan already yielded nothing — then these are the
    directories that ate the whole map. A dot-prefixed *file* (`src/.gitkeep`,
    the placeholder every fresh scaffold ships) and a `__pycache__` directory
    are deliberately not reported: those are intentionally-hidden non-source, so
    naming them would fire this warning on every empty repo."""
    hits = set()
    for root in src_roots:
        root = Path(root)
        if not root.exists():
            continue
        for path in root.rglob(pattern):
            if not path.is_file():
                continue
            dirs = path.relative_to(root).parts[:-1]
            for i, part in enumerate(dirs):
                if part.startswith("."):
                    hits.add(root.joinpath(*dirs[: i + 1]).as_posix())
                    break
    return sorted(hits)


def _source_files(src_roots):
    """(path, root_parent) for every non-hidden regular file under the roots —
    language-agnostic (used by --mode files). Same hidden/__pycache__ skip and
    rel-path base as _module_files, but no extension filter: on a non-Python
    repo the map must still see the code."""
    return [
        (path, base)
        for _root, base, path in _walk_roots(src_roots, "*")
        if path.is_file()
    ]


def first_comment_summary(text, prefixes):
    """A file's one-line summary for --mode files: the text of its first comment
    line. Skips a shebang; strips the comment token (and a trailing block close
    like `-->`/`*/`). Returns "" when the file opens with code, not a comment —
    the top-of-file comment is the summary convention, so we don't hunt inline
    comments deeper down."""
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#!"):
            continue
        for pre in prefixes:
            if line.startswith(pre):
                body = line[len(pre) :].rstrip()
                for close in ("-->", "*/"):
                    if body.endswith(close):
                        body = body[: -len(close)]
                return body.strip(" \t*-/")
        return ""  # first non-empty line is not a comment
    return ""


def build_files_map(src_roots, prefixes):
    """Stack-neutral MODULE MAP block: one row per source file (path + first
    comment-line summary), sorted by path. Deterministic, so `--check` trips on
    any file add/remove/rename or summary edit — the same freshness guarantee as
    the symbol map, one granularity coarser."""
    files = _source_files(src_roots)
    note = (
        "_Generated by `scripts/gen_arch_map.py --mode files` from the source "
        "tree (file-level fallback — no language parser). One row per source "
        "file; the summary is its first comment line. Do not edit by hand; run "
        "the check harness to refresh._"
    )
    if not files:
        return note + "\n\n_(no source scanned)_"
    rows = []
    for path, base in files:
        rel = path.relative_to(base).as_posix()
        try:
            summary = first_comment_summary(path.read_text(encoding="utf-8"), prefixes)
        except (UnicodeDecodeError, OSError):
            summary = ""  # binary/unreadable file: list it, no summary
        rows.append((rel, summary))
    lines = [note, "", "| Source file | Summary |", "|---|---|"]
    for rel, summary in sorted(rows):
        lines.append("| `{}` | {} |".format(rel, summary.replace("|", "\\|")))
    return "\n".join(lines)


def scan_inventory(src_roots, strict=True):
    """`[(rel, summary, imports, contracts, rows)]` — the same per-module
    records `build_map` renders, exposed as DATA. This is the seam the WI-455
    retirement re-pointed the map's consumers onto (sitting-2 decision 8:
    registries/source → dashboard, no markdown way-station): the dashboard's
    How-SW view (`traj_parse.sw_modules`), the spine checks'
    `check_trajectory.arch_inventory` and the `check_doc_refs` `sym:` oracle
    all read the source tree through this one walk instead of parsing a
    rendered markdown block back. Symbol-emptiness skip identical to the map's
    (a bare `__init__.py` never enters the inventory).

    SEQUENCING NOTE for the queued programs that also touch this module:
    WI-390 clause (2) re-declares the arch-map/Contracts surface and WI-448
    (the common-module inversion) may re-home the walk — both inherit THIS
    function as the consumers' single entry point, so a re-home moves one
    seam, not four parsers."""
    files, internal_names = _module_files(src_roots)
    out = []
    for path, root_parent in files:
        try:
            rel, summary, imports, contracts, rows = scan_module(
                path, root_parent, internal_names
            )
        except (UnicodeDecodeError, OSError):
            # A non-UTF-8 or unreadable .py cannot be judged. The WRITE path
            # (build_map, strict) keeps crashing loudly on it; the data
            # consumers (strict=False) feed warn-tier rules and the dashboard
            # render, where one binary-ish file must cost that file, not the
            # run — the posture the retired WI-399 mirror argued and kept.
            if strict:
                raise
            continue
        if not (summary or imports or contracts or rows):
            continue  # skip empty modules (e.g. bare __init__.py) — no noise
        out.append((rel, summary, imports, contracts, rows))
    return out


def build_map(src_roots):
    note = (
        "_Generated by `scripts/gen_arch_map.py` from the source tree (AST). "
        "Do not edit by hand; run the check harness to refresh. Summaries and "
        "`Implements:` come from your docstrings/comments._"
    )
    records = scan_inventory(src_roots)
    if not _module_files(src_roots)[0]:
        return note + "\n\n_(no source scanned)_"
    sections = [note]
    for rel, summary, imports, contracts, rows in records:
        sections.append("\n### `{}`".format(rel))
        if summary:
            sections.append("_{}_".format(summary.replace("|", "\\|")))
        if imports:
            # check_trajectory.arch_inventory parses this line (backticked bare
            # stems) as the cross-CMP rule's edge source (WI-064) — keep the
            # grammar in sync with that parser.
            sections.append(
                "Imports (internal): {}".format(
                    ", ".join("`{}`".format(i) for i in imports)
                )
            )
        # Declared interface seams (process.md §8), harvested from the module's
        # `Contracts: IF-###` docstring line — the arch-map is the oracle
        # check_trajectory reads for the docstring-vs-registry coverage warn.
        if contracts:
            sections.append("Contracts (interfaces): {}".format(", ".join(contracts)))
        if rows:
            sections.append("\n| Public item | Summary | Implements |\n|---|---|---|")
            for name, sig, summ, ids in rows:
                sections.append(
                    "| `{}{}` | {} | {} |".format(
                        name,
                        sig,
                        summ.replace("|", "\\|"),
                        ", ".join(ids) if ids else "",
                    )
                )
        else:
            sections.append("_(no public items)_")
    return "\n".join(sections)


def collect_parse_errors(src_roots):
    """(rel, message) for every scanned module that fails to parse. Used by
    --strict-parse to fail the gate, rather than only surfacing the PARSE ERROR
    text in the map (which `--check` would treat as up to date)."""
    errs = []
    files, _ = _module_files(src_roots)
    for path, root_parent in files:
        try:
            ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            rel = (
                path.relative_to(root_parent)
                .with_suffix("")
                .as_posix()
                .replace("/__init__", "")
            )
            errs.append((rel, str(exc)))
    return errs


def _resolve_import(imp, importer_rel, known):
    """Map an import string from internal_imports() to a scanned module's rel
    path; None if it doesn't resolve. Falls back to progressively shorter
    prefixes (`pkg.sub.name` -> `pkg.sub` -> `pkg`) so a symbol that merely
    looks like a module still lands on its containing module. Best-effort,
    same caveat as the map."""
    if imp.startswith("."):
        level = len(imp) - len(imp.lstrip("."))
        # Drop the importer's own name, then one more segment per extra dot.
        base = importer_rel.split("/")[:-level]
        tail = imp.lstrip(".")
        parts = base + (tail.split(".") if tail else [])
    else:
        parts = imp.split(".")
    while parts:
        cand = "/".join(parts)
        for k in known:
            if k == cand or k.endswith("/" + cand):
                return k
        parts = parts[:-1]
    return None


def build_dependency_diagram(src_roots, if_rows=None):
    """Mermaid `graph LR` of the internal-import graph — the imports the module
    map lists, as a picture. Plain text out; rendering is the viewer's job.

    When declared interface seams are supplied (`if_rows`, from
    `interfaces.csv`), module<->module seams are merged in as **distinctly styled**
    dotted, labeled edges (`A -. IF-003 .-> B`) so they read apart from the solid
    import arrows; a seam to a file or external actor is a How-SW dashboard node
    (gen_trajectory), not a code-import edge, so it is skipped here."""
    files, internal_names = _module_files(src_roots)
    note = (
        "_Generated by `scripts/gen_arch_map.py` from the source tree (AST): "
        "each solid arrow is an internal import; a dotted labeled arrow is a "
        "declared IF-### interface seam. Do not edit by hand; run the check "
        "harness to refresh._"
    )
    if not files:
        return note + "\n\n_(no source scanned)_"
    mods = []
    for path, root_parent in files:
        rel, summary, imports, _contracts, _rows = scan_module(
            path, root_parent, internal_names
        )
        mods.append((rel, summary, imports))
    known = [m[0] for m in mods]

    def node_id(rel):
        # Mermaid ids must avoid '/'-style separators and reserved words
        # (a module named `end` would otherwise break the graph) — prefix + sanitize.
        return "m_" + re.sub(r"\W", "_", rel)

    lines = [note, "", "```mermaid", "graph LR"]
    for rel, summary, _imports in mods:
        label = rel
        if summary:
            short = summary if len(summary) <= 48 else summary[:47] + "…"
            label = "{} — {}".format(rel, short)
        lines.append('    {}["{}"]'.format(node_id(rel), label.replace('"', "'")))
    edges = set()
    for rel, _summary, imports in mods:
        for imp in imports:
            target = _resolve_import(imp, rel, known)
            if target and target != rel:
                edges.add((node_id(rel), node_id(target)))
    for src_id, dst_id in sorted(edges):
        lines.append("    {} --> {}".format(src_id, dst_id))
    # Declared interface seams (process.md §8): module<->module IF rows as dotted,
    # labeled edges, distinct from the solid import arrows. Deterministic (sorted).
    known_norm = {_norm_module(k): node_id(k) for k in known}
    if_edges = set()
    for r in if_rows or []:
        iid = (r.get("IF-ID") or "").strip()
        if not IF_ID_RE.fullmatch(iid) or iid.endswith("-000"):
            continue
        a = known_norm.get(_norm_module(r.get("ThisProject", "")))
        b = known_norm.get(_norm_module(r.get("Counterpart", "")))
        if not a or not b or a == b:
            continue  # a seam to a file/external is a dashboard node, not drawn here
        src_n, dst_n = (
            (b, a)
            if (r.get("Direction") or "").strip().lower() == "consumes"
            else (a, b)
        )
        if_edges.add((src_n, dst_n, iid))
    for src_n, dst_n, iid in sorted(if_edges):
        lines.append("    {} -. {} .-> {}".format(src_n, iid, dst_n))
    lines.append("```")
    return "\n".join(lines)


def splice_region(doc_text, begin, end, content, target, required):
    """Replace the text between begin/end markers. If the markers are absent:
    error when required, else leave the text untouched. Returns the new text."""
    if begin not in doc_text or end not in doc_text:
        if required:
            raise SystemExit(
                "{} is missing markers:\n  {}\n  {}".format(target, begin, end)
            )
        return doc_text
    # A duplicated marker would make the splice ambiguous (and silently eat the
    # text between the copies) — refuse rather than corrupt the doc.
    if doc_text.count(begin) > 1 or doc_text.count(end) > 1:
        raise SystemExit(
            "{} contains a duplicated marker ({} / {}); keep exactly "
            "one pair per file".format(target, begin, end)
        )
    pre = doc_text.split(begin)[0]
    post = doc_text.split(end)[1]
    return "{}{}\n{}\n{}{}".format(pre, begin, content, end, post)


def _called_name(call):
    """The called function's bare name for a Call node (Name or method Attribute)."""
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def _all_functions(src_roots):
    """Map every function name in the source -> list of (module_rel, node,
    one-line summary), in scan order. A name can be defined in several modules —
    callers disambiguate (see build_flow)."""
    funcs = {}
    files, _ = _module_files(src_roots)
    for path, root_parent in files:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        rel = (
            path.relative_to(root_parent)
            .with_suffix("")
            .as_posix()
            .replace("/__init__", "")
        )
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                funcs.setdefault(node.name, []).append(
                    (rel, node, first_line(ast.get_docstring(node)))
                )
    return funcs


def build_flow(src_roots, entry):
    """Ordered list of the internal functions the entry orchestrator calls.

    `entry` is a bare function name (`run`) or module-qualified (`module:run`,
    matching the module path's tail, e.g. `export/io:run` or just `io:run`).
    A bare name defined in more than one module is an error — qualify it."""
    funcs = _all_functions(src_roots)
    mod, _, name = entry.rpartition(":")
    candidates = funcs.get(name, [])
    if mod:
        candidates = [c for c in candidates if c[0] == mod or c[0].endswith("/" + mod)]
    if not candidates:
        raise SystemExit("flow entry function not found: {}".format(entry))
    if len(candidates) > 1:
        raise SystemExit(
            "flow entry {!r} is ambiguous — defined in: {}. Qualify it as "
            "'module:{}'.".format(name, ", ".join(c[0] for c in candidates), name)
        )
    _rel, node, summary = candidates[0]
    internal = set(funcs)
    calls = []
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            cn = _called_name(n)
            if cn and cn in internal and cn != name:
                calls.append((n.lineno, n.col_offset, cn))
    calls.sort()
    note = (
        "_Generated by `scripts/gen_arch_map.py --flow {0}` — the ordered "
        "internal calls in `{0}`. Keep entry points thin: a readable flow here "
        "means the orchestrator delegates instead of computing. Loops/branches "
        "are not shown — see the overview above for control flow._".format(name)
    )
    lines = [note, ""]
    if summary:
        lines.append("**`{}`** — {}".format(name, summary))
        lines.append("")
    if not calls:
        lines.append(
            "_(no internal calls found — is `{}` the orchestrator, and "
            "is its module under --src?)_".format(name)
        )
    else:
        for i, (_l, _c, cn) in enumerate(calls, 1):
            s = funcs[cn][0][2]  # first definition's summary (display only)
            lines.append("{}. `{}`{}".format(i, cn, " — " + s if s else ""))
    return "\n".join(lines)


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--src",
        action="append",
        default=None,
        help="source root to scan (repeatable; default: src)",
    )
    ap.add_argument(
        "--doc",
        action="append",
        default=None,
        help="file(s) to update; repeatable, REQUIRED (the scaffolded "
        "docs/architecture.md default retired at WI-455). Point at AGENTS.md "
        "/ CLAUDE.md to route the map where agents read.",
    )
    ap.add_argument(
        "--flow",
        default=None,
        help="entry/orchestrator function whose call sequence fills "
        "the GENERATED FLOW markers (e.g. 'run' or 'mod:run')",
    )
    ap.add_argument(
        "--mode",
        choices=("symbols", "files"),
        default="symbols",
        help="symbols (default: Python-AST symbol map + diagram/flow) or "
        "files (stack-neutral one-row-per-file fallback)",
    )
    ap.add_argument(
        "--comment-prefix",
        action="append",
        default=None,
        help="comment token whose first line is a file's summary in --mode "
        "files (repeatable; default: # // --)",
    )
    ap.add_argument(
        "--interfaces",
        default="docs/requirements/interfaces.toml",
        help="the IF-### interface-seam registry whose module<->module rows are "
        "merged into the dependency diagram as distinctly-styled edges (process.md "
        "§8); absent file = no IF edges (symbol mode only)",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit 1 if any target is stale",
    )
    ap.add_argument(
        "--strict-parse",
        action="store_true",
        help="exit 1 if any scanned module fails to parse",
    )
    args = ap.parse_args()

    src_roots = args.src or ["src"]
    if not args.doc:
        raise SystemExit(
            "gen_arch_map: pass --doc <file carrying the MODULE MAP marker "
            "pair> — the scaffolded docs/architecture.md default retired at "
            "WI-455 (the derived architecture reads scan_inventory directly)"
        )
    docs = [Path(d) for d in args.doc]
    if args.mode == "files" and args.flow:
        raise SystemExit("--flow needs a parser; it is not available in --mode files")

    if args.mode == "files":
        prefixes = tuple(args.comment_prefix or DEFAULT_COMMENT_PREFIXES)
        pattern = "*"
        has_source = bool(_source_files(src_roots))
    else:
        pattern = "*.py"
        has_source = bool(_module_files(src_roots)[0])
    # An empty scan is legitimate pre-code, but on a repo whose code lives in
    # another language the symbol map — and its --check freshness gate — would
    # pass *vacuously* forever while the docs still promise drift-proofing. Say
    # so loudly rather than let the guarantee silently lapse; point at the
    # stack-neutral fallback and the porting contract (see ADOPTING.md).
    if not has_source:
        fallback = (
            ""
            if args.mode == "files"
            else "run this generator with `--mode files` for a stack-neutral "
            "file-level map, "
        )
        print(
            "gen_arch_map: WARNING - no source scanned under {} — the map is "
            "empty and --check passes vacuously. If this repo's code is in "
            "another language, {}port the generator to it (the marker block is "
            "the contract) or remove the arch-map step; see ADOPTING.md.".format(
                ", ".join(str(s) for s in src_roots), fallback
            ),
            file=sys.stderr,
        )
        # Second, sharper warning for the one shape where the emptiness is the
        # generator's own doing rather than the repo's: the root DOES hold
        # matching files, but every one of them sits behind a dot-prefixed
        # directory. Exit stays 0 (an empty map is still legitimate pre-code),
        # but the generic "port the generator" advice above is the wrong remedy
        # here, so say what actually happened and where.
        _warn_hidden_swallow(
            src_roots,
            pattern,
            "source files" if args.mode == "files" else "modules",
        )

    if args.mode == "files":
        generated = build_files_map(src_roots, prefixes)
        diagram = None  # diagram/flow are symbol-mode only (need a parser)
        flow = None
    else:
        generated = build_map(src_roots)
        diagram = build_dependency_diagram(src_roots, load_interfaces(args.interfaces))
        flow = build_flow(src_roots, args.flow) if args.flow else None

    stale = False
    for doc in docs:
        if not doc.exists():
            # Missing-target posture: arch-map's target is
            # a HAND-AUTHORED doc that must already exist (it holds prose around
            # the generated block), so its absence is a hard error — unlike the
            # fully-generated gen_okf / gen_trajectory outputs, whose --check
            # treats a missing file as stale/vacuous and (re)creates it.
            raise SystemExit("target file not found: {}".format(doc))
        current = doc.read_text(encoding="utf-8")
        updated = splice_region(current, BEGIN, END, generated, doc, required=True)
        # DIAGRAM and FLOW markers are optional per doc — presence opts in.
        if diagram is not None:
            updated = splice_region(
                updated, BEGIN_DIAGRAM, END_DIAGRAM, diagram, doc, required=False
            )
        if flow is not None:
            updated = splice_region(
                updated, BEGIN_FLOW, END_FLOW, flow, doc, required=False
            )
        if args.check:
            if updated != current:
                stale = True
                print(
                    "code map STALE in {}: run `python scripts/gen_arch_map.py`".format(
                        doc
                    ),
                    file=sys.stderr,
                )
        elif updated != current:
            # newline="\n" via open() (write_text(newline=) is 3.10+; scripts stay
            # 3.9-runnable, floor 3.11): LF on every OS so the generated block stays
            # byte-stable regardless of a downstream .gitattributes rule.
            with doc.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(updated)
            print("code map regenerated -> {}".format(doc))
        else:
            print("code map already up to date -> {}".format(doc))

    strict_fail = False
    if args.strict_parse:
        for rel, msg in collect_parse_errors(src_roots):
            print(
                "strict-parse: {} failed to parse — {}".format(rel, msg),
                file=sys.stderr,
            )
            strict_fail = True

    if args.check and stale:
        sys.exit(1)
    if strict_fail:
        sys.exit(1)
    if args.check:
        print("code map up to date.")


if __name__ == "__main__":
    main()
