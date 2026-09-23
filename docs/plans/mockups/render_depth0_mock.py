"""MOCKUP renderer — the depth-0 view as the assumption-tier plan would leave it.

Not kit code and not a generator of record: it reads the PROPOSED rows in
`external.operating-frame.toml` beside it, joins the live
`docs/requirements/interfaces.toml`, `system-requirements.toml` and
`stakeholder-needs.toml`, and writes `depth0-operating-frame.html` beside it.
The live, LOCKED frame and the live dashboard are untouched. It borrows the
dashboard's own stylesheet (`gen_trajectory.HTML_TEMPLATE`) and the
System-context view's drawing primitives, so the page reads as the How tab
would after the sitting.

Everything the view shows beyond the authored rows is DERIVED here, the way a
real generator would have to derive it: bundle membership from IF tie-backs,
each boundary IF's class (bridged / coincident / unclassified), each bundle's
kind (effect / design) from DA `effect_at`, and each DA's needs from the live
`sn_refs` of the SRs that cite it.

Run from the repo root:  python docs/plans/mockups/render_depth0_mock.py
Delete this folder once the sitting has built the real view.
"""

import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "project-trajectory" / "scripts"))

import gen_trajectory  # noqa: E402  (the dashboard's page stylesheet)
from rendering.traj_context import CTX_STYLE, _ctx_table  # noqa: E402
from rendering.traj_render import (  # noqa: E402
    SCROLL_CUE,
    _arrow_markers,
    _hscroll,
    _svg_fit_style,
    _svg_role,
    esc,
)

MOCK = HERE / "external.operating-frame.toml"
OUT = HERE / "depth0-operating-frame.html"
REQ = ROOT / "docs" / "requirements"

OPERATING = ("operational", "interoperating")
G = {
    "gutter": 250.0,
    "entw": 224.0,
    "sysx": 720.0,
    "sysw": 236.0,
    "lane": 80.0,
    "top": 100.0,
    "width": 1000.0,
    "gap": 72.0,
    "cardpad": 27.0,
    "carrymax": 58,
    "namemax": 30,
}
HEADS = {"in": (False, True), "out": (True, False), "inout": (True, True)}


def cut(text, budget):
    text = " ".join((text or "").split())
    return text if len(text) <= budget else text[: budget - 1] + "…"


def frame_of(row):
    return "operating" if row["class"] in OPERATING else "delivery"


def load():
    def read(name):
        return tomllib.loads((REQ / name).read_text(encoding="utf-8"))

    mock = tomllib.loads(MOCK.read_text(encoding="utf-8"))
    return (
        mock,
        read("interfaces.toml")["interface"],
        read("system-requirements.toml")["requirement"],
        read("stakeholder-needs.toml")["need"],
    )


