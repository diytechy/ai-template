"""gen_trajectory.py — the offline trajectory dashboard (Thread 52 phase 2).

The generator renders the root PROJECT_STATE.html from the work-item registry (the
`docs/work/` spec folder) + the spine as a
*view* (a design principle: text is truth). What matters is that it is fully
offline (no CDN), deterministic (so the --check freshness gate is byte-stable),
refuses to render an invalid registry, and stays vacuous when there is nothing to
show. Each is pinned by running the real script over a minimal temp project.
"""

import math
import re
import subprocess
import sys

import pytest
from conftest import ROOT, SCRIPTS, load_script
from traj_fixtures import (
    ARCH_MD,
    GOOD_WIS,
    _every_emitter_document,
    gen,
    html_of,
    make_repo,
    write_wis,
)


# --- renders a self-contained, offline dashboard -------------------------------


def test_generates_self_contained_dashboard(tmp_path):
    make_repo(tmp_path)
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (tmp_path / "PROJECT_STATE.html").exists()
    text = html_of(tmp_path)
    # both views present
    assert 'id="ice"' in text and 'id="dag"' in text
    # work items + spine ids rendered
    for wid in ("WI-001", "WI-002", "WI-003", "WI-004"):
        assert wid in text
    assert "SR-001" in text and "SN-001" in text and "LLR-001" in text
    assert "Stay correct over time" in text  # the vision header
    # execution meter: 1 of 4 done -> 25%
    assert "25%" in text
    # fully offline: no external hosts / CDN / external <script src>
    low = text.lower()
    assert "http://" not in low and "https://" not in low
    assert "<script src" not in low and "cdn" not in low
    # workstream tile (the renamed Track column) + the soft edge rendered dashed
    assert "Workstreams" in text
    assert 'class="edge soft"' in text
    assert "stroke-dasharray" in text


# WI-267: a `retired` (terminal WON'T-BUILD) WI gets its OWN dashboard bucket —
# a stone fill byte-distinct from done's green, the ⊗ glyph, a legend entry, and
# a separate count that is never folded into `done`.
RETIRED_WIS = GOOD_WIS + "WI-005,Abandoned idea,scripts,,,retired,superseded\n"


def test_retired_wi_renders_its_own_bucket(tmp_path):
    gt = load_script("gen_trajectory")
    # the retired fill is byte-distinct from every other status fill (not a
    # rename of done's green) — the render-legibility invariant.
    assert gt.STATUS_FILL["retired"] == "#78716c"
    assert len(set(gt.STATUS_FILL.values())) == len(gt.STATUS_FILL)
    make_repo(tmp_path, wis_body=RETIRED_WIS)
    assert gen(tmp_path).returncode == 0, "gen failed"
    text = html_of(tmp_path)
    # its own fill colour + the ⊗ glyph
    assert "#78716c" in text
    assert "⊗" in text
    # a legend entry naming the terminal state
    assert "retired — won't build" in text
    # counted SEPARATELY on the execution hero (never folded into done): 1 of 5
    # done -> 20%, plus a distinct "1 retired" clause.
    assert "20%" in text
    assert "1 retired" in text


def test_mobile_responsive_shell(tmp_path):
    """SR-038: the dashboard is usable on mobile viewports — the responsive
    shell markers must be present in the generated HTML (viewport meta,
    narrow-viewport single-column collapse, scrolling panels)."""
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert '<meta name="viewport" content="width=device-width' in text
    assert "@media (max-width:760px)" in text  # layout collapses to one column
    assert "overflow:auto" in text  # wide SVGs scroll inside their panel


def test_wide_views_carry_horizontal_scroll_affordance(tmp_path):
    """WI-219 (M-04, SR-052/SR-054): a view wider than the viewport must SIGNAL its
    off-screen content, not silently clip it at 390 px. Every horizontal-scroll
    container is a keyboard-focusable, labelled region (SR-052 keyboard/name) and
    carries a narrow-width scroll cue (SR-054 no truncation-without-affordance); no
    bare overflow wrapper survives."""
    make_repo(tmp_path)
    # architecture.md exercises the module-map table's scroll wrapper too, not just
    # the icicle / DAG SVG views.
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    # the cue is a real element, hidden by default, with the narrow breakpoint kept
    # as the no-JS fallback; WI-256 additionally reveals it whenever a container
    # ACTUALLY overflows (any width) so the fixed-width icicle / a wide drill layer
    # that clips at 1280/1680 signals its off-screen content, not just at 390.
    assert "↔ Scroll sideways to see the full view" in text
    assert ".scrollcue { display:none;" in text
    assert ".scrollcue{ display:block; }" in text  # inside @media (max-width:760px)
    assert ".scrollcue.cued { display:block; }" in text  # WI-256 overflow-driven cue
    # the JS toggles `.cued` from real overflow (scrollWidth vs clientWidth), and a
    # drill descend re-syncs the new layer via the exposed hook.
    assert "scrollWidth" in text and "clientWidth" in text
    assert "window.__syncCues" in text
    # the graph views are focusable, named scroll regions (SR-052 A1/A2)
    assert 'id="ice" class="view" tabindex="0" role="group"' in text
    assert 'aria-label="Architecture icicle, horizontally scrollable"' in text
    assert 'id="dag-view" class="view" tabindex="0" role="group"' in text
    # the module-map table's overflow wrapper is a labelled region too, not a bare
    # div whose scrollbar auto-hides on mobile.
    assert '<div class="tablescroll" tabindex="0" role="group"' in text
    assert 'style="overflow:auto"' not in text  # no un-affordanced scroll wrapper
    # focus on the region is perceivable (keyboard operability made visible)
    assert ".view:focus-visible" in text


def test_clip_edge_marker_is_gated_on_actual_overflow(tmp_path):
    """080-CRITIQUE #3 (WI-258): the scroll cue is a caption ABOVE the card, so the
    clip edge itself went unmarked — a clipped header stayed invisible until the
    reader scrolled. A `.clipr` right-edge fade now marks the point of cut, driven by
    the SAME actual-overflow measure as `.cued` (scrollWidth vs clientWidth) and
    cleared at the right end — present for an overflowing card, absent for a fitting
    one, and never unconditional on the card itself."""
    make_repo(tmp_path)
    # exercise the table scroller (.tablescroll) too, not just the SVG cards
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    # the edge marker is a right-edge fade gated on the `.clipr` class, on both the
    # SVG cards and the table scrollers
    assert ".view.clipr" in text and ".tablescroll.clipr" in text
    assert "mask-image: linear-gradient(to left" in text
    # it is CONDITIONAL — the base card rule never masks, so a fitting card shows none
    base_view = re.search(r"\.view \{[^}]*\}", text).group(0)
    assert "mask-image" not in base_view
    # the class is toggled from the SAME actual-overflow signal `.cued` uses, so it is
    # present only when the card overflows (and cleared once scrolled to the end)
    m = re.search(r"classList\.toggle\('clipr',([^;]+);", text)
    assert m, "no .clipr toggle emitted"
    assert "scrollWidth" in m.group(1) and "clientWidth" in m.group(1)
    # the fade tracks scroll position so it clears at the true right end, not forever
    assert "addEventListener('scroll'" in text


