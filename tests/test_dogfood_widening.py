"""The WI-242 schema widening is behaviour-neutral: a one-time regression.

Split out of `test_dogfood_sync.py`, whose structural drift checks stay in the
per-commit smoke tier. This case reads every live work item and runs four
registry consumers over two renderings of them, which made it the costliest
test in that module; it guards a migration that has already landed, so it is
registered in `tests/conftest.py`'s `SLOW_MODULES` and runs at slice/phase
close and in CI.
"""

import csv
import io

from conftest import ROOT, load_script
from test_dogfood_sync import TEMPLATE_DIR, _header

_OLD_HEADER = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "BuildTier",
    "SafetyClass",
]


def _write_registry(root, text):
    d = root / "docs" / "requirements"
    d.mkdir(parents=True, exist_ok=True)
    (d / "work-items.csv").write_bytes(text.encode("utf-8"))


def _render(rows, header):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    for r in rows:
        w.writerow([(r.get(c) or "") for c in header])
    return buf.getvalue()


def _consumer_signature(root):
    """Every registry consumer's output over the work-items.csv at ``root``,
    as one comparable tuple: schedule classification/disposition, the
    check_trajectory SSOT findings, the critique dials, and the plan modes.

    Phase 5 note: ``critique_control`` takes a repo root and now reads only the
    ``docs/work/`` home, so over these CSV-only scratch roots it returns the
    default and contributes a CONSTANT. The width-neutrality claim rests on the
    three row-dict consumers; the dial stays in the tuple so a consumer that
    starts disagreeing across widths is still caught wherever it reads from."""
    schedule = load_script("schedule")
    ct = load_script("check_trajectory")
    al = load_script("agent_loop")
    pr = load_script("plan_runner")
    reg = root / "docs" / "requirements" / "work-items.csv"

    with reg.open(encoding="utf-8-sig", newline="") as fh:
        srows = list(csv.DictReader(fh))
    sched = tuple(
        # Both classifier axes (WI-383): a width change must move neither the
        # concurrency answer nor the rank, and reading only one would miss half.
        (
            rec["id"],
            rec["disposition"],
            rec["concurrency"],
            rec["rank"],
            rec["priority"],
        )
        for rec in schedule.evaluate(schedule.load_wis(srows))
    )
    rows = ct.read_rows(reg)
    wis, integ = ct.load_wis(rows)
    ssot = tuple(sorted(ct.ssot_findings(wis, root)))
    crit = al.critique_control(root / "docs", {"WI-201", "WI-238", "WI-242"}, 3)
    modes = tuple(sorted({pr.wi_plan_mode(r) for r in rows}))
    return (sched, ssot, crit, modes, len(integ))


def test_schema_widening_is_behavior_neutral(tmp_path):
    """An empty new cell == the absent column, for every consumer: build a
    legacy 10-column shape and the migrated 17-column shape from the SAME live
    rows and assert identical consumer output. Directly proves the WI-242
    migration is behaviour-neutral, and would catch any consumer that started
    reading a new column positionally.

    The optional cells are CLEARED in both shapes before comparing: that is
    the guarantee under test (an *empty* new cell), and a live row may now
    legitimately use one — WI-275's ``Priority=1`` (2026-07-23) was the
    column's first use, and a deliberate priority is *supposed* to change the
    schedule. A consumer reading a new column positionally still corrupts the
    core ten and fails here regardless of cell content."""
    # The live rows come from the registry's one home, the docs/work/ folder
    # (Phase 5: the CSV home retired), read through the validator's own loader —
    # which derives that folder from the CSV path it is still handed.
    ct_live = load_script("check_trajectory")
    live_rows = ct_live.read_registry_rows(ROOT / "docs/requirements/work-items.csv")
    wide_header = _header(TEMPLATE_DIR / "work-items.template.csv")
    optional = [c for c in wide_header if c not in _OLD_HEADER]
    rows = [
        {**{c: (r.get(c) or "") for c in wide_header}, **{c: "" for c in optional}}
        for r in live_rows
    ]

    legacy_root = tmp_path / "legacy"
    wide_root = tmp_path / "wide"
    _write_registry(legacy_root, _render(rows, _OLD_HEADER))
    _write_registry(wide_root, _render(rows, wide_header))

    assert _consumer_signature(legacy_root) == _consumer_signature(wide_root)
