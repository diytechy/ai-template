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
real generator would have to derive it: each bundle's frame from its `system`
cell and each party's frames from its bundles; bundle membership from IF
tie-backs; which assumptions land on each bundle; each assumption's needs from
the live `sn_refs` of the SRs citing it; whether each assumption lands on its
stakeholders' party (or a party that mediates for it); how every live SR is
classified; and, for the extension, each boundary IF's class.

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

G = {
    "gutter": 250.0,
    "entw": 224.0,
    "sysx": 720.0,
    "sysw": 236.0,
    "lane": 88.0,
    "top": 100.0,
    "width": 1000.0,
    "gap": 72.0,
    "cardpad": 29.0,
    "carrymax": 58,
    "namemax": 30,
}
HEADS = {"in": (False, True), "out": (True, False), "inout": (True, True)}
FRAMES = ("kit", "delivery")


def cut(text, budget):
    text = " ".join((text or "").split())
    return text if len(text) <= budget else text[: budget - 1] + "…"


def code(x):
    return "<code>{}</code>".format(esc(x))


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
    ents, bnds = mock["entity"], mock["boundary"]
    das, rigs = mock.get("assumption", {}), mock.get("rig", {})

    # Frames: a bundle's is its `system` cell; a party's is the set of its bundles'.
    frames_of = {e: set() for e in ents}
    for b in bnds.values():
        frames_of[b["entity"]].add(b["system"])

    # Extension: bundle membership from IF tie-backs, and each IF's class.
    ties = {}
    for iid, row in ifs.items():
        for col in ("interface_from_external", "interface_to_external"):
            if row.get(col):
                ties.setdefault(iid, set()).add(row[col])
    for iid, change in mock.get("retie", {}).items():
        ties[iid] = {change["to"]}
    measured_ifs = {i for row in das.values() for i in row.get("measured_at", [])}
    waived_ifs = mock.get("if_coincident", {})

    def if_class(iid):
        if iid in measured_ifs:
            return "bridged"
        return "coincident" if iid in waived_ifs else "unclassified"

    # Why: SR -> DA (proposed da_refs), SR -> SN (live), SN -> STK -> party.
    cited_by, needs_of = {}, {}
    for sr, refs in mock.get("sr_da_refs", {}).items():
        for d in refs:
            cited_by.setdefault(d, []).append(sr)
            needs_of.setdefault(d, set()).update(srs.get(sr, {}).get("sn_refs", []))
    stks = mock.get("stakeholder", {})
    need_stk = mock.get("need_stakeholder_refs", {})

    def parties_of_need(sn):
        return {stks[s]["party"] for s in need_stk.get(sn, []) if stks[s].get("party")}

    def reaches(bundle_id, parties):
        ent = bnds[bundle_id]["entity"]
        return ent in parties or ents[ent].get("mediates") in parties

    reach = {}
    for d, row in das.items():
        if row.get("realized_by"):
            target = rigs[row["realized_by"]]["emulates"]
            ok = all(bnds[b]["entity"] == target for b in row["effect_at"])
            reach[d] = (ok, "fidelity: lands on the emulated party " + target)
        else:
            bad = [
                sn
                for sn in sorted(needs_of.get(d, []))
                if not all(reaches(b, parties_of_need(sn)) for b in row["effect_at"])
            ]
            reach[d] = (
                not bad,
                "lands on its stakeholders' party"
                if not bad
                else "does not reach the stakeholder of " + ", ".join(bad),
            )

    bundles = []
    for bid, b in bnds.items():
        members = sorted(i for i, bs in ties.items() if bid in bs)
        bundles.append(
            dict(
                b,
                id=bid,
                ifs=members,
                classes={i: if_class(i) for i in members},
                landing=sorted(d for d, row in das.items() if bid in row["effect_at"]),
            )
        )

    # Every live SR: its classification, and its frame from its (re-pointed) bundles.
    repoint = mock.get("sr_repoint", {})
    frame_of_bundle = {bid: b["system"] for bid, b in bnds.items()}
    sr_class, sr_frames = {}, {}
    for sr, row in srs.items():
        if sr in mock.get("sr_da_refs", {}):
            sr_class[sr] = "cites assumptions"
        elif sr in mock.get("sr_coincident", {}):
            sr_class[sr] = "coincident"
        else:
            sr_class[sr] = "unclassified"
        cited = repoint.get(sr, row.get("boundary_refs", []))
        sr_frames[sr] = {frame_of_bundle[b] for b in cited if b in frame_of_bundle}
    multi = sorted(sr for sr, fs in sr_frames.items() if len(fs) > 1)

    counts = {}
    for c in sr_class.values():
        counts[c] = counts.get(c, 0) + 1
    fidelity = {row.get("realized_by") for row in das.values()}
    unclassified_ifs = sum(
        1 for b in bundles for c in b["classes"].values() if c == "unclassified"
    )
    checks = [
        (
            "Every assumption is cited by at least one SR",
            all(d in cited_by for d in das),
            "{} assumptions".format(len(das)),
        ),
        (
            "Every assumption names a falsifier",
            all(row.get("falsifier") for row in das.values()),
            "prose; evidence links live on TCs (assumption_refs)",
        ),
        (
            "Every rig has a fidelity assumption naming it",
            all(r in fidelity for r in rigs),
            ", ".join(rigs),
        ),
        (
            "Every assumption lands on its stakeholders' party, or a party mediating "
            "for it (fidelity: on the emulated party)",
            all(ok for ok, _ in reach.values()),
            "; ".join(
                "{}: {}".format(d, why) for d, (ok, why) in reach.items() if not ok
            )
            or "all {} assumptions".format(len(das)),
        ),
        (
            "Every need an assumption serves has a stakeholder",
            all(need_stk.get(sn) for ns in needs_of.values() for sn in ns),
            "via the proposed stakeholder_refs",
        ),
        (
            "Every SR cites assumptions or states it is coincident",
            counts.get("unclassified", 0) == 0,
            ", ".join("{} {}".format(v, k) for k, v in sorted(counts.items())),
        ),
        (
            "No SR spans both frames",
            not multi,
            ", ".join(multi) + " — to be split" if multi else "none",
        ),
        (
            "Extension: boundary IFs classified (bridged or coincident)",
            unclassified_ifs == 0,
            "{} unclassified — the allocation work at DevStg-Arch".format(
                unclassified_ifs
            ),
        ),
    ]
    return dict(
        bundles=bundles,
        frames_of=frames_of,
        cited_by=cited_by,
        needs_of=needs_of,
        need_stk=need_stk,
        reach=reach,
        sr_class=sr_class,
        multi=multi,
        checks=checks,
    )


