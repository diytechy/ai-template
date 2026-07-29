"""plan_artifacts.py — the dual-plan round artifact filer (WI-198).

Exercises the coordinator's write-side of a round: DP-NNN directory allocation,
stage-artifact writes, filing the selected plan's rows as queued WIs (id
allocation, predecessor mapping incl. the fan-in row, tier map, R-A: queued
rows carry an empty Deliverable), the end-to-end `check_trajectory.py`-passes
fixture, header-safe optional-column handling, and the log append. Every test
builds its scaffolding under `tmp_path`
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
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SpecRef,"
    "BuildTier,CritiqueBudget,CritiqueExhaustion,Priority,Exclusive,BlockRef,"
    "EstTokens,SafetyClass,PlanMode\n"
)


def test_wi_header_matches_the_shipped_template():
    """Pin the three hand-maintained copies of the registry header — the shipped
    template (the product contract adopters copy), `plan_artifacts.WI_HEADER`
    (what a fresh registry gets), and this file's fixture — to one truth, so the
    next schema column cannot drift them apart silently (the 2026-07-17 H1
    failure mode; 2026-07-17b review M1)."""
    template = SCRIPTS.parent / "registries" / "work-items.template.csv"
    with template.open(encoding="utf-8-sig", newline="") as fh:
        header = next(csv.reader(fh))
    assert header == pa.WI_HEADER
    assert WI_HEADER_LINE == ",".join(header) + "\n"


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
            "WI-000,Example row,other,,,queued" + "," * 11 + "\n",
            "WI-001,Foundation,docs,,,done,shipped it" + "," * 10 + "\n",
            "WI-010,Round parent,unattended,,,done,parent shipped" + "," * 10 + "\n",
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


def _filed_rows(root):
    """The filed registry read back through the scheduler's own folder reader
    (the one home since Phase 5)."""
    sched = load_script("schedule")
    return sched.read_spec_rows(root / "docs" / "work")


def test_file_selected_wis_maps_predecessors_incl_fan_in(tmp_path):
    _seed_registry(tmp_path)
    pa.file_selected_wis(
        tmp_path,
        PLAN_TEXT,
        spec_ref="docs/plans/DP-001-x/plan.md",
        workstream="unattended",
        predecessor_wi="WI-010",
    )
    by_id = {r["WI-ID"]: r for r in _filed_rows(tmp_path)}
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
    by_id = {r["WI-ID"]: r for r in _filed_rows(tmp_path)}
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
    filed = [
        r for r in _filed_rows(tmp_path) if r["WI-ID"] in ("WI-011", "WI-012", "WI-013")
    ]
    assert len(filed) == 3
    for r in filed:
        assert r["Status"] == "queued"
        assert r["Deliverable"] == ""  # R-A: open WI carries no Deliverable
        assert r["SR-Refs"] == ""
        assert r["SpecRef"] == "docs/plans/DP-001-x/plan.md"
        assert r["Workstream"] == "unattended"
        assert r["SafetyClass"] == ""  # dispatcher audit, never inferred here
        assert r["PlanMode"] == ""  # only an explicitly dual filing sets this
        assert None not in r.values()  # row width matches the declared header


# (test_file_selected_wis_preserves_legacy_header_order and
# test_file_selected_wis_preserves_lf_and_appends_cleanly retired at
# concurrency-restructure Phase 5 with the CSV append path itself —
# filing writes spec files through wi_convert.write_spec_file, whose
# self-verification is the format guard.)


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


# --- the SECOND home: filing into docs/work/ (concurrency-restructure §2) -----
# The filer writes wherever the registry lives. CSV mode above is unchanged; the
# tests below drive the folder mode, the resolution BETWEEN them, and the one
# failure the union-allocation exists to make unreachable.


def _work(root):
    return root / "docs" / "work"


def _write_spec(root, where, wi_id, slug="thing", deliverable="", **frontmatter):
    """A spec file under `docs/work/<where>/`, LF whatever the platform."""
    path = _work(root) / where / "{}-{}.md".format(wi_id, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ['id = "{}"'.format(wi_id), 'title = "{}"'.format(slug)]
    lines += ['{} = "{}"'.format(k, v) for k, v in frontmatter.items()]
    text = "+++\n" + "".join(line + "\n" for line in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _file_three(root, spec_ref="docs/plans/DP-001-x/plan.md"):
    return pa.file_selected_wis(
        root,
        PLAN_TEXT,
        spec_ref=spec_ref,
        workstream="unattended",
        predecessor_wi="WI-010",
    )


def test_a_folder_registry_gets_spec_files_not_csv_rows(tmp_path):
    """The whole of folder mode: one file per work item, in `queued/`, and the
    CSV left byte-for-byte alone even though it is still on disk."""
    _seed_registry(tmp_path)
    _write_spec(
        tmp_path, "archive", "WI-010", slug="round-parent", deliverable="shipped"
    )
    before = _wi_csv(tmp_path).read_bytes()

    mapping = _file_three(tmp_path)
    assert mapping == {"P1": "WI-011", "P2": "WI-012", "P3": "WI-013"}
    assert _wi_csv(tmp_path).read_bytes() == before, "CSV written in folder mode"

    filed = sorted(p.name for p in (_work(tmp_path) / "queued").glob("*.md"))
    assert filed == [
        "WI-011-first-slice.md",
        "WI-012-second-slice.md",
        "WI-013-fan-in-slice.md",
    ], filed
    for path in (_work(tmp_path) / "queued").glob("*.md"):
        assert b"\r" not in path.read_bytes(), path.name


# (test_a_filed_spec_reads_back_as_the_row_csv_mode_would_have_written
# retired with CSV-mode filing at Phase 5; the RA-compliance test above
# reads the filed specs cell-by-cell through the scheduler's own reader.)


# (test_the_example_spec_alone_does_not_switch_the_filer_to_folder_mode
# retired at Phase 5: filing is folder-only, so there is no mode for the
# example to switch; its inertness is the readers' load_wis rule.)


def test_a_fresh_folder_first_scaffold_files_specs_without_resurrecting_a_csv(
    tmp_path,
):
    """A folder-first scaffold carries NO CSV and only the inert example under
    docs/work/. Filing its first real round must write spec files: the example
    never flips READ authority, but an absent CSV must not be created either —
    resurrecting the home the scaffold omitted would be the filer minting a
    second registry. Mutation-proven by construction: the pre-2c-ii filer
    (folder_is_authoritative alone) is the mutant, and it reds this test by
    creating the CSV."""
    _write_spec(tmp_path, "queued", "WI-000", slug="example")
    mapping = _file_three(tmp_path)
    assert mapping == {"P1": "WI-001", "P2": "WI-002", "P3": "WI-003"}
    assert not _wi_csv(tmp_path).exists(), "filing resurrected the CSV home"
    filed = sorted(p.name for p in (_work(tmp_path) / "queued").glob("*.md"))
    assert filed == [
        "WI-000-example.md",
        "WI-001-first-slice.md",
        "WI-002-second-slice.md",
        "WI-003-fan-in-slice.md",
    ], filed


def test_ids_are_allocated_over_BOTH_homes_so_a_transition_cannot_collide(tmp_path):
    """The union rule, driven from the direction that breaks a single-home
    allocator: the folder is authoritative, and the HIGHEST id lives only in the
    CSV the repo has stopped reading."""
    _seed_registry(tmp_path)  # highest CSV id: WI-010
    _write_spec(tmp_path, "archive", "WI-004", slug="older")
    assert pa._existing_wi_nums(_wi_csv(tmp_path)) == {0, 1, 4, 10}
    assert _file_three(tmp_path) == {"P1": "WI-011", "P2": "WI-012", "P3": "WI-013"}

    # And symmetrically: an id that exists ONLY in the folder still raises the
    # floor for a CSV-mode repo, which is the other half of "union".
    other = tmp_path / "other"
    _seed_registry(other)
    _write_spec(other, "queued", "WI-042", slug="filed-later")
    assert max(pa._existing_wi_nums(_wi_csv(other))) == 42


def test_mutation_folder_mode_refuses_a_duplicate_id(tmp_path):
    """The failure allocation makes unreachable, reached anyway: a spec already
    carrying the id the filer is about to mint. It must REFUSE by name — two
    files for one work item is the one state this registry cannot represent, and
    a silent overwrite would destroy the older one."""
    _seed_registry(tmp_path)
    _write_spec(tmp_path, "archive", "WI-010", slug="round-parent")
    # Stand in a broken allocator: WI-011 is already filed, in another status.
    _write_spec(tmp_path, "deferred", "WI-011", slug="already-here")

    rows = [{"WI-ID": "WI-011", "Title": "First slice", "Status": "queued"}]
    try:
        pa._write_spec_rows(_wi_csv(tmp_path), rows)
    except ValueError as exc:
        assert "WI-011" in str(exc) and "deferred/WI-011-already-here.md" in str(exc)
    else:
        raise AssertionError("a duplicate id was filed silently")

    # The honest other half: the same call with a free id succeeds, so the
    # refusal is about the collision and not about the code path.
    rows[0]["WI-ID"] = "WI-014"
    assert pa._write_spec_rows(_wi_csv(tmp_path), rows) == [
        "queued/WI-014-first-slice.md"
    ]
    # And the pre-existing spec was not touched on the way past.
    assert (_work(tmp_path) / "deferred" / "WI-011-already-here.md").exists()


def test_check_trajectory_passes_after_filing_into_the_folder(tmp_path):
    """The CSV mode's done-condition, restated for the second home: the real
    validator exits 0 over the folder the filer just wrote."""
    _write_spec(
        tmp_path, "archive", "WI-010", slug="round-parent", deliverable="parent shipped"
    )
    plan_dir = pa.allocate_round_dir(tmp_path, "fixture")
    plan_path = pa.write_stage(plan_dir, "plan-B-rev.md", PLAN_TEXT)
    spec_ref = str(plan_path.relative_to(tmp_path)).replace("\\", "/")
    assert set(_file_three(tmp_path, spec_ref).values()) == {
        "WI-011",
        "WI-012",
        "WI-013",
    }
    proc = run_py([SCRIPTS / "check_trajectory.py", "--root", tmp_path], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr


# (The CSV-mode P5 done-condition test retired at Phase 5;
# test_check_trajectory_passes_after_filing_into_the_folder above is the
# one done-condition — a seeded CSV now trips the stray-CSV finding by
# design.)


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
