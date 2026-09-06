"""check_trajectory.py — the work-item registry validator (Thread 52 phase 1).

The layer's whole value is what it blocks (cycles, dangling predecessors,
malformed/duplicate ids) *and* what it deliberately lets through: a
placeholder-only or absent registry is vacuously clean, a dangling SR ref only
warns (draft SRs are legitimate), and `docs/trajectory-check: off` silences the
check entirely. Each is pinned red/green by running the real script over a
minimal temp registry (no full scaffold needed — the validator reads the
`docs/work/` spec folder, which a fixture writes file by file).

WI-277 split this module by behavior boundary. What stays here is the parse +
decision core: graph validation, the R-A/R-E/R-F SSOT rules, SpecRef anchors,
the terminal `cancelled` status and status.md forward-only. The `--staged` git
effect and git-time recovery checks moved to tests/test_trajectory_staged.py,
the decisions over architecture inputs to tests/test_trajectory_arch.py, and the
decisions over spec bodies to tests/test_trajectory_specs.py.
"""

import csv
import difflib
import shutil


from conftest import ROOT, SCRIPTS, load_script, run_py

wi_convert = load_script("wi_convert")

# The fixture bodies below stay CSV-SHAPED — one line per work item, cells in one
# of these two column orders — because a table is how a registry fixture reads.
# The registry's one HOME is the `docs/work/` spec folder (concurrency-restructure
# Phase 5, RULING-4: the CSV home retired, and a work-items.csv left on disk is
# now itself an integrity error), so the writers below map each line through the
# format's own writer instead of writing a CSV.
WI_COLUMNS = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable"
# ...plus the SpecRef column (S1) — used by the SSOT-rule tests. (A BlockRef
# column retired with the blockref vocabulary at WI-553/OI-70.)
SR_WI_COLUMNS = WI_COLUMNS + ",SpecRef"
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)

PLACEHOLDER_ROW = (
    "WI-000,EXAMPLE - delete on first real entry,track-name,SR-000,,queued,demo\n"
)

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


def write_srs(root, *sr_ids):
    """Write a system-requirements.csv carrying just the given SR ids."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    rows = "".join(
        '{},Title,SN-001,"The system shall.",R,AC,,M,Test,Drafted\n'.format(s)
        for s in sr_ids
    )
    (req / "system-requirements.csv").write_text(SR_HEADER + rows, encoding="utf-8")


def run_traj(root, *extra):
    return run_py([SCRIPTS / "check_trajectory.py", "--root", root, *extra], cwd=root)


def write_wis_sr(root, body):
    """`write_wis` for a `body` that also fills the SpecRef cell."""
    return write_wis(root, body, SR_WI_COLUMNS)


def write_status(root, text):
    """Write docs/status.md (the forward-only working surface)."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "status.md").write_text(text, encoding="utf-8")