def derive(mock, ifs, srs):
    """The read model, computed from rows alone."""
    ents = mock["entity"]
    ties = {}
    for iid, row in ifs.items():
        for col in ("interface_from_external", "interface_to_external"):
            if row.get(col):
                ties.setdefault(iid, set()).add(row[col])
    for iid, change in mock.get("retie", {}).items():
        ties[iid] = {change["to"]}
    das = mock.get("assumption", {})
    waivers = mock.get("coincident", {})
    bridged = {i for row in das.values() for i in row["measured_at"]}

    def if_class(iid):
        if iid in bridged:
            return "bridged"
        return "coincident" if iid in waivers else "unclassified"

    cited_by, needs_of = {}, {}
    for sr, refs in mock.get("sr_cites", {}).items():
        for d in refs:
            cited_by.setdefault(d, []).append(sr)
            needs_of.setdefault(d, set()).update(srs.get(sr, {}).get("sn_refs", []))
    party_of_need = {
        sn: stk["party"]
        for stk in mock.get("stakeholder", {}).values()
        for sn in stk["needs"]
    }

    bundles = []
    for bid, b in mock["boundary"].items():
        members = sorted(i for i, bs in ties.items() if bid in bs)
        classes = {i: if_class(i) for i in members}
        landing = sorted(d for d, row in das.items() if bid in row["effect_at"])
        measured = sorted(
            d for d, row in das.items() if set(row["measured_at"]) & set(members)
        )
        bundles.append(
            dict(
                b,
                id=bid,
                frame=frame_of(ents[b["entity"]]),
                ifs=members,
                classes=classes,
                landing=landing,
                measured=measured,
                kind="effect" if landing else "design",
            )
        )
    by_id = {b["id"]: b for b in bundles}

    adopter = sorted(
        iid
        for iid, row in ifs.items()
        if any(
            "downstream adopter" in str(x)
            for x in [row.get("owner", "")]
            + list(row.get("consumers") or [])
            + list(row.get("requestors") or [])
        )
    )
    rigs = sorted(e for e, r in ents.items() if r.get("emulates"))
    fidelity = {row.get("realized_by") for row in das.values()}
    derived_needs = sorted({sn for ns in needs_of.values() for sn in ns})
    unreached = [
        sn
        for sn in derived_needs
        if not any(
            by_id[b]["frame"] == "operating"
            for d, ns in needs_of.items()
            if sn in ns
            for b in das[d]["effect_at"]
        )
    ]
    unclassified = sum(
        1 for b in bundles for c in b["classes"].values() if c == "unclassified"
    )
    checks = [
        (
            "Every DA is cited by at least one SR",
            all(d in cited_by for d in das),
            ", ".join(sorted(d for d in das if d not in cited_by))
            or "{} DA rows, all cited".format(len(das)),
        ),
        (
            "Every DA names a falsifier",
            all(row.get("falsifier") for row in das.values()),
            "the falsifier is prose; evidence links live on TCs (assumption_refs)",
        ),
        (
            "Every rig has a fidelity DA naming it",
            all(e in fidelity for e in rigs),
            ", ".join(rigs),
        ),
        (
            "Every DA lands on a declared bundle and measures declared IFs",
            all(
                all(b in by_id for b in row["effect_at"])
                and all(i in ties for i in row["measured_at"])
                for row in das.values()
            ),
            "effect_at and measured_at resolve",
        ),
        (
            "Every need a DA serves reaches an operating-frame bundle",
            not unreached,
            ", ".join(unreached) or ", ".join(derived_needs),
        ),
        (
            "Every need a DA serves has a stakeholder on the list",
            all(sn in party_of_need for sn in derived_needs),
            ", ".join(sn for sn in derived_needs if sn not in party_of_need)
            or "all listed",
        ),
        (
            "Boundary IFs still unclassified (neither bridged nor coincident)",
            unclassified == 0,
            "{} — the classification work of step 3".format(unclassified),
        ),
    ]
    return bundles, cited_by, needs_of, party_of_need, adopter, checks


def layout(mock, bundles):
    """Lanes top to bottom: the operating frame (its parties' bundles, then the
    parties still open), a gap, then the delivery frame (the deliverable's
    bundle, then the rigs, which cross nothing)."""
    by_party = {}
    for b in bundles:
        by_party.setdefault(b["entity"], []).append(b)
    ents = mock["entity"]
    rows, spans, bands, y = [], {}, [], G["top"]

    def place(key, lane_bundles):
        nonlocal y
        first = y
        for b in lane_bundles or [None]:
            rows.append((key, b, y))
            y += G["lane"]
        spans[key] = (first, y - G["lane"])

    for name in ("operating", "delivery"):
        start = y
        for e, r in ents.items():
            if frame_of(r) == name:
                place(e, by_party.get(e))
        if name == "operating":
            for key in mock.get("open", {}):
                place("open:" + key, None)
        bands.append((name, start, y - G["lane"]))
        y += G["gap"]
    return rows, spans, bands, y - G["gap"] + 30.0


