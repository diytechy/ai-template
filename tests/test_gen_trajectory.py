"""gen_trajectory.py — the offline trajectory dashboard (Thread 52 phase 2).

The generator renders the root PROJECT_STATE.html from work-items.csv + the spine as a
*view* (a design principle: text is truth). What matters is that it is fully
offline (no CDN), deterministic (so the --check freshness gate is byte-stable),
refuses to render an invalid registry, and stays vacuous when there is nothing to
show. Each is pinned by running the real script over a minimal temp project.
"""

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
    # — typed concept nodes, directed spine edges, each concept's DESCRIPTION
    # embedded and a link-OUT to its docs/okf/<tier>/<id>.md full body (the
    # middle-path embedding, ruling #15).
    with_bundle(tmp_path)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'data-tab="know"' in text and 'id="know"' in text
    # typed nodes + the type legend (fill keyed by OKF type)
    assert 'class="knode"' in text and "knowarrow" in text
    assert "System Requirement" in text and "Stakeholder Need" in text
    # a directed spine edge exists (SN-001 -> SR-001 both present as nodes)
    assert 'data-id="SN-001"' in text and 'data-id="SR-001"' in text
    assert "kedge" in text
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
    assert 'data-id="SR-002"' in text  # the surviving concept is still a node


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

    # know_graph: every concept node carries a <title> = id — title (type).
    know = _view_svg(text, 'id="know"')
    assert know.count("<title>") == know.count('class="knode"') > 0
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


def test_how_sw_containerizes_when_components_contain_modules(tmp_path):
    # With a CMP layer that contains modules, the How-SW panel becomes the
    # containerized <details> top view (≤10 items), not the flat table/graph.
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert 'class="cmptree"' in sw
    # WI-087: two top-level components is <= the > 3 threshold, so the blocks start
    # EXPANDED (a flat read of a small view); the count is threshold-independent.
    assert sw.count('<details class="cmpbox"') == 2  # two top-level components
    assert sw.count('<details class="cmpbox" open>') == 2  # <= 3 -> start expanded
    assert "Top view: 2 item" in sw
    # members are revealed inside the expansion; intra + boundary seams surface.
    assert "scripts/mod_a" in sw and "scripts/mod_c" in sw
    assert "IF-003" in sw  # intra-component seam
    assert "IF-004" in sw and "stack.ini" in sw  # boundary seam to a file hub


def test_boundary_aggregation_dedupes_cross_component_edges(tmp_path):
    # IF-001 and IF-002 both cross CMP-001 -> CMP-002; at the top level they
    # aggregate to ONE deduplicated component-to-component edge naming both ids.
    containerize(tmp_path)
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    xs = re.search(r'<ul class="xseams">(.*?)</ul>', sw, re.S).group(1)
    assert len(re.findall(r"<li>", xs)) == 1
    assert "IF-001, IF-002" in xs


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
    # A CMP with PartOf renders as a nested <details> inside its parent, and only
    # the top-level root is a first-view item.
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


# --- WI-074: the campaign-binned When view -------------------------------------
# The WHEN-axis mirror of FB5: work items sharing a Campaign tag containerize into
# a collapsed <details> box, campaign-crossing predecessor edges aggregate to one
# deduplicated container edge, campaign-less WIs render flat, and a registry with
# no Campaign values renders byte-identically to today (the flat SVG DAG).

CAMP_HEADER = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,Campaign\n"
)
# alpha = {WI-001, WI-002}, beta = {WI-003}, WI-004 standalone (no campaign).
CAMP_WIS = (
    "WI-001,Root,scripts,SR-001,,done,the adder,alpha-camp\n"
    "WI-002,Mid,scripts,SR-001,WI-001,active,harness,alpha-camp\n"
    "WI-003,Sub,scripts,SR-002,WI-001,queued,the subber,beta-camp\n"
    "WI-004,Release,docs,SR-002,WI-002;WI-003,queued,shipped,\n"
)


def dag_view(root):
    """The `dag` panel's view div content (the campaign tree or the flat SVG)."""
    return (
        html_of(root).split('id="dag-view" class="view">', 1)[1].split("</div>", 1)[0]
    )


