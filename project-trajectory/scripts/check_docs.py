#!/usr/bin/env python3
"""Doc navigability & staleness check: keep the hand-written doc set honest.

The harness already gates the freshness of *generated* blocks (the code map —
`gen_arch_map.py --check`), but nothing checks that the **hand-written** docs
stay navigable: that every intra-repo link resolves, every doc is reachable,
and a doc hasn't been frozen beside churning code. This operationalizes the
"verify no broken intra-doc links" step several gates ask a human to do by hand,
extending the "the map must stay honest" guarantee from code to docs
(process.md §3 "Reviewability").

Stdlib only, like trace.py / check_flows.py:

    python scripts/check_docs.py [--root .] [--docs docs] [--entry PATH ...]
                                 [--ignore GLOB ...] [--strict-orphans] [--stale]

It scans root-level `*.md` plus everything under `docs/`, then reports five
finding classes:

  - **broken intra-repo links** (target file/dir or `#anchor` missing) — a hard
    finding; exit 1.
  - **orphan docs** (no path from an entry root: root-level `*.md`, an optional
    `docs/index.md` Map-of-Content, or a `--entry`) — a warning by default; exit
    1 only with `--strict-orphans`. A fresh scaffold legitimately has standalone
    docs (interfaces, stakeholder-needs) until the project links them, so the
    floor is warn, not fail. Docs under `docs/archive/` (frozen history) are
    exempt — orphanhood is noise there, though their links are still validated.
  - **the vision tag** (process.md §4 G1's mechanizable half): the root README
    must carry the singleton `PROJECT-VISION:` tag exactly once — zero (the
    canonical vision statement is missing) or several (a re-authored variant;
    other docs point at the tag, never restate it) is a hard finding; exit 1.
    No root README at all degrades to a warning (a louder, different problem).
  - **README need coverage** (**opt-out**; process.md §4 G1): traceability is the
    kit's core value, so the root README is held to it too — every SN id cited
    anywhere in it must exist in the stakeholder-needs registry, and every
    Must/Should need in that registry must be cited somewhere in the README, so a
    requirements change mechanically ages the README. Draft/unratified needs (under
    a "draft" heading — SN maturity is section-as-state, §4a) are exempt from that
    floor until ratified. No delimiter markers: any
    `SN-###` in the README counts as a citation. A README opts out with an
    `<!-- sn-inventory: off -->` comment; a repo with no real needs yet (only the
    `-000` placeholder) is vacuously clean, so a fresh scaffold passes.
  - **staleness** (`--stale`, git-gated): a doc linking a *non-doc* file
    (source/asset) that was committed more recently than the doc itself — a
    "lying map" heuristic. Printed as a **`hint`**, a severity below `WARN`: it
    is a low-confidence nudge to look, not a finding (a linked file often
    changes without invalidating the prose), so it never counts toward the exit
    status. Degrades to a clean skip when git is unavailable or off a work tree.
    Docs under `docs/archive/` (frozen history) are exempt — staleness is noise
    there.

  - **status-surface structure** (**warn-only**, never the exit code;
    process-options.md "Trajectory / work-items layer"): `docs/status.md` is the
    lean status snapshot, so (S-1) it warns past a line budget — default 120,
    `docs/status-lint` overrides with an integer or the one word `off` (which
    disables S-1..S-3); (S-2) its Open-items marker must precede the `## Scope`
    heading (open items surface at the top); (S-3) with `docs/open-items.md`
    present, every `OI-N` inside the Needs-<human> block has a `## OI-N`
    section there (no undocumented owner ask) and every section id appears in
    status.md (no orphan brief). S-3 extraction is best-effort over the
    template's shape; a custom layout misses warnings, never false-fails.
    Vacuous when status.md (or, for S-3, open-items.md) is absent.

The root `OWNER_SCRATCHPAD.md` is exempt from all of the above: it holds the
human owner's free-form private notes and is dropped from doc discovery entirely
(agents must not read or act on it; its own header says so).

Scope (the high-value 80%): inline links `[text](dest)` and same-file/`file#frag`
anchors against GitHub-style heading slugs (plus `{#custom-id}` suffixes and
`<a name=...>`/`id=...`). Out of scope by design: reference-style links
(`[t][ref]`), images (`![alt](src)` — skipped, not existence-checked), and links
inside fenced/inline code (stripped before parsing). Anchors are only validated
against Markdown targets the script can parse.

Contracts: IF-002, IF-030 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII doc path or link target in a finding can't raise
    UnicodeEncodeError on a legacy Windows cp1252 console. Python 3.7+ streams
    expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# A fenced code block opens/closes on a line of >=3 backticks or tildes.
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
# Inline code span: a run of N backticks closed by a run of exactly N (CommonMark),
# stripped so `[x](y)` written as an example isn't parsed as a real link. The
# equal-length match matters for the double-backtick form `` `[`x`](y)` `` used
# when the span's own text contains backticks — a single-backtick regex mis-splits
# it and leaks `[](y)` as a phantom broken link (WI-174).
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?:(?!\1).)*?\1(?!`)", re.DOTALL)
# ATX heading: 1-6 leading #, optional trailing #s.
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
# Inline link: optional leading ! (image), [text](dest "optional title").
# dest is either <bracketed> or a run with no whitespace/closing paren.
LINK_RE = re.compile(r"(!?)\[[^\]]*\]\(\s*(<[^>]*>|[^)\s]*)(?:\s+[^)]*)?\)")
# Explicit anchors: a `{#custom-id}` heading suffix and HTML name=/id= attrs.
CUSTOM_ID_RE = re.compile(r"\{#([\w-]+)\}\s*$")
HTML_ANCHOR_RE = re.compile(r"""<a\s[^>]*\b(?:name|id)\s*=\s*["']([^"']+)["']""", re.I)
# A URL scheme (http:, mailto:, …) or protocol-relative // marks an external link.
EXTERNAL_RE = re.compile(r"^(?:[A-Za-z][A-Za-z0-9+.\-]*:|//)")
MD_SUFFIXES = (".md", ".markdown")
# The gen_okf.py knowledge bundle: a fully-generated tree gated by its own
# `gen_okf.py --check`. Dropped from doc discovery below so this tool never lints
# generated output (the gen_arch_map/gen_trajectory/check_doc_refs idiom); the
# path constant matches gen_okf's own OUT_DIR.
OKF_DIR = "docs/okf"
# The root owner scratchpad: free-form notes the human owner keeps, off-limits to
# agents (its own loud header says so). Dropped from doc discovery entirely — its
# links, orphanhood, and staleness never gate a commit (owner notes aren't a
# working surface) — via the same "never lint this file" idiom as OKF_DIR. It
# still resolves as a link *target* (the file is on disk) and the always-on
# secrets floor still scans it.
SCRATCHPAD = "OWNER_SCRATCHPAD.md"
# The design-history archive: frozen context. Archived docs KEEP broken-link
# validation (a dead link in the history still misleads a future reader, and the
# archival flow re-bases links once at archive time), but are DROPPED from orphan
# warnings and stale-mtime hints — "nothing links here" and "older than a file it
# links" are noise by definition for a doc that is deliberately frozen. Hardcoded
# like OKF_DIR (the archive lives under docs/ by convention, regardless of --docs).
ARCHIVE_DIR = "docs/archive"
# The singleton tag opening the root README's vision statement (process.md §4 G1).
VISION_TOKEN = "PROJECT-VISION:"
# README need coverage is ON by default (opt-out); a README disables it with this
# comment on its own line (process.md §4 G1). Anchored to a whole line so prose
# that merely *documents* the opt-out (inline, mid-sentence) can't trip it — a
# real opt-out puts the marker on its own line. Citations are any SN-### in the
# README — no delimiter markers.
SN_INVENTORY_OFF_RE = re.compile(
    r"^[ \t]*<!--\s*sn-inventory:\s*off\s*-->[ \t]*$", re.I | re.M
)
SN_ID_RE = re.compile(r"\bSN-\d+\b")


def _is_sn_example(sid):
    """The `-000` placeholder id the registry tooling ignores (matches trace.py)."""
    return sid.endswith("-000")


def _in_archive(relpath):
    """True for a doc under docs/archive/ — orphan/stale-exempt (links still
    checked), the frozen-history scan-scope (ARCHIVE_DIR)."""
    return relpath == ARCHIVE_DIR or relpath.startswith(ARCHIVE_DIR + "/")


def slugify(text):
    """GitHub-style heading slug: lowercase, drop punctuation, spaces->hyphens.

    Each whitespace run-member becomes its own hyphen (so "A & B" -> "a--b"),
    matching github-slugger closely enough for intra-doc anchor links.
    """
    s = text.strip()
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)  # [text](url) -> text
    s = s.replace("`", "").replace("*", "").replace("_", "")
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)  # keep word chars, whitespace, hyphen
    s = re.sub(r"\s", "-", s)
    return s


def blank_fenced(text):
    """Return the lines of `text` with fenced code blocks blanked out (line
    count preserved so reported line numbers stay accurate)."""
    out = []
    fence = None
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)[0]
                out.append("")
            else:
                out.append(line)
        else:
            if m and m.group(1)[0] == fence:
                fence = None
            out.append("")
    return out


def parse_doc(path):
    """Parse one Markdown file into its outbound links and its anchor set."""
    text = path.read_text(encoding="utf-8")
    links = []  # (lineno, dest)
    anchors = set()  # slugs/ids this doc exposes as #fragments
    seen = {}  # slug -> count, for GitHub's -1/-2 disambiguation
    unfenced = "\n".join(blank_fenced(text))
    # Strip spans over the whole document because CommonMark permits inline code
    # to cross a line boundary. Preserve its newlines so finding line numbers do
    # not shift when a multiline span precedes a real link.
    cleaned_text = INLINE_CODE_RE.sub(
        lambda match: "\n" * match.group(0).count("\n"), unfenced
    )
    for i, line in enumerate(cleaned_text.splitlines(), 1):
        for m in HTML_ANCHOR_RE.finditer(line):
            anchors.add(m.group(1).lower())
        heading = HEADING_RE.match(line)
        if heading:
            title = heading.group(2)
            cid = CUSTOM_ID_RE.search(title)
            if cid:
                anchors.add(cid.group(1).lower())
                title = CUSTOM_ID_RE.sub("", title)
            slug = slugify(title)
            if slug:
                n = seen.get(slug, 0)
                anchors.add(slug if n == 0 else "{}-{}".format(slug, n))
                seen[slug] = n + 1
            continue
        for m in LINK_RE.finditer(line):
            if m.group(1) == "!":
                continue  # image: out of scope (see module docstring)
            dest = m.group(2).strip()
            if dest.startswith("<") and dest.endswith(">"):
                dest = dest[1:-1].strip()
            if dest:
                links.append((i, dest))
    return {"links": links, "anchors": anchors}


def collect_docs(root, docs_dir, ignore=()):
    """Root-level *.md plus every *.md under docs/, de-duplicated and resolved.

    The gen_okf.py bundle under `docs/okf/` is dropped unconditionally: it is a
    fully-generated tree whose freshness `gen_okf.py --check` owns, so the doc set
    never lints its own generated output (the gen_arch_map/gen_trajectory idiom).
    The root `OWNER_SCRATCHPAD.md` is dropped the same way: free-form owner notes
    never gate (SCRATCHPAD).

    Paths matching an `ignore` glob (repo-relative POSIX) are dropped entirely —
    not parsed, not orphan-reported — so generated composites (the gitignored
    `docs/test/report.md`) don't show up as findings. Both the bundle and ignored
    files still resolve as link *targets*, since the file is on disk.
    """
    found = {}
    for p in sorted(root.glob("*.md")):
        found[p.resolve()] = True
    dd = root / docs_dir
    if dd.is_dir():
        for p in sorted(dd.rglob("*.md")):
            found[p.resolve()] = True
    docs = []
    for p in found:
        relpath = rel(p, root)
        # Never lint generated output: gen_okf.py --check owns docs/okf/ freshness.
        if relpath == OKF_DIR or relpath.startswith(OKF_DIR + "/"):
            continue
        # Owner-only free-form notes never gate: drop the scratchpad entirely.
        if relpath == SCRATCHPAD:
            continue
        if any(Path(relpath).match(g) for g in ignore):
            continue
        docs.append(p)
    return docs


def rel(path, root):
    """Display path: repo-relative POSIX, or absolute if outside the root."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def check_links(parsed, docs, root):
    """Validate every outbound link; build the doc->doc reachability graph.

    Returns (broken, graph): broken is a list of (src, lineno, dest, reason);
    graph maps each scanned doc to the set of scanned docs it links to.
    """
    docset = set(docs)
    broken = []
    graph = {d: set() for d in docs}
    anchor_cache = dict(parsed)  # memoize on-demand parses of off-set md targets
    for d, info in parsed.items():
        src = rel(d, root)
        for lineno, dest in info["links"]:
            if dest.startswith("#"):  # same-file anchor
                anchor = dest[1:].lower()
                if anchor and anchor not in info["anchors"]:
                    broken.append((src, lineno, dest, "no such anchor in this doc"))
                continue
            if EXTERNAL_RE.match(dest):
                continue
            path_part, _, frag = dest.partition("#")
            if not path_part:
                continue
            target = (d.parent / unquote(path_part)).resolve()
            if not target.exists():
                broken.append((src, lineno, dest, "target not found"))
                continue
            if target.is_dir():
                continue  # a link to a directory that exists is fine
            if target in docset:
                graph[d].add(target)
            if frag:
                tinfo = anchor_cache.get(target)
                if tinfo is None and target.suffix.lower() in MD_SUFFIXES:
                    tinfo = parse_doc(target)
                    anchor_cache[target] = tinfo
                if tinfo is not None and frag.lower() not in tinfo["anchors"]:
                    broken.append((src, lineno, dest, "no such anchor in target"))
    return broken, graph


