"""Parse/sources for the project-state dashboard — registries, docs, git.

The spine/OKF/arch-map/gate readers, the one subprocess capture seam
(_run_captured/_asof/_git), and the guarded `schedule` import's ONE home.
WI-280 split of gen_trajectory.py; the facade re-exports, so consumers are
unchanged.

Contracts: IF-082, IF-085, IF-111, IF-132 — the seams this module declares (process.md §8; rows of
record in docs/requirements/interfaces.toml). The first two are the sibling-held halves of
gen_trajectory's own seams: IF-082 is IF-056's derivation-loader read of
check_trajectory, IF-085 is IF-071's frontier read of schedule (whose guarded import
has its ONE home here). IF-132 (WI-455) is the How-SW module source: sw_modules
consumes gen_arch_map.scan_inventory over the declared src root, replacing the
retired parse of docs/architecture.md's committed MODULE MAP block.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

# The sanctioned sibling import (one home for registry loading/validation) —
# plain here: the facade's guarded import is the module family's ONE sys.path
# repair, and it runs before this module is ever imported.
import check_trajectory as ct
from kitlib import stage as _kitstage

# Sibling: the arch-map AST walk — sw_modules' source since WI-455 retired the
# committed docs/architecture.md MODULE MAP block it used to parse back
# (IF-132). Plain import for the same reason as `ct` above.
import gen_arch_map

# schedule.py — the ready-frontier derivation the generated STATUS block projects
# (WI-284): the forward-looking WI list is GENERATED, not hand-authored, so a
# `done` WI can never linger there and redden a later train's DONE gate. OPTIONAL:
# a scaffold that ships gen_trajectory without schedule.py (or a downstream not
# using the scheduler) simply omits the Ready-frontier block — `_frontier_lines`
# degrades to empty rather than crashing the whole generator (the kit's
# "non-adopter pays nothing" posture; a hard import here broke the hook-scaffold
# tests that copy check_trajectory but not schedule).
try:
    import schedule
except ImportError:
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import schedule
    except ImportError:
        schedule = None

# Workstream render order + display labels (the mutable grouping category on a
# work item; legacy `Track` header still read); unknown ones fall through in
# file order.
WORKSTREAM_LABELS = {
    "self-adoption": "Self-adoption",
    "scripts": "Scripts / harness",
    "docs": "Docs / process",
    "unattended": "Unattended layer",
    "deliverable": "Deliverables",
}


# --- spine parsing (ported from the proven gilbert generator, kit columns) -----


def _sn_rows(root):
    """Full stakeholder-need rows (id, need, why, priority, acceptance) from the
    md tables, the `-000` placeholder skipped and the rows id-sorted.

    ONE HOME now: this, gen_okf.sn_rows and trace._sn_prose all
    read `spine_carrier.folded_needs`. They were three copies pinned by a
    docstring saying "change all three together" — and they drifted anyway (one
    kept `-000`, one did not), rendering a phantom SN-000 root in the icicle."""
    return spine_carrier.folded_needs(root / "docs/requirements/stakeholder-needs.toml")


def read_sns(root):
    """(id, short-label) per stakeholder need — the SN count + icicle roots."""
    return [(r["id"], r["need"]) for r in _sn_rows(root)]


def _spine(root, skip_example=False):
    """`(srs, llrs, tcs)` — the SR/LLR/TC registry rows, id-prefix-filtered.

    The three readers of the spine (the What icicle, the maturity numbers, the
    Drafted/drifted pointer lines) each re-derived the same
    `read_rows(...) if id.startswith(...)` triple; the census charged the eight
    resulting blocks to WI-346 as `spine-load-repeat`. Explicitly NOT the F5
    case: F5 buys cross-SCRIPT copy-ability (a shared `_kitcommon.py` was
    rejected 2026-07-12) and every copy was inside this one file, so a
    module-local loader costs nothing and no independence is spent.

    ROW ORDER IS THE CONTRACT: rows come back exactly as `ct.read_rows` yields
    them — no sort, no set, no dict round-trip. The icicle picks a *primary*
    parent as the first listed ref and lays blocks out in arrival order, and
    `--check` byte-compares the rendered result, so a reordering here is a
    silent artifact change.

    `skip_example=True` additionally drops the `-000` placeholder rows a
    freshly copied template carries. That is the pending projection's rule — an
    example row owes no approval — stated once in the loader rather than
    re-derived at the call site. The default keeps them, because the icicle and
    the maturity counts render whatever the registry holds."""

    def rows(rel, col, prefix):
        out = []
        # Through the CARRIER, not ct.read_rows: these are spine
        # tiers, and a CSV parse of a TOML file yields NOTHING rather than
        # failing — the icicle would render an empty spine and --check would
        # happily byte-compare two empty renders.
        for r in spine_carrier.load(root / rel, col):
            rid = r.get(col) or ""
            if not rid.startswith(prefix):
                continue
            if skip_example and rid.endswith("-000"):
                continue
            out.append(r)
        return out

    return (
        rows(ct.SR_CSV, "SR-ID", "SR-"),
        rows("docs/requirements/low-level-requirements.toml", "LLR-ID", "LLR-"),
        rows("docs/test/test-cases.toml", "TC-ID", "TC-"),
    )


def spine_stats(root):
    """Definition-maturity numbers. 'Definition completeness' = SRs marked
    `Approved` / total SRs — how much of the requirement definition is decomposed
    and blessed, distinct from execution (work items done). The key stays
    `sr_verified` across D-9 step 5's rename: it is a dict key two renderers and
    their tests read, and re-keying a data contract is a separate act from
    renaming a cell value."""
    srs, llrs, tcs = _spine(root)
    sr_total = len(srs)
    sr_verified = sum(
        1 for r in srs if (r.get("Status") or "").strip().lower() == "approved"
    )
    return {
        "sn_total": len(read_sns(root)),
        "sr_total": sr_total,
        "sr_verified": sr_verified,
        "llr_total": len(llrs),
        "tc_total": len(tcs),
        "def_pct": round(100 * sr_verified / sr_total) if sr_total else 0,
    }


def project_vision(root):
    """One-line vision: the README `PROJECT-VISION:` tag (the kit's canonical
    one-home vision), else AGENTS.md's one-line purpose, else a constant."""
    readme = root / "README.md"
    if readme.exists():
        m = re.search(
            r"\*\*PROJECT-VISION:\*\*\s*(.+?)\n\s*\n",
            readme.read_text(encoding="utf-8"),
            re.S,
        )
        if m:
            return re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", m.group(1))).strip()
    agents = root / "AGENTS.md"
    if agents.exists():
        m = re.search(
            r"one-line purpose:\*\*\s*(.+?)(?:\n\s*-|\n\n)",
            agents.read_text(encoding="utf-8"),
            re.S,
        )
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".")
    return "A requirement-traced project built with agents and humans."


