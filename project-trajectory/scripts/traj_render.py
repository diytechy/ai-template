"""SVG/HTML rendering primitives for the project-state dashboard.

The escape/tab/scroll helpers, the declared colour/weight vocabularies
(TIER/STATUS/SW/OKF/PHASE + ring inks), the responsive svg wrappers, and
the shared Simulink-style drill renderer. WI-280 split of gen_trajectory.py;
the facade re-exports, so consumers are unchanged."""

import html
import math
import re

from traj_graph import GraphGeom, _layered_layout, orthogonal_route, route_graph


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


# WI-292 (U5 de-collision, 119-CRITIQUE): `tc` was `#047857`, byte-identical to
# STATUS_FILL["done"] — two different concepts (a TC/Test-Case tier vs a done
# status) reading as one colour wherever both appear (the icicle TC lane sits one
# tab from the status legend). `#0f766e` clears the same >=4.5:1 white-text floor
# and stays paired with OKF_TYPE_FILL["Test Case"] below (that mirror IS
# intentional — one concept, two label systems).
TIER_FILL = {"sn": "#4338ca", "sr": "#0e7490", "llr": "#64748b", "tc": "#0f766e"}
TIER_COL = {"sn": 0, "sr": 1, "llr": 2, "tc": 3}


# A focusable descendant, for `_svg_role`. Two shapes, because focusability is NOT
# only `tabindex`: an SVG `<a>` with an href is in the sequential tab order natively
# and therefore carries none. A `tabindex`-only predicate reported the loops diagram
# (9 linked stage cards) as a non-interactive graphic and left it `role="img"` — the
# exact defect WI-297 set out to close. Matching raw `<` is safe: `esc()` renders
# registry prose as `&lt;a href`, so document text cannot forge a hit.
_FOCUSABLE = re.compile(r"tabindex\s*=|<a\s[^>]*href\s*=", re.I)


# WI-307 (T7 + T4, 119-CRITIQUE + the WI-305 train critique): every emitted SVG
# used to carry a FIXED pixel `width`, so a diagram wider than the viewport could
# only be reached by horizontal scrolling — at 390px all four views demanded
# "Scroll sideways to see the full view" and cut off right-side lanes, and the
# How graph clipped `CMP-002 — Generators` mid-label (the T4 half of the same
# defect). A `viewBox` alone does not fix it: the fixed width pins the rendered
# size, so the box never scales.
#
# The fix is scale-to-fit WITH A LEGIBILITY FLOOR, not unbounded scaling. Pure
# scale-to-fit trades T7 for T4 — squeezing a 900px graph into 390px shrinks a
# 12px label to ~5px, which is the "readable at default zoom" floor T4 forbids.
# So the SVG scales down only to SHRINK_FLOOR of its natural width; past that it
# stops shrinking and the container's existing scroll + `.scrollcue` affordance
# takes over. That is the row's own rule — "keep the sideways-scroll hint only as
# a fallback for content that genuinely cannot fit" — made mechanical, and it is
# stated as residue rather than hidden: a view whose natural width exceeds
# 390 / SHRINK_FLOOR still scrolls, with the cue.
SHRINK_FLOOR = 0.62  # smallest fraction of natural width before scrolling resumes


def _svg_fit_style(width):
    """The responsive sizing for an emitted diagram: fill the container, keep the
    viewBox aspect, and never shrink past the label-legibility floor."""
    return "width:100%;max-width:{:.0f}px;min-width:{:.0f}px;height:auto".format(
        width, width * SHRINK_FLOOR
    )


# WI-367 (WI-323-CRITIQUE follow-up 2): every emitted diagram declared
# `viewBox="0 0 width height"` — the LAYOUT box, `pad` px of margin around the node
# grid — while the wire router deliberately sends a WRAP-AROUND (backward) edge
# around the OUTSIDE of its own endpoint boxes: `_detour_d` turns its lane at
# `x1 + _WIRE_STUB` / `xe - _WIRE_STUB`, a harness lead further out again (WI-257
# MINOR 1 already recorded that outboard reach; WI-366 widened it). At rank 0, and
# at the last rank, that turn lands OUTSIDE the layout box and the SVG viewport
# clips it: the lane stops flat at the box edge and its continuation re-enters a
# few px away — "a long horizontal line that stops at nothing, and a curve that
# starts from nothing" (the critique, which could not tell a clip from a routing
# margin from pixels alone). It is the CLIP. Measured on the shipped dashboard,
# in SVG user units: the roadmap root layer's wires reach x=-17.5 and x=711.0
# against a 0..692 box; the How-SW root layer reaches x=923.0 against 0..904.
#
# So the box is grown to the ink on all four sides, not the ink shrunk to the box:
# WI-435 found the same omission vertically (`CMP-004 → CMP-002` at y=-9.1 while
# the viewBox began at 0). Pulling the U-turn
# back inside would push it through its own endpoint box, the exact defect WI-257
# removed. The pad is measured from the BODY — like `_svg_role` above — so no
# emitter has to remember it, a successor emitter cannot forget it, and a diagram
# with no outboard ink (every layer but four of the shipped dashboard) keeps a
# byte-identical tag.
_INK_PAD = 2.0  # ink, not centerline: clears `--w-emph` 2.5's 1.25 half-width

# One token of a path `d`: a command letter or a number. What the emitters actually
# write into a framed diagram is absolute `M`/`L`/`C` (the wires) and one relative
# `h` (the containment arrow); `Q` is read too because the loops diagram writes it,
# and it would otherwise be the first thing a successor moved under this wrapper.
_PATH_TOKEN = re.compile(r"[A-Za-z]|-?\d+(?:\.\d+)?")


