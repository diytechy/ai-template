"""gen_trajectory.py — the offline trajectory dashboard (Thread 52 phase 2).

The generator renders the root PROJECT_STATE.html from work-items.csv + the spine as a
*view* (a design principle: text is truth). What matters is that it is fully
offline (no CDN), deterministic (so the --check freshness gate is byte-stable),
refuses to render an invalid registry, and stays vacuous when there is nothing to
show. Each is pinned by running the real script over a minimal temp project.
"""

import collections
import html
import re
import shutil

from conftest import ROOT, SCRIPTS, load_script, run_py

WI_HEADER = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable\n"

# A small but branching spine, so the icicle exercises multi-child subtrees and
# the taller-cell label path; SR-001 Verified + SR-002 Draft -> 50% definition.
SN_MD = """# Stakeholder Needs (SN-###)

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Do the thing well. | Users need it. | M | works end to end. |
"""
SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Core add,SN-001,"Shall add.",R,"add works",,M,Test,Verified
SR-002,Core sub,SN-001,"Shall subtract.",R,"sub works",,M,Test,Draft
"""
LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Adder,src/m,add,"a+b",(see TC),Implemented
LLR-002,SR-001,Adder edge,src/m,add,"overflow guard",(see TC),Implemented
LLR-003,SR-002,Subber,src/m,sub,"a-b",(see TC),Planned
"""
TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-001,SR-001;LLR-001,Unit,call add,Smoke,"a=1",ok,Yes,Verified
TC-002,LLR-001,Unit,call add,Smoke,"a=2",ok,Yes,Verified
TC-003,LLR-002,Unit,call add,Full,"a=3",ok,Yes,Verified
TC-004,SR-002;LLR-003,Unit,call sub,Full,"a=4",ok,No,Draft
"""
# A diamond DAG: WI-001 -> {WI-002, WI-003} -> WI-004; WI-003 also carries a
# soft (advisory, ~-prefixed) edge after WI-002 — dashed in the render, never
# a rank constraint.
GOOD_WIS = (
    "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
    "WI-002,Harness,scripts,SR-001,WI-001,active,harness green\n"
    "WI-003,Subtraction,scripts,SR-002,WI-001;~WI-002,queued,the subber\n"
    "WI-004,Release,docs,SR-002,WI-002;WI-003,queued,shipped\n"
)


def make_repo(root, wis_body=GOOD_WIS, readme=True, header=WI_HEADER):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    (req / "stakeholder-needs.md").write_text(SN_MD, encoding="utf-8")
    (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(TCS, encoding="utf-8")
    (req / "work-items.csv").write_text(header + wis_body, encoding="utf-8")
    if readme:
        (root / "README.md").write_text(
            '# demoproj\n\n<a id="vision"></a>\n'
            "**PROJECT-VISION:** Stay correct over time.\n\n## What\n",
            encoding="utf-8",
        )
    return root


def gen(root, *args):
    return run_py([SCRIPTS / "gen_trajectory.py", "--root", root, *args], cwd=root)


def html_of(root):
    return (root / "PROJECT_STATE.html").read_text(encoding="utf-8")


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
    wi = tmp_path / "docs" / "requirements" / "work-items.csv"
    wi.write_text(
        wi.read_text(encoding="utf-8") + "WI-005,More,scripts,SR-001,WI-004,queued,d\n",
        encoding="utf-8",
    )
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


ARCH_MD = """# Architecture

<!-- BEGIN GENERATED MODULE MAP -->
### `src/m`
_Demo module._

| Public item | Summary | Implements |
|---|---|---|
| `add(a, b)` | Adds. |  |
| `sub(a, b)` | Subtracts. |  |
<!-- END GENERATED MODULE MAP -->
"""


def test_how_sw_view_renders_from_the_module_map(tmp_path):
    # WI-039: with a committed symbol-mode module map, PROJECT_STATE gains the
    # How (SW architecture) view — a view of the code-map view; without one
    # (files-mode / absent) the tab is simply omitted.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    assert "How (SW architecture)" not in html_of(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-tab="sw"' in text and "How (SW architecture)" in text
    assert "src/m" in text and "add" in text


def test_cycle_refuses_to_render(tmp_path):
    make_repo(
        tmp_path,
        "WI-001,A,scripts,,WI-002,queued,d\nWI-002,B,scripts,,WI-001,queued,d\n",
    )
    proc = gen(tmp_path)
    assert proc.returncode == 1 and "cycle" in proc.stderr
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


# --- WI-056: the How-SW panel becomes a real interface graph --------------------

IF_HDR = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
    "Stability,Status,Component,Notes\n"
)


def test_how_sw_graph_renders_seams(tmp_path):
    # With a committed module map AND declared seams, the How-SW panel gains the
    # interface graph (module + file + external nodes, IF-labeled edges); the
    # render is byte-deterministic so --check stays stable.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (tmp_path / "docs" / "requirements" / "interfaces.csv").write_text(
        IF_HDR
        + 'IF-001,Provides,src/m,downstream adopter,"cli",SR-001,v1,Stable,Active,,\n'
        + 'IF-002,Consumes,src/m,docs/stack.ini,"reads",SR-001,v1,Stable,Active,,\n',
        encoding="utf-8",
    )
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "How (SW architecture)" in text
    assert "IF-001" in text and "swarrow" in text  # a labeled edge + the marker
    assert "downstream adopter" in text and "stack.ini" in text  # ext + file nodes
    first = text
    assert gen(tmp_path).returncode == 0
    assert html_of(tmp_path) == first  # deterministic


def test_how_sw_stays_a_table_without_seams(tmp_path):
    # No IF rows -> the panel keeps the bare module table (graph earned by seams);
    # no graph marker leaks into the render.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "How (SW architecture)" in text
    assert "swarrow" not in text


# --- WI-070: the Knowledge tab consumes the committed OKF bundle ----------------


def gen_okf(root):
    return run_py([SCRIPTS / "gen_okf.py", "--root", root], cwd=root)


def with_bundle(root):
    """make_repo + the OKF bundle the Knowledge tab consumes (gen_okf over the
    same registries), so the dashboard has a real docs/okf/ to render."""
    make_repo(root)
    assert gen_okf(root).returncode == 0
    assert (root / "docs" / "okf" / "system-requirements" / "SR-001.md").exists()
    return root


def test_knowledge_tab_renders_from_bundle(tmp_path):
    # C4: with a committed docs/okf/ bundle the dashboard gains the Knowledge tab
    # — typed concepts, each concept's DESCRIPTION embedded and a link-OUT to its
    # docs/okf/<tier>/<id>.md full body (the middle-path embedding, ruling #15).
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-tab="know"' in text and 'id="know"' in text
    # WI-159: the make_repo bundle spans SN/SR/LLR/TC = 4 types (> 3), so the tab
    # opens START-COLLAPSED as the shared type-tiered drill (one block per OKF
    # type, each a descend container), NOT the flat exploded concept graph.
    assert 'class="drill"' in text and 'data-tier="okf-type"' in text
    assert 'class="knode"' not in text  # the wall-of-nodes flat graph is gone
    assert "System Requirement" in text and "Stakeholder Need" in text
    # the concept nodes live in the descend layers, keyed for the detail aside
    assert 'data-node="SN-001"' in text and 'data-node="SR-001"' in text
    # the description is embedded in the detail data...
    assert "Shall add." in text
    # ...and the link-out points at a file that actually exists beside the HTML.
    href = "docs/okf/system-requirements/SR-001.md"
    assert href in text
    assert (tmp_path / href).exists()
    # the GENERATED banner line is bundle plumbing, never rendered as content.
    assert "a reference copy, not the source of truth" not in text
    # the responsive shell still holds with the extra tab present.
    assert '<meta name="viewport" content="width=device-width' in text
    assert "@media (max-width:760px)" in text


def test_knowledge_tab_omitted_and_byte_identical_without_bundle(tmp_path):
    # The vacuity guarantee: with no docs/okf/ the tab is omitted and the artifact
    # is byte-for-byte what it was before this view existed. Proven by round-trip:
    # render bundle-less, add the bundle (tab appears), remove it, re-render ==
    # the original bytes exactly.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    without = (tmp_path / "PROJECT_STATE.html").read_bytes()
    assert b'data-tab="know"' not in without

    assert gen_okf(tmp_path).returncode == 0
    assert gen(tmp_path).returncode == 0
    assert b'data-tab="know"' in (tmp_path / "PROJECT_STATE.html").read_bytes()

    shutil.rmtree(tmp_path / "docs" / "okf")
    assert gen(tmp_path).returncode == 0
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == without


def test_knowledge_tab_is_byte_deterministic(tmp_path):
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first


def test_check_stays_stable_through_regen_with_bundle(tmp_path):
    # No new --check exclusion: layout is computed from the sorted bundle at
    # generation time, so a fresh render passes --check.
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    fresh = gen(tmp_path, "--check")
    assert fresh.returncode == 0 and "up to date" in fresh.stdout


def test_malformed_okf_concept_is_skipped_with_warn(tmp_path):
    # A hand-broken bundle file must never crash the dashboard: it is skipped
    # with a stderr warn and the rest of the graph still renders.
    with_bundle(tmp_path)
    (tmp_path / "docs" / "okf" / "system-requirements" / "SR-001.md").write_text(
        "not a valid concept — no frontmatter\n", encoding="utf-8"
    )
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "skipping malformed OKF concept" in proc.stderr
    text = html_of(tmp_path)
    assert 'data-tab="know"' in text  # still renders
    assert 'data-node="SR-002"' in text  # the surviving concept is still a node


def test_meta_okf_bundle_renders_the_knowledge_graph():
    # Smoke test over the real meta-repo bundle (~219 concepts): the graph builds,
    # is typed, and every sampled link-out resolves to a committed file.
    gt = load_script("gen_trajectory")
    kg = gt.know_graph(ROOT)
    assert kg is not None
    svg, details = kg
    assert len(details) > 200
    assert details["SR-038"]["type"] == "System Requirement"
    assert "knowarrow" in svg
    for cid in ("SN-001", "SR-038", "TC-038"):
        assert (ROOT / details[cid]["href"]).exists()


# --- WI-159: the Knowledge graph obeys the SR-089 `>3` start-collapsed rule ------
# The T2 density fix: a bundle spanning > 3 OKF types opens COLLAPSED as the shared
# When/How-SW type-tiered drill (one block per type, descend into its concepts); a
# bundle of <= 3 types stays the flat concept graph (the tiering is earned by scale).


def _know_section(text):
    """The whole Knowledge <section> (all drill layers, incl. the hidden ones)."""
    return text.split('id="know"', 1)[1].split("</section>", 1)[0]


def _flat_bundle(root):
    """make_repo + a hand-written <= 3-type OKF bundle (SN + SR only), so the
    Knowledge graph stays below the `>3` type threshold and renders flat."""
    make_repo(root)
    okf = root / "docs" / "okf"
    for tier, cid, ctype in (
        ("stakeholder-needs", "SN-001", "Stakeholder Need"),
        ("system-requirements", "SR-001", "System Requirement"),
        ("system-requirements", "SR-002", "System Requirement"),
    ):
        d = okf / tier
        d.mkdir(parents=True, exist_ok=True)
        (d / (cid + ".md")).write_text(
            '---\ntype: "{}"\ntitle: "{} title"\ndescription: "desc {}"\n'
            "---\n# {}\n".format(ctype, cid, cid, cid),
            encoding="utf-8",
        )
    return root


def test_knowledge_graph_collapses_above_type_threshold(tmp_path):
    # > 3 OKF types (the make_repo bundle spans SN/SR/LLR/TC) -> the Knowledge tab
    # opens as the shared type-tiered drill, reusing the When/How collapse
    # mechanism (`class="drill"`, one descend container per OKF type), NOT the flat
    # exploded concept graph. The WI-070 richness (descriptions + link-outs) and
    # the `>3`-earned collapse both hold.
    gt = load_script("gen_trajectory")
    with_bundle(tmp_path)
    assert gt.know_view(tmp_path) is not None  # collapse earned by > 3 types
    assert gen(tmp_path).returncode == 0
    know = _know_section(html_of(tmp_path))
    assert 'class="drill"' in know  # the shared drill mechanism, single-sourced
    assert 'class="knode"' not in know  # not the flat wall-of-nodes
    # the root layer is one descend container per OKF type (SN/SR/LLR/TC = 4)
    assert know.count('data-tier="okf-type" data-descend=') == 4
    # concepts live in the descend layers, wired (data-node) to the detail aside
    assert 'data-node="SR-001"' in know
    assert "Shall add." in know  # description survives the collapse
    assert "docs/okf/system-requirements/SR-001.md" in know  # link-out survives


def test_knowledge_graph_stays_flat_at_or_below_type_threshold(tmp_path):
    # <= 3 OKF types -> know_view returns None and the flat concept graph renders
    # (byte-identical path), exactly as when_view keeps the flat DAG below its
    # thresholds. The tiering is earned by scale, so a small bundle stays legible flat.
    gt = load_script("gen_trajectory")
    _flat_bundle(tmp_path)
    assert gt.know_view(tmp_path) is None  # <= 3 types -> no collapse
    assert gen(tmp_path).returncode == 0
    know = _know_section(html_of(tmp_path))
    assert 'class="knode"' in know  # the flat concept graph
    assert 'data-id="SR-001"' in know  # flat nodes carry data-id
    assert 'data-tier="okf-type"' not in know  # no type-tiered collapse


# --- review 019: the WI-102 per-node <title> tooltip contract, pinned -----------


def _view_svg(text, marker):
    """The first SVG body after `marker` — one rendered view's node markup."""
    return text.split(marker, 1)[1].split("</svg>", 1)[0]


def test_svg_nodes_carry_escaped_title_tooltips(tmp_path):
    """Review 019 (on WI-102): the tooltip/a11y contract was untested — the one
    changed assertion made <title> optional, so a regression dropping it from
    any of the four emitters stayed green. Pin each emitter: every node <g>
    carries a <title> child, and the tip renders markup-hostile row content
    escaped."""
    make_repo(
        tmp_path,
        wis_body=(
            "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
            "WI-002,Harness <fast & loose>,scripts,SR-001,WI-001,active,harness\n"
        ),
    )
    # a markup-hostile SR title flows into the icicle and the OKF concept graph
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        SRS.replace("Core add", "Core add & <check>"), encoding="utf-8"
    )
    # the How-SW graph needs the module map + a declared seam (hostile external)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (tmp_path / "docs" / "requirements" / "interfaces.csv").write_text(
        IF_HDR + 'IF-001,Provides,src/m,pip & git,"cli",SR-001,v1,Stable,Active,,\n',
        encoding="utf-8",
    )
    assert gen_okf(tmp_path).returncode == 0  # the Knowledge tab's bundle
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = html_of(tmp_path)

    # arch_icicle: every cell carries a <title>; the SR tip renders escaped.
    ice = _view_svg(text, 'id="ice"')
    assert ice.count("<title>") == ice.count('class="cell') > 0
    assert "<title>SR-001 — Core add &amp; &lt;check&gt;</title>" in ice

    # dag_svg: every WI node carries a <title> = id — escaped title (status).
    dag = _view_svg(text, 'id="dag-view"')
    assert dag.count("<title>WI-") == 2
    assert "<title>WI-002 — Harness &lt;fast &amp; loose&gt; (active)</title>" in dag

    # sw_graph: node tips are kind-suffixed and escaped (module + external).
    sw = _view_svg(text, 'id="sw"')
    assert "<title>src/m (module)</title>" in sw
    assert "<title>pip &amp; git (external)</title>" in sw

    # Knowledge tab (collapsed drill, WI-159): every concept block carries a
    # <title> = id — title (type); the markup-hostile SR title is escaped. The
    # concept blocks live in the hidden descend layers, so scan the whole section
    # (not just the first svg, which is the type-summary root layer).
    know = text.split('id="know"', 1)[1].split("</section>", 1)[0]
    assert know.count('class="block') > 0  # concept/type blocks rendered
    assert (
        "<title>SR-001 — Core add &amp; &lt;check&gt; (System Requirement)</title>"
        in know
    )


# --- WI-073/FB5: the containerized How-SW top view -----------------------------

CONT_ARCH = """# Architecture
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_Module A._

| Public item | Summary | Implements |
|---|---|---|
| `run(x)` | Runs. |  |

### `scripts/mod_b`
_Module B._

| Public item | Summary | Implements |
|---|---|---|
| `go()` | Go. |  |

### `scripts/mod_c`
_Module C._

| Public item | Summary | Implements |
|---|---|---|
| `gen()` | Gen. |  |

### `scripts/mod_d`
_Module D._

| Public item | Summary | Implements |
|---|---|---|
| `emit()` | Emit. |  |
<!-- END GENERATED MODULE MAP -->
"""

