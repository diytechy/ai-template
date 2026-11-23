"""The requirement tree (WI-1027): one parent link per design row, one walk.

A design row may name one parent design row instead of its system
requirements. One walk in the shared kernel answers both directions of the
link, and every reader that relates a requirement to its design rows takes its
answer, so a row two levels down counts wherever a top-level row counts. The
cases here run in process over the three-level tree in
`tests/llr_tree_fixtures.py`; each reader's case was run red against the
reader before it took the walk.
"""

import argparse
import re
from pathlib import Path

import pytest
from conftest import load_script
from kitlib import spine as kspine

import llr_tree_fixtures as fx

# --- the walk ---------------------------------------------------------------


def _faulty():
    """The tree plus a second top-level row, a child whose parent is missing, a
    two-row cycle and a row below it, listed out of tree order."""
    rows = fx.llrs()
    rows.insert(0, rows.pop(2))  # the grandchild first
    rows += [
        {"LLR-ID": "LLR-020", "Parent": "LLR-099"},
        {"LLR-ID": "LLR-030", "Parent": "LLR-031"},
        {"LLR-ID": "LLR-031", "Parent": "LLR-030"},
        {"LLR-ID": "LLR-032", "Parent": "LLR-031"},
    ]
    return rows


def test_the_walk_goes_down_from_a_requirement_to_every_row_below_it_once():
    """Implements: TC-561"""
    tree = kspine.llr_tree(_faulty())
    # registry order, not tree order: the grandchild is listed first
    assert tree.below[fx.SR1] == [fx.GRAND, fx.TOP, fx.CHILD]
    assert tree.below[fx.SR2] == [fx.OTHER]


def test_the_walk_goes_down_from_a_design_row_to_its_descendants():
    """Implements: TC-561"""
    tree = kspine.llr_tree(_faulty())
    assert tree.below[fx.TOP] == [fx.GRAND, fx.CHILD]
    assert tree.below[fx.CHILD] == [fx.GRAND]
    assert fx.GRAND not in tree.below


def test_the_walk_goes_up_from_a_grandchild_to_its_chains_requirement():
    """Implements: TC-561"""
    tree = kspine.llr_tree(_faulty())
    assert tree.srs_of[fx.GRAND] == [fx.SR1]
    assert tree.srs_of[fx.TOP] == [fx.SR1]
    assert (tree.depth[fx.TOP], tree.depth[fx.CHILD], tree.depth[fx.GRAND]) == (0, 1, 2)
    assert tree.parent_of[fx.GRAND] == fx.CHILD


def test_a_missing_parent_or_a_cycle_reaches_no_requirement_and_the_walk_returns():
    """Implements: TC-561"""
    tree = kspine.llr_tree(_faulty())
    for rid in ("LLR-020", "LLR-030", "LLR-031", "LLR-032"):
        assert tree.srs_of[rid] == []
        assert rid not in tree.depth
        assert all(rid not in below for below in tree.below.values())
    assert tree.broken["LLR-020"] == ("missing", "LLR-020", "LLR-099")
    assert tree.broken["LLR-030"][0] == "cycle"
    assert tree.broken["LLR-032"] == ("under", "LLR-031", None)


def test_a_one_row_cycle_and_a_row_naming_two_parents_are_broken_too():
    """Implements: TC-561"""
    rows = fx.llrs() + [
        {"LLR-ID": "LLR-040", "Parent": "LLR-040"},
        {"LLR-ID": "LLR-041", "Parent": "LLR-001;LLR-009"},
    ]
    tree = kspine.llr_tree(rows)
    assert tree.broken["LLR-040"] == ("cycle", "LLR-040", ("LLR-040",))
    assert tree.broken["LLR-041"] == ("several", "LLR-041", ("LLR-001", "LLR-009"))


def test_llrs_under_keeps_its_rows_and_reaches_the_grandchild():
    """Implements: TC-561"""
    rows = fx.llrs()
    assert [r["LLR-ID"] for r in kspine.llrs_under([fx.SR1], rows)] == list(fx.TREE)
    assert kspine.llrs_under([fx.SR1], rows)[2] is rows[2]


# --- the cell and its faults (LLR-480) ---------------------------------------

coherence = load_script("coherence")


def _orphans(llrs, tcs=None, srs=None):
    srs = fx.srs() if srs is None else srs
    tcs = fx.tcs() if tcs is None else tcs
    findings, _ids = coherence.spine_orphan_findings(
        srs,
        llrs,
        tcs,
        [],
        {r["SR-ID"] for r in srs},
        {r["LLR-ID"] for r in llrs},
        {"SN-001"},
        set(),
    )
    return findings


