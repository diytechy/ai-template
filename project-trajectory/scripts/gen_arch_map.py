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

Reverse back-link coverage (`--backlink-coverage`): the same `Implements:`
grammar, run the other way round — for each LIVE LLR row, does any literal
declaration in the source surface name it? A REPORT, not a gate: the bar lives
in `docs/process.toml` `[checks] backlink_coverage_min` and ships at `0`, so the
number appears in every run and nothing fails. It measures PRESENCE, never
correctness. See the section above `main()` for the direction argument.

Usage:
    python scripts/gen_arch_map.py --doc FILE [--src SRC ...] [--flow ENTRY]
                                   [--mode symbols|files] [--comment-prefix TOK ...]
                                   [--check] [--strict-parse]
    python scripts/gen_arch_map.py --cli-doc FILE [--src SRC ...] [--check]
    python scripts/gen_arch_map.py --contracts-doc FILE [--src SRC ...] [--check]
    python scripts/gen_arch_map.py --backlink-coverage [--src SRC ...]
                                   [--root DIR] [--backlink-ext .EXT ...]
                                   [--strict-backlinks]

    --src            One or more source roots to scan (default: src). Repeatable.
    --doc            File(s) to update in place (required; repeatable) — each
                     must contain the MODULE MAP marker pair.
    --contracts-doc  File(s) carrying the INTERFACE REFERENCE marker pair,
                     spliced with each module's stated contracts.
    --cli-doc        File(s) carrying the CLI REFERENCE marker pair, spliced
                     with every scanned module's argparse surface (repeatable).
                     Its own mode: it needs no --doc, since the module map it
                     would demand there retired at WI-455.
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
    <!-- BEGIN GENERATED CLI REFERENCE -->  ... <!-- END GENERATED CLI REFERENCE -->  (required per --cli-doc)
    <!-- BEGIN GENERATED INTERFACE REFERENCE --> ... <!-- END GENERATED INTERFACE REFERENCE --> (required per --contracts-doc)

Contracts: IF-010, IF-025 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import ast
import re
import sys
import tomllib
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# The spine ROW cell vocabulary — what a Module / Endpoint cell reduces to.
from kitlib import spine as _kitspine

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


# The policy home (SN-028) this module reads ONE key out of — see
# `read_backlink_min`. Named here rather than inlined so the message a reader
# acts on and the file it points at cannot drift apart.
PROCESS_TOML = "process.toml"
BEGIN = "<!-- BEGIN GENERATED MODULE MAP -->"
END = "<!-- END GENERATED MODULE MAP -->"
BEGIN_FLOW = "<!-- BEGIN GENERATED FLOW -->"
END_FLOW = "<!-- END GENERATED FLOW -->"
BEGIN_DIAGRAM = "<!-- BEGIN GENERATED DEPENDENCY DIAGRAM -->"
END_DIAGRAM = "<!-- END GENERATED DEPENDENCY DIAGRAM -->"
# The CLI reference's own marker pair (OI-61 ruled (a)'s second step). It gets a
# DEDICATED target flag (`--cli-doc`) rather than riding `--doc`, and the reason
# is a standing ruling: the committed MODULE MAP retired at WI-455 — structure
# derives live into the dashboard — so a repo that wants the CLI surface written
# down must be able to have it WITHOUT re-committing the map that was
# deliberately retired.
BEGIN_CLI = "<!-- BEGIN GENERATED CLI REFERENCE -->"
END_CLI = "<!-- END GENERATED CLI REFERENCE -->"
BEGIN_CONTRACTS = "<!-- BEGIN GENERATED INTERFACE REFERENCE -->"
END_CONTRACTS = "<!-- END GENERATED INTERFACE REFERENCE -->"
# THE TWO PARSING GRAMMARS IN THIS MODULE ARE SEPARATE, and deliberately so.
# `Implements:` (below) is a SYMBOL-level back-link declaration over the four
# spine tiers; `Contracts:` (further down) is a MODULE-level interface-seam
# declaration over IF ids, with its own hard refusal of the ambiguous wrapped
# form (WI-478). They share nothing but a family resemblance — merging them
# would put one refusal policy on two conventions whose failure costs differ by
# an order of magnitude (see `backlink_ids`).
IMPLEMENTS_RE = re.compile(r"\b(?:SR|LLR|SN|TC)-\d+\b")
# The literal token a back-link DECLARATION must carry (WI-486 / OI-42 ruled
# (b)). `backlink_ids` is the kit's ONE definition of a back-link and both arms
# read it: the map's `Implements` column and the reverse-coverage scan.
IMPLEMENTS_MARKER = "Implements:"
# A declaration OPENS its line: nothing may precede the token but whitespace,
# comment markers (`#`, `//`, `--`, `*`, `;`, `%`, `<!--`) or quote characters.
# The 2026-08-21 review measured why — two docstring lines in
# `check_trajectory.py` explaining that `LLR-042` is DELIBERATELY UNCLAIMED
# were parsed as declarations OF `LLR-042`, so the map's third column reported
# the disclaimer as the tag, sourced entirely from the sentence denying it.
# Audited over the whole scanned surface, this rule classifies all 83 genuine
# declarations as declarations and both prose lines as prose (83/165 before and
# after).
# THE BACKTICK IS NOT IN THAT SET, and the omission is measured too: both prose
# lines write the token in backticks — a QUOTED token is a mention, and a
# mention is not a declaration. It is also the one character that would let the
# rule back in through the door it just closed.
# THIS NARROWS THE GRAMMAR for a declaration written after a summary sentence
# on the same line (`"""Do the thing. Implements: LLR-001"""`), which no longer
# declares; put the token at the start of its own line. RESYNC entry owed and
# written — an adopter's coverage percentage can move on this.
_DECL_OPENING = re.compile(r"^[\s#/\-*;%<!\"']*$")
# Interface-seam ids a module declares via a `Contracts: IF-###, ...` line
# (process.md §8) — harvested like Implements, but module-level (WI-056).
CONTRACTS_RE = re.compile(r"\bIF-\d+\b")
IF_ID_RE = re.compile(r"IF-\d+")
# Source-file extensions stripped when normalizing a module path, so a diagram
# node (`scripts/check`) and an IF endpoint written with the full repo path
# (`project-trajectory/scripts/check.py`) collapse to one key. ONE HOME since
# WI-448 slice 4 (`kitlib.spine`): this and `check_trajectory.py`'s copy were
# the real pair, and the retired comment here claimed sync with `trace.py` too,
# which has never carried the name.
_MODULE_EXTS = _kitspine.MODULE_EXTS
# The file types `--backlink-coverage` reads (OI-42's declared extension list):
# `_MODULE_EXTS` — the kit's existing answer to "what is a source module" —
# extended with the families that list half-covers. Overridable per repo with
# `--backlink-ext`, which REPLACES this list rather than adding to it.
#
# WIDEN THIS WITH CARE, and the asymmetry is the reason: the denominator is the
# LLR row count, never the file count, so adding an extension can only RAISE the
# measured percentage and never lower it. Over-inclusion therefore produces
# false PASSES — a stray `LLR-040` in a config comment scores as a carrier — so
# the conservative list is the tight one.
BACKLINK_EXTS = _MODULE_EXTS + (
    ".tsx",
    ".jsx",
    ".mjs",
    ".cjs",
    ".java",
    ".kt",
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".cs",
    ".rb",
    ".php",
    ".swift",
    ".scala",
    ".lua",
    ".sql",
)
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


