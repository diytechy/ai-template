"""The id carrier, in process: the record grammar, the carrier-space split,
the reserve verb's argument table, the fold, the fold lag, the range plan and
the landing judgement (TC-401; the landing and fold-lag judgements also pin
TC-402's pure half).

Parallel lanes cut from different bases would each draw "the next number" for
a spine space, so the carrier is the one allocation authority every lane
reserves from. These cases pin the pure stages that authority is built from,
and drive every refusal of the reserve verb's argument table through
`trace.py`'s CLI, in process, asserting that nothing is written: the carrier
ref stays where it was and the working watermark is byte-identical.

A missing module or symbol is turned into `pytest.fail`, so a red is this
file's own, never an import error. The real-repository cases (a lost race,
two worktrees, a conflicted fold, the landings) are in test_id_carrier_git.py
and test_id_landing.py, outside the smoke tier.

Implements: TC-401
"""

import sys

import pytest
from conftest import (
    ID_CARRIER_REF,
    declare_trunk,
    env_gate_skipif,
    fixture_commit,
    fixture_git,
    load_script,
    pin_autocrlf,
    plant_id_carrier,
    reserved_watermark,
)

TRACE = load_script("trace")
SPACES = tuple(TRACE.WATERMARK_SPACES)
TRUNK = {"WI", "OI", "DP"}


_LOADED = []


def _ic():
    """The carrier module, loaded once for the whole file (a fresh load per
    symbol would give each load its own `Refused` class, and a raise from one
    load would miss another load's `pytest.raises`), or this test's own failure
    while it is unbuilt."""
    if not _LOADED:
        try:
            _LOADED.append(load_script("id_carrier"))
        except (FileNotFoundError, ImportError) as exc:
            pytest.fail("the id carrier module is not built: {}".format(exc))
    return _LOADED[0]


def _sym(name):
    """One public name of the carrier module, or this test's own failure."""
    ic = _ic()
    if not hasattr(ic, name):
        pytest.fail("the id carrier module has no {}".format(name))
    return getattr(ic, name)


# --- the record grammar ------------------------------------------------------


def test_the_grammar_admits_the_well_formed_line_on_the_stripped_line():
    text = (
        "# ID WATERMARK\n"
        "# reservation: SR 6-7 (WI-978)\n"
        "   # reservation: TC 4-4 (WI-978)   \n"
        "SR = 7\n"
    )
    assert _sym("parse_reservations")(text) == [
        ("SR", 6, 7, "WI-978"),
        ("TC", 4, 4, "WI-978"),
    ]


@pytest.mark.parametrize(
    "line",
    [
        "# reservation: SR 7-6 (WI-978)",  # low above high
        "# reservation: WI 6-7 (WI-978)",  # a trunk space
        "# reservation: SR 6-7",  # no work item
        "# reservation: SR 6-7 (WI-978) and more",  # trailing text
        "# reservation: SR 0-3 (WI-978)",  # number 0 is never an allocation
        "# reservation: SR 6-7 (SR-001)",  # not a work item
    ],
    ids=["reversed", "trunk-space", "no-wi", "trailing", "zero", "not-a-wi"],
)
def test_a_malformed_line_is_not_a_record(line):
    assert _sym("parse_reservations")(line + "\nSR = 7\n") == []


# --- the carrier spaces ------------------------------------------------------


def test_the_carrier_spaces_are_every_space_but_the_trunk_minted_three():
    carrier_spaces = _sym("carrier_spaces")
    assert set(_sym("TRUNK_SPACES")) == TRUNK
    assert set(carrier_spaces(SPACES)) == set(SPACES) - TRUNK
    # Deny-by-default: a space added to the one list joins the carrier.
    assert "NEW" in set(carrier_spaces(SPACES + ("NEW",)))


# --- the reserve verb's arguments ---------------------------------------------


def test_the_counts_admit_each_carrier_space_from_1_to_50():
    parse_counts = _sym("parse_counts")
    assert parse_counts("SR=2,TC=1", SPACES) == {"SR": 2, "TC": 1}
    assert parse_counts("LLR=50", SPACES) == {"LLR": 50}
    assert parse_counts("B=1", SPACES) == {"B": 1}


