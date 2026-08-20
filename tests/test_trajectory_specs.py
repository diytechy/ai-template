"""check_trajectory.py — decision over spec bodies (WI-277: split verbatim
from tests/test_trajectory.py by behavior boundary).

The WI-349 cell-integrity (control-character) findings and the WI-352
completion reconciler: Done-when completion, the section boundary, the
warn-only trailer signal, the close-time half, and the signals deliberately
not reimplemented.
"""

import csv
import shutil
import subprocess


from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
)

wi_convert = load_script("wi_convert")


# The registry-fixture writers below are copied from tests/test_trajectory.py
# rather than imported — no test module in this suite imports another, and
# conftest is not this module's to extend (the suite idiom test_integrate.py's
# `git_repo` states; WI-277 kept it when splitting the monolith).
# The fixture bodies below stay CSV-SHAPED — one line per work item, cells in one
# of these two column orders — because a table is how a registry fixture reads.
# The registry's one HOME is the `docs/work/` spec folder (concurrency-restructure
# Phase 5, RULING-4: the CSV home retired, and a work-items.csv left on disk is
# now itself an integrity error), so the writers below map each line through the
# format's own writer instead of writing a CSV.
WI_COLUMNS = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable"
# ...plus the SpecRef + BlockRef columns (S1) — used by the SSOT-rule tests.
SR_WI_COLUMNS = WI_COLUMNS + ",SpecRef,BlockRef"

# `active/<branch>/` is the only status two levels deep and the branch is the
# integrator's, so a fixture writing an active row has to name one.
ACTIVE_BRANCH = "wi-fixture"


def _wi_rows(body, columns):
    """`body`'s lines as full 17-column registry rows, read with `csv` so a
    quoted cell parses exactly as it did when the body WAS the file."""
    names = columns.split(",")
    rows = []
    for cells in csv.reader(body.splitlines()):
        if not cells or not cells[0].strip():
            continue
        row = dict.fromkeys(wi_convert.COLUMNS, "")
        row.update(dict(zip(names, cells)))
        rows.append(row)
    return rows


