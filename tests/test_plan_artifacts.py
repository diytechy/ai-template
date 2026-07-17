"""plan_artifacts.py — the dual-plan round artifact filer (WI-198).

Exercises the coordinator's write-side of a round: DP-NNN directory allocation,
stage-artifact writes, filing the selected plan's rows as queued WIs (id
allocation, predecessor mapping incl. the fan-in row, tier map, R-A: queued
rows carry an empty Deliverable), the end-to-end `check_trajectory.py`-passes
fixture, and the log append. Every test builds its scaffolding under `tmp_path`
— the real `docs/` is never written.
"""

import csv

from conftest import SCRIPTS, load_script, run_py

pa = load_script("plan_artifacts")

# A minimal selected plan carrying a fan-in row (P3 depends on P1 AND P2) — the
# same commensurability table plan_coverage parses.
PLAN_TEXT = """# Selected plan (rev)

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | First slice | C1 | IF-001 | |
| P2 | Second slice | C2 | Proposed: nearest IF-002, wrong module | P1 |
| P3 | Fan-in slice | C3 | intra-module | P1;P2 |

## Notes

- No clause excluded.
"""

WI_HEADER_LINE = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SpecRef,BuildTier\n"
)


def _wi_csv(root):
    return root / "docs" / "requirements" / "work-items.csv"


