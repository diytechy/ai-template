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

Deterministic by construction (sorted inputs, fixed layout passes, no clocks;
the as-of stamp derives from the last source-touching *commit*), so the
`--check` freshness gate is byte-stable — like `gen_arch_map.py --check`.

Stdlib only. Usage:  python scripts/gen_trajectory.py [--root .] [--check]
  (default)  regenerate PROJECT_STATE.html when the sources changed.
  --check    validate + verify freshness without writing; nonzero exit if the
             registry is invalid or the committed HTML is stale.
An absent or placeholder-only registry renders nothing and passes vacuously (the
opt-out layer stays free for a repo that never adopts it).
Exit codes: 0 clean / vacuous / opted-out, 1 invalid registry or stale HTML.
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
# absent, so fall back to adding this file's directory explicitly. See
# THREAD_52_REVIEW.md F5.
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
    `-000`, one didn't), which rendered a phantom SN-000 root in the icicle
    (REVIEW_GRIND_FULL C6). Change both together."""
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


TIER_FILL = {"sn": "#6366f1", "sr": "#0891b2", "llr": "#64748b", "tc": "#059669"}
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
    # `_dag_ranks` / `check_trajectory._cycles` which walk the unbounded WI chain
    # (THREAD_52_REVIEW.md F4). Kept recursive so this block stays a faithful port
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

    def esc(s):
        return html.escape(str(s), quote=True)

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
        cells.append(
            '<g class="cell {}" data-id="{}" tabindex="0">'
            '<rect x="{}" y="{:.1f}" width="{}" height="{:.1f}" rx="3" '
            'fill="{}"></rect>{}</g>'.format(
                t, esc(nid), x, y, col_w, max(h - 1, 1), TIER_FILL[t], txt
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
STATUS_FILL = {"done": "#059669", "active": "#d97706", "queued": "#94a3b8"}


def _dag_ranks(wis, pred_map):
    """Longest-path layering: a node's rank is one past its deepest predecessor
    (a source is rank 0). The graph is validated acyclic before we get here.

    Iterative post-order (explicit stack), not recursion: a deep dependency chain
    would blow CPython's ~1000-frame limit and raise ``RecursionError`` instead of
    a rendered dashboard (THREAD_52_REVIEW.md F4). ``on_path`` tracks the nodes on
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


def _dag_layout(wis):
    """Return (positions, ranks, order) for the work items.

    Stages (Sugiyama-lite, deterministic): rank by longest path over **hard**
    edges (soft edges are advisory — they never constrain rank); seed each rank's
    order by (workstream, id) to keep workstreams clustered; run a fixed number of
    barycentre sweeps (down then up) to reduce edge crossings; assign coordinates,
    centring each rank vertically against the tallest one."""
    ids = {w["id"] for w in wis}
    by_id = {w["id"]: w for w in wis}
    pred_map = {w["id"]: [p for p in w["preds"] if p in ids] for w in wis}
    succ_map = {w["id"]: [] for w in wis}
    for w in wis:
        for p in pred_map[w["id"]]:
            succ_map[p].append(w["id"])

    rank = _dag_ranks(wis, pred_map)
    nranks = (max(rank.values()) + 1) if rank else 0
    order = {}
    for r in range(nranks):
        order[r] = sorted(
            (nid for nid in ids if rank[nid] == r),
            key=lambda n: (by_id[n]["workstream"], n),
        )
    for _ in range(4):
        for r in range(1, nranks):
            _reorder(order, r, pred_map, order[r - 1])
        for r in range(nranks - 2, -1, -1):
            _reorder(order, r, succ_map, order[r + 1])

    max_rows = max((len(order[r]) for r in order), default=0)
    content_h = max_rows * DAG_ROW_H + max(max_rows - 1, 0) * DAG_ROW_GAP
    pos = {}
    for r in range(nranks):
        layer = order[r]
        n = len(layer)
        layer_h = n * DAG_ROW_H + max(n - 1, 0) * DAG_ROW_GAP
        y0 = DAG_PAD + (content_h - layer_h) / 2
        x = DAG_PAD + r * (DAG_COL_W + DAG_COL_GAP)
        for i, nid in enumerate(layer):
            pos[nid] = (x, y0 + i * (DAG_ROW_H + DAG_ROW_GAP))
    width = DAG_PAD * 2 + nranks * DAG_COL_W + max(nranks - 1, 0) * DAG_COL_GAP
    height = DAG_PAD * 2 + content_h
    return pos, width, height