def card(key, mock, y0, y1):
    ents = mock["entity"]
    x, w = G["gutter"], G["entw"]
    y, h = y0 - G["cardpad"], (y1 - y0) + 2 * G["cardpad"]
    cx, cy = x + w / 2, (y0 + y1) / 2
    if key.startswith("open:"):
        o = mock["open"][key[5:]]
        name, sub, kls = o["name"], "open at the sitting", "ctxent ghost"
        tip = o["name"] + " — open at the sitting: " + o["why"]
    else:
        r = ents[key]
        kls = "ctxent" + (" rig" if r.get("emulates") else "")
        kls += "" if frame_of(r) == "operating" else " evo"
        sub = key + " · " + r["class"]
        if r.get("emulates"):
            sub += " · emulates " + r["emulates"]
        name = r["name"]
        tip = "{} — {} ({}): {}".format(key, name, r["class"], r["description"])
    return (
        '<g class="{}" data-node="{}"><title>{}</title>'
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="8"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
        '<tspan class="ctxname" x="{:.1f}" dy="-3">{}</tspan>'
        '<tspan class="ctxsub" x="{:.1f}" dy="15">{}</tspan></text></g>'
    ).format(
        kls,
        esc(key),
        esc(tip),
        x,
        y,
        w,
        h,
        cx,
        cy,
        cx,
        esc(cut(name, G["namemax"])),
        cx,
        esc(cut(sub, 40)),
    )


def summary(b):
    counts = {}
    for c in b["classes"].values():
        counts[c] = counts.get(c, 0) + 1
    ifs = (
        " · ".join(
            "{} {}".format(counts[k], k)
            for k in ("bridged", "coincident", "unclassified")
            if counts.get(k)
        )
        or "no IF of its own"
    )
    if b["landing"]:
        ifs += " · outcome of " + ", ".join(b["landing"])
    return ifs


def wire(b, y):
    x1, x2 = G["gutter"] + G["entw"] + 6.0, G["sysx"] - 6.0
    start, end = HEADS.get(b["direction"], (False, False))
    kls = "ctxcross fx-" + b["kind"] + ("" if b["ifs"] else " unrealized")
    label = "{} · {} · {}".format(b["id"], b["direction"], b["kind"])
    tip = (
        "{} ({}, {}) — {} | interfaces: {} | assumptions measured here: {} "
        "| outcome of: {}"
    ).format(
        b["id"],
        b["direction"],
        b["kind"],
        b["carries"],
        ", ".join("{} ({})".format(i, c) for i, c in b["classes"].items())
        or "none of its own",
        ", ".join(b["measured"]) or "none",
        ", ".join(b["landing"]) or "none",
    )
    mx = (x1 + x2) / 2
    return (
        '<g class="{}" data-edge="{}"><title>{}</title>'
        '<path class="ctxwire" d="M{:.1f},{:.1f} L{:.1f},{:.1f}"{}/>'
        '<text class="ctxwlab" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text>'
        '<text class="ctxwsub" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text>'
        '<text class="ctxwda" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text></g>'
    ).format(
        kls,
        esc(b["id"]),
        esc(tip),
        x1,
        y,
        x2,
        y,
        (' marker-start="url(#ctxarrow)"' if start else "")
        + (' marker-end="url(#ctxarrow)"' if end else ""),
        mx,
        y - 9.0,
        esc(label),
        mx,
        y + 14.0,
        esc(cut(b["carries"], G["carrymax"])),
        mx,
        y + 28.0,
        esc(cut(summary(b), G["carrymax"] + 6)),
    )


def arc(kind, a, b, i, label, tip):
    """A gutter arc between two cards' left edges: the Transition hand-off or an
    emulation edge. Never through a system card."""
    ay, by = (a[0] + a[1]) / 2, (b[0] + b[1]) / 2
    qx = G["gutter"] - 44.0 - 34.0 * i
    d = "M{:.1f},{:.1f} Q{:.1f},{:.1f} {:.1f},{:.1f}".format(
        G["gutter"], ay, qx, (ay + by) / 2, G["gutter"], by
    )
    marker = "ctxemuarrow" if kind == "ctxemu" else "ctxarrow"
    return (
        '<g class="{}"><title>{}</title><path d="{}" marker-end="url(#{})"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text></g>'
    ).format(
        kind,
        esc(tip),
        d,
        marker,
        (G["gutter"] + qx) / 2 - 4.0,  # the curve's apex: a quadratic's midpoint
        (ay + by) / 2 - 6.0,
        esc(label),
    )


