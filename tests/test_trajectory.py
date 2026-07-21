"""check_trajectory.py — the work-item registry validator (Thread 52 phase 1).

The layer's whole value is what it blocks (cycles, dangling predecessors,
malformed/duplicate ids) *and* what it deliberately lets through: a
placeholder-only or absent registry is vacuously clean, a dangling SR ref only
warns (draft SRs are legitimate), and `docs/trajectory-check: off` silences the
check entirely. Each is pinned red/green by running the real script over a
minimal temp registry (no full scaffold needed — the validator reads plain CSVs).
"""

import os
import shutil
import subprocess

import pytest

from conftest import ROOT, SCRIPTS, load_script, run_py

WI_HEADER = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable\n"
# The header with the SpecRef column (S1) — used by the SSOT-rule tests.
SR_WI_HEADER = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SpecRef,BlockRef\n"
)
LEGACY_HEADER = "WI-ID,Title,Track,SR-Refs,Predecessors,Status,Deliverable\n"
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)

PLACEHOLDER_ROW = (
    "WI-000,EXAMPLE - delete on first real entry,track-name,SR-000,,queued,demo\n"
)


def write_wis(root, body):
    """Write docs/requirements/work-items.csv with `body` under the header."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "work-items.csv").write_text(WI_HEADER + body, encoding="utf-8")
    return root


def write_srs(root, *sr_ids):
    """Write a system-requirements.csv carrying just the given SR ids."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    rows = "".join(
        '{},Title,SN-001,"The system shall.",R,AC,,M,Test,Draft\n'.format(s)
        for s in sr_ids
    )
    (req / "system-requirements.csv").write_text(SR_HEADER + rows, encoding="utf-8")


def run_traj(root, *extra):
    return run_py([SCRIPTS / "check_trajectory.py", "--root", root, *extra], cwd=root)


def write_wis_sr(root, body):
    """Write work-items.csv with the SpecRef-column header + `body`."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "work-items.csv").write_text(SR_WI_HEADER + body, encoding="utf-8")
    return root


def write_status(root, text):
    """Write docs/status.md (the forward-only working surface)."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "status.md").write_text(text, encoding="utf-8")