def backlink_ids(line):
    """The spine ids ONE line of text DECLARES as back-links — the kit's single
    definition of a back-link (WI-486 / OI-42 ruled (b)+(e)).

    A declaration is the literal `Implements:` token followed, ON THE SAME LINE,
    by `SN|SR|LLR|TC-###` ids. Anything else is prose: an id before the token,
    an id on a neighbouring line, an id in a sentence that never says
    `Implements:`. Both consumers read exactly this — `implements()` fills the
    map's third column with it, `scan_backlinks()` measures reverse coverage
    with it — so the map cannot report a link the coverage scan would not count,
    and vice versa.

    WHY IT IS A MARKER-LINE RULE. Until WI-486 this harvested ANY spine id from
    a symbol's docstring or the four comment lines above its `def`, which meant
    the column reported a regex's reading of nearby English: measured over the
    kit's own 788 public symbols, 50 carried a non-empty column holding 62
    back-links, of which 60 had never been declared by anyone and 13 named no
    live registry row. `trace.id_sort_key`'s docstring explains that "SR-9
    orders before SR-10" — a SORTING example — and the map recorded that
    function as implementing SR-9 and SR-10. A traceability artifact that
    invents links is worse than one that has none, because a reader can only
    discount what they know is empty.

    NO REFUSAL HERE, unlike `Contracts:` (WI-478), and the asymmetry is
    deliberate rather than an oversight. That grammar hard-fails on an id
    stranded on a continuation line because an IF declaration is module-level,
    rare, and feeds a coverage check that would otherwise report a
    visibly-declared seam as undeclared. A back-link is per-symbol and
    optional-by-dial (see `read_backlink_min`); raising a `SystemExit` because
    a declaration line happened to wrap mid-list would break every adopter's map
    generation over a docstring reflow. An id that wraps onto its own line is
    simply not declared — which the reverse-coverage number reports honestly.
    (No example of the token is spelled out in this docstring on purpose: this
    function's own prose is inside the surface it scans, and an illustration
    would be harvested as a real declaration — the very defect it describes.)"""
    before, marker, after = line.partition(IMPLEMENTS_MARKER)
    if not marker or not _DECL_OPENING.match(before):
        return []
    return IMPLEMENTS_RE.findall(after)


def implements(node, source_lines):
    """The requirement ids DECLARED near a symbol — in its own docstring, or in
    the four lines just above its `def`/`class`.

    Literal declarations only since WI-486: every line goes through
    `backlink_ids`, so a line that does not carry the `Implements:` token
    contributes nothing however many spine ids it mentions. Expect this column
    to be EMPTY for most symbols in most repos; that is the honest state of a
    convention almost nobody follows, and `--backlink-coverage` is what measures
    it rather than papering over it."""
    ids = set()
    for line in (ast.get_docstring(node) or "").splitlines():
        ids.update(backlink_ids(line))
    start = node.lineno - 1  # 0-based line of the def
    for i in range(max(0, start - 4), start):
        ids.update(backlink_ids(source_lines[i]))
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


# The marker line's WHOLE grammar, anchored: `Contracts:` then a comma-separated
# id list, then optional trailing prose introduced by an em dash, a hyphen or a
# parenthesis. Anchored rather than "starts right, then harvest every IF token
# on the line", because that weaker rule still read `Contracts: not IF-080; an
# example, not a declaration` as declaring IF-080 — the same defect one step
# down. An id list is either well formed or it is not a declaration.
# Comma OR semicolon: the kit's own tree uses both (plan_artifacts.py is
# semicolon-separated), and this grammar tightens against PROSE, never
# against a separator style someone already writes. A trailing full stop is
# allowed for the same reason and is safe where a trailing `and`/comma is not:
# nothing can follow it, so no id can be dropped by accepting it.
_MARKER_RE = re.compile(
    r"^Contracts:\s*(?P<ids>IF-\d+(?:\s*[,;]\s*IF-\d+)*)\.?\s*(?P<rest>[\u2014(:-].*)?$"
)
# What LOOKS like a marker: used only to tell a malformed declaration apart from
# ordinary prose, so the first can be reported instead of silently dropped.
_MARKER_LOOKALIKE_RE = re.compile(r"^Contracts\s*:")


def _marker_text(line):
    """`line` with a leading `#` and surrounding space stripped, so the
    docstring and top-of-file-comment forms read through one grammar."""
    return line.strip().lstrip("#").strip()


def _marker_ids(line):
    """The ids this line DECLARES, or None when it is not a marker line at all.

    An empty list means the line is marker-shaped but declares nothing — a
    finding, never a silent drop.
    """
    text = _marker_text(line)
    m = _MARKER_RE.match(text)
    if m:
        # NO **UNDECLARED** ID MAY SURVIVE IN THE TAIL. `Contracts: IF-001 - IF-002`
        # matches with `- IF-002` as trailing prose, which would declare one seam
        # and drop the other in silence — a PARTIAL parse, worse than refusing,
        # because the author sees a declaration that is quietly short. But the
        # tail RE-MENTIONING an id it already declared is ordinary explanatory
        # prose (check_trajectory.py and gen_trajectory.py both do it), so the
        # test is set difference, not presence: an id in the tail that the list
        # does not carry is what makes the line malformed.
        declared = [i.strip() for i in re.split(r"[,;]", m.group("ids"))]
        if set(CONTRACTS_RE.findall(m.group("rest") or "")) - set(declared):
            return []
        return declared
    if _MARKER_LOOKALIKE_RE.match(text):
        return []
    return None


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
        found = _marker_ids(line)
        if found:
            ids.update(found)
            _refuse_ambiguous_continuation(doc_lines[i + 1 :], ids)
    for i, line in enumerate(source_lines[:8]):
        if not line.lstrip().startswith("#"):
            continue
        found = _marker_ids(line)
        if found:
            ids.update(found)
            _refuse_ambiguous_continuation(source_lines[i + 1 : 8], ids)
    return sorted(ids)


