"""The What / When / How-SW dashboard views (WI-280 split of gen_trajectory.py).

The spine icicle, the flat work-item DAG, the tiered When roadmap, and the
How-SW seam graph / containment drill, plus their tab panels. The facade
re-exports, so consumers are unchanged."""

import html
import json
import re
from dataclasses import dataclass

import check_trajectory as ct
from traj_graph import (
    GraphGeom,
    _layered_layout,
    _routed_label_xy,
    flat_graph,
    route_graph,
)
from traj_parse import WORKSTREAM_LABELS, _sn_rows, _spine
from traj_render import (
    DRILL_STYLE,
    PHASE_ACCENTS,
    SCROLL_CUE,
    STATUS_BUCKET,
    STATUS_FILL,
    STATUS_GLYPH,
    SW_NODE_FILL,
    TIER_COL,
    TIER_FILL,
    _arrow_markers,
    _drill_layer_svg,
    _hscroll,
    _render_drill,
    _ring_style,
    _svg_fit_style,
    _svg_role,
    _svg_wrap,
    esc,
    tab_button,
    tab_panel_open,
)


# WI-306: the What-tab icicle drill ids (start-collapsed above the SR-089
# `>3` SN threshold - the T2 density fix, same idiom as the sibling views).
ARCH_DRILL_ID = "archdrill"
ARCH_ROOT_LAYER = "arch-root"
ICICLE_UNIT = 18  # px of height per TC leaf


@dataclass(frozen=True)
class TierSpec:
    """One spine tier's registry columns for the icicle's node build (WI-280
    S9 — the census's `tier-node-build` class: the SR and LLR arms of
    `arch_icicle` ran the same add/primary-parent/link loop over different
    columns, so the columns become the DECLARATION and the loop runs once)."""

    id_col: str
    tier: str
    body_col: str
    meta_label: str
    meta_col: str
    ref_col: str


# The two tiers the shared loop builds; the SN roots and the TC leaves keep
# their own arms (each reads a genuinely different row shape).
SR_TIER = TierSpec(
    "SR-ID", "sr", "Requirement", "Acceptance", "AcceptanceCriteria", "SN-Refs"
)
LLR_TIER = TierSpec("LLR-ID", "llr", "Detail", "Module", "Module", "SR-Refs")


