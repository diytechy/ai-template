"""The review test set's pure walk (WI-995), in process.

From a row's SRs, the walk reaches every LLR naming one of them and every test
case verifying either, puts each case in exactly one class, and returns the
tagged test files, the evidence listed beside them and every gap. It reads rows
only, so these cases hand it rows and an existence predicate. The lane reading
and the refusals are in `tests/test_review_set.py`; this module is that family's
in-process pin in the smoke tier.
"""

import pytest
from kitlib import spine as kspine

TEST_A = "tests/test_a.py"
TEST_B = "tests/test_b.py"


def _llr(llr, *srs):
    return {"LLR-ID": llr, "SR-Refs": ";".join(srs)}


def _tc(tc, verifies, evidence="", status="Approved"):
    return {"TC-ID": tc, "Verifies": verifies, "Evidence": evidence, "Status": status}


def _scope(srs, llrs=(), tcs=(), tags=None, exists=lambda _path: True):
    files, listed, gaps = kspine.review_scope(
        srs, llrs, tcs, tags or {}, "tests", exists
    )
    return list(files), list(listed), list(gaps)


def _names(items, text):
    return any(text in str(item) for item in items)


def test_the_walk_unions_direct_tcs_and_tcs_through_the_llrs():
    """Implements: TC-413"""
    llrs = [_llr("LLR-001", "SR-001"), _llr("LLR-009", "SR-009")]
    tcs = [
        _tc("TC-001", "SR-001", TEST_A),
        _tc("TC-002", "LLR-001", TEST_B),
        _tc("TC-009", "SR-009;LLR-009", "tests/test_out.py"),
    ]
    tags = {
        "TC-001": [TEST_A],
        "TC-002": [TEST_B + "::test_it"],
        "TC-009": ["tests/test_out.py"],
    }
    files, _listed, gaps = _scope(["SR-001"], llrs, tcs, tags)
    assert files == [TEST_A, TEST_B]
    assert gaps == []


def test_an_llr_naming_two_srs_is_reached_from_either():
    """Implements: TC-413"""
    llrs = [_llr("LLR-001", "SR-001", "SR-002")]
    tcs = [_tc("TC-001", "LLR-001", TEST_A)]
    tags = {"TC-001": [TEST_A]}
    assert _scope(["SR-001"], llrs, tcs, tags)[0] == [TEST_A]
    assert _scope(["SR-002"], llrs, tcs, tags)[0] == [TEST_A]


def test_a_drafted_tc_is_in_scope():
    """Implements: TC-413"""
    tcs = [_tc("TC-001", "SR-001", TEST_A, status="Drafted")]
    assert _scope(["SR-001"], (), tcs, {"TC-001": [TEST_A]})[0] == [TEST_A]


@pytest.mark.parametrize(
    "evidence, tags, where, named",
    [
        pytest.param(TEST_A, {"TC-001": [TEST_A]}, "files", TEST_A, id="tagged"),
        pytest.param(
            TEST_A,
            {},
            "gaps",
            "TC-001: no test file tags it (evidence names {})".format(TEST_A),
            id="untagged",
        ),
        pytest.param(
            "docs/inspect.md", {}, "listed", "docs/inspect.md", id="non-executable"
        ),
        pytest.param("", {}, "gaps", "TC-001: no evidence", id="no-cell"),
        pytest.param(
            "docs/gone.md",
            {},
            "gaps",
            "TC-001: no evidence (docs/gone.md)",
            id="missing-path",
        ),
    ],
)
def test_a_tc_falls_in_exactly_one_class(evidence, tags, where, named):
    """Implements: TC-413"""
    files, listed, gaps = _scope(
        ["SR-001"],
        tcs=[_tc("TC-001", "SR-001", evidence)],
        tags=tags,
        exists=lambda path: path != "docs/gone.md",
    )
    homes = {"files": files, "listed": listed, "gaps": gaps}
    assert [home for home, items in homes.items() if _names(items, named)] == [where]
    assert sum(len(items) for items in homes.values()) == 1, homes


def test_a_tagged_tc_lists_its_non_test_evidence_beside_the_set():
    """Implements: TC-413"""
    tcs = [_tc("TC-001", "SR-001", TEST_A + "; hooks/pre-commit")]
    files, listed, gaps = _scope(["SR-001"], (), tcs, {"TC-001": [TEST_A]})
    assert files == [TEST_A]
    assert _names(listed, "hooks/pre-commit")
    assert gaps == []


def test_the_set_is_the_sorted_files_of_the_tagged_nodes():
    """Implements: TC-413"""
    tcs = [_tc("TC-001", "SR-001", TEST_B), _tc("TC-002", "SR-001", TEST_A)]
    tags = {
        "TC-001": [TEST_B + "::test_late"],
        "TC-002": [TEST_A + "::test_one", TEST_A + "::test_two"],
    }
    assert _scope(["SR-001"], (), tcs, tags)[0] == [TEST_A, TEST_B]


def test_an_sr_verified_only_directly_has_no_gap():
    """Implements: TC-413"""
    tcs = [
        _tc("TC-001", "SR-001", TEST_A),
        _tc("TC-002", "SR-002", "docs/inspect.md"),
    ]
    files, listed, gaps = _scope(["SR-001", "SR-002"], (), tcs, {"TC-001": [TEST_A]})
    assert files == [TEST_A]
    assert _names(listed, "docs/inspect.md")
    assert gaps == []


def test_an_sr_verified_only_through_its_llr_has_no_gap():
    """Implements: TC-414"""
    llrs = [_llr("LLR-001", "SR-001")]
    tcs = [_tc("TC-001", "LLR-001", TEST_A)]
    files, _listed, gaps = _scope(["SR-001"], llrs, tcs, {"TC-001": [TEST_A]})
    assert files == [TEST_A]
    assert gaps == []


@pytest.mark.parametrize(
    "llrs, tcs, gap",
    [
        pytest.param((), (), "SR-001: no test case verifies it", id="sr"),
        pytest.param(
            [_llr("LLR-001", "SR-001")],
            [_tc("TC-001", "SR-001", TEST_A)],
            "LLR-001: no test case verifies it",
            id="llr",
        ),
        pytest.param(
            [_llr("LLR-001", "SR-001"), _llr("LLR-002", "SR-001")],
            [_tc("TC-001", "SR-001;LLR-001", TEST_A)],
            "LLR-002: no test case verifies it",
            id="sibling-llr",
        ),
    ],
)
def test_each_gap_is_named(llrs, tcs, gap):
    """Implements: TC-414"""
    gaps = _scope(["SR-001"], llrs, tcs, {"TC-001": [TEST_A]})[2]
    assert [str(item) for item in gaps] == [gap]