CONT_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component
LLR-001,SR-001,A,scripts/mod_a,run,d,(see TC),Verified,CMP-001
LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Verified,CMP-001
LLR-003,SR-002,C,scripts/mod_c,gen,d,(see TC),Verified,CMP-002
LLR-004,SR-002,D,scripts/mod_d,emit,d,(see TC),Verified,CMP-002
"""

CONT_CMPS = (
    "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
    "CMP-001,Core,software,,built,,,,\n"
    "CMP-002,Gen,software,,built,,,,\n"
)

# Two seams a->c and b->c both cross CMP-001 -> CMP-002 (must aggregate to ONE
# deduplicated edge); IF-003 is intra-CMP-001, IF-004 a boundary to a file hub.
CONT_IFS = (
    IF_HDR
    + "IF-001,Provides,scripts/mod_a,scripts/mod_c,call,SR-001,v1,Stable,Active,,\n"
    + "IF-002,Provides,scripts/mod_b,scripts/mod_c,call,SR-001,v1,Stable,Active,,\n"
    + "IF-003,Provides,scripts/mod_a,scripts/mod_b,call,SR-001,v1,Stable,Active,,\n"
    + "IF-004,Consumes,scripts/mod_a,docs/stack.ini,reads,SR-001,v1,Stable,Active,,\n"
)


def containerize(root):
    """make_repo + a 4-module arch-map, two software components tagging them via
    LLR Component tags, and the cross/intra/boundary seams."""
    make_repo(root)
    req = root / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(CONT_LLRS, encoding="utf-8")
    (req / "components.csv").write_text(CONT_CMPS, encoding="utf-8")
    (req / "interfaces.csv").write_text(CONT_IFS, encoding="utf-8")
    (root / "docs" / "architecture.md").write_text(CONT_ARCH, encoding="utf-8")
    return root


def sw_section(root):
    return html_of(root).split('id="sw"', 1)[1].split("</section>", 1)[0]


def _sw_layer_with(sw, marker):
    """The SVG of the first How-SW drill `.layer` whose blocks carry `marker`."""
    for _lid, svg in re.findall(
        r'<div class="layer" data-layer="(sw-\d+)"[^>]*>(.*?)</div>', sw, re.S
    ):
        if marker in svg:
            return svg
    raise AssertionError("no sw layer contains " + marker)


def test_how_sw_containerizes_when_components_contain_modules(tmp_path):
    # With a CMP layer that contains modules, the How-SW panel becomes the
    # containerized Simulink-style drill top view (≤10 items), not the flat table.
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert 'class="cmptree"' in sw and 'class="drill"' in sw
    root = _sw_layer_with(sw, 'data-tier="component"')
    assert root.count('data-tier="component"') == 2  # two top-level components
    assert root.count('data-tier="component" data-descend=') == 2  # each descends
    assert "Top view: 2 item" in sw
    # descending CMP-001 reveals its modules + its intra + boundary seams.
    inside = _sw_layer_with(sw, "scripts/mod_a")
    assert "scripts/mod_a" in inside
    assert "IF-003" in inside  # intra-component seam (mod_a -> mod_b)
    assert "IF-004" in inside and "stack.ini" in inside  # boundary seam to a file hub


def test_boundary_aggregation_dedupes_cross_component_edges(tmp_path):
    # IF-001 and IF-002 both cross CMP-001 -> CMP-002; at the top level they
    # aggregate to ONE deduplicated component-to-component wire naming both ids.
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    root = _sw_layer_with(sw_section(tmp_path), 'data-tier="component"')
    titles = re.findall(r'<path class="wire"[^>]*><title>(.*?)</title>', root)
    assert len(titles) == 1  # one aggregated cross-component wire
    assert "IF-001, IF-002" in titles


def test_no_cmp_renders_flat_view_byte_identical(tmp_path):
    # The vacuity guarantee: render flat (no CMP layer), add the containment
    # (panel changes), remove it, re-render == the original flat bytes exactly.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(CONT_ARCH, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    flat = (tmp_path / "PROJECT_STATE.html").read_bytes()
    assert b'class="cmptree"' not in flat

    req = tmp_path / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(CONT_LLRS, encoding="utf-8")
    (req / "components.csv").write_text(CONT_CMPS, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    assert b'class="cmptree"' in (tmp_path / "PROJECT_STATE.html").read_bytes()

    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (req / "components.csv").unlink()
    assert gen(tmp_path).returncode == 0
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == flat


def test_containerized_view_is_deterministic_and_check_stable(tmp_path):
    # Built from sorted inputs, no clocks -> a second render is byte-identical and
    # --check passes (no new freshness exclusion).
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0


def test_nested_components_render_inside_their_parent(tmp_path):
    # A CMP with PartOf renders as a nested component block inside its parent's
    # descend layer, and only the top-level root is a first-view item.
    containerize(tmp_path)
    req = tmp_path / "docs" / "requirements"
    (req / "components.csv").write_text(
        CONT_CMPS + "CMP-003,Sub,software,,built,,CMP-001,,\n", encoding="utf-8"
    )
    (req / "low-level-requirements.csv").write_text(
        CONT_LLRS.replace(
            "LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Verified,CMP-001",
            "LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Verified,CMP-003",
        ),
        encoding="utf-8",
    )
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    # Still two top-level items (CMP-001 with CMP-003 nested inside, and CMP-002).
    assert "Top view: 2 item" in sw
    assert "CMP-003" in sw  # the nested child is rendered (inside CMP-001)


def test_meta_component_top_view_smoke():
    # Over the real meta repo: 5 right-sized software components, 0 uncontained,
    # within the bound, and sw_containment renders the containerized panel.
    ct = load_script("check_trajectory")
    v = ct.component_top_view(ROOT)
    assert v["count"] <= ct.TOP_VIEW_MAX
    assert v["uncontained"] == []
    assert len(v["top_roots"]) == 5
    gt = load_script("gen_trajectory")
    cont = gt.sw_containment(ROOT, gt.sw_modules(ROOT))
    assert cont is not None
    tab, panel = cont
    assert 'data-tab="sw"' in tab and 'class="cmptree"' in panel


# --- a small registry fixture (<= 3 phases AND <= 3 workstreams) --------------
# Below both tiering thresholds `when_view` returns None, so the flat SVG DAG
# renders (the phase->workstream->work-item tiering is earned by scale).
SMALL_WIS = (
    "WI-001,Root,scripts,SR-001,,done,the adder\n"
    "WI-002,Mid,scripts,SR-001,WI-001,active,harness\n"
    "WI-003,Sub,scripts,SR-002,WI-001,queued,the subber\n"
    "WI-004,Release,docs,SR-002,WI-002;WI-003,queued,shipped\n"
)


# --- WI-087 / SR-051 (rev WI-141): the tiered, Simulink-style drill-down views --
# The When roadmap tiers into phase -> workstream -> work-item block
# LAYERS once a tier holds > 3 members:
# each layer is an SVG diagram of blocks with input/output ports, the aggregated
# cross-tier edges wired between ports (the deduped union of child edges), a
# container block double-clicked (or Enter/Space) to DESCEND one layer and a
# breadcrumb to return (superseding the old <details> expand). A registry below the
# thresholds renders byte-identically to the flat SVG DAG.

# Four SR phases (v1..v4 — the CLI is label-agnostic, so a downstream vN still
# tiers), so a WI's phase is derived from the SR it delivers.
TIER_SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase\n"
    'SR-001,P1,SN-001,"r",R,"a",,M,Test,Verified,v1\n'
    'SR-002,P2,SN-001,"r",R,"a",,M,Test,Verified,v2\n'
    'SR-003,P3,SN-001,"r",R,"a",,M,Test,Verified,v3\n'
    'SR-004,P4,SN-001,"r",R,"a",,M,Test,Verified,v4\n'
)
TIER_HDR = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable\n"

# Two v1 WIs both feed the single v2 WI -> the v1->v2 parent edge is the deduped
# union of two child edges. Phases: v1={001,002}, v2={003}, v3={004}, v4={005}.
TIER_UNION_WIS = (
    "WI-001,A,scripts,SR-001,,done,d,\n"
    "WI-002,B,docs,SR-001,,done,d,\n"
    "WI-003,C,unattended,SR-002,WI-001;WI-002,queued,d,\n"
    "WI-004,D,self-adoption,SR-003,WI-003,queued,d,\n"
    "WI-005,E,scripts,SR-004,WI-003,queued,d,\n"
)


def _layer_with(view, marker):
    """The SVG of the first drill `.layer` whose blocks carry `marker` (a drill
    layer div holds only its SVG — no nested divs — so the split is clean)."""
    for _lid, svg in re.findall(
        r'<div class="layer" data-layer="(when-\d+)"[^>]*>(.*?)</div>', view, re.S
    ):
        if marker in svg:
            return svg
    raise AssertionError("no layer contains " + marker)


def tiered_repo(root, wis_body, header=TIER_HDR, srs=TIER_SRS):
    """make_repo + a phase-carrying SR registry (the WI phase is derived from the
    SRs a work item delivers)."""
    make_repo(root, wis_body, header=header)
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        srs, encoding="utf-8"
    )
    return root


# --- WI-272 (review M-2): six registry statuses, four swatches, no rewriting ----

SIX_STATUS_WIS = (
    "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
    "WI-002,Harness,scripts,SR-001,WI-001,active,\n"
    "WI-003,Release,docs,SR-002,WI-002,queued,\n"
    "WI-004,Someday,docs,SR-002,WI-002,deferred,parked on purpose\n"
    "WI-005,Waiting,docs,SR-002,WI-002,blocked,needs an upstream decision\n"
    "WI-006,Dropped,docs,SR-002,WI-002,retired,won't build\n"
)


def test_wi272_deferred_and_blocked_are_never_rewritten_as_queued(tmp_path):
    """review M-2: the dashboard used to clamp every unknown status to `queued`
    — and not just for the swatch. The clamp ran BEFORE the tooltip, the
    accessible name, and the detail JSON were built, so a `deferred` row's own
    detail said `"status": "queued"`. Parked-by-choice and impeded-by-something
    are not ordinary queue work, and this is the repo's advertised state surface,
    so that mislabelling mis-prioritizes real work.

    Sharing a swatch is fine and stays (minting two more hues would worsen the
    live U5 near-duplicate residue); rewriting the STATUS is the defect.
    """
    make_repo(tmp_path, SIX_STATUS_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)

    for status in ("done", "active", "queued", "deferred", "blocked", "retired"):
        assert 'data-status="{}"'.format(status) in page, (
            "no node carries data-status={} — the DOM lost the true status".format(
                status
            )
        )
        assert '"status": "{}"'.format(status) in page, (
            "the detail JSON never reports {} — it is being rewritten".format(status)
        )
    # the hover title names the row's own status, not its bucket
    assert "WI-004 — Someday (deferred)" in page
    assert "WI-005 — Waiting (blocked)" in page
    # ...and the two share `queued`'s swatch, deliberately and visibly: the
    # legend names the grouping rather than leaving the shared colour to imply
    # they are queued.
    gt = load_script("gen_trajectory")
    assert gt.STATUS_BUCKET["deferred"] == gt.STATUS_BUCKET["blocked"] == "queued"
    assert "not started" in page
    for glyph in (gt.STATUS_GLYPH["deferred"], gt.STATUS_GLYPH["blocked"]):
        assert glyph in page, "the legend must show the glyph that tells them apart"


def test_wi272_status_is_carried_through_the_tiered_drill_too(tmp_path):
    # The flat DAG and the tiered drill are separate emitters; M-2 named both.
    # The drill's leaf label is glyph-prefixed per STATUS, so `deferred` and
    # `blocked` differ from `queued` there without any colour at all.
    tiered_repo(tmp_path, TIER_UNION_WIS + SIX_STATUS_WIS.replace("WI-00", "WI-01"))
    assert gen(tmp_path).returncode == 0
    gt = load_script("gen_trajectory")
    # Every WORK-ITEM block across every layer. Two narrowings, both learned by
    # getting them wrong: `_layer_with` returns one layer, so it saw only the
    # first phase/workstream group (done + active — the glyph assertion would
    # have passed vacuously); and `.blab` is the label class of EVERY drill
    # block, so a bare class scan also pulls in phase/workstream containers and
    # the whole How-SW drill, none of which have a status to prefix.
    labels = re.findall(
        r'data-tier="work-item"[^>]*data-label="([^"]*)"', html_of(tmp_path)
    )
    assert labels, "no work-item blocks rendered"
    glyphs = set(gt.STATUS_GLYPH.values())
    assert all(lab[0] in glyphs for lab in labels), labels
    # the parked/impeded glyphs actually reached the drill, so this is not vacuous
    assert any(lab[0] == gt.STATUS_GLYPH["deferred"] for lab in labels), labels
    assert any(lab[0] == gt.STATUS_GLYPH["blocked"] for lab in labels), labels


def test_when_view_tiers_by_phase_above_threshold(tmp_path):
    # > 3 phases -> the When view starts at a layer of 4 phase blocks, each a
    # descend container carrying the per-phase color accent; the count is surfaced.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert "Tiered roadmap: 4 phase(s), 4 workstream(s)" in view
    assert view.count('data-tier="phase"') == 4  # one block per phase
    # each phase block is a descend container (double-click / Enter to drill in)
    assert view.count('data-tier="phase" data-descend=') == 4
    # the per-phase colour accent legend renders through the shared component
    # (WI-294b: no longer a bespoke `span.ph` chip idiom)
    assert '<div class="legend"><span><i style="background:' in view


def test_when_view_parent_edge_is_deduped_union_of_child_edges(tmp_path):
    # The two v1->v2 child edges (WI-001->WI-003 and WI-002->WI-003) aggregate to
    # ONE parent block wire equal to their deduped union, carried as the wire title.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    phase_layer = _layer_with(html_of(tmp_path), 'data-tier="phase"')
    wire_titles = re.findall(
        r'<path class="wire"[^>]*><title>(.*?)</title>', phase_layer
    )
    # crossing phase pairs v1->v2, v2->v3, v2->v4 -> three aggregated wires
    assert len(wire_titles) == 3
    assert "WI-001→WI-003, WI-002→WI-003" in wire_titles  # deduped union, one wire


def test_when_view_nests_workstream_tier_inside_a_phase(tmp_path):
    # Within a phase that holds > 3 workstreams the workstream tier fires, nesting
    # phase -> workstream -> work item as descend layers; below the threshold flat.
    body = (
        "WI-001,A1,scripts,SR-001,,done,d,\n"
        "WI-002,A2,docs,SR-001,,done,d,\n"
        "WI-003,A3,unattended,SR-001,,done,d,\n"
        "WI-004,A4,self-adoption,SR-001,,done,d,\n"  # v1 spans 4 workstreams
        "WI-005,B1,scripts,SR-002,WI-001,active,d,\n"  # v2, one workstream -> flat
        "WI-006,C1,scripts,SR-003,WI-005,queued,d,\n"
        "WI-007,D1,scripts,SR-004,WI-006,queued,d,\n"
    )
    tiered_repo(tmp_path, body)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert view.count('data-tier="phase"') == 4  # 4 phase blocks at the root layer
    # only v1 (4 workstreams) explodes into a workstream layer -> 4 workstream blocks
    assert view.count('data-tier="workstream"') == 4
    assert "Scripts / harness" in view  # workstream label on a sub-block


def test_when_view_workstream_tier_when_phases_flat(tmp_path):
    # <= 3 phases but > 3 workstreams -> the workstream tier fires at the TOP
    # (the "or at the top when phases <= 3" rule); phases stay flat.
    body = (
        "WI-001,A,scripts,,,done,d,\n"
        "WI-002,B,docs,,WI-001,active,d,\n"
        "WI-003,C,unattended,,WI-001,queued,d,\n"
        "WI-004,D,self-adoption,,WI-002;WI-003,queued,d,\n"
        "WI-005,E,deliverable,,WI-004,queued,d,\n"  # five workstreams, all unphased
    )
    make_repo(tmp_path, body, header=TIER_HDR)  # default SRs (no Phase) -> unphased
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert "Tiered roadmap: 1 phase(s), 5 workstream(s)" in view
    assert view.count('data-tier="workstream"') == 5  # one block per workstream
    assert 'data-tier="phase"' not in view  # phases stay flat


def test_when_view_below_thresholds_returns_none_flat_dag(tmp_path):
    # <= 3 phases and <= 3 workstreams -> when_view returns None, so the caller keeps
    # the flat SVG DAG (the tiering is earned by scale). The rendered dashboard shows
    # the flat DAG with no drill layers.
    make_repo(tmp_path, SMALL_WIS)  # 2 workstreams, unphased -> 1 phase
    gt = load_script("gen_trajectory")
    ct = load_script("check_trajectory")
    wis, _ = ct.load_wis(ct.read_rows(tmp_path / ct.WI_CSV))
    assert gt.when_view(tmp_path, wis) is None
    assert gen(tmp_path).returncode == 0
    assert 'class="drill"' not in html_of(tmp_path)  # flat DAG, no tiered drill


def test_wi296_interaction_copy_matches_the_emitter_that_actually_ran(tmp_path):
    """WI-296: the When explainer must describe the emitter that RAN, not a promise
    only one of them keeps.

    Neighbourhood highlighting belongs to the FLAT emitter — the controller walks
    `.wi`/`.edge` nodes only `dag_svg` produces. The sentence used to claim it
    unconditionally, so above the `>3` rule (where the tiered drill view renders and
    those node sets are empty) the dashboard promised an interaction it did not have.

    Note what this does NOT do: the flat `.wi` path is live and is the default for a
    small/newly-scaffolded repo, so its copy — and its emitter — stay exactly as they
    were. 117-CRITIQUE read the empty `.wi` set in the meta-repo's own render as dead
    code; deleting it would have broken the When tab for every downstream adopter.
    """
    # small registry -> flat DAG -> the neighbourhood promise is TRUE and kept
    make_repo(tmp_path, SMALL_WIS)  # 2 workstreams, unphased -> 1 phase
    assert gen(tmp_path).returncode == 0
    flat = html_of(tmp_path)
    assert 'class="drill"' not in flat
    assert 'class="wi ' in flat  # the flat emitter really is the live one here
    assert "highlight its neighbourhood" in flat
    assert "Double-click</strong> a container" not in flat

    # a registry above the >3 rule -> tiered drill -> the copy describes descending
    tiered = tmp_path / "tiered"
    tiered.mkdir()
    tiered_repo(tiered, TIER_UNION_WIS)
    assert gen(tiered).returncode == 0
    drill = html_of(tiered)
    assert 'class="drill"' in drill
    assert "Double-click</strong> a container" in drill
    assert "the breadcrumb returns to any ancestor" in drill
    # the promise the tiered render cannot keep is gone
    assert "highlight its neighbourhood" not in drill


def test_when_view_is_deterministic_and_check_stable(tmp_path):
    # Sorted inputs, no clocks -> a re-render is byte-identical and --check passes.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0


# --- SR-051 rev (WI-141): the three interface-wired / descend-a-layer contracts --


def test_when_view_seams_wire_to_block_ports(tmp_path):
    # Each block carries an input port (left-middle) and an output port
    # (right-middle); each aggregated edge is a wire whose endpoints ATTACH to those
    # ports (Simulink-style), not free-floating text.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    root = _layer_with(html_of(tmp_path), 'data-tier="phase"')  # the phase layer
    out_ports = {
        round(float(cx), 1)
        for cx in re.findall(r'<circle class="port out" cx="([\d.]+)"', root)
    }
    in_ports = {
        round(float(cx), 1)
        for cx in re.findall(r'<circle class="port in" cx="([\d.]+)"', root)
    }
    assert out_ports and in_ports  # both port kinds render
    wires = re.findall(r'<path class="wire" d="M([\d.]+),[\d.]+ C.* ([\d.]+),', root)
    assert wires  # at least one wire
    # The start attaches on the OUT port; the arrow-bearing END lands PORT_R + 2
    # px short of the IN-port center so its arrowhead clears the port ring
    # (WI-249 render fix) — still "at" the port, just outside its circle.
    gt = load_script("gen_trajectory")
    end_gap = gt.PORT_R + 2
    in_ends = {round(cx - end_gap, 1) for cx in in_ports}
    for x1, x2 in wires:  # every wire leaves an OUT port and enters an IN port
        assert round(float(x1), 1) in out_ports
        assert round(float(x2), 1) in in_ends


def test_when_view_double_click_descends_a_layer(tmp_path):
    # A container block descends one layer on double-click (keyboard alt: Enter /
    # Space on the focused block); its data-descend names a real child layer.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    m = re.search(r'data-tier="phase" data-descend="(when-\d+)"', view)
    assert m and 'data-layer="{}"'.format(m.group(1)) in view  # target layer exists
    # focusable + labelled + a keyboard alternative to the pointer
    assert 'tabindex="0" role="button"' in view
    assert "addEventListener('dblclick'" in view
    assert "addEventListener('keydown'" in view and "e.key==='Enter'" in view


def test_when_view_breadcrumb_restores_parent(tmp_path):
    # The drill carries a breadcrumb whose crumb click truncates the trail back to
    # that ancestor (restoring the parent view); the root crumb is declared.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert '<nav class="crumbs"' in view and 'data-root-crumb="Roadmap"' in view
    assert "trail=trail.slice(0,i+1)" in view  # crumb click restores the ancestor


# --- SR-056 (WI-143): the decomposition render-polish contracts ------------------


def test_decomposition_one_arrow_per_containment_edge(tmp_path):
    # Each descend container (a containment edge) renders EXACTLY one horizontal
    # parent->child arrow (class="cedge"), making containment explicit rather than
    # implied by the descend interaction alone.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    phase_layer = _layer_with(html_of(tmp_path), 'data-tier="phase"')
    containers = phase_layer.count("data-descend=")  # 4 phase containers
    assert containers == 4
    assert phase_layer.count('class="cedge"') == containers  # one arrow each, no more


def test_tier_column_honors_declared_width_bound(tmp_path):
    # The tier column is a declared value (MAX_TIER_COL), not an adjective: every
    # block honours it, and a content-light layer renders NARROWER than the bound
    # (right-sized, not the former uniform column).
    gt = load_script("gen_trajectory")
    assert isinstance(gt.MAX_TIER_COL, int) and gt.MAX_TIER_COL > 0
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    widths = [
        int(w)
        for w in re.findall(
            r'<rect x="[\d.]+" y="[\d.]+" width="(\d+)" height="\d+" rx="8"',
            html_of(tmp_path),
        )
    ]
    assert widths  # blocks render
    assert all(w <= gt.MAX_TIER_COL for w in widths)  # never exceeds the bound
    assert any(w < gt.MAX_TIER_COL for w in widths)  # right-sized where content allows


def test_persistent_hover_highlight_keyed_to_last_node(tmp_path):
    # The persistent-highlight contract: every block is keyed by a data-node id; the
    # controller records the last-hovered/focused node (data-hl) and never clears on
    # exit (no mouseleave/mouseout in the drill controller) -> no flash-on-exit.
    gt = load_script("gen_trajectory")
    assert "addEventListener('mouseover'" in gt.DRILL_SCRIPT
    assert "setAttribute('data-hl'" in gt.DRILL_SCRIPT  # keyed to the last node
    assert "mouseleave" not in gt.DRILL_SCRIPT and "mouseout" not in gt.DRILL_SCRIPT
    assert ".block.hl" in gt.DRILL_STYLE  # the persistent highlight style
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert re.search(r'class="block[^"]*"[^>]*data-node="', view)  # blocks are keyed


def test_leaf_wi_block_surfaces_delivery_phase(tmp_path):
    # OI-10 fix: the leaf work-item block's hover title carries the delivery Phase,
    # so it stays visible when the phase tier is flat but a workstream tier drills in.
    body = (
        "WI-001,A1,scripts,SR-001,,done,d,\n"
        "WI-002,A2,docs,SR-001,,done,d,\n"
        "WI-003,A3,unattended,SR-001,,done,d,\n"
        "WI-004,A4,self-adoption,SR-001,,done,d,\n"  # v1 spans 4 workstreams -> tiers
    )
    tiered_repo(tmp_path, body)  # all v1 (SR-001 Phase=v1), <=3 phases so phase flat
    assert gen(tmp_path).returncode == 0
    # the leaf work-item block's hover title carries the delivery phase (· v1)
    assert re.search(r"<title>WI-001 — [^<]*\(done\) · v1</title>", html_of(tmp_path))


# Four one-module components -> the How-SW top view exceeds the > 3 threshold.
FOUR_CMP_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component
LLR-001,SR-001,A,scripts/mod_a,run,d,(see TC),Verified,CMP-001
LLR-002,SR-001,B,scripts/mod_b,go,d,(see TC),Verified,CMP-002
LLR-003,SR-002,C,scripts/mod_c,gen,d,(see TC),Verified,CMP-003
LLR-004,SR-002,D,scripts/mod_d,emit,d,(see TC),Verified,CMP-004
"""
FOUR_CMPS = (
    "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
    "CMP-001,Core,software,,built,,,,\n"
    "CMP-002,Two,software,,built,,,,\n"
    "CMP-003,Three,software,,built,,,,\n"
    "CMP-004,Four,software,,built,,,,\n"
)


def test_how_sw_collapses_above_component_threshold(tmp_path):
    # > 3 top-level components -> the root layer holds four component blocks, each a
    # descend container (double-click / Enter to explode into its modules).
    containerize(tmp_path)
    req = tmp_path / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(FOUR_CMP_LLRS, encoding="utf-8")
    (req / "components.csv").write_text(FOUR_CMPS, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert "Top view: 4 item" in sw
    root = _sw_layer_with(sw, 'data-tier="component"')
    assert root.count('data-tier="component" data-descend=') == 4  # four descend blocks


def test_meta_tiered_when_view_smoke():
    # Over the real meta repo (4 workstreams > 3): the When view tiers into a
    # workstream block layer with work-item blocks at the bottom tier, rendered as a
    # wired drill diagram.
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    wis, integrity = ct.load_wis(ct.read_rows(ROOT / ct.WI_CSV))
    assert not integrity
    view = gt.when_view(ROOT, wis)
    assert view is not None
    assert 'class="drill"' in view and 'data-tier="workstream"' in view
    assert 'data-tier="work-item"' in view  # work items are the bottom tier
    assert 'class="port in"' in view and 'class="wire"' in view  # interface-wired


# --- WI-085 / SR-050: the Process reference tab ---------------------------------


def with_gate(root, gate="G2", wis_body=GOOD_WIS, header=WI_HEADER):
    """make_repo + a derived-format docs/gate (comment header, then the runnable
    gate value) — the Process tab's render condition."""
    make_repo(root, wis_body, header=header)
    (root / "docs" / "gate").write_text(
        "# DERIVED GATE - generated by scripts/derive_gate.py\n"
        "# basis: SN=1 SR=2 LLR=3 TC=4 drafts=0 computed={g} per-phase=(none)\n"
        "{g}\n".format(g=gate),
        encoding="utf-8",
    )
    return root


def test_process_tab_renders_three_panels_from_live_data(tmp_path):
    # SR-050: with a docs/gate the dashboard gains the Process tab — the three
    # linked panels, each joining a canonical data source (docs/gate, the spine
    # registries, work-items.csv) rather than restating hand-set numbers.
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-tab="process"' in text and 'id="process"' in text
    # the three panels are present and titled
    assert "Artifact lifecycle × gates" in text
    assert "The resume loop" in text
    assert "Slices → phase → gates" in text
    # panel 1 joins the spine registries (make_repo: 1 SN, 2 SR / 1 Verified,
    # 3 LLR, 4 TC) — live counts, not prose
    assert "1 SN" in text
    assert "2 SR · 1 verified" in text
    assert "3 LLR" in text and "4 TC" in text
    assert "1 of 2 SR verified" in text
    # panel 2 carries the real agent_loop phase vocabulary + escalation edges
    for phase in ("PLAN", "BUILD", "REVIEW-A/B", "CRITIQUE", "INTEGRATE"):
        assert phase in text
    assert "DESIGN-CHECK" in text and "Page the human" in text
    # panel 3 states the two bars and joins work-items.csv (4 WIs, 1 done)
    assert "commit bar" in text and "gate bar" in text
    assert "4 work items · 1 done." in text
    # still fully offline with the new tab present
    low = text.lower()
    assert "http://" not in low and "https://" not in low


# --- WI-273 / SR-052 (M-3): the tabs are a real WAI-ARIA tablist ---------------


def test_tabs_are_an_aria_tablist(tmp_path):
    # M-3: the view switcher used visual `.active` state only — a screen reader
    # was never told which view is selected or how buttons and panels relate. The
    # always-present arch/dag tabs now carry the full ARIA tabs pattern: a labelled
    # tablist, aria-selected on the tabs, tabpanel back-references, and a roving
    # tabindex (only the selected tab is in the tab sequence).
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'role="tablist"' in text and 'aria-label="Dashboard views"' in text
    # the initial (arch) tab is selected and the sole tab stop
    assert (
        '<button class="active" role="tab" id="tab-arch" data-tab="arch" '
        'aria-controls="arch" aria-selected="true" tabindex="0">'
    ) in text
    # every other tab starts unselected and out of the roving sequence
    assert (
        '<button role="tab" id="tab-dag" data-tab="dag" aria-controls="dag" '
        'aria-selected="false" tabindex="-1">'
    ) in text
    # panels are tabpanels wired to their tab; the inactive one is hidden
    assert (
        '<section id="arch" class="panel active" role="tabpanel" '
        'aria-labelledby="tab-arch">'
    ) in text
    assert (
        '<section id="dag" class="panel" role="tabpanel" '
        'aria-labelledby="tab-dag" hidden>'
    ) in text


def test_extra_tabs_carry_the_same_tab_semantics(tmp_path):
    # A dynamically-added tab (here How-SW, gated on a committed module map) gets
    # the identical role=tab / aria-controls / hidden-tabpanel wiring, starting
    # unselected — not just the visual button.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert (
        '<button role="tab" id="tab-sw" data-tab="sw" aria-controls="sw" '
        'aria-selected="false" tabindex="-1">'
    ) in text
    assert (
        '<section id="sw" class="panel" role="tabpanel" '
        'aria-labelledby="tab-sw" hidden>'
    ) in text


