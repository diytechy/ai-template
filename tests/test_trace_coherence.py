"""The checker's cross-row coherence rules, and the two typed bags around them
(WI-483 slice 4, program shape item 5 — the engine splits).

`trace.analyze` was 553 lines at C901 complexity 50: the join rules, the carrier
sweeps, the delivery filter, the status criterion and the assembly of a 37-field
result, in one function, with `Registries` and `Findings` as EMPTY classes
populated as attribute bags. This file guards what the split bought:

  * the rules are reachable and testable on their own, one tier at a time,
    without loading a registry off disk;
  * the emission ORDER the report and the console compare is a property of the
    composer rather than of where an `append` happened to sit;
  * `Registries` is frozen and total, so no field springs into existence at a
    call site (the two `getattr(reg, ..., [])` defensive reads that shape used
    to force are gone) and nothing downstream may mutate what LOADING produced;
  * `Findings` is the mutable half, and its list defaults are PER INSTANCE — the
    classic dataclass trap, and the one that would silently make two analyses
    share a findings list;
  * `AnalysisFlags` is the engine's config, so a non-CLI caller no longer forges
    an `argparse.Namespace` to pass four booleans;
  * `coherence.py` imports no sibling of `scripts/`, which is what keeps the
    join rules below the module that composes them.

The BEHAVIOUR of every rule here is unchanged and is already covered end to end
by `tests/test_trace.py` and `tests/test_trace_rules.py`; the split was proven
byte-identical by a before/after compare of the console, `test/report.md` and
the gap census. These tests are about the boundary, not about re-asserting the
rules through a second door.
"""

import ast
import dataclasses
import pathlib

import pytest
from conftest import SCRIPTS, load_script


@pytest.fixture(scope="module")
def coherence():
    return load_script("coherence")


@pytest.fixture(scope="module")
def trace():
    return load_script("trace")


def _sr(sid, **cells):
    row = {"SR-ID": sid, "Status": "Approved", "Verification": "Test"}
    row.update(cells)
    return row


# --- the rules, one tier at a time -------------------------------------------


def test_the_orphan_rules_emit_sr_then_llr_then_tc_then_sn(coherence):
    # The order is what the report and the console compare, so it is a
    # property of the composer and not of where an append happened to sit.
    srs = [_sr("SR-001", **{"SN-Refs": "SN-001"})]
    llrs = [{"LLR-ID": "LLR-001", "SR-Refs": "", "Status": "Approved"}]
    tcs = [{"TC-ID": "TC-001", "Verifies": "", "Status": "Approved"}]
    orphans, ids = coherence.spine_orphan_findings(
        srs, llrs, tcs, [], {"SR-001"}, {"LLR-001"}, {"SN-001", "SN-002"}, set()
    )
    kinds = [f.split()[0] for f in orphans]
    assert kinds == sorted(kinds, key=["SR", "LLR", "TC", "SN"].index)
    # Every finding contributed its at-fault id, and nothing else did.
    assert ids == {"SR-001", "LLR-001", "TC-001", "SN-002"}


def test_a_drafted_row_stands_the_child_rules_down_but_not_its_sn_link(coherence):
    drafted = _sr("SR-002", Status="Drafted")
    orphans, _ = coherence.spine_orphan_findings(
        [drafted], [], [], [], {"SR-002"}, set(), {"SN-001"}, set()
    )
    assert orphans[0] == "SR SR-002 links no SN (every SR needs >=1 SN-Ref)"
    assert not [f for f in orphans if f.startswith("SR SR-002 has no")]


def test_off_spine_backlinks_resolve_against_ids_and_llr_module_paths(coherence):
    llrs = [{"LLR-ID": "LLR-001", "Module": "scripts/thing.py"}]
    assert coherence.llr_module_ids(llrs) == {"scripts/thing.py"}
    targets = {"SR-001", "LLR-001", "scripts/thing.py"}
    assert (
        coherence.budget_backlink_findings(
            [{"PB-ID": "PB-001", "Refs": "scripts/thing.py"}], targets
        )
        == []
    )
    assert coherence.budget_backlink_findings(
        [{"PB-ID": "PB-002", "Refs": ""}], targets
    )
    assert coherence.budget_backlink_findings(
        [{"PB-ID": "PB-003", "Refs": "SR-999"}], targets
    )
    assert coherence.delegation_findings(
        [{"REPO-ID": "REPO-001", "DelegatedSRs": "SR-999"}], {"SR-001"}
    )


