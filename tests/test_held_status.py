"""The held-rung rule's pure halves, in process: the row-text identity, the
binding's identity cell, and the approval-claim predicate.

A held-rung row's approval lands from a lane only as a CLARITY re-attestation
bound to the text its verdict judged. Two pieces of that rule need no git and
are pinned here:

  * THE ROW-TEXT IDENTITY. One digest of a row's approved text
    (`acceptance_record.approved_text_digest`), classed by the same cell split
    the amendment comparison uses, and the binding's `rows` cell that records
    it beside a verdict (`kitlib.sitting`). The digest must ignore what is not
    approved text (the id, `Status`, traced cells, an empty cell versus an
    absent one) and move for what is, or a verdict would bind the wrong thing.
  * THE CLAIM PREDICATE (`held_status.held_claims`). Which rows a tree makes an
    approval claim on against one parent: a live move into approval, or a copy
    entering, moving in its approved cells or `Status`, or retiring. The cases
    that are NOT claims (a Drafted sibling a whole-registry copy carries, a
    demotion, a below-approval move, a traced-only copy move, a released rung,
    an example row) are pinned beside one real claim, so an over-reporting
    predicate fails as surely as a silent one.

The real-git halves (the slot, the hook, the loop writers) are
`tests/test_held_status_git.py`'s.
"""

import functools
import inspect
import re

import pytest
from conftest import load_script

from kitlib import sitting as ksitting  # noqa: E402  (scripts/ is on the path)

ar = load_script("acceptance_record")
held_status = load_script("held_status")
snap = load_script("baseline_snapshot")
spine_carrier = load_script("spine_carrier")
tta = load_script("text_then_act")
integ = load_script("integrate")

SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
SR = (SR_REL, "SR-ID")
LLR = (LLR_REL, "LLR-ID")


# --- the row-text identity ----------------------------------------------------


def _sr_row(**cells):
    row = {
        "SR-ID": "SR-001",
        "Title": "Adds",
        "Requirement": "The kit shall add two numbers.",
        "Rationale": "the demo",
        "Status": "Approved",
        "Phase": "1",
        "SN-Refs": "SN-001",
    }
    row.update(cells)
    return row


def test_the_digest_ignores_the_id_status_and_traced_cells():
    digest = ar.approved_text_digest
    base = digest(SR_REL, "SR-ID", _sr_row())
    for cells in (
        {"Status": "Drafted"},
        {"SR-ID": "SR-002"},
        {"Phase": "9"},
        {"SN-Refs": "SN-002"},
    ):
        assert digest(SR_REL, "SR-ID", _sr_row(**cells)) == base, cells
    moved = digest(SR_REL, "SR-ID", _sr_row(Requirement="The kit shall add."))
    assert moved != base


_TOML_SR = (
    "[requirement.SR-001]\n"
    'title = "Adds"\n'
    'requirement = "The kit shall add two numbers."\n'
    'rationale = "the demo"\n'
    'status = "Approved"\n'
    "phase = 1\n"
)
_CSV_SR = (
    "SR-ID,Title,Requirement,Rationale,Area,Status,Phase\n"
    "SR-001,Adds,The kit shall add two numbers.,the demo,,Approved,1\n"
)


def test_the_digest_is_carrier_blind_and_empty_equals_absent():
    # The CSV twin carries an empty `Area` the TOML row does not name at all,
    # so the pair is also the empty-versus-absent case read off real carriers.
    digest = ar.approved_text_digest
    toml_row = spine_carrier.rows_from_text(_TOML_SR, "SR-ID", ".toml")["SR-001"]
    csv_row = spine_carrier.rows_from_text(_CSV_SR, "SR-ID", ".csv")["SR-001"]
    assert digest(SR_REL, "SR-ID", toml_row) == digest(SR_REL, "SR-ID", csv_row)
    row = _sr_row()
    assert digest(SR_REL, "SR-ID", dict(row, Area="")) == digest(SR_REL, "SR-ID", row)