def project_name(root):
    """The project's display name — the README's first H1, else the folder name."""
    readme = root / "README.md"
    if readme.exists():
        for line in readme.read_text(encoding="utf-8").splitlines():
            m = re.match(r"#\s+(.+)", line.strip())
            if m:
                return m.group(1).strip()
    return root.resolve().name or "Project"


def _run_captured(argv):
    """`subprocess.run(argv)` under this module's ONE capture contract.

    The five keywords: utf-8 with `errors="replace"` so a child emitting a
    single locale-undecodable byte mojibakes rather than crashing a render, and
    `stdin=DEVNULL` so a git that would prompt on a TTY takes its default
    instead of hanging an unattended run. WI-304 extracted exactly this block in
    `agent_dispatch` as `_run_captured` rather than sanctioning it; the census
    charged the two sites left here (`_asof`, `_git`) to WI-346 as
    `subprocess-capture`.

    Deliberately does NOT catch: `OSError` (no git binary at all) propagates,
    and both callers catch it to degrade to empty. That is the off-git
    best-effort contract — a non-repo pays nothing, but the helper does not
    silently swallow a failure a future caller might need to see."""
    return subprocess.run(
        argv,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )


def _asof(root):
    """'state as of commit <sha> · <date>' from the last commit touching the
    sources, or '' (no git / no commits). Git-derived, never now() — a wall
    clock would make every regeneration a byte change; this changes only when
    a source-touching commit lands, and --check ignores the line (ASOF_RE)."""
    sources = [
        p
        for p in (
            root / "docs" / "requirements" / "stakeholder-needs.toml",
            root / "docs" / "requirements" / "system-requirements.toml",
            root / "docs" / "requirements" / "low-level-requirements.toml",
            root / "docs" / "requirements" / "work-items.csv",
            # Both work-item homes (Phase 2b): whichever exists is a source of
            # this page, and `git log` over a directory is the same question
            # asked of the folder registry.
            root / "docs" / "work",
            root / "docs" / "test" / "test-cases.toml",
            root / "docs" / "runtime-flows.md",
            # The declared arch-map scan root: since WI-455 the How-SW view
            # reads the source AST directly, so source commits move the stamp.
            root / ct._arch_scan_profile(root)[0].strip().rstrip("/"),
            root / "README.md",
        )
        if p.exists()
    ]
    if not sources:
        return ""
    try:
        proc = _run_captured(
            ["git", "-C", str(root), "log", "-1", "--format=%h · %as", "--"]
            + [str(p) for p in sources]
        )
    except OSError:
        return ""
    stamp = (proc.stdout or "").strip()
    return (
        "state as of commit {}".format(stamp) if proc.returncode == 0 and stamp else ""
    )


