"""gen_trajectory.py — the offline trajectory dashboard (Thread 52 phase 2).

The generator renders docs/trajectory.html from work-items.csv + the spine as a
*view* (a design principle: text is truth). What matters is that it is fully
offline (no CDN), deterministic (so the --check freshness gate is byte-stable),
refuses to render an invalid registry, and stays vacuous when there is nothing to
show. Each is pinned by running the real script over a minimal temp project.
"""

import re

from conftest import SCRIPTS, run_py

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
    return (root / "docs" / "trajectory.html").read_text(encoding="utf-8")


# --- renders a self-contained, offline dashboard -------------------------------


def test_generates_self_contained_dashboard(tmp_path):
    make_repo(tmp_path)
    proc = gen(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (tmp_path / "docs" / "trajectory.html").exists()
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
    first = (tmp_path / "docs" / "trajectory.html").read_bytes()
    second = gen(tmp_path)
    assert second.returncode == 0
    assert "already up to date" in second.stdout  # unchanged -> not rewritten
    assert (tmp_path / "docs" / "trajectory.html").read_bytes() == first


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
    assert (tmp_path / "docs" / "trajectory.html").exists()


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
    assert not (tmp_path / "docs" / "trajectory.html").exists()
    assert gen(tmp_path, "--check").returncode == 0  # vacuously fresh


def test_opt_out_silences(tmp_path):
    make_repo(tmp_path)
    (tmp_path / "docs" / "trajectory-check").write_text("off\n", encoding="utf-8")
    proc = gen(tmp_path, "--check")
    assert proc.returncode == 0 and "off" in proc.stdout
    assert not (tmp_path / "docs" / "trajectory.html").exists()


def test_cycle_refuses_to_render(tmp_path):
    make_repo(
        tmp_path,
        "WI-001,A,scripts,,WI-002,queued,d\nWI-002,B,scripts,,WI-001,queued,d\n",
    )
    proc = gen(tmp_path)
    assert proc.returncode == 1 and "cycle" in proc.stderr
    assert not (tmp_path / "docs" / "trajectory.html").exists()
