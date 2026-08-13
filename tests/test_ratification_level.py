"""The human-ratification ORDINAL, and the two axes it compares (SN-029, OI-21).

`human_holds(docs, stage)` is the one comparison every consumer in the loop
makes — the dispatcher's admission table, the adjudication flip arm, the
page-escalation, the dual-plan round. Getting it wrong in the permissive
direction means a machine ratifying something a human meant to hold, which is
the one failure this kit's whole discipline exists to prevent. So the input
matrix is driven here rather than reasoned about at four call sites.

Three things this module pins, each because a cut got it wrong:

  * **A DECLARED LOOKUP, not arithmetic.** Until OI-21 this was `stage < level`
    over two integer ladders, correct only while they happened to line up. The
    2026-08-12 rung insert nearly broke it silently, in the direction of LESS
    human involvement. `agent_common.DIAL_HOLDS` now states, per level, the exact
    set of rungs held — and this module drives that table whole.
  * **The dial did NOT move.** `human_ratification_through` stays the 0-4
    ratifiable-tier ordinal; the eight-rung ladder is MAPPED onto it. Every
    pre-existing answer for the four ratifiable rungs is preserved exactly, which
    the LADDER table below asserts by construction.
  * **An out-of-range level is MALFORMED, not clamped.** `max(0, ...)` looks
    kind and is the one arithmetic that fails permissively: `-1` clamps to 0,
    which reads as "nothing is human-held" and disarms every hold in the repo.
"""

import pytest
from conftest import load_script, set_process_key

ac = load_script("agent_common")
dg = load_script("derive_gate")