def _add_tier_rows(rows, spec, parent_ids, add, link):
    """The shared per-tier node build (WI-280 S9, `TierSpec`): `add()` one
    detail record per row and `link()` it to its FIRST listed parent — the
    loop the SR and LLR arms each spelled out. `add`/`link` are the icicle's
    own accumulators, passed in so this stays a pure loop over the spec.
    Returns the tier's id set — the next tier's parent universe."""
    ids = {r[spec.id_col].strip() for r in rows}
    for r in rows:
        rid = r[spec.id_col].strip()
        add(
            rid,
            spec.tier,
            (r.get("Title") or "").strip(),
            (r.get(spec.body_col) or "").strip(),
            "{}: {}".format(spec.meta_label, (r.get(spec.meta_col) or "").strip()),
            (r.get("Status") or "").strip(),
        )
        parents = [
            s for s in ct._split_refs(r.get(spec.ref_col, "")) if s in parent_ids
        ]
        if parents:
            link(parents[0], rid)
    return ids


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

    srs, llrs, tcs = _spine(root)
    sr_ids = _add_tier_rows(srs, SR_TIER, sn_ids, add, link)
    llr_ids = _add_tier_rows(llrs, LLR_TIER, sr_ids, add, link)

    for r in tcs:
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

    col_w, gap = 200, 16

    def draw(nid, y, cells):
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
            '<g class="cell {}" data-id="{}" tabindex="0"{}>'
            "<title>{}</title>"
            '<rect x="{}" y="{:.1f}" width="{}" height="{:.1f}" rx="3" '
            'fill="{}"></rect>{}</g>'.format(
                t,
                esc(nid),
                _ring_style(TIER_FILL[t]),
                esc(tip),
                x,
                y,
                col_w,
                max(h - 1, 1),
                TIER_FILL[t],
                txt,
            )
        )
        cur = y
        for c in kids.get(nid, []):
            draw(c, cur, cells)
            cur += weight[c] * ICICLE_UNIT

    def panel(root_ids):
        """The leaf-proportional icicle for `root_ids`: the whole spine at the
        flat scale, or ONE SN's subtree as a drill layer."""
        cells = []
        y = 0.0
        for s in root_ids:
            draw(s, y, cells)
            y += weight[s] * ICICLE_UNIT
        width = 4 * col_w + 3 * gap
        heads = "".join(
            '<text class="lane-head" x="{:.0f}" y="-8" '
            'text-anchor="middle">{}</text>'.format(
                TIER_COL[t] * (col_w + gap) + col_w / 2, t.upper()
            )
            for t in ("sn", "sr", "llr", "tc")
        )
        body = heads + "".join(cells)
        return (
            '<svg viewBox="0 -22 {} {:.0f}" width="{}" style="{}" '
            'preserveAspectRatio="xMinYMin meet" role="{}">{}</svg>'.format(
                width, y + 22, width, _svg_fit_style(width), _svg_role(body), body
            )
        )

    # WI-306 (T2, 119-CRITIQUE MAJOR): the landing What view used to render the
    # WHOLE spine at leaf scale - one unit per TC - so a mature registry opened as
    # a multi-screen wall while the three WIRED tabs correctly opened at a summary
    # layer. Capping DEPTH would not have fixed it: height is leaf-proportional,
    # so stopping at the SR lane still stacks one unit per SR. The summary has to
    # be a coarser TIER - one block per SN, descend on click - which is what the
    # anchor's bad case ("a wall of nodes on open") and the row both ask for.
    #
    # Earned by scale exactly like its siblings (SR-089's `>3` rule): at or below
    # 3 SNs the flat icicle renders BYTE-IDENTICALLY, so a small project never
    # pays for tiering it cannot need.
    if len(roots) <= 3:
        return panel(roots), details, desc

    layers = []
    blocks = []
    for s in roots:
        lid = "archl-{}".format(s.lower())
        blocks.append(
            {
                "key": s,
                "label": s,
                "sub": (details[s]["title"] or "").strip(),
                "cls": "sn",
                "tier": "sn",
                "descend": lid,
                "crumb": s,
                "count": len(desc.get(s, [])),
            }
        )
        layers.append((lid, panel([s])))
    layers.insert(0, (ARCH_ROOT_LAYER, _drill_layer_svg(blocks, [])))
    return (
        _render_drill(ARCH_DRILL_ID, ARCH_ROOT_LAYER, "What (spine)", layers),
        details,
        desc,
    )


# --- the layered work-item DAG, computed in Python (Thread 52 ruling A) ---------

