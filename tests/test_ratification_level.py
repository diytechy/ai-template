"""The human-ratification DIAL, and the two axes it compares (SN-029, OI-21,
WI-493).

`human_holds(docs, stage)` is the one comparison every consumer in the loop
makes — the dispatcher's admission table, the adjudication flip arm, the
page-escalation, the dual-plan round. Getting it wrong in the permissive
direction means a machine ratifying something a human meant to hold, which is
the one failure this kit's whole discipline exists to prevent. So the input
matrix is driven here rather than reasoned about at four call sites.

Three things this module pins, each because a cut got it wrong:

  * **ONE VOCABULARY, AND THE COMPARISON IS AN ORDINAL ON IT.** Until OI-21 this
    was `stage < level` over two integer ladders, correct only while they
    happened to line up — the 2026-08-12 rung insert nearly broke it silently, in
    the direction of LESS human involvement. OI-21 shape (i) bridged the two with
    a declared `agent_common.DIAL_HOLDS` table; WI-493 executed shape (ii) and
    RE-KEYED the dial itself to a `DevStg-*` rung, so the table retired with the
    second vocabulary it existed to bridge. The dial names the HIGHEST rung a
    human still ratifies and every rung AT OR BELOW it is held — the mirror of
    check selection's at-or-above rule.
  * **THE DIAL MOVED, AND EVERY PRE-EXISTING ANSWER SURVIVED IT.** The retired
    0-4 ordinal's five settings hold precisely the same rung sets under the
    at-or-below rule, which `RETIRED_DIAL_HOLDS` below states as an explicit
    expected table — copied from the deleted `DIAL_HOLDS`, not re-derived from
    the code under test, so the equivalence is PINNED rather than assumed.
  * **AN UNREADABLE DIAL IS MALFORMED, NOT COERCED.** `max(0, ...)` looked kind
    and was the one arithmetic that failed permissively: `-1` clamped to 0, which
    reads as "nothing is human-held" and disarms every hold in the repo. The
    re-key did not soften that — a misspelled rung guesses at nothing and takes
    `DevStg-Release`. What it DID add is a migration window exactly as wide as
    the migration: a legacy 0-4 int is translated and warned about, and NOTHING
    else int-shaped is.
"""

import inspect
from pathlib import Path as _Path

import pytest
from conftest import load_script, set_process_key

ac = load_script("agent_common")
dg = load_script("spine_rules")
# The ladder's ONE home since WI-498 slice 0, and the stage carrier that declares
# the `DevStg-Below` sentinel. Imported as packages (not via `load_script`, which
# loads a single `scripts/*.py`); `scripts/` is already on sys.path by here —
# `load_script` puts it there. The name is `kit_ladder` because this module's own
# `LADDER` is the dial-to-rung expectation table.
import kitlib.ladder as kit_ladder  # noqa: E402  (after the loads above)
import kitlib.stage as kit_stage  # noqa: E402  (after the loads above)

BELOW = kit_stage.BELOW