def write_spec(root, rel):
    """Create an in-repo spec file so a SpecRef resolves (R-E)."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# spec\n", encoding="utf-8")


# --- vacuous / opt-out: the layer costs a non-adopter nothing ------------------


def test_absent_registry_is_vacuously_clean(tmp_path):
    # No work-items.csv at all (a repo that never touched the layer) -> pass.
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


def test_legacy_track_header_still_read(tmp_path):
    # A pre-rename registry (Track column) validates unchanged — the rename is
    # downstream-migrating but never breaking.
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "work-items.csv").write_text(
        LEGACY_HEADER + "WI-001,A,old-lane,,,done,d\n", encoding="utf-8"
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 work item(s)" in proc.stdout


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


# --- tolerant of messy input ----------------------------------------------------


def test_blank_or_non_wi_rows_are_ignored(tmp_path):
    # A stray row whose id isn't a WI (blank first cell) is skipped, not an error.
    write_wis(tmp_path, "WI-001,A,scripts,,,done,d\n,stray note,,,,,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 work item(s)" in proc.stdout


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


def test_blocked_status_is_first_class_with_blockref(tmp_path):
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,blocked,,docs/specs/WI-001.md,OI-7\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "unknown status" not in proc.stderr


def test_blocked_status_requires_blockref(tmp_path):
    write_spec(tmp_path, "docs/specs/WI-001.md")
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,blocked,,docs/specs/WI-001.md,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 1
    assert "blocked-ref WI-001" in proc.stderr and "BlockRef is empty" in proc.stderr


def test_unknown_status_warns_plain_fails_strict(tmp_path):
    # An out-of-vocabulary status lints (warn-first; ERROR under --strict).
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,paused,,,\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "unknown status" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "unknown status" in strict.stderr


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
    # A `path#anchor` SpecRef resolves on the path part alone (anchor ignored by
    # R-E; deeper validation rides check_doc_refs).
    write_spec(tmp_path, "docs/specs/effort.md")
    write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,queued,,docs/specs/effort.md#s1--first-slice\n",
    )
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
    write_spec(tmp_path, "docs/specs/effort.md")
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


def test_run_state_end_state_warns_for_actionable_queue_and_fails_strict(tmp_path):
    # WI-115: an end-state must not strand a queued WI whose hard predecessors
    # are all done; soft predecessors remain advisory.
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Done,scripts,,,done,shipped,\n"
        "WI-002,Next,scripts,,WI-001;~WI-003,queued,,docs/specs/WI-002.md\n"
        "WI-003,Advisory,scripts,,,active,,docs/specs/WI-002.md\n",
    )
    write_status(tmp_path, "Next: WI-002; WI-003 is its predecessor.\n")
    (tmp_path / "docs" / "run-state").write_text("NEEDS-HUMAN\n", encoding="utf-8")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "run-state NEEDS-HUMAN" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "run-state NEEDS-HUMAN" in strict.stderr


def test_run_state_check_is_vacuous_without_file_and_for_done_empty_queue(tmp_path):
    # Non-adopters have no run-state file; DONE is legal when no queued WI is ready.
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_wis_sr(
        tmp_path,
        "WI-001,Done,scripts,,,done,shipped,\n"
        "WI-002,Waiting,scripts,,WI-003,queued,,docs/specs/WI-002.md\n"
        "WI-003,Blocked predecessor,scripts,,,active,,docs/specs/WI-002.md\n",
    )
    write_status(tmp_path, "Next: WI-002; WI-003 is its predecessor.\n")
    absent = run_traj(tmp_path, "--strict")
    assert absent.returncode == 0, absent.stdout + absent.stderr
    assert "run-state" not in absent.stderr
    (tmp_path / "docs" / "run-state").write_text("DONE\n", encoding="utf-8")
    done = run_traj(tmp_path, "--strict")
    assert done.returncode == 0, done.stdout + done.stderr
    assert "run-state" not in done.stderr


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
    # A status.md carrying the kit's generated-block marker is an integrator
    # snapshot that cannot accrete prose — the token rule yields (freshness is its
    # unimplemented successor), so a done id in it does NOT flag, even --strict.
    write_wis_sr(tmp_path, "WI-001,Shipped,scripts,,,done,shipped it,\n")
    write_status(
        tmp_path,
        GENERATED_MARKER + "\n- WI-001 (from the registry snapshot)\n"
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
    wis = ct.load_wis(ct.read_rows(ROOT / "docs/requirements/work-items.csv"))[0]
    assert ct.status_forward_only_findings(ROOT, wis) == []


def test_legacy_csv_without_specref_column_still_parses(tmp_path):
    # A pre-S1 registry (no SpecRef column) reads the missing cell as empty and
    # never crashes: a done-only legacy registry validates clean; an open legacy
    # row simply draws the warn-first R-E notice (DictReader -> None -> "").
    write_wis(tmp_path, "WI-001,A,scripts,,,done,d\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 work item(s)" in proc.stdout
    write_wis(tmp_path, "WI-001,A,scripts,,,active,\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "R-E WI-001" in proc.stderr  # missing column -> warn, never a crash


def test_extra_legacy_column_is_tolerated(tmp_path):
    # A registry carrying an extra optional column (a legacy grouping tag, read by
    # name like Workstream — no vocabulary rule) validates exactly as one without
    # it: DictReader tolerates unknown columns, so a re-synced downstream that kept
    # a retired grouping tag never breaks.
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    hdr = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,LegacyTag\n"
    (req / "work-items.csv").write_text(
        hdr
        + "WI-001,A,scripts,,,done,d,some-slug-2026\n"
        + "WI-002,B,scripts,,WI-001,done,d,anything-goes-here\n",
        encoding="utf-8",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "2 work item(s)" in proc.stdout


# --- S1: the no-validation-delta warn (--staged) -------------------------------


def _init_followup_repo(root):
    """A git repo whose HEAD has WI-001 done (delivered SR-001) and WI-002 open,
    with WI-002 then closed as a follow-up on the same SR in the working tree.
    Returns the git runner; the caller stages the pieces under test."""
    git = shutil.which("git")
    if not git:
        pytest.skip("needs git on PATH")

    def run_git(*a):
        return subprocess.run(
            [git, "-C", str(root), *a], capture_output=True, text=True
        )

    run_git("init")
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    write_wis_sr(
        root,
        "WI-001,First,scripts,SR-001,,done,delivered SR-001,\n"
        "WI-002,Follow-up,scripts,SR-001,WI-001,active,,docs/specs/WI-002.md\n",
    )
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    # Close WI-002 in the working tree (a follow-up on SR-001, already delivered).
    write_wis_sr(
        root,
        "WI-001,First,scripts,SR-001,,done,delivered SR-001,\n"
        "WI-002,Follow-up,scripts,SR-001,WI-001,done,patched the code,\n",
    )
    return run_git


def test_staged_no_validation_delta_warns(tmp_path):
    # Closing a follow-up WI on an already-delivered SR while touching neither the
    # TC registry nor a test file warns: the fix did not land in the chain.
    run_git = _init_followup_repo(tmp_path)
    run_git("add", "docs/requirements/work-items.csv")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation chain did not change" in proc.stderr
    assert "WI-002" in proc.stderr


def test_staged_no_warn_when_a_test_changes(tmp_path):
    # The same close, but a test file is also staged -> the chain changed, no warn.
    run_git = _init_followup_repo(tmp_path)
    (tmp_path / "tests").mkdir(exist_ok=True)
    (tmp_path / "tests" / "test_fix.py").write_text("# covers the fix\n", "utf-8")
    run_git("add", "docs/requirements/work-items.csv", "tests/test_fix.py")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation chain did not change" not in proc.stderr


def test_staged_is_a_no_op_outside_git(tmp_path):
    # No git repo -> --staged is a silent no-op (warn-first, never a crash).
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,active,,docs/specs/WI-001.md\n")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "validation chain" not in proc.stderr


# --- WI-068: the critique-loop ratchet (--staged, warn-first) ------------------

CRITIQUE_SR_ROW = (
    'SR-050,Render realism,SN-001,"The render shall look realistic.",'
    '"Subjective.","Judged against docs/rubrics/render.md.",,S,Critique,Verified\n'
)


def _init_critique_close_repo(tmp_path, verdict="CHANGES-REQUESTED findings=2"):
    """A git repo with a Verification=Critique SR-050, a committed CRITIQUE verdict
    file, and WI-050 (on SR-050) closed queued->done in the working tree."""
    git = shutil.which("git")
    if not git:
        pytest.skip("needs git on PATH")

    def run_git(*a):
        return subprocess.run(
            [git, "-C", str(tmp_path), *a], capture_output=True, text=True
        )

    run_git("init")
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(SR_HEADER + CRITIQUE_SR_ROW, "utf-8")
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "- [MAJOR] render.png -> B1 seam artifact at the mesh join -> reseat -> @owner\n"
        "VERDICT: " + verdict + "\n",
        encoding="utf-8",
    )
    write_wis_sr(
        tmp_path, "WI-050,Render,scripts,SR-050,,active,,docs/specs/WI-050.md\n"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    # Close WI-050 (the Critique WI) in the working tree.
    write_wis_sr(tmp_path, "WI-050,Render,scripts,SR-050,,done,shipped the render,\n")
    return run_git


def test_critique_ratchet_warns_and_holds(tmp_path):
    # Closing a Critique WI while the latest CRITIQUE verdict is CHANGES-REQUESTED,
    # touching neither the TC registry, the tests dir, nor a docs/rubrics/ file ->
    # warn (the fix landed in the artifact, not the chain).
    run_git = _init_critique_close_repo(tmp_path)
    run_git("add", "docs/requirements/work-items.csv")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "latest CRITIQUE verdict is CHANGES-REQUESTED" in proc.stderr
    assert "WI-050" in proc.stderr
    # Add a rubric anchor (touch docs/rubrics/) -> the chain changed -> HOLDS.
    (tmp_path / "docs" / "rubrics").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "rubrics" / "render.md").write_text(
        "# render\n- B2 a newly-found failure mode\n", encoding="utf-8"
    )
    run_git("add", "docs/requirements/work-items.csv", "docs/rubrics/render.md")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "latest CRITIQUE verdict" not in proc.stderr


def test_critique_ratchet_silent_when_verdict_approves(tmp_path):
    # The latest CRITIQUE verdict is APPROVE -> no warn even with no chain delta.
    run_git = _init_critique_close_repo(tmp_path, verdict="APPROVE findings=0")
    run_git("add", "docs/requirements/work-items.csv")
    proc = run_traj(tmp_path, "--staged")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "latest CRITIQUE verdict" not in proc.stderr


# --- WI-056: architecture-connectivity coverage (warn-first, opt-out default-on)
# The views-checker runs at the same `trajectory` step; every finding is a WARN
# (never an exit-code change, even under --strict) and the meta driver is the
# "connectivity undeclared" warn a multi-module arch-map with no seams emits.

ARCH_2MOD = """# Arch
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_A._