def _git(root, *args):
    """`(returncode, stdout)` for a READ-ONLY git command, `(1, "")` on any
    failure — the `_asof` idiom (gen_trajectory shells git via stdlib rather than
    importing the dispatcher, which would drag the whole engine into a renderer).
    Every pending source degrades to empty off-git, so a non-repo pays nothing."""
    try:
        proc = _run_captured(["git", "-C", str(root), *args])
    except OSError:
        return 1, ""
    return proc.returncode, proc.stdout


def sw_modules(root):
    """[(module, summary, [public symbols])] derived straight from the source
    AST under the declared arch-map scan root (`[paths] src` + `[arch-map]
    mode`), via `gen_arch_map.scan_inventory` (IF-132) — the How-SW source.
    Until WI-455 (sitting-2 decision 8) this parsed the committed MODULE MAP
    block back out of `docs/architecture.md`; the registries→dashboard
    re-pointing retired that way-station. Selection is unchanged from the
    old parse: public FUNCTION symbols only (a class row rendered without a
    signature never matched), and a module with no symbol is dropped. Empty
    in files mode (no parser) or under an absent root — the panel is then
    omitted, exactly as it was pre-arch-map."""
    src, mode = ct._arch_scan_profile(root)
    if mode == "files":
        return []
    src_dir = root / src.strip().replace("\\", "/").rstrip("/")
    mods = []
    for rel, summary, _imports, _contracts, rows in gen_arch_map.scan_inventory(
        [src_dir], strict=False
    ):
        symbols = [name for name, sig, _summ, _ids in rows if sig]
        if symbols:
            mods.append({"name": rel, "summary": summary, "symbols": symbols})
    return mods