def test_drill_focus_ring_is_distinct_from_the_active_accent(tmp_path):
    """080-CRITIQUE #5 (WI-258): the drill keyboard-focus ring used #b45309 — byte-
    identical to the `active — you are here` status accent (--active) — so a focused-
    but-not-active block misread as active. The focus + persistent-highlight ring must
    paint a colour clearly distinct from the active accent in BOTH themes. WI-294a/
    WI-299 layered a per-node `--ring` property on top (a static hue can't clear 3:1
    against every fill), keeping `var(--accent)` as the CSS fallback — so the CSS
    RULE now reads `var(--ring,var(--accent))`; the fallback is what this test's
    active/accent distinctness still applies to."""
    gt = load_script("gen_trajectory")
    active = gt.STATUS_FILL[
        "active"
    ]  # #b45309 — the value --active / the legend paints
    assert active == "#b45309"
    # the drill focus + last-highlight strokes no longer paint the active hue
    strokes = re.findall(
        r"\.drill \.block(?::focus rect|\.hl rect)\{stroke:([^;]+);", gt.DRILL_STYLE
    )
    assert len(strokes) == 2, strokes
    for stroke in strokes:
        assert stroke != active, stroke
        assert stroke == "var(--ring,var(--accent))", stroke
    # resolve --accent (light :root + dark media) and --active from the emitted CSS,
    # and confirm the focus hue is clearly distinct from active in BOTH themes
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    active_tok = re.search(r"--active:(#[0-9a-f]{6})", css).group(1)
    accents = re.findall(r"--accent:(#[0-9a-f]{6})", css)
    assert active_tok == active
    assert len(accents) == 2, accents  # one per theme: light :root + dark media
    for accent in accents:
        assert accent != active_tok
        # a different hue, not a near-shade of the same orange (sum of channel deltas)
        d = sum(
            abs(int(accent[i : i + 2], 16) - int(active_tok[i : i + 2], 16))
            for i in (1, 3, 5)
        )
        assert d > 150, (accent, active_tok, d)


def test_generation_is_deterministic(tmp_path):
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    second = gen(tmp_path)
    assert second.returncode == 0
    assert "already up to date" in second.stdout  # unchanged -> not rewritten
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first


def test_dag_layers_by_dependency_rank(tmp_path):
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    dag = (
        html_of(tmp_path)
        .split('id="dag-view" class="view"', 1)[1]
        .split("</svg>", 1)[0]
    )
    xs = {
        m.group(1): float(m.group(2))
        for m in re.finditer(
            # each node <g> now carries a <title> tooltip child before its <rect>
            r'data-id="(WI-\d+)"[^>]*>(?:<title>[^<]*</title>)?<rect x="([\d.]+)"',
            dag,
        )
    }
    # the root sits left of its successors; the sink sits right of them.
    assert xs["WI-001"] < xs["WI-002"] < xs["WI-004"]
    assert xs["WI-001"] < xs["WI-003"] < xs["WI-004"]
    # WI-003's soft (~WI-002) edge is advisory: it must NOT deepen WI-003's rank
    assert xs["WI-002"] == xs["WI-003"]


def test_renders_without_readme_uses_fallbacks(tmp_path):
    # No README -> the vision/name fall back rather than crash.
    make_repo(tmp_path, readme=False)
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (tmp_path / "PROJECT_STATE.html").exists()


# --- the --check freshness gate ------------------------------------------------


def test_check_passes_fresh_and_trips_stale(tmp_path):
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    fresh = gen(tmp_path, "--check")
    assert fresh.returncode == 0 and "up to date" in fresh.stdout
    # edit the registry without regenerating -> the committed HTML is stale.
    write_wis(tmp_path, GOOD_WIS + "WI-005,More,scripts,SR-001,WI-004,queued,d\n")
    stale = gen(tmp_path, "--check")
    assert stale.returncode == 1 and "STALE" in stale.stderr
    # regenerating restores freshness.
    assert gen(tmp_path).returncode == 0
    assert gen(tmp_path, "--check").returncode == 0


def test_check_missing_html_is_stale(tmp_path):
    # Real work items but no generated HTML yet must FAIL --check (not vacuous),
    # so CI catches a repo that forgot to commit its dashboard.
    make_repo(tmp_path)
    proc = gen(tmp_path, "--check")
    assert proc.returncode == 1 and "STALE" in proc.stderr


# --- vacuous / opt-out / invalid -----------------------------------------------


def test_placeholder_only_renders_nothing(tmp_path):
    make_repo(tmp_path, "WI-000,EXAMPLE - delete,track,SR-000,,queued,demo\n")
    proc = gen(tmp_path)
    assert proc.returncode == 0
    assert not (tmp_path / "PROJECT_STATE.html").exists()
    assert gen(tmp_path, "--check").returncode == 0  # vacuously fresh


def test_opt_out_silences(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "docs" / "trajectory-check").write_text("off\n", encoding="utf-8")
    proc = gen(tmp_path, "--check")
    assert proc.returncode == 0 and "off" in proc.stdout
    assert not (tmp_path / "PROJECT_STATE.html").exists()


def test_asof_stamp_from_git_and_excluded_from_check(tmp_path):
    # WI-039: the as-of line derives from the last source-touching COMMIT
    # (never now(), so generation stays deterministic), is visible in the
    # shell, and is excluded from the --check byte-compare — a stamp-only
    # difference (the artifact committed one commit behind its sources' last
    # touch) must not read as stale.
    import subprocess

    make_repo(tmp_path)

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(tmp_path), *args], capture_output=True, text=True
        )

    git("init")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "T")
    git("add", "-A")
    git("commit", "-q", "-m", "sources")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'class="asof">state as of commit ' in text
    # Simulate the artifact carrying a previous stamp: content equal, stamp not.
    (tmp_path / "PROJECT_STATE.html").write_text(
        re.sub(
            r'(class="asof">state as of commit )[0-9a-f]+',
            r"\g<1>0000000",
            text,
        ),
        encoding="utf-8",
    )
    proc = gen(tmp_path, "--check")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_no_git_means_no_stamp_and_stays_deterministic(tmp_path):
    # Outside a git repo the stamp is simply absent — no crash, no wall clock.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    assert 'class="asof"></p>' in html_of(tmp_path)


# --- F5: the sanctioned sibling import loads in-process too ---------------------


def test_load_script_resolves_sibling_import_in_process():
    # gen_trajectory imports its sibling check_trajectory. Loading it the
    # in-process way (importlib via the suite's load_script — the first script to
    # need it) must resolve that import, not raise a bare ImportError: the trap
    # the next in-process test author would otherwise fall into (F5).
    gt = load_script("gen_trajectory")
    assert gt.ct is not None
    assert hasattr(gt.ct, "validate")  # the sibling is genuinely wired


def test_gen_trajectory_self_heals_sibling_import(monkeypatch):
    # The guarded import's OWN fallback (independent of the conftest shim): with
    # scripts/ off sys.path and the sibling not yet imported — the downstream
    # cherry-pick / import-from-elsewhere case — the module must still add its own
    # directory and resolve check_trajectory rather than raise ImportError (F5).
    import importlib.util
    import sys

    monkeypatch.delitem(sys.modules, "check_trajectory", raising=False)
    monkeypatch.delitem(sys.modules, "gen_trajectory", raising=False)
    monkeypatch.setattr(sys, "path", [p for p in sys.path if p != str(SCRIPTS)])
    spec = importlib.util.spec_from_file_location(
        "gen_trajectory", SCRIPTS / "gen_trajectory.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # exercises the except-branch; must not raise
    assert mod.ct is not None


# --- F4: the layout recursion is iterative — correct + crash-proof --------------


def test_dag_ranks_longest_path_and_deep_chain():
    # (a) correctness on a diamond: a node's rank is one past its DEEPEST
    # predecessor. (b) a chain far deeper than the recursion limit ranks by pure
    # iteration — the former recursive longest-path raised RecursionError.
    gt = load_script("gen_trajectory")
    wis = [{"id": i} for i in ("A", "B", "C", "D")]
    pred = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}
    assert gt._dag_ranks(wis, pred) == {"A": 0, "B": 1, "C": 1, "D": 2}
    # deepest-first orientation (node k depends on k+1) so the walk descends the
    # full chain from wis[0] — the shape that overflowed the old recursion.
    n = 5000
    chain = [{"id": str(k)} for k in range(n)]
    cpred = {str(k): ([str(k + 1)] if k < n - 1 else []) for k in range(n)}
    cranks = gt._dag_ranks(chain, cpred)
    assert cranks["0"] == n - 1  # one past a 4999-long predecessor path
    assert cranks[str(n - 1)] == 0  # the source