| Public item | Summary | Implements |
|---|---|---|
| `run()` | go |  |

### `scripts/mod_b`
_B._

| Public item | Summary | Implements |
|---|---|---|
| `go()` | g |  |
<!-- END GENERATED MODULE MAP -->
"""

ARCH_1MOD = """# Arch
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_A._

| Public item | Summary | Implements |
|---|---|---|
| `run()` | go |  |
<!-- END GENERATED MODULE MAP -->
"""

IF_HDR = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
    "Stability,Status,Component,Notes\n"
)


def write_arch(root, text):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "architecture.md").write_text(text, encoding="utf-8")


def write_ifs(root, body):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "interfaces.csv").write_text(IF_HDR + body, encoding="utf-8")


def test_interface_coverage_warns(tmp_path):
    # Multi-module arch-map with NO interfaces.csv -> "connectivity undeclared"
    # (the ruled opt-out, default-on posture), and the exit code is still 0.
    write_arch(tmp_path, ARCH_2MOD)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" in proc.stderr


def test_interface_check_off_silences(tmp_path):
    write_arch(tmp_path, ARCH_2MOD)
    (tmp_path / "docs" / "interfaces-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" not in proc.stderr


def test_single_module_inventory_is_vacuous(tmp_path):
    # <=1 module: nothing to connect, so the coverage layer stays silent.
    write_arch(tmp_path, ARCH_1MOD)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" not in proc.stderr


def test_uncovered_direction_warns(tmp_path):
    # One Provides seam a->b: a has no Consumes, b has no Provides -> both
    # missing-direction warns fire (exit 0).
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" in proc.stderr  # mod_a
    assert "declares no Provides seam" in proc.stderr  # mod_b


def test_source_sink_marker_suppresses_direction_warn(tmp_path):
    # mod_a marked source (consumes nothing), mod_b marked sink (provides nothing)
    # -> both missing-direction warns suppressed by the honesty valve.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,source\n'
        'IF-002,Consumes,scripts/mod_b,docs/stack.ini,"reads",SR-001,v1,Stable,Active,,sink\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" not in proc.stderr
    assert "declares no Provides seam" not in proc.stderr


def test_seam_tc_citation_warn(tmp_path):
    # A symmetric pair covers both directions, so only the Active-seam-TC warn
    # fires; a TC that cites IF-001 suppresses its warn, IF-002 still warns.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,Stable,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,Stable,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Verified\n",
        encoding="utf-8",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" not in proc.stderr  # symmetric -> covered
    assert "IF IF-001 is Active but cited by no TC" not in proc.stderr
    assert "IF IF-002 is Active but cited by no TC" in proc.stderr


def test_contracts_docstring_citation_warns(tmp_path):
    # A module's `Contracts (interfaces):` arch-map line names IF-003 (absent from
    # the registry) -> forward warn; and once the convention is in use, a registry
    # IF declared by no module warns in reverse.
    arch = ARCH_2MOD.replace("_A._\n", "_A._\nContracts (interfaces): IF-003\n")
    write_arch(tmp_path, arch)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,Stable,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,Stable,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares Contracts: IF-003 but no such IF-### row" in proc.stderr
    assert "no script declares it via a Contracts" in proc.stderr


def test_interface_warns_never_fail_strict(tmp_path):
    # Even under --strict, the connectivity warns never change the exit code
    # (they are warns, not the R-B..R-E coherence rules --strict promotes). With
    # no work-items registry the run is vacuously clean once the warns are printed.
    write_arch(tmp_path, ARCH_2MOD)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" in proc.stderr


# --- WI-073/FB5: the How-SW top-view right-sizing rule -------------------------
# The software-architecture top view is bounded at 10 items (top-level CMP
# components that contain a module + uncontained modules); over the bound is a
# finding — WARN plain, ERROR under --strict (G2+). Opt-out docs/components-check;
# vacuous below the bound or with no arch-map inventory (the bound is the rule).

CMP_HDR = "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
TAGGED_LLR_HDR = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component\n"
)


def _arch_n(n):
    """A generated MODULE MAP block of n modules scripts/mod_0..mod_{n-1}."""
    body = "".join(
        "### `scripts/mod_{i}`\n_M{i}._\n\n| Public item | Summary | Implements |\n"
        "|---|---|---|\n| `f{i}()` | go |  |\n\n".format(i=i)
        for i in range(n)
    )
    return (
        "# Arch\n<!-- BEGIN GENERATED MODULE MAP -->\n"
        + body
        + "<!-- END GENERATED MODULE MAP -->\n"
    )


def write_cmps(root, body):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "components.csv").write_text(CMP_HDR + body, encoding="utf-8")


def write_tagged_llrs(root, pairs):
    """`pairs` = [(module, CMP-id)]; writes an LLR csv (Component column) so a
    module joins its CMP through its LLR's Component tag (the AXES membership)."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    body = "".join(
        "LLR-{:03d},SR-001,T,{},f,d,(see TC),Verified,{}\n".format(i + 1, mod, cmp)
        for i, (mod, cmp) in enumerate(pairs)
    )
    (req / "low-level-requirements.csv").write_text(
        TAGGED_LLR_HDR + body, encoding="utf-8"
    )