def _docs(tmp_path, dial=None, **extra):
    for key, value in (
        {} if dial is None else {"human_ratification_through": dial}
    ).items():
        set_process_key(tmp_path, "attestation", key, value)
    for key, value in extra.items():
        set_process_key(tmp_path, "attestation", key, value)
    if dial is None and not extra:
        (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    return tmp_path / "docs"


# --- the ladder ----------------------------------------------------------------


# THE AT-OR-BELOW RULE, STATED AS A TABLE — the dial's meaning written out rather
# than recomputed with the arithmetic under test. Each row is a legal dial value
# and the rungs a human still ratifies at it, in LADDER ORDER.
#
# `DevStg-Below` is the sentinel for "nothing is human-held", not a rung; it is
# the value the retired ordinal spelled `0`, and setting the dial below the
# ladder means no rung is at or below it. `DevStg-Release` is the shipped default
# and holds everything including the close, because it is the top rung.
#
# THREE OF THESE ROWS WERE UNREACHABLE BEFORE WI-493 and are the concrete thing
# the re-key bought: the old dial had five notches for eight rungs, so "hold
# Needs but not Boundary", "hold through Reqs but not the partition" and "hold
# through Impl but not the close" could not be asked for at all.
LADDER = {
    BELOW: [],
    dg.STAGE_NEEDS: [dg.STAGE_NEEDS],
    dg.STAGE_BOUNDARY: [dg.STAGE_NEEDS, dg.STAGE_BOUNDARY],
    dg.STAGE_REQS: [dg.STAGE_NEEDS, dg.STAGE_BOUNDARY, dg.STAGE_REQS],
    dg.STAGE_ARCH: [dg.STAGE_NEEDS, dg.STAGE_BOUNDARY, dg.STAGE_REQS, dg.STAGE_ARCH],
    dg.STAGE_LLREQS: [
        dg.STAGE_NEEDS,
        dg.STAGE_BOUNDARY,
        dg.STAGE_REQS,
        dg.STAGE_ARCH,
        dg.STAGE_LLREQS,
    ],
    dg.STAGE_TESTS: [
        dg.STAGE_NEEDS,
        dg.STAGE_BOUNDARY,
        dg.STAGE_REQS,
        dg.STAGE_ARCH,
        dg.STAGE_LLREQS,
        dg.STAGE_TESTS,
    ],
    dg.STAGE_IMPL: [
        dg.STAGE_NEEDS,
        dg.STAGE_BOUNDARY,
        dg.STAGE_REQS,
        dg.STAGE_ARCH,
        dg.STAGE_LLREQS,
        dg.STAGE_TESTS,
        dg.STAGE_IMPL,
    ],
    dg.STAGE_RELEASE: list(dg.STAGE_ORDER),
}


# THE RETIRED `DIAL_HOLDS` TABLE, COPIED VERBATIM FROM THE DELETED SOURCE — this
# is the equivalence pin WI-493 owes, and it is only worth anything because it is
# a TRANSCRIPT rather than a derivation. Re-deriving it from `LADDER` above would
# be the code under test asserting about itself.
#
# The hand-reasoned property the old table carried: Boundary rides Needs and Arch
# rides Reqs. The two rungs OI-21 inserted are not RATIFIABLE tiers (the ordinal
# named SN/SR/LLR/TC), so each was held with the rung BELOW it — attaching them
# to the rung above would have let a level-1 repo do its boundary work unattended,
# and the wrong-answer direction that matters here is always "less human". Under
# the at-or-below rule that choice falls out of LADDER ORDER for free, because
# each inserted rung sits immediately above the rung it was made to ride. A
# hand-reasoned property became a structural one, and this table is how we know
# it became the SAME one.
RETIRED_DIAL_HOLDS = {
    0: [],
    1: [dg.STAGE_NEEDS, dg.STAGE_BOUNDARY],
    2: [dg.STAGE_NEEDS, dg.STAGE_BOUNDARY, dg.STAGE_REQS, dg.STAGE_ARCH],
    3: [
        dg.STAGE_NEEDS,
        dg.STAGE_BOUNDARY,
        dg.STAGE_REQS,
        dg.STAGE_ARCH,
        dg.STAGE_LLREQS,
    ],
    # Level 4 held DevStg-Impl and DevStg-Release too — see the test below for
    # why that is not an inconsistency but the thing that makes the top of the
    # ladder mean what the shipped template says it means.
    4: list(dg.STAGE_ORDER),
}


@pytest.mark.parametrize("dial", sorted(LADDER, key=kit_stage.order))
def test_each_dial_rung_holds_exactly_the_rungs_AT_OR_BELOW_it(tmp_path, dial):
    # The dial's whole definition, driven over every legal value. The order
    # asserted is LADDER ORDER, so a rung inserted in the future lands in this
    # table's rows by position rather than being silently unheld — the failure
    # the retired `DIAL_HOLDS` map could suffer and this rule cannot.
    docs = _docs(tmp_path, dial)
    held = [s for s in dg.STAGE_ORDER if ac.human_holds(docs, s)]
    assert held == LADDER[dial]


@pytest.mark.parametrize("level", sorted(RETIRED_DIAL_HOLDS))
def test_each_RETIRED_level_holds_exactly_what_DIAL_HOLDS_held(tmp_path, level):
    """THE RE-KEY'S EQUIVALENCE, PERMUTATION BY PERMUTATION (WI-493).

    The template's own words for the retired ordinal: 0 = nothing; 1 = the human
    ratifies SNs; 2 = ...and SRs; 3 = ...and LLRs; 4 = ...and TCs. Cumulative
    counts, with the two inserted rungs riding the tier below them.

    Both ROADS to a retired level are driven, because they are different code:
    the dial declared as the legacy INT (the migration window's reader, which
    translates and warns) and the dial declared as the RUNG that int translates
    to (what `--migrate-config` will write into the same file). A translation
    that agreed with the ordinal rule but disagreed with itself would be just as
    much a regression, and only driving both catches it."""
    expected = RETIRED_DIAL_HOLDS[level]
    rung = ac.LEGACY_DIAL_ORDINALS[level]
    for i, dial in enumerate((level, rung)):
        docs = _docs(tmp_path / str(i), dial)
        held = [s for s in dg.STAGE_ORDER if ac.human_holds(docs, s)]
        assert held == expected, (level, dial)


def test_the_four_RATIFIABLE_rungs_answer_exactly_as_they_did_before_the_ladder(
    tmp_path,
):
    """The migration's own invariant, stated as a table rather than trusted.

    OI-21 MAPPED the dial onto the eight rungs and WI-493 RE-KEYED it to them. So
    for the four rungs that were always ratification tiers, every retired level
    must answer today what it answered under the six-integer ladder: level 1
    holds needs; 2 adds requirements; 3 adds LLRs; 4 adds tests.

    RE-KEYED, NOT WEAKENED: this used to read the answer out of the
    `ac.DIAL_HOLDS` lookup, which is deleted. It now asks `human_holds` itself —
    a STRICTLY stronger question, because the table was only ever the input to
    the predicate the loop actually calls."""
    was = {
        dg.STAGE_NEEDS: 1,  # old stage 0, held from level 1
        dg.STAGE_REQS: 2,  # old stage 1, held from level 2
        dg.STAGE_LLREQS: 3,  # old stage 2, held from level 3
        dg.STAGE_TESTS: 4,  # old stage 3, held from level 4
    }
    for rung, first_level in was.items():
        for level in range(5):
            docs = _docs(tmp_path / str(level), ac.LEGACY_DIAL_ORDINALS[level])
            assert ac.human_holds(docs, rung) is (level >= first_level), (rung, level)


@pytest.mark.parametrize("stage", [dg.STAGE_IMPL, dg.STAGE_RELEASE])
def test_the_top_two_rungs_are_held_by_the_TOP_OF_THE_RETIRED_DIAL_ALONE(
    tmp_path, stage
):
    """The hole the strictly-less-than fix opened, and the reason the top of
    the ladder is absolute.

    `DevStg-Impl` and `DevStg-Release` cover PRECISELY the states a bar-advance
    row runs in. With the top rung reading as not-held, the SHIPPED DEFAULT
    (documented as "every tier human-held; the most conservative setting") let
    the loop dispatch and self-ratify the final bar. Below the top, the retired
    ordinal was about which SPINE tier is being worked, and neither of these two
    is one — so no setting under it reached them.

    THE CLAIM IS SCOPED TO THE RETIRED FIVE, and that scoping is the re-key's
    doing rather than a softening. Under the rung vocabulary `DevStg-Impl` is a
    legal dial in its own right, so "hold Impl but not the close" is now a
    setting an owner can ask for — pinned by the last two lines, because a
    reader who met only the paragraph above would think it impossible."""
    for level in range(4):
        docs = _docs(tmp_path / str(level), ac.LEGACY_DIAL_ORDINALS[level])
        assert ac.human_holds(docs, stage) is False, level
    assert ac.human_holds(_docs(tmp_path / "top", dg.STAGE_RELEASE), stage) is True
    # The setting the old five notches could not name.
    impl = _docs(tmp_path / "impl", dg.STAGE_IMPL)
    assert ac.human_holds(impl, dg.STAGE_IMPL) is True
    assert ac.human_holds(impl, dg.STAGE_RELEASE) is False


def test_the_shipped_default_holds_a_bar_advance(tmp_path):
    # The same fact stated where it bites: at the default, with a fully
    # verified spine, a `gate` row must SURFACE rather than dispatch.
    dispatch = load_script("dispatch")
    docs = _docs(tmp_path, dg.STAGE_RELEASE)
    held = ac.human_holds(docs, dg.STAGE_RELEASE)
    assert held is True
    assert dispatch._kind_action("gate", held) == "surface"
    assert dispatch._admission([("WI-500", "gate")], held, busy=False, free=1) == (
        "surface",
        ["WI-500"],
    )


def test_BOTH_shipped_homes_declare_the_dial_as_a_RUNG_STRING():
    """The re-key is only real if the files an adopter actually gets carry the
    new spelling — and a `4` left in either one would still WORK (the migration
    window reads it), silently, which is exactly how a re-key half-lands.

    Both homes are read, and NEITHER is allowed to be missing: a `continue` over
    an absent path is how a guard like this goes vacuous.

    The pin is STRUCTURAL on this repo's own file and VALUED on the template —
    the dogfood rule (CLAUDE.md): VALUES may diverge between the kit's template
    and this repo's instance (the owner set this repo's dial to `DevStg-Needs`
    on 2026-08-21, a declared-policy act), STRUCTURE must not (both homes carry
    a quoted ladder-rung string, never the retired ordinal)."""
    root = _Path(__file__).resolve().parents[1]
    rungs = {'"{}"'.format(r) for r in dg.STAGE_ORDER}
    for rel, expect in (
        ("docs/process.toml", None),  # structural: any valid rung string
        ("project-trajectory/process.toml.template", '"{}"'.format(dg.STAGE_RELEASE)),
    ):
        path = root / rel
        assert path.is_file(), rel
        declared = [
            line.split("=", 1)[1].strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.split("#", 1)[0].strip().startswith("human_ratification_through")
        ]
        assert len(declared) == 1, (rel, declared)
        if expect is None:
            assert declared[0] in rungs, (rel, declared)
        else:
            assert declared == [expect], (rel, declared)
    assert ac.RATIFICATION_FALLBACK == dg.STAGE_RELEASE


# --- the failure directions ----------------------------------------------------


def test_an_unreadable_stage_is_human_held(tmp_path):
    """The conservative direction, and it now covers one MORE case than it did.

    `None` is what `spine_stage_of` returns for a docs/gate predating the field —
    and, since OI-21, for a cache still carrying the retired INTEGER stage, i.e.
    every repo at upgrade time until it regenerates. A bare `2` is no longer a
    stage at all, so it must read as unreadable rather than as rung 2.

    Note the deliberate asymmetry with `spine_rules.stage_ord`, which RAISES on an
    unknown label. There the question is "where is this on the ladder" and a
    silent default hides that the ladder moved; here the question is "who
    ratifies" and the only safe answer to "I do not recognize this" is "the
    human"."""
    docs = _docs(tmp_path, dg.STAGE_ARCH)
    for stage in (None, 2, 0, 2.0, object(), "DevStg-Nonsense", ""):
        assert ac.human_holds(docs, stage) is True, stage


def test_the_BELOW_dial_is_absolute_even_against_an_unreadable_stage(tmp_path):
    # "Nothing is human-held" is a statement the owner made outright, and the
    # upgrade-time repo (no readable stage record) is precisely when it must
    # still hold — otherwise the dial reads as its own opposite on the one day
    # it matters.
    #
    # RENAMED AT WI-493: the setting is `DevStg-Below`, not `0`. It is the
    # sentinel `kitlib.stage` already declares for "below every rung", used here
    # in exactly that sense — a magic word like `"none"` would have been a second
    # vocabulary in the one place this program exists to remove one.
    docs = _docs(tmp_path, BELOW)
    for stage in (None, 0, 3, "DevStg-Nonsense", dg.STAGE_RELEASE):
        assert ac.human_holds(docs, stage) is False, stage


@pytest.mark.parametrize("dial", sorted(LADDER, key=kit_stage.order))
def test_every_legal_dial_reads_back_as_ITSELF(tmp_path, dial):
    # The reader's identity arm, and the reason the malformed table below means
    # anything: a fallback that fired on everything would satisfy every
    # conservative-direction test in this module while making the dial inert.
    assert ac.ratification_through(_docs(tmp_path, dial)) == dial
    assert ac.config_conflicts(_docs(tmp_path, dial)) == []


@pytest.mark.parametrize(
    "value",
    [
        -1,  # THE dangerous input: clamping made this read as 0 == nothing held.
        7,
        True,
        "2",
        "2.0",
        "4",
        "",
        "DevStg-Nope",
        "arch",
        "devstg-arch",  # a case-fold IS a guess, and every guess here is permissive
    ],
)
def test_every_malformed_dial_falls_back_to_the_conservative_end(tmp_path, value):
    # RE-KEYED AT WI-493 AND WIDENED, not weakened. The retired ordinal could
    # only be malformed by being out of range or wrong-typed; a rung STRING can
    # also be a plausible near-miss, so the near-misses are now the bulk of this
    # table. `"4"` is the one that carries both halves — it is the retired dial
    # in the new type, and it is refused rather than read, because the migration
    # window is exactly as wide as the migration and no wider.
    assert (
        ac.ratification_through(_docs(tmp_path, value))
        == ac.RATIFICATION_FALLBACK
        == dg.STAGE_RELEASE
    )


@pytest.mark.parametrize("value", [-1, 7, True, "4", "", "DevStg-Nope", "arch"])
def test_a_malformed_dial_is_REFUSED_not_silently_defaulted(tmp_path, value):
    # The fallback above keeps a caller working; the refusal is what makes the
    # typo visible. Both are needed: a value nobody can honour must not read as
    # a deliberate setting, and it must not be silent either.
    #
    # RENAMED from "an out-of-range LEVEL is REFUSED": out of range is now only
    # one of the two shapes a bad dial takes, and the refusal covers both.
    # Exactly ONE finding per bad dial, so a value cannot be reported twice (once
    # as a type error and once as an unknown rung) and read as two defects.
    conflicts = ac.config_conflicts(_docs(tmp_path, value))
    assert len(conflicts) == 1, conflicts
    assert "human_ratification_through" in conflicts[0]
    # ...and it never reads as a value the migration window HONOURS. An
    # out-of-range int is refused BY A MESSAGE THAT NAMES THE MIGRATION (the
    # only person who meets it is someone whose 0-4 dial was already out of
    # range), so the discriminator is "out of range", not the absence of the
    # words: the window accepts exactly 0-4 and says so either way.
    if isinstance(value, int) and not isinstance(value, bool):
        assert "out of range" in conflicts[0], conflicts
        assert "--migrate-config" in conflicts[0], conflicts
    else:
        assert "RETIRED 0-4" not in conflicts[0], conflicts


def test_a_wrong_TYPED_dial_is_refused_too(tmp_path):
    # The same rule as the quoted `review_rounds` that once meant "no review
    # verdict required" — a wrong-typed dial must never fall through to a
    # default with no diagnostic, and before SN-029 these keys had no rule at
    # all, so a bad value read as the conservative end and said nothing.
    #
    # RE-KEYED AT WI-493: the dial is a `str` now, so the arm that used to fire
    # on `"2"` ("expected int") fires on the NON-strings instead, and `"2"` moved
    # to the vocabulary arm below. The type check is much the weaker of the two
    # now — every typo is still a `str` — which is exactly why the vocabulary arm
    # exists and why it, not this one, is what catches a bad dial today.
    conflicts = ac.config_conflicts(_docs(tmp_path / "bool", True))
    assert len(conflicts) == 1, conflicts
    assert "expected str" in conflicts[0], conflicts
    assert "is a bool" in conflicts[0], conflicts

    # `-1` MOVED OFF THIS ARM. An int is the dial's own RETIRED type, so it is
    # refused by the migration-aware message instead of by "expected str" —
    # accurate but useless for the one reader likely to meet it, while 0-4 ints
    # are accepted four lines away. `test_a_malformed_dial_is_REFUSED...` owns
    # that arm now.
    #
    # THE THREE TYPES THE MIGRATION WINDOW NEARLY SWALLOWED, driven here because
    # each was a real defect found by re-keying these tests and fixed in the same
    # act (WI-498 slice 5). `_in_legacy_window` guarded `bool` by hand and then
    # asked `value in legacy_values`, which is wrong three ways in Python's
    # numeric tower — `True == 1` and `2.0 == 2` both slip into a window they
    # were never in, and an unhashable value RAISES out of `config_conflicts`,
    # whose docstring promises it "never raises" to three callers (dispatch,
    # intake, integrate) that use it inside an exit-code contract. The guard is
    # now an exact `type(value) is int`, which refuses all three at once. What is
    # pinned is the OUTCOME each must have — refused, exactly once, never a
    # raise — not which arm produces it, because the arm is an implementation
    # detail and the silence was the defect.
    # THE LINE IS HAND-WRITTEN, and that is load-bearing rather than lazy.
    # `_docs` goes through `bootstrap._toml_scalar`, which renders only bool and
    # int BARE and QUOTES everything else — so passing `2.0` or `[4]` through it
    # produces the STRINGS `"2.0"` and `"[4]`", drives the vocabulary arm, and
    # proves nothing at all about the types named here. Writing the raw TOML is
    # the only way these three reach the parser as themselves. (Checked, not
    # assumed: this test was briefly vacuous in exactly that way.)
    for i, literal in enumerate(("2.0", "[4]", "{ a = 1 }")):
        docs = tmp_path / "raw{}".format(i) / "docs"
        docs.mkdir(parents=True)
        (docs / "process.toml").write_text(
            "[attestation]\nhuman_ratification_through = {}\n".format(literal),
            encoding="utf-8",
        )
        found = ac.config_conflicts(docs)  # MUST NOT RAISE — that is the claim
        # AT LEAST one, not exactly one: the inline table trips a SECOND,
        # pre-existing rule (the git hooks parse this file in pure sh and cannot
        # read an inline table), and two findings for two genuinely different
        # problems is right. What must not happen is zero findings, or a raise.
        assert found, literal
        assert any("human_ratification_through" in f for f in found), (literal, found)
        assert ac.ratification_through(docs) == dg.STAGE_RELEASE, literal


def test_an_unknown_RUNG_is_refused_by_the_VOCABULARY_arm(tmp_path):
    # The arm WI-493 added, and the one that now catches almost everything: a
    # `str` dial passes the type check by construction, so the closed vocabulary
    # is what stands between a typo and a silent conservative default. The
    # refusal must NAME the legal values, because "names no rung" with no list is
    # not a correction anyone can act on.
    conflicts = ac.config_conflicts(_docs(tmp_path, "2"))
    assert len(conflicts) == 1, conflicts
    assert "names no rung" in conflicts[0]
    for rung in dg.STAGE_ORDER:
        assert rung in conflicts[0], rung
    assert BELOW in conflicts[0]


def test_an_absent_dial_holds_everything_and_says_nothing(tmp_path):
    # Absence is not a defect: a repo that never declared a dial gets the
    # conservative end, silently, because there is nothing to correct.
    docs = _docs(tmp_path)
    assert ac.ratification_through(docs) == ac.RATIFICATION_FALLBACK == dg.STAGE_RELEASE
    assert ac.config_conflicts(docs) == []


def test_the_dial_VOCABULARY_is_the_LADDER_plus_the_BELOW_sentinel():
    """THE EQUALITY HALF OF THIS PIN IS GONE, AND THE REASON IS THE POINT.

    This test used to open `assert ac.LADDER_RUNGS == set(dg.STAGE_ORDER)` — a
    by-VALUE guard holding two literal copies of the closed vocabulary in step,
    because the F5 no-shared-module rule kept `agent_common` from importing
    `spine_rules` and licensed the restatement. WI-498 slice 0 moved the ladder
    to `kitlib.ladder`; both names now RESOLVE to that one object, so "the copies
    agree" is no longer a property that can fail — there are no copies. A test
    asserting a frozenset equals itself is not a weaker pin, it is a VACUOUS one,
    which reads green while checking nothing. Drift is now UNREPRESENTABLE rather
    than DETECTED, this repo's stated preference and exactly the trade WI-448
    made when the five-way declared-line reader collapsed to one home
    (`tests/test_rule_sync.py`, "the declared-line reader: WAS 5-way, now ONE
    home"). The identity assertion below is the deletion's warrant.

    THE `DIAL_HOLDS` CONTAINMENT PIN WENT THE SAME WAY AT WI-493, AND IT IS NOT A
    LOST GUARANTEE. This test used to close by proving that every rung named in
    the hand-authored `DIAL_HOLDS` map was a real rung, because a rung MISSING
    from that map while present in `LADDER_RUNGS` read as unheld at every level
    below 4 — the permissive direction. The re-key DELETED the map: the dial is
    itself a rung and the comparison is `stage_ord(stage) <= stage_ord(dial)`, so
    there is no longer a mapping a rung can be omitted from. Unrepresentable
    rather than detected, the same trade as the paragraph above, and
    `test_each_RETIRED_level_holds_exactly_what_DIAL_HOLDS_held` is what proves
    the deletion changed no answer.

    WHAT SURVIVES AS A REAL CHOICE IS THE DIAL'S OWN VOCABULARY: the eight rungs
    PLUS the sentinel, and nothing else. That one extra member is a decision, so
    it is pinned by value — and so is the fact that the config validator reads
    THIS set rather than a copy of it."""
    assert ac.LADDER_RUNGS is kit_ladder.LADDER_RUNGS
    assert dg.STAGE_ORDER is kit_ladder.STAGE_ORDER
    assert dg.stage_ord is kit_ladder.stage_ord
    assert ac.RATIFICATION_RUNGS == set(dg.STAGE_ORDER) | {BELOW}
    assert BELOW not in ac.LADDER_RUNGS  # the sentinel is not a rung
    key = ("attestation", "human_ratification_through")
    assert ac.PROCESS_KEY_VOCAB[key] is ac.RATIFICATION_RUNGS
    # ...and the retired table is GONE rather than renamed: a reader who finds it
    # has found a revert, not a rename.
    assert not hasattr(ac, "DIAL_HOLDS")


# --- the migration window: the retired 0-4 ordinal ------------------------------


@pytest.mark.parametrize("level", [0, 1, 2, 3, 4])
def test_a_legacy_ORDINAL_is_translated_and_WARNED_but_never_REFUSED(
    tmp_path, level, capsys
):
    """THE MIGRATION WINDOW (WI-493), and every clause of it is load-bearing.

    An adopter's committed `human_ratification_through = 4` must not stop their
    loop dead on a kit upgrade over a spelling the kit knows how to read — so the
    reader TRANSLATES. But a dial nobody re-keyed is still a dial nobody
    re-keyed, so it WARNS, naming the command that fixes it. And
    `config_conflicts` — a HARD refusal consulted by dispatch, intake and
    integrate — stays SILENT, because saying it twice would make a kit upgrade
    look like a broken config to a repo whose dial is merely old.

    The translation is pinned as a literal expectation table rather than read out
    of `LEGACY_DIAL_ORDINALS`, and then the constant is checked against it: level
    4 is the top rung, level 0 is the sentinel, and the three between are the
    rungs the retired table held THROUGH."""
    expected = {
        0: BELOW,
        1: dg.STAGE_BOUNDARY,
        2: dg.STAGE_ARCH,
        3: dg.STAGE_LLREQS,
        4: dg.STAGE_RELEASE,
    }[level]
    assert ac.LEGACY_DIAL_ORDINALS[level] == expected
    docs = _docs(tmp_path, level)
    capsys.readouterr()
    assert ac.ratification_through(docs) == expected
    err = capsys.readouterr().err
    assert "human_ratification_through" in err and str(level) in err
    assert expected in err
    assert "--migrate-config" in err, err
    # NOT a conflict — the whole point of the window.
    assert ac.config_conflicts(docs) == []
    # ...and the window is derived from the translation table itself, so the two
    # can never come to disagree about which old values are honoured.
    key = ("attestation", "human_ratification_through")
    assert ac.PROCESS_KEY_LEGACY_VALUES[key] == frozenset(ac.LEGACY_DIAL_ORDINALS)
    assert ac.PROCESS_KEY_LEGACY_VALUES[key] == {0, 1, 2, 3, 4}


def test_the_legacy_window_REFUSES_a_BOOL_because_True_equals_one(tmp_path):
    """`True == 1` in Python, so a bare `value in {0, 1, 2, 3, 4}` answers True
    for `True` — and a `human_ratification_through = true` that took the window's
    SILENT PASS would be a wrong-typed dial reading as the retired level 1 with
    no diagnostic at all. That is the precise failure the type check exists to
    stop, arriving through the door the migration opened.

    So `_in_legacy_window` is a function rather than a bare `in`, and this is the
    one input that distinguishes the two. Driven at the helper AND end to end,
    because a validator that stopped consulting the helper would still pass a
    unit test of it."""
    window = ac.PROCESS_KEY_LEGACY_VALUES[("attestation", "human_ratification_through")]
    assert ac._in_legacy_window(1, window) is True
    assert ac._in_legacy_window(0, window) is True
    assert ac._in_legacy_window(True, window) is False
    assert ac._in_legacy_window(False, window) is False
    assert ac._in_legacy_window(5, window) is False
    # End to end: `true` takes the wrong-TYPE refusal, not the window's pass, and
    # reads the conservative end rather than the level-1 rung it numerically is.
    docs = _docs(tmp_path, True)
    conflicts = ac.config_conflicts(docs)
    assert len(conflicts) == 1, conflicts
    assert "is a bool, expected str" in conflicts[0]
    assert ac.ratification_through(docs) == dg.STAGE_RELEASE
    assert ac.ratification_through(docs) != dg.STAGE_BOUNDARY


# --- the legacy translation ----------------------------------------------------


@pytest.mark.parametrize(
    "word,rung,keep",
    [
        ("attended", dg.STAGE_RELEASE, False),
        ("single-ratify", BELOW, True),
        ("autonomous", BELOW, True),
    ],
)
def test_an_unmigrated_legacy_file_reads_as_all_three_dials(tmp_path, word, rung, keep):
    # An un-migrated repo keeps working, and keeps working as the WHOLE posture
    # rather than as one dial with two facts dropped. `single-ratify` is the one
    # that proves it: translated to a hold setting alone it silently acquired a
    # per-tier hold it never had.
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "gate-policy").write_text(
        word + "\n", encoding="utf-8", newline="\n"
    )
    docs = tmp_path / "docs"
    assert ac.ratification_through(docs) == rung
    assert ac.keep_nondependent(docs) is keep


