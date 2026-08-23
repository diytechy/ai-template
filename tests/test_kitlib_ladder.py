"""`kitlib.ladder` — the eight-rung DevStg stage vocabulary, one home (TC-179).

The vocabulary used to be DEFINED in four places and held together by equality
pins: `spine_rules` (the intended SSOT), `agent_common.LADDER_RUNGS` (a literal
frozenset, pinned), `traj_status._STAGE_LABELS` (a byte-identical copy of the
descriptions, pinned by NOTHING), and prose. WI-498 slice 0 collapsed that to one
module, so the pins retired: drift became UNREPRESENTABLE rather than DETECTED.

What is worth asserting AFTER that collapse is not "the copies agree" — a test
that a frozenset equals itself is vacuous and reads green while checking
nothing. It is the three properties the one home must actually hold:

  * the ladder's SHAPE (eight rungs, the ruled order, the derived size, a
    description per rung),
  * the ORDERING CONTRACT — `stage_ord` is the only legal comparison and it
    RAISES rather than defaulting, because the labels do NOT alphabetize,
  * and the module's IMPORT-CLEANLINESS, which is what makes it safe for the
    scaffolder and a render leaf alike.

The identity assertions that WARRANT the deleted pins live at their own sites
(`tests/test_approval_level.py`, and `test_every_reader_resolves_to_this_one_object`
below).
"""

import ast

import pytest
from conftest import SCRIPTS, load_script

from kitlib import ladder


def test_the_ladder_is_the_ruled_EIGHT_RUNGS_in_the_ruled_ORDER():
    """The order is the OI-21 ruling — requirements before architecture, the
    boundary once, LLReqs terminal — and it is asserted whole rather than
    spot-checked, because an insertion in the wrong place is the failure this
    vocabulary exists to make visible."""
    assert ladder.STAGE_ORDER == [
        "DevStg-Needs",
        "DevStg-Boundary",
        "DevStg-Reqs",
        "DevStg-Arch",
        "DevStg-LLReqs",
        "DevStg-Tests",
        "DevStg-Impl",
        "DevStg-Release",
    ]
    # The SIZE IS DERIVED, never authored — the whole point of the label
    # carrier: inserting a rung self-corrects every rendered "stage N of M".
    assert ladder.STAGE_OF == len(ladder.STAGE_ORDER) == 8
    assert ladder.LADDER_RUNGS == frozenset(ladder.STAGE_ORDER)
    # No rung is spelled twice, which a list cannot say for itself.
    assert len(ladder.LADDER_RUNGS) == len(ladder.STAGE_ORDER)


def test_every_rung_has_a_description_and_nothing_else_does():
    """A renderer degrades to bar-only wording for a rung it cannot describe, so
    a missing entry does not crash — it silently DROPS the stage from the
    dashboard. Both directions are pinned: no rung without a sentence, no
    sentence without a rung."""
    assert set(ladder.STAGE_DESC) == set(ladder.STAGE_ORDER)
    assert all(ladder.STAGE_DESC[rung].strip() for rung in ladder.STAGE_ORDER)


def test_stage_ord_is_the_position_and_RAISES_on_an_unknown_label():
    """The label is the identifier; position is derived. And an unknown label
    means the ladder moved under a cached value — the wrong-answer direction of
    a silent default is LESS human involvement, so it fails loudly."""
    for i, rung in enumerate(ladder.STAGE_ORDER):
        assert ladder.stage_ord(rung) == i
    # The retired spellings are the INPUTS under test here: a cached tag or a
    # bar label reaching this lookup is exactly the "the ladder moved under a
    # cached value" case, so the row that proves it raises must name them.
    for bad in ("", "DevStg-Bogus", "G2", "DevBar-Reqs", None, 3):  # check_vocab: allow
        with pytest.raises(ValueError):
            ladder.stage_ord(bad)


def test_the_labels_do_NOT_alphabetize_which_is_why_the_lookup_exists():
    """The trap the retired tags hid: `G1 < G2 < G3` was accidentally correct (check_vocab: allow)
    — so comparing gate names as raw strings survived for months. These labels
    invert rungs 1 and 3 under the same comparison, so the accident is gone and
    the ban has teeth. If this assertion ever fails, the ordering operators are
    no longer wrong-by-construction and `tests/test_stage_ladder.py`'s grep is
    the only thing left holding the rule."""
    assert sorted(ladder.STAGE_ORDER) != ladder.STAGE_ORDER
    assert sorted(["DevStg-Boundary", "DevStg-Arch"]) == [
        "DevStg-Arch",
        "DevStg-Boundary",
    ], "lexical order inverts rungs 1 and 3 — the reason stage_ord is mandatory"


def test_the_module_imports_NOTHING():
    """The strongest available form of the `kitlib` discipline rule.

    Every module in the package must stay import-clean of the rest of
    `scripts/` (`test_bootstrap.py::test_bootstrap_imports_only_the_common_package`
    asserts that much). This one goes further and imports nothing AT ALL, not
    even stdlib — a table of strings with an index lookup has no reason to reach
    for anything, and having nothing to reach for is what makes it safe for the
    scaffolder and for a render leaf. Asserted from the SOURCE, because that is
    the property a reader can check.
    """
    tree = ast.parse((SCRIPTS / "kitlib" / "ladder.py").read_text(encoding="utf-8"))
    imports = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    assert not imports, "kitlib.ladder must stay pure data: {}".format(
        [ast.dump(node) for node in imports]
    )


def test_every_reader_resolves_to_this_one_object():
    """THE WARRANT FOR THE RETIRED PINS, stated by IDENTITY rather than by value.

    Before WI-498 slice 0 these were three separate literals kept in step by
    equality tests (`agent_common`'s, pinned; `traj_status`'s, pinned by
    nothing at all — a renderer free to drift silently). `is` is the strongest
    statement available here and the cheapest: it says there is nothing left to
    drift, which is what makes deleting the old equality pins safe rather than
    merely convenient.
    """
    dg = load_script("spine_rules")
    ac = load_script("agent_common")
    ts = load_script("traj_status")
    assert dg.STAGE_ORDER is ladder.STAGE_ORDER
    assert dg.STAGE_DESC is ladder.STAGE_DESC
    assert dg.stage_ord is ladder.stage_ord
    assert ac.LADDER_RUNGS is ladder.LADDER_RUNGS
    assert ts._STAGE_LABELS is ladder.STAGE_DESC