def test_the_digest_has_the_done_when_shape():
    digest = ar.approved_text_digest
    assert re.fullmatch(r"sha256:[0-9a-f]{16}", digest(SR_REL, "SR-ID", _sr_row()))


# --- the binding's identity cell ------------------------------------------------

_IDS = {"SR-001": "sha256:0123456789abcdef", "SN-001": "sha256:fedcba9876543210"}
_BINDING = "brief = amendment\nkinds = amendment\noutcome = accepted\n"


def test_a_binding_round_trips_its_identities():
    render = ksitting.render_requested
    read = ksitting.read_identities
    text = render("amendment", ("amendment",), "accepted", identities=_IDS)
    assert read(text) == (_IDS, None)


def test_read_requested_ignores_the_identity_cell():
    # Every other reader of a binding reads brief, kinds and outcome only, so
    # the cell must neither change that answer nor appear without identities.
    render = ksitting.render_requested
    text = render("amendment", ("amendment",), "accepted", identities=_IDS)
    assert ksitting.read_requested(text) == ("amendment", ("amendment",), "accepted")
    assert render("amendment", ("amendment",), "accepted") == _BINDING


@pytest.mark.parametrize(
    "cell",
    [
        "",
        "rows = SR-001\n",
        "rows = SR-001=sha256:abc\n",
        "rows = SR-001=sha256:0123456789abcdef;SR-001=sha256:0123456789abcdef\n",
    ],
    ids=["no cell", "bad token", "short hex", "repeated id"],
)
def test_a_malformed_or_absent_identity_cell_reads_as_no_identity(cell):
    read = ksitting.read_identities
    identities, why = read(_BINDING + cell)
    assert identities is None
    assert why, cell


# --- the approval-claim predicate ---------------------------------------------


def _row(rid, status, text="the text", phase="1"):
    return {
        "SR-ID": rid,
        "Title": "t",
        "Requirement": text,
        "Status": status,
        "Phase": phase,
    }


def _rows(*rows):
    return {row[next(iter(row))]: row for row in rows}


def _held_everywhere(_registry):
    return True


@pytest.mark.parametrize(
    "before, after",
    [
        (_rows(_row("SR-001", "Drafted")), _rows(_row("SR-001", "Approved"))),
        (_rows(_row("SR-001", "Drafted")), _rows(_row("SR-001", "Founded"))),
        (_rows(), _rows(_row("SR-001", "Approved"))),
    ],
    ids=["Approved", "Founded", "born Approved"],
)
def test_a_live_flip_into_approval_is_a_claim(before, after):
    claims = held_status.held_claims
    got = claims({SR: (after, {})}, {SR: (before, {})}, _held_everywhere)
    assert got == {("SR-001", SR_REL, "SR-ID"): "a"}


_LIVE = _rows(_row("SR-001", "Approved", "new"))


@pytest.mark.parametrize(
    "before, after",
    [
        ((_LIVE, {}), (_LIVE, _LIVE)),
        (
            (_LIVE, _rows(_row("SR-001", "Approved", "old"))),
            (_LIVE, _LIVE),
        ),
        (
            (_LIVE, _rows(_row("SR-001", "Drafted", "new"))),
            (_LIVE, _LIVE),
        ),
        (
            (_LIVE, _LIVE),
            ({}, {}),
        ),
    ],
    ids=["entered", "approved cell moved", "Status moved", "retired"],
)
def test_a_copy_entry_move_or_retirement_is_a_claim(before, after):
    claims = held_status.held_claims
    got = claims({SR: after}, {SR: before}, _held_everywhere)
    assert got == {("SR-001", SR_REL, "SR-ID"): "b"}


# One real claim every not-judged case sits beside: SR-009 flips into approval.
_CLAIM_BEFORE = _row("SR-009", "Drafted")
_CLAIM_AFTER = _row("SR-009", "Approved")


def _beside_the_claim(before, after):
    """`(before, after)` sides: the SR tier carrying the real claim and the
    case's own SR rows, and the case's LLR rows in their own tier."""
    out = []
    for side, claim in ((before, _CLAIM_BEFORE), (after, _CLAIM_AFTER)):
        live, copy, llr = side
        out.append(
            {
                SR: (dict(live, **_rows(claim)), copy),
                LLR: (llr, {}),
            }
        )
    return out


