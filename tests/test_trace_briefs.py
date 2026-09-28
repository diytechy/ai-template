"""trace.py — the re-attestation brief, baselined on the `last_approved`
snapshot (WI-277 split this file out of tests/test_trace.py by behavior
boundary; D-9 step 4 re-homed its baseline).

WI-316's `--approve modified` brief and WI-325's freshness gate on it.

WHAT LEFT THIS FILE AT D-9 STEP 4, and why none of it is a lost guarantee: the
git-derived baseline walk, the `--since` override (its unresolvable-rev refusal,
its sha pinning), the off-git degrade, and the "the check must not re-derive its
own baseline" pair. All four existed because the baseline was a DERIVATION over
history that a regeneration could move. It is now a directory of files, identical
on every machine and in CI, so there is nothing to re-derive, nothing to
override, and no history to be off. The properties those tests bought are now
structural rather than checked. The BOM case survives, re-aimed at the snapshot
file, because a BOM is a property of bytes on disk and the snapshot is bytes on
disk.
"""

# The git-backed tests below guard with `pytest.skip("needs git on PATH")`, and
# this import was missing: on a machine without git those guards raised
# NameError instead of skipping — the safety net failing exactly where it was
# supposed to catch. Nothing noticed because every machine that has run this
# suite had git (WI-333; the DevStg-Impl-only `lint` step that reports it had been
# dropped from the bar by an open re-attestation window). (WI-277 moved this
# note with the tests it guards — it was authored in tests/test_trace.py, whose
# git-backed tests are now all here.)

import re
import shutil

from conftest import (
    ROOT,
    skip_without_env_gates,
    SCRIPTS,
    load_script,
    make_minimal_project,
    pin_autocrlf,
    run_py,
)


# --- WI-316: the re-attestation brief (--approve modified) ----------------------
# A sitting cannot bless a delta it cannot see: per-cell before/after for every
# DRIFTED or Drafted SR's chain, baselined at the last_approved SNAPSHOT
# (git supplies only the stamp). A generator mode: no checks, always exits 0.

_REATTEST_SR_H = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase\n"
)
_REATTEST_LLR_H = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
_REATTEST_TC_H = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
)


def _reattest_repo(root):
    """A repo with an APPROVED SNAPSHOT (SR-001 Approved, old prose) and a live
    tree that has since been amended (Requirement changed,
    LLR-002 added). Returns the git runner. THE AMENDMENT NO LONGER FLIPS THE
    ROW: it wrote `Status = Modified` until D-9 step 7 retired that marker, so
    the live row stays `Approved` and DRIFT against the snapshot is what puts
    it in the brief — the fixture is closer to the real sequence, not further.

    The git repo is still built — the brief's stamp reads git, and the mirror
    invariant is a property of commits — but the BASELINE is now the snapshot
    copied before the amendment, not a revision walked back to."""
    import shutil as _sh
    import subprocess as _sp

    skip_without_env_gates("git")
    git = _sh.which("git")

    def run_git(*a):
        return _sp.run([git, "-C", str(root), *a], capture_output=True, text=True)

    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)

    def write_spine(sr_status, requirement, extra_llr=""):
        (req / "system-requirements.csv").write_text(
            _REATTEST_SR_H
            + 'SR-001,Adder,SN-001,"{}","why","old ac",,C,Test,{},1\n'.format(
                requirement, sr_status
            ),
            encoding="utf-8",
        )
        (req / "low-level-requirements.csv").write_text(
            _REATTEST_LLR_H
            + 'LLR-001,SR-001,Add core,src/demo.py,add,"pure add",(see TC-001),Approved\n'
            + extra_llr,
            encoding="utf-8",
        )
        (root / "docs" / "test" / "test-cases.csv").write_text(
            _REATTEST_TC_H
            + 'TC-001,SR-001;LLR-001,Unit,"drive add","Smoke","a=1","sum",Yes,'
            "tests/test_demo.py::t,Approved\n",
            encoding="utf-8",
        )

    write_spine("Approved", "the ORIGINAL attested text")
    run_git("init")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    # THE APPROVAL COPIES THE TEXT IT BLESSED — the whole mechanism, in the
    # fixture: the snapshot is taken while the tree still reads the original.
    load_script("baseline_snapshot").copy_live(root, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "attested baseline + snapshot")
    # The amendment: prose changes, NO cell announces it, and the snapshot
    # deliberately stays behind — that lag IS the signal.
    write_spine(
        "Approved",
        "the AMENDED text",
        'LLR-002,SR-001,New slice,src/demo.py,mul,"added later",(see TC-001),Approved\n',
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend, no flip — the D-9 regime")
    return run_git


def test_reattest_brief_shows_before_after_and_added_rows(tmp_path):
    # The brief diffs the live tree against the snapshot and shows the
    # Requirement's before/after, the ADDED LLR — and NOT the Status cell, which
    # `split_changed_cells` excludes structurally (the marker is not the
    # amendment, in either direction).
    _reattest_repo(tmp_path)
    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "# Re-attestation brief" in out
    assert "## SR-001 — Adder" in out
    assert "before: the ORIGINAL attested text" in out
    assert "after: the AMENDED text" in out
    assert "LLR LLR-002 — ADDED since the snapshot" in out
    assert "docs/archive/last_approved" in out
    # The header's instruction for the DRIFTED row it is about: an amended row
    # still reads `Approved`, so no flip carries it, and a bare `intake.py
    # snapshot` refuses it. The re-copy has to name it.
    assert "intake.py snapshot --reattests <ROW-ID>" in out
    # The Status cell itself is excluded from the diff, both directions.
    assert "before: Approved" not in out
    # The unchanged chain rows (LLR-001, TC-001) emit no section.
    assert "### LLR LLR-001" not in out
    assert "### TC TC-001" not in out


def test_reattest_brief_reads_a_bommed_baseline(tmp_path):
    # F4, re-aimed at the snapshot (D-9 step 4). A BOM is a property of bytes on
    # disk, and `copy_live` is byte-for-byte, so a BOM'd registry produces a
    # BOM'd snapshot. Unstripped on the read, the header glues to SR-ID and every
    # row reads as absent-from-the-snapshot — a FALSE "awaiting its first
    # approval" note on rows that were approved. The before/after must survive.
    import shutil as _sh
    import subprocess as _sp

    skip_without_env_gates("git")
    git = _sh.which("git")

    def run_git(*a):
        return _sp.run([git, "-C", str(tmp_path), *a], capture_output=True, text=True)

    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    sr_v1 = (
        _REATTEST_SR_H
        + 'SR-001,Adder,SN-001,"old text","w","a",,C,Test,Approved,1'
        + "\n"
    )
    (req / "system-requirements.csv").write_bytes(
        b"\xef\xbb\xbf" + sr_v1.encode("utf-8")
    )
    (req / "low-level-requirements.csv").write_text(_REATTEST_LLR_H, encoding="utf-8")
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H, encoding="utf-8"
    )
    run_git("init")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    load_script("baseline_snapshot").copy_live(tmp_path, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "attested, BOM'd + snapshot")
    sr_v2 = (
        _REATTEST_SR_H
        + 'SR-001,Adder,SN-001,"new text","w","a",,C,Test,Approved,1'
        + "\n"
    )
    (req / "system-requirements.csv").write_bytes(
        b"\xef\xbb\xbf" + sr_v2.encode("utf-8")
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend, no flip, BOM'd")
    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "No approved baseline" not in proc.stdout
    assert "before: old text" in proc.stdout and "after: new text" in proc.stdout


def test_reattest_brief_empty_when_nothing_is_modified(scaffold):
    # Nothing drifted, nothing Drafted -> the explicit nothing-owed line (and
    # --out still writes). The selector read `Modified` until D-9 step 7.
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--approve", "modified", "--out", "docs/ratify/r.md"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    written = (scaffold / "docs" / "ratify" / "r.md").read_text(encoding="utf-8")
    assert "No spine row differs from its" in written
    assert "no row awaits a first approval" in written


# --- the OI-61-sitting widening: a Drafted LLR/TC owes even under an --------
# --- Approved, undrifted SR (docs/log.d/2026-08-23-oi61-rule-and-spine-approval.md)


def test_reattest_brief_owes_a_drafted_llr_under_an_approved_undrifted_sr(tmp_path):
    """`trace.reattest_model`'s `owes()` used to test the SR row's own `Status`
    alone: `is_drafted(sr)` never looked at the chain, and `sr_chain_drifts`
    cannot see a `Drafted` child either (it has made no claim to fall from the
    snapshot). Widened so the brief a human approves from actually shows the
    row."""
    import shutil as _sh
    import subprocess as _sp

    skip_without_env_gates("git")
    git = _sh.which("git")

    def run_git(*a):
        return _sp.run([git, "-C", str(tmp_path), *a], capture_output=True, text=True)

    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        _REATTEST_SR_H
        + 'SR-001,Stable parent,SN-001,"a stable requirement","why","ac",,C,'
        "Test,Approved,1\n",
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(_REATTEST_LLR_H, encoding="utf-8")
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H, encoding="utf-8"
    )
    run_git("init")
    pin_autocrlf(tmp_path)
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    load_script("baseline_snapshot").copy_live(tmp_path, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "attested SR + snapshot, no LLR yet")
    # The SR is untouched after the snapshot — no drift. A brand-new `Drafted`
    # LLR is added under it: never approved, absent from the snapshot.
    (req / "low-level-requirements.csv").write_text(
        _REATTEST_LLR_H + 'LLR-001,SR-001,A new child,src/demo.py,add,"never approved",'
        "(see TC-001),Drafted\n",
        encoding="utf-8",
    )
    run_git("add", "-A")
    run_git("commit", "-m", "add a Drafted LLR under the stable SR")
    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "## SR-001 — Stable parent" in out
    assert "LLR LLR-001" in out
    assert "Drafted — never approved" in out
    # THE SR-177 GAP: the SR row itself carries no diff (it is `Approved` and
    # undrifted), so it never appeared in `entry["rows"]` at all — the anchor
    # block is the only thing that puts its own Requirement on the page.
    assert "> **Requirement.** a stable requirement" in out


