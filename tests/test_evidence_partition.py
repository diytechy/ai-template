"""Assumption evidence counted apart from requirement evidence (TC-227).

A test case may evidence the domain assumptions a requirement's argument relies
on (`Assumption-Refs`) instead of, or beside, the requirements and design rows
it verifies (`Verifies`). The two are different obligations: that the system
does what its requirements say, and that what they say reaches the outcome. So
every reader that counts evidence makes the same split, and the readers that
answer "is this requirement verified" keep reading `Verifies` alone.

In memory throughout: the spine is plain row dicts in the carrier's column
names, and the census's one file read (which work items are closed) is
replaced by the set it would return.
"""

import copy
from types import SimpleNamespace

import pytest

from conftest import load_script

TRACE = load_script("trace")
COHERENCE = load_script("coherence")
SPINE_RULES = load_script("spine_rules")


@pytest.fixture()
def census(monkeypatch):
    """The census with its work-registry read replaced: SR-001 and its design
    row are claimed built by a closed work item."""
    module = load_script("census")
    monkeypatch.setattr(module, "_implemented_ids", lambda root: {"SR-001", "LLR-001"})
    return module


SRS = [
    {
        "SR-ID": "SR-001",
        "Title": "Adds",
        "SN-Refs": "SN-001",
        "DA-Refs": "DA-001",
        "Status": "Approved",
        "Verification": "Test",
    }
]
LLRS = [
    {"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Title": "Adder", "Status": "Approved"}
]


def _tc(tid, verifies="", assumptions="", status="Approved"):
    row = {"TC-ID": tid, "Verifies": verifies, "Method": "m", "Status": status}
    if assumptions:
        row["Assumption-Refs"] = assumptions
    return row


def _spine(status="Approved"):
    """A requirement-only case, an assumption-only case, a case citing both,
    and a case citing neither."""
    return [
        _tc("TC-001", "SR-001;LLR-001", status=status),
        _tc("TC-002", "", "DA-001", status=status),
        _tc("TC-003", "SR-001;LLR-001", "DA-001", status=status),
        _tc("TC-004", "", status=status),
    ]


def _ids(rows):
    return [r["TC-ID"] for r in rows]


def _stripped(tcs):
    """The same spine with every assumption reference removed."""
    out = copy.deepcopy(tcs)
    for row in out:
        row.pop("Assumption-Refs", None)
    return out


def test_the_partition_counts_a_case_citing_both_once_in_each():
    requirement, assumption = TRACE.assumption_evidence_rows(_spine())
    assert _ids(requirement) == ["TC-001", "TC-003"]
    assert _ids(assumption) == ["TC-002", "TC-003"]


def _group(roots, label):
    return next((r for r in roots if r["id"] == label), None)


def _walk(node):
    yield node
    for child in node["children"]:
        yield from _walk(child)


def test_the_forest_lists_an_assumption_only_case_under_its_own_group():
    roots = TRACE.build_forest({"SN-001"}, SRS, LLRS, _spine(), set())
    group = _group(roots, "(assumption evidence)")
    assert group is not None, [r["id"] for r in roots]
    assert [n["id"] for n in group["children"]] == ["TC-002"]
    nothing = _group(roots, "(TCs verifying nothing valid)")
    assert nothing is not None
    assert [n["id"] for n in nothing["children"]] == ["TC-004"]
    # The case citing both sits under the design row it verifies, and only there.
    placed = [n["id"] for root in roots for n in _walk(root)]
    assert placed.count("TC-003") == 1
    sn = _group(roots, "SN-001")
    assert "TC-003" in [n["id"] for n in _walk(sn)]


def test_the_census_counts_assumption_evidence_apart(census, tmp_path):
    reg = SimpleNamespace(srs=SRS, llrs=LLRS, tcs=_spine(status="Failed"))
    requirement = census.red_tc_census(tmp_path, reg)
    assumption = census.red_tc_census(tmp_path, reg, assumptions=True)
    parsed = [census.parse_red_tc(line) for line in requirement]
    assert parsed == [
        ("TC-001", ["SR-001", "LLR-001"]),
        ("TC-003", ["SR-001", "LLR-001"]),
    ]
    assert [line.split()[3] for line in assumption] == ["TC-002", "TC-003"]
    assert all("DA-001" in line for line in assumption)
    # A distinct line class: the requirement census's one reader never takes an
    # assumption line for one of its own.
    assert all(census.parse_red_tc(line) is None for line in assumption)


def test_the_census_names_no_assumption_case_whose_argument_is_not_claimed(
    census, tmp_path
):
    unclaimed = [dict(SRS[0], **{"SR-ID": "SR-002"})]
    reg = SimpleNamespace(srs=unclaimed, llrs=[], tcs=_spine(status="Failed"))
    assert census.red_tc_census(tmp_path, reg, assumptions=True) == []


def test_the_report_counts_assumption_evidence_beside_requirement_evidence():
    rows = TRACE.evidence_metric_rows(_spine())
    assert rows == [
        "| Test cases — requirement evidence | 2 |",
        "| Test cases — assumption evidence | 2 |",
    ]
    # A project that never cites an assumption renders the report it always did.
    assert TRACE.evidence_metric_rows(_stripped(_spine())) == []


def test_the_requirement_readers_ignore_assumption_references():
    tcs = _spine()
    bare = _stripped(tcs)
    # The verified-requirement join: which requirements and design rows have a test.
    assert SPINE_RULES._decomposed_sr_ids(LLRS, tcs) == SPINE_RULES._decomposed_sr_ids(
        LLRS, bare
    )

    # The SR -> LLR -> TC matrix is built from these two indexes.
    def buckets(rows):
        return [
            {
                parent: [k.get("TC-ID") or k.get("LLR-ID") for k in kids]
                for parent, kids in index.items()
            }
            for index in TRACE.chain_buckets(LLRS, rows)
        ]

    assert buckets(tcs) == buckets(bare)
    # The triangle rule, on a case pairing an LLR with an SR it does not decompose.
    skew = tcs + [_tc("TC-005", "SR-009;LLR-001", "DA-001")]
    assert TRACE.triangle_findings(skew, LLRS) == TRACE.triangle_findings(
        _stripped(skew), LLRS
    )
    assert TRACE.triangle_findings(skew, LLRS)

    def sr_rules(rows):
        orphans, _ = COHERENCE.spine_orphan_findings(
            SRS, LLRS, rows, [], {"SR-001"}, {"LLR-001"}, {"SN-001"}, set()
        )
        return [f for f in orphans if not f.startswith("TC ")]

    assert sr_rules(tcs) == sr_rules(bare)