def test_deep_chain_renders_without_recursionerror(tmp_path):
    # End-to-end (validate -> layout -> HTML) over a chain deeper than the
    # recursion limit completes and writes the dashboard.
    n = 1500
    body = "".join(
        "WI-{:04d},step,scripts,SR-001,{},queued,d\n".format(
            k, "WI-{:04d}".format(k + 1) if k < n else ""
        )
        for k in range(1, n + 1)
    )
    make_repo(tmp_path, body)
    proc = gen(tmp_path)
    assert "RecursionError" not in proc.stderr, proc.stderr
    assert proc.returncode == 0, (proc.stdout + proc.stderr)[:2000]
    text = html_of(tmp_path)
    assert "WI-0001" in text and "WI-{:04d}".format(n) in text


# --- WI-253: obstacle-aware wire routing (T8 — edge routing legibility) ----------
# The layered emitters route a wire that would cut an unrelated node box around it
# (a clear horizontal lane), so no edge reads as connected to a box it merely
# crosses, and crossings fall in open space rather than under labels / port fans.


def _sample_path_d(d, n=48):
    """A path `d` of M / L / C commands -> a polyline (the same cubic sampling the
    router's own hit-test uses), so a test can assert what a viewer's eye follows."""
    toks = re.findall(r"[MLC]|-?[\d.]+", d)
    pts, i, cur = [], 0, None
    while i < len(toks):
        c = toks[i]
        i += 1
        if c in "ML":
            cur = (float(toks[i]), float(toks[i + 1]))
            i += 2
            pts.append(cur)
        elif c == "C":
            p1 = (float(toks[i]), float(toks[i + 1]))
            p2 = (float(toks[i + 2]), float(toks[i + 3]))
            e = (float(toks[i + 4]), float(toks[i + 5]))
            i += 6
            gt = load_script("gen_trajectory")
            pts.extend(gt._cubic_points(cur, p1, p2, e, n)[1:])
            cur = e
    return pts


def _polyline_crosses(pts, rect):
    gt = load_script("gen_trajectory")
    return any(
        gt._seg_hits_rect(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], rect)
        for i in range(len(pts) - 1)
    )


def test_route_edges_detours_around_a_blocking_box():
    # A → C spans three columns with B centred between them; the straight wire at
    # B's row would cut B's box. The router must re-route around it (a lane detour),
    # and the routed path must clear B by the sampled polyline a viewer follows.
    gt = load_script("gen_trajectory")
    rects = {
        "A": (0.0, 100.0, 100.0, 40.0),
        "B": (200.0, 100.0, 100.0, 40.0),
        "C": (400.0, 100.0, 100.0, 40.0),
    }
    edges = [("A->C", 100.0, 120.0, 400.0, 120.0, "A", "C")]
    routes = gt._route_edges(edges, rects, 12, 2)
    d = routes["A->C"]
    assert "L" in d  # a detour, not the straight legacy cubic
    assert not _polyline_crosses(_sample_path_d(d), rects["B"])  # clears the box


def test_route_edges_leaves_a_clear_wire_byte_identical():
    # A → B is adjacent with nothing between: the router keeps the exact legacy
    # cubic (byte-for-byte), so the many clean in-column wires — and every
    # downstream render — are unchanged by the WI-253 routing.
    gt = load_script("gen_trajectory")
    rects = {"A": (0.0, 100.0, 100.0, 40.0), "B": (200.0, 100.0, 100.0, 40.0)}
    routes = gt._route_edges(
        [("A->B", 100.0, 120.0, 200.0, 120.0, "A", "B")], rects, 12, 2
    )
    dx = max((200.0 - 100.0) * 0.4, 12)
    xe = 200.0 - 2
    legacy = "M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}".format(
        100.0, 120.0, 100.0 + dx, 120.0, xe - dx, 120.0, xe, 120.0
    )
    assert routes["A->B"] == legacy
    assert "L" not in routes["A->B"]


def test_route_edges_reroutes_a_backward_seam():
    # A consumer→producer (right→left) seam used to sweep the whole width straight
    # through every box; the router lanes it around instead. C (right) → A (left)
    # past the intermediate B must clear B.
    gt = load_script("gen_trajectory")
    rects = {
        "A": (0.0, 100.0, 100.0, 40.0),
        "B": (200.0, 100.0, 100.0, 40.0),
        "C": (400.0, 100.0, 100.0, 40.0),
    }
    routes = gt._route_edges(
        [("C->A", 500.0, 120.0, 0.0, 120.0, "C", "A")], rects, 12, 2
    )
    d = routes["C->A"]
    assert "L" in d
    assert not _polyline_crosses(_sample_path_d(d), rects["B"])


def test_route_edges_stub_corridor_box_not_through_box():
    # 110-REVIEW-A MINOR (WI-255): a box overlapping ONLY a port-stub corridor
    # (within 18px of a port) was dropped from the lane search, so a direct cubic
    # that hit it was silently kept — a fail-open through-box. `S` sits in A's
    # output-stub corridor (x 104..118, x1=100); the straight legacy cubic cuts it,
    # so the router MUST re-verify the full routed polyline and detour around it.
    gt = load_script("gen_trajectory")
    rects = {
        "A": (0.0, 100.0, 100.0, 40.0),
        "S": (104.0, 120.0, 14.0, 70.0),
        "C": (400.0, 180.0, 100.0, 40.0),
    }
    edge = ("A->C", 100.0, 120.0, 400.0, 200.0, "A", "C")
    # the scenario is real: the direct cubic the router first tries cuts `S`.
    xe, dx = 400.0 - 2, max((400.0 - 100.0) * 0.4, 12)
    direct = gt._cubic_points(
        (100.0, 120.0), (100.0 + dx, 120.0), (xe - dx, 200.0), (xe, 200.0)
    )
    assert _polyline_crosses(direct, rects["S"])  # a through-box if kept
    d = gt._route_edges([edge], rects, 12, 2)["A->C"]
    assert "L" in d  # detoured, not the silent through-box cubic
    assert not _polyline_crosses(_sample_path_d(d), rects["S"])  # clears the box