def write_spec(root, rel, *headings):
    """Create an in-repo spec file so a SpecRef resolves (R-E).

    `headings` become `##` sections, so a `path#anchor` SpecRef citing one of
    them resolves on BOTH halves (WI-354). A caller that passes none is testing
    the path half only and must not cite an anchor."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    body = "# spec\n" + "".join("\n## {}\n".format(h) for h in headings)
    p.write_text(body, encoding="utf-8")


# --- vacuous / opt-out: the layer costs a non-adopter nothing ------------------


def test_absent_registry_is_vacuously_clean(tmp_path):
    # No docs/work/ at all (a repo that never touched the layer) -> pass.
    (tmp_path / "docs" / "requirements").mkdir(parents=True)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "vacuously clean" in proc.stdout


def test_placeholder_only_is_vacuously_clean(tmp_path):
    # A fresh scaffold ships only the inert WI-000 example row -> pass.
    write_wis(tmp_path, PLACEHOLDER_ROW)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "vacuously clean" in proc.stdout


def test_opt_out_silences_even_a_broken_registry(tmp_path):
    # docs/trajectory-check `off` short-circuits before any validation, so even a
    # registry with a cycle passes — the deliberate exit for a repo that opts out.
    write_wis(
        tmp_path,
        "WI-001,A,t,,WI-002,queued,d\nWI-002,B,t,,WI-001,queued,d\n",
    )
    (tmp_path / "docs" / "trajectory-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "off" in proc.stdout


# --- a real graph validates -----------------------------------------------------


def test_valid_graph_passes(tmp_path):
    # A small acyclic DAG with mixed statuses. Open rows carry an EMPTY
    # Deliverable (R-A: filled only at close). No SR registry is written, so the
    # SR-ref warn is suppressed (the known_srs-empty guard) and it still passes.
    write_wis(
        tmp_path,
        "WI-001,Root,scripts,SR-001,,done,d\n"
        "WI-002,Mid,scripts,SR-001,WI-001,active,\n"
        "WI-003,Leaf,docs,SR-002,WI-001;WI-002,queued,\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "3 work item(s)" in proc.stdout
    assert "1 done" in proc.stdout
    assert "acyclic" in proc.stdout
    assert "not in the SR registry" not in proc.stderr  # no SR -> no dangling warn


# --- hard errors (exit 1) -------------------------------------------------------


def test_cycle_fails(tmp_path):
    write_wis(
        tmp_path,
        "WI-001,A,t,,WI-002,queued,d\nWI-002,B,t,,WI-001,queued,d\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 1
    assert "dependency cycle" in proc.stderr


def test_self_loop_is_a_cycle(tmp_path):
    write_wis(tmp_path, "WI-001,A,t,,WI-001,queued,d\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1
    assert "dependency cycle" in proc.stderr


def test_unresolved_predecessor_fails(tmp_path):
    write_wis(tmp_path, "WI-001,A,t,,WI-099,queued,d\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1
    assert "predecessor 'WI-099' is not a work item" in proc.stderr


def test_duplicate_id_fails(tmp_path):
    write_wis(
        tmp_path,
        "WI-001,A,t,,,queued,d\nWI-001,B,t,,,queued,d\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 1
    assert "duplicate work-item id WI-001" in proc.stderr


def test_malformed_id_fails(tmp_path):
    write_wis(tmp_path, "WI-abc,A,t,,,queued,d\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1
    assert "malformed work-item id" in proc.stderr


# --- soft (~) predecessor edges: advisory ordering, never a blocker --------------


def test_soft_predecessor_must_still_resolve(tmp_path):
    # A soft edge names a WI that must exist — advisory ordering to a phantom
    # node is a data error like any dangling predecessor.
    write_wis(tmp_path, "WI-001,A,t,,~WI-099,queued,d\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1
    assert "predecessor 'WI-099' is not a work item" in proc.stderr


def test_soft_only_cycle_warns_but_passes(tmp_path):
    # A cycle that closes only through soft edges is a hint conflict (WARN),
    # not an unstartable trajectory (the hard-edge acyclicity rule).
    write_wis(
        tmp_path,
        "WI-001,A,t,,~WI-002,queued,\nWI-002,B,t,,~WI-001,queued,\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "soft-edge cycle" in proc.stderr


def test_mixed_hard_soft_graph_passes(tmp_path):
    # A hard diamond with one soft ordering hint stays clean.
    write_wis(
        tmp_path,
        "WI-001,Root,scripts,,,done,d\n"
        "WI-002,Mid,scripts,,WI-001,active,\n"
        "WI-003,Leaf,docs,,WI-001;~WI-002,queued,\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "acyclic" in proc.stdout


# (test_legacy_track_header_still_read retired at concurrency-restructure
# Phase 5: a CSV *header* — legacy `Track` column and all — is not a thing the
# one registry home has. `load_wis` still reads `Track` as a Workstream
# fallback for a row dict, and test_wi_loader_sync pins the row contract the
# three readers share.)


# --- SR refs: warn (not fail) when the SR registry is present -------------------


def test_dangling_sr_ref_warns_but_passes(tmp_path):
    # The SR registry exists (SR-001) but a WI cites SR-999: a WARN on stderr, a
    # clean exit — a draft SR referenced ahead of its row is legitimate.
    write_wis(tmp_path, "WI-001,A,scripts,SR-999,,queued,\n")
    write_srs(tmp_path, "SR-001")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" in proc.stderr and "SR-999" in proc.stderr
    assert "clean" in proc.stdout


def test_known_sr_ref_does_not_warn(tmp_path):
    write_wis(tmp_path, "WI-001,A,scripts,SR-001,,done,d\n")
    write_srs(tmp_path, "SR-001")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" not in proc.stderr


# --- Title length (WI-479, M-03): warn (never fail), open-only, summarised ------


def test_overlong_open_title_warns_but_passes(tmp_path):
    # A queued (open) WI with a Title past the concise-label bound: a WARN on
    # stderr naming the id and its length, a clean exit — never a failure and
    # never a rewrite of the cell.
    long_title = "T" * 150
    write_wis(tmp_path, "WI-001,{},t,,,queued,\n".format(long_title))
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" in proc.stderr
    assert "carry a Title over" in proc.stderr
    assert "WI-001 (150 chars)" in proc.stderr


def test_concise_open_title_does_not_warn(tmp_path):
    write_wis(tmp_path, "WI-001,Short title,t,,,queued,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "carry a Title over" not in proc.stderr


def test_overlong_closed_title_is_excluded_as_historical(tmp_path):
    # A `done` row keeps its long Title forever (a historical record) — this
    # advisory is scoped to OPEN_STATUSES and never asks anyone to reword it.
    long_title = "T" * 150
    write_wis(tmp_path, "WI-001,{},t,,,done,shipped\n".format(long_title))
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "carry a Title over" not in proc.stderr


def test_many_overlong_open_titles_summarise_to_one_line(tmp_path):
    # Six open WIs over the bound produce ONE warn line naming the count and
    # the first five (worst-first) — never one line per row (the IF-coverage
    # rule elsewhere in check_trajectory.py sets this precedent).
    rows = "".join(
        "WI-{:03d},{},t,,,queued,\n".format(n, "T" * (130 + n)) for n in range(1, 7)
    )
    write_wis(tmp_path, rows)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stderr.count("carry a Title over") == 1
    assert "6 open work item(s)" in proc.stderr
    assert "(first 5 shown)" in proc.stderr


# --- tolerant of messy input ----------------------------------------------------


# (test_blank_or_non_wi_rows_are_ignored retired at concurrency-restructure
# Phase 5: a blank-id ROW is a CSV shape. Its folder-home counterpart is not a
# tolerance but a REFUSAL — a spec whose frontmatter carries no `id` is a
# malformed spec the validator names (test_wi_folder_loaders) — while the
# tolerance that does survive, a non-`WI-*.md` file in the registry folder, is
# `spec_files`' own contract, pinned there too.)


def test_comment_only_toggle_reads_on(tmp_path):
    # docs/trajectory-check holding only a comment has no declared line, so it
    # reads on (the safe default) — the check runs rather than silently skipping.
    write_wis(tmp_path, "WI-001,A,t,,WI-002,queued,d\nWI-002,B,t,,WI-001,queued,d\n")
    (tmp_path / "docs" / "trajectory-check").write_text(
        "# opts out with the one word off\n", encoding="utf-8"
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 1  # the cycle is caught: comment-only != off
    assert "dependency cycle" in proc.stderr


# --- F4: deep graphs fail on their merits, never with RecursionError -----------


def _chain(n, closed=False):
    """A chain WI-0001 -> WI-0002 -> ... -> WI-{n}, each depending on the NEXT so
    a DFS from the first row descends the whole depth (what crashed the former
    recursive walk). `closed` makes WI-{n} point back at WI-0001 -> one long
    cycle."""
    rows = []
    for k in range(1, n + 1):
        pred = "WI-{:04d}".format(k + 1) if k < n else ("WI-0001" if closed else "")
        # `done,d` keeps every row SSOT-compliant (R-A: Deliverable iff done), so
        # the deep-graph behavior under test is isolated from the coherence rules.
        rows.append("WI-{:04d},step,scripts,,{},done,d".format(k, pred))
    return "\n".join(rows) + "\n"


def test_deep_acyclic_chain_validates_without_recursionerror(tmp_path):
    # A dependency chain far deeper than CPython's ~1000-frame limit is acyclic,
    # so it must validate clean — the old recursive cycle-DFS raised RecursionError.
    write_wis(tmp_path, _chain(3000))
    proc = run_traj(tmp_path)
    assert "RecursionError" not in proc.stderr, proc.stderr
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_deep_cycle_reported_cleanly_not_recursionerror(tmp_path):
    # The same depth closed into one long cycle is reported as a dependency cycle
    # (clean exit 1), not crashed with a raw traceback.
    write_wis(tmp_path, _chain(3000, closed=True))
    proc = run_traj(tmp_path)
    assert "RecursionError" not in proc.stderr, proc.stderr
    assert proc.returncode == 1
    assert "dependency cycle" in proc.stderr


# --- S1: the registry SSOT rules -----------------------------------------------
# R-A is a hard error at every run (the pre-commit floor); R-E warns plain and
# gates under --strict; the vocabulary gains `deferred`. R-B/R-C (open-WI status
# repetition) stay retired (WI-180); R-D's done-id rule is RESTORED mode-aware
# (WI-200) — its own test block below.


def test_ra_open_wi_with_deliverable_fails_plain(tmp_path):
    # R-A: an open WI's Deliverable is filled only at close — a filled one on an
    # open row is an incoherent handoff, a hard error even without --strict.
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,queued,shipped it,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "R-A" in proc.stderr and "Deliverable is non-empty" in proc.stderr


def test_ra_done_wi_with_empty_deliverable_fails_plain(tmp_path):
    # R-A: a done WI must record what shipped — an empty Deliverable is a hard
    # error, the mirror of the open case.
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,done,,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "R-A" in proc.stderr and "Deliverable is empty" in proc.stderr


def test_deferred_status_is_first_class(tmp_path):
    # `deferred` is a known open state: empty Deliverable + a resolvable SpecRef
    # passes clean, with no unknown-status lint.
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,deferred,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "clean" in proc.stdout
    assert "unknown status" not in proc.stderr


def test_blocked_is_a_queued_spec_carrying_a_blockref(tmp_path):
    # Phase 5 / §7: `blocked` is no longer a status. A parked WI is a QUEUED spec
    # whose `blockref` names what must clear, and the blocked disposition is
    # DERIVED (the scheduler's readiness, gen_trajectory's rendering) — so the
    # evidence rides along and the validator judges an ordinary open row: empty
    # Deliverable + resolvable SpecRef passes --strict with no lint.
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,queued,,docs/specs/WI-001.md,OI-7\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "unknown status" not in proc.stderr
    assert "blocked" not in proc.stderr


# (test_blocked_status_requires_blockref and
# test_unknown_status_warns_plain_fails_strict retired at concurrency-restructure
# Phase 5: both drove a Status CELL the one registry home cannot hold. Status is
# now the spec's DIRECTORY, so `blocked` and `paused` alike are unwritable — an
# undeclared directory is refused by the loader and named as a malformed spec
# (test_wi_folder_loaders::test_an_unknown_status_directory_is_refused_not_bucketed),
# which is a hard error at every run rather than this warn-first lint. The
# `status-vocab` and `blocked-ref` rules in `ssot_findings` are consequently
# unreachable from the registry — reported as a production finding, not patched
# around here.)


def test_re_empty_specref_warns_plain_fails_strict(tmp_path):
    # R-E: an open WI must name a SpecRef — warn plain, ERROR under --strict.
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,active,,\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "R-E WI-001" in plain.stderr and "no SpecRef" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "R-E WI-001" in strict.stderr


def test_re_dangling_specref_warns_plain_fails_strict(tmp_path):
    # R-E: a SpecRef whose path part does not exist in the repo is dangling.
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,active,,docs/specs/WI-999.md#gone\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "does not resolve" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "R-E WI-001" in strict.stderr


def test_specref_with_anchor_resolves(tmp_path):
    # A `path#anchor` SpecRef whose anchor really is a heading is clean on BOTH
    # halves. Until WI-354 this test cited a heading the file did not have and
    # still passed, because R-E read only the path — the assertion pinned the
    # very gap the rule now closes, so it is the positive case now.
    write_spec(tmp_path, "docs/specs/effort.md", "S1 — first slice")
    write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,queued,,docs/specs/effort.md#s1--first-slice\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_specref_anchor_that_names_no_heading_warns_plain_fails_strict(tmp_path):
    # WI-354: the anchor half of R-E. The path exists, so the pre-WI-354 rule saw
    # nothing; the heading does not, so the citation is not actually traceable.
    # Same warn-plain / error-under---strict tier as the rest of R-E.
    write_spec(tmp_path, "docs/specs/effort.md", "S1 — first slice")
    write_wis_sr(
        tmp_path, "WI-001,A,scripts,,,queued,,docs/specs/effort.md#s9--no-such\n"
    )
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "R-E WI-001" in plain.stderr and "names no such heading" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "R-E WI-001" in strict.stderr


def _need_registry(root):
    p = root / "docs" / "requirements" / "stakeholder-needs.toml"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('[need.SN-1]\nneed = "one"\n', encoding="utf-8")


def test_specref_on_a_registry_carrier_resolves_a_bare_row_id(tmp_path):
    # 2026-09-06: the dual-plan composer refuses any need-carrier fragment that
    # is not an exact row id, so R-E must hold the same line at the commit bar.
    _need_registry(tmp_path)
    write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,queued,,docs/requirements/stakeholder-needs.toml#SN-1\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_specref_table_path_fragment_on_a_registry_is_a_finding(tmp_path):
    # `#need.SN-1` is the literal TOML table path — a natural spelling that used
    # to pass R-E (any fragment on a .toml target was "unknown") and then page
    # the planning round at draw time. The finding names the accepted spelling.
    _need_registry(tmp_path)
    write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,queued,,docs/requirements/stakeholder-needs.toml#need.SN-1\n",
    )
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "R-E WI-001" in plain.stderr and "did you mean #SN-1?" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    unknown = write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,queued,,docs/requirements/stakeholder-needs.toml#SN-9\n",
    )
    del unknown
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "names no such row" in strict.stderr, strict.stderr


def test_specref_anchor_report_names_the_nearest_heading(tmp_path):
    # The finding must be ACTIONABLE, not merely true: a wrong anchor is nearly
    # always stale or TRUNCATED rather than invented (WI-326 cited a truncated
    # docs/log.md slug for two days), so the report names the near miss. difflib
    # alone scores a short prefix of a long slug poorly, which is exactly that
    # shape, so `nearest_anchor` prefers a prefix relation first.
    write_spec(tmp_path, "docs/specs/effort.md", "S1 first slice with a long tail")
    write_wis_sr(
        tmp_path, "WI-001,A,scripts,,,queued,,docs/specs/effort.md#s1-first-slice\n"
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 1
    assert "did you mean #s1-first-slice-with-a-long-tail?" in proc.stderr, proc.stderr


def test_nearest_anchor_prefix_pass_beats_difflib_on_a_severe_truncation():
    """The prefix pass must EARN its place, measured — not asserted.

    131-REVIEW-A MINOR 5 refuted the original rationale by deleting the branch and
    watching every test stay green: WI-326's own 44-of-76-char truncation scores
    0.733 and plain difflib finds it unaided. The branch survives because a
    SEVERER truncation defeats difflib outright, and this pins that exact pair, so
    deleting the branch now fails and the docstring cannot rot back into the
    over-claim."""
    ct = load_script("check_trajectory")
    full = "2026-07-26--wi-326-a-green-that-hid-47-tests-caught-by-not-trusting"
    anchors = frozenset({full, "decisions-log", "audit-log", "gate-sign-offs"})

    mild = "2026-07-26--wi-326-a-green-that-hid-47-tests"
    assert difflib.get_close_matches(mild, sorted(anchors), n=1, cutoff=0.6) == [full]

    severe = "2026-07-26--wi-326"
    assert difflib.get_close_matches(severe, sorted(anchors), n=1, cutoff=0.6) == []
    assert ct.nearest_anchor(severe, anchors) == full


def _wi_row(wid, preds="", status="queued"):
    return {
        "WI-ID": wid,
        "Title": wid,
        "Workstream": "scripts",
        "Status": status,
        "Predecessors": preds,
        "SR-Refs": "",
        "SpecRef": "",
        "Deliverable": "",
        "BlockRef": "",
    }


def test_oi_predecessor_resolves_against_the_open_items_registry():
    # OI-73 arm 5: an `OI-###` in Predecessors is a hard edge on an open-item
    # ruling, split out of the WI graph and resolved against the open-items
    # registry — a known OI is clean, an unknown one is a dangling-edge ERROR
    # (the same class as an unknown WI predecessor), never a WI-graph cycle node.
    ct = load_script("check_trajectory")
    wis, _integrity = ct.load_wis([_wi_row("WI-001", preds="OI-70")])
    assert wis[0]["preds"] == [] and wis[0]["oi_preds"] == ["OI-70"]
    assert ct.validate(wis, frozenset(), frozenset({"OI-70"})) == []
    errs = ct.validate(wis, frozenset(), frozenset())
    assert any("OI-70" in e and "not a minted open item" in e for e in errs)


def test_oi_predecessor_is_never_a_dependency_cycle_node():
    # An open item is not a WI node, so a self-referential-looking edge through
    # an OI can never be reported as a cycle — the acyclicity set is WI-only.
    ct = load_script("check_trajectory")
    wis, _ = ct.load_wis(
        [_wi_row("WI-001", preds="OI-70"), _wi_row("WI-002", preds="WI-001")]
    )
    errs = ct.validate(wis, frozenset(), frozenset({"OI-70"}))
    assert not any("cycle" in e for e in errs)


def test_specref_with_no_path_is_a_finding(tmp_path):
    # 131-REVIEW-A BLOCKER 1: a bare `#anchor` names no document, so nothing can
    # resolve it. This returned CLEAN both before and after WI-354 — the one shape
    # that made "both halves resolve" untrue as written.
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,queued,,#totally-invented\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "R-E WI-001" in plain.stderr and "has no path" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1


def test_specref_naming_a_directory_is_a_finding(tmp_path):
    # Same review: `exists()` is true for a directory, so one resolved clean.
    (tmp_path / "docs" / "specs").mkdir(parents=True, exist_ok=True)
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,queued,,docs/specs\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "names a directory" in strict.stderr, strict.stderr


def test_specref_and_markdown_link_agree_on_the_same_anchor(tmp_path):
    """The WI-354 design claim, as a property rather than a comment: the SAME
    reference must not pass in one home and fail in the other.

    Before WI-354 a truncated anchor was an error as a LINK (check_docs) and
    invisible as a SpecRef (check_trajectory), which is how WI-326's ref survived
    two days. The anchor set now comes from check_docs.parse_doc, so this asserts
    the two homes agree on a heading whose slug is non-trivial — em dash, code
    span and punctuation all normalize — in BOTH directions, and in mixed CASE."""
    cd = load_script("check_docs")
    heading = "S1 — the `--strict` slice, part 2"
    write_spec(tmp_path, "docs/specs/effort.md", heading)
    # Ground truth is the anchor set the DOC exposes, read back with check_docs'
    # own parser — never a hand-written literal, which would assert my arithmetic
    # about em dashes rather than the agreement between the two homes.
    anchors = cd.parse_doc(tmp_path / "docs" / "specs" / "effort.md")["anchors"]
    (slug,) = [a for a in anchors if a != "spec"]
    # The subtlety that made a hand-written literal wrong twice, now ASSERTED
    # rather than described (131-REVIEW-A MINOR 7: the docstring named a code
    # span the fixture did not contain): parse_doc strips inline code spans over
    # the whole document BEFORE slugifying headings, so slugify(raw heading) is
    # NOT the anchor whenever the heading carries one.
    assert cd.slugify(heading) != slug, (cd.slugify(heading), slug)

    def homes(anchor):
        (tmp_path / "docs" / "citer.md").write_text(
            "# citer\n\n[ref](specs/effort.md#{})\n".format(anchor), encoding="utf-8"
        )
        write_wis_sr(
            tmp_path,
            "WI-001,A,scripts,,,queued,,docs/specs/effort.md#{}\n".format(anchor),
        )
        docs = run_py([SCRIPTS / "check_docs.py", "--root", tmp_path], cwd=tmp_path)
        traj = run_traj(tmp_path, "--strict")
        return (
            "no such anchor" in (docs.stdout + docs.stderr),
            "names no such heading" in (traj.stdout + traj.stderr),
        )

    # The real slug: neither home objects.
    assert homes(slug) == (False, False)
    # MIXED CASE of the real slug: check_docs compares fragments lowercased, so
    # neither home may object. This is the case that KILLS the mutation
    # 131-REVIEW-A MAJOR 2 drove: dropping `frag.lower()` in specref_findings
    # survived all five original tests while making check_trajectory reject an
    # anchor check_docs accepts — reopening the exact cross-home disagreement
    # this test exists to prevent.
    assert homes(slug.upper()) == (False, False)
    assert homes(slug.capitalize()) == (False, False)
    # Truncated (the WI-326 shape) and plain wrong: BOTH homes object.
    assert homes(slug[:12]) == (True, True)
    assert homes("totally-invented") == (True, True)


def test_specref_anchor_on_a_non_markdown_target_is_not_judged(tmp_path):
    # Anchors are a markdown concept. A SpecRef into a non-markdown in-repo file
    # keeps the pre-WI-354 path-only behaviour rather than inventing a finding.
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "gate").write_text("DevStg-Impl\n", encoding="utf-8")
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,queued,,docs/gate#anything\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_rf_done_wi_with_specref_warns_plain_fails_strict(tmp_path):
    # R-F (WI-251): close clears the SpecRef — a done row still carrying one is
    # the close-side incoherence R-E's open half never saw. Warn plain, ERROR
    # under --strict. The spec file itself is also flagged (no open citer).
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,done,shipped it,docs/specs/WI-001.md\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "R-F WI-001" in plain.stderr and "still set" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "R-F WI-001" in strict.stderr


def test_rf_orphan_live_spec_warns_plain_fails_strict(tmp_path):
    # R-F: a live docs/specs file no open WI cites belongs in the archive — the
    # residue rot the sweep clears must not silently re-grow.
    write_spec(tmp_path, "docs/specs/WI-009.md")
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,done,shipped it,\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "docs/specs/WI-009.md" in plain.stderr and "no open WI" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1


def test_rf_shared_doc_lives_while_any_open_citer_remains(tmp_path):
    # R-F negative: a shared effort doc archives only at its LAST open citer's
    # close — a deferred WI is open, so the doc (cited via #anchor) stays live
    # even though a done sibling once shipped from it (SpecRef duly cleared).
    write_spec(tmp_path, "docs/specs/effort.md", "s2")
    write_wis_sr(
        tmp_path,
        "WI-001,Done half,scripts,,,done,shipped it,\n"
        "WI-002,Parked half,scripts,,,deferred,,docs/specs/effort.md#s2\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_rf_scaffold_boilerplate_excluded(tmp_path):
    # R-F negative: the scaffolded README + -000 exemplar are permanent (the
    # WI-251 banner fix) and never read as archivable residue — a fresh scaffold
    # stays vacuously green.
    write_spec(tmp_path, "docs/specs/README.md")
    write_spec(tmp_path, "docs/specs/WI-000.md")
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,done,shipped it,\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- WI-267: the terminal `cancelled` status ----------------------------------
# `cancelled` (spelled `retired` until WI-384 gave it its own directory and an
# unambiguous name) is a WON'T-BUILD row that stays in the registry forever with
# its reason in `Deliverable` and an empty `SpecRef` — terminal like `done`, NOT
# an overload of it. It is a valid status (no unknown-status lint), counted
# separately, and validated by R-A (Deliverable = the reason) + R-F (SpecRef
# cleared). A live WI hard-depending on a cancelled one surfaces (dead-dep).


def test_cancelled_status_is_first_class(tmp_path):
    # A well-formed cancelled row: filled Deliverable (the reason), empty
    # SpecRef. Valid under --strict: no unknown-status lint, no R-A/R-E/R-F.
    write_wis_sr(tmp_path, "WI-001,Dropped,scripts,,,cancelled,superseded by WI-050,\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "unknown status" not in proc.stderr
    assert "R-A" not in proc.stderr and "R-F" not in proc.stderr


def test_cancelled_is_counted_separately_not_as_done(tmp_path):
    # The clean-summary counts cancelled apart from done: 1 done + 1 cancelled
    # over 2 rows is "1 done (50%)" plus a "1 cancelled" note (never 2 done).
    write_wis_sr(
        tmp_path,
        "WI-001,Shipped,scripts,,,done,shipped it,\n"
        "WI-002,Dropped,scripts,,,cancelled,not worth it,\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 done (50%)" in proc.stdout
    assert "1 cancelled" in proc.stdout


def test_cancelled_wi_with_empty_deliverable_fails_ra(tmp_path):
    # R-A: a cancelled row must record WHY it will not be built — an empty
    # Deliverable is the same hard error as an empty one on a done row.
    write_wis_sr(tmp_path, "WI-001,Dropped,scripts,,,cancelled,,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "R-A" in proc.stderr and "Deliverable is empty" in proc.stderr


def test_cancelled_wi_with_specref_fails_rf(tmp_path):
    # R-F: cancellation is terminal — the SpecRef is cleared. A cancelled row
    # still carrying one is flagged like a done row (warn plain, ERROR strict).
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Dropped,scripts,,,cancelled,superseded,docs/specs/WI-001.md\n",
    )
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "R-F WI-001" in plain.stderr and "still set" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "R-F WI-001" in strict.stderr


def test_a_draft_wi_is_open_and_valid(tmp_path):
    # WI-384: `draft` is an OPEN status — non-terminal, so R-A wants an EMPTY
    # Deliverable, and R-E wants a resolvable SpecRef. It is a first-class
    # status word (no unknown-status lint) precisely because the directory that
    # produces it is declared; that declaration is what reserves its id.
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(
        tmp_path, "WI-001,Still thinking,scripts,,,draft,,docs/specs/WI-001.md\n"
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "unknown status" not in proc.stderr
    assert "R-A" not in proc.stderr and "R-E" not in proc.stderr


def test_a_draft_wi_with_a_filled_deliverable_fails_ra(tmp_path):
    # The other half: `draft` is open, so a filled Deliverable is the same hard
    # R-A error it is on any other open row — the backward record is filled at
    # close, and a draft has not closed anything.
    write_wis_sr(tmp_path, "WI-001,Still thinking,scripts,,,draft,already?,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "R-A" in proc.stderr and "open" in proc.stderr


def test_open_wi_depending_on_cancelled_pred_is_flagged(tmp_path):
    # Decision 3 (dead-dep): a live WI whose hard predecessor is cancelled can
    # never become ready — surfaced (warn plain, ERROR under --strict) so the
    # owner re-homes or cancels it, rather than waiting forever.
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Dropped,scripts,,,cancelled,superseded,\n"
        "WI-002,Live,scripts,,WI-001,queued,,docs/specs/WI-002.md\n",
    )
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "dead-dep WI-002" in plain.stderr
    assert "terminal WI(s) WI-001" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "dead-dep WI-002" in strict.stderr


def test_open_wi_depending_on_partial_pred_is_flagged(tmp_path):
    # OI-73 arm 6: `partial` is as terminal to the scheduler as `cancelled` — a
    # lane that stopped early moves its spec to partial/ and never integrates
    # `done`, so a live WI hard-depending on one waits forever. This was the
    # WI-541 -> WI-540 strand repaired by hand; the finding now reports it.
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Stopped,scripts,,,partial,stopped early,\n"
        "WI-002,Live,scripts,,WI-001,queued,,docs/specs/WI-002.md\n",
    )
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "dead-dep WI-002" in plain.stderr
    assert "terminal WI(s) WI-001" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1


def test_done_predecessor_of_open_wi_is_not_a_dead_dep(tmp_path):
    # Decision 3 control: a `done` predecessor is a LIVE, satisfied edge — never
    # flagged dead. Only a terminal (cancelled/partial) predecessor triggers it.
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Shipped,scripts,,,done,shipped it,\n"
        "WI-002,Live,scripts,,WI-001,queued,,docs/specs/WI-002.md\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "dead-dep" not in proc.stderr


def test_cancelled_id_in_status_md_is_not_forward_only_finding(tmp_path):
    # Confirmed-no-change: the forward-only rule (WI-200) flags only `done` ids
    # (completed work whose record moved to log.md). A cancelled row's reason
    # lives permanently in the registry, so — like a deferred id — a cancelled id
    # may be referenced in status.md prose without tripping the rule.
    write_wis_sr(tmp_path, "WI-001,Dropped,scripts,,,cancelled,superseded,\n")
    write_status(tmp_path, "## Note\n- WI-001 cancelled: superseded, see the log.\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "forward-only" not in proc.stderr


def test_compliant_registry_and_status_passes_strict(tmp_path):
    # The whole model, coherent: a done row with a Deliverable and no SpecRef, an
    # open row with an empty Deliverable + resolvable SpecRef -> --strict is fully
    # green (R-A + R-E). status.md names only the open WI-002, so the restored
    # R-D done-id rule (WI-200) finds nothing (R-B/R-C stay retired, WI-180).
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Done thing,scripts,SR-001,,done,shipped it,\n"
        "WI-002,Next thing,scripts,SR-002,WI-001,active,,docs/specs/WI-002.md\n",
    )
    write_srs(tmp_path, "SR-001", "SR-002")
    write_status(tmp_path, "## Next action\n- WI-002 — build the next thing.\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "clean" in proc.stdout


def test_coherent_registry_passes_strict_without_status_md(tmp_path):
    # status.md is absent, so the restored R-D done-id rule (WI-200) is vacuous
    # and R-B/R-C stay retired (WI-180): a coherent registry (R-A clean, every
    # open WI's SpecRef resolves) passes --strict, and those rules never surface.
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,active,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for rule in ("R-B", "R-C", "R-D"):
        assert rule not in proc.stderr


# (test_run_state_end_state_warns_for_actionable_queue_and_fails_strict and
# test_run_state_check_is_vacuous_without_file_and_for_done_empty_queue retired
# at concurrency-restructure Phase 5 with `run_state_findings` itself: the
# WI-115 stale-end-state warn read `docs/run-state`, which left with the
# dispatcher that wrote it, so a stale parked state is now unrepresentable. The
# vacuity half went with it rather than being left to pass on a check that no
# longer exists.)


def test_placeholder_only_stays_vacuous_under_strict(tmp_path):
    # The opt-out promise holds under --strict too: a fresh scaffold's inert
    # WI-000 row triggers no SSOT finding.
    write_wis(tmp_path, PLACEHOLDER_ROW)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "vacuously clean" in proc.stdout


# --- WI-200: status.md forward-only (the mode-aware R-D restoration) -----------
# A `done` WI id token in a hand-edited status.md is a finding — WARN plain,
# ERROR under --strict — that yields to a generated-snapshot marker. It shares the
# trajectory-check opt-out and the placeholder/absent-registry vacuity.
GENERATED_MARKER = "<!-- BEGIN GENERATED TRAJECTORY SNAPSHOT -->"
FORWARD_ONLY = "status.md is forward-only"


def test_clean_status_has_no_forward_only_finding(tmp_path):
    # A done WI whose id is NOT echoed in status.md is clean (the file names only
    # the open work ahead), under --strict too.
    write_wis_sr(tmp_path, "WI-001,Shipped,scripts,,,done,shipped it,\n")
    write_status(tmp_path, "## Next action\n- everything closed; await the owner.\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert FORWARD_ONLY not in proc.stderr


def test_done_id_in_status_warns_plain_errors_strict(tmp_path):
    # A closed WI id lingering in status.md: WARN plain (exit 0), ERROR --strict.
    write_wis_sr(tmp_path, "WI-001,Shipped,scripts,,,done,shipped it,\n")
    write_status(tmp_path, "## Recently closed\n- WI-001 landed the thing.\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "WARN" in plain.stderr and FORWARD_ONLY in plain.stderr
    assert "WI-001" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert "ERROR" in strict.stderr and FORWARD_ONLY in strict.stderr
    assert "WI-001" in strict.stderr


def test_open_ids_in_status_are_not_a_finding(tmp_path):
    # queued/active/deferred ids are legal in status.md (they ARE the next work);
    # only `done` ids flag. A done id absent from the file stays silent.
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_spec(tmp_path, "docs/specs/WI-003.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Shipped,scripts,,,done,shipped it,\n"
        "WI-002,Next,scripts,,,queued,,docs/specs/WI-002.md\n"
        "WI-003,Later,scripts,,,deferred,,docs/specs/WI-003.md\n",
    )
    write_status(tmp_path, "Next: WI-002; deferred backlog: WI-003.\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert FORWARD_ONLY not in proc.stderr


def test_generated_marker_stands_the_rule_down(tmp_path):
    # A done id INSIDE a generated block does not flag: the block is spliced by
    # gen_trajectory --status and its freshness is the status-map byte-compare
    # step's job, so the token rule yields there (and only there — see the
    # sibling test below).
    write_wis_sr(tmp_path, "WI-001,Shipped,scripts,,,done,shipped it,\n")
    write_status(
        tmp_path,
        GENERATED_MARKER + "\n- WI-001 (from the registry snapshot)\n"
        "<!-- END GENERATED TRAJECTORY SNAPSHOT -->\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert FORWARD_ONLY not in proc.stderr


def test_generated_marker_exempts_only_the_block(tmp_path):
    # Repo-review 2026-07-21 H-5: the marker used to stand the rule down for
    # the WHOLE file, leaving the hand-authored remainder of a hybrid
    # status.md (the WI-234 splice shape) enforced by nothing — exactly where
    # done-ids accrete (and did, on this repo's own status.md). The block
    # stays exempt; the remainder stays policed.
    write_wis_sr(tmp_path, "WI-001,Shipped,scripts,,,done,shipped it,\n")
    write_status(
        tmp_path,
        "## Standing floors just armed\n- WI-001 landed the thing.\n\n"
        + GENERATED_MARKER
        + "\n- WI-001 (from the registry snapshot)\n"
        "<!-- END GENERATED TRAJECTORY SNAPSHOT -->\n",
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert FORWARD_ONLY in strict.stderr and "WI-001" in strict.stderr
    # And a hybrid file whose hand region is clean stays clean.
    write_status(
        tmp_path,
        "## Next action\n- await the owner.\n\n"
        + GENERATED_MARKER
        + "\n- WI-001 (from the registry snapshot)\n"
        "<!-- END GENERATED TRAJECTORY SNAPSHOT -->\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert FORWARD_ONLY not in proc.stderr


def test_forward_only_opt_out_silences(tmp_path):
    # docs/trajectory-check: off silences the whole check, done id and all.
    write_wis_sr(tmp_path, "WI-001,Shipped,scripts,,,done,shipped it,\n")
    write_status(tmp_path, "## Recently closed\n- WI-001 landed.\n")
    (tmp_path / "docs" / "trajectory-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert FORWARD_ONLY not in proc.stderr


def test_forward_only_vacuous_on_placeholder_registry(tmp_path):
    # A placeholder-only registry has no real (let alone done) WIs, so even a
    # status.md echoing the inert WI-000 id triggers nothing.
    write_wis(tmp_path, PLACEHOLDER_ROW)
    write_status(tmp_path, "## Recently closed\n- WI-000 example.\n")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert FORWARD_ONLY not in proc.stderr


def test_forward_only_unit_over_the_real_meta_repo():
    # Prove the pruned meta-repo status.md passes: its named WI ids (WI-194..200
    # open, the deferred backlog) carry no `done` id, so the rule finds nothing.
    ct = load_script("check_trajectory")
    wis = ct.load_wis(ct.read_registry_rows(ROOT / "docs/requirements/work-items.csv"))[
        0
    ]
    assert ct.status_forward_only_findings(ROOT, wis) == []


# --- WI-284: the forward-only cascade is broken by generation ------------------
# The forward-looking WI list is GENERATED (the scheduler frontier) inside the
# STATUS block the forward-only rule exempts, so integrating a WI drops it from
# status.md on the next `--status` regen — it can never strand a `done` id in the
# hand-authored region and redden a later train's DONE gate (the bug that burned
# WI-276's budget). These pin the two halves: the frontier self-prunes, and the
# hand-authored region is still policed.


# Rows the scheduler can CLASSIFY (a bare row fails closed as `unclassified` and
# never reaches the ready frontier): SafetyClass=ordinary is the minimal signal
# for an ordinary, packable WI.
_FRONTIER_COLUMNS = WI_COLUMNS + ",SafetyClass"


def _write_frontier_wis(root, body):
    write_wis(root, body, _FRONTIER_COLUMNS)


def test_wi284_generated_frontier_drops_a_closed_wi(tmp_path):
    gt = load_script("gen_trajectory")
    _write_frontier_wis(
        tmp_path,
        "WI-001,First thing,scripts,,,queued,,ordinary\n"
        "WI-002,Second thing,scripts,,,queued,,ordinary\n",
    )
    before = "\n".join(gt._frontier_lines(tmp_path))
    assert "Ready frontier" in before and "WI-001" in before and "WI-002" in before
    # WI-001 integrates -> done. Regenerating the frontier drops it automatically;
    # nothing hand-edited, no stranded id.
    _write_frontier_wis(
        tmp_path,
        "WI-001,First thing,scripts,,,done,,ordinary\n"
        "WI-002,Second thing,scripts,,,queued,,ordinary\n",
    )
    after = "\n".join(gt._frontier_lines(tmp_path))
    assert "WI-001" not in after
    assert "WI-002" in after


def test_wi284_done_id_in_generated_block_is_exempt_but_still_policed_outside(tmp_path):
    ct = load_script("check_trajectory")
    write_wis(tmp_path, "WI-001,First,scripts,,,done,\n")
    wis = ct.load_wis(
        ct.read_registry_rows(tmp_path / "docs/requirements/work-items.csv")
    )[0]
    # Named ONLY inside the generated block (where the frontier lives) -> exempt.
    write_status(
        tmp_path,
        "# S\n\n<!-- BEGIN GENERATED STATUS -->\n"
        "- **Ready frontier** — **WI-001** first thing\n"
        "<!-- END GENERATED STATUS -->\n\n- **Next action:** work the frontier.\n",
    )
    assert ct.status_forward_only_findings(tmp_path, wis) == []
    # The same done id stranded in the hand-authored region still flags (the guard
    # the generated frontier keeps out of, not one it silences).
    write_status(
        tmp_path,
        "# S\n\n<!-- BEGIN GENERATED STATUS -->\n<!-- END GENERATED STATUS -->\n\n"
        "- **Next action:** finish **WI-001** first.\n",
    )
    assert any("WI-001" in f for f in ct.status_forward_only_findings(tmp_path, wis))


def test_a_spec_that_names_no_specref_still_parses(tmp_path):
    # An absent cell is absent, not a crash: the folder form OMITS an empty
    # frontmatter key entirely (absent and empty mean the same thing there), so a
    # done spec with no `specref` validates clean and an open one simply draws the
    # warn-first R-E notice. This was the pre-S1 legacy-CSV shape; it is now every
    # spec that has nothing to say in a cell.
    write_wis(tmp_path, "WI-001,A,scripts,,,done,d\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 work item(s)" in proc.stdout
    write_wis(tmp_path, "WI-001,A,scripts,,,active,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "R-E WI-001" in proc.stderr  # absent key -> warn, never a crash


# (test_extra_legacy_column_is_tolerated retired at concurrency-restructure
# Phase 5: it drove `csv.DictReader`'s tolerance of an unknown COLUMN in the CSV
# home. The folder form has no header to carry a stale column, and an unknown
# frontmatter KEY is simply not read into the 17-key row — `parse_spec_row`'s own
# contract, pinned in test_wi_folder_loaders.)


def test_branch_length_warns_on_prebranch_specs_only(tmp_path):
    """The hand-filed-spec half of the MAX_PATH cliff (2026-08-16b, F3):
    dispatch derives the branch from the on-disk filename stem verbatim, so a
    queued/draft/deferred spec past the minted ceiling warns — while terminal
    and active states are exempt (their branch exists or never will), and the
    ceiling itself sits exactly at id + '-' + SLUG_CHARS."""
    ct = load_script("check_trajectory")
    long_slug = "x" * (ct._SLUG_CHARS_MIRROR + 1)
    at_cap = "y" * ct._SLUG_CHARS_MIRROR
    for state, name in [
        ("queued", f"WI-901-{long_slug}.md"),
        ("queued", f"WI-902-{at_cap}.md"),
        ("complete", f"WI-903-{long_slug}.md"),
        ("active", f"WI-904-{long_slug}.md"),
    ]:
        d = tmp_path / "docs" / "work" / state
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text('+++\nid = "WI-90x"\n+++\n', encoding="utf-8")
    out = ct.branch_length_findings(tmp_path)
    assert len(out) == 1, out
    assert "WI-901" in out[0] and "MAX_PATH" in out[0]