def _path_axis(d, axis):
    """Every x or y coordinate a path visits, including cubic control points. A
    Bézier lies inside its control hull, so min/max over these bound the ink without
    sampling the curve — and on the shipped dashboard the bound is exact, because
    every outboard extreme is a lane's own `L` endpoint. An unrecognised command
    stops the scan rather than consuming its arguments as coordinates: a shape this
    helper has never seen can then only be under-padded, never mis-placed."""
    toks = _PATH_TOKEN.findall(d)
    values, cx, cy, cmd, i = [], 0.0, 0.0, "", 0
    while i < len(toks):
        if toks[i].isalpha():
            cmd, i = toks[i], i + 1
            continue
        if cmd in ("M", "L", "C", "Q"):  # absolute, x,y pairs
            if i + 1 >= len(toks):
                break  # a truncated pair: under-pad, never read past the end
            cx, cy, i = float(toks[i]), float(toks[i + 1]), i + 2
        elif cmd == "h":  # relative horizontal
            cx, i = cx + float(toks[i]), i + 1
        elif cmd == "v":  # relative vertical
            cy, i = cy + float(toks[i]), i + 1
        else:
            break
        values.append((cx, cy)[axis])
    return values


def _path_xs(d):
    return _path_axis(d, 0)


def _path_ys(d):
    return _path_axis(d, 1)


def _ink_overflow(width, height, body):
    """Whole units of wire ink outside the layout box: left/right/top/bottom."""
    ds = re.findall(r'\sd="([^"]+)"', re.sub(r"<defs>.*?</defs>", "", body, flags=re.S))
    xs = [x for d in ds for x in _path_xs(d)]
    ys = [y for d in ds for y in _path_ys(d)]
    if not xs or not ys:
        return 0, 0, 0, 0
    # Whole units, and INTS: a float pad would negate to `-0.0` and render every
    # unpadded diagram's viewBox as `-0 0 …`, churning the whole dashboard.
    return (
        max(0, math.ceil(_INK_PAD - min(xs))),
        max(0, math.ceil(max(xs) + _INK_PAD - width)),
        max(0, math.ceil(_INK_PAD - min(ys))),
        max(0, math.ceil(max(ys) + _INK_PAD - height)),
    )


def _svg_frame(width, height, body):
    """The `viewBox` / `width` / `style` attribute triple every emitted diagram
    opens with, its box grown on every side to whatever wire ink the router put
    outside the layout box (WI-367). The declared natural width grows with it, so a
    diagram that already fits its card renders at exactly its former scale and only
    the clipped stubs appear; one that was already scaled to fit shrinks by the pad
    fraction (measured: the How-SW root layer 0.800 -> 0.782 CSS px per unit at
    1680px, its 12px labels 9.60 -> 9.38px, far above the `SHRINK_FLOOR` floor)."""
    left, right, top, bottom = _ink_overflow(width, height, body)
    box_w, box_h = width + left + right, height + top + bottom
    return 'viewBox="{:d} {:d} {:.0f} {:.0f}" width="{:.0f}" style="{}"'.format(
        -left, -top, box_w, box_h, box_w, _svg_fit_style(box_w)
    )


def _svg_wrap(width, height, body):
    """The `<svg>` wrapper shared by the graph emitters (dag / sw / know), which
    differ only in their content. Folding `_svg_role` in makes the WI-297
    invariant STRUCTURAL, not a rule each emitter must remember: a call site
    cannot emit a container without the content-driven role, because it never
    writes the tag. The per-site `role=` interpolation this replaced is the shape
    that let a children-presentational role sit over focusable nodes. `_svg_frame`
    (WI-367) is folded in for the same reason."""
    return '<svg {} preserveAspectRatio="xMinYMin meet" role="{}">{}</svg>'.format(
        _svg_frame(width, height, body), _svg_role(body), body
    )


def _svg_role(body):
    """The ARIA role for an emitted `<svg>`, chosen from its CONTENT: `group` when
    the body holds any focusable descendant, else `img` (which then owes a name).

    `role="img"` is children-presentational, so declaring it over an interactive
    graph prunes the very `<title>`s the A2 anchor rests on. Deciding from the body
    rather than per call site keeps a future emitter from reintroducing that
    silently. Full rationale + the measured before/after: LLR-101 / TC-104 (WI-297)."""
    return "group" if _FOCUSABLE.search(body) else "img"


# SVG corner radii (U3 core, WI-310). The `rx` PRESENTATION ATTRIBUTE cannot read
# a CSS custom property portably, so this scale is declared here in Python rather
# than beside the `--r-*` tokens in the stylesheet — same rule, different
# mechanism. Before WI-310 the emitters used 3/6/7/8/9/12, of which FOUR (6, 7,
# 8, 9) were doing the single job "round a node box": exactly the drift U3 exists
# to catch.
#
# These are the DECLARATION, not the substitution. The `rx="…"` values stay
# literals in the rect templates, because those templates are implicitly
# concatenated multi-line strings ending in `.format(...)`, and splicing a
# constant in with `+` rebinds `.format` to the last fragment alone — a real bug
# this WI hit and backed out. `test_u3_svg_corner_radii_match_the_declared_scale`
# closes the loop instead, asserting BOTH the emitted set and the source literals
# against this tuple, so a seventh radius cannot appear un-declared.
SVG_RX = ("3", "8", "12")  # icicle cell · any node box · process chip