def system_card(y0, y1, name, sub1, sub2, tip, kls):
    sy, sh = y0 - 34.0, (y1 - y0) + 68.0
    scx, scy = G["sysx"] + G["sysw"] / 2, sy + sh / 2
    return (
        '<g class="{}" data-node="system"><title>{}</title>'
        '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{:.1f}" rx="12"/>'
        '<text x="{:.1f}" y="{:.1f}" text-anchor="middle">'
        '<tspan class="ctxsysname" x="{:.1f}" dy="-8">{}</tspan>'
        '<tspan class="ctxsyssub" x="{:.1f}" dy="17">{}</tspan>'
        '<tspan class="ctxsyssub" x="{:.1f}" dy="14">{}</tspan></text></g>'
    ).format(
        kls,
        esc(tip),
        G["sysx"],
        sy,
        G["sysw"],
        sh,
        scx,
        scy,
        scx,
        esc(name),
        scx,
        esc(sub1),
        scx,
        esc(sub2),
    )


def svg(mock, bundles):
    rows, spans, bands, height = layout(mock, bundles)
    ents = mock["entity"]
    das = mock.get("assumption", {})
    parts, systems = [], []
    labels = {
        "operating": "OPERATING FRAME — the kit, in operation (system-of-interest)",
        "delivery": (
            "DELIVERY FRAME — this repository's build and release (enabling system)"
        ),
    }
    for name, y0, y1 in bands:
        parts.append(
            # The label sits just right of the gutter, above the band's first
            # card, so no gutter arc crosses it.
            '<g class="ctxplane"><rect x="12" y="{:.1f}" width="{:.1f}" '
            'height="{:.1f}" rx="10"/><text x="{:.1f}" y="{:.1f}">{}</text></g>'.format(
                y0 - 62.0,
                G["width"] - 24.0,
                (y1 - y0) + 98.0,
                G["gutter"] + 4.0,
                y0 - 42.0,
                labels[name],
            )
        )
        lanes = [y for _k, b, y in rows if b and b["frame"] == name]
        if name == "operating":
            n = sum(1 for b in bundles if b["frame"] == name)
            systems.append(
                system_card(
                    min(lanes),
                    max(lanes),
                    "the kit",
                    "in operation",
                    "{} bundle(s) · {} assumption(s)".format(n, len(das)),
                    "The system-of-interest: the kit as it runs in a repository.",
                    "ctxsys",
                )
            )
        else:
            systems.append(
                system_card(
                    y0,
                    y1,
                    "delivery system",
                    "this repository's build and release",
                    "emits the Template · runs the rigs",
                    "The kit's enabling system: builds, verifies and releases it.",
                    "ctxsys evo",
                )
            )
    arcs = []
    for i, (rid, r) in enumerate(mock.get("relationship", {}).items()):
        arcs.append(
            arc(
                "ctxrel",
                spans[r["from"]],
                spans[r["to"]],
                i,
                "Transition",
                "{} — {} → {} ({}): {}".format(
                    rid, r["from"], r["to"], r["kind"], r["flow"]
                ),
            )
        )
    n = len(arcs)
    for j, (eid, r) in enumerate(e for e in ents.items() if e[1].get("emulates")):
        arcs.append(
            arc(
                "ctxemu",
                spans[eid],
                spans[r["emulates"]],
                n + j,
                "emulates",
                "{} emulates {}: {}".format(eid, r["emulates"], r["description"]),
            )
        )
    wires = [wire(b, y) for _k, b, y in rows if b]
    cards = [card(k, mock, *spans[k]) for k in spans]
    body = (
        _arrow_markers(("ctxarrow", "ctxarrow-head"))
        + _arrow_markers(("ctxemuarrow", "ctxemu-head"))
        + "".join(parts)
        + "".join(arcs)
        + "".join(wires)
        + "".join(cards)
        + "".join(systems)
    )
    return (
        '<svg class="ctxsvg" viewBox="0 0 {:.0f} {:.0f}" style="{}" '
        'preserveAspectRatio="xMidYMid meet" role="{}" aria-label="The proposed '
        "depth-0 view in two frames: the kit in operation with its parties and "
        "bundles above; the delivery system with the Template and the rigs below; "
        "the Transition hand-off linking them, and each rig tied to the party it "
        'emulates">{}</svg>'
    ).format(G["width"], height, _svg_fit_style(G["width"]), _svg_role(body), body)