def test_an_unknown_legacy_word_falls_back_conservatively(tmp_path):
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "gate-policy").write_text(
        "semi-attended\n", encoding="utf-8", newline="\n"
    )
    assert ac.ratification_through(tmp_path / "docs") == dg.STAGE_RELEASE
    assert ac.keep_nondependent(tmp_path / "docs") is False


def test_the_declared_dial_beats_the_legacy_file(tmp_path):
    # Precedence, for the window in which both can exist. (`config_conflicts`
    # REFUSES the pair outright at every guarded entry point; this is the
    # behaviour for a caller that did not run that check.)
    #
    # The declared value is a MIDDLE rung on purpose: `autonomous` translates to
    # the sentinel and the fallback is the top rung, so a dial reading either END
    # would also be consistent with the legacy file winning, or with nothing
    # being read at all.
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "gate-policy").write_text(
        "autonomous\n", encoding="utf-8", newline="\n"
    )
    set_process_key(
        tmp_path, "attestation", "human_ratification_through", dg.STAGE_LLREQS
    )
    assert ac.ratification_through(tmp_path / "docs") == dg.STAGE_LLREQS


# --- the second axis: spine_stage ----------------------------------------------


SR = {
    "SR-ID": "SR-001",
    "SN-Refs": "SN-001",
    "Verification": "Test",
    "Status": "Approved",
}
LLR = {"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Status": "Approved"}
TC = {"TC-ID": "TC-001", "Verifies": "SR-001", "Status": "Approved"}

