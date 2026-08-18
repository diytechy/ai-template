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
  3. **How (SW)** — the module map scanned LIVE from the source tree under
     `[paths] src` (`gen_arch_map.scan_inventory`; WI-455 retired the committed
     `docs/architecture.md` way-station), plus the authored Runtime flows
     embedded from `docs/runtime-flows.md`; omitted when there is no symbol
     inventory, e.g. files-mode.
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
     the slice -> phase -> gate-bar cadence, and (WI-142/LLR-056) the two circular working loops —
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
             (WI-234); with --check, byte-compare BOTH for freshness — the
             successor invariant to the WI-200 forward-only token guard. Vacuous
             (exit 0) per file when it is absent or has no marker pair.
An absent or placeholder-only registry renders nothing and passes vacuously (the
opt-out layer stays free for a repo that never adopts it).
Exit codes: 0 clean / vacuous / opted-out, 1 invalid registry or stale HTML.

WI-280 decomposition: the implementation lives in sibling modules —
traj_graph.py (pure layout + wire routing), traj_parse.py (registry/doc/git
sources + the guarded `schedule` import), traj_render.py (SVG/HTML
primitives, palettes, the drill renderer), traj_views.py (the What/When/
How-SW views + panels), traj_panels.py (the Knowledge/Process/Next-work
panels), traj_status.py (the --status snapshot + pending projection) —
each re-exported here, so
`import gen_trajectory` stays the one consumer seam and the render is
byte-identical across the split.

