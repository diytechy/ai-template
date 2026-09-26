"""The assumption tier's rules, called on in-memory rows (TC-219, TC-220,
TC-221, TC-224).

`assumption_rules.py` is a pure join module beside `frame_rules.py`: it reads
no file, so every rule here is driven with plain row dicts in the carrier's
column names. The checker-level contract (which pipe each finding rides, the
exit code, the watermark, the scaffold's blank form) is pinned separately in
`tests/test_assumptions_registry.py`, which drives `trace.py` over scaffolds.

A domain assumption is a claim about the world a requirement's argument relies
on (SR-191), a surrogate is a stand-in for an outside party in tests (SR-192),
each requirement cites its assumptions or records why it needs none (SR-193)
and declares its form (SR-194), and an assumption nothing cites or nothing
could falsify is reported (SR-196).
"""

import copy
import tomllib

import pytest

from conftest import KIT, load_script

CARRIER = load_script("spine_carrier")
import kitlib.spine as SPINE  # noqa: E402  (after the load above puts scripts/ on the path)


@pytest.fixture(scope="module")
def rules():
    """The module under test, loaded once. A fixture rather than a module-level
    load, so a missing module reds every case on its own line."""
    return load_script("assumption_rules")


# --- the frame and the rows the cases share ----------------------------------

EXTS = [{"EXT-ID": "EXT-001"}, {"EXT-ID": "EXT-002"}]
BIFS = [
    {"B-ID": "B-01", "Entity": "EXT-001"},
    {"B-ID": "B-02", "Entity": "EXT-002"},
]


def _da(did="DA-001", **cells):
    row = {
        "DA-ID": did,
        "EffectAt": "B-01",
        "Assumption": "A reviewer reads the brief before approving.",
        "HoldsWhen": "The brief is short enough to read in one sitting.",
        "Obstacle": "The brief grows past what one sitting reads.",
        "Falsifier": "An approval recorded before the brief was opened.",
        "Status": "Drafted",
        "Standing": "active",
    }
    row.update(cells)
    return row


def _sur(sid="SUR-001", **cells):
    row = {
        "SUR-ID": sid,
        "Name": "Scripted reviewer",
        "Emulates": "EXT-001",
        "Description": "A model run reading the brief in place of a person.",
        "Status": "Drafted",
    }
    row.update(cells)
    return row


def _sr(sid, **cells):
    row = {"SR-ID": sid, "SN-Refs": "SN-001"}
    row.update(cells)
    return row


def _named(lines, *needles):
    return [line for line in lines if all(n in line for n in needles)]


# --- TC-219: surrogate_findings (SR-192, LLR-221) ------------------------------


def test_a_surrogate_emulating_a_declared_entity_passes(rules):
    das = [_da(RealizedBy="SUR-001")]
    assert rules.surrogate_findings([_sur()], das, EXTS, BIFS) == ([], [])


@pytest.mark.parametrize("party", ["EXT-009", "CMP-001", "IF-001"])
def test_an_undeclared_or_non_entity_party_fails_naming_the_surrogate(rules, party):
    """Only a declared entity resolves in `Emulates`: an unknown entity id and
    a component or interface id fail alike."""
    das = [_da(RealizedBy="SUR-001")]
    failures, _advisories = rules.surrogate_findings(
        [_sur(Emulates=party)], das, EXTS, BIFS
    )
    assert _named(failures, "SUR-001", party), failures


def test_an_empty_emulates_list_fails_naming_the_surrogate(rules):
    das = [_da(RealizedBy="SUR-001")]
    for empty in ("", "  "):
        failures, _advisories = rules.surrogate_findings(
            [_sur(Emulates=empty)], das, EXTS, BIFS
        )
        assert _named(failures, "SUR-001", "Emulates"), failures


@pytest.mark.parametrize("cell", ["Name", "Description", "Status"])
def test_a_surrogate_missing_a_required_cell_fails_naming_it(rules, cell):
    row = _sur()
    del row[cell]
    failures, _advisories = rules.surrogate_findings(
        [row], [_da(RealizedBy="SUR-001")], EXTS, BIFS
    )
    assert _named(failures, "SUR-001", cell), failures


