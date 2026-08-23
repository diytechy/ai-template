"""The Knowledge / Process / Next-work dashboard panels (WI-280 split of
gen_trajectory.py).

The OKF concept graph + type-tiered drill, the method-reference Process tab
(lifecycle x the stage ladder, the station/lane cycle, the slice cadence), and the
landing-hero Next-work card. The facade re-exports, so consumers are unchanged.

`kitlib.station` and `schedule` are imported for their CONSTANTS only (the
terminal outcomes, the bar attestation label, the kind tables): the station
render derives its stage vocabulary from the modules that ship the flow, instead
of restating it as literals that drift (the 2026-08-01 diagram review's ruling —
the dashboard must never be pinned to itself).

A VIEW IMPORTS READ MODELS, NEVER A LIFECYCLE SERVICE (WI-483). Until this
module's `station` re-point it reached those two constants through `integrate`,
the 2,500-line merge coordinator — an edge of the seven-module import cycle the
2026-08-19 repository review recorded (H-02), and the one direction a layered
system forbids outright, since a render leaf writes nothing and must not be able
to. The vocabulary moved DOWN to `kitlib/station.py`, below both. The rule is
asserted, not merely written here: `tests/test_import_layers.py`.

Contracts: IF-093, IF-094 — the constants-only Consumes seams on kitlib.station (OUTCOME_DIRS, BAR_GREEN) and schedule (the kind tables); rows of record in docs/requirements/interfaces.toml.
"""

import html
import json

import schedule
import traj_parse
from kitlib import station
from traj_graph import GraphGeom, flat_graph
from traj_parse import OKF_TIER_ORDER, _okf_nodes, _process_doc, _stage_value
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
    _svg_fit_style,
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
    (WI-159, the LLR-052 `>3` density rule), or None when the bundle spans <= 3 OKF
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
    # The `>3` rule (LLR-052): the tiering is EARNED by scale — a bundle spanning
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
            (lid, _drill_layer_svg(_okf_concept_blocks(groups[t], nodes), [], lid))
        )
        type_layer[t] = lid
    root_blocks, type_details = _okf_root_blocks(ordered_types, groups, type_layer)
    root_id = new_id()
    layers.append(
        (
            root_id,
            _drill_layer_svg(root_blocks, _okf_type_edges(edges, type_of), root_id),
        )
    )
    return _render_drill("know", root_id, "Concepts", layers), type_details