def test_every_tab_controls_a_labelled_panel(tmp_path):
    # The ARIA wiring must be complete for EVERY tab the dashboard emits: each
    # role=tab's aria-controls names a role=tabpanel whose aria-labelledby points
    # back at the tab's id. Rendered with the full optional set (How-SW + Process
    # + Knowledge) so a future tab that forgets the pattern trips here.
    make_repo(tmp_path)
    (tmp_path / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (tmp_path / "docs" / "gate").write_text(
        "# DERIVED GATE - generated by scripts/derive_gate.py\n"
        "# basis: SN=1 SR=2 LLR=3 TC=4 drafts=0 computed=G2 per-phase=(none)\n"
        "G2\n",
        encoding="utf-8",
    )
    assert gen_okf(tmp_path).returncode == 0
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)

    tabs = re.findall(r'<button[^>]*role="tab"[^>]*>', text)
    assert len(tabs) >= 5, tabs  # arch, dag, sw, know, process
    controls = {}  # panel id -> controlling tab id
    for t in tabs:
        tid = re.search(r'id="(tab-[^"]+)"', t).group(1)
        ctl = re.search(r'aria-controls="([^"]+)"', t).group(1)
        assert re.search(r'aria-selected="(true|false)"', t), t
        assert re.search(r'tabindex="(0|-1)"', t), t
        assert ctl not in controls, "two tabs control the same panel: " + ctl
        controls[ctl] = tid

    panels = re.findall(r'<section[^>]*role="tabpanel"[^>]*>', text)
    labelled = set()
    for p in panels:
        pid = re.search(r'id="([^"]+)"', p).group(1)
        lbl = re.search(r'aria-labelledby="([^"]+)"', p).group(1)
        assert pid in controls, "panel with no controlling tab: " + pid
        assert controls[pid] == lbl, (pid, lbl)  # the two cross-reference
        labelled.add(pid)
    # a bijection: exactly one tabpanel per tab, and vice versa
    assert labelled == set(controls)


def test_tab_controller_does_keyboard_and_roving_tabindex(tmp_path):
    # The ARIA tabs pattern is behavioural: Arrow/Home/End move + activate with a
    # roving tabindex, and aria-selected + panel `hidden` stay in sync. The suite
    # runs no browser, so the controller wiring is asserted as source (the render
    # critique validates it live).
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "querySelector('nav.tabs')" in text
    assert "querySelectorAll('[role=tab]')" in text
    for key in (
        "'ArrowRight'",
        "'ArrowLeft'",
        "'ArrowDown'",
        "'ArrowUp'",
        "'Home'",
        "'End'",
    ):
        assert key in text, key
    assert "setAttribute('aria-selected', on ? 'true' : 'false')" in text
    assert "panel.hidden = !on" in text
    assert "t.tabIndex = on ? 0 : -1" in text
    assert "tab.focus()" in text  # focus follows the roving selection


def test_tab_button_and_panel_helpers_emit_the_aria_pattern():
    gt = load_script("gen_trajectory")
    b = gt.tab_button("xy", "Label X")
    for frag in (
        'role="tab"',
        'id="tab-xy"',
        'data-tab="xy"',
        'aria-controls="xy"',
        'aria-selected="false"',
        'tabindex="-1"',
        ">Label X</button>",
    ):
        assert frag in b, frag
    assert gt.tab_panel_open("xy") == (
        '<section id="xy" class="panel" role="tabpanel"'
        ' aria-labelledby="tab-xy" hidden>'
    )


def test_process_current_gate_highlight_follows_docs_gate(tmp_path):
    # The current-gate highlight reflects docs/gate: a stage is `now` iff the
    # gate value falls in its declared gate span.
    with_gate(tmp_path, "G1")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "Current gate: <b>G1</b>" in text
    assert 'class="stg now" data-gates="G1"' in text  # SN
    assert 'class="stg now" data-gates="G1→G2"' in text  # SR
    assert 'class="stg" data-gates="G2"' in text  # LLR not yet
    assert 'class="stg" data-gates="G3"' in text  # code+tests not yet

    (tmp_path / "docs" / "gate").write_text("G3\n", encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "Current gate: <b>G3</b>" in text
    assert 'class="stg" data-gates="G1"' in text  # SN no longer highlighted
    assert 'class="stg now" data-gates="G2→G3"' in text  # TC
    assert 'class="stg now" data-gates="G3"' in text  # code+tests


def test_process_link_outs_prefer_the_scaffolded_docs(tmp_path):
    # Link-outs resolve in THIS repo: the scaffolded docs/ copies win when
    # present (the downstream case); with neither present the scaffolded
    # default is emitted (what bootstrap writes).
    with_gate(tmp_path)
    assert gen(tmp_path).returncode == 0
    assert 'href="docs/process.md"' in html_of(tmp_path)  # the default

    (tmp_path / "docs" / "process.md").write_text("# process\n", encoding="utf-8")
    (tmp_path / "docs" / "process-options.md").write_text("# opts\n", encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'href="docs/process.md"' in text
    assert 'href="docs/process-options.md"' in text


def test_process_wi_counts_join_work_items(tmp_path):
    # Panel 3's numbers are a live join over work-items.csv (total + done counts).
    with_gate(tmp_path, "G2", SMALL_WIS)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "4 work items · 1 done." in text


def test_process_tab_omitted_and_byte_identical_without_gate(tmp_path):
    # The vacuity guarantee (the Knowledge-tab idiom): with no docs/gate the tab
    # is omitted and the artifact is byte-for-byte what it was before this view
    # existed. Proven by round-trip: render gate-less, add the gate (tab
    # appears), remove it, re-render == the original bytes exactly.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    without = (tmp_path / "PROJECT_STATE.html").read_bytes()
    assert b'data-tab="process"' not in without

    (tmp_path / "docs" / "gate").write_text("G1\n", encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    assert b'data-tab="process"' in (tmp_path / "PROJECT_STATE.html").read_bytes()

    (tmp_path / "docs" / "gate").unlink()
    assert gen(tmp_path).returncode == 0
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == without


def test_process_tab_is_byte_deterministic_and_check_stable(tmp_path):
    # Sorted inputs, no clocks -> a second render is byte-identical and --check
    # passes fresh / trips stale (no new freshness exclusion).
    with_gate(tmp_path)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0
    # a gate flip is content: --check must trip until regenerated
    (tmp_path / "docs" / "gate").write_text("G3\n", encoding="utf-8")
    stale = gen(tmp_path, "--check")
    assert stale.returncode == 1 and "STALE" in stale.stderr


def test_meta_process_tab_smoke():
    # Over the real meta repo: the panel renders, the banner matches the real
    # docs/gate, and every link-out resolves (here the kit masters, since the
    # meta-repo scaffolds no docs/process.md).
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    wis, integrity = ct.load_wis(ct.read_rows(ROOT / ct.WI_CSV))
    assert not integrity
    out = gt.process_panel(ROOT, wis, gt.spine_stats(ROOT))
    assert out is not None
    tab, panel = out
    assert 'data-tab="process"' in tab
    gate = gt._gate_value(ROOT)
    assert gate and "Current gate: <b>{}</b>".format(gate) in panel
    hrefs = set(re.findall(r'href="([^"]+)"', panel))
    assert "project-trajectory/PROCESS.md" in hrefs
    for href in hrefs:
        assert (ROOT / href).exists(), href


# --- WI-142 / SR-055: the two circular working-loop panels ----------------------


def _loops_div(text):
    """The `<div class="loops">…</div>` block (Panel 4), balanced across its
    nested `<div>`s, sliced from the rendered panel/HTML."""
    start = text.index('<div class="loops">')
    depth, i = 0, start
    while i < len(text):
        if text.startswith("<div", i):
            depth += 1
        elif text.startswith("</div>", i):
            depth -= 1
            if depth == 0:
                return text[start : i + len("</div>")]
        i += 1
    raise AssertionError("unbalanced loops div")


def test_process_tab_renders_intake_and_decision_loops(tmp_path):
    # SR-055: the Process tab renders both circular loops as linked flow panels,
    # each with its ordered stages, and the gate-ratification stage lives in
    # loop B (the human-decision loop). WI-250: the render is a single SVG
    # drawing the loops as intersecting hoops, so the assertions target the SVG
    # structure (hoop discs, arrow-wired stage cards) rather than a CSS grid.
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "The working loops" in text
    loops = _loops_div(text)
    # one self-contained SVG with both named hoops
    assert 'class="loopsvg"' in loops
    assert "A · Intake loop" in loops and "B · Human-decision loop" in loops
    # loop A's ordered stage titles (each a card's bold <tspan> label)
    for stg in ("Intake", "Triage → WIs", "Resume loop", "Build / review", "Merge"):
        assert ">" + stg + "<" in loops, stg
    # loop B's ordered stage titles, incl. the gate-ratification stage
    for stg in ("Open items", "Human review", "Decisions record"):
        assert ">" + stg + "<" in loops, stg
    assert "gate-ratification table" in loops
    # the gate-ratification stage sits in loop B: its card carries a loop-B node
    # key, and it appears after the loop-B label emitted with that hoop.
    b_start = loops.index("B · Human-decision loop")
    assert loops.index("gate-ratification table") > b_start
    assert 'data-node="b-1"' in loops  # Open items — loop B, stage 1
    # Both hoops are explicitly closed cycles (hub → … → hub), not open rows.
    assert loops.count('data-cycle="closed"') == 2
    assert 'class="hoop hoop-a"' in loops
    assert 'class="hoop hoop-b"' in loops
    # still fully offline
    low = text.lower()
    assert "http://" not in low and "https://" not in low


def test_process_loops_share_one_llm_agent_entry(tmp_path):
    # The LLM_Agent entry hub is rendered exactly once as the shared central
    # junction of both hoops (not duplicated per loop).
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    loops = _loops_div(html_of(tmp_path))
    assert loops.count(">LLM_Agent<") == 1
    assert loops.count('class="hub"') == 1
    # both hoops are present around that one hub
    assert 'class="hoop hoop-a"' in loops and 'class="hoop hoop-b"' in loops


def test_process_loop_layout_is_a_shared_circular_junction(tmp_path):
    # WI-250: the render draws two overlapping hoop discs whose directed edges
    # (one arrowhead each) trace each loop and converge on the single shared hub.
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    loops = _loops_div(text)
    # two hoop discs, each a closed cycle, sharing one hub
    assert loops.count('class="hoop hoop-') == 2
    assert loops.count('data-cycle="closed"') == 2
    assert loops.count('class="hub"') == 1
    # every loop edge is directional: hub→s1→…→sn→hub is (n+1) arrows per loop,
    # 6 for the 5-stage intake loop + 5 for the 4-stage decision loop = 11.
    assert loops.count('marker-end="url(#floparrow)"') == 11
    # the SVG-loop CSS replaced the old grid racetrack entirely.
    assert "#process .loopsvg{" in text
    assert "#process .hoop{" in text
    assert "#process .loops{display:grid" not in text
    assert "#process div.loop{" not in text
    assert "#process .pflow.loop" not in text


def test_process_loop_stage_links_resolve():
    # Over the real meta repo (where every canonical home exists): each stage
    # links to its canonical doc and every emitted href resolves.
    gt = load_script("gen_trajectory")
    loops = gt._loop_panel(ROOT)
    hrefs = re.findall(r'href="([^"]+)"', loops)
    assert hrefs, "loop stages should link to their canonical homes"
    for href in hrefs:
        assert (ROOT / href).exists(), href
    # every canonical home named by SR-055 is linked (docs/next-wi retired, WI-180:
    # the Resume-loop stage now links the WI registry it derives the frontier from)
    for home in (
        "docs/status.md",
        "docs/requirements/work-items.csv",
        # WI-322: the human-decision loop lands on the GENERATED owner surface,
        # not the retired markdown file.
        "docs/open-items.html",
        "docs/log.md",
    ):
        assert 'href="{}"'.format(home) in loops, home


def test_process_loops_byte_identical_without_data(tmp_path):
    # The loop structure is the method's, not the repo's data: the loops block
    # renders byte-for-byte the same whether the registry is minimal or
    # work-item-rich (SR-055 "a data-less repo renders byte-identically").
    minimal = tmp_path / "min"
    minimal.mkdir()
    with_gate(minimal, "G2")
    assert gen(minimal).returncode == 0
    rich = tmp_path / "rich"
    rich.mkdir()
    with_gate(rich, "G2", SMALL_WIS)
    assert gen(rich).returncode == 0
    assert _loops_div(html_of(minimal)) == _loops_div(html_of(rich))


# --- WI-144: the 042-CRITIQUE rubric-meeting build round (dashboard-*.md) -------
# Regression guards for the six rubric-meeting fixes (A4/U4/A3/U3/U1 done here;
# T2 knowledge-density is the round's handed-off remainder). These guard the build
# against regressions; they are NOT the owner-gated formal TC-HARDEN cases (the
# per-<text> WCAG parse / dead-selector / legend-per-fill TCs route via §5 intake).


def _wcag(fg, bg):
    def lum(h):
        h = h.lstrip("#")
        chan = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
        f = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chan]
        return 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2]

    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def test_a4_node_fills_meet_the_wcag_floor():
    # dashboard-accessibility.md A4: every node fill keeps >= 4.5:1 for its label
    # text. Node text is #fff except the queued status (dark #0f172a on the light
    # gray), so every fill in the shared palette must clear the floor with one of
    # those two — the darkened palette this build lands.
    gt = load_script("gen_trajectory")
    white_fills = set(gt.STATUS_FILL.values()) - {gt.STATUS_FILL["queued"]}
    white_fills |= set(gt.TIER_FILL.values())
    white_fills |= set(gt.SW_NODE_FILL.values())
    white_fills |= set(gt.OKF_TYPE_FILL.values())
    white_fills |= set(gt.PHASE_ACCENTS)
    for fill in sorted(white_fills):
        assert _wcag("#ffffff", fill) >= 4.5, (fill, _wcag("#ffffff", fill))
    # the queued fill carries dark text instead
    assert _wcag("#0f172a", gt.STATUS_FILL["queued"]) >= 4.5


def test_a4_every_emitted_dashboard_contrast_pair_meets_floor():
    """TC-HARDEN: computed colors must catch badge/boundary/focus regressions."""
    gt = load_script("gen_trajectory")
    for status, fill in gt.STATUS_FILL.items():
        ink = "#0f172a" if status == "queued" else "#ffffff"
        assert _wcag(ink, fill) >= 4.5, (status, ink, fill)
    for fill in gt.PHASE_ACCENTS:
        assert _wcag("#ffffff", fill) >= 4.5, fill
    assert _wcag("#64748b", "#ffffff") >= 3
    assert _wcag("#64748b", "#0f172a") >= 3
    assert _wcag("#b45309", "#ffffff") >= 3


def test_every_emitted_interactive_selector_matches_a_node(tmp_path):
    """TC-HARDEN: controller selectors must not silently target dead markup."""
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    assert re.search(r'class="block[^>]*data-wi="WI-\d+"', page)
    assert re.search(r'class="block[^>]*data-node="[^"]+"', page)
    assert re.search(r'class="block[^>]*data-node="[^"]+"(?![^>]*data-wi=)', page)


def test_every_multifill_panel_emits_a_palette_bijection_legend(tmp_path):
    """TC-HARDEN: every phase fill is explained exactly once in the When legend."""
    gt = load_script("gen_trajectory")
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    # WI-294b: the phase legend is the `.legend` div immediately following the
    # When drill's summary paragraph (no more bespoke `phaselegend` marker class).
    anchor = "crossing edges).</p>"
    legend = page.split(anchor, 1)[1].split("</div>", 1)[0]
    swatches = re.findall(r'<i style="background:(#[0-9a-f]{6})">', legend)
    assert set(swatches) == set(gt.PHASE_ACCENTS[: len(swatches)])
    assert swatches
    assert len(swatches) == len(set(swatches))


def test_a4_no_sub_label_opacity_discount(tmp_path):
    # A4: the emitted CSS must not discount sub-label text opacity (which dropped
    # the effective contrast below the floor). No `.sub`/`.bsub`/`.hubsub`
    # `{ ... opacity }` — `.hubsub` joined the rule in WI-293, where a surviving
    # `fill-opacity:.85` put the dark-theme hub sub-label at 2.57:1.
    # Fixture is with_gate, not with_bundle: `.hubsub` only exists once the
    # Process tab renders, so under with_bundle this guard was vacuous for it.
    with_gate(tmp_path, "G2")
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    assert ".hubsub{" in css, "Process tab did not render — guard would be vacuous"
    assert re.search(r"\.(?:sub|bsub|hubsub)\s*\{[^}]*opacity", css) is None


def _css_var(css, name, dark=False):
    """The value of custom property `name` as declared for the light (`:root`) or
    dark (`prefers-color-scheme: dark`) theme in the emitted stylesheet. Dark
    falls back to the light declaration, which is what the cascade does when the
    dark block does not override the token."""
    if dark:
        block = css.split("prefers-color-scheme: dark", 1)[1].split("}", 1)[0]
        hit = re.search(re.escape(name) + r":\s*(#[0-9a-fA-F]{3,8})", block)
        if hit:
            return hit.group(1)
    root = css.split(":root", 1)[1]
    return re.search(re.escape(name) + r":\s*(#[0-9a-fA-F]{3,8})", root).group(1)


def test_a4_theme_token_fills_behind_white_text_meet_the_floor(tmp_path):
    """TC-HARDEN (WI-293): a fill declared as a THEME TOKEN must clear the floor
    in BOTH themes, not just the one it was designed in.

    The sibling A4 tests check palette CONSTANTS (STATUS_FILL, PHASE_ACCENTS, …),
    so a `fill:var(--token)` whose value differs per theme was invisible to them —
    which is exactly how the Process hub shipped white-on-#818cf8 at 2.98:1 in
    dark while measuring 6.29:1 in light. Any token used as a fill behind white
    text is checked against both declarations here.
    """
    with_gate(tmp_path, "G2")  # the Process tab's render condition
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    # every custom property used as a fill under a white-text selector
    white_text_fill_tokens = {"--hub"}
    assert "fill:var(--hub)" in css, "hub fill token missing from emitted CSS"
    for token in sorted(white_text_fill_tokens):
        for dark in (False, True):
            value = _css_var(css, token, dark=dark)
            ratio = _wcag("#ffffff", value)
            assert ratio >= 4.5, (token, "dark" if dark else "light", value, ratio)


def test_a4_hub_fill_is_not_the_page_accent(tmp_path):
    """WI-293 regression guard: --accent is tuned as INK on the page background
    and lightens in dark theme, so re-pointing the hub fill at it silently
    reintroduces the 2.98:1 defect. The hub keeps its own token."""
    with_gate(tmp_path, "G2")  # the Process tab's render condition
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    hub_rule = re.search(r"#process \.hub rect\{([^}]*)\}", css)
    assert hub_rule, "hub rect rule missing"
    assert "var(--accent)" not in hub_rule.group(1), hub_rule.group(1)


def test_a3_status_glyph_pairs_every_status_fill(tmp_path):
    # dashboard-accessibility.md A3 (no info by colour alone): a drill work-item
    # block pairs its status fill with a shape-distinct glyph in the visible label.
    gt = load_script("gen_trajectory")
    # One glyph per STATUS, not per fill (WI-272). Six statuses share four
    # swatches, so pairing glyphs with fills would have left `deferred`/`blocked`
    # — the two that share `queued`'s swatch — with no non-colour cue at all,
    # which is precisely the case A3 exists for.
    assert set(gt.STATUS_GLYPH) == set(gt.STATUS_BUCKET)
    assert set(gt.STATUS_BUCKET.values()) == set(gt.STATUS_FILL)
    assert len(set(gt.STATUS_GLYPH.values())) == len(gt.STATUS_GLYPH), (
        "two statuses share a glyph — the shape cue stops distinguishing them"
    )
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    leaf = _layer_with(html_of(tmp_path), 'data-tier="work-item"')
    labels = re.findall(r'class="blab">([^<]*)</tspan>', leaf)
    assert labels, "no work-item blocks rendered"
    glyphs = set(gt.STATUS_GLYPH.values())
    for lab in labels:
        assert lab[0] in glyphs, lab  # every leaf label is glyph-prefixed


def test_u4_when_drill_blocks_wire_to_the_detail_panel(tmp_path):
    # dashboard-{uniformity U4, usability T3, accessibility A1}: the When drill's
    # leaf blocks advertise their bare id (`data-wi`) and the page wires
    # click/focus-for-detail to them — the panel was previously dead (`#dag .wi`
    # matched zero drill blocks).
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = html_of(tmp_path)
    assert re.search(r'class="block[^"]*"[^>]*data-wi="WI-\d+"', view)
    assert ".block[data-wi]" in view  # the wiring loop targets the drill blocks


def test_u3_sw_drill_has_a_legend_and_a_wired_detail_aside(tmp_path):
    # dashboard-uniformity.md U3: the How-SW drill gets the same legend + detail
    # aside its sibling When drill has (fills were explained nowhere; no aside).
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert 'class="legend"' in sw and 'id="sw-detail"' in sw
    assert "module" in sw and "external actor" in sw  # node-kind legend entries
    assert ".block[data-node]" in sw  # the detail wiring targets the sw blocks


def test_u3_phase_legend_renders_through_the_shared_legend_component(tmp_path):
    """dashboard-uniformity.md U1/U3 (WI-294b, 119-CRITIQUE): the When tab's
    phase-accent key used to be a bespoke `span.ph`/`.phaselegend` idiom — a
    smaller swatch (.55rem vs .8rem), an inline "Phase accent:" prefix, and
    placement inside the drill's summary paragraph rather than below the card
    like every other legend (the status legend on the SAME tab, and the
    Knowledge/How-SW legends). It now renders through the identical
    `.legend`/`<i>` component those use."""
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    # the bespoke idiom is gone: no per-emitter swatch rule, no chip markup
    assert "span.ph" not in page
    assert "phaselegend" not in page
    assert 'class="ph"' not in page
    # the phase key now emits the shared component's exact markup shape
    assert re.search(
        r'<div class="legend">(<span><i style="background:#[0-9a-f]{6}"></i>[^<]+</span>)+</div>',
        page,
    )


# WI-309: the U1 residue ("whether the resulting sizes read as visually
# uniform") was undecidable only because the scale was never DECLARED. Declare
# it and the question becomes set membership — which is this test.

# The three families, and why there are three rather than one. A `rem` inside an
# SVG would resize labels out of boxes whose geometry is fixed px; an `em` sizes
# against its parent, which is the point for inline `code`. Claiming "one scale"
# across them would be false, so the invariant is "every size names a declared
# step", not "every size shares one unit".
TYPE_SCALE_FAMILIES = {
    "node (px, fixed SVG geometry)": ["--nlabel", "--nsub", "--nhead"],
    "page (rem, scales with root)": [
        "--tiny",
        "--xsmall",
        "--small",
        "--body",
        "--lead",
        "--display",
        "--hero",
    ],
    "relative (em, sizes against parent)": ["--rel"],
}


def _style_surfaces(html):
    """Only where a font-size actually PAINTS: `<style>` blocks and inline
    `style=` attributes. The rendered document also *quotes* CSS inside prose
    (a registry Detail cell explaining a past palette fix names
    `font-size:13px`), and a naive whole-document scan reads that as a
    declaration — judging documentation as if it were code."""
    blocks = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S)
    blocks += re.findall(r'style="([^"]*)"', html)
    return blocks


