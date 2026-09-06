"""The System-context view: the depth-0 FRAME, rendered (WI-455).

Sitting-2 decision 8 ruled that the boundary record — SN-040's "kept with the
architecture" — is SATISFIED by a DERIVED view rather than by a picture drawn
beside an architecture document. This module IS that view: the LOCKED frame in
`docs/requirements/external.toml` (who is outside, what crosses the boundary,
and the external-to-external flows the system is not a party to) laid out as one
self-contained SVG plus the full row tables, spliced into the same How tab that
already carries the derived structure and the authored narrative. Nothing here
edits the frame and nothing restates it: the render model is
`traj_parse.frame_context`.

ITS OWN MODULE rather than a seventh section of `traj_views.py`, and that was
the ratchet's call, not a preference: the view lands at ~440 lines and would
have pushed `traj_views` past the module-size decomposition threshold
(`tests/test_module_size_ratchet.py`, now measured in SLOC), whose rule is
decompose, never bump. It
is a clean seam anyway — one data source, one tab block, no shared state with
the What/When/How-SW views.

A VIEW IMPORTS RENDER PRIMITIVES AND NOTHING ELSE (WI-483): this is a render
leaf — it takes an already-loaded read model and returns markup, writes nothing,
and imports no lifecycle service (`tests/test_import_layers.py`).

Fully server-computed (fixed geometry, `.1f` rounding, id-sorted inputs, no
clocks), so the `--check` freshness byte-compare stays stable; a repo with no
`external.toml` renders byte-identically to before the view existed.
"""

from .traj_render import (
    SCROLL_CUE,
    _arrow_markers,
    _hscroll,
    _svg_fit_style,
    _svg_role,
    esc,
)


# The diagram's fixed geometry. One lane per crossing; the parties in a column
# at `gutter`, the system opposite at `sysx`, and the relationship arcs bowing
# into the gutter's own margin so they never cross the system card.
CTX_GEOM = {
    "gutter": 150.0,  # left margin the relationship arcs bow into
    "entw": 214.0,  # entity-card width
    "sysx": 610.0,  # system-card left edge
    "sysw": 236.0,  # system-card width
    "lane": 74.0,  # one crossing lane's pitch
    "top": 52.0,  # the first lane's center
    "width": 900.0,  # viewBox width
    "pad": 46.0,  # below the last lane
    "cardpad": 26.0,  # an entity card's reach above/below its outermost lane
    "carrymax": 54,  # `carries` chars on the wire before it truncates
    "namemax": 30,  # entity-name chars on its card
}

# The system's own point of view, spelled once: a crossing's `direction` is read
# FROM THE SYSTEM (the registry's closed vocabulary), so `in` draws party →
# system and `out` draws system → party. An unrecognised value falls back to the
# undirected line rather than guessing a heading.
_CTX_HEADS = {
    "in": (False, True),
    "out": (True, False),
    "inout": (True, True),
}


def _ctx_cut(text, budget):
    """`text` fitted to a wire/card label, ellipsized rather than clipped. The
    whole cell always rides the element's `<title>`, so truncation here never
    loses information."""
    text = " ".join(text.split())
    return text if len(text) <= budget else text[: budget - 1] + "…"


def _ctx_layout(frame):
    """`(order, spans, lanes, height)` for the context diagram.

    ONE LANE PER CROSSING, grouped so an entity's crossings are contiguous and
    its card can span them: the frame's parties differ in how many boundaries
    they hold (this repo's session entity holds three, the package one), and a
    one-row-per-entity layout would have to stack three labels on one wire.
    Entities that hold no crossing keep a lane of their own — a declared party
    with nothing crossing is a real frame state, not an empty row to drop."""
    g = CTX_GEOM
    by_entity = {}
    for c in frame["crossings"]:
        by_entity.setdefault(c["entity"] or "—", []).append(c)
    declared = [e["id"] for e in frame["entities"]]
    # Declared parties that hold crossings first (in registry id order), then any
    # party a crossing names but the frame does not declare — an integrity finding
    # `trace.py` reports, which this view must show rather than silently drop —
    # then the declared parties with no crossing.
    order = (
        [e for e in declared if e in by_entity]
        + sorted(k for k in by_entity if k not in declared)
        + [e for e in declared if e not in by_entity]
    )
    spans, lanes, i = {}, [], 0
    for ent in order:
        first = i
        for c in by_entity.get(ent, []):
            lanes.append((ent, c, g["top"] + i * g["lane"]))
            i += 1
        if not by_entity.get(ent):
            i += 1
        spans[ent] = (g["top"] + first * g["lane"], g["top"] + (i - 1) * g["lane"])
    return order, spans, lanes, g["top"] + max(i, 1) * g["lane"] + g["pad"]