def _know_panel(root, svg, details):
    """The Knowledge tab + panel — a fully self-contained block (its style, the
    embedded detail data, and the interaction JS all live inside the panel), so
    when there is no bundle and the panel is not appended the artifact is
    byte-identical to before this view existed (the vacuity guarantee).

    Above the LLR-052 `>3` type threshold the panel renders the START-COLLAPSED
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


# --- the Process tab: how this project is built (WI-085 / LLR-051) --------------
#
# The method reference view: the dashboard's other tabs show project *state*;
# this one shows the *process* the state moves through. Data-derived where a
# canonical source exists — the effective stage from docs/stage, tier counts from
# the spine registries, work-item counts from the docs/work/ registry — and linking out to
# the process docs everywhere a canonical home exists. The in-view restatement
# is limited to the relationships no single doc states as one picture (the
# lifecycle x ladder ordering, the station cycle, the slice -> phase -> gate-bar
# cadence) — the WI-085 anti-duplication ruling.

# --- the station/lane cycle (WI-389, docs/concurrency-v2.md ruled 2026-07-31) ---
#
# WI-389 render redesign, replacing the WI-250 two-intersecting-hoops picture
# (which drew the pre-station serial loop). One directed closed cycle at the
# level the tab's audience reads: claim -> lane build -> the three terminal
# outcomes converging on the station refresh -> the serial merge slot -> trunk
# advance -> the post-merge intake mint -> the dispatcher tick — with the spine
# barrier and the intake arm visible. The 2026-08-01 diagram review's
# constraint governs the vocabulary: stage names are DERIVED from the shipped
# modules' own constants (station.OUTCOME_DIRS, station.BAR_GREEN,
# schedule's kind tables) wherever one exists, and every label that must stay a
# literal here is held by a sync pin against the module it mirrors
# (tests/test_traj_panels.py, the station suite) — the dashboard is never again
# pinned to itself. Fully server-computed (fixed coordinates, `.1f` rounding,
# sorted derivations, no clocks) so the `--check` freshness byte-compare stays
# stable and a data-less repo renders identically.

STATION_GEOM = {
    "colL": 150.0,  # left column x — dispatcher tick / intake mint / trunk advance
    "colM": 450.0,  # middle column x — claim / merge slot (+ the property caption)
    "colR": 750.0,  # right column x — lane build / outcomes / station refresh
    "rowT": 70.0,  # top-row card centers
    "rowB": 420.0,  # bottom-row card centers
    "oy": (175.0, 245.0, 315.0),  # outcome-card centers, top -> bottom
    "iy": 245.0,  # intake-mint card center (left column midpoint)
    "cardw": 176.0,  # station-card width
    "cardh": 62.0,  # station-card height (title + two note lines)
    "outw": 168.0,  # outcome-card width
    "outh": 44.0,  # outcome-card height (title + one note line)
    "width": 900.0,  # viewBox width
    "height": 545.0,  # viewBox height
    "notemax": 34,  # note char budget before it truncates to fit its card
}

# The admission-arm vocabulary (the §A8 policy table). HARDCODED because the
# dispatcher exports no constant for it (`dispatch._kind_action` returns these
# as literals); the sync pin — test_station_barrier_and_admission_arms_pin_to_
# the_dispatcher — recomputes the set from `_kind_action` over every kind x
# session hold and reds here the moment the dispatcher's vocabulary moves.
_ADMISSION_ARMS = ("parallel", "exclusive", "batch", "surface")


def _exclusive_kinds():
    """The kinds the spine barrier holds for, DERIVED from schedule's ruled
    tables (§A1/§A8), in rank order — the frontier's own sort."""
    return [
        kind
        for kind in sorted(
            schedule._KIND_CONCURRENCY,
            key=lambda k: (schedule._KIND_RANK[k], k),
        )
        if schedule._KIND_CONCURRENCY[kind] == schedule.CONCURRENCY_EXCLUSIVE
    ]


def _outcome_cards():
    """The terminal outcomes as (name, [declaring dirs]) pairs, DERIVED from
    kitlib.station.OUTCOME_DIRS — the same one-home read the merge slot uses to
    classify a finished lane (§A3: the outcome IS the directory the claimed
    specs moved into; there is no fourth answer). Sorted for determinism."""
    by_outcome = {}
    for status_dir, outcome in station.OUTCOME_DIRS.items():
        by_outcome.setdefault(outcome, []).append(status_dir)
    return [(outcome, sorted(dirs)) for outcome, dirs in sorted(by_outcome.items())]


def _station_card(key, title, notes, href, cx, cy, w, h):
    """One station card centered at (cx, cy): a rounded rect, a bold title and
    up to two (fit-truncated) note lines, wrapped in an `<a>` when a canonical
    home exists. The full text always rides a `<title>` so truncation never
    loses information."""
    g = STATION_GEOM
    x, y = cx - w / 2, cy - h / 2
    shown = [
        n if len(n) <= g["notemax"] else n[: g["notemax"] - 1] + "…" for n in notes
    ]
    spans = '<tspan class="stgt" x="{:.1f}" dy="{:.0f}">{}</tspan>'.format(
        cx, -12.0 if len(notes) > 1 else -2.0, esc(title)
    )
    for i, note in enumerate(shown):
        spans += '<tspan class="stgn" x="{:.1f}" dy="{}">{}</tspan>'.format(
            cx, 14 if i == 0 else 12, esc(note)
        )
    body = (
        "<title>{}</title>"
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="8"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text>'.format(
            esc(title + " — " + " · ".join(notes)), x, y, w, h, cx, cy, spans
        )
    )
    attrs = 'class="stg" data-node="st-{}"'.format(esc(key))
    if href:
        return '<a href="{}" {}>{}</a>'.format(esc(href), attrs, body)
    return "<g {}>{}</g>".format(attrs, body)


