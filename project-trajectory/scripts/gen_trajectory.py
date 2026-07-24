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

Contracts: IF-011, IF-024, IF-052, IF-056, IF-071 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv). IF-071 (WI-290) is the frontier DECISION seam: gen_trajectory reads schedule.frontier for the generated STATUS block + Process-tab loop — distinct from IF-056's derivation-loader seam to check_trajectory (validate vs decide).
"""

import argparse
import html
import json
import math
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
# the hand-authored briefs). The block is emitted in two regions split by the
# PENDING_LOCAL_LABEL line: (a)+(d) are committed-tree-PURE and (b)+(c) plus the
# stranded-train shape are MACHINE-LOCAL (refs/llm-derived). Its `--check` gates
# only the pure region — the machine-local lines are generated for humans but
# excluded from the byte-compare, because `refs/llm/*` don't transport with
# clone/push, so gating them would read STALE in any second clone (M-10/WI-266);
# the same exclusion applies on every machine (one place: `_mask_machine_local`),
# so the harness `status-map` step and the post-integration re-run skip identical
# lines. Deterministic (sorted refs, no clocks), so the gated region is
# byte-stable. Opt-in: an open-items.md without the marker pair is left untouched.
OPEN_ITEMS_MD = "docs/open-items.md"
PENDING_BEGIN = "<!-- BEGIN GENERATED PENDING -->"
PENDING_END = "<!-- END GENERATED PENDING -->"
# The always-emitted lead of the machine-local ADVISORY sub-section of the
# PENDING block, and the stable boundary `_mask_machine_local` splits on so the
# `--status --check` freshness gate byte-compares ONLY the committed-tree-pure
# region (M-10/WI-266). Everything AFTER this exact-full-line — the refs/llm/*-
# derived conflict/reservation/quarantine/stranded lines — is generated for
# humans but excluded from the gate on every machine, because those refs do not
# transport with clone/push (a second clone reproduces empty). Kept as one line
# so the exact-full-line match holds; the label is itself gated (it sits at the
# boundary, inclusive) so the exclusion can't be silently edited away.
PENDING_LOCAL_LABEL = (
    "_Machine-local advisory — source conflicts, reservations, quarantines, and "
    "stranded-train attestations re-derived from `refs/llm/*` as of the dispatch "
    "machine at generation time. These refs do not transport with clone/push, so "
    "this section is regenerated every dispatch loop and is NOT part of the "
    "`--status --check` freshness gate (M-10/WI-266); a second clone (CI, another "
    "machine) may show it empty._"
)
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
# WI-267: `retired` is a TERMINAL WON'T-BUILD status with its OWN dashboard bucket
# — a muted stone hue byte-distinct from every other fill (done/active/queued and
# the drill tiers), never folded into done's green. deferred/blocked are not keyed
# here (they clamp to the queued fill in `_wi_st`); retired is, so a dead-end row
# reads as visibly terminal, not merely parked.
STATUS_FILL = {
    "done": "#047857",
    "active": "#b45309",
    "queued": "#94a3b8",
    "retired": "#78716c",
}
# A3 (no-info-by-color-alone): a redundant, shape-distinct status glyph paired with
# every status fill — the meaning survives without colour perception. Prefixed to a
# drill work-item block's label (and named in its hover title / detail). `retired`
# gets the circled-times ⊗ (a struck-out terminal), distinct from ✓/●/○.
STATUS_GLYPH = {"done": "✓", "active": "●", "queued": "○", "retired": "⊗"}

# WI-249 render-legibility fix (render-dashboard-critique found every wire's
# arrowhead invisible: some used a near-white fill (`var(--border)`, a light
# panel-hairline token never meant to carry a filled shape), the rest fixed a
# `strokeWidth`-scaled size so a 1.5px wire drew a triangle a couple of px
# across). One shared marker builder for every directed-edge graph on the
# dashboard (the WI DAG, the How-SW seam graph, the OKF concept graph, every
# `_drill_layer_svg` wire) — `userSpaceOnUse` sizing so the triangle stays a
# fixed, legible size regardless of the wire's stroke-width, and the path
# always takes a CSS class (never an inline fill) so it follows the same
# `--muted`/`--accent` theme tokens as its wire in both light and dark.
ARROW_SIZE = 9  # px, userSpaceOnUse — independent of any wire's stroke-width


def _arrow_markers(*specs):
    """`<defs>` wrapping one `<marker>` per spec: `(marker_id, css_class)`, or
    `(marker_id, css_class, size)` to override the default `ARROW_SIZE` (the
    `cedgearrow` containment marker renders a touch smaller)."""
    markers = "".join(
        '<marker id="{}" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="{sz}" markerHeight="{sz}" markerUnits="userSpaceOnUse" '
        'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
        'class="{}"></path></marker>'.format(
            esc(spec[0]), esc(spec[1]), sz=spec[2] if len(spec) > 2 else ARROW_SIZE
        )
        for spec in specs
    )
    return "<defs>{}</defs>".format(markers)


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
    # never constrained the ranking. A hub node's several edges fan out across
    # its side rather than bundling on the exact same pixel (`_port_fan`, the
    # same knot-avoidance the drill-layer wires use).
    wi_edges = [
        (p, w["id"], cls)
        for w in wis
        for p, cls in [(p, "edge") for p in w["preds"]]
        + [(p, "edge soft") for p in w["soft"]]
        if p in ids
    ]
    out_groups, in_groups = {}, {}
    for e in wi_edges:
        out_groups.setdefault(e[0], []).append(e)
        in_groups.setdefault(e[1], []).append(e)
    out_off = _port_fan(out_groups, lambda e: e[1], pos, DAG_ROW_H)
    in_off = _port_fan(in_groups, lambda e: e[0], pos, DAG_ROW_H)

    # A cross-rank edge that would cut an unrelated WI box detours around it
    # (`_route_edges`, WI-253); a clear edge keeps its bowed cubic byte-for-byte.
    rects = {
        w["id"]: (pos[w["id"]][0], pos[w["id"]][1], DAG_COL_W, DAG_ROW_H) for w in wis
    }
    routes = _route_edges(
        [
            (
                e,
                pos[e[0]][0] + DAG_COL_W,
                pos[e[0]][1] + DAG_ROW_H / 2 + out_off[e],
                pos[e[1]][0],
                pos[e[1]][1] + DAG_ROW_H / 2 + in_off[e],
                e[0],
                e[1],
            )
            for e in wi_edges
        ],  # fmt: skip
        rects,
        12,
        2,
    )
    edges = []
    for e in wi_edges:
        p, wid, cls = e
        edges.append(
            '<path class="{}" data-src="{}" data-tgt="{}" '
            'd="{}" marker-end="url(#arrow)"></path>'.format(
                cls, esc(p), esc(wid), routes[e]
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

    defs = _arrow_markers(("arrow", "arrowhead"))
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

    out_groups, in_groups = {}, {}
    for e in edges:
        out_groups.setdefault(e[0], []).append(e)
        in_groups.setdefault(e[1], []).append(e)
    out_off = _port_fan(out_groups, lambda e: e[1], pos, SW_ROW_H)
    in_off = _port_fan(in_groups, lambda e: e[0], pos, SW_ROW_H)

    rects = {k: (pos[k][0], pos[k][1], SW_COL_W, SW_ROW_H) for k in node_ids}
    routes = _route_edges(
        [
            (
                e,
                pos[e[0]][0] + SW_COL_W,
                pos[e[0]][1] + SW_ROW_H / 2 + out_off[e],
                pos[e[1]][0],
                pos[e[1]][1] + SW_ROW_H / 2 + in_off[e],
                e[0],
                e[1],
            )
            for e in edges
        ],  # fmt: skip
        rects,
        12,
        2,
    )
    edge_svg = []
    for e in sorted(edges):
        s, d, iid = e
        x1, y1 = pos[s][0] + SW_COL_W, pos[s][1] + SW_ROW_H / 2 + out_off[e]
        x2, y2 = pos[d][0], pos[d][1] + SW_ROW_H / 2 + in_off[e]
        mx, my = (x1 + (x2 - 2)) / 2, (y1 + y2) / 2
        lx, ly = _routed_label_xy(routes[e], mx, my)
        edge_svg.append(
            '<path class="swedge" d="{}" marker-end="url(#swarrow)"></path>'
            '<text class="swlab" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text>'
            "".format(routes[e], lx, ly - 2, esc(iid))
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
    defs = _arrow_markers(("swarrow", "swarrow-head"))
    style = (
        "<style>#sw .swedge{fill:none;stroke:var(--muted);stroke-width:1.4;}"
        "#sw .swarrow-head{fill:var(--muted);}"
        "#sw .swlab{fill:var(--muted);font-size:9px;}</style>"
    )
    return (
        '<svg viewBox="0 0 {:.0f} {:.0f}" width="{:.0f}" '
        'preserveAspectRatio="xMinYMin meet" role="img">{}{}{}{}</svg>'.format(
            width, height, width, defs, style, "".join(edge_svg), "".join(node_svg)
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
    """The containerized How-SW top view as a Simulink-style drill (SR-090..SR-092,
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
            "wrap": True,  # WI-246: wrap the `CMP-### — Name` label onto id/name lines
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
# Eight categorical hues, distinct hue-to-hue (was eight near-identical maroon/plum
# steps — WI-247, 075-CRITIQUE T5: adjacent phases were indistinguishable). Each is
# dark enough to carry WHITE block text (all >= 5.9:1 WCAG) and the set clears the
# `dataviz` skill's categorical validator on a white surface — chroma floor, adjacent
# CVD deltaE 9.6 (>= 8 target), normal-vision 18.8 (>= 15) — `validate_palette.js`,
# ordered so consecutive sorted phases sit far apart in hue.
#   These must NOT collide with the OTHER colour vocabularies on the When/DAG page
# (REVIEW-A MAJOR): every value is byte-distinct from STATUS_FILL (done #047857,
# active #b45309, queued #94a3b8 — the status legend on the same tab) and from
# TIER_FILL (#4338ca/#0e7490/#64748b/#047857), and each sits >= 11 deltaE from the
# three same-tab status hues, so a phase block never reads as a status. Excluding the
# emerald/orange/slate status families leaves the cool + magenta + one-red arc — hence
# the cool lean; distinct hues are preferred over same-hue lightness shades (the very
# jitter WI-247 removes), which caps CVD below the old maroon-free 20+.
PHASE_ACCENTS = (
    "#0369a1", "#6d28d9", "#991b1b", "#1d4ed8",
    "#be123c", "#4f46e5", "#be185d", "#7e22ce",
)  # fmt: skip

# --- SR-089..SR-092 (WI-141): the Simulink-style drill renderer ---------------
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
    # 080-CRITIQUE #5 (WI-258): the focus/highlight ring paints the --accent hue, NOT
    # the status-orange #b45309 it used to — that value is byte-identical to --active
    # ("active — you are here"), so a focused-but-not-active block misread as active.
    # --accent is the dashboard's focus language (cf. `.view:focus-visible`) and a
    # clearly different hue from active in BOTH themes; stroke-width 2.5 keeps it visible.
    ".drill .block:focus rect{stroke:var(--accent);stroke-width:2.5;}"
    # SR-056: the hover/focus highlight persists on the last-hovered block until
    # another takes it (the shared .hl idiom — cf. the icicle/DAG/knowledge views).
    ".drill .block.hl rect{stroke:var(--accent);stroke-width:2.5;}"
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
    # WI-256: a descend/crumb-nav swaps the visible layer, changing the outer
    # `.view` scrollWidth — refresh the overflow scroll cue for the new layer.
    "});if(window.__syncCues)window.__syncCues();}"
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


def _drill_block_label(b, col_w, cx, cy):
    """The centred `<text>` for one drill block. A plain label renders as the bold
    label line over its sub-label. A block flagged `wrap` with an `ID — Name` label
    (the CMP component blocks, "CMP-004 — Unattended loop & floor") WRAPS onto an id
    line over a name line — the `arch_icicle` id/name idiom (WI-246/075-CRITIQUE T4) —
    so the full component name reads at default zoom instead of truncating to
    "CMP-004 — Unattended…"; the sub-label (module count) drops to a third line. The
    name line uses the smaller sub font, so its budget (and the right-sized column)
    fit the longest declared name. The explicit `wrap` flag (not a `" — "` string
    sniff) keeps an incidental em-dash in some other block's name from wrapping."""
    fill = b.get("textfill", "var(--text)")
    head = '<text x="{:.1f}" y="{:.1f}" text-anchor="middle" fill="{}">'.format(
        cx, cy, fill
    )
    if b.get("wrap") and " — " in b["label"]:
        idpart, namepart = b["label"].split(" — ", 1)
        nbudget = max(1, (col_w - TIER_COL_PAD) // _BSUB_CH)
        if len(namepart) > nbudget:
            namepart = namepart[: nbudget - 1] + "…"
        return (
            head
            + '<tspan x="{:.1f}" dy="-11" class="blab">{}</tspan>'
            '<tspan x="{:.1f}" dy="11" class="bsub">{}</tspan>'
            '<tspan x="{:.1f}" dy="11" class="bsub">{}</tspan></text>'.format(
                cx, esc(idpart), cx, esc(namepart), cx, esc(b["sub"])
            )
        )
    max_label = max(1, (col_w - TIER_COL_PAD) // _BLAB_CH)
    main_label = b["label"]
    if len(main_label) > max_label:
        main_label = main_label[: max_label - 1] + "…"
    return (
        head
        + '<tspan x="{:.1f}" dy="-2" class="blab">{}</tspan>'
        '<tspan x="{:.1f}" dy="13" class="bsub">{}</tspan></text>'.format(
            cx, esc(main_label), cx, esc(b["sub"])
        )
    )


def _port_fan(groups, other_of, pos, row_h):
    """Per-port vertical fan-out offsets (keyed by edge tuple) so several wires
    sharing one port spread across a small band instead of converging on the
    exact same pixel — the "knot" a plain center-to-center wire draws when 3+
    edges share a port. Offsets are ordered by the OTHER endpoint's row (so a
    wire to a higher block leaves/lands higher), which also keeps neighbouring
    wires from needlessly crossing each other right at the port. A single-edge
    port gets offset 0 (byte-identical to the former center-only routing)."""
    offsets = {}
    for items in groups.values():
        n = len(items)
        if n <= 1:
            for e in items:
                offsets[e] = 0.0
            continue
        items_sorted = sorted(items, key=lambda e: (pos[other_of(e)][1], e))
        span = min(row_h * 0.6, (n - 1) * 6.0)
        step = span / (n - 1)
        start = -span / 2
        for i, e in enumerate(items_sorted):
            offsets[e] = start + i * step
    return offsets


# --- WI-253: obstacle-aware wire routing, single-sourced across every emitter ----
#
# Every layered view (the WI DAG, the How-SW seam/containment graph, the OKF
# knowledge graph, the drill layers) draws its wires as a horizontal-tangent
# cubic from a source OUTPUT port to a target INPUT port. A wire spanning more
# than one column — or any backward (right→left) seam — used to run straight
# through the intermediate node boxes and cross other wires under the port fans
# (T8 in dashboard-usability.md). These helpers detect a wire that would cut an
# unrelated box and re-route it through a clear horizontal LANE over/under the
# blocking band, entering each port on a short horizontal stub (crossings then
# happen in open space, never under a label or port cluster). A wire whose
# direct cubic is already clear keeps the legacy path byte-for-byte, so the many
# short in-column wires (and every downstream render) are unchanged.
# Deterministic: pure geometry, sorted inputs, no clocks, no dict-order use.

_WIRE_HIT_MARGIN = 3.0  # a box is "hit" only when the cubic comes within this
_WIRE_CLEAR = 7.0  # a detour lane sits this far outside the blocking band
_WIRE_STUB = 18.0  # the horizontal run a detour keeps at each port before lifting
_MAX_LANES = 24  # WI-257: candidate lanes tried per pass (bounds dense-overlap cost)


def _cubic_points(p0, p1, p2, p3, n=24):
    """Sample a cubic Bézier into n+1 points (deterministic polyline)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1.0 - t
        a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
        pts.append(
            (
                a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1],
            )
        )
    return pts


def _seg_hits_rect(x1, y1, x2, y2, rect):
    """True when the segment (x1,y1)->(x2,y2) crosses the axis-aligned rect
    (rx, ry, rw, rh). Liang–Barsky parametric clip — deterministic, no float
    surprises past the formatted 0.1px grid."""
    rx, ry, rw, rh = rect
    dx, dy = x2 - x1, y2 - y1
    p = (-dx, dx, -dy, dy)
    q = (x1 - rx, rx + rw - x1, y1 - ry, ry + rh - y1)
    t0, t1 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return False
        else:
            r = qi / pi
            if pi < 0:
                if r > t1:
                    return False
                t0 = max(t0, r)
            else:
                if r < t0:
                    return False
                t1 = min(t1, r)
    return t0 <= t1


def _polyline_hits(pts, rects):
    """True when any segment of the polyline `pts` crosses any rect in `rects`."""
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        for r in rects:
            if _seg_hits_rect(x1, y1, x2, y2, r):
                return True
    return False


def _lane_candidates(y_pref, blocked, lo, hi):
    """Clear-of-band y positions within [lo, hi], nearest y_pref FIRST. Bands are
    pre-inflated by the clearance, so a value just past a band edge already carries
    the margin. The head is exactly the former `_clear_lane_y` pick (a stable sort
    keeps the first candidate on distance ties), so a wire that already had a clear
    lane keeps it byte-for-byte; the tail lets `_detour_d` fall through to the next
    lane when the nearest one still grazes a stub-corridor box."""
    merged = []
    for t, b in sorted(blocked):
        if merged and t <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append([t, b])
    cands = [y_pref]
    for t, b in merged:
        cands.append(t - 0.1)
        cands.append(b + 0.1)
    valid = [
        c for c in cands if lo <= c <= hi and not any(t <= c <= b for t, b in merged)
    ]
    return sorted(valid, key=lambda c: abs(c - y_pref))


def _detour_points(x1, sy, y1, xa, xb, xe, ty, y2, lane):
    """The routed polyline a viewer's eye follows: source-port bend up to the lane,
    the straight lane segment, then the bend down into the target port. Samples the
    SAME two cubics `_detour_str` formats, so the hit-test and the emitted `d`
    describe one curve (the lane segment is the (xa,lane)->(xb,lane) hop between).
    `sy`/`ty` are the PORT-CENTER terminals (WI-256), `y1`/`y2` the fanned control
    heights — the wire lands on its port circle but still bows to its fan strand."""
    mx1, mx2 = (x1 + xa) / 2.0, (xb + xe) / 2.0
    pts = _cubic_points((x1, sy), (mx1, y1), (mx1, lane), (xa, lane))
    pts += _cubic_points((xb, lane), (mx2, lane), (mx2, y2), (xe, ty))
    return pts


def _detour_str(x1, sy, y1, xa, xb, xe, ty, y2, lane):
    """The detour `d` (two cubics + a straight lane hop). Terminals `sy`/`ty` sit on
    the port centers; the first/last control uses the fanned `y1`/`y2`. Byte-
    identical to the former inline format when a wire is unfanned (sy==y1, ty==y2)."""
    mx1, mx2 = (x1 + xa) / 2.0, (xb + xe) / 2.0
    return (
        "M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f} "
        "L{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}".format(
            x1,
            sy,
            mx1,
            y1,
            mx1,
            lane,
            xa,
            lane,
            xb,
            lane,
            mx2,
            lane,
            mx2,
            y2,
            xe,
            ty,
        )  # fmt: skip
    )


def _detour_d(
    x1, sy, y1, xe, ty, y2, obstacles, clearance=_WIRE_CLEAR, stub=_WIRE_STUB
):
    """A path 'd' that leaves the source port (x1, port-center sy) rightward, runs a
    clear horizontal lane over/under the blocking `obstacles`, and enters the target
    port (xe, port-center ty) on a short horizontal stub. `y1`/`y2` are the fanned
    control heights (WI-256: the terminal lands on the port circle, the bend keeps
    the fan strand). `obstacles` are (x,y,w,h) rects with the wire's own endpoints
    already removed.

    WI-255: the FULL routed polyline (both stubs, the two bends, and the lane) is
    re-verified clear of EVERY obstacle overlapping the routed x-span — a box
    sitting only in a port-stub corridor (formerly dropped from the lane search,
    letting the caller silently keep a through-box direct cubic) is now caught.
    Lanes are tried nearest the endpoint midline first, so an already-clear detour
    regenerates byte-for-byte; the first lane whose full polyline clears wins. When
    no lane is fully clear, the least-obstructed deterministic path is returned
    (never a silent through-box when a clear route exists within the searched
    lanes, and always terminating — the candidate set is finite). Returns None only
    when no obstacle sits in the routed span at all (caller keeps the direct cubic).

    WI-257 MINOR 1: the stubs reach xa = x1+stub / xb = xe-stub — up to `stub` px
    OUTSIDE [x1, xe] — so the obstacle span and the hit accounting cover the
    stub-EXTENDED range; a box sitting only in an outboard-stub zone is now
    hit-tested (formerly a residual fail-open). WI-257 MINOR 2: the candidate set
    is capped and the clear-check short-circuits at the first hit, so DENSE-overlap
    geometry stays bounded — a clear lane is returned the moment one is found, and
    the O(obstacles) per-box hit count runs only to rank the pathological
    no-clear-lane fallback."""
    xa, xb = x1 + stub, xe - stub
    fox, fxh = min(x1, xe, xa, xb), max(x1, xe, xa, xb)
    full = [r for r in obstacles if r[0] < fxh and r[0] + r[2] > fox]
    if not full:
        return None
    lox, hix = min(xa, xb), max(xa, xb)
    lane_span = [r for r in full if r[0] < hix and r[0] + r[2] > lox]
    y_pref = (y1 + y2) / 2.0
    best = None  # (hit_count, d): the least-bad deterministic fallback
    # First pass over just the lane-span boxes reproduces the legacy lane (byte
    # stable); the second folds in the stub-corridor boxes to find a clear route
    # (skipped when the two sets are identical — a redundant re-scan).
    for src in (lane_span, full):
        if not src:
            continue
        blocked = [(r[1] - clearance, r[1] + r[3] + clearance) for r in src]
        lo = min(r[1] for r in src) - 40.0
        hi = max(r[1] + r[3] for r in src) + 40.0
        for lane in _lane_candidates(y_pref, blocked, lo, hi)[:_MAX_LANES]:
            pts = _detour_points(x1, sy, y1, xa, xb, xe, ty, y2, lane)
            if not _polyline_hits(pts, full):  # early-exit: first clear lane wins
                return _detour_str(x1, sy, y1, xa, xb, xe, ty, y2, lane)
            hits = sum(1 for r in full if _polyline_hits(pts, (r,)))
            if best is None or hits < best[0]:
                best = (hits, _detour_str(x1, sy, y1, xa, xb, xe, ty, y2, lane))
        if lane_span == full:
            break  # the second pass would re-scan the identical obstacle set
    return best[1] if best else None


def _routed_label_xy(d, fx, fy):
    """Where an edge label should sit so it rides its wire. A DETOURED path carries
    a straight lane segment ("... xa,lane L xb,lane ..."); anchor to that lane's
    midpoint (WI-255 — the label formerly stuck to the straight-chord midpoint and
    floated off a re-routed wire). A clear (direct-cubic) path has no 'L' and keeps
    the caller's straight-chord fallback (fx, fy), so its label is byte-identical."""
    if " L" not in d:
        return fx, fy
    before, after = d.split(" L", 1)
    ax, ay = before.rsplit(" ", 1)[1].split(",")
    bx = after.split(" ", 1)[0].split(",")[0]
    return (float(ax) + float(bx)) / 2.0, float(ay)


def _route_edges(edges, rects_by_id, min_dx, end_trim):
    """The one wire router every layered emitter calls. `edges` is a list of
    (key, x1, y1, x2, y2, src_id, tgt_id): x1,y1 the source OUTPUT port, x2 the
    target block's LEFT edge (untrimmed — the legacy dx is measured from it), y2
    the target port. `rects_by_id` maps a node id to its (x,y,w,h) box. Returns
    {key: d}. A wire whose direct cubic clears every non-endpoint box keeps the
    exact legacy `d` (byte-identical); a blocked wire detours (`_detour_d`).

    WI-256: the wire's TERMINALS snap to the port centers (rect mid-height) while
    its first/last control keeps the fanned `y1`/`y2`, so a steep fanned wire lands
    ON its port circle instead of a block corner, yet still bows to its strand. An
    unfanned wire (its passed y already the port center) is byte-identical.

    WI-257: a BACKWARD edge (target input port at or left of the source output port,
    xe <= x1) is lane-routed rather than kept as a direct cubic. Its direct cubic
    doubles back and dives UNDER its own endpoint boxes (its only obstacles), so it
    reads as sprouting from a box edge and is untraceable end-to-end (080-CRITIQUE).
    Routing it around a visible lane requires its own endpoint boxes in the obstacle
    set — the source box trimmed a hair off its port edge so the wire's legitimate
    start-on-port isn't miscounted as a through-box (its body still constrains the
    lane). Forward edges are untouched (xe > x1), so every clean wire stays
    byte-identical. Deterministic — inputs are sorted, no dict-iteration order
    escapes."""
    ordered = sorted(rects_by_id.items())
    out = {}
    for key, x1, y1, x2, y2, src, tgt in sorted(edges, key=lambda e: e[0]):
        xe = x2 - end_trim
        dx = max((x2 - x1) * 0.4, min_dx)
        rs, rt = rects_by_id.get(src), rects_by_id.get(tgt)
        sy = rs[1] + rs[3] / 2 if rs else y1  # source port center (terminal)
        ty = rt[1] + rt[3] / 2 if rt else y2  # target port center (terminal)
        obstacles = [v for k, v in ordered if k != src and k != tgt]
        infl = [
            (r[0] - _WIRE_HIT_MARGIN, r[1] - _WIRE_HIT_MARGIN,
             r[2] + 2 * _WIRE_HIT_MARGIN, r[3] + 2 * _WIRE_HIT_MARGIN)
            for r in obstacles
        ]  # fmt: skip
        direct = _cubic_points((x1, sy), (x1 + dx, y1), (xe - dx, y2), (xe, ty))
        backward = xe <= x1
        d = None
        if _polyline_hits(direct, infl) or backward:
            span = list(obstacles)
            if backward:  # route the lane around its own endpoint boxes too
                if rs:
                    span.append((rs[0], rs[1], rs[2] - 0.1, rs[3]))  # trim port edge
                if rt:
                    span.append(rt)
            d = _detour_d(x1, sy, y1, xe, ty, y2, span)
        if d is None:
            d = "M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}".format(
                x1, sy, x1 + dx, y1, xe - dx, y2, xe, ty
            )
        out[key] = d
    return out


def _drill_layer_svg(blocks, edges):
    """One drill layer as a plain SVG block diagram. Each block is a rectangle with
    an input port (left-middle) and an output port (right-middle); each aggregated
    `edges` entry (src_key, tgt_key, title) is a wire from the source block's OUTPUT
    port to the target block's INPUT port (Simulink-style). Blocks lay out left->
    right by the shared layered pipeline over the edge set, so a producer sits left
    of its consumer and crossings are reduced. Byte-deterministic.

    Two render-legibility fixes (both formerly silent since a screenshot, not the
    raw markup, is what shows them — see the render-dashboard-critique skill):
    (1) a wire's endpoint is pulled back by PORT_R so its `marker-end` arrowhead
    lands just outside the port ring instead of dead center — the ring is drawn
    AFTER wires (so it layers on top) and, at the former center-to-center length,
    fully swallowed the arrowhead every time; (2) `_port_fan` spreads multiple
    wires sharing one port across a small vertical band instead of bundling them
    onto the exact same pixel, so a fan-in/fan-out reads as distinct strands."""
    keys = [b["key"] for b in blocks]
    by_key = {b["key"]: b for b in blocks}
    order = {k: i for i, k in enumerate(sorted(keys))}
    pred_map = {k: [] for k in keys}
    succ_map = {k: [] for k in keys}
    seen = set()
    wire_edges = []
    for a, b, t in edges:
        if a in by_key and b in by_key and a != b and (a, b) not in seen:
            seen.add((a, b))
            pred_map[b].append(a)
            succ_map[a].append(b)
            wire_edges.append((a, b, t))
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

    out_groups, in_groups = {}, {}
    for e in wire_edges:
        out_groups.setdefault(e[0], []).append(e)
        in_groups.setdefault(e[1], []).append(e)
    out_off = _port_fan(out_groups, lambda e: e[1], pos, row_h)
    in_off = _port_fan(in_groups, lambda e: e[0], pos, row_h)

    # The start stays on the output port (no arrowhead there, so it reads as
    # attached); the END is pulled PORT_R + 2 px short of the input-port center
    # so its `marker-end` arrowhead draws in the clear gap just outside the ring
    # (WI-249). A wire that would cut an unrelated block detours (`_route_edges`,
    # WI-253) through a clear lane instead of straight through the box.
    rects = {
        b["key"]: (pos[b["key"]][0], pos[b["key"]][1], col_w, row_h) for b in blocks
    }
    routes = _route_edges(
        [
            (
                e,
                pos[e[0]][0] + col_w,
                pos[e[0]][1] + row_h / 2 + out_off[e],
                pos[e[1]][0],
                pos[e[1]][1] + row_h / 2 + in_off[e],
                e[0],
                e[1],
            )
            for e in wire_edges
        ],  # fmt: skip
        rects,
        14,
        PORT_R + 2,
    )
    wires = []
    for e in sorted(wire_edges):
        title = e[2]
        wires.append(
            '<path class="wire" d="{}" marker-end="url(#drillarrow)">{}</path>'.format(
                routes[e],
                "<title>{}</title>".format(esc(title)) if title else "",
            )
        )

    nodes = []
    for b in blocks:
        x, y = pos[b["key"]]
        cy = y + row_h / 2
        cx = x + col_w / 2
        label = _drill_block_label(b, col_w, cx, cy)
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

    defs = _arrow_markers(("drillarrow", "warrow"), ("cedgearrow", "cedgehead", 8))
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
    """The When roadmap as a Simulink-style drill-down (SR-089/SR-091/SR-092,
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
            # workstream tier drills in (SR-089 "expose delivery phase").
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
    /* A4 (WI-293): the Process hub carries WHITE text on its own fill, so its
       fill is a THEME-INVARIANT token, not --accent. --accent is tuned for
       readability *as ink* on the page background and lightens to #818cf8 in
       dark, which as a *fill* behind white text measures 2.98:1 — under the
       4.5:1 AA floor. Declared here and deliberately NOT overridden in the dark
       block: #fff on #4f46e5 is 6.29:1 in both themes. Keep any successor
       palette change (WI-292) off this token unless it re-checks white-on-fill. */
    --hub:#4f46e5;
    --done:#047857; --active:#b45309; --queued:#94a3b8; --retired:#78716c;
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
     font-size:var(--small); font-weight:600; grid-column:1 / -1; }
  /* WI-256: the cue is driven by ACTUAL overflow (JS toggles `.cued` when a
     container's scrollWidth exceeds its clientWidth), so a view that clips at a
     DESKTOP width — the fixed-width icicle, a wide drill layer — signals its
     off-screen content instead of the former narrow-only media cue. `grid-column`
     keeps the revealed cue on its own full-width row so it never displaces the
     view out of the `.layout` grid's 1fr column. The `max-width:760px` rule below
     stays as the no-JS fallback. */
  .scrollcue.cued { display:block; }
  /* WI-258 (080-CRITIQUE #3): the `.scrollcue` caption sits ABOVE the card, so the
     point of truncation itself stayed unmarked — a clipped column header was
     invisible until the reader scrolled. When a container ACTUALLY overflows to the
     right, the JS toggles `.clipr` from the SAME scrollWidth>clientWidth measure that
     drives `.cued` (and clears it once scrolled to the end), fading the card's right
     (clip) edge so the cut is discoverable where it happens. Alpha-only mask keeps it
     theme-agnostic (light + dark) and obscures nothing once the end is reached. */
  .view.clipr, .tablescroll.clipr {
     -webkit-mask-image: linear-gradient(to left, transparent, #000 2.2rem);
             mask-image: linear-gradient(to left, transparent, #000 2.2rem); }
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
  #dag .edge { fill:none; stroke:var(--muted); stroke-width:1.4; opacity:.85; }
  #dag .edge.soft { stroke-dasharray:5 4; opacity:.65; }
  #dag .edge.hl { stroke:#f59e0b; stroke-width:2; opacity:1; }
  #dag .arrowhead { fill:var(--muted); }
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
          <div class="sub">$wi_done of $wi_total work items done · $wi_active active$wi_retired_clause</div>
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
        <span><i style="background:var(--retired)"></i>retired — won't build (terminal)</span>
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
    const statusColor = { done:'#047857', active:'#b45309', queued:'#94a3b8', retired:'#78716c' };

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

    // WI-256: show a scroll cue whenever a container ACTUALLY overflows (any
    // width), not just below the 760px media breakpoint. Each `.view`/`.tablescroll`
    // toggles its preceding `.scrollcue` sibling. Recomputed on resize, on tab
    // switch (a hidden panel measures 0), and — via `window.__syncCues` — when a
    // drill descends into a wider layer. A ResizeObserver covers display:none->block.
    const scrollBoxes = [...document.querySelectorAll('.view, .tablescroll')];
    function syncScrollCues(){
      for(const el of scrollBoxes){
        const over = el.scrollWidth > el.clientWidth + 1;
        let cue = el.previousElementSibling;
        while(cue && !cue.classList.contains('scrollcue')) cue = cue.previousElementSibling;
        if(cue) cue.classList.toggle('cued', over);
        // WI-258: fade the right (clip) edge while content is cut there — same
        // actual-overflow signal as `.cued`, cleared once scrolled to the end.
        el.classList.toggle('clipr', over && el.scrollLeft < el.scrollWidth - el.clientWidth - 1);
      }
    }
    window.__syncCues = syncScrollCues;
    if(window.ResizeObserver){
      const ro = new ResizeObserver(syncScrollCues);
      for(const el of scrollBoxes) ro.observe(el);
    }
    window.addEventListener('resize', syncScrollCues);
    for(const el of scrollBoxes) el.addEventListener('scroll', syncScrollCues);
    syncScrollCues();

    for (const b of document.querySelectorAll('nav.tabs button'))
      b.onclick = () => {
        for (const x of document.querySelectorAll('nav.tabs button')) x.classList.toggle('active', x===b);
        for (const p of document.querySelectorAll('.panel')) p.classList.toggle('active', p.id===b.dataset.tab);
        syncScrollCues();
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

# The dashboard's native tier code per OKF type (the same SN/SR/LLR/TC vocabulary
# the stat tiles use). WI-159 labels each collapsed type block with its terse code
# so the SN->SR->LLR->TC summary reads legibly AND fits its container without a
# right-edge clip; the full type name rides the sub-tooltip, breadcrumb and legend.
OKF_TYPE_CODE = {
    "Stakeholder Need": "SN",
    "System Requirement": "SR",
    "Low-Level Requirement": "LLR",
    "Test Case": "TC",
    "Interface": "IF",
    "Process Guide": "PG",
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

    out_groups, in_groups = {}, {}
    for e in edges:
        out_groups.setdefault(e[0], []).append(e)
        in_groups.setdefault(e[1], []).append(e)
    out_off = _port_fan(out_groups, lambda e: e[1], pos, KN_ROW_H)
    in_off = _port_fan(in_groups, lambda e: e[0], pos, KN_ROW_H)

    rects = {k: (pos[k][0], pos[k][1], KN_COL_W, KN_ROW_H) for k in node_ids}
    routes = _route_edges(
        [
            (
                e,
                pos[e[0]][0] + KN_COL_W,
                pos[e[0]][1] + KN_ROW_H / 2 + out_off[e],
                pos[e[1]][0],
                pos[e[1]][1] + KN_ROW_H / 2 + in_off[e],
                e[0],
                e[1],
            )
            for e in edges
        ],  # fmt: skip
        rects,
        12,
        2,
    )
    edge_svg = []
    for e in edges:
        s, d = e
        edge_svg.append(
            '<path class="kedge" data-src="{}" data-tgt="{}" '
            'd="{}" marker-end="url(#knowarrow)"></path>'.format(
                esc(s), esc(d), routes[e]
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
    defs = _arrow_markers(("knowarrow", "knowarrow-head"))
    svg = (
        '<svg viewBox="0 0 {:.0f} {:.0f}" width="{:.0f}" '
        'preserveAspectRatio="xMinYMin meet" role="img">{}{}{}</svg>'.format(
            width, height, width, defs, "".join(edge_svg), "".join(node_svg)
        )
    )
    return svg, details


def _okf_concept_blocks(cids, nodes):
    """The leaf concept blocks for one OKF type's descend layer (WI-159): one block
    per concept, `data-node`=id (wired to the aside by the panel), fill-keyed by
    type. A type's members carry no intra-layer edge (spine edges cross types), so
    the layer is a plain column."""
    blocks = []
    for cid in cids:
        info = nodes[cid]
        kt = (info.get("title") or "").strip()
        tip = cid + (" — " + kt if kt else "") + " ({})".format(info["type"])
        blocks.append(
            {
                "key": cid,
                "label": cid,
                "sub": kt if len(kt) <= 20 else kt[:19] + "…",
                "fill": OKF_TYPE_FILL.get(info["type"], "#64748b"),
                "textfill": "#fff",
                "stroke": "rgba(15,23,42,.15)",
                "tier": "concept",
                "title": tip,
            }
        )
    return blocks


def _okf_type_edges(edges, type_of):
    """The concept spine edges aggregated to one wire per crossing OKF-type pair
    (WI-159, the When-view boundary idiom): the deduped union count per ordered
    (src-type, tgt-type) pair. Deterministic (sorted)."""
    agg = {}
    for s, d in edges:
        ts, td = type_of[s], type_of[d]
        if ts != td:
            agg.setdefault((ts, td), set()).add((s, d))
    return [
        (a, b, "{} spine link(s)".format(len(e))) for (a, b), e in sorted(agg.items())
    ]


def _okf_root_blocks(ordered_types, groups, type_layer):
    """The root-layer type blocks + their aside detail records (WI-159): one descend
    container per OKF type, fill-keyed, labelled with its concept count."""
    type_details, root_blocks = {}, []
    for t in ordered_types:
        n = len(groups[t])
        fill = OKF_TYPE_FILL.get(t, "#64748b")
        type_details[t] = {
            "type": "OKF type",
            "title": "",
            "description": "{} {} concept(s) — double-click (or focus and press "
            "Enter) to descend into them.".format(n, t),
            "href": "",
            "resource": "",
            "fill": fill,
        }
        root_blocks.append(
            {
                "key": t,
                # The terse tier code keeps the collapsed row narrow enough to fit
                # its container (no right-edge clip); the full type name stays in
                # the sub-tooltip, the breadcrumb crumb and the legend.
                "label": OKF_TYPE_CODE.get(t, t),
                "sub": "{} concept(s)".format(n),
                "fill": fill,
                "textfill": "#fff",
                "stroke": "rgba(15,23,42,.15)",
                "tier": "okf-type",
                "descend": type_layer[t],
                "crumb": t,
                "title": "{} — {} concept(s)".format(t, n),
            }
        )
    return root_blocks, type_details


def know_view(root):
    """The OKF concept graph as a START-COLLAPSED, type-tiered Simulink-style drill
    (WI-159, the SR-089 `>3` density rule), or None when the bundle spans <= 3 OKF
    types — the caller then keeps the flat concept graph (`know_graph`), byte-
    identical for a small bundle.

    The single-sourced fix for the T2 "opens fully exploded" defect: instead of
    100s of concept nodes under an edge hairball, the default view is one BLOCK per
    OKF `type` wired by the aggregated cross-type spine edges (SN -> SR -> LLR ->
    TC), and each type block DESCENDS (double-click / Enter, breadcrumb to return)
    into a layer of its concept blocks — the exact When/How-SW drill mechanism
    (`_okf_nodes` -> `_drill_layer_svg` / `_render_drill` / DRILL_STYLE /
    DRILL_SCRIPT), no new idiom. A collapsed default is a handful of blocks, so it
    is never wider than its container (the T4 clip resolves too). Each concept block
    carries `data-node`=id, wired to the #know-detail aside by the panel.

    Returns `(drill_body, type_details)` — the rendered drill (breadcrumb + layers +
    controller) and the per-type detail records the aside shows for a type block.
    Deterministic (sorted inputs, no clocks) so `--check` stays stable."""
    nodes, edges = _okf_nodes(root)
    if not nodes:
        return None
    type_of = {cid: nodes[cid]["type"] for cid in nodes}
    groups = {}
    for cid in sorted(nodes):  # sorted -> each group's members are id-ordered
        groups.setdefault(type_of[cid], []).append(cid)
    # The `>3` rule (SR-089): the tiering is EARNED by scale — a bundle spanning
    # <= 3 types stays the flat concept graph, exactly as the When roadmap keeps the
    # flat DAG at <= 3 phases AND <= 3 workstreams.
    if len(groups) <= 3:
        return None
    # Order the type blocks by the tier precedence of their concepts so the spine
    # reads SN -> SR -> LLR -> TC left to right (off-spine kinds fall after).
    ordered_types = sorted(
        groups,
        key=lambda t: (
            min(OKF_TIER_ORDER.get(nodes[c]["tier"], 99) for c in groups[t]),
            t,
        ),
    )
    counter = [0]
    layers = []  # (layer_id, svg), in deterministic order

    def new_id():
        counter[0] += 1
        return "know-{}".format(counter[0] - 1)

    type_layer = {}
    for t in ordered_types:
        lid = new_id()
        layers.append(
            (lid, _drill_layer_svg(_okf_concept_blocks(groups[t], nodes), []))
        )
        type_layer[t] = lid
    root_blocks, type_details = _okf_root_blocks(ordered_types, groups, type_layer)
    root_id = new_id()
    layers.append(
        (root_id, _drill_layer_svg(root_blocks, _okf_type_edges(edges, type_of)))
    )
    return _render_drill("know", root_id, "Concepts", layers), type_details


def _know_panel(root, svg, details):
    """The Knowledge tab + panel — a fully self-contained block (its style, the
    embedded detail data, and the interaction JS all live inside the panel), so
    when there is no bundle and the panel is not appended the artifact is
    byte-identical to before this view existed (the vacuity guarantee).

    Above the SR-089 `>3` type threshold the panel renders the START-COLLAPSED
    type-tiered drill (`know_view`, WI-159 — the T2 density fix); at or below it,
    the flat concept graph (`know_graph`) below."""
    tab = '<button data-tab="know">Knowledge (OKF)</button>'
    legend = "".join(
        '<span><i style="background:{}"></i>{}</span>'.format(c, html.escape(t))
        for t, c in OKF_TYPE_FILL.items()
    )
    # Emitted in BOTH modes: the flat `.knode`/`.kedge` rules stay the single
    # declared source of the shared node-label scale + muted edge token (harmless
    # when collapsed renders `.block`s instead), and `#know-detail .body` styles the
    # aside in either shape.
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
        "#knowgraph .knowarrow-head{fill:var(--muted);}"
        "#know-detail .body{overflow-wrap:anywhere;}"
        "</style>"
    )

    # WI-159: the start-collapsed drill (single-sourced from the When/How mechanism)
    # when the bundle spans > 3 OKF types; else fall through to the flat graph.
    kv = know_view(root)
    if kv:
        drill_body, type_details = kv
        # The aside data merges the concept details with the per-type summaries the
        # root type blocks show. sort_keys -> byte-deterministic (cf. sw_containment).
        merged = dict(details)
        merged.update(type_details)
        dj = json.dumps(merged, ensure_ascii=False, sort_keys=True).replace(
            "</", "<\\/"
        )
        # Wire every block (type + concept) to the #know-detail aside — the same
        # click/focus-for-detail idiom the How-SW drill uses; the drill controller
        # (DRILL_SCRIPT, via _render_drill) already owns descend/breadcrumb.
        detail_script = (
            "<script>(function(){\n"
            "  const D = " + dj + ";\n"
            "  const know = document.getElementById('know'); if(!know) return;\n"
            "  const box = document.getElementById('know-detail'); if(!box) return;\n"
            "  const esc = s => { const d=document.createElement('div');"
            " d.textContent = s==null?'':s; return d.innerHTML; };\n"
            "  function show(id){\n"
            "    const d = D[id];\n"
            "    if(!d){ box.innerHTML = '<p class=\"hint\">No detail.</p>'; return; }\n"
            '    let h = \'<span class="badge" style="background:\''
            "+(d.fill||'#64748b')+'\">'+esc(d.type)+'</span>'\n"
            "      + '<h3>'+esc(id)+(d.title?' — '+esc(d.title):'')+'</h3>'\n"
            "      + '<p class=\"body\">'+esc(d.description)+'</p>';\n"
            '    if(d.href) h += \'<p class="meta">Full concept: <a href="\''
            "+esc(d.href)+'\">'+esc(d.href)+'</a>'"
            "+(d.resource?'<br>Source: '+esc(d.resource):'')+'</p>';\n"
            "    box.innerHTML = h;\n"
            "  }\n"
            "  for(const b of know.querySelectorAll('.block[data-node]')){\n"
            "    const id=b.getAttribute('data-node');\n"
            "    b.addEventListener('click', () => show(id));\n"
            "    b.addEventListener('focus', () => show(id)); }\n"
            "})();</script>"
        )
        cap = (
            '<p class="cap">The committed <code>docs/okf/</code> knowledge bundle as a '
            "typed concept graph — the dashboard is the bundle's first real "
            "<strong>consumer</strong>. It opens <strong>collapsed</strong>: one block "
            "per OKF <code>type</code> wired by the aggregated <code>SN→SR→LLR→TC</code> "
            "spine links. <strong>Double-click</strong> a type — or focus it and press "
            "Enter — to <strong>descend</strong> into its concepts; the "
            "<strong>breadcrumb</strong> returns. <strong>Click</strong> a concept to "
            "read its description and open the full file. A view — the registries are "
            "the source of truth.</p>\n"
        )
        panel = (
            '<section id="know" class="panel">\n'
            "<h2>Knowledge graph (OKF concepts)</h2>\n"
            + cap
            + DRILL_STYLE
            + style
            + "\n"
            '<div class="layout">\n'
            + SCROLL_CUE
            + '<div id="knowgraph" class="view" '
            + _hscroll("OKF concept graph, horizontally scrollable")
            + ">"
            + drill_body
            + "</div>\n"
            '<aside id="know-detail" class="detail"><p class="hint">Double-click a type '
            "block (or focus it and press Enter) to descend into its concepts; click a "
            "concept to read its description and open the full concept file in "
            "<code>docs/okf/</code>.</p></aside>\n"
            "</div>\n"
            '<div class="legend">'
            + legend
            + "</div>\n"
            + detail_script
            + "\n</section>"
        )
        return tab, panel

    # </ -> <\/ so a stray "</script>" inside description text can't close the tag
    # (the build_html j() guard, applied locally because this data is embedded in
    # the panel's own inline script rather than the shared one).
    dj = json.dumps(details, ensure_ascii=False).replace("</", "<\\/")
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


# --- the two intersecting working-loop hoops (SR-055) ---------------------------
#
# WI-250 render redesign. The former render laid the two loops out as CSS-grid
# "racetracks" — pill borders drawn around a grid of stage cards. A render
# critique (the render-dashboard-critique skill) judged the actual pixels: the
# flow direction was invisible (a border is not a directed cycle) and the "both
# loops start here" junction read as a box off to the side, not as the point
# where the two hoops meet. This render draws the honest picture SR-055 asks
# for: two directed hoops (a real cycle of stage cards wired by curved,
# arrow-headed edges) that overlap at one shared LLM_Agent hub in the middle —
# the AI-terminal / resume-script entry both loops pass through. Fully server-
# computed (fixed trig, `.1f` rounding, sorted/no-clock) so the `--check`
# freshness byte-compare stays stable and a data-less repo renders identically.

LOOP_GEOM = {
    "cy": 320.0,  # shared vertical center of both hoops
    "r": 210.0,  # hoop radius
    "ax": 280.0,  # loop-A (intake) hoop center x
    "bx": 560.0,  # loop-B (human-decision) hoop center x — overlaps A (dist 280<2r)
    "gap": 120.0,  # angular window (deg) reserved hub-side; no stage sits in it
    "cardw": 136.0,  # stage-card width
    "cardh": 48.0,  # stage-card height
    "hubw": 138.0,  # LLM_Agent hub width
    "hubh": 60.0,  # LLM_Agent hub height
    "bow": 30.0,  # how far a loop edge bows outward from the hoop center
    "labely": 30.0,  # hoop-name label baseline (top margin, clear of top cards)
    "width": 840.0,  # viewBox width
    "height": 620.0,  # viewBox height
    "notemax": 30,  # note char budget before it truncates to fit the card
}


def _loop_node_xy(cx, cy, r, deg):
    """Circle point at `deg` (math angle: 0°=right, 90°=up), SVG y-down."""
    rad = math.radians(deg)
    return cx + r * math.cos(rad), cy - r * math.sin(rad)


def _loop_stage_angles(jdeg, spin, n, gap):
    """The `n` stage angles around a hoop: evenly spread over the (360−gap)° arc
    the hub gap leaves open, walking from the hub in `spin` (±1) direction, so the
    listed order reads as the flow around the ring and the two stages nearest the
    hub sit gap/2 clear of it (no crowding at the shared lens)."""
    seg = (360.0 - gap) / n
    return [jdeg + spin * (gap / 2.0 + (k + 0.5) * seg) for k in range(n)]


def _loop_svg(hub_xy, loops):
    """One SVG drawing the working loops as intersecting hoops. `loops` is a list
    of (loop_id, name, hoop_center_x, junction_deg, spin, stages); each stage is
    (title, note, href_or_None). Stages sit around their hoop (the junction angle
    reserved for the shared hub), wired hub→s1→…→sn→hub by curved arrows that bow
    outward so the sequence traces the hoop; `spin` ±1 picks the rotation sense.
    The hub is drawn last, on top, at `hub_xy`."""
    g = LOOP_GEOM
    cy, r = g["cy"], g["r"]
    hx, hy = hub_xy

    edge_layer, card_layer, region_layer = [], [], []
    for loop_id, name, cx, jdeg, spin, stages in loops:
        angles = _loop_stage_angles(jdeg, spin, len(stages), g["gap"])
        pts = [_loop_node_xy(cx, cy, r, a) for a in angles]

        # A faint filled hoop-region disc behind each loop makes the two
        # overlapping rings — and their shared lens — legible at a glance. Each
        # hoop is a closed cycle (hub→…→hub), marked `data-cycle="closed"`. The
        # loop name rides the top margin above its hoop, clear of every card, and
        # is emitted here (before the cards) so a stage's loop membership is
        # readable in source order too.
        region_layer.append(
            '<circle class="hoop hoop-{}" data-cycle="closed" '
            'cx="{:.1f}" cy="{:.1f}" r="{:.1f}"/>'
            '<text class="hooplab" x="{:.1f}" y="{:.1f}" text-anchor="middle">'
            "{}</text>".format(esc(loop_id), cx, cy, r, cx, g["labely"], esc(name))
        )

        # The directed cycle: hub → stage1 → … → stageN → hub. Each edge bows
        # outward from the hoop center so the strand of arrows traces the ring.
        chain = [(hx, hy)] + pts + [(hx, hy)]
        for i in range(len(chain) - 1):
            x1, y1 = chain[i]
            x2, y2 = chain[i + 1]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ox, oy = mx - cx, my - cy  # outward normal from hoop center
            olen = math.hypot(ox, oy) or 1.0
            cxp, cyp = mx + ox / olen * g["bow"], my + oy / olen * g["bow"]
            # Trim both ends so the arrow starts/lands just outside the cards.
            x1t, y1t = _shorten(x1, y1, cxp, cyp, 28.0)
            x2t, y2t = _shorten(x2, y2, cxp, cyp, 32.0)
            edge_layer.append(
                '<path class="floop" d="M{:.1f},{:.1f} Q{:.1f},{:.1f} {:.1f},{:.1f}" '
                'marker-end="url(#floparrow)"/>'.format(x1t, y1t, cxp, cyp, x2t, y2t)
            )

        for i, ((title, note, href), (px, py)) in enumerate(zip(stages, pts), 1):
            card_layer.append(_loop_card(loop_id, i, title, note, href, px, py))

    hub = (
        '<g class="hub"><rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" '
        'rx="12"/><text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
        '<tspan class="hubname" x="{:.1f}" dy="-5">LLM_Agent</tspan>'
        '<tspan class="hubsub" x="{:.1f}" dy="16">shared entry · both loops</tspan>'
        '<tspan class="hubsub" x="{:.1f}" dy="12">start here</tspan></text></g>'.format(
            hx - g["hubw"] / 2,
            hy - g["hubh"] / 2,
            g["hubw"],
            g["hubh"],
            hx,
            hy,
            hx,
            hx,
            hx,
        )
    )
    defs = _arrow_markers(("floparrow", "floparrow-head"))
    return (
        '<svg class="loopsvg" viewBox="0 0 {:.0f} {:.0f}" '
        'preserveAspectRatio="xMidYMid meet" role="img" '
        'aria-label="The two working loops drawn as intersecting hoops sharing '
        'one central entry hub">{}{}{}{}{}</svg>'.format(
            g["width"],
            g["height"],
            defs,
            "".join(region_layer),
            "".join(edge_layer),
            "".join(card_layer),
            hub,
        )
    )


def _shorten(x, y, tx, ty, dist):
    """Point `dist` px from (x,y) toward (tx,ty) — trims an edge off a card."""
    dx, dy = tx - x, ty - y
    d = math.hypot(dx, dy) or 1.0
    f = min(dist / d, 1.0)
    return x + dx * f, y + dy * f


def _loop_card(loop_id, idx, title, note, href, px, py):
    """One stage card centered at (px, py): a rounded rect with a bold title and a
    (fit-truncated) note, wrapped in an `<a>` when a canonical home exists. The
    full note always rides a `<title>` so truncation never loses information."""
    g = LOOP_GEOM
    w, h = g["cardw"], g["cardh"]
    x, y = px - w / 2, py - h / 2
    shown = note if len(note) <= g["notemax"] else note[: g["notemax"] - 1] + "…"
    body = (
        "<title>{}</title>"
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="9"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
        '<tspan class="stgt" x="{:.1f}" dy="-2">{}</tspan>'
        '<tspan class="stgn" x="{:.1f}" dy="14">{}</tspan></text>'.format(
            esc(title + " — " + note),
            x,
            y,
            w,
            h,
            px,
            py,
            px,
            esc(title),
            px,
            esc(shown),
        )
    )
    attrs = 'class="stg" data-node="{}-{}"'.format(esc(loop_id), idx)
    if href:
        return '<a href="{}" {}>{}</a>'.format(esc(href), attrs, body)
    return "<g {}>{}</g>".format(attrs, body)


def _loop_panel(root):
    """The two intersecting working-loop hoops (SR-055) as one self-contained
    `<div class="loops">` block: the intake loop (A) and the human-decision
    loop (B), drawn as two directed hoops that overlap at a single shared
    LLM_Agent hub rendered once. Each stage links to its canonical home *when
    that home exists in this repo*, so every emitted href resolves (a repo
    missing the file renders the stage as a plain card — still deterministic;
    the tab itself is gated on docs/gate upstream). No clocks, no repo counts:
    the loop structure is the method's, not the repo's data, so it renders
    byte-identically regardless of the registries."""

    def home(rel):
        return rel if (root / rel).exists() else None

    wi_csv = "docs/requirements/work-items.csv"
    intake_loop = [
        ("Intake", "owner/agent hands work in", home("docs/status.md")),
        ("Triage → WIs", "scoped work items with spec detail", home(wi_csv)),
        ("Resume loop", "scheduler derives the ready frontier", home(wi_csv)),
        ("Build / review", "BUILD then REVIEW-A/B", home("docs/log.md")),
        ("Merge", "verdicts merged; the loop repeats", home("docs/log.md")),
    ]
    decide_loop = [
        ("Open items", "incl. the gate-ratification table", home("docs/open-items.md")),
        ("Human review", "the owner reviews and rules", home("docs/open-items.md")),
        ("Decisions record", "the ruling appends to the log", home("docs/log.md")),
        ("Merge", "the item leaves the surface; repeats", home("docs/log.md")),
    ]

    g = LOOP_GEOM
    hub_xy = ((g["ax"] + g["bx"]) / 2, g["cy"])
    svg = _loop_svg(
        hub_xy,
        [
            # loop A hub-gap faces right (toward the hub); it spins CCW.
            ("a", "A · Intake loop", g["ax"], 0.0, +1, intake_loop),
            # loop B hub-gap faces left (toward the hub); it spins CW so the two
            # hoops mirror around the shared junction.
            ("b", "B · Human-decision loop", g["bx"], 180.0, -1, decide_loop),
        ],
    )
    return '<div class="loops">{}</div>'.format(svg)


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
        # Panel 4 — the two intersecting working-loop hoops sharing one LLM_Agent
        # hub. Drawn as a single self-contained SVG (`.loopsvg`); the two `.hoop`
        # discs overlap so their shared lens is where the hub sits, `.floop`
        # edges carry the directional arrows, and the `.hub` card renders last on
        # top. Scales down with the panel; no grid tracks / pseudo-element arrows.
        "#process .loops{margin:.7rem 0;}"
        "#process .loopsvg{display:block;width:100%;height:auto;max-width:720px;"
        "margin:0 auto;font-family:inherit;}"
        "#process .hoop{fill:var(--accent);opacity:.05;stroke:var(--accent);"
        "stroke-opacity:.35;stroke-width:1.5;}"
        "#process .hooplab{fill:var(--accent);font-size:13px;font-weight:700;"
        "letter-spacing:.01em;}"
        "#process .floop{fill:none;stroke:var(--muted);stroke-width:1.8;"
        "opacity:.9;}"
        "#process .floparrow-head{fill:var(--muted);}"
        "#process a.stg{cursor:pointer;}"
        "#process .stg rect{fill:var(--surface);stroke:var(--border);"
        "stroke-width:1.2;filter:drop-shadow(0 1px 2px rgba(15,23,42,.12));}"
        "#process a.stg:hover rect,#process a.stg:focus rect{stroke:var(--accent);"
        "stroke-width:2;}"
        "#process .stg:focus{outline:none;}"
        "#process .stgt{fill:var(--text);font-size:12px;font-weight:700;}"
        "#process .stgn{fill:var(--muted);font-size:9.5px;}"
        "#process .hub rect{fill:var(--hub);stroke:var(--hub);"
        "filter:drop-shadow(0 2px 5px rgba(15,23,42,.28));}"
        "#process .hubname{fill:#fff;font-size:13px;font-weight:800;}"
        # A4 (WI-293): no fill-opacity discount on hub sub-labels — the same rule
        # `.sub`/`.bsub` already follow. At .85 the effective ink dropped to
        # 2.57:1 in dark theme; at full opacity on --hub it is 6.29:1.
        "#process .hubsub{fill:#fff;font-size:8.5px;}"
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
    # WI-267: `retired` (terminal WON'T-BUILD) rows get their OWN count, never
    # folded into done. Surfaced on the execution hero only when present, so the
    # common no-retired dashboard sub-line is unchanged. The execution % stays
    # done/total — retired work was deliberately abandoned, not completed.
    retired = sum(1 for w in wis if w["status"] == "retired")
    wi_retired_clause = " · {} retired".format(retired) if retired else ""
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
        # WI-159: _know_panel starts collapsed (the type-tiered drill) above the
        # SR-089 `>3` type threshold, else renders the flat concept graph.
        tab, panel = _know_panel(root, *know)
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
        wi_retired_clause=wi_retired_clause,
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
    docs/open-items.md, emitted in two regions separated by the always-present
    ``PENDING_LOCAL_LABEL`` line:

      * a committed-tree-PURE region (blocked WI rows with a BlockRef + the
        NEEDS-HUMAN run-state ask) that the `--status --check` freshness gate
        byte-compares — a pure function of the committed tree, so it reads
        identically in any clone; and
      * a MACHINE-LOCAL advisory region (refs/llm/conflict records, quarantined
        trains, stranded-train attestations) generated for humans but EXCLUDED
        from the byte-compare on every machine, because those `refs/llm/*` don't
        transport with clone/push (M-10/WI-266). `_mask_machine_local` drops it
        for the compare using ``PENDING_LOCAL_LABEL`` as the boundary.

    Derived from durable state ONLY (never the journal cache), deterministic
    (sorted, no clocks) so the gated region is byte-stable, exactly like the
    status snapshot."""
    pure_lead = (
        "_Pending owner actions — a generated projection of durable, "
        "committed-tree state (blocked rows with a ratify/attest pointer, and the "
        "NEEDS-HUMAN run-state ask); regenerated by `python "
        "project-trajectory/scripts/gen_trajectory.py --status`, do not hand-edit. "
        "This section is freshness-gated by the harness `status-map` step. The "
        "briefs above are hand-authored and untouched by regeneration._"
    )
    blocked_lines, blocked_ids = _blocked_pending(root)
    pure_items = blocked_lines + _runstate_pending(root)
    pure_body = (
        "\n".join(pure_items)
        if pure_items
        else "_None — no durable owner action is pending._"
    )
    local_items = (
        _stranded_pending(root, blocked_ids)
        + _conflict_pending(root)
        + _quarantine_pending(root)
    )
    local_body = (
        "\n".join(local_items)
        if local_items
        else "_None currently observed on this machine._"
    )
    return "{}\n\n{}\n\n{}\n\n{}".format(
        pure_lead, pure_body, PENDING_LOCAL_LABEL, local_body
    )


def _mask_machine_local(doc_text):
    """Return `doc_text` with the machine-local advisory ITEMS of the PENDING
    block dropped — everything strictly between the ``PENDING_LOCAL_LABEL`` line
    (kept, so the label itself stays gated) and ``PENDING_END`` (kept). This is
    the ONE place the `--status --check` byte-compare is scoped to the
    committed-tree-pure region, so the pre-commit gate and the post-integration
    re-run exclude exactly the same refs/llm-derived lines — no split-brain
    (M-10/WI-266). The boundary is ANCHORED to WITHIN the PENDING_BEGIN..PENDING_END
    generated block: a hand-authored line byte-identical to the label placed
    outside that block can never become the split point (it would otherwise drop
    the whole pure region and silently disable the gate). Text without the
    marker/label triple is returned untouched (an older file missing the label
    reads as drift and re-generation restores it)."""
    lines = doc_text.splitlines(keepends=True)

    def _find(target, start):
        for k in range(start, len(lines)):
            if lines[k].rstrip("\r\n") == target:
                return k
        return None

    begin_i = _find(PENDING_BEGIN, 0)
    if begin_i is None:
        return doc_text
    end_i = _find(PENDING_END, begin_i + 1)
    if end_i is None:
        return doc_text
    label_i = _find(PENDING_LOCAL_LABEL, begin_i + 1)
    if label_i is None or label_i >= end_i:
        return doc_text
    return "".join(lines[: label_i + 1] + lines[end_i:])


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
        # PURITY (M-10/WI-266): gate ONLY the committed-tree-pure region. The
        # machine-local advisory lines derive from `refs/llm/*`, which don't
        # transport with clone/push — byte-comparing them would read STALE in any
        # second clone (CI, another machine). `_mask_machine_local` drops those
        # lines from BOTH the regenerated and the committed text, so a difference
        # confined to them passes; blocked rows, the run-state ask, the label and
        # the lead prose still bite.
        if _mask_machine_local(updated) != _mask_machine_local(current):
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
    lines.extend(_frontier_lines(root))
    return "\n".join(lines)


# The forward-looking WI list is DERIVED here (WI-284), not hand-authored: the
# scheduler's dependency-ready frontier in build order. Because it lives inside
# the generated block (which check_trajectory.status_forward_only_findings
# exempts) AND is drawn only from ready — i.e. open, never-`done` — rows, a WI
# that integrates simply drops out on the next `--status` regen: the integrator
# runs that regen in _regenerate_disposition_artifacts, so status.md can no
# longer strand a closed id (the cascade that burned WI-276). Pure/deterministic
# (registry-derived, no reservations, no clocks), so `--status --check` stays a
# stable byte-compare. Capped so a long backlog stays one readable line-group.
_FRONTIER_CAP = 12


def _frontier_lines(root):
    """The `- **Ready frontier**` generated bullet: dependency-ready WIs in
    scheduler order, id + one-line title. Empty when nothing is ready (a drained
    or placeholder registry) OR when schedule.py is unavailable (a scaffold that
    omits it), so the block stays byte-stable and vacuous."""
    if schedule is None:
        return []
    try:
        rows = schedule.load_rows(root / "docs/requirements/work-items.csv")
        wis = schedule.load_wis(rows)
        ready = schedule.frontier(wis)  # reserved=None -> pure registry frontier
    except (OSError, ValueError):
        return []
    if not ready:
        return []
    titles = {w["id"]: w.get("title", "") for w in wis}
    prios = {w["id"]: w.get("priority", 0) for w in wis}
    shown = ready[:_FRONTIER_CAP]
    out = [
        "- **Ready frontier** _(dependency-ready WIs in build order — generated "
        "from the scheduler; a closed WI drops out automatically, so this list "
        "is never stale and never names a `done` id):_"
    ]
    for r in shown:
        wid = r["id"]
        p = prios.get(wid, 0)
        pri = " `P{}`".format(p) if p else ""
        title = _clip_title(titles.get(wid, ""))
        out.append("  - **{}**{} — {}".format(wid, pri, title))
    if len(ready) > _FRONTIER_CAP:
        out.append(
            "  - _(+{} more ready — see the dashboard)_".format(
                len(ready) - _FRONTIER_CAP
            )
        )
    return out


def _clip_title(title, limit=90):
    """First clause of a WI Title, clipped — the registry titles are long."""
    head = title.split(" - ")[0].split(" — ")[0].strip()
    if len(head) > limit:
        head = head[: limit - 1].rstrip() + "…"
    return head or "(untitled)"


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
        # newline="\n" via open() (write_text(newline=) is 3.10+; scripts stay
        # 3.9-runnable, floor 3.11): LF on every OS so the generated block stays
        # byte-stable regardless of a downstream .gitattributes rule.
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
        # newline="\n" via open() (write_text(newline=) is 3.10+; scripts stay
        # 3.9-runnable, floor 3.11): LF on every OS, so byte-stability doesn't rest
        # on a downstream .gitattributes eol=lf rule surviving.
        with out.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(generated)
        print("gen_trajectory: wrote {}".format(OUT_HTML))
    return 0


if __name__ == "__main__":
    sys.exit(main())