def _write_registry(root, rows):
    """Write a minimal LF work-items.csv (header + `rows`, each a raw CSV line).

    ``newline=""`` writes the ``\\n`` bytes verbatim (no Windows translation), so
    the fixture genuinely holds LF — the convention the append must preserve."""
    path = _wi_csv(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(WI_HEADER_LINE + "".join(rows))
    return path


def _rows(root):
    with _wi_csv(root).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# --- directory allocation -----------------------------------------------------


def test_allocate_first_round_is_dp001(tmp_path):
    d = pa.allocate_round_dir(tmp_path, "my-slug")
    assert d.name == "DP-001-my-slug"
    assert d.is_dir()


def test_allocate_next_round_increments(tmp_path):
    (tmp_path / "docs" / "plans" / "DP-001-existing").mkdir(parents=True)
    d = pa.allocate_round_dir(tmp_path, "second")
    assert d.name == "DP-002-second"
    assert d.is_dir()


def test_allocate_skips_the_gap_from_the_max(tmp_path):
    plans = tmp_path / "docs" / "plans"
    (plans / "DP-001-a").mkdir(parents=True)
    (plans / "DP-004-b").mkdir()
    d = pa.allocate_round_dir(tmp_path, "c")
    assert d.name == "DP-005-c"  # max + 1, not a gap-fill


# --- stage writes -------------------------------------------------------------


def test_write_stage_writes_named_utf8_files(tmp_path):
    d = pa.allocate_round_dir(tmp_path, "r")
    p = pa.write_stage(d, "verdict.md", "# Verdict — select plan B — em dash ✓\n")
    assert p == d / "verdict.md"
    assert p.read_text(encoding="utf-8").startswith("# Verdict")
    assert "✓" in p.read_text(encoding="utf-8")


def test_write_stage_creates_dir_if_missing(tmp_path):
    target = tmp_path / "docs" / "plans" / "DP-009-x"
    p = pa.write_stage(target, "goal.md", "# Goal\n")
    assert p.read_text(encoding="utf-8") == "# Goal\n"


# --- filing selected WIs ------------------------------------------------------


def _seed_registry(root):
    """A registry with the inert example row + a done parent WI (WI-010)."""
    return _write_registry(
        root,
        [
            "WI-000,Example row,other,,,queued,,,\n",
            "WI-001,Foundation,docs,,,done,shipped it,,\n",
            "WI-010,Round parent,unattended,,,done,parent shipped,,\n",
        ],
    )


def test_file_selected_wis_allocates_sequential_ids(tmp_path):
    _seed_registry(tmp_path)
    mapping = pa.file_selected_wis(
        tmp_path,
        PLAN_TEXT,
        spec_ref="docs/plans/DP-001-x/plan.md",
        workstream="unattended",
        predecessor_wi="WI-010",
    )
    # max existing real id = 10 -> the slice starts at 11.
    assert mapping == {"P1": "WI-011", "P2": "WI-012", "P3": "WI-013"}


def test_file_selected_wis_maps_predecessors_incl_fan_in(tmp_path):
    _seed_registry(tmp_path)
    pa.file_selected_wis(
        tmp_path,
        PLAN_TEXT,
        spec_ref="docs/plans/DP-001-x/plan.md",
        workstream="unattended",
        predecessor_wi="WI-010",
    )
    by_id = {r["WI-ID"]: r for r in _rows(tmp_path)}
    # P1 has no plan-local edge -> only the round parent.
    assert by_id["WI-011"]["Predecessors"] == "WI-010"
    # P2 depends on P1 (mapped) + the parent.
    assert by_id["WI-012"]["Predecessors"] == "WI-011;WI-010"
    # P3 is the fan-in row: P1 AND P2, both mapped, + the parent.
    assert by_id["WI-013"]["Predecessors"] == "WI-011;WI-012;WI-010"


def test_file_selected_wis_honors_tier_map_and_defaults_medium(tmp_path):
    _seed_registry(tmp_path)
    pa.file_selected_wis(
        tmp_path,
        PLAN_TEXT,
        spec_ref="docs/plans/DP-001-x/plan.md",
        workstream="unattended",
        predecessor_wi="WI-010",
        tier_map={"P1": "strong", "P3": "quick"},
    )
    by_id = {r["WI-ID"]: r for r in _rows(tmp_path)}
    assert by_id["WI-011"]["BuildTier"] == "strong"
    assert by_id["WI-012"]["BuildTier"] == "medium"  # unmapped -> default
    assert by_id["WI-013"]["BuildTier"] == "quick"


def test_filed_rows_are_ra_compliant_queued(tmp_path):
    _seed_registry(tmp_path)
    pa.file_selected_wis(
        tmp_path,
        PLAN_TEXT,
        spec_ref="docs/plans/DP-001-x/plan.md",
        workstream="unattended",
        predecessor_wi="WI-010",
    )
    filed = [r for r in _rows(tmp_path) if r["WI-ID"] in ("WI-011", "WI-012", "WI-013")]
    assert len(filed) == 3
    for r in filed:
        assert r["Status"] == "queued"
        assert r["Deliverable"] == ""  # R-A: open WI carries no Deliverable
        assert r["SR-Refs"] == ""
        assert r["SpecRef"] == "docs/plans/DP-001-x/plan.md"
        assert r["Workstream"] == "unattended"


def test_file_selected_wis_preserves_lf_and_appends_cleanly(tmp_path):
    _seed_registry(tmp_path)
    pa.file_selected_wis(
        tmp_path,
        PLAN_TEXT,
        spec_ref="docs/plans/DP-001-x/plan.md",
        workstream="unattended",
        predecessor_wi="WI-010",
    )
    raw = _wi_csv(tmp_path).read_bytes()
    assert b"\r\n" not in raw  # the seed was LF; the append preserved it
    assert raw.endswith(b"\n")
    # No row got glued onto the previous one (a proper terminator was written).
    assert b",WI-011,Foundation" not in raw


def test_no_plan_table_files_nothing(tmp_path):
    _seed_registry(tmp_path)
    before = _wi_csv(tmp_path).read_bytes()
    mapping = pa.file_selected_wis(
        tmp_path,
        "# A brief with no Plan-WI table at all\n",
        spec_ref="docs/plans/DP-001-x/plan.md",
        workstream="unattended",
        predecessor_wi="WI-010",
    )
    assert mapping == {}
    assert _wi_csv(tmp_path).read_bytes() == before  # untouched


# --- the P5 done-condition: check_trajectory passes on the result -------------


def test_check_trajectory_passes_after_filing(tmp_path):
    """The P5 done-condition: after filing on a fixture repo, the real
    check_trajectory.py exits 0 and the new rows are well-formed + acyclic."""
    _seed_registry(tmp_path)
    # A resolvable SpecRef so the row is coherent even under --strict (R-E).
    plan_dir = pa.allocate_round_dir(tmp_path, "fixture")
    plan_path = pa.write_stage(plan_dir, "plan-B-rev.md", PLAN_TEXT)
    spec_ref = str(plan_path.relative_to(tmp_path)).replace("\\", "/")

    mapping = pa.file_selected_wis(
        tmp_path,
        PLAN_TEXT,
        spec_ref=spec_ref,
        workstream="unattended",
        predecessor_wi="WI-010",
    )
    assert set(mapping.values()) == {"WI-011", "WI-012", "WI-013"}

    proc = run_py([SCRIPTS / "check_trajectory.py", "--root", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # And clean under --strict too (predecessors resolve, SpecRef resolves).
    strict = run_py(
        [SCRIPTS / "check_trajectory.py", "--root", tmp_path, "--strict"], cwd=tmp_path
    )
    assert strict.returncode == 0, strict.stdout + strict.stderr


# --- log append ---------------------------------------------------------------


def test_append_log_summary_appends_block(tmp_path):
    log = tmp_path / "docs" / "log.md"
    log.parent.mkdir(parents=True)
    log.write_text("# Log\n\nExisting entry.\n", encoding="utf-8")
    pa.append_log_summary(tmp_path, "## DP-001 verdict — selected plan B")
    text = log.read_text(encoding="utf-8")
    assert text.startswith("# Log\n\nExisting entry.\n")
    assert text.endswith("## DP-001 verdict — selected plan B\n")
    assert "Existing entry." in text  # prior content untouched


def test_append_log_summary_creates_missing_log(tmp_path):
    (tmp_path / "docs").mkdir()
    log = pa.append_log_summary(tmp_path, "## First entry\n")
    assert log.read_text(encoding="utf-8") == "## First entry\n"
