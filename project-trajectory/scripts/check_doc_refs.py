#!/usr/bin/env python3
"""Doc reference validation — prose that names dead files or symbols (Thread 49).

`check_docs.py` proves a markdown *link* resolves; this closes the two rot
classes links can't see, with false-positive control as the design center
(validate precise shapes, never every backticked word):

  1. PATH TIER (aggressive — low ambiguity, high value): a backticked token
     shaped like a repo path (contains "/" and ends in a known source/doc
     extension, or starts with a conventional top-level dir) must exist on
     disk. A renamed or deleted file named in prose is one of the commonest
     real rots. A trailing LINE SUFFIX (`docs/x.md:40`, `docs/x.md:40-41`) is
     stripped first — a citation to a line still names the file, and it names
     it for both the shape test and the resolution (WI-396). URLs, globs, and
     `{placeholder}` shapes are skipped; a line carrying `path-ok` is exempt
     (the `privacy-ok` idiom) for deliberate examples naming files that don't
     exist here.

     Split UNTRACED from DANGLING (WI-062). A path that isn't on disk is not
     automatically rot, and treating it as such buried the signal: this repo
     reported 561 findings, of which 534 were explainable and 27 were worth
     looking at — and noise is how a real broken link hides. A missing path is
     reported as *untraced*, not dangling, when it has a mechanical reason:

       - KIT-RELATIVE — it resolves under `--kit-root` (default
         `project-trajectory/`, skipped when absent). A kit's own prose names
         its portable unit by the paths a DOWNSTREAM repo will have after
         copy-in (`scripts/check.py`, `hooks/pre-commit`, `ci/check.yml`), so
         those tokens are correct for their reader and merely not rooted here.
       - HISTORICAL — the doc is a RECORD surface (`--record-prefix`, default
         the log, archive, reviews, plans and review reports). A session log
         naming a file that has since been retired is accurate history, not a
         broken pointer; "fixing" it would falsify the record.
       - DECLARED (WI-308) — the path is listed, with its reason, in the
         `--declared-absences` file (default `docs/declared-absences`; ignored
         when absent). A repo states there what it deliberately does not carry:
         an opt-in registry it never enabled, a scaffold destination a meta-repo
         has no use for, a policy file whose ABSENCE is the documented default.
         Prose naming one is correct for its reader, and the declared reason is
         quoted back in the finding. Fail-soft in the safe direction: no file, or
         a line with no `<path> — <reason>` separator, declares nothing.

     Untraced findings are counted, never gate, and print only with
     `--show-untraced`. `--strict` gates on dangling alone. The distinction is
     the whole point: a suppression list hides findings, a REASON classifies
     them, so an untraced count that jumps is still a signal you can read.
  2. SYMBOL TIER (opt-in convention — no heuristic storm): only references
     written `sym:<module>.<name>` are checked, against the generated module
     map in architecture.md (the arch-map inventory is the oracle — reuse the
     artifact, don't re-parse the AST). You *assert* a symbol exists and the
     check holds you to it. No module map / no symbols -> the tier skips
     cleanly (a files-mode or non-Python stack degrades gracefully).
  3. REGISTRY TIER (WI-394, owner ruling R2 2026-08-01, option (c)): the
     spine's Evidence-class cells — TC `Evidence`, LLR `Module`/`CodeSymbol`/
     `TestRefs`, the four pointers OUT of the registries into the code and
     test tree — must cite files that EXIST. These cells are exactly what
     answers "how do you know this row is Verified", and every other link in
     the chain is mechanized; a deletion never asks what cited the deleted
     file, so they rot silently. A cell is a KNOWN joined list, split before
     the shape test; the FILE half of a `tests/x.py::node` citation is
     checked, and the `::node` selector is ruled PROSE — an accepted,
     documented gap (docs/enforcement-audit.md), never an implied check, so a
     renamed-but-still-present test node is deliberately NOT detected.
     Placeholder rows (`*-000`) are skipped so scaffolded templates stay
     copy-ready; absent registries skip the tier cleanly.

Ships WARN-FIRST and product-layer like check_stubs.py: exit 0 with warnings
unless --strict; NOT wired into check.py's required floor. Opt in per repo:

    [step:doc-refs]
    command = {py} scripts/check_doc_refs.py --strict

Scan surface = root *.md + docs/**/*.md (the check_docs surface) + the spine
registries' Evidence-class cells (tier 3). Stdlib only.

Contracts: IF-008, IF-028, IF-072 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
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
# Doc surfaces that RECORD what was true at a moment. A retired file named in a
# session log is accurate history; rewriting it to satisfy a linter would
# falsify the record, so a missing path there is untraced, never dangling.
#
# The line is WHO CAN ACT, not genre (WI-384, where adding the closed work-item
# directories was proposed, built, measured INERT and reverted): this list
# matches the CONTAINING FILE, so an entry here silences every missing path in
# every file under it, forever — a catch-all that can only ever cover tokens no
# earlier branch of `untraced_reason` already explains. It is right for
# `docs/log.md`, append-only compiled history nobody can maintain per-token, and
# wrong for a surface whose author is still standing there and can declare the
# path with its reason. That is also why `docs/log.d/` is deliberately absent
# while `docs/log.md` is present: a fragment is judged strictly while its author
# can still edit it, and becomes record the moment the trunk step compiles it —
# the same rule applied consistently, not an oversight.
RECORD_PREFIXES = (
    "docs/log.md",
    "docs/archive/",
    "docs/reviews/",
    "docs/plans/",
    "docs/repo-review-",
    "docs/test/report.md",
)
# The portable unit a kit ships. Prose inside it addresses files by the paths an
# ADOPTING repo will have after copy-in, so `scripts/check.py` is correct for its
# reader even though this repo keeps it at `project-trajectory/scripts/check.py`.
DEFAULT_KIT_ROOT = "project-trajectory"
# A repo may DECLARE the paths it deliberately does not carry, each with its
# reason, in one file (WI-308). Prose naming one is correct-for-its-reader in the
# same way a kit-relative path is: the reference describes a real destination,
# and its absence here is the documented state. Optional — no file, no reason.
DEFAULT_ABSENCES = "docs/declared-absences"
# A citation may point at a LINE inside the file it names: `docs/x.md:40`,
# `docs/x.md:40-41`. The path is the token WITHOUT that suffix, so it is stripped
# before the shape test and before the stat (WI-396). Both sites, deliberately:
# `is_path_shaped` is a predicate that cannot hand a rewritten token back, so
# stripping in it alone would leave `path_findings` stat-ing the whole
# `path:line` string and calling a live file missing.
#
# Suffixing is what made the old rule ASYMMETRIC rather than merely strict. It
# defeats the extension test (nothing ends in `.md` once `:40-41` is appended),
# which threw every suffixed token onto PATH_PREFIXES — a list of the DOWNSTREAM
# layout — so a suffixed reference into `project-trajectory/` (the tree this
# kit's own product lives in, and one no adopting repo carries) landed in NO
# bucket at all: not dangling, not untraced, never classified. Stripping fixes
# every prefix at once, which is why it is preferred over growing that list.
LINE_SUFFIX = re.compile(r":\d+(?:-\d+)?$")
BACKTICK = re.compile(r"`([^`\n]+)`")
SYM = re.compile(r"\bsym:([A-Za-z_][\w.]*)\.(\w+)\b")
MOD_HEAD = re.compile(r"^### `([^`]+)`")
SYM_ROW = re.compile(r"^\| `(\w+)[(`]")


def _strip_line_suffix(token):
    """`docs/x.md:40-41` -> `docs/x.md` (WI-396). Only a trailing all-digit
    `:<line>` / `:<line>-<line>` goes; anything else is part of the path."""
    return LINE_SUFFIX.sub("", token)


def _strip_node_selector(token):
    """`tests/x.py::test_name` -> `tests/x.py` (WI-394, ruling (c)). The FILE
    half of a pytest node id is a checkable path; the `::node` selector is
    ruled prose and never validated. Stripped at both sites, for the same
    reason WI-396 strips the line suffix at both: `is_path_shaped` is a
    predicate and cannot hand a rewritten token back."""
    return token.split("::", 1)[0]


def is_path_shaped(token):
    token = token.strip()
    if not token or "://" in token or any(c in token for c in "*{}<>$ "):
        return False
    # `;`/`,` join a list of paths — not a single filesystem path, so they
    # stay out of the path tier's scope (false-positive control is the point).
    # `::` used to keep a whole pytest node id out with them; WI-394 (owner
    # ruling R2, option (c)) RE-SCOPED that guard: a node id
    # (tests/x.py::test_name — the kit's sanctioned Evidence form) is a real
    # FILE plus a selector, so the file half is judged like any path while the
    # selector stays prose.
    if ";" in token or "," in token:
        return False
    token = _strip_node_selector(token)
    # Placeholder shapes, alongside `{}`/`*` above (WI-062): `…` stands in for
    # "and the rest" and `###`/`NNN` for "your id here", so `docs/specs/WI-###.md`
    # is a FORM, not a path. `#` also opens a markdown anchor, and an anchored
    # doc reference is a LINK — check_docs.py's job, not this tool's.
    if "…" in token or "#" in token or "NNN" in token:
        return False
    if "/" not in token:
        return False
    token = _strip_line_suffix(token)
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


def load_declared_absences(path):
    """`{path: reason}` from a declared-absences file, or `{}` when it is absent
    (WI-308). Format is one `<path> — <reason>` per line, `#` comments and blanks
    ignored; a line without the separator is skipped rather than fatal, so a
    malformed entry degrades to "not declared" — the conservative direction, since
    the failure mode of guessing is silencing a real rot."""
    if path is None or not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for sep in (" — ", " - "):
            if sep in line:
                p, reason = line.split(sep, 1)
                out[p.strip().rstrip("/")] = reason.strip()
                break
    return out


def untraced_reason(token, rel, root, kit_root, record_prefixes, absences=None):
    """Why a missing path is explainable, or None when it is real rot (WI-062).

    Order is by specificity, and only affects the message: a token can be both
    kit-relative and in a record surface. A DECLARED absence (WI-308) is the most
    specific of all — the repo has stated, with a reason, that it does not carry
    this path — so it is checked first and reports the declared reason verbatim."""
    if absences and token in absences:
        return "declared absent by design — {}".format(absences[token])
    if kit_root is not None and (kit_root / token).exists():
        return (
            "resolves under {}/ — a kit-relative path, correct for a repo "
            "that adopted the kit".format(kit_root.name)
        )
    if any(rel.startswith(p) for p in record_prefixes):
        return (
            "a record surface — history naming a path that has since moved or retired"
        )
    return None


def judge_token(
    token, entry, bad, untraced, rel, root, kit_root, record_prefixes, absences=None
):
    """Judge one cited token and file its verdict under `entry` — the finding
    label quoting the token as WRITTEN, so a reader can find it in the surface
    that cited it. Out-of-scope and resolving tokens file nothing.

    Shared by the path tier and the registry tier (WI-394), so the
    strip/stat/reason chain lives once: the stat, the untraced classification
    and the declared-absences lookup all take the STRIPPED path — the second
    of the two sites WI-396 names, and the WI-394 node-selector strip rides
    the same rule."""
    if not is_path_shaped(token):
        return
    clean = _strip_line_suffix(_strip_node_selector(token.strip())).rstrip("/")
    if (root / clean).exists():
        return
    why = untraced_reason(clean, rel, root, kit_root, record_prefixes, absences)
    if why:
        untraced.append("{} — {}".format(entry, why))
    else:
        bad.append("{} does not exist in the repo".format(entry))


def path_findings(line, rel, n, root, kit_root, record_prefixes, absences=None):
    """One line's path-tier verdicts as `(dangling, untraced)` (WI-062).

    Lifted out of `findings_for` so the per-token classification lives in one
    readable place rather than adding branches to the file walk — `findings_for`
    is already the tool's densest function."""
    bad, untraced = [], []
    for token in BACKTICK.findall(line):
        entry = "{}:{}: `{}`".format(rel, n, token)
        judge_token(
            token, entry, bad, untraced, rel, root, kit_root, record_prefixes, absences
        )
    return bad, untraced