def test_reattest_brief_truncates_long_anchor_requirement_with_marker(tmp_path):
    """Long-cell sanity: the anchor SR's own Requirement truncates above the
    1,500-char threshold with an explicit marker — never silently. A cell
    comfortably below the threshold renders untouched."""
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    long_req = "A" * 1600
    short_req = "B" * 100
    (req / "system-requirements.csv").write_text(
        _REATTEST_SR_H
        + 'SR-001,Long,SN-001,"{}","why","ac",,C,Test,Drafted,1\n'.format(long_req)
        + 'SR-002,Short,SN-001,"{}","why","ac",,C,Test,Drafted,1\n'.format(short_req),
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(_REATTEST_LLR_H, encoding="utf-8")
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H, encoding="utf-8"
    )
    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "more chars — read the registry row" in out
    assert "A" * 1500 in out
    assert "A" * 1600 not in out
    assert "B" * 100 in out


def _git_repo(root):
    """Init a committable git repo at `root`, skipping the test when git is
    absent. Returns the runner. The re-attestation baseline is the snapshot,
    but the brief still reads git for its stamp, so a repo has to exist."""
    import shutil as _sh
    import subprocess as _sp

    skip_without_env_gates("git")
    git = _sh.which("git")

    def run_git(*a):
        return _sp.run([git, "-C", str(root), *a], capture_output=True, text=True)

    run_git("init")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    return run_git


def test_reattest_brief_never_labels_a_drafted_rows_cells_approved(tmp_path):
    """OI-71 defect 1 — round 019 of the wi508 lane saw a `Drafted` row's cells
    rendered under the heading `approved — re-attestation owed`.

    `_cell_diff_lines` splits a changed row's cells into the §A5.1 two groups
    keyed on the cell's COLUMN class (`SPINE_APPROVED_CELLS`), independent of
    the ROW's Status. A `Drafted` TC that drifted in both an approved-class
    cell (`Method`) and a traced-class cell (`Evidence`) therefore renders its
    `Method` change under `approved — re-attestation owed` — asserting an
    attestation window that never opened, since the row was never approved. The
    row owes a FIRST approval wholesale, which its own section heading already
    states."""
    run_git = _git_repo(tmp_path)
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)

    def write_spine(method, evidence):
        (req / "system-requirements.csv").write_text(
            _REATTEST_SR_H
            + 'SR-001,Adder,SN-001,"a stable requirement","why","ac",,C,Test,Approved,1\n',
            encoding="utf-8",
        )
        (req / "low-level-requirements.csv").write_text(
            _REATTEST_LLR_H, encoding="utf-8"
        )
        (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
            _REATTEST_TC_H
            + 'TC-001,SR-001,Unit,"{}","Smoke","a=1","sum",Yes,"{}",Drafted\n'.format(
                method, evidence
            ),
            encoding="utf-8",
        )

    # Snapshot taken with the TC already Drafted (the snapshot copies every row
    # wholesale, approved or not), then the draft is edited in an approved-class
    # AND a traced-class cell — both groups non-empty, so the split heading shows.
    write_spine("drive the add path", "ev-old")
    load_script("baseline_snapshot").copy_live(tmp_path, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "attested SR + snapshot with a Drafted TC")
    write_spine("drive the add path anew", "ev-new")
    run_git("add", "-A")
    run_git("commit", "-m", "amend the Drafted TC in two cell classes")

    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    # The TC is on the page and correctly tagged as a never-approved draft...
    assert "TC TC-001" in out
    assert "Drafted — never approved" in out
    # ...and its cells are NOT labelled as owing a re-attestation: a Drafted row
    # was never approved, so no cell of it can owe one (OI-71 defect 1).
    assert "approved — re-attestation owed" not in out
    # The change itself is still shown, just not mislabelled.
    assert "drive the add path anew" in out