MOCK_STYLE = (
    "<style>"
    "#sw .ctxplane rect{fill:none;stroke:var(--border);stroke-width:1.2;"
    "stroke-dasharray:6 5;}"
    "#sw .ctxplane text{fill:var(--muted);font-size:var(--nsub);font-weight:700;"
    "letter-spacing:.06em;}"
    "#sw .ctxent.evo rect{fill:var(--bg);}"
    "#sw .ctxent.rig rect{stroke:var(--accent);stroke-dasharray:2 3;"
    "stroke-width:1.6;}"
    "#sw .ctxent.ghost rect{fill:none;stroke-dasharray:6 4;filter:none;}"
    "#sw .ctxent.ghost .ctxname{fill:var(--muted);}"
    "#sw .ctxsys.evo rect{fill:var(--surface);stroke:var(--slot);stroke-width:2;}"
    "#sw .ctxsys.evo .ctxsysname,#sw .ctxsys.evo .ctxsyssub{fill:var(--text);}"
    "#sw .fx-effect .ctxwire{stroke:var(--accent);stroke-width:2.6;}"
    "#sw .fx-effect .ctxwlab{fill:var(--accent);}"
    "#sw .ctxwda{fill:var(--muted);font-size:var(--nsub);font-style:italic;}"
    "#sw .ctxemu path{fill:none;stroke:var(--accent);stroke-width:1.8;"
    "stroke-dasharray:1 5;stroke-linecap:round;}"
    "#sw .ctxemu text{fill:var(--accent);font-size:var(--nsub);font-weight:700;}"
    "#sw .ctxemu-head{fill:var(--accent);}"
    "#sw .legend i.effect{background:none;height:0;border-top:3px solid var(--accent);}"
    "#sw .legend i.design{background:none;height:0;border-top:2px solid var(--muted);}"
    "#sw .legend i.emu{background:none;height:0;border-top:2px dotted var(--accent);}"
    "#sw .legend i.rigk{background:var(--surface);border:1.5px dashed var(--accent);}"
    "#sw .legend i.evo{background:var(--bg);border:1px solid var(--border);}"
    "#sw .legend i.evosys{background:var(--surface);border:2px solid var(--slot);}"
    ".mockbanner{border:2px dashed var(--accent);border-radius:10px;padding:.8rem 1rem;"
    "margin:1rem 0;background:var(--surface);}"
    ".ok{color:var(--text);font-weight:700;}.bad{color:var(--accent);font-weight:700;}"
    "main.mock{max-width:1180px;margin:0 auto;padding:1rem 16px 3rem;}"
    "</style>"
)


def need_text(needs, sn):
    raw = needs.get(sn, {}).get("need", "")
    raw = raw.split("**", 2)[-1] if raw.startswith("**Scope") else raw
    return cut(raw.replace("**", ""), 90)


def code(x):
    return "<code>{}</code>".format(esc(x))


