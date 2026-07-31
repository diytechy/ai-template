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
How-SW views + panels) — each re-exported here, so
`import gen_trajectory` stays the one consumer seam and the render is
byte-identical across the split.

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

# --- WI-280 split: the decomposed sibling modules ------------------------------
# The implementation lives in the split siblings — traj_graph.py (layout +
# wire routing), traj_parse.py (sources + the guarded `schedule` import's one
# home), traj_render.py (SVG/HTML primitives + the drill renderer),
# traj_views.py (the What/When/How-SW views + panels) — and this facade
# re-exports the consumer-read names so every existing `gen_trajectory.<name>`
# import keeps resolving (the seam, and its Contracts: line, stay HERE). These
# imports sit AFTER the guarded check_trajectory import above on purpose: that
# guard is this module's ONE sys.path repair, and the siblings rely on it when
# this file is loaded from outside scripts/ (the F5 self-heal contract).
import traj_views
import traj_render
import traj_parse
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
    schedule,
    spine_stats,
    sw_modules,
)
import traj_graph
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
    sw_containment,
    sw_graph,
    when_view,
)
from traj_graph import (  # noqa: F401
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

# --- the pending-owner-actions projection (WI-234) ------------------------------
# `--status` also splices a second GENERATED block — at the END of
# the generated owner surface docs/open-items.html (WI-322), beside the briefs
# leaves byte-untouched) — projecting every DURABLE pending-owner action so the
# owner's one review surface never misses a hard stop. A pure projection of
# committed-tree state ONLY:
#   (a) `blocked` WI rows carrying a BlockRef (the attestation/ratification
#       page);
#   (b) Draft/Modified SR rows (WI-316): a `Draft` SR owes a ratification, a
#       `Modified` SR owes a re-attest (post-attestation amendment, process.md
#       §7) — one pointer line each, naming the on-demand brief
#       (`trace.py --ratify <id>` / `--ratify modified`) that carries the depth.
#   (c) a tracked `docs/work/pause` (concurrency-restructure §5.6): one
#       `Paused since <date>` line, the declared reason rendered verbatim (no
#       clock), so an open pause is a visible accruing cost.
# One line per pending action with a pointer (never a brief — the depth stays in
# the hand-authored briefs). Deterministic (sorted rows, no clocks), so the
# gated region is byte-stable; a pure function of the committed tree, so the
# `--check` freshness gate byte-compares the WHOLE block in any clone. Opt-in:
# a repo carrying no open-items registry renders nothing.
# (The dispatcher-era MACHINE-LOCAL advisory region — refs/llm/* conflict/
# reservation/quarantine/stranded-train lines, excluded from the compare under
# M-10/WI-266 because those refs never transported — retired with the
# dispatcher at concurrency-restructure Phase 5, and the run-state ask source
# with it: git history and the integrator's own refusals are the record now.)

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
          ◌ deferred (parked by choice), ⊘ blocked (has an impediment)</span>
        <span><i style="background:var(--retired)"></i>⊗ retired — won't build (terminal)</span>
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
    out_off = _port_fan(out_groups, lambda e: e[1], pos, KN_ROW_H, KN_ROW_GAP)
    in_off = _port_fan(in_groups, lambda e: e[0], pos, KN_ROW_H, KN_ROW_GAP)

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
    if schedule is None:
        return ""
    try:
        wis = schedule.load_wis(
            schedule.load_registry_rows(root / "docs/requirements/work-items.csv")
        )
        records = schedule.evaluate(wis)
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
        wi_retired_clause=wi_retired_clause,
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
    """`[(OI-id, one-liner)]` for every PENDING decision, id-order — the status
    snapshot's one-line-per-item projection.

    Reads `docs/requirements/open-items.csv` (WI-322, OI-10 ruled option (b)):
    the registry is the source and `docs/open-items.html` is the rendered owner
    surface, so a markdown section parse has nothing left to parse. The
    one-liner is the row's `OneLine` cell, else the first sentence of its
    `Recommendation` — the same fallback the markdown contract had, kept so a
    row that states only a recommendation still projects something useful.
    Empty when the registry is absent (a repo carrying no decisions)."""
    p = root / "docs" / "requirements" / "open-items.csv"
    if not p.is_file():
        return []
    out = []
    for row in ct.read_rows(p):  # the shared reader — BOM-safe, one CSV idiom
        oid = (row.get("OI-ID") or "").strip()
        if not _OI_ID_RE.fullmatch(oid) or oid.endswith("-000"):
            continue
        if (row.get("Status") or "").strip().lower() != "pending":
            continue  # a ruled row is history; the Decisions log holds it
        one = (row.get("OneLine") or "").strip()
        if not one:
            reco = (row.get("Recommendation") or "").strip()
            one = _first_sentence(reco) if reco else ""
        out.append((oid, _clean_oneliner(one)))
    return sorted(out, key=lambda t: int(t[0].split("-")[1]))


# --- the pending-owner-actions projection sources (WI-234) ----------------------


def _blocked_pending(root):
    """Source (a): `(lines, ids)` — one line per blocked work item, and the set
    of WI ids covered. In the spec-folder registry blocked is DERIVED: a
    `queued/` item carrying a `blockref` key (concurrency-restructure §2.1 —
    `blocked` has no directory). The pointer is the BlockRef path."""
    wis, _ = ct.load_wis(ct.read_registry_rows(root / ct.WI_CSV))
    lines, ids = [], set()
    for w in sorted(wis, key=lambda w: w["id"]):
        if w["status"] != "queued" or not w["blockref"]:
            continue
        lines.append(
            "- **{}** blocked — attest/ratify `{}`, then unblock the registry "
            "row.".format(w["id"], w["blockref"])
        )
        ids.add(w["id"])
    return lines, ids


def _spine_pending(root):
    """Source (e), WI-316: one pointer line per `Draft` SR (ratification owed)
    and per `Modified` SR (re-attest owed — a post-attestation amendment,
    process.md §7). The SR is the attestation unit, so only SR rows project —
    a Modified LLR/TC rides its owning SR's line (trace.py's chain-consistency
    warn flags the orphaned-child case). Durable committed-tree state, so these
    join the freshness-gated PURE region; pointer-only per this block's charter
    — the depth (per-cell before/after) lives in the on-demand brief the line
    names, `trace.py --ratify modified`, never here. Sorted by id, no clocks."""
    # `skip_example=True`: a copied template's `-000` example row owes no
    # ratification. Only the SR arm projects (the attestation unit), so the
    # LLR/TC arms of the loader go unused here.
    srs = _spine(root, skip_example=True)[0]
    lines = []
    for r in sorted(srs, key=lambda x: x["SR-ID"]):
        status = (r.get("Status") or "").strip().lower()
        if status not in ("draft", "modified"):
            continue
        sid = r["SR-ID"]
        title = (r.get("Title") or "").strip() or "(untitled)"
        phase = (r.get("Phase") or "").strip()
        phase_note = " (phase {} pulls the derived gate)".format(phase) if phase else ""
        if status == "draft":
            lines.append(
                "- **{} `Draft` — ratification owed**{}: {} — ratify in a "
                "reviewed Status-change commit (`Draft`→`Planned`; the "
                "`gate-advance` skill); hierarchy brief: `python "
                "project-trajectory/scripts/trace.py --ratify {}`.".format(
                    sid, phase_note, title, sid
                )
            )
        else:
            lines.append(
                "- **{} `Modified` — re-attest owed**{}: {} — bless the "
                "amendment in a reviewed Status-change commit "
                "(`Modified`→`Verified`, or →`Planned` if the evidence no "
                "longer verifies the amended text); before/after brief: "
                "`python project-trajectory/scripts/trace.py --ratify "
                "modified` (a pre-regime streak — amendments that landed "
                "while the row stayed Verified — needs `--since <rev>`; "
                "committed briefs live in `docs/ratify/`).".format(
                    sid, phase_note, title
                )
            )
    return lines


# Byte-identical with `agent_common.PAUSE_MALFORMED`: the coordinator's reader
# and this projection must say the same thing about an unreadable pause file.
# Copied rather than imported — this module's ONE sanctioned sibling import is
# check_trajectory (see the header), and a renderer must not start depending on
# the coordinator layer for a string. `tests/test_gen_trajectory_pending.py`
# pins the two equal, so the copy cannot drift silently.
PAUSE_MALFORMED = "<malformed docs/work/pause — fix or delete it>"


def _pause_pending(root):
    """Source (f): the tracked pause declaration `docs/work/pause`
    (`docs/concurrency-restructure.md` §5.6) — TOML `reason` + `since`. Zero or
    one bullet, so an open pause is a VISIBLE accruing cost rather than a
    forgotten one (the stale-reason lesson); unpausing is a deletion commit, so
    the bullet clears itself.

    Committed-tree-PURE and deterministic: the declared `since` renders
    VERBATIM — never an age computed from `now()`, which would make the gated
    region change without a commit. Fail-CLOSED like the coordinator's reader: a
    malformed file still projects, loudly, because a pause you cannot read is
    still a pause. Where that reader NORMALIZES (its callers get a typed dict),
    this one only has to answer "readable or not" before formatting, so it asks
    once and catches — same outcomes, a renderer's shape."""
    import tomllib  # the module's only TOML reader; kept local to this one use

    p = root / "docs" / "work" / "pause"
    if not p.is_file():
        return []
    try:
        declared = tomllib.loads(p.read_text(encoding="utf-8"))
        reason, since = declared["reason"], declared.get("since") or ""
        if not isinstance(reason, str):
            raise TypeError("pause `reason` must be text")
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, TypeError):
        reason, since = PAUSE_MALFORMED, ""
    return [
        "- **Paused{}** — {}.".format(
            " since {}".format(since) if since else "",
            reason or "no reason declared",
        )
    ]