def test_a_well_formed_tree_is_silent():
    """Implements: TC-560"""
    assert _orphans(fx.llrs()) == []


FAULTS = [
    (
        {"LLR-ID": "LLR-050", "Title": "t", "Detail": "d"},
        "LLR LLR-050 has no SR parent",
    ),
    (
        {"LLR-ID": "LLR-051", "Parent": fx.TOP, "SR-Refs": fx.SR2},
        "LLR LLR-051 is a child of LLR-001 and names SR-Refs (SR-002)",
    ),
    (
        {"LLR-ID": "LLR-052", "Parent": "LLR-099"},
        "LLR LLR-052 names parent LLR-099, which is no live design row",
    ),
    (
        {"LLR-ID": "LLR-053", "Parent": fx.SR1},
        "LLR LLR-053 names parent SR-001, which is no live design row",
    ),
    (
        {"LLR-ID": "LLR-054", "Parent": "LLR-001;LLR-009"},
        "LLR LLR-054 names 2 parents (LLR-001, LLR-009)",
    ),
    (
        {"LLR-ID": "LLR-055", "Parent": "LLR-055"},
        "LLR LLR-055 is on a parent cycle (LLR-055 -> LLR-055)",
    ),
]


@pytest.mark.parametrize("status", ["Drafted", "Accepted"])
@pytest.mark.parametrize("fault,text", FAULTS)
def test_each_fault_is_reported_once_at_either_status(fault, text, status):
    """Implements: TC-560"""
    llrs = fx.llrs() + [dict(fault, Status=status)]
    tcs = fx.tcs() + [{"TC-ID": "TC-050", "Verifies": fault["LLR-ID"]}]
    findings = _orphans(llrs, tcs)
    hits = [f for f in findings if f.startswith(text)]
    assert len(hits) == 1, findings
    assert [f for f in findings if fault["LLR-ID"] in f] == hits


def test_each_row_on_a_two_row_cycle_names_the_cycle():
    """Implements: TC-560"""
    llrs = fx.llrs() + [
        {"LLR-ID": "LLR-060", "Parent": "LLR-061", "Status": "Drafted"},
        {"LLR-ID": "LLR-061", "Parent": "LLR-060", "Status": "Drafted"},
    ]
    findings = _orphans(llrs)
    assert (
        "LLR LLR-060 is on a parent cycle (LLR-060 -> LLR-061 -> LLR-060)" in findings
    )
    assert (
        "LLR LLR-061 is on a parent cycle (LLR-061 -> LLR-060 -> LLR-061)" in findings
    )


def test_a_row_below_a_missing_parent_names_where_its_chain_breaks():
    """Implements: TC-560"""
    llrs = fx.llrs() + [
        {"LLR-ID": "LLR-070", "Parent": "LLR-099", "Status": "Drafted"},
        {"LLR-ID": "LLR-071", "Parent": "LLR-070", "Status": "Drafted"},
    ]
    findings = _orphans(llrs)
    assert "LLR LLR-071 reaches no SR: its parent chain breaks at LLR-070" in findings
    assert [f for f in findings if f.startswith("LLR LLR-071")] == [
        "LLR LLR-071 reaches no SR: its parent chain breaks at LLR-070"
    ]


STRICT = argparse.Namespace(strict=True, strict_integrity=False)


def _analyze(trace, root):
    return trace.analyze(
        trace.load_registries(Path(root) / "docs"), trace.AnalysisFlags()
    )


def test_the_strict_check_fails_on_a_fault(tmp_path):
    """Implements: TC-560"""
    trace = load_script("trace")
    rows = fx.llrs() + [{"LLR-ID": "LLR-052", "Parent": "LLR-099", "Title": "t",
                         "Detail": "d", "Status": "Drafted", "Phase": "1"}]  # fmt: skip
    findings = _analyze(trace, fx.write(tmp_path / "bad", llr_rows=rows))
    assert any("names parent LLR-099" in f for f in findings.orphans)
    assert trace.exit_code(findings, STRICT) == 1
    clean = _analyze(trace, fx.write(tmp_path / "ok"))
    assert clean.orphans == []
    assert trace.exit_code(clean, STRICT) == 0


