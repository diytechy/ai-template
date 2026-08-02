"""WI-291 drift guard: the kit's work-item registry parsers must agree.

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

**Phase 2b widened this guard twice** (docs/concurrency-restructure.md §7):

  * a THIRD copy of the registry reader now lives in `agent_common.py` — the
    spec-folder reader (`docs/work/<status>/WI-###-<slug>.md`) is duplicated
    verbatim into all three scripts on the same F5 grounds, so all three must
    read one folder into byte-identical rows;
  * the registry has TWO REPRESENTATIONS, and the guard that matters is that
    they are the same registry. The fixture below is built ONCE and materialized
    into a spec folder by `scripts/wi_convert.py`, then both representations are
    pushed through both `load_wis`. All four outputs must agree — which is the
    representation-equivalence proof and the drift guard in one object, because
    the failure they share is "one reader decided something the others did not".

**Phase 5 retired the CSV HOME** (RULING-4): `docs/work/` is the registry, and
the CSV survives only as `wi_convert.py`'s legacy interchange format. The CSV
halves below therefore no longer pin a dual-read — they pin CONVERTER FIDELITY,
which is the same assertion aimed at the same defect (a cell that means one thing
in one form and another in the other), so they are kept rather than retired.

Both new guards are mutation-proven at the bottom of the file: a single corrupted
spec cell must red the equivalence, and a reader that skips a file must red the
three-way comparison. A guard nobody has seen fail is not a guard (WI-293).
"""

import csv

import pytest
from conftest import load_script

sched = load_script("schedule")
ctraj = load_script("check_trajectory")
acommon = load_script("agent_common")
# Phase 2c-i moved the converter into the kit, so the bespoke tools/ importer
# this module carried is gone — it loads like the three readers it feeds.
wi_convert = load_script("wi_convert")

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
        "Bar": "",
        "Deliverable": "",
        "SpecRef": "",
    }
    base.update(kw)
    return base