# WI-267: `cancelled` is a TERMINAL WON'T-BUILD status with its OWN dashboard
# bucket (spelled `retired` until WI-384) — a muted stone hue byte-distinct from
# every other fill (done/active/queued and the drill tiers), never folded into
# done's green, so a dead-end row reads as visibly terminal, not merely parked.
STATUS_FILL = {
    "done": "#047857",
    "active": "#b45309",
    "queued": "#94a3b8",
    "cancelled": "#78716c",
}

# WI-272 (review M-2): the registry's SEVEN statuses map onto FOUR fills, and this
# table is that mapping made EXPLICIT. It used to be an inline `if not in
# STATUS_FILL: "queued"` clamp, which did not merely share a swatch — it rewrote
# the status itself, so a `deferred` row's tooltip, accessible name, and detail
# JSON all *said* "queued". Parked-by-choice and impeded-by-something are not
# ordinary queue work, and the dashboard is this repo's advertised state surface,
# so mislabelling them mis-prioritizes real work.
#
# The fix keeps ONE colour per concept rather than minting two more hues: the
# shared swatch means "not started", the three sub-states are told apart by their
# own GLYPH and by the true status word carried in every text surface, and the
# legend names the grouping instead of pretending it isn't there. Minting hues
# would also have made the live U5 near-duplicate residue worse (LLR-102) — the
# palette is already dense.
STATUS_BUCKET = {
    "done": "done",
    "active": "active",
    "queued": "queued",
    "draft": "queued",
    "deferred": "queued",
    "blocked": "queued",
    "cancelled": "cancelled",
    # SR-144's third terminal shares the `cancelled` SWATCH — both are "this
    # row will not advance" — but keeps its own glyph below, because what they
    # mean differs: cancelled is "never", partial is "not all of it, and a
    # successor may carry the rest".
    "partial": "cancelled",
}
# The one label the shared swatch may carry: naming the bucket is what stops it
# reading as "queued" (review M-2's "name it explicitly").
STATUS_BUCKET_LABEL = {"queued": "not started", "done": "done", "active": "active"}
# A3 (no-info-by-color-alone): a redundant, shape-distinct glyph per STATUS — one
# per *status*, not per fill, so the four statuses sharing the "not started"
# swatch stay distinguishable without colour perception at all. ○ open / ✎ being
# written / ◌ parked (a dotted, un-drawn ring) / ⊘ barred / ⊗ struck-out terminal.
STATUS_GLYPH = {
    "done": "✓",
    "active": "●",
    "queued": "○",
    "draft": "✎",
    "deferred": "◌",
    "blocked": "⊘",
    "cancelled": "⊗",
    "partial": "◐",
}


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


def tab_button(tab, label):
    """One dynamically-added dashboard tab as a WAI-ARIA `role="tab"` button
    (WI-273, SR-052). Every generated extra starts *unselected*: the first tab
    (`arch`) is the initial selection and is hardwired in the template, so an
    extra carries `aria-selected="false"` and drops out of the roving tab
    sequence (`tabindex="-1"`) until chosen. `aria-controls` names the panel it
    reveals; that panel's `aria-labelledby` points back at this button's
    `id="tab-<tab>"`. The tab controller flips these on selection."""
    return (
        '<button role="tab" id="tab-{t}" data-tab="{t}" aria-controls="{t}"'
        ' aria-selected="false" tabindex="-1">{label}</button>'
    ).format(t=tab, label=label)


def tab_panel_open(pid):
    """Opening `<section>` tag for a dynamically-added tab panel (WI-273,
    SR-052): a `role="tabpanel"` labelled by its controlling tab and `hidden`
    until selected. The tab controller clears `hidden` together with the
    `.active` display class so assistive tech and the visual layer agree."""
    return (
        '<section id="{p}" class="panel" role="tabpanel"'
        ' aria-labelledby="tab-{p}" hidden>'
    ).format(p=pid)


def _arrow_markers(*specs):
    """`<defs>` wrapping one `<marker>` per spec: `(marker_id, css_class)`,
    `(marker_id, css_class, size)` to override the default `ARROW_SIZE` (the
    `cedgearrow` containment marker renders a touch smaller), or
    `(marker_id, css_class, size, ring)` to stamp the marker itself with a
    `--ring` value.

    That last form exists because marker content is rendered from the `<defs>`
    tree, not from the element referencing it: a custom property set on the
    referencing node does NOT reach inside the marker, so a head that must match
    its host node's contrast-safe ink has to carry its own `--ring` (WI-317)."""
    markers = "".join(
        '<marker id="{}" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="{sz}" markerHeight="{sz}" markerUnits="userSpaceOnUse" '
        'orient="auto-start-reverse"{ring}><path d="M0,0 L10,5 L0,10 z" '
        'class="{}"></path></marker>'.format(
            esc(spec[0]),
            esc(spec[1]),
            sz=spec[2] if len(spec) > 2 else ARROW_SIZE,
            ring=' style="--ring:{}"'.format(spec[3]) if len(spec) > 3 else "",
        )
        for spec in specs
    )
    return "<defs>{}</defs>".format(markers)