def test_the_required_field_check_asks_sr_refs_of_a_top_level_row_only():
    """Implements: TC-560"""
    trace = load_script("trace")
    top = {"LLR-ID": "LLR-080", "Title": "t", "Detail": "d", "Status": "Drafted"}
    child = dict(top, **{"LLR-ID": "LLR-081", "Parent": fx.TOP})
    findings = trace.schema_findings("LLR", [top, child])
    assert findings == ["LLR LLR-080 has empty required field SR-Refs"]


def test_a_design_registry_whose_rows_carry_a_parent_loads(tmp_path):
    """Implements: TC-560"""
    import spine_carrier

    root = fx.write(tmp_path)
    rows = spine_carrier.load(
        root / "docs/requirements/low-level-requirements.toml", "LLR-ID"
    )
    assert [r.get("Parent", "") for r in rows] == ["", fx.TOP, fx.CHILD, ""]


def test_the_parent_cell_is_accepted_text():
    """A re-parent of an accepted row is an amendment of that row (the plan's
    D1; decisions record maint-wi-1027 D-001): the cell is in the accepted half
    of the design registry's cell split, by name."""
    acceptance_record = load_script("acceptance_record")
    rel = "docs/requirements/low-level-requirements.toml"
    assert "Parent" in acceptance_record.SPINE_ACCEPTED_CELLS[rel]
    assert acceptance_record.spine_cell_class(rel, "Parent") == "accepted"
    moved = acceptance_record.split_changed_cells(
        rel, "LLR-ID", {"LLR-ID": "LLR-002", "Parent": "LLR-001"},
        {"LLR-ID": "LLR-002", "Parent": "LLR-009"},
    )  # fmt: skip
    assert moved == {"accepted": {"Parent": ("LLR-001", "LLR-009")}, "traced": {}}


# --- a parent's discharge (LLR-408 over the tree) ----------------------------


def test_a_parent_no_case_names_is_reported_though_its_descendants_are_verified():
    """Implements: TC-566"""
    findings = _orphans(fx.llrs(), fx.tcs(drop=("TC-001",)) + [
        {"TC-ID": "TC-010", "Verifies": fx.SR1}])  # fmt: skip
    assert (
        "LLR LLR-001 has no test (TC) - a parent: its children's test cases do "
        "not discharge it"
    ) in findings
    assert not any(f.startswith(("LLR LLR-002", "LLR LLR-003")) for f in findings)


def test_a_parent_named_by_its_own_case_or_drafted_is_not_reported():
    """Implements: TC-566"""
    assert _orphans(fx.llrs()) == []
    drafted = fx.llrs(**{fx.TOP: "Drafted"})
    tcs = fx.tcs(drop=("TC-001",)) + [{"TC-ID": "TC-010", "Verifies": fx.SR1}]
    assert _orphans(drafted, tcs) == []


def test_an_unverified_accepted_grandchild_is_reported():
    """Implements: TC-566"""
    findings = _orphans(fx.llrs(), fx.tcs(drop=("TC-003",)))
    assert findings == ["LLR LLR-003 has no test (TC)"]


def test_the_strict_check_fails_on_an_undischarged_parent(tmp_path):
    """Implements: TC-566"""
    trace = load_script("trace")
    tcs = fx.tcs(drop=("TC-001",)) + [dict(fx.row("TC-009", fx.tcs()),
                                           **{"TC-ID": "TC-010", "Verifies": fx.SR1})]  # fmt: skip
    findings = _analyze(trace, fx.write(tmp_path, tc_rows=tcs))
    assert any(
        f.startswith("LLR LLR-001 has no test (TC) - a parent")
        for f in findings.orphans
    )
    assert trace.exit_code(findings, STRICT) == 1


# --- the checker and the stage read the tree (LLR-481) ------------------------


def test_the_triangle_rule_reads_a_grandchilds_requirement_up_its_chain():
    """Implements: TC-567"""
    trace = load_script("trace")
    coherent = [{"TC-ID": "TC-020", "Verifies": fx.SR1 + ";" + fx.GRAND}]
    incoherent = [{"TC-ID": "TC-021", "Verifies": fx.SR2 + ";" + fx.GRAND}]
    assert trace.triangle_findings(coherent, fx.llrs()) == []
    [line] = trace.triangle_findings(incoherent, fx.llrs())
    assert line.startswith(
        "TC TC-021 cites LLR-003 alongside SR SR-002 but LLR-003 decomposes SR-001"
    )


