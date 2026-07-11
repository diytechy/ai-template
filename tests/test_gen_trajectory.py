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


def make_repo(root, wis_body=GOOD_WIS, readme=True):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    (req / "stakeholder-needs.md").write_text(SN_MD, encoding="utf-8")
    (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(TCS, encoding="utf-8")
    (req / "work-items.csv").write_text(WI_HEADER + wis_body, encoding="utf-8")
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
    dag = html_of(tmp_path).split('id="dag" class="view"', 1)[1].split("</svg>", 1)[0]
    xs = {
        m.group(1): float(m.group(2))
        for m in re.finditer(r'data-id="(WI-\d+)"[^>]*><rect x="([\d.]+)"', dag)
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
