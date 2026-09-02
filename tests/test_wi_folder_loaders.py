"""The spec-folder work-item registry, read by the three surviving loaders.

`docs/work/<status>/WI-###-<slug>.md` is the ONE registry home
(docs/concurrency-restructure.md §2; the CSV home retired at Phase 5,
RULING-4). Three scripts — `schedule.py`, `check_trajectory.py` and
`agent_common.py` — each carry their own verbatim copy of a reader that emits
rows with the SAME 17 keys `csv.DictReader` once yielded, so everything
downstream of one function per script was untouched by the migration.

`tests/test_wi_loader_sync.py` proves the three copies agree with each other
(and, as converter fidelity, with wi_convert's CSV form). THIS module tests
what only the folder can do:

  * the one-home read (Phase 5: the CSV home retired) and the deliberate
    asymmetry — a stray resurrected CSV is an INTEGRITY ERROR from the
    validator and SILENCE from the scheduler and the coordinator, because a
    worker reads the registry and does not adjudicate it;
  * the malformed-spec split, the same shape: the validator names the file, the
    other two skip it (a broken registry is the validator's job to report, not
    the scheduler's to crash on);
  * `active/<branch>/`, the only status two levels deep;
  * the git plumbing, which is where the CSV's assumptions do not survive —
    status-at-HEAD from `ls-tree` PATHS, staleness across a status MOVE, and
    close detection from a staged RENAME.

Every guard here is mutation-proven: each is also run against the defect it
exists to catch, and must fail. The staleness guard in particular drives the
failure shape rather than the happy path — it asserts the clock survives a
`git mv` AND that dropping either git flag makes it reset, which is how the
measurement got made instead of assumed.
"""

import os
import shutil
import subprocess

import pytest
from conftest import (
    KIT,
    SCRIPTS,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
)

sched = load_script("schedule")
ctraj = load_script("check_trajectory")
acommon = load_script("agent_common")

MODULES = (("schedule", sched), ("check_trajectory", ctraj), ("agent_common", acommon))
# The two that stay quiet about registry problems (the scheduler and the worker
# coordinator); check_trajectory is the validator and is tested apart.
QUIET_MODULES = (("schedule", sched), ("agent_common", acommon))

CSV_HEADER = ",".join(sched.WI_COLUMNS) + "\n"
# The spine SR registry's header, for the fixtures whose findings cite an SR.
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)


def spec_text(wid, title="Thing", order=0, deliverable="", **frontmatter):
    """One spec file's text in the format `scripts/wi_convert.py` emits."""
    lines = ['id = "{}"'.format(wid), 'title = "{}"'.format(title)]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(
                "{} = [{}]".format(key, ", ".join('"{}"'.format(v) for v in value))
            )
        elif isinstance(value, int):
            lines.append("{} = {}".format(key, value))
        else:
            lines.append('{} = "{}"'.format(key, value))
    if order is not None:
        lines.append("order = {}".format(order))
    text = "+++\n" + "".join(line + "\n" for line in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def write_spec(root, where, wid, slug="thing", **kw):
    """Write `docs/work/<where>/<wid>-<slug>.md` under `root`; return its path.

    `newline="\\n"` explicitly: a fixture that takes the platform default cannot
    test the platform (the WI-337 lesson)."""
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def write_archived_spec(root, where, wid, slug="thing", **kw):
    """Write `docs/archive/work/<where>/<wid>-<slug>.md` under `root` — the
    terminal-history home since WI-504 (OI-55 ruled (a)); return its path.
    `write_spec`'s twin, one directory deeper."""
    path = root / "docs" / "archive" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def write_csv(root, rows):
    """Write `docs/requirements/work-items.csv` from `[{column: cell}]`."""
    path = root / "docs" / "requirements" / "work-items.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(
        ",".join((row.get(column) or "") for column in sched.WI_COLUMNS) + "\n"
        for row in rows
    )
    path.write_text(CSV_HEADER + body, encoding="utf-8", newline="\n")
    return path


def csv_path(root):
    return root / "docs" / "requirements" / "work-items.csv"


# --- the dual-read resolution -------------------------------------------------


def test_no_spec_folder_reads_an_empty_registry(tmp_path):
    """With no `docs/work/` the registry is simply EMPTY — the non-adopter
    posture. A work-items.csv on disk changes nothing for the readers (the CSV
    home retired at Phase 5); the validator alone names the stray file."""
    write_csv(
        tmp_path, [{"WI-ID": "WI-001", "Title": "from the csv", "Status": "done"}]
    )
    assert sched.load_registry_rows(csv_path(tmp_path)) == []
    assert ctraj.read_registry_rows(csv_path(tmp_path)) == []
    assert acommon.load_wi_registry(tmp_path) == {}


def test_the_folder_wins_when_it_holds_specs(tmp_path):
    write_csv(
        tmp_path, [{"WI-ID": "WI-001", "Title": "from the csv", "Status": "done"}]
    )
    write_spec(tmp_path, "queued", "WI-001", title="from the folder")
    assert sched.load_registry_rows(csv_path(tmp_path))[0]["Title"] == "from the folder"
    assert ctraj.read_registry_rows(csv_path(tmp_path))[0]["Title"] == "from the folder"
    assert acommon.load_wi_registry(tmp_path)["WI-001"]["Title"] == "from the folder"


def test_an_empty_or_specless_work_dir_reads_empty(tmp_path):
    """An empty `docs/work/`, and one holding a file with no status directory
    above it, both read as an empty registry — never a crash, and never a
    resurrected CSV read."""
    write_csv(
        tmp_path, [{"WI-ID": "WI-001", "Title": "from the csv", "Status": "done"}]
    )
    work = tmp_path / "docs" / "work"
    work.mkdir(parents=True)
    assert sched.load_registry_rows(csv_path(tmp_path)) == []
    (work / "pause").write_text("reason = 'draining'\n", encoding="utf-8", newline="\n")
    (work / "WI-999-loose.md").write_text(
        spec_text("WI-999"), encoding="utf-8", newline="\n"
    )
    assert sched.load_registry_rows(csv_path(tmp_path)) == []


def test_the_work_dir_is_derived_from_the_csv_path_not_a_second_constant(tmp_path):
    """`docs/requirements/work-items.csv` -> `docs/work`, in every copy."""
    for name, mod in MODULES:
        assert mod.spec_work_dir(csv_path(tmp_path)) == tmp_path / "docs" / "work", name