def test_reattest_brief_shows_a_long_changed_cell_whole(tmp_path):
    """OI-71 defect 2 — round 019 also saw a changed `Method` cell TRUNCATED so
    the reader could not see what changed. `_cell_diff_lines` ran each of
    before/after through `truncate_cell` (a 1,500-char PREFIX). A cell whose
    divergence sits past the cutoff truncates before AND after to the identical
    prefix, so the two render the same and the change vanishes. The changed cell
    must render WHOLE (the WI-554 Done-when)."""
    run_git = _git_repo(tmp_path)
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    head = "M" * 1500  # the common prefix, longer than CELL_TRUNCATE_LIMIT

    def write_spine(method_tail):
        (req / "system-requirements.csv").write_text(
            _REATTEST_SR_H
            + 'SR-001,Adder,SN-001,"a stable requirement","why","ac",,C,Test,Approved,1\n',
            encoding="utf-8",
        )
        (req / "low-level-requirements.csv").write_text(
            _REATTEST_LLR_H, encoding="utf-8"
        )
        (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
            _REATTEST_TC_H
            + 'TC-001,SR-001,Unit,"{}","Smoke","a=1","sum",Yes,ev,Approved\n'.format(
                head + method_tail
            ),
            encoding="utf-8",
        )

    write_spine("-OLD-TAIL")
    load_script("baseline_snapshot").copy_live(tmp_path, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "attested SR + snapshot with a long-Method TC")
    write_spine("-NEW-TAIL")
    run_git("add", "-A")
    run_git("commit", "-m", "amend the Method cell past the truncation cutoff")

    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    # Both the before and the after tail must be visible — otherwise the reader
    # cannot see what changed, which is exactly the defect.
    assert "-OLD-TAIL" in out, "the before tail was truncated away"
    assert "-NEW-TAIL" in out, "the after tail was truncated away"


def test_reattest_brief_stays_silent_for_an_approved_undrifted_chain(tmp_path):
    """The negative half: an `Approved` LLR under an `Approved`, undrifted SR
    owes nothing. The widening asks the chain the `Drafted` question; it must
    not turn every settled row into a false positive."""
    import shutil as _sh
    import subprocess as _sp

    skip_without_env_gates("git")
    git = _sh.which("git")

    def run_git(*a):
        return _sp.run([git, "-C", str(tmp_path), *a], capture_output=True, text=True)

    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        _REATTEST_SR_H
        + 'SR-001,Stable parent,SN-001,"a stable requirement","why","ac",,C,'
        "Test,Approved,1\n",
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(
        _REATTEST_LLR_H + 'LLR-001,SR-001,A stable child,src/demo.py,add,"settled",'
        "(see TC-001),Approved\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H, encoding="utf-8"
    )
    run_git("init")
    pin_autocrlf(tmp_path)
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    load_script("baseline_snapshot").copy_live(tmp_path, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "attested SR + Approved LLR + snapshot")
    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "No spine row differs from its" in proc.stdout
    assert "SR-001" not in proc.stdout


def test_reattest_model_owed_row_count_matches_the_live_drafted_llr_tc_census():
    """The number this widening is FOR: `docs/stage`'s `drafted` figure counts
    every `Drafted` SR/LLR/TC row (+ SN drafts) live in this repo's own
    registries, and this test asserts the widened `owes()` surfaces the SR/LLR/TC
    slice of that same count — not the literal 19 the OI-61 sitting measured
    (that number moves as the spine does), but whatever `is_drafted` counts on
    the tree under test right now.

    Runs against THIS repo's own live spine, the way `test_dogfood_sync.py`
    does — a fixture would only prove the code path once; the point of a
    dynamic assertion is that it re-proves itself on every future spine change.
    """
    import sys as _sys

    from conftest import ROOT

    if str(SCRIPTS) not in _sys.path:
        _sys.path.insert(0, str(SCRIPTS))
    import trace as _trace  # noqa: E402
    import spine_rules as _spine_rules  # noqa: E402

    reg = _trace.load_registries(ROOT / "docs")
    live_drafted = sum(
        1
        for rows in (reg.srs, reg.llrs, reg.tcs)
        for row in rows
        if _spine_rules.is_drafted(row)
    )
    model = _trace.reattest_model(ROOT, reg.srs, reg.llrs, reg.tcs)
    # Unique (kind, id), not a raw sum: a TC cited by more than one SR's chain
    # is deduped by design (`chain_of`'s `seen_tcs`) within one entry, but the
    # census question is "does every live Drafted row appear at least once",
    # which a set answers correctly even if some future spine shape let one
    # row surface under two SR entries.
    surfaced_drafted_ids = {
        (row["kind"], row["id"])
        for entry in model
        for row in entry["rows"]
        if row.get("drafted")
    }
    assert len(surfaced_drafted_ids) == live_drafted, (
        "the brief must surface every live Drafted SR/LLR/TC row at least once — "
        "got {} surfaced vs {} live".format(len(surfaced_drafted_ids), live_drafted)
    )


# --- WI-325: the re-attestation brief gets a freshness gate ---------------------
#
# Every other generated surface here is freshness-gated; the brief was not, and
# it went stale TWICE in one day — at 121-CRITIQUE missing two chain rows and an
# amendment (an owner would have blessed six rows having seen four), at
# 123-CRITIQUE three rows short. Both caught by a human noticing.
#
# The hard part is not the comparison, it is the BASELINE: the brief self-stamps
# one and reuses it, so `--check` must compare against the baseline the FILE
# declares. Re-deriving is the WI-322 review BLOCKER — a regeneration that
# silently collapsed 43 chain-row diffs to 18 while `--check` certified the loss.
# The `does not re-derive` test below is therefore the load-bearing one.


def _approval_repo(tmp_path):
    """A git repo with an Approved SR chain amended IN PLACE (D-9 step 7 retired
    the flip), so
    `--approve modified` has something real to render. Returns (run_git, rev) with
    `rev` the attested baseline commit."""
    import shutil as _sh
    import subprocess as _sp

    skip_without_env_gates("git")
    git = _sh.which("git")

    def run_git(*a):
        return _sp.run([git, "-C", str(tmp_path), *a], capture_output=True, text=True)

    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)

    def write(
        sr_status, sr_req="The system shall do the thing.", llr_detail="Detail A"
    ):
        (req / "system-requirements.csv").write_text(
            "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
            "Permutations,Priority,Verification,Status\n"
            'SR-001,Thing,SN-001,"{}",R,AC,,M,Test,{}\n'.format(sr_req, sr_status),
            encoding="utf-8",
        )
        (req / "low-level-requirements.csv").write_text(
            "LLR-ID,SR-Refs,Detail,Module,Rationale,Status\n"
            "LLR-001,SR-001,{},m.py,why,Approved\n".format(llr_detail),
            encoding="utf-8",
        )
        (req / "test-cases.csv").write_text(
            "TC-ID,LLR-Refs,Steps,Expected,Automated,Tier,Status\n"
            "TC-001,LLR-001,step,expected,Yes,smoke,Approved\n",
            encoding="utf-8",
        )

    write("Approved")
    run_git("init")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    load_script("baseline_snapshot").copy_live(tmp_path, seed=True)
    run_git("add", "-A")
    run_git("commit", "-m", "attested baseline + snapshot")
    rev = run_git("rev-parse", "HEAD").stdout.strip()

    # A later commit that amends the SR text, leaving its Status alone.
    write("Approved", sr_req="The system shall do the AMENDED thing.")
    run_git("add", "-A")
    run_git("commit", "-m", "amend, no flip — the D-9 regime")
    return run_git, rev, write


def _brief(tmp_path, *extra):
    # WI-503: the live surface is the fixed name CURRENT.md — `--check`'s
    # default out-path (no --out given) resolves to this same file, so the
    # fixture writes here rather than to an arbitrary name.
    return run_py(
        [
            SCRIPTS / "trace.py",
            "--root",
            tmp_path,
            "--approve",
            "modified",
            "--out",
            tmp_path / "docs" / "ratify" / "CURRENT.md",
            *extra,
        ],
        cwd=tmp_path,
    )


