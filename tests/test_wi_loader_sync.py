"""WI-291 drift guard: schedule.load_wis and check_trajectory.load_wis must agree.

`schedule.py` (CMP-004, the pure decision engine) and `check_trajectory.py`
(CMP-001, the validator) each carry their OWN work-item-registry parser — a
deliberate, census-sanctioned duplication (docs/dupes-allow blocks
`d47d5975c21b` / `f800f0c60265`). The kit's F5 working agreement keeps them
separate ON PURPOSE: `schedule.py` stays stdlib-only and self-contained (no kit
import) so it ships independently copy-able, and IF-053 fixes the dependency
arrow (the validator consumes the scheduler, never the reverse), so a shared
`wi_registry.py` was NOT extracted (owner ruling 2026-07-12; WI-291).

The only real risk of two parsers is that they DRIFT — one starts handling a
row shape the other doesn't, and the scheduler's frontier silently disagrees
with the validator's graph. This test removes that risk without a shared module:
it feeds one fixture registry (with every edge case both parsers must decide the
same way) through both and asserts they produce identical SHARED decisions —
which WI ids are real, and each one's hard/soft predecessors, status, SR-refs,
title, and blockref. Fields unique to one side (schedule's priority/safetyclass;
check_trajectory's workstream/specref/integrity errors) are out of scope. A
divergence here is a real bug; re-sync the two parsers (or, if the divergence is
intended, this test is where the decision to fork them is recorded).
"""

from conftest import load_script

sched = load_script("schedule")
ctraj = load_script("check_trajectory")

# The parsing decisions BOTH modules make — the surface that must never drift.
SHARED_FIELDS = ("id", "title", "status", "preds", "soft", "srs", "blockref")


def _row(wid, **kw):
    """A raw registry row as csv.DictReader yields it (absent keys -> '')."""
    base = {
        "WI-ID": wid,
        "Title": wid,
        "Status": "queued",
        "Predecessors": "",
        "SR-Refs": "",
        "BlockRef": "",
        # columns only one side reads — present so neither KeyErrors:
        "Workstream": "",
        "Priority": "",
        "Exclusive": "",
        "EstTokens": "",
        "SafetyClass": "ordinary",
        "PlanMode": "",
        "Deliverable": "",
        "SpecRef": "",
    }
    base.update(kw)
    return base


# One fixture registry exercising every decision both parsers share: the -000
# example skip, a malformed id, a duplicate id, hard + soft (~) predecessors,
# the six statuses, multi-ref SR cells, and a blockref.
FIXTURE_ROWS = [
    _row("WI-001", Status="done", Title="root"),
    _row(
        "WI-002", Status="queued", Predecessors="WI-001", **{"SR-Refs": "SR-001;SR-002"}
    ),
    _row("WI-003", Status="blocked", Predecessors="WI-002;~WI-001", BlockRef="SR-009"),
    _row("WI-004", Status="deferred"),
    _row("WI-005", Status="retired"),
    _row("WI-006", Status="active", Predecessors="~WI-002"),
    _row("WI-000", Status="queued", Title="inert example row (must be skipped)"),
    _row("WI-abc", Status="queued", Title="malformed id (must be skipped)"),
    _row("WI-002", Status="done", Title="duplicate id (second occurrence skipped)"),
    _row("", Title="blank / non-WI row"),
]


def _shared(wi):
    return {k: wi.get(k) for k in SHARED_FIELDS}


def test_load_wis_shared_decisions_match():
    sched_wis = sched.load_wis(FIXTURE_ROWS)
    ctraj_wis, _integrity = ctraj.load_wis(FIXTURE_ROWS)

    # Same real WIs, in the same row order (both iterate the registry in order).
    assert [w["id"] for w in sched_wis] == [w["id"] for w in ctraj_wis]

    # Same shared parsing decision for each — a mismatch is drift.
    assert [_shared(w) for w in sched_wis] == [_shared(w) for w in ctraj_wis]


def test_both_skip_example_malformed_and_duplicate_ids():
    ids = [w["id"] for w in sched.load_wis(FIXTURE_ROWS)]
    ct_ids = [w["id"] for w in ctraj.load_wis(FIXTURE_ROWS)[0]]
    # The inert -000 row, the malformed id, and the blank row never become WIs;
    # a duplicate id appears exactly once. Both parsers must agree on all four.
    for produced in (ids, ct_ids):
        assert "WI-000" not in produced
        assert "WI-abc" not in produced
        assert produced.count("WI-002") == 1
        assert produced == ["WI-001", "WI-002", "WI-003", "WI-004", "WI-005", "WI-006"]


def test_hard_and_soft_predecessor_split_agrees():
    sched_by = {w["id"]: w for w in sched.load_wis(FIXTURE_ROWS)}
    ctraj_by = {w["id"]: w for w in ctraj.load_wis(FIXTURE_ROWS)[0]}
    # WI-003: hard WI-002 + soft ~WI-001 — both must split identically.
    for by in (sched_by, ctraj_by):
        assert by["WI-003"]["preds"] == ["WI-002"]
        assert by["WI-003"]["soft"] == ["WI-001"]
        assert by["WI-006"]["preds"] == []
        assert by["WI-006"]["soft"] == ["WI-002"]
