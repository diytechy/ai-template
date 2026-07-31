"""The Knowledge / Process / Next-work dashboard panels (WI-280 split of
gen_trajectory.py).

The OKF concept graph + type-tiered drill, the method-reference Process tab
(lifecycle x gates, the resume loop, the two working-loop hoops), and the
landing-hero Next-work card. The facade re-exports, so consumers are unchanged."""

import html
import json
import math

import traj_parse
from traj_graph import GraphGeom, flat_graph
from traj_parse import OKF_TIER_ORDER, _gate_value, _okf_nodes, _process_doc
from traj_render import (
    DRILL_STYLE,
    OKF_TYPE_CODE,
    OKF_TYPE_FILL,
    SCROLL_CUE,
    _arrow_markers,
    _drill_layer_svg,
    _hscroll,
    _render_drill,
    _ring_style,
    _svg_role,
    _svg_wrap,
    esc,
    tab_button,
    tab_panel_open,
)
from traj_status import _title_clause


KN_COL_W = 150
KN_COL_GAP = 60
KN_ROW_H = 30
KN_ROW_GAP = 12
KN_PAD = 16


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
    pos, width, height, routes, _out_off, _in_off = flat_graph(
        node_ids,
        edges,
        GraphGeom(KN_COL_W, KN_COL_GAP, KN_ROW_H, KN_ROW_GAP, KN_PAD),
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
            '<g class="knode" data-id="{}" tabindex="0"{}>'
            "<title>{}</title>"
            '<rect x="{:.1f}" y="{:.1f}" width="{}" height="{}" rx="8" '
            'fill="{}"></rect><text x="{:.1f}" y="{:.1f}" text-anchor="middle" '
            'dominant-baseline="central">{}</text></g>'.format(
                esc(k),
                _ring_style(fill),
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
    svg = _svg_wrap(width, height, defs + "".join(edge_svg) + "".join(node_svg))
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
    tab = tab_button("know", "Knowledge (OKF)")
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
        "#knowgraph .knode rect{stroke:rgba(15,23,42,.15);stroke-width:var(--w-node);"
        "cursor:pointer;transition:opacity .1s ease;}"
        "#knowgraph .knode text{fill:#fff;font-size:var(--nlabel);pointer-events:none;}"
        "#knowgraph .knode.dim,#knowgraph .kedge.dim{opacity:var(--o-dim);}"
        "#knowgraph .knode.hl rect{stroke:var(--ring,#f59e0b);stroke-width:var(--w-emph);}"
        # U3 (dashboard-uniformity): the directed-dependency edge shares the drill
        # `.wire` idiom — one `--muted` stroke token (was a hardcoded #94a3b8 that
        # diverged from `.wire` in light mode) at the same 1.5 width.
        "#knowgraph .kedge{fill:none;stroke:var(--muted);stroke-width:var(--w-line);}"
        "#knowgraph .kedge.hl{stroke:#f59e0b;stroke-width:var(--w-emph);}"
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
            tab_panel_open("know") + "\n"
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
        tab_panel_open("know") + "\n"
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
    body = defs + "".join(region_layer + edge_layer + card_layer) + hub
    return (
        '<svg class="loopsvg" viewBox="0 0 {:.0f} {:.0f}" '
        'preserveAspectRatio="xMidYMid meet" role="{}" '
        'aria-label="The two working loops drawn as intersecting hoops sharing '
        'one central entry hub">{}</svg>'.format(
            g["width"], g["height"], _svg_role(body), body
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
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="8"/>'
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

    # The work-item registry's home, whichever it is (Phase 2b): the spec folder
    # when this repo has migrated, else the CSV. `home` is an existence probe, so
    # asking it for both and taking the first that answers keeps every emitted
    # href resolvable without the panel knowing which home won.
    wi_home = home("docs/work") or home("docs/requirements/work-items.csv")
    intake_loop = [
        ("Intake", "owner/agent hands work in", home("docs/status.md")),
        ("Triage → WIs", "scoped work items with spec detail", wi_home),
        ("Resume loop", "scheduler derives the ready frontier", wi_home),
        ("Build / review", "BUILD then REVIEW-A/B", home("docs/log.md")),
        ("Merge", "verdicts merged; the loop repeats", home("docs/log.md")),
    ]
    decide_loop = [
        (
            "Open items",
            "incl. the gate-ratification table",
            home("docs/open-items.html"),
        ),
        ("Human review", "the owner reviews and rules", home("docs/open-items.html")),
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
        "#process h3{font-size:var(--body);margin:1.5rem 0 .25rem;letter-spacing:-.01em;}"
        "#process .gnow{background:var(--surface);border:1px solid var(--border);"
        "border-radius:var(--r-card);padding:.6rem .9rem;box-shadow:var(--shadow);"
        "display:inline-block;margin:.2rem 0 .4rem;}"
        "#process .gnow b{color:var(--accent);}"
        "#process ol.pflow{list-style:none;display:flex;flex-wrap:wrap;"
        "gap:.55rem;padding:0;margin:.5rem 0;align-items:stretch;}"
        "#process .pflow li{position:relative;background:var(--surface);"
        "border:1px solid var(--border);border-radius:var(--r-card);"
        "padding:.5rem .7rem .55rem;box-shadow:var(--shadow);max-width:200px;}"
        "#process .pflow li+li{margin-left:1rem;}"
        '#process .pflow li+li::before{content:"→";'
        "position:absolute;left:-.95rem;top:50%;transform:translateY(-50%);"
        "color:var(--muted);}"
        "#process .pflow li.now{border:2px solid var(--accent);"
        "padding:calc(.5rem - 1px) calc(.7rem - 1px) calc(.55rem - 1px);}"
        "#process .pflow li.opt{border-style:dashed;}"
        "#process .pflow b{display:block;font-size:var(--small);}"
        "#process .pflow .g{display:block;font-size:var(--tiny);font-weight:700;"
        "letter-spacing:.04em;color:var(--accent);}"
        "#process .pflow .n{display:block;font-size:var(--tiny);color:var(--muted);}"
        "#process ul.esc{font-size:var(--body);color:var(--muted);margin:.4rem 0 0;"
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
        "#process .hoop{fill:var(--accent);opacity:var(--o-wash);stroke:var(--accent);"
        "stroke-opacity:var(--o-ghost);stroke-width:var(--w-line);}"
        "#process .hooplab{fill:var(--accent);font-size:var(--nhead);font-weight:700;"
        "letter-spacing:.01em;}"
        "#process .floop{fill:none;stroke:var(--muted);stroke-width:var(--w-line);"
        "opacity:var(--o-muted);}"
        "#process .floparrow-head{fill:var(--muted);}"
        "#process a.stg{cursor:pointer;}"
        "#process .stg rect{fill:var(--surface);stroke:var(--border);"
        "stroke-width:var(--w-line);filter:drop-shadow(0 1px 2px rgba(15,23,42,.12));}"
        "#process a.stg:hover rect,#process a.stg:focus rect{stroke:var(--accent);"
        "stroke-width:var(--w-emph);}"
        "#process .stg:focus{outline:none;}"
        "#process .stgt{fill:var(--text);font-size:var(--nlabel);font-weight:700;}"
        "#process .stgn{fill:var(--muted);font-size:var(--nsub);}"
        "#process .hub rect{fill:var(--hub);stroke:var(--hub);"
        "filter:drop-shadow(0 2px 5px rgba(15,23,42,.28));}"
        "#process .hubname{fill:#fff;font-size:var(--nhead);font-weight:800;}"
        # A4 (WI-293): no fill-opacity discount on hub sub-labels — the same rule
        # `.sub`/`.bsub` already follow. At .85 the effective ink dropped to
        # 2.57:1 in dark theme; at full opacity on --hub it is 6.29:1.
        "#process .hubsub{fill:#fff;font-size:var(--nsub);}"
        "</style>"
    )
    panel = (
        tab_panel_open("process") + "\n"
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
        "<code>open-items.html</code>, <code>log.md</code>); the loop structure is "
        "the method's, not this repo's data.</p>\n" + loops_html + "\n"
        "</section>"
    )
    return tab_button("process", "Process"), panel


# --- the landing-hero "Next work" surface (T1 / SR-054, WI-305) ----------------
# "Find the next work" is one of SR-054's three core reading tasks, and
# 119-CRITIQUE (T1) found it had NO path: with zero `active` rows nothing marked
# "you are here", the Process tab's resume loop is a static method diagram, and
# the only route to a queued item was When -> descend a phase -> descend a
# workstream -> scan for a queued node — the anchor's own bad case, expanding
# nested blocks to locate something. This names the dependency-ready WIs the
# scheduler derives (schedule.frontier — the SAME frontier IF-071 projects into
# status.md's Ready-frontier block) right on the landing view, so the task costs
# ZERO tab switches. Ready WIs come first (actionable now); when the cap has room
# the next WAITING WIs follow, each annotated with the blocking predecessor that
# holds it — so the surface renders "the ready/queued WIs ... with their blocking
# predecessor" in one glance. OPTIONAL, exactly like `_frontier_lines`: a scaffold
# that ships gen_trajectory without schedule.py renders NO block (empty string)
# rather than crashing — the kit's "non-adopter pays nothing" posture.
_NEXT_WORK_CAP = 6
# WI-319 (T4, 121-CRITIQUE MINOR): a bound on ONE item's height, not a text
# budget. The card used to spend a fixed 60 characters whatever width it had —
# cutting "…tiering expo…" mid-word at 1680px with the card half empty, the
# anchor's truncated-WITHOUT-affordance case. HTML already fits text to the space
# available, so the clause is emitted whole and the card's width does the
# fitting; this only bounds the tail of a registry cell that carries its whole
# rationale in the Title (measured over 320 rows: median 44, p90 126, max 609).
_NEXT_WORK_TITLE = 140


def _next_work_title(title):
    """One next-work item's title cell, as escaped markup. Under the bound it is
    simply the whole clause, wrapped by the card. Over it, the remainder discloses
    through a NATIVE `<details>` — operable by pointer and by keyboard, needing no
    script — cut at a word so the text reads continuously once opened, which is
    what makes the ellipsis one a reader can act on rather than a dead end."""
    head = _title_clause(title)
    if len(head) <= _NEXT_WORK_TITLE:
        return esc(head)
    cut = head.rfind(" ", 0, _NEXT_WORK_TITLE + 1)
    if cut <= 0:
        cut = _NEXT_WORK_TITLE
    return (
        '<details><summary>{}<span class="nwrev">… show all</span></summary>'
        "{}</details>"
    ).format(esc(head[:cut].rstrip()), esc(head[cut:]))


def _next_work_html(root):
    """The hero "Next work" list as an HTML string, or "" when schedule.py is
    unavailable or the registry carries no real work items. Ready WIs first (in
    the scheduler's deterministic build order), then the next waiting WIs
    annotated with their blocking predecessor — so the surface is byte-stable
    under the --check freshness compare and always either names the next work or
    says why none is ready."""
    if traj_parse.schedule is None:
        return ""
    try:
        wis = traj_parse.schedule.load_wis(
            traj_parse.schedule.load_registry_rows(
                root / "docs/requirements/work-items.csv"
            )
        )
        records = traj_parse.schedule.evaluate(wis)
    except (OSError, ValueError):
        return ""
    if not wis:
        return ""
    titles = {w["id"]: w.get("title", "") for w in wis}
    by_id = {w["id"]: w for w in wis}
    status = {w["id"]: w["status"] for w in wis}
    ready = [r for r in records if r["disposition"] == "ready"]
    waiting = [r for r in records if r["disposition"] == "waiting"]
    shown = (ready + waiting)[:_NEXT_WORK_CAP]

    if not shown:
        open_left = any(r["disposition"] not in ("done", "retired") for r in records)
        msg = (
            "No ready work — see the When roadmap for open items."
            if open_left
            else "All work items are done."
        )
        return (
            '<div class="card nextwork"><div class="label">Next work</div>'
            '<p class="nwnone">{}</p></div>'.format(esc(msg))
        )

    items = []
    for r in shown:
        wid = r["id"]
        title = _next_work_title(titles.get(wid, ""))  # already escaped markup
        if r["disposition"] == "waiting":
            # The unmet hard predecessors that hold this WI (WI-267: a `retired`
            # dead-end predecessor also shows — it will never be `done`).
            blockers = [p for p in by_id[wid]["preds"] if status.get(p) != "done"]
            after = (
                ' <span class="nwafter">after {}</span>'.format(
                    esc(", ".join(blockers))
                )
                if blockers
                else ""
            )
            items.append(
                '<li class="waiting"><span class="nwid">{}</span> '
                '<span class="nwt">{}</span>{}</li>'.format(esc(wid), title, after)
            )
        else:
            items.append(
                '<li><span class="nwid">{}</span> '
                '<span class="nwt">{}</span></li>'.format(esc(wid), title)
            )
    extra = len(ready) + len(waiting) - len(shown)
    if extra > 0:
        items.append(
            '<li class="nwmore">+{} more — see the When roadmap</li>'.format(extra)
        )
    return (
        '<div class="card nextwork"><div class="label">Next work</div>'
        '<ul class="nwlist">{}</ul></div>'.format("".join(items))
    )