def runtime_flows(root):
    """`[(title, [mermaid blocks])]` from the authored `docs/runtime-flows.md`
    (the narrative half of the architecture record, WI-455): every heading
    inside the check_flows-checked doc that owns >=1 ```mermaid fence, in file
    order — the dashboard embeds them beside the derived How-SW views so
    PROJECT_STATE.html carries the FULL architecture (sitting-2 decision 8).
    Empty when the doc is absent (a repo not yet at DevStg-Tests pays
    nothing)."""
    doc = root / "docs" / "runtime-flows.md"
    if not doc.exists():
        return []
    flows, title, buf, in_fence = [], None, [], False
    fence = []
    for line in doc.read_text(encoding="utf-8", errors="replace").splitlines():
        if in_fence:
            if line.strip() == "```":
                in_fence = False
                if title is not None:
                    buf.append("\n".join(fence))
            else:
                fence.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            if title is not None and buf:
                flows.append((title, buf))
            title, buf = m.group(2).strip(), []
            continue
        if line.strip().startswith("```mermaid"):
            in_fence, fence = True, []
    if title is not None and buf:
        flows.append((title, buf))
    return flows


def _real_rows(rows, id_col, prefix, sort=True):
    """The registry's REAL rows: right id prefix, `-000` example rows dropped.

    One home for the predicate `cmp_rows` used to state inline — the frame's
    three tiers and the interface tier would otherwise have restated it four
    more times. `sort=False` keeps FILE order, which is what `cmp_rows` (and the
    table it feeds) has always rendered; the frame tiers take id order, since a
    diagram laid out in file order would move whenever a row is inserted."""
    out = []
    for r in rows:
        rid = (r.get(id_col) or "").strip()
        if rid.startswith(prefix) and not rid.endswith("-000"):
            out.append(dict(r, **{id_col: rid}))
    return sorted(out, key=lambda r: r[id_col]) if sort else out


def frame_context(root):
    """The depth-0 FRAME — `docs/requirements/external.toml` — as the read model
    behind the dashboard's System-context view (WI-455, sitting-2 decision 8:
    the boundary record is SATISFIED by the derived view, so the frame is
    generated into the architecture tab and never hand-drawn).

    `None` when the frame declares nothing — a project that never declares a
    boundary simply does not create the file (the registry's own applies-when),
    and the view is then omitted rather than rendered empty (the Knowledge-tab
    vacuity idiom). Otherwise four id-sorted lists:

      `entities`       one per `[entity.EXT-###]`.
      `crossings`      one per `[boundary.B-##]`, each carrying `realized_by` —
                       `(IF-id, in|out)` for every interface row whose
                       directional tie-back names it. DERIVED from
                       `interfaces.toml`, never read off the frame row: the
                       frame is LOCKED and a realization is the other side's
                       claim, which is exactly the split that lets an SR state
                       the crossing while an LLR states which piece provides it.
      `relationships`  one per `[relationship.REL-###]` — external-to-external,
                       the system not a party. No interface vocabulary reaches
                       them here either, deliberately: a relationship is not a
                       crossing.
      `untied`         the interface rows whose endpoint carries the `external:`
                       marker and which tie back to NO crossing, with the reason
                       each row records. Those absences were ADJUDICATED one at a
                       time (WI-455 slice 2) and the reason lives in the row, so
                       the view states them rather than quietly rendering a
                       shorter frame than the registry holds.

    Deterministic (sorted ids, no clocks) so the `--check` freshness byte-compare
    stays stable."""
    req = root / "docs" / "requirements"
    ext = req / "external.toml"
    entities = _real_rows(ct.spine_carrier.load(ext, "EXT-ID"), "EXT-ID", "EXT-")
    crossings = _real_rows(ct.spine_carrier.load(ext, "B-ID"), "B-ID", "B-")
    rels = _real_rows(ct.spine_carrier.load(ext, "REL-ID"), "REL-ID", "REL-")
    if not (entities or crossings or rels):
        return None

    ifs = _real_rows(
        ct.spine_carrier.load(req / "interfaces.toml", "IF-ID"), "IF-ID", "IF-"
    )
    realized, untied = {}, []
    for r in ifs:
        ties = [
            (kind, (r.get(col) or "").strip())
            for col, kind in (
                ("InterfaceFromExternal", "in"),
                ("InterfaceToExternal", "out"),
            )
        ]
        ties = [(kind, bid) for kind, bid in ties if bid]
        for kind, bid in ties:
            realized.setdefault(bid, []).append((r["IF-ID"], kind))
        if ties:
            continue
        endpoint = next(
            (
                cell
                for cell in (
                    (r.get("ThisProject") or "").strip(),
                    (r.get("Counterpart") or "").strip(),
                )
                if cell.startswith("external:")
            ),
            "",
        )
        if endpoint:
            untied.append(
                {
                    "id": r["IF-ID"],
                    "endpoint": endpoint,
                    "reason": (r.get("Notes") or "").strip(),
                }
            )

    names = {e["EXT-ID"]: (e.get("Name") or "").strip() for e in entities}

    def cell(row, key):
        return (row.get(key) or "").strip()

    return {
        "entities": [
            {
                "id": e["EXT-ID"],
                "name": cell(e, "Name"),
                "class": cell(e, "Class"),
                "description": cell(e, "Description"),
                "status": cell(e, "Status"),
            }
            for e in entities
        ],
        "crossings": [
            {
                "id": b["B-ID"],
                "entity": cell(b, "Entity"),
                "entity_name": names.get(cell(b, "Entity"), ""),
                "direction": cell(b, "Direction"),
                "carries": cell(b, "Carries"),
                "status": cell(b, "Status"),
                "realized_by": sorted(realized.get(b["B-ID"], [])),
            }
            for b in crossings
        ],
        "relationships": [
            {
                "id": r["REL-ID"],
                "from": cell(r, "From"),
                "to": cell(r, "To"),
                "from_name": names.get(cell(r, "From"), ""),
                "to_name": names.get(cell(r, "To"), ""),
                "kind": cell(r, "Kind"),
                "flow": cell(r, "Flow"),
                "status": cell(r, "Status"),
            }
            for r in rels
        ],
        "untied": sorted(untied, key=lambda u: u["id"]),
    }