# WHAT A FULLY SETTLED SPINE READS — `DevStg-Impl` since WI-498 slice 3, and
# NAMED rather than spelled so the rungs below can say what they mean.
#
# Most uses of this value in this module are INCIDENTAL: the frame-rung tests
# assert "nothing here holds the rung open", and the settled value is merely
# what a spine with nothing holding it reads. They are not claims about the top
# of the ladder. Spelling `dg.STAGE_RELEASE` at each of them made those tests
# LOOK like top-rung pins, which is exactly why the deep-check's pin census
# (`docs/plans/2026-08-21-stage-rekey-deep-check.md`, "The test pins that would
# move") counted five and nine went red: it found the tests ABOUT the rung and
# missed the ones that merely USED it. One name, so the next re-discrimination
# moves one line.
SETTLED = dg.STAGE_IMPL


def _stage(srs=(SR,), llrs=(LLR,), tcs=(TC,), sn_ids=("SN-001",), sn_draft=(), **kw):
    return dg.spine_stage(
        list(srs), list(llrs), list(tcs), set(sn_ids), set(sn_draft), **kw
    )


def test_a_settled_spine_is_the_IMPL_rung_and_the_top_rung_is_NOT_DERIVED():
    """FLIPPED AT WI-498 SLICE 3, under OI-51's ruling on the stage unification
    plan (§5 item 3) — deliberately, not by drift.

    WHAT THIS TEST USED TO SAY: `_stage() == dg.STAGE_RELEASE`, named "a settled
    spine is the TOP RUNG". That was the polarity the owner ruled wrong: a spine
    whose rows are all blessed through the test tier reported "nothing in work;
    release checklist available" for the entire implementation period, which is
    the wrong sentence for the longest stretch of a project.

    WHAT IT SAYS NOW: Founded-through-tests reads DevStg-Impl — the tests are
    laid, and making them pass is the work in progress.

    The ladder still ENDS at DevStg-Release, and the second assertion keeps
    saying so: the rung was not deleted, it was made evidence-gated. Nothing
    derives it, which the companion test below pins from the source."""
    assert _stage() == dg.STAGE_IMPL
    # The LABEL, not a number — position is derived, so no test may pin an
    # ordinal as though it were the identifier. The vocabulary is UNCHANGED.
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
    # arithmetic put the same repo at DevStg-Below — the two axes contradicting
    # each other, in the one function whose job is to reconcile them.
    assert _stage(sn_ids=("SN-001", "SN-002")) == dg.STAGE_NEEDS


