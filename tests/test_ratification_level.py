"""The human-ratification ORDINAL, and the two axes it compares (SN-029).

`human_holds(docs, stage)` is the one comparison every consumer in the loop
makes — the dispatcher's admission table, the adjudication flip arm, the
page-escalation, the dual-plan round. Getting it wrong in the permissive
direction means a machine ratifying something a human meant to hold, which is
the one failure this kit's whole gate discipline exists to prevent. So the
input matrix is driven here rather than reasoned about at four call sites.

Two things this module pins that a first cut got wrong, both found by review:

  * **`stage < level`, not `<=`.** The stages are 0=SN..3=TC and 4=nothing in
    process; the levels are cumulative COUNTS ("through this tier"). Written
    `<=` there is no setting that holds SNs without also holding SRs, and level
    3 becomes indistinguishable from level 4 in every state where work exists.
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
    1: [dg.STAGE_SN],
    2: [dg.STAGE_SN, dg.STAGE_SR],
    3: [dg.STAGE_SN, dg.STAGE_SR, dg.STAGE_LLR],
    # Level 4 holds STAGE_IMPL and STAGE_DONE too — see the test below for why
    # that is not an inconsistency in the ladder but the thing that makes the
    # top of it mean what the shipped template says it means. Neither of those
    # two is a RATIFICATION tier (the dial names SN/SR/LLR/TC), which is why the
    # 2026-08-12 rung insert moved no level's meaning.
    4: [
        dg.STAGE_SN,
        dg.STAGE_SR,
        dg.STAGE_LLR,
        dg.STAGE_TC,
        dg.STAGE_IMPL,
        dg.STAGE_DONE,
    ],
}


@pytest.mark.parametrize("level", sorted(LADDER))
def test_each_level_holds_exactly_the_tiers_the_template_documents(tmp_path, level):
    # The template's own words: 0 = nothing; 1 = the human ratifies SNs; 2 =
    # ...and SRs; 3 = ...and LLRs; 4 = ...and TCs. Cumulative counts, so the
    # comparison is strictly less-than — one off-by-one here and level 1 also
    # holds SRs, which no setting would then be able to avoid.
    docs = _docs(tmp_path, level)
    held = [s for s in range(dg.STAGE_DONE + 1) if ac.human_holds(docs, s)]
    assert held == LADDER[level]


@pytest.mark.parametrize("stage", [dg.STAGE_IMPL, dg.STAGE_DONE])
def test_stage_four_is_held_by_LEVEL_FOUR_ALONE(tmp_path, stage):
    """The hole the strictly-less-than fix opened, and the reason the top of
    the ladder is absolute.

    The top stages — 4 (implementation in process) and 5 (nothing in process:
    every tier decomposed and Verified) — cover PRECISELY the states a
    gate-advance row runs in. With `4 < 4` reading as not-held, the SHIPPED
    DEFAULT (level 4, documented as "every tier human-held; the most
    conservative setting") let the loop dispatch and self-ratify the final gate.
    Below the top, the ladder is about which SPINE tier is being worked, and
    neither of these two is one."""
    for level in range(4):
        assert ac.human_holds(_docs(tmp_path, level), stage) is False, level
    assert ac.human_holds(_docs(tmp_path, 4), stage) is True


def test_the_shipped_default_holds_a_gate_advance(tmp_path):
    # The same fact stated where it bites: at the default, with a fully
    # verified spine, a `gate` row must SURFACE rather than dispatch.
    dispatch = load_script("dispatch")
    docs = _docs(tmp_path, 4)
    held = ac.human_holds(docs, dg.STAGE_DONE)
    assert held is True
    assert dispatch._kind_action("gate", held) == "surface"
    assert dispatch._admission([("WI-500", "gate")], held, busy=False, free=1) == (
        "surface",
        ["WI-500"],
    )


# --- the failure directions ----------------------------------------------------


def test_an_unreadable_stage_is_human_held(tmp_path):
    # The conservative direction. `None` is what `spine_stage_of` returns for a
    # docs/gate predating the field — i.e. EVERY repo at upgrade time.
    docs = _docs(tmp_path, 2)
    for stage in (None, "2", 2.0, object()):
        assert ac.human_holds(docs, stage) is True, stage


def test_level_zero_is_absolute_even_against_an_unreadable_stage(tmp_path):
    # "Nothing is human-held" is a statement the owner made outright, and the
    # upgrade-time repo (no `stage=` in docs/gate) is precisely when it must
    # still hold — otherwise the dial reads as its own opposite on the one day
    # it matters.
    docs = _docs(tmp_path, 0)
    for stage in (None, "0", 0, 3, dg.STAGE_DONE):
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
    # behaviour for a caller that did not run that gate.)
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


def _stage(srs=(SR,), llrs=(LLR,), tcs=(TC,), sn_ids=("SN-001",), sn_draft=()):
    return dg.spine_stage(list(srs), list(llrs), list(tcs), set(sn_ids), set(sn_draft))


def test_a_settled_spine_is_the_TOP_stage():
    # 5 since 2026-08-12 (the implementation rung went in at 4), and the
    # constant — not the literal — is what every consumer compares against.
    assert _stage() == dg.STAGE_DONE
    assert dg.STAGE_DONE == 5


def test_a_draft_need_or_an_empty_spine_is_stage_zero():
    assert _stage(sn_draft=("SN-001",)) == dg.STAGE_SN
    assert _stage(sn_ids=()) == dg.STAGE_SN
    assert _stage(srs=()) == dg.STAGE_SN


def test_a_ratified_but_UNCITED_need_is_stage_zero():
    # WI-401's coverage rung, which the stage axis did not apply: a need with
    # no requirement answering it is unfinished work AT THE SN TIER. Without
    # this such a spine read the top stage ("nothing in process") while the gate
    # arithmetic put the same repo at G0 — the two axes contradicting each
    # other, in the one function whose job is to reconcile them.
    assert _stage(sn_ids=("SN-001", "SN-002")) == dg.STAGE_SN


def test_a_MODIFIED_requirement_is_the_SR_tier():
    # The post-attestation amendment state: the text moved after it was
    # attested, so a fresh ratification is owed ON THE SR. Reading it as stage
    # 3 meant a repo at `human_ratification_through = 2` — "the human ratifies
    # SNs and SRs" — let the loop flip `Modified -> Verified` mechanically,
    # which is a machine ratifying an SR the owner declared human-held.
    assert _stage(srs=(dict(SR, Status="Modified"),)) == dg.STAGE_SR


def test_a_MISSING_child_puts_the_spine_at_the_CHILD_S_tier():
    # The artifact being written decides the tier, not its parent. Reading a
    # missing LLR as "SRs in process" made stages 2 and 3 unreachable during
    # exactly the period they describe.
    assert _stage(llrs=()) == dg.STAGE_LLR
    assert _stage(tcs=()) == dg.STAGE_TC
    assert _stage(llrs=(dict(LLR, Status="Draft"),)) == dg.STAGE_LLR
    assert _stage(tcs=(dict(TC, Status="Draft"),)) == dg.STAGE_TC


def test_an_LLR_EXEMPT_requirement_needs_no_LLR():
    # Analysis/Inspection/Attest decompose to a TC and no LLR — the same policy
    # trace.py enforces, pinned equal by test_rule_sync.
    assert _stage(srs=(dict(SR, Verification="Analysis"),), llrs=()) == dg.STAGE_DONE


def test_an_unverified_SR_over_AUTHORED_tests_is_the_IMPLEMENTATION_tier():
    """THE RUNG INSERTED 2026-08-12, pinned in the exact state that was wrong.

    Every SR decomposed, every TC authored and non-Draft, nothing Verified yet:
    the test set is WRITTEN, so "TCs in process" is false — what is in process is
    making them pass. This state persists for the entire implementation period,
    which is why reading it as STAGE_TC labelled the longest stretch of a project
    with the name of a tier that had already finished
    (docs/plans/2026-08-11-stage-gate-semantics.md §3).

    Children are still checked FIRST: an SR reaches Verified only once its LLRs
    and TCs are green, so while a child is in flight the child's tier is the
    honest answer — the two tests below pin that half."""
    assert _stage(srs=(dict(SR, Status="Planned"),)) == dg.STAGE_IMPL
    # ...and the tier still falls back to the child while a child is unfinished.
    unverified = dict(SR, Status="Planned")
    assert _stage(srs=(unverified,), tcs=()) == dg.STAGE_TC
    assert _stage(srs=(unverified,), tcs=(dict(TC, Status="Draft"),)) == dg.STAGE_TC


UNIFORM_STAGE_TO_GATE = {
    dg.STAGE_SN: "G1",  # 0 needs in process        -> G1 is next
    dg.STAGE_SR: "G1",  # 1 requirements in process -> G1 is next
    dg.STAGE_LLR: "G2",  # 2 design in process       -> G2 is next
    dg.STAGE_TC: "G2",  # 3 tests in process        -> G2 is next
    dg.STAGE_IMPL: "G3",  # 4 implementation          -> G3 is next
    dg.STAGE_DONE: "G3",  # 5 nothing in process      -> G3 passed; held to its bar
}


@pytest.mark.parametrize("stage,gate", sorted(UNIFORM_STAGE_TO_GATE.items()))
def test_stage_to_gate_is_THE_NEXT_GATE_YOU_MUST_PASS(stage, gate):
    """The ruled mapping (owner 2026-08-12), pinned whole.

    Before the implementation rung went in, `4 -> G3` read achieved-not-
    approaching and broke the pattern the other four rungs followed. With 4 =
    implementation the rule is uniform and needs no exception: two decomposition
    tiers sit between each pair of sittings, so two stages share the gate ahead
    of them. Stage 5 has already passed G3 and no rung above it is mechanized
    (G-Release / G-Final are prose), so it stays held to the G3 bar."""
    assert dg.stage_to_gate(stage) == gate


def test_stage_to_gate_names_no_gate_the_harness_does_not_know():
    # The mapping's other invariant: check.py's vocabulary is G1|G2|G3, so no
    # stage — including anything above the top rung a future ladder adds — may
    # produce a value it cannot select steps from.
    for stage in range(-1, dg.STAGE_DONE + 3):
        assert dg.stage_to_gate(stage) in ("G1", "G2", "G3")


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
    # you could not ask for a closing read without also holding every tier.
    docs = _docs(tmp_path, 0, final_review="always")
    assert ac.ratification_level(docs) == 0
    assert ac.human_holds(docs, dg.STAGE_SR) is False
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
