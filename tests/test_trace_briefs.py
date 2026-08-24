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

from conftest import (
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
    assert "the commit that last wrote this record" in out, out
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
    the one the authority gate makes a human declare (`--approves`), because it
    is indistinguishable from laundering without the declaration."""
    _run_git, _rev, write = _approval_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    write("Approved", sr_req="The system shall do the AMENDED thing.")
    load_script("baseline_snapshot").copy_live(tmp_path, approves="the sitting")
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
    # ...and the copy is what clears it — carrying the ref that names the act,
    # since 2026-08-20: absorbing approved text under a standing approval is the
    # one refresh that cannot be told from laundering without a human saying so.
    load_script("baseline_snapshot").copy_live(tmp_path, approves="the sitting")
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
