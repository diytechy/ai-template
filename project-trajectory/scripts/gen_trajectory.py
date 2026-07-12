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

Contracts: IF-011, IF-024 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
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


TRACE_CARD_W, TRACE_CARD_H, TRACE_COL_GAP, TRACE_ROW_GAP, TRACE_PAD = (
    214,
    54,
    82,
    14,
    34,
)


def trace_flow_svg(root):
    """Uniform-card four-column trace graph preserving every valid parent."""
    details, tier, parents, children = {}, {}, {}, {}

    def add(nid, kind, title, body, meta="", status=""):
        details[nid] = {
            "tier": kind,
            "title": title,
            "body": body,
            "meta": meta,
            "status": status,
        }
        tier[nid] = kind
        parents.setdefault(nid, [])
        children.setdefault(nid, [])

    def link(parent, child):
        if parent in details and child in details and child not in children[parent]:
            children[parent].append(child)
            parents[child].append(parent)

    sns = _sn_rows(root)
    for row in sns:
        add(
            row["id"],
            "sn",
            row["need"],
            row["need"],
            "Why: {} · Acceptance: {}".format(row["why"], row["acceptance"]),
        )
    sn_ids = {r["id"] for r in sns}
    srs = [
        r
        for r in ct.read_rows(root / ct.SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    ]
    for row in srs:
        sid = row["SR-ID"].strip()
        phase = (row.get("Phase") or "").strip()
        add(
            sid,
            "sr",
            (row.get("Title") or "").strip(),
            (row.get("Requirement") or "").strip(),
            "Phase: {} · Acceptance: {}".format(
                phase or "—", (row.get("AcceptanceCriteria") or "").strip()
            ),
            (row.get("Status") or "").strip(),
        )
    sr_ids = {r["SR-ID"].strip() for r in srs}
    for row in srs:
        for parent in ct._split_refs(row.get("SN-Refs", "")):
            if parent in sn_ids:
                link(parent, row["SR-ID"].strip())
    llrs = [
        r
        for r in ct.read_rows(root / "docs/requirements/low-level-requirements.csv")
        if (r.get("LLR-ID") or "").startswith("LLR-")
    ]
    for row in llrs:
        add(
            row["LLR-ID"].strip(),
            "llr",
            (row.get("Title") or "").strip(),
            (row.get("Detail") or "").strip(),
            "Module: {}".format((row.get("Module") or "").strip()),
            (row.get("Status") or "").strip(),
        )
    llr_ids = {r["LLR-ID"].strip() for r in llrs}
    for row in llrs:
        for parent in ct._split_refs(row.get("SR-Refs", "")):
            if parent in sr_ids:
                link(parent, row["LLR-ID"].strip())
    tcs = [
        r
        for r in ct.read_rows(root / "docs/test/test-cases.csv")
        if (r.get("TC-ID") or "").startswith("TC-")
    ]
    for row in tcs:
        verifies = ct._split_refs(row.get("Verifies", ""))
        add(
            row["TC-ID"].strip(),
            "tc",
            "verifies {}".format("; ".join(verifies)),
            (row.get("Expected") or "").strip(),
            "Method: {}".format((row.get("Method") or "").strip()),
            (row.get("Status") or "").strip(),
        )
    for row in tcs:
        for parent in ct._split_refs(row.get("Verifies", "")):
            if parent in llr_ids or parent in sr_ids:
                link(parent, row["TC-ID"].strip())
    for nid in details:
        details[nid]["meta"] += " · Parents: {} · Children: {}".format(
            ", ".join(sorted(parents[nid])) or "—",
            ", ".join(sorted(children[nid])) or "—",
        )

    kinds = ("sn", "sr", "llr", "tc")
    columns = {kind: sorted(n for n in tier if tier[n] == kind) for kind in kinds}
    max_rows = max((len(v) for v in columns.values()), default=1)
    content_h = max_rows * TRACE_CARD_H + max(max_rows - 1, 0) * TRACE_ROW_GAP
    pos = {}
    for col, kind in enumerate(kinds):
        lane_h = (
            len(columns[kind]) * TRACE_CARD_H
            + max(len(columns[kind]) - 1, 0) * TRACE_ROW_GAP
        )
        y0 = TRACE_PAD + (content_h - lane_h) / 2
        x = TRACE_PAD + col * (TRACE_CARD_W + TRACE_COL_GAP)
        for index, nid in enumerate(columns[kind]):
            pos[nid] = (x, y0 + index * (TRACE_CARD_H + TRACE_ROW_GAP))

    def esc(value):
        return html.escape(str(value), quote=True)

    edges = []
    for source in sorted(children):
        for target in sorted(children[source]):
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            sx, sy, tx, ty = (
                x1 + TRACE_CARD_W,
                y1 + TRACE_CARD_H / 2,
                x2,
                y2 + TRACE_CARD_H / 2,
            )
            mid = (sx + tx) / 2
            edges.append(
                '<path class="trace-edge" data-src="{}" data-tgt="{}" d="M{:.1f},{:.1f} H{:.1f} V{:.1f} H{:.1f}" marker-end="url(#trace-arrow)"></path>'.format(
                    esc(source), esc(target), sx, sy, mid, ty, tx
                )
            )
    cards = []
    for nid in sorted(details, key=lambda n: (TIER_COL[tier[n]], n)):
        x, y = pos[nid]
        kind, title = tier[nid], details[nid]["title"] or ""
        short = title if len(title) <= 28 else title[:27] + "…"
        draft = details[nid]["status"].lower() == "draft"
        cards.append(
            '<g class="cell {}{}" data-id="{}" tabindex="0" role="button" aria-label="{} {}{}"><rect class="trace-card" x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="8"></rect><rect class="trace-accent" x="{:.1f}" y="{:.1f}" width="5" height="{}" rx="2" fill="{}"></rect><text x="{:.1f}" y="{:.1f}"><tspan class="wid">{}</tspan><tspan x="{:.1f}" dy="17" class="sub">{}</tspan>{}</text></g>'.format(
                kind,
                " draft" if draft else "",
                esc(nid),
                kind.upper(),
                esc(nid),
                " Draft" if draft else "",
                x,
                y,
                TRACE_CARD_W,
                TRACE_CARD_H,
                x,
                y,
                TRACE_CARD_H,
                TIER_FILL[kind],
                x + 14,
                y + 20,
                esc(nid),
                x + 14,
                esc(short),
                '<tspan x="{:.1f}" dy="15" class="state">DRAFT</tspan>'.format(
                    x + TRACE_CARD_W - 54
                )
                if draft
                else "",
            )
        )
    width = 2 * TRACE_PAD + 4 * TRACE_CARD_W + 3 * TRACE_COL_GAP
    height = content_h + 2 * TRACE_PAD
    lanes = []
    for col, kind in enumerate(kinds):
        x = TRACE_PAD + col * (TRACE_CARD_W + TRACE_COL_GAP) - 10
        lanes.append(
            '<rect class="trace-lane" x="{:.1f}" y="8" width="{}" height="{:.1f}" rx="10"></rect><text class="lane-head" x="{:.1f}" y="26">{} · {}</text>'.format(
                x,
                TRACE_CARD_W + 20,
                height - 16,
                x + 10,
                kind.upper(),
                len(columns[kind]),
            )
        )
    defs = '<defs><marker id="trace-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z"></path></marker></defs>'
    svg = '<svg class="traceflow" viewBox="0 0 {:.0f} {:.0f}" width="{:.0f}" preserveAspectRatio="xMinYMin meet" role="img" aria-label="Complete SN to SR to LLR to TC traceability flow">{}{}{}{}</svg>'.format(
        width, height, width, defs, "".join(lanes), "".join(edges), "".join(cards)
    )
    descendants = {}
    for nid in details:
        seen, stack = set(), list(children[nid])
        while stack:
            child = stack.pop()
            if child not in seen:
                seen.add(child)
                stack.extend(children.get(child, []))
        descendants[nid] = sorted(seen)
    return svg, details, descendants


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


# --- the How-SW interface graph (WI-056), reusing the WI-DAG layouter -----------

SW_NODE_FILL = {"module": "#0891b2", "file": "#7c3aed", "external": "#64748b"}
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

    def esc(s):
        return html.escape(str(s), quote=True)

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
        node_svg.append(
            '<g><rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="6" '
            'fill="{}"></rect><text x="{:.1f}" y="{:.1f}" text-anchor="middle" '
            'dominant-baseline="central" fill="#fff" font-size="10">{}</text>'
            "</g>".format(
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

SW_CONTAINMENT_STYLE = (
    "<style>"
    "#sw .cmptree{margin-top:.4rem;}"
    "#sw details.cmpbox{border:1px solid var(--border);border-radius:10px;"
    "margin:.45rem 0;background:var(--surface);box-shadow:var(--shadow);}"
    "#sw details.cmpbox>summary{cursor:pointer;font-weight:600;padding:.6rem .8rem;"
    "list-style-position:inside;}"
    "#sw details.cmpbox>summary .sub{font-weight:400;color:var(--muted);}"
    "#sw .cmpbody{padding:.1rem .85rem .7rem;}"
    "#sw details.cmpbox details.cmpbox{margin-left:.7rem;}"
    "#sw .uncontained{padding:.5rem .8rem;border:1px dashed var(--border);"
    "border-radius:10px;margin:.35rem 0;}"
    "#sw ul.xseams,#sw ul.cmpseams{margin:.2rem 0 .7rem;padding-left:1.3rem;"
    "font-size:.9rem;}"
    "#sw ul.xseams li,#sw ul.cmpseams li{margin:.1rem 0;}"
    "#sw table.swmap{margin:.35rem 0;}"
    "</style>"
)


def sw_containment(root, mods):
    """The containerized How-SW top view (WI-073), or None when no `CMP-###`
    component contains an arch-map module (the caller then keeps today's flat
    panel, byte-identical). Returns `(tab, panel)`.

    The top view is a native `<details>` tree of the top-level components plus the
    uncontained modules; each component expands to its member modules, its nested
    child components, and the interface seams internal to it. IF seams whose
    endpoints fall in two different top-level items render once as an aggregated
    component-to-component edge at the top level. Deterministic (sorted inputs, no
    clocks), so the `--check` freshness compare stays byte-stable."""
    view = ct.component_top_view(root)
    if not view["top_roots"]:
        return None

    by_id = view["by_id"]
    children_of = view["children_of"]
    module_cmps = view["module_cmps"]
    module_roots = view["module_roots"]
    inv = view["inventory"]  # {norm: display}
    mod_by_norm = {ct._norm_module(m["name"]): m for m in mods}

    def esc(s):
        return html.escape(str(s), quote=True)

    # A module's DIRECT container(s) = the finest CMP(s) its LLRs tag; a coarser
    # ancestor contains it through PartOf (rendered as the nested tree).
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

    def item_keys(norm):
        """The top-level item key(s) a module falls under: its top-level CMP
        root(s) when contained, else its own `mod:` key when it is an uncontained
        inventory module, else empty (a file/external endpoint is not a top item)."""
        if module_roots.get(norm):
            return set(module_roots[norm])
        if norm in inv:
            return {"mod:" + norm}
        return set()

    # Classify every declared seam into: cross-component edges (deduped to the
    # boundary), per-component intra seams, and per-component boundary seams
    # (to a file/external hub).
    cross, intra, boundary = {}, {}, {}
    for r in ct.load_ifs(ct.read_rows(root / ct.IF_CSV)):
        tk, tkey, tdisp = _sw_node(r["this"], inv)
        ck, ckey, cdisp = _sw_node(r["counterpart"], inv)
        if r["direction"] == "consumes":  # flip so producer -> consumer
            (pk, pkey, pdisp), (nk, nkey, ndisp) = (ck, ckey, cdisp), (tk, tkey, tdisp)
        else:
            (pk, pkey, pdisp), (nk, nkey, ndisp) = (tk, tkey, tdisp), (ck, ckey, cdisp)
        iid = r["id"]
        pnorm = pkey.split(":", 1)[1] if pk == "module" else None
        nnorm = nkey.split(":", 1)[1] if nk == "module" else None
        pkeys = item_keys(pnorm) if pnorm else set()
        nkeys = item_keys(nnorm) if nnorm else set()
        if pkeys and nkeys:
            for a in sorted(pkeys):
                for b in sorted(nkeys):
                    if a == b:
                        if a.startswith("CMP-"):
                            intra.setdefault(a, set()).add((iid, pdisp, ndisp))
                    else:
                        cross.setdefault((a, b), set()).add(iid)
        else:  # one endpoint is a file/external hub -> a boundary seam
            mnorm = (
                pnorm
                if module_roots.get(pnorm)
                else (nnorm if module_roots.get(nnorm) else None)
            )
            if mnorm:
                for a in module_roots[mnorm]:
                    boundary.setdefault(a, set()).add((iid, pdisp, ndisp))

    def label_key(k):
        if k.startswith("CMP-"):
            nm = by_id.get(k, {}).get("name", "")
            return "{} — {}".format(k, nm) if nm else k
        return k.split(":", 1)[1]

    def mod_rows(norms):
        out = []
        for n in norms:
            m = mod_by_norm.get(n)
            if not m:
                out.append(
                    "<tr><td><code>{}</code></td><td>—</td><td>—</td></tr>".format(
                        esc(inv.get(n, n))
                    )
                )
                continue
            syms = ", ".join(m["symbols"][:8]) + ("…" if len(m["symbols"]) > 8 else "")
            out.append(
                "<tr><td><code>{}</code></td><td>{}</td><td>{}<br>"
                '<span class="sub"><code>{}</code></span></td></tr>'.format(
                    esc(m["name"]), len(m["symbols"]), esc(m["summary"]), esc(syms)
                )
            )
        return "".join(out)

    def module_table(norms):
        if not norms:
            return ""
        return (
            '<table class="swmap"><thead><tr><th>Module</th><th>Public</th>'
            "<th>Summary · symbols</th></tr></thead><tbody>{}</tbody>"
            "</table>".format(mod_rows(norms))
        )

    def seam_block(cid):
        items = []
        for iid, a, b in sorted(intra.get(cid, set())):
            items.append(
                "<li><code>{}</code>: {} → {}</li>".format(esc(iid), esc(a), esc(b))
            )
        for iid, a, b in sorted(boundary.get(cid, set())):
            items.append(
                '<li><code>{}</code>: {} → {} <span class="sub">(boundary)</span>'
                "</li>".format(esc(iid), esc(a), esc(b))
            )
        if not items:
            return ""
        return (
            '<p class="sub" style="margin:.5rem 0 .1rem">Seams within this '
            'component:</p><ul class="cmpseams">{}</ul>'.format("".join(items))
        )

    def render_cmp(cid, seams):
        kids = [c for c in children_of.get(cid, []) if subtree_modules(c)]
        body = "".join(render_cmp(c, "") for c in kids)
        body += module_table(direct.get(cid, []))
        body += seams
        nm = by_id.get(cid, {}).get("name", "")
        n = len(subtree_modules(cid))
        head = '<code>{}</code>{} <span class="sub">· {} module(s)</span>'.format(
            esc(cid), " — " + esc(nm) if nm else "", n
        )
        return (
            '<details class="cmpbox"><summary>{}</summary>'
            '<div class="cmpbody">{}</div></details>'.format(head, body)
        )

    tab = '<button data-tab="sw">How (SW architecture)</button>'
    start_level = "component" if len(view["top_roots"]) > 3 else "module"
    tree = "".join(render_cmp(r, seam_block(r)) for r in view["top_roots"])
    unc = "".join(
        '<div class="uncontained"><code>{}</code> '
        '<span class="sub">— uncontained: no Component tag on its LLR(s)</span>'
        "</div>".format(esc(inv.get(n, n)))
        for n in view["uncontained"]
    )
    xlines = "".join(
        "<li><code>{}</code> → <code>{}</code> "
        '<span class="sub">({})</span></li>'.format(
            esc(label_key(a)), esc(label_key(b)), esc(", ".join(sorted(iids)))
        )
        for (a, b), iids in sorted(cross.items())
    )
    cross_html = (
        '<p class="cap">Cross-component seams — aggregated to the boundary (one '
        "edge per crossing pair; the module-level seams live inside each "
        'component):</p><ul class="xseams">{}</ul>'.format(xlines)
        if xlines
        else ""
    )
    summary_line = (
        '<p class="cap"><strong>Top view: {} item(s)</strong> — {} top-level '
        "component(s) + {} uncontained module(s); bounded at {} "
        '(process-options.md "Component layer"). Software items are '
        "<strong>containerized</strong> into the component they belong to; "
        "<strong>drill into</strong> a component to reveal its members and internal "
        "seams.</p>".format(
            view["count"],
            len(view["top_roots"]),
            len(view["uncontained"]),
            ct.TOP_VIEW_MAX,
        )
    )
    panel = (
        '<section id="sw" class="panel">\n<h2>Software architecture (How)</h2>\n'
        + SW_CONTAINMENT_STYLE
        + "\n"
        + summary_line
        + cross_html
        + '<div class="cmptree" data-hierarchy="component-module" data-start-level="{}" '
        'aria-label="Component to module software hierarchy">'.format(start_level)
        + tree
        + unc
        + "</div>\n</section>"
    )
    return tab, panel


# --- the campaign-binned When view (WI-074) ------------------------------------
#
# The WHEN-axis mirror of the HOW-axis FB5 containment above: work items sharing a
# `Campaign` grouping tag containerize into a collapsed <details> box (expandable
# to their member rows), campaign-crossing predecessor edges aggregate to one
# deduplicated container-to-container edge (contributing WI edges listed), and a
# campaign-less WI renders flat. Reuses the sw_containment idiom (native
# <details>, boundary-aggregated edges, sorted-input determinism -> byte-stable
# through --check). When NO work item carries a campaign this returns None and
# the caller keeps today's flat SVG DAG, so a campaign-less registry renders
# byte-identically. There is deliberately NO right-sizing bound here (the FB5
# asymmetry): a campaign is bounded by construction — one re-attestation sitting's
# worth of WIs — so binning is presentation only, no new gate.

CAMPAIGN_STYLE = (
    "<style>"
    "#dag .camptree{margin-top:.2rem;}"
    "#dag details.campbox{border:1px solid var(--border);border-radius:10px;"
    "margin:.45rem 0;background:var(--surface);box-shadow:var(--shadow);}"
    "#dag details.campbox>summary{cursor:pointer;font-weight:600;padding:.55rem .8rem;"
    "list-style-position:inside;}"
    "#dag details.campbox>summary .sub{font-weight:400;color:var(--muted);}"
    "#dag .campbody{padding:.1rem .85rem .6rem;}"
    "#dag table.witable{border-collapse:collapse;width:100%;font-size:.85rem;"
    "margin:.3rem 0;}"
    "#dag table.witable th,#dag table.witable td{text-align:left;padding:.35rem .5rem;"
    "border-bottom:1px solid var(--border);vertical-align:top;}"
    "#dag table.witable .sub{color:var(--muted);}"
    "#dag .st{display:inline-block;width:.62rem;height:.62rem;border-radius:50%;"
    "vertical-align:-1px;margin-right:.35rem;}"
    "#dag ul.xcamp{margin:.2rem 0 .7rem;padding-left:1.3rem;font-size:.9rem;}"
    "#dag ul.xcamp li{margin:.1rem 0;}"
    "#dag .standalone{margin-top:.6rem;}"
    "</style>"
)


def campaign_containment(wis):
    """The campaign-binned When view (WI-074), or None when no work item carries a
    `Campaign` value (the caller then keeps today's flat SVG DAG, byte-identical).
    Returns the HTML string that fills the `dag` panel's view.

    Campaign members collapse into a native `<details>` container (expand to a
    member table); campaign-less WIs render flat below the containers; predecessor
    edges whose endpoints fall in two different top-level items (campaign or a
    standalone WI) aggregate to one deduplicated container-to-container edge at the
    top level, listing the contributing WI edges. Deterministic (sorted inputs, no
    clocks), so the `--check` freshness compare stays byte-stable."""
    by_camp = {}
    campaignless = []
    for w in wis:
        if w.get("campaign"):
            by_camp.setdefault(w["campaign"], []).append(w)
        else:
            campaignless.append(w)
    if not by_camp:
        return None

    ids = {w["id"] for w in wis}

    def esc(s):
        return html.escape(str(s), quote=True)

    # A top-level item key: the campaign slug when tagged, else `WI:<id>` (a
    # campaign-less WI is its own top-level item — the sw_containment "uncontained"
    # analogue). label() unwraps the `WI:` sentinel back to the bare id.
    key_of = {w["id"]: (w["campaign"] or "WI:" + w["id"]) for w in wis}

    def label(k):
        return k[len("WI:") :] if k.startswith("WI:") else k

    def st_of(w):
        return w["status"] if w["status"] in STATUS_FILL else "queued"

    def wi_row(w):
        st = st_of(w)
        delivers = ", ".join(w["srs"]) or "—"
        after = ", ".join(w["preds"] + ["~" + p for p in w["soft"]]) or "—"
        return (
            "<tr><td><code>{}</code></td><td>{}</td>"
            '<td><span class="st" style="background:{}"></span>{}</td>'
            '<td><code>{}</code></td><td class="sub"><code>{}</code></td></tr>'.format(
                esc(w["id"]),
                esc(w["title"]),
                STATUS_FILL[st],
                esc(st),
                esc(delivers),
                esc(after),
            )
        )

    def wi_table(members):
        rows = "".join(wi_row(w) for w in sorted(members, key=lambda w: w["id"]))
        return (
            '<table class="witable"><thead><tr><th>WI</th><th>Title</th>'
            "<th>Status</th><th>Delivers</th><th>After</th></tr></thead>"
            "<tbody>{}</tbody></table>".format(rows)
        )

    # Cross-boundary predecessor edges -> aggregate to one edge per crossing pair,
    # deduplicating the contributing WI edges (the FB5 boundary-aggregation idiom).
    cross = {}
    for w in wis:
        kw = key_of[w["id"]]
        for p in w["preds"] + w["soft"]:
            if p not in ids:
                continue
            kp = key_of[p]
            if kp != kw:
                cross.setdefault((kp, kw), set()).add((p, w["id"]))

    tree = ""
    for slug in sorted(by_camp):
        members = by_camp[slug]
        head = '<code>{}</code> <span class="sub">· {} item(s)</span>'.format(
            esc(slug), len(members)
        )
        tree += (
            '<details class="campbox"><summary>{}</summary>'
            '<div class="campbody">{}</div></details>'.format(head, wi_table(members))
        )

    standalone = ""
    if campaignless:
        standalone = (
            '<div class="standalone"><p class="sub" style="margin:.5rem 0 .2rem">'
            "Standalone work items — no campaign:</p>{}</div>".format(
                wi_table(campaignless)
            )
        )

    xlines = "".join(
        "<li><code>{}</code> → <code>{}</code> "
        '<span class="sub">({})</span></li>'.format(
            esc(label(a)),
            esc(label(b)),
            esc(", ".join("{}→{}".format(p, w) for p, w in sorted(edges))),
        )
        for (a, b), edges in sorted(cross.items())
    )
    cross_html = (
        '<p class="cap">Cross-campaign dependency edges — aggregated to the '
        "boundary (one edge per crossing pair; per-WI predecessors live in each "
        'member row\'s <em>After</em> column):</p><ul class="xcamp">{}</ul>'.format(
            xlines
        )
        if xlines
        else ""
    )
    summary_line = (
        '<p class="cap"><strong>Binned by campaign: {} campaign(s) + {} standalone '
        "work item(s).</strong> Work items sharing a <code>Campaign</code> tag are "
        "<strong>containerized</strong>; <strong>expand</strong> a campaign to "
        "reveal its members and the requirements they deliver. A campaign is "
        "bounded by construction (one re-attestation sitting), so there is no "
        "right-sizing bound here.</p>".format(len(by_camp), len(campaignless))
    )
    shell = (
        CAMPAIGN_STYLE
        + summary_line
        + cross_html
        + '<div class="camptree">'
        + tree
        + standalone
        + "</div>"
    )
    return shell


PHASE_TAG_RE = re.compile(r"\[([^\]]+)\]-\[g[0-3]\]", re.I)


def wi_phase_sets(root, wis):
    """Derive WI phase sets from SR rows and explicit [phase]-[gN] anchors."""
    sr_phase = {
        (r.get("SR-ID") or "").strip(): (r.get("Phase") or "").strip()
        for r in ct.read_rows(root / ct.SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    }
    out = {}
    for w in wis:
        phases = {sr_phase[s] for s in w["srs"] if sr_phase.get(s)}
        match = PHASE_TAG_RE.search(w["title"])
        if match:
            phases.add(match.group(1))
        out[w["id"]] = tuple(sorted(phases))
    return out


def when_hierarchy(root, wis):
    """Phase→workstream WI hierarchy with lifecycle frontier and Campaign mode."""
    phase_sets = wi_phase_sets(root, wis)
    groups, parked = {}, []
    for w in wis:
        if w["status"] == "deferred":
            parked.append(w)
            continue
        phases = phase_sets[w["id"]]
        phase = (
            phases[0] if len(phases) == 1 else ("Cross-phase" if phases else "Unphased")
        )
        groups.setdefault(phase, {}).setdefault(w["workstream"], []).append(w)
    if not any(phase_sets.values()) and not parked:
        return campaign_containment(wis)
    if not groups:
        return campaign_containment(wis)

    def esc(value):
        return html.escape(str(value), quote=True)

    def row(w):
        phases = phase_sets[w["id"]]
        badges = "".join(
            '<span class="phasebadge">{}</span>'.format(esc(p)) for p in phases
        )
        if not badges:
            badges = '<span class="phasebadge muted">Unphased</span>'
        campaign = (
            '<span class="campbadge">{}</span>'.format(esc(w["campaign"]))
            if w.get("campaign")
            else ""
        )
        after = ", ".join(w["preds"] + ["~" + p for p in w["soft"]]) or "—"
        return (
            '<tr class="wrow {}" data-wi="{}"><td><code>{}</code></td><td>{}<div>{}{}</div></td>'
            '<td><span class="statusbadge {}">{}</span></td><td class="sub"><code>{}</code></td></tr>'
        ).format(
            esc(w["status"]),
            esc(w["id"]),
            esc(w["id"]),
            esc(w["title"]),
            badges,
            campaign,
            esc(w["status"]),
            esc(w["status"]),
            esc(after),
        )

    def table(items):
        return (
            '<table class="witable"><thead><tr><th>WI</th><th>Work item</th><th>Status</th><th>After</th></tr></thead>'
            "<tbody>{}</tbody></table>"
        ).format("".join(row(w) for w in sorted(items, key=lambda x: x["id"])))

    phase_order = sorted(groups, key=lambda p: (p in ("Cross-phase", "Unphased"), p))
    active_phases = {
        phase
        for phase, streams in groups.items()
        if any(w["status"] == "active" for items in streams.values() for w in items)
    }
    frontier = next(iter(sorted(active_phases)), phase_order[-1] if phase_order else "")
    blocks = []
    for phase in phase_order:
        streams = groups[phase]
        total = sum(len(v) for v in streams.values())
        is_current = phase == frontier
        stream_html = []
        for name in sorted(streams):
            items = streams[name]
            stream_html.append(
                '<details class="streambox"{}><summary><span>{}</span><span class="sub">{} item(s)</span></summary>{}</details>'.format(
                    " open"
                    if is_current and any(w["status"] == "active" for w in items)
                    else "",
                    esc(WORKSTREAM_LABELS.get(name, name)),
                    len(items),
                    table(items),
                )
            )
        blocks.append(
            '<details class="phasebox{}"{} data-phase="{}"><summary><span class="phase-title">{}</span>'
            '<span class="sub">{} workstream(s) · {} item(s){}</span></summary><div class="phasebody">{}</div></details>'.format(
                " current" if is_current else "",
                " open" if is_current else "",
                esc(phase),
                esc(phase),
                len(streams),
                total,
                " · current delivery frontier" if is_current else "",
                "".join(stream_html),
            )
        )
    parked_html = (
        '<details class="parked"><summary>Parked / deferred <span class="sub">· {} item(s)</span></summary>{}</details>'.format(
            len(parked), table(parked)
        )
        if parked
        else ""
    )
    campaign = campaign_containment(wis)
    alternate = (
        '<details class="campaign-alt"><summary>Alternate grouping · Campaign</summary>{}</details>'.format(
            campaign
        )
        if campaign
        else ""
    )
    shell = (
        CAMPAIGN_STYLE
        + "<style>#dag .frontier{border-left:3px solid var(--active);padding-left:.8rem}"
        "#dag .phasebox,#dag .streambox,#dag .parked,#dag .campaign-alt{border:1px solid var(--border);border-radius:12px;margin:.55rem 0;background:var(--surface)}"
        "#dag .phasebox.current{border-color:var(--active);box-shadow:0 0 0 2px color-mix(in srgb,var(--active) 18%,transparent)}"
        "#dag .phasebox>summary,#dag .streambox>summary,#dag .parked>summary,#dag .campaign-alt>summary{cursor:pointer;display:flex;justify-content:space-between;gap:1rem;padding:.7rem .85rem;font-weight:650}"
        "#dag .phasebody,#dag .streambox table,#dag .parked table,#dag .campaign-alt>div{margin:.2rem .85rem .8rem}"
        "#dag .phasebadge,#dag .campbadge,#dag .statusbadge{display:inline-block;border-radius:999px;padding:.05rem .42rem;margin:.18rem .25rem 0 0;font-size:.7rem;border:1px solid var(--border)}"
        "#dag .campbadge{border-style:dashed}.statusbadge.active{color:#b45309}.statusbadge.done{color:#047857}.statusbadge.deferred{color:var(--muted)}"
        '</style><div class="whenhier"><p class="cap"><strong>Phase → Workstream → WI.</strong> The highlighted block marks the <strong>NOW · delivery frontier</strong> from phase/lifecycle state — not calendar time. Campaign remains an alternate grouping.</p>'
    )
    return shell + '<div class="frontier" data-frontier="{}">{}{}</div>{}</div>'.format(
        esc(frontier), "".join(blocks), parked_html, alternate
    )


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
  #ice .trace-lane { fill:var(--surface); stroke:var(--border); stroke-width:1.2;
        stroke-dasharray:5 5; }
  #ice .trace-edge { fill:none; stroke:#94a3b8; stroke-width:1.25; }
  #ice #trace-arrow path { fill:#94a3b8; }
  #ice .traceflow .trace-card { fill:var(--surface); stroke:var(--border); stroke-width:1; }
  #ice .traceflow .cell text { fill:var(--text); font-size:11px; text-anchor:start; }
  #ice .traceflow .cell .wid { font-weight:750; }
  #ice .traceflow .cell .sub { fill:var(--muted); font-size:9.5px; }
  #ice .traceflow .cell .state { fill:#b45309; font-size:8px; font-weight:800; }
  #ice .traceflow .cell.draft .trace-card { stroke:#d97706; stroke-dasharray:4 3; }
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
      <h2>Complete traceability flow</h2>
      <p class="cap">Every valid relationship in the <code>SN→SR→LLR→TC</code>
      spine, including secondary parents. Uniform cards keep dense tiers readable;
      dotted containers separate artifact kinds and arrows show direction.
      <strong>Hover or focus</strong> to highlight descendants; <strong>click</strong>
      to read full text, status, parents and children. Draft artifacts remain visible.</p>
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
        <div id="dag-view" class="view">$dag_svg</div>
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
            '<div class="view">{}</div>\n'.format(graph)
        )
    panel = (
        '<section id="sw" class="panel">\n<h2>Software architecture (How)</h2>\n'
        + graph_block
        + '<p class="cap">The module map from <code>docs/architecture.md</code> — a '
        "view of the generated code map (its <code>--check</code> keeps it honest "
        "against the AST), unified here so one artifact answers What, How and "
        'When.</p>\n<div style="overflow:auto"><table class="swmap"><thead><tr>'
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
    "Stakeholder Need": "#6366f1",
    "System Requirement": "#0891b2",
    "Low-Level Requirement": "#64748b",
    "Test Case": "#059669",
    "Interface": "#7c3aed",
    "Process Guide": "#d97706",
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

    def esc(s):
        return html.escape(str(s), quote=True)

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
        node_svg.append(
            '<g class="knode" data-id="{}" tabindex="0">'
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="6" '
            'fill="{}"></rect><text x="{:.1f}" y="{:.1f}" text-anchor="middle" '
            'dominant-baseline="central">{}</text></g>'.format(
                esc(k),
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
        "#knowgraph .knode text{fill:#fff;font-size:9px;pointer-events:none;}"
        "#knowgraph .knode.dim,#knowgraph .kedge.dim{opacity:.15;}"
        "#knowgraph .knode.hl rect{stroke:#f59e0b;stroke-width:2.5;}"
        "#knowgraph .kedge{fill:none;stroke:#94a3b8;stroke-width:1.2;}"
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
        '<div id="knowgraph" class="view">' + svg + "</div>\n"
        '<aside id="know-detail" class="detail"><p class="hint">Hover a concept to '
        "highlight its neighbourhood; click to read its description and open the "
        "full concept file in <code>docs/okf/</code>.</p></aside>\n"
        "</div>\n"
        '<div class="legend">' + legend + "</div>\n" + script + "\n</section>"
    )
    return tab, panel


def build_html(root, wis):
    total = len(wis)
    done = sum(1 for w in wis if w["status"] == "done")
    active = sum(1 for w in wis if w["status"] == "active")
    stats = spine_stats(root)
    workstreams = len({w["workstream"] for w in wis})
    arch, arch_details, arch_desc = trace_flow_svg(root)
    dag, wi_details = dag_svg(wis)
    # WI-074: when any work item carries a Campaign tag, the When view bins the
    # DAG into collapsed campaign containers (the WHEN-axis FB5 mirror); with no
    # campaign values this returns None and the flat SVG DAG renders unchanged, so
    # a campaign-less registry stays byte-identical.
    dag_view = when_hierarchy(root, wis) or dag
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
        dag_svg=dag_view,
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
        help="validate + verify freshness without writing (nonzero on "
        "stale/invalid). Missing-target posture (C9): a fully-generated "
        "output, so a missing file reads as stale — unlike arch-map, whose "
        "hand-authored target must exist",
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