def contracts_grammar_findings(module, tree, source_lines):
    """Named findings for a line that LOOKS like a declaration and is not one.

    The point is that a tightened grammar must never drop a declaration in
    silence: a marker-shaped line whose id list will not parse, and a mid-line
    `Contracts:` carrying ids (the form that declared something before the
    grammar was anchored), are both REPORTED here so an upgrading repo is told
    rather than quietly losing its seams."""
    doc = ast.get_docstring(tree) or ""
    return _grammar_findings_over(
        module, list(doc.splitlines()) + list(source_lines[:8])
    )


def _grammar_findings_over(module, lines):
    out, seen = [], set()
    for line in dict.fromkeys(lines):
        text = _marker_text(line)
        if _marker_ids(line) == []:
            out.append(
                "{}: `{}` is marker-shaped but declares no parsable id list — "
                "the grammar is `Contracts: IF-###[, IF-###]...` (comma or "
                "semicolon) and this line declares nothing. An id after the "
                "list, as in `IF-001 - IF-002`, is refused rather than parsed "
                "part-way: a declaration that is quietly short is worse than "
                "one that is refused".format(module, text[:90])
            )
        elif (
            _marker_ids(line) is None
            and "Contracts:" in text
            and CONTRACTS_RE.search(text)
        ):
            out.append(
                "{}: `{}` carries `Contracts:` and an IF id MID-LINE — the "
                "marker must open its own line, so this declares nothing; move "
                "it to the start of a line".format(module, text[:90])
            )
    for line in out:
        seen.add(line)
    return sorted(seen)


_BODY_OPEN_RE = re.compile(r"^Contract\s+(IF-\d+):\s*(.*)$")


def module_contract_bodies(tree, source_lines):
    """`{IF-###: body}` — the contract text a module states for each seam it
    declares, harvested from its own docstring.

    THE GRAMMAR. A body opens on a line whose first token is `Contract IF-###:`
    and runs to the next such line, a blank line, or the end of the docstring;
    wrapped lines join into one paragraph. The opener is `Contract IF-###:`
    rather than a bare `IF-###:` deliberately — a bare id-colon is ordinary
    docstring prose (`IF-001: legacy identifier retained`, a mapping table, an
    example), and a grammar that cannot be written by accident is the only kind
    safe to hard-fail on.

    FOUR REFUSALS, each a `ContractsGrammarError`: a body before the marker
    line, because the marker is what declares; a body for an undeclared id,
    because the marker line stays the ONE declaration site; a second body for
    one id, because silently keeping the last is how two contracts become one;
    and a body carrying an HTML comment, because the text is spliced into a
    generated Markdown document and could otherwise close its own end marker.

    Why the module and not the registry cell: the declaration then sits beside
    the code that must honour it, so a rename or a retirement moves the two
    together. The registry row states what CROSSES and points here; this states
    what the providing side promises.
    """
    declared = set(module_contracts(tree, source_lines))
    doc = ast.get_docstring(tree) or ""
    return _contract_bodies(doc.splitlines(), declared)


def _contract_bodies(lines, declared):
    """The body grammar over a list of LINES — a module docstring's, or a
    non-Python file's comment header with its markers stripped
    (`header_lines`). One grammar, two carriers: a registry, a config file or
    a git hook states its contracts exactly as a module does."""
    # WHERE EACH ID WAS DECLARED, not merely where the first marker sits: a
    # module may carry more than one marker line, and a body must follow the one
    # that declares ITS id — otherwise a body can precede its own declaration
    # and swallow the marker that follows it.
    declared_at = {}
    for i, line in enumerate(lines):
        for iid in _marker_ids(line) or ():
            declared_at.setdefault(iid, i)
    bodies, current, buf = {}, None, []

    def flush():
        if not current:
            return
        text = " ".join(part.strip() for part in buf if part.strip())
        if not text:
            raise ContractsGrammarError(
                "{} opens a contract body and states nothing — write the "
                "contract or drop the opener.".format(current)
            )
        if "<!--" in text or "-->" in text:
            raise ContractsGrammarError(
                "{}'s contract body carries an HTML comment; the text is "
                "spliced into a generated Markdown document and must not be "
                "able to close its own markers.".format(current)
            )
        bodies[current] = text

    for i, line in enumerate(lines):
        m = _BODY_OPEN_RE.match(line.strip())
        if m:
            flush()
            current, buf = m.group(1), [m.group(2)]
            if current not in declared_at or i < declared_at[current]:
                raise ContractsGrammarError(
                    "{} states a contract body before this module's "
                    "`Contracts:` marker line — the marker declares, the body "
                    "elaborates, and the order says which is which.".format(current)
                )
            if current not in declared:
                raise ContractsGrammarError(
                    "{} carries a contract body but is not declared on this "
                    "module's `Contracts:` line — the marker line is the one "
                    "declaration site; add the id there or drop the "
                    "body.".format(current)
                )
            if current in bodies:
                raise ContractsGrammarError(
                    "{} carries more than one contract body — one seam states "
                    "one contract.".format(current)
                )
            continue
        if current is None:
            continue
        # A marker line ends a body as firmly as a blank line does; otherwise a
        # declaration written below a body is swallowed into that body's prose.
        if not line.strip() or _marker_ids(line) is not None:
            flush()
            current, buf = None, []
            continue
        buf.append(line)
    flush()
    return bodies


# Files whose leading comment block is `#`-prefixed lines. Anything else that
# is not Markdown is read the same way, so a shell hook, an INI file and an
# extensionless config all declare through one grammar.
_MARKDOWN_SUFFIXES = (".md", ".markdown", ".html")