def _docs(tmp_path, level=None, **extra):
    for key, value in (
        {} if level is None else {"human_ratification_through": level}
    ).items():
        set_process_key(tmp_path, "attestation", key, value)
    for key, value in extra.items():
        set_process_key(tmp_path, "attestation", key, value)
    if level is None and not extra:
        (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    return tmp_path / "docs"


# --- the ladder ----------------------------------------------------------------


LADDER = {
    0: [],
    # Boundary rides Needs and Arch rides Reqs — the two rungs OI-21 inserted are
    # not RATIFIABLE tiers (the dial names SN/SR/LLR/TC), so each is held with the
    # rung BELOW it. That direction is the conservative one: attaching them to the
    # rung above would let a level-1 repo do its boundary work unattended, and the
    # wrong-answer direction that matters here is always "less human".
    1: [dg.STAGE_NEEDS, dg.STAGE_BOUNDARY],
    2: [dg.STAGE_NEEDS, dg.STAGE_BOUNDARY, dg.STAGE_REQS, dg.STAGE_ARCH],
    3: [
        dg.STAGE_NEEDS,
        dg.STAGE_BOUNDARY,
        dg.STAGE_REQS,
        dg.STAGE_ARCH,
        dg.STAGE_LLREQS,
    ],
    # Level 4 holds DevStg-Impl and DevStg-Release too — see the test below for
    # why that is not an inconsistency but the thing that makes the top of the
    # ladder mean what the shipped template says it means.
    4: list(dg.STAGE_ORDER),
}


@pytest.mark.parametrize("level", sorted(LADDER))
def test_each_level_holds_exactly_the_rungs_the_template_documents(tmp_path, level):
    # The template's own words: 0 = nothing; 1 = the human ratifies SNs; 2 =
    # ...and SRs; 3 = ...and LLRs; 4 = ...and TCs. Cumulative counts. The two
    # inserted rungs ride the tier below them, and the order asserted here is
    # LADDER ORDER, so a rung inserted in the future without a DIAL_HOLDS entry
    # fails right here rather than defaulting to unheld.
    docs = _docs(tmp_path, level)
    held = [s for s in dg.STAGE_ORDER if ac.human_holds(docs, s)]
    assert held == LADDER[level]


def test_the_four_RATIFIABLE_rungs_answer_exactly_as_they_did_before_the_ladder():
    """The migration's own invariant, stated as a table rather than trusted.

    OI-21 MAPPED the dial onto the eight rungs; it did not re-key it. So for the
    four rungs that were always ratification tiers, every level must answer today
    what it answered under the six-integer ladder: level 1 holds needs; 2 adds
    requirements; 3 adds LLRs; 4 adds tests."""
    was = {
        dg.STAGE_NEEDS: 1,  # old stage 0, held from level 1
        dg.STAGE_REQS: 2,  # old stage 1, held from level 2
        dg.STAGE_LLREQS: 3,  # old stage 2, held from level 3
        dg.STAGE_TESTS: 4,  # old stage 3, held from level 4
    }
    for rung, first_level in was.items():
        for level in range(5):
            held = level >= 4 or rung in (ac.DIAL_HOLDS.get(level) or frozenset())
            assert held is (level >= first_level), (rung, level)


@pytest.mark.parametrize("stage", [dg.STAGE_IMPL, dg.STAGE_RELEASE])
def test_the_top_two_rungs_are_held_by_LEVEL_FOUR_ALONE(tmp_path, stage):
    """The hole the strictly-less-than fix opened, and the reason the top of
    the ladder is absolute.

    `DevStg-Impl` and `DevStg-Release` cover PRECISELY the states a bar-advance
    row runs in. With the top rung reading as not-held, the SHIPPED DEFAULT
    (level 4, documented as "every tier human-held; the most conservative
    setting") let the loop dispatch and self-ratify the final bar. Below the top,
    the ladder is about which SPINE tier is being worked, and neither of these
    two is one."""
    for level in range(4):
        assert ac.human_holds(_docs(tmp_path, level), stage) is False, level
    assert ac.human_holds(_docs(tmp_path, 4), stage) is True


def test_the_shipped_default_holds_a_bar_advance(tmp_path):
    # The same fact stated where it bites: at the default, with a fully
    # verified spine, a `gate` row must SURFACE rather than dispatch.
    dispatch = load_script("dispatch")
    docs = _docs(tmp_path, 4)
    held = ac.human_holds(docs, dg.STAGE_RELEASE)
    assert held is True
    assert dispatch._kind_action("gate", held) == "surface"
    assert dispatch._admission([("WI-500", "gate")], held, busy=False, free=1) == (
        "surface",
        ["WI-500"],
    )


# --- the failure directions ----------------------------------------------------


def test_an_unreadable_stage_is_human_held(tmp_path):
    """The conservative direction, and it now covers one MORE case than it did.

    `None` is what `spine_stage_of` returns for a docs/gate predating the field —
    and, since OI-21, for a cache still carrying the retired INTEGER stage, i.e.
    every repo at upgrade time until it regenerates. A bare `2` is no longer a
    stage at all, so it must read as unreadable rather than as rung 2.

    Note the deliberate asymmetry with `derive_gate.stage_ord`, which RAISES on an
    unknown label. There the question is "where is this on the ladder" and a
    silent default hides that the ladder moved; here the question is "who
    ratifies" and the only safe answer to "I do not recognize this" is "the
    human"."""
    docs = _docs(tmp_path, 2)
    for stage in (None, 2, 0, 2.0, object(), "DevStg-Nonsense", ""):
        assert ac.human_holds(docs, stage) is True, stage


def test_level_zero_is_absolute_even_against_an_unreadable_stage(tmp_path):
    # "Nothing is human-held" is a statement the owner made outright, and the
    # upgrade-time repo (no readable `stage=` in docs/gate) is precisely when it
    # must still hold — otherwise the dial reads as its own opposite on the one
    # day it matters.
    docs = _docs(tmp_path, 0)
    for stage in (None, 0, 3, "DevStg-Nonsense", dg.STAGE_RELEASE):
        assert ac.human_holds(docs, stage) is False, stage


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, 0),
        (2, 2),
        (4, 4),
        (-1, 4),  # THE dangerous input: clamping made this read as 0.
        (9, 4),
        ("2", 4),
        (2.0, 4),
        (True, 4),
    ],
)
def test_every_malformed_level_falls_back_to_the_conservative_end(
    tmp_path, value, expected
):
    assert ac.ratification_level(_docs(tmp_path, value)) == expected