def test_campaign_binning_containerizes_members(tmp_path):
    # With campaign-tagged WIs the When panel becomes the containerized <details>
    # tree: one collapsed box per campaign, members revealed inside, standalone
    # WIs flat below.
    make_repo(tmp_path, CAMP_WIS, header=CAMP_HEADER)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert 'class="camptree"' in text
    assert text.count('<details class="campbox">') == 2  # alpha + beta
    assert "alpha-camp" in text and "beta-camp" in text
    assert "Binned by campaign: 2 campaign(s) + 1 standalone" in text
    # a member row surfaces the WI, its title, and the requirement it delivers
    view = dag_view(tmp_path)
    assert "WI-002" in view and "Mid" in view and "SR-001" in view


def test_campaign_less_wi_renders_flat_outside_any_container(tmp_path):
    # A campaign-less WI is NOT wrapped in a campbox — it renders flat in the
    # standalone section.
    make_repo(tmp_path, CAMP_WIS, header=CAMP_HEADER)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "Standalone work items" in text
    # Within the camptree region, WI-004 lives in the standalone section, never
    # inside a campaign container (the campboxes precede the standalone marker).
    tree_region = text.split('class="camptree"', 1)[1]
    containers, standalone = tree_region.split('class="standalone"', 1)
    assert "WI-004" in standalone  # the campaign-less WI renders flat
    assert "WI-004" not in containers  # ...and not inside any campaign container
    assert "WI-001" in containers and "WI-003" in containers  # members are binned