def test_component_membership_is_checked_from_the_primitive_side(coherence):
    cmps = [{"CMP-ID": "CMP-001", "PartOf": "", "SupersededBy": ""}]
    assert coherence.component_membership_findings(cmps, [], [], [], []) == []
    bad = coherence.component_membership_findings(
        cmps, [{"LLR-ID": "LLR-001", "Component": "CMP-404"}], [], [], []
    )
    assert bad == ["LLR LLR-001 Component tag references unknown CMP-404"]
    # An empty component registry disarms the membership half entirely (a
    # project that declares no components tags nothing).
    assert (
        coherence.component_membership_findings(
            [], [{"LLR-ID": "LLR-001", "Component": "CMP-404"}], [], [], []
        )
        == []
    )


def test_the_knowledge_ref_resolves_only_the_pack_prefix(tmp_path, coherence):
    (tmp_path / "knowledge").mkdir()
    (tmp_path / "knowledge" / "real.md").write_text("pack", encoding="utf-8")
    rows = [
        {"CMP-ID": "CMP-001", "Knowledge": "docs/knowledge/real"},
        {"CMP-ID": "CMP-002", "Knowledge": "https://example.test/thing"},
        {"CMP-ID": "CMP-003", "Knowledge": "docs/knowledge/missing"},
    ]
    out = coherence.knowledge_pack_advisories(rows, tmp_path)
    assert len(out) == 1 and "CMP-003" in out[0]
    # Containment: a traversal ref never resolves outside the pack root.
    escape = coherence.knowledge_pack_advisories(
        [{"CMP-ID": "CMP-004", "Knowledge": "docs/knowledge/../../etc/passwd"}],
        tmp_path,
    )
    assert len(escape) == 1


def test_the_phase_scope_always_covers_the_foundation_phase(coherence):
    srs = [_sr("SR-001", Phase="1"), _sr("SR-002", Phase="5")]
    scope = coherence.PhaseScope.of(srs, "5")
    assert scope.covers(srs[0]), "the minimum phase is in scope for every filter"
    assert scope.covers(srs[1])
    assert not scope.covers(_sr("SR-003", Phase="3"))
    # A blank Phase is downstream-compat and always in scope; no filter covers all.
    assert scope.covers(_sr("SR-004", Phase=""))
    assert coherence.PhaseScope.of(srs, "").covers(_sr("SR-005", Phase="3"))


def test_the_status_criterion_defers_out_of_phase_and_stands_down_for_drafted(
    coherence,
):
    srs = [
        _sr("SR-001", Status="Implemented", Phase="1"),
        _sr("SR-002", Status="Drafted", Phase="1"),
        _sr("SR-003", Status="Implemented", Phase="7"),
    ]
    findings, deferred = coherence.status_criterion_findings(
        srs, coherence.PhaseScope.of(srs, "1")
    )
    assert len(findings) == 1 and "SR-001" in findings[0]
    assert len(deferred) == 1 and "SR-003" in deferred[0]


# --- the typed bags ----------------------------------------------------------


def test_registries_is_frozen_and_total(trace):
    reg = trace.load_registries(pathlib.Path("docs"))
    assert dataclasses.is_dataclass(reg)
    with pytest.raises(dataclasses.FrozenInstanceError):
        reg.srs = []
    # TOTAL: the loader fills every declared field, so no reader needs a
    # `getattr(reg, name, default)` to survive a bag that was never populated.
    for f in dataclasses.fields(reg):
        assert getattr(reg, f.name) is not None or f.name == "sn_md"


