"""baseline_snapshot.py — the four drift corners, read over a copied tree.

Split verbatim from `tests/test_baseline_snapshot.py`, which is registered in
`tests/conftest.py`'s `SLOW_MODULES`. These four copy this repository's real
registries into a tmp tree, seed a snapshot and compare rows in-process, with
no git and no subprocess, so they keep TC-153's four corners in the per-commit
smoke tier: an approved cell moving under an approved row is drift, a traced
cell moving is not, the status marker is never the amendment, and a row below
approval has no claim to fall from. The premise that needs a real two-commit
repository stays in the slow module.
"""

from baseline_snapshot_fixtures import SR_REL, _first_row_at, _rewrite, _seeded, _tree
from conftest import load_script

SNAP = load_script("baseline_snapshot")
CT = load_script("check_trajectory")


def test_a_approved_cell_moving_under_an_approved_row_is_DRIFT(tmp_path):
    root = _seeded(tmp_path)
    sid, _row = _first_row_at(root, "approved")
    snapshot = SNAP.load_all(root)
    before = SNAP.rows_for(snapshot, SR_REL, "SR-ID")
    live = {
        r["SR-ID"]: r for r in load_script("spine_carrier").load(root / SR_REL, "SR-ID")
    }
    # Green first: a freshly copied tree has drifted nowhere. Without this the
    # assertion below could pass on a comparison that always says "changed".
    assert not SNAP.is_drifted(SR_REL, "SR-ID", live[sid], before)
    _rewrite(root, SR_REL, live[sid]["Title"], live[sid]["Title"] + " (amended)")
    live2 = {
        r["SR-ID"]: r for r in load_script("spine_carrier").load(root / SR_REL, "SR-ID")
    }
    assert SNAP.is_drifted(SR_REL, "SR-ID", live2[sid], before)
    assert set(SNAP.drifted_cells(SR_REL, "SR-ID", live2[sid], before)) == {"Title"}


def test_a_TRACED_cell_moving_is_NOT_drift(tmp_path):
    # The WI-388 ruling, unchanged by the new baseline: re-pointing what a
    # requirement answers to routes to ADJUDICATION and never arms a re-attest
    # window. If this ever flips, the re-tier campaign arms a window on every
    # row it touches, which is the noise that gets a window ignored.
    root = _seeded(tmp_path)
    snapshot = SNAP.load_all(root)
    before = SNAP.rows_for(snapshot, SR_REL, "SR-ID")
    sid, row = _first_row_at(root, "approved")
    moved = dict(row, Phase="99")  # `Phase` is declared TRACED for the SR tier
    assert CT.spine_cell_class(SR_REL, "Phase") == "traced"
    assert not SNAP.is_drifted(SR_REL, "SR-ID", moved, before)


def test_a_row_below_approval_can_never_be_drifted(tmp_path):
    # It has made no claim to fall from. A Drafted row differing from its snapshot
    # copy is work in progress, not a broken attestation. The live registries
    # carry no Drafted row since the 2026-08-20 signing, so the fixture makes
    # its own (first SR flipped pre-seed) rather than borrowing one.
    root = _tree(tmp_path)
    _rewrite(root, SR_REL, 'status = "Approved"', 'status = "Drafted"')
    SNAP.copy_live(root, seed=True)
    snapshot = SNAP.load_all(root)
    before = SNAP.rows_for(snapshot, SR_REL, "SR-ID")
    sid, row = _first_row_at(root, "drafted")
    amended = dict(row, Title=(row.get("Title") or "") + " (amended)")
    assert amended["Title"] != before[sid].get("Title")
    assert not SNAP.is_drifted(SR_REL, "SR-ID", amended, before)


def test_status_itself_is_never_the_amendment(tmp_path):
    # `Status` is the MARKER, not the content: folding it into the comparison
    # would make every flip look like an amendment and every real amendment
    # invisible behind its own flip.
    root = _seeded(tmp_path)
    before = SNAP.rows_for(SNAP.load_all(root), SR_REL, "SR-ID")
    sid, row = _first_row_at(root, "approved")
    assert not SNAP.is_drifted(SR_REL, "SR-ID", dict(row, Status="Approved"), before)
