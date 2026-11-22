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

CMP_HEADER = "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,Notes\n"
# The TOML carrier since WI-443 (OI-14 part B). `superseded_by` and `part_of`
# are typed arrays; an EMPTY cell is an ABSENT KEY, never `""` — writing the
# empty string is itself a refusal (`spine_carrier.empty_value_findings`).
ROW = (
    "[component.{cid}]\n"
    'name = "arm"\n'
    'category = "physical"\n'
    'knowledge = "docs/knowledge/arm"\n'
    'state = "{state}"\n'
    "{sup}{partof}"
    'notes = "note"\n\n'
)


def cmp_path(root):
    return root / "docs" / "requirements" / "components.toml"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def write_cmps(root, *rows):
    cmp_path(root).write_text("".join(rows), encoding="utf-8")
    record_ids(root)


def row(cid, state="planned", sup="", partof=""):
    return ROW.format(
        cid=cid,
        state=state,
        sup='superseded_by = ["{}"]\n'.format(sup) if sup else "",
        partof='part_of = ["{}"]\n'.format(partof) if partof else "",
    )


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


def test_a_design_row_component_column_places_nothing(scaffold):
    # A design row names no component since WI-1023: its placement is derived
    # from the interfaces its verifying cases name. A legacy CSV registry still
    # carrying the column is not read for membership, so a phantom id there is
    # no finding (the TOML carrier refuses the key outright).
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    text = llr.read_text(encoding="utf-8").rstrip("\n").splitlines()
    text[0] += ",Component"
    text[1] += ",CMP-404"
    llr.write_text("\n".join(text) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "CMP-404" not in report_of(scaffold)


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
KROW = (
    "[component.{cid}]\n"
    'name = "arm"\n'
    'category = "software"\n'
    'knowledge = "{know}"\n'
    'state = "built"\n'
    'notes = "note"\n\n'
)


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


def write_if(root, component):
    (root / "docs" / "requirements" / "interfaces.toml").write_text(
        # The revision 35 shape: the owner is a component id, the far side a
        # declared party; the `component` cell under test is the retired one.
        "# External party: downstream\n\n"
        "[interface.IF-001]\n"
        'owner = "CMP-001"\n'
        'consumers = ["external:downstream"]\n'
        'channel = "call"\n'
        'version = "v1"\n'
        'status = "Accepted"\n'
        'component = "{}"\n'.format(component),
        encoding="utf-8",
    )
    record_ids(root)


def test_if_component_tag_must_resolve(scaffold):
    """Implements: TC-044"""
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    write_if(scaffold, "CMP-404")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "IF IF-001 Component tag references unknown CMP-404" in report_of(scaffold)


def test_an_if_component_tag_is_a_retired_cell_even_when_it_resolves(scaffold):
    """An interface's place in the component view is derived from its
    endpoints (WI-1022), so the cell itself is the finding, resolving or not."""
    make_minimal_project(scaffold)
    write_cmps(scaffold, row("CMP-001"))
    write_if(scaffold, "CMP-001")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "carries the retired `component` cell (set on IF-001)" in report_of(scaffold)


# --- the module -> component join, one home (WI-429, WI-1005) ----------------


def test_module_components_keys_each_declared_file_by_its_module():
    """`kitlib.spine.module_components`, the join's one home, over the files'
    `Component:` declarations (WI-1021; its input was the design rows' tags
    until then). Each path lands on its `norm_module` key in any of its
    spellings, so a seam, an import and a header meet on one key. Two files
    sharing a key (`check.py`, `check.sh`) keep both components. A value that
    cannot name a component makes no membership, and a well-formed id naming
    no component row is kept: the join does not filter against the component
    registry.

    Implements: TC-435"""
    from kitlib import spine

    mapping = spine.module_components(
        {
            "project-trajectory/scripts/a.py": "CMP-001",
            "scripts/kitlib/__init__.py": "CMP-002",
            "docs/process.toml": "CMP-003",
            "project-trajectory/scripts/check.py": "CMP-001",
            "project-trajectory/scripts/check.sh": "CMP-002",
            "scripts/lower.py": "cmp-001",
            "scripts/none.py": "none",
            "scripts/dangling.py": "CMP-404",
        }
    )
    assert mapping == {
        "scripts/a": {"CMP-001"},
        "scripts/kitlib": {"CMP-002"},
        "docs/process.toml": {"CMP-003"},
        "scripts/check": {"CMP-001", "CMP-002"},
        "scripts/dangling": {"CMP-404"},
    }