def cmp_rows(root):
    """Real CMP-### component rows (the optional physical/component layer)."""
    rows = ct.spine_carrier.load(
        root / "docs" / "requirements" / "components.toml", "CMP-ID"
    )
    return _real_rows(rows, "CMP-ID", "CMP-", sort=False)


# --- the Knowledge tab: the committed OKF bundle as a concept graph (WI-070) ----
#
# The dashboard becomes docs/okf's *first real consumer* (the 2026-07-11 OKF
# audit found the bundle had none). A view of a view: gen_okf.py emits the
# bundle from the spine, this reads it back and renders it. The small
# frontmatter/link loader below is DUPLICATED here rather than imported from
# gen_okf per the F5 small-loader rule — the sanctioned sibling import is
# reserved for the large evolving check_trajectory graph core, not for a stable
# parser a downstream cherry-pick would drag a second module in for.
OKF_DIR = "docs/okf"

# Tier precedence orients every link upstream -> downstream, so the concept
# graph is a DAG the WI-DAG layouter can rank (SN -> SR -> LLR -> TC). Interfaces
# and process guides carry no spine links in the bundle, so their rank is
# immaterial — they render as isolated rank-0 nodes (an honest picture of what
# the bundle actually links).
OKF_TIER_ORDER = {
    "stakeholder-needs": 0,
    "system-requirements": 1,
    "low-level-requirements": 2,
    "test-cases": 3,
    "interfaces": 4,
    "process-guides": 5,
}