COUNT_REFUSALS = [
    ("WI=1", "minted on trunk"),
    ("OI=1", "minted on trunk"),
    ("DP=1", "minted on trunk"),
    ("ZZ=1", "ZZ"),
    ("SR=x", "SR"),
    ("SR=0", "SR"),
    ("SR=51", "SR"),
    ("SR=1,SR=2", "SR"),
    ("", ""),
    ("SR", "SR"),
]
COUNT_IDS = [
    "wi",
    "oi",
    "dp",
    "unknown",
    "not-int",
    "below-1",
    "above-50",
    "repeated",
    "no-pair",
    "no-equals",
]


@pytest.mark.parametrize("counts,named", COUNT_REFUSALS, ids=COUNT_IDS)
def test_the_counts_refuse_outside_the_table(counts, named):
    refused = _sym("Refused")
    with pytest.raises(refused) as exc:
        _sym("parse_counts")(counts, SPACES)
    message = str(exc.value)
    assert "\n" not in message.strip() and named in message


def _check_work_item():
    """The reserve verb's work-item check: the tracer reads it through the
    kit's one lane-input parser, so it lives beside the verb, not here."""
    return TRACE.check_work_item, TRACE.id_carrier.Refused


def test_the_work_item_admits_one_well_formed_id():
    check_work_item, _refused = _check_work_item()
    assert check_work_item("WI-978") == "WI-978"
    assert check_work_item(" WI-401 ") == "WI-401"


WI_REFUSALS = ["", "WI-001,WI-002", "WI-001 WI-002", "wi-001", "SR-001", "WI-"]
WI_IDS = ["empty", "comma-list", "space-list", "lower-case", "not-wi", "no-number"]


@pytest.mark.parametrize("text", WI_REFUSALS, ids=WI_IDS)
def test_the_work_item_refuses_anything_but_one_id(text):
    check_work_item, refused = _check_work_item()
    with pytest.raises(refused) as exc:
        check_work_item(text)
    assert "\n" not in str(exc.value).strip()


# --- the fold -----------------------------------------------------------------


def test_the_fold_takes_each_spaces_maximum_and_the_union_of_records():
    lane = reserved_watermark({"SR": 7, "TC": 3}, [("SR", 6, 7, "WI-1")])
    trunk = reserved_watermark(
        {"SR": 9, "TC": 2, "B": 8},
        [("SR", 8, 9, "WI-2")],
        corrections={"B": [(7, 8, "OI-47")]},
    )
    marks, reservations, corrections = _sym("fold")([lane, trunk])
    assert (marks["SR"], marks["TC"], marks["B"]) == (9, 3, 8)
    assert reservations == [("SR", 6, 7, "WI-1"), ("SR", 8, 9, "WI-2")]
    assert corrections == {"B": [(7, 8, "OI-47")]}


def test_the_fold_collapses_duplicates_and_sorts_by_space_then_low():
    one = reserved_watermark(
        {"SR": 9, "TC": 4}, [("TC", 4, 4, "WI-2"), ("SR", 8, 9, "WI-2")]
    )
    two = reserved_watermark(
        {"SR": 9, "TC": 4}, [("SR", 8, 9, "WI-2"), ("SR", 6, 7, "WI-1")]
    )
    _marks, reservations, _corrections = _sym("fold")([one, two])
    assert reservations == [
        ("SR", 6, 7, "WI-1"),
        ("SR", 8, 9, "WI-2"),
        ("TC", 4, 4, "WI-2"),
    ]


# --- the fold lag ---------------------------------------------------------------

CARRIER = reserved_watermark(
    {"SR": 9, "TC": 4}, [("SR", 6, 7, "WI-1"), ("SR", 8, 9, "WI-2")]
)


def test_no_lag_when_the_file_holds_the_fold_or_there_is_no_carrier():
    fold_lag = _sym("fold_lag")
    held = reserved_watermark(
        {"SR": 9, "TC": 4}, [("SR", 6, 7, "WI-1"), ("SR", 8, 9, "WI-2")]
    )
    assert fold_lag(CARRIER, held) == []
    assert fold_lag(None, reserved_watermark({"SR": 1})) == []


def test_a_recorded_mark_above_the_files_is_a_lag():
    held_records = [("SR", 6, 7, "WI-1"), ("SR", 8, 9, "WI-2")]
    lines = _sym("fold_lag")(
        CARRIER, reserved_watermark({"SR": 8, "TC": 4}, held_records)
    )
    assert lines and any("SR" in ln and "9" in ln for ln in lines), lines


