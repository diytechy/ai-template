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

The tier's two reach rules ride here too, on the same in-memory rows: an
assumption lands where each stakeholder it serves is, directly or through a
party that mediates for it (SR-195, TC-223), and a need met in operation has a
requirement or an assumption reaching an operation crossing (SR-188, TC-214).
The one frame rule they need, a recorded mediation resolving, is
`frame_rules.mediation_findings`, called here beside them. Which pipe those
three join is pinned here too, by calling `trace.analyze` in-process on an
empty registry: no scaffold, no subprocess.
"""

import copy
import dataclasses
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


# --- the reach frame the TC-223 and TC-214 cases share -------------------------
# EXT-001 is an operator's session with an operation crossing of its own; EXT-002
# the delivered package, crossed by the delivery system alone; EXT-003 an
# operator with no crossing of their own, reached only through EXT-004, a
# session that carries their writes and shows them the system's verdicts.

REACH_EXTS = [
    {"EXT-ID": "EXT-001"},
    {"EXT-ID": "EXT-002"},
    {"EXT-ID": "EXT-003"},
    {"EXT-ID": "EXT-004", "Mediates": "EXT-003"},
]
REACH_BIFS = [
    {"B-ID": "B-01", "Entity": "EXT-001", "System": "operation"},
    {"B-ID": "B-04", "Entity": "EXT-004", "System": "operation"},
    {"B-ID": "B-05", "Entity": "EXT-002", "System": "delivery"},
]


def _stk(sid, party=None, status="Approved"):
    row = {
        "STK-ID": sid,
        "Name": "Stakeholder " + sid,
        "Description": "Owns an outcome of the system in use.",
        "Status": status,
    }
    if party is not None:
        row["Party"] = party
    return row


def _need(nid, *stakeholders):
    """A need as `spine_carrier.load_needs` hands it over: lower-case keys, its
    id under `id` and a list cell `;`-joined."""
    return {"id": nid, "stakeholder_refs": ";".join(stakeholders)}


REACH_STKS = [
    _stk("STK-01", "EXT-001"),
    _stk("STK-02", "EXT-003"),
    _stk("STK-03"),
]
REACH_NEEDS = [
    _need("SN-001", "STK-01"),
    _need("SN-002", "STK-02"),
    _need("SN-003", "STK-03"),
]


@pytest.fixture(scope="module")
def frame_rules():
    return load_script("frame_rules")


def _reach(rules, das, srs, stks=REACH_STKS, surs=()):
    return rules.assumption_reach_advisories(
        das, srs, REACH_NEEDS, stks, REACH_EXTS, REACH_BIFS, list(surs)
    )


def _citing(sid, needs, das="DA-001", **cells):
    row = {"SR-ID": sid, "SN-Refs": needs, "DA-Refs": das}
    row.update(cells)
    return row


# --- TC-223: mediation_findings (SR-195, LLR-226) ------------------------------


def test_a_mediation_naming_a_declared_other_entity_passes(frame_rules):
    assert frame_rules.mediation_findings(REACH_EXTS) == []


@pytest.mark.parametrize("empty", ["", "   "])
def test_an_empty_mediation_is_no_mediation(frame_rules, empty):
    exts = REACH_EXTS[:3] + [{"EXT-ID": "EXT-004", "Mediates": empty}]
    assert frame_rules.mediation_findings(exts) == []


def test_a_mediation_naming_an_undeclared_entity_fails_naming_both(frame_rules):
    exts = REACH_EXTS[:3] + [{"EXT-ID": "EXT-004", "Mediates": "EXT-009"}]
    failures = frame_rules.mediation_findings(exts)
    assert len(failures) == 1 and _named(failures, "EXT-004", "EXT-009"), failures


def test_a_mediation_naming_the_entity_itself_fails_naming_it(frame_rules):
    exts = REACH_EXTS[:3] + [{"EXT-ID": "EXT-004", "Mediates": "EXT-004"}]
    failures = frame_rules.mediation_findings(exts)
    assert len(failures) == 1 and _named(failures, "EXT-004", "itself"), failures


def test_the_example_entitys_mediation_is_inert(frame_rules):
    exts = REACH_EXTS + [{"EXT-ID": "EXT-000", "Mediates": "EXT-404"}]
    assert frame_rules.mediation_findings(exts) == []


def test_the_entity_tier_ships_its_mediates_cell():
    """One entity id, carried as `mediates` and read as `Mediates`, and shipped
    on the template's example entity so the blank form shows it."""
    assert "mediates" in SPINE.OFFSPINE_KEYS["EXT-ID"]
    assert CARRIER.REGISTRY_COLUMN["mediates"] == "Mediates"
    template = tomllib.loads(
        (KIT / "registries" / "external.template.toml").read_text(encoding="utf-8")
    )
    assert "mediates" in template["entity"]["EXT-000"], sorted(
        template["entity"]["EXT-000"]
    )