def layout(mock, model):
    """Lanes top to bottom: the kit frame (its parties' bundles, then the parties
    still open), a gap, then the delivery frame (the Template's bundle, then the
    rigs, which cross nothing)."""
    by_party = {}
    for b in model["bundles"]:
        by_party.setdefault((b["entity"], b["system"]), []).append(b)
    rows, spans, bands, y = [], {}, [], G["top"]

    def place(key, lane_bundles):
        nonlocal y
        first = y
        for b in lane_bundles or [None]:
            rows.append((key, b, y))
            y += G["lane"]
        spans[key] = (first, y - G["lane"])

    for frame in FRAMES:
        start = y
        for e in mock["entity"]:
            if frame in model["frames_of"][e]:
                place(e, by_party.get((e, frame)))
        if frame == "kit":
            for key in mock.get("open", {}):
                place("open:" + key, None)
        else:
            for key in mock.get("rig", {}):
                place("rig:" + key, None)
        bands.append((frame, start, y - G["lane"]))
        y += G["gap"]
    return rows, spans, bands, y - G["gap"] + 30.0


def card(key, mock, y0, y1):
    x, w = G["gutter"], G["entw"]
    y, h = y0 - G["cardpad"], (y1 - y0) + 2 * G["cardpad"]
    cx, cy = x + w / 2, (y0 + y1) / 2
    if key.startswith("open:"):
        o = mock["open"][key[5:]]
        name, sub, kls = o["name"], "open at the sitting", "ctxent ghost"
        tip = o["name"] + " — open at the sitting: " + o["why"]
    elif key.startswith("rig:"):
        rid = key[4:]
        r = mock["rig"][rid]
        name, sub, kls = (
            r["name"],
            rid + " · rig · emulates " + r["emulates"],
            "ctxent rig",
        )
        tip = "{} — {} (rig, emulates {}): {}".format(
            rid, r["name"], r["emulates"], r["description"]
        )
    else:
        r = mock["entity"][key]
        kls = "ctxent" + (" evo" if r["class"] == "deliverable" else "")
        sub = key + " · " + r["class"]
        if r.get("mediates"):
            sub += " · mediates " + r["mediates"]
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
        esc(cut(sub, 42)),
    )