def test_u1_every_font_size_resolves_to_a_declared_scale_step(tmp_path):
    """dashboard-uniformity.md U1 core (WI-309): one declared type scale.

    Before this, 18 raw literals sat against 5 tokens — `.7rem`/`.75rem`,
    `.9`/`.95`/`.98rem`, `1.05`/`1.1rem`, `8.5px`/`9px` each being near-duplicate
    steps for ONE role, 3-7% apart. No reader distinguishes those; no rule
    justified them; and "do the sizes read as uniform?" cannot be answered about
    a scale nobody wrote down.
    """
    declared = {t for fam in TYPE_SCALE_FAMILIES.values() for t in fam}

    for label, html in _every_emitter_document(tmp_path):
        # every declared step is defined exactly once, with a real value
        for token in declared:
            defs = re.findall(
                re.escape(token) + r"\s*:\s*([0-9.]+(?:px|rem|em))\s*;", html
            )
            assert len(defs) == 1, (label, token, defs)

        used = []
        for surface in _style_surfaces(html):
            used += re.findall(r"font-size\s*:\s*([^;}\"']+)", surface)
        assert used, "vacuous — no font-size found in {}".format(label)

        raw = sorted({v.strip() for v in used if not v.strip().startswith("var(")})
        assert not raw, (
            "in the {} render, font-size(s) bypass the declared scale: {} — add a "
            "step with a stated role, or reuse the nearest one".format(label, raw)
        )
        unknown = sorted(
            {
                v.strip()
                for v in used
                if v.strip().startswith("var(")
                and re.sub(r"var\(\s*|\s*\)", "", v.strip()) not in declared
            }
        )
        assert not unknown, (label, unknown)

    # ...and the declared set stays SMALL. A scale that grows a step per call
    # site is not a scale; this is the pressure that forces the merge decision.
    assert len(declared) <= 12, sorted(declared)


# WI-310: the U3 residue ("spacing, exact visual weight") measured as drift —
# 8 stroke-widths, 7 opacities, 5 corner radii, with FIVE stroke widths doing the
# single job "draw a connector". Same declare-then-assert shape as the type scale.
WEIGHT_TOKENS = {
    "stroke-width": ["--w-hair", "--w-node", "--w-line", "--w-emph"],
    "opacity": [
        "--o-wash",
        "--o-dim",
        "--o-ghost",
        "--o-soft",
        "--o-muted",
        "--o-full",
    ],
    "border-radius": ["--r-chip", "--r-ctl", "--r-card", "--r-pill"],
}


def test_u3_every_weight_value_resolves_to_a_declared_token(tmp_path):
    """dashboard-uniformity.md U3 core (WI-310): one declared token per role for
    the properties that carry visual weight.

    `stroke-opacity` is checked under `opacity` deliberately — it is the same
    scale applied to a stroke, and letting it keep its own literals would leave
    the exact hole this closes.
    """
    for label, html in _every_emitter_document(tmp_path):
        for prop, tokens in WEIGHT_TOKENS.items():
            for token in tokens:
                defs = re.findall(re.escape(token) + r"\s*:\s*([^;]+);", html)
                assert len(defs) == 1, (label, token, defs)

            used = []
            for surface in _style_surfaces(html):
                # (?<![-\w]) so `stroke-opacity` is not eaten by `opacity`
                used += re.findall(
                    r"(?<![-\w])" + re.escape(prop) + r"\s*:\s*([^;}\"']+)", surface
                )
                if prop == "opacity":
                    used += re.findall(r"stroke-opacity\s*:\s*([^;}\"']+)", surface)
            if not used:
                continue  # this render does not exercise the property
            raw = sorted({v.strip() for v in used if not v.strip().startswith("var(")})
            assert not raw, (
                "in the {} render, {} value(s) bypass the declared tokens: {} — "
                "name the role or reuse the nearest step".format(label, prop, raw)
            )
            unknown = sorted(
                {
                    re.sub(r"var\(\s*|\s*\)", "", v.strip())
                    for v in used
                    if re.sub(r"var\(\s*|\s*\)", "", v.strip()) not in tokens
                }
            )
            assert not unknown, (label, prop, unknown)


def test_u3_svg_corner_radii_match_the_declared_scale(tmp_path):
    """U3 core, the SVG half (WI-310): `rx` is a presentation attribute and
    cannot read a CSS custom property portably, so `SVG_RX` is its declaration
    and this closes the loop — asserting the DECLARATION against both the source
    literals and every rendered document, so the tuple cannot quietly disagree
    with what the emitters actually draw.
    """
    gt = load_script("gen_trajectory")
    declared = set(gt.SVG_RX)
    assert declared, "SVG_RX is empty"

    src = (SCRIPTS / "gen_trajectory.py").read_text(encoding="utf-8")
    in_source = set(re.findall(r'\brx="([0-9.]+)"', src))
    assert in_source <= declared, (
        "rect template(s) draw an undeclared corner radius {} — add the role to "
        "SVG_RX or reuse a declared step".format(sorted(in_source - declared))
    )
    assert in_source, "vacuous — no rx literal found in the emitters"

    for label, html in _every_emitter_document(tmp_path):
        rendered = set(re.findall(r'\brx="([0-9.]+)"', html))
        assert rendered <= declared, (label, sorted(rendered - declared))


# WI-311: the U5 residue ("near-duplicate but non-identical hues") turned out to
# be the SAME arithmetic the phase check already did, on a set nobody had
# widened. Two floors, both judgements, both recorded here rather than in a
# commit message:
#
#   WITHIN a vocabulary — 15. Every member can sit beside every other in one
#   legend, so the bar is the strict one the phase accents already met.
#   ACROSS vocabularies — 12. Two colours from different vocabularies meet less
#   often (a status fill and a phase accent share no legend), so the bar is
#   lower — but not absent, because 120-CRITIQUE reported a reader conflating
#   exactly such a pair. 12 clears every confirmed conflation without forcing a
#   wholesale re-hue; the closest surviving pair is 12.5.
U5_FLOOR_WITHIN, U5_FLOOR_CROSS = 15.0, 12.0


def _palette_vocabularies(gt):
    """`{name: {key: hex}}` for every declared colour vocabulary."""
    return {
        "status": dict(gt.STATUS_FILL),
        "tier": dict(gt.TIER_FILL),
        "okf": dict(gt.OKF_TYPE_FILL),
        "sw": dict(gt.SW_NODE_FILL),
        "phase": {str(i): h for i, h in enumerate(gt.PHASE_ACCENTS)},
    }


# tier <-> okf is a DECLARED mirror: one concept wearing two label systems, so
# the pair is exempt by design rather than by convenience.
U5_MIRROR = {
    ("tier", "sn"): ("okf", "Stakeholder Need"),
    ("tier", "sr"): ("okf", "System Requirement"),
    ("tier", "llr"): ("okf", "Low-Level Requirement"),
    ("tier", "tc"): ("okf", "Test Case"),
}


def _u5_is_mirror(va, ka, vb, kb):
    return U5_MIRROR.get((va, ka)) == (vb, kb) or U5_MIRROR.get((vb, kb)) == (va, ka)


def test_u5_pairwise_deltae_holds_within_and_across_every_vocabulary():
    """dashboard-uniformity.md U5 core, the residue half (WI-311).

    `test_u5_phase_accents_clear_a_pairwise_deltae_floor` already applied ΔE —
    but only inside `PHASE_ACCENTS`, which is why "a reader perceives a collision
    the identity check misses" could be written off as perceptual. It is not: it
    is the same formula on the set nobody widened. When this was first run it
    found three real conflations, worst 8.6.
    """
    gt = load_script("gen_trajectory")
    vocabs = _palette_vocabularies(gt)
    flat = [(v, k, h) for v, d in vocabs.items() for k, h in d.items()]
    assert len(flat) >= 20, "vacuous — too few declared colours: {}".format(len(flat))

    worst = []
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            va, ka, ha = flat[i]
            vb, kb, hb = flat[j]
            if _u5_is_mirror(va, ka, vb, kb):
                assert ha == hb, ("a declared mirror must be byte-equal", ha, hb)
                continue
            floor = U5_FLOOR_WITHIN if va == vb else U5_FLOOR_CROSS
            d = _delta_e76(ha, hb)
            if d < floor:
                worst.append((round(d, 1), floor, va, ka, ha, vb, kb, hb))
    assert not worst, (
        "colour pair(s) below the perceptual floor — a reader cannot reliably "
        "tell these apart: {}".format(sorted(worst))
    )


# WI-312: the A2 residue ("whether each control READS as well-named"). Presence
# was already checked; QUALITY was not, and quality is largely mechanical.
#
# SCOPE, corrected during the build and worth stating: A2 governs INTERACTIVE
# elements and meaningful graphics. The first measurement counted every `<title>`
# in the document and reported 57 bare-id names — but those sit on EDGE PATHS
# (`<path class="wire"><title>IF-001</title>`), which are neither focusable nor
# named graphics. A tooltip on a decorative connector is a usability nicety, not
# an accessible-name defect, and asserting over it would have manufactured 57
# findings that WCAG does not make. Measured over the right set, the real defect
# was one: three drills each labelling their breadcrumb landmark "Breadcrumb".
_BARE_ID = re.compile(r"(?:WI|SR|SN|LLR|TC|IF|CMP)-\d+")


def _named_controls(html):
    """`[(kind, name), …]` for every focusable element and role=img graphic."""
    out = []
    for m in re.finditer(r"<(g|svg|button|nav)\b([^>]*)>", html):
        tag, attrs = m.group(1), m.group(2)
        if not (
            'tabindex="0"' in attrs or 'role="img"' in attrs or tag in ("button", "nav")
        ):
            continue
        aria = re.search(r'aria-label="([^"]*)"', attrs)
        if aria:
            out.append((tag, aria.group(1)))
            continue
        tail = html[m.end() : m.end() + 400]
        title = re.match(r"\s*<title>([^<]*)</title>", tail)
        if title:
            out.append((tag, title.group(1)))
            continue
        text = re.sub(r"<[^>]+>", "", tail.split("</" + tag + ">")[0]).strip()
        out.append((tag, text))
    return out


def test_a2_every_control_name_is_present_and_not_a_bare_id(tmp_path):
    """dashboard-accessibility.md A2 core, the QUALITY half (WI-312).

    A name that is merely present can still be useless. Two rules that hold
    everywhere: a control must HAVE a name, and that name must not be a bare
    registry id — `IF-001` tells a screen-reader user nothing about what the
    control is or does.
    """
    for label, html in _every_emitter_document(tmp_path):
        controls = _named_controls(html)
        # 10, not a bigger round number: the smallest fixture legitimately
        # renders 18 controls, and a floor tuned to the largest render would
        # fail honest small projects rather than catch a vacuous sweep.
        assert len(controls) >= 10, "vacuous — {} found {} controls".format(
            label, len(controls)
        )
        unnamed = [c for c in controls if not c[1].strip()]
        assert not unnamed, (label, "controls with no accessible name", unnamed[:5])
        bare = [c for c in controls if _BARE_ID.fullmatch(c[1].strip())]
        assert not bare, (
            "in the {} render, control(s) are named by a bare registry id, which "
            "says nothing about what they are: {}".format(label, bare[:5])
        )


def test_a2_landmark_names_are_distinct(tmp_path):
    """A2 quality, the uniqueness half (WI-312).

    Scoped to LANDMARKS (`<nav>`), deliberately. A screen-reader user listing a
    page's navigation regions hears their names as a flat list, so two called
    "Breadcrumb" are indistinguishable — which is exactly what three drills
    each emitting `aria-label="Breadcrumb"` produced.

    NOT asserted document-wide: a descend control for the same container
    legitimately appears in several drill layers, and only one layer is visible
    at a time, so those repeats are the same control reached by different paths
    rather than an ambiguity a reader ever faces.

    Note this rule is carried mainly by the SHIPPED artifact: each fixture below
    renders a single drill, so only a document with two or more navs exercises
    it (the `< 2` skip). That is a real coverage limit — verified by reverting
    the fix, which fails here only once the dashboard is regenerated.
    """
    for label, html in _every_emitter_document(tmp_path):
        names = re.findall(r"<nav\b[^>]*aria-label=\"([^\"]*)\"", html)
        if len(names) < 2:
            continue
        assert len(set(names)) == len(names), (
            "in the {} render, navigation landmarks share a name — a reader "
            "listing them cannot tell which is which: {}".format(label, sorted(names))
        )


def test_u1_process_tab_type_scale_matches_the_shared_tokens(tmp_path):
    """dashboard-uniformity.md U1 (WI-295, 119-CRITIQUE MINOR): the Process tab's
    "working loops" SVG (`.stgt`/`.stgn`/`.hooplab`/`.hubname`) used to hardcode
    12px/9.5px/13px/13px, deviating from the --nlabel:10px/--nsub:8.5px every
    other emitter (icicle/dag/knowledge) shares. `.stgt`/`.stgn` are the same
    per-node-label role as --nlabel/--nsub and now reuse them directly;
    `.hooplab`/`.hubname` are a once-per-diagram HEADLINE label, a genuinely
    different role, so they get the ONE documented scale step --nhead (not two
    independently drifting magic numbers)."""
    with_gate(tmp_path, "G2")  # the Process tab's render condition
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    assert "--nhead:" in css
    assert "#process .stgt{fill:var(--text);font-size:var(--nlabel)" in css
    assert "#process .stgn{fill:var(--muted);font-size:var(--nsub)" in css
    assert "#process .hooplab{fill:var(--accent);font-size:var(--nhead)" in css
    assert "#process .hubname{fill:#fff;font-size:var(--nhead)" in css
    # no ad-hoc px sizes remain on these four selectors
    for selector in (".stgt", ".stgn", ".hooplab", ".hubname"):
        rule = re.search(r"#process " + re.escape(selector) + r"\{([^}]*)\}", css)
        assert rule, selector
        assert "px" not in rule.group(1), (selector, rule.group(1))


def test_u1_node_labels_share_one_type_scale(tmp_path):
    # dashboard-uniformity.md U1: one shared node-label / sub-label size across the
    # emitters — declared once as CSS vars, referenced (no per-emitter px override).
    # The icicle + knowledge rules render in any bundle repo; the drill `.blab`
    # rule needs a tiered (drill) render.
    with_bundle(tmp_path / "bundle")
    assert gen(tmp_path / "bundle").returncode == 0
    css = html_of(tmp_path / "bundle")
    assert "--nlabel:" in css and "--nsub:" in css
    assert "#ice .cell text { fill:#fff; font-size:var(--nlabel)" in css
    assert "#knowgraph .knode text{fill:#fff;font-size:var(--nlabel)" in css
    # the specific per-emitter node-label overrides this build removed are gone
    assert "#ice .cell text { fill:#fff; font-size:10px" not in css
    assert "#knowgraph .knode text{fill:#fff;font-size:9px" not in css

    tiered_repo(tmp_path / "drill", TIER_UNION_WIS)
    assert gen(tmp_path / "drill").returncode == 0
    assert ".blab{font-size:var(--nlabel)" in html_of(tmp_path / "drill")