def test_the_carrier_contributes_only_its_records_and_the_marks_they_justify():
    # The carrier's TC mark (trunk's, as of a reservation) has no record, so a
    # fold never copies it into a working file and a file below it does not
    # lag: a lane cut before trunk raised it could not commit it.
    carried = _sym("carried")(CARRIER)
    marks, records, _corrections = _sym("fold")([carried])
    assert marks == {"SR": 9}
    assert records == [("SR", 6, 7, "WI-1"), ("SR", 8, 9, "WI-2")]
    held_records = [("SR", 6, 7, "WI-1"), ("SR", 8, 9, "WI-2")]
    file_text = reserved_watermark({"SR": 9, "TC": 3, "WI": 2}, held_records)
    assert _sym("fold_lag")(CARRIER, file_text) == []
    assert _sym("carried")(None) is None


def test_a_carrier_record_the_file_lacks_is_a_lag():
    lines = _sym("fold_lag")(
        CARRIER, reserved_watermark({"SR": 9, "TC": 4}, [("SR", 6, 7, "WI-1")])
    )
    assert lines and any("SR 8-9 (WI-2)" in ln for ln in lines), lines


def test_a_file_ahead_of_the_carrier_does_not_lag():
    # The lane's own live ids raised its marks past every record: the fold of
    # the carrier into this file changes nothing, so nothing lags.
    ahead = reserved_watermark(
        {"SR": 12, "TC": 6, "LLR": 3},
        [("SR", 6, 7, "WI-1"), ("SR", 8, 9, "WI-2")],
    )
    assert _sym("fold_lag")(CARRIER, ahead) == []


# --- the range plan -------------------------------------------------------------


def test_a_range_starts_one_above_the_larger_of_carrier_and_trunk():
    plan = _sym("plan_reservation")
    got = plan({"SR": 7, "TC": 3}, {"SR": 9, "TC": 2}, {"SR": 2, "TC": 1}, "WI-5")
    assert got == [("SR", 10, 11, "WI-5"), ("TC", 4, 4, "WI-5")]
    # First use: no carrier marks, so trunk's committed marks are the floor.
    assert plan({}, {"SR": 9}, {"SR": 1}, "WI-5") == [("SR", 10, 10, "WI-5")]


# --- the landing judgement ------------------------------------------------------

OWN = ("SR", 6, 7, "WI-978")
OTHER = ("SR", 8, 9, "WI-979")
NO_CARRIER = dict(carrier_records=[], landing_records=[], carrier_present=False)
LANDING_CASES = {
    # row 1: no carrier-space id added passes, whatever else holds.
    "nothing-added": (dict(NO_CARRIER, added=[], claim_problem="no claim"), None),
    # a `-000` placeholder is never an allocation, so never judged.
    "placeholder": (dict(NO_CARRIER, added=[("SR", 0)]), None),
    # row 2: every added id inside its own work item's record.
    "own-record": (dict(added=[("SR", 6), ("SR", 7)]), None),
    # row 3: outside every record naming the work item (here: another's).
    "other-record": (dict(added=[("SR", 8)]), ("SR-008", "WI-978", "--reserve-ids")),
    # row 4: ids added and no carrier ref.
    "no-carrier": (
        dict(NO_CARRIER, added=[("SR", 6)]),
        ("SR-006", "WI-978", "--reserve-ids"),
    ),
    # row 5: ids added and the work item unreadable from the claim.
    "claim-unreadable": (
        dict(added=[("SR", 6)], wi_ids=[], claim_problem="docs/work/active/x/"),
        ("docs/work/active/x/",),
    ),
    # row 3, a retired number re-used: inside its own record, and still refused.
    "retired-in-own-record": (
        dict(added=[("SR", 6)], retired={("SR", 6): "docs/log.d/retired/SR-006.md"}),
        ("SR-006", "docs/log.d/retired/SR-006.md"),
    ),
    # a live id the landing's own retirement record names, though no id is
    # added (retired, then authored again, under one number its parent held).
    "reissued-with-none-added": (
        dict(reissued={("SR", 3): "docs/log.d/retired/SR-003.md"}),
        ("SR-003", "docs/log.d/retired/SR-003.md"),
    ),
    # row 6: a record the landing carries that neither carrier nor parent holds.
    "landing-only-record": (
        dict(added=[("SR", 6)], landing_records=[OWN, ("SR", 10, 10, "WI-978")]),
        ("# reservation: SR 10-10 (WI-978)",),
    ),
}