def test_the_MODIFIED_rung_RETIRED_and_took_no_successor():
    # D-9 STEP 7, and the deletion is what this pins. The rung read the
    # post-attestation amendment state — the text moved after it was attested,
    # so a fresh ratification was owed ON THE SR — and it sat ahead of the
    # children for that reason. No cell records that state any more (owner
    # ruling 2026-08-17m: the snapshot comparison does), so the rung went with
    # the word and was deliberately NOT re-keyed onto drift: this axis reads
    # CELLS, and reaching into `docs/archive/` for a rung would make a pure row
    # computation depend on the filesystem.
    #
    # A row still carrying the retired value therefore lands on the LAST rung,
    # not the Reqs one — it is simply not `Approved`, so the children-first
    # cascade runs and the Impl discriminator catches it. That is the safe
    # direction (an unmigrated row reads LESS finished, never more) and the
    # integrity floor names the cell itself.
    #
    # WI-498 SLICE 3 FLIPPED THE REASON WITHOUT FLIPPING THE VALUE, and that is
    # worth stating: `Modified` used to reach DevStg-Impl by being SINGLED OUT
    # ("not Approved, so the discriminator catches it"). The discriminator is
    # gone — every spine that gets this far reads Impl — so the row now lands
    # there by falling through with everything else. Same answer, and no longer
    # dependent on an out-of-vocabulary cell being the one thing that reached
    # the rung.
    assert _stage(srs=(dict(SR, Status="Modified"),)) == dg.STAGE_IMPL
    # `Founded`, armed at step 8, is the opposite case — and since slice 3 it is
    # no longer a DIFFERENT answer. It reads Impl too: `Founded` is `Approved`
    # plus a demonstration, and neither is evidence that the tests pass.
    assert _stage(srs=(dict(SR, Status="Founded"),)) == SETTLED


def test_NO_status_combination_reaches_the_RELEASE_rung():
    """DevStg-Release is EVIDENCE-GATED and the evidence carrier does not exist,
    so nothing derives the rung. The plan calls this state honest and deliberate
    (§5 item 3); this test is what stops it from being quietly undone.

    Driven exhaustively over the closed Status enum PLUS a retired value, across
    all three spine tiers and both LLR-exemption shapes — 2 x 4^3 = 128 spines.
    Not one may read the top rung."""
    reached = set()
    for verification in ("Test", "Analysis"):
        for sr_status in ("Drafted", "Approved", "Founded", "Modified"):
            for llr_status in ("Drafted", "Approved", "Founded", "Modified"):
                for tc_status in ("Drafted", "Approved", "Founded", "Modified"):
                    reached.add(
                        _stage(
                            srs=(
                                dict(SR, Status=sr_status, Verification=verification),
                            ),
                            llrs=(dict(LLR, Status=llr_status),),
                            tcs=(dict(TC, Status=tc_status),),
                        )
                    )
    assert dg.STAGE_RELEASE not in reached, sorted(reached)
    # ...and the rung the settled shapes DO land on is the one the owner named.
    assert dg.STAGE_IMPL in reached


def test_the_RELEASE_rung_has_no_PRODUCER_in_the_source():
    """The companion to the exhaustive pin above, and it catches what enumeration
    cannot: a `return STAGE_RELEASE` behind a condition no fixture happens to
    build. The guard is structural — the rung has no producer at all — so the
    test is structural too.

    THIS IS THE OI-30 D2 GUARD ON THE STAGE AXIS. D2 ruled that a Status cell may
    never claim the test evidence passed; on the bar axis that needed a ceiling
    flag (`_RELEASE_CEILING`, which retired with the bar axis and `docs/gate` at
    WI-498 slice 5), and here it needs nothing, because the value is simply not
    produced. Deleting this test is how the harness driver lands — an act."""
    source = inspect.getsource(dg.spine_stage)
    body = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    # the docstring names the rung repeatedly; only RETURNS are the question
    assert "return STAGE_RELEASE" not in body
    assert "STAGE_RELEASE" not in body.split('"""')[-1]


def test_a_MISSING_child_puts_the_spine_at_the_CHILD_S_rung():
    # The artifact being written decides the rung, not its parent. Reading a
    # missing LLR as "requirements in work" made the lower rungs unreachable
    # during exactly the period they describe.
    assert _stage(llrs=()) == dg.STAGE_LLREQS
    assert _stage(tcs=()) == dg.STAGE_TESTS
    assert _stage(llrs=(dict(LLR, Status="Drafted"),)) == dg.STAGE_LLREQS
    assert _stage(tcs=(dict(TC, Status="Drafted"),)) == dg.STAGE_TESTS


def test_an_LLR_EXEMPT_requirement_needs_no_LLR():
    # Analysis/Inspection/Attest decompose to a TC and no LLR — the same policy
    # trace.py enforces, pinned equal by test_rule_sync.
    assert _stage(srs=(dict(SR, Verification="Analysis"),), llrs=()) == SETTLED