def _lab(hexcolor):
    """CIE L*a*b* for a `#rrggbb` string, sRGB D65 (matches the palette comment's
    deltaE convention). Pure-Python — no numpy dependency for one small check."""
    h = hexcolor.lstrip("#")
    rgb = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92 for c in rgb]
    r, g, b = [c * 100 for c in rgb]
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    xn, yn, zn = 95.047, 100.0, 108.883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t + 16 / 116)

    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def _delta_e76(h1, h2):
    l1, a1, b1 = _lab(h1)
    l2, a2, b2 = _lab(h2)
    return ((l1 - l2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2) ** 0.5


def test_u5_no_hex_reused_across_unrelated_colour_vocabularies():
    """dashboard-uniformity.md U5 (WI-292, 119-CRITIQUE BLOCKER): one hue must
    carry one meaning across the whole document. Hex-collision half of the core:
    no value may repeat across STATUS_FILL / TIER_FILL / OKF_TYPE_FILL /
    SW_NODE_FILL / PHASE_ACCENTS EXCEPT the intentional TIER_FILL<->OKF_TYPE_FILL
    SN/SR/LLR/TC mirror (one concept, two label systems) and the CSS `--accent`
    token, which PHASE_ACCENTS must also never equal (the focus/hover ring is
    painted in `--accent`, so a phase sharing it makes that phase's ring
    invisible — 119-CRITIQUE A4/T5)."""
    gt = load_script("gen_trajectory")
    tier_to_type = {
        "sn": "Stakeholder Need",
        "sr": "System Requirement",
        "llr": "Low-Level Requirement",
        "tc": "Test Case",
    }
    for tier, type_name in tier_to_type.items():
        assert gt.TIER_FILL[tier] == gt.OKF_TYPE_FILL[type_name], (
            tier,
            type_name,
        )  # the mirror must pair the SAME concept, not merely reuse the same set
    mirror = set(gt.TIER_FILL[t] for t in tier_to_type)

    vocabs = {
        "status": set(gt.STATUS_FILL.values()),
        "tier+type": mirror
        | {gt.OKF_TYPE_FILL["Interface"], gt.OKF_TYPE_FILL["Process Guide"]},
        "sw": set(gt.SW_NODE_FILL.values()),
        "phase": set(gt.PHASE_ACCENTS),
    }
    names = list(vocabs)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            collide = vocabs[names[i]] & vocabs[names[j]]
            assert not collide, (names[i], names[j], collide)

    accent_light, accent_dark = "#4f46e5", "#818cf8"
    for fill in gt.PHASE_ACCENTS:
        assert fill.lower() not in (accent_light, accent_dark), fill


def test_u5_phase_accents_clear_a_pairwise_deltae_floor():
    """U5 core, pairwise half: PHASE_ACCENTS is judged as a rendered legend where
    every swatch can sit beside every other one, so the floor is PAIRWISE, not
    merely adjacent-in-declaration-order — the exact metric gap (WI-247's
    validator checked adjacent pairs only) that let two indistinguishable violets
    ship (075-CRITIQUE T5 / 119-CRITIQUE precursor)."""
    gt = load_script("gen_trajectory")
    accents = gt.PHASE_ACCENTS
    worst = min(
        _delta_e76(accents[i], accents[j])
        for i in range(len(accents))
        for j in range(i + 1, len(accents))
    )
    assert worst >= 15, worst


def test_a4_ring_ink_clears_the_3to1_floor_against_every_node_fill():
    """dashboard-accessibility.md A4 (WI-299, 119-CRITIQUE BLOCKER) +
    dashboard-usability.md T5: `_ring_ink` picks whichever of white/near-black
    contrasts more against a fill, so it must clear the 3:1 UI-boundary floor for
    EVERY fill the dashboard actually uses — not just the ones a hand-picked
    example happened to check."""
    gt = load_script("gen_trajectory")
    fills = (
        set(gt.STATUS_FILL.values())
        | set(gt.TIER_FILL.values())
        | set(gt.OKF_TYPE_FILL.values())
        | set(gt.SW_NODE_FILL.values())
        | set(gt.PHASE_ACCENTS)
    )
    for fill in sorted(fills):
        ink = gt._ring_ink(fill)
        # WI-317: the ink set is CLOSED, not incidental — the containment-arrow
        # markers are emitted one per ink, so a third value would ship an arrow
        # head with no marker to paint it.
        assert ink in gt.RING_INKS, (fill, ink, gt.RING_INKS)
        assert _wcag(ink, fill) >= 3, (fill, ink, _wcag(ink, fill))


def _theme_tokens(css, name):
    """The light and dark values of a CSS custom property, in that order (light
    `:root` first, then the `prefers-color-scheme: dark` block) — the same
    two-value shape `test_drill_focus_ring_is_distinct_from_the_active_accent`
    relies on."""
    vals = re.findall(r"--{}:(#[0-9a-f]{{3,8}})".format(name), css)
    assert len(vals) == 2, (name, vals)
    return vals


def _cedge_paint(rule_value, block_ring, accent):
    """Resolve what a browser paints for a `.cedge` shaft/head declaration, given
    the host block's inline `--ring` (absent for a theme-token fill) and the
    theme's `--accent`. Mirrors CSS `var()` fallback: `var(--ring,X)` takes the
    block's ring when it declares one, else X."""
    m = re.fullmatch(r"var\(--ring,(.+)\)", rule_value)
    if m:
        return block_ring or _cedge_paint(m.group(1), block_ring, accent)
    if rule_value == "var(--accent)":
        return accent
    assert rule_value.startswith("#"), rule_value  # a fixed hue, resolved as-is
    return rule_value


def test_t5_containment_arrow_clears_the_3to1_floor_against_every_host_fill(tmp_path):
    """dashboard-usability.md T5 / LLR-105 (WI-317, found by the WI-305 train's
    critique 2026-07-26): the containment arrow — the `.cedge` shaft plus its
    `cedgearrow` marker head — is painted INSIDE the host block, over that
    block's own fill, and it is the affordance a reader must find to descend a
    tier. So T5's 3:1 UI-boundary floor applies to it exactly as it applied to
    the focus ring WI-299 fixed, and the failure mode is the identical one:
    a single fixed hue (`var(--accent)`) vanishes on whichever fill happens to
    match it — measured 1.06:1 in light (#4f46e5 on the phase-1 #0369a1) and
    1.99:1 in dark (#818cf8 on the same fill). The paint must derive from the
    host fill's contrast-safe control token (`--ring`, LLR-105's machinery), and
    the arithmetic must close over EVERY declared fill, not a sampled one."""
    gt = load_script("gen_trajectory")
    shaft = re.search(r"\.drill \.cedge\{[^}]*stroke:([^;]+);", gt.DRILL_STYLE).group(1)
    head = re.search(r"\.drill \.cedgehead\{fill:([^;]+);", gt.DRILL_STYLE).group(1)

    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    accents = _theme_tokens(css, "accent")

    # 1. Arithmetic over the CLOSED vocabulary: every fill a descendable block can
    #    carry, in both themes — the LLR-105 closure, not a hand-picked example.
    fills = (
        set(gt.STATUS_FILL.values())
        | set(gt.TIER_FILL.values())
        | set(gt.OKF_TYPE_FILL.values())
        | set(gt.SW_NODE_FILL.values())
        | set(gt.PHASE_ACCENTS)
    )
    for fill in sorted(fills):
        ring = gt._ring_ink(fill)
        for accent in accents:
            for paint in (
                _cedge_paint(shaft, ring, accent),
                _cedge_paint(head, ring, accent),
            ):
                assert _wcag(paint, fill) >= 3, (fill, paint, _wcag(paint, fill))

    # 2. The theme-token fills (`var(--surface)` containers) keep the fallback
    #    paint, so it must clear the floor against the resolved surface too.
    for surface, accent in zip(_theme_tokens(css, "surface"), accents):
        for paint in (
            _cedge_paint(shaft, None, accent),
            _cedge_paint(head, None, accent),
        ):
            assert _wcag(paint, surface) >= 3, (surface, paint, _wcag(paint, surface))

    # 3. RENDERED, not merely declared: every emitted arrow sits in a block whose
    #    marker head resolves to that block's own ring (a shared head painted from
    #    one hue is exactly the defect — the shaft alone passing is not enough).
    blocks = [b for b in css.split('<g class="block ') if 'class="cedge"' in b]
    assert blocks, "no containment arrows emitted"
    for b in blocks:
        block = b.split("</g>", 1)[0]
        ring = re.search(r"--ring:(#[0-9a-f]{6})", block)
        marker = re.search(r'class="cedge"[^>]*marker-end="url\(#([^)]+)\)"', block)
        assert marker, block[:200]
        mdef = re.search(
            r'<marker id="{}"[^>]*?(?: style="--ring:(#[0-9a-f]{{6}})")?>'.format(
                re.escape(marker.group(1))
            ),
            css,
        )
        assert mdef, marker.group(1)
        assert mdef.group(1) == (ring.group(1) if ring else None), (
            marker.group(1),
            mdef.group(1),
            ring.group(1) if ring else None,
        )


# --- T6 theme-lock (WI-314): the anchor's mechanized core --------------------
#
# "Every surface's background/text token resolves from one theme set; no mid-page
# inversion" (the WI-300 per-anchor table, residue NONE). The measurable content
# is FAMILY PAIRING, not "no literals": a fixed status swatch carrying fixed
# white ink is theme-locked *correctly* — it never flips, and neither does its
# ink. What inverts a page is a MIXED pair (a theme-varying ink on a fixed fill,
# or fixed ink on a theme-varying surface) or a SECOND theme mechanism scoped
# below `:root`. Those are what these guards forbid.
T6_HOST_DERIVED_TOKENS = {
    # `--ring` is stamped per node (`_ring_style`) and per marker (`_cedge_marker`)
    # FROM the host fill, so it is invariant-with-an-invariant-host and varying-
    # with-a-varying-host by construction — dual by design, not unclassified.
    # Its pairing obligation is the 3:1 floor LLR-105/TC-108 own.
    "--ring",
}


def _theme_families(css):
    """`(varying, invariant)` — the CSS custom properties that change with the
    theme versus those deliberately declared once. Derived from the emitted
    document (the dark block's override set IS the definition of varying), never
    hand-listed, so a new token joins a family by existing."""
    root = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
    light = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", root))
    dark_block = re.search(
        r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{(.*?)\}", css, re.S
    ).group(1)
    dark = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);?", dark_block))
    assert not set(dark) - set(light), (
        "the dark block overrides token(s) `:root` never declares — a surface "
        "that exists in only one theme: {}".format(sorted(set(dark) - set(light)))
    )
    return set(dark), set(light) - set(dark)


def _paint_family(value, varying):
    """`"varying"`, `"invariant"`, or None (not a colour) for one paint value —
    resolving `var(--token)` through the family split above."""
    value = value.strip()
    m = re.match(r"var\(\s*(--[\w-]+)", value)
    if m:
        if m.group(1) in T6_HOST_DERIVED_TOKENS:
            return None
        return "varying" if m.group(1) in varying else "invariant"
    return (
        "invariant" if re.match(r"#[0-9a-fA-F]{3,8}$|rgba?\(|hsla?\(", value) else None
    )


def _css_rules(css):
    return [
        (m.group(1).strip(), m.group(2))
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css)
    ]


def _decl(body, prop):
    m = re.search(r"(?:^|[;\s])" + prop + r"\s*:\s*([^;}]+)", body)
    return m.group(1).strip() if m else None


def test_t6_theme_lock_has_one_mechanism_and_no_mixed_family_pair(tmp_path):
    """dashboard-usability.md T6 / LLR-117 (WI-314): the dashboard renders in one
    theme at a time, applied to the whole page — no tab, panel, or node flips to
    the opposite theme mid-view. Mechanized as the two ways that can actually
    break: a theme mechanism scoped below `:root` (a second
    `prefers-color-scheme` block, or a per-component `color-scheme`), and a
    surface/ink pair drawn from two different theme families.

    Swept over EVERY emitter, not one fixture, for the A2 review's reason: a
    document walk judges only what its fixture renders, and the emitter that
    does not render is where the violation hides."""
    gt = load_script("gen_trajectory")
    vocabulary = (
        set(gt.STATUS_FILL.values())
        | set(gt.TIER_FILL.values())
        | set(gt.OKF_TYPE_FILL.values())
        | set(gt.SW_NODE_FILL.values())
        | set(gt.PHASE_ACCENTS)
    )
    nodes, pairs, seen, text_fills = 0, 0, set(), {}
    for label, html in _every_emitter_document(tmp_path):
        css = "\n".join(re.findall(r"<style>(.*?)</style>", html, re.S))
        varying, invariant = _theme_families(css)
        assert varying and invariant, (label, sorted(varying), len(invariant))

        # 1. ONE mechanism, at the root. A second block — or one scoped to a
        #    component — is precisely a mid-page seam.
        blocks = re.findall(
            r"@media\s*\([^)]*prefers-color-scheme[^)]*\)\s*\{\s*([^\s{]+)", css
        )
        assert blocks == [":root"], (label, blocks)
        schemes = [
            s.strip() for s in re.findall(r"([^{}]*)\{[^{}]*color-scheme\s*:", css)
        ]
        assert schemes == [":root"], (label, schemes)

        # 2. The page's own surface pair follows the theme — if `body` painted a
        #    fixed background or ink, the whole document would be theme-locked to
        #    one side while every card kept flipping.
        body_rule = next(
            b for s, b in _css_rules(css) if s.split(",")[0].strip() == "body"
        )
        for prop in ("background", "color"):
            assert _paint_family(_decl(body_rule, prop), varying) == "varying", (
                label,
                prop,
                _decl(body_rule, prop),
            )
        pairs += _assert_no_mixed_css_rule(label, css, varying)
        nodes += _assert_no_mixed_svg_node(label, html, varying)
        _collect_css_text_fills(html, css, varying, text_fills)
        # 6. No ad-hoc theme-locked SURFACE. Every rect fill is either a theme
        #    token (it flips) or a member of a declared colour vocabulary (a
        #    node, deliberately invariant, and A4's arithmetic already owns its
        #    ink). A literal outside both would be a fixed panel — the seam a
        #    reader crosses that the pair checks above cannot see, because a
        #    background rect carries no text of its own.
        for fill in set(re.findall(r'<rect\b[^>]*fill="([^"]+)"', html)):
            assert fill.startswith("var(") or fill in vocabulary, (label, fill)
            seen.add(_paint_family(fill, varying))
    for sel, (fams, hosts) in sorted(text_fills.items()):
        assert len(fams) == 1, (sel, fams)  # one rule, one family, every emitter
        # a text paint with a host anywhere in the sweep must match that host's
        # family; one with no host anywhere lands on the page and must follow it
        assert hosts == fams if hosts else fams == {"varying"}, (sel, fams, hosts)
    assert pairs >= 1, "vacuous — no bg/ink rule pair classified at all"
    assert nodes >= 50, "vacuous — only {} node pair(s) classified".format(nodes)
    assert len(text_fills) >= 4, "vacuous — {} css text fill(s)".format(len(text_fills))
    # both families must actually occur, or the sweep proves nothing about mixing
    assert {"varying", "invariant"} <= seen, seen


def _assert_no_mixed_css_rule(label, css, varying):
    """3. No CSS rule pairs a background and an ink from two families. Stated
    plainly rather than dressed up: the page CSS has exactly ONE rule that
    declares a classifiable background AND ink today — `body` (the rest pair an
    ink with `background:none`) — so this check's value is prospective, and the
    sweep's weight is carried by 4 and 5. The one badge idiom that pairs both
    inline is composed in JS from the invariant vocabulary, where A4's
    arithmetic (LLR-114) already owns the pairing."""
    pairs = 0
    for sel, body in _css_rules(css):
        bg = _decl(body, "background(?:-color)?")
        ink = _decl(body, "color")
        fams = {_paint_family(bg or "", varying), _paint_family(ink or "", varying)}
        if bg and ink and None not in fams:
            pairs += 1
            assert len(fams) == 1, (label, sel[:70], bg, ink, fams)
    return pairs


def _assert_no_mixed_svg_node(label, html, varying):
    """4. Same rule for every emitted SVG node: an inline rect fill and the
    inline text fill drawn on it must come from one family."""
    nodes = 0
    for g in re.findall(r"<g\b[^>]*>.*?</g>", html, re.S):
        rect = re.search(r'<rect\b[^>]*fill="([^"]+)"', g)
        text = re.search(r'<text\b[^>]*fill="([^"]+)"', g)
        if not (rect and text):
            continue
        fams = {
            _paint_family(rect.group(1), varying),
            _paint_family(text.group(1), varying),
        }
        if None in fams:
            continue
        nodes += 1
        assert len(fams) == 1, (label, rect.group(1), text.group(1), fams)
    return nodes


def _collect_css_text_fills(html, css, varying, into):
    """5. The CSS-driven half: an SVG text fill declared in a rule, paired
    against the family its host nodes actually paint in the artifact — derived
    per selector, not a hand-copied list.

    Accumulated ACROSS the sweep before judging, because "this selector has no
    host rect here" is ambiguous in a single document: it means either "the
    paint lands on the page background" (`#ice .lane-head`) or "this emitter
    does not render those nodes" (`#ice .cell` in the shipped artifact, where
    WI-306's start-collapsed drill replaced the flat icicle). Only a selector
    with no host anywhere is the former."""
    for sel, body in _css_rules(css):
        fill = _decl(body, "fill")
        if not fill or not re.search(r"\btext\b|\btspan\b", sel):
            continue
        fam = _paint_family(fill, varying)
        if fam is None:
            continue
        host = re.sub(r"\s+(?:text|tspan)\b.*$", "", sel.split(",")[0].strip())
        seen_fam, seen_hosts = into.setdefault(sel, (set(), set()))
        seen_fam.add(fam)
        seen_hosts |= _host_rect_families(html, host, varying)


def _host_rect_families(html, selector, varying):
    """The paint families of the rects belonging to `#id .cls[.cls2]` in the
    emitted document — the host surface a CSS-declared text fill lands on.
    Empty when the selector names no rect-bearing node (a lane head, an arrow
    marker), which is itself the signal that the paint sits on the page."""
    m = re.match(r"#([\w-]+)\s+\.([\w.-]+)$", selector)
    if not m:
        return set()
    region = html.split('id="{}"'.format(m.group(1)), 1)
    if len(region) < 2:
        return set()
    wanted = set(m.group(2).split("."))
    fams = set()
    for g in re.findall(r"<g\b[^>]*>.*?</g>", region[1].split("</svg>", 1)[0], re.S):
        cls = re.search(r'class="([^"]*)"', g)
        rect = re.search(r'<rect\b[^>]*fill="([^"]+)"', g)
        if not (cls and rect) or not wanted <= set(cls.group(1).split()):
            continue
        fam = _paint_family(rect.group(1), varying)
        if fam:
            fams.add(fam)
    return fams


def test_u3_ring_token_is_the_one_highlight_idiom_across_every_emitter(tmp_path):
    """dashboard-uniformity.md U3/U4 (WI-294a, 119-CRITIQUE): the hover/focus
    highlight ring used to be `var(--accent)` in the drill emitters (When/How-SW)
    but a hardcoded `#f59e0b` amber in the icicle/flat-DAG/knowledge emitters —
    two idioms for the same "this node is highlighted" concept. All four now
    read the SAME `--ring` custom property (with each emitter's old hue kept
    only as the CSS fallback), and each node carries its own computed `--ring`
    value inline so the ring clears contrast against ITS fill specifically."""
    tiered_repo(tmp_path / "drill", TIER_UNION_WIS)
    assert gen(tmp_path / "drill").returncode == 0
    css = html_of(tmp_path / "drill")
    assert ".drill .block:focus rect{stroke:var(--ring,var(--accent))" in css
    assert ".drill .block.hl rect{stroke:var(--ring,var(--accent))" in css
    assert "#ice .cell.hl rect { stroke:var(--ring,#f59e0b)" in css
    assert "#dag .wi.hl rect { stroke:var(--ring,#f59e0b)" in css
    # every emitter actually stamps a per-node --ring value, not just the CSS
    assert re.search(r'class="cell [^"]*"[^>]*style="--ring:#[0-9a-f]{6}"', css)
    assert re.search(r'class="block [^"]*"[^>]*style="--ring:#[0-9a-f]{6}"', css)

    # the Knowledge tab's top-view `.knode` flat graph only renders for a
    # <= 3-type OKF bundle (_flat_bundle) — with_bundle's SN/SR/LLR/TC spans 4
    # types, which earns the tiered drill above the threshold instead (T2).
    _flat_bundle(tmp_path / "flat")
    assert gen(tmp_path / "flat").returncode == 0
    know_css = html_of(tmp_path / "flat")
    assert "#knowgraph .knode.hl rect{stroke:var(--ring,#f59e0b)" in know_css
    assert re.search(r'class="knode"[^>]*style="--ring:#[0-9a-f]{6}"', know_css)


def test_a3_flat_dag_fallback_also_prefixes_the_status_glyph(tmp_path):
    # dashboard-accessibility A3 (046-REVIEW-A): the <=3-tier flat `dag_svg`
    # fallback (a small registry that never tiers) must encode status by the same
    # visible glyph the drill uses, not by fill hue alone. GOOD_WIS renders flat.
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)  # 4 WIs, 2 workstreams, no phases -> flat SVG DAG
    assert gen(tmp_path).returncode == 0
    dag = html_of(tmp_path).split('id="dag-view"', 1)[1].split("</svg>", 1)[0]
    wids = re.findall(r'class="wid">([^<]*)</tspan>', dag)
    assert wids, "no flat-DAG work-item labels rendered"
    glyphs = set(gt.STATUS_GLYPH.values())
    for lab in wids:
        assert lab[0] in glyphs, lab  # every id label is glyph-prefixed


def test_a1_drill_leaf_blocks_are_keyboard_focusable(tmp_path):
    # dashboard-accessibility A1 (048 BLOCKER): a leaf drill block carries a
    # click/focus detail handler (`.block[data-wi]`/`[data-node]`), so it must be
    # keyboard-focusable — not only the descend containers. Every block is now
    # `tabindex="0"`, and a leaf `data-wi` block is reachable by keyboard.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    leaf = _layer_with(html_of(tmp_path), 'data-tier="work-item"')
    blocks = re.findall(r"<g (class=\"block[^>]*)>", leaf)
    assert blocks, "no leaf work-item blocks rendered"
    for b in blocks:
        assert 'tabindex="0"' in b, b  # focusable
    # and the leaf carrying the panel wiring is itself focusable (not a container)
    assert re.search(r'tabindex="0"[^>]*data-wi="WI-\d+"', leaf)


def _svg_subtrees(text):
    """(open-tag, body) for every EMITTED <svg> — the views nest no <svg> inside
    another, so a non-greedy split is exact once the decoys are gone.

    Two decoys, both found by adversarial review of the first draft. The embedded
    JSON <script> blobs carry registry prose that can contain a literal `<svg>`
    (LLR-101's own text does), which both invents a phantom subtree and greedily
    swallows ~112 KB up to the next real `</svg>` — hiding a real container from
    the walk. So strip <script> regions first, and require the tag to carry at
    least one attribute (every emitted svg has viewBox/class; a bare `<svg>` in
    prose has none)."""
    text = re.sub(r"<script\b.*?</script>", "", text, flags=re.S)
    return re.findall(r"(<svg\s[^>]*>)(.*?)</svg>", text, re.S)


def _focusable_count(body):
    """Focusable descendants of an svg body: `tabindex` in any quoting, plus SVG
    `<a href>`, which is natively tab-ordered and so carries no tabindex."""
    return len(re.findall(r"tabindex\s*=|<a\s[^>]*href\s*=", body, re.I))


def _named(tag, body):
    """Does this svg have an accessible name? `aria-label` on the element, or a
    FIRST-DIRECT-CHILD <title> — per SVG-AAM a <title> nested inside a <g> names
    that <g>, not the svg, so accepting any descendant <title> would pass an
    unnamed graphic."""
    return "aria-label=" in tag or re.match(r"\s*<title[\s>]", body) is not None


def test_a2_no_focusable_node_sits_inside_a_children_presentational_svg(tmp_path):
    # dashboard-accessibility A2 (WI-297): role="img" is CHILDREN-PRESENTATIONAL —
    # ARIA expects the subtree pruned — so a graph holding focusable nodes must not
    # declare it, or the per-node <title>s A2 rests on may never reach a screen
    # reader and the nodes may be unreachable. Measured before the fix: 1,146 of the
    # document's 1,150 tabindex elements sat inside a role="img" subtree.
    #
    # This is the mechanized core of A2 and the reason the 116/004/118 critiques
    # split: they argued about container NAMING while the ROLE was pruning the
    # children. It asserts the invariant over the WHOLE emitted document, so any
    # future emitter that adds focusable nodes under role="img" fails here.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    subtrees = _svg_subtrees(text)
    assert subtrees, "no <svg> emitted"
    assert _focusable_count(text), "fixture emitted no focusable nodes — vacuous pass"
    for tag, body in subtrees:
        if 'role="img"' in tag:
            assert not _focusable_count(body), (
                "role=img (children-presentational) over focusable descendants: " + tag
            )
            # a genuinely non-interactive graphic still owes its own name
            assert _named(tag, body), "role=img with no accessible name: " + tag


def test_a2_role_predicate_counts_native_links_as_focusable():
    # The unit half, and the regression guard for the defect adversarial review
    # found in the first draft: focusability is NOT only `tabindex`. An SVG <a> with
    # an href is natively tab-ordered and so carries none, and a tabindex-only
    # predicate classified the loops diagram (9 linked stage cards, each with a
    # <title>) as a non-interactive graphic — leaving role="img" over exactly the
    # elements A2 protects. Also pins the quoting-agnostic and no-false-positive
    # halves, since `esc()` renders prose links as `&lt;a href`.
    gt = load_script("gen_trajectory")
    assert (
        gt._svg_role('<a href="docs/status.md" class="stg"><title>x</title></a>')
        != "img"
    )
    assert gt._svg_role('<g tabindex="0"><title>n</title></g>') != "img"
    assert gt._svg_role("<g tabindex=0></g>") != "img"
    assert gt._svg_role("<g tabindex = '0'></g>") != "img"
    # a genuinely static graphic still earns img, and escaped prose cannot forge a hit
    assert (
        gt._svg_role('<path d="M0 0"/><text>&lt;a href="x"&gt; in prose</text>')
        == "img"
    )