def test_no_campaign_values_render_byte_identical(tmp_path):
    # The vacuity guarantee: an all-empty Campaign column (or none at all) renders
    # byte-for-byte what it did before the column existed. Proven by round-trip:
    # render column-less (flat SVG), add campaigns (tree appears), strip them back
    # to an all-empty column, re-render == the original bytes exactly.
    plain_body = "".join(row.rsplit(",", 1)[0] + "\n" for row in CAMP_WIS.splitlines())
    make_repo(tmp_path, plain_body)  # default WI_HEADER, no Campaign column
    assert gen(tmp_path).returncode == 0
    flat = (tmp_path / "PROJECT_STATE.html").read_bytes()
    assert b'class="camptree"' not in flat

    wi = tmp_path / "docs" / "requirements" / "work-items.csv"
    wi.write_text(CAMP_HEADER + CAMP_WIS, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    assert b'class="camptree"' in (tmp_path / "PROJECT_STATE.html").read_bytes()

    # all-empty Campaign column (present but no values) == column-absent behavior.
    empty_col = "".join(row + ",\n" for row in plain_body.splitlines())
    wi.write_text(CAMP_HEADER + empty_col, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == flat


def test_campaign_boundary_edges_dedupe(tmp_path):
    # Two predecessor edges alpha->beta (WI-003 depends on WI-001 AND WI-002, both
    # in alpha) aggregate to ONE deduplicated container edge naming both WI edges.
    body = (
        "WI-001,A1,scripts,SR-001,,done,d,alpha-camp\n"
        "WI-002,A2,scripts,SR-001,,done,d,alpha-camp\n"
        "WI-003,B1,scripts,SR-001,WI-001;WI-002,queued,d,beta-camp\n"
    )
    make_repo(tmp_path, body, header=CAMP_HEADER)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    xs = re.search(r'<ul class="xcamp">(.*?)</ul>', text, re.S).group(1)
    assert len(re.findall(r"<li>", xs)) == 1  # one crossing pair -> one edge
    assert "WI-001→WI-003" in xs and "WI-002→WI-003" in xs  # both contributors


def test_campaign_view_is_deterministic_and_check_stable(tmp_path):
    # Built from sorted inputs, no clocks -> a second render is byte-identical and
    # --check passes (no new freshness exclusion).
    make_repo(tmp_path, CAMP_WIS, header=CAMP_HEADER)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0


def test_meta_campaign_binning_smoke():
    # Over the real meta repo: every campaign tag in the registry renders as a
    # collapsed container in the When view, and the known campaigns are present.
    # The count is derived, not pinned: a new campaign row must not break an
    # unrelated smoke test (it did once — the 2026-07-12 deep-review campaign).
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    wis, integrity = ct.load_wis(ct.read_rows(ROOT / ct.WI_CSV))
    assert not integrity
    view = gt.campaign_containment(wis)
    assert view is not None
    campaigns = {w["campaign"] for w in wis if w["campaign"]}
    assert view.count('<details class="campbox">') == len(campaigns)
    for slug in (
        "working-surface-restructure-2026-07-11",
        "capability-expansion-2026-07-11",
        "owner-feedback-2026-07-11",
        "campaign-binning-batch-2026-07-11",
    ):
        assert slug in view


# --- WI-087 / SR-051: the tiered, phase-aware drill-down views -----------------
# The When roadmap tiers into phase -> workstream -> work-item <details> blocks
# once a tier holds > 3 members (generalizing the WI-074 campaign binning), each
# WI carries a per-phase color accent, parent edges aggregate the deduped union of
# their members' crossing edges, and the How-SW view starts collapsed above the
# > 3 component threshold. A registry below the thresholds renders byte-identically
# to the flat WI-074 view.

# Four SR phases (v1..v4), so a WI's phase is derived from the SR it delivers.
TIER_SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase\n"
    'SR-001,P1,SN-001,"r",R,"a",,M,Test,Verified,v1\n'
    'SR-002,P2,SN-001,"r",R,"a",,M,Test,Verified,v2\n'
    'SR-003,P3,SN-001,"r",R,"a",,M,Test,Verified,v3\n'
    'SR-004,P4,SN-001,"r",R,"a",,M,Test,Verified,v4\n'
)
TIER_HDR = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,Campaign\n"

# Two v1 WIs both feed the single v2 WI -> the v1->v2 parent edge is the deduped
# union of two child edges. Phases: v1={001,002}, v2={003}, v3={004}, v4={005}.
TIER_UNION_WIS = (
    "WI-001,A,scripts,SR-001,,done,d,\n"
    "WI-002,B,docs,SR-001,,done,d,\n"
    "WI-003,C,unattended,SR-002,WI-001;WI-002,queued,d,\n"
    "WI-004,D,self-adoption,SR-003,WI-003,queued,d,\n"
    "WI-005,E,scripts,SR-004,WI-003,queued,d,\n"
)


def tiered_repo(root, wis_body, header=TIER_HDR, srs=TIER_SRS):
    """make_repo + a phase-carrying SR registry (the WI phase is derived from the
    SRs a work item delivers)."""
    make_repo(root, wis_body, header=header)
    (root / "docs" / "requirements" / "system-requirements.csv").write_text(
        srs, encoding="utf-8"
    )
    return root


def test_when_view_tiers_by_phase_above_threshold(tmp_path):
    # > 3 phases -> the When view starts at phase blocks (4), each carrying the
    # per-phase color accent; the phase count is surfaced.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    # `dag_view` truncates at the first nested </div>; the tierbox markup is unique
    # to the When panel, so count over the full page.
    view = html_of(tmp_path)
    assert "Tiered roadmap: 4 phase(s), 4 workstream(s)" in view
    assert view.count('<details class="tierbox">') == 4  # one block per phase
    assert "· phase ·" in view  # the tier is labeled
    assert '<span class="ph"' in view  # the per-phase color accent renders


def test_when_view_parent_edge_is_deduped_union_of_child_edges(tmp_path):
    # The two v1->v2 child edges (WI-001->WI-003 and WI-002->WI-003) aggregate to
    # ONE parent block edge equal to their deduped union.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    view = dag_view(tmp_path)
    xt = re.search(r'<ul class="xtier">(.*?)</ul>', view, re.S).group(1)
    # crossing phase pairs: v1->v2, v2->v3, v2->v4 -> three aggregated edges
    assert len(re.findall(r"<li>", xt)) == 3
    v1v2 = re.search(r"<code>v1</code> → <code>v2</code>.*?\((.*?)\)", xt, re.S).group(
        1
    )
    assert v1v2 == "WI-001→WI-003, WI-002→WI-003"  # deduped union


def test_when_view_nests_workstream_tier_inside_a_phase(tmp_path):
    # Within a phase that holds > 3 workstreams the workstream tier fires,
    # nesting phase -> workstream -> work item; below the threshold it stays flat.
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
    assert "· phase ·" in view and "· workstream ·" in view  # both tiers rendered
    # 4 phase blocks + 4 workstream blocks nested inside v1 = 8 tierboxes.
    assert view.count('<details class="tierbox">') == 8
    assert "<code>Scripts / harness</code>" in view  # workstream label on a sub-block


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
    assert view.count('<details class="tierbox">') == 5  # one block per workstream
    assert "· workstream ·" in view and "· phase ·" not in view


def test_when_view_flat_below_thresholds_is_the_campaign_view(tmp_path):
    # <= 3 phases and <= 3 workstreams -> when_view delegates to
    # campaign_containment byte-for-byte (the tiering is earned by scale).
    make_repo(tmp_path, CAMP_WIS, header=CAMP_HEADER)  # 2 workstreams, unphased
    gt = load_script("gen_trajectory")
    ct = load_script("check_trajectory")
    wis, _ = ct.load_wis(ct.read_rows(tmp_path / ct.WI_CSV))
    view = gt.when_view(tmp_path, wis)
    assert view == gt.campaign_containment(wis)  # identical bytes
    assert 'class="tierbox"' not in view and 'class="campbox"' in view


def test_when_view_is_deterministic_and_check_stable(tmp_path):
    # Sorted inputs, no clocks -> a re-render is byte-identical and --check passes.
    tiered_repo(tmp_path, TIER_UNION_WIS)
    assert gen(tmp_path).returncode == 0
    first = (tmp_path / "PROJECT_STATE.html").read_bytes()
    again = gen(tmp_path)
    assert again.returncode == 0 and "already up to date" in again.stdout
    assert (tmp_path / "PROJECT_STATE.html").read_bytes() == first
    assert gen(tmp_path, "--check").returncode == 0


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
    # > 3 top-level components -> the blocks start COLLAPSED (click-to-explode);
    # contrast the <= 3 case (test_how_sw_containerizes...), which starts expanded.
    containerize(tmp_path)
    req = tmp_path / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(FOUR_CMP_LLRS, encoding="utf-8")
    (req / "components.csv").write_text(FOUR_CMPS, encoding="utf-8")
    assert gen(tmp_path).returncode == 0
    sw = sw_section(tmp_path)
    assert "Top view: 4 item" in sw
    assert sw.count('<details class="cmpbox">') == 4  # four collapsed blocks
    assert '<details class="cmpbox" open>' not in sw  # > 3 -> not auto-expanded


def test_meta_tiered_when_view_smoke():
    # Over the real meta repo (4 workstreams > 3): the When view tiers into
    # workstream blocks with the campaign containers nested at the bottom tier.
    ct = load_script("check_trajectory")
    gt = load_script("gen_trajectory")
    wis, integrity = ct.load_wis(ct.read_rows(ROOT / ct.WI_CSV))
    assert not integrity
    view = gt.when_view(ROOT, wis)
    assert view is not None
    assert '<details class="tierbox">' in view  # workstream tier fires
    assert "· workstream ·" in view
    assert 'class="campbox"' in view  # campaigns stay the bottom-tier container


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
    assert "Slices → campaigns → gates" in text
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
    # panel 3 states the two bars and joins work-items.csv (4 WIs, 1 done, none
    # campaign-binned under the plain header)
    assert "commit bar" in text and "gate bar" in text
    assert "4 work items · 1 done · 0 campaign-binned across 0 campaign(s)" in text
    # still fully offline with the new tab present
    low = text.lower()
    assert "http://" not in low and "https://" not in low


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


def test_process_campaign_stats_join_work_items(tmp_path):
    # Panel 3's numbers are a live join over work-items.csv campaign bins.
    with_gate(tmp_path, "G2", CAMP_WIS, header=CAMP_HEADER)
    assert gen(tmp_path).returncode == 0
    text = html_of(tmp_path)
    assert "4 work items · 1 done · 3 campaign-binned across 2 campaign(s)" in text


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