@pytest.mark.parametrize("case", sorted(LANDING_CASES))
def test_the_landing_judgement_rules_each_row_of_the_table(case):
    kwargs, named = LANDING_CASES[case]
    args = dict(
        added=[],
        carrier_records=[OWN, OTHER],
        wi_ids=["WI-978"],
        landing_records=[OWN],
        parent_records=[],
        carrier_present=True,
        claim_problem=None,
    )
    args.update(kwargs)
    lines = _sym("landing_lines")(**args)
    if named is None:
        assert lines == [], lines
    else:
        assert lines, case
        text = "\n".join(lines)
        assert all(word in text for word in named), (named, lines)


# --- the reserve verb's refusals, through the CLI ---------------------------------


@pytest.fixture(scope="module")
def claimed_trunk(tmp_path_factory):
    """A trunk on `main` holding WI-001's claim and a committed watermark, with
    a carrier already planted. Shared by the refusal cases, each of which
    asserts it wrote nothing, so no case can see another's leftovers."""
    root = tmp_path_factory.mktemp("claimed-trunk")
    fixture_git(root, "init", "-q")
    pin_autocrlf(root)
    fixture_git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    declare_trunk(root, "main")
    claim = root / "docs" / "work" / "active" / "wi-001" / "WI-001-x.md"
    claim.parent.mkdir(parents=True)
    claim.write_text('+++\nid = "WI-001"\n+++\n', encoding="utf-8", newline="\n")
    text = reserved_watermark({"SR": 5, "TC": 3, "WI": 1})
    (root / TRACE.WATERMARK).write_text(text, encoding="utf-8", newline="\n")
    fixture_commit(root, "seed: the claim and the watermark")
    plant_id_carrier(root, reserved_watermark({"SR": 7}, [("SR", 6, 7, "WI-001")]))
    return root


def _state(root):
    """The two durable states a reservation may write: the carrier tip and the
    working watermark's bytes."""
    tip = fixture_git(root, "rev-parse", ID_CARRIER_REF)
    return tip, (root / TRACE.WATERMARK).read_bytes()


def _trace_cli(monkeypatch, capsys, root, *args):
    """`trace.py --root <root> <args>`, in process: (exit code, stdout, stderr)."""
    monkeypatch.setattr(sys, "argv", ["trace.py", "--root", str(root), *args])
    try:
        TRACE.main()
        code = 0
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
    out, err = capsys.readouterr()
    return code, out, err


CLI_REFUSALS = [
    ("", "SR=1", ""),
    ("WI-001,WI-002", "SR=1", ""),
    ("wi-001", "SR=1", ""),
    ("WI-002", "SR=1", "WI-002"),
] + [("WI-001", counts, named) for counts, named in COUNT_REFUSALS]
CLI_IDS = ["wi-empty", "wi-list", "wi-malformed", "wi-not-claimed"] + [
    "counts-" + i for i in COUNT_IDS
]


@env_gate_skipif("git")
@pytest.mark.parametrize("wi,counts,named", CLI_REFUSALS, ids=CLI_IDS)
def test_each_reserve_refusal_writes_nothing(
    claimed_trunk, monkeypatch, capsys, wi, counts, named
):
    before = _state(claimed_trunk)
    code, _out, err = _trace_cli(
        monkeypatch, capsys, claimed_trunk, "--reserve-ids", wi, counts
    )
    assert code == 1, err
    assert len(err.strip().splitlines()) == 1 and named in err, err
    assert _state(claimed_trunk) == before


@env_gate_skipif("git")
def test_a_reserve_with_no_counts_argument_is_a_usage_error(
    claimed_trunk, monkeypatch, capsys
):
    before = _state(claimed_trunk)
    code, _out, err = _trace_cli(
        monkeypatch, capsys, claimed_trunk, "--reserve-ids", "WI-001"
    )
    assert code == 2, err
    # The verb's own usage error, not argparse refusing an unknown flag.
    assert "--reserve-ids" in err and "expected 2 arguments" in err, err
    assert _state(claimed_trunk) == before
