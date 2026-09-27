"""trunk_step.py's regen plan, read off a run where every family skips.

A tree that carries none of the generated surfaces makes `regen` walk its whole
step table, print a skip notice per family and run no generator at all, so the
declared order and the skip notice are observable with no git repository and no
subprocess. These two cases were split out of `test_trunk_step.py`, whose other
cases need a real git history or a real generator run and are registered in
`tests/conftest.py`'s `SLOW_MODULES`; they keep the trunk step's step table in
the per-commit smoke tier.
"""

from conftest import load_script

ts = load_script("trunk_step")


def test_regen_skips_absent_artifact_families(tmp_path, capsys):
    # A repo that carries none of the generated surfaces pays nothing — and the
    # skip is PRINTED, so "nothing regenerated" is never mistaken for "all fresh".
    assert ts.regen(tmp_path) == 0
    out = capsys.readouterr().out
    for name in (
        "okf",
        "derived-stage",
        "trajectory",
        "status",
        "open-items",
    ):
        assert "skipping {}".format(name) in out


def test_regen_runs_in_declared_dependency_order(tmp_path, capsys):
    # SR-173: a producer runs before every consumer that reads it — okf first
    # (the dashboard's Knowledge tab reads the BUNDLE), derived-stage before
    # trajectory and status (both read docs/stage), open-items last (nothing
    # reads it back). Asserted on the EXECUTED surface (the printed per-step
    # lines of a real run), not on the REGEN_STEPS table, so a reorder of the
    # table shows up here even though every family skips.
    #
    # `arch-map` LED this list until WI-455 retired it: the module map derives
    # live from the source AST, so there is no committed block to regenerate
    # and no producer edge into okf left to assert.
    assert ts.regen(tmp_path) == 0
    out = capsys.readouterr().out
    pos = [
        out.index("skipping {}".format(name))
        for name in (
            "okf",
            "derived-stage",
            "trajectory",
            "status",
            "open-items",
        )
    ]
    assert pos == sorted(pos), "regen must execute in declared dependency order"