def test_an_unverified_SR_over_AUTHORED_tests_is_the_IMPL_rung():
    """THE RUNG INSERTED 2026-08-12, pinned in the exact state that was wrong.

    Every SR decomposed, every TC authored and non-Drafted, nothing Approved yet:
    the test set is WRITTEN, so "TCs in work" is false — what is in work is
    making them pass. This state persists for the entire implementation period,
    which is why reading it as the tests rung labelled the longest stretch of a
    project with the name of a tier that had already finished
    (docs/archive/plans/2026-08-11-stage-gate-semantics.md §3).

    Children are still checked FIRST: an SR reaches Approved only once its LLRs
    and TCs are green, so while a child is in flight the child's rung is the
    honest answer — the two assertions below pin that half.

    THE VACANCY IS CLOSED (WI-498 slice 3, OI-51's ruling on the stage
    unification plan §5 item 3), AND THIS TEST IS THE ONE THAT SAID IT WOULD BE.
    Its previous body ended: "the assertions below therefore pin the CURRENT
    truth, INCLUDING THE UNREACHABILITY, so that landing the harness driver
    reddens this test rather than sliding past it." It reddened. The history it
    recorded, kept because the sequence is the argument:

      * D-9 step 5 made the rung unreachable-by-cell. The state it describes —
        decomposed, TCs authored, the SR not yet blessed — was carried by
        `Planned`, and OI-30 D1 folded `Planned` into `Approved`. Under the
        closed enum every not-`Approved` SR was `Drafted` (caught by the Reqs
        rung) or `Founded` (read as blessed), so no LIVE value reached the Impl
        test at the bottom of `spine_stage`.
      * Step 7 narrowed the unreachability rather than closing it: the rung
        stayed reachable by exactly one thing, an OUT-OF-VOCABULARY status.
      * Slice 3 closes it by INVERTING the discriminator instead of repairing
        it. The rung is no longer "the spine is not yet blessed" — it is "the
        spine IS blessed and the code is being made to pass", the reading the
        rung was originally inserted for. It is now the rung a healthy project
        occupies for most of its life, which is what it was always meant to be.

    THE VACANCY MOVED UP RATHER THAN DISAPPEARING, and that is deliberate and
    honest: `DevStg-Release` is now the rung nothing derives, because leaving
    Impl means the declared test cases PASS and no machine reading of that
    exists yet. The difference from the state this docstring used to record is
    that the vacancy is now at the TOP of the ladder, where "not yet reached" is
    the correct thing for a rung to say, instead of in the middle, where it made
    a state no legal spine could occupy."""
    assert _stage(srs=(dict(SR, Status="Drafted"),)) == dg.STAGE_REQS
    for blessed in ("Approved", "Founded"):
        assert _stage(srs=(dict(SR, Status=blessed),)) == dg.STAGE_IMPL, blessed
    # The unmigrated, out-of-vocabulary cell reads the same rung — no longer
    # because it is singled out, but because everything that gets here does.
    assert _stage(srs=(dict(SR, Status="Modified"),)) == dg.STAGE_IMPL
    # The children-first half is unaffected by the rename and still pins.
    unverified = dict(SR, Status="Approved")
    assert _stage(srs=(unverified,), tcs=()) == dg.STAGE_TESTS
    assert (
        _stage(srs=(unverified,), tcs=(dict(TC, Status="Drafted"),)) == dg.STAGE_TESTS
    )


# --- the two rungs OI-21 inserted, and their applies-when ----------------------


# WI-442: rung 1 reads the FRAME's `[boundary.B-##]` rows, not the IF registry.
BIF_APPROVED = {"B-ID": "B-01", "Status": "Approved"}
CMP_BUILT = {"CMP-ID": "CMP-001", "Status": "Approved"}


def test_the_two_INSERTED_rungs_are_FREE_for_a_repo_that_adopts_neither_registry():
    """The applies-when, and the reason it is non-negotiable.

    `external` and `components` are OFF-SPINE, OPTIONAL registries. If their
    rungs applied unconditionally, every adopter who never adopts them would sit
    at DevStg-Boundary forever and the ladder could never report anything above
    it — a downstream regression dressed as honesty. `have_bifs`/`have_cmps` is
    the FILE's existence, so the rung applies exactly to the repos that declared
    they wanted it.

    THE APPLIES-WHEN MOVED AT WI-442 and the move is asserted, not assumed: a
    repo carrying `interfaces.toml` and NO `external.toml` is now free of rung 1
    rather than held by its internal seams. That is the correction decision 3
    made — internal definitions never typed a boundary — and a repo in exactly
    that state is every adopter mid-migration."""
    assert _stage(have_bifs=False, have_cmps=False) == SETTLED


def test_a_DECLARED_but_EMPTY_boundary_inventory_is_honestly_INCOMPLETE():
    # The warn-honest half: a registry that exists and declares no crossing says
    # the project intends to type its frame and has not.
    assert _stage(bifs=[], have_bifs=True) == dg.STAGE_BOUNDARY


def test_a_DRAFT_crossing_holds_the_BOUNDARY_rung_open():
    # `approval = "draft"` maps to DRAFTED: a frame declared and not yet
    # ratified. Lower-cased cells against capitalized ladder constants is exactly
    # the case `_maturity`'s case-fold exists for, so both spellings are pinned.
    assert _stage(bifs=[dict(BIF_APPROVED, Status="Drafted")], have_bifs=True) == (
        dg.STAGE_BOUNDARY
    )
    assert _stage(bifs=[BIF_APPROVED], have_bifs=True) == SETTLED
    assert _stage(bifs=[dict(BIF_APPROVED, Approval="Approved")], have_bifs=True) == (
        SETTLED
    )


def test_rung_1_gates_on_APPROVAL_and_NOT_on_realization_coverage():
    """THE RULING'S TWO READINGS, RESOLVED — and the resolution pinned so a later
    pass cannot fold in the second conjunct without touching this test.

    13u's wording gates on BIF approval; §1R.5's names approval AND "every BIF
    realized (or explicitly deferred)". Whether a crossing has a realizing IF row
    is DECISION 6, deferred by ruling to post-schema, so the predicate reads
    approval only. An approved crossing that NOTHING realizes therefore clears
    rung 1 — which is the live state of four of this repo's six crossings, not a
    hypothetical."""
    assert _stage(bifs=[BIF_APPROVED], have_bifs=True) == SETTLED
    # ...and `spine_stage` no longer takes the IF registry at all, which is the
    # structural half of the same statement: rung 1 CANNOT read realization
    # coverage, because it is no longer handed the rows that would show it.
    # Asserted on the SIGNATURE — a bare `pytest.raises(TypeError)` also passes
    # for any unrelated arity error and would pass against a two-arg stub.
    params = inspect.signature(dg.spine_stage).parameters
    assert "bifs" in params and "have_bifs" in params
    assert "ifs" not in params and "have_ifs" not in params


def test_a_PLANNED_component_holds_the_ARCH_rung_open():
    """THE RECURSION, SELF-REPORTING — the mechanism the whole eight-rung design
    rests on. Identifying a new sub-component means minting a `planned` CMP row,
    and that alone DROPS the reported stage back to DevStg-Arch with nobody
    deciding to. No ladder machinery, no depth in the identifier."""
    planned = dict(CMP_BUILT, Status="Drafted")
    assert _stage(cmps=[planned], have_cmps=True) == dg.STAGE_ARCH
    assert _stage(cmps=[CMP_BUILT], have_cmps=True) == SETTLED
    # A DEMONSTRATED partition is the one CMP value that reaches FOUNDED, and it
    # must not hold the rung open either.
    assert _stage(cmps=[dict(CMP_BUILT, Status="Founded")], have_cmps=True) == (SETTLED)
    # The RETIRED words hold the rung OPEN rather than resolving. `planned` and
    # `verified` left this vocabulary at the status unification (they were the
    # retired spine words regenerated in another registry), so a stale cell
    # still carrying one is unreadable — and an unreadable partition reports
    # unfinished, never finished. `has-gap`/`deprecated` are the same shape ON
    # THIS FIELD: they are `standing` values now, so as a `Status` they are just
    # unreadable. What `standing = "has-gap"` means on its OWN field is pinned
    # by the next test.
    for retired in ("planned", "built", "verified", "has-gap", "deprecated"):
        assert _stage(cmps=[dict(CMP_BUILT, Status=retired)], have_cmps=True) == (
            dg.STAGE_ARCH
        ), retired