def test_top_view_over_bound_warns_plain_fails_strict(tmp_path):
    # 12 modules, no CMP rows -> 12 uncontained top items > 10.
    write_arch(tmp_path, _arch_n(12))
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "How-SW top view has 12 items" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "How-SW top view has 12 items" in strict.stderr


def test_declaring_components_below_bound_clears_it(tmp_path):
    # 3 components containing all 12 modules -> top view = 3 <= 10.
    write_arch(tmp_path, _arch_n(12))
    write_cmps(
        tmp_path,
        "CMP-001,A,software,,built,,,,\n"
        "CMP-002,B,software,,built,,,,\n"
        "CMP-003,C,software,,built,,,,\n",
    )
    write_tagged_llrs(
        tmp_path,
        [("scripts/mod_{}".format(i), "CMP-00{}".format(i % 3 + 1)) for i in range(12)],
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_nested_cmp_counts_only_at_top_level_root(tmp_path):
    # CMP-003 nests under CMP-001 (PartOf); its members count under CMP-001, so
    # the roots are {CMP-001, CMP-002} = 2 top items, well under the bound.
    write_arch(tmp_path, _arch_n(12))
    write_cmps(
        tmp_path,
        "CMP-001,Core,software,,built,,,,\n"
        "CMP-002,Other,software,,built,,,,\n"
        "CMP-003,Nested,software,,built,,CMP-001,,\n",
    )
    pairs = []
    for i in range(12):
        cmp = "CMP-001" if i < 4 else ("CMP-003" if i < 8 else "CMP-002")
        pairs.append(("scripts/mod_{}".format(i), cmp))
    write_tagged_llrs(tmp_path, pairs)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_uncontained_modules_count_toward_the_bound(tmp_path):
    # One component holding a single module leaves 11 uncontained -> 1 + 11 = 12.
    write_arch(tmp_path, _arch_n(12))
    write_cmps(tmp_path, "CMP-001,Only,software,,built,,,,\n")
    write_tagged_llrs(tmp_path, [("scripts/mod_0", "CMP-001")])
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "1 top-level component(s) + 11 uncontained module(s)" in strict.stderr


def test_top_view_off_switch_silences(tmp_path):
    write_arch(tmp_path, _arch_n(12))
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_ten_module_inventory_is_vacuous(tmp_path):
    # Exactly at the bound with no CMP rows -> passes trivially (the bound, not
    # the registry, is the rule).
    write_arch(tmp_path, _arch_n(10))
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_absent_inventory_top_view_is_vacuous(tmp_path):
    # No architecture.md at all -> nothing to bound (pre-arch-map / files-mode).
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


# --- WI-153: knowledge⇒component coupling (research-knowledge.md §3a) -----------
# When docs/knowledge/ holds a real pack, an uncontained arch-map module is a
# finding *regardless of* the 10-item bound — WARN plain, ERROR under --strict —
# so the knowledge⇒component web must be complete wherever packs are enabled. It
# reuses the Component-tag join (no new join), the docs/components-check opt-out,
# and stays dormant until a real pack (not the README index) exists.

KN_MSG = "arch-map module(s) are in no CMP-### component"


def write_pack(root, label, body="# Pack\n"):
    d = root / "docs" / "knowledge"
    d.mkdir(parents=True, exist_ok=True)
    (d / (label + ".md")).write_text(body, encoding="utf-8")


def test_pack_presence_arms_coupling_below_bound(tmp_path):
    # 3 modules (well under the 10-item bound), none contained, + one pack: the
    # top-view rule is vacuous here, but the pack arms the coupling finding.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "docs/knowledge/ holds 1 pack(s) but 3 " + KN_MSG in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert KN_MSG in strict.stderr


def test_coupling_dormant_without_packs(tmp_path):
    # Same uncontained 3-module arch-map but no pack -> below the bound, silent.
    write_arch(tmp_path, _arch_n(3))
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_readme_index_alone_does_not_arm_coupling(tmp_path):
    # The scaffolded README.md is the index, not a pack -> still dormant.
    write_arch(tmp_path, _arch_n(3))
    (tmp_path / "docs" / "knowledge").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "knowledge" / "README.md").write_text("# idx\n", "utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_coupling_clears_when_every_module_contained(tmp_path):
    # A pack exists, but every module is tagged into a CMP -> web complete, silent.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_tagged_llrs(
        tmp_path, [("scripts/mod_{}".format(i), "CMP-001") for i in range(3)]
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_coupling_reports_only_the_uncontained_modules(tmp_path):
    # A pack + a CMP holding one of three modules -> two remain uncontained.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_tagged_llrs(tmp_path, [("scripts/mod_0", "CMP-001")])
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "holds 1 pack(s) but 2 " + KN_MSG in strict.stderr


def test_coupling_respects_the_components_check_off_switch(tmp_path):
    # docs/components-check: off silences the coupling as it does the top view.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_coupling_needs_an_arch_map_inventory(tmp_path):
    # A pack but no arch-map -> no modules to leave uncontained -> dormant.
    write_pack(tmp_path, "prompt-image")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


# --- WI-093: the [phase]-[g*] archetype + phase-drop detector ------------------
# The derived-gate model (docs/specs/derived-gate-model.md §7/§9.3): a phase's
# pre-dev batch is a WI whose Title carries a `[<phase>]-[g<N>]` tag; the derived
# gate dropping below a phase's closed anchor level warns to open a new phase-gate
# WI. All warn-first; the logic is unit-tested via load_script.


def _wis(ct, rows):
    return ct.load_wis(rows)[0]


def test_phase_anchors_parse_and_duplicate_warn():
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {
                "WI-ID": "WI-201",
                "Title": "[v2]-[g1] structure v2 reqs",
                "Status": "done",
            },
            {
                "WI-ID": "WI-202",
                "Title": "[v2]-[g2] decompose v2",
                "Predecessors": "WI-201",
                "Status": "queued",
            },
            {
                "WI-ID": "WI-203",
                "Title": "[v2]-[g2] a duplicate g2",
                "Status": "queued",
            },
            {"WI-ID": "WI-204", "Title": "an ordinary WI", "Status": "queued"},
        ],
    )
    anchors, warns = ct.phase_anchors(wis)
    assert ("v2", 1) in anchors and ("v2", 2) in anchors
    assert anchors[("v2", 2)]["id"] == "WI-202"  # first wins
    assert any("duplicate phase-gate anchor [v2]-[g2]" in w for w in warns)