def header_lines(path):
    """The leading comment block of a NON-Python file, its comment markers
    stripped, as the lines the marker and body grammar read.

    Two carriers: `#`-prefixed lines at the top of a TOML/INI/CSV/shell/
    extensionless file (a `#!` shebang on line 1 is skipped; the block ends at
    the first line that is not a `#` comment), or the FIRST `<!-- ... -->`
    block at the top of a Markdown file. `[]` when the file opens with anything
    else — a header is the first thing in the file or it is not a header."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    if path.suffix.lower() in _MARKDOWN_SUFFIXES:
        i = 0
        while i < len(lines) and not lines[i].strip():
            i += 1
        if i >= len(lines) or not lines[i].lstrip().startswith("<!--"):
            return []
        out, first = [], lines[i].lstrip()[4:]
        rest = [first] + lines[i + 1 :]
        for line in rest:
            if "-->" in line:
                out.append(line[: line.index("-->")].strip())
                break
            out.append(line.strip())
        return out
    out = []
    for j, line in enumerate(lines):
        s = line.strip()
        if j == 0 and s.startswith("#!"):
            continue
        if not s.startswith("#"):
            break
        out.append(s.lstrip("#").strip())
    return out


def file_contracts(path):
    """`(ids, bodies)` a non-Python file declares through its header — the same
    `Contracts:` marker and `Contract IF-###:` bodies a module docstring
    carries, so a registry, a config file or a git hook is an owner that
    declares exactly as a module does (OI-67). `([], {})` for a file with no
    header or no marker. Grammar errors raise as they do for a module."""
    lines = header_lines(path)
    ids = set()
    for i, line in enumerate(lines):
        found = _marker_ids(line)
        if found:
            ids.update(found)
            _refuse_ambiguous_continuation(lines[i + 1 :], ids)
    return sorted(ids), (_contract_bodies(lines, ids) if ids else {})


def _resolve_owner_path(root, owner):
    """The tree path an IF owner names, or None: tried verbatim under `root`
    and under the kit's own home, the two spellings the registry uses."""
    for base in (owner, "project-trajectory/" + owner):
        candidate = root / base
        if candidate.exists():
            return candidate
    return None


def owner_files(root, if_rows):
    """`[(owner_as_written, path)]` for every IF row whose owner is a FILE in
    the tree rather than a Python module or an `external:` party — the files
    the contract scan reads beside the module walk. A directory owner declares
    through its `README.md` when it has one and is skipped otherwise; a `.py`
    owner is the module walk's, not this list's. Sorted, deduplicated."""
    seen, out = set(), []
    for r in if_rows or []:
        owner = _kitspine.seam_owner(r)
        if not owner or owner.startswith("external:") or owner in seen:
            continue
        path = _resolve_owner_path(Path(root), owner)
        if path is None or path.suffix == ".py":
            continue
        if path.is_dir():
            path = path / "README.md"
            if not path.is_file():
                continue
        seen.add(owner)
        out.append((owner, path))
    return sorted(out)


def file_grammar_findings(owner, path):
    """`contracts_grammar_findings` over a file header: the lossy marker forms
    are reported by name for a registry or a hook exactly as for a module."""
    return _grammar_findings_over(owner, header_lines(path))


# A module path reduced to a naming-convention-neutral key (strip a leading
# `project-trajectory/`, any source extension, `/__init__`) so an IF endpoint
# and a diagram node match regardless of which form the author used. ONE HOME
# since WI-448 slice 4 (`kitlib.spine.norm_module`), kept under this module's
# own private name so no call site below moves.
_norm_module = _kitspine.norm_module


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
            sections.append("_{}_".format(_md_safe(summary)))
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


# --- the generated CLI reference (OI-61 ruled (a), second step) ---------------
# The registry's 27 CLI `Contract` cells used to PARAPHRASE these argparse
# surfaces by hand, at a mean of 274 characters each, with nothing checking that
# the paraphrase still matched. This is the same walk one step further, and it
# is the kit's own rule applied to its own registry: generated, not
# hand-maintained. What it harvests is deliberately narrow — the flags, their
# help text and the module's declared seams — because that is what an argparse
# tree can be read for WITHOUT importing the module, and importing shipped
# scripts to document them would run their side effects.


def _add_argument_calls(tree):
    """Every `....add_argument(...)` call node in `tree`, in source order.

    Matched on the ATTRIBUTE NAME only, not on a resolved parser object: a
    module builds its parser as `ap`, `parser`, a subparser or a group, and
    chasing which is which needs type inference that a stdlib AST walk does not
    have. The false-positive cost of the loose match is a non-argparse method
    that happens to be called `add_argument`, which nothing in this kit has."""
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "add_argument"
    ]


def _option_record(call):
    """`(names, help)` for one `add_argument` call, or None when its names are
    not literals.

    Only CONSTANT arguments are read. A flag computed at runtime, or help text
    built by an f-string or a concatenation with a variable, yields `""` for the
    help rather than a guess — an empty cell is honest, and a half-rendered
    f-string in a generated reference would be worse than nothing."""
    names = [
        a.value
        for a in call.args
        if isinstance(a, ast.Constant) and isinstance(a.value, str)
    ]
    if not names:
        return None
    text = ""
    for kw in call.keywords:
        if kw.arg == "help" and isinstance(kw.value, ast.Constant):
            if isinstance(kw.value.value, str):
                text = " ".join(kw.value.value.split())
    return names, text


def scan_cli(src_roots):
    """`[(rel, summary, contracts, options)]` for every scanned module that
    BUILDS AN ARGUMENT PARSER — the CLI half of the same AST harvest
    `scan_inventory` does for symbols.

    A module with no `ArgumentParser(` construction is not a CLI and is left
    out entirely: the reference is a list of the surfaces an adopter can
    actually run, not a list of files. Sorted by module path (`_walk_roots`
    sorts), so the rendered block is byte-stable across regeneration."""
    out = []
    for _root, base, path in _walk_roots(src_roots, "*.py"):
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (UnicodeDecodeError, OSError, SyntaxError):
            continue
        if "ArgumentParser(" not in text:
            continue
        options = []
        for call in _add_argument_calls(tree):
            record = _option_record(call)
            if record:
                options.append(record)
        if not options:
            continue
        rel = path.relative_to(base).with_suffix("").as_posix()
        out.append(
            (
                rel,
                first_line(ast.get_docstring(tree)),
                module_contracts(tree, text.splitlines()),
                options,
            )
        )
    return out