def _ctx_entity_card(ent, name, kls, y0, y1):
    """One external party's card: the name, and beneath it the row id plus the
    frame's `class` vocabulary term for the party."""
    g = CTX_GEOM
    y, h = y0 - g["cardpad"], (y1 - y0) + 2 * g["cardpad"]
    cx, cy = g["gutter"] + g["entw"] / 2, (y0 + y1) / 2
    sub = ent + (" · " + kls if kls else "")
    return (
        '<g class="ctxent" data-node="{}"><title>{}</title>'
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="8"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
        '<tspan class="ctxname" x="{:.1f}" dy="-3">{}</tspan>'
        '<tspan class="ctxsub" x="{:.1f}" dy="15">{}</tspan></text></g>'.format(
            esc(ent),
            esc("{} — {}{}".format(ent, name or ent, " (" + kls + ")" if kls else "")),
            g["gutter"],
            y,
            g["entw"],
            h,
            cx,
            cy,
            cx,
            esc(_ctx_cut(name or ent, g["namemax"])),
            cx,
            esc(sub),
        )
    )


def _ctx_wire(crossing, y):
    """One boundary crossing as a directed wire between its party's card and the
    system card, labelled with the crossing id, its direction and the head of
    what it carries.

    An UNREALIZED crossing (no interface row ties back to it) draws dashed. That
    is not decoration: the frame is locked and a crossing exists whether or not
    any module realizes it yet, so the view has to be able to say "declared, not
    yet realized" without a hand-maintained annotation."""
    g = CTX_GEOM
    x1, x2 = g["gutter"] + g["entw"] + 6.0, g["sysx"] - 6.0
    direction = crossing["direction"]
    start, end = _CTX_HEADS.get(direction, (False, False))
    ifs = crossing["realized_by"]
    label = crossing["id"] + (" · " + direction if direction else "")
    return (
        '<g class="ctxcross{dash}" data-edge="{eid}"><title>{tip}</title>'
        '<path class="ctxwire" d="M{x1:.1f},{y:.1f} L{x2:.1f},{y:.1f}"{heads}/>'
        '<text class="ctxwlab" x="{mx:.1f}" y="{ly:.1f}" text-anchor="middle">'
        "{label}</text>"
        '<text class="ctxwsub" x="{mx:.1f}" y="{sy:.1f}" text-anchor="middle">'
        "{carries}</text></g>".format(
            dash="" if ifs else " unrealized",
            eid=esc(crossing["id"]),
            tip=esc(
                "{} ({}) — {} | {}".format(
                    crossing["id"],
                    direction or "direction unstated",
                    crossing["carries"] or "carries unstated",
                    "realized by " + ", ".join(i for i, _ in ifs)
                    if ifs
                    else "no interface row realizes it yet",
                )
            ),
            x1=x1,
            x2=x2,
            y=y,
            heads=(' marker-start="url(#ctxarrow)"' if start else "")
            + (' marker-end="url(#ctxarrow)"' if end else ""),
            mx=(x1 + x2) / 2,
            ly=y - 9.0,
            sy=y + 14.0,
            label=esc(label),
            carries=esc(_ctx_cut(crossing["carries"], g["carrymax"])),
        )
    )