# WI-292 (U5 de-collision, 119-CRITIQUE): all three used to reuse another
# vocabulary's hex for an unrelated concept — module `#0e7490` = TIER_FILL["sr"]/
# OKF_TYPE_FILL["System Requirement"] (a source module misread as an SR), file
# `#7c3aed` = OKF_TYPE_FILL["Interface"], external `#64748b` = TIER_FILL["llr"].
# Reassigned to hexes not used by STATUS_FILL/TIER_FILL/OKF_TYPE_FILL/PHASE_ACCENTS.
# WI-300 (U2 core): `component` used to be a bare `#475569` literal inside
# `cmp_block`, so the How-SW vocabulary had four kinds but declared three — the
# one kind whose colour lived outside the dict was invisible to every check that
# reasons over the vocabulary (U5's collision sweep, `_ring_ink`'s enumeration,
# and U2's own single-source rule). A vocabulary is only "one vocabulary" if
# every member is IN it.
SW_NODE_FILL = {
    "module": "#2563eb",
    "file": "#a21caf",
    "external": "#334155",
    "component": "#44403c",  # stone — the neutral container badge (10.27:1 on #fff)
}


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
# TIER_FILL/OKF_TYPE_FILL/SW_NODE_FILL, and each sits >= 11 deltaE from the three
# same-tab status hues, so a phase block never reads as a status. Excluding the
# emerald/orange/slate status families leaves the cool + magenta + one-red arc — hence
# the cool lean; distinct hues are preferred over same-hue lightness shades (the very
# jitter WI-247 removes), which caps CVD below the old maroon-free 20+.
#   WI-292 (U5 de-collision, 119-CRITIQUE): three of the eight were replaced.
# `#4f46e5` was byte-identical to the CSS `--accent` token, so the focus/hover ring
# painted in `var(--accent)` (WI-258) vanished on whichever phase happened to draw
# that slot — `#4d7c0f` replaces it. `#6d28d9` sat only 7.4 deltaE from `#7e22ce`
# (both violet, indistinguishable side by side in the phase legend) and `#1d4ed8`
# was byte-identical to `SW_NODE_FILL["module"]` (a phase block misread as a
# How-SW module) — `#1e40af`/`#155e75` replace them. Pairwise (not merely
# adjacent) deltaE across the full set is now >= 15 (`test_u5_...` asserts this).
PHASE_ACCENTS = (
    "#0369a1", "#1e40af", "#991b1b", "#134e4a",
    "#be123c", "#4d7c0f", "#be185d", "#7e22ce",
)  # fmt: skip


def _ring_ink(fill):
    """The higher-contrast of pure white/near-black against `fill` (WI-294a/
    WI-299, 119-CRITIQUE BLOCKER+MAJOR): the focus/hover ring used to be a single
    hue per emitter (`var(--accent)` in the drill views, `#f59e0b` amber in the
    icicle/flat-DAG/knowledge views) — a hue picked once cannot clear 3:1 against
    EVERY node fill (it vanished at 1.00:1 on the phase-3 block, whose fill IS
    `--accent`), and the two hues also read as two different idioms for the same
    "this node is highlighted" concept (uniformity U3/U4). Every node fill here
    is a small, enumerable, THEME-INVARIANT set (STATUS_FILL/TIER_FILL/
    OKF_TYPE_FILL/SW_NODE_FILL/PHASE_ACCENTS), so the ink can be computed once
    per fill at generation time instead of hard-coded: by the WCAG relative-
    luminance formula, whichever of white/black contrasts less against a given
    fill still clears >= 4.58:1 in the worst case (the point where white and
    black tie), comfortably above the 3:1 UI-boundary floor for every fill in
    use. Emitted as an inline `--ring` custom property the shared CSS rules read
    with a safe fallback, so a fill this helper never saw (a future emitter) does
    not silently regress — it just falls back to the old single-hue behaviour."""

    def lum(hexval):
        h = hexval.lstrip("#")
        chan = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
        lin = [
            c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chan
        ]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

    fill_lum = lum(fill)
    white = 1.05 / (fill_lum + 0.05)
    black = (fill_lum + 0.05) / 0.05
    return RING_INKS[0] if white >= black else RING_INKS[1]


# The closed set `_ring_ink` chooses between — declared, not implied, because the
# containment-arrow markers are emitted one per ink (`_cedge_marker`): a third
# ink would need a third marker, and a test asserts the closure.
RING_INKS = ("#ffffff", "#0f172a")


def _cedge_marker(fill):
    """`(marker id, ring ink)` for the containment/descend arrow drawn INSIDE a
    block of `fill` (WI-317, T5 — the arrow measured 1.06:1 light / 1.99:1 dark
    when it was painted in a fixed `var(--accent)` over the phase-1 `#0369a1`).

    The arrow is an expand/descend affordance sitting on the node's own fill, so
    it takes the same per-fill contrast-safe ink as the focus ring — but a marker
    cannot inherit the host node's `--ring` (see `_arrow_markers`), so each ink
    gets its own marker and the block references the one matching its fill. A
    theme-token fill (`var(--surface)`) keeps the unsuffixed marker and the CSS
    `var(--accent)` fallback, exactly as `_ring_style` leaves it unstamped."""
    if fill and fill.startswith("#"):
        ink = _ring_ink(fill)
        return "cedgearrow-{}".format(ink.lstrip("#")), ink
    return "cedgearrow", None