def entry_roots(root, docs, docs_dir, extra):
    """Reachability roots: top-level *.md, an optional docs/index.md Map-of-
    Content, and any explicit --entry. These are never reported as orphans."""
    roots = set()
    docset = set(docs)
    for d in docs:
        if d.parent == root:
            roots.add(d)
    moc = (root / docs_dir / "index.md").resolve()
    if moc in docset:
        roots.add(moc)
    for e in extra:
        roots.add((root / e).resolve())
    return roots


def reachable(roots, graph):
    """Docs reachable from any entry root by following doc->doc links."""
    seen = set()
    stack = [r for r in roots if r in graph]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph.get(node, ()))
    return seen


def find_orphans(docs, graph, roots, root):
    """Scanned docs with no path from an entry root (entry roots excepted).

    Archived docs (docs/archive/) are dropped from the orphan list: orphanhood is
    noise for frozen history (their links are still validated). See _in_archive.
    """
    reached = reachable(roots, graph)
    orphans = [
        rel(d, root)
        for d in docs
        if d not in roots and d not in reached and not _in_archive(rel(d, root))
    ]
    return sorted(orphans)


def _root_readme(docs, root):
    """The root-level README.md among the scanned docs, or None."""
    return next(
        (d for d in docs if d.parent == root and d.name.lower() == "readme.md"),
        None,
    )