def test_routed_label_rides_a_detoured_edge():
    # 110-REVIEW-A MINOR (WI-255): a detoured swedge's label used to anchor to the
    # straight-chord midpoint and float off its wire. It must ride the routed lane;
    # a clear (direct-cubic) edge keeps the chord-midpoint fallback byte-for-byte.
    gt = load_script("gen_trajectory")
    detour = (
        "M100.0,120.0 C109.0,120.0 109.0,112.9 118.0,112.9 "
        "L380.0,112.9 C389.0,112.9 389.0,200.0 398.0,200.0"
    )
    lx, ly = gt._routed_label_xy(detour, 999.0, 888.0)
    assert (lx, ly) == (249.0, 112.9)  # lane midpoint ((118+380)/2, 112.9)
    straight = "M100.0,120.0 C112.0,120.0 386.0,200.0 398.0,200.0"
    assert gt._routed_label_xy(straight, 999.0, 888.0) == (999.0, 888.0)


# --- WI-320 / SR-054 T8: the through-box rule, swept over what actually ships --
# 121-CRITIQUE's MAJOR is the first finding ever to land on T8, and only half of it
# is measurable. The row's split: bind the objective floor — NO edge passes through
# an unrelated node box — before anyone re-routes the layout for the lane
# separation the critic also asked for. The unit tests above prove the ROUTER on
# synthetic geometry; this proves the ARTIFACT, which is a different claim: the
# router returns a least-bad fallback when it cannot find a clear lane, so "the
# algorithm detours" does not imply "nothing shipped through a box".
_WIRE_RE = re.compile(r'<path class="wire[^"]*" d="([^"]*)"')
_NODE_RE = re.compile(
    r'<g class="(?:block|wi)\b[^>]*?(?:data-node|data-id)="([^"]*)".*?'
    r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="([\d.]+)"',
    re.S,
)


def _endpoint_of(point, rect, pad):
    return (
        rect[0] - pad <= point[0] <= rect[0] + rect[2] + pad
        and rect[1] - pad <= point[1] <= rect[1] + rect[3] + pad
    )


def test_t8_no_wire_passes_through_an_unrelated_node_box(tmp_path):
    gt = load_script("gen_trajectory")
    pad = gt.PORT_R + 4.0  # a wire legitimately starts/ends ON its own port circle
    swept = detoured = 0
    through = []
    for label, doc in _every_emitter_document(tmp_path):
        for svg in re.findall(r"<svg\b.*?</svg>", doc, re.S):
            nodes = [
                (m.group(1), tuple(float(m.group(k)) for k in (2, 3, 4, 5)))
                for m in _NODE_RE.finditer(svg)
            ]
            if not nodes:
                continue
            for d in _WIRE_RE.findall(svg):
                pts = _sample_path_d(d)
                if len(pts) < 2:
                    continue
                swept += 1
                detoured += "L" in d
                for nid, rect in nodes:
                    if _endpoint_of(pts[0], rect, pad) or _endpoint_of(
                        pts[-1], rect, pad
                    ):
                        continue  # its own source / target box
                    if _polyline_crosses(pts, rect):
                        through.append((label, nid, rect, d[:70]))
                        break
    assert swept, "vacuous - no wires emitted anywhere in the sweep"
    # Non-vacuity with teeth: the rule must actually be under load. If nothing
    # needed re-routing, a broken router would pass this sweep unnoticed.
    assert detoured, "vacuous - no wire in the sweep had to route around anything"
    assert not through, "wire(s) through an unrelated box: {}".format(through[:4])


def test_route_edges_terminals_snap_to_port_circle():
    # 079-CRITIQUE (WI-256): a fanned wire (its passed port y offset from the block
    # mid-height for strand separation) used to TERMINATE at cy+offset, so a steep
    # strand landed on a block corner, not its port circle. Terminals now snap to
    # the rect center; the fan offset lives in the control point (the wire still
    # bows). Holds for both the direct cubic and the detour.
    gt = load_script("gen_trajectory")
    direct = gt._route_edges(
        [("A->C", 100.0, 108.0, 200.0, 132.0, "A", "C")],
        {"A": (0.0, 100.0, 100.0, 40.0), "C": (200.0, 100.0, 100.0, 40.0)},
        12,
        2,
    )["A->C"]
    dn = [float(t) for t in re.findall(r"-?[\d.]+", direct)]
    assert dn[1] == 120.0 and dn[-1] == 120.0  # terminals on the port centers
    assert 108.0 in dn and 132.0 in dn  # the fan offset survives in the controls
    detour = gt._route_edges(
        [("A->C", 100.0, 108.0, 400.0, 132.0, "A", "C")],
        {k: (i * 200.0, 100.0, 100.0, 40.0) for i, k in enumerate("ABC")},
        12,
        2,
    )["A->C"]
    tn = [float(t) for t in re.findall(r"-?[\d.]+", detour)]
    assert "L" in detour and tn[1] == 120.0 and tn[-1] == 120.0


# --- WI-366: the port harness (WI-323-CRITIQUE follow-up 1) ---------------------
# The fan offset used to live only in a control point, so strands of one port left
# the same pixel and whatever lane the router then picked decided how close they
# ran — the critique pixel-measured 2.5-3 CSS px pitch over a ~55 px descent and
# 0.07 px at the tightest site. The pure geometry below is what makes the fan step
# the RENDERED pitch; the perceptual half of the claim stays with the before/after
# shots and the periodic advisory critique (no crossing-count proxy, standing rule).


def _first_clear(pa, pb, target, limit=60.0):
    """The arclength along `pa` at which it first gets `target` px clear of polyline
    `pb`, or None within `limit` — the departure-zone measure the critique's
    "reach >= 8 px within ~15 px of the port" clause states."""
    acc = 0.0
    for p, q in zip(pa, pa[1:]):
        acc += math.dist(p, q)
        if acc > limit:
            return None
        near = min(_seg_pt_dist(q, b0, b1) for b0, b1 in zip(pb, pb[1:]))
        if near >= target:
            return acc
    return None


def _seg_pt_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    span = dx * dx + dy * dy
    t = (
        0.0
        if span == 0
        else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / span))
    )
    return math.dist(p, (a[0] + t * dx, a[1] + t * dy))


def test_port_fan_steps_by_the_declared_pitch():
    # The fan STEP is the rendered pitch now (the harness materializes it), so it must
    # be `_FAN_PITCH` whenever the row slot can hold the whole band, and a single-edge
    # port must still get exactly 0.0 (that is what keeps unfanned wires byte-stable).
    gt = load_script("gen_trajectory")
    pos = {n: (0.0, float(i) * 10) for i, n in enumerate("abcdefghij")}
    for n in range(2, 6):
        names = "abcdefghij"[:n]
        group = {"src": [("src", t) for t in names]}
        off = gt._port_fan(group, lambda e: e[1], pos, 46.0, 22.0)
        band = sorted(off.values())
        steps = [round(b - a, 6) for a, b in zip(band, band[1:])]
        assert steps == [gt._FAN_PITCH] * (n - 1), (n, steps)
        assert round(sum(band), 6) == 0.0  # centred on the port
    lone = gt._port_fan({"src": [("src", "a")]}, lambda e: e[1], pos, 46.0, 22.0)
    assert lone[("src", "a")] == 0.0


def test_port_fan_band_stays_inside_its_row_slot():
    # The cap is the row SLOT minus one pitch: a wider band would put the outermost
    # strand of one port within a pitch of its vertical neighbour's, trading a fused
    # fan for a fused pair BETWEEN fans. A port too crowded for the slot steps tighter
    # instead of overflowing.
    gt = load_script("gen_trajectory")
    pos = {n: (0.0, float(i) * 10) for i, n in enumerate(range(40))}
    row_h, row_gap = 46.0, 22.0
    for n in (2, 5, 9, 20):
        group = {"src": [("src", t) for t in range(n)]}
        band = sorted(gt._port_fan(group, lambda e: e[1], pos, row_h, row_gap).values())
        assert band[-1] - band[0] <= row_h + row_gap - gt._FAN_PITCH
        gap = band[-1] - band[0]
        # ...and two adjacent ports' outermost strands still clear one pitch
        assert (row_h + row_gap) - gap >= gt._FAN_PITCH