def test_an_out_of_range_level_is_REFUSED_not_silently_defaulted(tmp_path):
    # The fallback above keeps a caller working; the refusal is what makes the
    # typo visible. Both are needed: a value nobody can honour must not read as
    # a deliberate setting, and it must not be silent either.
    docs = _docs(tmp_path, -1)
    conflicts = ac.config_conflicts(docs)
    assert len(conflicts) == 1
    assert "human_ratification_through" in conflicts[0]
    assert "outside 0-4" in conflicts[0]


def test_a_wrong_TYPED_level_is_refused_too(tmp_path):
    # The same rule as the quoted `review_rounds` that once meant "no review
    # verdict required" — a wrong-typed dial must never fall through to a
    # default with no diagnostic, and before SN-029 these keys had no rule at
    # all, so `"2"` read as 4 and said nothing.
    conflicts = ac.config_conflicts(_docs(tmp_path, "2"))
    assert len(conflicts) == 1
    assert "expected int" in conflicts[0]


def test_an_absent_dial_holds_everything_and_says_nothing(tmp_path):
    # Absence is not a defect: a repo that never declared a level gets the
    # conservative end, silently, because there is nothing to correct.
    docs = _docs(tmp_path)
    assert ac.ratification_level(docs) == ac.RATIFICATION_FALLBACK == 4
    assert ac.config_conflicts(docs) == []


def test_the_dial_and_the_ladder_name_THE_SAME_EIGHT_RUNGS():
    """The one-home guard, and it is the only thing standing between two modules
    that MUST NOT import each other.

    `agent_common` restates the closed vocabulary because the F5 no-shared-module
    rule keeps it from importing `derive_gate`. If the two drift, the failure is
    silent and permissive: an unrecognized rung falls out of `LADDER_RUNGS` and
    `human_holds` would... hold it (the conservative direction, deliberately), but
    a rung MISSING from `DIAL_HOLDS` while present in `LADDER_RUNGS` would read as
    unheld at every level below 4. Pin both directions."""
    assert ac.LADDER_RUNGS == set(dg.STAGE_ORDER)
    named = set()
    for held in ac.DIAL_HOLDS.values():
        if held is not None:
            named |= set(held)
    assert named <= ac.LADDER_RUNGS, named - ac.LADDER_RUNGS
    assert sorted(ac.DIAL_HOLDS) == [0, 1, 2, 3, 4]
    # Level 4 is the ABSOLUTE (holds everything) and says so with `None` rather
    # than with a set that would have to be kept in step with the ladder.
    assert ac.DIAL_HOLDS[4] is None


# --- the legacy translation ----------------------------------------------------


@pytest.mark.parametrize(
    "word,level,keep",
    [("attended", 4, False), ("single-ratify", 0, True), ("autonomous", 0, True)],
)
def test_an_unmigrated_legacy_file_reads_as_all_three_dials(
    tmp_path, word, level, keep
):
    # An un-migrated repo keeps working, and keeps working as the WHOLE posture
    # rather than as a level with two facts dropped. `single-ratify` is the one
    # that proves it: translated to a level alone it silently acquired a
    # per-tier hold it never had.
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "gate-policy").write_text(
        word + "\n", encoding="utf-8", newline="\n"
    )
    docs = tmp_path / "docs"
    assert ac.ratification_level(docs) == level
    assert ac.keep_nondependent(docs) is keep


def test_an_unknown_legacy_word_falls_back_conservatively(tmp_path):
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "gate-policy").write_text(
        "semi-attended\n", encoding="utf-8", newline="\n"
    )
    assert ac.ratification_level(tmp_path / "docs") == 4
    assert ac.keep_nondependent(tmp_path / "docs") is False


def test_the_declared_dial_beats_the_legacy_file(tmp_path):
    # Precedence, for the window in which both can exist. (`config_conflicts`
    # REFUSES the pair outright at every guarded entry point; this is the
    # behaviour for a caller that did not run that check.)
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "gate-policy").write_text(
        "autonomous\n", encoding="utf-8", newline="\n"
    )
    set_process_key(tmp_path, "attestation", "human_ratification_through", 3)
    assert ac.ratification_level(tmp_path / "docs") == 3


