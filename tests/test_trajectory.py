"""check_trajectory.py — the work-item registry validator (Thread 52 phase 1).

The layer's whole value is what it blocks (cycles, dangling predecessors,
malformed/duplicate ids) *and* what it deliberately lets through: a
placeholder-only or absent registry is vacuously clean, a dangling SR ref only
warns (draft SRs are legitimate), and `docs/trajectory-check: off` silences the
check entirely. Each is pinned red/green by running the real script over a
minimal temp registry (no full scaffold needed — the validator reads plain CSVs).
"""

import shutil
import subprocess

import pytest

from conftest import SCRIPTS, load_script, run_py

WI_HEADER = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable\n"
# The header with the SpecRef column (S1) — used by the SSOT-rule tests.
SR_WI_HEADER = (
    "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,SpecRef\n"
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


# --- S1: the status.md <-> registry SSOT rules ---------------------------------
# R-A is a hard error at every run (the pre-commit floor); R-B..R-E warn plain
# and gate under --strict; the vocabulary gains `deferred`.


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


def test_unknown_status_warns_plain_fails_strict(tmp_path):
    # An out-of-vocabulary status lints (warn-first; ERROR under --strict).
    write_wis_sr(tmp_path, "WI-001,A,scripts,,,blocked,,\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "unknown status" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "unknown status" in strict.stderr


def test_rd_done_id_in_status_warns_plain_fails_strict(tmp_path):
    # R-D: a done WI id must not linger on the forward-only status.md — warn
    # plain, ERROR under --strict. WI-002 (open) keeps status.md R-B/R-C clean.
    write_spec(tmp_path, "docs/specs/WI-002.md")
    write_wis_sr(
        tmp_path,
        "WI-001,First,scripts,,,done,d,\n"
        "WI-002,Next,scripts,,WI-001,active,,docs/specs/WI-002.md\n",
    )
    write_status(tmp_path, "Next: WI-002. Superseded WI-001 (leaked done id).\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "R-D WI-001" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "R-D WI-001" in strict.stderr


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
    write_spec(tmp_path, "docs/specs/campaign.md")
    write_wis_sr(
        tmp_path,
        "WI-001,A,scripts,,,queued,,docs/specs/campaign.md#s1--first-slice\n",
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_compliant_registry_and_status_passes_strict(tmp_path):
    # The whole model, coherent: a done row with a Deliverable and no SpecRef, an
    # open row with an empty Deliverable + resolvable SpecRef, status.md naming
    # the open WI and never the done one -> --strict is fully green.
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


def test_absent_status_md_is_vacuous_for_rbcd_under_strict(tmp_path):
    # No status.md: R-B/R-C/R-D cannot apply (a repo may keep no blackboard), so
    # a registry that is otherwise coherent passes even under --strict.
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


def test_campaign_column_is_read_and_never_validated(tmp_path):
    # WI-074: the optional Campaign grouping tag is read (like Workstream, no
    # vocabulary rule) and never breaks validation — a registry carrying it, with
    # arbitrary slug values, validates exactly as one without it.
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    hdr = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,Campaign\n"
    (req / "work-items.csv").write_text(
        hdr
        + "WI-001,A,scripts,,,done,d,my-campaign-2026\n"
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