def _ctx_rel_arc(rel, i, spans):
    """One external-to-external relationship, bowed into the left gutter between
    the two parties' cards — never through the system card, because the system
    is not a party to it. A self-referential row (both ends one party) draws a
    small loop off that card rather than a degenerate zero-length curve."""
    g = CTX_GEOM
    a, b = spans.get(rel["from"]), spans.get(rel["to"])
    if a is None or b is None:
        return ""  # a party the frame does not declare — the table still states it
    ay, by = (a[0] + a[1]) / 2, (b[0] + b[1]) / 2
    qx = g["gutter"] - 30.0 - 26.0 * i
    if rel["from"] == rel["to"]:
        y1, y2 = ay - 15.0, ay + 15.0
    else:
        y1, y2 = ay, by
    d = "M{:.1f},{:.1f} Q{:.1f},{:.1f} {:.1f},{:.1f}".format(
        g["gutter"], y1, qx, (y1 + y2) / 2, g["gutter"], y2
    )
    return (
        '<g class="ctxrel" data-edge="{}"><title>{}</title>'
        '<path d="{}" marker-end="url(#ctxarrow)"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text></g>'.format(
            esc(rel["id"]),
            esc(
                "{} — {} → {} ({}): {}".format(
                    rel["id"],
                    rel["from_name"] or rel["from"],
                    rel["to_name"] or rel["to"],
                    rel["kind"] or "kind unstated",
                    rel["flow"] or "flow unstated",
                )
            ),
            d,
            qx,
            (y1 + y2) / 2 - 8.0,
            esc(rel["id"]),
        )
    )


def _context_svg(frame, project):
    """The depth-0 frame as one self-contained SVG: the external parties in a
    column, the system as the emphasized card opposite them, every declared
    crossing a directed wire between the two, and the external-to-external
    relationships bowed clear of the system entirely."""
    g = CTX_GEOM
    order, spans, lanes, height = _ctx_layout(frame)
    ent_name = {e["id"]: e for e in frame["entities"]}
    cards = [
        _ctx_entity_card(
            ent,
            (ent_name.get(ent) or {}).get("name", ""),
            (ent_name.get(ent) or {}).get("class", ""),
            *spans[ent],
        )
        for ent in order
    ]
    wires = [_ctx_wire(c, y) for _ent, c, y in lanes]
    arcs = [_ctx_rel_arc(r, i, spans) for i, r in enumerate(frame["relationships"])]
    sys_y = g["top"] - 32.0
    sys_h = max(y for _e, _c, y in lanes) - g["top"] + 64.0 if lanes else 64.0
    sys_cy = sys_y + sys_h / 2
    sys_cx = g["sysx"] + g["sysw"] / 2
    system = (
        '<g class="ctxsys" data-node="system"><title>{}</title>'
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="12"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
        '<tspan class="ctxsysname" x="{:.1f}" dy="-8">{}</tspan>'
        '<tspan class="ctxsyssub" x="{:.1f}" dy="17">the system — depth 0</tspan>'
        '<tspan class="ctxsyssub" x="{:.1f}" dy="14">{} crossing(s) declared'
        "</tspan></text></g>".format(
            esc(
                "{} — the system this frame is drawn around. Everything outside "
                "it is a party; every wire is a declared crossing.".format(project)
            ),
            g["sysx"],
            sys_y,
            g["sysw"],
            sys_h,
            sys_cx,
            sys_cy,
            sys_cx,
            esc(_ctx_cut(project, CTX_GEOM["namemax"])),
            sys_cx,
            sys_cx,
            len(frame["crossings"]),
        )
    )
    body = (
        _arrow_markers(("ctxarrow", "ctxarrow-head"))
        + "".join(arcs)
        + "".join(wires)
        + "".join(cards)
        + system
    )
    return (
        '<svg class="ctxsvg" viewBox="0 0 {:.0f} {:.0f}" style="{}" '
        'preserveAspectRatio="xMidYMid meet" role="{}" '
        'aria-label="The depth-0 frame: the external parties in a column, the '
        "system opposite them, each declared boundary crossing a directed wire "
        'between the two, and the external-to-external relationships">{}</svg>'.format(
            g["width"], height, _svg_fit_style(g["width"]), _svg_role(body), body
        )
    )