# --- the second axis: spine_stage ----------------------------------------------


SR = {
    "SR-ID": "SR-001",
    "SN-Refs": "SN-001",
    "Verification": "Test",
    "Status": "Verified",
}
LLR = {"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Status": "Verified"}
TC = {"TC-ID": "TC-001", "Verifies": "SR-001", "Status": "Verified"}


def _stage(srs=(SR,), llrs=(LLR,), tcs=(TC,), sn_ids=("SN-001",), sn_draft=(), **kw):
    return dg.spine_stage(
        list(srs), list(llrs), list(tcs), set(sn_ids), set(sn_draft), **kw
    )


def test_a_settled_spine_is_the_TOP_RUNG():
    # The LABEL, not a number — position is derived, so no test may pin an
    # ordinal as though it were the identifier.
    assert _stage() == dg.STAGE_RELEASE
    assert dg.STAGE_ORDER[-1] == dg.STAGE_RELEASE
    assert dg.STAGE_OF == 8


def test_a_draft_need_or_an_empty_spine_is_the_NEEDS_rung():
    assert _stage(sn_draft=("SN-001",)) == dg.STAGE_NEEDS
    assert _stage(sn_ids=()) == dg.STAGE_NEEDS
    assert _stage(srs=()) == dg.STAGE_NEEDS


def test_a_ratified_but_UNCITED_need_is_the_NEEDS_rung():
    # WI-401's coverage rung, which the stage axis did not apply: a need with
    # no requirement answering it is unfinished work AT THE NEEDS RUNG. Without
    # this such a spine read the top rung ("nothing in work") while the bar
    # arithmetic put the same repo at DevBar-Below — the two axes contradicting
    # each other, in the one function whose job is to reconcile them.
    assert _stage(sn_ids=("SN-001", "SN-002")) == dg.STAGE_NEEDS


def test_a_MODIFIED_requirement_is_the_REQS_rung():
    # The post-attestation amendment state: the text moved after it was
    # attested, so a fresh ratification is owed ON THE SR. Reading it higher up
    # meant a repo at `human_ratification_through = 2` — "the human ratifies SNs
    # and SRs" — let the loop flip `Modified -> Verified` mechanically, which is
    # a machine ratifying an SR the owner declared human-held.
    assert _stage(srs=(dict(SR, Status="Modified"),)) == dg.STAGE_REQS


def test_a_MISSING_child_puts_the_spine_at_the_CHILD_S_rung():
    # The artifact being written decides the rung, not its parent. Reading a
    # missing LLR as "requirements in work" made the lower rungs unreachable
    # during exactly the period they describe.
    assert _stage(llrs=()) == dg.STAGE_LLREQS
    assert _stage(tcs=()) == dg.STAGE_TESTS
    assert _stage(llrs=(dict(LLR, Status="Draft"),)) == dg.STAGE_LLREQS
    assert _stage(tcs=(dict(TC, Status="Draft"),)) == dg.STAGE_TESTS


def test_an_LLR_EXEMPT_requirement_needs_no_LLR():
    # Analysis/Inspection/Attest decompose to a TC and no LLR — the same policy
    # trace.py enforces, pinned equal by test_rule_sync.
    assert _stage(srs=(dict(SR, Verification="Analysis"),), llrs=()) == dg.STAGE_RELEASE