# --- the inert `-000` example (Phase 2c-i) ------------------------------------
# `bootstrap.py` scaffolds `docs/work/queued/WI-000-example.md` beside the CSV
# template, so the folder home ships ADDITIVE. That only works if the example is
# inert in BOTH senses the CSV's `-000` row is: skipped by `load_wis`, and unable
# to decide which home is authoritative. Without the second, a fresh scaffold
# would get an empty registry plus a two-registries-present finding on its first
# check — measured, not assumed, which is why these guards exist.


def _example_spec(root):
    """The shipped `WI-000` template, written where bootstrap scaffolds it."""
    path = root / "docs" / "work" / "queued" / "WI-000-example.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        (KIT / "work" / "WI-000.template.md").read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )
    return path


def test_the_example_spec_alone_is_an_empty_registry_without_findings(tmp_path):
    """A fresh scaffold holds only the inert `-000` example: the registry
    reads empty at `load_wis` (the example goes inert there) and, with no
    stray CSV, the validator has nothing to say."""
    _example_spec(tmp_path)
    rows = ctraj.read_registry_rows(csv_path(tmp_path))
    assert [r["WI-ID"] for r in rows] == ["WI-000"]
    assert sched.load_wis(rows) == []
    errors = []
    ctraj.read_registry_rows(csv_path(tmp_path), errors)
    assert errors == [], errors


def test_a_real_spec_beside_the_example_reads_normally(tmp_path):
    """The `-000` exemption is `load_wis`'s inertness rule, never a directory
    rule — a genuine spec in the same directory reads like any other."""
    _example_spec(tmp_path)
    write_spec(tmp_path, "queued", "WI-001", title="from the folder")
    assert sched.load_registry_rows(csv_path(tmp_path))[0]["Title"] == "from the folder"
    assert [
        w["id"] for w in sched.load_wis(sched.load_registry_rows(csv_path(tmp_path)))
    ] == ["WI-001"]


def test_the_example_spec_parses_and_then_goes_inert_in_load_wis(tmp_path):
    """It is READ like any other spec — the exemption is the authority rule, not
    a second skip — and goes inert exactly where the CSV's `-000` row does, in
    `load_wis`. Both halves asserted: a silent parse failure would look
    identical to inertness from the outside."""
    _example_spec(tmp_path)
    write_spec(tmp_path, "queued", "WI-001")
    work = tmp_path / "docs" / "work"
    for name, mod in MODULES:
        rows = mod.read_spec_rows(work)
        # The shipped example is HAND-FILED — no `order` key — so it sorts after
        # every numbered spec, which is the documented fallback and not an
        # accident of this fixture.
        assert [r["WI-ID"] for r in rows] == ["WI-001", "WI-000"], name
        example = rows[-1]
        assert example["Status"] == "queued", name
        assert example["Deliverable"].startswith("**What this file is.**"), name
    assert [w["id"] for w in sched.load_wis(sched.read_spec_rows(work))] == ["WI-001"]
    assert [w["id"] for w in ctraj.load_wis(sched.read_spec_rows(work))[0]] == [
        "WI-001"
    ]


def test_mutation_a_malformed_example_would_be_reported_not_hidden(tmp_path):
    """The exemption must not have turned the example into an unchecked file:
    break it and the validator's reader still names it."""
    path = _example_spec(tmp_path)
    path.write_text("not a spec at all\n", encoding="utf-8", newline="\n")
    errors = []
    ctraj.read_spec_rows(tmp_path / "docs" / "work", on_error=errors.append)
    assert len(errors) == 1 and "WI-000-example.md" in errors[0], errors


# --- a stray CSV: the validator speaks, the others do not ---------------------


def test_a_stray_csv_is_an_integrity_error_from_the_validator(tmp_path):
    write_csv(tmp_path, [{"WI-ID": "WI-001", "Title": "csv", "Status": "done"}])
    write_spec(tmp_path, "queued", "WI-001")
    errors = []
    rows = ctraj.read_registry_rows(csv_path(tmp_path), errors)
    assert rows and rows[0]["Status"] == "queued"
    assert len(errors) == 1, errors
    assert "CSV registry home retired" in errors[0]
    assert "docs/work" in errors[0] and "work-items.csv" in errors[0]


def test_the_scheduler_and_the_coordinator_stay_silent_on_both_present(
    tmp_path, capsys
):
    """The asymmetry is the point: reporting a transition state is the
    validator's job, and a scheduler that refused would stop the repo dead."""
    write_csv(tmp_path, [{"WI-ID": "WI-001", "Title": "csv", "Status": "done"}])
    write_spec(tmp_path, "queued", "WI-001")
    assert sched.load_registry_rows(csv_path(tmp_path))[0]["Status"] == "queued"
    assert acommon.load_wi_registry(tmp_path)["WI-001"]["Status"] == "queued"
    assert capsys.readouterr() == ("", "")


def test_mutation_removing_the_csv_clears_the_stray_finding(tmp_path):
    """The finding's own remedy, exercised: delete the CSV and it goes away —
    otherwise the error would be unactionable noise rather than a migration step."""
    write_csv(tmp_path, [{"WI-ID": "WI-001", "Title": "csv", "Status": "done"}])
    write_spec(tmp_path, "queued", "WI-001")
    errors = []
    ctraj.read_registry_rows(csv_path(tmp_path), errors)
    assert errors, "fixture premise gone: the two-registry state does not report"
    csv_path(tmp_path).unlink()
    cleared = []
    ctraj.read_registry_rows(csv_path(tmp_path), cleared)
    assert cleared == []


# --- status is location -------------------------------------------------------


@pytest.mark.parametrize(
    "where,expected",
    [
        ("draft", "draft"),
        ("queued", "queued"),
        ("deferred", "deferred"),
        ("complete", "done"),
        ("cancelled", "cancelled"),
        ("active/llm-wi-001", "active"),
        ("active/feature/nested-branch", "active"),
    ],
)
def test_the_directory_is_the_status(tmp_path, where, expected):
    """`active/<branch>/` is the only status two levels deep, so the status is
    the FIRST path component — a rule the file's own parent cannot express."""
    write_spec(tmp_path, where, "WI-001")
    for name, mod in MODULES:
        rows = mod.read_spec_rows(tmp_path / "docs" / "work")
        assert [r["Status"] for r in rows] == [expected], name