Contracts: IF-011, IF-024, IF-052, IF-056, IF-071 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv). IF-071 (WI-290) is the frontier DECISION seam: gen_trajectory reads schedule.frontier for the generated STATUS block + Process-tab loop — distinct from IF-056's derivation-loader seam to check_trajectory (validate vs decide).
"""

import argparse
import html
import json
import re
import string
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

# --- WI-280 split: the decomposed sibling modules ------------------------------
# The implementation lives in the split siblings — traj_graph.py (layout +
# wire routing), traj_parse.py (sources + the guarded `schedule` import's one
# home), traj_render.py (SVG/HTML primitives + the drill renderer),
# traj_views.py (the What/When/How-SW views + panels), traj_panels.py (the
# Knowledge/Process/Next-work panels), traj_status.py (the --status snapshot
# + pending projection) — and this facade re-exports the consumer-read names
# so every existing `gen_trajectory.<name>` import keeps resolving (the seam,
# and its Contracts: line, stay HERE). These
# imports sit AFTER the guarded check_trajectory import above on purpose: that
# guard is this module's ONE sys.path repair, and the siblings rely on it when
# this file is loaded from outside scripts/ (the F5 self-heal contract).
# Every sibling is ALSO bound as a bare module attribute (`gen_trajectory.traj_parse`
# and friends): the facade's re-exported names are values, so a consumer that must
# reach the module OBJECT — the suite patches `gt.traj_graph._detour_points` and
# `gt.traj_parse.subprocess`, which only works on the instance the moved code
# actually resolves in — has one place to reach it. Deliberate, hence the
# per-line F401 suppression each carries: unused HERE is the point.
import traj_views  # noqa: F401
import traj_status  # noqa: F401
import traj_render  # noqa: F401
import traj_panels  # noqa: F401
import traj_parse  # noqa: F401
from traj_parse import (  # noqa: F401
    OKF_DIR,
    OKF_TIER_ORDER,
    PROCESS_GATE_FILE,
    WORKSTREAM_LABELS,
    _asof,
    _gate_value,
    _git,
    _okf_frontmatter,
    _okf_nodes,
    _process_doc,
    _run_captured,
    _sn_rows,
    _spine,
    cmp_rows,
    project_name,
    project_vision,
    read_sns,
    runtime_flows,
    schedule,
    spine_stats,
    sw_modules,
)
import traj_graph  # noqa: F401
from traj_render import (  # noqa: F401
    ARROW_SIZE,
    CEDGE_LEN,
    DRILL_GEOM,
    DRILL_SCRIPT,
    DRILL_STYLE,
    MAX_TIER_COL,
    OKF_TYPE_CODE,
    OKF_TYPE_FILL,
    PHASE_ACCENTS,
    PORT_R,
    RING_INKS,
    SCROLL_CUE,
    SHRINK_FLOOR,
    STATUS_BUCKET,
    STATUS_BUCKET_LABEL,
    STATUS_FILL,
    STATUS_GLYPH,
    SVG_RX,
    SW_NODE_FILL,
    TIER_COL,
    TIER_FILL,
    _BLAB_CH,
    _BSUB_CH,
    _FOCUSABLE,
    _INK_PAD,
    _arrow_markers,
    _cedge_marker,
    _drill_block_label,
    _drill_layer_svg,
    _fit_lines,
    _hscroll,
    _ink_overflow,
    _path_xs,
    _render_drill,
    _ring_ink,
    _ring_style,
    _svg_fit_style,
    _svg_frame,
    _svg_role,
    _svg_wrap,
    _tier_col_width,
    esc,
    tab_button,
    tab_panel_open,
)
from traj_views import (  # noqa: F401
    DEFAULT_PHASE,
    SW_CMPTREE_STYLE,
    _cmp_panel,
    _dag_layout,
    _sw_node,
    _sw_panel,
    _wi_phases,
    _wi_st,
    _wi_status,
    arch_icicle,
    dag_svg,
    flows_block,
    sw_containment,
    sw_graph,
    when_view,
)
from traj_status import (  # noqa: F401
    PAUSE_MALFORMED,
    STATUS_BEGIN,
    STATUS_END,
    STATUS_MD,
    _blocked_pending,
    _clip_title,
    _frontier_lines,
    _gate_facts,
    _open_item_oneliners,
    _pause_pending,
    _spine_counts,
    _spine_pending,
    _splice_status,
    _title_clause,
    pending_block,
    run_status,
    status_block,
)
from traj_panels import (  # noqa: F401
    _NEXT_WORK_CAP,
    _NEXT_WORK_TITLE,
    _know_panel,
    _next_work_html,
    _next_work_title,
    _station_panel,
    know_graph,
    know_view,
    process_panel,
)
from traj_graph import (  # noqa: F401
    GraphGeom,
    _FAN_PITCH,
    _LEAD_RUNGS,
    _MAX_LANES,
    _cubic_points,
    _dag_ranks,
    _detour_d,
    _detour_points,
    _layered_layout,
    _lead_rung,
    _port_fan,
    _route_edges,
    _routed_label_xy,
    _seg_hits_rect,
    flat_graph,
    route_graph,
)

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
HTML_TEMPLATE = string.Template("""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$project — Project State</title>
<style>
  :root {
    color-scheme: light dark;
    --bg:#f8fafc; --surface:#ffffff; --border:#e2e8f0; --text:#0f172a;
    --muted:#64748b; --accent:#4f46e5;
    /* Focused dependency tracing: blue flows into the selected node; amber
       flows out. Both carry foreground ink, so both are theme tokens — and both
       sit deliberately OUTSIDE every declared concept palette. WI-435's first
       pass reused SW_NODE_FILL's "module" ink and STATUS_FILL's "active" ink, so
       one colour carried two meanings inside a single diagram: a module block
       wired by same-blue "incoming" strands, an active work item wired by
       same-amber "outgoing" ones. A3's sweep convicts that reuse — and it reads
       THIS comment as paint too, which is why no hex is spelled out here. */
    --trace-in:#1d4ed8; --trace-out:#ea580c;
    /* A4 (WI-293): the Process tab's emphasized node (the merge slot since the
       WI-389 station-cycle redraw; the hub before it) carries WHITE text on its
       own fill, so its fill is a THEME-INVARIANT token, not --accent. --accent
       is tuned for readability *as ink* on the page background and lightens to
       #818cf8 in dark, which as a *fill* behind white text measures 2.98:1 —
       under the 4.5:1 AA floor. Declared here and deliberately NOT overridden
       in the dark block: #fff on #4f46e5 is 6.29:1 in both themes. Keep any
       successor palette change (WI-292) off this token unless it re-checks
       white-on-fill. */
    --slot:#4f46e5;
    --done:#047857; --active:#b45309; --queued:#94a3b8; --cancelled:#78716c;
    /* ===== THE TYPE SCALE (U1 core, WI-309) =================================
       Every font-size in this document resolves to a step declared here —
       `test_u1_every_font_size_resolves_to_a_declared_scale_step` enforces it
       over every emitter. Before WI-309 there were 18 raw literals against 5
       tokens, including `.7rem`/`.75rem`, `.9`/`.95`/`.98rem`,
       `1.05`/`1.1rem` and `8.5px`/`9px` — near-duplicate steps for ONE role,
       3-7% apart, which no reader distinguishes and no rule justified. Those
       merged into the nearer step; two literals (`.85rem`, `.8rem`) were
       byte-identical to a token that simply was not being used.

       THREE FAMILIES, because there genuinely are three. Claiming "one scale"
       across them would be false:
         - NODE (px): SVG labels. Fixed px because the SVG geometry is fixed px
           — a rem here would resize labels out of their boxes.
         - PAGE (rem): prose and chrome, scaling with the root size.
         - RELATIVE (em): text that must size against its PARENT, not the root
           (inline `code`, a table sub-line).
       Add a step only with a role no existing step covers, and say the role. */
    /* node: per-node label, its sub-label, and a once-per-diagram headline
       (the Process hub title and the icicle lane heads are the same role). */
    --nlabel:10px; --nsub:8.5px; --nhead:13px;
    /* page: tiny < xsmall < small < body < lead < display < hero. */
    --tiny:.75rem; --xsmall:.8rem; --small:.85rem; --body:.9rem;
    --lead:1.05rem; --display:1.4rem; --hero:2rem;
    /* relative: one step, for text sized against its parent. */
    --rel:.9em;
    /* ===== WEIGHT, EMPHASIS AND CORNER (U3 core, WI-310) ====================
       The same declare-then-assert discipline as the type scale above, for the
       three properties that carry "visual weight" —
       `test_u3_every_weight_value_resolves_to_a_declared_token` enforces it.
       Measured before WI-310: 8 distinct stroke-widths, 7 opacities and 5
       corner radii, which is drift rather than a system: FIVE stroke widths
       (1, 1.2, 1.4, 1.5, 1.8) were doing the single job "draw a connector".
       Each token below names a ROLE; near-duplicates merged into the role's
       step. Add one only for a role no existing step covers. */
    /* stroke — a hairline separator, a node's own outline, any connector
       (edge/wire/port/containment arrow), and the focus/hover emphasis. */
    --w-hair:.5; --w-node:1; --w-line:1.5; --w-emph:2.5;
    /* alpha — a background wash, a de-emphasised node, a faint outline, an
       advisory (soft) edge, an ordinary edge, and the reset to fully opaque. */
    --o-wash:.05; --o-dim:.15; --o-ghost:.35; --o-soft:.65;
    --o-muted:.85; --o-full:1;
    /* corner — legend chip, small control, card/panel, and a full pill. */
    --r-chip:3px; --r-ctl:6px; --r-card:12px; --r-pill:999px;
    --shadow:0 1px 3px rgba(15,23,42,.06),0 1px 2px rgba(15,23,42,.04);
  }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#0b1120; --surface:#0f172a; --border:#1e293b; --text:#e2e8f0;
            --muted:#94a3b8; --accent:#818cf8;
            --trace-in:#60a5fa; --trace-out:#f59e0b;
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
  .mark { font-weight:700; letter-spacing:-.02em; font-size:var(--lead); }
  .mark .dot { color:var(--accent); }
  .top-sub { color:var(--muted); font-size:var(--small); }
  .hero { padding:2.25rem 0 1.5rem; }
  .hero h1 { font-size:var(--lead); text-transform:uppercase; letter-spacing:.08em;
             color:var(--muted); margin:0 0 .6rem; font-weight:600; }
  .asof { color:var(--muted); font-size:var(--small); margin:.4rem 0 0; }
  table.swmap { border-collapse:collapse; width:100%; font-size:var(--body); }
  table.swmap th, table.swmap td { text-align:left; padding:.45rem .6rem;
    border-bottom:1px solid var(--border); vertical-align:top; }
  table.swmap .sub { color:var(--muted); font-size:var(--rel); }
  .vision { font-size:var(--display); line-height:1.4; font-weight:600;
            letter-spacing:-.02em; margin:0; max-width:60ch; }
  .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
           gap:1rem; margin:1.75rem 0 .5rem; }
  .card { background:var(--surface); border:1px solid var(--border);
          border-radius:var(--r-card); padding:1.1rem 1.2rem; box-shadow:var(--shadow); }
  .card .label { font-size:var(--xsmall); text-transform:uppercase; letter-spacing:.05em;
                 color:var(--muted); font-weight:600; }
  .card .big { font-size:var(--hero); font-weight:700; letter-spacing:-.03em;
               margin:.15rem 0 .1rem; }
  .card .sub { font-size:var(--small); color:var(--muted); }
  .card .sub.nowat { color:var(--active); font-weight:600; margin-top:.2rem; }
  .meter { background:var(--border); border-radius:var(--r-pill); height:.55rem;
           overflow:hidden; margin-top:.7rem; }
  .meter > span { display:block; height:100%; border-radius:var(--r-pill); }
  .meter.def > span { background:var(--accent); }
  .meter.exe > span { background:var(--done); }
  .tiles { display:flex; flex-wrap:wrap; gap:.5rem; }
  .tile { flex:1 1 90px; background:var(--surface); border:1px solid var(--border);
          border-radius:var(--r-card); padding:.7rem .8rem; text-align:center;
          box-shadow:var(--shadow); }
  .tile b { display:block; font-size:var(--display); letter-spacing:-.02em; }
  .tile span { font-size:var(--tiny); color:var(--muted); text-transform:uppercase;
               letter-spacing:.04em; }
  /* T1 (SR-054, WI-305): the landing "Next work" surface — a `.card` box (reusing
     its surface/border/label styling) listing the scheduler's ready frontier so
     "find the next work" costs zero tab switches. */
  .nextwork { margin:.5rem 0 1rem; }
  .nwlist { list-style:none; margin:.5rem 0 0; padding:0; display:grid; gap:.35rem; }
  .nwlist li { font-size:var(--small); color:var(--text); }
  .nwlist .nwid { font-weight:700; }
  .nwlist .nwt { color:var(--muted); }
  .nwlist li.waiting .nwid { color:var(--muted); }
  .nwafter { color:var(--active); font-size:var(--xsmall); font-weight:600; }
  .nwmore { color:var(--muted); font-size:var(--xsmall); }
  /* T4 (WI-319, 121-CRITIQUE MINOR): a title long enough to still need clipping
     after the card stopped budgeting by character count reveals through a NATIVE
     disclosure — operable by pointer and keyboard, with no script — so the
     ellipsis a reader meets is one they can act on. Opening hides the cue and
     the remainder joins the text it was cut from. */
  .nwt details, .nwt summary { display:inline; }
  .nwt summary { cursor:pointer; list-style:none; }
  .nwt summary::-webkit-details-marker { display:none; }
  .nwt .nwrev { color:var(--accent); font-size:var(--xsmall); font-weight:600;
                margin-left:.15rem; }
  .nwt details[open] .nwrev { display:none; }
  .nwnone { color:var(--muted); font-size:var(--small); margin:.5rem 0 0; }
  nav.tabs { display:flex; flex-wrap:wrap; gap:.25rem; margin:2rem 0 0; border-bottom:1px solid var(--border); }
  nav.tabs button { appearance:none; background:none; border:none; cursor:pointer;
     font:inherit; font-weight:600; color:var(--muted); padding:.6rem .9rem;
     border-bottom:2px solid transparent; margin-bottom:-1px; }
  nav.tabs button:hover { color:var(--text); }
  nav.tabs button.active { color:var(--accent); border-bottom-color:var(--accent); }
  .panel { display:none; padding-top:1.4rem; }
  .panel.active { display:block; }
  .panel h2 { font-size:var(--lead); margin:0 0 .3rem; letter-spacing:-.01em; }
  .panel p.cap { color:var(--muted); margin:0 0 1rem; max-width:70ch; }
  .layout { display:grid; grid-template-columns:1fr 320px; gap:1rem; }
  .view { overflow:auto; max-height:660px; background:var(--surface);
          border:1px solid var(--border); border-radius:var(--r-card); box-shadow:var(--shadow);
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
  #ice .cell rect { stroke:rgba(255,255,255,.35); stroke-width:var(--w-hair); cursor:pointer;
        transition:opacity .1s ease; }
  #ice .cell text { fill:#fff; font-size:var(--nlabel); pointer-events:none; }
  #ice .cell .sub { font-size:var(--nsub); }
  #ice .lane-head { fill:var(--muted); font-size:var(--nhead); font-weight:700; letter-spacing:.06em; }
  .cell.dim, .wi.dim, .edge.dim { opacity:var(--o-dim); }
  #ice .cell.hl rect { stroke:var(--ring,#f59e0b); stroke-width:var(--w-emph); }
  .cell:focus, .wi:focus { outline:none; }
  #dag .wi rect { stroke:rgba(15,23,42,.15); stroke-width:var(--w-node); cursor:pointer;
        transition:opacity .1s ease; }
  #dag .wi text { fill:#fff; pointer-events:none; }
  #dag .wi .wid { font-size:var(--nlabel); font-weight:700; }
  #dag .wi .sub { font-size:var(--nsub); }
  #dag .wi.queued text { fill:#0f172a; }
  #dag .wi.hl rect { stroke:var(--ring,#f59e0b); stroke-width:var(--w-emph); }
  #dag .edge { fill:none; stroke:var(--muted); stroke-width:var(--w-line); opacity:var(--o-muted); }
  #dag .edge.soft { stroke-dasharray:5 4; opacity:var(--o-soft); }
  #dag .edge.hl { stroke:#f59e0b; stroke-width:var(--w-emph); opacity:var(--o-full); }
  #dag .arrowhead { fill:var(--muted); }
  .detail { background:var(--surface); border:1px solid var(--border);
        border-radius:var(--r-card); padding:1rem 1.1rem; box-shadow:var(--shadow);
        overflow-y:auto; max-height:640px; }
  .detail .hint { color:var(--muted); }
  .detail .badge { display:inline-block; font-size:var(--xsmall); font-weight:700;
        text-transform:uppercase; letter-spacing:.05em; padding:.15rem .5rem;
        border-radius:var(--r-ctl); color:#fff; }
  .detail h3 { font-size:var(--body); margin:.55rem 0 .35rem; letter-spacing:-.01em; }
  .detail .status { color:var(--muted); font-size:var(--xsmall); margin:0 0 .5rem; }
  .detail .body { color:var(--text); margin:.2rem 0; }
  .detail .meta { color:var(--muted); font-size:var(--small); margin-top:.6rem;
        border-top:1px solid var(--border); padding-top:.55rem; }
  @media (max-width:760px){ .layout{ grid-template-columns:1fr; }
        .detail{ max-height:none; } .scrollcue{ display:block; } }
  .legend { display:flex; flex-wrap:wrap; gap:1rem; margin-top:.9rem;
            font-size:var(--small); color:var(--muted); }
  .legend i { display:inline-block; width:.8rem; height:.8rem; border-radius:var(--r-chip);
              vertical-align:-1px; margin-right:.35rem; }
  footer { margin-top:2.5rem; padding-top:1rem; border-top:1px solid var(--border);
           color:var(--muted); font-size:var(--xsmall); }
  code { font-size:var(--rel); }
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
          <div class="sub">$sr_verified of $sr_total system requirements approved</div>
          <div class="meter def"><span style="width:$def_pct%"></span></div>
        </div>
        <div class="card">
          <div class="label">Execution</div>
          <div class="big">$wi_pct%</div>
          <div class="sub">$wi_done of $wi_total work items done · $wi_active active$wi_cancelled_clause</div>
          $wi_active_line
          <div class="meter exe"><span style="width:$wi_pct%"></span></div>
        </div>
      </div>

      $next_work

      <div class="tiles">
        <div class="tile"><b>$sn_total</b><span>SN</span></div>
        <div class="tile"><b>$sr_total</b><span>SR</span></div>
        <div class="tile"><b>$llr_total</b><span>LLR</span></div>
        <div class="tile"><b>$tc_total</b><span>TC</span></div>
        <div class="tile"><b>$wi_total</b><span>Work items</span></div>
        <div class="tile"><b>$workstreams</b><span>Workstreams</span></div>
      </div>
    </section>

    <nav class="tabs" role="tablist" aria-label="Dashboard views">
      <button class="active" role="tab" id="tab-arch" data-tab="arch" aria-controls="arch" aria-selected="true" tabindex="0">What (SR breakdown)</button>
      <button role="tab" id="tab-dag" data-tab="dag" aria-controls="dag" aria-selected="false" tabindex="-1">When (roadmap DAG)</button>
      $extra_tabs
    </nav>

    <section id="arch" class="panel active" role="tabpanel" aria-labelledby="tab-arch">
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
      <div class="legend">$tier_legend</div>
    </section>

    <section id="dag" class="panel" role="tabpanel" aria-labelledby="tab-dag" hidden>
      <h2>Work-item trajectory</h2>
      <p class="cap">The dependency DAG from <code>docs/requirements/work-items.csv</code>,
      laid out left→right by <strong>dependency rank</strong> (a work item sits one
      column past its deepest hard predecessor). <strong>Solid edges block</strong>
      (hard dependencies); <strong>dashed edges are advisory ordering</strong> (soft,
      <code>~</code>-prefixed — they never gate readiness). Cross-workstream edges are
      the seams. $dag_interaction Plain SVG — no libraries, fully
      offline.</p>
      <div class="layout">
        $scroll_cue
        <div id="dag-view" class="view" tabindex="0" role="group"
             aria-label="Work-item trajectory graph, horizontally scrollable">$dag_svg</div>
        <aside id="dag-detail" class="detail"><p class="hint">Click a work item to read its
          detail — workstream, status, the SRs it delivers, its predecessors.</p></aside>
      </div>
      <div class="legend">
        <span><i style="background:var(--done)"></i>✓ done</span>
        <span><i style="background:var(--active)"></i>● active — you are here</span>
        <span><i style="background:var(--queued)"></i>not started — ○ queued (ready),
          ✎ draft (still being figured out), ◌ deferred (parked by choice),
          ⊘ blocked (has an impediment)</span>
        <span><i style="background:var(--cancelled)"></i>⊗ cancelled — won't build (terminal)</span>
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
        '<span class="badge" style="background:'+tierColor+';color:'+(tierColor===statusColor.queued?'#0f172a':'#fff')+'">'+esc(d.tier||d.status)+'</span>'
        + '<h3>'+esc(id)+(d.title?' — '+esc(d.title):'')+'</h3>'
        + (d.status&&d.tier?'<p class="status">'+esc(d.status)+'</p>':'')
        + '<p class="body">'+esc(d.body)+'</p>'
        + (d.meta?'<p class="meta">'+esc(d.meta)+'</p>':'');
    }
    /* A3 (WI-313 rework): these maps are SUBSTITUTED from TIER_FILL/STATUS_FILL,
       never hand-copied — the adversarial review found the previous literals
       kept a pre-WI-311 tc hex that had become the done-green, the same defect
       the static legend fix missed here. test_a3_js_detail_maps_mirror_the_
       declared_palettes holds them equal to the Python constants. */
    const tierColor = $tier_color_js;
    const statusColor = $status_color_js;

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
      c.addEventListener('click', () => renderDetail(iceBox, archDetails[id], id, tierColor[archDetails[id]?.tier]||tierColor.llr));
      c.addEventListener('focus', () => { iceHover(id); renderDetail(iceBox, archDetails[id], id, tierColor[archDetails[id]?.tier]||tierColor.llr); });
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
      n.addEventListener('click', () => renderDetail(dagBox, wiDetails[id], id, statusColor[wiDetails[id]?.status]||statusColor.queued));
      n.addEventListener('focus', () => { dagHover(id); renderDetail(dagBox, wiDetails[id], id, statusColor[wiDetails[id]?.status]||statusColor.queued); });
    }
    if(dag) dag.addEventListener('mouseleave', dagClear);
    // When roadmap (drill render): every block opens the SAME detail aside.
    // on single-click / focus. The `.wi` wiring above serves the small-registry SVG
    // DAG fallback; this serves the tiered drill (its blocks carry `data-wi`, and the
    // drill's own controller keeps dblclick=descend + hover=highlight). One selector
    // matches per render mode, so neither is a dead wiring for the artifact it renders.
    if(dag) for(const b of dag.querySelectorAll('.block[data-wi]')){
      const id = b.getAttribute('data-wi');
      const show = () => renderDetail(dagBox, wiDetails[id], id, statusColor[wiDetails[id]?.status]||statusColor.queued);
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

    // WI-273 (SR-052): the view switcher is a WAI-ARIA tablist, not a row of
    // styled buttons. selectTab keeps the three bits of state assistive tech
    // reads in sync — which tab is aria-selected, panel visibility (the .active
    // display class AND the hidden attribute), and the roving tabindex (only the
    // selected tab is in the tab sequence) — plus the visual .active class and
    // the overflow scroll cues. Keyboard: Left/Right and Up/Down move focus and
    // activate the tab; Home/End jump to the first/last; Enter/Space fall through
    // to the native <button> click. Automatic activation (arrow selects at once)
    // is safe because every panel is already in the DOM.
    const tablist = document.querySelector('nav.tabs');
    if(tablist){
      const tabs = [...tablist.querySelectorAll('[role=tab]')];
      const selectTab = (tab, moveFocus) => {
        for(const t of tabs){
          const on = t===tab;
          t.classList.toggle('active', on);
          t.setAttribute('aria-selected', on ? 'true' : 'false');
          t.tabIndex = on ? 0 : -1;
          const panel = document.getElementById(t.dataset.tab);
          if(panel){ panel.classList.toggle('active', on); panel.hidden = !on; }
        }
        if(moveFocus) tab.focus();
        syncScrollCues();
      };
      tablist.addEventListener('click', e => {
        const tab = e.target.closest('[role=tab]');
        if(tab) selectTab(tab, false);
      });
      tablist.addEventListener('keydown', e => {
        const i = tabs.indexOf(e.target);
        if(i < 0) return;
        let j;
        if(e.key==='ArrowRight' || e.key==='ArrowDown') j = (i+1) % tabs.length;
        else if(e.key==='ArrowLeft' || e.key==='ArrowUp') j = (i-1+tabs.length) % tabs.length;
        else if(e.key==='Home') j = 0;
        else if(e.key==='End') j = tabs.length-1;
        else return;
        e.preventDefault();
        selectTab(tabs[j], true);
      });
    }
  </script>
</body></html>
""")


def build_html(root, wis):
    total = len(wis)
    done = sum(1 for w in wis if w["status"] == "done")
    active = sum(1 for w in wis if w["status"] == "active")
    # WI-267: `cancelled` (terminal WON'T-BUILD) rows get their OWN count, never
    # folded into done. Surfaced on the execution hero only when present, so the
    # common no-cancellation dashboard sub-line is unchanged. The execution %
    # stays done/total — cancelled work was deliberately abandoned, not completed.
    cancelled = sum(1 for w in wis if w["status"] == "cancelled")
    wi_cancelled_clause = " · {} cancelled".format(cancelled) if cancelled else ""
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
    tiered_dag = when_view(root, wis)
    dag_view = tiered_dag or dag
    # WI-296: the interaction sentence must describe the emitter that ACTUALLY ran.
    # It used to promise "Hover a work item to highlight its neighbourhood"
    # unconditionally, but neighbourhood highlighting is the FLAT emitter's — the
    # controller walks `.wi`/`.edge` nodes only `dag_svg` produces. Above the >3 rule
    # the tiered drill view renders instead, where those node sets are empty and the
    # promise silently went unmet (117-CRITIQUE read the empty `.wi` set in THIS
    # repo's render as dead code; it is not — it is the small-project default, and the
    # flat path is what every freshly scaffolded downstream repo gets).
    dag_interaction = (
        "<strong>Double-click</strong> a container — or focus it and press Enter — "
        "to descend a layer, and the breadcrumb returns to any ancestor; "
        "<strong>click</strong> a work item for its detail."
        if tiered_dag
        else "<strong>Hover</strong> a work item to highlight its neighbourhood; "
        "<strong>click</strong> for its detail."
    )
    extra_tabs, extra_panels = [], []
    mods = sw_modules(root)
    # WI-455 (sitting-2 decision 8): the authored Runtime flows embed in the
    # How-SW panel, so the dashboard carries the FULL architecture — the
    # derived structure AND the narrative. "" when none are authored.
    flows_html = flows_block(runtime_flows(root))
    if mods:
        # WI-073: when a CMP layer contains modules, the How-SW panel becomes the
        # containerized top view (≤ ct.TOP_VIEW_MAX items, expandable); otherwise
        # it keeps today's flat graph/table (byte-identical for a no-CMP repo).
        tab, panel = sw_containment(root, mods) or _sw_panel(mods, sw_graph(root, mods))
        if flows_html:
            assert panel.endswith("</section>")
            panel = panel[: -len("</section>")] + flows_html + "\n</section>"
        extra_tabs.append(tab)
        extra_panels.append(panel)
    elif flows_html:
        # A files-mode / pre-code repo with authored flows still gets the How
        # tab: the narrative is architecture even before a symbol map exists.
        extra_tabs.append(tab_button("sw", "How (SW architecture)"))
        extra_panels.append(
            tab_panel_open("sw")
            + "\n<h2>Software architecture (How)</h2>\n"
            + flows_html
            + "\n</section>"
        )
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
        # LLR-052 `>3` type threshold, else renders the flat concept graph.
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

    # A3 (WI-313): the icicle tier legend derives from TIER_FILL rather than
    # restating it. The hardcoded spans this replaced kept a pre-WI-311 TC hex
    # (#047857) that had since become STATUS_FILL["done"] — a legend labelling
    # the done-green "TC" while the actual TC cells painted TIER_FILL["tc"].
    # Iterates the DICT (not a literal key tuple) so a new tier member cannot
    # be silently dropped from the legend — the adversarial-review finding.
    tier_legend = "".join(
        '<span><i style="background:{}"></i>{}</span>'.format(fill, tier.upper())
        for tier, fill in TIER_FILL.items()
    )
    return HTML_TEMPLATE.substitute(
        asof=html.escape(_asof(root)),
        tier_legend=tier_legend,
        tier_color_js=json.dumps(TIER_FILL),
        status_color_js=json.dumps(STATUS_FILL),
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
        wi_cancelled_clause=wi_cancelled_clause,
        wi_active_line=wi_active_line,
        next_work=_next_work_html(root),
        arch_svg=arch,
        arch_details=j(arch_details),
        arch_desc=j(arch_desc),
        dag_svg=dag_view,
        dag_interaction=dag_interaction,
        wi_details=j(wi_details),
        scroll_cue=SCROLL_CUE,
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
    ap.add_argument(
        "--status",
        action="store_true",
        help="splice the derived-facts snapshot (spine + derived gate + "
        "open-items one-liners) into docs/status.md instead of rendering the "
        "dashboard; with --check, byte-compare it for freshness (the WI-200 "
        "forward-only guard's successor). Vacuous without the marker pair. The "
        "pending-owner-actions projection moved to gen_open_items.py with "
        "WI-322 — this still DERIVES it (`pending_block`), that renders it.",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if args.status:
        # `--status` gates the status snapshot alone since WI-322: the
        # pending-owner-actions projection moved to the generated owner surface
        # docs/open-items.html (its own `open-items` harness step), because the
        # markdown file it used to splice into is retired. `pending_block` stays
        # here — it is still the ONE derivation of what is pending; gen_open_items
        # imports it rather than growing a second opinion.
        return traj_status.run_status(root, args.check)

    if not ct.read_trajectory_enabled(root):
        print(
            "gen_trajectory: off (docs/process.toml [checks] trajectory_check) "
            "— nothing to render."
        )
        return 0

    wis, integrity = ct.load_wis(ct.read_registry_rows(root / ct.WI_CSV))
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
