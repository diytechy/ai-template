"""trace.py's optional domain-neutral component registry (the AXES/CMP layer,
process-options.md "Component layer"): CMP-### rows live off the SN->SR->LLR->TC
spine as the set-grained knowledge + lifecycle home. Structure is derived, never
restated on the CMP row — membership is a `Component` tag on the primitive rows —
so what trace.py checks is exactly the joins: PartOf / SupersededBy must name real
CMP ids, a primitive's Component tag must resolve to a real CMP row, a malformed
CMP id fails --strict, and a leftover CMP-000 placeholder never blocks a gate.

A CMP row's `Knowledge` cell may also name a hand-owned knowledge pack
(research-knowledge.md §3a) as a `docs/knowledge/<label>` ref; trace.py resolves
those to real pack files as a warn-only advisory (a missing pack never gates),
and leaves skill names and URLs in the same cell alone.
"""

from conftest import make_minimal_project, run_py, record_ids

CMP_HEADER = (
    "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
)
ROW = "{cid},arm,physical,docs/knowledge/arm,{state},{sup},{partof},,note\n"


def cmp_path(root):
    return root / "docs" / "requirements" / "components.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_cmps(root, *rows):
    cmp_path(root).write_text(CMP_HEADER + "".join(rows), encoding="utf-8")
    record_ids(root)


def row(cid, state="planned", sup="", partof=""):
    return ROW.format(cid=cid, state=state, sup=sup, partof=partof)


def test_scaffolded_placeholder_is_inert(scaffold):
    # bootstrap lays components.csv down with only the CMP-000 example row; the
    # placeholder never blocks a gate, even under --no-placeholders (the
    # interfaces.csv / PB-000 / MOD-000 stance).
    make_minimal_project(scaffold)
    assert cmp_path(scaffold).exists()
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "components=" not in proc.stdout  # no real rows -> no counts emitted