def test_each_terminal_state_is_its_own_directory(tmp_path):
    """WI-384: the two terminals are told apart by LOCATION and nothing else.

    Before, both lived in `archive/` and a `disposition` key told them apart —
    an attribute, a validator and two raise paths for one missing folder. The
    split deleted all of it: the reader below asks the path and has nothing else
    to consult, so folder and attribute can no longer disagree because there is
    no attribute."""
    write_spec(tmp_path, "cancelled", "WI-001", deliverable="why it never will")
    write_spec(tmp_path, "complete", "WI-002", order=1, deliverable="shipped")
    for name, mod in MODULES:
        rows = mod.read_spec_rows(tmp_path / "docs" / "work")
        assert [(r["WI-ID"], r["Status"]) for r in rows] == [
            ("WI-001", "cancelled"),
            ("WI-002", "done"),
        ], name


def test_terminal_history_reads_from_its_archive_home(tmp_path):
    """WI-504 (OI-55 ruled (a)): a spec under `docs/archive/work/<status>/`
    reads exactly like one under `docs/work/<status>/` — the registry is ONE
    logical set of rows split across two directory trees, so a terminal row
    relocated one directory deeper is neither lost nor duplicated, and a repo
    with an open row still in `docs/work/` and terminal history already moved
    reads BOTH halves as a single ordered registry."""
    write_spec(tmp_path, "queued", "WI-001", order=0)
    write_archived_spec(
        tmp_path, "cancelled", "WI-002", order=1, deliverable="why it never will"
    )
    write_archived_spec(tmp_path, "complete", "WI-003", order=2, deliverable="shipped")
    for name, mod in MODULES:
        rows = mod.read_spec_rows(tmp_path / "docs" / "work")
        assert [(r["WI-ID"], r["Status"]) for r in rows] == [
            ("WI-001", "queued"),
            ("WI-002", "cancelled"),
            ("WI-003", "done"),
        ], name


def test_a_restructured_spec_reads_as_the_fourth_terminal_state(tmp_path):
    """The 2026-09-02 restructure plan §1.6: `restructured` is a DECLARED status
    directory, so a row a consolidation absorbed into a successor reads as
    itself rather than being skipped as an undeclared folder — the invisible-row
    hazard `draft/`'s declaration exists to close.

    Both roots, because status is the directory NAME and the archive is only its
    parent: the canonical home is `docs/archive/work/restructured/`, and a spec
    filed under the active workspace reads identically (nothing should be
    silently dropped mid-move). All three loaders, because a status one reader
    knows and another does not is how a row falls out of half the machinery."""
    write_spec(tmp_path, "queued", "WI-001", order=0, supersedes="WI-002;WI-003")
    write_archived_spec(
        tmp_path,
        "restructured",
        "WI-002",
        order=1,
        deliverable="Restructured into WI-001.",
    )
    write_spec(
        tmp_path,
        "restructured",
        "WI-003",
        order=2,
        deliverable="Restructured into WI-001.",
    )
    for name, mod in MODULES:
        rows = mod.read_spec_rows(tmp_path / "docs" / "work")
        assert [(r["WI-ID"], r["Status"]) for r in rows] == [
            ("WI-001", "queued"),
            ("WI-002", "restructured"),
            ("WI-003", "restructured"),
        ], name
        assert rows[1]["Deliverable"] == "Restructured into WI-001.", name
    # ... and the validator reads it clean: terminal, so the filled Deliverable
    # is REQUIRED (R-A) rather than an open row's forbidden one.
    errors = []
    rows = ctraj.read_registry_rows(csv_path(tmp_path), errors)
    assert errors == []
    wis, integrity = ctraj.load_wis(rows)
    assert integrity == []
    assert "restructured" in ctraj.TERMINAL_STATUSES
    assert "restructured" not in ctraj.OPEN_STATUSES
    assert "restructured" not in ctraj.BACKLOG_STALE_STATUSES
    assert [f for f in ctraj.ssot_findings(wis, tmp_path) if f[0] == "R-A"] == []


def test_a_restructured_row_owes_the_line_that_names_its_successor(tmp_path):
    """The mutation twin of the row above: `restructured` is terminal, and R-A's
    filled-Deliverable rule bites on it exactly as it does on `done`/`cancelled`.
    `partial` is the ONE terminal exempt from the cell (its per-close report is
    the record); an absorbed row has no report, so the one line naming the
    successor is the only record there is and an empty cell is an ERROR."""
    write_spec(tmp_path, "queued", "WI-001", order=0)  # the work dir must exist
    write_archived_spec(tmp_path, "restructured", "WI-002", order=1, deliverable="")
    rows = ctraj.read_registry_rows(csv_path(tmp_path))
    wis, _integrity = ctraj.load_wis(rows)
    findings = [f for f in ctraj.ssot_findings(wis, tmp_path) if f[0] == "R-A"]
    assert [(rule, hard) for rule, hard, _msg in findings] == [("R-A", True)], findings
    assert "WI-002" in findings[0][2] and "successor" in findings[0][2], findings


def test_a_restructured_row_may_keep_its_specref_like_a_partial_one(tmp_path):
    """R-F's carve-out covers BOTH continuing terminals, not just `partial`.

    R-F clears a terminal row's SpecRef so a closed row stops pointing at a live
    spec a reader would take as current. `partial` is carved out because partial
    work continues by MINTING A SUCCESSOR and the successor's `supersedes`
    lineage is worth nothing if the thread it continues has already been cut —
    and that reason applies to an absorbed row word for word (the 2026-09-02
    restructure plan says the move follows "the same rule as `partial`"). So the
    cell is a MAY: WI-002 keeps it, WI-003 cleared it, and neither is a finding.
    The `cancelled` control is what proves the rule still bites where it should
    — otherwise this test would pass on a checker that had stopped reading."""
    write_spec(tmp_path, "queued", "WI-001", order=0, supersedes="WI-002;WI-003")
    write_archived_spec(
        tmp_path,
        "restructured",
        "WI-002",
        order=1,
        deliverable="Restructured into WI-001.",
        specref="docs/specs/WI-002.md",
    )
    write_archived_spec(
        tmp_path,
        "restructured",
        "WI-003",
        order=2,
        deliverable="Restructured into WI-001.",
    )
    write_archived_spec(
        tmp_path,
        "cancelled",
        "WI-004",
        order=3,
        deliverable="refuted",
        specref="docs/specs/WI-004.md",
    )
    wis, _integrity = ctraj.load_wis(ctraj.read_registry_rows(csv_path(tmp_path)))
    findings = ctraj.spec_lifecycle_findings(tmp_path, wis)
    assert [f for f in findings if "WI-002" in f or "WI-003" in f] == [], findings
    assert len([f for f in findings if "WI-004" in f]) == 1, findings