def test_lead_rung_turns_the_furthest_traveller_off_first():
    # Order matters as much as the stagger: the strand diving furthest must leave the
    # harness while the others are still coasting, or it crosses every strand it is
    # inboard of. Up to `_LEAD_RUNGS` wires every neighbouring pair lands on a
    # DIFFERENT rung (that is what gives a steep pair a horizontal gap); past it the
    # cap collapses the LEAST-travelled end, and the rungs stay bounded.
    gt = load_script("gen_trajectory")
    n = gt._LEAD_RUNGS
    down = [gt._lead_rung(k, n, True) for k in range(n)]
    up = [gt._lead_rung(k, n, False) for k in range(n)]
    assert down[-1] == 0 and up[0] == 0  # the furthest traveller turns off first
    assert down == sorted(down, reverse=True) and up == sorted(up)
    for row in (down, up):
        assert all(a != b for a, b in zip(row, row[1:]))
        assert max(row) <= gt._LEAD_RUNGS - 1
    wide = [gt._lead_rung(k, 12, True) for k in range(12)]
    assert max(wide) == gt._LEAD_RUNGS - 1  # capped, so the harness stays bounded
    # the collapsed strands are the LEAST-travelled ones (rung 0 = furthest, kept
    # distinct); the shallow end shares the innermost turn-off.
    assert wide[-gt._LEAD_RUNGS :] == list(range(gt._LEAD_RUNGS - 1, -1, -1))
    assert set(wide[: -gt._LEAD_RUNGS]) == {gt._LEAD_RUNGS - 1}


def test_route_edges_harness_reaches_the_fan_pitch_near_the_port():
    # The measured defect, reproduced: two wires out of ONE port whose targets sit far
    # apart vertically, so the router lanes them both and the port-side bends used to
    # dominate the fan offset. Both strokes must get `_FAN_PITCH` clear of each other
    # within ~15px of the port, and each must still START on the port center.
    gt = load_script("gen_trajectory")
    rects = {
        "A": (0.0, 300.0, 100.0, 46.0),
        "B": (200.0, 300.0, 100.0, 46.0),
        "T1": (400.0, 60.0, 100.0, 46.0),
        "T2": (400.0, 540.0, 100.0, 46.0),
    }
    off = gt._port_fan(
        {"A": [("A->T1", "T1"), ("A->T2", "T2")]},
        lambda e: e[1],
        {"T1": (400.0, 60.0), "T2": (400.0, 540.0)},
        46.0,
        22.0,
    )
    edges = [
        (k, 100.0, 323.0 + off[(k, t)], 400.0, rects[t][1] + 23.0, "A", t)
        for k, t in (("A->T1", "T1"), ("A->T2", "T2"))
    ]
    routes = gt._route_edges(edges, rects, 14, 6.5)
    pts = {k: _sample_path_d(d, 96) for k, d in routes.items()}
    for d in routes.values():
        assert d.startswith("M100.0,323.0 ")  # still leaves the port CENTER
    a, b = pts["A->T1"], pts["A->T2"]
    for pa, pb in ((a, b), (b, a)):
        s = _first_clear(pa, pb, gt._FAN_PITCH - 0.1)
        assert s is not None and s <= 16.0, s
    # and the strands do NOT cross each other inside the harness (the failure mode a
    # stagger in the wrong order introduces)
    assert all((p[1] < 323.0) == (a[8][1] < 323.0) for p in a[8:24])


def test_route_edges_single_wire_port_keeps_the_legacy_path():
    # Only a SHARED port owes a harness. A one-wire port keeps the exact legacy `d`,
    # which is what holds the many unfanned wires — and every downstream render —
    # byte-identical across this change.
    gt = load_script("gen_trajectory")
    rects = {"A": (0.0, 100.0, 100.0, 40.0), "B": (200.0, 100.0, 100.0, 40.0)}
    lone = gt._route_edges(
        [("A->B", 100.0, 120.0, 200.0, 120.0, "A", "B")], rects, 12, 2
    )
    dx = max((200.0 - 100.0) * 0.4, 12)
    assert lone[
        "A->B"
    ] == "M{:.1f},{:.1f} C{:.1f},{:.1f} {:.1f},{:.1f} {:.1f},{:.1f}".format(
        100.0, 120.0, 100.0 + dx, 120.0, 198.0 - dx, 120.0, 198.0, 120.0
    )
    shared = gt._route_edges(
        [
            ("A->B1", 100.0, 116.0, 200.0, 116.0, "A", "B"),
            ("A->B2", 100.0, 124.0, 200.0, 124.0, "A", "B"),
        ],
        rects,
        12,
        2,
    )
    for d in shared.values():  # two cubics: the harness plus the routed remainder
        assert d.count("C") >= 2 and d.startswith("M100.0,120.0 ")


def test_route_edges_lane_routes_a_backward_edge_with_only_endpoint_obstacles():
    # 080-CRITIQUE follow-up #1 (WI-257): a BACKWARD edge (target input port at or
    # left of the source output port) whose ONLY obstacles are its own endpoint
    # boxes used to keep the direct cubic — which doubles back and dives UNDER both
    # boxes, so the wire reads as sprouting from a box edge and is untraceable
    # end-to-end (When 1→unphased / unphased→2..4, How-SW CMP-001→CMP-004). It is
    # now lane-routed around a visible detour lane. A (source, top) and B (target,
    # below) are stacked in one column with NOTHING between them.
    gt = load_script("gen_trajectory")
    rects = {"A": (0.0, 100.0, 120.0, 40.0), "B": (0.0, 200.0, 120.0, 40.0)}
    edge = ("A->B", 120.0, 120.0, 0.0, 220.0, "A", "B")  # out-port right, in-port left
    d = gt._route_edges([edge], rects, 12, 2)["A->B"]
    assert " L" in d  # lane-routed, not the kept-direct cubic (bites on revert)
    # the kept-direct cubic (pre-WI-257) dived through the TARGET box body...
    xe, dx = 0.0 - 2, max((0.0 - 120.0) * 0.4, 12)
    direct = gt._cubic_points(
        (120.0, 120.0), (120.0 + dx, 120.0), (xe - dx, 220.0), (xe, 220.0)
    )
    assert _polyline_crosses(direct, rects["B"])  # the "dives beneath" defect
    # ...the lane-routed wire clears it, so the wire is traceable end-to-end.
    assert not _polyline_crosses(_sample_path_d(d), rects["B"])
    dn = [float(t) for t in re.findall(r"-?[\d.]+", d)]
    assert dn[1] == 120.0 and dn[-1] == 220.0  # terminals still snap to port centers


# --- WI-367: the viewBox holds the wrap-around lanes (WI-323-CRITIQUE follow-up 2) -
# A backward edge is routed AROUND the outside of its own endpoint boxes (WI-257,
# just above), so at rank 0 / the last rank its U-turn lands outside the layout box
# `[0, width]` the viewBox used to declare — and the SVG viewport clipped it: the
# lane stopped flat at the box edge and its continuation re-entered a few px away.
# `_svg_frame` grows the box to the ink instead of shrinking the ink to the box.