def test_clean_component_rows_pass(scaffold):
    make_minimal_project(scaffold)
    write_cmps(
        scaffold,
        row("CMP-001"),
        row("CMP-002", partof="CMP-001", sup=""),
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "components=2 component-findings=0" in proc.stdout


def test_partof_must_name_a_real_cmp(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001", partof="CMP-999"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CMP CMP-001 PartOf references unknown CMP-999" in report_of(scaffold)


def test_supersededby_must_name_a_real_cmp(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001", state="deprecated", sup="CMP-777"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CMP CMP-001 SupersededBy references unknown CMP-777" in report_of(scaffold)


def test_llr_component_tag_must_resolve(scaffold):
    # The membership join, checked from the primitive side: an LLR tagged with a
    # phantom component is a finding once a real CMP registry exists.
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    text = llr.read_text(encoding="utf-8").rstrip("\n").splitlines()
    text[0] += ",Component"
    text[1] += ",CMP-404"
    llr.write_text("\n".join(text) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "Component tag references unknown CMP-404" in report_of(scaffold)


def test_llr_component_tag_resolving_passes(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    text = llr.read_text(encoding="utf-8").rstrip("\n").splitlines()
    text[0] += ",Component"
    text[1] += ",CMP-001"
    llr.write_text("\n".join(text) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "component-findings=0" in proc.stdout


def test_malformed_cmp_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-XX"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CMP id 'CMP-XX' is malformed" in report_of(scaffold)


# --- WI-153: warn-first `Knowledge`-ref resolution (research-knowledge.md §3a) --
# A CMP's Knowledge cell may name a `docs/knowledge/<label>` pack; trace.py resolves
# it to a real file as a warn-only advisory (never a gate), and leaves skill names
# and URLs in the same cell unchecked.
KROW = "{cid},arm,software,{know},built,,,,note\n"


def krow(cid, know):
    return KROW.format(cid=cid, know=know)


def write_pack(root, label, body="# Pack\n"):
    d = root / "docs" / "knowledge"
    d.mkdir(parents=True, exist_ok=True)
    target = d / (label + ".md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")


def test_knowledge_ref_missing_pack_warns_only(scaffold):
    # A docs/knowledge/-shaped ref with no pack file is a warn-only advisory: it
    # is loud on stdout + in the report, but never changes the exit code — not
    # even under --strict (a pack is advisory context, never a gate).
    make_minimal_project(scaffold)
    write_cmps(scaffold, krow("CMP-001", "docs/knowledge/missing"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "knowledge-advisories=1" in proc.stdout
    assert "names no pack (docs/knowledge/missing.md)" in proc.stdout
    assert "Knowledge-pack advisories (warn-only)" in report_of(scaffold)
    assert "names no pack (docs/knowledge/missing.md)" in report_of(scaffold)


def test_knowledge_ref_present_pack_resolves(scaffold):
    # The ref resolves whether or not the author writes the `.md` suffix.
    make_minimal_project(scaffold)
    write_pack(scaffold, "found")
    write_cmps(
        scaffold,
        krow("CMP-001", "docs/knowledge/found"),
        krow("CMP-002", "docs/knowledge/found.md"),
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "knowledge-advisories" not in proc.stdout


def test_knowledge_ref_must_resolve_inside_pack_home(scaffold):
    # Traversal/absolute refs are not packs even when they happen to name an
    # existing Markdown file; normalized paths that stay in-home remain valid.
    make_minimal_project(scaffold)
    write_pack(scaffold, "nested/found")
    write_cmps(
        scaffold,
        krow("CMP-001", "docs/knowledge/../architecture"),
        krow(
            "CMP-002",
            "docs/knowledge/"
            + str((scaffold / "docs" / "architecture.md").resolve()).replace("\\", "/"),
        ),
        krow("CMP-003", "docs/knowledge/nested/../nested/found"),
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "knowledge-advisories=2" in proc.stdout
    assert "docs/knowledge/../architecture" in proc.stdout
    assert "architecture.md' names no pack" in proc.stdout


def test_knowledge_skill_and_url_refs_are_unchecked(scaffold):
    # A bare skill name and a URL share the cell with pack refs but are not
    # file-checkable, so neither yields an advisory.
    make_minimal_project(scaffold)
    write_cmps(scaffold, krow("CMP-001", "registry-hygiene;https://example.com/x"))
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "knowledge-advisories" not in proc.stdout


def test_knowledge_ref_mixed_cell_checks_only_the_pack(scaffold):
    # One cell, three refs (skill, present pack, missing pack): only the missing
    # pack advises; the skill and the resolved pack are silent.
    make_minimal_project(scaffold)
    write_pack(scaffold, "there")
    write_cmps(
        scaffold,
        krow("CMP-001", "registry-hygiene;docs/knowledge/there;docs/knowledge/gone"),
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "knowledge-advisories=1" in proc.stdout
    assert "names no pack (docs/knowledge/gone.md)" in proc.stdout
    assert "docs/knowledge/there" not in report_of(scaffold)


# --- WI-064: the IF tier joins the Component-tag membership sweep ---------------
# trace.py has read interfaces.csv since WI-056, but an IF row's `Component` tag
# was the one membership cell it never validated (the old comment predated
# WI-056). An IF tagged with a phantom CMP is now the same finding an LLR one is.

IF_HEADER = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
    "Stability,Status,Component,Notes\n"
)


def write_if(root, component):
    (root / "docs" / "requirements" / "interfaces.csv").write_text(
        IF_HEADER
        + 'IF-001,Provides,src/demo,downstream,"call",SR-001,v1,Stable,Active,{},\n'.format(
            component
        ),
        encoding="utf-8",
    )
    record_ids(root)


def test_if_component_tag_must_resolve(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    write_if(scaffold, "CMP-404")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "IF IF-001 Component tag references unknown CMP-404" in report_of(scaffold)


def test_if_component_tag_resolving_passes(scaffold):
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    write_if(scaffold, "CMP-001")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "component-findings=0" in proc.stdout


# --- the `;`-joined Module cell in the membership join (WI-429) ---------------


def test_module_components_splits_a_joined_module_cell(tmp_path):
    """`LLR.Module` is a `;`-joined list, and the AXES membership join must read
    it as one. It did not: an unsplit `a.py;b.py` normalized to a single nonsense
    key, so a row spanning two modules tagged NEITHER — silently, because a
    membership map missing an entry is indistinguishable from a module nobody
    tagged. Found when the WI-429 repair widened 2 such cells to 13 and dropped
    `scripts/traj_parse` out of every component."""
    from conftest import load_script

    ct = load_script("check_trajectory")
    reg = tmp_path / "docs" / "requirements"
    reg.mkdir(parents=True)
    (reg / "low-level-requirements.toml").write_text(
        "[design.LLR-001]\n"
        'module = "project-trajectory/scripts/a.py;project-trajectory/scripts/b.py"\n'
        'component = "CMP-001"\n'
        "\n[design.LLR-002]\n"
        'module = "project-trajectory/scripts/c.py"\n'
        'component = "CMP-002;CMP-003"\n',
        encoding="utf-8",
    )
    mapping = ct.module_components(tmp_path)
    assert mapping["scripts/a"] == {"CMP-001"}, "the first half must be tagged"
    assert mapping["scripts/b"] == {"CMP-001"}, "and so must the second"
    assert not [k for k in mapping if ";" in k], "no joined key may survive"
    assert mapping["scripts/c"] == {"CMP-002", "CMP-003"}, "tags still multi-valued"