def dag_svg(wis):
    """The work-item DAG as one plain SVG string + a details dict for the panel."""
    ids = {w["id"] for w in wis}
    pos, width, height = _dag_layout(wis)

    def esc(s):
        return html.escape(str(s), quote=True)

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
                esc(w["id"]),
                x + DAG_COL_W / 2,
                esc(short),
            )
        )
        nodes.append(
            '<g class="wi {}" data-id="{}" tabindex="0">'
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="7" '
            'fill="{}"></rect>{}</g>'.format(
                st, esc(w["id"]), x, y, DAG_COL_W, DAG_ROW_H, STATUS_FILL[st], label
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


HTML_TEMPLATE = string.Template("""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$project — Project State</title>
<style>
  :root {
    color-scheme: light dark;
    --bg:#f8fafc; --surface:#ffffff; --border:#e2e8f0; --text:#0f172a;
    --muted:#64748b; --accent:#4f46e5;
    --done:#059669; --active:#d97706; --queued:#94a3b8;
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
  nav.tabs { display:flex; gap:.25rem; margin:2rem 0 0; border-bottom:1px solid var(--border); }
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
  #ice .cell rect { stroke:rgba(255,255,255,.35); stroke-width:.5; cursor:pointer;
        transition:opacity .1s ease; }
  #ice .cell text { fill:#fff; font-size:10px; pointer-events:none; }
  #ice .cell .sub { font-size:8.5px; opacity:.85; }
  #ice .lane-head { fill:var(--muted); font-size:11px; font-weight:700; letter-spacing:.06em; }
  .cell.dim, .wi.dim, .edge.dim { opacity:.15; }
  #ice .cell.hl rect { stroke:#f59e0b; stroke-width:2.5; }
  .cell:focus, .wi:focus { outline:none; }
  #dag .wi rect { stroke:rgba(15,23,42,.15); stroke-width:1; cursor:pointer;
        transition:opacity .1s ease; }
  #dag .wi text { fill:#fff; pointer-events:none; }
  #dag .wi .wid { font-size:10px; font-weight:700; }
  #dag .wi .sub { font-size:8.5px; opacity:.9; }
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
  .detail .badge { display:inline-block; font-size:.68rem; font-weight:700;
        text-transform:uppercase; letter-spacing:.05em; padding:.15rem .5rem;
        border-radius:6px; color:#fff; }
  .detail h3 { font-size:.98rem; margin:.55rem 0 .35rem; letter-spacing:-.01em; }
  .detail .status { color:var(--muted); font-size:.8rem; margin:0 0 .5rem; }
  .detail .body { color:var(--text); margin:.2rem 0; }
  .detail .meta { color:var(--muted); font-size:.83rem; margin-top:.6rem;
        border-top:1px solid var(--border); padding-top:.55rem; }
  @media (max-width:760px){ .layout{ grid-template-columns:1fr; }
        .detail{ max-height:none; } }
  .legend { display:flex; flex-wrap:wrap; gap:1rem; margin-top:.9rem;
            font-size:.85rem; color:var(--muted); }
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
        <div id="ice" class="view">$arch_svg</div>
        <aside id="arch-detail" class="detail"><p class="hint">Hover to highlight a subtree;
          click a block to read its full text — requirement, acceptance, status.</p></aside>
      </div>
      <div class="legend">
        <span><i style="background:#6366f1"></i>SN</span>
        <span><i style="background:#0891b2"></i>SR</span>
        <span><i style="background:#64748b"></i>LLR</span>
        <span><i style="background:#059669"></i>TC</span>
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
        <div id="dag" class="view">$dag_svg</div>
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
        '<span class="badge" style="background:'+tierColor+'">'+esc(d.tier||d.status)+'</span>'
        + '<h3>'+esc(id)+(d.title?' — '+esc(d.title):'')+'</h3>'
        + (d.status&&d.tier?'<p class="status">'+esc(d.status)+'</p>':'')
        + '<p class="body">'+esc(d.body)+'</p>'
        + (d.meta?'<p class="meta">'+esc(d.meta)+'</p>':'');
    }
    const tierColor = { sn:'#6366f1', sr:'#0891b2', llr:'#64748b', tc:'#059669' };
    const statusColor = { done:'#059669', active:'#d97706', queued:'#94a3b8' };

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


def _sw_panel(mods):
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
    panel = (
        '<section id="sw" class="panel">\n<h2>Software architecture (How)</h2>\n'
        '<p class="cap">The module map from <code>docs/architecture.md</code> — a view '
        "of the generated code map (its <code>--check</code> keeps it honest against "
        "the AST), unified here so one artifact answers What, How and When.</p>\n"
        '<div style="overflow:auto"><table class="swmap"><thead><tr>'
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
        '<div style="overflow:auto"><table class="swmap"><thead><tr>'
        "<th>CMP</th><th>Name</th><th>Category</th><th>State</th><th>PartOf</th>"
        "</tr></thead><tbody>{}</tbody></table></div>\n</section>".format("".join(body))
    )
    return tab, panel


def build_html(root, wis):
    total = len(wis)
    done = sum(1 for w in wis if w["status"] == "done")
    active = sum(1 for w in wis if w["status"] == "active")
    stats = spine_stats(root)
    workstreams = len({w["workstream"] for w in wis})
    arch, arch_details, arch_desc = arch_icicle(root)
    dag, wi_details = dag_svg(wis)
    extra_tabs, extra_panels = [], []
    mods = sw_modules(root)
    if mods:
        tab, panel = _sw_panel(mods)
        extra_tabs.append(tab)
        extra_panels.append(panel)
    cmps = cmp_rows(root)
    if cmps:
        tab, panel = _cmp_panel(cmps)
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
        arch_svg=arch,
        arch_details=j(arch_details),
        arch_desc=j(arch_desc),
        dag_svg=dag,
        wi_details=j(wi_details),
    )


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
        help="validate + verify freshness without writing (nonzero on stale/invalid)",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

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
        # .gitattributes eol=lf rule surviving (REVIEW_GRIND_FULL C7).
        with out.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(generated)
        print("gen_trajectory: wrote {}".format(OUT_HTML))
    return 0


if __name__ == "__main__":
    sys.exit(main())