def _viewbox_of(svg_tag):
    return [float(v) for v in re.search(r'viewBox="([^"]+)"', svg_tag).group(1).split()]


# A registry with a deliberate WRAP-AROUND: WI-001 (rank 0) carries a SOFT
# (advisory, `~`-prefixed) edge after WI-004 (the last rank), so its wire runs
# right-to-left across the whole diagram and the router sends it around the OUTSIDE
# of both endpoint boxes — the exact shape the viewBox used to cut. A soft edge
# never constrains the ranking, so the registry stays a legal acyclic DAG.
WRAPAROUND_WIS = (
    "WI-001,Bootstrap,scripts,SR-001,~WI-004,done,the adder\n"
    "WI-002,Harness,scripts,SR-001,WI-001,active,harness green\n"
    "WI-003,Subtraction,scripts,SR-002,WI-001;~WI-002,queued,the subber\n"
    "WI-004,Release,docs,SR-002,WI-002;WI-003,queued,shipped\n"
)


def test_svg_viewbox_contains_every_routed_wire(tmp_path):
    """No emitted wire is cut by its own viewBox — the WI-367 objective floor.

    Swept over every emitter that really renders, on the SAMPLED polyline a viewer's
    eye follows (not the source `d`), and with the same `_INK_PAD` clearance the
    generator claims, so a stroke's half-width is inside the box too. Non-vacuous by
    construction: the sweep must contain at least one wire that genuinely runs
    outboard of the layout box, which is the shape that was being clipped.

    The repo's own committed `PROJECT_STATE.html` is deliberately NOT in this sweep:
    it is a generated artifact whose freshness belongs to the trunk lane, not to a
    work branch (concurrency-restructure §5.2), so reading it would assert a property
    of *this* emitter against markup an older one wrote — a standing red on every
    work branch. `WRAPAROUND_WIS` supplies the outboard shape it used to contribute,
    from a fixture generated inside this test run.
    """
    gt = load_script("gen_trajectory")
    wrap = tmp_path / "wraparound"
    wrap.mkdir(parents=True, exist_ok=True)
    make_repo(wrap, WRAPAROUND_WIS)
    assert gen(wrap).returncode == 0
    docs = [(lb, d) for lb, d in _every_emitter_document(tmp_path) if lb != "shipped"]
    docs.append(("wrap-around", html_of(wrap)))
    # The fixture must really produce the shape, or the sweep is a tautology: an
    # emitter that never routes outboard trivially never clips. A padded box (a
    # negative viewBox min-x) is the visible proof that it did.
    assert re.search(r'<svg viewBox="-\d', docs[-1][1]), "fixture lost its wrap-around"
    clipped, outboard, swept = [], 0, 0
    for label, doc in docs:
        for svg in re.findall(r"<svg\b.*?</svg>", doc, re.S):
            tag = svg[: svg.index(">") + 1]
            if "viewBox" not in tag:
                continue
            vx, _vy, vw, _vh = _viewbox_of(tag)
            body = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.S)
            for d in re.findall(r'\sd="([^"]+)"', body):
                pts = _sample_path_d(d)
                if len(pts) < 2:
                    continue  # not an M/L/C wire (the containment arrow, the loops arc)
                swept += 1
                lo = min(p[0] for p in pts)
                hi = max(p[0] for p in pts)
                outboard += lo < 0.0 or hi > vw + vx
                if lo - vx < gt._INK_PAD or (vx + vw) - hi < gt._INK_PAD:
                    clipped.append((label, round(lo, 1), round(hi, 1), tag[:60]))
    assert swept > 30, "vacuous — the sweep found no routed wires"
    assert outboard, "vacuous — no wire in the sweep runs outboard of its layout box"
    assert not clipped, "wire(s) clipped by their viewBox: {}".format(clipped[:4])


def test_svg_frame_pads_only_the_side_that_carries_outboard_ink():
    # The shipped roadmap root layer's numbers (measured 2026-07-30): a 692-wide
    # layout box whose wrap-around lanes reach x=-17.5 on the left and x=711.0 on the
    # right. Each side is padded to the ink plus `_INK_PAD`, rounded out to a whole
    # unit, and the DECLARED width grows with the box — so a diagram that already fit
    # its card keeps its former scale and merely stops being cut.
    gt = load_script("gen_trajectory")
    lanes = (
        '<path class="wire" d="M703.0,10.0 L-17.5,10.0"/>'
        '<path class="wire" d="M20.0,30.0 L711.0,30.0"/>'
    )
    both = gt._svg_frame(692, 354, lanes)
    assert both.startswith('viewBox="-20 0 733 354" width="733"')
    assert "max-width:733px" in both and "min-width:454px" in both
    # ...and a lane that only overruns the right edge does not shift the left one.
    right = gt._svg_frame(904, 150, '<path class="wire" d="M20.0,10.0 L923.0,10.0"/>')
    assert right.startswith('viewBox="0 0 925 150" width="925"')


def test_svg_frame_leaves_a_diagram_with_no_outboard_ink_untouched():
    # The pad is measured from the body, so the overwhelming majority of emitted
    # diagrams — every one whose wires stay inside the layout box — must keep the
    # pre-WI-367 tag byte-for-byte. `-0` is the trap: a float negation of a zero pad
    # would render `viewBox="-0 0 ..."` and churn every diagram in the dashboard.
    gt = load_script("gen_trajectory")
    inside = gt._svg_frame(600, 200, '<path class="wire" d="M20.0,10.0 L580.0,10.0"/>')
    assert inside == 'viewBox="0 0 600 200" width="600" style="{}"'.format(
        gt._svg_fit_style(600)
    )
    # A marker's path lives in the MARKER's viewBox, not user space: `<defs>` must be
    # cut before the scan or every arrowhead would read as ink at x=0..10.
    marked = gt._svg_frame(600, 200, gt._arrow_markers(("a", "b")))
    assert marked == inside, "defs leaked into the ink scan"


def test_path_xs_reads_the_emitted_vocabulary_and_bails_on_anything_else():
    # `_path_xs` bounds the ink from the control hull. It must read the relative `h`
    # of the containment arrow as a DELTA (not an absolute x), and it must stop at a
    # command it does not know rather than consuming that command's arguments as
    # coordinates — under-padding a never-seen shape is recoverable, mis-placing the
    # whole box is not.
    gt = load_script("gen_trajectory")
    assert gt._path_xs("M100.0,9.0 h20") == [100.0, 120.0]
    assert gt._path_xs("M1.0,2.0 C3.0,4.0 5.0,6.0 7.0,8.0") == [1.0, 3.0, 5.0, 7.0]
    assert gt._path_xs("M1.0,2.0 A5 5 0 0 1 900,900") == [1.0]


def test_detour_hit_tests_the_outboard_stub_zone():
    # 111-REVIEW-A MINOR 1 (WI-257): _detour_d re-verified obstacles only over
    # [min(x1,xe), max(x1,xe)], but the detour's stubs reach xa=x1+stub / xb=xe-stub
    # — up to 18px OUTSIDE that span. A box sitting only in an outboard stub zone was
    # never hit-tested, so the router returned a grazing detour (the residual
    # fail-open, trial-679 class). Backward seam D(right, x1=500) → C(left, xe=160):
    # the left stub reaches xb=142, and box E overlaps [142,150] (the outboard stub
    # zone) while sitting LEFT of the old span [160,500]; F forces a real lane detour.
    gt = load_script("gen_trajectory")
    x1, sy, y1, xe, ty, y2 = 500.0, 145.0, 145.0, 160.0, 165.0, 165.0
    stub = 18.0
    f_box = (300.0, 130.0, 100.0, 50.0)  # inside the main span -> forces a detour
    e_box = (100.0, 125.0, 50.0, 40.0)  # x-span [100,150]
    assert e_box[0] + e_box[2] <= min(x1, xe)  # E is OUTSIDE the old [min,max] span
    assert e_box[0] + e_box[2] > xe - stub  # ...but overlaps the left outboard stub
    d = gt._detour_d(x1, sy, y1, xe, ty, y2, [f_box, e_box])
    assert " L" in d
    pts = _sample_path_d(d)
    assert not _polyline_crosses(pts, e_box)  # now hit-tested and routed around
    assert not _polyline_crosses(pts, f_box)