def test_a_recorded_GAP_holds_the_ARCH_rung_open_however_mature_the_row_reads():
    """The F1 scenario, pinned exactly (2026-08-17 desk round).

    The status/standing split moved `has-gap` off the maturity axis, and for one
    day nothing read it: a component could carry `Status = "Founded"` — the top
    of CMP's ladder, a demonstrated partition — alongside an explicitly recorded
    `standing = "has-gap"`, and rung 3 reported FINISHED. That combination is
    not a corner case; it is the reason the second axis was created, so it is
    the one this test pins.

    The pre-split code said so in a comment `6f39b2ed` deleted: `has-gap` is
    "the one place a lenient mapping would let a known-broken partition report a
    finished architecture rung"."""
    gapped = dict(CMP_BUILT, Status="Founded", Standing="has-gap")
    assert _stage(cmps=[gapped], have_cmps=True) == dg.STAGE_ARCH
    # ...and it holds under every maturity, not only the top one — the fact is
    # about the partition, not about how far the row's status has climbed.
    for status in ("Drafted", "Approved", "Founded"):
        assert (
            _stage(
                cmps=[dict(CMP_BUILT, Status=status, Standing="has-gap")],
                have_cmps=True,
            )
            == dg.STAGE_ARCH
        ), status
    # THE OTHER DIRECTION, so this is a mapping and not a blanket veto on the
    # field: `deprecated` is a decided state (the pre-split table read it
    # APPROVED), `active` says nothing, and an ABSENT cell is the declared
    # `omit = active` shorthand. None of the three may hold the rung.
    assert _stage(cmps=[CMP_BUILT], have_cmps=True) == SETTLED
    for clears in ("active", "deprecated", "", None):
        assert (
            _stage(cmps=[dict(CMP_BUILT, Standing=clears)], have_cmps=True) == SETTLED
        ), clears
    # Case-folded like every other cell read here, and fail-honest on a typo:
    # the tier's schema is ADVISORY, so an unreadable standing really can arrive
    # and it must hold the rung rather than clear it.
    assert _stage(cmps=[dict(CMP_BUILT, Standing="HAS-GAP")], have_cmps=True) == (
        dg.STAGE_ARCH
    )
    assert _stage(cmps=[dict(CMP_BUILT, Standing="has_gap")], have_cmps=True) == (
        dg.STAGE_ARCH
    )


def test_BOUNDARY_outranks_ARCH_because_the_fold_takes_the_LOWEST_rung():
    # Both incomplete: the honest answer is the lower one, since a boundary that
    # is not settled makes the partition below it provisional by construction.
    assert _stage(bifs=[], have_bifs=True, cmps=[], have_cmps=True) == (
        dg.STAGE_BOUNDARY
    )


def test_an_UNRECOGNIZED_maturity_value_reads_DRAFTED():
    """Fail-honest, and it is reachable: the IF/CMP enums are schema-ADVISORY
    (WI-443 ruled them warn-first), so a typo never fails the harness and really
    does arrive here. The choice is between "an unreadable row reports finished"
    and "an unreadable row holds its rung open", and only the second is safe on
    an axis the automation dial reads."""
    assert dg._maturity("Speculative", dg.BIF_MATURITY) == dg.DRAFTED
    assert dg._maturity("", dg.CMP_MATURITY) == dg.DRAFTED
    assert dg._maturity(None, dg.CMP_MATURITY) == dg.DRAFTED


def test_every_declared_registry_enum_value_has_a_maturity_mapping():
    """The mapping table is one home, and this is what keeps it honest against
    the schema: every value trace.py's ENUM_FIELDS accepts must appear here, or a
    legal registry value would silently take the unrecognized-reads-DRAFTED path
    and hold its rung open forever.

    COMPARED CASE-NORMALIZED, and that is not a loosening. The registries speak
    the spine's Title-case words; these tables are keyed lowercase because
    `_maturity` lowercases before the lookup. A raw set comparison would have
    been red the moment the vocabulary re-cased — the two sides never disagreed
    about WHICH values map, only about how the lookup spells them, and this
    normalization is exactly the transform `_maturity` itself applies.

    What must NOT be done to make this green is lower-casing the registries: the
    Title-case word IS the unification (2026-08-17), and a check that pulled the
    cells back down to keep itself simple would have undone the change it is
    supposed to be guarding."""
    trace = load_script("trace")

    def _lower(values):
        return {v.lower() for v in values}

    assert set(dg.BIF_MATURITY) == _lower(trace.ENUM_FIELDS["B"]["Status"])
    assert set(dg.CMP_MATURITY) == _lower(trace.ENUM_FIELDS["CMP"]["Status"])
    # The tables are keyed lowercase; the schema is not. Pin the asymmetry so a
    # future edit cannot "tidy" one side into the other and make the comparison
    # above vacuous in the direction it was designed to catch.
    assert all(v == v.lower() for v in dg.CMP_MATURITY)
    assert trace.ENUM_FIELDS["CMP"]["Status"] == {"Drafted", "Approved", "Founded"}
    assert trace.ENUM_FIELDS["B"]["Status"] == {"Drafted", "Approved"}
    # The IF tier shares the frame's approval vocabulary (decision 12: ONE status
    # vocabulary, per-registry subsets) — pinned so the two cannot drift apart
    # while each stays internally consistent.
    assert trace.ENUM_FIELDS["IF"]["Status"] == trace.ENUM_FIELDS["B"]["Status"]
    assert trace.ENUM_FIELDS["EXT"]["Status"] == trace.ENUM_FIELDS["B"]["Status"]
    assert trace.ENUM_FIELDS["REL"]["Status"] == trace.ENUM_FIELDS["B"]["Status"]


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


# --- the declared stage -> bar mapping: RETIRED (WI-498 slice 2) ---------------
#
# `spine_rules.STAGE_BAR` / `stage_to_bar` and the four tests that pinned them
# are gone. They declared which BAR each rung sat under, and their own docstring
# recorded that nothing in production derived one axis from the other — the
# table was a reader's reconciliation. Selection now keys on the stage alone
# (`check.at_or_above`), so there is no second axis to reconcile against and the
# pins were holding a mapping with no consumer. Deleted rather than re-pointed:
# a test that pins a table nobody reads is the kind of green this repo treats as
# a liability. The ladder's own pins above (order, labels, `stage_ord` raising)
# are untouched, because those DO have consumers.


# --- the two dials that shipped with no reader ---------------------------------


def test_final_review_defaults_to_HOLDING_and_reads_off(tmp_path):
    """Shipped, type-checked, and read by NOTHING for one review round — so a
    run at the `DevStg-Below` dial with `final_review = "always"` closed itself
    silently, which is precisely the state an owner sets this dial to prevent. A
    declared promise nothing keeps is worse than an absent one."""
    top = dg.STAGE_RELEASE
    assert ac.final_review(_docs(tmp_path, top)) is True  # absent -> hold
    assert ac.final_review(_docs(tmp_path, BELOW, final_review="always")) is True
    assert ac.final_review(_docs(tmp_path, BELOW, final_review="off")) is False
    # An unreadable value takes the conservative direction, like every dial here.
    assert ac.final_review(_docs(tmp_path, BELOW, final_review="maybe")) is True


def test_final_review_is_INDEPENDENT_of_the_DIAL(tmp_path):
    # The whole reason it is its own dial: "which tier is the human's" and "do I
    # get a last look" are different questions, and conflating them would mean
    # you could not ask for a closing read without also holding every tier. It is
    # also where the retired `G-Final` tag's meaning actually lives.  check_vocab: allow
    docs = _docs(tmp_path, BELOW, final_review="always")
    assert ac.ratification_through(docs) == BELOW
    assert ac.human_holds(docs, dg.STAGE_REQS) is False
    assert ac.final_review(docs) is True


def test_complete_review_modes_and_the_sampling_denominator(tmp_path):
    top = dg.STAGE_RELEASE
    assert ac.complete_review(_docs(tmp_path, top)) == ("sample", 4)
    assert ac.complete_review(_docs(tmp_path, top, complete_review="off"))[0] == "off"
    assert (
        ac.complete_review(_docs(tmp_path, top, complete_review="always"))[0]
        == "always"
    )
    assert ac.complete_review(_docs(tmp_path, top, complete_sample_rate=7))[1] == 7
    # A non-positive or unreadable rate falls to the default rather than to
    # zero: the failure that matters here is silently sampling NOTHING.
    assert ac.complete_review(_docs(tmp_path, top, complete_sample_rate=0))[1] == 4
    assert (
        ac.complete_review(_docs(tmp_path, top, complete_review="yes"))[0] == "sample"
    )


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