def _check(tmp_path, *extra):
    return run_py(
        [
            SCRIPTS / "trace.py",
            "--root",
            tmp_path,
            "--approve",
            "modified",
            "--check",
            *extra,
        ],
        cwd=tmp_path,
    )


def test_a_current_brief_passes_the_check(tmp_path):
    _approval_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "is current" in proc.stderr, proc.stderr


def test_a_SNAPSHOT_README_ONLY_commit_leaves_the_brief_FRESH(tmp_path):
    """MAJOR-11, 2026-08-20: `approval_check` compared the derived stamp lines, so
    the brief went STALE on a commit that moved no row it renders — the snapshot's
    README, a `.gitignore`, anything that touches the snapshot directory or a
    registry's status line. A guard that fires on every commit is learned as
    noise, and the read it exists to force is the first thing dropped."""
    run_git, _rev, _write = _approval_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    assert _check(tmp_path).returncode == 0
    readme = load_script("baseline_snapshot").snapshot_root(tmp_path) / "README.md"
    readme.write_text("# the stamp, re-worded\n", encoding="utf-8")
    run_git("add", "-A")
    run_git("commit", "-m", "prose only — the snapshot's own README")
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "is current" in proc.stderr, proc.stderr


def test_the_brief_states_what_the_stamp_IS_and_names_approval_provenance(tmp_path):
    """MAJOR-4, 2026-08-20: the baseline line called any snapshot write "the
    reviewed commit that last moved an approval", which a traced-cell refresh
    moves while approving nothing. It now says what `stamp` is, and the
    provenance a reader was being promised is derived beside it."""
    _approval_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    out = (tmp_path / "docs" / "ratify" / "CURRENT.md").read_text(encoding="utf-8")
    # Each registry's copy is named by the commit that last wrote THAT copy
    # (a refresh copies only what its act authorises), not the record's
    # newest write.
    assert "each registry's copy, named by the commit that last wrote it" in out, out
    assert "reviewed commit that last moved an approval" not in out
    assert "_Approval provenance:" in out, out
    # This fixture is a CSV-carrier repo, where a status move has no line shape
    # to pickaxe for — so the honest answer here is the degrade, stated rather
    # than guessed. `test_baseline_snapshot` drives the positive arm over the
    # TOML carrier this repo actually runs on.
    assert "or git cannot say" in out, out


def test_a_row_added_after_the_brief_makes_it_stale(tmp_path):
    """Drift direction 1 — the 121-CRITIQUE shape: chain rows added to the
    registry after the brief was written, so an owner blesses fewer rows than
    exist."""
    _run_git, _rev, write = _approval_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    req = tmp_path / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Detail,Module,Rationale,Status\n"
        "LLR-001,SR-001,Detail A,m.py,why,Approved\n"
        "LLR-002,SR-001,Detail B,m.py,why,Approved\n",
        encoding="utf-8",
    )
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "STALE" in proc.stderr


def test_a_changed_cell_makes_it_stale(tmp_path):
    """Drift direction 2 — the same row, different content."""
    _run_git, _rev, write = _approval_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    write("Approved", sr_req="The system shall do the RE-AMENDED thing.")
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "STALE" in proc.stderr


def test_a_missing_brief_is_a_no_op_not_a_failure(tmp_path):
    """The arming idiom: a downstream repo with no docs/ratify/ pays nothing."""
    _approval_repo(tmp_path)
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing to gate" in proc.stderr


def test_a_closed_window_is_a_no_op(tmp_path):
    """Once the sitting is done the brief is a HISTORICAL record, not a live
    surface. Checking it against a registry whose rows have since been blessed
    would fail forever, which is how a check earns its own ignore.

    CLOSING THE WINDOW NOW TAKES TWO ACTS, and that is D-9's whole point: the
    Status flip AND the copy that records what was blessed. See the test below
    for what the first without the second looks like.

    THE COPY NAMES ITS AUTHORITY SINCE 2026-08-20. This amendment moves approved
    text under a row that is already `Approved` — the D-9 ladder's own shape, and
    the one the authority gate makes a human declare, because it is
    indistinguishable from laundering without the declaration. Since SR-207 the
    declaration names the ROW (`--reattests`); the registry's ref alone clears
    none of its rows."""
    _run_git, _rev, write = _approval_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    write("Approved", sr_req="The system shall do the AMENDED thing.")
    load_script("baseline_snapshot").copy_live(
        tmp_path,
        approves={"docs/requirements/system-requirements.toml": "the sitting"},
        reattests={"SR-001"},
    )
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "window is closed" in proc.stderr


