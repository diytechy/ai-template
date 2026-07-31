"""Pure graph layout and wire routing for the project-state dashboard.

The layered (Sugiyama-lite) rank/order/coordinate pipeline and the
obstacle-aware wire router every layered emitter calls. WI-280 split of
gen_trajectory.py; the facade re-exports, so consumers are unchanged.
"""


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


_FAN_PITCH = 8.0  # WI-366: the separation two strands of ONE port must reach
_PORT_LEAD = 11.0  # ...the run over which they reach it, before any routing bend
_LEAD_RUNGS = 3  # ...and how many staggered turn-off points that run offers


def _port_fan(groups, other_of, pos, row_h, row_gap):
    """Per-port vertical fan-out offsets (keyed by edge tuple) so several wires
    sharing one port spread across a small band instead of converging on the
    exact same pixel — the "knot" a plain center-to-center wire draws when 3+
    edges share a port. Offsets are ordered by the OTHER endpoint's row (so a
    wire to a higher block leaves/lands higher), which also keeps neighbouring
    wires from needlessly crossing each other right at the port. A single-edge
    port gets offset 0 (byte-identical to the former center-only routing).

    WI-366 (WI-323-CRITIQUE follow-up 1) sets the STEP to `_FAN_PITCH` — the
    separation the critic measured as the floor a reader needs to attribute one
    stroke to one edge — where it was a bare 6.0 that the render then damped to
    ~2.6 (the offset only moved a CONTROL point, and a cubic tracks a displaced
    control at ~4/9 of its offset). `_route_edges` now spends `_PORT_LEAD` px
    materializing the offset before any routing bend starts, so the step IS the
    rendered pitch.

    The cap is the ROW SLOT, not a fraction of the block: two vertically adjacent
    ports sit `row_h + row_gap` apart, so a band wider than that minus one pitch
    would fuse the outermost strand of one port with its neighbour's — trading a
    fused fan for a fused pair between fans. A port with more wires than the slot
    can hold at `_FAN_PITCH` (9 at the widest today, in a drilled-in layer) steps
    proportionally tighter rather than overflowing; that residue is real and
    stated, not hidden behind the average case."""
    offsets = {}
    for items in groups.values():
        n = len(items)
        if n <= 1:
            for e in items:
                offsets[e] = 0.0
            continue
        items_sorted = sorted(items, key=lambda e: (pos[other_of(e)][1], e))
        span = min(row_h + row_gap - _FAN_PITCH, (n - 1) * _FAN_PITCH)
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
_MAX_LANES = 48  # WI-257: candidate lanes tried per pass (bounds dense-overlap cost);
# WI-323 raised it from 24 because each band-edge lane now carries `_LANE_STACK`
# rungs behind it, so the cap has to cover the same reach in BASE lanes as before.
_LANE_SEP = 10.0  # two lanes closer than this in one corridor read as a single line
_CORRIDOR_MIN_OVERLAP = 40.0  # shorter shared runs read as a crossing, not a corridor
_LANE_STACK = 3  # outboard rungs offered behind each band-edge lane
# WI-323 dialled `_LANE_SEP` against the shipped dashboard, not from theory: at the
# 1.5px `--w-line` stroke, 6.0 cleared every clash at its OWN threshold yet still left
# 16 pairs inside 10px (visibly a doubled line); 10.0 with a 3-rung stack clears every
# pair at both, and the tightest surviving corridor is a 10-14px pair. Wider forces a
# lane out of the 22px inter-row channel and the wire jumps a whole band instead.


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
    lane when the nearest one still grazes a stub-corridor box.

    WI-323: each band-edge lane also carries a short STACK of rungs `_LANE_SEP` apart,
    stepping AWAY from y_pref (so away from the band that pushed the wire out) and
    inserted directly behind their parent. A wire whose corridor is free still takes
    the head, so its `d` is byte-identical; a wire the corridor ledger pushes off
    takes the neighbouring rung rather than jumping to a distant band edge."""
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

    def free(c):
        return lo <= c <= hi and not any(t <= c <= b for t, b in merged)

    out, seen = [], set()
    for c in sorted((c for c in cands if free(c)), key=lambda c: abs(c - y_pref)):
        step = _LANE_SEP if c >= y_pref else -_LANE_SEP
        for r in [c + k * step for k in range(_LANE_STACK + 1)]:
            if round(r, 3) not in seen and free(r):
                seen.add(round(r, 3))
                out.append(r)
    return out


def _lane_seg(d):
    """The (x_lo, x_hi, y) of a routed path's straight lane hop, or None for a direct
    cubic. The lane is the only straight run `_detour_str` emits ("... xa,lane L
    xb,lane ..."), so `" L"` identifies it without re-parsing the curves."""
    if " L" not in d:
        return None
    before, after = d.split(" L", 1)
    ax, ay = before.rsplit(" ", 1)[1].split(",")
    bx = after.split(" ", 1)[0].split(",")[0]
    return min(float(ax), float(bx)), max(float(ax), float(bx)), float(ay)


def _corridor_clash(xlo, xhi, lane, taken):
    """True when this lane would ride within `_LANE_SEP` of an already-placed lane
    over a shared run longer than `_CORRIDOR_MIN_OVERLAP` — the pair then reads as ONE
    line for that stretch and a reader cannot attribute it to one source and one
    target (121-CRITIQUE MAJOR, second clause). A shorter shared run is a crossing in
    open space, which T8 permits, so it is not a clash."""
    for txlo, txhi, ty in taken:
        if abs(ty - lane) < _LANE_SEP:
            if min(xhi, txhi) - max(xlo, txlo) > _CORRIDOR_MIN_OVERLAP:
                return True
    return False


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


def _harness_seg(xa, ya, xb, yb, mx):
    """One HARNESS segment (WI-366): a cubic from (xa,ya) to (xb,yb) with BOTH controls
    at x = mx, so the whole y change happens around mx and the rest of the run is flat
    — the port-side bend idiom `_detour_str` already draws, with the bend x named
    separately from the segment's end so a strand can turn off EARLY and then coast.
    Leaves and arrives horizontally, so it joins the port ring and hands off to the
    routed remainder without a kink."""
    return "C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}".format(mx, ya, mx, yb, xb, yb)


def _lead_rung(k, n, down):
    """How many `_FAN_PITCH` rungs strand `k` of an `n`-wire port coasts before it
    turns off its harness (WI-366). Neighbouring strands sit on DIFFERENT rungs, so a
    pair that both plunge steeply out of the port begins its plunge `_FAN_PITCH` px
    apart in X — which is what a steep pair needs, because a VERTICAL offset collapses
    to `off * cos(angle)` on a near-vertical stroke (the 8 px the harness opens at the
    port reads as ~4.7 px down the descent, and read as the ~2.5 px the critic
    measured before it).

    `k` indexes the strands by fan height (0 = topmost) and `down` says whether this
    one's target lies below its port. The strand travelling FURTHEST in its direction
    turns off FIRST, so it dives past the others while they are still coasting flat —
    turn off in the other order and the early diver crosses every strand it is still
    inboard of, trading a fused pair for a knot of crossings at the port.

    Rungs are capped at `_LEAD_RUNGS` so the harness stays well inside the column
    channel however many wires share the port. On a port with more than `_LEAD_RUNGS`
    wires the cap collapses the LEAST-travelled end of the fan onto one turn-off, and
    that is the right end to give up: a strand whose target is nearly level leaves at a
    shallow angle, where the fan offset already reads as the full pitch and no x
    stagger is owed. The residue is the pair whose targets are both near-level and
    both far enough to plunge — measured on the shipped views, raising the cap past 3
    moved one pair of 271, so the bound stays."""
    return min((n - 1 - k) if down else k, _LEAD_RUNGS - 1)


def _port_strands(edges):
    """Where each wire sits in the fan at each of its two ports (WI-366), read off the
    `_route_edges` edge list rather than threaded through by every caller: `_port_fan`
    groups by node id, and every edge out of one node leaves that node's single output
    port (every edge into it enters its single input port), so the same grouping is
    recoverable here. Returns `(source, target)` dicts mapping an edge key to its
    (index by fan height, wires on that port). Sorted, so it is deterministic."""
    at_port = ({}, {})
    for e in edges:
        at_port[0].setdefault(e[5], []).append(e)
        at_port[1].setdefault(e[6], []).append(e)
    strand = ({}, {})
    for end, ykey in ((0, 2), (1, 4)):  # e[2] is the source fan y, e[4] the target's
        for es in at_port[end].values():
            for i, e in enumerate(sorted(es, key=lambda e: (e[ykey], e[0]))):
                strand[end][e[0]] = (i, len(es))
    return strand


def _harness_ends(strand, key, sy, y1, ty, y2):
    """`(lead, tail)` — how many px each end of this wire spends holding its own fan
    height before/after the routed remainder (WI-366). 0 at a port this wire has to
    itself, which is what keeps every unfanned wire byte-identical. Both ends stagger
    their turn-off by fan rung, mirrored: on departure the strand travelling furthest
    turns off SOONEST, on arrival it joins the flat run LATEST, so in both cases it
    clears the strands it would otherwise cross."""
    lead = tail = 0.0
    ko, no = strand[0][key]
    ki, ni = strand[1][key]
    if no > 1:
        lead = _PORT_LEAD + _lead_rung(ko, no, y2 >= sy) * _FAN_PITCH
    if ni > 1:
        tail = _PORT_LEAD + _lead_rung(ki, ni, y1 >= ty) * _FAN_PITCH
    return lead, tail


def _routed_dx(span, min_dx, harnessed, routed):
    """The horizontal control offset of a wire's direct cubic. `span` is the legacy
    measure (target box left edge minus the wire's start), so an UNHARNESSED wire gets
    the legacy value byte-for-byte. A harnessed wire's bow is additionally kept inside
    the `routed` width the harness left it — a two-ended harness on a
    single-column hop can leave less room than `min_dx`, and a control past the far
    endpoint draws a visible backward loop (WI-366)."""
    dx = max(span * 0.4, min_dx)
    if harnessed and routed > 0:
        return min(dx, routed / 2.0)
    return dx


def _spliced_harness(d, lead, tail, src_ends, tgt_ends):
    """`d` — a path routed between the STRAND ends of the harness — with the harness
    bends spliced back on, so the wire still terminates on both port centers (WI-366).
    `src_ends` is (port x, port cy, strand x, strand y) at the source, `tgt_ends` the
    mirror at the target. An unharnessed end is left exactly as routed."""
    if lead:  # replaces the routed sub-path's own `M`, keeping one continuous path
        x1, sy, xs, y1 = src_ends
        d = "M{:.1f},{:.1f} {} {}".format(
            x1, sy, _harness_seg(x1, sy, xs, y1, x1 + _PORT_LEAD / 2.0),
            d.split(" ", 1)[1],
        )  # fmt: skip
    if tail:
        xt, y2, xe, ty = tgt_ends
        d = "{} {}".format(d, _harness_seg(xt, y2, xe, ty, xe - _PORT_LEAD / 2.0))
    return d


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
    x1, sy, y1, xe, ty, y2, obstacles, clearance=_WIRE_CLEAR, stub=_WIRE_STUB, taken=()
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
    no-clear-lane fallback.

    WI-323: `taken` is the caller's corridor ledger — the (x_lo, x_hi, y) lane hops
    already placed in this diagram. Preference order is clear-of-every-box AND
    corridor-free, then clear-but-coincident, then the least-bad fallback. The middle
    tier is exactly what this function returned before the ledger existed, so the
    ledger can only move a wire from one FULLY CLEAR lane to another: the T8
    through-box floor (LLR-120/TC-125) cannot regress through this parameter."""
    xa, xb = x1 + stub, xe - stub
    fox, fxh = min(x1, xe, xa, xb), max(x1, xe, xa, xb)
    full = [r for r in obstacles if r[0] < fxh and r[0] + r[2] > fox]
    if not full:
        return None
    lox, hix = min(xa, xb), max(xa, xb)
    lane_span = [r for r in full if r[0] < hix and r[0] + r[2] > lox]
    y_pref = (y1 + y2) / 2.0
    best = None  # (hit_count, d): the least-bad deterministic fallback
    shared = None  # first box-clear lane that still rides an occupied corridor
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
            if not _polyline_hits(pts, full):
                d = _detour_str(x1, sy, y1, xa, xb, xe, ty, y2, lane)
                if not _corridor_clash(min(xa, xb), max(xa, xb), lane, taken):
                    return d  # early-exit: first box-clear, corridor-free lane wins
                shared = shared or d
                continue  # a clear lane cannot improve on `best`; keep looking
            hits = sum(1 for r in full if _polyline_hits(pts, (r,)))
            if best is None or hits < best[0]:
                best = (hits, _detour_str(x1, sy, y1, xa, xb, xe, ty, y2, lane))
        if lane_span == full:
            break  # the second pass would re-scan the identical obstacle set
    return shared or (best[1] if best else None)


def _routed_label_xy(d, fx, fy):
    """Where an edge label should sit so it rides its wire. A DETOURED path carries
    a straight lane segment ("... xa,lane L xb,lane ..."); anchor to that lane's
    midpoint (WI-255 — the label formerly stuck to the straight-chord midpoint and
    floated off a re-routed wire). A clear (direct-cubic) path has no 'L' and keeps
    the caller's straight-chord fallback (fx, fy), so its label is byte-identical."""
    seg = _lane_seg(d)
    if seg is None:
        return fx, fy
    return (seg[0] + seg[1]) / 2.0, seg[2]


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
    escapes.

    WI-366 (WI-323-CRITIQUE follow-up 1): a port with 2+ wires gets a HARNESS. The
    fan offset used to live only in the first/last CONTROL point, so every strand of
    a port left the same pixel on a slightly different heading and the routing bend
    — whose own control sits ~9 px out — then dominated: where a strand's fan rank
    and its assigned lane disagreed (which WI-323's corridor ledger made common,
    because a lane is now claimed by edge order, not by the other endpoint's row) the
    two strands crossed back over each other AT the port and ran fused for tens of px
    — 2.5–3 CSS px pitch over a ~55 px descent, and 0.07 px at the tightest site.

    Each strand now RISES from the port center to its own `_FAN_PITCH`-spaced height
    over `_PORT_LEAD` px, coasts flat to its own staggered turn-off (`_lead_rung`),
    and only the REMAINDER of the span is routed. The rise reaches the pitch before
    any lane can pull, whatever lane that is, and the stagger gives a pair that both
    plunge steeply a HORIZONTAL gap as well — the narrow "stagger the departures" form
    the critic asked for, not a two-phase route-then-refan pass. Measured on the
    shipped roadmap (SVG user units = CSS px there): the tightest pair right of block
    1's port went 0.07 → 8.0 px at 15 px from the port, and the three pairs right of
    `unphased`'s port that never reached 8 px at all now do, by 17–20 px.

    A SINGLE-wire port is untouched (no harness, terminal on the port center), so
    every unfanned wire — the majority — stays byte-identical. The harness bend is
    not itself hit-tested: it lives in the `col_gap` channel immediately outside its
    own block, where by construction no box sits (the widest harness, `_PORT_LEAD` +
    (`_LEAD_RUNGS` - 1) * `_FAN_PITCH` = 27 px, is under half the narrowest channel),
    and the T8 sweep (`test_t8_no_wire_passes_through_an_unrelated_node_box`) samples
    the FULL emitted `d` against every box, so a harness that ever cut one fails
    there."""
    ordered = sorted(rects_by_id.items())
    out = {}
    strand = _port_strands(edges)
    # WI-323 (121-CRITIQUE MAJOR, second clause): the SHARED-CORRIDOR LEDGER. Each
    # wire was routed in isolation, so every long-haul wire pushed out of the same
    # node band picked the same nearest clear lane and several ran coincident for
    # hundreds of px. Lanes are now claimed as they are placed, and a later wire in
    # the same horizontal corridor takes the next stacked lane instead. The ledger is
    # per-call (one diagram, one coordinate system) and filled in the sorted edge
    # order above, so which wire wins the innermost lane is deterministic.
    taken = []
    for key, x1, y1, x2, y2, src, tgt in sorted(edges, key=lambda e: e[0]):
        xe = x2 - end_trim
        rs, rt = rects_by_id.get(src), rects_by_id.get(tgt)
        sy = rs[1] + rs[3] / 2 if rs else y1  # source port center (terminal)
        ty = rt[1] + rt[3] / 2 if rt else y2  # target port center (terminal)
        # The harness (WI-366) consumes the first/last stretch; what is left is routed,
        # and the strand — not the port center — is its terminal there.
        lead, tail = _harness_ends(strand, key, sy, y1, ty, y2)
        xs, xt = x1 + lead, xe - tail
        sy_r, ty_r = (y1 if lead else sy), (y2 if tail else ty)
        dx = _routed_dx(x2 - tail - xs, min_dx, lead or tail, xt - xs)
        obstacles = [v for k, v in ordered if k != src and k != tgt]
        infl = [
            (r[0] - _WIRE_HIT_MARGIN, r[1] - _WIRE_HIT_MARGIN,
             r[2] + 2 * _WIRE_HIT_MARGIN, r[3] + 2 * _WIRE_HIT_MARGIN)
            for r in obstacles
        ]  # fmt: skip
        direct = _cubic_points((xs, sy_r), (xs + dx, y1), (xt - dx, y2), (xt, ty_r))
        backward = xt <= xs
        d = None
        if _polyline_hits(direct, infl) or backward:
            span = list(obstacles)
            if backward:  # route the lane around its own endpoint boxes too
                if rs:
                    span.append((rs[0], rs[1], rs[2] - 0.1, rs[3]))  # trim port edge
                if rt:
                    span.append(rt)
            d = _detour_d(xs, sy_r, y1, xt, ty_r, y2, span, taken=taken)
        if d is None:
            d = "M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}".format(
                xs, sy_r, xs + dx, y1, xt - dx, y2, xt, ty_r
            )
        d = _spliced_harness(d, lead, tail, (x1, sy, xs, y1), (xt, y2, xe, ty))
        seg = _lane_seg(d)
        if seg is not None:
            taken.append(seg)
        out[key] = d
    return out