def test_phase_anchor_g2_without_g1_predecessor_warns():
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-201", "Title": "[v3]-[g1] x", "Status": "done"},
            {"WI-ID": "WI-202", "Title": "[v3]-[g2] y", "Status": "queued"},  # no pred
        ],
    )
    _, warns = ct.phase_anchors(wis)
    assert any("does not list its [v3]-[g1]" in w for w in warns)


def _write_gate(root, per_phase, value="G1"):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "gate").write_text(
        "# header\n# basis: SN=1 SR=3 LLR=3 TC=3 drafts=0 computed={} "
        "per-phase={}\n# computed 2026-07-12 (as-of x)\n{}\n".format(
            value, per_phase, value
        ),
        encoding="utf-8",
    )


def test_read_derived_phases_parses_basis(tmp_path):
    ct = load_script("check_trajectory")
    _write_gate(tmp_path, "v1=G3;v2=G0")
    assert ct.read_derived_phases(tmp_path) == {"v1": 3, "v2": 0}
    # A legacy hand-set gate with no basis line yields no phase data (vacuous).
    (tmp_path / "docs" / "gate").write_text("# legacy\nG3\n", encoding="utf-8")
    assert ct.read_derived_phases(tmp_path) == {}


def test_phase_drop_detector_warns(tmp_path):
    ct = load_script("check_trajectory")
    # v2 closed at [g2] (done) but the derived level for v2 is now G0 (a reopen).
    _write_gate(tmp_path, "v1=G3;v2=G0")
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-210", "Title": "[v2]-[g1] x", "Status": "done"},
            {
                "WI-ID": "WI-211",
                "Title": "[v2]-[g2] y",
                "Predecessors": "WI-210",
                "Status": "done",
            },
        ],
    )
    warns = ct.phase_findings(tmp_path, wis)
    assert any("phase 'v2' dropped to G0" in w and "[v2]-[g2]" in w for w in warns)
    # Back at G2: no drop warn (the phase re-cleared its anchor level).
    _write_gate(tmp_path, "v1=G3;v2=G2", value="G2")
    assert ct.phase_findings(tmp_path, wis) == []


def test_phase_findings_vacuous_without_anchors(tmp_path):
    ct = load_script("check_trajectory")
    _write_gate(tmp_path, "v1=G0")  # a phase at G0 but NO anchor records a close
    wis = _wis(ct, [{"WI-ID": "WI-220", "Title": "ordinary", "Status": "queued"}])
    assert ct.phase_findings(tmp_path, wis) == []


# --- WI-146(b): the ratification-brief hierarchy-view lint --------------------
# A `## OI-N` brief whose decision is a `[phase]-[g1|g2]` ratification should
# *link* the generated batch-scoped hierarchy view rather than hand-copy rows.
# Warn-first (never a gate fail); vacuous without such a brief.


def _write_open_items(root, body):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "open-items.md").write_text(body, encoding="utf-8")
    return root


def test_ratify_brief_without_view_warns(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        "# Open items\n"
        "Intro naming `[v3]-[g2]` in passing (before any section).\n\n"
        "## OI-20 — v3 g2 close\n"
        "- Decision: ratify the `[v3]-[g2]` dashboard batch.\n"
        "- Options: accept.\n\n"
        "## OI-21 — unrelated\n"
        "- Decision: something else, no anchor here.\n",
    )
    warns = ct.ratify_brief_findings(tmp_path)
    # Exactly the ratification brief warns; the intro prose and OI-21 do not.
    assert len(warns) == 1
    assert warns[0].startswith("OI-20:")
    assert "hierarchy view" in warns[0]


def test_ratify_brief_with_generator_command_only_warns(tmp_path):
    # A bare `trace.py --ratify` command mention is NOT proof the view exists and
    # is carried — the brief must *link* the generated view (WI-146 REVIEW-A).
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        "## OI-20 — v3 g2 close\n"
        "- Decision: ratify the `[v3]-[g2]` batch. Hierarchy: run "
        "`trace.py --ratify v3`.\n",
    )
    warns = ct.ratify_brief_findings(tmp_path)
    assert len(warns) == 1 and warns[0].startswith("OI-20:")