DAG_COL_W = 172  # node width
DAG_COL_GAP = 60  # horizontal gap between dependency ranks
DAG_ROW_H = 46  # node height
DAG_ROW_GAP = 22  # vertical gap between nodes in a rank
DAG_PAD = 18


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
    # A cross-rank edge that would cut an unrelated WI box detours around it
    # (`route_graph` -> `_route_edges`, WI-253); a clear edge keeps its bowed
    # cubic byte-for-byte.
    routes, _out_off, _in_off = route_graph(
        [w["id"] for w in wis],
        wi_edges,
        pos,
        GraphGeom(DAG_COL_W, DAG_COL_GAP, DAG_ROW_H, DAG_ROW_GAP, DAG_PAD),
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
        status = _wi_status(w)  # what the row IS — every text surface below
        st = STATUS_BUCKET[status]  # which swatch it paints in (WI-272)
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
                "{} {}".format(STATUS_GLYPH[status], esc(w["id"])),
                x + DAG_COL_W / 2,
                esc(short),
            )
        )
        tip = "{} — {} ({})".format(w["id"], title, status)
        nodes.append(
            # WI-272: `class` carries the swatch BUCKET (the `#dag .wi.queued`
            # text rule keys on it), `data-status` the row's own word — appended
            # last, like the drill's, so existing adjacency assertions hold.
            '<g class="wi {}" data-id="{}" tabindex="0"{} data-status="{}">'
            "<title>{}</title>"
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="8" '
            'fill="{}"></rect>{}</g>'.format(
                st,
                esc(w["id"]),
                _ring_style(STATUS_FILL[st]),
                esc(status),
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
            # `status` is the registry's own word; `bucket` is the swatch it
            # shares (WI-272). Two fields, so the detail JSON can never again
            # report a parked row as queued.
            "status": status,
            "bucket": st,
            "title": title,
            "body": "Workstream: {}".format(ws),
            "meta": "Delivers: {} · After: {}".format(
                ", ".join(w["srs"]) or "—",
                ", ".join(w["preds"] + ["~" + p for p in w["soft"]]) or "—",
            ),
        }

    defs = _arrow_markers(("arrow", "arrowhead"))
    svg = _svg_wrap(width, height, defs + "".join(edges) + "".join(nodes))
    return svg, details


# --- the How-SW interface graph (WI-056), reusing the WI-DAG layouter -----------

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
    # The label anchor below still bows to the fan strand, so this is the one
    # emitter that reads the offsets `flat_graph` returns beside the routes.
    pos, width, height, routes, out_off, in_off = flat_graph(
        node_ids,
        edges,
        GraphGeom(SW_COL_W, SW_COL_GAP, SW_ROW_H, SW_ROW_GAP, SW_PAD),
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
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="8" '
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
        "<style>#sw .swedge{fill:none;stroke:var(--muted);stroke-width:var(--w-line);}"
        "#sw .swarrow-head{fill:var(--muted);}"
        "#sw .swlab{fill:var(--muted);font-size:var(--nsub);}</style>"
    )
    return _svg_wrap(
        width, height, defs + style + "".join(edge_svg) + "".join(node_svg)
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


def _subtree_modules(cid, direct, children_of):
    """Every module in `cid` and its PartOf-descendants (cycle-guarded) —
    lifted out of `sw_containment` (WI-280 S9) with its joins passed in."""
    seen, frontier, out = set(), [cid], set()
    while frontier:
        n = frontier.pop()
        if n in seen:
            continue
        seen.add(n)
        out.update(direct.get(n, []))
        frontier.extend(children_of.get(n, []))
    return out


def _layer_edges(ifs, inv, block_of, in_scope, allow_boundary):
    """Aggregated seam wires among one drill layer's blocks + the file/external
    blocks they reach — lifted out of `sw_containment` (WI-280 S9), which passes
    its declared seams + inventory in. `block_of(norm)` -> the sibling block
    key(s) a module maps to at this layer (empty when out of this layer's
    scope); a seam whose two module endpoints land in different sibling blocks
    (or a boundary seam to a file/external, when `allow_boundary(norm)`)
    becomes one deduped wire."""
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
        return _subtree_modules(cid, direct, children_of)

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
            "fill": SW_NODE_FILL["component"],
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
        return _layer_edges(ifs, inv, block_of, in_scope, allow_boundary)

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

    tab = tab_button("sw", "How (SW architecture)")
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
        tab_panel_open("sw")
        + "\n<h2>Software architecture (How)</h2>\n"
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


def _wi_status(w):
    """A work item's TRUE status, for every text surface (WI-272).

    `blocked` is DERIVED here — a `queued/` spec carrying a `blockref`
    (concurrency-restructure §2.1: blocked has no directory) — so the render
    keeps telling the reader a parked row is parked, the exact distinction
    WI-272/review-M-2 protects; the loaders themselves never mint the status.
    Only a status the vocabulary does not know at all falls back, and it falls
    back to `queued` because that is the safe read for an unrecognized row —
    the declared statuses are always reported as themselves."""
    if w["status"] == "queued" and w.get("blockref"):
        return "blocked"
    return w["status"] if w["status"] in STATUS_BUCKET else "queued"


def _wi_st(w):
    """A work item's FILL BUCKET — the colour key, not the status (WI-272).

    Six statuses, four fills: `deferred` and `blocked` share `queued`'s swatch
    under the "not started" grouping. Callers that paint use this; callers that
    LABEL must use `_wi_status`, or the render goes back to telling the reader a
    parked row is queued."""
    return STATUS_BUCKET[_wi_status(w)]


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


def _agg_edges(subset, key_of):
    """One aggregated edge per crossing (key_of[p] != key_of[w]) pair, valued by
    the deduped union of contributing WI edges — so a parent edge is exactly that
    union (the WI-074 boundary idiom; lifted out of `when_view`, WI-280 S9).
    Returns sorted (a, b, title) triples."""
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


def _wi_block(w, phase_of, key=None):
    """One leaf work-item block for the tiered roadmap (lifted out of
    `when_view`, WI-280 S9; the delivery-phase map is passed in)."""
    status = _wi_status(w)  # the row's own status — labels, titles, detail
    st = STATUS_BUCKET[status]  # the swatch it shares (WI-272)
    t = w["title"]
    return {
        "key": key or w["id"],
        # A3: the status glyph rides in the visible label (so the column width
        # accounts for it), redundant with the fill hue; `wi` carries the bare id
        # for the detail-panel wiring (U4) independent of the decorated label.
        # The glyph is per STATUS, so `deferred`/`blocked` stay distinguishable
        # from `queued` even though the three share one swatch.
        "label": "{} {}".format(STATUS_GLYPH[status], w["id"]),
        "wi": w["id"],
        "sub": t if len(t) <= 20 else t[:19] + "…",
        "fill": STATUS_FILL[st],
        "textfill": "#0f172a" if st == "queued" else "#fff",
        "stroke": "rgba(15,23,42,.15)",
        "tier": "work-item",
        # `cls` is the SWATCH bucket (the `#dag .wi.queued` text rule and its
        # siblings key on it); `status` is the row's own word, emitted as
        # `data-status` so the DOM never loses it. One idiom, matching the
        # flat DAG's node groups (U4).
        "cls": st,
        "status": status,
        # OI-10 fix: surface the delivery Phase in the leaf block's hover title
        # too, so it stays visible when the phase tier is flat (≤3 phases) but a
        # workstream tier drills in (SR-089 "expose delivery phase").
        "title": "{} — {} ({}) · {}".format(w["id"], t, status, phase_of[w["id"]]),
    }


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

    def wi_layer(members):
        """A leaf layer of work-item blocks wired by their intra-set edges."""
        lid = new_id()
        blocks = [
            _wi_block(w, phase_of) for w in sorted(members, key=lambda w: w["id"])
        ]
        edges = _agg_edges(members, {w["id"]: w["id"] for w in members})
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
            edges = _agg_edges(subset, {w["id"]: keyfn(w) for w in subset})
            layers.append((lid, _drill_layer_svg(blocks, edges)))
            return lid
        # No tier crosses its threshold here -> the bottom-tier work-item layer.
        return wi_layer(subset)

    tiers = [
        ("phase", lambda w: phase_of[w["id"]]),
        ("workstream", lambda w: w["workstream"]),
    ]
    root_id = build(wis, tiers)

    # WI-294b (119-CRITIQUE U1/U3): rendered through the shared `.legend`/`<i>`
    # component (see sw_view's node-kind legend) instead of a bespoke smaller
    # inline chip idiom, so the phase key matches every other legend's size,
    # placement, and styling.
    legend = "".join(
        '<span><i style="background:{}"></i>{}</span>'.format(color[p], esc(p))
        for p in sorted(phases)
    )
    summary = (
        '<p class="cap"><strong>Tiered roadmap: {} phase(s), {} workstream(s).</strong> '
        "A tier renders as wired blocks only when it holds more than 3 members "
        "(phase ⊃ workstream ⊃ work item). <strong>Double-click</strong> a "
        "block — or focus it and press Enter — to <strong>descend</strong> a layer; "
        "the <strong>breadcrumb</strong> returns. A block’s ports carry the aggregated "
        "dependency edges (the deduped union of its members’ crossing edges).</p>"
        '<div class="legend">{}</div>'.format(len(phases), len(workstreams), legend)
    )
    return DRILL_STYLE + summary + _render_drill("when", root_id, "Roadmap", layers)


def _sw_panel(mods, graph=None):
    tab = tab_button("sw", "How (SW architecture)")
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
            # A3 (WI-313): the flat seam graph encodes node KIND by fill, and it
            # rendered with no legend — the containment drill earned one in the
            # 048/U3 round; this fallback never did. Same shared `.legend`
            # component; component containers never render here, so three entries.
            + (
                '<div class="legend">'
                '<span><i style="background:{module}"></i>module</span>'
                '<span><i style="background:{file}"></i>file (shared-contract hub)</span>'
                '<span><i style="background:{external}"></i>external actor</span>'
                "</div>\n"
            ).format(**SW_NODE_FILL)
        )
    panel = (
        tab_panel_open("sw")
        + "\n<h2>Software architecture (How)</h2>\n"
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
    tab = tab_button("cmp", "How (physical)")
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
        tab_panel_open("cmp") + "\n<h2>Components (How — physical)</h2>\n"
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