# The spine cells that point OUT of the registries into the code/test tree
# (WI-394): the four columns carrying the spine's claim to be grounded in the
# code. Pointers BETWEEN registries (Verifies, SR-Refs, Component) are joined
# and validated by trace.py; these are the ones nothing checked. `CodeSymbol`
# carries `/`-joined symbol names, not paths — it is scanned so a real path
# written there is held to the rule, and `is_path_shaped` keeps the symbol
# joins out of scope. `TestRefs` is conventionally `(see TC-###)` — a registry
# pointer, trace.py's side of the line — and likewise yields no path token.
SPINE_CELLS = (
    ("docs/test/test-cases.csv", "TC-ID", ("Evidence",)),
    (
        "docs/requirements/low-level-requirements.csv",
        "LLR-ID",
        ("Module", "CodeSymbol", "TestRefs"),
    ),
)
# A registry cell is a KNOWN joined list (`;` between citations, whitespace
# between node ids), so it is SPLIT before the shape test — unlike a backticked
# prose token, where a joiner keeps the whole token out of the path tier.
CELL_JOIN = re.compile(r"[\s;,]+")


def registry_findings(
    root, kit_root=None, record_prefixes=RECORD_PREFIXES, absences=None
):
    """`(dangling, untraced)` over the spine's Evidence-class cells (WI-394).

    The markdown tiers never see the CSVs. Ruling (c): the FILE half of each
    citation must exist (`Path.exists`, repo-relative); the `::node` selector
    is ruled prose. Same classification as the path tier — a missing file with
    a mechanical reason is untraced, the rest is dangling. Placeholder rows
    (`*-000`) are skipped so scaffolded templates stay copy-ready; a repo
    without the registries (or a pre-spine rung) skips the tier cleanly.
    """
    bad, untraced = [], []
    for rel, idcol, cols in SPINE_CELLS:
        reg = root / rel
        if not reg.is_file():
            continue
        with reg.open(newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                rid = (row.get(idcol) or "").strip()
                if not rid or rid.endswith("-000"):
                    continue
                for col in cols:
                    for token in CELL_JOIN.split(row.get(col) or ""):
                        entry = "{}: {} {}: `{}`".format(rel, rid, col, token)
                        judge_token(
                            token,
                            entry,
                            bad,
                            untraced,
                            rel,
                            root,
                            kit_root,
                            record_prefixes,
                            absences,
                        )
    return bad, untraced


def authored_lines(doc):
    """`(n, line)` pairs of the surface's hand-authored lines. Generated marker
    blocks (the module map, flow diagrams) are not hand-authored prose — their
    freshness is the generator's --check contract, and their tokens (module
    names like `src/demo`) are not disk paths — so they are skipped here, once,
    for every doc lint that walks a surface (this module's tiers and
    check_figures.py both read through it, WI-392)."""
    in_generated = False
    for n, line in enumerate(
        doc.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1
    ):
        if "<!-- BEGIN GENERATED" in line:
            in_generated = True
        if "<!-- END GENERATED" in line:
            in_generated = False
            continue
        if in_generated:
            continue
        yield n, line


def findings_for(
    doc, root, oracle, kit_root=None, record_prefixes=RECORD_PREFIXES, absences=None
):
    """`(dangling, untraced)` — see the module docstring for the split."""
    out, untraced = [], []
    rel = doc.relative_to(root).as_posix()
    for n, line in authored_lines(doc):
        if "path-ok" in line:
            continue  # deliberate example naming a path that isn't here
        bad, explained = path_findings(
            line, rel, n, root, kit_root, record_prefixes, absences
        )
        out += bad
        untraced += explained
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
    return out, untraced


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
        help="exit 1 on DANGLING findings (default: warn-first, exit 0). "
        "Untraced findings never gate — see --show-untraced.",
    )
    ap.add_argument(
        "--kit-root",
        default=DEFAULT_KIT_ROOT,
        help="second root a path may resolve against — a kit's portable unit, "
        "whose prose addresses files by the paths an adopting repo will have "
        "(default {}; ignored when absent)".format(DEFAULT_KIT_ROOT),
    )
    ap.add_argument(
        "--record-prefix",
        action="append",
        default=None,
        help="doc prefix that RECORDS history, where a moved/retired path is "
        "accurate rather than broken (repeatable; defaults to {})".format(
            ", ".join(RECORD_PREFIXES)
        ),
    )
    ap.add_argument(
        "--declared-absences",
        default=DEFAULT_ABSENCES,
        help="file declaring the paths this repo deliberately does not carry, "
        "one `<path> — <reason>` per line; a reference to one is untraced with "
        "its declared reason (default {}; ignored when absent)".format(
            DEFAULT_ABSENCES
        ),
    )
    ap.add_argument(
        "--show-untraced",
        action="store_true",
        help="print the explained findings too, with their reason",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()
    kit_root = (root / args.kit_root) if args.kit_root else None
    if kit_root is not None and not kit_root.is_dir():
        kit_root = None
    records = tuple(args.record_prefix) if args.record_prefix else RECORD_PREFIXES
    absences = load_declared_absences(
        (root / args.declared_absences) if args.declared_absences else None
    )
    oracle = load_symbol_oracle(root / args.arch)
    if not oracle:
        print(
            "check_doc_refs: no symbol inventory in {} — the sym: tier is "
            "skipped (path tier still runs).".format(args.arch)
        )
    findings, untraced = [], []
    for doc in doc_files(root):
        found, explained = findings_for(doc, root, oracle, kit_root, records, absences)
        findings += found
        untraced += explained
    reg_bad, reg_untraced = registry_findings(root, kit_root, records, absences)
    findings += reg_bad
    untraced += reg_untraced
    for f in findings:
        print("check_doc_refs: WARN - " + f, file=sys.stderr)
    if args.show_untraced:
        for u in untraced:
            print("check_doc_refs: UNTRACED - " + u, file=sys.stderr)
    # Always REPORT the untraced count even when the list is silent: a
    # classification you can't see the size of is a suppression list.
    tail = ""
    if untraced:
        tail = " · {} untraced (explained: declared absent, kit-relative, or a record surface){}".format(
            len(untraced), "" if args.show_untraced else " — --show-untraced to list"
        )
    if findings:
        print(
            "check_doc_refs: {} dangling reference(s){}{}.".format(
                len(findings),
                "" if args.strict else " (warn-first; --strict gates)",
                tail,
            )
        )
        return 1 if args.strict else 0
    print("check_doc_refs: OK - no dangling path or sym: references{}.".format(tail))
    return 0


if __name__ == "__main__":
    sys.exit(main())