CTX_STYLE = (
    "<style>"
    "#sw h3{font-size:var(--body);margin:1.5rem 0 .25rem;letter-spacing:-.01em;}"
    "#sw .context{margin:.7rem 0;}"
    "#sw .ctxsvg{display:block;margin:0 auto;font-family:inherit;}"
    "#sw .ctxent rect{fill:var(--surface);stroke:var(--border);"
    "stroke-width:var(--w-line);filter:drop-shadow(0 1px 2px rgba(15,23,42,.12));}"
    "#sw .ctxname{fill:var(--text);font-size:var(--nlabel);font-weight:700;}"
    "#sw .ctxsub{fill:var(--muted);font-size:var(--nsub);}"
    # The system card takes the merge slot's theme-invariant emphasis token
    # (`--slot`, 6.29:1 against white at full opacity — the WI-293 A4 reading),
    # not `--accent`: this is the one node the eye must find first, and the
    # accent hue is already spoken for by focus rings and "now" markers.
    "#sw .ctxsys rect{fill:var(--slot);stroke:var(--slot);"
    "filter:drop-shadow(0 2px 5px rgba(15,23,42,.28));}"
    "#sw .ctxsysname{fill:#fff;font-size:var(--nhead);font-weight:800;}"
    "#sw .ctxsyssub{fill:#fff;font-size:var(--nsub);}"
    "#sw .ctxwire{fill:none;stroke:var(--muted);stroke-width:var(--w-line);}"
    "#sw .ctxcross.unrealized .ctxwire{stroke-dasharray:5 4;}"
    "#sw .ctxwlab{fill:var(--text);font-size:var(--nlabel);font-weight:700;}"
    "#sw .ctxwsub{fill:var(--muted);font-size:var(--nsub);}"
    "#sw .ctxrel path{fill:none;stroke:var(--muted);stroke-width:var(--w-line);"
    "stroke-dasharray:2 3;}"
    "#sw .ctxrel text{fill:var(--muted);font-size:var(--nsub);font-weight:700;}"
    "#sw .ctxarrow-head{fill:var(--muted);}"
    "#sw .legend i.sys{background:var(--slot);}"
    "#sw .legend i.party{background:var(--surface);border:1px solid var(--border);}"
    "#sw .legend i.unreal,#sw .legend i.rel{background:none;height:0;"
    "border-top:2px dashed var(--muted);}"
    "#sw .legend i.rel{border-top-style:dotted;}"
    "#sw ul.ctxuntied{font-size:var(--body);color:var(--muted);margin:.4rem 0 0;"
    "padding-left:1.2rem;}"
    "#sw ul.ctxuntied b{color:var(--text);}"
    "</style>"
)


def _ctx_table(caption, headers, rows, label):
    """One frame tier as a scrollable table — the same `.swmap` component the
    module map and the CMP registry already render through."""
    head = "".join("<th>{}</th>".format(h) for h in headers)
    body = "".join(
        "<tr>{}</tr>".format("".join("<td>{}</td>".format(c) for c in r)) for r in rows
    )
    return (
        caption
        + SCROLL_CUE
        + '<div class="tablescroll" {}>'.format(_hscroll(label))
        + '<table class="swmap"><thead><tr>{}</tr></thead>'
        "<tbody>{}</tbody></table></div>\n".format(head, body)
    )