def test_a2_the_repos_own_shipped_dashboard_holds_the_invariant():
    # The document walk above can only judge the emitters its FIXTURE renders —
    # adversarial review measured that at 2 of 6, and the one genuine violation
    # lived in an emitter the fixture never rendered. This asserts the same
    # invariant over the artifact this repo actually ships, which exercises every
    # emitter that really renders (the loops diagram among them).
    #
    # The invariant is "not children-presentational", NOT "is role=group": dropping
    # the role (inheriting the SVG-AAM graphics-document default) or declaring
    # role="graphics-document" satisfies A2 equally, and the test must not pin one
    # implementation when LLR-101 does not.
    shipped = ROOT / "PROJECT_STATE.html"
    if not shipped.is_file():
        import pytest

        pytest.skip("no committed dashboard in this checkout")
    subtrees = _svg_subtrees(shipped.read_text(encoding="utf-8"))
    assert len(subtrees) >= 10, "decoy-stripping went wrong: {}".format(len(subtrees))
    offenders = [
        (tag[:80], _focusable_count(body))
        for tag, body in subtrees
        if 'role="img"' in tag and _focusable_count(body)
    ]
    assert not offenders, "children-presentational role over focusables: {}".format(
        offenders
    )
    assert sum(_focusable_count(b) for _, b in subtrees), "vacuous — no focusables"


# --- WI-306 / SR-054 T2: the What icicle earns its tiering by scale -----------
# 119-CRITIQUE MAJOR: the landing What view rendered the WHOLE spine at leaf
# scale (one unit per TC), opening as a multi-screen wall while the three wired
# tabs correctly opened at a summary layer. Capping DEPTH would not have fixed
# it - height is leaf-proportional, so stopping at the SR lane still stacks one
# unit per SR - so the summary has to be a coarser TIER: one block per SN,
# descend on click, earned above the SR-089 `>3` rule like its sibling views.

_T2_SN_HEADER = (
    "# Stakeholder Needs (SN-###)\n\n"
    "| SN-ID | Need | Why it matters | Priority | Acceptance intent |\n"
    "|---|---|---|---|---|\n"
)