def _st_edge(edge_id, x1, y1, x2, y2, qx=None, qy=None, alt=False):
    """One directed station edge (a straight segment, or a quadratic when a
    bow point is given), arrow-headed and keyed by `data-edge` so the tests
    can assert the flow topology rather than coordinates."""
    if qx is None:
        d = "M{:.1f},{:.1f} L{:.1f},{:.1f}".format(x1, y1, x2, y2)
    else:
        d = "M{:.1f},{:.1f} Q{:.1f},{:.1f} {:.1f},{:.1f}".format(x1, y1, qx, qy, x2, y2)
    return (
        '<path class="{}" data-edge="{}" d="{}" marker-end="url(#stnarrow)"/>'.format(
            "stedge alt" if alt else "stedge", esc(edge_id), d
        )
    )


def _station_svg(root):
    """The station cycle as one self-contained SVG. Layout is a fixed rounded-
    rectangle circuit (three columns x two rows): the top row runs dispatcher
    tick -> claim -> lane build, the right column fans build out into the
    derived terminal outcomes and back into the station refresh (three arrows
    into one merge — the §A3 property, made unmissable), the bottom row runs
    refresh -> merge slot -> trunk advance, and the left column closes the ring
    through the intake mint back to the tick. Every edge carries an arrowhead
    (the WI-250 critique's lesson: a border is not a directed cycle)."""

    def home(rel):
        return rel if (root / rel).exists() else None

    # The work-item registry's home, whichever it is (Phase 2b): the spec folder
    # when this repo has migrated, else the CSV (an existence probe, so every
    # emitted href resolves; a repo missing a home renders a plain card).
    wi_home = home("docs/work") or home("docs/requirements/work-items.csv")
    log_home = home("docs/log.md")
    opts_doc = _process_doc(
        root, "docs/process-options.md", "project-trajectory/PROCESS_OPTIONS.md"
    )

    g = STATION_GEOM
    L, M, R = g["colL"], g["colM"], g["colR"]
    T, B, iy = g["rowT"], g["rowB"], g["iy"]
    w, h = g["cardw"], g["cardh"]
    ow, oh = g["outw"], g["outh"]
    oy = g["oy"]
    outcomes = _outcome_cards()
    bar_label = station.BAR_GREEN.rstrip(":")

    # The ring edges + the outcome fan, one closed directed cycle. Anchors are
    # card-edge points; ends stop 5px short so the arrowheads land cleanly.
    edges = [
        _st_edge("tick-claim", L + 93.0, T, M - 93.0, T),
        _st_edge("claim-build", M + 88.0, T, R - 93.0, T),
        _st_edge("build-{}".format(outcomes[0][0]), R, T + h / 2, R, oy[0] - 27.0),
        _st_edge(
            "build-{}".format(outcomes[1][0]),
            R - 88.0,
            T + 16.0,
            R - 89.0,
            oy[1],
            qx=585.0,
            qy=170.0,
        ),
        _st_edge(
            "build-{}".format(outcomes[2][0]),
            R - 88.0,
            T + 26.0,
            R - 89.0,
            oy[2],
            qx=560.0,
            qy=206.0,
        ),
        _st_edge(
            "{}-refresh".format(outcomes[0][0]),
            R + 84.0,
            oy[0],
            R + 68.0,
            B - 36.0,
            qx=898.0,
            qy=282.0,
        ),
        _st_edge(
            "{}-refresh".format(outcomes[1][0]),
            R + 84.0,
            oy[1],
            R + 36.0,
            B - 36.0,
            qx=880.0,
            qy=317.0,
        ),
        _st_edge("{}-refresh".format(outcomes[2][0]), R, oy[2] + 22.0, R, B - 36.0),
        _st_edge("refresh-slot", R - 88.0, B, M + 93.0, B),
        _st_edge("slot-advance", M - 88.0, B, L + 93.0, B),
        _st_edge("advance-intake", L, B - h / 2, L, iy + 36.0),
        _st_edge("intake-tick", L, iy - h / 2, L, T + 36.0),
        # The one bounded retry: a lost slot race re-refreshes (dashed).
        _st_edge(
            "slot-refresh",
            M + 64.0,
            B + 35.0,
            R - 20.0,
            B + 34.0,
            qx=605.0,
            qy=512.0,
            alt=True,
        ),
    ]

    # The spine barrier, drawn as a gate ON the admission edge (tick -> claim):
    # an exclusive-kind row stops new admission until the station is idle.
    barrier = (
        '<g class="stbarrier"><title>The spine barrier — an exclusive-kind row '
        "({}) stops new admission; the lanes drain; the batch runs alone as the "
        "sole toucher of trunk.</title>"
        '<rect class="stbar" x="288.5" y="58.0" width="3.5" height="24.0"/>'
        '<rect class="stbar" x="296.5" y="58.0" width="3.5" height="24.0"/>'
        '<text class="stbarlab" x="294.0" y="96.0" text-anchor="middle">'
        "spine barrier</text></g>".format(esc(" · ".join(_exclusive_kinds())))
    )

    # The §A3 property, stated once in the ring's empty center; line two is the
    # derived outcome vocabulary itself.
    center = (
        '<text class="stprop" x="{:.1f}" y="238.0" text-anchor="middle">'
        "every lane ends in a merge</text>"
        '<text class="stprop2" x="{:.1f}" y="256.0" text-anchor="middle">'
        "{} — a branch never hangs</text>".format(
            M, M, esc(" · ".join(name for name, _ in outcomes))
        )
    )
    race_label = (
        '<text class="stlab" x="600.0" y="505.0" text-anchor="middle">'
        "lost race → refresh again</text>"
    )

    # Lane multiplicity: the build card renders over a stacked shadow pair —
    # up to `lanes` worker lanes run this leg in parallel (§A4.3).
    shadows = "".join(
        '<rect class="stshadow" x="{:.1f}" y="{:.1f}" width="{:.1f}" '
        'height="{:.1f}" rx="8"/>'.format(R - w / 2 + d, T - h / 2 + d, w, h)
        for d in (16.0, 8.0)
    )

    cards = [
        _station_card(
            "tick",
            "Dispatcher tick",
            ("frontier → admission by kind", "exclusive row ⇒ the barrier"),
            opts_doc,
            L,
            T,
            w,
            h,
        ),
        _station_card(
            "claim",
            "Claim",
            ("serial trunk commit · branch cut", "specs → active/<branch>/"),
            wi_home,
            M,
            T,
            w,
            h,
        ),
        shadows,
        _station_card(
            "build",
            "Lane build",
            ("one worker session per lane", "own worktree · parallel lanes"),
            log_home,
            R,
            T,
            w,
            h,
        ),
    ]
    for (name, dirs), y in zip(outcomes, oy):
        target = "queued" if "queued" in dirs else dirs[0]
        cards.append(
            _station_card(
                name,
                name,
                ("specs → " + " ".join(d + "/" for d in dirs),),
                # WI-504 (OI-55 ruled (a)): the three terminal dirs are the
                # ONLY status dirs `_outcome_cards` ever names (it is derived
                # from `station.OUTCOME_DIRS`, which holds no open state), and
                # they now live under the archive, one directory deeper — the
                # card should link a viewer to where the specs actually are,
                # not to the tombstone README left behind at the old path.
                home("docs/archive/work/" + target),
                R,
                y,
                ow,
                oh,
            )
        )
    cards += [
        _station_card(
            "refresh",
            "Station refresh",
            (
                "merge trunk in · trunk_step · bar",
                "green ⇒ {} @ branch tip".format(bar_label),
            ),
            opts_doc,
            R,
            B,
            w,
            h,
        ),
        # The merge slot, the cycle's serial waist — the emphasized node,
        # emitted in flow order (refresh → slot → advance): nothing overlaps
        # it, so source order can read as the ring reads.
        '<g class="slot" data-node="st-slot"><title>The merge slot — the '
        "exclusive turn to advance trunk. Serial and sub-second: the bar runs "
        "outside it, the slot only re-checks ancestry and merges.</title>"
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="12"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
        '<tspan class="slotname" x="{:.1f}" dy="-12">Merge slot</tspan>'
        '<tspan class="slotsub" x="{:.1f}" dy="15">serial · one branch at a time'
        "</tspan>"
        '<tspan class="slotsub" x="{:.1f}" dy="12">ancestor check → --no-ff '
        "merge</tspan></text></g>".format(M - w / 2, B - h / 2, w, h, M, B, M, M, M),
        _station_card(
            "advance",
            "Trunk advance",
            ("advance trunk to the barred tree", "unload the lane worktree"),
            log_home,
            L,
            B,
            w,
            h,
        ),
        _station_card(
            "intake",
            "Intake mint",
            ("new rows at the landed merge:", "amendment · disposition · drafts"),
            wi_home,
            L,
            iy,
            w,
            h,
        ),
    ]

    defs = _arrow_markers(("stnarrow", "stnarrow-head"))
    body = (
        defs
        + '<g class="ring" data-cycle="closed">'
        + "".join(edges)
        + "</g>"
        + barrier
        + center
        + race_label
        + "".join(cards)
    )
    return (
        '<svg class="stationsvg" viewBox="0 0 {:.0f} {:.0f}" style="{}" '
        'preserveAspectRatio="xMidYMid meet" role="{}" '
        'aria-label="The station cycle drawn as one directed loop: dispatcher '
        "tick, claim, lane build, the terminal outcomes converging on the "
        "station refresh, the serial merge slot, trunk advance and the intake "
        'mint">{}</svg>'.format(
            g["width"], g["height"], _svg_fit_style(g["width"]), _svg_role(body), body
        )
    )