def tables(mock, bundles, derived, needs):
    cited_by, needs_of, party_of_need, adopter, checks = derived
    ents = mock["entity"]
    das = mock.get("assumption", {})
    names = {e: r["name"] for e, r in ents.items()}
    bundle_rows = []
    for b in bundles:
        by_class = {}
        for i, c in b["classes"].items():
            by_class.setdefault(c, []).append(i)
        members = "<br>".join(
            "{}: {}".format(c, ", ".join(code(i) for i in by_class[c]))
            for c in ("bridged", "coincident", "unclassified")
            if c in by_class
        )
        bundle_rows.append(
            (
                code(b["id"]),
                "{}<br><span class='sub'>{}</span>".format(
                    esc(names.get(b["entity"], b["entity"])), esc(b["entity"])
                ),
                esc(b["frame"]),
                esc(b["direction"]),
                "<strong>{}</strong>".format(esc(b["kind"])),
                members or "<span class='sub'>none of its own</span>",
                ", ".join(code(d) for d in b["measured"]),
                ", ".join(code(d) for d in b["landing"]),
                esc(b["carries"]),
            )
        )
    da_rows = []
    for d, r in das.items():
        need_cells = "<br>".join(
            "<span title='{}'>{}</span> → {}".format(
                esc(need_text(needs, sn)),
                code(sn),
                esc(party_of_need.get(sn, "no stakeholder")),
            )
            for sn in sorted(needs_of.get(d, []))
        )
        da_rows.append(
            (
                code(d),
                ", ".join(code(s) for s in cited_by.get(d, [])),
                need_cells,
                ", ".join(code(i) for i in r["measured_at"]),
                ", ".join(code(b) for b in r["effect_at"]),
                code(r["realized_by"]) if r.get("realized_by") else "",
                esc(r["assumption"]),
                esc(r["holds_when"]),
                esc(r["obstacle"]),
                esc(r["falsifier"]),
                "{} / {}".format(esc(r["status"]), esc(r["standing"])),
            )
        )
    party_rows = [
        (
            code(e),
            esc(r["name"]),
            esc(r["class"]),
            esc(frame_of(r)),
            code(r["emulates"]) if r.get("emulates") else "",
            esc(r["description"]),
            esc(r["status"]),
        )
        for e, r in ents.items()
    ]
    rel_rows = [
        (
            code(rid),
            "{} → {}".format(esc(names[r["from"]]), esc(names[r["to"]])),
            esc(r["kind"]),
            esc(r["flow"]),
            esc(r["status"]),
        )
        for rid, r in mock.get("relationship", {}).items()
    ]
    waiver_rows = [
        (code(iid), esc(why)) for iid, why in mock.get("coincident", {}).items()
    ]
    retie_rows = [
        (
            code(iid),
            code(ch["to"]),
            esc(ch.get("new", "re-tied from its live bundle")),
        )
        for iid, ch in mock.get("retie", {}).items()
    ]
    open_rows = [(esc(o["name"]), esc(o["why"])) for o in mock.get("open", {}).values()]
    check_rows = [
        (
            esc(name),
            "<span class='ok'>✓</span>" if ok else "<span class='bad'>✗</span>",
            esc(detail),
        )
        for name, ok, detail in checks
    ]
    return (
        _ctx_table(
            "<h3>Bundles</h3>\n<p class='cap'>Authored identities (§5.7); "
            "membership <em>derived</em> from <code>interfaces.toml</code> "
            "tie-backs after the re-ties below. Each member IF is classified — "
            "<em>bridged</em> when a DA measures through it, <em>coincident</em> "
            "when it carries an explicit waiver, <em>unclassified</em> otherwise. "
            "A bundle is <em>effect</em> when some DA names it in "
            "<code>effect_at</code> (§4).</p>\n",
            (
                "Bundle",
                "Party",
                "Frame",
                "Dir",
                "Kind (derived)",
                "Interfaces, by class",
                "DAs measured here",
                "DAs landing here",
                "Carries",
            ),
            bundle_rows,
            "Bundle table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Assumptions</h3>\n<p class='cap'>DA rows (§6.2). The needs are "
            "<em>derived</em>: the live <code>sn_refs</code> of the SRs that cite "
            "the DA through their proposed <code>da_refs</code>, each resolved to "
            "its stakeholder's party. Maturity and validity are separate "
            "fields.</p>\n",
            (
                "DA",
                "Cited by",
                "Needs (derived) → party",
                "Measured at",
                "Effect at",
                "Rig",
                "Assumption",
                "Holds when",
                "Obstacle",
                "Falsifier",
                "Status / standing",
            ),
            da_rows,
            "Assumption table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Parties and outputs</h3>\n",
            ("Row", "Name", "Class", "Frame", "Emulates", "Description", "State"),
            party_rows,
            "Party table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>The link between the frames</h3>\n",
            ("Relationship", "Between", "Kind", "Flow", "State"),
            rel_rows,
            "Relationship table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Coincident waivers (proposed cells on boundary IFs)</h3>\n",
            ("Interface", "Why the reading is the outcome"),
            waiver_rows,
            "Waiver table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Interface re-ties the redraw implies</h3>\n",
            ("Interface", "Now ties to", "Note"),
            retie_rows,
            "Re-tie table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Open at the sitting</h3>\n",
            ("Party", "Why it is open"),
            open_rows,
            "Open-party table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Checks the mockup ran</h3>\n<p class='cap'>What a later "
            "generator would compute from the rows. {} interface rows still name "
            "the dropped adopter as a far side and need re-pointing by judgment "
            "(§5.7); the mockup leaves them where they are.</p>\n".format(len(adopter)),
            ("Check", "Result", "Detail"),
            check_rows,
            "Check table, horizontally scrollable",
        )
    )