def context_block(frame, project):
    """The System-context embed for the How panel (WI-455, sitting-2 decision 8):
    the depth-0 frame as a generated diagram plus its three row tables and the
    adjudicated no-tie-back list. "" when the repo declares no frame, so a
    project that never draws a boundary pays nothing.

    Where the derived structure below it answers "what is this built of", this
    answers the question that has to be settled BEFORE that one — what is
    outside, and what crosses — which is why it renders first in the tab."""
    if not frame:
        return ""
    counts = "{} entit{} · {} crossing(s) · {} relationship(s)".format(
        len(frame["entities"]),
        "y" if len(frame["entities"]) == 1 else "ies",
        len(frame["crossings"]),
        len(frame["relationships"]),
    )
    ent_rows = [
        (
            "<code>{}</code>".format(esc(e["id"])),
            esc(e["name"]),
            esc(e["class"]),
            esc(e["description"]),
            esc(e["status"]),
        )
        for e in frame["entities"]
    ]
    cross_rows = []
    for c in frame["crossings"]:
        ifs = ", ".join(
            "<code>{}</code>".format(esc(i)) for i, _kind in c["realized_by"]
        )
        cross_rows.append(
            (
                "<code>{}</code>".format(esc(c["id"])),
                '{}<br><span class="sub">{}</span>'.format(
                    esc(c["entity_name"] or c["entity"]), esc(c["entity"])
                ),
                esc(c["direction"]),
                esc(c["carries"]),
                esc(c["status"]),
                ifs or '<span class="sub">none — declared, not yet realized</span>',
            )
        )
    rel_rows = [
        (
            "<code>{}</code>".format(esc(r["id"])),
            "{} → {}".format(
                esc(r["from_name"] or r["from"]), esc(r["to_name"] or r["to"])
            ),
            esc(r["kind"]),
            esc(r["flow"]),
            esc(r["status"]),
        )
        for r in frame["relationships"]
    ]
    untied = ""
    if frame["untied"]:
        untied = (
            "<h3>External endpoints that tie back to no crossing</h3>\n"
            '<p class="cap">An interface row whose far end is outside this tree '
            "but which realizes NO declared crossing. Each absence was "
            "adjudicated one row at a time and the reason is recorded on the row "
            "— so the view states them here rather than rendering a frame "
            "shorter than the registry holds.</p>\n"
            '<ul class="ctxuntied">'
            + "".join(
                "<li><b>{}</b> — <code>{}</code>. {}</li>".format(
                    esc(u["id"]), esc(u["endpoint"]), esc(u["reason"])
                )
                for u in frame["untied"]
            )
            + "</ul>\n"
        )
    return (
        "\n<h2>System context (the depth-0 frame)</h2>\n"
        '<p class="cap">Who is outside this system, what crosses its boundary, '
        "and the external-to-external flows the system is <em>not</em> a party "
        "to — derived from <code>docs/requirements/external.toml</code>, whose "
        "rows change only by a recorded ruling. <strong>"
        + esc(counts)
        + ".</strong> A crossing exists whether or not any module realizes it "
        "yet, so the realizing <code>IF-###</code> rows are joined from "
        "<code>interfaces.toml</code> and an unrealized crossing draws dashed. "
        "This is the boundary record itself: generated, never hand-drawn.</p>\n"
        + CTX_STYLE
        + SCROLL_CUE
        + '<div class="tablescroll" {}>'.format(
            _hscroll("System-context diagram, horizontally scrollable")
        )
        + '<div class="context">{}</div>'.format(_context_svg(frame, project))
        + "</div>\n"
        # The swatches take their paint from the CSS tokens by CLASS rather than
        # by an inline hex: `--slot` and `--surface` are declared in the
        # stylesheet, and a legend that restated either as a literal would be a
        # second copy of a theme token — the exact drift U2/U5 exist to catch,
        # and it would also paint the light value in dark theme.
        '<div class="legend">'
        '<span><i class="ctxkey sys"></i>the system</span>'
        '<span><i class="ctxkey party"></i>external party</span>'
        '<span><i class="ctxkey unreal"></i>unrealized crossing</span>'
        '<span><i class="ctxkey rel"></i>external-to-external relationship</span>'
        "</div>\n"
        + _ctx_table(
            "<h3>Boundary crossings</h3>\n",
            ("Crossing", "Party", "Direction", "Carries", "State", "Realized by"),
            cross_rows,
            "Boundary-crossing table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>External parties</h3>\n",
            ("Party", "Name", "Class", "Description", "State"),
            ent_rows,
            "External-party table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>External-to-external relationships</h3>\n"
            '<p class="cap">The system is not a party to these, and they carry no '
            "interface vocabulary: a relationship is not a crossing and never "
            "grows a realizing <code>IF-###</code> row.</p>\n",
            ("Relationship", "Between", "Kind", "Flow", "State"),
            rel_rows,
            "External-relationship table, horizontally scrollable",
        )
        + untied
    )