def _ring_style(fill):
    """`style="--ring:…"` for a node `<g>`/`<rect>` given its fill, or "" when
    `fill` is not a concrete hex (e.g. `var(--surface)`) — those keep the CSS
    fallback since a theme-varying token can't be resolved at generation time."""
    if not fill or not fill.startswith("#"):
        return ""
    return ' style="--ring:{}"'.format(_ring_ink(fill))


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
    # WI-294b (119-CRITIQUE U1/U3): the phase-accent key used to be its own
    # inline `span.ph` chip idiom (.55rem swatch, "Phase accent:" prefix, inside
    # the drill summary paragraph) — visibly smaller and differently placed than
    # every other legend in the document. It now renders through the SAME
    # `.legend`/`<i>` component the status/type/module legends use (see the
    # `.legend i` rule below), so no per-emitter style rule is needed here.
    ".drill nav.crumbs{display:flex;flex-wrap:wrap;align-items:center;gap:.1rem;"
    "margin:.1rem 0 .6rem;font-size:var(--small);}"
    ".drill nav.crumbs .crumb{appearance:none;background:none;border:none;"
    "cursor:pointer;font:inherit;color:var(--accent);padding:.15rem .35rem;"
    "border-radius:var(--r-ctl);}"
    ".drill nav.crumbs .crumb[aria-current]{color:var(--text);font-weight:600;"
    "cursor:default;}"
    ".drill nav.crumbs .sep{color:var(--muted);}"
    ".drill .tracebar{display:flex;flex-wrap:wrap;align-items:center;gap:.45rem 1rem;"
    "margin:0 0 .65rem;padding:.55rem .7rem;border:1px solid var(--border);"
    "border-radius:var(--r-ctl);background:var(--surface);font-size:var(--small);"
    "color:var(--muted);}"
    ".drill .tracebar strong{color:var(--text);}"
    ".drill .tracekey{display:inline-flex;align-items:center;gap:.3rem;white-space:nowrap;}"
    ".drill .tracekey i{display:inline-block;width:1.2rem;border-top:2px solid currentColor;}"
    ".drill .tracekey.in{color:var(--trace-in);}.drill .tracekey.out{color:var(--trace-out);}"
    ".drill .layer[hidden]{display:none;}"
    ".drill svg.drillsvg{display:block;font-family:inherit;}"
    ".drill .block[data-descend]{cursor:pointer;}"
    ".drill .block[data-descend] rect{stroke-width:var(--w-line);}"
    ".drill .block:focus{outline:none;}"
    # WI-294a/WI-299 (119-CRITIQUE): a single hue (--accent, then amber elsewhere)
    # cannot clear 3:1 against every node fill — it vanished at 1.00:1 on the
    # phase-3 block, whose fill IS --accent (080-CRITIQUE #5 / WI-258's fix only
    # solved the status-orange collision, not the phase-3 one). `_ring_style`
    # now emits a per-node `--ring` custom property (white or near-black,
    # whichever clears more contrast against THAT node's own fill), shared
    # identically across every SVG emitter (the icicle/flat-DAG/knowledge rules
    # below read the same property) — one highlight idiom, not two, and one that
    # cannot fail regardless of which fill it lands on. The static fallback keeps
    # today's behaviour for any node a future emitter doesn't tag with --ring.
    ".drill .block:focus rect{stroke:var(--ring,var(--accent));stroke-width:var(--w-emph);}"
    # SR-056: the hover/focus highlight persists on the last-hovered block until
    # another takes it (the shared .hl idiom — cf. the icicle/DAG/knowledge views).
    ".drill .block.hl rect{stroke:var(--ring,var(--accent));stroke-width:var(--w-emph);}"
    ".drill .block .blab{font-size:var(--nlabel);font-weight:700;}"
    ".drill .block .bsub{font-size:var(--nsub);}"
    ".drill .port{fill:var(--surface);stroke:var(--muted);stroke-width:var(--w-line);}"
    ".drill .port.in{stroke:var(--accent);}"
    ".drill .wire{fill:none;stroke:var(--muted);stroke-width:var(--w-line);opacity:var(--o-muted);"
    "stroke-linejoin:round;stroke-linecap:round;marker-end:var(--arrow);}"
    ".drill[data-focused-trace] .port.in{stroke:var(--trace-in);}"
    ".drill[data-focused-trace] .port.out{stroke:var(--trace-out);}"
    ".drill[data-focused-trace] .wire{opacity:var(--o-wash);"
    "transition:opacity .12s ease,stroke .12s ease,stroke-width .12s ease;}"
    ".drill[data-focused-trace] .wire.trace-in{stroke:var(--trace-in);stroke-width:var(--w-emph);opacity:var(--o-full);"
    "marker-end:var(--arrow-in);}"
    ".drill[data-focused-trace] .wire.trace-out{stroke:var(--trace-out);stroke-width:var(--w-emph);opacity:var(--o-full);"
    "marker-end:var(--arrow-out);}"
    ".drill[data-focused-trace] .block.trace-muted{opacity:var(--o-ghost);}"
    ".drill[data-focused-trace] .block.trace-in rect{stroke:var(--trace-in);stroke-width:var(--w-emph);}"
    ".drill[data-focused-trace] .block.trace-out rect{stroke:var(--trace-out);stroke-width:var(--w-emph);}"
    ".drill[data-focused-trace] .block.trace-focus rect{stroke:var(--ring,var(--text));stroke-width:var(--w-emph);}"
    ".drill .warrow{fill:var(--muted);}"
    ".drill .warrow-in{fill:var(--trace-in);}.drill .warrow-out{fill:var(--trace-out);}"
    # SR-056: one horizontal parent→child arrow per containment edge — a distinct
    # colour (vs. the muted dependency wire) marks it as a descend/containment edge.
    # WI-317 (T5): that colour was a fixed `var(--accent)`, and the arrow is drawn
    # INSIDE the block, over the node's own fill — 1.06:1 light / 1.99:1 dark on
    # the phase-1 `#0369a1`, the same way the focus ring vanished at 1.00:1 before
    # WI-299. It now reads the same per-node `--ring` control token; the head is
    # painted by a per-ink marker (`_cedge_marker`) because marker content cannot
    # see the referencing node's custom properties. `var(--accent)` stays the
    # fallback for a theme-token fill, where accent is tuned as ink already.
    ".drill .cedge{fill:none;stroke:var(--ring,var(--accent));stroke-width:var(--w-line);}"
    ".drill .cedgehead{fill:var(--ring,var(--accent));}"
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
    "const traceEl=drill.querySelector('.trace-status');"
    "const tracing=drill.hasAttribute('data-focused-trace');"
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
    "});if(tracing)selectDefault();if(window.__syncCues)window.__syncCues();}"
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
    "function visibleLayer(){return byId[trail[trail.length-1].id];}"
    "function selectNode(el){"
    "const layer=visibleLayer();if(!layer||!el)return;"
    "const key=el.getAttribute('data-node');"
    "const blocks=[...layer.querySelectorAll('.block[data-node]')];"
    "const wires=[...layer.querySelectorAll('.wire[data-from][data-to]')];"
    "for(const b of blocks)b.classList.remove('trace-focus','trace-in','trace-out','trace-muted');"
    "for(const w of wires)w.classList.remove('trace-in','trace-out');"
    "const incoming=[],outgoing=[];"
    "for(const w of wires){const from=w.getAttribute('data-from'),to=w.getAttribute('data-to');"
    "if(to===key){w.classList.add('trace-in');incoming.push(from);}"
    "if(from===key){w.classList.add('trace-out');outgoing.push(to);}}"
    "for(const b of blocks){const k=b.getAttribute('data-node');"
    "if(k===key)b.classList.add('trace-focus');"
    "else if(incoming.includes(k))b.classList.add('trace-in');"
    "else if(outgoing.includes(k))b.classList.add('trace-out');"
    "else b.classList.add('trace-muted');}"
    "drill.setAttribute('data-trace',key||'');"
    "if(traceEl){const label=el.getAttribute('data-label')||key;"
    "const nameOf=k=>{const b=blocks.find(x=>x.getAttribute('data-node')===k);"
    "return b?(b.getAttribute('data-label')||k):k;};"
    "const names=xs=>xs.length?xs.map(nameOf).join(', '):'none';"
    "traceEl.innerHTML='<strong>'+escapeHtml(label)+'</strong> · ← Needs: '+"
    "escapeHtml(names(incoming))+' · Unlocks → '+escapeHtml(names(outgoing));}}"
    "function escapeHtml(s){const x=document.createElement('span');x.textContent=s||'';return x.innerHTML;}"
    "function selectDefault(){const layer=visibleLayer();if(!layer)return;"
    "const blocks=[...layer.querySelectorAll('.block[data-node]')],"
    "wires=[...layer.querySelectorAll('.wire[data-from][data-to]')];"
    "let best=null,bestDegree=Infinity;for(const b of blocks){const k=b.getAttribute('data-node');"
    "const d=wires.filter(w=>w.getAttribute('data-from')===k||w.getAttribute('data-to')===k).length;"
    "if(d>0&&d<bestDegree){best=b;bestDegree=d;}}selectNode(best||blocks[0]);}"
    "function highlight(el){"
    "if(hl===el)return;"
    "if(hl)hl.classList.remove('hl');"
    "hl=el;el.classList.add('hl');"
    "drill.setAttribute('data-hl',el.getAttribute('data-node')||'');if(tracing)selectNode(el);}"
    "for(const el of drill.querySelectorAll('.block')){"
    "el.addEventListener('mouseover',function(){highlight(el);});"
    "el.addEventListener('focus',function(){highlight(el);});"
    "if(tracing)el.addEventListener('click',function(){highlight(el);});}"
    "render();}"
    "})();</script>"
)