def test_the_paraphrase_advisory_compares_a_grandchild_with_its_chains_requirement():
    """Implements: TC-567"""
    trace_text = load_script("trace_text")
    llrs = fx.llrs()
    fx.row(fx.GRAND, llrs)["Detail"] = (
        "The kit shall export the records a reviewer selects."
    )
    [line] = trace_text.paraphrase_advisories(fx.srs(), llrs)
    assert line.startswith("LLR LLR-003 Detail mostly re-words SR-001")


def test_a_grandchilds_effective_perspectives_include_its_chains_requirements():
    """Implements: TC-567"""
    trace = load_script("trace")
    srs = fx.srs()
    srs[0]["Hat-Refs"] = "SECURITY"
    by_id = {r["SR-ID"]: r for r in srs}
    llrs = fx.llrs()
    srs_of = kspine.llr_tree(llrs).srs_of
    assert trace.effective_hats(fx.row(fx.GRAND, llrs), by_id, srs_of) == ["SECURITY"]
    _f, advisories = trace.hat_findings(srs, llrs, {"SECURITY"}, by_id)
    [coverage] = [a for a in advisories if a.startswith("hat coverage")]
    # SR-002 and its one row are the two uncovered; the three tree rows are not
    assert coverage.startswith("hat coverage: 2 of 6 ")


def _forest(trace, llrs=None, tcs=None):
    srs = fx.srs()
    return trace.build_forest(
        {"SN-001"}, srs, llrs or fx.llrs(), tcs or fx.tcs(), set()
    )


def test_the_outline_nests_the_grandchild_under_the_child_under_the_top_row():
    """Implements: TC-567"""
    trace = load_script("trace")
    lines = trace.outline_lines(_forest(trace))
    at = {
        line.strip()[2:].split(" ")[0]: len(line) - len(line.lstrip()) for line in lines
    }
    assert at[fx.TOP] < at[fx.CHILD] < at[fx.GRAND]
    order = [line.strip()[2:].split(" ")[0] for line in lines]
    assert order[order.index(fx.TOP) :][:5] == [
        fx.TOP,
        "TC-001",
        fx.CHILD,
        "TC-002",
        fx.GRAND,
    ]
    assert not any("no SR parent" in line for line in lines)


def test_the_matrix_lists_every_row_below_a_requirement():
    """Implements: TC-567"""
    trace = load_script("trace")
    rows = trace.matrix_lines(fx.srs(), fx.llrs(), fx.tcs())
    assert "| SR-001 | LLR-001 LLR-002 LLR-003 | TC-001 | Accepted |" in rows
    assert "| SR-002 | LLR-009 | TC-009 | Accepted |" in rows


def test_the_graph_draws_each_parent_link():
    """Implements: TC-567"""
    trace = load_script("trace")
    lines = trace.mermaid_graph({"SN-001"}, fx.srs(), fx.llrs(), fx.tcs(), set())
    assert "    LLR_001 --> LLR_002" in lines
    assert "    LLR_002 --> LLR_003" in lines
    assert "    SR_001 --> LLR_001" in lines


def test_the_stage_places_a_grandchild_in_its_requirements_phase():
    """Implements: TC-567"""
    derive_stage = load_script("derive_stage")
    groups = derive_stage._phase_groups(fx.srs(), fx.llrs(), fx.tcs())
    phase1 = [r["LLR-ID"] for r in groups["1"][1]]
    assert phase1 == list(fx.TREE)
    assert {r["TC-ID"] for r in groups["1"][2]} == {"TC-001", "TC-002", "TC-003"}
    assert [r["LLR-ID"] for r in groups["2"][1]] == [fx.OTHER]


def _spine(llrs):
    return {
        "srs": fx.srs(), "llrs": llrs, "tcs": fx.tcs(), "sn_ids": {"SN-001"},
        "sn_draft": set(), "bifs": [], "cmps": [], "have_bifs": False,
        "have_cmps": False,
    }  # fmt: skip


def test_a_drafted_grandchild_holds_its_phases_live_reading():
    """Implements: TC-567"""
    derive_stage = load_script("derive_stage")
    drafted = _spine(fx.llrs(**{fx.GRAND: "Drafted"}))
    _overall, live = derive_stage._stage_map(drafted, settled=False)
    _overall, settled = derive_stage._stage_map(drafted, settled=True)
    _overall, all_settled = derive_stage._stage_map(_spine(fx.llrs()), settled=True)
    assert live["1"] == "DevStg-LLReqs"
    assert live["2"] == "DevStg-Impl"
    assert settled == all_settled