def _station_panel(root):
    """The station cycle (the concurrency-v2 flow as shipped by dispatch.py /
    lane.py / integrate.py / intake.py) as a self-contained block: the SVG ring
    plus the escalation notes no card has room to state — the barrier, the
    admission arms, the empty-frontier ladder and the two bounded retries.
    Stage links resolve via existence probes; no clocks, no repo counts: the
    structure is the method's, not the repo's data, so it renders
    byte-identically regardless of the registries."""

    def home(rel):
        return rel if (root / rel).exists() else None

    oi_home = home("docs/open-items.html")
    oi_link = (
        '<a href="{}">open-items.html</a>'.format(esc(oi_home))
        if oi_home
        else "open-items.html"
    )
    notes = (
        '<ul class="esc">\n'
        "<li><b>Spine barrier</b> — an exclusive-kind row ({kinds}) stops new "
        "admission; the lanes drain; the batch runs alone — one window, one "
        "owner sitting.</li>\n"
        "<li><b>Admission arms</b> — what the dispatcher does with a ready row, "
        "by kind × the declared gate policy: {arms}. Surfaced approvals "
        "drain to cards on {oi}; the run exits 0 with the asks visible.</li>\n"
        "<li><b>Empty frontier</b> — the exit ladder: a registry gap census "
        "hands the intake its mint (gap-closure rows re-fill the frontier); "
        "else pending approvals surface; else an honest drain.</li>\n"
        "<li><b>Red bar · lost race</b> — a red refresh goes back to the lane "
        "to fix on the branch; a slot ancestor miss re-refreshes, and after one "
        "lost race the branch takes the slot for its retry.</li>\n"
        "</ul>"
    ).format(
        kinds=esc(" · ".join(_exclusive_kinds())),
        arms=esc(" · ".join(_ADMISSION_ARMS)),
        oi=oi_link,
    )
    # WI-415 (390px legibility): the ring no longer shrinks past the shared
    # SHRINK_FLOOR (_station_svg's inline style), so a narrow viewport now
    # overflows instead of blurring the notes to ~3.3 CSS px — the SAME
    # scroll-signal pattern the OKF graph / drill / seam / module views already
    # carry (WI-219/WI-256), not a new affordance invented for this panel.
    return (
        SCROLL_CUE
        + '<div class="tablescroll" {}>'.format(
            _hscroll("Station cycle, horizontally scrollable")
        )
        + '<div class="station">{}</div>'.format(_station_svg(root))
        + "</div>\n"
        + notes
    )