# One fixture registry exercising every decision both parsers share: the -000
# example skip, a malformed id, a duplicate id, hard + soft (~) predecessors,
# the seven statuses, multi-ref SR cells, and a blockref.
FIXTURE_ROWS = [
    _row("WI-001", Status="done", Title="root"),
    _row(
        "WI-002", Status="queued", Predecessors="WI-001", **{"SR-Refs": "SR-001;SR-002"}
    ),
    _row("WI-003", Status="blocked", Predecessors="WI-002;~WI-001", BlockRef="SR-009"),
    _row("WI-004", Status="deferred"),
    _row("WI-005", Status="cancelled"),
    _row("WI-006", Status="active", Predecessors="~WI-002"),
    _row("WI-007", Status="draft"),
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
        assert produced == [
            "WI-001",
            "WI-002",
            "WI-003",
            "WI-004",
            "WI-005",
            "WI-006",
            "WI-007",
        ]


def test_hard_and_soft_predecessor_split_agrees():
    sched_by = {w["id"]: w for w in sched.load_wis(FIXTURE_ROWS)}
    ctraj_by = {w["id"]: w for w in ctraj.load_wis(FIXTURE_ROWS)[0]}
    # WI-003: hard WI-002 + soft ~WI-001 — both must split identically.
    for by in (sched_by, ctraj_by):
        assert by["WI-003"]["preds"] == ["WI-002"]
        assert by["WI-003"]["soft"] == ["WI-001"]
        assert by["WI-006"]["preds"] == []
        assert by["WI-006"]["soft"] == ["WI-002"]


# --- Phase 2b: one registry, two representations, three readers ---------------
# The spec form cannot carry every row shape above — `wi_convert` REFUSES a
# status outside draft/queued/deferred/done/cancelled (a classifier that cannot
# finish is louder than a catch-all), and a duplicate id or a blank WI-ID has no
# filename. Those stay CSV-only concerns, exercised above. This fixture is the
# part of the registry both homes can express, and it deliberately keeps the
# cells most likely to be lost in translation: the `~` soft prefix, a multi-id SR
# cell, an int-valued Priority, a cancelled row (its own directory since WI-384,
# with no attribute left to carry), the inert -000 example row, and a Deliverable
# carrying the punctuation an escaper breaks on.
CONVERTIBLE_ROWS = [
    {
        "WI-ID": "WI-001",
        "Title": "root",
        "Workstream": "scripts",
        "SR-Refs": "SR-001;SR-002",
        "Predecessors": "",
        "Status": "done",
        "Deliverable": 'shipped: "quoted", back\\slash, and a #hash',
        "SpecRef": "",
        "BuildTier": "medium",
        "CritiqueBudget": "",
        "CritiqueExhaustion": "",
        "Priority": "2",
        "Exclusive": "",
        "BlockRef": "",
        "EstTokens": "1200",
        "SafetyClass": "ordinary",
        "PlanMode": "",
        "Bar": "",
    },
    {
        "WI-ID": "WI-002",
        "Title": "hard + soft predecessors",
        "Workstream": "scripts",
        "SR-Refs": "SR-002",
        "Predecessors": "WI-001;~WI-005",
        "Status": "queued",
        "Deliverable": "",
        "SpecRef": "docs/specs/WI-002.md",
        "BuildTier": "",
        "CritiqueBudget": "1",
        "CritiqueExhaustion": "",
        "Priority": "1",
        "Exclusive": "docs/status.md",
        "BlockRef": "SR-009",
        "EstTokens": "",
        "SafetyClass": "spine",
        "PlanMode": "dual",
        # The WI-388 strictness key, carried where the cells most likely to be
        # lost in translation live: bar declares verification strictness for
        # this row's lane; it never affects scheduling.
        "Bar": "G2",
    },
    {
        "WI-ID": "WI-003",
        "Title": "parked with a reason",
        "Workstream": "docs",
        "SR-Refs": "",
        "Predecessors": "",
        "Status": "deferred",
        "Deliverable": "",
        "SpecRef": "docs/specs/WI-003.md",
        "BuildTier": "",
        "CritiqueBudget": "",
        "CritiqueExhaustion": "",
        "Priority": "0",
        "Exclusive": "",
        "BlockRef": "",
        "EstTokens": "",
        "SafetyClass": "",
        "PlanMode": "",
        "Bar": "",
    },
    {
        "WI-ID": "WI-005",
        "Title": "won't build",
        "Workstream": "scripts",
        "SR-Refs": "SR-003",
        "Predecessors": "",
        "Status": "cancelled",
        "Deliverable": "cancelled: superseded by WI-001",
        "SpecRef": "",
        "BuildTier": "",
        "CritiqueBudget": "",
        "CritiqueExhaustion": "",
        "Priority": "",
        "Exclusive": "",
        "BlockRef": "",
        "EstTokens": "",
        "SafetyClass": "ordinary",
        "PlanMode": "",
        "Bar": "",
    },
    {
        "WI-ID": "WI-000",
        "Title": "inert example row (must be skipped)",
        "Workstream": "",
        "SR-Refs": "",
        "Predecessors": "",
        "Status": "queued",
        "Deliverable": "",
        "SpecRef": "",
        "BuildTier": "",
        "CritiqueBudget": "",
        "CritiqueExhaustion": "",
        "Priority": "",
        "Exclusive": "",
        "BlockRef": "",
        "EstTokens": "",
        "SafetyClass": "",
        "PlanMode": "",
        "Bar": "",
    },
]

# Every reader that must agree. The name each module gives the folder reader is
# the same on purpose — three verbatim copies, so a rename in one is drift too.
SPEC_READERS = (
    ("schedule", sched),
    ("check_trajectory", ctraj),
    ("agent_common", acommon),
)


@pytest.fixture(scope="module")
def both_homes(tmp_path_factory):
    """`(csv_rows, work_dir)` — one fixture registry in BOTH representations, the
    folder materialized from the CSV by the converter that defines the format."""
    tmp = tmp_path_factory.mktemp("both-homes")
    csv_path = tmp / "docs" / "requirements" / "work-items.csv"
    csv_path.parent.mkdir(parents=True)
    # newline="" is the csv module's contract and lineterminator pins LF, so the
    # fixture cannot inherit the platform it is meant to be independent of.
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(wi_convert.COLUMNS)
        for row in CONVERTIBLE_ROWS:
            writer.writerow([row[column] for column in wi_convert.COLUMNS])
    wi_convert.to_specs(csv_path, tmp / "docs" / "work")
    return csv_path, tmp / "docs" / "work"


def _reader_disagreements(named_rows):
    """Findings for a `[(name, rows)]` list whose entries must all be equal —
    the three-way comparison, exposed so its own mutation proof can drive it."""
    reference_name, reference = named_rows[0]
    return [
        "{} disagrees with {}".format(name, reference_name)
        for name, rows in named_rows[1:]
        if rows != reference
    ]


def test_the_three_folder_readers_read_one_folder_identically(both_homes):
    """The F5 copies are copies. Any behavioural difference between them — a
    field parsed, a file skipped, an order chosen — shows up here as unequal
    rows, which is the whole reason the duplication is allowed to exist."""
    _csv_path, work_dir = both_homes
    named_rows = [(name, mod.read_spec_rows(work_dir)) for name, mod in SPEC_READERS]
    assert named_rows[0][1], "the fixture folder produced no rows — guard vacuous"
    assert _reader_disagreements(named_rows) == []


def test_the_two_representations_are_the_same_registry(both_homes):
    """Cell-exact equivalence at the ROW level — the level the CONVERSION happens
    at, so everything above it is untouched by which form a registry arrived in."""
    csv_path, work_dir = both_homes
    csv_rows = sched.load_rows(csv_path)
    folder_rows = sched.read_spec_rows(work_dir)
    assert _cell_diff(csv_rows, folder_rows) == []


def test_the_bar_key_is_carried_by_every_reader(both_homes):
    """The WI-388 `bar` column crosses both representations and all three F5
    readers together (the loader tables gain the column as one edit): bar
    declares verification strictness for this row's lane; it never affects
    scheduling — so the scheduler's own load_wis deliberately does NOT parse
    it into the decision dicts."""
    csv_path, work_dir = both_homes
    for rows in (sched.load_rows(csv_path),) + tuple(
        mod.read_spec_rows(work_dir) for _name, mod in SPEC_READERS
    ):
        by_id = {r["WI-ID"]: r for r in rows}
        assert by_id["WI-002"]["Bar"] == "G2"
        assert by_id["WI-001"]["Bar"] == ""
    # Never a scheduling input: the WI dicts the frontier is computed from
    # carry no bar key at all — structurally, not by convention.
    for wi in sched.load_wis(sched.read_spec_rows(work_dir)):
        assert "bar" not in wi


def test_a_context_section_is_read_past_by_all_three_readers(tmp_path):
    """The WI-388 `## Context` body section (advisory registry joins, written
    at mint) is body furniture the loaders read PAST: the Deliverable cell
    stays exactly what the `## Deliverable` section holds, whether the Context
    block leads the body (an open minted row) or follows the Deliverable (a
    closed one)."""
    work = tmp_path / "docs" / "work"
    (work / "queued").mkdir(parents=True)
    (work / "complete").mkdir(parents=True)
    (work / "queued" / "WI-011-minted.md").write_text(
        '+++\nid = "WI-011"\ntitle = "minted"\n+++\n'
        "\n## Context\n\n- precedent: WI-009 (cancelled) shared SR-001\n",
        encoding="utf-8",
        newline="\n",
    )
    (work / "complete" / "WI-012-closed.md").write_text(
        '+++\nid = "WI-012"\ntitle = "closed"\n+++\n'
        "\n## Deliverable\n\nshipped the thing\n"
        "\n## Context\n\n- advisory joins, kept for the record\n",
        encoding="utf-8",
        newline="\n",
    )
    for name, mod in SPEC_READERS:
        rows = {r["WI-ID"]: r for r in mod.read_spec_rows(work)}
        assert set(rows) == {"WI-011", "WI-012"}, name
        assert rows["WI-011"]["Deliverable"] == "", name
        assert rows["WI-012"]["Deliverable"] == "shipped the thing", name


def _cell_diff(csv_rows, folder_rows):
    """Every differing cell between two row lists, as `id/column` strings."""
    findings = []
    if len(csv_rows) != len(folder_rows):
        findings.append("row count {} != {}".format(len(csv_rows), len(folder_rows)))
    for lhs, rhs in zip(csv_rows, folder_rows):
        for column in wi_convert.COLUMNS:
            if (lhs.get(column) or "") != (rhs.get(column) or ""):
                findings.append("{}/{}".format(lhs.get("WI-ID"), column))
    return findings


def test_all_four_loader_outputs_agree_on_the_shared_decisions(both_homes):
    """The four-way proof: {schedule, check_trajectory} x {CSV, folder}."""
    csv_path, work_dir = both_homes
    csv_rows = sched.load_rows(csv_path)
    folder_rows = sched.read_spec_rows(work_dir)
    outputs = {
        "schedule/csv": sched.load_wis(csv_rows),
        "schedule/folder": sched.load_wis(folder_rows),
        "check_trajectory/csv": ctraj.load_wis(csv_rows)[0],
        "check_trajectory/folder": ctraj.load_wis(folder_rows)[0],
    }
    reference = [_shared(w) for w in outputs["schedule/csv"]]
    assert [w["id"] for w in outputs["schedule/csv"]] == [
        "WI-001",
        "WI-002",
        "WI-003",
        "WI-005",
    ], "fixture premise gone (the -000 row must be skipped by every reader)"
    for name, wis in outputs.items():
        assert [_shared(w) for w in wis] == reference, name


def test_the_soft_prefix_survives_the_round_trip_into_load_wis(both_homes):
    """`~WI-005` is MEANING, not decoration: it is what makes an edge advisory.
    The converter joins `needs` with ';' and keeps the `~` verbatim, and the
    folder reader must hand `load_wis` a cell it splits the same way."""
    _csv_path, work_dir = both_homes
    for _name, mod in SPEC_READERS:
        by_id = {r["WI-ID"]: r for r in mod.read_spec_rows(work_dir)}
        assert by_id["WI-002"]["Predecessors"] == "WI-001;~WI-005"
    folder = {w["id"]: w for w in sched.load_wis(sched.read_spec_rows(work_dir))}
    assert folder["WI-002"]["preds"] == ["WI-001"]
    assert folder["WI-002"]["soft"] == ["WI-005"]


# --- mutation proofs: each new guard must fail on the defect it is for --------


def test_mutation_one_corrupted_spec_cell_reds_the_equivalence(both_homes, tmp_path):
    """Drive the failure shape rather than trusting the green: retype ONE
    frontmatter value in the folder and the cell-exact compare must name it."""
    csv_path, work_dir = both_homes
    victim = next(p for p in work_dir.rglob("WI-002-*.md"))
    broken = tmp_path / "work"
    _copy_tree(work_dir, broken)
    target = next(p for p in broken.rglob("WI-002-*.md"))
    text = target.read_text(encoding="utf-8")
    assert 'needs = ["WI-001", "~WI-005"]' in text, victim
    target.write_text(
        text.replace('needs = ["WI-001", "~WI-005"]', 'needs = ["WI-001", "WI-005"]'),
        encoding="utf-8",
        newline="\n",
    )
    findings = _cell_diff(sched.load_rows(csv_path), sched.read_spec_rows(broken))
    assert "WI-002/Predecessors" in findings, findings


def test_mutation_a_reader_that_drops_a_file_reds_the_three_way_check(both_homes):
    """The three-way comparison's own failure mode, constructed: stand in a
    reader that silently skipped one spec and the comparison must name it."""
    _csv_path, work_dir = both_homes
    full = sched.read_spec_rows(work_dir)
    partial = [row for row in full if row["WI-ID"] != "WI-003"]
    assert partial != full, "the fixture has no WI-003 — this proof is vacuous"
    findings = _reader_disagreements(
        [("schedule", full), ("check_trajectory", full), ("agent_common", partial)]
    )
    assert findings == ["agent_common disagrees with schedule"], findings


def _copy_tree(src, dest):
    for path in src.rglob("*.md"):
        target = dest / path.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            path.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
        )