def test_the_settled_grouping_reads_the_walk_over_the_live_rows():
    """A settled child under a Drafted parent keeps its requirement's phase:
    the settled subset drops the parent, so the chain is read over the live
    rows and handed in.

    Implements: TC-567"""
    derive_stage = load_script("derive_stage")
    live = fx.llrs(**{fx.TOP: "Drafted"})
    settled = [r for r in live if r["Status"] != "Drafted"]
    srs_of = kspine.llr_tree(live).srs_of
    groups = derive_stage._phase_groups(fx.srs(), settled, fx.tcs(), srs_of=srs_of)
    assert [r["LLR-ID"] for r in groups["1"][1]] == [fx.CHILD, fx.GRAND]
    assert {r["TC-ID"] for r in groups["1"][2]} == {"TC-001", "TC-002", "TC-003"}


# --- the briefs read the tree (Done-when 2; regression cases, D5) ------------


def test_the_acceptance_hierarchy_nests_the_grandchild_under_its_parent():
    trace = load_script("trace")
    lines = trace.acceptance_lines(
        "SR-001,SR-002", {"SN-001"}, fx.srs(), fx.llrs(), fx.tcs()
    )
    heads = [line for line in lines if line.startswith("#### LLR-")]
    assert heads == [
        "#### LLR-001 — Export pipeline [Accepted]",
        "#### LLR-002 — Row selection [Accepted] (below LLR-001)",
        "#### LLR-003 — Flag parsing [Accepted] (below LLR-002)",
        "#### LLR-009 — Import reader [Accepted]",
    ]


def test_an_srs_chain_holds_every_row_below_it():
    trace = load_script("trace")
    chain = trace.spine_chain(
        fx.SR1, fx.srs(), *trace.chain_buckets(fx.llrs(), fx.tcs())
    )
    assert [rid for kind, rid, _row in chain if kind == "LLR"] == list(fx.TREE)
    assert [rid for kind, rid, _row in chain if kind == "TC"] == [
        "TC-001",
        "TC-002",
        "TC-003",
    ]


def test_the_re_acceptance_model_owes_a_drafted_grandchilds_first_acceptance(tmp_path):
    trace = load_script("trace")
    llrs = fx.llrs(**{fx.GRAND: "Drafted"})
    model = trace.reaccept_model(tmp_path, fx.srs(), llrs, fx.tcs(), snapshot=None)
    [entry] = [e for e in model if e["id"] == fx.SR1]
    assert entry["kind"] == "accept"
    assert [r["id"] for r in entry["rows"] if r["drafted"]] == [fx.GRAND]


def test_the_consolidation_briefs_spine_names_the_grandchild(tmp_path):
    adjudicate_brief = load_script("adjudicate_brief")
    root = fx.write(tmp_path)
    wanted = adjudicate_brief._cited_spine(
        root, ["WI-001"], {"WI-001": {"SR-Refs": fx.SR1}}
    )
    assert wanted == {fx.SR1, *fx.TREE}


def test_the_context_blocks_code_map_names_the_grandchild(tmp_path):
    intake = load_script("intake")
    root = fx.write(tmp_path)
    block = intake._context_block(root, {"WI-ID": "WI-001", "SR-Refs": fx.SR1}, [])
    assert "- LLR-003 [" in block
    assert "- TC-003 -> " in block


# --- the remaining readers read the tree (Done-when 2; regression cases) -----


def test_the_component_view_reaches_a_placed_grandchilds_requirement():
    gen_components = load_script("gen_components")
    llrs = fx.llrs()
    tcs = fx.tcs() + [{"TC-ID": "TC-030", "Verifies": fx.GRAND + ";IF-001"}]
    ifs = [{"IF-ID": "IF-001", "Owner": "CMP-001", "Consumers": "CMP-001"}]
    cmps = [{"CMP-ID": "CMP-001", "Name": "Exporter"}]
    view, unplaced = gen_components.build(cmps, fx.srs(), llrs, ifs, tcs, {})
    assert fx.SR1 in view["CMP-001"]["sr_refs"]
    assert fx.SR1 not in unplaced["sr_refs"]


def test_the_implemented_id_census_claims_a_grandchild_of_a_done_rows_requirement(
    monkeypatch, tmp_path
):
    census = load_script("census")
    root = fx.write(tmp_path)
    monkeypatch.setattr(census.schedule, "load_wis",
                        lambda _rows: [{"status": "done", "srs": [fx.SR1]}])  # fmt: skip
    monkeypatch.setattr(census.ac, "load_registry_rows", lambda _root: [])
    assert census._implemented_ids(root) >= {fx.SR1, *fx.TREE}