# --- TC-223: reaching_parties and the reach check (SR-195, LLR-227) ------------


def test_reaching_parties_holds_each_needs_parties_and_their_mediators(rules):
    """A need reaches its approved stakeholders' parties and every entity whose
    `Mediates` names one of them; a need whose stakeholders declare no party
    reaches nobody."""
    assert rules.reaching_parties(REACH_NEEDS, REACH_STKS, REACH_EXTS) == {
        "SN-001": {"EXT-001"},
        "SN-002": {"EXT-003", "EXT-004"},
        "SN-003": set(),
    }


@pytest.mark.parametrize("status", ["Approved", "Founded"])
def test_landing_on_the_served_needs_stakeholders_party_passes(rules, status):
    """`Founded` reads above `Approved` on the one ladder, so an agreed
    stakeholder at either rung is read."""
    stks = [_stk("STK-01", "EXT-001", status)] + REACH_STKS[1:]
    das = [_da("DA-001", EffectAt="B-01")]
    assert _reach(rules, das, [_citing("SR-001", "SN-001")], stks) == []


def test_landing_on_a_party_that_mediates_for_it_passes(rules):
    """SN-002's stakeholder is EXT-003, which has no crossing of its own; B-04
    belongs to EXT-004, which mediates for it."""
    das = [_da("DA-001", EffectAt="B-04")]
    assert _reach(rules, das, [_citing("SR-001", "SN-002")]) == []


def test_a_served_need_no_landing_reaches_is_reported_naming_it(rules):
    """DA-001 serves SN-001 and SN-002 and lands on B-01 alone, which reaches
    only the first: the second need is named, and B-01 is not."""
    das = [_da("DA-001", EffectAt="B-01")]
    advisories = _reach(rules, das, [_citing("SR-001", "SN-001;SN-002")])
    assert len(advisories) == 1 and _named(advisories, "DA-001", "SN-002"), advisories
    assert not _named(advisories, "SN-001") and not _named(advisories, "B-01")


def test_a_landing_crossing_reaching_no_served_need_is_reported_naming_it(rules):
    """B-01 reaches SN-001 and B-04 reaches SN-002; B-05 reaches neither."""
    das = [_da("DA-001", EffectAt="B-01;B-04;B-05")]
    advisories = _reach(rules, das, [_citing("SR-001", "SN-001;SN-002")])
    assert len(advisories) == 1 and _named(advisories, "DA-001", "B-05"), advisories


def test_the_served_needs_are_derived_and_never_recorded(rules):
    """Needs served through two citing requirements are judged together, and
    no row handed in is written to."""
    das = [_da("DA-001", EffectAt="B-01")]
    srs = [_citing("SR-001", "SN-001"), _citing("SR-002", "SN-002")]
    before = copy.deepcopy((das, srs, REACH_NEEDS, REACH_STKS, REACH_EXTS))
    advisories = _reach(rules, das, srs)
    assert len(advisories) == 1 and _named(advisories, "DA-001", "SN-002"), advisories
    assert (das, srs, REACH_NEEDS, REACH_STKS, REACH_EXTS) == before


def test_a_fidelity_assumption_on_an_emulated_partys_crossing_passes(rules):
    """Judged against its surrogate's emulated parties instead of the needs':
    B-05 reaches none of SN-001's parties, but EXT-002 is the party its
    surrogate stands in for."""
    das = [_da("DA-001", EffectAt="B-05", RealizedBy="SUR-001")]
    surs = [_sur(Emulates="EXT-002")]
    assert _reach(rules, das, [_citing("SR-001", "SN-001")], surs=surs) == []


def test_a_fidelity_assumption_landing_elsewhere_is_reported(rules):
    """B-01 would reach SN-001's own party, and it does not count: a stand-in's
    fidelity is a claim about the party it answers for."""
    das = [_da("DA-001", EffectAt="B-01", RealizedBy="SUR-001")]
    surs = [_sur(Emulates="EXT-002")]
    advisories = _reach(rules, das, [_citing("SR-001", "SN-001")], surs=surs)
    # Exactly two: the served need no landing reaches, and the idle landing.
    unreached, idle = _named(advisories, "SN-001"), _named(advisories, "B-01")
    assert len(advisories) == 2, advisories
    assert len(unreached) == 1 and len(idle) == 1, advisories
    assert unreached != idle, advisories
    assert all(line.startswith("assumption DA-001 ") for line in advisories)