def _okf_frontmatter(text):
    """Parse an OKF concept file's frontmatter — the subset gen_okf emits, whose
    scalars are JSON strings (valid YAML). Returns {type,title,description,
    resource} present, or None when the block is missing/unterminated so the
    caller skips the file with a warn rather than crashing the dashboard."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    fm = {}
    for ln in lines[1:]:
        if ln.strip() == "---":
            return fm
        m = re.match(r"(\w+):\s*(.*)$", ln)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if key in ("type", "title", "description", "resource"):
            try:
                fm[key] = json.loads(val)  # JSONDecodeError is a ValueError
            except ValueError:
                fm[key] = val.strip('"')
    return None  # no closing fence -> malformed


def _okf_nodes(root):
    """Walk docs/okf/<tier>/*.md -> (nodes, sorted-edges), or ({}, []) with no
    bundle. Nodes are frontmatter-typed; edges are the SN->SR->LLR->TC spine
    links parsed from the '- Label: [id](href)' lists, oriented upstream->
    downstream by tier. index.md / UPSTREAM.md are not concepts; the GENERATED
    banner (a '>' blockquote, never a '- ' list line) is never read as content;
    a malformed file is skipped with a stderr warn (a hand-broken bundle can
    never crash generation)."""
    base = root / OKF_DIR
    if not base.is_dir():
        return {}, []
    nodes, raw_links = {}, {}
    for tier_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        tier = tier_dir.name
        for f in sorted(tier_dir.glob("*.md")):
            if f.name in ("index.md", "UPSTREAM.md"):
                continue
            cid = f.stem
            try:
                text = f.read_text(encoding="utf-8")
                fm = _okf_frontmatter(text)
            except OSError:
                fm, text = None, ""
            if not fm or not fm.get("type"):
                print(
                    "gen_trajectory: skipping malformed OKF concept {} (no "
                    "frontmatter/type).".format(f.relative_to(root).as_posix()),
                    file=sys.stderr,
                )
                continue
            nodes[cid] = {
                "type": fm.get("type", ""),
                "title": fm.get("title", ""),
                "description": fm.get("description", ""),
                "resource": fm.get("resource", ""),
                "tier": tier,
                "href": "{}/{}/{}.md".format(OKF_DIR, tier, cid),
            }
            targets = set()
            for ln in text.split("\n"):
                if ln.lstrip().startswith("- "):  # a link-list line only
                    for m in re.finditer(r"\[([^\]]+)\]\(", ln):
                        targets.add(m.group(1).strip())
            raw_links[cid] = targets
    edges = set()
    for cid, targets in raw_links.items():
        a = OKF_TIER_ORDER.get(nodes[cid]["tier"], 99)
        for tid in targets:
            if tid == cid or tid not in nodes:  # self / non-concept text -> drop
                continue
            b = OKF_TIER_ORDER.get(nodes[tid]["tier"], 99)
            if a < b:
                edges.add((cid, tid))
            elif b < a:
                edges.add((tid, cid))
    return nodes, sorted(edges)


PROCESS_STAGE_FILE = _kitstage.STAGE_FILE


def _stage_value(root):
    """The repo's effective stage from `docs/stage`, or None when the file is
    absent or carries no readable record. None is the Process tab's omit
    condition: no stage layer, no method view.

    READS THE RECORDED FILE, deliberately not through the self-healing reader
    (WI-498 slice 5). The dashboard is itself a generated artifact regenerated at
    the same points `docs/stage` is, and its freshness is gated by
    `trajectory-map`; rendering the COMMITTED record keeps the page and the file
    it cites describing one commit. A render leaf that derived fresh would print
    a value the file beside it does not carry, which for a display is the worse
    failure — and it would spawn the derivation to draw a page.

    The duplicated "first non-comment line" parse this replaces is gone with the
    positional file: `kitlib.stage.parse` addresses the field BY NAME, so a
    reordered record cannot silently hand a display the wrong value."""
    path = root / PROCESS_STAGE_FILE
    if not path.exists():
        return None
    try:
        record = _kitstage.parse(path.read_text(encoding="utf-8", errors="replace"))
    except ValueError:  # a hand-edited or cross-ladder value: omit the layer
        return None
    return record.get("stage") if record else None


def _process_doc(root, scaffolded, master):
    """The process-doc link target that resolves in THIS repo: the scaffolded
    docs/ copy when present (the downstream case), else the kit master (the
    meta-repo case, which never scaffolds docs/process.md), else the scaffolded
    default (what bootstrap writes). File presence only — deterministic."""
    for rel in (scaffolded, master):
        if (root / rel).exists():
            return rel
    return scaffolded