def test_the_surrogate_required_cells_are_the_stated_four(rules):
    assert rules.SUR_REQUIRED == ("Name", "Emulates", "Description", "Status")


def test_a_fidelity_assumption_naming_an_undeclared_surrogate_fails_naming_it(rules):
    failures, _advisories = rules.surrogate_findings(
        [_sur()], [_da(RealizedBy="SUR-009")], EXTS, BIFS
    )
    assert _named(failures, "DA-001", "SUR-009"), failures


def test_a_fidelity_assumption_landing_off_its_surrogates_parties_fails(rules):
    """DA-001 lands on B-02, a crossing of EXT-002, while its surrogate emulates
    EXT-001 only: the stand-in answers for a party the assumption never
    reaches."""
    failures, _advisories = rules.surrogate_findings(
        [_sur()], [_da(EffectAt="B-02", RealizedBy="SUR-001")], EXTS, BIFS
    )
    assert _named(failures, "DA-001", "SUR-001"), failures
    assert all(f.startswith("assumption DA-001 ") for f in failures), failures


def test_a_fidelity_assumption_landing_on_an_emulated_partys_crossing_passes(rules):
    both = _sur(Emulates="EXT-001;EXT-002")
    das = [_da(EffectAt="B-02", RealizedBy="SUR-001")]
    assert rules.surrogate_findings([both], das, EXTS, BIFS) == ([], [])


def test_a_fidelity_assumption_names_exactly_one_surrogate(rules):
    surs = [_sur(), _sur("SUR-002")]
    failures, _advisories = rules.surrogate_findings(
        surs, [_da(RealizedBy="SUR-001;SUR-002")], EXTS, BIFS
    )
    assert _named(failures, "DA-001", "SUR-001", "SUR-002"), failures


def test_a_surrogate_no_assumption_names_is_one_advisory(rules):
    surs = [_sur(), _sur("SUR-002")]
    failures, advisories = rules.surrogate_findings(
        surs, [_da(RealizedBy="SUR-001")], EXTS, BIFS
    )
    assert failures == []
    assert len(advisories) == 1 and "SUR-002" in advisories[0], advisories


def test_a_surrogate_status_outside_the_vocabulary_fails_the_integrity_floor(rules):
    """The failure is the surrogate rule's, and the tier composes every
    surrogate failure into the always-on integrity class, not the frame class
    `--strict` alone reads."""
    surs = [_sur(Status="Bananas")]
    das = [_da(RealizedBy="SUR-001")]
    failures, _advisories = rules.surrogate_findings(surs, das, EXTS, BIFS)
    assert _named(failures, "SUR-001", "Bananas"), failures
    frame, integrity, _advisories = rules.assumption_tier_findings(
        [], das, surs, EXTS, BIFS
    )
    assert _named(integrity, "SUR-001", "Bananas"), integrity
    assert not _named(frame, "SUR-001"), frame


# --- TC-220: classification and citations (SR-193, LLR-222, LLR-223) ----------

DAS = [_da("DA-001"), _da("DA-002")]


def test_each_requirement_is_classified_by_its_citations_and_its_waiver(rules):
    srs = [
        _sr("SR-001", **{"DA-Refs": "DA-001;DA-002"}),
        _sr("SR-002", Coincident="The requirement's output is the outcome."),
        _sr("SR-003"),
        _sr("SR-004", **{"DA-Refs": "DA-001", "Coincident": "Both, by mistake."}),
    ]
    assert rules.classify_srs(srs, DAS) == {
        "SR-001": "bridged",
        "SR-002": "coincident",
        "SR-003": "unclassified",
        "SR-004": "both",
    }
    failures, advisories = rules.sr_classification_advisories(srs, DAS)
    assert failures == []
    assert not _named(advisories, "SR-001") and not _named(advisories, "SR-002")
    assert len(_named(advisories, "SR-003")) == 1, advisories
    assert len(_named(advisories, "SR-004")) == 1, advisories
    assert len(advisories) == 2, advisories