def check_vision(docs, root):
    """The root README must state the vision exactly once (process.md §4 G1).

    The `PROJECT-VISION:` tag is the purpose fact's canonical home — other docs
    point at it and never restate it — so a missing tag and a re-authored
    duplicate are both hard findings. Mentions inside code spans/fences are
    stripped first (quoting the convention is not stating a vision). Returns
    (failures, warnings) as printable message strings; no root README at all is
    a warning, not a failure, so bare doc trees stay usable.
    """
    readme = _root_readme(docs, root)
    if readme is None:
        return [], ["no root README.md - {} tag check skipped".format(VISION_TOKEN)]
    lines = blank_fenced(readme.read_text(encoding="utf-8"))
    n = sum(INLINE_CODE_RE.sub("", line).count(VISION_TOKEN) for line in lines)
    src = rel(readme, root)
    if n == 0:
        return [
            "{}: missing the {} tag (the canonical vision statement; "
            "process.md §4 G1)".format(src, VISION_TOKEN)
        ], []
    if n > 1:
        return [
            "{}: {} {} tags (the tag is a singleton - other docs point at "
            "it, never restate it)".format(src, n, VISION_TOKEN)
        ], []
    return [], []


def _registry_needs(path):
    """(all real SN ids, Must/Should SN ids) scraped from the SN markdown registry.

    Existence uses the same whole-file `SN-\\d+` scrape as trace.py; the
    Must/Should floor reads the Priority column of whichever table declares one
    (the core-needs table), so edge-case/Could rows don't force README bullets.
    A registry with no Priority column yields an empty floor (existence still
    checked) rather than a spurious finding.
    """
    text = path.read_text(encoding="utf-8")
    all_ids = {s for s in SN_ID_RE.findall(text) if not _is_sn_example(s)}
    must_should = set()
    prio_col = None
    in_draft = False
    for line in blank_fenced(text):
        stripped = line.lstrip()
        heading = re.match(r"#{1,6}\s+(.*)", stripped)
        if heading:
            # SN maturity is section-as-state (derived-gate model §4a): a heading
            # whose text contains "draft" marks its needs unratified (G0), so they
            # are exempt from the Must/Should README-coverage floor below (existence
            # still holds — a draft SN the README cites must still be a real id).
            in_draft = "draft" in heading.group(1).lower()
            prio_col = None
            continue
        if not stripped.startswith("|"):
            prio_col = None  # a non-table line ends the current table
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        lowered = [c.lower() for c in cells]
        if "priority" in lowered:
            prio_col = lowered.index("priority")
            continue
        if prio_col is None or prio_col >= len(cells):
            continue
        if not in_draft and cells[prio_col].upper() in ("M", "S", "MUST", "SHOULD"):
            must_should.update(
                s for s in SN_ID_RE.findall(line) if not _is_sn_example(s)
            )
    return all_ids, must_should