def pending_block(root):
    """The GENERATED PENDING block CONTENT (between the markers) for the
    generated owner surface: blocked WI rows with a BlockRef + Draft/Modified
    spine rows owing a ratification/re-attest + the tracked `docs/work/pause`
    declaration. A pure function of the committed tree — deterministic (sorted,
    no clocks) — so the harness `open-items` freshness gate byte-compares the
    WHOLE block through `gen_open_items.py --check` (the renderer since
    WI-322, NOT `--status`) and it reads identically in any clone. (The
    dispatcher-era machine-local advisory region retired with the dispatcher
    at concurrency-restructure Phase 5.)"""
    pure_lead = (
        "_Pending owner actions — a generated projection of durable, "
        "committed-tree state (blocked rows with a ratify/attest pointer, "
        "Draft/Modified spine rows owing a ratification or re-attest, and the "
        "tracked pause declaration); regenerated by `python "
        "project-trajectory/scripts/gen_trajectory.py --status`, do not hand-edit. "
        "This section is freshness-gated by the harness `status-map` step. The "
        "briefs above are hand-authored and untouched by regeneration._"
    )
    blocked_lines, _blocked_ids = _blocked_pending(root)
    pure_items = blocked_lines + _spine_pending(root) + _pause_pending(root)
    pure_body = (
        "\n".join(pure_items)
        if pure_items
        else "_None — no durable owner action is pending._"
    )
    return "{}\n\n{}".format(pure_lead, pure_body)