@pytest.mark.parametrize("empty", ["", "   "])
def test_an_empty_or_whitespace_citation_counts_as_absent(rules, empty):
    srs = [_sr("SR-001", **{"DA-Refs": empty})]
    assert rules.classify_srs(srs, DAS) == {"SR-001": "unclassified"}
    failures, advisories = rules.sr_classification_advisories(srs, DAS)
    assert failures == [] and len(_named(advisories, "SR-001")) == 1, advisories


def test_a_citation_naming_an_undeclared_assumption_fails_naming_the_requirement(
    rules,
):
    srs = [_sr("SR-001", **{"DA-Refs": "DA-001;DA-009"})]
    failures, advisories = rules.sr_classification_advisories(srs, DAS)
    assert _named(failures, "SR-001", "DA-009"), failures
    assert "SR-001" not in rules.classify_srs(srs, DAS)
    assert advisories == []


def test_an_assumptions_needs_are_derived_from_the_requirements_citing_it(rules):
    srs = [
        _sr("SR-001", **{"SN-Refs": "SN-001", "DA-Refs": "DA-001"}),
        _sr("SR-002", **{"SN-Refs": "SN-002;SN-003", "DA-Refs": "DA-001;DA-002"}),
        _sr("SR-003", **{"SN-Refs": "SN-004"}),
    ]
    before = copy.deepcopy(srs)
    citing = rules.da_citing_srs(srs)
    assert citing == {"DA-001": ["SR-001", "SR-002"], "DA-002": ["SR-002"]}
    by_id = {r["SR-ID"]: r for r in srs}
    served = {
        did: {sn for sid in sids for sn in SPINE.refs(by_id[sid]["SN-Refs"])}
        for did, sids in citing.items()
    }
    assert served == {
        "DA-001": {"SN-001", "SN-002", "SN-003"},
        "DA-002": {"SN-002", "SN-003"},
    }
    # The need link stays on the requirement: nothing is rewritten, and the
    # assumption's schema has no cell a need could be recorded in.
    assert srs == before
    assert not {"sn_refs", "needs"} & set(SPINE.OFFSPINE_KEYS["DA-ID"])


def test_no_assumptions_registry_makes_every_call_vacuous(rules):
    srs = [_sr("SR-001"), _sr("SR-002", **{"DA-Refs": "DA-009"})]
    assert rules.classify_srs(srs, []) == {}
    assert rules.sr_classification_advisories(srs, []) == ([], [])
    assert rules.uncited_assumption_advisories([], srs) == []
    assert rules.assumption_tier_findings(srs, [], [], EXTS, BIFS) == ([], [], [])


def test_the_template_example_requirement_carries_both_new_keys():
    template = tomllib.loads(
        (KIT / "registries" / "system-requirements.template.toml").read_text(
            encoding="utf-8"
        )
    )
    example = template["requirement"]["SR-000"]
    assert "da_refs" in example and "coincident" in example, sorted(example)
    for key in ("da_refs", "coincident", "form"):
        assert key in SPINE.SPINE_TIER_KEYS["SR-ID"], key


# --- TC-221: the form cell (SR-194, LLR-224) -----------------------------------


def test_the_three_forms_are_declared_once_in_the_schema_module():
    assert SPINE.FORM_VALUES == ("interface", "assumption", "cross-cutting")


@pytest.mark.parametrize("form", ["interface", "assumption", "cross-cutting"])
def test_each_of_the_three_forms_passes(rules, form):
    assert rules.sr_form_findings([_sr("SR-001", Form=form)]) == ([], [])


def test_a_requirement_with_no_form_is_one_advisory_naming_it(rules):
    failures, advisories = rules.sr_form_findings([_sr("SR-001")])
    assert failures == []
    assert len(advisories) == 1 and "SR-001" in advisories[0], advisories


def test_a_form_outside_the_three_fails_the_integrity_class_naming_the_row(rules):
    srs = [_sr("SR-001", Form="behavioural")]
    failures, advisories = rules.sr_form_findings(srs)
    assert _named(failures, "SR-001", "behavioural"), failures
    assert advisories == []
    frame, integrity, _advisories = rules.assumption_tier_findings(
        srs, DAS, [], EXTS, BIFS
    )
    assert _named(integrity, "SR-001", "behavioural"), integrity
    assert not _named(frame, "behavioural"), frame