def test_the_loader_is_the_only_construction_site_of_registries():
    # A frozen record is only a guarantee while the loader is the one place
    # that fills it; a second construction site is a second schema.
    sites = []
    for path in sorted(pathlib.Path(SCRIPTS).rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                name = getattr(fn, "id", None) or getattr(fn, "attr", None)
                if name == "Registries":
                    sites.append("{}:{}".format(path.name, node.lineno))
    assert len(sites) == 1, "Registries is constructed at " + "; ".join(sites)


def test_findings_list_defaults_are_per_instance(trace):
    # The dataclass trap this bag would otherwise walk into: two analyses
    # sharing one findings list. `field(default_factory=list)`, not `= []`.
    a, b = trace.Findings(), trace.Findings()
    a.watermark_advisories.append("x")
    assert b.watermark_advisories == []
    assert a.orphan_ids is not b.orphan_ids


def test_the_two_post_analyze_fields_are_declared_not_conjured(trace):
    # `watermark_advisories` and `snapshot_findings` are filled AFTER analyze
    # returns, because their rules read the filesystem and git. That is real
    # mutable runtime state and it is DECLARED, so a reader of the class knows
    # the fields exist before some later line invents them.
    names = {f.name for f in dataclasses.fields(trace.Findings)}
    assert {"watermark_advisories", "snapshot_findings"} <= names


def test_analysis_flags_takes_a_record_or_a_namespace(trace):
    import argparse

    ns = argparse.Namespace(
        phase="2", require_verified=True, no_placeholders=False, strict_schema=True
    )
    flags = trace.AnalysisFlags.of(ns)
    assert (flags.phase, flags.require_verified, flags.strict_schema) == (
        "2",
        True,
        True,
    )
    assert trace.AnalysisFlags.of(flags) is flags, "of() is idempotent"
    assert dataclasses.is_dataclass(flags) and not flags.no_placeholders


def test_no_caller_forges_an_argparse_namespace_for_the_engine():
    # The reason AnalysisFlags exists: census.gap_census imported argparse to
    # build a four-field Namespace, because the CLI namespace WAS the config
    # type. A future caller reaching for the same trick should red here.
    tree = ast.parse(pathlib.Path(SCRIPTS, "census.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert not any(a.name == "argparse" for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.module != "argparse"
    assert "AnalysisFlags" in pathlib.Path(SCRIPTS, "census.py").read_text(
        encoding="utf-8"
    )


# --- the boundary ------------------------------------------------------------


def test_the_coherence_rules_import_no_sibling_of_scripts():
    # What keeps the join rules BELOW the engine that composes them. kitlib is
    # allowed (it is the shipped row vocabulary); a sibling is not.
    tree = ast.parse(pathlib.Path(SCRIPTS, "coherence.py").read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    siblings = {p.stem for p in pathlib.Path(SCRIPTS).glob("*.py")} - {"coherence"}
    assert not (imported & siblings), "coherence.py reached for " + str(
        imported & siblings
    )


def test_trace_re_exports_every_moved_name(trace, coherence):
    # The move cost no caller a line: trace.py still answers to each name, and
    # to the SAME object rather than to a re-implementation.
    for name in (
        "spine_orphan_findings",
        "llr_module_ids",
        "budget_backlink_findings",
        "delegation_findings",
        "component_membership_findings",
        "knowledge_pack_advisories",
        "status_criterion_findings",
        "PhaseScope",
        "_repo_id",
    ):
        moved = getattr(trace, name)
        # Identity is not the test: `load_script` loads each module fresh, so
        # the two fixtures hold different objects for the same source. What
        # matters is that trace answers to the name and that the definition
        # lives in coherence.py, not in a re-implementation up here.
        assert moved is not None, name
        assert getattr(moved, "__module__", "coherence") == "coherence", name


def test_analyze_is_a_composer_and_stays_one():
    # The regression this slice exists to prevent: rules accreting back into
    # the engine. `analyze` is measured, not described — if it grows past the
    # composer it now is, that is the 553-line function coming back.
    tree = ast.parse(pathlib.Path(SCRIPTS, "trace.py").read_text(encoding="utf-8"))
    fn = next(
        n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "analyze"
    )
    span = fn.end_lineno - fn.lineno + 1
    assert span <= 240, "analyze is {} lines (was 553; composer budget 240)".format(
        span
    )
    # And no nested def: C901 charges one to its enclosing function, which is
    # exactly how this engine's number got to 50.
    assert not [
        n for n in ast.walk(fn) if isinstance(n, ast.FunctionDef) and n is not fn
    ]