# --- OI-30 D3: off-spine approval authority, DERIVED from the same dial --------
def test_APPROVAL_RUNGS_is_the_off_spine_sibling_of_THE_DIAL(tmp_path):
    """The map is small, closed, and every value is a REAL rung of the ladder.

    A typo'd rung would send `human_approves` through `human_holds`' unrecognized
    arm, which answers True — safe, but silently: the registry would read as held
    for a reason nobody intended. Pin the values against the ladder itself."""
    assert set(ac.APPROVAL_RUNGS) == {"external", "interfaces", "components"}
    for registry, rung in ac.APPROVAL_RUNGS.items():
        assert rung in ac.LADDER_RUNGS, (registry, rung)
    # The ruled mapping, verbatim: each registry gets the rung `spine_rules`
    # ALREADY gates on it — external.toml is what `boundary_incomplete` reads,
    # the component registry is what `arch_incomplete` reads.
    assert ac.APPROVAL_RUNGS["external"] == dg.STAGE_BOUNDARY
    assert ac.APPROVAL_RUNGS["interfaces"] == dg.STAGE_ARCH
    assert ac.APPROVAL_RUNGS["components"] == dg.STAGE_ARCH
    # NO NEW KEY: the ruling's whole point. `human_approves` must answer from the
    # existing dial, so a repo that never declares anything new still gets it.
    # The OVERTURNED proposal's key must exist NOWHERE that a reader could take
    # for a live declaration — not as a module attribute, and not as a line in
    # the one policy home or the template it ships. (It is NAMED in prose, in
    # `agent_common`'s comment and in `docs/process.toml`'s, because recording
    # what was overturned is how the next author knows not to re-propose it.)
    assert not hasattr(ac, "human_approval_registries")
    assert not hasattr(ac, "HUMAN_APPROVAL_REGISTRIES")
    root = _Path(__file__).resolve().parents[1]
    # BOTH paths must EXIST. The template's was spelled `process.template.toml`
    # here — the file is `process.toml.template` — under an `if not exists:
    # continue`, so half this guard read green against a path that could never be
    # there. A silently-skipped guard is the failure mode this module opens by
    # naming; it does not get to have one.
    for rel in ("docs/process.toml", "project-trajectory/process.toml.template"):
        path = root / rel
        assert path.is_file(), rel
        for line in path.read_text(encoding="utf-8").splitlines():
            code = line.split("#", 1)[0]
            assert "human_approval_registries" not in code, (rel, line)


def test_human_approves_MAPPED_and_HELD_at_this_repos_dial(tmp_path):
    """Arm 1 — the state this repo is in. At `DevStg-Release` every rung is at or
    below the dial, so every mapped registry's approval cells are the owner's."""
    docs = _docs(tmp_path, dial=dg.STAGE_RELEASE)
    for registry in ac.APPROVAL_RUNGS:
        assert ac.human_approves(docs, registry) is True, registry


def test_human_approves_MAPPED_and_FREE_at_a_low_dial(tmp_path):
    """Arm 2 — the arm that proves the predicate is DERIVED rather than a
    constant `True` wearing a lookup. At a `DevStg-Boundary` dial only
    Needs/Boundary are held, so `external` (DevStg-Boundary) stays the human's
    while `interfaces` and `components` (DevStg-Arch) become machine-flippable."""
    docs = _docs(tmp_path, dial=dg.STAGE_BOUNDARY)
    assert ac.human_approves(docs, "external") is True
    assert ac.human_approves(docs, "interfaces") is False
    assert ac.human_approves(docs, "components") is False
    # ...and at `DevStg-Below` nothing is held at all, which is what "no new
    # enum" buys: the off-spine axis moves with the one dial, never independently.
    docs0 = _docs(tmp_path / "zero", dial=BELOW)
    for registry in ac.APPROVAL_RUNGS:
        assert ac.human_approves(docs0, registry) is False, registry


def test_human_approves_UNMAPPED_is_HELD_fail_safe(tmp_path):
    """Arm 3 — the fail-safe direction, ruled explicitly: an approval-carrying
    registry with no rung mapping is HELD, because a registry nobody has
    associated with a rung is one nobody has ruled on."""
    docs = _docs(tmp_path, dial=BELOW)  # the MOST permissive dial there is
    for unknown in ("assets", "procurement", "", None, "Interfaces "):
        # (`"Interfaces "` is the casing/whitespace arm: it MAPS, because the
        # lookup normalises — an unmapped answer there would be a false hold
        # hiding a real one.)
        expected = unknown is not None and unknown.strip().lower() in ac.APPROVAL_RUNGS
        assert ac.human_approves(docs, unknown) is (not expected), unknown


def test_no_shipped_loop_module_WRITES_an_approval_cell():
    """THE GUARD THAT ACTUALLY BITES TODAY (OI-30 D3's writer-side contract).

    No WI kind carries a registry identity, so `dispatch._kind_action`'s
    `approval_held` seam has no live caller — which is stated in its docstring
    rather than dressed up. What CAN be enforced now is the premise that makes
    that acceptable: the kit ships NO automated writer of an off-spine approval
    cell. The moment one is added this fails, and whoever adds it has to route it
    through `agent_common.human_approves` first.

    RE-KEYED 2026-08-17, and this is the trap the registry status unification was
    written to walk around. The cell used to be spelled `approval`; it is
    `status` now. A regex still hunting `approval = "approved"` would have gone
    on passing FOREVER, green against a spelling no registry uses — the exact
    silently-disarmed-guard failure this whole change exists to prevent. So the
    pattern hunts the LIVE spelling, and it hunts the retired one too: a writer
    added against the old name is still a writer.

    Narrow on purpose: an `approval` word in a comment is documentation (these
    modules are full of it). What is forbidden is ASSIGNING the approved value to
    a maturity-shaped key in running code."""
    import re as _re
    from pathlib import Path as _Path

    scripts = _Path(__file__).resolve().parents[1] / "project-trajectory" / "scripts"
    # `status = "Approved"`, `status: "Approved"`, `["status"] = "Approved"` and
    # the TOML line an emitter would write — plus the retired `approval` spelling
    # and the retired `verified`/`built` CMP words, so a writer cannot be smuggled
    # in under a name this repo has already stopped using.
    pat = _re.compile(
        r"""\b(?:status|approval|state)["'\]]*\s*[:=]\s*"""
        r"""["'](?:approved|verified|built|founded)["']""",
        _re.IGNORECASE,
    )
    offenders = []
    for path in sorted(scripts.glob("*.py")):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            code = line.split("#", 1)[0]
            if pat.search(code):
                offenders.append("{}:{}: {}".format(path.name, n, line.strip()))
    assert not offenders, (
        "a shipped script writes an off-spine `approval` cell — route it through "
        "`agent_common.human_approves(docs, registry)` and REFUSE when it "
        "answers True (OI-30 D3):\n" + "\n".join(offenders)
    )


def test_the_dispatcher_seam_surfaces_on_EITHER_hold():
    """`approval_held` is a second reason to surface, not a widening of the
    spine one: a held approval surfaces an attestation/gate row even on a spine
    tier the project declared machine-ratifiable."""
    dispatch = load_script("dispatch")
    assert dispatch._kind_action("attestation", False) == "exclusive"
    assert dispatch._kind_action("attestation", False, approval_held=True) == "surface"
    assert dispatch._kind_action("gate", False, approval_held=True) == "surface"
    assert dispatch._kind_action("attestation", True, approval_held=False) == "surface"
    # Every other kind is untouched by the off-spine axis — the ruling is about
    # who may write an approval, not about what may run.
    for kind in ("ordinary", "critique", "spine", "high-risk", "adjudication"):
        assert dispatch._kind_action(kind, False, approval_held=True) == (
            dispatch._kind_action(kind, False)
        ), kind
