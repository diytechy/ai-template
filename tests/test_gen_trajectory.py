"""gen_trajectory.py — the offline trajectory dashboard (Thread 52 phase 2).

The generator renders the root PROJECT_STATE.html from the work-item registry (the
`docs/work/` spec folder) + the spine as a
*view* (a design principle: text is truth). What matters is that it is fully
offline (no CDN), deterministic (so the --check freshness gate is byte-stable),
refuses to render an invalid registry, and stays vacuous when there is nothing to
show. Each is pinned by running the real script over a minimal temp project.
"""

import re

from conftest import SCRIPTS, load_script
from traj_fixtures import (
    ARCH_MD,
    GOOD_WIS,
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