def test_with_no_assumptions_registry_no_form_is_asked_for(rules):
    """The rule itself asks every requirement; the TIER asks only once the
    registry holds a real assumption row, so the vacuity lives where the tier
    is composed. The template's `-000` example is no adoption."""
    srs = [_sr("SR-001"), _sr("SR-002", Form="behavioural")]
    failures, advisories = rules.sr_form_findings(srs)
    assert _named(failures, "SR-002") and _named(advisories, "SR-001")
    for das in ([], [_da("DA-000")]):
        assert rules.assumption_tier_findings(srs, das, [], EXTS, BIFS) == (
            [],
            [],
            [],
        ), das
    _frame, integrity, advisories = rules.assumption_tier_findings(
        srs, DAS, [], EXTS, BIFS
    )
    assert _named(integrity, "SR-002", "behavioural"), integrity
    assert _named(advisories, "SR-001", "Form"), advisories


# --- TC-224: uncited and falsifier-less assumptions (SR-196, LLR-228) ----------


@pytest.mark.parametrize("status", ["Drafted", "Approved"])
def test_an_assumption_no_requirement_cites_is_reported_once(rules, status):
    das = [_da("DA-001", Status=status), _da("DA-002", Status=status)]
    srs = [_sr("SR-001", **{"DA-Refs": "DA-001"})]
    advisories = rules.uncited_assumption_advisories(das, srs)
    assert len(advisories) == 1 and "DA-002" in advisories[0], advisories


@pytest.mark.parametrize("status", ["Drafted", "Approved"])
def test_an_assumption_with_no_falsifier_is_reported_once(rules, status):
    blank = _da("DA-002", Status=status)
    del blank["Falsifier"]
    das = [_da("DA-001", Status=status), blank, _da("DA-003", Falsifier="  ")]
    advisories = rules.no_falsifier_advisories(das)
    assert len(advisories) == 2, advisories
    assert _named(advisories, "DA-002") and _named(advisories, "DA-003")


@pytest.mark.parametrize("status", ["Drafted", "Approved"])
def test_a_cited_assumption_with_a_falsifier_produces_nothing(rules, status):
    das = [_da("DA-001", Status=status)]
    srs = [_sr("SR-001", **{"DA-Refs": "DA-001"})]
    assert rules.uncited_assumption_advisories(das, srs) == []
    assert rules.no_falsifier_advisories(das) == []


def test_neither_report_moves_the_strict_exit(rules):
    """Both reports ride the warn pipe: the tier routes them to its advisories,
    never to the frame or integrity class a strict exit reads."""
    blank = _da("DA-001")
    del blank["Falsifier"]
    frame, integrity, advisories = rules.assumption_tier_findings(
        [_sr("SR-001", Form="interface", Coincident="Its output is the outcome.")],
        [blank],
        [],
        EXTS,
        BIFS,
    )
    assert frame == [] and integrity == [], (frame, integrity)
    assert _named(advisories, "DA-001", "cite"), advisories
    assert _named(advisories, "DA-001", "falsif"), advisories


# --- the tier's applies-when (SR-191) ------------------------------------------


def test_with_no_crossing_declared_the_whole_tier_is_vacuous(rules):
    broken = _da(EffectAt="B-09", Status="Bananas", RealizedBy="SUR-009")
    srs = [_sr("SR-001", **{"DA-Refs": "DA-404"}, Form="behavioural")]
    assert rules.assumption_row_findings([broken], []) == []
    assert rules.assumption_tier_findings(
        srs, [broken], [_sur(Emulates="EXT-404")], [], []
    ) == ([], [], [])


def test_the_example_rows_are_inert(rules):
    example = _da("DA-000", EffectAt="B-000", Status="Bananas")
    assert rules.assumption_row_findings([example], BIFS) == []
    sur = _sur("SUR-000", Emulates="EXT-000", Status="Bananas")
    assert rules.surrogate_findings([sur], [example], EXTS, BIFS) == ([], [])