@pytest.mark.parametrize("named", ["SUR-009", "SUR-001;SUR-002"])
def test_a_fidelity_assumption_whose_surrogate_does_not_resolve_is_not_judged(
    rules, named
):
    """An undeclared surrogate, or two where a fidelity assumption states the
    match of exactly one, is `surrogate_findings`' reference failure. Reach is
    not judged on top of it: there is no emulated party to judge against. B-04
    is EXT-004's, which no surrogate here emulates, so any judgement at all
    would report it."""
    das = [_da("DA-001", EffectAt="B-04", RealizedBy=named)]
    surs = [_sur(Emulates="EXT-002"), _sur("SUR-002", Emulates="EXT-002")]
    srs = [_citing("SR-001", "SN-001")]
    assert _reach(rules, das, srs, surs=surs) == []
    failures, _advisories = rules.surrogate_findings(surs, das, REACH_EXTS, REACH_BIFS)
    assert _named(failures, "DA-001"), failures


def test_a_served_need_with_no_party_bearing_stakeholder_is_unreachable(rules):
    das = [_da("DA-001", EffectAt="B-01")]
    advisories = _reach(rules, das, [_citing("SR-001", "SN-003")])
    assert _named(advisories, "DA-001", "SN-003", "unreachable"), advisories


def test_a_drafted_stakeholders_party_is_not_read(rules):
    """With STK-01 in draft, SN-001 has no agreed party, so the landing that
    would reach it reaches nobody."""
    stks = [_stk("STK-01", "EXT-001", "Drafted")] + REACH_STKS[1:]
    assert rules.reaching_parties(REACH_NEEDS, stks, REACH_EXTS)["SN-001"] == set()
    das = [_da("DA-001", EffectAt="B-01")]
    advisories = _reach(rules, das, [_citing("SR-001", "SN-001")], stks)
    assert _named(advisories, "DA-001", "SN-001", "unreachable"), advisories


def test_an_uncited_assumption_is_not_judged(rules):
    das = [_da("DA-001", EffectAt="B-05"), _da("DA-002", EffectAt="B-05")]
    srs = [_citing("SR-001", "SN-001", das="", **{"Boundary-Refs": "B-01"})]
    assert _reach(rules, das, srs) == []


def test_the_reach_check_is_silent_with_no_crossing_declared(rules):
    das = [_da("DA-001", EffectAt="B-05")]
    srs = [_citing("SR-001", "SN-001;SN-003")]
    assert (
        rules.assumption_reach_advisories(
            das, srs, REACH_NEEDS, REACH_STKS, REACH_EXTS, [], []
        )
        == []
    )


# --- TC-214: need_frame_gap_advisories (SR-188, LLR-214) -----------------------


def _gap(rules, srs, das, stks=REACH_STKS, bifs=REACH_BIFS, needs=REACH_NEEDS):
    return rules.need_frame_gap_advisories(needs, stks, srs, bifs, das)


# SN-001's one requirement names the delivery crossing and cites an assumption
# landing there too: nothing that answers the need reaches an operation crossing.
GAP_SRS = [_citing("SR-001", "SN-001", **{"Boundary-Refs": "B-05"})]
GAP_DAS = [_da("DA-001", EffectAt="B-05")]


def test_a_need_met_in_operation_with_no_operation_crossing_is_reported(rules):
    advisories = _gap(rules, GAP_SRS, GAP_DAS)
    assert len(advisories) == 1 and _named(advisories, "SN-001", "STK-01"), advisories


def test_the_gap_is_reported_once_per_need(rules):
    stks = REACH_STKS + [_stk("STK-04", "EXT-001")]
    needs = [_need("SN-001", "STK-01", "STK-04")]
    advisories = _gap(rules, GAP_SRS, GAP_DAS, stks, needs=needs)
    assert len(advisories) == 1, advisories
    assert _named(advisories, "SN-001", "STK-01", "STK-04"), advisories


def test_a_requirement_on_an_operation_crossing_clears_the_gap(rules):
    srs = GAP_SRS + [
        _citing("SR-002", "SN-001", das="", **{"Boundary-Refs": "B-01"}),
    ]
    assert _gap(rules, srs, GAP_DAS) == []