def build_cli_reference(src_roots):
    """The rendered CLI-reference block: one section per CLI module, its
    summary, the interface seams it declares, and a flag/help table.

    The `Contracts:` line is what makes this a REFERENCE for the registry
    rather than a second document beside it — an `IF-###` cell that now says
    only "SR-006's obligation delivered as a CLI at check.py" is one hop from
    the flags, and the hop is a generated one."""
    note = (
        "_Generated by `scripts/gen_arch_map.py --cli-doc` from each module's "
        "argparse tree (AST, no import). Do not edit by hand; run the check "
        "harness to refresh. Help text comes from your `help=` strings._"
    )
    records = scan_cli(src_roots)
    if not records:
        return note + "\n\n_(no command-line surface scanned)_"
    sections = [note]
    for rel, summary, contracts, options in records:
        sections.append("\n### `{}`".format(rel))
        if summary:
            sections.append("_{}_".format(_md_safe(summary)))
        if contracts:
            sections.append("Contracts (interfaces): {}".format(", ".join(contracts)))
        sections.append("\n| Option | Help |\n|---|---|")
        for names, text in options:
            sections.append(
                "| {} | {} |".format(
                    ", ".join("`{}`".format(n) for n in names),
                    text.replace("|", "\\|"),
                )
            )
    return "\n".join(sections)


def _md_safe(text):
    """Text safe to splice into the generated Markdown.

    A body that carries an HTML comment is REFUSED at parse time, but a module
    SUMMARY is not the author's contract and refusing a whole module over its
    first docstring line would be disproportionate — so the comment delimiters
    are defanged here instead. Either way nothing a source file says can close
    this document's own end marker."""
    return text.replace("|", "\\|").replace("<!--", "&lt;!--").replace("-->", "--&gt;")


def scan_contracts(src_roots, owner_files=()):
    """`([(source, summary, ids, bodies)], [unreadable])` — every module AND
    every file owner declaring a seam, sorted by path so the rendered block is
    byte-stable, plus the sources the scan could NOT read.

    `owner_files` is `owner_files()`'s list — the registries, config files and
    hooks the IF registry names as owners — read through `file_contracts` so a
    non-Python owner is listed beside the modules, under the path the registry
    spells. The second half of the tuple is the point: a reference that
    silently omitted a source it failed to parse would report a clean, fresh
    document over a tree it had not actually read. The caller renders the list."""
    out, unreadable = [], []
    for owner, path in owner_files:
        try:
            ids, bodies = file_contracts(path)
        except (UnicodeDecodeError, OSError) as exc:
            unreadable.append((owner, type(exc).__name__))
            continue
        if ids:
            head = next(
                (ln for ln in header_lines(path) if ln and _marker_ids(ln) is None), ""
            )
            out.append((owner, head, ids, bodies))
    for _root, base, path in _walk_roots(src_roots, "*.py"):
        rel = path.relative_to(base).with_suffix("").as_posix()
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (UnicodeDecodeError, OSError, SyntaxError) as exc:
            unreadable.append((rel, type(exc).__name__))
            continue
        lines = text.splitlines()
        ids = module_contracts(tree, lines)
        if not ids:
            continue
        out.append(
            (
                rel,
                first_line(ast.get_docstring(tree)),
                ids,
                module_contract_bodies(tree, lines),
            )
        )
    return sorted(out), unreadable


def build_contract_reference(src_roots, owner_files=()):
    """The rendered interface-reference block: the contracts modules STATE, then
    a compact list of the seams they declare and do not state.

    Stated contracts lead because they are what the document is for. The
    unstated ones are one line per module rather than a placeholder paragraph
    each — a real debt list stays readable, and 130-odd repeated "not stated
    here" paragraphs would bury the contracts a reader came for. Neither is
    dropped: a declared seam with no contract is debt, and debt that cannot be
    seen is what this whole build exists to stop."""
    note = (
        "_Generated by `scripts/gen_arch_map.py --contracts-doc` from each "
        "owner's `Contracts:` declaration and `Contract IF-###:` bodies — a "
        "module docstring (AST, no import) or a registry, config or hook "
        "file's comment header. Do not edit by hand; run the check harness to "
        "refresh._"
    )
    records, unreadable = scan_contracts(src_roots, owner_files)
    if not records and not unreadable:
        return note + "\n\n_(no declared interface seams scanned)_"

    stated = sum(len(b) for _r, _s, _i, b in records)
    declared = sum(len(i) for _r, _s, i, _b in records)
    sections = [
        note,
        "",
        "_{} source(s) declare {} seam(s); {} carry a stated contract._".format(
            len(records), declared, stated
        ),
    ]

    if unreadable:
        # Loud, and in the document itself: the alternative is a green check
        # over a tree the generator could not read.
        sections.append("\n## Modules the scan could not read")
        sections.append(
            "_These are NOT covered below. A contract they declare is invisible "
            "to this reference._\n"
        )
        for rel, why in unreadable:
            sections.append("- `{}` — {}".format(rel, why))

    sections.append("\n## Stated contracts")
    if not stated:
        sections.append("\n_No module states a contract yet._")
    for rel, summary, ids, bodies in records:
        if not bodies:
            continue
        sections.append("\n### `{}`".format(rel))
        if summary:
            sections.append("_{}_".format(_md_safe(summary)))
        for iid in ids:
            if iid in bodies:
                sections.append("\n**{}** — {}".format(iid, bodies[iid]))

    gaps = [
        (rel, [i for i in ids if i not in bodies]) for rel, _s, ids, bodies in records
    ]
    gaps = [(rel, missing) for rel, missing in gaps if missing]
    if gaps:
        sections.append("\n## Declared, not stated")
        sections.append(
            "_The seam is declared here and its contract is not. One line per "
            "module; this is the debt list, not an error._\n"
        )
        for rel, missing in gaps:
            sections.append("- `{}` — {}".format(rel, ", ".join(missing)))
    return "\n".join(sections)