def page(mock, ifs, srs, needs):
    bundles, *derived = derive(mock, ifs, srs)
    head = gen_trajectory.HTML_TEMPLATE.template
    css = head[head.index("<style>") : head.index("</style></head>") + len("</style>")]
    spent = ", ".join(code(i) for i in mock["spent"]["ids"])
    legend = (
        '<div class="legend">'
        '<span><i class="ctxkey sys"></i>system-of-interest (in operation)</span>'
        '<span><i class="ctxkey evosys"></i>delivery system (enabling)</span>'
        '<span><i class="ctxkey party"></i>operating party</span>'
        '<span><i class="ctxkey evo"></i>delivery-frame output</span>'
        '<span><i class="ctxkey rigk"></i>rig (emulates a party)</span>'
        '<span><i class="ctxkey effect"></i>effect bundle</span>'
        '<span><i class="ctxkey design"></i>design bundle</span>'
        '<span><i class="ctxkey unreal"></i>no IF of its own</span>'
        '<span><i class="ctxkey emu"></i>emulation edge</span>'
        '<span><i class="ctxkey rel"></i>Transition hand-off</span>'
        "</div>\n"
    )
    live = "live frame: 4 entities · 4 crossings · 3 relationships · 0 assumptions"
    ops = sum(1 for b in bundles if b["frame"] == "operating")
    proposed = (
        "{} rows (entities and outputs) · {} bundles ({} operating, {} delivery) · "
        "{} relationship · {} assumptions"
    ).format(
        len(mock["entity"]),
        len(bundles),
        ops,
        len(bundles) - ops,
        len(mock.get("relationship", {})),
        len(mock.get("assumption", {})),
    )
    return (
        "<!doctype html>\n<html lang='en'><head><meta charset='utf-8'>\n"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
        "<title>Depth-0 frame mockup</title>\n"
        + css
        + MOCK_STYLE
        + "</head><body><main class='mock'><div id='sw'>\n"
        "<h1>Depth-0 view — two-frame mockup</h1>\n"
        "<div class='mockbanner'><strong>MOCKUP, not the live frame.</strong> "
        "Rendered from <code>docs/plans/mockups/external.operating-frame.toml</code> "
        "by <code>render_depth0_mock.py</code>, joined with the live "
        "<code>interfaces.toml</code>, <code>system-requirements.toml</code> and "
        "<code>stakeholder-needs.toml</code>. It shows the How tab's System-context "
        "section as the assumption-tier plan "
        "(<code>docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md</code>, "
        "revised after review) would leave it. The LOCKED <code>external.toml</code> "
        "and the live dashboard are unchanged. Ids above the live watermark are "
        "proposed.</div>\n"
        "<h2>System context (the depth-0 view)</h2>\n"
        "<p class='cap'><strong>" + esc(proposed) + "</strong> (" + esc(live) + "). "
        "Two systems-of-interest in one view: the kit in operation above, and "
        "below it the delivery system that builds, verifies and releases it. The "
        "Transition hand-off is the only link. Every wire is a bundle: an "
        "authored identity whose interfaces are derived and classified. Spent ids, "
        "never re-minted: "
        + spent
        + ".</p>\n"
        + CTX_STYLE
        + SCROLL_CUE
        + "<div class='tablescroll' {}>".format(
            _hscroll("Depth-0 view mockup, horizontally scrollable")
        )
        + "<div class='context'>{}</div></div>\n".format(svg(mock, bundles))
        + legend
        + tables(mock, bundles, derived, needs)
        + "</div></main></body></html>\n"
    )


def main():
    mock, ifs, srs, needs = load()
    OUT.write_text(page(mock, ifs, srs, needs), encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
