"""check_trajectory's forward-only status rule over this repository itself.

Split verbatim from `tests/test_trajectory.py`, whose cases drive
`check_trajectory.py` as a subprocess and which is registered in
`tests/conftest.py`'s `SLOW_MODULES`. This one calls the rule in-process over
the live work-item folder and `docs/status.md`, so it keeps TC-075's in-memory
clause in the per-commit smoke tier, where a closed id left in the status file
is seen at the commit that leaves it.
"""

from conftest import ROOT, load_script


def test_forward_only_unit_over_the_real_meta_repo():
    """Implements: TC-075"""
    # Prove the pruned meta-repo status.md passes: its named WI ids (WI-194..200
    # open, the deferred backlog) carry no `done` id, so the rule finds nothing.
    ct = load_script("check_trajectory")
    wis = ct.load_wis(ct.read_registry_rows(ROOT / "docs/requirements/work-items.csv"))[
        0
    ]
    assert ct.status_forward_only_findings(ROOT, wis) == []


def test_an_unknown_id_and_an_absent_status_page_draw_no_finding(tmp_path):
    """Implements: TC-075"""
    # Only an id the work registry records as done is a finding: with no status
    # page the rule has nothing to read and stands down, and an id the registry
    # does not know is not a finding beside a done id that is.
    ct = load_script("check_trajectory")
    wis = [{"id": "WI-001", "status": "done"}]
    assert ct.status_forward_only_findings(tmp_path, wis) == []
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "status.md").write_text(
        "## Next action\n- WI-999 and WI-001 are both named here.\n",
        encoding="utf-8",
    )
    findings = ct.status_forward_only_findings(tmp_path, wis)
    assert len(findings) == 1 and findings[0].startswith("WI-001:")