def check_inventory(docs, root, docs_dir):
    """The root README honors the traceability spine (process.md §4 G1).

    ON by default (opt-out): every SN id cited anywhere in the README must exist
    in the stakeholder-needs registry, and every Must/Should need in that registry
    must be cited somewhere in the README — so a requirements change mechanically
    ages the README. No delimiter markers: any `SN-###` counts as a citation. A
    README opts out with an `<!-- sn-inventory: off -->` comment; a repo with no
    real needs yet (only the `-000` placeholder) is vacuously clean. Returns
    (failures, warnings) as printable message strings.
    """
    readme = _root_readme(docs, root)
    if readme is None:
        return [], []  # the vision check already reports a missing README
    text = readme.read_text(encoding="utf-8")
    if SN_INVENTORY_OFF_RE.search(text):
        return [], []  # explicit opt-out
    registry = (root / docs_dir / "requirements" / "stakeholder-needs.md").resolve()
    if not registry.exists():
        return [], []  # no needs to hold the README to (vacuous)
    src = rel(readme, root)
    cited = {s for s in SN_ID_RE.findall(text) if not _is_sn_example(s)}
    all_ids, must_should = _registry_needs(registry)
    reg = rel(registry, root)
    fails = []
    for sid in sorted(cited - all_ids):
        fails.append(
            "{}: README cites {}, absent from the needs registry "
            "(fix the id, or opt out with <!-- sn-inventory: off -->)".format(src, sid)
        )
    for sid in sorted(must_should - cited):
        fails.append(
            "{}: {} (Must/Should) is cited by no README bullet "
            "(add it to the README, or opt out with <!-- sn-inventory: off -->)".format(
                reg, sid
            )
        )
    return fails, []