def test_the_touched_module_prefilter_sees_a_grandchilds_files():
    consolidate = load_script("consolidate")
    index = {fx.GRAND: ["project-trajectory/scripts/flags.py"]}
    assert consolidate._llr_modules({fx.SR1}, fx.llrs(), index) == {"flags.py"}


def test_the_release_checklists_phase_scope_keeps_a_grandchild():
    checklist = load_script("gen_release_checklist")
    ids = checklist._scope_ids(fx.srs(), fx.llrs(), {"1"}, None)
    assert ids >= {fx.SR1, *fx.TREE}
    assert fx.OTHER not in ids


def test_the_okf_export_links_a_child_to_its_parent(tmp_path):
    gen_okf = load_script("gen_okf")
    out = gen_okf.emit(fx.write(tmp_path))
    child = out["low-level-requirements/LLR-002.md"]
    parent = out["low-level-requirements/LLR-001.md"]
    line = next(x for x in child.splitlines() if x.startswith("- Decomposes:"))
    assert "[LLR-001](../low-level-requirements/LLR-001.md)" in line
    line = next(x for x in parent.splitlines() if x.startswith("- Decomposed by:"))
    assert "[LLR-002](../low-level-requirements/LLR-002.md)" in line


def test_the_knowledge_pack_join_reaches_a_placed_grandchilds_requirement(tmp_path):
    check_trajectory = load_script("check_trajectory")
    root = fx.write(tmp_path, tc_rows=fx.tcs() + [
        {"TC-ID": "TC-030", "Verifies": fx.GRAND + ";IF-001"}])  # fmt: skip
    (root / "docs/requirements/interfaces.toml").write_text(
        '[interface.IF-001]\nowner = "CMP-001"\nconsumers = ["CMP-001"]\n'
        'channel = "call"\n',
        encoding="utf-8",
    )
    assert check_trajectory._placed_sr_components(root, ["CMP-001"]) == {
        fx.SR1: {"CMP-001"}
    }


# --- the test-first pairing reads the tree (LLR-257) --------------------------


def test_a_case_naming_only_a_grandchild_is_paired_with_its_chains_requirement():
    """Implements: TC-565"""
    check_test_first = load_script("check_test_first")
    design = {r["LLR-ID"]: r for r in fx.llrs()}
    tests = {"TC-003": {"TC-ID": "TC-003", "Verifies": fx.GRAND}}
    pairs = check_test_first._associations(tests, design)
    assert ("TC-003", fx.SR1) in pairs


# --- the state view draws a child inside its parent (LLR-482) ----------------

_CELL = re.compile(r'<g class="cell (\w+)" data-id="([^"]+)"[^>]*>.*?<rect x="(\d+)"')


def _columns(tmp_path, llrs):
    from rendering import traj_views

    svg, _details, _desc = traj_views.arch_icicle(fx.write(tmp_path, llr_rows=llrs))
    return {rid: (tier, int(x)) for tier, rid, x in _CELL.findall(svg)}


def test_the_spine_view_draws_each_child_one_column_further_in(tmp_path):
    """Implements: TC-562"""
    cols = _columns(tmp_path, fx.llrs())
    step = cols[fx.SR1][1] - cols["SN-001"][1]
    assert cols[fx.TOP][1] == 2 * step
    assert cols[fx.CHILD][1] == 3 * step
    assert cols[fx.GRAND][1] == 4 * step
    assert {cols[t][1] for t in ("TC-001", "TC-002", "TC-003", "TC-009")} == {5 * step}
    assert cols[fx.OTHER][1] == 2 * step


def test_a_spine_with_no_child_keeps_one_design_column(tmp_path):
    """Implements: TC-562"""
    flat = [dict(r, **{"SR-Refs": fx.SR1}) for r in fx.llrs()]
    for r in flat:
        r.pop("Parent", None)
    flat[-1]["SR-Refs"] = fx.SR2
    cols = _columns(tmp_path, flat)
    step = cols[fx.SR1][1] - cols["SN-001"][1]
    assert {cols[rid][1] for rid in (*fx.TREE, fx.OTHER)} == {2 * step}
    assert {cols[t][1] for t in ("TC-001", "TC-002", "TC-003", "TC-009")} == {3 * step}