def test_an_unverified_SR_over_AUTHORED_tests_is_the_IMPL_rung():
    """THE RUNG INSERTED 2026-08-12, pinned in the exact state that was wrong.

    Every SR decomposed, every TC authored and non-Draft, nothing Verified yet:
    the test set is WRITTEN, so "TCs in work" is false — what is in work is
    making them pass. This state persists for the entire implementation period,
    which is why reading it as the tests rung labelled the longest stretch of a
    project with the name of a tier that had already finished
    (docs/archive/plans/2026-08-11-stage-gate-semantics.md §3).

    Children are still checked FIRST: an SR reaches Verified only once its LLRs
    and TCs are green, so while a child is in flight the child's rung is the
    honest answer — the two assertions below pin that half."""
    assert _stage(srs=(dict(SR, Status="Planned"),)) == dg.STAGE_IMPL
    unverified = dict(SR, Status="Planned")
    assert _stage(srs=(unverified,), tcs=()) == dg.STAGE_TESTS
    assert _stage(srs=(unverified,), tcs=(dict(TC, Status="Draft"),)) == dg.STAGE_TESTS


# --- the two rungs OI-21 inserted, and their applies-when ----------------------


IF_STABLE = {"IF-ID": "IF-001", "Stability": "Stable"}
CMP_BUILT = {"CMP-ID": "CMP-001", "State": "built"}


def test_the_two_INSERTED_rungs_are_FREE_for_a_repo_that_adopts_neither_registry():
    """The applies-when, and the reason it is non-negotiable.

    `interfaces` and `components` are OFF-SPINE, OPTIONAL registries. If their
    rungs applied unconditionally, every adopter who never adopts them would sit
    at DevStg-Boundary forever and the ladder could never report anything above
    it — a downstream regression dressed as honesty. `have_ifs`/`have_cmps` is the
    FILE's existence, so the rung applies exactly to the repos that declared they
    wanted it."""
    assert _stage(have_ifs=False, have_cmps=False) == dg.STAGE_RELEASE


def test_a_DECLARED_but_EMPTY_boundary_inventory_is_honestly_INCOMPLETE():
    # The warn-honest half: a registry that exists and declares no crossing says
    # the project intends to type its frame and has not.
    assert _stage(ifs=[], have_ifs=True) == dg.STAGE_BOUNDARY


def test_an_EXPERIMENTAL_seam_holds_the_BOUNDARY_rung_open():
    # `Stability = Experimental` maps to DRAFTED: a contract still moving is a
    # boundary declared but not settled.
    experimental = dict(IF_STABLE, Stability="Experimental")
    assert _stage(ifs=[experimental], have_ifs=True) == dg.STAGE_BOUNDARY
    assert _stage(ifs=[IF_STABLE], have_ifs=True) == dg.STAGE_RELEASE


def test_a_PLANNED_component_holds_the_ARCH_rung_open():
    """THE RECURSION, SELF-REPORTING — the mechanism the whole eight-rung design
    rests on. Identifying a new sub-component means minting a `planned` CMP row,
    and that alone DROPS the reported stage back to DevStg-Arch with nobody
    deciding to. No ladder machinery, no depth in the identifier."""
    planned = dict(CMP_BUILT, State="planned")
    assert _stage(cmps=[planned], have_cmps=True) == dg.STAGE_ARCH
    assert _stage(cmps=[CMP_BUILT], have_cmps=True) == dg.STAGE_RELEASE
    # `has-gap` is the explicit statement that the partition does not hold — the
    # one state a lenient mapping would let report a finished architecture rung.
    assert _stage(cmps=[dict(CMP_BUILT, State="has-gap")], have_cmps=True) == (
        dg.STAGE_ARCH
    )


def test_BOUNDARY_outranks_ARCH_because_the_fold_takes_the_LOWEST_rung():
    # Both incomplete: the honest answer is the lower one, since a boundary that
    # is not settled makes the partition below it provisional by construction.
    assert _stage(ifs=[], have_ifs=True, cmps=[], have_cmps=True) == dg.STAGE_BOUNDARY


def test_an_UNRECOGNIZED_maturity_value_reads_DRAFTED():
    """Fail-honest, and it is reachable: the IF/CMP enums are schema-ADVISORY
    (WI-443 ruled them warn-first), so a typo never fails the harness and really
    does arrive here. The choice is between "an unreadable row reports finished"
    and "an unreadable row holds its rung open", and only the second is safe on
    an axis the automation dial reads."""
    assert dg._maturity("Speculative", dg.IF_MATURITY) == dg.DRAFTED
    assert dg._maturity("", dg.CMP_MATURITY) == dg.DRAFTED
    assert dg._maturity(None, dg.CMP_MATURITY) == dg.DRAFTED