def process_panel(root, wis, stats):
    """The Process tab + panel as (tab, panel), or None when there is no
    docs/stage (the tab is then omitted -> a stage-less repo renders
    byte-identically; the Knowledge-tab vacuity idiom). Three linked panels:
    artifact lifecycle x the stage ladder (live tier counts; the tier whose rung
    the repo currently stands at is highlighted), the station cycle (WI-389 — the
    concurrency-v2 station/lane model as shipped, its vocabulary derived
    from the flow modules' own constants), and slices -> phase -> the check bars
    (commit bar vs gate bar). Fully self-contained (style inside the panel, no
    script needed — the shared tab switcher handles it); sorted inputs, no
    clocks."""
    stage = _stage_value(root)
    if not stage:
        return None

    proc_doc = _process_doc(root, "docs/process.md", "project-trajectory/PROCESS.md")
    opts_doc = _process_doc(
        root, "docs/process-options.md", "project-trajectory/PROCESS_OPTIONS.md"
    )

    # Panel 1 — artifact lifecycle x THE STAGE LADDER. Live counts join the spine
    # registries; a TIER is highlighted when the repo's effective stage falls in
    # that tier's rung span.
    #
    # RE-KEYED FROM BAR SPANS TO RUNGS (WI-498 slice 5), and this was forced, not
    # cosmetic: the value fed in here used to be a BAR (one of three) and the
    # spans were bar spans, so with `docs/stage` supplying a RUNG (one of eight) a
    # repo standing at DevStg-Arch or DevStg-LLReqs would have matched no row at
    # all and the panel would have highlighted nothing, silently. Under one
    # vocabulary the mapping also gets simpler to state: each tier is named for
    # the rung at which producing it IS the work in hand.
    #
    # The two FRAME rungs ride with the tier that authors them, which is the
    # bundling this panel already used for architecture: `DevStg-Boundary` sits
    # with SR because the crossings are a requirements-tier artifact
    # (docs/requirements/external.toml), exactly as `DevStg-Arch` sits with LLR.
    # Six rows against eight rungs, and no row claims `DevStg-Release` — nothing
    # derives that rung (slice 3), so a row highlighting there would be a claim
    # the axis cannot make.
    #
    # NB "tier" below is a lifecycle ROW of this panel; the rung beside it is the
    # process.md §4 stage. One ladder now, so the old "two different axes" caveat
    # this comment used to carry is gone with the axis it warned about.
    tiers = [
        ("Vision", "", "one home (the README tag)"),
        ("SN", "DevStg-Needs", "{} SN".format(stats["sn_total"])),
        (
            "SR",
            "DevStg-Boundary→DevStg-Reqs",
            "{} SR · {} approved".format(stats["sr_total"], stats["sr_verified"]),
        ),
        (
            "LLR + architecture",
            "DevStg-Arch→DevStg-LLReqs",
            "{} LLR".format(stats["llr_total"]),
        ),
        ("TC", "DevStg-Tests", "{} TC".format(stats["tc_total"])),
        (
            "code + tests",
            "DevStg-Impl",
            "{} of {} SR approved".format(stats["sr_verified"], stats["sr_total"]),
        ),
    ]
    stage_lis = []
    for label, span, note in tiers:
        now = stage in span.split("→") if span else False
        stage_lis.append(
            '<li class="stg{cls}" data-stages="{span}">{tag}<b>{label}</b>'
            '<span class="g">{spantxt}</span>'
            '<span class="n">{note}</span></li>'.format(
                cls=" now" if now else "",
                span=esc(span),
                # WI-470 (SR-052/A3 coverage): the "now" marker used to be an
                # accent BORDER alone — colour is the only thing that told a
                # reader which tier is current, one panel away from the plain
                # "Next stage to clear" sentence above. This pairs it with a
                # word at the marked tier itself, not just elsewhere on the page.
                tag='<span class="nowtag">now</span>' if now else "",
                label=esc(label),
                spantxt=esc(span or "—"),
                note=esc(note),
            )
        )

    # Panel 3 — the slice -> phase -> check-bar cadence (the docs/work/ registry
    # is canonical). "Bar" here is the SURVIVING sense — a set of checks that must
    # pass — not the retired three-value axis; the heading says which.
    wi_done = sum(1 for w in wis if w["status"] == "done")
    bars = [
        ("per-WI slice", "one scoped work item; ends at the commit bar"),
        ("commit bar", "the per-commit suite + doc checks — every commit"),
        ("phase close", "a phase's slices batch to one re-attestation sitting"),
        ("rung bar", "the full check.py --stage run at phase close / advance"),
        ("CI", "runs the same bar on every push"),
    ]
    bar_lis = "".join(
        '<li class="stg"><b>{}</b><span class="n">{}</span></li>'.format(esc(b), esc(n))
        for b, n in bars
    )

    # Panel 2 — the station cycle (WI-389). The pre-station resume-loop chips
    # died with the serial loop they drew; the station render derives its own
    # vocabulary (see _station_svg).
    station_html = _station_panel(root)

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
        # The worded pair to the accent border above (WI-470): the word "now"
        # is what survives without colour perception, the border is decoration
        # on top of it. Coloured TEXT on --surface, not a filled badge — the
        # same combination `.pflow .g` already uses below, deliberately: an
        # accent FILL with white text measures 2.98:1 in dark theme (checked
        # against the A4 threshold this dashboard holds itself to elsewhere,
        # e.g. the WI-293 --slot note), which a second filled chip here would
        # have repeated.
        "#process .pflow li.now .nowtag{display:block;font-size:var(--tiny);"
        "font-weight:800;letter-spacing:.06em;text-transform:uppercase;"
        "color:var(--accent);margin-bottom:.15rem;}"
        "#process .pflow li.opt{border-style:dashed;}"
        "#process .pflow b{display:block;font-size:var(--small);}"
        "#process .pflow .g{display:block;font-size:var(--tiny);font-weight:700;"
        "letter-spacing:.04em;color:var(--accent);}"
        "#process .pflow .n{display:block;font-size:var(--tiny);color:var(--muted);}"
        "#process ul.esc{font-size:var(--body);color:var(--muted);margin:.4rem 0 0;"
        "padding-left:1.2rem;}"
        "#process ul.esc b{color:var(--text);}"
        # Panel 2 — the station cycle, a single self-contained SVG
        # (`.stationsvg`): `.stedge` paths carry the directional arrows (the
        # dashed `.alt` edge is the bounded lost-race retry), `.stg` cards are
        # the stations, and the `.slot` node — the serial merge waist — renders
        # last, emphasized on its own theme-invariant fill token.
        "#process .station{margin:.7rem 0;}"
        # WI-415 (390px legibility): sizing lives in the inline `style=` attribute
        # (`_svg_fit_style`, the same SHRINK_FLOOR-governed floor the icicle/dag/
        # know diagrams already use), not here — a hardcoded `max-width:860px`
        # with no `min-width` let the ring shrink all the way to the viewport,
        # which is what rendered ~3.3 CSS px note text at 390 px.
        "#process .stationsvg{display:block;margin:0 auto;font-family:inherit;}"
        "#process .stedge{fill:none;stroke:var(--muted);stroke-width:var(--w-line);"
        "opacity:var(--o-muted);}"
        "#process .stedge.alt{stroke-dasharray:5 4;}"
        "#process .stnarrow-head{fill:var(--muted);}"
        "#process a.stg{cursor:pointer;}"
        "#process .stg rect{fill:var(--surface);stroke:var(--border);"
        "stroke-width:var(--w-line);filter:drop-shadow(0 1px 2px rgba(15,23,42,.12));}"
        "#process a.stg:hover rect,#process a.stg:focus rect{stroke:var(--accent);"
        "stroke-width:var(--w-emph);}"
        "#process .stg:focus{outline:none;}"
        "#process .stgt{fill:var(--text);font-size:var(--nlabel);font-weight:700;}"
        "#process .stgn{fill:var(--muted);font-size:var(--nsub);}"
        "#process .stshadow{fill:var(--surface);stroke:var(--border);"
        "stroke-width:var(--w-line);}"
        "#process .stbar{fill:var(--accent);}"
        "#process .stbarlab{fill:var(--accent);font-size:var(--nsub);"
        "font-weight:700;letter-spacing:.02em;}"
        "#process .stlab{fill:var(--muted);font-size:var(--nsub);}"
        "#process .stprop{fill:var(--text);font-size:var(--nlabel);font-weight:700;}"
        "#process .stprop2{fill:var(--muted);font-size:var(--nsub);}"
        "#process .slot rect{fill:var(--slot);stroke:var(--slot);"
        "filter:drop-shadow(0 2px 5px rgba(15,23,42,.28));}"
        "#process .slotname{fill:#fff;font-size:var(--nhead);font-weight:800;}"
        # A4 (WI-293): no fill-opacity discount on slot sub-labels — the same
        # rule `.sub`/`.bsub` already follow. At .85 the effective ink dropped
        # to 2.57:1 in dark theme; at full opacity on --slot it is 6.29:1.
        "#process .slotsub{fill:#fff;font-size:var(--nsub);}"
        "</style>"
    )
    panel = (
        tab_panel_open("process") + "\n"
        "<h2>How this project is built</h2>\n"
        '<p class="cap">The method reference — the other tabs show project '
        "<em>state</em>; this one shows the <strong>process</strong> the state "
        "moves through. Data-derived where a canonical source exists "
        "(<code>docs/stage</code>, the spine registries, "
        "<code>docs/work/</code>). A view — the process docs are the source "
        "of truth.</p>\n" + style + "\n"
        '<p class="gnow">Stage: <b>' + esc(stage) + "</b> — the rung this repo is "
        "IN, derived over its settled spine and recorded in <code>docs/stage</code> "
        "(<code>derive_stage.py</code>). ONE ladder: a stage is a state, and "
        "approval is the event that moves it. The highlighted tier is the one "
        "whose artifacts are the work in hand at this rung.</p>\n"
        "<h3>1 · Artifact lifecycle × the stage ladder</h3>\n"
        '<p class="cap">Each tier decomposes the one above it; beside it is the '
        "rung at which producing that tier IS the work — the tiers (§3) and the "
        "ladder (§4) live "
        'in <a href="' + esc(proc_doc) + '">' + esc(proc_doc) + "</a>. Counts are "
        "live from this repo's registries.</p>\n"
        '<ol class="pflow">' + "".join(stage_lis) + "</ol>\n"
        "<h3>2 · The station cycle</h3>\n"
        '<p class="cap">One work item, once around the loop: claimed off the '
        "ready frontier onto its own lane, built by one worker session, closed "
        "into a terminal outcome, refreshed against trunk, and merged through "
        "the serial slot — the intake mint then feeds the registry back to the "
        'dispatcher. The full contract is <a href="'
        + esc(opts_doc)
        + '">'
        + esc(opts_doc)
        + "</a> “Unattended operation” · “Parallel work”.</p>\n"
        + station_html
        + "\n"
        "<h3>3 · Slices → phase → the check bars</h3>\n"
        '<p class="cap">A per-WI slice ends at the <strong>commit bar</strong>; '
        "a phase closes at the <strong>rung bar</strong> — the commit-bar-vs-rung-bar "
        'cadence lives in <a href="'
        + esc(opts_doc)
        + '">'
        + esc(opts_doc)
        + "</a> “Trajectory / work-items layer”. Live from "
        "<code>docs/work/</code>: "
        + esc(len(wis))
        + " work items · "
        + esc(wi_done)
        + " done.</p>\n"
        '<ol class="pflow">' + bar_lis + "</ol>\n"
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
        open_left = any(r["disposition"] not in ("done", "cancelled") for r in records)
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
            # The unmet hard predecessors that hold this WI (WI-267: a
            # `cancelled` dead-end predecessor also shows — never `done`).
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
