#!/usr/bin/env python3
"""Generate the offline project-state dashboard (root `PROJECT_STATE.html`).

A *view*, never a source of truth (the `gen_arch_map.py` / `trace.py` idiom): it
only renders `docs/requirements/work-items.csv` + the `SN->SR->LLR->TC` spine +
the committed code map. The registry loading and validation are **reused from
`check_trajectory.py`** (one home for the rules); this script adds the rendering.
One self-contained HTML file — a vision header, a git-derived **as-of stamp**
visible on open (never `now()`; excluded from the freshness compare, see
ASOF_RE), definition + execution %-meters, and the model's views (WI-039, the
ratified AXES artifact spec — formerly `docs/trajectory.html`):

  1. **What** — an SVG *icicle* of the SN->SR->LLR->TC spine (block height
     leaf-proportional; hover highlights a subtree, click reads the full text).
     Plain SVG generated here — no library.
  2. **When** — the WI dependency DAG as a **layered SVG** computed in Python
     (topological rank -> crossing-reduced ordering -> coordinates -> SVG),
     done/active/queued shading, hover/click detail. **No CDN / no JS layout
     library** — the kit's offline-render principle (Thread 52 ruling A).
  3. **How (SW)** — the module map parsed from `docs/architecture.md`'s
     generated block (a view of the committed code-map artifact; omitted when
     there is no symbol inventory, e.g. files-mode).
  4. **How (physical)** — the `CMP-###` component table when the optional
     component layer carries real rows (the graph rendering is deferred-on-need
     per the AXES ratification); omitted otherwise.
  5. **Knowledge** — the committed `docs/okf/` OKF bundle as a typed concept
     graph (the dashboard is the bundle's first real *consumer*, WI-070): nodes
     fill-keyed by OKF `type`, directed spine edges from the link lists, laid out
     by the same Python layouter; the detail panel embeds each concept's
     description and links out to its `docs/okf/<tier>/<id>.md` for the full body
     (the middle-path embedding). Omitted when there is no bundle, so a
     bundle-less repo renders byte-identically to before this view existed.
  6. **Process** — the method reference (WI-085): *how this project is built* —
     the artifact lifecycle x gates flow (live tier counts from the spine, the
     current derived gate highlighted from `docs/gate`), the agent-resume loop,
     the slice -> phase -> gate-bar cadence, and (WI-142/SR-055) the two circular working loops —
     intake and human-decision — sharing one LLM_Agent entry. Data-derived where
     a canonical source exists; links out to the process docs and the canonical
     working surfaces. Omitted when there is no `docs/gate`, so a gate-less repo
     renders byte-identically.

Deterministic by construction (sorted inputs, fixed layout passes, no clocks;
the as-of stamp derives from the last source-touching *commit*), so the
`--check` freshness gate is byte-stable — like `gen_arch_map.py --check`.

Stdlib only. Usage:  python scripts/gen_trajectory.py [--root .] [--check] [--status]
  (default)  regenerate PROJECT_STATE.html when the sources changed.
  --check    validate + verify freshness without writing; nonzero exit if the
             registry is invalid or the committed HTML is stale.
  --status   splice the derived-facts snapshot (spine + derived gate + open-items
             one-liners) into docs/status.md's `<!-- BEGIN GENERATED STATUS -->`
             block (WI-202) AND the durable pending-owner-actions projection into
             docs/open-items.md's `<!-- BEGIN GENERATED PENDING -->` block
             (WI-234); with --check, byte-compare BOTH for freshness — the
             successor invariant to the WI-200 forward-only token guard. Vacuous
             (exit 0) per file when it is absent or has no marker pair.
An absent or placeholder-only registry renders nothing and passes vacuously (the
opt-out layer stays free for a repo that never adopts it).
Exit codes: 0 clean / vacuous / opted-out, 1 invalid registry or stale HTML.

Contracts: IF-011, IF-024, IF-052, IF-056 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import html
import json
import re
import string
import subprocess
import sys
from pathlib import Path

# Single source of truth for loading + validating the WI registry (Phase 1):
# importing the sibling — rather than duplicating its ~200-line graph core —
# keeps the `trajectory` gate step and this renderer from ever disagreeing on
# what a valid registry is. This is the kit's ONE sanctioned sibling import,
# allowed *because* the two scripts always ship and re-sync together (bootstrap
# MAPPING); a small, stable helper is still inlined rather than imported (the
# bootstrap.py precedent). Run as a script/subprocess, the sibling resolves via
# sys.path[0] (this file's own directory); loaded another way — an in-process
# test through importlib, a downstream tool importing the module — that entry is
# absent, so fall back to adding this file's directory explicitly.
try:
    import check_trajectory as ct
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_trajectory as ct

# The unified project-state artifact at the repo ROOT (WI-039, the ratified
# AXES spec): what was docs/trajectory.html, plus the How-SW view and the
# git-derived as-of stamp. One self-contained file, all diagrams inside.
OUT_HTML = "PROJECT_STATE.html"

# The one line the --check byte-compare ignores: the as-of stamp derives from
# the last commit touching the sources, so the artifact committed alongside a
# source edit is legitimately one commit behind on that line alone — gating on
# it would force a follow-up regen commit after every source commit. Content
# freshness stays byte-exact; the stamp is informational.
ASOF_RE = re.compile(r'<p class="asof">.*?</p>', re.S)

# --- the docs/status.md derived-snapshot block (WI-202) ------------------------
# `--status` splices a GENERATED block into the OTHERWISE hand-authored status.md
# carrying ONLY derived facts (the spine + derived gate + the open-items
# one-liners), the gen_arch_map-into-architecture.md block-splice idiom. Its
# `--check` is the freshness successor to the WI-200 forward-only token guard:
# with this marker present, check_trajectory.status_forward_only_findings stands
# its token rule down (the marker is `<!-- BEGIN GENERATED ... -->`, which its
# _STATUS_GENERATED_RE matches) and THIS byte-compare becomes the invariant. The
# forward-only INTENT — Next action, the OI briefs, Scope — stays hand-authored
# OUTSIDE the markers. Opt-in: a status.md without the marker pair is left
# untouched, so `--status --check` passes vacuously downstream.
STATUS_MD = "docs/status.md"
STATUS_BEGIN = "<!-- BEGIN GENERATED STATUS -->"
STATUS_END = "<!-- END GENERATED STATUS -->"
# derive_gate.py's cached `# basis:` line in docs/gate — the fresh, freshness-
# guarded derivation the status snapshot PROJECTS (never recomputes).
_GATE_BASIS_RE = re.compile(r"^#\s*basis:\s*(.+)$", re.M)

# --- the docs/open-items.md GENERATED PENDING projection (WI-234) ---------------
# `--status` also splices a second GENERATED block — at the END of
# docs/open-items.md, below the hand-authored OI briefs (which regeneration
# leaves byte-untouched) — projecting every DURABLE pending-owner action so the
# owner's one review surface never misses a parallel-branch hard stop again. A
# pure projection of durable state ONLY; the out/dispatch journal is a
# rebuildable cache (§11) and is never read here:
#   (a) `blocked` WI rows carrying a BlockRef (the attestation/ratification page)
#       — with the `git show <train>:<path>` read path when the doc lives only
#       on a train branch and not the dev tree (the WI-229 shape);
#   (b) source-conflict records under refs/llm/conflict/* (WI-232): train + paths;
#   (c) quarantined trains — a reservation ref whose metadata is unreadable or
#       whose train branch is missing (the agent_dispatch reconcile quarantine
#       conditions, re-derived from the DURABLE refs, never the journal);
#   (d) the run-state `ask:` line when docs/run-state reads NEEDS-HUMAN.
# One line per pending action with a pointer (never a brief — the depth stays in
# the hand-authored briefs). Its `--check` is the same byte-compare freshness
# gate as the status snapshot, so the harness `status-map` step already catches a
# stale projection. Deterministic (sorted refs, no clocks), so `--check` is
# byte-stable. Opt-in: an open-items.md without the marker pair is left untouched.
OPEN_ITEMS_MD = "docs/open-items.md"
PENDING_BEGIN = "<!-- BEGIN GENERATED PENDING -->"
PENDING_END = "<!-- END GENERATED PENDING -->"
_RESERVATION_NS = "refs/llm/reservations/"
_CONFLICT_NS = "refs/llm/conflict/"
_TRAIN_BRANCH_PREFIX = "llm/train/"
_WI_REF_RE = re.compile(r"^WI-\d+$")

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
    """Full stakeholder-need rows (id, need, why, acceptance) from the md table,
    the `-000` placeholder skipped and the rows id-sorted for determinism.

    Kept byte-for-byte in sync with gen_okf.sn_rows (a small stable helper
    duplicated per the F5 rule, not shared) — the two once drifted (one kept
    `-000`, one didn't), which rendered a phantom SN-000 root in the icicle.
    Change both together."""
    md = root / "docs/requirements/stakeholder-needs.md"
    rows = []
    if not md.exists():
        return rows
    for line in md.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(SN-\d+)\s*\|(.*)", line)
        if not m or m.group(1).endswith("-000"):
            continue
        cells = [re.sub(r"\*\*|`", "", c).strip() for c in m.group(2).split("|")]
        rows.append(
            {
                "id": m.group(1),
                "need": cells[0] if cells else "",
                "why": cells[1] if len(cells) > 1 else "",
                "acceptance": cells[3] if len(cells) > 3 else "",
            }
        )
    return sorted(rows, key=lambda r: r["id"])


def read_sns(root):
    """(id, short-label) per stakeholder need — the SN count + icicle roots."""
    return [(r["id"], r["need"]) for r in _sn_rows(root)]


TIER_FILL = {"sn": "#4338ca", "sr": "#0e7490", "llr": "#64748b", "tc": "#047857"}
TIER_COL = {"sn": 0, "sr": 1, "llr": 2, "tc": 3}
ICICLE_UNIT = 18  # px of height per TC leaf


def arch_icicle(root):
    """SVG icicle (partition) of the SN->SR->LLR->TC spine + (details, descendants).

    Height is leaf-proportional: a TC is one unit, an LLR spans the sum of its
    TCs, an SR the sum of its LLRs, an SN the sum of its SRs — so every column
    totals the same height. Multi-parent refs are simplified to a primary parent
    (first listed) to make a tree; the detail panel still lists every parent.
    Pure SVG — no library."""
    details, tier, kids = {}, {}, {}

    def add(nid, t, title, body, meta="", status=""):
        details[nid] = {
            "tier": t,
            "title": title,
            "body": body,
            "meta": meta,
            "status": status,
        }
        tier[nid] = t
        kids.setdefault(nid, [])

    def link(parent, child):
        kids.setdefault(parent, []).append(child)

    sns = _sn_rows(root)
    sn_ids = {r["id"] for r in sns}
    for r in sns:
        meta = " · ".join(
            p
            for p in (
                "Why: {}".format(r["why"]) if r["why"] else "",
                "Acceptance: {}".format(r["acceptance"]) if r["acceptance"] else "",
            )
            if p
        )
        add(r["id"], "sn", r["need"], r["need"], meta)

    srs = [
        r
        for r in ct.read_rows(root / ct.SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    ]
    sr_ids = {r["SR-ID"].strip() for r in srs}
    for r in srs:
        sid = r["SR-ID"].strip()
        add(
            sid,
            "sr",
            (r.get("Title") or "").strip(),
            (r.get("Requirement") or "").strip(),
            "Acceptance: {}".format((r.get("AcceptanceCriteria") or "").strip()),
            (r.get("Status") or "").strip(),
        )
        parents = [s for s in ct._split_refs(r.get("SN-Refs", "")) if s in sn_ids]
        if parents:
            link(parents[0], sid)

    llrs = [
        r
        for r in ct.read_rows(root / "docs/requirements/low-level-requirements.csv")
        if (r.get("LLR-ID") or "").startswith("LLR-")
    ]
    llr_ids = {r["LLR-ID"].strip() for r in llrs}
    for r in llrs:
        lid = r["LLR-ID"].strip()
        add(
            lid,
            "llr",
            (r.get("Title") or "").strip(),
            (r.get("Detail") or "").strip(),
            "Module: {}".format((r.get("Module") or "").strip()),
            (r.get("Status") or "").strip(),
        )
        parents = [s for s in ct._split_refs(r.get("SR-Refs", "")) if s in sr_ids]
        if parents:
            link(parents[0], lid)

    for r in [
        r
        for r in ct.read_rows(root / "docs/test/test-cases.csv")
        if (r.get("TC-ID") or "").startswith("TC-")
    ]:
        tid = r["TC-ID"].strip()
        add(
            tid,
            "tc",
            "verifies {}".format((r.get("Verifies") or "").strip()),
            (r.get("Expected") or "").strip(),
            "Method: {}".format((r.get("Method") or "").strip()),
            (r.get("Status") or "").strip(),
        )
        vs = ct._split_refs(r.get("Verifies", ""))
        parent = next((v for v in vs if v in llr_ids), None) or next(
            (v for v in vs if v in sr_ids), None
        )
        if parent:
            link(parent, tid)

    # The next three walks (wt/collect/draw) recurse over `kids`, and unlike the
    # work-item DAG this tree's depth is capped at 4 by construction: `link()` is
    # only ever called SN->SR, SR->LLR, LLR->TC, SR->TC (see the tiers above), so
    # no input — pathological or not — can deepen it past the SN->SR->LLR->TC
    # spine. They therefore need no iterative rewrite or depth guard, unlike
    # `_dag_ranks` / `check_trajectory._cycles` which walk the unbounded WI chain.
    # Kept recursive so this block stays a faithful port
    # of the proven gilbert icicle; if that port is ever hardened upstream (for a
    # deeper tree there), mirror it — here it is provably safe.
    weight = {}

    def wt(nid):
        ch = kids.get(nid, [])
        weight[nid] = sum(wt(c) for c in ch) if ch else 1
        return weight[nid]

    roots = [r["id"] for r in sns]
    for s in roots:
        wt(s)

    desc = {}

    def collect(nid):
        out = []
        for c in kids.get(nid, []):
            out.append(c)
            out += collect(c)
        desc[nid] = out
        return out

    for s in roots:
        collect(s)

    cells = []
    col_w, gap = 200, 16

    def draw(nid, y):
        h = weight[nid] * ICICLE_UNIT
        t = tier[nid]
        x = TIER_COL[t] * (col_w + gap)
        cx, cy = x + col_w / 2, y + h / 2
        title = (details[nid]["title"] or "").strip()
        txt = ""
        if h >= 12:
            line1 = '<tspan x="{:.0f}" dy="{}">{}</tspan>'.format(
                cx, -3 if h >= 30 else 0, esc(nid)
            )
            line2 = ""
            if h >= 30 and title:
                short = title if len(title) <= 26 else title[:25] + "…"
                line2 = '<tspan x="{:.0f}" dy="12" class="sub">{}</tspan>'.format(
                    cx, esc(short)
                )
            txt = (
                '<text x="{:.0f}" y="{:.1f}" text-anchor="middle" '
                'dominant-baseline="central">{}{}</text>'.format(cx, cy, line1, line2)
            )
        tip = nid + (" — " + title if title else "")
        cells.append(
            '<g class="cell {}" data-id="{}" tabindex="0">'
            "<title>{}</title>"
            '<rect x="{}" y="{:.1f}" width="{}" height="{:.1f}" rx="3" '
            'fill="{}"></rect>{}</g>'.format(
                t, esc(nid), esc(tip), x, y, col_w, max(h - 1, 1), TIER_FILL[t], txt
            )
        )
        cur = y
        for c in kids.get(nid, []):
            draw(c, cur)
            cur += weight[c] * ICICLE_UNIT

    y = 0.0
    for s in roots:
        draw(s, y)
        y += weight[s] * ICICLE_UNIT

    width = 4 * col_w + 3 * gap
    heads = "".join(
        '<text class="lane-head" x="{:.0f}" y="-8" text-anchor="middle">{}</text>'.format(
            TIER_COL[t] * (col_w + gap) + col_w / 2, t.upper()
        )
        for t in ("sn", "sr", "llr", "tc")
    )
    svg = (
        '<svg viewBox="0 -22 {} {:.0f}" width="{}" '
        'preserveAspectRatio="xMinYMin meet" role="img">{}{}</svg>'.format(
            width, y + 22, width, heads, "".join(cells)
        )
    )
    return svg, details, desc


def spine_stats(root):
    """Definition-maturity numbers. 'Definition completeness' = SRs marked
    Verified / total SRs — how much of the requirement definition is decomposed
    and confirmed, distinct from execution (work items done)."""
    srs = [
        r
        for r in ct.read_rows(root / ct.SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    ]
    llrs = [
        r
        for r in ct.read_rows(root / "docs/requirements/low-level-requirements.csv")
        if (r.get("LLR-ID") or "").startswith("LLR-")
    ]
    tcs = [
        r
        for r in ct.read_rows(root / "docs/test/test-cases.csv")
        if (r.get("TC-ID") or "").startswith("TC-")
    ]
    sr_total = len(srs)
    sr_verified = sum(
        1 for r in srs if (r.get("Status") or "").strip().lower() == "verified"
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


# --- the layered work-item DAG, computed in Python (Thread 52 ruling A) ---------

DAG_COL_W = 172  # node width
DAG_COL_GAP = 60  # horizontal gap between dependency ranks
DAG_ROW_H = 46  # node height
DAG_ROW_GAP = 22  # vertical gap between nodes in a rank
DAG_PAD = 18
STATUS_FILL = {"done": "#047857", "active": "#b45309", "queued": "#94a3b8"}
# A3 (no-info-by-color-alone): a redundant, shape-distinct status glyph paired with
# every status fill — the meaning survives without colour perception. Prefixed to a
# drill work-item block's label (and named in its hover title / detail).
STATUS_GLYPH = {"done": "✓", "active": "●", "queued": "○"}


def _dag_ranks(wis, pred_map):
    """Longest-path layering: a node's rank is one past its deepest predecessor
    (a source is rank 0). The graph is validated acyclic before we get here.

    Iterative post-order (explicit stack), not recursion: a deep dependency chain
    would blow CPython's ~1000-frame limit and raise ``RecursionError`` instead of
    a rendered dashboard. ``on_path`` tracks the nodes on
    the current DFS branch; in a DAG no predecessor is ever on the path, so the
    guard is inert for valid input, and a stray back-edge (a cycle that slipped
    past validation) degrades to no constraint rather than spinning — the same
    belt-and-suspenders the former recursion's placeholder gave, but termination
    is now guaranteed on *any* input."""
    rank, on_path = {}, set()
    for w in wis:
        if w["id"] in rank:
            continue
        stack = [w["id"]]
        while stack:
            n = stack[-1]
            if n in rank:
                on_path.discard(n)
                stack.pop()
                continue
            on_path.add(n)
            pending = [p for p in pred_map[n] if p not in rank and p not in on_path]
            if pending:
                stack.extend(pending)
            else:
                ready = [rank[p] for p in pred_map[n] if p in rank]
                rank[n] = 1 + max(ready, default=-1)
                on_path.discard(n)
                stack.pop()
    return rank


def _reorder(order, r, neigh_map, adj_layer):
    """Sort layer `r` by the barycentre (mean index) of each node's neighbours in
    the adjacent layer; a node with no neighbour there keeps its current index.
    Stable and id-tie-broken, so the sweep is deterministic."""
    pos = {n: i for i, n in enumerate(adj_layer)}
    cur_pos = {n: i for i, n in enumerate(order[r])}

    def bary(n):
        ns = [pos[m] for m in neigh_map[n] if m in pos]
        return sum(ns) / len(ns) if ns else cur_pos[n]

    order[r] = sorted(order[r], key=lambda n: (bary(n), n))


def _layered_layout(node_list, pred_map, succ_map, seed_key, geometry):
    """The shared Sugiyama-lite pipeline behind every layered view (the WI DAG,
    the How-SW seam graph, the OKF knowledge graph — each once carried its own
    copy of this block; deduplicated by the 2026-07-12 review, H3).

    Stages (deterministic): rank by longest path over `pred_map`
    (`_dag_ranks`); seed each rank's order by `seed_key`; run a fixed number of
    barycentre sweeps (down then up, `_reorder`) to reduce edge crossings;
    assign coordinates, centring each rank vertically against the tallest one.
    `geometry` is (col_w, col_gap, row_h, row_gap, pad). Returns
    (positions, width, height)."""
    col_w, col_gap, row_h, row_gap, pad = geometry
    ids = [n["id"] for n in node_list]
    rank = _dag_ranks(node_list, pred_map)
    nranks = (max(rank.values()) + 1) if rank else 0
    order = {}
    for r in range(nranks):
        order[r] = sorted((nid for nid in ids if rank[nid] == r), key=seed_key)
    for _ in range(4):
        for r in range(1, nranks):
            _reorder(order, r, pred_map, order[r - 1])
        for r in range(nranks - 2, -1, -1):
            _reorder(order, r, succ_map, order[r + 1])

    max_rows = max((len(order[r]) for r in order), default=0)
    content_h = max_rows * row_h + max(max_rows - 1, 0) * row_gap
    pos = {}
    for r in range(nranks):
        layer = order[r]
        n = len(layer)
        layer_h = n * row_h + max(n - 1, 0) * row_gap
        y0 = pad + (content_h - layer_h) / 2
        x = pad + r * (col_w + col_gap)
        for i, nid in enumerate(layer):
            pos[nid] = (x, y0 + i * (row_h + row_gap))
    width = pad * 2 + nranks * col_w + max(nranks - 1, 0) * col_gap
    height = pad * 2 + content_h
    return pos, width, height


def _dag_layout(wis):
    """(positions, width, height) for the work items: the shared layered
    pipeline, with hard edges only (soft edges are advisory — they never
    constrain rank) and each rank's order seeded by (workstream, id) to keep
    workstreams clustered."""
    ids = {w["id"] for w in wis}
    by_id = {w["id"]: w for w in wis}
    pred_map = {w["id"]: [p for p in w["preds"] if p in ids] for w in wis}
    succ_map = {w["id"]: [] for w in wis}
    for w in wis:
        for p in pred_map[w["id"]]:
            succ_map[p].append(w["id"])
    return _layered_layout(
        wis,
        pred_map,
        succ_map,
        lambda n: (by_id[n]["workstream"], n),
        (DAG_COL_W, DAG_COL_GAP, DAG_ROW_H, DAG_ROW_GAP, DAG_PAD),
    )


def dag_svg(wis):
    """The work-item DAG as one plain SVG string + a details dict for the panel."""
    ids = {w["id"] for w in wis}
    pos, width, height = _dag_layout(wis)

    # Edges first (drawn under the nodes). A hard predecessor sits in a lower
    # rank, so hard edges run left->right; a horizontal control offset softens
    # them. Soft (advisory) edges render dashed and may run backwards — they
    # never constrained the ranking.
    edges = []
    for w in wis:
        for p, cls in [(p, "edge") for p in w["preds"]] + [
            (p, "edge soft") for p in w["soft"]
        ]:
            if p not in ids:
                continue
            x1, y1 = pos[p][0] + DAG_COL_W, pos[p][1] + DAG_ROW_H / 2
            x2, y2 = pos[w["id"]][0], pos[w["id"]][1] + DAG_ROW_H / 2
            dx = max((x2 - x1) * 0.4, 12)
            edges.append(
                '<path class="{}" data-src="{}" data-tgt="{}" '
                'd="M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}" '
                'marker-end="url(#arrow)"></path>'.format(
                    cls, esc(p), esc(w["id"]), x1, y1, x1 + dx, y1, x2 - dx, y2, x2, y2
                )
            )

    nodes, details = [], {}
    for w in wis:
        x, y = pos[w["id"]]
        st = w["status"] if w["status"] in STATUS_FILL else "queued"
        title = w["title"]
        short = title if len(title) <= 22 else title[:21] + "…"
        label = (
            '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
            '<tspan x="{:.1f}" dy="-2" class="wid">{}</tspan>'
            '<tspan x="{:.1f}" dy="13" class="sub">{}</tspan></text>'.format(
                x + DAG_COL_W / 2,
                y + DAG_ROW_H / 2,
                x + DAG_COL_W / 2,
                # A3 (no info by colour alone): the flat fallback pairs its status
                # fill with the same visible glyph the tiered drill uses, so a small
                # (<=3-tier) registry still encodes status by shape, not hue alone.
                "{} {}".format(STATUS_GLYPH[st], esc(w["id"])),
                x + DAG_COL_W / 2,
                esc(short),
            )
        )
        tip = "{} — {} ({})".format(w["id"], title, st)
        nodes.append(
            '<g class="wi {}" data-id="{}" tabindex="0">'
            "<title>{}</title>"
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="7" '
            'fill="{}"></rect>{}</g>'.format(
                st,
                esc(w["id"]),
                esc(tip),
                x,
                y,
                DAG_COL_W,
                DAG_ROW_H,
                STATUS_FILL[st],
                label,
            )
        )
        ws = WORKSTREAM_LABELS.get(w["workstream"], w["workstream"])
        details[w["id"]] = {
            "status": st,
            "title": title,
            "body": "Workstream: {}".format(ws),
            "meta": "Delivers: {} · After: {}".format(
                ", ".join(w["srs"]) or "—",
                ", ".join(w["preds"] + ["~" + p for p in w["soft"]]) or "—",
            ),
        }

    defs = (
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" class="arrowhead"></path></marker></defs>'
    )
    svg = (
        '<svg viewBox="0 0 {:.0f} {:.0f}" width="{:.0f}" '
        'preserveAspectRatio="xMinYMin meet" role="img">{}{}{}</svg>'.format(
            width, height, width, defs, "".join(edges), "".join(nodes)
        )
    )
    return svg, details


# --- the How-SW interface graph (WI-056), reusing the WI-DAG layouter -----------

SW_NODE_FILL = {"module": "#0e7490", "file": "#7c3aed", "external": "#64748b"}
SW_COL_W = 168
SW_COL_GAP = 64
SW_ROW_H = 40
SW_ROW_GAP = 20
SW_PAD = 16


def _sw_node(raw, module_norm):
    """Classify an IF endpoint string into (kind, node-key, display). A module is
    an arch-map inventory member (matched via the normalized name); a file is a
    path-shaped counterpart (a shared-contract hub like docs/stack.ini); anything
    else (downstream adopter / git / agent CLI) is an external actor."""
    norm = ct._norm_module(raw)
    if norm in module_norm:
        return "module", "mod:" + norm, module_norm[norm]
    s = (raw or "").strip()
    if ("/" in s or re.search(r"\.\w{1,5}$", s)) and " " not in s:
        return "file", "file:" + s, s
    return "external", "ext:" + s, s


def sw_graph(root, mods):
    """The How-SW interface graph as one plain SVG string, or None when no IF
    seams are declared (the panel then keeps the bare module table — the organized
    graph is *earned* by declaring seams). Nodes are the arch-map modules plus the
    files / external actors the seams reference; edges are producer->consumer
    IF-### seams labeled by id. Reuses the shared layered pipeline
    (`_layered_layout`), so producers sit left of consumers and crossings are
    reduced. Byte-deterministic: sorted inputs, fixed
    passes, no clocks — the `--check` freshness compare stays stable."""
    ifs = ct.load_ifs(ct.read_rows(root / ct.IF_CSV))
    if not ifs or not mods:
        return None
    module_norm = {ct._norm_module(m["name"]): m["name"] for m in mods}
    nodes, edges = {}, []
    for r in ifs:
        tk, tkey, tdisp = _sw_node(r["this"], module_norm)
        ck, ckey, cdisp = _sw_node(r["counterpart"], module_norm)
        nodes.setdefault(tkey, {"display": tdisp, "kind": tk})
        nodes.setdefault(ckey, {"display": cdisp, "kind": ck})
        # Consumes flips the arrow so it always runs producer -> consumer.
        edges.append((ckey, tkey, r["id"]) if r["direction"] == "consumes"
                     else (tkey, ckey, r["id"]))  # fmt: skip
    if not nodes:
        return None

    node_ids = sorted(nodes)
    node_list = [{"id": k} for k in node_ids]
    pred_map = {k: [] for k in node_ids}
    succ_map = {k: [] for k in node_ids}
    for s, d, _iid in edges:
        pred_map[d].append(s)
        succ_map[s].append(d)
    pos, width, height = _layered_layout(
        node_list,
        pred_map,
        succ_map,
        lambda k: k,
        (SW_COL_W, SW_COL_GAP, SW_ROW_H, SW_ROW_GAP, SW_PAD),
    )

    edge_svg = []
    for s, d, iid in sorted(edges):
        x1, y1 = pos[s][0] + SW_COL_W, pos[s][1] + SW_ROW_H / 2
        x2, y2 = pos[d][0], pos[d][1] + SW_ROW_H / 2
        dx = max((x2 - x1) * 0.4, 12)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        edge_svg.append(
            '<path d="M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}" '
            'fill="none" stroke="#94a3b8" stroke-width="1.3" '
            'marker-end="url(#swarrow)"></path>'
            '<text x="{:.1f}" y="{:.1f}" text-anchor="middle" fill="#64748b" '
            'font-size="9">{}</text>'.format(
                x1, y1, x1 + dx, y1, x2 - dx, y2, x2, y2, mx, my - 2, esc(iid)
            )
        )
    node_svg = []
    for k in node_ids:
        x, y = pos[k]
        info = nodes[k]
        disp = info["display"]
        short = disp if len(disp) <= 22 else disp[:21] + "…"
        tip = "{} ({})".format(disp, info["kind"])
        node_svg.append(
            "<g><title>{}</title>"
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="6" '
            'fill="{}"></rect><text x="{:.1f}" y="{:.1f}" text-anchor="middle" '
            'dominant-baseline="central" fill="#fff" font-size="10">{}</text>'
            "</g>".format(
                esc(tip),
                x,
                y,
                SW_COL_W,
                SW_ROW_H,
                SW_NODE_FILL[info["kind"]],
                x + SW_COL_W / 2,
                y + SW_ROW_H / 2,
                esc(short),
            )  # fmt: skip
        )
    defs = (
        '<defs><marker id="swarrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"></path></marker></defs>'
    )
    return (
        '<svg viewBox="0 0 {:.0f} {:.0f}" width="{:.0f}" '
        'preserveAspectRatio="xMinYMin meet" role="img">{}{}{}</svg>'.format(
            width, height, width, defs, "".join(edge_svg), "".join(node_svg)
        )
    )


# --- the containerized How-SW top view (WI-073/FB5) -----------------------------
#
# The software-architecture diagram's first view must show at most
# ct.TOP_VIEW_MAX items — top-level components (a CMP with no PartOf that contains
# a module) + uncontained modules — so a large module set stays legible. The
# containment derivation is imported from the sibling (`ct.component_top_view`),
# the ONE home for the module→CMP join, so this render and the right-sizing rule
# can never disagree on the count. Rendered as a native `<details>` tree (no JS —
# deterministic, offline, byte-stable through --check); IF seams aggregate to the
# container boundary at the top level (one deduped component-to-component edge per
# crossing pair), and intra-component seams appear only in a component's
# expansion. When no CMP contains a module the caller keeps today's flat panel,
# so a repo without a component layer renders byte-identically.

SW_CMPTREE_STYLE = "<style>#sw .cmptree{margin-top:.4rem;}</style>"


def sw_containment(root, mods):
    """The containerized How-SW top view (WI-073) as a Simulink-style drill (SR-051
    rev, WI-141), or None when no `CMP-###` component contains an arch-map module
    (the caller then keeps today's flat panel, byte-identical). Returns
    `(tab, panel)`.

    The root layer is a block diagram of the top-level components plus the
    uncontained modules; a component block is double-clicked (or Enter/Space) to
    DESCEND one layer into its member modules, nested child components, and the
    seams internal to it, and a breadcrumb returns. IF-### seams wire endpoint block
    OUTPUT ports -> INPUT ports; a seam whose endpoints fall in two different
    top-level items renders once as an aggregated component-to-component wire at the
    top (deduped to the boundary). Deterministic (sorted inputs, no clocks)."""
    view = ct.component_top_view(root)
    if not view["top_roots"]:
        return None

    by_id = view["by_id"]
    children_of = view["children_of"]
    module_cmps = view["module_cmps"]
    module_roots = view["module_roots"]
    inv = view["inventory"]  # {norm: display}

    # A module's DIRECT container(s) = the finest CMP(s) its LLRs tag; a coarser
    # ancestor contains it through PartOf (rendered as the nested drill layers).
    direct = {cid: [] for cid in by_id}
    for norm, tags in module_cmps.items():
        for cid in tags:
            direct[cid].append(norm)
    for cid in direct:
        direct[cid] = sorted(direct[cid])

    def subtree_modules(cid):
        """Every module in `cid` and its PartOf-descendants (cycle-guarded)."""
        seen, frontier, out = set(), [cid], set()
        while frontier:
            n = frontier.pop()
            if n in seen:
                continue
            seen.add(n)
            out.update(direct.get(n, []))
            frontier.extend(children_of.get(n, []))
        return out

    ifs = ct.load_ifs(ct.read_rows(root / ct.IF_CSV))
    counter = [0]
    layers = []
    # U3: a per-block detail record (keyed by the block's `data-node`) so the How-SW
    # drill gets the same click/focus-for-detail aside its sibling When drill has. The
    # module summary comes from the arch-map rows (`mods`), keyed by display name.
    sw_details = {}
    mod_summary = {m["name"]: m.get("summary", "") for m in mods}

    def new_id():
        counter[0] += 1
        return "sw-{}".format(counter[0] - 1)

    def cmp_label(cid):
        nm = by_id.get(cid, {}).get("name", "")
        return "{} — {}".format(cid, nm) if nm else cid

    def cmp_block(cid, child):
        n = len(subtree_modules(cid))
        sw_details["cmp:" + cid] = {
            "kind": "component",
            "title": cmp_label(cid),
            "body": "A CMP-### component: {} module(s) in it and its PartOf parts. "
            "Double-click to descend into its members and internal seams.".format(n),
            "fill": "#475569",  # slate — the neutral container badge (7.58:1 on #fff)
        }
        return {
            "key": "cmp:" + cid,
            "label": cmp_label(cid),
            "sub": "component · {} module(s)".format(n),
            "fill": "var(--surface)",
            "stroke": "var(--border)",
            "tier": "component",
            "descend": child,
            "crumb": cid,
            "title": "{} — {} module(s)".format(cmp_label(cid), n),
        }

    def mod_block(norm):
        disp = inv.get(norm, norm)
        sw_details["mod:" + norm] = {
            "kind": "module",
            "title": disp,
            "body": mod_summary.get(disp) or "A source module in the architecture map.",
            "fill": SW_NODE_FILL["module"],
        }
        return {
            "key": "mod:" + norm,
            "label": disp,
            "sub": "module",
            "fill": SW_NODE_FILL["module"],
            "textfill": "#fff",
            "stroke": "rgba(15,23,42,.15)",
            "tier": "module",
            "title": disp,
        }

    def ext_block(key, disp, kind):
        sw_details[key] = {
            "kind": kind,
            "title": disp,
            "body": "A {} the modules reach across a declared IF-### seam.".format(
                kind
            ),
            "fill": SW_NODE_FILL.get(kind, "#64748b"),
        }
        return {
            "key": key,
            "label": disp,
            "sub": kind,
            "fill": SW_NODE_FILL.get(kind, "#64748b"),
            "textfill": "#fff",
            "stroke": "rgba(15,23,42,.15)",
            "tier": kind,
            "title": "{} ({})".format(disp, kind),
        }

    def layer_edges(block_of, in_scope, allow_boundary):
        """Aggregated seam wires among this layer's blocks + the file/external
        blocks they reach. `block_of(norm)` -> the sibling block key(s) a module
        maps to at this layer (empty when out of this layer's scope); a seam whose
        two module endpoints land in different sibling blocks (or a boundary seam to
        a file/external, when `allow_boundary(norm)`) becomes one deduped wire."""
        agg, externals = {}, {}
        for r in ifs:
            tk, tkey, tdisp = _sw_node(r["this"], inv)
            ck, ckey, cdisp = _sw_node(r["counterpart"], inv)
            if r["direction"] == "consumes":  # flip so producer -> consumer
                (pk, pkey, pd), (nk, nkey, nd) = (ck, ckey, cdisp), (tk, tkey, tdisp)
            else:
                (pk, pkey, pd), (nk, nkey, nd) = (tk, tkey, tdisp), (ck, ckey, cdisp)
            pn = pkey.split(":", 1)[1] if pk == "module" else None
            nn = nkey.split(":", 1)[1] if nk == "module" else None
            if pk == "module" and nk == "module":  # internal / cross seam
                if pn not in in_scope or nn not in in_scope:
                    continue
                pkeys, nkeys = block_of(pn), block_of(nn)
            else:  # boundary seam to a file / external hub
                # exactly one endpoint is the module; the other is the hub. Keep
                # the producer -> consumer orientation (module producer wires OUT to
                # the hub; module consumer takes the hub's OUT into its IN).
                if pk == "module":
                    mnorm, (ekey, edisp, ekind) = pn, (nkey, nd, nk)
                else:
                    mnorm, (ekey, edisp, ekind) = nn, (pkey, pd, pk)
                if mnorm not in in_scope or not allow_boundary(mnorm):
                    continue
                externals[ekey] = (edisp, ekind)
                mkeys = block_of(mnorm)
                pkeys, nkeys = (mkeys, {ekey}) if pk == "module" else ({ekey}, mkeys)
            for a in sorted(pkeys):
                for b in sorted(nkeys):
                    if a != b:
                        agg.setdefault((a, b), set()).add(r["id"])
        edges = [(a, b, ", ".join(sorted(ids))) for (a, b), ids in sorted(agg.items())]
        return edges, externals

    def emit_cmp_layer(cid):
        lid = new_id()
        sub = subtree_modules(cid)
        child_cmps = [c for c in children_of.get(cid, []) if subtree_modules(c)]
        dmods = direct.get(cid, [])

        def block_of(norm):
            if norm in dmods:
                return {"mod:" + norm}
            return {"cmp:" + c for c in child_cmps if norm in subtree_modules(c)}

        edges, externals = layer_edges(block_of, sub, lambda n: True)
        blocks = [cmp_block(c, emit_cmp_layer(c)) for c in child_cmps]
        blocks += [mod_block(m) for m in dmods]
        blocks += [ext_block(k, d, kind) for k, (d, kind) in sorted(externals.items())]
        layers.append((lid, _drill_layer_svg(blocks, edges)))
        return lid

    # Root layer: top-level component blocks + uncontained module blocks, wired by
    # the cross-component seams (a contained module's boundary seams live one layer
    # in; an uncontained module's boundary seam has nowhere deeper, so it shows here).
    def root_block_of(norm):
        roots = module_roots.get(norm) or set()
        if roots:
            return {"cmp:" + r for r in roots}
        return {"mod:" + norm} if norm in inv else set()

    root_id = new_id()
    root_edges, root_ext = layer_edges(
        root_block_of, set(inv), lambda n: not module_roots.get(n)
    )
    root_blocks = [cmp_block(r, emit_cmp_layer(r)) for r in view["top_roots"]]
    root_blocks += [mod_block(n) for n in view["uncontained"]]
    root_blocks += [ext_block(k, d, kind) for k, (d, kind) in sorted(root_ext.items())]
    layers.append((root_id, _drill_layer_svg(root_blocks, root_edges)))

    tab = '<button data-tab="sw">How (SW architecture)</button>'
    summary_line = (
        '<p class="cap"><strong>Top view: {} item(s)</strong> — {} top-level '
        "component(s) + {} uncontained module(s); bounded at {} "
        '(process-options.md "Component layer"). Software items are '
        "<strong>containerized</strong>; <strong>double-click</strong> a component "
        "— or focus it and press Enter — to <strong>descend</strong> into its "
        "members and internal seams, and the breadcrumb returns.</p>".format(
            view["count"],
            len(view["top_roots"]),
            len(view["uncontained"]),
            ct.TOP_VIEW_MAX,
        )
    )
    # U3: node-kind legend (the fills were "explained nowhere" in the How tab) —
    # built from the shared SW_NODE_FILL so it stays in lock-step with the blocks.
    legend = (
        '<span><i style="background:var(--surface);border:1px solid '
        'var(--border)"></i>component</span>'
        '<span><i style="background:{module}"></i>module</span>'
        '<span><i style="background:{file}"></i>file (shared-contract hub)</span>'
        '<span><i style="background:{external}"></i>external actor</span>'.format(
            **SW_NODE_FILL
        )
    )
    # U3: a #sw-detail aside wired click/focus-for-detail, mirroring the When drill.
    # Self-contained (its own embedded data + controller), so a no-CMP repo that never
    # appends this panel stays byte-identical. sort_keys -> byte-deterministic.
    dj = json.dumps(sw_details, ensure_ascii=False, sort_keys=True).replace(
        "</", "<\\/"
    )
    detail_script = (
        "<script>(function(){\n"
        "  const D = " + dj + ";\n"
        "  const sw = document.getElementById('sw'); if(!sw) return;\n"
        "  const box = document.getElementById('sw-detail'); if(!box) return;\n"
        "  const esc = s => { const d=document.createElement('div');"
        " d.textContent = s==null?'':s; return d.innerHTML; };\n"
        "  function show(key){\n"
        "    const d = D[key];\n"
        "    if(!d){ box.innerHTML = '<p class=\"hint\">No detail.</p>'; return; }\n"
        '    box.innerHTML = \'<span class="badge" style="background:\''
        "+(d.fill||'#64748b')+'\">'+esc(d.kind)+'</span>'\n"
        "      + '<h3>'+esc(d.title)+'</h3>'\n"
        "      + '<p class=\"body\">'+esc(d.body)+'</p>';\n"
        "  }\n"
        "  for(const b of sw.querySelectorAll('.block[data-node]')){\n"
        "    const key=b.getAttribute('data-node');\n"
        "    b.addEventListener('click', () => show(key));\n"
        "    b.addEventListener('focus', () => show(key)); }\n"
        "})();</script>"
    )
    panel = (
        '<section id="sw" class="panel">\n<h2>Software architecture (How)</h2>\n'
        + DRILL_STYLE
        + SW_CMPTREE_STYLE
        + "\n"
        + summary_line
        + '<div class="layout">\n'
        + SCROLL_CUE
        + '<div class="view" '
        + _hscroll("Architecture drill, horizontally scrollable")
        + '><div class="cmptree">'
        + _render_drill("sw", root_id, "Architecture", layers)
        + "</div></div>\n"
        + '<aside id="sw-detail" class="detail"><p class="hint">Click a component or '
        "module to read its detail; double-click a component (or focus it and press "
        "Enter) to descend into its members and internal seams.</p></aside>\n"
        + "</div>\n"
        + '<div class="legend">'
        + legend
        + "</div>\n"
        + detail_script
        + "\n</section>"
    )
    return tab, panel


# --- shared When-view rendering helpers ---------------------------------------
def esc(s):
    return html.escape(str(s), quote=True)


# WI-219 (M-04): every horizontal-scroll container gets an explicit, accessible
# affordance so a view wider than the viewport SIGNALS its off-screen content
# instead of silently clipping at 390 px — a narrow-width visual cue (paired with
# the `.scrollcue` media rule) plus focusable/labelled-region attributes (SR-052
# keyboard reachability + accessible name, SR-054 no truncation-without-affordance).
SCROLL_CUE = (
    '<p class="scrollcue" aria-hidden="true">↔ Scroll sideways to see the full view</p>'
)


def _hscroll(label):
    """Attributes making a horizontal-scroll container a keyboard-focusable, named
    region — pair with `SCROLL_CUE` and the `.view`/`.tablescroll` CSS (WI-219)."""
    return 'tabindex="0" role="group" aria-label="{}"'.format(esc(label))


def _wi_st(w):
    """A work item's status clamped to a known fill key."""
    return w["status"] if w["status"] in STATUS_FILL else "queued"


# --- WI-087: phase-aware, count-thresholded tiering over the When view ----------
#
# A phase -> workstream -> work-item hierarchy: a tier collapses into native
# <details> blocks only when its LOCAL group count exceeds 3 (flat at or below —
# the owner's "> 3" rule), the work items are the bottom tier, each WI carries a
# per-phase color accent (the grouping-primary encoding, ruling Q2), and every
# rendered tier draws one deduped parent-to-parent edge per crossing pair,
# aggregated from the union of its members' crossing edges (the FB5 boundary idiom,
# applied per tier). A registry with <= 3 phases AND <= 3 workstreams renders the
# flat SVG DAG (byte-identical) — the tiering is EARNED by scale, so a small
# project stays flat.

# A stable, sorted-order palette for the per-phase accent (grouping-primary
# encoding). Deterministic: the i-th sorted phase label takes the i-th color.
PHASE_ACCENTS = (
    "#9f1239", "#881337", "#701a75", "#86198f",
    "#831843", "#9d174d", "#7f1d1d", "#713f12",
)  # fmt: skip

# --- SR-051 rev (WI-141): the Simulink-style drill renderer --------------------
#
# Shared by the tiered When roadmap and the containerized How-SW view: a tier is a
# diagram of BLOCKS (SVG rectangles) each with an input port (left-middle) and an
# output port (right-middle); the aggregated cross-block edges are WIRES from a
# source block's output port to a target block's input port. A container block
# carries `data-descend` -> a child layer id; double-click (or Enter/Space on a
# focused block) DESCENDS one layer and a breadcrumb restores any ancestor,
# superseding the shipped in-place-<details>-expand render. Self-contained (own
# style + controller, no external fetch) and byte-deterministic (sorted inputs, no
# clocks), so the --check freshness compare stays stable.

DRILL_GEOM = (
    172,
    60,
    46,
    22,
    18,
)  # (col_w, col_gap, row_h, row_gap, pad) — DAG geometry
PORT_R = 4.5

# SR-056 decomposition-render polish. A drill layer's column is RIGHT-SIZED to its
# widest member's content rather than the former uniform DRILL_GEOM width, capped
# at the declared bound MAX_TIER_COL (a named value, not an adjective) — narrower
# columns where content allows, never wider than the bound. Integer/fixed so the
# render stays byte-deterministic. The per-char pixel weights over-estimate the
# real glyph widths so a right-sized column never clips its centred label.
MAX_TIER_COL = DRILL_GEOM[0]  # 172 — the declared upper bound (the former width)
TIER_COL_MIN = 96  # a floor so a short-label block stays a comfortable click target
TIER_COL_PAD = 24  # fixed padding around the widest label (≈12px each side)
_BLAB_CH = 7  # px/char, over-estimates the shared bold node label (`--nlabel`, `.blab`)
_BSUB_CH = 5  # px/char, over-estimates the shared sub-label (`--nsub`, `.bsub`)
CEDGE_LEN = 9  # the containment arrow's shaft length (a horizontal parent→child →)


def _tier_col_width(blocks):
    """The right-sized column width for one drill layer (SR-056): the widest
    member's content — the block label vs. its sub-label, whichever is wider — plus
    a fixed padding, clamped to [TIER_COL_MIN, MAX_TIER_COL]. A content-light layer
    renders narrower than the bound; nothing exceeds it. Deterministic (fixed ints)."""
    content = max(
        (
            max(len(b["label"]) * _BLAB_CH, len(b.get("sub", "")) * _BSUB_CH)
            for b in blocks
        ),
        default=0,
    )
    return max(TIER_COL_MIN, min(MAX_TIER_COL, content + TIER_COL_PAD))


DRILL_STYLE = (
    "<style>"
    "#dag span.ph,#sw span.ph{display:inline-block;width:.55rem;height:.55rem;"
    "border-radius:2px;vertical-align:-1px;margin-right:.4rem;}"
    "#dag .phaselegend,#sw .phaselegend{margin:.3rem 0 .6rem;}"
    ".drill nav.crumbs{display:flex;flex-wrap:wrap;align-items:center;gap:.1rem;"
    "margin:.1rem 0 .6rem;font-size:.85rem;}"
    ".drill nav.crumbs .crumb{appearance:none;background:none;border:none;"
    "cursor:pointer;font:inherit;color:var(--accent);padding:.15rem .35rem;"
    "border-radius:6px;}"
    ".drill nav.crumbs .crumb[aria-current]{color:var(--text);font-weight:600;"
    "cursor:default;}"
    ".drill nav.crumbs .sep{color:var(--muted);}"
    ".drill .layer[hidden]{display:none;}"
    ".drill svg.drillsvg{display:block;font-family:inherit;}"
    ".drill .block[data-descend]{cursor:pointer;}"
    ".drill .block[data-descend] rect{stroke-width:1.5;}"
    ".drill .block:focus{outline:none;}"
    ".drill .block:focus rect{stroke:#b45309;stroke-width:2.5;}"
    # SR-056: the hover/focus highlight persists on the last-hovered block until
    # another takes it (the shared .hl idiom — cf. the icicle/DAG/knowledge views).
    ".drill .block.hl rect{stroke:#b45309;stroke-width:2.5;}"
    ".drill .block .blab{font-size:var(--nlabel);font-weight:700;}"
    ".drill .block .bsub{font-size:var(--nsub);}"
    ".drill .port{fill:var(--surface);stroke:var(--muted);stroke-width:1.2;}"
    ".drill .port.in{stroke:var(--accent);}"
    ".drill .wire{fill:none;stroke:var(--muted);stroke-width:1.5;opacity:.85;}"
    ".drill .warrow{fill:var(--muted);}"
    # SR-056: one horizontal parent→child arrow per containment edge — the accent
    # colour (vs. the muted dependency wire) marks it as a descend/containment edge.
    ".drill .cedge{fill:none;stroke:var(--accent);stroke-width:1.5;}"
    ".drill .cedgehead{fill:var(--accent);}"
    "</style>"
)

# Self-contained controller (no libraries, runs at parse time). Idempotent: it
# wires every `.drill` on the page once (the `data-ready` guard), so including it
# in more than one drill view is harmless.
DRILL_SCRIPT = (
    "<script>(function(){"
    "for(const drill of document.querySelectorAll('.drill:not([data-ready])')){"
    "drill.setAttribute('data-ready','1');"
    "const layers=[...drill.querySelectorAll('.layer')];"
    "const byId={};for(const l of layers)byId[l.getAttribute('data-layer')]=l;"
    "const crumbsEl=drill.querySelector('nav.crumbs');"
    "let trail=[{id:drill.getAttribute('data-root'),"
    "crumb:drill.getAttribute('data-root-crumb')||'Top'}];"
    "function render(){"
    "const cur=trail[trail.length-1].id;"
    "for(const l of layers)l.hidden=(l.getAttribute('data-layer')!==cur);"
    "crumbsEl.innerHTML='';"
    "trail.forEach(function(t,i){"
    "const b=document.createElement('button');b.type='button';b.className='crumb';"
    "b.textContent=t.crumb;"
    "if(i===trail.length-1)b.setAttribute('aria-current','true');"
    "b.onclick=function(){trail=trail.slice(0,i+1);render();};"
    "crumbsEl.appendChild(b);"
    "if(i<trail.length-1){const s=document.createElement('span');s.className='sep';"
    "s.textContent=' \\u203a ';crumbsEl.appendChild(s);}"
    "});}"
    "function descend(el){"
    "const id=el.getAttribute('data-descend');if(!id||!byId[id])return;"
    "if(trail.some(function(t){return t.id===id;}))return;"
    "trail.push({id:id,crumb:el.getAttribute('data-crumb')||id});render();}"
    "for(const el of drill.querySelectorAll('[data-descend]')){"
    "el.addEventListener('dblclick',function(){descend(el);});"
    "el.addEventListener('keydown',function(e){"
    "if(e.key==='Enter'||e.key===' '){e.preventDefault();descend(el);}});}"
    # SR-056: the highlight persists on the last-hovered/focused block (keyed by its
    # data-node id) until another takes it — no mouseleave clear, so no flash-on-exit.
    "let hl=null;"
    "function highlight(el){"
    "if(hl===el)return;"
    "if(hl)hl.classList.remove('hl');"
    "hl=el;el.classList.add('hl');"
    "drill.setAttribute('data-hl',el.getAttribute('data-node')||'');}"
    "for(const el of drill.querySelectorAll('.block')){"
    "el.addEventListener('mouseover',function(){highlight(el);});"
    "el.addEventListener('focus',function(){highlight(el);});}"
    "render();}"
    "})();</script>"
)


def _drill_layer_svg(blocks, edges):
    """One drill layer as a plain SVG block diagram. Each block is a rectangle with
    an input port (left-middle) and an output port (right-middle); each aggregated
    `edges` entry (src_key, tgt_key, title) is a wire from the source block's OUTPUT
    port to the target block's INPUT port (Simulink-style). Blocks lay out left->
    right by the shared layered pipeline over the edge set, so a producer sits left
    of its consumer and crossings are reduced. Byte-deterministic."""
    keys = [b["key"] for b in blocks]
    by_key = {b["key"]: b for b in blocks}
    order = {k: i for i, k in enumerate(sorted(keys))}
    pred_map = {k: [] for k in keys}
    succ_map = {k: [] for k in keys}
    seen = set()
    for a, b, _t in edges:
        if a in by_key and b in by_key and a != b and (a, b) not in seen:
            seen.add((a, b))
            pred_map[b].append(a)
            succ_map[a].append(b)
    col_w = _tier_col_width(blocks)  # SR-056: right-sized, ≤ MAX_TIER_COL
    geom = (col_w,) + DRILL_GEOM[1:]
    pos, width, height = _layered_layout(
        [{"id": k} for k in keys],
        pred_map,
        succ_map,
        lambda k: (order[k], k),
        geom,
    )
    _cw, _cg, row_h, _rg, _pad = geom

    wires = []
    for a, b, title in sorted(edges):
        if a not in pos or b not in pos or a == b:
            continue
        x1, y1 = pos[a][0] + col_w, pos[a][1] + row_h / 2
        x2, y2 = pos[b][0], pos[b][1] + row_h / 2
        dx = max((x2 - x1) * 0.4, 14)
        wires.append(
            '<path class="wire" d="M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} '
            '{:.1f},{:.1f}" marker-end="url(#drillarrow)">{}</path>'.format(
                x1,
                y1,
                x1 + dx,
                y1,
                x2 - dx,
                y2,
                x2,
                y2,
                "<title>{}</title>".format(esc(title)) if title else "",
            )
        )

    nodes = []
    for b in blocks:
        x, y = pos[b["key"]]
        cy = y + row_h / 2
        max_label = max(1, (col_w - TIER_COL_PAD) // _BLAB_CH)
        main_label = b["label"]
        if len(main_label) > max_label:
            main_label = main_label[: max_label - 1] + "…"
        label = (
            '<text x="{:.1f}" y="{:.1f}" text-anchor="middle" fill="{}">'
            '<tspan x="{:.1f}" dy="-2" class="blab">{}</tspan>'
            '<tspan x="{:.1f}" dy="13" class="bsub">{}</tspan></text>'.format(
                x + col_w / 2,
                cy,
                b.get("textfill", "var(--text)"),
                x + col_w / 2,
                esc(main_label),
                x + col_w / 2,
                esc(b["sub"]),
            )
        )
        ports = (
            '<circle class="port in" cx="{:.1f}" cy="{:.1f}" r="{}"></circle>'
            '<circle class="port out" cx="{:.1f}" cy="{:.1f}" r="{}"></circle>'.format(
                x, cy, PORT_R, x + col_w, cy, PORT_R
            )
        )
        attrs = 'class="block {}" data-tier="{}"'.format(
            b.get("cls", ""), esc(b.get("tier", ""))
        )
        cedge = ""
        if b.get("descend"):
            attrs += (
                ' data-descend="{}" data-crumb="{}" tabindex="0" role="button"'
                ' aria-label="{}"'.format(
                    esc(b["descend"]),
                    esc(b.get("crumb", b["label"])),
                    esc("Descend into " + str(b["label"])),
                )
            )
            # SR-056: one horizontal parent→child arrow makes the containment edge
            # explicit (top-right, clear of the centred label), not merely implied.
            ax = x + col_w - CEDGE_LEN - 6
            cedge = (
                '<path class="cedge" d="M{:.1f},{:.1f} h{}" '
                'marker-end="url(#cedgearrow)"><title>contains → descend</title>'
                "</path>".format(ax, y + 9, CEDGE_LEN)
            )
        else:
            # A1 (dashboard-accessibility): a leaf block is interactive too — the
            # page wires click + focus-for-detail to `.block[data-wi]`/`[data-node]`
            # — so it must be keyboard-focusable, matching the descend containers'
            # `tabindex`. Its `<title>` supplies the accessible name (A2).
            attrs += ' tabindex="0"'
        # SR-056: a stable per-block node key so the persistent highlight can be
        # keyed to the last-hovered node (appended last, preserving the existing
        # `data-tier="…" data-descend="…"` adjacency other views assert on).
        attrs += ' data-node="{}"'.format(esc(b["key"]))
        attrs += ' data-label="{}" data-summary="{}"'.format(
            esc(b["label"]), esc(b.get("sub", ""))
        )
        # U4: a leaf work-item block advertises its bare id so the When panel can
        # wire single-click + focus to the detail aside (the sw drill sets no `wi`).
        if b.get("wi"):
            attrs += ' data-wi="{}"'.format(esc(b["wi"]))
        nodes.append(
            "<g {}><title>{}</title>"
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="8" '
            'fill="{}" stroke="{}"></rect>{}{}{}</g>'.format(
                attrs,
                esc(b.get("title", b["label"])),
                x,
                y,
                col_w,
                row_h,
                b.get("fill", "var(--surface)"),
                b.get("stroke", "var(--muted)"),
                ports,
                cedge,
                label,
            )
        )

    defs = (
        '<defs><marker id="drillarrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" class="warrow"></path></marker>'
        '<marker id="cedgearrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto">'
        '<path d="M0,0 L10,5 L0,10 z" class="cedgehead"></path></marker></defs>'
    )
    return (
        '<svg viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" '
        'preserveAspectRatio="xMinYMin meet" role="img" class="drillsvg">'
        "{d}{wi}{no}</svg>".format(
            w=width, h=height, d=defs, wi="".join(wires), no="".join(nodes)
        )
    )


def _render_drill(drill_id, root_id, root_crumb, layers):
    """Assemble a drill view: a breadcrumb nav + one `.layer` per tier layer (the
    root shown, the rest `hidden`), plus the self-contained controller. `layers` is
    an ordered list of (layer_id, svg); each container block inside a layer carries
    `data-descend` -> a child layer id."""
    divs = "".join(
        '<div class="layer" data-layer="{}"{}>{}</div>'.format(
            esc(lid), "" if lid == root_id else " hidden", svg
        )
        for lid, svg in layers
    )
    return (
        '<div class="drill" data-drill="{did}" data-root="{root}" '
        'data-root-crumb="{crumb}">'
        '<nav class="crumbs" aria-label="Breadcrumb"></nav>'
        '<div class="layers">{divs}</div></div>{script}'.format(
            did=esc(drill_id),
            root=esc(root_id),
            crumb=esc(root_crumb),
            divs=divs,
            script=DRILL_SCRIPT,
        )
    )


# The label for an SR whose `Phase` cell is blank — the derived-gate model's
# unnamed default phase (derive_gate prints it `(default)` too). A WI delivering
# such an SR IS phased (the default phase), distinct from a WI that delivers no SR
# at all (`unphased`).
DEFAULT_PHASE = "(default)"


def _wi_phases(root, wis):
    """Each WI id -> its delivery-phase label, derived from the `Phase` column of
    the SRs it delivers (work-items.csv carries no Phase of its own). A delivered
    SR always has a phase — its `Phase` cell, or `(default)` when blank; a WI
    delivering SRs across phases joins them sorted (`(default)+v2`); a WI that
    delivers no SR is `unphased`. Deterministic (sorted, no clocks) so the render
    stays `--check`-stable."""
    sr_phase = {}
    for r in ct.read_rows(root / ct.SR_CSV):
        sid = (r.get("SR-ID") or "").strip()
        if sid.startswith("SR-"):
            sr_phase[sid] = (r.get("Phase") or "").strip() or DEFAULT_PHASE
    out = {}
    for w in wis:
        phs = sorted({sr_phase[s] for s in w["srs"] if s in sr_phase})
        out[w["id"]] = "+".join(phs) if phs else "unphased"
    return out


def when_view(root, wis):
    """The When roadmap as a Simulink-style, count-thresholded drill-down (SR-051
    rev, WI-141): phase ⊃ workstream ⊃ work-item block LAYERS, each tier
    a diagram of blocks whose input/output ports are wired by the aggregated
    cross-tier dependency edges (the deduped union of the child edges). A container
    block is double-clicked — or focused and Enter/Space'd — to DESCEND one layer,
    and the breadcrumb restores any ancestor, superseding the shipped in-place
    `<details>` expand. A phase/workstream tier renders only when its LOCAL group
    count exceeds 3 (flat at or below), and the bottom tier is the work-item blocks.
    A registry with <= 3 phases AND <= 3 workstreams returns None, so the caller
    keeps the flat SVG DAG (byte-identical). Deterministic (sorted inputs,
    no clocks)."""
    phase_of = _wi_phases(root, wis)
    phases = {phase_of[w["id"]] for w in wis}
    workstreams = {w["workstream"] for w in wis}
    if len(phases) <= 3 and len(workstreams) <= 3:
        return None  # no tier to draw -> the caller keeps the flat SVG DAG

    color = {
        p: PHASE_ACCENTS[i % len(PHASE_ACCENTS)] for i, p in enumerate(sorted(phases))
    }
    counter = [0]
    layers = []  # (layer_id, svg), in deterministic DFS order

    def new_id():
        counter[0] += 1
        return "when-{}".format(counter[0] - 1)

    def agg_edges(subset, key_of):
        """One aggregated edge per crossing (key_of[p] != key_of[w]) pair, valued by
        the deduped union of contributing WI edges — so a parent edge is exactly that
        union (the WI-074 boundary idiom). Returns sorted (a, b, title) triples."""
        member = {w["id"] for w in subset}
        agg = {}
        for w in subset:
            kw = key_of[w["id"]]
            for p in w["preds"] + w["soft"]:
                if p in member and key_of[p] != kw:
                    agg.setdefault((key_of[p], kw), set()).add((p, w["id"]))
        return [
            (a, b, ", ".join("{}→{}".format(p, w) for p, w in sorted(e)))
            for (a, b), e in sorted(agg.items())
        ]

    def wi_block(w, key=None):
        st = _wi_st(w)
        t = w["title"]
        return {
            "key": key or w["id"],
            # A3: the status glyph rides in the visible label (so the column width
            # accounts for it), redundant with the fill hue; `wi` carries the bare id
            # for the detail-panel wiring (U4) independent of the decorated label.
            "label": "{} {}".format(STATUS_GLYPH[st], w["id"]),
            "wi": w["id"],
            "sub": t if len(t) <= 20 else t[:19] + "…",
            "fill": STATUS_FILL[st],
            "textfill": "#0f172a" if st == "queued" else "#fff",
            "stroke": "rgba(15,23,42,.15)",
            "tier": "work-item",
            "cls": st,
            # OI-10 fix: surface the delivery Phase in the leaf block's hover title
            # too, so it stays visible when the phase tier is flat (≤3 phases) but a
            # workstream tier drills in (SR-051 "surfaces each work item Phase").
            "title": "{} — {} ({}) · {}".format(w["id"], t, st, phase_of[w["id"]]),
        }

    def wi_layer(members):
        """A leaf layer of work-item blocks wired by their intra-set edges."""
        lid = new_id()
        blocks = [wi_block(w) for w in sorted(members, key=lambda w: w["id"])]
        edges = agg_edges(members, {w["id"]: w["id"] for w in members})
        layers.append((lid, _drill_layer_svg(blocks, edges)))
        return lid

    def build(subset, remaining):
        for i, (name, keyfn) in enumerate(remaining):
            groups = {}
            for w in subset:
                groups.setdefault(keyfn(w), []).append(w)
            if len(groups) <= 3:
                continue  # this tier stays flat -> try the next grouping
            lid = new_id()
            rest = remaining[i + 1 :]
            blocks = []
            for gv in sorted(groups):
                members = groups[gv]
                child = build(members, rest)
                lbl = WORKSTREAM_LABELS.get(gv, gv) if name == "workstream" else gv
                blk = {
                    "key": gv,
                    "label": lbl,
                    "sub": "{} · {} item(s)".format(name, len(members)),
                    "tier": name,
                    "descend": child,
                    "crumb": lbl,
                    "title": "{} {} — {} work item(s)".format(name, lbl, len(members)),
                }
                if name == "phase":
                    blk.update(fill=color[gv], textfill="#fff", stroke=color[gv])
                else:
                    blk.update(fill="var(--surface)", stroke="var(--muted)")
                blocks.append(blk)
            edges = agg_edges(subset, {w["id"]: keyfn(w) for w in subset})
            layers.append((lid, _drill_layer_svg(blocks, edges)))
            return lid
        # No tier crosses its threshold here -> the bottom-tier work-item layer.
        return wi_layer(subset)

    tiers = [
        ("phase", lambda w: phase_of[w["id"]]),
        ("workstream", lambda w: w["workstream"]),
    ]
    root_id = build(wis, tiers)

    legend = "".join(
        '<span class="ph" style="background:{}"></span>{}'.format(color[p], esc(p))
        for p in sorted(phases)
    )
    summary = (
        '<p class="cap"><strong>Tiered roadmap: {} phase(s), {} workstream(s).</strong> '
        "A tier renders as wired blocks only when it holds more than 3 members "
        "(phase ⊃ workstream ⊃ work item). <strong>Double-click</strong> a "
        "block — or focus it and press Enter — to <strong>descend</strong> a layer; "
        "the <strong>breadcrumb</strong> returns. A block’s ports carry the aggregated "
        "dependency edges (the deduped union of its members’ crossing edges).</p>"
        '<div class="legend phaselegend"><strong>Phase accent:</strong>{}</div>'.format(
            len(phases), len(workstreams), legend
        )
    )
    return DRILL_STYLE + summary + _render_drill("when", root_id, "Roadmap", layers)


HTML_TEMPLATE = string.Template("""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$project — Project State</title>
<style>
  :root {
    color-scheme: light dark;
    --bg:#f8fafc; --surface:#ffffff; --border:#e2e8f0; --text:#0f172a;
    --muted:#64748b; --accent:#4f46e5;
    --done:#047857; --active:#b45309; --queued:#94a3b8;
    /* U1: one shared node-label / sub-label type scale across every SVG emitter
       (icicle, drill, knowledge) — no per-emitter font-size overrides. */
    --nlabel:10px; --nsub:8.5px; --small:.85rem; --xsmall:.8rem;
    --shadow:0 1px 3px rgba(15,23,42,.06),0 1px 2px rgba(15,23,42,.04);
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#0b1120; --surface:#0f172a; --border:#1e293b; --text:#e2e8f0;
            --muted:#94a3b8; --accent:#818cf8;
            --shadow:0 1px 3px rgba(0,0,0,.4); }
  }
  * { box-sizing: border-box; }
  body { font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
         margin:0; background:var(--bg); color:var(--text);
         -webkit-font-smoothing:antialiased; }
  .wrap { max-width:1120px; margin-inline:auto; padding:0 1.25rem 3rem; }
  header.top { border-bottom:1px solid var(--border); background:var(--surface);
               position:sticky; top:0; z-index:5; }
  .top-inner { max-width:1120px; margin-inline:auto; padding:.85rem 1.25rem;
               display:flex; align-items:baseline; gap:.6rem; }
  .mark { font-weight:700; letter-spacing:-.02em; font-size:1.05rem; }
  .mark .dot { color:var(--accent); }
  .top-sub { color:var(--muted); font-size:.85rem; }
  .hero { padding:2.25rem 0 1.5rem; }
  .hero h1 { font-size:1.05rem; text-transform:uppercase; letter-spacing:.08em;
             color:var(--muted); margin:0 0 .6rem; font-weight:600; }
  .asof { color:var(--muted); font-size:.85rem; margin:.4rem 0 0; }
  table.swmap { border-collapse:collapse; width:100%; font-size:.9rem; }
  table.swmap th, table.swmap td { text-align:left; padding:.45rem .6rem;
    border-bottom:1px solid var(--border); vertical-align:top; }
  table.swmap .sub { color:var(--muted); font-size:.85em; }
  .vision { font-size:1.4rem; line-height:1.4; font-weight:600;
            letter-spacing:-.02em; margin:0; max-width:60ch; }
  .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
           gap:1rem; margin:1.75rem 0 .5rem; }
  .card { background:var(--surface); border:1px solid var(--border);
          border-radius:12px; padding:1.1rem 1.2rem; box-shadow:var(--shadow); }
  .card .label { font-size:.8rem; text-transform:uppercase; letter-spacing:.05em;
                 color:var(--muted); font-weight:600; }
  .card .big { font-size:2rem; font-weight:700; letter-spacing:-.03em;
               margin:.15rem 0 .1rem; }
  .card .sub { font-size:.85rem; color:var(--muted); }
  .card .sub.nowat { color:var(--active); font-weight:600; margin-top:.2rem; }
  .meter { background:var(--border); border-radius:999px; height:.55rem;
           overflow:hidden; margin-top:.7rem; }
  .meter > span { display:block; height:100%; border-radius:999px; }
  .meter.def > span { background:var(--accent); }
  .meter.exe > span { background:var(--done); }
  .tiles { display:flex; flex-wrap:wrap; gap:.5rem; }
  .tile { flex:1 1 90px; background:var(--surface); border:1px solid var(--border);
          border-radius:10px; padding:.7rem .8rem; text-align:center;
          box-shadow:var(--shadow); }
  .tile b { display:block; font-size:1.4rem; letter-spacing:-.02em; }
  .tile span { font-size:.75rem; color:var(--muted); text-transform:uppercase;
               letter-spacing:.04em; }
  nav.tabs { display:flex; flex-wrap:wrap; gap:.25rem; margin:2rem 0 0; border-bottom:1px solid var(--border); }
  nav.tabs button { appearance:none; background:none; border:none; cursor:pointer;
     font:inherit; font-weight:600; color:var(--muted); padding:.6rem .9rem;
     border-bottom:2px solid transparent; margin-bottom:-1px; }
  nav.tabs button:hover { color:var(--text); }
  nav.tabs button.active { color:var(--accent); border-bottom-color:var(--accent); }
  .panel { display:none; padding-top:1.4rem; }
  .panel.active { display:block; }
  .panel h2 { font-size:1.1rem; margin:0 0 .3rem; letter-spacing:-.01em; }
  .panel p.cap { color:var(--muted); margin:0 0 1rem; max-width:70ch; }
  .layout { display:grid; grid-template-columns:1fr 320px; gap:1rem; }
  .view { overflow:auto; max-height:660px; background:var(--surface);
          border:1px solid var(--border); border-radius:12px; box-shadow:var(--shadow);
          padding:.6rem; }
  .view svg { display:block; font-family:inherit; }
  /* WI-219 (M-04): a view wider than the viewport must SIGNAL its off-screen
     content, never silently clip it at 390 px. Each horizontal-scroll region is a
     keyboard-focusable, labelled region (SR-052 A1/A2) with a visible focus ring,
     and carries a narrow-width scroll cue (SR-054 T4) so nothing reads as
     truncated-without-affordance. */
  .tablescroll { overflow:auto; }
  .view:focus-visible, .tablescroll:focus-visible {
     outline:2px solid var(--accent); outline-offset:2px; }
  .scrollcue { display:none; margin:.1rem 0 .5rem; color:var(--muted);
     font-size:var(--small); font-weight:600; }
  #ice .cell rect { stroke:rgba(255,255,255,.35); stroke-width:.5; cursor:pointer;
        transition:opacity .1s ease; }
  #ice .cell text { fill:#fff; font-size:var(--nlabel); pointer-events:none; }
  #ice .cell .sub { font-size:var(--nsub); }
  #ice .lane-head { fill:var(--muted); font-size:11px; font-weight:700; letter-spacing:.06em; }
  .cell.dim, .wi.dim, .edge.dim { opacity:.15; }
  #ice .cell.hl rect { stroke:#f59e0b; stroke-width:2.5; }
  .cell:focus, .wi:focus { outline:none; }
  #dag .wi rect { stroke:rgba(15,23,42,.15); stroke-width:1; cursor:pointer;
        transition:opacity .1s ease; }
  #dag .wi text { fill:#fff; pointer-events:none; }
  #dag .wi .wid { font-size:var(--nlabel); font-weight:700; }
  #dag .wi .sub { font-size:var(--nsub); }
  #dag .wi.queued text { fill:#0f172a; }
  #dag .wi.hl rect { stroke:#f59e0b; stroke-width:2.5; }
  #dag .edge { fill:none; stroke:var(--border); stroke-width:1.4; }
  #dag .edge.soft { stroke-dasharray:5 4; opacity:.75; }
  #dag .edge.hl { stroke:#f59e0b; stroke-width:2; }
  #dag .arrowhead { fill:var(--border); }
  .detail { background:var(--surface); border:1px solid var(--border);
        border-radius:12px; padding:1rem 1.1rem; box-shadow:var(--shadow);
        overflow-y:auto; max-height:640px; }
  .detail .hint { color:var(--muted); }
  .detail .badge { display:inline-block; font-size:var(--xsmall); font-weight:700;
        text-transform:uppercase; letter-spacing:.05em; padding:.15rem .5rem;
        border-radius:6px; color:#fff; }
  .detail h3 { font-size:.98rem; margin:.55rem 0 .35rem; letter-spacing:-.01em; }
  .detail .status { color:var(--muted); font-size:var(--xsmall); margin:0 0 .5rem; }
  .detail .body { color:var(--text); margin:.2rem 0; }
  .detail .meta { color:var(--muted); font-size:var(--small); margin-top:.6rem;
        border-top:1px solid var(--border); padding-top:.55rem; }
  @media (max-width:760px){ .layout{ grid-template-columns:1fr; }
        .detail{ max-height:none; } .scrollcue{ display:block; } }
  .legend { display:flex; flex-wrap:wrap; gap:1rem; margin-top:.9rem;
            font-size:var(--small); color:var(--muted); }
  .legend i { display:inline-block; width:.8rem; height:.8rem; border-radius:3px;
              vertical-align:-1px; margin-right:.35rem; }
  footer { margin-top:2.5rem; padding-top:1rem; border-top:1px solid var(--border);
           color:var(--muted); font-size:.8rem; }
  code { font-size:.9em; }
</style></head><body>
  <header class="top"><div class="top-inner">
    <span class="mark">$project<span class="dot">.</span></span>
    <span class="top-sub">Project State</span>
  </div></header>

  <div class="wrap">
    <section class="hero">
      <h1>Vision</h1>
      <p class="vision">$vision</p>
      <p class="asof">$asof</p>

      <div class="cards">
        <div class="card">
          <div class="label">Definition completeness</div>
          <div class="big">$def_pct%</div>
          <div class="sub">$sr_verified of $sr_total system requirements verified</div>
          <div class="meter def"><span style="width:$def_pct%"></span></div>
        </div>
        <div class="card">
          <div class="label">Execution</div>
          <div class="big">$wi_pct%</div>
          <div class="sub">$wi_done of $wi_total work items done · $wi_active active</div>
          $wi_active_line
          <div class="meter exe"><span style="width:$wi_pct%"></span></div>
        </div>
      </div>

      <div class="tiles">
        <div class="tile"><b>$sn_total</b><span>SN</span></div>
        <div class="tile"><b>$sr_total</b><span>SR</span></div>
        <div class="tile"><b>$llr_total</b><span>LLR</span></div>
        <div class="tile"><b>$tc_total</b><span>TC</span></div>
        <div class="tile"><b>$wi_total</b><span>Work items</span></div>
        <div class="tile"><b>$workstreams</b><span>Workstreams</span></div>
      </div>
    </section>

    <nav class="tabs">
      <button class="active" data-tab="arch">What (SR breakdown)</button>
      <button data-tab="dag">When (roadmap DAG)</button>
      $extra_tabs
    </nav>

    <section id="arch" class="panel active">
      <h2>Architecture decomposition</h2>
      <p class="cap">The <code>SN→SR→LLR→TC</code> spine as an <strong>icicle</strong>:
      block height is leaf-proportional — a TC is one unit, an LLR spans the sum of
      its TCs, an SR the sum of its LLRs — so every lane totals the same height.
      <strong>Hover</strong> to highlight a block and its children; <strong>click</strong>
      to read its full text. A view — the registries are the source of truth.</p>
      <div class="layout">
        $scroll_cue
        <div id="ice" class="view" tabindex="0" role="group"
             aria-label="Architecture icicle, horizontally scrollable">$arch_svg</div>
        <aside id="arch-detail" class="detail"><p class="hint">Hover to highlight a subtree;
          click a block to read its full text — requirement, acceptance, status.</p></aside>
      </div>
      <div class="legend">
        <span><i style="background:#4338ca"></i>SN</span>
        <span><i style="background:#0e7490"></i>SR</span>
        <span><i style="background:#64748b"></i>LLR</span>
        <span><i style="background:#047857"></i>TC</span>
      </div>
    </section>

    <section id="dag" class="panel">
      <h2>Work-item trajectory</h2>
      <p class="cap">The dependency DAG from <code>docs/requirements/work-items.csv</code>,
      laid out left→right by <strong>dependency rank</strong> (a work item sits one
      column past its deepest hard predecessor). <strong>Solid edges block</strong>
      (hard dependencies); <strong>dashed edges are advisory ordering</strong> (soft,
      <code>~</code>-prefixed — they never gate readiness). Cross-workstream edges are
      the seams. <strong>Hover</strong> a work item to highlight its neighbourhood;
      <strong>click</strong> for its detail. Plain SVG — no libraries, fully
      offline.</p>
      <div class="layout">
        $scroll_cue
        <div id="dag-view" class="view" tabindex="0" role="group"
             aria-label="Work-item trajectory graph, horizontally scrollable">$dag_svg</div>
        <aside id="dag-detail" class="detail"><p class="hint">Click a work item to read its
          detail — workstream, status, the SRs it delivers, its predecessors.</p></aside>
      </div>
      <div class="legend">
        <span><i style="background:var(--done)"></i>done</span>
        <span><i style="background:var(--active)"></i>active — you are here</span>
        <span><i style="background:var(--queued)"></i>queued</span>
      </div>
    </section>

    $extra_panels

    <footer>Generated by <code>scripts/gen_trajectory.py</code> from
      <code>work-items.csv</code> + the <code>SN→SR→LLR→TC</code> spine — a view,
      never a source of truth. Re-run after editing the registry.</footer>
  </div>

  <script>
    const archDetails = $arch_details, archDesc = $arch_desc, wiDetails = $wi_details;
    function esc(s){ const d=document.createElement('div'); d.textContent = s==null?'':s; return d.innerHTML; }

    function renderDetail(box, d, id, tierColor){
      if(!d){ box.innerHTML = '<p class="hint">No detail.</p>'; return; }
      box.innerHTML =
        '<span class="badge" style="background:'+tierColor+';color:'+(tierColor==='#94a3b8'?'#0f172a':'#fff')+'">'+esc(d.tier||d.status)+'</span>'
        + '<h3>'+esc(id)+(d.title?' — '+esc(d.title):'')+'</h3>'
        + (d.status&&d.tier?'<p class="status">'+esc(d.status)+'</p>':'')
        + '<p class="body">'+esc(d.body)+'</p>'
        + (d.meta?'<p class="meta">'+esc(d.meta)+'</p>':'');
    }
    const tierColor = { sn:'#4338ca', sr:'#0e7490', llr:'#64748b', tc:'#047857' };
    const statusColor = { done:'#047857', active:'#b45309', queued:'#94a3b8' };

    // Icicle: hover highlights a block + its descendants; click shows detail.
    const ice = document.getElementById('ice');
    const iceCells = ice ? [...ice.querySelectorAll('.cell')] : [];
    const iceBox = document.getElementById('arch-detail');
    function iceHover(id){
      const fam = new Set([id, ...(archDesc[id]||[])]);
      for(const c of iceCells){
        const cid = c.getAttribute('data-id');
        c.classList.toggle('dim', !fam.has(cid));
        c.classList.toggle('hl', cid===id);
      }
    }
    for(const c of iceCells){
      const id = c.getAttribute('data-id');
      c.addEventListener('mouseover', () => iceHover(id));
      c.addEventListener('click', () => renderDetail(iceBox, archDetails[id], id, tierColor[archDetails[id]?.tier]||'#64748b'));
      c.addEventListener('focus', () => { iceHover(id); renderDetail(iceBox, archDetails[id], id, tierColor[archDetails[id]?.tier]||'#64748b'); });
    }
    if(ice) ice.addEventListener('mouseleave', () => { for(const c of iceCells) c.classList.remove('dim','hl'); });

    // DAG: hover highlights a node, its incident edges and immediate neighbours.
    const dag = document.getElementById('dag');
    const wiNodes = dag ? [...dag.querySelectorAll('.wi')] : [];
    const wiEdges = dag ? [...dag.querySelectorAll('.edge')] : [];
    const dagBox = document.getElementById('dag-detail');
    function dagHover(id){
      const near = new Set([id]);
      for(const e of wiEdges){
        const s = e.getAttribute('data-src'), t = e.getAttribute('data-tgt');
        if(s===id) near.add(t); if(t===id) near.add(s);
      }
      for(const n of wiNodes) n.classList.toggle('dim', !near.has(n.getAttribute('data-id')));
      for(const n of wiNodes) n.classList.toggle('hl', n.getAttribute('data-id')===id);
      for(const e of wiEdges){
        const inc = e.getAttribute('data-src')===id || e.getAttribute('data-tgt')===id;
        e.classList.toggle('dim', !inc); e.classList.toggle('hl', inc);
      }
    }
    function dagClear(){ for(const n of wiNodes) n.classList.remove('dim','hl');
      for(const e of wiEdges) e.classList.remove('dim','hl'); }
    for(const n of wiNodes){
      const id = n.getAttribute('data-id');
      n.addEventListener('mouseover', () => dagHover(id));
      n.addEventListener('click', () => renderDetail(dagBox, wiDetails[id], id, statusColor[wiDetails[id]?.status]||'#94a3b8'));
      n.addEventListener('focus', () => { dagHover(id); renderDetail(dagBox, wiDetails[id], id, statusColor[wiDetails[id]?.status]||'#94a3b8'); });
    }
    if(dag) dag.addEventListener('mouseleave', dagClear);
    // When roadmap (drill render): every block opens the SAME detail aside.
    // on single-click / focus. The `.wi` wiring above serves the small-registry SVG
    // DAG fallback; this serves the tiered drill (its blocks carry `data-wi`, and the
    // drill's own controller keeps dblclick=descend + hover=highlight). One selector
    // matches per render mode, so neither is a dead wiring for the artifact it renders.
    if(dag) for(const b of dag.querySelectorAll('.block[data-wi]')){
      const id = b.getAttribute('data-wi');
      const show = () => renderDetail(dagBox, wiDetails[id], id, statusColor[wiDetails[id]?.status]||'#94a3b8');
      b.addEventListener('click', show);
      b.addEventListener('focus', show);
    }
    if(dag) for(const b of dag.querySelectorAll('.block[data-node]:not([data-wi])')){
      const id=b.getAttribute('data-label'), summary=b.getAttribute('data-summary');
      const show=()=>renderDetail(dagBox,{tier:b.getAttribute('data-tier'),title:id,body:summary},id,'#64748b');
      b.addEventListener('click',show); b.addEventListener('focus',show);
    }

    for (const b of document.querySelectorAll('nav.tabs button'))
      b.onclick = () => {
        for (const x of document.querySelectorAll('nav.tabs button')) x.classList.toggle('active', x===b);
        for (const p of document.querySelectorAll('.panel')) p.classList.toggle('active', p.id===b.dataset.tab);
      };
  </script>
</body></html>
""")


def _asof(root):
    """'state as of commit <sha> · <date>' from the last commit touching the
    sources, or '' (no git / no commits). Git-derived, never now() — a wall
    clock would make every regeneration a byte change; this changes only when
    a source-touching commit lands, and --check ignores the line (ASOF_RE)."""
    sources = [
        p
        for p in (
            root / "docs" / "requirements" / "stakeholder-needs.md",
            root / "docs" / "requirements" / "system-requirements.csv",
            root / "docs" / "requirements" / "low-level-requirements.csv",
            root / "docs" / "requirements" / "work-items.csv",
            root / "docs" / "test" / "test-cases.csv",
            root / "docs" / "architecture.md",
            root / "README.md",
        )
        if p.exists()
    ]
    if not sources:
        return ""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "log", "-1", "--format=%h · %as", "--"]
            + [str(p) for p in sources],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
        )
    except OSError:
        return ""
    stamp = (proc.stdout or "").strip()
    return (
        "state as of commit {}".format(stamp) if proc.returncode == 0 and stamp else ""
    )


def sw_modules(root):
    """[(module, summary, [public symbols])] parsed from architecture.md's
    GENERATED MODULE MAP block — the committed arch-map artifact is the
    How-SW source (a view of a view; no AST re-parse). Empty on a files-mode
    map or a missing doc, and the panel is then omitted."""
    md = root / "docs" / "architecture.md"
    mods, current, inside = [], None, False
    if not md.exists():
        return mods
    for line in md.read_text(encoding="utf-8").splitlines():
        if "BEGIN GENERATED MODULE MAP" in line:
            inside = True
            continue
        if "END GENERATED" in line:
            inside = False
            current = None
            continue
        if not inside:
            continue
        m = re.match(r"^### `([^`]+)`", line)
        if m:
            current = {"name": m.group(1), "summary": "", "symbols": []}
            mods.append(current)
            continue
        if current is None:
            continue
        s = re.match(r"^\| `(\w+)[(`]", line)
        if s:
            current["symbols"].append(s.group(1))
            continue
        t = re.match(r"^_(.+)_$", line.strip())
        if t and not current["summary"]:
            current["summary"] = t.group(1)
    return [m for m in mods if m["symbols"]]


def cmp_rows(root):
    """Real CMP-### component rows (the optional physical/component layer)."""
    rows = ct.read_rows(root / "docs" / "requirements" / "components.csv")
    return [
        r
        for r in rows
        if (r.get("CMP-ID") or "").strip().startswith("CMP-")
        and not (r.get("CMP-ID") or "").strip().endswith("-000")
    ]


def _sw_panel(mods, graph=None):
    tab = '<button data-tab="sw">How (SW architecture)</button>'
    rows = []
    for m in mods:
        syms = ", ".join(m["symbols"][:8]) + ("…" if len(m["symbols"]) > 8 else "")
        rows.append(
            "<tr><td><code>{}</code></td><td>{}</td><td>{}<br>"
            '<span class="sub"><code>{}</code></span></td></tr>'.format(
                html.escape(m["name"]),
                len(m["symbols"]),
                html.escape(m["summary"]),
                html.escape(syms),
            )
        )
    # The declared-seam graph is *earned* by IF-### rows: present it above the
    # symbol table when seams exist, else the panel stays a bare module list
    # (WI-056). None -> "" keeps the no-seam render byte-identical to before.
    graph_block = ""
    if graph:
        graph_block = (
            '<p class="cap">Declared <code>IF-###</code> interface seams '
            "(process.md §8): each arrow is a directed seam "
            "(producer&nbsp;→&nbsp;consumer) labeled by id; module, file "
            "(shared-contract hub) and external-actor nodes are styled distinctly. "
            'A module with no seam is a "connectivity undeclared" gap.</p>\n'
            + SCROLL_CUE
            + '<div class="view" {}>{}</div>\n'.format(
                _hscroll("Interface-seam graph, horizontally scrollable"), graph
            )
        )
    panel = (
        '<section id="sw" class="panel">\n<h2>Software architecture (How)</h2>\n'
        + graph_block
        + '<p class="cap">The module map from <code>docs/architecture.md</code> — a '
        "view of the generated code map (its <code>--check</code> keeps it honest "
        "against the AST), unified here so one artifact answers What, How and "
        "When.</p>\n"
        + SCROLL_CUE
        + '<div class="tablescroll" '
        + _hscroll("Module map table, horizontally scrollable")
        + '><table class="swmap"><thead><tr>'
        "<th>Module</th><th>Public</th><th>Summary · symbols</th></tr></thead>"
        "<tbody>{}</tbody></table></div>\n</section>".format("".join(rows))
    )
    return tab, panel


def _cmp_panel(rows):
    tab = '<button data-tab="cmp">How (physical)</button>'
    body = []
    for r in rows:
        body.append(
            "<tr>{}</tr>".format(
                "".join(
                    "<td>{}</td>".format(html.escape((r.get(k) or "").strip()))
                    for k in ("CMP-ID", "Name", "Category", "State", "PartOf")
                )
            )
        )
    panel = (
        '<section id="cmp" class="panel">\n<h2>Components (How — physical)</h2>\n'
        '<p class="cap">The <code>CMP-###</code> component registry (membership derives '
        "from <code>Component</code> tags on the primitives; the graph view is "
        "deferred-on-need — this table is the honest current rendering).</p>\n"
        + SCROLL_CUE
        + '<div class="tablescroll" '
        + _hscroll("Component registry table, horizontally scrollable")
        + '><table class="swmap"><thead><tr>'
        "<th>CMP</th><th>Name</th><th>Category</th><th>State</th><th>PartOf</th>"
        "</tr></thead><tbody>{}</tbody></table></div>\n</section>".format("".join(body))
    )
    return tab, panel


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

# Node fill keyed by the OKF `type` (the icicle tier palette, extended for the
# two off-spine concept kinds the bundle also carries).
OKF_TYPE_FILL = {
    "Stakeholder Need": "#4338ca",
    "System Requirement": "#0e7490",
    "Low-Level Requirement": "#64748b",
    "Test Case": "#047857",
    "Interface": "#7c3aed",
    "Process Guide": "#b45309",
}

KN_COL_W = 150
KN_COL_GAP = 60
KN_ROW_H = 30
KN_ROW_GAP = 12
KN_PAD = 16


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


def know_graph(root):
    """The OKF concept graph as (svg, details), or None when there is no bundle
    (the tab is then omitted -> a bundle-less repo renders byte-identically).
    Nodes typed + fill-keyed by OKF `type`; directed spine edges from the link
    lists; laid out server-side by the shared layered pipeline
    (`_layered_layout`), so producers sit left of consumers and the
    render is byte-deterministic — no new `--check` exclusion. The detail dict
    embeds each concept's description and its docs/okf/<tier>/<id>.md link-out
    (the middle-path body embedding)."""
    nodes, edges = _okf_nodes(root)
    if not nodes:
        return None
    node_ids = sorted(nodes)
    node_list = [{"id": k} for k in node_ids]
    pred_map = {k: [] for k in node_ids}
    succ_map = {k: [] for k in node_ids}
    for s, d in edges:
        pred_map[d].append(s)
        succ_map[s].append(d)
    pos, width, height = _layered_layout(
        node_list,
        pred_map,
        succ_map,
        lambda k: k,
        (KN_COL_W, KN_COL_GAP, KN_ROW_H, KN_ROW_GAP, KN_PAD),
    )

    edge_svg = []
    for s, d in edges:
        x1, y1 = pos[s][0] + KN_COL_W, pos[s][1] + KN_ROW_H / 2
        x2, y2 = pos[d][0], pos[d][1] + KN_ROW_H / 2
        dx = max((x2 - x1) * 0.4, 12)
        edge_svg.append(
            '<path class="kedge" data-src="{}" data-tgt="{}" '
            'd="M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}" '
            'marker-end="url(#knowarrow)"></path>'.format(
                esc(s), esc(d), x1, y1, x1 + dx, y1, x2 - dx, y2, x2, y2
            )
        )
    node_svg, details = [], {}
    for k in node_ids:
        x, y = pos[k]
        info = nodes[k]
        fill = OKF_TYPE_FILL.get(info["type"], "#64748b")
        short = k if len(k) <= 20 else k[:19] + "…"
        kt = (info.get("title") or "").strip()
        tip = k + (" — " + kt if kt else "") + " ({})".format(info["type"])
        node_svg.append(
            '<g class="knode" data-id="{}" tabindex="0">'
            "<title>{}</title>"
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="6" '
            'fill="{}"></rect><text x="{:.1f}" y="{:.1f}" text-anchor="middle" '
            'dominant-baseline="central">{}</text></g>'.format(
                esc(k),
                esc(tip),
                x,
                y,
                KN_COL_W,
                KN_ROW_H,
                fill,
                x + KN_COL_W / 2,
                y + KN_ROW_H / 2,
                esc(short),
            )  # fmt: skip
        )
        details[k] = {
            "type": info["type"],
            "title": info["title"],
            "description": info["description"],
            "resource": info["resource"],
            "href": info["href"],
            "fill": fill,
        }
    defs = (
        '<defs><marker id="knowarrow" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#94a3b8"></path></marker></defs>'
    )
    svg = (
        '<svg viewBox="0 0 {:.0f} {:.0f}" width="{:.0f}" '
        'preserveAspectRatio="xMinYMin meet" role="img">{}{}{}</svg>'.format(
            width, height, width, defs, "".join(edge_svg), "".join(node_svg)
        )
    )
    return svg, details


def _know_panel(svg, details):
    """The Knowledge tab + panel — a fully self-contained block (its style, the
    embedded detail data, and the interaction JS all live inside the panel), so
    when there is no bundle and the panel is not appended the artifact is
    byte-identical to before this view existed (the vacuity guarantee)."""
    tab = '<button data-tab="know">Knowledge (OKF)</button>'
    # </ -> <\/ so a stray "</script>" inside description text can't close the tag
    # (the build_html j() guard, applied locally because this data is embedded in
    # the panel's own inline script rather than the shared one).
    dj = json.dumps(details, ensure_ascii=False).replace("</", "<\\/")
    legend = "".join(
        '<span><i style="background:{}"></i>{}</span>'.format(c, html.escape(t))
        for t, c in OKF_TYPE_FILL.items()
    )
    style = (
        "<style>"
        "#knowgraph .knode rect{stroke:rgba(15,23,42,.15);stroke-width:1;"
        "cursor:pointer;transition:opacity .1s ease;}"
        "#knowgraph .knode text{fill:#fff;font-size:var(--nlabel);pointer-events:none;}"
        "#knowgraph .knode.dim,#knowgraph .kedge.dim{opacity:.15;}"
        "#knowgraph .knode.hl rect{stroke:#f59e0b;stroke-width:2.5;}"
        # U3 (dashboard-uniformity): the directed-dependency edge shares the drill
        # `.wire` idiom — one `--muted` stroke token (was a hardcoded #94a3b8 that
        # diverged from `.wire` in light mode) at the same 1.5 width.
        "#knowgraph .kedge{fill:none;stroke:var(--muted);stroke-width:1.5;}"
        "#knowgraph .kedge.hl{stroke:#f59e0b;stroke-width:2;}"
        "#know-detail .body{overflow-wrap:anywhere;}"
        "</style>"
    )
    script = (
        "<script>(function(){\n"
        "  const D = " + dj + ";\n"
        "  const g = document.getElementById('knowgraph'); if(!g) return;\n"
        "  const box = document.getElementById('know-detail');\n"
        "  const nodes = [...g.querySelectorAll('.knode')];\n"
        "  const edges = [...g.querySelectorAll('.kedge')];\n"
        "  const esc = s => { const d=document.createElement('div');"
        " d.textContent = s==null?'':s; return d.innerHTML; };\n"
        "  function hover(id){\n"
        "    const near = new Set([id]);\n"
        "    for(const e of edges){ const s=e.getAttribute('data-src'),"
        " t=e.getAttribute('data-tgt');\n"
        "      if(s===id) near.add(t); if(t===id) near.add(s); }\n"
        "    for(const n of nodes){ const nid=n.getAttribute('data-id');\n"
        "      n.classList.toggle('dim', !near.has(nid));"
        " n.classList.toggle('hl', nid===id); }\n"
        "    for(const e of edges){ const inc = e.getAttribute('data-src')===id"
        " || e.getAttribute('data-tgt')===id;\n"
        "      e.classList.toggle('dim', !inc); e.classList.toggle('hl', inc); }\n"
        "  }\n"
        "  function show(id){\n"
        "    const d = D[id];\n"
        "    if(!d){ box.innerHTML = '<p class=\"hint\">No detail.</p>'; return; }\n"
        '    box.innerHTML = \'<span class="badge" style="background:\''
        "+(d.fill||'#64748b')+'\">'+esc(d.type)+'</span>'\n"
        "      + '<h3>'+esc(id)+(d.title?' — '+esc(d.title):'')+'</h3>'\n"
        "      + '<p class=\"body\">'+esc(d.description)+'</p>'\n"
        "      + '<p class=\"meta\">Full concept: <a href=\"'+esc(d.href)+'\">'"
        "+esc(d.href)+'</a>'\n"
        "      + (d.resource?'<br>Source: '+esc(d.resource):'')+'</p>';\n"
        "  }\n"
        "  for(const n of nodes){ const id=n.getAttribute('data-id');\n"
        "    n.addEventListener('mouseover', () => hover(id));\n"
        "    n.addEventListener('click', () => show(id));\n"
        "    n.addEventListener('focus', () => { hover(id); show(id); }); }\n"
        "  g.addEventListener('mouseleave', () => { for(const n of nodes)"
        " n.classList.remove('dim','hl'); for(const e of edges)"
        " e.classList.remove('dim','hl'); });\n"
        "})();</script>"
    )
    panel = (
        '<section id="know" class="panel">\n'
        "<h2>Knowledge graph (OKF concepts)</h2>\n"
        '<p class="cap">The committed <code>docs/okf/</code> knowledge bundle as a '
        "typed concept graph — the dashboard is the bundle's first real "
        "<strong>consumer</strong>. Node fill keys the OKF <code>type</code>; "
        "directed edges are the <code>SN→SR→LLR→TC</code> spine links. "
        "<strong>Hover</strong> to highlight a concept's neighbourhood; "
        "<strong>click</strong> to read its description and open the full concept "
        "file. A view — the registries are the source of truth.</p>\n" + style + "\n"
        '<div class="layout">\n'
        + SCROLL_CUE
        + '<div id="knowgraph" class="view" '
        + _hscroll("OKF concept graph, horizontally scrollable")
        + ">"
        + svg
        + "</div>\n"
        '<aside id="know-detail" class="detail"><p class="hint">Hover a concept to '
        "highlight its neighbourhood; click to read its description and open the "
        "full concept file in <code>docs/okf/</code>.</p></aside>\n"
        "</div>\n"
        '<div class="legend">' + legend + "</div>\n" + script + "\n</section>"
    )
    return tab, panel


# --- the Process tab: how this project is built (WI-085 / SR-050) --------------
#
# The method reference view: the dashboard's other tabs show project *state*;
# this one shows the *process* the state moves through. Data-derived where a
# canonical source exists — the current gate from docs/gate, tier counts from
# the spine registries, work-item counts from work-items.csv — and linking out to
# the process docs everywhere a canonical home exists. The in-view restatement
# is limited to the relationships no single doc states as one picture (the
# lifecycle x gates ordering, the loop chips, the slice -> phase -> gate-bar
# cadence) — the WI-085 anti-duplication ruling.

PROCESS_GATE_FILE = "docs/gate"


def _gate_value(root):
    """The runnable gate from docs/gate — the first non-comment line (the
    derive_gate.parse_cache contract, a small stable parse duplicated per the F5
    rule), or None when the file is absent/comment-only. None is the Process
    tab's omit condition: no gate layer, no method view."""
    path = root / PROCESS_GATE_FILE
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            return s
    return None


def _process_doc(root, scaffolded, master):
    """The process-doc link target that resolves in THIS repo: the scaffolded
    docs/ copy when present (the downstream case), else the kit master (the
    meta-repo case, which never scaffolds docs/process.md), else the scaffolded
    default (what bootstrap writes). File presence only — deterministic."""
    for rel in (scaffolded, master):
        if (root / rel).exists():
            return rel
    return scaffolded


def _loop_panel(root):
    """The two circular working loops (SR-055) as one self-contained
    `<div class="loops">` block: the intake loop (A) and the human-decision
    loop (B), sharing a single LLM_Agent entry node rendered once. Each stage
    links to its canonical home *when that home exists in this repo*, so every
    emitted href resolves (a repo missing the file renders the stage as plain
    text — still deterministic; the tab itself is gated on docs/gate upstream).
    No clocks, no repo counts: the loop structure is the method's, not the
    repo's data, so it renders byte-identically regardless of the registries."""

    def canon(rel, label):
        if (root / rel).exists():
            return '<a href="{}">{}</a>'.format(esc(rel), esc(label))
        return esc(label)

    wi_csv = "docs/requirements/work-items.csv"
    intake_loop = [
        ("Intake", canon("docs/status.md", "owner/agent hands work in")),
        ("Triage → WIs", canon(wi_csv, "scoped work items with spec detail")),
        ("Resume loop", canon(wi_csv, "the scheduler derives the ready frontier")),
        ("Build / review", canon("docs/log.md", "BUILD then REVIEW-A/B")),
        ("Merge", canon("docs/log.md", "verdicts merged; the loop repeats")),
    ]
    decide_loop = [
        (
            "Open items",
            canon("docs/open-items.md", "populated incl. the gate-ratification table"),
        ),
        ("Human review", canon("docs/open-items.md", "the owner reviews and rules")),
        ("Decisions record", canon("docs/log.md", "the ruling appends to the log")),
        (
            "Merge",
            canon("docs/log.md", "the item leaves the surface; the loop repeats"),
        ),
    ]

    def loop_ol(loop_id, name, stages):
        lis = "".join(
            '<li class="stg" data-node="{}"><b>{}</b>'
            '<span class="n">{}</span></li>'.format(index, esc(title), note)
            for index, (title, note) in enumerate(stages, 1)
        )
        return (
            '<div class="loop loop-{}" data-cycle="closed">'
            '<b class="loopname">{}</b><ol class="pflow loop">{}</ol></div>'.format(
                esc(loop_id), esc(name), lis
            )
        )

    return (
        '<div class="loops">'
        '<div class="entry">'
        "<b>LLM_Agent</b>"
        "<span>the shared entry point — both loops start here</span></div>"
        + loop_ol("a", "A · Intake loop", intake_loop)
        + loop_ol("b", "B · Human-decision loop", decide_loop)
        + "</div>"
    )


def process_panel(root, wis, stats):
    """The Process tab + panel as (tab, panel), or None when there is no
    docs/gate (the tab is then omitted -> a gate-less repo renders
    byte-identically; the Knowledge-tab vacuity idiom). Three linked panels:
    artifact lifecycle x gates (live tier counts; the stages the current
    derived gate spans are highlighted), the agent-resume loop (the managed
    agent_loop phase vocabulary with its escalation edges), slices ->
    phase -> gates (commit bar vs gate bar), and (SR-055) the two circular working loops — intake and
    human-decision — sharing one LLM_Agent entry, each stage linking to its
    canonical home. Fully self-contained (style inside the panel, no script
    needed — the shared tab switcher handles it); sorted inputs, no clocks."""
    gate = _gate_value(root)
    if not gate:
        return None

    proc_doc = _process_doc(root, "docs/process.md", "project-trajectory/PROCESS.md")
    opts_doc = _process_doc(
        root, "docs/process-options.md", "project-trajectory/PROCESS_OPTIONS.md"
    )

    # Panel 1 — artifact lifecycle x gates. Live counts join the spine
    # registries; a stage is highlighted when the current gate falls in its
    # gate span (G2 spans SR / LLR+architecture / TC — the tiers a G2 project
    # is working across).
    stages = [
        ("Vision", "", "one home (the README tag)"),
        ("SN", "G1", "{} SN".format(stats["sn_total"])),
        (
            "SR",
            "G1→G2",
            "{} SR · {} verified".format(stats["sr_total"], stats["sr_verified"]),
        ),
        ("LLR + architecture", "G2", "{} LLR".format(stats["llr_total"])),
        ("TC", "G2→G3", "{} TC".format(stats["tc_total"])),
        (
            "code + tests",
            "G3",
            "{} of {} SR verified".format(stats["sr_verified"], stats["sr_total"]),
        ),
    ]
    stage_lis = []
    for label, span, note in stages:
        now = gate in span.split("→") if span else False
        stage_lis.append(
            '<li class="stg{}" data-gates="{}"><b>{}</b><span class="g">{}</span>'
            '<span class="n">{}</span></li>'.format(
                " now" if now else "",
                esc(span),
                esc(label),
                esc(span or "—"),
                esc(note),
            )
        )

    # Panel 3 — the slice -> phase -> gate cadence (work-items.csv is canonical).
    wi_done = sum(1 for w in wis if w["status"] == "done")
    bars = [
        ("per-WI slice", "one scoped work item; ends at the commit bar"),
        ("commit bar", "the per-commit suite + doc checks — every commit"),
        ("phase close", "a phase's slices batch to one re-attestation sitting"),
        ("gate bar", "the full check.py --gate run at phase close / advance"),
        ("CI", "runs the same bar on every push"),
    ]
    bar_lis = "".join(
        '<li class="stg"><b>{}</b><span class="n">{}</span></li>'.format(esc(b), esc(n))
        for b, n in bars
    )

    # Panel 2 — the resume loop (the agent_loop.py phase vocabulary; CRITIQUE is
    # tier-conditional, so its chip renders dashed).
    loop_steps = [
        ("read status", ""),
        ("PLAN", ""),
        ("BUILD", ""),
        ("REVIEW-A/B", ""),
        ("CRITIQUE", "opt"),
        ("INTEGRATE", ""),
        ("commit", ""),
        ("hook / gate", ""),
        ("repeat", ""),
    ]
    loop_lis = "".join(
        '<li class="stg{}"><b>{}</b></li>'.format(" " + cls if cls else "", esc(s))
        for s, cls in loop_steps
    )

    # Panel 4 — the two circular working loops (SR-055).
    loops_html = _loop_panel(root)

    style = (
        "<style>"
        "#process h3{font-size:.95rem;margin:1.5rem 0 .25rem;letter-spacing:-.01em;}"
        "#process .gnow{background:var(--surface);border:1px solid var(--border);"
        "border-radius:10px;padding:.6rem .9rem;box-shadow:var(--shadow);"
        "display:inline-block;margin:.2rem 0 .4rem;}"
        "#process .gnow b{color:var(--accent);}"
        "#process ol.pflow{list-style:none;display:flex;flex-wrap:wrap;"
        "gap:.55rem;padding:0;margin:.5rem 0;align-items:stretch;}"
        "#process .pflow li{position:relative;background:var(--surface);"
        "border:1px solid var(--border);border-radius:10px;"
        "padding:.5rem .7rem .55rem;box-shadow:var(--shadow);max-width:200px;}"
        "#process .pflow li+li{margin-left:1rem;}"
        '#process .pflow li+li::before{content:"→";'
        "position:absolute;left:-.95rem;top:50%;transform:translateY(-50%);"
        "color:var(--muted);}"
        "#process .pflow li.now{border:2px solid var(--accent);"
        "padding:calc(.5rem - 1px) calc(.7rem - 1px) calc(.55rem - 1px);}"
        "#process .pflow li.opt{border-style:dashed;}"
        "#process .pflow b{display:block;font-size:.85rem;}"
        "#process .pflow .g{display:block;font-size:.7rem;font-weight:700;"
        "letter-spacing:.04em;color:var(--accent);}"
        "#process .pflow .n{display:block;font-size:.75rem;color:var(--muted);}"
        "#process ul.esc{font-size:.9rem;color:var(--muted);margin:.4rem 0 0;"
        "padding-left:1.2rem;}"
        "#process ul.esc b{color:var(--text);}"
        # Panel 4 — the two circular working loops, sharing one LLM_Agent entry.
        "#process .loops{display:grid;grid-template-columns:minmax(7.5rem,auto) 1fr;"
        "grid-template-rows:1fr 1fr;gap:.8rem 0;align-items:stretch;"
        "margin:.7rem 0;isolation:isolate;}"
        "#process .entry{grid-column:1;grid-row:1/3;align-self:center;z-index:3;"
        "background:var(--surface);"
        "border:2px solid var(--accent);border-radius:10px;"
        "padding:.45rem .8rem;box-shadow:var(--shadow);max-width:9.5rem;}"
        "#process .entry b{display:block;font-size:.88rem;color:var(--accent);}"
        "#process .entry span{font-size:.72rem;color:var(--muted);}"
        "#process div.loop{grid-column:2;position:relative;border:2px solid var(--accent);"
        "border-left-width:3px;border-radius:999px;padding:1.45rem 2rem 1.2rem 3rem;"
        "margin-left:-1rem;min-height:10.5rem;}"
        "#process .loop-a{grid-row:1;}#process .loop-b{grid-row:2;}"
        '#process div.loop::after{content:"";position:absolute;left:-.45rem;top:50%;'
        "width:.72rem;height:.72rem;border-top:3px solid var(--accent);"
        "border-right:3px solid var(--accent);transform:translateY(-50%) rotate(-135deg);"
        "background:var(--bg);}"
        "#process .loop .loopname{position:absolute;left:3rem;top:.3rem;"
        "font-size:.82rem;font-weight:700;color:var(--accent);}"
        "#process ol.pflow.loop{display:grid;grid-template-columns:repeat(3,minmax(7rem,1fr));"
        "grid-template-rows:repeat(2,auto);gap:.65rem 1rem;margin:0;align-items:center;}"
        "#process .pflow.loop li{max-width:none;margin-left:0;}"
        "#process .pflow.loop li+li::before{display:none;}"
        "#process .pflow.loop li:nth-child(1){grid-column:1;grid-row:1;}"
        "#process .pflow.loop li:nth-child(2){grid-column:2;grid-row:1;}"
        "#process .pflow.loop li:nth-child(3){grid-column:3;grid-row:1;}"
        "#process .pflow.loop li:nth-child(4){grid-column:3;grid-row:2;}"
        "#process .pflow.loop li:nth-child(5){grid-column:1;grid-row:2;}"
        "#process .loop-b .pflow.loop li:nth-child(2){grid-column:3;}"
        "#process .loop-b .pflow.loop li:nth-child(3){grid-column:3;grid-row:2;}"
        "#process .loop-b .pflow.loop li:nth-child(4){grid-column:1;grid-row:2;}"
        "#process .pflow.loop a{color:inherit;}"
        "@media(max-width:760px){#process .loops{grid-template-columns:1fr;"
        "grid-template-rows:auto;}#process .entry{grid-column:1;grid-row:1;"
        "justify-self:center;max-width:none;}#process div.loop{grid-column:1;"
        "margin:-.65rem 0 0;padding:2.2rem 1rem 1rem;border-radius:28px;}"
        "#process .loop-a{grid-row:2}#process .loop-b{grid-row:3}"
        "#process ol.pflow.loop{grid-template-columns:1fr;}"
        "#process .pflow.loop li:nth-child(n){grid-column:1;grid-row:auto;}"
        "#process div.loop::after{left:50%;top:-.4rem;transform:translateX(-50%) rotate(-45deg);}}"
        "</style>"
    )
    panel = (
        '<section id="process" class="panel">\n'
        "<h2>How this project is built</h2>\n"
        '<p class="cap">The method reference — the other tabs show project '
        "<em>state</em>; this one shows the <strong>process</strong> the state "
        "moves through. Data-derived where a canonical source exists "
        "(<code>docs/gate</code>, the spine registries, "
        "<code>work-items.csv</code>). A view — the process docs are the source "
        "of truth.</p>\n" + style + "\n"
        '<p class="gnow">Current gate: <b>' + esc(gate) + "</b> — derived from "
        "artifact states and cached to <code>docs/gate</code> "
        "(<code>derive_gate.py</code>); highlighted stages are the tiers this "
        "gate spans.</p>\n"
        "<h3>1 · Artifact lifecycle × gates</h3>\n"
        '<p class="cap">Each tier decomposes the one above it and is ratified '
        "through the gate it spans — the tiers (§3) and the gate bars (§4) live "
        'in <a href="' + esc(proc_doc) + '">' + esc(proc_doc) + "</a>. Counts are "
        "live from this repo's registries.</p>\n"
        '<ol class="pflow">' + "".join(stage_lis) + "</ol>\n"
        "<h3>2 · The resume loop</h3>\n"
        '<p class="cap">The managed <code>agent_loop.py</code> walk-away flow — '
        'the full contract is <a href="'
        + esc(opts_doc)
        + '">'
        + esc(opts_doc)
        + "</a> “Unattended operation”. The dashed CRITIQUE phase is "
        "tier-conditional.</p>\n"
        '<ol class="pflow">' + loop_lis + "</ol>\n"
        '<ul class="esc">\n'
        "<li><b>DESIGN-CHECK</b> — a review finding that indicts the design "
        "routes the next session to a design pass, not a re-build.</li>\n"
        "<li><b>Page the human</b> — nothing routable, or the declared gate "
        "policy requires a human act: the loop parks with the ask recorded in "
        "<code>docs/status.md</code>.</li>\n"
        "</ul>\n"
        "<h3>3 · Slices → phase → gates</h3>\n"
        '<p class="cap">A per-WI slice ends at the <strong>commit bar</strong>; '
        "a phase closes at the <strong>gate bar</strong> — the commit-bar-vs-gate-bar "
        'cadence lives in <a href="'
        + esc(opts_doc)
        + '">'
        + esc(opts_doc)
        + "</a> “Trajectory / work-items layer”. Live from "
        "<code>work-items.csv</code>: "
        + esc(len(wis))
        + " work items · "
        + esc(wi_done)
        + " done.</p>\n"
        '<ol class="pflow">' + bar_lis + "</ol>\n"
        "<h3>4 · The working loops</h3>\n"
        '<p class="cap">Two circular flows close the method — how work '
        "<strong>enters</strong> (A) and how the human <strong>decides</strong> "
        "(B) — both entered by the same agent. Each stage links to its canonical "
        "home (<code>status.md</code>, <code>work-items.csv</code>, "
        "<code>open-items.md</code>, <code>log.md</code>); the loop structure is "
        "the method's, not this repo's data.</p>\n" + loops_html + "\n"
        "</section>"
    )
    return '<button data-tab="process">Process</button>', panel


def build_html(root, wis):
    total = len(wis)
    done = sum(1 for w in wis if w["status"] == "done")
    active = sum(1 for w in wis if w["status"] == "active")
    # T1 (dashboard-usability): name the in-flight work on the landing hero so
    # "find the next work" costs zero tab switches — the When drill buries the
    # active leaf several descents deep. Empty (no markup) when nothing is active.
    active_wis = [w for w in wis if w["status"] == "active"]
    wi_active_line = ""
    if active_wis:
        names = "; ".join("{} — {}".format(w["id"], w["title"]) for w in active_wis)
        wi_active_line = '<div class="sub nowat">{} {}</div>'.format(
            STATUS_GLYPH["active"], html.escape(names)
        )
    stats = spine_stats(root)
    workstreams = len({w["workstream"] for w in wis})
    arch, arch_details, arch_desc = arch_icicle(root)
    dag, wi_details = dag_svg(wis)
    # WI-087: the When view tiers into phase -> workstream -> work-item block
    # layers once a tier holds more than 3 members; at <= 3 phases and <= 3
    # workstreams `when_view` returns None, so the flat SVG DAG renders instead
    # (byte-identical to a small registry's roadmap).
    dag_view = when_view(root, wis) or dag
    extra_tabs, extra_panels = [], []
    mods = sw_modules(root)
    if mods:
        # WI-073: when a CMP layer contains modules, the How-SW panel becomes the
        # containerized top view (≤ ct.TOP_VIEW_MAX items, expandable); otherwise
        # it keeps today's flat graph/table (byte-identical for a no-CMP repo).
        tab, panel = sw_containment(root, mods) or _sw_panel(mods, sw_graph(root, mods))
        extra_tabs.append(tab)
        extra_panels.append(panel)
    # The How-physical CMP table holds the *non-software* components; software
    # components live in the containerized How-SW view above (WI-073), so a
    # domain-neutral CMP row lands in the tab that matches its Category.
    physical = [
        r
        for r in cmp_rows(root)
        if (r.get("Category") or "").strip().lower() != "software"
    ]
    if physical:
        tab, panel = _cmp_panel(physical)
        extra_tabs.append(tab)
        extra_panels.append(panel)
    know = know_graph(root)  # the OKF bundle's first real consumer (WI-070)
    if know:
        tab, panel = _know_panel(*know)
        extra_tabs.append(tab)
        extra_panels.append(panel)
    proc = process_panel(root, wis, stats)  # the method reference view (WI-085)
    if proc:
        tab, panel = proc
        extra_tabs.append(tab)
        extra_panels.append(panel)

    # </ -> <\/ so a stray "</script>" inside requirement text can't close the tag.
    def j(o):
        return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

    return HTML_TEMPLATE.substitute(
        asof=html.escape(_asof(root)),
        extra_tabs="\n      ".join(extra_tabs),
        extra_panels="\n\n    ".join(extra_panels),
        project=html.escape(project_name(root)),
        vision=html.escape(project_vision(root)),
        def_pct=stats["def_pct"],
        sr_verified=stats["sr_verified"],
        sn_total=stats["sn_total"],
        sr_total=stats["sr_total"],
        llr_total=stats["llr_total"],
        tc_total=stats["tc_total"],
        workstreams=workstreams,
        wi_pct=round(100 * done / total) if total else 0,
        wi_done=done,
        wi_total=total,
        wi_active=active,
        wi_active_line=wi_active_line,
        arch_svg=arch,
        arch_details=j(arch_details),
        arch_desc=j(arch_desc),
        dag_svg=dag_view,
        wi_details=j(wi_details),
        scroll_cue=SCROLL_CUE,
    )


# --- the status.md derived snapshot (WI-202) -----------------------------------


def _gate_facts(root):
    """The derived-gate facts for the status snapshot, read from `docs/gate` — the
    cached, freshness-guarded SSOT (derive_gate.py owns it; check.py's `derived-gate`
    step keeps it fresh). Returns `(gate_value, basis)`: the gate is the first
    non-comment line; `basis` parses the `# basis:` line's `k=v` tokens
    (SN/SR/LLR/TC/drafts/computed/phase/per-phase) when present, else `{}` (a legacy
    hand-set gate with no basis line). The snapshot PROJECTS this rather than
    recomputing what derive_gate already cached — one home for the derivation."""
    p = root / "docs" / "gate"
    if not p.exists():
        return "", {}
    text = p.read_text(encoding="utf-8", errors="replace")
    gate = ""
    for ln in text.splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            gate = ln
            break
    basis = {}
    m = _GATE_BASIS_RE.search(text)
    if m:
        for tok in m.group(1).split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                basis[k] = v
    return gate, basis


def _spine_counts(root, basis):
    """`{SN,SR,LLR,TC}` string counts for the snapshot: the fresh `docs/gate`
    basis line when present (the authoritative derivation), else a direct count
    of the registries (the legacy-gate fallback)."""
    if all(k in basis for k in ("SN", "SR", "LLR", "TC")):
        return {k: basis[k] for k in ("SN", "SR", "LLR", "TC")}
    st = spine_stats(root)
    return {
        "SN": str(st["sn_total"]),
        "SR": str(st["sr_total"]),
        "LLR": str(st["llr_total"]),
        "TC": str(st["tc_total"]),
    }


_ONELINE_LABEL_RE = re.compile(
    r"(?i)^[ \t]*[-*][ \t]*\*\*one[- ]?line:?\*\*[ \t]*(.*)$"
)
_RECO_LABEL_RE = re.compile(
    r"(?i)^[ \t]*[-*][ \t]*\*\*recommendation[^:*]*:?\*\*[ \t]*(.*)$"
)
_OI_ID_RE = re.compile(r"\bOI-\d+\b")


def _field_value(body, label_re):
    """The full (possibly soft-wrapped) value of a `- **Label:** …` field in a
    brief body, or None. Markdown wraps a long field across indented continuation
    lines; they are joined with a space, stopping at the first blank line, the
    next `-`/`*` bullet, or a heading — so the projection captures the whole
    sentence, not just its first physical line."""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        m = label_re.match(line)
        if not m:
            continue
        parts = [m.group(1).strip()]
        for nxt in lines[i + 1 :]:
            s = nxt.strip()
            if not s or re.match(r"[-*]\s", s) or s.startswith("#"):
                break
            parts.append(s)
        return " ".join(p for p in parts if p).strip()
    return None


def _clean_oneliner(s):
    """Normalize a projected one-liner: Markdown link `[text](url)` -> its text,
    stray emphasis/backticks dropped, whitespace collapsed. Keeps the snapshot
    scannable and byte-stable regardless of the brief's inline markup."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"\*\*|`", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _first_sentence(s):
    """The first sentence of `s` (up to the first sentence-ending `.`/`!`/`?`),
    else all of `s`. A `;`-joined clause stays whole — only a full stop ends it."""
    m = re.search(r"^(.*?[.!?])(?:\s|$)", s)
    return (m.group(1) if m else s).strip()


def _open_item_oneliners(root):
    """`[(OI-id, one-liner)]` projected from `docs/open-items.md`'s `## OI-N`
    sections, id-order. The one-liner is the section's explicit `- **One-line:** …`
    field, else the first sentence of its `- **Recommendation…:** …` line — the
    contract pinned in docs/specs/open-items-surface.md, so the projection is
    deterministic. Volatile per-item facts (an OI's live git state) stay in the
    brief, never the stamped snapshot. Empty when open-items.md is absent."""
    p = root / "docs" / "open-items.md"
    if not p.is_file():
        return []
    text = p.read_text(encoding="utf-8", errors="replace")
    parts = ct.OI_SECTION_RE.split(text)  # [pre, head1, body1, head2, body2, ...]
    out = []
    for i in range(1, len(parts), 2):
        head = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        m = _OI_ID_RE.search(head)
        if not m:
            continue
        oid = m.group(0)
        one = _field_value(body, _ONELINE_LABEL_RE)
        if one is None:
            reco = _field_value(body, _RECO_LABEL_RE)
            one = _first_sentence(reco) if reco else ""
        out.append((oid, _clean_oneliner(one)))
    return sorted(out, key=lambda t: int(t[0].split("-")[1]))


# --- the docs/open-items.md pending-owner-actions projection (WI-234) -----------


def _git(root, *args):
    """`(returncode, stdout)` for a READ-ONLY git command, `(1, "")` on any
    failure — the `_asof` idiom (gen_trajectory shells git via stdlib rather than
    importing the dispatcher, which would drag the whole engine into a renderer).
    Every pending source degrades to empty off-git, so a non-repo pays nothing."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,
        )
    except OSError:
        return 1, ""
    return proc.returncode, proc.stdout


def _ref_meta(root, ref):
    """The JSON metadata a reservation/conflict ref's commit message carries
    (a dict), or None when the ref is absent/unreadable/malformed. Mirrors
    agent_dispatch.reservation_meta / read_conflict, read-only."""
    code, sha = _git(root, "rev-parse", "--verify", "--quiet", ref)
    if code != 0 or not sha.strip():
        return None
    code, body = _git(root, "log", "-1", "--format=%B", sha.strip())
    if code != 0:
        return None
    try:
        meta = json.loads(body)
    except ValueError:
        return None
    return meta if isinstance(meta, dict) else None


def _train_carrying_path(root, relpath):
    """The first train branch (`llm/train/*`, id-sorted) whose tree contains
    `relpath`, or '' — the read path for an attestation doc frozen on a train and
    absent from the dev tree (the WI-229 shape: `git show <train>:<path>`)."""
    code, out = _git(
        root,
        "for-each-ref",
        "--format=%(refname)",
        "refs/heads/" + _TRAIN_BRANCH_PREFIX,
    )
    if code != 0:
        return ""
    heads = "refs/heads/"
    branches = sorted(
        ln.strip()[len(heads) :]
        for ln in out.splitlines()
        if ln.strip().startswith(heads + _TRAIN_BRANCH_PREFIX)
    )
    for br in branches:
        code, _ = _git(root, "cat-file", "-e", "{}:{}".format(br, relpath))
        if code == 0:
            return br
    return ""


def _blocked_pending(root):
    """Source (a): `(lines, ids)` — one line per `blocked` WI row carrying a
    BlockRef, and the set of WI ids covered (so the stranded-train source below
    never double-lists one). The pointer is the BlockRef path; when a path-shaped
    ref is absent from the dev tree but a train branch carries it, the
    `git show <train>:<path>` read path is used instead."""
    wis, _ = ct.load_wis(ct.read_rows(root / ct.WI_CSV))
    lines, ids = [], set()
    for w in sorted(wis, key=lambda w: w["id"]):
        if w["status"] != "blocked" or not w["blockref"]:
            continue
        ref = w["blockref"]
        pointer = "`{}`".format(ref)
        path = ref.split("#", 1)[0]
        pathish = "/" in path or "." in path
        if pathish and not (root / path).exists():
            train = _train_carrying_path(root, path)
            if train:
                pointer = "`git show {}:{}`".format(train, path)
        lines.append(
            "- **{}** blocked — attest/ratify {}, then unblock the registry "
            "row.".format(w["id"], pointer)
        )
        ids.add(w["id"])
    return lines, ids


def _scan_reservations(root):
    """`(trains, unreadable)` re-derived from the DURABLE refs/llm/reservations/*
    (never the out/dispatch journal): `trains` maps `train_id ->
    {"wis": [...], "base": <sha>}` from readable metadata; `unreadable` is the
    list of WI ids whose reservation metadata is missing/malformed. Mirrors
    agent_dispatch._reservation_trains read-only."""
    code, out = _git(
        root, "for-each-ref", "--format=%(refname)", _RESERVATION_NS.rstrip("/")
    )
    trains, unreadable = {}, []
    if code != 0:
        return trains, unreadable
    for ln in out.splitlines():
        refname = ln.strip()
        if not refname.startswith(_RESERVATION_NS):
            continue
        wid = refname[len(_RESERVATION_NS) :]
        if not _WI_REF_RE.match(wid):
            continue
        meta = _ref_meta(root, refname)
        if not meta or not meta.get("train") or not meta.get("wis"):
            unreadable.append(wid)
            continue
        entry = trains.setdefault(
            meta["train"], {"wis": [], "base": (meta.get("base") or "").strip()}
        )
        entry["wis"].append(wid)
    return trains, unreadable


def _train_tip(root, tid):
    """The train branch tip sha, or '' when the branch is absent."""
    code, tip = _git(
        root,
        "rev-parse",
        "--verify",
        "--quiet",
        "refs/heads/" + _TRAIN_BRANCH_PREFIX + tid,
    )
    return tip.strip() if code == 0 else ""


def _train_blocked_trailers(root, base, tip):
    """`[(wi, blockref, commit_sha)]` for every `Blocked-WI:` trailer in the
    commit bodies of `base..tip` (id-order per commit, newest first). Git's own
    trailer parser is deliberately NOT used: the frozen-plan commit separates its
    trailer lines with blank lines, which git treats as separate paragraphs and
    drops all but the last — so a line-regex over the raw `%B` body is the
    durable read (WI-229's `9fed833` shape)."""
    rng = (base + ".." + tip) if base else tip
    code, out = _git(root, "log", rng, "--format=%x1e%H%n%B")
    if code != 0:
        return []
    found = []
    for rec in out.split("\x1e"):
        if not rec.strip("\n"):
            continue
        sha, _, body = rec.strip("\n").partition("\n")
        wi, blockref = "", ""
        for bl in body.splitlines():
            m = re.match(r"(?i)^\s*Blocked-WI:\s*(WI-\d+)\s*$", bl)
            if m:
                wi = m.group(1)
            m = re.match(r"(?i)^\s*BlockRef:\s*(\S+)\s*$", bl)
            if m:
                blockref = m.group(1)
        if wi:
            found.append((wi, blockref, sha.strip()))
    return found


def _attestation_pointer(root, tid, blockref, sha):
    """The train read path to the blocking ratify doc for a stranded WI: the
    BlockRef path (its `#anchor` stripped) when the train carries it, else the
    first `docs/ratify/*` path the trailer commit touched, else the trailer
    commit itself — all reachable with `git show <train>[:<path>]`."""
    branch = _TRAIN_BRANCH_PREFIX + tid
    if blockref:
        path = blockref.split("#", 1)[0]
        if path and _git(root, "cat-file", "-e", "{}:{}".format(branch, path))[0] == 0:
            return "`git show {}:{}`".format(branch, path)
    code, out = _git(root, "show", "--name-only", "--format=", sha)
    if code == 0:
        ratify = sorted(
            p.strip() for p in out.splitlines() if p.strip().startswith("docs/ratify/")
        )
        if ratify:
            return "`git show {}:{}`".format(branch, ratify[0])
    return "the frozen plan at commit `{}` (`git show {}`)".format(sha[:12], sha[:12])


def _stranded_pending(root, already):
    """Source (a′): reserved WIs stranded on a PRESENT train awaiting owner
    attestation — the WI-229 shape the registry doesn't mark `blocked` (its row
    stays queued while the plan freezes on the train). For each persistent
    reservation whose train branch exists, the train's commit bodies are scanned
    for a `Blocked-WI:` trailer naming a reserved WI whose registry row is still
    OPEN (queued/active/blocked); that projects an attestation line with the
    train read path to the blocking ratify doc. `already` = the WI ids source (a)
    covered, skipped so no WI double-lists."""
    reg = {w["id"]: w["status"] for w in ct.load_wis(ct.read_rows(root / ct.WI_CSV))[0]}
    open_states = {"queued", "active", "blocked"}
    trains, _ = _scan_reservations(root)
    lines, seen = [], set()
    for tid in sorted(trains):
        reserved = set(trains[tid]["wis"])
        tip = _train_tip(root, tid)
        if not tip:
            continue
        for wi, blockref, sha in _train_blocked_trailers(
            root, trains[tid]["base"], tip
        ):
            if wi not in reserved or wi in already or wi in seen:
                continue
            if reg.get(wi) not in open_states:
                continue
            seen.add(wi)
            lines.append(
                "- **{}** — awaiting owner attestation/ratification on train `{}`: "
                "{}; attest, amend, or park the row.".format(
                    wi, tid, _attestation_pointer(root, tid, blockref, sha)
                )
            )
    return lines


def _conflict_pending(root):
    """Source (b): one line per durable source-conflict record under
    refs/llm/conflict/* (WI-232), naming the train and its conflicted paths — a
    genuine human merge the dispatcher must not retry. An unreadable/malformed
    record is surfaced too (not silently skipped), matching the reservations'
    fail-loud posture."""
    code, out = _git(
        root, "for-each-ref", "--format=%(refname)", _CONFLICT_NS.rstrip("/")
    )
    if code != 0:
        return []
    tids = sorted(
        ln.strip()[len(_CONFLICT_NS) :]
        for ln in out.splitlines()
        if ln.strip().startswith(_CONFLICT_NS)
    )
    lines = []
    for tid in tids:
        meta = _ref_meta(root, _CONFLICT_NS + tid)
        if not meta:
            lines.append(
                "- **Unreadable conflict record** — inspect `{}{}`.".format(
                    _CONFLICT_NS, tid
                )
            )
            continue
        paths = meta.get("paths") or "textual conflict against the integrated tree"
        train = meta.get("train") or tid
        lines.append(
            "- **Source conflict** — train `{}` conflicts on {}; resolve by hand "
            "(merge/rebase the train), then relaunch.".format(train, paths)
        )
    return lines


def _quarantine_pending(root):
    """Source (c): one line per quarantined train, re-derived from the DURABLE
    reservation refs (never the out/dispatch journal): a reservation whose
    metadata is unreadable, or whose train branch is missing — the reconcile
    quarantine conditions (agent_dispatch._reservation_trains /
    _reconcile_reserved_train). id-sorted for determinism."""
    trains, unreadable = _scan_reservations(root)
    lines = [
        "- **Quarantined reservation** `{0}` — unreadable reservation metadata; "
        "inspect `{1}{0}`.".format(wid, _RESERVATION_NS)
        for wid in sorted(unreadable)
    ]
    for tid in sorted(trains):
        if not _train_tip(root, tid):
            lines.append(
                "- **Quarantined train** `{}` — reservation without a train branch "
                "({}); inspect the reservation refs.".format(
                    tid, ", ".join(sorted(trains[tid]["wis"]))
                )
            )
    return lines


def _runstate_pending(root):
    """Source (d): the run-state `ask:` line when docs/run-state reads
    NEEDS-HUMAN (the first non-comment line, `read_declared`'s rule). Empty for
    RUNNING/BLOCKED/DONE or an absent file."""
    p = root / "docs" / "run-state"
    if not p.is_file():
        return []
    state, ask = "", ""
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if not state:
            state = s
        elif s.lower().startswith("ask:") and not ask:
            ask = s[len("ask:") :].strip()
    if state != "NEEDS-HUMAN":
        return []
    tail = " — {}".format(ask) if ask else ""
    return [
        "- **Run-state NEEDS-HUMAN**{} — see the stop banner / "
        "[status.md](status.md).".format(tail)
    ]


def pending_block(root):
    """The GENERATED PENDING block CONTENT (between the markers) for
    docs/open-items.md: one line per DURABLE pending-owner action (blocked rows
    with a BlockRef, refs/llm/conflict records, quarantined trains, the
    NEEDS-HUMAN run-state ask). Derived from durable state ONLY (never the
    journal cache), deterministic (sorted, no clocks) so `--status --check` is
    byte-stable, exactly like the status snapshot."""
    lead = (
        "_Pending owner actions — a generated projection of durable state "
        "(blocked rows, stranded attestations, source conflicts, quarantines, the "
        "NEEDS-HUMAN run-state ask); regenerated by `python "
        "project-trajectory/scripts/gen_trajectory.py --status`, do not hand-edit. "
        "The briefs above are hand-authored and untouched by regeneration._"
    )
    blocked_lines, blocked_ids = _blocked_pending(root)
    items = (
        blocked_lines
        + _stranded_pending(root, blocked_ids)
        + _conflict_pending(root)
        + _quarantine_pending(root)
        + _runstate_pending(root)
    )
    body = "\n".join(items) if items else "_None — no durable owner action is pending._"
    return lead + "\n\n" + body


def _splice_pending(doc_text, content):
    """Replace the text between the PENDING markers with `content`; returns
    `(new_text, present)`. Markers are matched only as EXACT FULL LINES, so a
    hand-authored brief quoting the marker string on an indented or fenced line
    is ignored — regeneration never chokes on it. `present` is False when the
    pair is absent (the opt-in / graceful-degrade posture — a lone marker or
    neither → left untouched, `--status --check` passes vacuously). Anomalies
    fail CLOSED with a named error, never a silent rewrite: a duplicated marker
    line, or an inverted pair (END before BEGIN). The file's dominant line-ending
    style is preserved (a CRLF checkout stays CRLF), so the byte-untouched
    guarantee holds on autocrlf."""
    crlf = doc_text.count("\r\n")
    nl = "\r\n" if crlf and crlf >= (doc_text.count("\n") - crlf) else "\n"
    lines = doc_text.splitlines()
    begins = [i for i, ln in enumerate(lines) if ln == PENDING_BEGIN]
    ends = [i for i, ln in enumerate(lines) if ln == PENDING_END]
    if not begins or not ends:
        return doc_text, False
    if len(begins) > 1 or len(ends) > 1:
        raise SystemExit(
            "{}: duplicated PENDING marker line ({} begin / {} end); keep exactly "
            "one {} / {} pair".format(
                OPEN_ITEMS_MD, len(begins), len(ends), PENDING_BEGIN, PENDING_END
            )
        )
    begin, end = begins[0], ends[0]
    if end < begin:
        raise SystemExit(
            "{}: PENDING markers are inverted ({} appears before {}); refusing to "
            "splice".format(OPEN_ITEMS_MD, PENDING_END, PENDING_BEGIN)
        )
    new_lines = lines[: begin + 1] + content.splitlines() + lines[end:]
    result = nl.join(new_lines)
    if doc_text.endswith(("\n", "\r")):
        result += nl
    return result, True


def run_pending(root, check):
    """`--status` companion: splice the durable pending-owner projection into
    docs/open-items.md's PENDING block (or, with `check`, byte-compare and fail on
    drift). Vacuous — exit 0 — when open-items.md is absent or has no marker pair
    (the opt-in posture, so a repo that never adopts the surface pays nothing)."""
    path = root / OPEN_ITEMS_MD
    if not path.exists():
        if not check:
            print(
                "gen_trajectory: no {} — nothing to project (vacuous).".format(
                    OPEN_ITEMS_MD
                )
            )
        return 0
    # newline="" preserves the file's own line endings on read, so a CRLF
    # checkout round-trips byte-for-byte through the splice (the hand region stays
    # untouched) rather than being normalized to LF.
    with path.open("r", encoding="utf-8", newline="") as fh:
        current = fh.read()
    updated, present = _splice_pending(current, pending_block(root))
    if not present:
        if not check:
            print(
                "gen_trajectory: {} has no GENERATED PENDING markers — vacuous "
                "(add the {} / {} pair to opt in).".format(
                    OPEN_ITEMS_MD, PENDING_BEGIN, PENDING_END
                )
            )
        return 0
    if check:
        if updated != current:
            print(
                "pending owner-actions projection STALE in {}: run `python "
                "scripts/gen_trajectory.py --status`".format(OPEN_ITEMS_MD),
                file=sys.stderr,
            )
            return 1
        print("pending owner-actions projection up to date.")
        return 0
    if updated == current:
        print(
            "gen_trajectory: {} pending projection already up to date.".format(
                OPEN_ITEMS_MD
            )
        )
    else:
        # newline="" writes the spliced text verbatim — _splice_pending already
        # embedded the file's own line endings, so translation must stay off.
        with path.open("w", encoding="utf-8", newline="") as fh:
            fh.write(updated)
        print(
            "gen_trajectory: pending projection regenerated -> {}".format(OPEN_ITEMS_MD)
        )
    return 0


def status_block(root):
    """The GENERATED STATUS block CONTENT (between the markers) for docs/status.md:
    the derived gate + spine snapshot (projected from `docs/gate`, the freshness-
    guarded SSOT) plus the open-items one-liners (from open-items.md). Derived
    facts ONLY — the forward-only intent stays hand-authored outside the markers.
    Deterministic (no clocks), so the `--status --check` byte-compare is stable,
    exactly like the arch-map / dashboard freshness gates."""
    gate, basis = _gate_facts(root)
    counts = _spine_counts(root, basis)
    seams = len(ct.load_ifs(ct.read_rows(root / ct.IF_CSV)))
    comps = len(cmp_rows(root))

    gate_bits = []
    if basis.get("per-phase"):
        gate_bits.append("per-phase `{}`".format(basis["per-phase"]))
    if basis.get("phase"):
        gate_bits.append("derived current **phase={}**".format(basis["phase"]))
    gate_detail = " ({})".format(", ".join(gate_bits)) if gate_bits else ""

    drafts = basis.get("drafts")
    draft_bit = ""
    if drafts is not None:
        draft_bit = " ({} draft{})".format(drafts, "" if drafts == "1" else "s")

    lines = [
        "_Derived facts — regenerated by `python "
        "project-trajectory/scripts/gen_trajectory.py --status`; do not hand-edit "
        "(the forward-only intent below is hand-authored)._",
        "",
        "- **Active gate:** derived **{}**{} — the harness at the derived gate is "
        "the bar; [`derive_gate.py`](../project-trajectory/scripts/derive_gate.py) "
        "computes it, cached to [`docs/gate`](gate).".format(
            gate or "(none)", gate_detail
        ),
        "- **Spine:** **SN={sn} SR={sr} LLR={llr} TC={tc}**{d} · {seams} seam{sp} · "
        "{comps} component{cp}.".format(
            sn=counts["SN"],
            sr=counts["SR"],
            llr=counts["LLR"],
            tc=counts["TC"],
            d=draft_bit,
            seams=seams,
            sp="" if seams == 1 else "s",
            comps=comps,
            cp="" if comps == 1 else "s",
        ),
    ]
    ois = _open_item_oneliners(root)
    if ois:
        lines.append(
            "- **Open items** _(projected from [open-items.md](open-items.md) — "
            "each item's blast radius, options, and recommendation live there):_"
        )
        lines.extend("  - **{}** — {}".format(oid, one) for oid, one in ois)
    return "\n".join(lines)


def _splice_status(doc_text, content):
    """Replace the text between the STATUS markers with `content`. Returns
    `(new_text, present)`; `present` is False when the marker pair is absent — the
    opt-in posture, a status.md without markers is left untouched so `--status
    --check` passes vacuously downstream. A duplicated marker is refused (it would
    make the splice ambiguous), the gen_arch_map.splice_region rule."""
    if STATUS_BEGIN not in doc_text or STATUS_END not in doc_text:
        return doc_text, False
    if doc_text.count(STATUS_BEGIN) > 1 or doc_text.count(STATUS_END) > 1:
        raise SystemExit(
            "{}: duplicated STATUS marker; keep exactly one {} / {} pair".format(
                STATUS_MD, STATUS_BEGIN, STATUS_END
            )
        )
    pre = doc_text.split(STATUS_BEGIN)[0]
    post = doc_text.split(STATUS_END)[1]
    return "{}{}\n{}\n{}{}".format(pre, STATUS_BEGIN, content, STATUS_END, post), True


def run_status(root, check):
    """`--status` mode: splice the derived snapshot into docs/status.md (or, with
    `check`, byte-compare and fail on drift). Vacuous — exit 0 — when status.md is
    absent or carries no marker pair (the opt-in posture)."""
    path = root / STATUS_MD
    if not path.exists():
        print("gen_trajectory: no {} — nothing to splice (vacuous).".format(STATUS_MD))
        return 0
    current = path.read_text(encoding="utf-8")
    updated, present = _splice_status(current, status_block(root))
    if not present:
        print(
            "gen_trajectory: {} has no GENERATED STATUS markers — vacuous (add the "
            "{} / {} pair to opt in).".format(STATUS_MD, STATUS_BEGIN, STATUS_END)
        )
        return 0
    if check:
        if updated != current:
            print(
                "status snapshot STALE in {}: run `python "
                "scripts/gen_trajectory.py --status`".format(STATUS_MD),
                file=sys.stderr,
            )
            return 1
        print("status snapshot up to date.")
        return 0
    if updated == current:
        print(
            "gen_trajectory: {} status snapshot already up to date.".format(STATUS_MD)
        )
    else:
        # newline="\n" via open() (write_text(newline=) is 3.10+, floor 3.8): LF
        # on every OS so the generated block stays byte-stable regardless of a
        # downstream .gitattributes rule.
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(updated)
        print("gen_trajectory: status snapshot regenerated -> {}".format(STATUS_MD))
    return 0


def main():
    ct._utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root", default=".", help="repo root (default: current directory)"
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="validate + verify freshness without writing (nonzero on "
        "stale/invalid). Missing-target posture (C9): a fully-generated "
        "output, so a missing file reads as stale — unlike arch-map, whose "
        "hand-authored target must exist",
    )
    ap.add_argument(
        "--status",
        action="store_true",
        help="splice the derived-facts snapshot (spine + derived gate + "
        "open-items one-liners) into docs/status.md AND the durable "
        "pending-owner-actions projection into docs/open-items.md instead of "
        "rendering the dashboard; with --check, byte-compare both for freshness "
        "(the WI-200 forward-only guard's successor). Vacuous without the "
        "marker pair.",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if args.status:
        # Both marker-block projections ride `--status` so the harness
        # `status-map` step's `--status --check` freshness-gates BOTH the
        # status snapshot and the pending-owner-actions projection (WI-234).
        rc = run_status(root, args.check)
        rc_pending = run_pending(root, args.check)
        return rc or rc_pending

    if not ct.read_trajectory_enabled(root):
        print("gen_trajectory: off (docs/trajectory-check) — nothing to render.")
        return 0

    wis, integrity = ct.load_wis(ct.read_rows(root / ct.WI_CSV))
    if not wis and not integrity:
        print(
            "gen_trajectory: no work items (placeholder-only or absent registry) — "
            "nothing to render; vacuously clean."
        )
        return 0

    errors = integrity + ct.validate(wis, ct.load_known_srs(root))
    if errors:
        for e in errors:
            print("gen_trajectory: ERROR - {}".format(e), file=sys.stderr)
        return 1

    generated = build_html(root, wis)
    out = root / OUT_HTML
    if args.check:
        current = out.read_text(encoding="utf-8") if out.exists() else None
        # The as-of stamp is excluded from the freshness compare (see ASOF_RE):
        # content gates byte-exact, the stamp is informational.
        if current is None or ASOF_RE.sub("", current) != ASOF_RE.sub("", generated):
            print(
                "project-state dashboard STALE in {}: run `python "
                "scripts/gen_trajectory.py`".format(OUT_HTML),
                file=sys.stderr,
            )
            return 1
        print("project-state dashboard up to date.")
        return 0

    if out.exists() and out.read_text(encoding="utf-8") == generated:
        print("gen_trajectory: already up to date -> {}".format(OUT_HTML))
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        # newline="\n" via open() (write_text(newline=) is 3.10+, floor is 3.8):
        # LF on every OS, so byte-stability doesn't rest on a downstream
        # .gitattributes eol=lf rule surviving.
        with out.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(generated)
        print("gen_trajectory: wrote {}".format(OUT_HTML))
    return 0


if __name__ == "__main__":
    sys.exit(main())