_NOT_JUDGED = {
    # A whole-registry copy carries a Drafted row the lane edited.
    "Drafted sibling": (
        (
            _rows(_row("SR-002", "Drafted", "old")),
            _rows(_row("SR-002", "Drafted", "old")),
            {},
        ),
        (
            _rows(_row("SR-002", "Drafted", "new")),
            _rows(_row("SR-002", "Drafted", "new")),
            {},
        ),
    ),
    "demotion": (
        (_rows(_row("SR-002", "Approved")), _rows(_row("SR-002", "Approved")), {}),
        (_rows(_row("SR-002", "Drafted")), _rows(_row("SR-002", "Approved")), {}),
    ),
    "below-approval move": (
        (_rows(_row("SR-002", "")), {}, {}),
        (_rows(_row("SR-002", "Drafted")), {}, {}),
    ),
    "traced-only copy move": (
        (
            _rows(_row("SR-002", "Approved", phase="2")),
            _rows(_row("SR-002", "Approved", phase="1")),
            {},
        ),
        (
            _rows(_row("SR-002", "Approved", phase="2")),
            _rows(_row("SR-002", "Approved", phase="2")),
            {},
        ),
    ),
    "released rung": (
        (
            {},
            {},
            {"LLR-002": {"LLR-ID": "LLR-002", "Detail": "d", "Status": "Drafted"}},
        ),
        (
            {},
            {},
            {"LLR-002": {"LLR-ID": "LLR-002", "Detail": "d", "Status": "Approved"}},
        ),
    ),
    "-000 row": (
        (_rows(_row("SR-000", "Drafted")), {}, {}),
        (_rows(_row("SR-000", "Approved")), {}, {}),
    ),
}


@pytest.mark.parametrize("case", sorted(_NOT_JUDGED))
def test_not_judged(case):
    claims = held_status.held_claims
    before, after = _beside_the_claim(*_NOT_JUDGED[case])

    def held(registry):
        return registry != LLR_REL  # the design rung is released

    got = claims(after, before, held)
    assert got == {("SR-009", SR_REL, "SR-ID"): "a"}, case


def test_an_unmapped_registry_is_held():
    held_by = held_status.registry_held
    claims = held_status.held_claims
    unmapped = "docs/requirements/widgets.toml"
    assert held_by("DevStg-Below", unmapped) is True
    assert held_by("DevStg-Below", SR_REL) is False
    assert held_by("DevStg-Reqs", SR_REL) is True
    tier = (unmapped, "W-ID")
    before = {tier: ({"W-001": {"W-ID": "W-001", "Status": "Drafted"}}, {})}
    after = {tier: ({"W-001": {"W-ID": "W-001", "Status": "Approved"}}, {})}
    got = claims(after, before, functools.partial(held_by, "DevStg-Below"))
    assert got == {("W-001", unmapped, "W-ID"): "a"}


def test_HELD_TIERS_equals_the_snapshotted_tiers():
    assert tuple(held_status.HELD_TIERS) == tuple(snap.SNAPSHOT_TIERS)


def test_the_rule_rides_the_lane_commit_walk():
    names = [rider.__name__ for rider in tta.LANE_COMMIT_RIDERS]
    assert "commit_held_approval_lines" in names, names
    assert names.index("commit_held_approval_lines") > names.index(
        "commit_parent_first_lines"
    ), names


def test_the_slot_no_longer_runs_a_loop_lane_held_status_rung():
    # The lane rule judges every lane alike, so the loop-lane rung retires.
    assert not hasattr(integ, "_held_status_refusal")
    ladder = inspect.getsource(integ._merge_refusal)
    assert "_held_status_refusal" not in ladder


def test_the_ledger_clarity_arm_is_retired():
    # The held CLARITY exception reads the bound identity, never the ledger.
    assert not hasattr(ar, "held_reattest_refusal")
    assert "held_reattest_refusal" not in inspect.getsource(ar.merge_approval_refusal)