def _contracts_doc_exit(src_roots, args):
    """Splice (or `--check`) the interface reference into each
    `--contracts-doc` target; the process exit code.

    Vacuous on an absent target, on `--cli-doc`'s reasoning: a repo that has
    not adopted the reference has no file to be stale and the harness step must
    cost it nothing. What that trades away is the same and is stated the same
    way — deleting the doc disarms this gate silently, and what catches THAT is
    the `[generated]` declaration plus the links into it, not this run."""
    # The file owners come from the registry the same flag names for the
    # diagram; its home is `docs/requirements/`, two levels under the root.
    registry = Path(args.interfaces)
    root = registry.resolve().parent.parent.parent
    generated = build_contract_reference(
        src_roots, owner_files(root, load_interfaces(registry))
    )
    stale = False
    for doc in [Path(d) for d in args.contracts_doc]:
        if not doc.exists():
            print("no interface reference at {} — nothing to check.".format(doc))
            continue
        current = doc.read_text(encoding="utf-8")
        updated = splice_region(
            current, BEGIN_CONTRACTS, END_CONTRACTS, generated, doc, True
        )
        if args.check:
            if updated != current:
                stale = True
                print(
                    "Interface reference STALE in {}: run `python "
                    "scripts/gen_arch_map.py --contracts-doc {}`".format(doc, doc),
                    file=sys.stderr,
                )
        elif updated != current:
            with doc.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(updated)
            print("wrote interface reference -> {}".format(doc))
        else:
            print("interface reference up to date.")
    return 1 if stale else 0


def _cli_doc_exit(src_roots, args):
    """Splice (or `--check`) the CLI reference into each `--cli-doc` target;
    the process exit code.

    Its own mode, returning before main()'s `--doc`/MODULE MAP contract, on
    `--backlink-coverage`'s reasoning: this target carries the CLI block and
    NOT the retired module map, so demanding a MODULE MAP marker pair would
    refuse the one document this step exists to write."""
    generated = build_cli_reference(src_roots)
    stale = False
    for doc in [Path(d) for d in args.cli_doc]:
        if not doc.exists():
            # VACUOUS, unlike --doc's hard refusal, and the asymmetry is the
            # opt-in posture: a repo that has not adopted the CLI reference has
            # no file to be stale, and the harness step must cost it nothing.
            # What that trades away is stated rather than hidden — deleting the
            # doc disarms this gate silently, and what catches THAT is the
            # `[generated]` declaration plus the links into it, not this run.
            print("no CLI reference at {} — nothing to check.".format(doc))
            continue
        current = doc.read_text(encoding="utf-8")
        updated = splice_region(current, BEGIN_CLI, END_CLI, generated, doc, True)
        if args.check:
            if updated != current:
                stale = True
                print(
                    "CLI reference STALE in {}: run `python "
                    "scripts/gen_arch_map.py --cli-doc {}`".format(doc, doc),
                    file=sys.stderr,
                )
        elif updated != current:
            with doc.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(updated)
            print("CLI reference regenerated -> {}".format(doc))
        else:
            print("CLI reference already up to date -> {}".format(doc))
    if stale:
        return 1
    if args.check:
        print("CLI reference up to date.")
    return 0


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


def _seam_edges(if_rows, known_norm):
    """The module<->module IF seams as `(src_node, dst_node, IF-###)` triples,
    in the direction the information runs: owner -> consumer on a `consumers`
    row, requestor -> owner on a `requestors` row. A row whose owner sits
    outside the map draws nothing: a seam owned by a file or an external actor
    is a How-SW dashboard node, not a code-import edge."""
    edges = set()
    for r in if_rows or []:
        iid = (r.get("IF-ID") or "").strip()
        if not IF_ID_RE.fullmatch(iid) or iid.endswith("-000"):
            continue
        own_n = known_norm.get(_norm_module(_kitspine.seam_owner(r)))
        if not own_n:
            continue
        inbound, far = _kitspine.seam_far_side(r)
        for endpoint in far:
            far_n = known_norm.get(_norm_module(endpoint))
            if far_n and far_n != own_n:
                edges.add((far_n, own_n, iid) if inbound else (own_n, far_n, iid))
    return edges


def build_dependency_diagram(src_roots, if_rows=None):
    """Mermaid `graph LR` of the internal-import graph — the imports the module
    map lists, as a picture. Plain text out; rendering is the viewer's job.

    When declared interface seams are supplied (`if_rows`, from
    `interfaces.csv`), module<->module seams are merged in as **distinctly styled**
    dotted, labeled edges (`A -. IF-003 .-> B`) so they read apart from the solid
    import arrows; a seam to a file or external actor is a How-SW dashboard node
    (gen_trajectory), not a code-import edge, so it is skipped here. The edge
    runs owner -> consumer, both read off the row (OI-67)."""
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
    if_edges = _seam_edges(if_rows, known_norm)
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


# --- REVERSE BACK-LINK COVERAGE (WI-486; OI-42 ruled (b)+(e), 2026-08-20) -----
# THE QUESTION, AND WHY IT RUNS THIS WAY ROUND. For each LIVE LLR row, does any
# literal `Implements:` declaration in the declared source surface name it? That
# is LLR-to-code, not comment-to-registry, and the direction is the whole design:
# running from the registry outward, the scan never forms an opinion about an id
# it finds in a comment, so a RETIRED id narrating accurate history (which ruling
# D-4 makes a true sentence, never a defect) is simply not a subject here. The
# rival shape — scan comments, check each id resolves — needs a declared
# history-marker convention before it can be anything but noise, and inventing
# one is a design decision, not a regex. This shape needs none.
#
# WHAT IT MEASURES AND WHAT IT DOES NOT. PRESENCE, never CORRECTNESS: a
# back-link naming the wrong symbol counts clean. It is a coverage number for a
# convention, not a verifier of the links it counts. Say that out loud rather
# than letting a percentage imply more than it holds.
#
# SURFACE = `docs/stack.ini` `[paths] src`, and deliberately NOT `[paths] tests`
# — an LLR that is verified but never built must not score as implemented, and
# the LLR-to-TC link already lives in the registry (`TestRefs`/`Verifies`).
LLR_REGISTRY = "docs/requirements/low-level-requirements.toml"
BACKLINK_MIN_KEY = "backlink_coverage_min"


def scan_backlinks(src_roots, exts=BACKLINK_EXTS):
    """`{spine id: [source path, ...]}` for every literal `Implements:`
    declaration under `src_roots` — the reverse index the coverage number is
    computed from.

    TEXT, not AST, and language-agnostic by construction: it reads comment
    content rather than syntax, so it costs an adopter no parser and no
    toolchain in any language. Unreadable/binary files are skipped rather than
    crashing the scan (a report must not die on one stray file)."""
    exts = tuple(e.lower() for e in exts)
    found = {}
    for _root, base, path in _walk_roots(src_roots, "*"):
        if not path.is_file() or path.suffix.lower() not in exts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(base).as_posix()
        for line in text.splitlines():
            for rid in backlink_ids(line):
                found.setdefault(rid, set()).add(rel)
    return {rid: sorted(paths) for rid, paths in sorted(found.items())}