def test_an_assumption_landing_on_an_operation_crossing_clears_the_gap(rules):
    assert _gap(rules, GAP_SRS, [_da("DA-001", EffectAt="B-01")]) == []


def test_a_need_reached_only_through_a_mediator_is_out_of_scope(rules):
    """SN-002's stakeholder is EXT-003, which has no operation crossing of its
    own; EXT-004 mediates for it and has one, and that does not bring the need
    into scope."""
    srs = [_citing("SR-001", "SN-002", **{"Boundary-Refs": "B-05"})]
    assert _gap(rules, srs, GAP_DAS, needs=[REACH_NEEDS[1]]) == []


def test_a_drafted_stakeholder_is_not_read(rules):
    stks = [_stk("STK-01", "EXT-001", "Drafted")] + REACH_STKS[1:]
    assert _gap(rules, GAP_SRS, GAP_DAS, stks) == []


def test_a_stakeholder_with_no_party_produces_nothing(rules):
    srs = [_citing("SR-001", "SN-003", **{"Boundary-Refs": "B-05"})]
    assert _gap(rules, srs, GAP_DAS, needs=[REACH_NEEDS[2]]) == []


def test_each_vacuous_input_produces_nothing(rules):
    """No frame, no stakeholder list, and a frame whose crossings declare no
    system value."""
    unplaced = [{k: v for k, v in b.items() if k != "System"} for b in REACH_BIFS]
    assert _gap(rules, GAP_SRS, GAP_DAS, bifs=[]) == []
    assert _gap(rules, GAP_SRS, GAP_DAS, stks=[]) == []
    assert _gap(rules, GAP_SRS, GAP_DAS, bifs=unplaced) == []


# --- the composition: which pipe each report rides -----------------------------
# The rules above return lists; which class a list joins is `trace.analyze`'s
# decision, and it is the one that makes a report warn or fail. LLR-214 names
# the checker as the composer of the gap advisory into the warn pipe, and the
# reach check rides beside it, so both are pinned THROUGH `analyze`: in-process,
# on an empty registry loaded from a blank directory with the frame, the
# stakeholder, the need, the requirement and the assumption substituted in.


@pytest.fixture(scope="module")
def trace():
    return load_script("trace")


def _analyzed(trace, tmp_path, **rows):
    """`trace.analyze` over an empty registry carrying only `rows`."""
    empty = trace.load_registries(tmp_path / "docs")
    return trace.analyze(dataclasses.replace(empty, **rows), trace.AnalysisFlags())


def _pipes_holding(findings, line):
    """The name of every list-valued `Findings` field holding `line`."""
    return sorted(
        f.name
        for f in dataclasses.fields(findings)
        if isinstance(getattr(findings, f.name), list)
        and line in getattr(findings, f.name)
    )


def test_both_reach_reports_ride_the_warn_pipe_alone(trace, tmp_path):
    """SN-001's one requirement names the delivery crossing and cites DA-001,
    which lands there too: the reach check names DA-001 against SN-001, and the
    gap advisory names SN-001. Each line is in the warn pipe and in no other
    list, so neither can join a failure set without this test reddening."""
    findings = _analyzed(
        trace,
        tmp_path,
        srs=GAP_SRS,
        exts=REACH_EXTS,
        bifs=REACH_BIFS,
        stks=REACH_STKS,
        sn_needs=[REACH_NEEDS[0]],
        das=GAP_DAS,
    )
    reach = _named(findings.interface_advisories, "assumption DA-001", "SN-001")
    gap = _named(findings.interface_advisories, "need SN-001", "met in operation")
    assert reach and gap, findings.interface_advisories
    for line in reach + gap:
        assert _pipes_holding(findings, line) == ["interface_advisories"], line


def test_a_bad_mediation_joins_the_frame_class(trace, tmp_path):
    """The frame class is what `--strict` fails on: a mediation naming an
    undeclared entity lands there, and not in the warn pipe."""
    exts = REACH_EXTS[:3] + [{"EXT-ID": "EXT-004", "Mediates": "EXT-009"}]
    findings = _analyzed(trace, tmp_path, exts=exts, bifs=REACH_BIFS)
    lines = _named(findings.frame_backlink_findings, "EXT-004", "EXT-009")
    assert len(lines) == 1, findings.frame_backlink_findings
    assert _pipes_holding(findings, lines[0]) == ["frame_backlink_findings"]