def test_a_restructured_deliverable_owes_the_fixed_successor_grammar(tmp_path):
    """R-A's `restructured` arm: the line is a LINEAGE RECORD, so it is parsed.

    An absorbed row's whole permanent record is the successor it names — there
    is no handback report behind it — so free prose in that cell is a lineage
    that looks recorded and is not. Three drives: the good form (one successor
    and several), the parenthetical form the first live restructure actually
    wrote, and a successor whose own `Supersedes` cell does not name the row
    back (the half nothing checked, so a typo split the pair silently)."""
    write_spec(tmp_path, "queued", "WI-001", order=0, supersedes="WI-002;WI-003")
    write_archived_spec(
        tmp_path,
        "restructured",
        "WI-002",
        order=1,
        deliverable="Restructured into WI-001.",
    )
    write_archived_spec(
        tmp_path,
        "restructured",
        "WI-003",
        order=2,
        deliverable="Restructured into WI-001, WI-004.",
    )
    write_spec(tmp_path, "queued", "WI-004", order=3)  # a live row, but not mutual
    write_archived_spec(
        tmp_path,
        "restructured",
        "WI-005",
        order=4,
        deliverable="Restructured into WI-001 (Done-when 1) and WI-004.",
    )
    wis, _integrity = ctraj.load_wis(ctraj.read_registry_rows(csv_path(tmp_path)))
    findings = [f for f in ctraj.ssot_findings(wis, tmp_path) if f[0] == "R-A"]
    assert all(hard for _rule, hard, _msg in findings), findings
    messages = [msg for _rule, _hard, msg in findings]
    # WI-002's single successor and WI-003's first are both mutual: clean.
    assert [m for m in messages if m.startswith("WI-002")] == [], messages
    # WI-003's SECOND successor is a live row that never claimed it.
    assert len([m for m in messages if m.startswith("WI-003")]) == 1, messages
    assert (
        "does not name it back" in [m for m in messages if m.startswith("WI-003")][0]
    ), messages
    # WI-005's parenthetical is refused on grammar alone, before mutuality.
    wi005 = [m for m in messages if m.startswith("WI-005")]
    assert len(wi005) == 1 and "exactly one line" in wi005[0], messages


def test_a_restructured_row_naming_a_successor_that_does_not_exist_is_reported(
    tmp_path,
):
    """The other half of the same arm: a successor id that is no row at all.
    Split from the mutuality case because the two fail for different reasons and
    a reader needs the message to say which — a typo'd id and a live row that
    disowns you are different repairs."""
    write_spec(tmp_path, "queued", "WI-001", order=0)
    write_archived_spec(
        tmp_path,
        "restructured",
        "WI-002",
        order=1,
        deliverable="Restructured into WI-404.",
    )
    wis, _integrity = ctraj.load_wis(ctraj.read_registry_rows(csv_path(tmp_path)))
    findings = [f for f in ctraj.ssot_findings(wis, tmp_path) if f[0] == "R-A"]
    assert len(findings) == 1 and findings[0][1] is True, findings
    assert "no such work item exists" in findings[0][2], findings


def test_a_live_hard_edge_onto_a_restructured_row_is_reported(tmp_path):
    """The validator NET behind the re-point step (restructure plan §1.5): the
    close that absorbs a row re-points every inbound hard edge to the successor,
    and a dependent the re-point missed would otherwise wait forever in silence.
    Same finding class as an edge onto a `partial` row — the scheduler agrees
    (`waiting:hard-pred-restructured:`), so neither can call the edge live."""
    write_archived_spec(
        tmp_path, "restructured", "WI-001", deliverable="Restructured into WI-003."
    )
    write_spec(tmp_path, "queued", "WI-002", needs=["WI-001"], order=1)
    wis, _integrity = ctraj.load_wis(ctraj.read_registry_rows(csv_path(tmp_path)))
    findings = ctraj.dead_dependency_findings(wis)
    assert len(findings) == 1, findings
    assert findings[0].startswith(
        "WI-002: open WI hard-depends on terminal WI(s) WI-001"
    ), findings
    # The control: re-pointed at the successor, the same registry is clean —
    # so the finding above is the dead edge talking, not the shape of the tree.
    write_spec(tmp_path, "queued", "WI-003", order=2)
    (tmp_path / "docs" / "work" / "queued" / "WI-002-thing.md").write_text(
        spec_text("WI-002", needs=["WI-003"], order=1), encoding="utf-8", newline="\n"
    )
    wis, _integrity = ctraj.load_wis(ctraj.read_registry_rows(csv_path(tmp_path)))
    assert ctraj.dead_dependency_findings(wis) == []


def test_a_leftover_disposition_key_is_inert_not_authoritative(tmp_path):
    """The deleted attribute stays deleted. A spec still carrying the old
    `disposition` key — a downstream repo mid-migration — reads by its FOLDER,
    with the stale key ignored like any other unknown frontmatter. There is
    deliberately no validator left to consult it, so it cannot contradict the
    location."""
    write_spec(
        tmp_path, "complete", "WI-001", disposition="retired", deliverable="shipped"
    )
    for name, mod in MODULES:
        rows = mod.read_spec_rows(tmp_path / "docs" / "work")
        assert [r["Status"] for r in rows] == ["done"], name


# --- `draft/`: a DECLARED directory, and why the declaration is the point -----