def status_block(root):
    """The GENERATED STATUS block CONTENT (between the markers) for docs/status.md:
    the derived gate + spine snapshot (projected from `docs/gate`, the freshness-
    guarded SSOT) plus the open-items one-liners (from the registry). Derived
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
            "- **Open items** _(pending rows of "
            "[requirements/open-items.csv](requirements/open-items.csv); each "
            "item's blast radius, options and recommendation render in "
            "[open-items.html](open-items.html), the generated owner surface):_"
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
        rows = schedule.load_registry_rows(root / "docs/requirements/work-items.csv")
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


def _title_clause(title):
    """The leading clause of a WI Title — the name of the work, before the
    rationale the registry cell carries after it."""
    return title.split(" - ")[0].split(" — ")[0].strip() or "(untitled)"


def _clip_title(title, limit=90):
    """First clause of a WI Title, clipped — the registry titles are long. The
    status.md frontier line still budgets by character (one markdown line, and
    status.md carries its own line budget); the dashboard card does not — see
    `_next_work_title`."""
    head = _title_clause(title)
    if len(head) > limit:
        head = head[: limit - 1].rstrip() + "…"
    return head


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
        return run_status(root, args.check)

    if not ct.read_trajectory_enabled(root):
        print("gen_trajectory: off (docs/trajectory-check) — nothing to render.")
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
