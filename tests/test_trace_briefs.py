"""trace.py — the re-attestation brief, baselined on the `last_approved`
snapshot (WI-277 split this file out of tests/test_trace.py by behavior
boundary; D-9 step 4 re-homed its baseline).

WI-316's `--ratify modified` brief and WI-325's freshness gate on it.

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


# --- WI-316: the re-attestation brief (--ratify modified) ----------------------
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
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
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
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "No approved baseline" not in proc.stdout
    assert "before: old text" in proc.stdout and "after: new text" in proc.stdout


def test_reattest_brief_empty_when_nothing_is_modified(scaffold):
    # Nothing drifted, nothing Drafted -> the explicit nothing-owed line (and
    # --out still writes). The selector read `Modified` until D-9 step 7.
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--ratify", "modified", "--out", "docs/ratify/r.md"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    written = (scaffold / "docs" / "ratify" / "r.md").read_text(encoding="utf-8")
    assert "No spine row differs from its" in written
    assert "no row awaits a first approval" in written


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


def _ratify_repo(tmp_path):
    """A git repo with an Approved SR chain amended IN PLACE (D-9 step 7 retired
    the flip), so
    `--ratify modified` has something real to render. Returns (run_git, rev) with
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
    return run_py(
        [
            SCRIPTS / "trace.py",
            "--root",
            tmp_path,
            "--ratify",
            "modified",
            "--out",
            tmp_path / "docs" / "ratify" / "brief.md",
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
            "--ratify",
            "modified",
            "--check",
            *extra,
        ],
        cwd=tmp_path,
    )


def test_a_current_brief_passes_the_check(tmp_path):
    _ratify_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "is current" in proc.stderr, proc.stderr


def test_a_SNAPSHOT_README_ONLY_commit_leaves_the_brief_FRESH(tmp_path):
    """MAJOR-11, 2026-08-20: `ratify_check` compared the derived stamp lines, so
    the brief went STALE on a commit that moved no row it renders — the snapshot's
    README, a `.gitignore`, anything that touches the snapshot directory or a
    registry's status line. A guard that fires on every commit is learned as
    noise, and the read it exists to force is the first thing dropped."""
    run_git, _rev, _write = _ratify_repo(tmp_path)
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
    _ratify_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    out = (tmp_path / "docs" / "ratify" / "brief.md").read_text(encoding="utf-8")
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
    _run_git, _rev, write = _ratify_repo(tmp_path)
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
    _run_git, _rev, write = _ratify_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    write("Approved", sr_req="The system shall do the RE-AMENDED thing.")
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "STALE" in proc.stderr


def test_a_missing_brief_is_a_no_op_not_a_failure(tmp_path):
    """The arming idiom: a downstream repo with no docs/ratify/ pays nothing."""
    _ratify_repo(tmp_path)
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

    THE COPY NAMES ITS AUTHORITY SINCE 2026-08-20. This amendment moves ratified
    text under a row that is already `Approved` — the D-9 ladder's own shape, and
    the one the authority gate makes a human declare (`--approves`), because it
    is indistinguishable from laundering without the declaration."""
    _run_git, _rev, write = _ratify_repo(tmp_path)
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
    _run_git, _rev, write = _ratify_repo(tmp_path)
    write("Approved", sr_req="The system shall do the AMENDED thing.")
    proc = run_py(
        [SCRIPTS / "trace.py", "--root", tmp_path, "--ratify", "modified"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "## SR-001" in proc.stdout
    assert "before: The system shall do the thing." in proc.stdout
    assert "after: The system shall do the AMENDED thing." in proc.stdout
    # ...and the copy is what clears it — carrying the ref that names the act,
    # since 2026-08-20: absorbing ratified text under a standing approval is the
    # one refresh that cannot be told from laundering without a human saying so.
    load_script("baseline_snapshot").copy_live(tmp_path, approves="the sitting")
    after = run_py(
        [SCRIPTS / "trace.py", "--root", tmp_path, "--ratify", "modified"],
        cwd=tmp_path,
    )
    assert "## SR-001" not in after.stdout
    assert "No spine row differs from its" in after.stdout


def test_the_newest_brief_is_chosen_by_stamped_name(tmp_path):
    """Briefs are date-stamped per sitting, so the live one is derived rather
    than configured — and by NAME, not mtime, because a checkout rewrites mtimes
    and this check exists precisely not to trust the working tree."""
    tr = load_script("trace")
    ratify = tmp_path / "docs" / "ratify"
    ratify.mkdir(parents=True)
    for name in ("2026-01-01-reattest.md", "2026-07-27-reattest.md", "README.md"):
        (ratify / name).write_text("x\n", encoding="utf-8")
    assert tr.newest_ratify_brief(tmp_path).name == "2026-07-27-reattest.md"
    assert tr.newest_ratify_brief(tmp_path / "nowhere") is None