def test_detour_bounds_the_candidate_set_and_second_pass(monkeypatch):
    # 111-REVIEW-A MINOR 2 (WI-257): the two-pass × per-candidate full re-verify made
    # _route_edges 30-50x slower on DENSE overlap. The clear-check now short-circuits
    # (the first fully-clear lane wins) and the candidate set is capped at _MAX_LANES
    # per pass, with the redundant second pass skipped when it would re-scan the same
    # obstacle set (lane_span == full).
    gt = load_script("gen_trajectory")
    calls = [0]
    real_points = gt._detour_points

    def counting(*a, **k):
        calls[0] += 1
        return real_points(*a, **k)

    # WI-280: `_detour_d` resolves `_detour_points` in traj_graph's own namespace
    # now, so patch the module the caller looks in. `gt.traj_graph` IS the cached
    # sys.modules instance the facade's re-exports bound from (a fresh
    # `load_script("traj_graph")` would build a second, unconsulted module object).
    monkeypatch.setattr(gt.traj_graph, "_detour_points", counting)
    # short-circuit: one blocking box, the nearest lane clears at once -> the router
    # returns after a single trial rather than sweeping every candidate.
    rects = {
        "A": (0.0, 100.0, 100.0, 40.0),
        "B": (200.0, 100.0, 100.0, 40.0),
        "C": (400.0, 100.0, 100.0, 40.0),
    }
    gt._route_edges([("A->C", 100.0, 120.0, 400.0, 120.0, "A", "C")], rects, 12, 2)
    assert calls[0] <= 2  # first clear lane wins; no exhaustive sweep
    # cap + second-pass skip: feed 500 candidate lanes that NEVER clear (a box tall
    # enough in y to block every one). The router must evaluate exactly ONE capped
    # pass — _MAX_LANES trials — not the 1000 the two uncapped passes would have.
    calls[0] = 0
    monkeypatch.setattr(
        gt.traj_graph,
        "_lane_candidates",
        lambda *a, **k: [float(i) for i in range(500)],
    )
    dense = {
        "S": (0.0, 300.0, 100.0, 40.0),
        "T": (500.0, 300.0, 100.0, 40.0),
        "B": (250.0, 0.0, 100.0, 520.0),  # spans y[0,520] -> no lane in 0..499 clears
    }
    gt._route_edges([("S->T", 100.0, 320.0, 500.0, 320.0, "S", "T")], dense, 12, 2)
    assert (
        calls[0] == gt._MAX_LANES
    )  # capped to one pass; the redundant second pass is skipped


def _wire_through_box_violations(markup):
    """Every (wire d, blocking rect) pair where a wire's sampled polyline crosses a
    node box that is not its own source/target — the T8 through-box invariant. Each
    `<svg>` is a self-contained drill layer with its OWN coordinate system, so wires
    are only ever tested against boxes in the SAME svg (a panel concatenates many)."""
    num = r"(-?[\d.]+)"
    bad = []
    for svg in re.findall(r"<svg\b.*?</svg>", markup, re.S):
        rects = [
            (float(a), float(b), float(c), float(e))
            for a, b, c, e in re.findall(
                r'<rect x="'
                + num
                + r'" y="'
                + num
                + r'" width="'
                + num
                + r'" height="'
                + num
                + r'"',
                svg,
            )
            if float(c) > 20 and float(e) > 20
        ]
        wires = re.findall(
            r'<path class="(?:wire|swedge|kedge|edge(?: soft)?)"[^>]*?d="([^"]+)"', svg
        )
        for d in wires:
            pts = _sample_path_d(d)
            if len(pts) < 2:
                continue
            start, end = pts[0], pts[-1]
            for r in rects:
                rx, ry, rw, rh = r
                on_src = (
                    abs(start[0] - (rx + rw)) < 2 and ry - 3 <= start[1] <= ry + rh + 3
                )
                on_tgt = abs(end[0] - rx) < 10 and ry - 3 <= end[1] <= ry + rh + 3
                if on_src or on_tgt:
                    continue
                if _polyline_crosses(pts, r):
                    bad.append((d, r))
    return bad


def test_meta_containerized_sw_wires_avoid_unrelated_boxes():
    # Over the real meta repo the How-SW top view carries backward CMP seams — the
    # exact case 078-CRITIQUE flagged (CMP-001 → CMP-002/004 sweeping through boxes).
    # No wire in that panel may cross a component box it is not wired to.
    gt = load_script("gen_trajectory")
    cont = gt.sw_containment(ROOT, gt.sw_modules(ROOT))
    assert cont is not None
    _tab, panel = cont
    assert _wire_through_box_violations(panel) == []


def test_meta_knowledge_and_when_wires_avoid_unrelated_boxes():
    # The Knowledge concept graph and the tiered When roadmap over the real meta
    # repo: every wired diagram obeys the T8 through-box invariant.
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    kg = gt.know_graph(ROOT)
    assert kg is not None
    svg, _details = kg
    assert _wire_through_box_violations(svg) == []
    wis, integrity = ct.load_wis(ct.read_registry_rows(ROOT / ct.WI_CSV))
    assert not integrity
    when = gt.when_view(ROOT, wis)
    assert when is not None
    assert _wire_through_box_violations(when) == []


def test_fallback_dag_and_sw_graph_wires_avoid_unrelated_boxes():
    # 110-REVIEW-A MINOR: the meta panels render the tiered/containerized views,
    # so the flat fallbacks `dag_svg` / `sw_graph` (a small registry's roadmap, a
    # seam-less repo's How-SW) never enter the meta scans above — a routing
    # regression in either integration would ship unseen. Drive both over the
    # real registry and hold them to the same T8 through-box invariant; the
    # wire-presence floors keep the scan honest (an emitter rename or a dropped
    # `<svg>` wrapper would otherwise pass vacuously).
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    wis, integrity = ct.load_wis(ct.read_registry_rows(ROOT / ct.WI_CSV))
    assert not integrity
    dag, _details = gt.dag_svg(wis)
    assert dag.lstrip().startswith("<svg") and dag.count('<path class="edge') > 100
    assert _wire_through_box_violations(dag) == []
    sw = gt.sw_graph(ROOT, gt.sw_modules(ROOT))
    assert sw is not None
    assert sw.lstrip().startswith("<svg") and sw.count('<path class="swedge"') > 10
    assert _wire_through_box_violations(sw) == []


# --- WI-346: the one local spine loader + the one capture helper ---------------
# Three functions (`arch_icicle`, `spine_stats`, `_spine_pending`) each re-derived
# the SR/LLR/TC `read_rows(...) if id.startswith(...)` triple, and `_asof`/`_git`
# each spelled out the same five subprocess capture keywords — nine sanctioned
# census blocks (`spine-load-repeat`, `subprocess-capture`). Extracted to
# `_spine(root, skip_example=False)` and `_run_captured(argv)`.