def _write_spec_row(work, row, order):
    """Write one row as its spec file under `work`.

    Everything goes through `wi_convert`, the format's single writer — except the
    directory for an `active` row, which that writer deliberately does not know:
    the integrator's BRANCH names `active/<branch>/`, so a fixture supplies one
    and reuses the same renderer for the file itself."""
    if (row.get("Status") or "").strip() != "active":
        return wi_convert.write_spec_file(work, row, order=order)
    text = wi_convert.FENCE + "\n"
    text += wi_convert.render_frontmatter(wi_convert.frontmatter_pairs(row, order))
    text += wi_convert.FENCE + "\n"
    if row.get("Deliverable"):
        text += wi_convert.DELIVERABLE_PREFIX + row["Deliverable"] + "\n"
    path = work / "active" / ACTIVE_BRANCH / wi_convert.spec_filename(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def write_wis(root, body, columns=WI_COLUMNS):
    """Write the work-item registry — the `docs/work/` spec folder — from the
    CSV-shaped `body`, one spec file per line.

    The folder is REPLACED on every call: one call writes the whole registry, so
    a test that re-writes it (a status flip) MOVES the item's file rather than
    leaving a second copy in the old status directory. Two rows sharing an id
    stay two files (their titles differ, so their slugs do), which is what keeps
    the duplicate-id integrity error reachable."""
    work = root / "docs" / "work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for order, row in enumerate(_wi_rows(body, columns), 1):
        _write_spec_row(work, row, order)
    return root


def run_traj(root, *extra):
    return run_py([SCRIPTS / "check_trajectory.py", "--root", root, *extra], cwd=root)


def write_wis_sr(root, body):
    """`write_wis` for a `body` that also fills the SpecRef + BlockRef cells."""
    return write_wis(root, body, SR_WI_COLUMNS)


# --- WI-349: the cell-integrity rule, at the level where it still applies -------
#
# `cell_integrity_errors` was written for the assumption `staged_findings` made
# about the CSV home: one work-item row is one PHYSICAL line, so a cell holding a
# break silently mis-parses the line-wise diff. The four end-to-end guards that
# drove it through a written work-items.csv retired at concurrency-restructure
# Phase 5 with that home and that diff:
#
#   test_embedded_newline_in_a_cell_is_a_hard_error
#   test_the_same_row_without_the_newline_is_clean (its mutation twin)
#   test_a_carriage_return_in_a_cell_is_caught_too
#   test_a_broken_id_cell_is_reported_by_row_number (row NUMBER is a CSV position)
#
# Nothing reads the folder registry line-wise — a Deliverable body's newline is
# the format working as designed (test_wi_folder_loaders) — and `main()` no
# longer calls the check at all. The function survives for the spine CSVs, whose
# rows ARE lines, so the unit-level guards below stay: they call it directly on
# row dicts, which is exactly the reachable surface.


def test_every_other_check_passed_on_such_a_row_before_this_one(tmp_path):
    """The finding itself, pinned: the row is well-formed CSV and satisfies every
    OTHER rule, so before this check existed the validator reported clean. If this
    ever fails, `cell_integrity_errors` has started riding on some unrelated rule
    rather than on the newline — the vacuity that would make it worthless."""
    ct = load_script("check_trajectory")
    row = {
        "WI-ID": "WI-001",
        "Title": "two\nlines",
        "Workstream": "t",
        "SR-Refs": "",
        "Predecessors": "",
        "Status": "queued",
        "Deliverable": "",
        "SpecRef": "docs/log.md",
    }
    wis, integrity = ct.load_wis([row])
    assert integrity == [], integrity
    assert ct.validate(wis, set()) == []
    assert [f for f in ct.ssot_findings(wis, tmp_path) if f[1]] == []
    # ...and the new check is the one and only thing that catches it.
    assert len(ct.cell_integrity_errors([row])) == 1


def test_a_control_character_in_a_cell_is_caught(tmp_path):
    """WI-349 rework, after an adversarial review found a literal 0x08 that
    `9e2008a` had written into the live registry: a shell heredoc collapsed the
    backslash of a Windows path, so `Git` + BACKSPACE reached the Deliverable
    cell and every gate step passed over it. A control character is invisible in
    every editor and diff, so only a byte-level check can ever see one."""
    ct = load_script("check_trajectory")
    for code in (0x00, 0x08, 0x1B, 0x7F):
        row = {"WI-ID": "WI-001", "Title": "Git" + chr(code) + "in"}
        errs = ct.cell_integrity_errors([row])
        assert len(errs) == 1, (code, errs)
        assert "0x{:02X}".format(code) in errs[0], errs
        assert "Title cell" in errs[0], errs


def test_a_tab_is_not_a_control_finding(tmp_path):
    """The mutation twin that keeps the rule from being 'any byte under 0x20':
    a TAB is ordinary whitespace inside a quoted cell and breaks nothing."""
    ct = load_script("check_trajectory")
    assert ct.cell_integrity_errors([{"WI-ID": "WI-001", "Title": "a\tb"}]) == []


def test_a_break_is_reported_as_a_break_not_as_a_control_byte(tmp_path):
    """CR and LF are C0 controls too, so without the early return they would be
    reported twice under two different diagnoses — and the reader's next action
    differs between them."""
    ct = load_script("check_trajectory")
    errs = ct.cell_integrity_errors([{"WI-ID": "WI-001", "Title": "a\nb"}])
    assert (
        len(errs) == 1
        and "literal LF" in errs[0]
        and "control character" not in errs[0]
    )


def test_the_registry_this_repo_ships_is_control_character_clean(tmp_path):
    """The live registry, read as BYTES rather than through the loader — which is
    how the 0x08 was found and how it would have been missed again. Cheap, and it
    is the only test here that would have caught the real defect."""
    from conftest import ROOT

    # Phase 5: the live registry is the docs/work/ spec folder, its ONE home —
    # scan every spec's raw bytes, same instrument, same rule (0x09/0x0A/0x0D
    # allowed).
    sources = sorted((ROOT / "docs" / "work").rglob("WI-*.md"))
    assert sources, "the registry has no home at all"
    for path in sources:
        data = path.read_bytes()
        bad = sorted({b for b in data if b < 0x20 and b not in (0x09, 0x0A, 0x0D)})
        assert not bad, "control byte(s) in {}: {}".format(
            path.name, [hex(b) for b in bad]
        )


# --- WI-352: the completion reconciler -----------------------------------------
#
# Status stays an ATTESTATION (owner ruling 2026-07-28); what was missing is the
# RECONCILER every other declared-vs-computed pair here already has. Each signal
# below is driven against a CONSTRUCTED spec, and each has a twin proving it stays
# silent in the other direction — the three false-positive classes measured while
# building it (a shared spec, a sibling section, an archived spec) are pinned as
# hard as the findings themselves.


def _write_spec(root, name, body):
    specs = root / "docs" / "specs"
    specs.mkdir(parents=True, exist_ok=True)
    (specs / name).write_text(body, encoding="utf-8")
    return specs / name


DONE_WHEN_ALL_TICKED = "# WI-001\n\n## Done-when\n\n- [x] one\n- [x] two\n"
DONE_WHEN_SOME_OPEN = "# WI-001\n\n## Done-when\n\n- [x] one\n- [ ] two\n"


def test_open_row_whose_spec_reports_finished_warns(tmp_path):
    """The WI-328 shape: every Done-when box ticked, the row still open."""
    _write_spec(tmp_path, "WI-001.md", DONE_WHEN_ALL_TICKED)
    write_wis_sr(tmp_path, "WI-001,A,t,,,queued,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "completion WI-001: status=queued" in proc.stderr, proc.stderr
    assert "reports the work FINISHED" in proc.stderr


def test_open_row_whose_spec_reports_finished_errors_under_strict(tmp_path):
    """Gate tier: a contradiction between two homes for one fact cannot reach a
    green DevStg-Tests/DevStg-Impl, matching R-E/R-F."""
    _write_spec(tmp_path, "WI-001.md", DONE_WHEN_ALL_TICKED)
    write_wis_sr(tmp_path, "WI-001,A,t,,,queued,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ERROR - completion WI-001" in proc.stderr


def test_one_unticked_box_is_enough_to_stay_silent(tmp_path):
    """The mutation twin. Without it the finding above could be riding on the
    mere presence of a spec rather than on the box states."""
    _write_spec(tmp_path, "WI-001.md", DONE_WHEN_SOME_OPEN)
    write_wis_sr(tmp_path, "WI-001,A,t,,,queued,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "completion" not in proc.stderr


def test_a_spec_with_no_ticked_boxes_at_all_is_not_finished(tmp_path):
    """`ticked and not unticked` — an untouched spec has zero of each, and zero
    ticked must not read as done. This is the vacuity a bare `not unticked`
    would introduce."""
    _write_spec(tmp_path, "WI-001.md", "# WI-001\n\n## Done-when\n\n(nothing yet)\n")
    write_wis_sr(tmp_path, "WI-001,A,t,,,queued,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "completion" not in proc.stderr


def test_a_shared_spec_is_never_read_for_the_citing_wi(tmp_path):
    """MEASURED false positive, from the live repo: WI-324 (queued) cites
    docs/specs/WI-321.md, whose Done-when belongs to WI-321. Following SpecRef
    reported WI-324's work "FINISHED" out of ticks WI-321 had made. The
    reconciler reads a WI's OWN, name-identified spec only."""
    _write_spec(tmp_path, "WI-001.md", DONE_WHEN_ALL_TICKED)
    write_wis_sr(
        tmp_path,
        "WI-001,A,t,,,done,shipped,\nWI-002,B,t,,,queued,,docs/specs/WI-001.md\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WI-002" not in proc.stderr


def test_done_row_with_unticked_boxes_in_its_live_spec_warns(tmp_path):
    """The mirror direction — 40c92f6 exists because a box was ticked early."""
    _write_spec(tmp_path, "WI-001.md", DONE_WHEN_SOME_OPEN)
    write_wis_sr(tmp_path, "WI-001,A,t,,,done,shipped,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "completion WI-001: status=done" in proc.stderr, proc.stderr
    assert "1 unticked" in proc.stderr


def test_an_open_citer_suppresses_the_done_side(tmp_path):
    """A shared effort doc legitimately carries the citer's remaining boxes after
    its first owner closes — the same "no open citer" test R-F uses to decide
    when a spec may be archived."""
    _write_spec(tmp_path, "WI-001.md", DONE_WHEN_SOME_OPEN)
    write_wis_sr(
        tmp_path,
        "WI-001,A,t,,,done,shipped,\nWI-002,B,t,,,queued,,docs/specs/WI-001.md\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "completion" not in proc.stderr


def test_an_archived_spec_is_not_reported_by_the_standing_check(tmp_path):
    """SCOPING DECISION, pinned: run over the archive this produced 38 findings
    on the live repo, none actionable — a closed WI's record is its Deliverable
    and log entry, so the only remaining action is cosmetic, and a check whose
    recommended action is "nothing" is the wall of warns WI-308 recorded as how a
    check earns its own ignore. The close-time check owns that moment instead."""
    archive = tmp_path / "docs" / "archive" / "specs"
    archive.mkdir(parents=True, exist_ok=True)
    (archive / "WI-001.2026-01-01.md").write_text(DONE_WHEN_SOME_OPEN, encoding="utf-8")
    write_wis_sr(tmp_path, "WI-001,A,t,,,done,shipped,\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "completion" not in proc.stderr


# --- the Done-when SECTION boundary --------------------------------------------


def test_boxes_under_a_sibling_heading_are_not_done_when(tmp_path):
    """docs/specs/WI-321.md's real shape: its Done-when is followed by a sibling
    `## Split off, deliberately` holding ANOTHER WI's boxes. Folding those in
    would attribute one WI's unfinished work to another."""
    ct = load_script("check_trajectory")
    text = (
        "# WI-001\n\n## Done-when\n\n- [x] mine\n\n"
        "## Split off, deliberately\n\n- [ ] someone else's\n"
    )
    assert ct._done_when_boxes(text) == (1, 0)


def test_boxes_under_a_subheading_of_done_when_do_count(tmp_path):
    """The other half of the section rule: a Done-when that subdivides keeps its
    boxes, so the boundary is heading LEVEL, not merely the next heading."""
    ct = load_script("check_trajectory")
    text = "# WI-001\n\n## Done-when\n\n- [x] a\n\n### Sub\n\n- [ ] b\n"
    assert ct._done_when_boxes(text) == (1, 1)


def test_a_migration_checklist_is_not_completion_evidence(tmp_path):
    """Checkboxes outside a Done-when heading are STEPS, not evidence. Counting
    them would make a kit-version-bump doc read as an unfinished WI."""
    ct = load_script("check_trajectory")
    text = "# WI-001\n\n## Migration checklist\n\n- [ ] step one\n- [ ] step two\n"
    assert ct._done_when_boxes(text) == (0, 0)


def test_the_numbered_done_when_heading_form_is_recognised(tmp_path):
    """Older specs number their sections ("7. Done-when"), and "Done when"
    without the hyphen is in live use too."""
    ct = load_script("check_trajectory")
    assert ct._done_when_boxes("## 7. Done-when\n\n- [x] a\n") == (1, 0)
    assert ct._done_when_boxes("## Done when\n\n- [x] a\n") == (1, 0)


# --- the trailer signal: warn-only, and pinned as such -------------------------


def test_a_trailer_claiming_an_open_wi_warns(tmp_path):
    skip_without_env_gates("git")
    git = shutil.which("git")
    write_wis_sr(tmp_path, "WI-001,A,t,,,queued,,docs/log.md\n")
    (tmp_path / "docs" / "log.md").write_text("log\n", encoding="utf-8")
    for args in (
        ("init",),
        ("config", "user.email", "t@example.com"),
        ("config", "user.name", "T"),
        ("add", "-A"),
        ("commit", "-m", "build it\n\nWI: WI-001"),
    ):
        subprocess.run([git, "-C", str(tmp_path), *args], capture_output=True)
        if args == ("init",):
            pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "completion WI-001" in proc.stderr and "trailer" in proc.stderr


def test_the_trailer_signal_never_joins_the_exit_code(tmp_path):
    """DEVIATION from the WI row, pinned so it cannot be undone by accident. The
    row asks for ERROR under --strict; its own argument forbids it. A trailer
    means "a commit CLAIMS this WI", not "the work is right" — WI-336's code
    landed while its row CORRECTLY stayed queued, a review having refuted three
    of its claims. Erroring here would block the DevStg-Impl gate for the length of that
    rework, with no honest way out but a false close."""
    skip_without_env_gates("git")
    git = shutil.which("git")
    write_wis_sr(tmp_path, "WI-001,A,t,,,queued,,docs/log.md\n")
    (tmp_path / "docs" / "log.md").write_text("log\n", encoding="utf-8")
    for args in (
        ("init",),
        ("config", "user.email", "t@example.com"),
        ("config", "user.name", "T"),
        ("add", "-A"),
        ("commit", "-m", "build it\n\nWI: WI-001"),
    ):
        subprocess.run([git, "-C", str(tmp_path), *args], capture_output=True)
        if args == ("init",):
            pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN - completion WI-001" in proc.stderr
    assert "ERROR" not in proc.stderr


# --- the close-time half --------------------------------------------------------


def _staged_close_repo(tmp_path, spec_body):
    """A repo whose HEAD has WI-001 queued and whose INDEX closes it."""
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*a):
        return subprocess.run([git, "-C", str(tmp_path), *a], capture_output=True)

    _write_spec(tmp_path, "WI-001.md", spec_body)
    write_wis_sr(tmp_path, "WI-001,A,t,,,queued,,docs/specs/WI-001.md\n")
    run_git("init")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "open")
    write_wis_sr(tmp_path, "WI-001,A,t,,,done,shipped,\n")
    run_git("add", "-A")
    return run_git


def test_closing_a_wi_with_unticked_boxes_warns_at_commit_time(tmp_path):
    """The moment that matters: the spec is still live, the author is still in
    the change, and both homes can be made to agree in one commit. WI-334 closed
    2026-07-27 with five boxes never ticked and nothing said so."""
    _staged_close_repo(tmp_path, DONE_WHEN_SOME_OPEN)
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WI-001: this commit closes it" in proc.stderr, proc.stderr
    assert "1 unticked" in proc.stderr


def test_closing_a_wi_with_every_box_ticked_is_silent(tmp_path):
    """The twin — otherwise the warn above could fire on any close at all."""
    _staged_close_repo(tmp_path, DONE_WHEN_ALL_TICKED)
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "this commit closes it" not in proc.stderr


def test_the_close_time_check_is_a_no_op_off_git(tmp_path):
    """Same degradation as every other staged check — a gate run has no index."""
    ct = load_script("check_trajectory")
    assert ct.staged_completion_findings(tmp_path) == []


# --- the signal deliberately NOT reimplemented ---------------------------------


def test_done_with_an_empty_deliverable_is_already_r_a_and_is_not_duplicated(tmp_path):
    """The WI row asked for a fourth signal — a `done` row with an empty
    Deliverable. R-A already makes that a HARD error at every run, strictly
    stronger than this tier, so a second weaker copy would be the duplication the
    kit's working agreement forbids. Pinned here so the omission reads as a
    decision rather than a gap."""
    write_wis_sr(tmp_path, "WI-001,A,t,,,done,,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "R-A" in proc.stderr
    assert "completion" not in proc.stderr


def test_the_live_only_scope_is_load_bearing_not_vacuous():
    """130-REVIEW-A MAJOR 5: the two figures justifying WI-352's live-only scope
    were signed and wrong (38 vs the real 40; "258 of 282" vs 281 of 296). The
    first was measured against an EARLIER implementation and never re-measured
    after `_own_spec` changed — the measure-after-the-last-edit rule; the second
    was inferred rather than measured.

    The remedy is not a corrected number in prose, which rots the same way. It is
    this: the DESIGN CLAIM re-derived from the live repo on every run. Scoping the
    done-side check to live specs only matters if the archive would in fact
    produce findings, so assert that it does — with headroom, as a property rather
    than a freeze."""
    ct = load_script("check_trajectory")
    # Read through the validator's own registry loader (Phase 5: `docs/work/`,
    # derived from the path below), so the claim stays re-derivable from the
    # registry itself rather than from a second walk of the folder.
    rows = ct.read_registry_rows(ROOT / "docs" / "requirements" / "work-items.csv")
    status = {r["WI-ID"]: r["Status"].strip() for r in rows}
    archive = ROOT / "docs" / "archive" / "specs"
    findings = 0
    for path in sorted(archive.glob("*.md")):
        wid = path.name.split(".")[0]
        if status.get(wid) != "done":
            continue
        _ticked, unticked = ct._done_when_boxes(
            path.read_text(encoding="utf-8", errors="replace")
        )
        findings += bool(unticked)
    assert findings >= 10, (
        "only {} archived spec(s) would report unticked boxes — the live-only "
        "scope was justified by there being MANY unactionable archive findings, "
        "so if this has dropped near zero the scoping decision needs "
        "re-arguing".format(findings)
    )


def test_done_when_holds_the_overwhelming_majority_of_checkboxes():
    """The premise of the section rule, re-derived rather than quoted.

    If checkboxes stopped clustering under `Done-when`, scoping the tally to that
    section would start MISSING completion evidence instead of excluding
    migration checklists — so the premise is asserted, not asserted once in a
    docstring and left to rot."""
    import re as _re

    ct = load_script("check_trajectory")
    box = _re.compile(r"^\s*[-*]\s+\[[ xX]\]")
    inside = total = 0
    for folder in ("specs", "archive/specs"):
        for path in sorted((ROOT / "docs" / folder).glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            total += sum(1 for ln in text.splitlines() if box.match(ln))
            ticked, unticked = ct._done_when_boxes(text)
            inside += ticked + unticked
    assert total > 0, "no checkboxes at all — this guard has gone vacuous"
    assert inside * 10 >= total * 9, (
        "only {} of {} checkboxes sit under a Done-when heading; below ~90% the "
        "section rule stops being a filter and starts being a blind spot".format(
            inside, total
        )
    )