def test_draft_is_never_ready_exactly_like_deferred(tmp_path):
    """WI-384: `draft` and `deferred` are both never-ready and differ only in
    what they SAY — `deferred` is a decision (not now), `draft` is the absence of
    one (still being figured out). So each keeps its own disposition and reason
    code rather than one being folded into the other."""
    write_spec(tmp_path, "draft", "WI-001", safety_class="ordinary")
    write_spec(tmp_path, "deferred", "WI-002", order=1, safety_class="ordinary")
    write_spec(tmp_path, "queued", "WI-003", order=2, safety_class="ordinary")
    rows = sched.read_spec_rows(tmp_path / "docs" / "work")
    records = sched.evaluate(sched.load_wis(rows))
    by_id = {r["id"]: r for r in records}
    assert by_id["WI-001"]["disposition"] == "draft"
    assert by_id["WI-001"]["reasons"] == ["excluded:draft"]
    assert by_id["WI-002"]["disposition"] == "deferred"
    assert by_id["WI-002"]["reasons"] == ["excluded:deferred"]
    # ... and the frontier holds only the queued row, so neither slipped in.
    assert [r["id"] for r in sched.frontier(sched.load_wis(rows))] == ["WI-003"]


def test_a_drafted_id_is_visible_to_the_registry_and_so_reserved(tmp_path):
    """The reason `draft/` is a declared status directory: id reservation —
    corrected at WI-384's REVIEW-A round 1, because the ruled clause was half
    false and this test is what proves which half.

    `read_spec_rows` walks `<status>/WI-*.md` and skips anything under a
    directory it does not know, so a draft parked in an improvised folder never
    enters the registry: the duplicate-id GUARD and the dashboard go blind to
    the id it holds. What the ruling ALSO claimed — that `max(id) + 1` would
    reissue the id — is not true of the shipped mint, which reads filenames
    through `wi_convert.spec_paths`, an unfiltered walk that never consults
    `SPEC_STATUS_DIRS` (driven on two temp trees: declared and undeclared both
    mint the same next id). So the mint is safe either way and the declaration
    makes the reservation CHECKED rather than incidental. This asserts what is
    actually true — the declared folder is seen by the readers and by the
    duplicate-id guard, and the undeclared one is not."""
    write_spec(tmp_path, "draft", "WI-042", title="held id")
    work = tmp_path / "docs" / "work"
    for name, mod in MODULES:
        rows = mod.read_spec_rows(work)
        assert [(r["WI-ID"], r["Status"]) for r in rows] == [("WI-042", "draft")], name
    # The id is in the graph, so the duplicate-id guard can see a collision...
    write_spec(tmp_path, "queued", "WI-042", slug="collides", order=1)
    _wis, integrity = ctraj.load_wis(ctraj.read_registry_rows(csv_path(tmp_path)))
    assert any("WI-042" in msg and "duplicate" in msg.lower() for msg in integrity), (
        integrity
    )
    # ... whereas the SAME spec in an undeclared folder is invisible, which is
    # the hazard the declaration closes (the counterfactual, not a hypothesis).
    other = tmp_path / "elsewhere"
    write_spec(other, "thinking", "WI-042", title="held id")
    assert sched.read_spec_rows(other / "docs" / "work") == []


def test_the_soft_prefix_survives_into_the_hard_soft_split(tmp_path):
    """`~` is meaning, not decoration — it is what makes an edge advisory."""
    write_spec(tmp_path, "queued", "WI-003", needs=["WI-001", "~WI-002"])
    rows = sched.read_spec_rows(tmp_path / "docs" / "work")
    assert rows[0]["Predecessors"] == "WI-001;~WI-002"
    for wis in (sched.load_wis(rows), ctraj.load_wis(rows)[0]):
        assert wis[0]["preds"] == ["WI-001"]
        assert wis[0]["soft"] == ["WI-002"]


def test_rows_come_back_in_registry_order(tmp_path):
    """The explicit `order` key first, then numeric id — a hand-filed spec with
    no order sorts after every numbered one instead of landing arbitrarily."""
    write_spec(tmp_path, "queued", "WI-010", order=1)
    write_spec(tmp_path, "complete", "WI-004", order=0, deliverable="shipped")
    write_spec(tmp_path, "queued", "WI-002", order=None)
    write_spec(tmp_path, "queued", "WI-001", order=None)
    rows = sched.read_spec_rows(tmp_path / "docs" / "work")
    assert [r["WI-ID"] for r in rows] == ["WI-004", "WI-010", "WI-001", "WI-002"]


# --- the malformed-spec split -------------------------------------------------

MALFORMED = {
    "bad-toml": "+++\nid = \nname\n+++\n",
    "no-fence": 'id = "WI-001"\n',
    "unclosed-fence": '+++\nid = "WI-001"\n',
    "no-id": '+++\ntitle = "nameless"\n+++\n',
    "non-string-id": "+++\nid = 7\n+++\n",
    "id-filename-mismatch": '+++\nid = "WI-002"\n+++\n',
    "body-is-not-deliverable": '+++\nid = "WI-001"\n+++\n\n## Notes\n\nfree text\n',
}


@pytest.mark.parametrize("kind", sorted(MALFORMED))
def test_the_validator_reports_a_malformed_spec_and_names_the_file(tmp_path, kind):
    path = tmp_path / "docs" / "work" / "queued" / "WI-001-thing.md"
    path.parent.mkdir(parents=True)
    path.write_text(MALFORMED[kind], encoding="utf-8", newline="\n")
    errors = []
    rows = ctraj.read_registry_rows(csv_path(tmp_path), errors)
    assert rows == []
    assert len(errors) == 1, errors
    assert "queued/WI-001-thing.md" in errors[0], errors


@pytest.mark.parametrize("kind", sorted(MALFORMED))
def test_the_scheduler_and_coordinator_skip_a_malformed_spec_silently(
    tmp_path, capsys, kind
):
    path = tmp_path / "docs" / "work" / "queued" / "WI-001-thing.md"
    path.parent.mkdir(parents=True)
    path.write_text(MALFORMED[kind], encoding="utf-8", newline="\n")
    write_spec(tmp_path, "queued", "WI-007", order=1)
    for name, mod in QUIET_MODULES:
        rows = mod.read_spec_rows(tmp_path / "docs" / "work")
        # The good spec still loads — one broken file must not blank the backlog.
        assert [r["WI-ID"] for r in rows] == ["WI-007"], name
    assert capsys.readouterr() == ("", "")