def _fit_lines(text, budget, max_lines):
    """`text` broken onto at most `max_lines` lines of at most `budget` characters,
    preferring a space break; the last line is ellipsized when text remains. A word
    longer than the budget is hard-cut rather than allowed to run past the box.
    `[]` for empty text, so a caller can keep its own empty-sub rendering."""
    text = (text or "").strip()
    if not text:
        return []
    lines, rest = [], text
    while rest and len(lines) < max_lines:
        if len(rest) <= budget:
            lines.append(rest)
            rest = ""
            break
        cut = rest.rfind(" ", 0, budget + 1)
        if cut <= 0:  # one word longer than the budget
            cut = budget
        lines.append(rest[:cut].rstrip())
        rest = rest[cut:].lstrip()
    if rest:
        last = lines[-1]
        lines[-1] = (last[: budget - 1].rstrip() if len(last) >= budget else last) + "…"
    return lines


def _drill_block_label(b, col_w, cx, cy):
    """The centred `<text>` for one drill block. A plain label renders as the bold
    label line over its sub-label. A block flagged `wrap` with an `ID — Name` label
    (the CMP component blocks, "CMP-009 — W4 Human & adopter surfaces") WRAPS onto an id
    line over a name line — the `arch_icicle` id/name idiom (WI-246/075-CRITIQUE T4) —
    so the full component name reads at default zoom instead of truncating to
    "CMP-009 — W4 Human & adopter…"; the sub-label (module count) drops to a third line. The
    name line uses the smaller sub font, so its budget (and the right-sized column)
    fit the longest declared name. The explicit `wrap` flag (not a `" — "` string
    sniff) keeps an incidental em-dash in some other block's name from wrapping.

    WI-318 (T4, 121-CRITIQUE MAJOR): the SUB-label used to be emitted RAW, so a
    block whose sub is a sentence rather than a count — the What root layer draws
    each SN's whole need there — ran outside its own box at every width, and
    `_tier_col_width` cannot absorb that (it clamps at MAX_TIER_COL). It is now
    fitted to the column like the label. Three text lines is the ceiling — the grid
    the `wrap` branch above already proved fits `row_h` — so the budget is two sub
    lines; a sub that already fits one renders byte-identically to before. Rule,
    scope and residue: LLR-119 / TC-124."""
    fill = b.get("textfill", "var(--text)")
    head = '<text x="{:.1f}" y="{:.1f}" text-anchor="middle" fill="{}">'.format(
        cx, cy, fill
    )
    nbudget = max(1, (col_w - TIER_COL_PAD) // _BSUB_CH)
    if b.get("wrap") and " — " in b["label"]:
        idpart, namepart = b["label"].split(" — ", 1)
        if len(namepart) > nbudget:
            namepart = namepart[: nbudget - 1] + "…"
        # The id and name lines already spend the 3-line budget, so the sub fits
        # one line here.
        sub = (_fit_lines(b["sub"], nbudget, 1) or [""])[0]
        return (
            head
            + '<tspan x="{:.1f}" dy="-11" class="blab">{}</tspan>'
            '<tspan x="{:.1f}" dy="11" class="bsub">{}</tspan>'
            '<tspan x="{:.1f}" dy="11" class="bsub">{}</tspan></text>'.format(
                cx, esc(idpart), cx, esc(namepart), cx, esc(sub)
            )
        )
    max_label = max(1, (col_w - TIER_COL_PAD) // _BLAB_CH)
    main_label = b["label"]
    if len(main_label) > max_label:
        main_label = main_label[: max_label - 1] + "…"
    subs = _fit_lines(b["sub"], nbudget, 2) or [""]
    # Two lines keep the original grid byte-for-byte; three take the `wrap` grid.
    head_dy, sub_dy = (-2, 13) if len(subs) == 1 else (-11, 11)
    span = '<tspan x="{:.1f}" dy="{}" class="{}">{}</tspan>'
    return (
        head
        + span.format(cx, head_dy, "blab", esc(main_label))
        + "".join(span.format(cx, sub_dy, "bsub", esc(s)) for s in subs)
        + "</text>"
    )


def _edge_ports(side, px, cy, attached, offsets):
    """The connector circles on ONE side of one block: a single centred ring when
    no wire lands there, otherwise one ring per edge at that edge's own fan offset
    (WI-435 — several edges sharing a side used to collapse into one centre-port
    wedge). Each ring carries its edge's endpoints, so a connector and its wire
    are attributable to each other in the markup as well as on screen."""
    if not attached:
        return (
            '<circle class="port {}" cx="{:.1f}" cy="{:.1f}" r="{}"></circle>'.format(
                side, px, cy, PORT_R
            )
        )
    return "".join(
        '<circle class="port {} wire-port" cx="{:.1f}" cy="{:.1f}" '
        'data-from="{}" data-to="{}" r="{}"></circle>'.format(
            side, px, cy + offsets[e], esc(e[0]), esc(e[1]), PORT_R
        )
        for e in attached
    )


def _drill_layer_svg(blocks, edges, marker_scope):
    """One drill layer as a plain SVG block diagram. Each block is a rectangle with
    an input port (left-middle) and an output port (right-middle); each aggregated
    `edges` entry (src_key, tgt_key, title) is a wire from the source block's OUTPUT
    port to the target block's INPUT port (Simulink-style). Blocks lay out left->
    right by the shared layered pipeline over the edge set, so a producer sits left
    of its consumer and crossings are reduced. Byte-deterministic.

    WI-435 keeps the shared obstacle-aware corridor calculation but presents drill
    wires as orthogonal M/L paths. Fan offsets terminate at explicit per-edge port
    circles, so several edges no longer merge into one centre-port wedge. The end
    remains pulled back by PORT_R + 2 so a 12px focused arrowhead stays visible;
    marker ids are scoped per layer because duplicate ids resolved a visible path
    through a hidden layer's marker definition. `marker_scope` is REQUIRED for
    that reason — a default would let a successor emitter re-mint the collision
    silently, and the symptom (an arrowhead that vanishes in one layer only) is
    invisible in the markup a test reads."""
    keys = [b["key"] for b in blocks]
    marker_scope = re.sub(r"[^A-Za-z0-9_-]", "-", marker_scope) or "drill"
    arrow = marker_scope + "-drillarrow"
    arrow_in = marker_scope + "-drillarrow-in"
    arrow_out = marker_scope + "-drillarrow-out"
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
    geom = GraphGeom(col_w, *DRILL_GEOM[1:])
    pos, width, height = _layered_layout(
        [{"id": k} for k in keys],
        pred_map,
        succ_map,
        lambda k: (order[k], k),
        geom,
    )
    _cw, _cg, row_h, row_gap, _pad = geom

    # Backward dependencies need an outboard lane. Reserve a visible top/bottom
    # gutter before routing so those square U-turns stay inside the drawing instead
    # of relying on a clipped negative-y lane at the card edge.
    backward = sum(pos[b][0] <= pos[a][0] + col_w for a, b, _t in wire_edges)
    if backward:
        gutter = min(38, 8 + backward * 10)
        pos = {key: (x, y + gutter) for key, (x, y) in pos.items()}
        height += 2 * gutter

    # Each route begins at its own output connector and ends PORT_R + 2 px before
    # its own input connector, leaving the marker visible outside the ring. The
    # shared router still chooses obstacle-clear corridors; `orthogonal_route`
    # squares those corridors and rechecks candidate bends against every other box.
    fan_span = row_h - 2 * (PORT_R + 3)
    rects = {key: (x, y, col_w, row_h) for key, (x, y) in pos.items()}
    routes, out_off, in_off = route_graph(
        keys,
        wire_edges,
        pos,
        geom,
        14,
        PORT_R + 2,
        fan_terminals=True,
        fan_span=fan_span,
    )
    wires = []
    for e in sorted(wire_edges):
        title = e[2]
        wires.append(
            '<path class="wire" d="{}" data-from="{}" data-to="{}" '
            'style="--arrow:url(#{});--arrow-in:url(#{});--arrow-out:url(#{})">'
            "{}</path>".format(
                orthogonal_route(
                    routes[e],
                    [rect for key, rect in rects.items() if key not in e[:2]],
                ),
                esc(e[0]),
                esc(e[1]),
                esc(arrow),
                esc(arrow_in),
                esc(arrow_out),
                "<title>{}</title>".format(esc(title)) if title else "",
            )
        )

    nodes = []
    cedge_markers = {}  # WI-317: marker id -> ring ink, only the ones this layer uses
    for b in blocks:
        x, y = pos[b["key"]]
        cy = y + row_h / 2
        cx = x + col_w / 2
        label = _drill_block_label(b, col_w, cx, cy)
        incoming = sorted(e for e in wire_edges if e[1] == b["key"])
        outgoing = sorted(e for e in wire_edges if e[0] == b["key"])
        ports = _edge_ports("in", x, cy, incoming, in_off) + _edge_ports(
            "out", x + col_w, cy, outgoing, out_off
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
            # WI-317: its head is the marker matching THIS block's ring ink.
            ax = x + col_w - CEDGE_LEN - 6
            marker, ink = _cedge_marker(b.get("fill"))
            mid = marker_scope + "-" + marker
            cedge_markers[mid] = ink
            cedge = (
                '<path class="cedge" d="M{:.1f},{:.1f} h{}" '
                'marker-end="url(#{})"><title>contains → descend</title>'
                "</path>".format(ax, y + 9, CEDGE_LEN, mid)
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
        # WI-272: the row's TRUE status, where the swatch alone cannot carry it
        # (`deferred`/`blocked` share `queued`'s fill). Appended last for the same
        # adjacency reason as data-node above. Absent for non-status blocks (the
        # phase/workstream containers and the whole How-SW drill).
        if b.get("status"):
            attrs += ' data-status="{}"'.format(esc(b["status"]))
        # WI-294a/WI-299: appended last, same reason as data-node above — keeps
        # every existing adjacency assertion (`data-tier="…" data-descend="…"`)
        # intact for tests that don't know this attribute exists.
        attrs += _ring_style(b.get("fill"))
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

    defs = _arrow_markers(
        (arrow, "warrow"),
        (arrow_in, "warrow-in", 12),
        (arrow_out, "warrow-out", 12),
        *(
            (mid, "cedgehead", 8) if ink is None else (mid, "cedgehead", 8, ink)
            for mid, ink in sorted(cedge_markers.items())
        ),
    )
    body = defs + "".join(wires) + "".join(nodes)
    return (
        '<svg {a} preserveAspectRatio="xMinYMin meet" role="{r}" class="drillsvg">'
        "{b}</svg>".format(a=_svg_frame(width, height, body), r=_svg_role(body), b=body)
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
    focused = drill_id in {"when", "sw"}
    tracebar = (
        '<div class="tracebar"><span class="trace-status" aria-live="polite">'
        "Select a card to trace its direct relationships</span>"
        '<span class="tracekey in"><i></i>→ selected: prerequisites</span>'
        '<span class="tracekey out"><i></i>selected → dependents</span></div>'
        if focused
        else ""
    )
    return (
        '<div class="drill" data-drill="{did}"{focused} data-root="{root}" '
        'data-root-crumb="{crumb}">'
        # A2 name QUALITY (WI-312): three drills each render a breadcrumb, and
        # all three used to be `aria-label="Breadcrumb"`. A screen-reader user
        # listing the page's navigation landmarks then hears "Breadcrumb" three
        # times with nothing to tell them apart — a name can be present, correct
        # and still useless. The root crumb already names the view, so it makes
        # each landmark self-identifying at no cost.
        '<nav class="crumbs" aria-label="{crumb} breadcrumb"></nav>{tracebar}'
        '<div class="layers">{divs}</div></div>{script}'.format(
            did=esc(drill_id),
            focused=' data-focused-trace="true"' if focused else "",
            root=esc(root_id),
            crumb=esc(root_crumb),
            tracebar=tracebar,
            divs=divs,
            script=DRILL_SCRIPT,
        )
    )


# Node fill keyed by the OKF `type` (the icicle tier palette, extended for the
# two off-spine concept kinds the bundle also carries). SN/SR/LLR/TC intentionally
# mirror TIER_FILL — one concept, two label systems (a tier code vs a type name).
# `Test Case` mirrors TIER_FILL["tc"]; `Process Guide` used to reuse
# STATUS_FILL["active"]'s `#b45309` for an unrelated concept (WI-292, U5
# de-collision, 119-CRITIQUE) and is reassigned below.
OKF_TYPE_FILL = {
    "Stakeholder Need": "#4338ca",
    "System Requirement": "#0e7490",
    "Low-Level Requirement": "#64748b",
    "Test Case": "#0f766e",
    "Interface": "#701a75",
    "Process Guide": "#9a3412",
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