def test_ratify_brief_with_view_link_is_silent(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        "## OI-20 — v3 g2 close\n"
        "- Decision: ratify the `[v3]-[g2]` batch. "
        "See the [tree](ratify/v3-g2.md).\n",
    )
    assert ct.ratify_brief_findings(tmp_path) == []


def test_ratify_brief_lint_vacuous_without_brief(tmp_path):
    ct = load_script("check_trajectory")
    # No open-items.md at all -> nothing to check.
    assert ct.ratify_brief_findings(tmp_path) == []
    # A section with a ratification word but no [phase]-[g*] anchor -> not a brief.
    _write_open_items(
        tmp_path,
        "## OI-30 — general\n- Decision: whether to ratify a policy change.\n",
    )
    assert ct.ratify_brief_findings(tmp_path) == []
    # ...and an anchor with no ratification language -> also not a brief.
    _write_open_items(
        tmp_path,
        "## OI-31 — scheduling\n- Decision: sequence `[v3]-[g2]` after v2 work.\n",
    )
    assert ct.ratify_brief_findings(tmp_path) == []


# --- WI-064: the cross-CMP-edge-without-IF rule ---------------------------------
# An internal import edge between two DIFFERENT components with no covering
# IF-### row is a finding (the AXES ratified model's enforceability ruling) —
# WARN plain, ERROR under --strict, sharing the docs/components-check opt-out.
# Edges come from the MODULE MAP block's `Imports (internal):` lines; the seam
# side joins interfaces.csv endpoints in either direction. Vacuous whenever any
# input is absent (never-breaking).

ARCH_2MOD_IMPORT = """# Arch
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_A._
Imports (internal): `mod_b`

| Public item | Summary | Implements |
|---|---|---|
| `run()` | go |  |

### `scripts/mod_b`
_B._

| Public item | Summary | Implements |
|---|---|---|
| `go()` | g |  |
<!-- END GENERATED MODULE MAP -->
"""

TWO_CMPS = "CMP-001,A,software,,built,,,,\nCMP-002,B,software,,built,,,,\n"


def _cross_cmp_repo(tmp_path, cmp_b="CMP-002"):
    """mod_a (CMP-001) imports mod_b (cmp_b); no IF row unless a test adds one."""
    write_arch(tmp_path, ARCH_2MOD_IMPORT)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(
        tmp_path, [("scripts/mod_a", "CMP-001"), ("scripts/mod_b", cmp_b)]
    )