def if_summary(b):
    counts = {}
    for c in b["classes"].values():
        counts[c] = counts.get(c, 0) + 1
    return (
        "IFs: "
        + " · ".join(
            "{} {}".format(counts[k], k)
            for k in ("bridged", "coincident", "unclassified")
            if counts.get(k)
        )
        if counts
        else "no IF of its own"
    )


def wire(b, y):
    x1, x2 = G["gutter"] + G["entw"] + 6.0, G["sysx"] - 6.0
    start, end = HEADS.get(b["direction"], (False, False))
    kls = "ctxcross" + (" lands" if b["landing"] else "")
    kls += "" if b["ifs"] else " unrealized"
    lands = (
        "outcome of " + ", ".join(b["landing"])
        if b["landing"]
        else "no assumption lands here"
    )
    tip = "{} ({}, {} frame) — {} | {} | interfaces: {}".format(
        b["id"],
        b["direction"],
        b["system"],
        b["carries"],
        lands,
        ", ".join("{} ({})".format(i, c) for i, c in b["classes"].items())
        or "none of its own",
    )
    mx = (x1 + x2) / 2
    return (
        '<g class="{}" data-edge="{}"><title>{}</title>'
        '<path class="ctxwire" d="M{:.1f},{:.1f} L{:.1f},{:.1f}"{}/>'
        '<text class="ctxwlab" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text>'
        '<text class="ctxwsub" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text>'
        '<text class="ctxwda" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text>'
        '<text class="ctxwif" x="{:.1f}" y="{:.1f}" text-anchor="middle">{}</text></g>'
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
        esc("{} · {}".format(b["id"], b["direction"])),
        mx,
        y + 14.0,
        esc(cut(b["carries"], G["carrymax"])),
        mx,
        y + 28.0,
        esc(cut(lands, G["carrymax"] + 6)),
        mx,
        y + 41.0,
        esc(cut(if_summary(b) + "  (extension)", G["carrymax"] + 10)),
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


def svg(mock, model):
    rows, spans, bands, height = layout(mock, model)
    das = mock.get("assumption", {})
    labels = {
        "kit": "KIT FRAME — the kit, in operation (system-of-interest)",
        "delivery": "DELIVERY FRAME — this repository's build and release",
    }
    parts, systems = [], []
    for frame, y0, y1 in bands:
        parts.append(
            # The label sits just right of the gutter, above the band's first
            # card, so no gutter arc crosses it.
            '<g class="ctxplane"><rect x="12" y="{:.1f}" width="{:.1f}" '
            'height="{:.1f}" rx="10"/><text x="{:.1f}" y="{:.1f}">{}</text></g>'.format(
                y0 - 62.0,
                G["width"] - 24.0,
                (y1 - y0) + 100.0,
                G["gutter"] + 4.0,
                y0 - 42.0,
                labels[frame],
            )
        )
        lanes = [y for _k, b, y in rows if b and b["system"] == frame]
        if frame == "kit":
            systems.append(
                system_card(
                    min(lanes),
                    max(lanes),
                    "the kit",
                    "in operation",
                    "{} bundles · {} assumptions".format(len(lanes), len(das)),
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
    for j, (rid, r) in enumerate(mock.get("rig", {}).items()):
        arcs.append(
            arc(
                "ctxemu",
                spans["rig:" + rid],
                spans[r["emulates"]],
                n + j,
                "emulates",
                "{} emulates {}: {}".format(rid, r["emulates"], r["description"]),
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
    "#sw .ctxent.rig rect{fill:var(--bg);stroke:var(--accent);stroke-dasharray:2 3;"
    "stroke-width:1.6;}"
    "#sw .ctxent.ghost rect{fill:none;stroke-dasharray:6 4;filter:none;}"
    "#sw .ctxent.ghost .ctxname{fill:var(--muted);}"
    "#sw .ctxsys.evo rect{fill:var(--surface);stroke:var(--slot);stroke-width:2;}"
    "#sw .ctxsys.evo .ctxsysname,#sw .ctxsys.evo .ctxsyssub{fill:var(--text);}"
    "#sw .ctxcross.lands .ctxwire{stroke:var(--accent);stroke-width:2.6;}"
    "#sw .ctxcross.lands .ctxwlab{fill:var(--accent);}"
    "#sw .ctxwda{fill:var(--muted);font-size:var(--nsub);font-style:italic;}"
    "#sw .ctxwif{fill:var(--muted);font-size:var(--nsub);opacity:.75;}"
    "#sw .ctxemu path{fill:none;stroke:var(--accent);stroke-width:1.8;"
    "stroke-dasharray:1 5;stroke-linecap:round;}"
    "#sw .ctxemu text{fill:var(--accent);font-size:var(--nsub);font-weight:700;}"
    "#sw .ctxemu-head{fill:var(--accent);}"
    "#sw .legend i.lands{background:none;height:0;border-top:3px solid var(--accent);}"
    "#sw .legend i.plain{background:none;height:0;border-top:2px solid var(--muted);}"
    "#sw .legend i.emu{background:none;height:0;border-top:2px dotted var(--accent);}"
    "#sw .legend i.rigk{background:var(--bg);border:1.5px dashed var(--accent);}"
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


def tables(mock, model, needs):
    ents, das = mock["entity"], mock.get("assumption", {})
    stks = mock.get("stakeholder", {})
    names = {e: r["name"] for e, r in ents.items()}

    def mark(ok):
        return "<span class='ok'>✓</span>" if ok else "<span class='bad'>✗</span>"

    bundle_rows = []
    for b in model["bundles"]:
        by_class = {}
        for i, c in b["classes"].items():
            by_class.setdefault(c, []).append(i)
        bundle_rows.append(
            (
                code(b["id"]),
                "{}<br><span class='sub'>{}</span>".format(
                    esc(names.get(b["entity"], b["entity"])), esc(b["entity"])
                ),
                esc(b["system"]),
                esc(b["direction"]),
                ", ".join(code(d) for d in b["landing"])
                or "<span class='sub'>none — nothing asserted</span>",
                "<br>".join(
                    "{}: {}".format(c, ", ".join(code(i) for i in by_class[c]))
                    for c in ("bridged", "coincident", "unclassified")
                    if c in by_class
                )
                or "<span class='sub'>none of its own</span>",
                esc(b["carries"]),
            )
        )
    da_rows = []
    for d, r in das.items():
        need_cells = "<br>".join(
            "<span title='{}'>{}</span> → {}".format(
                esc(need_text(needs, sn)),
                code(sn),
                ", ".join(
                    "{} ({})".format(s, stks[s].get("party", "—"))
                    for s in model["need_stk"].get(sn, [])
                )
                or "no stakeholder",
            )
            for sn in sorted(model["needs_of"].get(d, []))
        )
        ok, why = model["reach"][d]
        da_rows.append(
            (
                code(d),
                ", ".join(code(s) for s in model["cited_by"].get(d, [])),
                need_cells,
                ", ".join(code(b) for b in r["effect_at"]),
                "{} {}".format(mark(ok), esc(why)),
                code(r["realized_by"]) if r.get("realized_by") else "",
                esc(r["assumption"]),
                esc(r["holds_when"]),
                esc(r["obstacle"]),
                esc(r["falsifier"]),
                "{} / {}".format(esc(r["status"]), esc(r["standing"])),
                ", ".join(code(i) for i in r.get("measured_at", [])),
            )
        )
    rig_rows = [
        (
            code(rid),
            esc(r["name"]),
            code(r["emulates"]),
            ", ".join(
                code(d) for d, row in das.items() if row.get("realized_by") == rid
            ),
            esc(r["description"]),
        )
        for rid, r in mock.get("rig", {}).items()
    ]
    party_rows = [
        (
            code(e),
            esc(r["name"]),
            esc(r["class"]),
            esc(", ".join(sorted(model["frames_of"][e]))),
            code(r["mediates"]) if r.get("mediates") else "",
            esc(r["description"]),
            esc(r["status"]),
        )
        for e, r in ents.items()
    ]
    stk_rows = [
        (
            code(s),
            esc(r["name"]),
            code(r["party"]) if r.get("party") else "",
            ", ".join(
                code(sn) for sn, refs in sorted(model["need_stk"].items()) if s in refs
            ),
        )
        for s, r in stks.items()
    ]
    sr_by_class = {}
    for sr, c in sorted(model["sr_class"].items()):
        sr_by_class.setdefault(c, []).append(sr)
    sr_rows = [
        (
            esc(c),
            str(len(srs)),
            ", ".join(code(s) for s in srs)
            if c != "unclassified"
            else "<span class='sub'>the remaining SRs — C2's work</span>",
        )
        for c, srs in sorted(sr_by_class.items())
    ]
    waiver_rows = [
        (code(sr), esc(why)) for sr, why in mock.get("sr_coincident", {}).items()
    ]
    rel_rows = [
        (
            code(rid),
            "{} → {}".format(esc(names[r["from"]]), esc(names[r["to"]])),
            esc(r["kind"]),
            esc(r["flow"]),
        )
        for rid, r in mock.get("relationship", {}).items()
    ]
    ext_rows = [
        (code(iid), code(ch["to"]), esc(ch.get("new", "re-tied from its live bundle")))
        for iid, ch in mock.get("retie", {}).items()
    ] + [
        (code(iid), "coincident", esc(why))
        for iid, why in mock.get("if_coincident", {}).items()
    ]
    open_rows = [(esc(o["name"]), esc(o["why"])) for o in mock.get("open", {}).values()]
    check_rows = [(esc(n), mark(ok), esc(det)) for n, ok, det in model["checks"]]
    return (
        _ctx_table(
            "<h3>Bundles</h3>\n<p class='cap'>Authored identities (§5.7), each "
            "declaring the system it crosses into. <em>No label is put on a "
            "bundle</em> (§4): the view shows which assumptions land there, and "
            "— for the extension — how its interfaces are classified.</p>\n",
            (
                "Bundle",
                "Party",
                "Frame",
                "Dir",
                "Assumptions landing here",
                "Interfaces by class (extension)",
                "Carries",
            ),
            bundle_rows,
            "Bundle table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Assumptions</h3>\n<p class='cap'>DA rows (§6.2). Needs are "
            "<em>derived</em> from the live <code>sn_refs</code> of the SRs that "
            "cite the assumption; each need resolves to its stakeholders and their "
            "party. The reach column checks <code>effect_at</code> against that "
            "party (or a party mediating for it).</p>\n",
            (
                "DA",
                "Cited by",
                "Needs → stakeholders (party)",
                "Effect at",
                "Reach",
                "Rig",
                "Assumption",
                "Holds when",
                "Obstacle",
                "Falsifier",
                "Status / standing",
                "Measured at (extension)",
            ),
            da_rows,
            "Assumption table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Rigs</h3>\n<p class='cap'>Rows in <code>assumptions.toml</code>, "
            "not frame parties: the frame's <code>enabling</code> class means a "
            "runtime dependency (§5.3).</p>\n",
            ("Rig", "Name", "Emulates", "Fidelity assumption", "Description"),
            rig_rows,
            "Rig table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>SRs, by how their argument is carried</h3>\n<p class='cap'>Over "
            "all live SRs. <em>Unclassified</em> is unknown, never coincidence "
            "(§4).</p>\n",
            ("Classification", "SRs", "Which"),
            sr_rows,
            "SR classification table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Coincident waivers on SRs</h3>\n",
            ("SR", "Why its S alone delivers its needs"),
            waiver_rows,
            "SR waiver table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Parties</h3>\n",
            ("Party", "Name", "Class", "Frames", "Mediates", "Description", "State"),
            party_rows,
            "Party table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Stakeholders</h3>\n<p class='cap'>The proposed list (Q12); each "
            "need cites its stakeholders (<code>stakeholder_refs</code>).</p>\n",
            ("Stakeholder", "Name", "Party", "Needs citing it"),
            stk_rows,
            "Stakeholder table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>The lifecycle hand-off between the frames</h3>\n<p class='cap'>"
            "Transition is the only lifecycle link; emulation edges and "
            "assumptions whose evidence and outcome sit in different frames also "
            "cross, and are drawn as what they are.</p>\n",
            ("Relationship", "Between", "Kind", "Flow"),
            rel_rows,
            "Relationship table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Extension: interface re-ties and coincident waivers</h3>\n",
            ("Interface", "Change", "Note"),
            ext_rows,
            "Extension table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Open at the sitting</h3>\n",
            ("Party", "Why it is open"),
            open_rows,
            "Open-party table, horizontally scrollable",
        )
        + _ctx_table(
            "<h3>Checks the mockup ran</h3>\n<p class='cap'>What a later "
            "generator would compute from the rows.</p>\n",
            ("Check", "Result", "Detail"),
            check_rows,
            "Check table, horizontally scrollable",
        )
    )


def page(mock, ifs, srs, needs):
    model = derive(mock, ifs, srs)
    head = gen_trajectory.HTML_TEMPLATE.template
    css = head[head.index("<style>") : head.index("</style></head>") + len("</style>")]
    spent = ", ".join(code(i) for i in mock["spent"]["ids"])
    legend = (
        '<div class="legend">'
        '<span><i class="ctxkey sys"></i>the kit, in operation</span>'
        '<span><i class="ctxkey evosys"></i>delivery system</span>'
        '<span><i class="ctxkey party"></i>party</span>'
        '<span><i class="ctxkey evo"></i>the Template</span>'
        '<span><i class="ctxkey rigk"></i>rig</span>'
        '<span><i class="ctxkey lands"></i>an assumption lands here</span>'
        '<span><i class="ctxkey plain"></i>nothing asserted</span>'
        '<span><i class="ctxkey unreal"></i>no IF of its own</span>'
        '<span><i class="ctxkey emu"></i>emulates</span>'
        '<span><i class="ctxkey rel"></i>Transition</span>'
        "</div>\n"
    )
    kit = sum(1 for b in model["bundles"] if b["system"] == "kit")
    proposed = (
        "{} parties · {} bundles ({} kit, {} delivery) · {} relationship · "
        "{} assumptions · {} rigs"
    ).format(
        len(mock["entity"]),
        len(model["bundles"]),
        kit,
        len(model["bundles"]) - kit,
        len(mock.get("relationship", {})),
        len(mock.get("assumption", {})),
        len(mock.get("rig", {})),
    )
    live = "live frame: 4 entities · 4 crossings · 3 relationships"
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
        "<code>stakeholder-needs.toml</code>. It shows the How tab's "
        "System-context section as the assumption-tier plan "
        "(<code>docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md</code>, "
        "after review round 2) would leave it. The LOCKED <code>external.toml</code> "
        "and the live dashboard are unchanged. Ids above the live watermark are "
        "proposed.</div>\n"
        "<h2>System context (the depth-0 view)</h2>\n"
        "<p class='cap'><strong>" + esc(proposed) + "</strong> (" + esc(live) + "). "
        "Two systems-of-interest in one view: the kit in operation above, and "
        "below it the delivery system that builds, verifies and releases it. Each "
        "bundle declares which system it crosses into. A highlighted wire is one "
        "where an assumption's outcome lands; the faint last line on each wire "
        "is the extension's interface classification. Spent ids, never "
        "re-minted: "
        + spent
        + ".</p>\n"
        + CTX_STYLE
        + SCROLL_CUE
        + "<div class='tablescroll' {}>".format(
            _hscroll("Depth-0 view mockup, horizontally scrollable")
        )
        + "<div class='context'>{}</div></div>\n".format(svg(mock, model))
        + legend
        + tables(mock, model, needs)
        + "</div></main></body></html>\n"
    )


def main():
    mock, ifs, srs, needs = load()
    OUT.write_text(page(mock, ifs, srs, needs), encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