def _spine_with_sns(root, n):
    """Rewrite the fixture spine to span `n` SNs, each with one SR/LLR/TC - the
    scale knob the `>3` rule turns on."""
    req = root / "docs" / "requirements"
    (req / "stakeholder-needs.md").write_text(
        _T2_SN_HEADER
        + "".join(
            "| SN-{i:03d} | Need {i}. | Matters {i}. | M | works {i}. |\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )
    (req / "system-requirements.csv").write_text(
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
        + "".join(
            'SR-{i:03d},Req {i},SN-{i:03d},"Shall {i}.",R,"ac {i}",,M,Test,'
            "Verified\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
        + "".join(
            'LLR-{i:03d},SR-{i:03d},Low {i},src/m.py,f{i},"d {i}",(see TC),'
            "Verified\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,"
        "Evidence,Status\n"
        + "".join(
            'TC-{i:03d},SR-{i:03d};LLR-{i:03d},Unit,m {i},Smoke,"p","e {i}",Yes,'
            "tests/t.py::t{i},Verified\n".format(i=i)
            for i in range(1, n + 1)
        ),
        encoding="utf-8",
    )


def test_t2_what_icicle_starts_collapsed_above_the_sn_threshold(tmp_path):
    # Above the `>3` rule the What view is a start-collapsed drill: one descend
    # block per SN in the root layer, one child layer each, and the deep TC cells
    # sit in HIDDEN child layers - not in the initially-shown root, which is the
    # wall the anchor forbids.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-drill="archdrill"' in text
    assert text.count('data-descend="archl-sn-') == 8
    assert text.count('data-layer="archl-sn-') == 8
    root_layer = text.split('data-layer="arch-root"', 1)[1].split("</div>", 1)[0]
    assert "SN-001" in root_layer
    assert "TC-001" not in root_layer  # no leaf cells in the opening view


def test_t2_small_spine_keeps_the_flat_icicle(tmp_path):
    # At or below 3 SNs the tiering is NOT earned: the flat icicle renders, so a
    # small project never pays for a drill it cannot need - the same symmetry the
    # When and Knowledge views hold to.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 3)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-drill="archdrill"' not in text
    assert "TC-001" in text  # deep cells render inline, unhidden


# --- WI-307 / SR-054 T7 + T4: every diagram scales to fit, with a floor -------
# 119-CRITIQUE T7 and the WI-305 train critique (T7 + T4): every emitted SVG
# carried a FIXED pixel width, so at 390px all four views demanded "Scroll
# sideways to see the full view" and cut off right-side lanes, and the How graph
# clipped `CMP-002 - Generators` mid-label. A viewBox alone cannot fix that - the
# fixed width pins the rendered size. These guards hold the responsive sizing on
# EVERY emitter (the defect was per-wrapper, so a per-view test would miss a
# fourth emitter added later) and pin the legibility floor that keeps the fix
# from trading T7 for T4.

_FIT_RE = re.compile(
    r'style="width:100%;max-width:(\d+)px;min-width:(\d+)px;height:auto"'
)


def test_t7_every_emitted_svg_scales_to_fit(tmp_path):
    # Derived from the emitted document, not a hand list: EVERY <svg> must carry
    # the responsive style, and none may keep a bare fixed width. A new emitter
    # that forgets it fails here.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    svgs = re.findall(r"<svg\b[^>]*>", text)
    assert svgs, "vacuous - no svg emitted"
    missing = [t[:90] for t in svgs if "width:100%" not in t]
    assert not missing, "svg(s) without responsive sizing: {}".format(missing)
    # A fixed width with no fit style is the exact pre-fix shape.
    assert not re.findall(r'<svg viewBox="[^"]*" width="\d+"(?! style=)', text)


def test_t7_shrink_floor_keeps_labels_legible(tmp_path):
    # The floor is the T4 half: pure scale-to-fit would squeeze a wide graph into
    # 390px and shrink a 12px label past readable, so min-width pins how far the
    # diagram may shrink. Assert the emitted ratio matches the declared constant
    # rather than re-hardcoding it (one home for the number).
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    pairs = _FIT_RE.findall(html_of(tmp_path))
    assert pairs, "vacuous - no responsive svg found"
    for natural, floor in pairs:
        expected = int(float(natural) * gt.SHRINK_FLOOR)
        assert abs(int(floor) - expected) <= 1, (natural, floor, expected)
    assert 0 < gt.SHRINK_FLOOR < 1


# --- WI-318 / SR-054 T4: no label ink outside the block it belongs to ---------
# 121-CRITIQUE MAJOR: the What/Architecture root layer drew each SN's whole need
# as the block's sub-label, unwrapped — one centred line that began outside the
# left edge of its box and ran past the right one, at 390px AND at 1680px, so the
# text was unreadable AS a label and broke the box too. `_tier_col_width` cannot
# absorb it: it clamps at MAX_TIER_COL, so a 400-character need asks for a 2000px
# column and gets 172.
#
# The binding is the T4 anchor's mechanizable floor, stated geometrically and
# swept over the EMITTED document: every `<tspan>` a drill block renders must fit
# inside that block's own rect, horizontally and vertically. Deliberately not a
# per-view assertion — the defect lives in the one shared label emitter that feeds
# four views, so a fifth view added later is covered without touching this test.
_BLOCK_RE = re.compile(r'<g class="block\b.*?</g>', re.S)
_BRECT_RE = re.compile(
    r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="([\d.]+)"'
)
_BTEXT_RE = re.compile(r'<text x="[-\d.]+" y="([-\d.]+)"[^>]*>(.*?)</text>', re.S)
_BSPAN_RE = re.compile(
    r'<tspan x="([-\d.]+)" dy="([-\d.]+)" class="(blab|bsub)">([^<]*)</tspan>'
)
# Conservative vertical glyph extents as a fraction of the declared font size:
# enough of an over-estimate that a real render cannot exceed them.
_ASCENT, _DESCENT = 0.8, 0.25


def _label_boxes(html_text):
    """Every drill-block label line as (block, class, text, ink-rect, block-rect),
    measured from the emitted markup with the emitter's own declared per-character
    widths and the font sizes the emitted CSS declares."""
    gt = load_script("gen_trajectory")
    size = {
        cls: float(re.search(r"--{}:([\d.]+)px".format(var), html_text).group(1))
        for cls, var in (("blab", "nlabel"), ("bsub", "nsub"))
    }
    per_char = {"blab": gt._BLAB_CH, "bsub": gt._BSUB_CH}
    out = []
    for block in _BLOCK_RE.findall(html_text):
        rect = _BRECT_RE.search(block)
        text = _BTEXT_RE.search(block)
        if not rect or not text:
            continue
        rx, ry, rw, rh = (float(v) for v in rect.groups())
        baseline = float(text.group(1))
        node = re.search(r'data-node="([^"]*)"', block)
        for x, dy, cls, raw in _BSPAN_RE.findall(text.group(2)):
            baseline += float(dy)
            # Entities are ONE glyph: measuring `&#x27;` as six characters would
            # invent overflow on every apostrophe.
            width = len(html.unescape(raw)) * per_char[cls]
            cx = float(x)
            out.append(
                (
                    node.group(1) if node else "?",
                    cls,
                    raw,
                    (
                        cx - width / 2,
                        baseline - size[cls] * _ASCENT,
                        cx + width / 2,
                        baseline + size[cls] * _DESCENT,
                    ),
                    (rx, ry, rx + rw, ry + rh),
                )
            )
    return out


_LONG_NEED = (  # the real SN-001, the row the critic read at 390px and 1680px
    "A team can drop the kit into a new or existing repo and get a working "
    "gated, requirement-traced process without hand-building the tooling."
)


def _spine_with_a_long_need(root, n=8):
    """The tiered spine fixture with ONE realistic sentence-length need, so the
    sweep below is exercised against the shape that actually overflowed."""
    _spine_with_sns(root, n)
    sn = root / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(
        sn.read_text(encoding="utf-8").replace("| Need 1. |", "| " + _LONG_NEED + " |"),
        encoding="utf-8",
    )


def test_t4_no_block_label_renders_outside_its_own_box(tmp_path):
    make_repo(tmp_path)
    _spine_with_a_long_need(tmp_path)
    assert gen(tmp_path).returncode == 0
    boxes = _label_boxes(html_of(tmp_path))
    assert boxes, "vacuous - no drill block labels emitted"
    # Non-vacuity with teeth: the sentence-length need must actually be in there,
    # or this sweep proves nothing about the defect it was written for.
    assert any(_LONG_NEED.split()[0] in raw for _n, _c, raw, _i, _b in boxes)
    outside = [
        (node, cls, raw, ink, box)
        for node, cls, raw, ink, box in boxes
        if ink[0] < box[0] or ink[1] < box[1] or ink[2] > box[2] or ink[3] > box[3]
    ]
    assert not outside, "label ink outside its block: {}".format(outside[:4])


def test_t4_a_sentence_length_sub_label_wraps_and_ellipsizes(tmp_path):
    # The fix path itself: too long for one line -> a second line, then an
    # ellipsis. (The full string keeps its homes on the block: <title>,
    # aria-label, data-summary.)
    make_repo(tmp_path)
    _spine_with_a_long_need(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    block = next(
        b for b in _BLOCK_RE.findall(text) if 'data-node="SN-001"' in b and "…" in b
    )
    subs = re.findall(r'class="bsub">([^<]*)</tspan>', block)
    assert len(subs) == 2, subs
    assert subs[0] and not subs[0].endswith("…")  # broke on a word, not mid-word
    assert subs[1].endswith("…")
    assert _LONG_NEED.startswith(html.unescape(subs[0]))
    assert _LONG_NEED in text  # the whole need still reads, via <title>/summary


def test_t4_a_short_sub_label_keeps_the_two_line_grid(tmp_path):
    # The wrap is earned by length, not applied to everything: a sub that already
    # fits renders on the untouched two-line grid.
    make_repo(tmp_path)
    _spine_with_sns(tmp_path, 8)
    assert gen(tmp_path).returncode == 0
    block = next(
        b for b in _BLOCK_RE.findall(html_of(tmp_path)) if 'data-node="SN-002"' in b
    )
    assert 'dy="-2" class="blab"' in block and 'dy="13" class="bsub"' in block
    assert len(re.findall(r'class="bsub"', block)) == 1


def test_fit_lines_breaks_on_words_then_ellipsizes():
    gt = load_script("gen_trajectory")
    assert gt._fit_lines("", 10, 2) == []
    assert gt._fit_lines("short", 10, 2) == ["short"]  # untouched when it fits
    assert gt._fit_lines("one two three", 8, 2) == ["one two", "three"]
    # More text than the budget holds: the last line ends in an ellipsis and no
    # line exceeds the budget.
    got = gt._fit_lines("aa bb cc dd ee ff gg", 8, 2)
    assert got == ["aa bb cc", "dd ee f…"], got
    assert all(len(line) <= 8 for line in got)
    # A single word longer than the budget is cut, never allowed to run past.
    assert gt._fit_lines("supercalifragilistic", 8, 2) == ["supercal", "ifragil…"]


def test_t1_hero_names_the_active_work_item(tmp_path):
    # dashboard-usability T1 (048): the landing hero names the in-flight work item
    # (id + title) so finding "the next work" costs zero tab switches. WI-002 is
    # the active row in GOOD_WIS.
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    hero = text.split('class="hero"', 1)[1].split("</section>", 1)[0]
    assert 'class="sub nowat"' in hero
    assert "WI-002" in hero and "Harness" in hero  # id + title on the hero


def test_t1_hero_active_line_absent_when_nothing_is_active(tmp_path):
    # T1: no active WI -> no hero active line (empty markup, not a stray label).
    wis = (
        "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
        "WI-002,Release,docs,SR-002,WI-001,queued,shipped\n"
    )
    make_repo(tmp_path, wis)
    assert gen(tmp_path).returncode == 0
    assert 'class="sub nowat"' not in html_of(tmp_path)


# --- WI-305 (SR-054 T1): the landing "Next work" surface -----------------------
# 119-CRITIQUE's MAJOR: "find the next work" had no path — with 0 active rows
# nothing marked "you are here" and the only route to a queued item was drilling
# nested When blocks. The fix surfaces the scheduler's ready frontier (the SAME
# derivation IF-071 projects to status.md) on the landing view. The scheduler
# fails a bare row closed as `unclassified`, so these fixtures carry the minimal
# SafetyClass=ordinary signal (mirroring test_trajectory._FRONTIER_HEADER).
NW_HEADER = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SafetyClass\n"
)


def _hero_of(root):
    text = html_of(root)
    return text.split('class="hero"', 1)[1].split("</section>", 1)[0]


def test_t1_next_work_names_the_ready_frontier_with_zero_active(tmp_path):
    # The exact critique bad case: nothing is active, yet the next work must be
    # named ON THE LANDING VIEW (zero tab switches), not buried in the When drill.
    wis = (
        "WI-001,Bootstrap,scripts,SR-001,,done,adder,ordinary\n"
        "WI-002,Harness,scripts,SR-001,WI-001,queued,harness,ordinary\n"
        "WI-003,Subtraction,scripts,SR-002,WI-001,queued,subber,ordinary\n"
    )
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    hero = _hero_of(tmp_path)
    # no active row -> the old nowat line is absent, but the next-work path exists
    assert 'class="sub nowat"' not in hero
    assert 'class="card nextwork"' in hero
    assert "Next work" in hero
    # both dependency-ready WIs are named on the landing surface
    assert "WI-002" in hero and "WI-003" in hero
    # a `done` WI never appears as next work
    assert "WI-001" not in hero.split('class="nwlist"', 1)[1].split("</ul>", 1)[0]


def test_t1_next_work_annotates_the_blocking_predecessor(tmp_path):
    # A queued WI whose hard predecessor is not yet done is surfaced WITH the
    # predecessor that blocks it (the critique's "named, with their blocking
    # predecessor").
    wis = (
        "WI-001,Groundwork,scripts,SR-001,,queued,ground,ordinary\n"
        "WI-002,Release,docs,SR-002,WI-001,queued,shipped,ordinary\n"
    )
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    hero = _hero_of(tmp_path)
    assert 'class="card nextwork"' in hero
    assert "WI-001" in hero and "WI-002" in hero  # ready + waiting both listed
    assert 'class="nwafter"' in hero and "after WI-001" in hero


def test_t1_next_work_says_all_done_when_drained(tmp_path):
    # A drained registry does not render an empty surface — it says so, so the
    # landing view still answers "what's next" (nothing).
    wis = (
        "WI-001,Bootstrap,scripts,SR-001,,done,adder,ordinary\n"
        "WI-002,Release,docs,SR-002,WI-001,done,shipped,ordinary\n"
    )
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    hero = _hero_of(tmp_path)
    assert 'class="card nextwork"' in hero
    assert "All work items are done." in hero
    assert 'class="nwlist"' not in hero


# --- WI-319 / SR-054 T4: the next-work card fits its title to the CARD ---------
# 121-CRITIQUE MINOR: the card spent a fixed 60-character budget whatever width it
# had, so WI-308 read "…tiering expo…" — cut mid-word at 1680px with the card half
# empty, and nothing visible to act on. HTML already fits text to the space
# available; the budget was the only thing preventing it. `_NEXT_WORK_TITLE` now
# bounds ONE item's height rather than its text, and where it bites the remainder
# discloses through a native `<details>` (operable by pointer and keyboard, no
# script — its operability is HTML semantics, which is what makes it assertable
# from the markup at all).
_NW_LONG = (  # 109 chars — the real WI-308 clause the critic read
    "Triage the 22 dangling doc references WI-062's tiering exposed, "
    "then wire [step:doc-refs] into docs/stack.ini"
)


def _nw_items(root):
    hero = _hero_of(root)
    return hero.split('class="nwlist"', 1)[1].split("</ul>", 1)[0]


def test_t4_next_work_title_is_not_budgeted_by_character_count(tmp_path):
    # The reported shape: a clause the old fixed budget cut at 60 characters now
    # renders WHOLE, with no ellipsis anywhere in the list.
    wis = 'WI-001,"{}",docs,SR-001,,queued,d,ordinary\n'.format(_NW_LONG)
    make_repo(tmp_path, wis, header=NW_HEADER)
    assert gen(tmp_path).returncode == 0
    items = _nw_items(tmp_path)
    assert len(_NW_LONG) > 60, "vacuous - the fixture must exceed the old budget"
    assert html.unescape(items).count(_NW_LONG) == 1
    assert "…" not in items


def test_t4_an_over_bound_next_work_title_discloses_operably(tmp_path):
    # Past the bound the card still does not dead-end: a native disclosure, a
    # VISIBLE cue on it, and the whole clause present — head and remainder
    # rejoining exactly, so opening it reads continuously.
    gt = load_script("gen_trajectory")
    clause = "Bound the seam ".join(str(i) for i in range(40))
    assert len(clause) > gt._NEXT_WORK_TITLE
    make_repo(
        tmp_path,
        "WI-001,{},docs,SR-001,,queued,d,ordinary\n".format(clause),
        header=NW_HEADER,
    )
    assert gen(tmp_path).returncode == 0
    items = _nw_items(tmp_path)
    assert "<details><summary>" in items and "</details>" in items
    assert 'class="nwrev"' in items  # the cue a reader can see and click
    head, rest = items.split('<span class="nwrev">', 1)
    head = html.unescape(head.split("<details><summary>", 1)[1])
    rest = html.unescape(rest.split("</summary>", 1)[1].split("</details>", 1)[0])
    assert head + rest == clause  # nothing lost, and it rejoins cleanly
    assert head.rstrip() == head and rest.startswith(" ")  # cut at a word
    # The reveal must not depend on script (a static file opened from disk) nor be
    # hidden by the emitter's own CSS.
    css = html_of(tmp_path)
    assert ".nwt summary { cursor:pointer" in css
    assert re.search(r"\.nwt summary\s*\{[^}]*display:none", css) is None


# --- WI-315 (SR-054 T1 binding): the three core reading tasks each reach a
# LABELLED entry point within one tab switch of the landing view ----------------
# WI-300's option-(f) pattern applied to T1, the last SR-054 anchor whose
# mechanizable half had no owner. The 2026-07-26 owner ruling reworded T1 off the
# word "obvious" onto an operational gloss: each of the three core reading tasks
# (find the project state / the next work / how the parts connect) is reachable in
# <= 1 tab switch from the landing view, its entry point a LABELLED nav control or
# a NAMED landing surface. The design constraint (the whole lesson of 119-CRITIQUE's
# MAJOR): assert against the RENDERED artifact carrying real registry data, never
# the nav skeleton — a next-work surface that renders NOTHING on a zero-active
# registry passes a skeleton check but fails the reader. So the fixture reproduces
# the artifact the critic failed: zero active rows (all queued), plus a committed
# module map (ARCH_MD) so the How-SW view (task 3) is present.
T1_ALL_QUEUED = (
    "WI-001,Bootstrap the adder,scripts,SR-001,,queued,adder,ordinary\n"
    "WI-002,Wire the harness,scripts,SR-001,WI-001,queued,harness,ordinary\n"
)


def _landing_dashboard(root):
    """Render the dashboard on the T1 failure condition — zero active rows plus a
    module map, so all three reading tasks' entry points are present — and return
    (hero, navbar), the two slices of the emitted document a reader lands on."""
    make_repo(root, T1_ALL_QUEUED, header=NW_HEADER)
    (root / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    assert gen(root).returncode == 0
    html = html_of(root)
    hero = html.split('class="hero"', 1)[1].split("</section>", 1)[0]
    navbar = html.split('nav class="tabs"', 1)[1].split("</nav>", 1)[0]
    return hero, navbar


def test_t1_three_core_reading_tasks_reach_labelled_entry_points(tmp_path):
    hero, navbar = _landing_dashboard(tmp_path)
    # The exact 119-CRITIQUE state: nothing is active, so the "you are here" line
    # is absent — yet every task below must still reach a labelled entry point.
    assert 'class="sub nowat"' not in hero

    # Task 1 — find the project state: NAMED landing surfaces, 0 tab switches.
    assert '<div class="label">Definition completeness</div>' in hero
    assert '<div class="label">Execution</div>' in hero

    # Task 2 — find the next work: a NAMED landing surface (0 switches) that
    # carries actual content, not an empty region (the 119-CRITIQUE defect — the
    # surface exists in the emitter but rendered nothing on zero-active data).
    assert 'class="card nextwork"' in hero
    assert '<div class="label">Next work</div>' in hero
    nwlist = hero.split('class="nwlist"', 1)[1].split("</ul>", 1)[0]
    assert "WI-001" in nwlist  # the dependency-ready WI is named, not an empty box

    # Task 3 — find how the parts connect: a LABELLED nav control (1 switch),
    # sitting directly in the tab bar — never behind a descend/expand.
    assert 'data-tab="sw"' in navbar
    assert "How (SW architecture)" in navbar


# --- WI-300 / SR-053: the last two uniformity anchors get a child LLR + TC -----
# U5/U3/U1 were bound by WI-292/294/295. U2 and U4 pass structurally but were
# never BOUND, so the coarse `TC-054` critique kept re-judging them by eye. These
# two tests are their cores.

# Hexes that legitimately appear in the shipped document without being a concept
# fill. Each entry names WHY, because the temptation when this test reds is to
# widen the list rather than fix the emitter — and a widened allowlist is exactly
# how a second colour vocabulary gets in.
U2_NON_CONCEPT_HEXES = {
    # `--ring`'s CSS fallback: the literal a browser uses when an emitter this
    # repo has not written yet emits a node with no computed ring ink
    # (_ring_ink's docstring states the degrade-gracefully intent). It lives in a
    # `<style>` block, so it genuinely is a paint surface — the one real entry.
    "#f59e0b",
}


def _how_sw_flat(root):
    """Declared seams but no containerization — the FLAT `sw_graph`.

    `containerize` earns the containment drill instead, so a sweep carrying only
    that fixture never renders `sw_graph`'s own `<style>` block. This is the
    third emitter a whole-document sweep has silently missed (after `knode` and
    the per-layer drill read), which is why `_every_emitter_document` is the one
    place that list lives."""
    make_repo(root)
    (root / "docs" / "architecture.md").write_text(ARCH_MD, encoding="utf-8")
    (root / "docs" / "requirements" / "interfaces.csv").write_text(
        IF_HDR
        + 'IF-001,Provides,src/m,downstream adopter,"cli",SR-001,v1,Stable,Active,,\n'
        + 'IF-002,Consumes,src/m,docs/stack.ini,"reads",SR-001,v1,Stable,Active,,\n',
        encoding="utf-8",
    )
    return root


def _every_emitter_document(tmp_path):
    """`[(label, html), ...]` covering EVERY emitter that really renders.

    The A2 adversarial review's lesson, generalized: a document walk can only
    judge the emitters its fixture happens to render, and it measured the then-
    current fixture at 2 of 6 — the one genuine violation lived in an emitter
    that never rendered, so the test passed while the defect shipped. A
    whole-document uniformity check has exactly that failure mode, so it sweeps
    the union: the artifact this repo ships (the loops diagram, the How-SW
    graph, the tiered drill) plus fixtures for the emitters a meta-repo's own
    dashboard does not exercise. Note BOTH knowledge fixtures — `with_bundle`'s
    four OKF types earn the tiered drill, so only `_flat_bundle` (<= 3 types)
    renders the flat `.knode` concept graph, and a sweep with just the former is
    blind to that emitter.
    """
    docs = []
    shipped = ROOT / "PROJECT_STATE.html"
    if shipped.is_file():
        docs.append(("shipped", shipped.read_text(encoding="utf-8")))
    for label, build in (
        ("flat-dag", lambda p: make_repo(p)),
        ("knowledge-tiered", lambda p: with_bundle(p)),
        ("knowledge-flat", lambda p: _flat_bundle(p)),
        ("tiered-drill", lambda p: tiered_repo(p, TIER_UNION_WIS)),
        ("how-sw-drill", lambda p: containerize(p)),
        ("how-sw-flat", _how_sw_flat),
        ("process", lambda p: with_gate(p, "G2")),
    ):
        root = tmp_path / label
        root.mkdir(parents=True, exist_ok=True)
        build(root)
        assert gen(root).returncode == 0, label
        docs.append((label, html_of(root)))
    return docs


def test_u2_every_concept_fill_comes_from_one_declared_vocabulary(tmp_path):
    """dashboard-uniformity.md U2 (WI-300 core): one status/phase/type colour
    vocabulary means every concept's fill is looked up from a declared palette —
    so the same concept CANNOT render two hexes, because there is only one place
    the hex can come from.

    The defect this catches is an emitter painting a concept with a LITERAL, and
    a literal is invisible to every check that reasons over the palette dicts
    (U5's collision sweep and `_ring_ink`'s enumeration both walk the DICTS).
    The How-SW `component` badge was exactly that — a four-kind vocabulary
    declaring three, with the fourth a bare `#475569` inside `cmp_block`.
    """
    gt = load_script("gen_trajectory")

    declared = set()
    for name in dir(gt):
        if not name.isupper():
            continue
        value = getattr(gt, name)
        members = value.values() if isinstance(value, dict) else value
        if isinstance(value, (dict, tuple, list)):
            declared |= {
                v.lower() for v in members if isinstance(v, str) and v.startswith("#")
            }
    assert len(declared) >= 15, "vocabulary lookup found nothing: {}".format(declared)

    for label, html in _every_emitter_document(tmp_path):
        # A `--token:#hex` definition is the theme layer (surfaces, text,
        # borders), not a concept encoding — declared once in the CSS by design.
        tokens = {
            h.lower() for h in re.findall(r"--[\w-]+:\s*(#[0-9a-fA-F]{3,8})", html)
        }
        # Only where a hex actually PAINTS. WI-311 re-hued three values, and the
        # rendered palette-rationale prose still NAMES the retired ones to
        # explain why they were retired — a whole-document scan read those as
        # emitters and would have grown `U2_NON_CONCEPT_HEXES` by one entry per
        # retirement, which is the "widen the list rather than fix it" trap that
        # list's own comment warns about. Scoping to paint surfaces makes prose
        # structurally out of scope instead.
        painted = []
        for surface in _style_surfaces(html):
            painted += re.findall(r"#[0-9a-fA-F]{6}\b", surface)
        for attr in ("fill", "stroke", "stop-color", "flood-color"):
            painted += re.findall(attr + r'="(#[0-9a-fA-F]{6})"', html)
        assert painted, "vacuous — no painted hex found in {}".format(label)
        stray = {
            h.lower()
            for h in painted
            if h.lower() not in declared
            and h.lower() not in tokens
            and h.lower() not in U2_NON_CONCEPT_HEXES
        }
        assert not stray, (
            "in the {} render, hex(es) belong to no declared vocabulary and no "
            "theme token — an emitter is painting a concept with a literal, "
            "which is a second colour vocabulary by another name: {}".format(
                label, sorted(stray)
            )
        )


def test_u4_one_interaction_idiom_per_node_role_across_every_emitter(tmp_path):
    """dashboard-uniformity.md U4 (WI-300 core): one interaction idiom per
    structure, narrowed (per the ruling) to ATTRIBUTE parity — runtime behaviour
    parity would need a browser harness.

    Two roles exist and each must be spelled ONE way everywhere:

    * an **identified** node (icicle `.cell`, flat-DAG `.wi`, knowledge `.knode`)
      advertises its registry id through `data-id`;
    * a **detail-bearing** drill node (`.block`, in both the When and How-SW
      drills) advertises its detail-map key through `data-node`.

    And every node of either role is made focusable the same way — `tabindex="0"`
    on the group. The failure this forbids is a new emitter inventing `data-key`
    or a hand-rolled focus mechanism: two spellings of one interaction, which is
    what U4 exists to catch.
    """
    roles = {
        "cell": "data-id",
        "wi": "data-id",
        "knode": "data-id",
        "block": "data-node",
    }
    seen = collections.Counter()
    for label, html in _every_emitter_document(tmp_path):
        for tag in re.findall(r"<g\b[^>]*>", html):
            cls = re.search(r'class="([^"]*)"', tag)
            if not cls:
                continue
            kind = cls.group(1).split()[0]
            if kind not in roles:
                continue
            seen[kind] += 1
            assert 'tabindex="0"' in tag, (
                "in {}, a {} node is not focusable the shared way: {}".format(
                    label, kind, tag[:120]
                )
            )
            assert roles[kind] + '="' in tag, (
                "in {}, a {} node does not carry its role's declared attribute "
                "{}: {}".format(label, kind, roles[kind], tag[:120])
            )
            # ...and does not ALSO carry the other role's attribute, which would
            # be one node addressed two ways.
            for attr in set(roles.values()) - {roles[kind]}:
                assert attr + '="' not in tag, (label, kind, attr, tag[:120])
    # EVERY declared node kind must actually have rendered. Without this the
    # sweep degrades silently into "the emitters this fixture happened to run"
    # — the exact vacuity the A2 review caught, and the reason a `knode`
    # regression slipped past this test's first draft.
    missing = sorted(set(roles) - set(seen))
    assert not missing, (
        "no node rendered for kind(s) {} — the sweep is blind to them, so it "
        "cannot claim they share the idiom (seen: {})".format(missing, dict(seen))
    )


# --- WI-313 / SR-052: bind A1/A3/A4 — the last undecomposed accessibility -----
# anchors, same shape as the U-anchor bindings above: declare the set, assert
# membership, sweep every emitter, and state the narrowing in the owning LLR.

# A1, the closure half. The page's interactivity is exactly what its emitted JS
# WIRES, so the selector list is DERIVED from the document's own
# `querySelectorAll` calls rather than hand-copied — a selector newly wired in
# an emitter fails the test until it is classified here, which is the closure
# the per-element A1 tests above (drill blocks, tabs) do not give. A `control`
# entry's matches receive per-element activation listeners (click / focus /
# dblclick / keydown), so every element they match must be keyboard-focusable;
# each non-control entry states why its matches are not focus stops.
A1_WIRED_SELECTORS = {
    ".block": "control",
    ".block[data-node]": "control",
    ".block[data-node]:not([data-wi])": "control",
    ".block[data-wi]": "control",
    ".cell": "control",
    ".wi": "control",
    ".knode": "control",
    "[data-descend]": "control",
    "[role=tab]": "control",
    ".edge": "hover-dim target — classes toggled on it, no listener attaches",
    ".kedge": "hover-dim target, the knowledge-graph spelling",
    ".layer": "drill-layer bookkeeping — shown/hidden, never a focus stop",
    ".view, .tablescroll": "scroll containers — scroll-cue listeners only",
    ".drill:not([data-ready])": "controller root marker, not a control",
    "nav.crumbs": "breadcrumb landmark — its controls are runtime <button>s",
    "nav.tabs": "tablist container — activation is delegated via closest()",
}

# Every DOM-selecting API the emitted JS may use, in any quote style. The
# adversarial review defeated the first draft (querySelectorAll + single
# quotes only) with five other spellings, two of which the emitters already
# use (querySelector('nav.crumbs'), closest('[role=tab]')).
_SELECTOR_CALL = re.compile(
    r"(?:querySelectorAll|querySelector|closest|matches)\(\s*(['\"`])(.*?)\1\s*\)"
)


def _wired_selectors(html):
    """Every selector the document's own scripts pass to a DOM-selecting API —
    and a loud failure on a NON-LITERAL selector argument, which the static
    derivation cannot see and therefore must not silently allow."""
    out = set()
    for script in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S):
        out |= {m.group(2) for m in _SELECTOR_CALL.finditer(script)}
        dynamic = re.findall(
            r"(?:querySelectorAll|querySelector|closest|matches)\(\s*[^'\"`)]", script
        )
        assert not dynamic, (
            "a DOM-selecting call takes a non-literal selector — the A1 closure "
            "cannot classify what it cannot read; use a literal: " + repr(dynamic)
        )
    return out


def _open_tags(html):
    """(tag, attrs) for every open tag in the MARKUP — scripts stripped first
    (the TC-104 decoy lesson: embedded JSON prose fakes markup), and the attr
    scan is quote-aware so a `>` inside an attribute value cannot truncate it."""
    markup = re.sub(r"<script\b.*?</script>", "", html, flags=re.S)
    return re.findall(r"<(\w+)((?:[^>\"]|\"[^\"]*\")*)>", markup)


def _a1_selector_matches(sel, attrs):
    """Match the tiny selector grammar the emitters use — `.cls`, `[attr]`,
    `[attr=v]`, and a trailing `:not([attr])`. A richer selector must extend
    this matcher deliberately (the fullmatch assert makes that loud)."""
    m = re.fullmatch(
        r"(?:\.(?P<cls>[\w-]+))?(?P<conds>(?:\[[\w-]+(?:=[\w-]+)?\])*)"
        r"(?::not\(\[(?P<neg>[\w-]+)\]\))?",
        sel,
    )
    assert m, "selector grammar not handled by this matcher: " + sel
    if m.group("cls"):
        cls = re.search(r'class="([^"]*)"', attrs)
        if not cls or m.group("cls") not in cls.group(1).split():
            return False
    for name, val in re.findall(r"\[([\w-]+)(?:=([\w-]+))?\]", m.group("conds")):
        if val:
            if not re.search(re.escape(name) + r'="' + re.escape(val) + r'"', attrs):
                return False
        elif name + '="' not in attrs:
            return False
    if m.group("neg") and m.group("neg") + '="' in attrs:
        return False
    return True


def _a1_focusable(tag, attrs):
    """Keyboard-focusable: explicit `tabindex="0"`, or natively tab-ordered — a
    `<button>` (the roving-tabindex tabs stay buttons), or an `<a href>` (the
    LLR-101 lesson: a native SVG link carries no tabindex and needs none)."""
    return (
        'tabindex="0"' in attrs or tag == "button" or (tag == "a" and "href=" in attrs)
    )


def test_a1_every_wired_interaction_selector_matches_only_focusable_elements(
    tmp_path,
):
    """dashboard-accessibility.md A1 core (WI-313): every element the page wires
    an interaction to is reachable by keyboard.

    The per-element tests above check KNOWN controls (drill leaves, tabs); what
    none of them assert is the CLOSURE — that the set of wired selectors and the
    set of focusable elements cannot drift apart. Deriving the selectors from
    the emitted JS closes it from one side (a new wired selector fails until
    classified); asserting every declared selector is seen and every control
    selector matches somewhere closes it from the other (a stale entry, or a
    sweep gone blind, also fails).
    """
    seen_selectors = set()
    matched = collections.Counter()
    for label, html in _every_emitter_document(tmp_path):
        wired = _wired_selectors(html)
        unclassified = wired - set(A1_WIRED_SELECTORS)
        assert not unclassified, (
            "in the {} render, the page wires selector(s) this test has no "
            "focusability classification for — decide control vs container and "
            "add them to A1_WIRED_SELECTORS: {}".format(label, sorted(unclassified))
        )
        seen_selectors |= wired
        tags = _open_tags(html)
        for sel, role in A1_WIRED_SELECTORS.items():
            if role != "control" or sel not in wired:
                continue
            for tag, attrs in tags:
                if _a1_selector_matches(sel, attrs):
                    matched[sel] += 1
                    assert _a1_focusable(tag, attrs), (
                        "in the {} render, a wired control is not keyboard-"
                        "focusable: {} matched <{}{}>".format(
                            label, sel, tag, attrs[:120]
                        )
                    )
    stale = set(A1_WIRED_SELECTORS) - seen_selectors
    assert not stale, (
        "classified selector(s) never appeared in any render — the entry is "
        "stale or the sweep is blind: {}".format(sorted(stale))
    )
    unexercised = {s for s, r in A1_WIRED_SELECTORS.items() if r == "control"} - set(
        matched
    )
    assert not unexercised, (
        "control selector(s) matched no element anywhere — vacuous: {}".format(
            sorted(unexercised)
        )
    )


def test_a1_focus_walk_follows_document_order(tmp_path):
    """A1's "sensible order" residue, narrowed to what is assertable (the
    WI-300 ruling's recorded recommendation): document order IS emission order,
    and the focus walk follows document order as long as nothing carries a
    positive tabindex. The only values the page may use are `0` (join the walk
    in document order) and `-1` — and every `-1` must sit on a tablist button,
    where the WI-273 roving-tabindex controller owns the order via arrow keys.
    Whether that order FEELS sensible is the perceptual half the ruling dropped,
    stated in LLR-112 as the scope narrowing.
    """
    for label, html in _every_emitter_document(tmp_path):
        seen = 0
        for tag, attrs in _open_tags(html):
            ti = re.search(r"tabindex\s*=\s*\"?(-?\d+)\"?", attrs)
            if not ti:
                continue
            seen += 1
            assert ti.group(1) in ("0", "-1"), (
                "in the {} render, a positive tabindex reorders the focus "
                "walk: <{}{}>".format(label, tag, attrs[:120])
            )
            if ti.group(1) == "-1":
                assert tag == "button" and 'role="tab"' in attrs, (
                    "in the {} render, tabindex=-1 outside the roving tablist "
                    "removes a control from the walk: <{}{}>".format(
                        label, tag, attrs[:120]
                    )
                )
        assert seen, "vacuous — no tabindex found in {}".format(label)


# A3 (no information by colour alone), the closure half. The status glyphs and
# the flat-DAG fallback are owned above; what was never asserted is that EVERY
# vocabulary member that paints is explained somewhere in words.
def _legend_swatches(html):
    """[(resolved-hex-or-raw-value, label), …] for every legend swatch, with
    `var()` resolved against the document's own token definitions — the status
    legend paints via `var(--done)` etc., and a raw hex scan under-reports it."""
    tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", html))
    out = []
    for m in re.finditer(r'<i style="background:([^"]+)"></i>\s*([^<]*)', html):
        value = m.group(1).strip()
        var = re.fullmatch(r"var\((--[\w-]+)\)", value)
        if var:
            value = tokens.get(var.group(1), value)
        out.append((value.lower(), m.group(2).strip()))
    return out


def test_a3_every_painted_vocabulary_member_is_explained_in_words(tmp_path):
    """dashboard-accessibility.md A3 core (WI-313): for every declared colour
    vocabulary, every member that actually PAINTS in a document resolves to a
    legend swatch labelled in words in that same document.

    The vocabularies are enumerated from the module (`_palette_vocabularies`,
    the U5 closure), so a new vocabulary cannot ship without entering this
    sweep. SCOPE, and its narrowing (LLR-113): the cue must exist in the same
    document — that it sits within eyeshot of the painted element is layout
    this does not re-assert. The JS-rendered detail-panel badge is out of scope
    because its background carries its concept as the badge's own visible text
    (`esc(d.kind)`), so that colour never carries the information alone.
    """
    gt = load_script("gen_trajectory")
    vocabs = _palette_vocabularies(gt)
    explained = collections.Counter()
    for label, html in _every_emitter_document(tmp_path):
        markup = re.sub(r"<script\b.*?</script>", "", html, flags=re.S)
        painted = " ".join(_style_surfaces(markup))
        for attr in ("fill", "stroke"):
            painted += " " + " ".join(
                re.findall(attr + r'="(#[0-9a-fA-F]{6})"', markup)
            )
        painted = painted.lower()
        worded = {h for h, lab in _legend_swatches(markup) if lab}
        for vname, members in vocabs.items():
            for key, hx in members.items():
                if hx.lower() not in painted:
                    continue
                explained[vname] += 1
                assert hx.lower() in worded, (
                    "in the {} render, {}[{}] paints {} but no legend swatch "
                    "explains that colour in words — the encoding is colour-"
                    "alone for a reader who cannot perceive it".format(
                        label, vname, key, hx
                    )
                )
    missing = set(vocabs) - set(explained)
    assert not missing, (
        "no render painted any member of vocabulary(ies) {} — the sweep is "
        "blind to them and cannot claim they are explained".format(sorted(missing))
    )


def test_a3_icicle_tier_legend_swatches_are_the_painted_tier_palette(tmp_path):
    """The defect this WI found on first measurement (the method's rule 1,
    again): the What-tab tier legend HARDCODED its four swatches, and its TC
    swatch kept a pre-WI-311 hex that had since become `STATUS_FILL["done"]` —
    so the legend labelled the done-green "TC" while the actual TC cells
    painted `TIER_FILL["tc"]`, and the document-wide check above stayed green
    only because the Knowledge tab's own legend covered the real hex. The
    legend now derives from TIER_FILL; this pins the bijection the same way
    `test_every_multifill_panel_emits_a_palette_bijection_legend` pins the
    phase legend's. Expected is built from the DICT, not a key tuple, so a
    fifth tier member missing from the legend also fails (adversarial-review
    hardening — emitter and test previously shared the same literal tuple)."""
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    page = html_of(tmp_path)
    legend = page.split('id="arch-detail"', 1)[1]
    legend = legend.split('<div class="legend">', 1)[1].split("</div>", 1)[0]
    entries = re.findall(r'<i style="background:(#[0-9a-f]{6})"></i>([A-Z]+)', legend)
    assert entries == [(fill, tier.upper()) for tier, fill in gt.TIER_FILL.items()], (
        entries
    )


def test_a3_js_detail_maps_mirror_the_declared_palettes(tmp_path):
    """A3, the JS half (adversarial-review finding F1): the detail-panel badge
    paints from `const tierColor` / `const statusColor` maps in the emitted
    main script. Those used to be HAND-COPIED literals — and kept the same
    stale pre-WI-311 tc hex the static legend fix eliminated, so clicking a TC
    cell rendered a badge in the done-green while the cell and the legend both
    said `TIER_FILL["tc"]`. The maps are now substituted from the constants;
    this holds every emitted copy byte-equal to the Python palettes, so a
    hand-copy cannot come back."""
    gt = load_script("gen_trajectory")
    for label, html in _every_emitter_document(tmp_path):
        seen = 0
        for name, expect in (
            ("tierColor", gt.TIER_FILL),
            ("statusColor", gt.STATUS_FILL),
        ):
            for m in re.finditer(r"const " + name + r" = (\{[^;]*?\});", html):
                got = dict(
                    re.findall(
                        r"[\"']?(\w+)[\"']?\s*:\s*[\"'](#[0-9a-fA-F]{6})[\"']",
                        m.group(1),
                    )
                )
                seen += 1
                assert got == dict(expect), (
                    "in the {} render, the emitted {} map disagrees with the "
                    "declared palette — a hand-copied colour vocabulary: {}".format(
                        label, name, got
                    )
                )
        assert seen >= 2, "vacuous — {} emitted no detail colour maps".format(label)


def test_a3_css_status_tokens_mirror_status_fill(tmp_path):
    """A3, the token half: the DAG status legend paints via `var(--done)` etc.,
    while the nodes paint the STATUS_FILL constants directly — so a drift
    between the CSS token block and the Python dict mislabels the legend the
    same way the hardcoded tier legend did. Holds the four status tokens equal
    to STATUS_FILL in `:root` and asserts the dark block does NOT override them
    (they are theme-invariant by design)."""
    gt = load_script("gen_trajectory")
    make_repo(tmp_path)
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    for status, fill in gt.STATUS_FILL.items():
        assert _css_var(css, "--" + status) == fill, (status, fill)
    dark = css.split("prefers-color-scheme: dark", 1)[1].split("}", 1)[0]
    for status in gt.STATUS_FILL:
        assert "--" + status + ":" not in dark, (
            "--{} is overridden in dark — the status vocabulary is declared "
            "theme-invariant".format(status)
        )


def _brace_body(text, open_index):
    """The text between a `{` at open_index and its matching `}`."""
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_index + 1 : i]
    return text[open_index + 1 :]


def _wiring_bodies(script, sel):
    """The for-loop bodies that iterate the elements `querySelectorAll(sel)`
    yields — both emitted shapes: the immediate `for(const x of …qSA('sel')){}`
    loop, and `const NAME = […qSA('sel')…]` followed by `for(const x of NAME)`
    loops elsewhere in the same script."""
    bodies = []
    for m in re.finditer(r"querySelectorAll\('" + re.escape(sel) + r"'\)", script):
        head = script[max(0, m.start() - 100) : m.start()]
        if re.search(r"for\s*\(\s*const\s+\w+\s+of\s+[\w.\[\]? ]*$", head):
            bodies.append(_brace_body(script, script.index("{", m.end())))
            continue
        assign = re.search(r"const\s+(\w+)\s*=[^;{]*$", head)
        if assign:
            for lm in re.finditer(
                r"for\s*\(\s*const\s+\w+\s+of\s+" + assign.group(1) + r"\s*\)\s*\{",
                script,
            ):
                bodies.append(_brace_body(script, lm.end() - 1))
    return bodies


def test_a1_every_wired_control_pairs_click_with_focus_or_keydown(tmp_path):
    """A1's OPERABLE half, statically (adversarial-review finding F5): the
    ruling's A1 core is "natively focusable or tabindex + a KEY HANDLER", and
    the first binding quietly dropped the key-handler half claiming it needed a
    browser. It does not: the same static read that derives the selectors can
    assert that every control-selector wiring loop that attaches a mouse
    activation (`click`/`dblclick`) also attaches a keyboard-reachable path
    (`focus`, whose handler does the same work in these emitters, or
    `keydown`). Runtime behaviour equivalence is still not driven — that
    narrowing stands — but mouse-only wiring can no longer ship silently.
    Runtime-created controls (the breadcrumb buttons) are native <button>s,
    where a click listener IS keyboard-operable, and stay out of scope."""
    paired = 0
    for label, html in _every_emitter_document(tmp_path):
        for script in re.findall(r"<script\b[^>]*>(.*?)</script>", html, re.S):
            for sel, role in A1_WIRED_SELECTORS.items():
                if role != "control":
                    continue
                bodies = "".join(_wiring_bodies(script, sel))
                if not bodies:
                    continue
                if "addEventListener('click'" in bodies or (
                    "addEventListener('dblclick'" in bodies
                ):
                    paired += 1
                    assert (
                        "addEventListener('focus'" in bodies
                        or "addEventListener('keydown'" in bodies
                    ), (
                        "in the {} render, {} wires a mouse activation with no "
                        "keyboard path beside it: {}".format(label, sel, bodies[:200])
                    )
    assert paired >= 4, (
        "vacuous — only {} control wiring loops with a mouse activation were "
        "found across the sweep".format(paired)
    )


# Every hex-bearing UPPERCASE constant in the emitter, with the role that says
# WHICH floor applies to it. `fill-vocabulary` members are backgrounds (label ink
# 4.5:1, focus ring 3:1); a `control-ink` member is the foreground painted on
# those fills, so it is floor-checked in the other direction by the ring/arrow
# tests and closed here against `_ring_ink`'s reachable outputs (WI-317). A new
# constant fails the sweep until it is classified.
A4_HEX_CONSTANT_ROLES = {
    "STATUS_FILL": "fill-vocabulary",
    "TIER_FILL": "fill-vocabulary",
    "OKF_TYPE_FILL": "fill-vocabulary",
    "SW_NODE_FILL": "fill-vocabulary",
    "PHASE_ACCENTS": "fill-vocabulary",
    "RING_INKS": "control-ink",
}


def test_a4_the_vocabulary_sweep_is_closed_and_every_member_clears_the_floors():
    """dashboard-accessibility.md A4 closure (WI-313). The sibling A4 tests own
    the arithmetic; what none of them owned is the SET — each sweeps a
    hand-copied list of the palette constants, so a sixth vocabulary could ship
    outside every floor check. Reflection closes it: every UPPERCASE
    module-level collection holding hex members must be one of the five
    declared vocabularies (a new one fails here until it joins
    `_palette_vocabularies` and the A4/U5 sweeps), and every member of the
    REFLECTED set must clear both floors — 4.5:1 for its label ink and 3:1 for
    its computed focus ring — so a new vocabulary enters the arithmetic by
    existing, not by being remembered.
    """
    gt = load_script("gen_trajectory")

    def _flatten(value):
        """Every string reachable inside a constant — nested dicts/tuples/
        lists/sets and bare strings included, because the adversarial review
        defeated the flat-dict-only draft with a per-theme dict-of-dicts (the
        WI-293 shape), a tuple-of-tuples, a set, and a bare string constant."""
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for v in value.values():
                yield from _flatten(v)
        elif isinstance(value, (tuple, list, set, frozenset)):
            for v in value:
                yield from _flatten(v)

    found = {}
    for name in dir(gt):
        if not name.isupper():
            continue
        strings = list(_flatten(getattr(gt, name)))
        # ANY hex form counts as hex-bearing (3/4/6/8 digits) — a shorthand or
        # alpha member must not escape the closure by being oddly spelled.
        hexes = [s for s in strings if re.fullmatch(r"#[0-9a-fA-F]{3,8}", s)]
        if hexes:
            found[name] = hexes
    assert set(found) == set(A4_HEX_CONSTANT_ROLES), (
        "the hex-bearing constant set changed — a new constant must declare its "
        "ROLE in A4_HEX_CONSTANT_ROLES (and a new colour vocabulary must also "
        "join _palette_vocabularies and the A4/U5 sweeps) before it ships: "
        "{}".format(sorted(found))
    )
    # Every member must be CANONICAL 6-digit lowercase — the contrast
    # arithmetic below is only defined for that form, so a shorthand or
    # alpha-carrying member fails here rather than shipping unmeasured.
    for name, hexes in found.items():
        bad = [h for h in hexes if not re.fullmatch(r"#[0-9a-f]{6}", h)]
        assert not bad, (name, "non-canonical hex member(s)", bad)
    # Label ink is white everywhere except the one declared exception: `queued`
    # is the light-gray fill that carries dark slate ink (see
    # test_a4_node_fills_meet_the_wcag_floor, which states the same rule).
    dark_ink_fills = {gt.STATUS_FILL["queued"]}
    fills = []
    for name, hexes in sorted(found.items()):
        if A4_HEX_CONSTANT_ROLES[name] != "fill-vocabulary":
            continue
        fills.extend(hexes)
        for fill in hexes:
            ink = "#0f172a" if fill in dark_ink_fills else "#ffffff"
            assert _wcag(ink, fill) >= 4.5, (name, fill, ink, _wcag(ink, fill))
            ring = gt._ring_ink(fill)
            assert _wcag(ring, fill) >= 3, (name, fill, ring, _wcag(ring, fill))
    # A `control-ink` constant is measured the other way round — it is painted ON
    # the fills, so its floors are the ring/arrow ones the sibling tests own; what
    # closes HERE is that the set is exactly what `_ring_ink` can choose (WI-317
    # emits one containment-arrow marker per ink, so an unreachable member is dead
    # markup and a reachable non-member would ship an arrow head with no marker).
    for name in [n for n, r in A4_HEX_CONSTANT_ROLES.items() if r == "control-ink"]:
        assert set(found[name]) == {gt._ring_ink(f) for f in fills}, (
            name,
            sorted(found[name]),
            sorted({gt._ring_ink(f) for f in fills}),
        )


# A4, the theme-token half (adversarial-review finding F4): LLR-114 claims the
# floors cover "emitted theme tokens", but the only token test hand-maintained
# a set of one ({"--hub"}) — the exact hand-copied-list defect the LLR says it
# closed. Same cure as A1's selectors: DERIVE the set from the emitted CSS and
# force a classification, so a new `fill:var(--x)` fails until a human states
# its role — and the roles that carry white text get the both-themes floor.
A4_FILL_TOKEN_ROLES = {
    "--hub": "white-text-fill",  # the Process hub rect, white label on it
    "--accent": "ink",  # .hooplab headline TEXT colour, not a fill behind text
    "--muted": "ink",  # sub-label / edge text colour
    "--text": "ink",  # body text colour used as SVG fill
    "--surface": "container-fill",  # component boxes; dark --text sits on it
    # WI-317: the containment-arrow head is FILLED with the per-node control ink.
    # Not a background — its floor is 3:1 against the host node fill, owned by
    # test_t5_containment_arrow_clears_the_3to1_floor_against_every_host_fill.
    "--ring": "control-ink",
}


def test_a4_every_css_fill_token_is_classified_and_floor_checked(tmp_path):
    """Every theme token the emitted CSS uses as a `fill:` must be classified
    in A4_FILL_TOKEN_ROLES; `white-text-fill` roles clear 4.5:1 under white in
    BOTH themes (the WI-293 lesson — a per-theme token passed light and shipped
    2.98:1 in dark), and `container-fill` roles keep the page's own `--text`
    readable on them in both themes."""
    with_gate(tmp_path, "G2")  # the Process tab renders --hub, the widest set
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    used = set(re.findall(r"fill:\s*var\((--[\w-]+)", css))
    assert used, "vacuous — no fill:var() token found"
    unclassified = used - set(A4_FILL_TOKEN_ROLES)
    assert not unclassified, (
        "fill token(s) with no declared role — classify before shipping: {}".format(
            sorted(unclassified)
        )
    )
    for token, role in A4_FILL_TOKEN_ROLES.items():
        if role == "white-text-fill":
            for dark in (False, True):
                value = _css_var(css, token, dark=dark)
                assert _wcag("#ffffff", value) >= 4.5, (token, dark, value)
        elif role == "container-fill":
            for dark in (False, True):
                surface = _css_var(css, token, dark=dark)
                text = _css_var(css, "--text", dark=dark)
                assert _wcag(text, surface) >= 4.5, (token, dark, surface, text)


def test_u3_knowledge_edge_stroke_uses_the_shared_muted_token(tmp_path):
    # dashboard-uniformity U3 (048 MINOR): the knowledge-graph directed edge shares
    # the drill `.wire` stroke idiom (the `--muted` token), not a hardcoded hex
    # that diverged from `.wire` in light mode.
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    css = html_of(tmp_path)
    # WI-310: the width is now the shared `--w-line` connector token rather than
    # a bare 1.5 — same claim (one idiom), one more literal retired.
    assert (
        "#knowgraph .kedge{fill:none;stroke:var(--muted);stroke-width:var(--w-line);}"
        in css
    )
    assert "#knowgraph .kedge{fill:none;stroke:#94a3b8" not in css


# --- the docs/status.md derived snapshot (WI-202, --status) --------------------

# A docs/gate carrying derive_gate.py's `# basis:` line — the fresh, cached
# derivation the snapshot PROJECTS (never recomputes).
GATE_FILE = (
    "# DERIVED GATE — generated by scripts/derive_gate.py (do not hand-edit).\n"
    "# basis: SN=1 SR=2 LLR=3 TC=4 drafts=1 computed=G2 phase=2 per-phase=1=G3;2=G2\n"
    "# computed 2026-07-17 (as-of abc1234)\n"
    "G2\n"
)
# One-line field vs Recommendation fallback; OI-3's field soft-wraps two lines,
# and its Decision carries a volatile git-state that must NOT reach the snapshot.
# WI-322: briefs are ROWS of the open-items registry, not markdown sections.
# Declared out of id order on purpose — the projection sorts numerically — and
# OI-2 carries no OneLine, so the first-sentence-of-Recommendation fallback is
# exercised too.
OPEN_ITEMS_HEADER = (
    "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
    "Recommendation,WI-Refs,RuledDate,RulingRef\n"
)
OPEN_ITEMS = OPEN_ITEMS_HEADER + (
    'OI-2,the second decision,pending,,,"whether to flip the flag.",,,'
    '"keep it off until phase 3. A later sitting revisits.",,,\n'
    "OI-1,the first decision,pending,,"
    '"push — the branch is remote-tracked, so the unpushed commits are pure '
    'durability risk (the merge is a separate sitting).",'
    '"origin exists, ahead 9 commits at check — verify at read time.",,,,,,\n'
)
STATUS_MARKED = (
    "# Status\n\n## Current State\n\n"
    "<!-- BEGIN GENERATED STATUS -->\n"
    "<!-- END GENERATED STATUS -->\n\n"
    "- **Next action:** hand-authored intent stays here.\n\n"
    "## Scope\n\n- **Goal:** the thing.\n"
)


def make_status_repo(root, status=STATUS_MARKED, open_items=OPEN_ITEMS, gate=GATE_FILE):
    make_repo(root)
    (root / "docs" / "gate").write_text(gate, encoding="utf-8")
    if open_items is not None:
        (root / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
        (root / "docs" / "requirements" / "open-items.csv").write_text(
            open_items, encoding="utf-8"
        )
    if status is not None:
        (root / "docs" / "status.md").write_text(status, encoding="utf-8")
    return root


def status_text(root):
    return (root / "docs" / "status.md").read_text(encoding="utf-8")


def block_of(root):
    t = status_text(root)
    return t.split("<!-- BEGIN GENERATED STATUS -->", 1)[1].split(
        "<!-- END GENERATED STATUS -->", 1
    )[0]


def test_status_splices_derived_facts(tmp_path):
    make_status_repo(tmp_path)
    proc = gen(tmp_path, "--status")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    block = block_of(tmp_path)
    # derived gate + spine come from the docs/gate basis line (the SSOT cache)
    assert "derived **G2**" in block
    assert "per-phase `1=G3;2=G2`" in block and "phase=2" in block
    assert "SN=1 SR=2 LLR=3 TC=4" in block and "(1 draft)" in block
    # the hand-authored intent + Scope stay OUTSIDE the markers, untouched
    after = status_text(tmp_path).split("<!-- END GENERATED STATUS -->", 1)[1]
    assert "hand-authored intent stays here" in after and "## Scope" in after


def test_status_open_items_projection_and_ordering(tmp_path):
    make_status_repo(tmp_path)
    assert gen(tmp_path, "--status").returncode == 0
    block = block_of(tmp_path)
    # id-order (OI-1 before OI-2) regardless of file order
    assert block.index("**OI-1**") < block.index("**OI-2**")
    # OI-1: the explicit One-line field, soft-wrapped lines joined into one bullet
    assert (
        "**OI-1** — push — the branch is remote-tracked, so the unpushed commits "
        "are pure durability risk (the merge is a separate sitting)." in block
    )
    # OI-2: no One-line field -> the FIRST sentence of Recommendation, not the rest
    assert "**OI-2** — keep it off until phase 3." in block
    assert "A later sitting revisits" not in block


def test_status_does_not_bake_volatile_git_state(tmp_path):
    # Done-when 4: an item's live git state (OI-1's "ahead 9 commits") lives in the
    # brief's Decision field, never the stamped snapshot.
    make_status_repo(tmp_path)
    assert gen(tmp_path, "--status").returncode == 0
    assert "ahead 9 commits" not in block_of(tmp_path)


def test_status_check_fresh_and_stale(tmp_path):
    make_status_repo(tmp_path)
    assert gen(tmp_path, "--status").returncode == 0
    fresh = gen(tmp_path, "--status", "--check")
    assert fresh.returncode == 0 and "up to date" in fresh.stdout
    # an open-items edit stales the block (caught at commit, not first in CI)
    oi = tmp_path / "docs" / "requirements" / "open-items.csv"
    oi.write_text(
        oi.read_text(encoding="utf-8")
        + "OI-5,a new ask,pending,,decide soon.,,,,,,,\n",
        encoding="utf-8",
    )
    stale = gen(tmp_path, "--status", "--check")
    assert stale.returncode == 1 and "STALE" in stale.stderr
    # regenerating restores freshness and now projects OI-5
    assert gen(tmp_path, "--status").returncode == 0
    assert gen(tmp_path, "--status", "--check").returncode == 0
    assert "**OI-5** — decide soon." in block_of(tmp_path)


def test_status_vacuous_without_markers_or_file(tmp_path):
    # Opt-in posture: a status.md without the marker pair is left untouched and
    # --check passes vacuously; an absent status.md is likewise a clean no-op.
    make_status_repo(tmp_path, status="# Status\n\n## Scope\n\n- Goal\n")
    before = status_text(tmp_path)
    proc = gen(tmp_path, "--status")
    assert proc.returncode == 0 and "no GENERATED STATUS markers" in proc.stdout
    assert status_text(tmp_path) == before  # untouched
    assert gen(tmp_path, "--status", "--check").returncode == 0
    (tmp_path / "docs" / "status.md").unlink()
    assert gen(tmp_path, "--status", "--check").returncode == 0


def test_status_legacy_gate_without_basis_falls_back_to_counts(tmp_path):
    # A legacy hand-set docs/gate (no `# basis:` line) still renders: the gate
    # value is read from the first non-comment line and the spine counts fall back
    # to a direct registry count (SN=1 SR=2 LLR=3 TC=4 in the fixture spine).
    make_status_repo(tmp_path, gate="# legacy hand-set gate\nG1\n")
    assert gen(tmp_path, "--status").returncode == 0
    block = block_of(tmp_path)
    assert "derived **G1**" in block
    assert "SN=1 SR=2 LLR=3 TC=4" in block


def test_status_forward_only_guard_is_scoped_to_the_generated_block(tmp_path):
    # The WI-200 handoff, re-scoped by repo-review 2026-07-21 H-5: the marker
    # exempts ONLY the spliced block (its freshness is the status-map step's
    # job); the hand-authored remainder of a hybrid status.md stays policed —
    # the old whole-file stand-down left it enforced by nothing, and this
    # repo's own status.md promptly accreted done-WI prose. Uses an all-done
    # registry so no other --strict rule fires (R-A wants a Deliverable iff
    # done; R-E wants a SpecRef on OPEN rows only).
    coherent = (
        "WI-001,Bootstrap,scripts,SR-001,,done,the adder\n"
        "WI-002,Harness,scripts,SR-001,WI-001,done,harness green\n"
    )
    make_repo(tmp_path, coherent)
    (tmp_path / "docs" / "gate").write_text(GATE_FILE, encoding="utf-8")
    # 1) A clean hand region beside the generated block: --strict is clean
    # (whatever done ids the BLOCK itself carries are the splice's business).
    (tmp_path / "docs" / "status.md").write_text(STATUS_MARKED, encoding="utf-8")
    assert gen(tmp_path, "--status").returncode == 0
    marked = run_py(
        [SCRIPTS / "check_trajectory.py", "--root", tmp_path, "--strict"], cwd=tmp_path
    )
    assert marked.returncode == 0, marked.stdout + marked.stderr
    assert "forward-only" not in (marked.stdout + marked.stderr)
    # 2) A done id accreting in the HAND region of the same marked file: a
    # finding, ERROR under --strict (this was silently clean before H-5).
    (tmp_path / "docs" / "status.md").write_text(
        STATUS_MARKED.replace(
            "hand-authored intent stays here.",
            "WI-001 shipped the adder (a done id in prose).",
        ),
        encoding="utf-8",
    )
    assert gen(tmp_path, "--status").returncode == 0
    hand = run_py(
        [SCRIPTS / "check_trajectory.py", "--root", tmp_path, "--strict"], cwd=tmp_path
    )
    assert hand.returncode == 1, hand.stdout + hand.stderr
    assert "forward-only" in hand.stderr and "WI-001" in hand.stderr
    # 3) Markers stripped entirely: the rule polices the whole file (unchanged).
    stripped = (
        status_text(tmp_path)
        .replace("<!-- BEGIN GENERATED STATUS -->", "")
        .replace("<!-- END GENERATED STATUS -->", "")
    )
    (tmp_path / "docs" / "status.md").write_text(stripped, encoding="utf-8")
    rearmed = run_py(
        [SCRIPTS / "check_trajectory.py", "--root", tmp_path, "--strict"], cwd=tmp_path
    )
    assert rearmed.returncode == 1 and "forward-only" in rearmed.stderr


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

    monkeypatch.setattr(gt, "_detour_points", counting)
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
        gt, "_lane_candidates", lambda *a, **k: [float(i) for i in range(500)]
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
    wis, integrity = ct.load_wis(ct.read_rows(ROOT / ct.WI_CSV))
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
    wis, integrity = ct.load_wis(ct.read_rows(ROOT / ct.WI_CSV))
    assert not integrity
    dag, _details = gt.dag_svg(wis)
    assert dag.lstrip().startswith("<svg") and dag.count('<path class="edge') > 100
    assert _wire_through_box_violations(dag) == []
    sw = gt.sw_graph(ROOT, gt.sw_modules(ROOT))
    assert sw is not None
    assert sw.lstrip().startswith("<svg") and sw.count('<path class="swedge"') > 10
    assert _wire_through_box_violations(sw) == []
