"""trunk_step.py's regen plan, read off a run where every family skips.

A tree that carries none of the generated surfaces makes `regen` walk its whole
step table, print a skip notice per family and run no generator at all, so the
declared order and the skip notice are observable with no git repository and no
subprocess. These two cases were split out of `test_trunk_step.py`, whose other
cases need a real git history or a real generator run and are registered in
`tests/conftest.py`'s `SLOW_MODULES`; they keep the trunk step's step table in
the per-commit smoke tier.

Both arms read `REGEN_STEPS` WHOLE rather than a hand-written sample of names.
A sample leaves every step added after it unobserved by default: the
`verdict-rollup` row's printed skip went unasserted that way while its design
row claimed it. Reading the table makes a new row covered by both arms with no
edit here.
"""

import re

from conftest import load_script

ts = load_script("trunk_step")

# One executed per-step line: the skip notice (with the reason the table names)
# or the success line. Both carry the step's name, which is what the order arm
# reads; the skip arm reads the whole line.
_STEP_LINE = re.compile(
    r"^trunk_step: regen — (?:skipping (?P<skipped>\S+) \(|(?P<ran>\S+) ok\.$)"
)


def _executed_steps(out):
    """The step names in the order the run printed them."""
    names = []
    for line in out.splitlines():
        m = _STEP_LINE.match(line)
        if m:
            names.append(m.group("skipped") or m.group("ran"))
    return names


def _declared_steps():
    return [name for name, *_rest in ts.REGEN_STEPS]


def test_regen_skips_absent_artifact_families(tmp_path, capsys):
    # A repo that carries none of the generated surfaces pays nothing — and the
    # skip is PRINTED, so "nothing regenerated" is never mistaken for "all fresh".
    # Every row prints either its `ok` line or its skip with the reason the
    # table names; on this empty tree none applies, so each one is a skip.
    assert ts.regen(tmp_path) == 0
    lines = capsys.readouterr().out.splitlines()
    for name, _applies, _argv, why, _writes in ts.REGEN_STEPS:
        skip = "trunk_step: regen — skipping {} ({}).".format(name, why)
        ok = "trunk_step: regen — {} ok.".format(name)
        assert skip in lines or ok in lines, name
    # LLR-208's claim about the rollup's step, named so its loss is a red here
    # even though the table read above would silently shrink with it.
    assert (
        "trunk_step: regen — skipping verdict-rollup (docs/reviews/ absent)." in lines
    )


def test_regen_runs_in_declared_dependency_order(tmp_path, capsys):
    # The EXECUTED order (the printed per-step lines of a real run) is the
    # DECLARED order, across every row: one line per row, none missing, none
    # extra, none reordered.
    assert ts.regen(tmp_path) == 0
    executed = _executed_steps(capsys.readouterr().out)
    assert executed == _declared_steps(), "regen must execute in declared order"
    # SR-173: a producer runs before every consumer that reads it — okf first
    # (the dashboard's Knowledge tab reads the BUNDLE), derived-stage before
    # trajectory and status (both read docs/stage). These edges are the
    # declared order's reason, so a reorder of the table that breaks one is a
    # red here even though the executed order would still match the table.
    for producer, consumer in (
        ("okf", "trajectory"),
        ("derived-stage", "trajectory"),
        ("derived-stage", "status"),
    ):
        assert executed.index(producer) < executed.index(consumer), (producer, consumer)


def test_a_row_added_to_the_table_is_covered_by_both_arms(
    tmp_path, capsys, monkeypatch
):
    # The arms' readers are the table, so a new row needs no edit here: append
    # one and the executed-order reader sees it in place, with its skip line.
    extra = ("new-family", lambda root: False, None, "nothing to read", ())
    monkeypatch.setattr(ts, "REGEN_STEPS", (*ts.REGEN_STEPS, extra))
    assert ts.regen(tmp_path) == 0
    out = capsys.readouterr().out
    assert _executed_steps(out) == _declared_steps()
    assert _executed_steps(out)[-1] == "new-family"
    assert "trunk_step: regen — skipping new-family (nothing to read)." in out