def test_an_unknown_status_directory_is_refused_not_bucketed(tmp_path):
    """The catch-all failure this repo has made twice: a directory nobody
    declared must be a refusal naming the file, never a silent `queued`."""
    write_spec(tmp_path, "in-review", "WI-001")
    errors = []
    assert ctraj.read_registry_rows(csv_path(tmp_path), errors) == []
    assert "is not a status directory" in errors[0], errors
    assert sched.read_spec_rows(tmp_path / "docs" / "work") == []


def test_the_retired_archive_directory_is_now_refused_by_name(tmp_path):
    """WI-384 deleted `archive/` from the vocabulary, and deleting a directory
    from a DECLARED set is what makes its reappearance loud.

    Not hypothetical: a branch cut before the split closes its WI into
    `archive/`, and the composed tree then holds a directory nobody declares. It
    must be a named refusal that stops the validator, never a silent skip that
    drops the row out of the registry — the reconciliation is to move the file
    into `complete/` or `cancelled/`."""
    write_spec(tmp_path, "archive", "WI-001", deliverable="shipped")
    errors = []
    assert ctraj.read_registry_rows(csv_path(tmp_path), errors) == []
    assert "'archive' is not a status directory" in errors[0], errors
    assert "complete" in errors[0] and "cancelled" in errors[0], errors
    # ... and the quiet readers drop it, which is exactly why the LOUD half
    # above has to exist: on its own a skip is indistinguishable from an
    # empty backlog.
    assert sched.read_spec_rows(tmp_path / "docs" / "work") == []


def test_mutation_a_valid_spec_produces_no_finding(tmp_path):
    """The other half of every refusal test above: the same reader, the same
    call, a WELL-FORMED file — so the errors above are the malformation talking
    and not the reader refusing everything."""
    write_spec(tmp_path, "queued", "WI-001", deliverable="")
    errors = []
    rows = ctraj.read_registry_rows(csv_path(tmp_path), errors)
    assert errors == []
    assert [r["WI-ID"] for r in rows] == ["WI-001"]


# --- main(): the validator end-to-end over a folder registry ------------------


def test_a_multi_line_deliverable_is_the_format_working_not_a_broken_cell(tmp_path):
    """Why the CSV cell-integrity rule is scoped to the CSV home. That rule
    exists because `staged_findings` compares `work-items.csv` line-wise, and in
    the folder registry nothing does — the Deliverable is a BODY section, where a
    newline is the format working as designed."""
    body = "line one\n\nline two"
    write_spec(tmp_path, "complete", "WI-001", deliverable=body)
    rows = ctraj.read_registry_rows(csv_path(tmp_path))
    assert rows[0]["Deliverable"] == body
    # The same cell in the CSV home IS a hard error — so the scoping decision is
    # load-bearing, not cosmetic: applied here it would reject a valid registry.
    assert ctraj.cell_integrity_errors(rows) != []


def _validator_repo(tmp_path):
    """A minimal repo the trajectory validator can run over end-to-end."""
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    (tmp_path / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + "SR-001,A,SN-001,does X,R,AC,,M,Test,Drafted\n",
        encoding="utf-8",
        newline="\n",
    )
    # A MULTI-LINE Deliverable on purpose: it is legal in the folder registry
    # (the body is prose) and illegal in the CSV one, so a run that stays clean
    # here proves the cell-integrity rule really is scoped to the CSV home.
    write_spec(
        tmp_path,
        "complete",
        "WI-001",
        sr_refs=["SR-001"],
        deliverable="shipped it\n\nand recorded why",
    )
    write_spec(
        tmp_path,
        "queued",
        "WI-002",
        order=1,
        sr_refs=["SR-001"],
        needs=["WI-001"],
        specref="docs/specs/WI-002.md",
    )
    spec = tmp_path / "docs" / "specs" / "WI-002.md"
    spec.parent.mkdir(parents=True)
    spec.write_text("# WI-002\n", encoding="utf-8", newline="\n")
    return tmp_path