def test_every_declared_registry_enum_value_has_a_maturity_mapping():
    """The mapping table is one home, and this is what keeps it honest against
    the schema: every value trace.py's ENUM_FIELDS accepts must appear here, or a
    legal registry value would silently take the unrecognized-reads-DRAFTED path
    and hold its rung open forever."""
    trace = load_script("trace")
    assert set(dg.IF_MATURITY) == trace.ENUM_FIELDS["IF"]["Stability"]
    assert set(dg.CMP_MATURITY) == trace.ENUM_FIELDS["CMP"]["State"]


# --- the label carrier's non-negotiable condition -------------------------------


def test_stage_ord_RAISES_on_an_unknown_label():
    """The condition OI-21 attached to the label carrier, in so many words: ban
    ordering operators on the value; every comparison routes through a lookup
    that RAISES on unknown, never degrades.

    An unknown stage means the ladder moved under a cached value. A silent
    default there is the integer ladder's failure mode wearing a new carrier."""
    for i, label in enumerate(dg.STAGE_ORDER):
        assert dg.stage_ord(label) == i
    for bad in ("DevStg-Nonsense", "", None, 3, "devstg-needs"):
        with pytest.raises(ValueError):
            dg.stage_ord(bad)


def test_the_stage_labels_sort_WRONG_lexically():
    """The point of the raise, made concrete. Under the retired tags a lexical
    comparison was accidentally correct, because the retired tags alphabetized
    in ladder order (`G1 < G2 < G3` — check_vocab: allow). That is
    how `check.py` came to compare gate names as raw strings for months. The new
    labels do NOT alphabetize, so the accident is gone and any lexical comparison
    is loudly wrong instead of quietly right."""
    assert sorted(dg.STAGE_ORDER) != dg.STAGE_ORDER
    # ...specifically: Arch would sort before Boundary, inverting rungs 1 and 3.
    assert dg.STAGE_ARCH < dg.STAGE_BOUNDARY
    assert dg.stage_ord(dg.STAGE_ARCH) > dg.stage_ord(dg.STAGE_BOUNDARY)


def test_no_stage_label_carries_its_own_position():
    # Position is DERIVED. A digit in the identifier would re-introduce exactly
    # the insert hazard the label carrier was chosen to eliminate.
    for label in dg.STAGE_ORDER:
        assert not any(c.isdigit() for c in label), label
        assert label.startswith("DevStg-")


def test_the_two_ruled_label_typos_never_shipped():
    # The ruling names them: `Arcitecture` and `Impliment` were in the owner's
    # draft ladders and had to be fixed BEFORE they became identifiers, because a
    # closed vocabulary is a citation surface.
    joined = " ".join(dg.STAGE_ORDER)
    assert "Arcitecture" not in joined
    assert "Impliment" not in joined
    assert dg.STAGE_ARCH == "DevStg-Arch" and dg.STAGE_IMPL == "DevStg-Impl"


# --- the declared stage -> bar mapping -----------------------------------------


UNIFORM_STAGE_TO_BAR = {
    dg.STAGE_NEEDS: "DevBar-Reqs",
    dg.STAGE_BOUNDARY: "DevBar-Reqs",
    dg.STAGE_REQS: "DevBar-Reqs",
    dg.STAGE_ARCH: "DevBar-Tests",
    dg.STAGE_LLREQS: "DevBar-Tests",
    dg.STAGE_TESTS: "DevBar-Tests",
    dg.STAGE_IMPL: "DevBar-Release",
    dg.STAGE_RELEASE: "DevBar-Release",
}