def test_cross_cmp_import_without_seam_warns_plain_fails_strict(tmp_path):
    _cross_cmp_repo(tmp_path)
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert (
        "cross-component import scripts/mod_a (CMP-001) -> scripts/mod_b (CMP-002)"
        in plain.stderr
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "has no declared IF-### seam" in strict.stderr


def test_cross_cmp_import_with_declared_seam_is_silent(tmp_path):
    _cross_cmp_repo(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Consumes,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,\n',
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_cross_cmp_seam_covers_either_direction(tmp_path):
    # The seam row authored from mod_b's side (b -> a) still covers the a -> b
    # import edge — a seam is one declared relationship, not a directed pair.
    _cross_cmp_repo(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_b,scripts/mod_a,"call",SR-001,v1,Stable,Active,,\n',
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_intra_cmp_import_is_silent(tmp_path):
    # Both endpoints in CMP-001: internal wiring, never a finding.
    _cross_cmp_repo(tmp_path, cmp_b="CMP-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_cross_cmp_unmapped_endpoint_is_vacuous(tmp_path):
    # mod_b has no Component membership: coverage is the containment rule's job,
    # so the cross-CMP rule stays silent rather than double-reporting.
    write_arch(tmp_path, ARCH_2MOD_IMPORT)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(tmp_path, [("scripts/mod_a", "CMP-001")])
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_cross_cmp_no_imports_lines_is_vacuous(tmp_path):
    # An arch-map without `Imports (internal):` lines (older gen, or no internal
    # imports) contributes no edges — the rule costs nothing.
    write_arch(tmp_path, ARCH_2MOD)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(
        tmp_path, [("scripts/mod_a", "CMP-001"), ("scripts/mod_b", "CMP-002")]
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_components_check_off_silences_cross_cmp(tmp_path):
    _cross_cmp_repo(tmp_path)
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


# --- specs act on declared interface boundaries (WI-191) ----------------------

# One Stable seam + one Proposed seam for the spec-citation checks.
SPEC_IFS_ONE = (
    'IF-001,Consumes,scripts/mod_a,docs/stack.ini,"reads",SR-001,v1,Stable,Stable,,\n'
)
SPEC_IFS_PROPOSED = SPEC_IFS_ONE + (
    'IF-050,Provides,scripts/mod_a,scripts/mod_b,"new seam",SR-001,v1,'
    "Experimental,Proposed,,\n"
)


def write_spec_file(root, name, body):
    d = root / "docs" / "specs"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(body, encoding="utf-8")


def _spec_repo(root, spec_name, spec_body, ifs=SPEC_IFS_ONE):
    # A non-vacuous WI registry (the spec check runs past the WI-load) + the IF
    # registry + one spec file. The done WI keeps R-A clean; no open WI leaves
    # R-E vacuous, so the only findings are the spec-interface ones.
    write_wis(root, "WI-001,A,scripts,,,done,Shipped it.\n")
    write_ifs(root, ifs)
    write_spec_file(root, spec_name, spec_body)


def test_spec_interfaces_unarmed_is_vacuous(tmp_path):
    _spec_repo(tmp_path, "WI-001.md", "# WI-001\n\n## Approach\n\nNo section.\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Interfaces" not in proc.stderr  # no `## Interfaces` -> not armed


def test_spec_interfaces_resolvable_passes(tmp_path):
    _spec_repo(
        tmp_path,
        "WI-001.md",
        "# WI-001\n\n## Interfaces\n\n- IF-001: acts on the stack reader.\n\n"
        "## Done-when\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "resolves to no row" not in proc.stderr


def test_spec_interfaces_unresolvable_warns_then_errors_under_strict(tmp_path):
    body = "# WI-001\n\n## Interfaces\n\n- IF-999: no such seam.\n\n## Done-when\n"
    _spec_repo(tmp_path, "WI-001.md", body)
    proc = run_traj(tmp_path)  # WARN plain, exit 0
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF-999 which resolves to no row" in proc.stderr
    strict = run_traj(tmp_path, "--strict")  # ERROR, exit 1
    assert strict.returncode == 1
    assert "IF-999 which resolves to no row" in strict.stderr


def test_spec_interfaces_proposed_needs_rationale(tmp_path):
    bare = "# WI-001\n\n## Interfaces\n\n- IF-050 (Proposed)\n\n## Done-when\n"
    _spec_repo(tmp_path, "WI-001.md", bare, ifs=SPEC_IFS_PROPOSED)
    proc = run_traj(tmp_path)
    assert "Proposed seam IF-050 with no rationale" in proc.stderr
    # A rationale naming the nearest existing seam + why it falls short -> clean.
    ok = (
        "# WI-001\n\n## Interfaces\n\n- IF-050 (Proposed): a new provide; nearest "
        "IF-001 is a consume, insufficient because this is the opposite "
        "direction.\n"
    )
    write_spec_file(tmp_path, "WI-001.md", ok)
    assert "Proposed seam IF-050" not in run_traj(tmp_path).stderr


def test_spec_interfaces_empty_section_warns(tmp_path):
    _spec_repo(tmp_path, "WI-001.md", "# WI-001\n\n## Interfaces\n\nTBD.\n\n## X\n")
    assert (
        "cites no IF-### and states no intra-module escape" in run_traj(tmp_path).stderr
    )


def test_spec_interfaces_intra_module_escape_passes(tmp_path):
    body = (
        "# WI-001\n\n## Interfaces\n\nIntra-module: acts only within scripts/mod_a; "
        "no cross-module seam (PROCESS.md §8).\n"
    )
    _spec_repo(tmp_path, "WI-001.md", body)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cites no IF-###" not in proc.stderr


def test_spec_interfaces_readme_and_example_not_armed(tmp_path):
    # The specs/ README documents the rule and the inert WI-000 example both carry
    # the heading, but neither is an armed spec-of-record.
    _spec_repo(
        tmp_path, "README.md", "# Specs\n\n## Interfaces\n\nThe rule: cite IF-###.\n"
    )
    write_spec_file(tmp_path, "WI-000.md", "# WI-000\n\n## Interfaces\n\n- IF-999 x\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF-999" not in proc.stderr


# --- WI-205: the backlog-staleness warn (warn-only, git-driven, silent off-git)
# An open WI whose cited SR row or SpecRef target was amended AFTER the WI row was
# last touched is re-flagged for a driven re-validation. Fixtures pin commit times
# via GIT_*_DATE so the strictly-newer compare is deterministic (two commits in the
# same wall-clock second would otherwise tie and never warn).

SR_ROW_V1 = 'SR-001,Feature SR,SN-001,"The system shall do X.",R,AC,,M,Test,Draft\n'
SR_ROW_V2 = (
    'SR-001,Feature SR,SN-001,"The system shall do X and Y.",R,AC,,M,Test,Draft\n'
)


def _write_sr_row(root, row):
    """Write a system-requirements.csv carrying a single raw SR row."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.csv").write_text(SR_HEADER + row, encoding="utf-8")


def _staleness_git(tmp_path):
    """A git runner whose commits can be stamped at a chosen epoch (`at=`), so the
    committer-time compare the staleness check reads is deterministic."""
    git = shutil.which("git")
    if not git:
        pytest.skip("needs git on PATH")
    base = dict(os.environ)

    def run_git(*a, at=None):
        env = base
        if at is not None:
            env = dict(base)
            stamp = "@{} +0000".format(at)
            env["GIT_AUTHOR_DATE"] = stamp
            env["GIT_COMMITTER_DATE"] = stamp
        return subprocess.run(
            [git, "-C", str(tmp_path), *a], capture_output=True, text=True, env=env
        )

    run_git("init")
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    return run_git


def _init_amended_sr_repo(tmp_path, status="active"):
    """A git repo where WI-001 (given status) cites SR-001, both committed at
    t=1000, then SR-001's row text is amended at t=2000 — the SR row is strictly
    newer than the WI row (the staleness precondition)."""
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, SR_ROW_V1)
    write_wis_sr(
        tmp_path,
        "WI-001,Feature,scripts,SR-001,,{},,docs/specs/WI-001.md\n".format(status),
    )
    write_spec(tmp_path, "docs/specs/WI-001.md")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=1000)
    _write_sr_row(tmp_path, SR_ROW_V2)
    run_git("add", "-A")
    run_git("commit", "-m", "amend SR-001", at=2000)
    return run_git


def test_backlog_staleness_amended_sr_warns(tmp_path):
    # A cited SR amended after the WI row was filed -> the WI is re-flagged.
    _init_amended_sr_repo(tmp_path)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WI-001: cites SR-001 amended after the WI row was last touched" in (
        proc.stderr
    )


def test_backlog_staleness_wi_touched_after_amend_is_quiet(tmp_path):
    # Re-affirming (any reviewed edit to the WI row, here at t=3000, after the SR
    # amendment) re-dates its blame and clears the warn.
    run_git = _init_amended_sr_repo(tmp_path)
    write_wis_sr(
        tmp_path,
        "WI-001,Feature (re-affirmed 2026-07-17),scripts,SR-001,,active,,"
        "docs/specs/WI-001.md\n",
    )
    run_git("add", "-A")
    run_git("commit", "-m", "re-affirm WI-001", at=3000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "amended after the WI row" not in proc.stderr


def test_backlog_staleness_specref_edit_warns(tmp_path):
    # The SpecRef target edited after the WI row was last touched -> re-flagged.
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, SR_ROW_V1)
    write_wis_sr(
        tmp_path, "WI-001,Feature,scripts,SR-001,,active,,docs/specs/WI-001.md\n"
    )
    write_spec(tmp_path, "docs/specs/WI-001.md")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=1000)
    (tmp_path / "docs" / "specs" / "WI-001.md").write_text(
        "# spec v2\n", encoding="utf-8"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "edit spec", at=2000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (
        "WI-001: its SpecRef docs/specs/WI-001.md changed after the WI row"
        in proc.stderr
    )
    assert "amended after the WI row" not in proc.stderr


def test_backlog_staleness_off_git_is_silent(tmp_path):
    # No git repo -> no blame basis -> no warn, no crash (best-effort off-git).
    _write_sr_row(tmp_path, SR_ROW_V2)
    write_wis_sr(
        tmp_path, "WI-001,Feature,scripts,SR-001,,active,,docs/specs/WI-001.md\n"
    )
    write_spec(tmp_path, "docs/specs/WI-001.md")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "amended after the WI row" not in proc.stderr
    assert "changed after the WI row" not in proc.stderr


def test_backlog_staleness_deferred_is_exempt(tmp_path):
    # A deferred WI citing an amended SR is EXEMPT (it re-enters via an owner
    # un-defer, itself the driven look) -> no warn.
    _init_amended_sr_repo(tmp_path, status="deferred")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "amended after the WI row" not in proc.stderr


def test_backlog_staleness_never_errors_under_strict(tmp_path):
    # The warn stays warn-only even under --strict (exit 0 with the finding).
    _init_amended_sr_repo(tmp_path)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WI-001: cites SR-001 amended after the WI row was last touched" in (
        proc.stderr
    )


# --- WI-243: the perceptual re-fire warn (git-time staleness, warn-first) -------


def _init_critique_staleness_repo(
    tmp_path, ev_at=1000, render_at=2000, verdict="APPROVE findings=0"
):
    """A git repo with a Verification=Critique SR-050, a CRITIQUE evidence file
    committed at `ev_at`, a done WI-050 (so the full check reaches the perceptual
    warn, past the no-work-items early return), and a render-surface file
    `scripts/gen_trajectory.py` committed at `render_at`. `render_at > ev_at` is
    the staleness precondition. The checker locates the generator via its
    `scripts/gen_trajectory.py` fallback (its `__file__`-co-located primary path
    is the real repo tree, not under tmp_path)."""
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, CRITIQUE_SR_ROW)
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "VERDICT: " + verdict + "\n", encoding="utf-8"
    )
    write_wis_sr(tmp_path, "WI-050,Render,scripts,SR-050,,done,shipped,\n")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=ev_at)
    scripts = tmp_path / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "gen_trajectory.py").write_text(
        "# dashboard generator\n", encoding="utf-8"
    )
    run_git("add", "-A")
    run_git("commit", "-m", "touch render surface", at=render_at)
    return run_git


def test_critique_staleness_warns_at_commit_bar_when_render_surface_newer(tmp_path):
    # The render surface changed after the latest CRITIQUE -> the perceptual stamp
    # is stale. At the commit bar (non-strict) it is a WARN, not an error (exit 0).
    _init_critique_staleness_repo(tmp_path)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale SR-050" in proc.stderr
    assert "scripts/gen_trajectory.py" in proc.stderr


def test_critique_staleness_quiet_when_evidence_is_newer(tmp_path):
    # A fresh critique (evidence committed AFTER the render change) re-dates the
    # evidence and clears the warn.
    _init_critique_staleness_repo(tmp_path, ev_at=2000, render_at=1000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale" not in proc.stderr


def test_critique_staleness_off_git_is_silent(tmp_path):
    # No git repo -> no commit-time basis -> no warn, no crash (best-effort).
    _write_sr_row(tmp_path, CRITIQUE_SR_ROW)
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "VERDICT: APPROVE findings=0\n", encoding="utf-8"
    )
    write_wis_sr(tmp_path, "WI-050,Render,scripts,SR-050,,done,shipped,\n")
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "gen_trajectory.py").write_text("# gen\n", encoding="utf-8")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale" not in proc.stderr


def test_critique_staleness_vacuous_without_a_critique_sr(tmp_path):
    # A non-Critique SR pays nothing, even with a newer render surface.
    run_git = _staleness_git(tmp_path)
    _write_sr_row(tmp_path, SR_ROW_V1)  # Verification=Test
    reviews = tmp_path / "docs" / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    (reviews / "001-CRITIQUE.md").write_text(
        "VERDICT: APPROVE findings=0\n", encoding="utf-8"
    )
    write_wis_sr(tmp_path, "WI-001,Feature,scripts,SR-001,,done,shipped,\n")
    run_git("add", "-A")
    run_git("commit", "-m", "init", at=1000)
    (tmp_path / "scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "scripts" / "gen_trajectory.py").write_text("# gen\n", encoding="utf-8")
    run_git("add", "-A")
    run_git("commit", "-m", "render", at=2000)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "perceptual-stale" not in proc.stderr


def test_critique_staleness_fails_closed_under_strict(tmp_path):
    # FAIL-CLOSED (WI-243, owner 2026-07-20): under --strict (the G3 gate) a stale
    # render surface is an ERROR (exit 1), not just a warn — it cannot reach green.
    _init_critique_staleness_repo(tmp_path)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ERROR - perceptual-stale SR-050" in proc.stderr