def git_commit_lookup(root):
    """Return a memoized path->last-commit-epoch lookup, or None when git is
    unavailable or `root` isn't inside a git work tree (so --stale degrades to a
    clean skip rather than failing)."""
    if not shutil.which("git"):
        return None
    probe = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if probe.returncode != 0 or probe.stdout.strip() != "true":
        return None
    cache = {}

    def lookup(path):
        if path in cache:
            return cache[path]
        out = subprocess.run(
            ["git", "-C", str(root), "log", "-1", "--format=%ct", "--", str(path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        val = int(out.stdout.strip()) if out.stdout.strip().isdigit() else None
        cache[path] = val
        return val

    return lookup


def find_stale(parsed, root, lookup):
    """Docs linking a non-doc file committed more recently than the doc itself.

    `lookup` is path->epoch (injectable for tests). Doc-to-doc links are skipped
    (too noisy a signal); unresolvable/untracked targets degrade to skip. Archived
    docs (docs/archive/) are skipped entirely: staleness is noise for deliberately
    frozen history (_in_archive, the FB4 scan-scope).
    """
    stale = []
    for d, info in parsed.items():
        if _in_archive(rel(d, root)):
            continue
        d_time = lookup(d)
        if d_time is None:
            continue
        for lineno, dest in info["links"]:
            if dest.startswith("#") or EXTERNAL_RE.match(dest):
                continue
            path_part = dest.partition("#")[0]
            if not path_part:
                continue
            target = (d.parent / unquote(path_part)).resolve()
            if not target.is_file() or target.suffix.lower() in MD_SUFFIXES:
                continue
            t_time = lookup(target)
            if t_time is not None and t_time > d_time:
                stale.append((rel(d, root), lineno, dest))
    return stale


# --- status-surface structure (S-1..S-3; warn-only) --------------------------
# The lean-surface contract on docs/status.md, mechanized at its self-proving
# floor: length + ordering + OI coherence. Content quality (is the pros/cons
# real?) is reviewer-class by the enforcement audit and deliberately NOT here.

STATUS_BUDGET_DEFAULT = 120
_OI_RE = re.compile(r"\bOI-\d+\b")
_OI_HEADING_RE = re.compile(r"^#{2,3}\s+[^\n]*?\b(OI-\d+)\b", re.M)
_NEEDS_HUMAN_RE = re.compile(r"needs\s*\\?<human>", re.I)
_SCOPE_HEADING_RE = re.compile(r"^##\s+scope\b", re.I | re.M)
_OPEN_ITEMS_MARKER_RE = re.compile(r"open items", re.I)


def _status_lint_policy(root, docs_dir):
    """The `docs/status-lint` declared value (declared-file idiom: `#` comment
    lines, one value on the last non-blank line): an int line budget, the string
    "off", or None (absent/blank/unparseable => the default budget)."""
    p = root / docs_dir / "status-lint"
    if not p.exists():
        return None
    value = None
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            value = line
    if value is None:
        return None
    if value.lower() == "off":
        return "off"
    try:
        return int(value)
    except ValueError:
        return None


def _needs_human_block(text):
    """The Needs-<human> block of status.md, best-effort over the template's
    mandated shape: from the marker line, a bullet's block runs while lines are
    blank or indented deeper than the marker; a heading's block runs to the next
    heading. Returns "" when no marker is found (S-3 then only checks the
    orphan-brief direction)."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not _NEEDS_HUMAN_RE.search(line):
            continue
        block = [line]
        if line.lstrip().startswith("#"):
            for nxt in lines[i + 1 :]:
                if nxt.lstrip().startswith("#"):
                    break
                block.append(nxt)
        else:
            indent = len(line) - len(line.lstrip())
            for nxt in lines[i + 1 :]:
                if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                    break
                block.append(nxt)
        return "\n".join(block)
    return ""


def check_status_surface(root, docs_dir):
    """S-1 (line budget) / S-2 (Open items before ## Scope) / S-3 (OI coherence
    with docs/open-items.md) over docs/status.md — warnings only, never the exit
    code (the WI-129 stance: warn, don't gate, don't mutate). Vacuous when
    status.md is absent or docs/status-lint says `off`."""
    status = root / docs_dir / "status.md"
    if not status.exists():
        return []
    policy = _status_lint_policy(root, docs_dir)
    if policy == "off":
        return []
    budget = policy if isinstance(policy, int) else STATUS_BUDGET_DEFAULT
    text = status.read_text(encoding="utf-8", errors="replace")
    warns = []

    n_lines = len(text.splitlines())
    if n_lines > budget:
        warns.append(
            "status.md is {} lines (budget {}): it is the lean status snapshot "
            "— move depth to open-items.md / the WI registry / the log "
            "(docs/status-lint overrides the budget, `off` disables)".format(
                n_lines, budget
            )
        )

    scope = _SCOPE_HEADING_RE.search(text)
    marker = _OPEN_ITEMS_MARKER_RE.search(text)
    if scope and not marker:
        warns.append(
            "status.md has a ## Scope section but no Open-items marker — the "
            "open items must surface on the working surface"
        )
    elif scope and marker and marker.start() > scope.start():
        warns.append(
            "status.md lists Open items after ## Scope — open items surface at "
            "the top, backward/context matter below"
        )

    open_items = root / docs_dir / "open-items.md"
    if open_items.exists():
        oi_text = open_items.read_text(encoding="utf-8", errors="replace")
        briefed = set(_OI_HEADING_RE.findall(oi_text))
        needs = set(_OI_RE.findall(_needs_human_block(text)))
        for oid in sorted(needs - briefed):
            warns.append(
                "{}: a Needs-<human> item in status.md with no `## {}` section "
                "in open-items.md (every owner ask carries its brief)".format(oid, oid)
            )
        for oid in sorted(briefed - set(_OI_RE.findall(text))):
            warns.append(
                "{}: briefed in open-items.md but never named in status.md "
                "(an orphan brief — ruled items move to the log's Decisions "
                "and the section is deleted)".format(oid)
            )
    return warns


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--docs", default="docs", help="docs subdirectory to scan (default: docs)"
    )
    ap.add_argument(
        "--entry",
        action="append",
        default=[],
        metavar="PATH",
        help="extra entry-root doc for reachability (repeatable)",
    )
    ap.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="GLOB",
        help="repo-relative glob to drop from the scanned set, e.g. a generated "
        "composite like docs/test/report.md (repeatable)",
    )
    ap.add_argument(
        "--strict-orphans",
        action="store_true",
        help="treat orphan docs as failures, not warnings",
    )
    ap.add_argument(
        "--stale",
        action="store_true",
        help="also warn on docs older than the non-doc files they link (needs git)",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    docs = collect_docs(root, args.docs, args.ignore)
    if not docs:
        print("check_docs: OK - no Markdown docs found under {}".format(root))
        return
    parsed = {d: parse_doc(d) for d in docs}

    broken, graph = check_links(parsed, docs, root)
    roots = entry_roots(root, docs, args.docs, args.entry)
    orphans = find_orphans(docs, graph, roots, root)
    vision_fails, vision_warns = check_vision(docs, root)
    inv_fails, inv_warns = check_inventory(docs, root, args.docs)

    for src, lineno, dest, reason in broken:
        print(
            "check_docs: FAIL - {}:{} broken link -> {} ({})".format(
                src, lineno, dest, reason
            )
        )
    for o in orphans:
        print(
            "check_docs: {} - orphan doc (no path from an entry root): {}".format(
                "FAIL" if args.strict_orphans else "WARN", o
            )
        )
    for msg in vision_fails + inv_fails:
        print("check_docs: FAIL - " + msg)
    # Warn-only by design (never the exit code): the status-surface structure.
    status_warns = check_status_surface(root, args.docs)
    for msg in vision_warns + inv_warns + status_warns:
        print("check_docs: WARN - " + msg)

    if args.stale:
        lookup = git_commit_lookup(root)
        if lookup is None:
            print(
                "check_docs: staleness check skipped "
                "(git unavailable or not a git work tree)"
            )
        else:
            for src, lineno, dest in find_stale(parsed, root, lookup):
                print(
                    "check_docs: hint - possibly stale: {}:{} links {} "
                    "(changed after the doc)".format(src, lineno, dest)
                )

    readme_fails = vision_fails + inv_fails
    failed = broken or readme_fails or (args.strict_orphans and orphans)
    n_links = sum(
        1
        for info in parsed.values()
        for _, dest in info["links"]
        if not EXTERNAL_RE.match(dest)
    )
    if failed:
        print(
            "check_docs: FAIL - {} broken link(s), {} orphan(s), "
            "{} README finding(s) across {} doc(s).".format(
                len(broken), len(orphans), len(readme_fails), len(docs)
            )
        )
        sys.exit(1)
    print(
        "check_docs: OK - {} doc(s), {} intra-repo link(s), 0 broken{}.".format(
            len(docs),
            n_links,
            " ({} orphan warning(s))".format(len(orphans)) if orphans else "",
        )
    )


if __name__ == "__main__":
    main()
