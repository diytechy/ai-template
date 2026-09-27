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
    # Prove the pruned meta-repo status.md passes: its named WI ids (WI-194..200
    # open, the deferred backlog) carry no `done` id, so the rule finds nothing.
    ct = load_script("check_trajectory")
    wis = ct.load_wis(ct.read_registry_rows(ROOT / "docs/requirements/work-items.csv"))[
        0
    ]
    assert ct.status_forward_only_findings(ROOT, wis) == []