# Deliberately NOT id-sorted, and deliberately noisy: a scrambled file order, a
# `-000` example row in the middle, and a row whose id carries no tier prefix.
# ROW ORDER IS THE CONTRACT — the icicle links each row to its FIRST listed
# parent and lays blocks out in arrival order, and `--check` byte-compares the
# render, so a sort or a set/dict round-trip inside the loader is a silent
# artifact change. A sorted fixture could not see that.
SCRAMBLED_SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
    'SR-009,Late,SN-001,"Shall late.",R,"late",,M,Test,Verified\n'
    'SR-000,Example,SN-001,"Shall example.",R,"example",,M,Test,Draft\n'
    'SR-002,Middle,SN-001,"Shall middle.",R,"middle",,M,Test,Modified\n'
    'NOTE,Not a requirement,SN-001,"Shall not.",R,"nope",,M,Test,Draft\n'
    'SR-001,First,SN-001,"Shall first.",R,"first",,M,Test,Verified\n'
)
SCRAMBLED_LLRS = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
    'LLR-007,SR-001,Late,src/m,add,"late",(see TC),Implemented\n'
    'LLR-000,SR-001,Example,src/m,add,"example",(see TC),Planned\n'
    "NOTE,SR-001,Not an LLR,src/m,add,nope,(see TC),Planned\n"
    'LLR-001,SR-001,First,src/m,add,"first",(see TC),Implemented\n'
)
SCRAMBLED_TCS = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n"
    "TC-005,LLR-001,Unit,call add,Smoke,a=5,ok,Yes,Verified\n"
    "NOTE,LLR-001,Unit,not a case,Smoke,a=0,ok,Yes,Draft\n"
    "TC-000,LLR-001,Unit,call add,Smoke,a=0,ok,Yes,Draft\n"
    "TC-001,LLR-001,Unit,call add,Smoke,a=1,ok,Yes,Verified\n"
)


def _scrambled_spine(root):
    """A registry whose three spine files are out of id order and carry both a
    `-000` example and a non-prefixed row."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    (req / "system-requirements.csv").write_text(SCRAMBLED_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(SCRAMBLED_LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(
        SCRAMBLED_TCS, encoding="utf-8"
    )
    return root


def test_spine_loader_equals_the_former_inline_filters_in_file_order(tmp_path):
    root = _scrambled_spine(tmp_path)
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    # The three comprehensions the three call sites each carried before WI-346,
    # transcribed verbatim from the pre-extraction source.
    want_srs = [
        r
        for r in ct.read_rows(root / ct.SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    ]
    want_llrs = [
        r
        for r in ct.read_rows(root / "docs/requirements/low-level-requirements.csv")
        if (r.get("LLR-ID") or "").startswith("LLR-")
    ]
    want_tcs = [
        r
        for r in ct.read_rows(root / "docs/test/test-cases.csv")
        if (r.get("TC-ID") or "").startswith("TC-")
    ]
    srs, llrs, tcs = gt._spine(root)
    # Whole-row equality: the loader must hand back the rows themselves, not a
    # projection — every call site reads columns the loader never names.
    assert srs == want_srs
    assert llrs == want_llrs
    assert tcs == want_tcs
    # Order spelled out, so a regression reads as the scramble it broke rather
    # than as an opaque list mismatch. `-000` survives the DEFAULT load.
    assert [r["SR-ID"] for r in srs] == ["SR-009", "SR-000", "SR-002", "SR-001"]
    assert [r["LLR-ID"] for r in llrs] == ["LLR-007", "LLR-000", "LLR-001"]
    assert [r["TC-ID"] for r in tcs] == ["TC-005", "TC-000", "TC-001"]


def test_spine_loader_drops_example_rows_only_when_asked(tmp_path):
    root = _scrambled_spine(tmp_path)
    gt = load_script("gen_trajectory")
    srs, llrs, tcs = gt._spine(root, skip_example=True)
    # `-000` gone from all three tiers, everything else still in file order.
    assert [r["SR-ID"] for r in srs] == ["SR-009", "SR-002", "SR-001"]
    assert [r["LLR-ID"] for r in llrs] == ["LLR-007", "LLR-001"]
    assert [r["TC-ID"] for r in tcs] == ["TC-005", "TC-001"]
    # The default keeps them: only the pending projection owes the `-000` rule
    # (an example row owes no ratification); the icicle and the maturity counts
    # render whatever the registry holds.
    d_srs, d_llrs, d_tcs = gt._spine(root)
    assert "SR-000" in [r["SR-ID"] for r in d_srs]
    assert "LLR-000" in [r["LLR-ID"] for r in d_llrs]
    assert "TC-000" in [r["TC-ID"] for r in d_tcs]
    # And the rule reaches its real caller: SR-000 is `Draft`, so a leaked
    # example row would invent a ratification the owner does not owe.
    pending = gt._spine_pending(root)
    assert pending, "the Draft/Modified SRs must still project"
    assert not any("SR-000" in line for line in pending)
    assert any("SR-002" in line for line in pending)  # Modified -> re-attest


class _SubprocessShim:
    """Stands in for gen_trajectory's `subprocess` binding so a spy never
    mutates the real stdlib module out from under the rest of the suite."""

    DEVNULL = subprocess.DEVNULL

    def __init__(self, run):
        self.run = run


def test_run_captured_states_the_five_keywords_and_degrades_off_git(
    tmp_path, monkeypatch
):
    gt = load_script("gen_trajectory")
    # 1. The contract itself — all five keywords, stated once. Dropping
    #    `errors="replace"` alone reintroduces the L-25 crash on exactly the
    #    rare input nobody tests with, so pin the kwargs, not just the result.
    seen = {}

    def spy(argv, **kwargs):
        seen.update(kwargs)
        return subprocess.run(argv, **kwargs)

    # WI-280: `_run_captured` resolves `subprocess` in traj_parse's namespace now,
    # so patch the module the call looks in (gt.traj_parse is the cached instance).
    monkeypatch.setattr(gt.traj_parse, "subprocess", _SubprocessShim(spy))
    proc = gt._run_captured([sys.executable, "-c", "print('hi')"])
    assert seen == {
        "capture_output": True,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "stdin": subprocess.DEVNULL,
    }
    assert proc.stdout.strip() == "hi"  # captured + decoded, not bytes/None

    # 2. No child at all: `_run_captured` deliberately does NOT swallow the
    #    OSError — the callers own the degrade, which is what lets a future
    #    caller see a failure this helper has no business deciding about.
    def boom(argv, **kwargs):
        raise OSError("no git here")

    monkeypatch.setattr(gt.traj_parse, "subprocess", _SubprocessShim(boom))
    with pytest.raises(OSError):
        gt._run_captured(["git", "--version"])
    # ...and both callers degrade to their empty forms rather than propagate.
    # (No registry is seeded: `_git`/`_asof` read git, not the work items.)
    assert gt._git(tmp_path, "rev-parse", "HEAD") == (1, "")
    assert gt._asof(tmp_path) == ""

    # 3. Real git, no repo: the other off-git shape (a child that RUNS and
    #    fails). tmp_path is not a work tree, so git exits nonzero.
    monkeypatch.undo()
    code, out = gt._git(tmp_path, "rev-parse", "--verify", "--quiet", "HEAD")
    assert code != 0 and out.strip() == ""
    assert gt._asof(tmp_path) == ""