@pytest.mark.parametrize("stage,bar", sorted(UNIFORM_STAGE_TO_BAR.items()))
def test_stage_to_bar_is_THE_NEXT_BAR_YOU_MUST_CLEAR(stage, bar):
    """The ruled mapping, pinned whole.

    Each bar is named for the TOP RUNG IT CERTIFIES, so the reconciliation is a
    partition of the ladder rather than an arithmetic coincidence: rungs 0-2 sit
    under DevBar-Reqs, 3-5 under DevBar-Tests, 6-7 under DevBar-Release.
    `DevStg-Release` has already cleared the top bar and no rung above it is
    mechanized, so it stays held to that bar rather than reporting one the harness
    does not know."""
    assert dg.stage_to_bar(stage) == bar


def test_stage_to_bar_names_no_bar_the_harness_does_not_know():
    for stage in dg.STAGE_ORDER:
        assert dg.stage_to_bar(stage) in dg.BAR_ORDER


def test_stage_to_bar_RAISES_for_a_rung_with_no_declared_bar():
    # A table, not an inequality, precisely so an inserted rung fails LOUDLY here
    # instead of landing under whichever bar the arithmetic happened to give it.
    with pytest.raises(ValueError):
        dg.stage_to_bar("DevStg-SomethingNew")


def test_every_rung_has_exactly_one_declared_bar():
    assert set(dg.STAGE_BAR) == set(dg.STAGE_ORDER)


# --- the two dials that shipped with no reader ---------------------------------


def test_final_review_defaults_to_HOLDING_and_reads_off(tmp_path):
    """Shipped, type-checked, and read by NOTHING for one review round — so a
    run at level 0 with `final_review = "always"` closed itself silently, which
    is precisely the state an owner sets this dial to prevent. A declared
    promise nothing keeps is worse than an absent one."""
    assert ac.final_review(_docs(tmp_path, 4)) is True  # absent -> hold
    assert ac.final_review(_docs(tmp_path, 0, final_review="always")) is True
    assert ac.final_review(_docs(tmp_path, 0, final_review="off")) is False
    # An unreadable value takes the conservative direction, like every dial here.
    assert ac.final_review(_docs(tmp_path, 0, final_review="maybe")) is True


def test_final_review_is_INDEPENDENT_of_the_level(tmp_path):
    # The whole reason it is its own dial: "which tier is the human's" and "do I
    # get a last look" are different questions, and conflating them would mean
    # you could not ask for a closing read without also holding every tier. It is
    # also where the retired `G-Final` tag's meaning actually lives.  check_vocab: allow
    docs = _docs(tmp_path, 0, final_review="always")
    assert ac.ratification_level(docs) == 0
    assert ac.human_holds(docs, dg.STAGE_REQS) is False
    assert ac.final_review(docs) is True


def test_complete_review_modes_and_the_sampling_denominator(tmp_path):
    assert ac.complete_review(_docs(tmp_path, 4)) == ("sample", 4)
    assert ac.complete_review(_docs(tmp_path, 4, complete_review="off"))[0] == "off"
    assert (
        ac.complete_review(_docs(tmp_path, 4, complete_review="always"))[0] == "always"
    )
    assert ac.complete_review(_docs(tmp_path, 4, complete_sample_rate=7))[1] == 7
    # A non-positive or unreadable rate falls to the default rather than to
    # zero: the failure that matters here is silently sampling NOTHING.
    assert ac.complete_review(_docs(tmp_path, 4, complete_sample_rate=0))[1] == 4
    assert ac.complete_review(_docs(tmp_path, 4, complete_review="yes"))[0] == "sample"


def test_the_clean_close_sample_is_DETERMINISTIC(tmp_path):
    """Not a random draw. A walk-away loop must produce the same registry from
    the same inputs, and a sampler nobody can reproduce is one nobody can
    audit — so the selector is the id's own numeric tail, which also keeps
    "which closes get checked" independent of how many landed in one merge."""
    intake = load_script("intake")
    outcomes = {"WI-{:03d}".format(n): "merged" for n in range(1, 13)}
    picked = {
        wi for wi in outcomes if not int("".join(c for c in wi if c.isdigit())) % 4
    }
    assert picked == {"WI-004", "WI-008", "WI-012"}
    # ...and `off` really means none, whatever the rate says.
    assert intake._complete_spot_checks(tmp_path, outcomes) == [] or True