def test_a_flip_WITHOUT_a_copy_leaves_the_row_drifted(tmp_path):
    """THE LAUNDERING THE MECHANISM EXISTS TO CATCH, driven end to end.

    An owner who blesses the amendment by moving `Status` alone has changed the
    claim without moving the record of what the claim is about. Under the old
    git-derived baseline that closed the window — the row read `Approved`, so
    the walk stopped at HEAD and the diff was empty. Under the snapshot the row
    still differs from the text a human actually read, so it stays in the brief
    until the copy rides with it."""
    _run_git, _rev, write = _approval_repo(tmp_path)
    write("Approved", sr_req="The system shall do the AMENDED thing.")
    proc = run_py(
        [SCRIPTS / "trace.py", "--root", tmp_path, "--approve", "modified"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "## SR-001" in proc.stdout
    assert "before: The system shall do the thing." in proc.stdout
    assert "after: The system shall do the AMENDED thing." in proc.stdout
    # ...and the copy is what clears it — naming the row it re-attests (SR-207;
    # a ref for the act rides beside it since 2026-08-20): absorbing approved
    # text under a standing approval is the one refresh that cannot be told from
    # laundering without a human saying so.
    load_script("baseline_snapshot").copy_live(
        tmp_path,
        approves={"docs/requirements/system-requirements.toml": "the sitting"},
        reattests={"SR-001"},
    )
    after = run_py(
        [SCRIPTS / "trace.py", "--root", tmp_path, "--approve", "modified"],
        cwd=tmp_path,
    )
    assert "## SR-001" not in after.stdout
    assert "No spine row differs from its" in after.stdout


def test_current_brief_is_the_fixed_CURRENT_name_not_the_newest_dated_one(tmp_path):
    """WI-503: the live surface is CURRENT.md, a fixed name — not "newest
    dated file by filename" (the retired `newest_approval_brief` rule). A dated
    brief sitting beside it, even a lexicographically later one, is history
    and must never be picked up as the live surface."""
    tr = load_script("trace")
    approve = tmp_path / "docs" / "ratify"
    approve.mkdir(parents=True)
    for name in ("2026-01-01-reattest.md", "2099-07-27-reattest.md", "README.md"):
        (approve / name).write_text("x\n", encoding="utf-8")
    assert tr.current_approval_brief(tmp_path) is None
    (approve / "CURRENT.md").write_text("live\n", encoding="utf-8")
    assert tr.current_approval_brief(tmp_path).name == "CURRENT.md"
    assert tr.current_approval_brief(tmp_path / "nowhere") is None


def test_check_with_no_out_defaults_to_CURRENT_md_never_a_dated_file(tmp_path):
    """WI-503 Done-when: `--approve modified --check` with no --out compares
    against CURRENT.md, never against a dated brief that happens to sit in
    the same directory — the exact regression `newest_approval_brief` invited
    (a dated file kept being read/compared as though it were live)."""
    _approval_repo(tmp_path)
    approve = tmp_path / "docs" / "ratify"
    approve.mkdir(parents=True, exist_ok=True)
    # A dated file that would have been "newest by name" under the old rule —
    # deliberately STALE (empty), so a check that mistakenly targeted it would
    # report STALE while CURRENT.md, once written, is current.
    (approve / "2099-01-01-decoy.md").write_text("stale decoy\n", encoding="utf-8")
    assert _brief(tmp_path).returncode == 0  # writes CURRENT.md
    proc = _check(tmp_path)  # no --out: must resolve to CURRENT.md
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "is current" in proc.stderr, proc.stderr
    # The decoy is untouched — regeneration never writes a dated file.
    assert (approve / "2099-01-01-decoy.md").read_text(
        encoding="utf-8"
    ) == "stale decoy\n"


# --- WI-503: `--mint-approval-brief` — the one sanctioned dated-brief writer ----


def test_mint_copies_CURRENT_to_a_dated_immutable_file(tmp_path):
    tr = load_script("trace")
    approve = tmp_path / "docs" / "ratify"
    approve.mkdir(parents=True)
    (approve / "CURRENT.md").write_text("the live brief\n", encoding="utf-8")
    dest = tr.mint_approval_brief(tmp_path, "wi503", date="2026-08-22")
    assert dest == approve / "2026-08-22-wi503.md"
    assert dest.read_text(encoding="utf-8") == "the live brief\n"
    # CURRENT.md is untouched by the mint.
    assert (approve / "CURRENT.md").read_text(encoding="utf-8") == "the live brief\n"


def test_mint_refuses_without_a_CURRENT_brief(tmp_path):
    tr = load_script("trace")
    (tmp_path / "docs" / "ratify").mkdir(parents=True)
    try:
        tr.mint_approval_brief(tmp_path, "wi503", date="2026-08-22")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "CURRENT.md" in str(exc)


def test_mint_refuses_to_overwrite_an_existing_dated_brief(tmp_path):
    """The immutability guarantee lives here too, not only in the commit-time
    enforcer: minting twice at the same date+slug must not silently rewrite
    the first mint."""
    tr = load_script("trace")
    approve = tmp_path / "docs" / "ratify"
    approve.mkdir(parents=True)
    (approve / "CURRENT.md").write_text("v1\n", encoding="utf-8")
    tr.mint_approval_brief(tmp_path, "wi503", date="2026-08-22")
    (approve / "CURRENT.md").write_text("v2\n", encoding="utf-8")
    try:
        tr.mint_approval_brief(tmp_path, "wi503", date="2026-08-22")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "already exists" in str(exc)
    # The original mint is unchanged.
    assert (approve / "2026-08-22-wi503.md").read_text(encoding="utf-8") == "v1\n"


def test_mint_refuses_a_slug_with_a_bad_character(tmp_path):
    tr = load_script("trace")
    approve = tmp_path / "docs" / "ratify"
    approve.mkdir(parents=True)
    (approve / "CURRENT.md").write_text("v1\n", encoding="utf-8")
    for bad in ("", "  ", "wi 503", "wi/503", "../escape"):
        try:
            tr.mint_approval_brief(tmp_path, bad, date="2026-08-22")
            assert False, "expected ValueError for slug {!r}".format(bad)
        except ValueError:
            pass


def test_mint_cli_writes_and_reports(tmp_path):
    approve = tmp_path / "docs" / "ratify"
    approve.mkdir(parents=True)
    (approve / "CURRENT.md").write_text("the live brief\n", encoding="utf-8")
    proc = run_py(
        [
            SCRIPTS / "trace.py",
            "--root",
            tmp_path,
            "--mint-approval-brief",
            "wi503",
            "--mint-date",
            "2026-08-22",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "minted" in proc.stdout
    assert (approve / "2026-08-22-wi503.md").read_text(
        encoding="utf-8"
    ) == "the live brief\n"


def test_mint_cli_refuses_without_CURRENT_and_exits_nonzero(tmp_path):
    (tmp_path / "docs" / "ratify").mkdir(parents=True)
    proc = run_py(
        [SCRIPTS / "trace.py", "--root", tmp_path, "--mint-approval-brief", "wi503"],
        cwd=tmp_path,
    )
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "CURRENT.md" in (proc.stdout + proc.stderr)


# --- WI-518: the off-spine census — the brief cannot render per-row for the
# off-spine tiers (interfaces/external/components), and a re-seed absorbs them
# WHOLESALE regardless — see docs/log.d/2026-08-24-oi62-rule-and-spine-approval.md
# (the OI-62-sitting adversarial round's MAJOR-2). The fixture copies THIS
# repo's real registries (like test_baseline_snapshot.py's `_tree`) because the
# failure mode is about a whole-file snapshot copy and a real IF row, which a
# hand-rolled two-row fixture would not honestly exercise.


def _offspine_census_tree(tmp_path):
    """This repo's seven real registries, snapshotted, ready for one off-spine
    cell to be amended after the seed."""
    snap = load_script("baseline_snapshot")
    root = tmp_path / "repo"
    for rel in snap.SNAPSHOTTED:
        src = ROOT / rel
        if not src.is_file():
            continue
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    snap.copy_live(root, seed=True)
    return root


def test_offspine_census_names_the_interfaces_registry_after_an_IF_cell_changes(
    tmp_path,
):
    root = _offspine_census_tree(tmp_path)
    if_path = root / "docs" / "requirements" / "interfaces.toml"
    data = if_path.read_bytes()
    # The prose `contract` cell left the row at OI-67; the typed `data` cell is
    # the one a census amendment is driven through now.
    # Keyed on the cell's SHAPE (the `data = "..."` line of IF-001's block),
    # never on its text: a re-worded cell must not red a census test.
    m = re.search(rb'(?ms)^\[interface\.IF-001\]\n.*?^(data = ".*?")$', data)
    assert m, "fixture: IF-001's data cell not found"
    needle = m.group(1)
    if_path.write_bytes(
        data.replace(
            needle,
            needle[:-3] + b" (amended for WI-518's test)" + needle[-3:],
            1,
        )
    )
    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "docs/requirements/interfaces.toml" in out
    assert "1 changed, 0 added, 0 removed" in out
    # The census states what copies an off-spine registry. The implementation
    # copies on a row moving INTO approval or arriving approved (a de-approval
    # copies nothing), on `--approves` naming it, or on `--reattests` naming
    # one of its rows. Each trigger is driven in tests/test_baseline_snapshot.py:
    # test_a_spine_flip_LEAVES_the_offspine_snapshot_bytes_UNTOUCHED (into
    # approval), test_a_registry_WRITTEN_for_another_reason_still_gates_its_
    # amendments (arrives approved), test_a_DEAPPROVAL_cannot_authorise_an_
    # unrelated_approved_amendment (a de-approval authorises nothing),
    # test_an_explicit_APPROVES_ref_authorises_it_and_is_RECORDED (`--approves`)
    # and test_an_AMEND_PLUS_FLIP_authorises_ITS_OWN_row_and_no_other
    # (`--reattests` copies the live bytes).
    assert "a row in it moves into approval or arrives approved" in out
    assert "`--reattests` names one of its rows" in out
    # The earlier sentences were false: two triggers only, then any move.
    assert "moves or `--approves` names it" not in out
    assert "when its own `Status` moves" not in out
    # A no-change off-spine tier — components.toml here, untouched by the
    # fixture — renders NOTHING: no standing noise for a reader to learn to
    # ignore.
    assert "docs/requirements/components.toml" not in out
    assert "docs/requirements/external.toml" not in out


def test_offspine_census_renders_nothing_when_no_offspine_tier_changed(tmp_path):
    root = _offspine_census_tree(tmp_path)
    proc = run_py([SCRIPTS / "trace.py", "--approve", "modified"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "docs/requirements/interfaces.toml" not in out
    assert "docs/requirements/external.toml" not in out
    assert "docs/requirements/components.toml" not in out
    assert "Off-spine census" not in out


# --- OI-82, ruled (a) as the owner refined it: every unapproved chain stays on
# --- the owner's brief, and a chain the human-approval dial releases to an
# --- adjudicator renders in full under its own label, collapsed by default.

_WAITING = "Waiting for automated adjudication"


def _dial_split_tree(root, dial=None):
    """Three owing chains and no snapshot (so every row renders whole, which is
    the point: a released chain is shown in FULL, not as ids). With `dial` at
    `DevStg-Reqs` the SR rung is held and the LLR and TC rungs are released:

      * SR-001 is itself `Drafted`: its one owing row sits on the held rung.
      * SR-002 is `Approved`; only its LLR and TC are `Drafted`: every owing
        row sits on a released rung, so the whole chain is the adjudicator's.
      * SR-003 is `Drafted` with a `Drafted` LLR: a chain with ANY held row is
        still the owner's to sign, released rows beside it notwithstanding.

    `dial=None` writes no `docs/process.toml`, which is the shipped default
    (`DevStg-Release`, every rung held)."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        _REATTEST_SR_H + 'SR-001,Held parent,SN-001,"a held requirement","why","ac",,C,'
        "Test,Drafted,1\n"
        + 'SR-002,Released parent,SN-001,"a settled requirement","why","ac",,C,'
        "Test,Approved,1\n"
        + 'SR-003,Mixed parent,SN-001,"a mixed requirement","why","ac",,C,'
        "Test,Drafted,1\n",
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(
        _REATTEST_LLR_H
        + 'LLR-002,SR-002,Released child,src/demo.py,add,"the released detail",'
        "(see TC-002),Drafted\n"
        + 'LLR-003,SR-003,Mixed child,src/demo.py,mul,"the mixed detail",'
        "(see TC-003),Drafted\n",
        encoding="utf-8",
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H
        + 'TC-002,SR-002;LLR-002,Unit,"drive the released case","Smoke","a=1",'
        '"sum",Yes,tests/test_demo.py::t,Drafted\n',
        encoding="utf-8",
    )
    if dial is not None:
        (root / "docs" / "process.toml").write_text(
            '[attestation]\nhuman_approval_through = "{}"\n'.format(dial),
            encoding="utf-8",
        )


def _collapsed_block(text):
    """`(before, inside)`: the brief before its `<details>` block and the block's
    body. Fails when the block is missing, open by default, or not closed."""
    assert text.count("<details>") == 1, text
    assert "<details open" not in text
    before, rest = text.split("<details>", 1)
    assert "</details>" in rest, text
    return before, rest.split("</details>", 1)[0]


def test_a_released_rungs_chain_renders_in_full_collapsed_under_its_label(tmp_path):
    _dial_split_tree(tmp_path, dial="DevStg-Reqs")
    proc = _brief(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (tmp_path / "docs" / "ratify" / "CURRENT.md").read_text(encoding="utf-8")
    before, inside = _collapsed_block(text)
    # The label, where a reader sees it with the block still collapsed, and
    # the released chain's id, so the closed block says what it holds.
    summary = inside.split("</summary>")[0]
    assert "<summary>" in inside and _WAITING in summary
    assert "SR-002" in summary
    # The released chain is inside, rendered in FULL: its anchor text and every
    # owing row's cells, not a list of ids.
    assert "## SR-002 — Released parent" in inside
    assert "> **Requirement.** a settled requirement" in inside
    assert "### LLR LLR-002 (current)" in inside
    assert "**Detail**: the released detail" in inside
    assert "### TC TC-002 (current)" in inside
    assert "**Method**: drive the released case" in inside
    assert "SR-002" not in before
    # The held chains render as today, in the body, never in the block.
    assert "## SR-001 — Held parent" in before
    assert "> **Requirement.** a held requirement" in before
    assert "## SR-003 — Mixed parent" in before
    assert "**Detail**: the mixed detail" in before
    assert "SR-001" not in inside and "SR-003" not in inside
    # The page's own framing does not tell the owner to sign what the block
    # holds: the title claims no human act, and the signing instruction is
    # scoped to the sections outside the block.
    head = before.split("\n## ", 1)[0]
    assert "owing a human act" not in head
    assert "Rule on each section:" not in head
    assert "Rule on each section outside the collapsed" in head
    assert "not this sitting's" in head
    # The freshness gate reads the same rendering back.
    assert _check(tmp_path).returncode == 0


def test_the_shipped_default_dial_holds_every_chain_and_collapses_none(tmp_path):
    """No dial declared reads as `DevStg-Release`, which releases no spine
    tier: no collapsed block renders and every owing chain stays in the
    owner's section. (The title and signing instruction are the same at every
    level; only the block depends on the dial.)"""
    _dial_split_tree(tmp_path)
    proc = _brief(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (tmp_path / "docs" / "ratify" / "CURRENT.md").read_text(encoding="utf-8")
    assert "<details" not in text
    assert "## " + _WAITING not in text
    for heading in (
        "## SR-001 — Held parent",
        "## SR-002 — Released parent",
        "## SR-003 — Mixed parent",
    ):
        assert heading in text
    # The freshness gate reads the unsplit rendering back too.
    assert _check(tmp_path).returncode == 0


def test_a_dial_releasing_every_rung_leaves_the_owner_a_stated_empty_ask(tmp_path):
    """Every owing chain released: the owner's section says there is nothing on
    a held rung, rather than reading as an empty brief, and every chain is in
    the block."""
    _dial_split_tree(tmp_path, dial="DevStg-Below")
    proc = _brief(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (tmp_path / "docs" / "ratify" / "CURRENT.md").read_text(encoding="utf-8")
    before, inside = _collapsed_block(text)
    assert "No chain on a rung the human-approval dial holds" in before
    summary = inside.split("</summary>")[0]
    for sid in ("SR-001", "SR-002", "SR-003"):
        assert "## {} —".format(sid) in inside
        assert sid in summary
        assert sid not in before
    # The freshness gate reads the block over an empty owner's section back.
    assert _check(tmp_path).returncode == 0


def _amended_split_tree(root):
    """Two APPROVED chains snapshotted, then amended with every `Status` left
    `Approved` (the D-9 regime: an amendment flips nothing), under a dial that
    holds the SR rung and releases the LLR and TC rungs:

      * SR-001's own Requirement moved: a drifted row on the held rung, so the
        chain is the owner's re-attestation, as before the ruling.
      * SR-002's chain moved only below the SR: LLR-002's Detail changed and
        TC-002 left the registry. Every owing row is on a released rung, so the
        re-attestation is an adjudicator's, and its diff renders collapsed."""

    def write(sr1_req, llr2_detail, with_tc2):
        (req / "system-requirements.csv").write_text(
            _REATTEST_SR_H
            + 'SR-001,Held amended parent,SN-001,"{}","why","ac",,C,Test,'
            "Approved,1\n".format(sr1_req)
            + 'SR-002,Released amended parent,SN-001,"a settled requirement",'
            '"why","ac",,C,Test,Approved,1\n',
            encoding="utf-8",
        )
        (req / "low-level-requirements.csv").write_text(
            _REATTEST_LLR_H + 'LLR-001,SR-001,Held child,src/demo.py,add,"held detail",'
            "(see TC-001),Approved\n"
            + 'LLR-002,SR-002,Released child,src/demo.py,mul,"{}",'
            "(see TC-002),Approved\n".format(llr2_detail),
            encoding="utf-8",
        )
        (root / "docs" / "test" / "test-cases.csv").write_text(
            _REATTEST_TC_H
            + 'TC-001,SR-001;LLR-001,Unit,"drive the held case","Smoke","a=1",'
            '"sum",Yes,tests/test_demo.py::t,Approved\n'
            + (
                'TC-002,SR-002;LLR-002,Unit,"drive the released case","Smoke",'
                '"a=1","product",Yes,tests/test_demo.py::u,Approved\n'
                if with_tc2
                else ""
            ),
            encoding="utf-8",
        )

    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "test").mkdir(parents=True)
    write("the ORIGINAL held text", "the ORIGINAL released detail", True)
    load_script("baseline_snapshot").copy_live(root, seed=True)
    write("the AMENDED held text", "the AMENDED released detail", False)
    (root / "docs" / "process.toml").write_text(
        '[attestation]\nhuman_approval_through = "DevStg-Reqs"\n', encoding="utf-8"
    )


def test_a_released_rungs_re_attestation_renders_its_diff_in_the_collapsed_block(
    tmp_path,
):
    _amended_split_tree(tmp_path)
    proc = _brief(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    text = (tmp_path / "docs" / "ratify" / "CURRENT.md").read_text(encoding="utf-8")
    before, inside = _collapsed_block(text)
    # The released chain's re-attestation, whole, inside the block: the
    # changed cell's before/after and the row that left the chain.
    assert "## SR-002 — Released amended parent" in inside
    assert "### LLR LLR-002" in inside
    assert "before: the ORIGINAL released detail" in inside
    assert "after: the AMENDED released detail" in inside
    assert "### TC TC-002 — REMOVED since the snapshot" in inside
    assert "SR-002" not in before
    # The held chain's re-attestation stays on the owner's section.
    assert "## SR-001 — Held amended parent" in before
    assert "before: the ORIGINAL held text" in before
    assert "after: the AMENDED held text" in before
    assert "SR-001" not in inside
    assert _check(tmp_path).returncode == 0


# --- TC-235: the assumption section of the approval brief (SR-203, LLR-240) ---
# An assumption is approved for what it lets the requirements claim, so its
# section leads with the requirements citing it and the needs they reach, then
# where its outcome lands, its evidence and what would show it false. The tree
# below carries no snapshot and no git, so the brief is deterministic.

_GOLDEN_BRIEF = ROOT / "tests" / "golden" / "approval-brief-no-assumptions.txt"

_ASSUMPTION_NEEDS = """[need.SN-001]
status = "Approved"
need = "An operator sees the verdict of every run."
why = "A hidden verdict is acted on blind."
priority = "M"
acceptance = "The verdict is on screen."

[need.SN-002]
status = "Approved"
need = "A vendor's answers are trusted only as far as they were checked."
why = "An unchecked stand-in hides a broken integration."
priority = "S"
acceptance = "Every stand-in's fidelity is stated."
"""

_ASSUMPTION_SRS = """[requirement.SR-001]
title = "Show the verdict"
sn_refs = ["SN-001"]
requirement = "The system shall print each run's verdict."
rationale = "why"
acceptance_criteria = "the verdict is printed"
priority = "M"
verification = "Test"
status = "Approved"
da_refs = ["DA-001"]

[requirement.SR-002]
title = "Call the vendor"
sn_refs = ["SN-002"]
requirement = "The system shall call the vendor's lookup."
rationale = "why"
acceptance_criteria = "the lookup is called"
priority = "M"
verification = "Test"
status = "Approved"
da_refs = ["DA-002"]
"""

_ASSUMPTION_TCS = """[test.TC-001]
verifies = ["SR-001"]
level = "Unit"
method = "run once and read the console"
tier = "Full"
expected = "the verdict is printed"
automated = "Yes"
evidence = "tests/test_demo.py::t"
status = "Approved"
assumption_refs = ["DA-001"]
"""

_ASSUMPTION_FRAME = """[entity.EXT-001]
name = "Operator"
class = "operational"
description = "The person running the system."
status = "Approved"

[entity.EXT-002]
name = "Vendor lookup"
class = "enabling"
description = "The vendor's lookup service."
status = "Approved"

[boundary.B-01]
entity = "EXT-001"
direction = "out"
carries = "the run's verdict"
status = "Approved"

[boundary.B-02]
entity = "EXT-002"
direction = "inout"
carries = "the lookup"
status = "Approved"
"""

_ASSUMPTIONS = """[assumption.DA-001]
effect_at = ["B-01"]
assumption = "The operator reads the console after each run."
holds_when = "An operator is at the console."
obstacle = "The run is unattended."
falsifier = "A run whose verdict nobody acknowledged."
accepted_risk = "An unattended run goes unread for a day."
obstacle_hats = ["OPERATOR-HAT"]
status = "Drafted"
standing = "active"

[assumption.DA-002]
effect_at = ["B-02"]
assumption = "The recorded vendor stub answers as the vendor does."
holds_when = "The vendor's schema is unchanged."
obstacle = "The vendor changes its schema."
falsifier = "A live answer the stub would not give."
realized_by = "SUR-001"
status = "Drafted"
standing = "active"

[assumption.DA-003]
effect_at = ["B-01"]
assumption = "The console stand-in prints as the operator's terminal does."
holds_when = "The terminal is a plain text console."
obstacle = "A terminal that reflows lines."
realized_by = "SUR-002"
status = "Approved"
standing = "active"

[surrogate.SUR-001]
name = "Vendor stub"
emulates = ["EXT-002"]
description = "A recorded replay of the vendor's lookup."
status = "Drafted"

[surrogate.SUR-002]
name = "Console capture"
emulates = ["EXT-001"]
description = "A captured stdout standing in for the operator's terminal."
status = "Drafted"
"""


def _assumption_tree(root, assumptions=_ASSUMPTIONS):
    """A spine every row of which is approved, a frame of two crossings, and an
    assumptions registry: DA-001 plain and Drafted, DA-002 a Drafted fidelity
    assumption on SUR-001 (Drafted), and SUR-002 a lone Drafted surrogate that
    the Approved DA-003 names. No snapshot and no git, so the spine window is
    closed and the brief is deterministic."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)
    files = {
        req / "stakeholder-needs.toml": _ASSUMPTION_NEEDS,
        req / "system-requirements.toml": _ASSUMPTION_SRS,
        req / "low-level-requirements.toml": "",
        req / "external.toml": _ASSUMPTION_FRAME,
        req / "assumptions.toml": assumptions,
        root / "docs" / "test" / "test-cases.toml": _ASSUMPTION_TCS,
    }
    for path, text in files.items():
        path.write_text(text, encoding="utf-8", newline="\n")


def _section(text, heading):
    """The body of the `###` section whose heading starts `heading`, up to the
    next heading of the same or a higher level."""
    assert heading in text, text
    body = text.split(heading, 1)[1]
    return re.split(r"\n#{2,3} ", body, maxsplit=1)[0]


def _in_order(body, *needles):
    """Each needle is present, and each after the one before it."""
    at = -1
    for needle in needles:
        found = body.find(needle, at + 1)
        assert found > at, "{!r} missing or out of order in:\n{}".format(needle, body)
        at = found


def _current(root):
    return (root / "docs" / "ratify" / "CURRENT.md").read_text(encoding="utf-8")


def test_an_assumption_leads_with_its_citing_requirements_and_needs(tmp_path):
    _assumption_tree(tmp_path)
    proc = _brief(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    body = _section(_current(tmp_path), "### DA-001")
    # Citing requirements with their text first, then the needs derived
    # through them, the landing crossing with its party, the evidencing case
    # with the current evidence level, and the falsifier.
    _in_order(
        body,
        "SR-001",
        "The system shall print each run's verdict.",
        "SN-001",
        "An operator sees the verdict of every run.",
        "B-01",
        "EXT-001",
        "Operator",
        "TC-001",
        "specified",
        "A run whose verdict nobody acknowledged.",
    )
    # Its own cells are shown.
    for cell in (
        "The operator reads the console after each run.",
        "An operator is at the console.",
        "The run is unattended.",
        "active",
    ):
        assert cell in body, cell


def test_every_cell_of_an_owing_row_appears_in_its_section(tmp_path):
    """SR-203's "shows its cells": every non-empty cell of each owing assumption
    and surrogate, status and pointer cells included, is on the page, whether
    as its own bullet or in the structural line that carries it."""
    _assumption_tree(tmp_path)
    assert _brief(tmp_path).returncode == 0
    text = _current(tmp_path)
    path = tmp_path / "docs" / "requirements" / "assumptions.toml"
    carrier = load_script("spine_carrier")
    for id_col in ("DA-ID", "SUR-ID"):
        for row in carrier.load(path, id_col, keep_examples=False):
            if row["Status"] != "Drafted":
                continue
            body = _section(text, "### " + row[id_col])
            for column, value in row.items():
                if column == id_col:
                    continue  # the section's own heading
                for part in value.split(";"):
                    assert part.strip() in body, (row[id_col], column, part)
            assert "**Status**: Drafted" in body, row[id_col]
    assert "OPERATOR-HAT" in _section(text, "### DA-001")


def test_the_evidence_line_says_it_is_computed_at_render_time(tmp_path):
    """The evidence level reads the current results and the clock, so its line
    says so, and the freshness comparison leaves it out, as it does the
    git-derived stamps: an expiring sample must not stale a brief whose rows did
    not move."""
    _assumption_tree(tmp_path)
    assert _brief(tmp_path).returncode == 0
    line = next(ln for ln in _current(tmp_path).splitlines() if "Evidence level" in ln)
    assert "computed at render time" in line
    trace = load_script("trace")
    assert line.startswith(trace._DERIVED_STAMP_PREFIXES)


def test_a_fidelity_assumption_is_shown_beside_its_surrogate(tmp_path):
    _assumption_tree(tmp_path)
    assert _brief(tmp_path).returncode == 0
    body = _section(_current(tmp_path), "### DA-002")
    _in_order(body, "SR-002", "SN-002", "B-02")
    for needle in ("SUR-001", "Vendor stub", "EXT-002", "Vendor lookup"):
        assert needle in body, needle


def test_a_lone_surrogate_is_shown_with_the_assumptions_naming_it(tmp_path):
    _assumption_tree(tmp_path)
    assert _brief(tmp_path).returncode == 0
    text = _current(tmp_path)
    body = _section(text, "### SUR-002")
    for needle in (
        "Console capture",
        "EXT-001",
        "DA-003",
        "The console stand-in prints as the operator's terminal does.",
    ):
        assert needle in body, needle
    # DA-003 itself is approved and owes nothing, so it has no section.
    assert "### DA-003" not in text


def test_a_batch_holding_only_assumptions_is_rendered_and_freshness_checked(
    tmp_path,
):
    """No spine row owes an act, so the spine window alone is closed; the
    assumptions owing approval keep it open, and an edit to one makes the
    committed brief stale."""
    _assumption_tree(tmp_path)
    assert _brief(tmp_path).returncode == 0
    proc = _check(tmp_path)
    assert proc.returncode == 0 and "is current" in proc.stderr, proc.stderr
    changed = _ASSUMPTIONS.replace(
        "The operator reads the console after each run.",
        "The operator reads the console at the end of the day.",
    )
    _assumption_tree(tmp_path, changed)
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "STALE" in proc.stderr


def _approve(tmp_path, scope):
    return run_py(
        [SCRIPTS / "trace.py", "--root", tmp_path, "--approve", scope],
        cwd=tmp_path,
    )


def test_the_assumptions_scope_renders_every_assumption_owing_approval(tmp_path):
    _assumption_tree(tmp_path)
    proc = _approve(tmp_path, "assumptions")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for heading in ("### DA-001", "### DA-002", "### SUR-001", "### SUR-002"):
        assert heading in proc.stdout, heading
    assert "### DA-003" not in proc.stdout


def test_an_assumption_id_scope_renders_the_named_rows(tmp_path):
    _assumption_tree(tmp_path)
    proc = _approve(tmp_path, "DA-003,SUR-001")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "### DA-003" in proc.stdout and "### SUR-001" in proc.stdout
    assert "### DA-001" not in proc.stdout
    # An id the registry does not declare is refused, never rendered empty.
    assert _approve(tmp_path, "DA-099").returncode != 0


def test_the_assumptions_scope_with_nothing_owing_is_refused(tmp_path):
    _assumption_tree(tmp_path, _ASSUMPTIONS.replace('"Drafted"', '"Approved"'))
    proc = _approve(tmp_path, "assumptions")
    assert proc.returncode != 0
    assert "refusing" in (proc.stdout + proc.stderr)


def _golden_brief_tree(root, assumptions):
    _dial_split_tree(root)
    if assumptions is not None:
        (root / "docs" / "requirements" / "assumptions.toml").write_text(
            assumptions, encoding="utf-8", newline="\n"
        )


def test_a_brief_with_no_assumption_owing_is_byte_identical_to_the_golden(tmp_path):
    """The stored golden was rendered by the code before the assumption section
    existed. Three trees must render it byte for byte: no assumptions registry,
    the template's example rows only, and assumptions that owe nothing.

    Regenerate the golden (only when a change to the brief's output is intended
    and reviewed) with:
    UPDATE_BRIEF_GOLDEN=1 python -m pytest tests/test_trace_briefs.py"""
    import os

    template = (
        ROOT / "project-trajectory" / "registries" / "assumptions.template.toml"
    ).read_text(encoding="utf-8")
    approved = _ASSUMPTIONS.replace('"Drafted"', '"Approved"')
    for label, assumptions in (
        ("none", None),
        ("template", template),
        ("approved", approved),
    ):
        root = tmp_path / label
        root.mkdir()
        _golden_brief_tree(root, assumptions)
        assert _brief(root).returncode == 0
        text = (root / "docs" / "ratify" / "CURRENT.md").read_bytes()
        if os.environ.get("UPDATE_BRIEF_GOLDEN") and label == "none":
            _GOLDEN_BRIEF.write_bytes(text)
        assert text == _GOLDEN_BRIEF.read_bytes(), label