def test_the_validator_runs_clean_over_a_folder_registry(tmp_path):
    """The whole of `main()` in folder mode — every rule below the loader reads
    the same 17-key rows, so a green here is the "zero behaviour change" claim
    exercised from the other side."""
    _validator_repo(tmp_path)
    proc = run_py([SCRIPTS / "check_trajectory.py", "--strict"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "2 work item(s)" in proc.stdout, proc.stdout


def test_the_validator_fails_the_run_on_a_stray_csv(tmp_path):
    """A resurrected CSV is an ERROR at the exit code, not a warn: it is a
    second encoding of the registry that nothing reads."""
    _validator_repo(tmp_path)
    write_csv(tmp_path, [{"WI-ID": "WI-001", "Title": "csv", "Status": "done"}])
    proc = run_py([SCRIPTS / "check_trajectory.py"], cwd=tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CSV registry home retired" in proc.stderr, proc.stderr
    assert "error(s) in docs/work" in proc.stderr, proc.stderr


# --- the git plumbing ---------------------------------------------------------


def git_repo(root):
    """A git runner over `root` whose commits can be stamped (`at=`), so every
    time compare below is deterministic (two commits in one wall-clock second
    would tie and prove nothing) — the `_staleness_git` pattern."""
    skip_without_env_gates("git")
    git = shutil.which("git")
    base = dict(os.environ)

    def run_git(*args, at=None):
        env = base
        if at is not None:
            env = dict(base)
            stamp = "@{} +0000".format(at)
            env["GIT_AUTHOR_DATE"] = stamp
            env["GIT_COMMITTER_DATE"] = stamp
        proc = subprocess.run(
            [git, "-C", str(root), *args], capture_output=True, text=True, env=env
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return proc.stdout

    run_git("init")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    return run_git


def git_move(root, run_git, src, dst):
    """`git mv`, creating the destination directory first: a status change in
    this registry moves a spec into a directory that need not exist yet, and
    `git mv` refuses a missing destination rather than creating one."""
    (root / dst).parent.mkdir(parents=True, exist_ok=True)
    run_git("mv", src, dst)


def test_status_at_head_comes_from_ls_tree_paths(tmp_path):
    """The HEAD status map reads the TREE LISTING, not the blobs: in this
    registry the directory IS the status, so one subprocess and no content read
    answers the whole question."""
    run_git = git_repo(tmp_path)
    write_spec(tmp_path, "queued", "WI-001")
    write_spec(tmp_path, "complete", "WI-002", order=1, deliverable="shipped")
    write_spec(tmp_path, "deferred", "WI-003", order=2)
    write_spec(tmp_path, "active/llm-x", "WI-004", order=3)
    write_spec(tmp_path, "cancelled", "WI-005", order=4, deliverable="never")
    write_spec(tmp_path, "draft", "WI-006", order=5)
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    head = ctraj._head_spec_status_map(tmp_path)
    # WI-005 is the case the tree listing could NOT answer before WI-384: the
    # two terminals shared `archive/` and were told apart by a frontmatter key,
    # which is a blob, so a HEAD-cancelled item read `done`. One directory per
    # state makes paths alone exact.
    assert {wid: v["status"] for wid, v in head.items()} == {
        "WI-001": "queued",
        "WI-002": "done",
        "WI-003": "deferred",
        "WI-004": "active",
        "WI-005": "cancelled",
        "WI-006": "draft",
    }
    # Paths alone cannot carry SR-Refs; the map says so rather than guessing.
    assert all(v["srs"] == [] for v in head.values())


def test_status_at_head_is_none_when_head_predates_the_folder(tmp_path):
    """The migration commit's own case — the caller falls back to the CSV at
    HEAD, so the whole registry does not read as newly-closed."""
    run_git = git_repo(tmp_path)
    write_csv(tmp_path, [{"WI-ID": "WI-001", "Title": "csv", "Status": "queued"}])
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    assert ctraj._head_spec_status_map(tmp_path) is None


def test_mutation_a_content_only_head_map_would_be_a_different_answer(tmp_path):
    """Drive the failure shape: rewrite one spec's BODY in the working tree
    without moving it. The HEAD map must be unchanged, because it reads paths —
    a map built from blobs would move."""
    run_git = git_repo(tmp_path)
    path = write_spec(tmp_path, "queued", "WI-001")
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    before = ctraj._head_spec_status_map(tmp_path)
    path.write_text(
        spec_text("WI-001", title="renamed in place", deliverable="x"),
        encoding="utf-8",
        newline="\n",
    )
    assert ctraj._head_spec_status_map(tmp_path) == before
    # ... and a MOVE does change it, so the guard is reading something.
    git_move(
        tmp_path,
        run_git,
        "docs/work/queued/WI-001-thing.md",
        "docs/work/complete/WI-001-thing.md",
    )
    run_git("commit", "-am", "close")
    assert ctraj._head_spec_status_map(tmp_path)["WI-001"]["status"] == "done"


def _staleness_repo(tmp_path):
    """A repo where WI-001 is filed at t=1000 and then MOVED (status change,
    nothing else) at t=2000 — the exact shape that must not re-date the row."""
    run_git = git_repo(tmp_path)
    write_spec(tmp_path, "queued", "WI-001", specref="docs/specs/WI-001.md")
    run_git("add", "-A")
    run_git("commit", "-m", "file WI-001", at=1000)
    git_move(
        tmp_path,
        run_git,
        "docs/work/queued/WI-001-thing.md",
        "docs/work/deferred/WI-001-thing.md",
    )
    run_git("commit", "-m", "defer WI-001", at=2000)
    return run_git


def test_a_status_move_does_not_reset_the_staleness_clock(tmp_path):
    _staleness_repo(tmp_path)
    work_dir = tmp_path / "docs" / "work"
    times = ctraj._spec_row_times(tmp_path, work_dir, ["WI-001"])
    assert times == {"WI-001": 1000}, times


def test_mutation_dropping_either_git_flag_resets_the_clock(tmp_path):
    """The measurement, kept executable. Neither `--follow` nor
    `--diff-filter=AM` alone gets the right answer — which is why the docstring
    on `_path_commit_time` names both, and why this is asserted rather than
    believed."""
    _staleness_repo(tmp_path)
    rel = "docs/work/deferred/WI-001-thing.md"
    assert ctraj._path_commit_time(tmp_path, rel, row_history=True) == 1000
    # --follow only (the plain call plus the flag by hand):
    follow_only = ctraj._git(
        tmp_path, ["log", "-1", "--format=%ct", "--follow", "--", rel]
    )
    assert int(follow_only.strip()) == 2000
    # --diff-filter only:
    filter_only = ctraj._git(
        tmp_path, ["log", "-1", "--format=%ct", "--diff-filter=AM", "--", rel]
    )
    assert int(filter_only.strip()) == 2000
    # ... and neither, which is the default the CSV path uses:
    assert ctraj._path_commit_time(tmp_path, rel) == 2000


def test_a_real_content_edit_does_redate_the_clock(tmp_path):
    """The other direction, or the guard above would be satisfied by a function
    that always answered "the first commit": editing the spec IS the driven look
    the warn asks for, and it must clear the warn.

    Note the FILENAME is unchanged here — that is the whole of the promise. The
    sibling below pins what happens when it is not."""
    run_git = _staleness_repo(tmp_path)
    (tmp_path / "docs" / "work" / "deferred" / "WI-001-thing.md").write_text(
        spec_text("WI-001", title="re-affirmed", specref="docs/specs/WI-001.md"),
        encoding="utf-8",
        newline="\n",
    )
    run_git("commit", "-am", "re-affirm WI-001", at=3000)
    times = ctraj._spec_row_times(tmp_path, tmp_path / "docs" / "work", ["WI-001"])
    assert times == {"WI-001": 3000}, times


def test_a_retitle_plus_content_edit_does_not_redate_the_clock(tmp_path):
    """WI-362, the ACCEPTED blind spot, asserted so that changing it is a
    deliberate act rather than a side effect.

    The Title drives the spec FILENAME, so re-titling a work item RENAMES its
    file — and `--diff-filter=AM` drops a rename whatever else the same commit
    did (git scores it `R<similarity>`, never `M`). A downstream author who
    re-affirms by re-titling therefore keeps the pre-edit clock and the warn does
    not clear. The owner ruled (2026-07-29) to state that in the warn text rather
    than build rename detection; if a later WI builds the detection, this
    assertion is the one it must consciously flip."""
    run_git = git_repo(tmp_path)
    write_spec(tmp_path, "queued", "WI-001", specref="docs/specs/WI-001.md")
    run_git("add", "-A")
    run_git("commit", "-m", "file WI-001", at=1000)
    git_move(
        tmp_path,
        run_git,
        "docs/work/queued/WI-001-thing.md",
        "docs/work/queued/WI-001-reaffirmed.md",
    )
    (tmp_path / "docs" / "work" / "queued" / "WI-001-reaffirmed.md").write_text(
        spec_text("WI-001", title="Reaffirmed", specref="docs/specs/WI-001.md"),
        encoding="utf-8",
        newline="\n",
    )
    run_git("add", "-A")
    run_git("commit", "-m", "re-title WI-001", at=3000)
    times = ctraj._spec_row_times(tmp_path, tmp_path / "docs" / "work", ["WI-001"])
    assert times == {"WI-001": 1000}, times
    # ... and the warn text a reader gets says so, so the blind spot is not
    # silent: it names the WI's own spec file (the file the clock actually
    # reads — review 2026-07-29 confirmed pointing at "the spec" sent readers
    # to the SpecRef target, which can never clear the warn) and the rename
    # rule, not "any reviewed edit".
    assert "the WI's own spec file under docs/work/" in ctraj.BACKLOG_REAFFIRM_HINT
    assert "keeping its filename" in ctraj.BACKLOG_REAFFIRM_HINT
    assert "rename does not re-date the clock" in ctraj.BACKLOG_REAFFIRM_HINT


def test_staleness_only_logs_the_rows_it_examines(tmp_path):
    """One `git log` per OPEN row, not per work item — the bounded-cost property
    the single `git blame` had, restated for a one-file-per-row registry."""
    _staleness_repo(tmp_path)
    times = ctraj._spec_row_times(tmp_path, tmp_path / "docs" / "work", [])
    assert times == {}


def test_backlog_staleness_reads_the_folder_registry_end_to_end(tmp_path):
    """The finding itself, in folder mode: a cited SR amended after the spec was
    last edited re-flags the work item."""
    run_git = git_repo(tmp_path)
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        SR_HEADER + "SR-001,A,SN-001,does X,R,AC,,M,Test,Drafted\n",
        encoding="utf-8",
        newline="\n",
    )
    write_spec(tmp_path, "queued", "WI-001", sr_refs=["SR-001"])
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=1000)
    (req / "system-requirements.csv").write_text(
        SR_HEADER + "SR-001,A,SN-001,does X and Y,R,AC,,M,Test,Drafted\n",
        encoding="utf-8",
        newline="\n",
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend SR-001", at=2000)
    rows = ctraj.read_registry_rows(csv_path(tmp_path))
    wis, _ = ctraj.load_wis(rows)
    findings = ctraj.backlog_staleness_findings(tmp_path, wis)
    assert findings and "WI-001: cites SR-001 amended after" in findings[0]
    # Mutation: re-affirm the way the warn text asks for — a content edit at the
    # SAME path (a dated frontmatter comment), leaving the Title and so the
    # filename alone — and the warn must clear.
    spec = tmp_path / "docs" / "work" / "queued" / "WI-001-thing.md"
    spec.write_text(
        spec.read_text(encoding="utf-8").replace(
            "+++\n", "+++\n# re-affirmed 2026-07-29\n", 1
        ),
        encoding="utf-8",
        newline="\n",
    )
    run_git("commit", "-am", "re-affirm", at=3000)
    assert ctraj.backlog_staleness_findings(tmp_path, wis) == []


def _closing_repo(tmp_path):
    """A repo whose HEAD has WI-001 done and WI-002 queued, with WI-002's spec
    STAGED as a move into complete/ — a closure, expressed as a rename."""
    run_git = git_repo(tmp_path)
    write_spec(
        tmp_path, "complete", "WI-001", sr_refs=["SR-001"], deliverable="shipped"
    )
    write_spec(tmp_path, "queued", "WI-002", order=1, sr_refs=["SR-001"])
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    git_move(
        tmp_path,
        run_git,
        "docs/work/queued/WI-002-thing.md",
        "docs/work/complete/WI-002-thing.md",
    )
    return run_git


def test_a_staged_rename_into_complete_reads_as_a_closure(tmp_path):
    _closing_repo(tmp_path)
    staged = ctraj._staged_wi_registry(tmp_path)
    assert staged is not None, "the staged move was not detected at all"
    _names, cur_map, head_map = staged
    assert cur_map["WI-002"]["status"] == "done"
    assert head_map["WI-002"]["status"] == "queued"
    assert [wid for wid, _cur in ctraj._newly_closed(cur_map, head_map)] == ["WI-002"]


def test_the_staged_scan_is_a_no_op_when_no_spec_is_staged(tmp_path):
    """Same repo, nothing staged under `docs/work` — the scan must say nothing
    rather than reporting every closed spec as newly closed."""
    run_git = git_repo(tmp_path)
    write_spec(tmp_path, "complete", "WI-001", deliverable="shipped")
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    (tmp_path / "unrelated.txt").write_text("x\n", encoding="utf-8", newline="\n")
    run_git("add", "unrelated.txt")
    assert ctraj._staged_wi_registry(tmp_path) is None


def test_head_srs_are_filled_from_the_working_tree(tmp_path):
    """`ls-tree` cannot see SR-Refs, so the HEAD map borrows them from the file
    on disk — which is the same file, unchanged, for every id this commit did
    not touch. Without this the follow-up ratchet would be vacuous in folder
    mode: a fail-open, and this repo's oldest lesson."""
    _closing_repo(tmp_path)
    _names, _cur, head_map = ctraj._staged_wi_registry(tmp_path)
    assert head_map["WI-001"]["srs"] == ["SR-001"]


def test_the_no_validation_delta_warn_still_fires_in_folder_mode(tmp_path):
    """End-to-end: closing WI-002 as a follow-up on SR-001 (already delivered by
    the done WI-001) without touching the validation chain must still warn."""
    run_git = _closing_repo(tmp_path)
    run_git("add", "-A")
    findings = ctraj.staged_findings(tmp_path)
    assert findings and "WI-002" in findings[0], findings
    assert "validation chain did not change" in findings[0]


def test_mutation_touching_the_chain_clears_the_folder_mode_warn(tmp_path):
    """The same close with a test file staged — the warn must go, or the guard
    above is just "this function returns a string"."""
    run_git = _closing_repo(tmp_path)
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_fix.py").write_text(
        "# covers the fix\n", encoding="utf-8", newline="\n"
    )
    run_git("add", "-A")
    assert ctraj.staged_findings(tmp_path) == []