def backlink_coverage(src_roots, row_ids, exts=BACKLINK_EXTS):
    """`(covered, uncovered, percent)` for `row_ids` against the declarations
    found under `src_roots`. `percent` is 0.0 for an EMPTY row set, which the
    caller must read as vacuous rather than as a failure — a repo with no LLR
    rows has nothing to cover."""
    declared = scan_backlinks(src_roots, exts)
    covered = sorted(rid for rid in row_ids if rid in declared)
    uncovered = sorted(rid for rid in row_ids if rid not in declared)
    total = len(covered) + len(uncovered)
    return covered, uncovered, (100.0 * len(covered) / total if total else 0.0)


# --- ENCLOSING-SYMBOL RESOLUTION (WI-502; OI-53 ruled (d)) -------------------
# The declaration grammar above (`backlink_ids`) answers "does this LINE
# declare an id"; this answers "which def/class TEXTUALLY CONTAINS that line" —
# the question check_trajectory's CodeSymbol crosscheck needs to compare a
# tag's real site against the registry row's `CodeSymbol`/`Module` claim. AST,
# Python-only (unlike the language-agnostic `scan_backlinks` above): resolving
# an enclosing symbol needs a parser, so this half of the shared grammar stops
# at `.py`. ONE HOME (WI-486): check_trajectory imports `implements_report`
# rather than re-walking the tree — a second AST symbol walk in a second module
# is exactly the D-6/F5 hazard `module_bindings` above already argues against.
def _scope_index(tree):
    """`[(start_line, end_line, dotted_qualname)]` for every def/class in
    `tree`, at any nesting depth (unlike `module_bindings`, which is
    module-scope-only by design for the rendered map's public-API view). A
    method's range nests inside its class's, so picking the entry with the
    LARGEST `start_line` that still contains a target line is the innermost
    (most specific) enclosing scope."""
    scopes = []

    def walk(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                qualname = prefix + child.name
                scopes.append(
                    (child.lineno, getattr(child, "end_lineno", child.lineno), qualname)
                )
                walk(child, qualname + ".")
            else:
                walk(child, prefix)

    walk(tree, "")
    return scopes


def _top_level_targets(tree):
    """`[(start_line, name)]` for every module-scope NAME BINDING in
    `tree.body` — a def, a class, or a (possibly annotated) assignment to a
    bare name, tuple/list-unpack targets contributing each element. Sorted by
    line.

    A registry `CodeSymbol` cell routinely names a module-level CONSTANT
    (`STATUS_FILL`, `HTML_TEMPLATE`), and the kit's own convention for tagging
    one is a comment ending in `Implements: ...` sitting directly ABOVE the
    assignment — outside any AST node's own line range, the same shape
    `implements()`'s 4-line docstring lookback already reads for a `def`.
    `enclosing_symbol` below is this file's other consumer of that shape: the
    nearest FOLLOWING top-level statement is what a bare comment line
    describes, so a declaration line with no containing def/class resolves to
    that statement's bound name rather than falling all the way to bare
    module scope."""

    def names(target):
        if isinstance(target, ast.Name):
            return [target.id]
        if isinstance(target, (ast.Tuple, ast.List)):
            out = []
            for elt in target.elts:
                out.extend(names(elt))
            return out
        return []

    out = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append((node.lineno, node.name))
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                out.extend((node.lineno, n) for n in names(t))
        elif isinstance(node, ast.AnnAssign):
            out.extend((node.lineno, n) for n in names(node.target))
    return sorted(out)


def enclosing_symbol(scopes, top_level, lineno):
    """The symbol a declaration at `lineno` belongs to: the dotted qualname of
    the innermost `scopes` (a `_scope_index` result) entry containing it when
    one does; failing that, the name bound by the nearest FOLLOWING entry in
    `top_level` (a `_top_level_targets` result) — a comment directly above a
    module-level constant or def; failing that, `""` for true module scope
    (the front-matter docstring, or a declaration nothing follows) — the
    value `backlink_ids`' caller compares against a `CodeSymbol` cell's
    "module-only" (empty-cell) claim."""
    best, best_start = "", -1
    for start, end, qualname in scopes:
        if start <= lineno <= end and start > best_start:
            best, best_start = qualname, start
    if best:
        return best
    # The WINDOW is small and deliberate: `implements()` already reads at most
    # 4 lines above a `def` as its docstring-free lookback, so a comment more
    # than 4 lines ahead of the next top-level statement is not "directly
    # above" it — it is prose somewhere in a longer block (a module
    # docstring's closing paragraph, say), and reads as true module scope
    # rather than borrowing a distant statement's name.
    for start, name in top_level:
        if start > lineno:
            return name if start - lineno <= 4 else ""
    return ""


def declaration_sites(path):
    """`[(lineno, [spine ids], enclosing_symbol)]` for every literal
    `Implements:` declaration line in one `.py` file — `backlink_ids`'
    grammar, AST-scoped to name what encloses each declaration. `[]` for a
    file that fails to parse or decode (surface, don't crash, the
    `scan_module`/`scan_inventory` posture)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    scopes = _scope_index(tree)
    top_level = _top_level_targets(tree)
    sites = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        ids = backlink_ids(line)
        if ids:
            sites.append((lineno, ids, enclosing_symbol(scopes, top_level, lineno)))
    return sites


def implements_report(src_roots):
    """`(sites, known_names)` over every `.py` file under `src_roots`:
    `sites` is `{rel_path: [(lineno, ids, enclosing_symbol), ...]}` from
    `declaration_sites`; `known_names` is the set of every name `_scope_index`
    or `_top_level_targets` found anywhere in the surface (dotted def/class
    qualnames plus bare module-level constants) — a real symbol exists in
    this set wherever it lives, so a `CodeSymbol` cell naming something
    outside it is naming a function-local variable or a symbol that is gone,
    not a stale-but-real one. The one AST walk check_trajectory's CodeSymbol
    crosscheck consumes (WI-502; the `scan_inventory` idiom above)."""
    sites = {}
    known = set()
    for _root, base, path in _walk_roots(src_roots, "*.py"):
        rel = path.relative_to(base).as_posix()
        found = declaration_sites(path)
        if found:
            sites[rel] = found
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text)
        except (UnicodeDecodeError, OSError, SyntaxError):
            continue
        known.update(qualname for _s, _e, qualname in _scope_index(tree))
        known.update(name for _start, name in _top_level_targets(tree))
    return sites, known


def read_backlink_min(root):
    """`[checks] backlink_coverage_min` from `docs/process.toml` — the declared
    minimum reverse-coverage percentage. 0 (report the number, gate nothing) is
    both the shipped default and the answer for an absent, unreadable,
    wrong-typed or out-of-range dial.

    A LOCAL `tomllib` READ, per F5 (owner 2026-07-12, no shared `_kitcommon.py`):
    this module is imported by three checkers and copied standalone into every
    scaffold, so it must not reach into the coordinator layer that already knows
    how to read this file. It is the same posture `check_trajectory._process_check`
    and `gen_okf._process_check` hold for their own keys.

    IT FALLS BACK TO 0 RATHER THAN "ON, LOUDLY" — the opposite of those two
    boolean readers, and the reason is that this dial is not a boolean. A
    malformed file cannot tell us what bar the adopter meant, and inventing one
    would gate a repo on a number nobody declared. The loud half is not lost, it
    is elsewhere and stronger: `agent_common.PROCESS_ONLY_KEYS` type-checks this
    key and `config_conflicts` REFUSES a wrong-typed dial outright, so the
    residual silent case here is a file that fails to parse at all — which the
    same refusal reports on its own line."""
    path = Path(root) / "docs" / PROCESS_TOML
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return 0
    value = (data.get("checks") or {}).get(BACKLINK_MIN_KEY)
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return value if 0 <= value <= 100 else 0


def live_llr_ids(root, registry=LLR_REGISTRY):
    """Every LLR id in the project's design registry, `-000` template rows
    dropped. `[]` when the registry is absent under either carrier — a repo
    without a design tier has nothing to measure, and the report says so."""
    return [
        str(row.get("LLR-ID") or "").strip()
        for row in spine_carrier.load(Path(root) / registry, "LLR-ID", False)
        if str(row.get("LLR-ID") or "").strip()
    ]


def backlink_report(src_roots, root, exts=BACKLINK_EXTS, registry=LLR_REGISTRY):
    """`(lines, ok)` — the reverse-coverage report and whether the declared
    minimum is met. `ok` is True whenever the scan is VACUOUS (no LLR rows), so
    a fresh scaffold and a repo that never adopted the design tier both pay
    nothing."""
    ids = live_llr_ids(root, registry)
    minimum = read_backlink_min(root)
    roots = ", ".join(str(s) for s in src_roots)
    if not ids:
        return [
            "back-link coverage: no live LLR rows under {} — vacuous.".format(
                Path(root) / registry
            )
        ], True
    covered, uncovered, pct = backlink_coverage(src_roots, ids, exts)
    lines = [
        "back-link coverage: {}/{} live LLR rows ({:.1f}%) are named by a "
        "literal `Implements:` declaration under {}; declared minimum {}% "
        "(docs/{} [checks] {}).".format(
            len(covered), len(ids), pct, roots, minimum, PROCESS_TOML, BACKLINK_MIN_KEY
        )
    ]
    if minimum == 0:
        # The shipped position, and it is stated on every run rather than
        # implied by silence: a reader must be able to tell "this repo declined
        # the bar" from "this repo has never heard of the layer".
        lines.append(
            "back-link coverage: REPORT-ONLY — the minimum is 0, so the number "
            "is reported and nothing is gated. Raise it when your practice "
            "earns the bar."
        )
    elif pct < minimum:
        lines.append(
            "back-link coverage: WARNING - {:.1f}% is below the declared "
            "minimum of {}%. {} LLR row(s) carry no back-link, starting with "
            "{}. Raise coverage by writing the declarations, never by lowering "
            "the dial.".format(pct, minimum, len(uncovered), ", ".join(uncovered[:5]))
        )
    return lines, (pct >= minimum)


def _backlink_exit(src_roots, args):
    """Print the report and return the process exit code. Warn-first by default;
    `--strict-backlinks` promotes a below-minimum reading to a failure, the same
    warn-then-error ladder `interfaces_check`/`components_check` ride."""
    exts = tuple(args.backlink_ext) if args.backlink_ext else BACKLINK_EXTS
    lines, ok = backlink_report(src_roots, args.root, exts)
    for line in lines:
        print(line, file=sys.stdout if ok else sys.stderr)
    return 1 if (not ok and args.strict_backlinks) else 0


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
        "--cli-doc",
        action="append",
        default=None,
        help="REPORT MODE (needs no --doc): file(s) carrying the CLI REFERENCE "
        "marker pair, spliced with the argparse surface of every scanned "
        "module (repeatable). Honours --check.",
    )
    ap.add_argument(
        "--contracts-doc",
        action="append",
        default=None,
        help="REPORT MODE (needs no --doc): file(s) carrying the INTERFACE "
        "REFERENCE marker pair, spliced with the contract each module states "
        "for the seams it declares (repeatable). Honours --check.",
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
    ap.add_argument(
        "--backlink-coverage",
        action="store_true",
        help="REPORT MODE (writes nothing, needs no --doc): what share of live "
        "LLR rows is named by a literal `Implements:` declaration under --src. "
        "The bar is docs/process.toml [checks] backlink_coverage_min",
    )
    ap.add_argument(
        "--root",
        default=".",
        help="repo root holding docs/process.toml and the LLR registry "
        "(--backlink-coverage only; default: .)",
    )
    ap.add_argument(
        "--backlink-ext",
        action="append",
        default=None,
        help="source extension the back-link scan reads (repeatable; REPLACES "
        "the default list, which is _MODULE_EXTS plus the wider source "
        "families — see BACKLINK_EXTS)",
    )
    ap.add_argument(
        "--strict-backlinks",
        action="store_true",
        help="exit 1 when back-link coverage is below the declared minimum "
        "(warn-first without it; vacuous while the minimum is 0)",
    )
    args = ap.parse_args()

    src_roots = args.src or ["src"]
    # The report mode returns before every --doc/marker contract below: it reads
    # the source tree and writes nothing, so requiring a splice target would be
    # asking for a document the measurement never touches.
    if args.backlink_coverage:
        sys.exit(_backlink_exit(src_roots, args))
    if args.cli_doc:
        sys.exit(_cli_doc_exit(src_roots, args))
    if args.contracts_doc:
        sys.exit(_contracts_doc_exit(src_roots, args))
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
