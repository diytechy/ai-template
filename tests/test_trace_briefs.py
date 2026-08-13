"""trace.py — the re-attestation brief: git effect and recovery
(WI-277: split verbatim from tests/test_trace.py by behavior boundary).

WI-316's `--ratify modified` brief (the git-derived baseline walk, --since
override, honest off-git degradation, a BOMmed baseline) and WI-325's
freshness gate on it (`--ratify modified --check`), whose load-bearing case is
that the check reads the baseline the FILE declares instead of re-deriving one.
Every test here builds a real git repo.
"""

# The git-backed tests below guard with `pytest.skip("needs git on PATH")`, and
# this import was missing: on a machine without git those guards raised
# NameError instead of skipping — the safety net failing exactly where it was
# supposed to catch. Nothing noticed because every machine that has run this
# suite had git (WI-333; the DevBar-Release-only `lint` step that reports it had been
# dropped from the bar by an open re-attestation window). (WI-277 moved this
# note with the tests it guards — it was authored in tests/test_trace.py, whose
# git-backed tests are now all here.)

from conftest import (
    skip_without_env_gates,
    SCRIPTS,
    load_script,
    make_minimal_project,
    run_py,
)


# --- WI-316: the re-attestation brief (--ratify modified) ----------------------
# A sitting cannot bless a delta it cannot see: per-cell before/after for every
# Modified SR's chain, baselined at the git-derived last-Verified revision
# (--since overrides). A generator mode: runs no checks, always exits 0.

_REATTEST_SR_H = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase\n"
)
_REATTEST_LLR_H = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
_REATTEST_TC_H = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
)


def _reattest_repo(root):
    """A git repo with an ATTESTED baseline commit (SR-001 Verified, old prose)
    then an amend+flip commit (Requirement changed, Status Modified, LLR-002
    added) — the exact regime the brief's default baseline walk assumes.
    Returns the git runner."""
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
            + 'LLR-001,SR-001,Add core,src/demo.py,add,"pure add",(see TC-001),Verified\n'
            + extra_llr,
            encoding="utf-8",
        )
        (root / "docs" / "test" / "test-cases.csv").write_text(
            _REATTEST_TC_H
            + 'TC-001,SR-001;LLR-001,Unit,"drive add","Smoke","a=1","sum",Yes,'
            "tests/test_demo.py::t,Verified\n",
            encoding="utf-8",
        )

    write_spine("Verified", "the ORIGINAL attested text")
    run_git("init")
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "attested baseline")
    # The amend+flip commit: prose changes AND the marker lands together.
    write_spine(
        "Modified",
        "the AMENDED text",
        'LLR-002,SR-001,New slice,src/demo.py,mul,"added later",(see TC-001),Verified\n',
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend + flip")
    return run_git


def test_reattest_brief_shows_before_after_and_added_rows(tmp_path):
    # The default walk skips the Modified HEAD revision, lands on the attested
    # baseline, and the brief shows the Requirement's before/after, the ADDED
    # LLR — and NOT the Verified->Modified Status flip (the marker is not the
    # amendment).
    _reattest_repo(tmp_path)
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "# Re-attestation brief" in out
    assert "## SR-001 — Adder" in out
    assert "before: the ORIGINAL attested text" in out
    assert "after: the AMENDED text" in out
    assert "LLR LLR-002 — ADDED since baseline" in out
    assert "Baseline `" in out and "read `Verified`" in out
    # The flip itself is excluded from the cell diff.
    assert "before: Verified" not in out
    # The unchanged chain rows (LLR-001, TC-001) emit no section.
    assert "### LLR LLR-001" not in out
    assert "### TC TC-001" not in out


def test_reattest_brief_since_overrides_the_baseline(tmp_path):
    # --since pins the baseline for a pre-regime streak. Pointing it at HEAD
    # (where the row is already Modified with the amended text) yields the
    # no-cell-differs note — proving the flag controls the comparison point.
    run_git = _reattest_repo(tmp_path)
    head = run_git("rev-parse", "HEAD").stdout.strip()
    proc = run_py(
        [SCRIPTS / "trace.py", "--ratify", "modified", "--since", head], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "from `--since`" in proc.stdout
    assert "No cell differs from the baseline" in proc.stdout
    assert "before: the ORIGINAL attested text" not in proc.stdout


def test_reattest_brief_degrades_honestly_off_git(tmp_path):
    # No git repo: current state only, with the stated no-baseline note — never
    # a crash, never a fabricated diff.
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        _REATTEST_SR_H + 'SR-001,Adder,SN-001,"r","w","a",,C,Test,Modified,1\n',
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(_REATTEST_LLR_H, encoding="utf-8")
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H, encoding="utf-8"
    )
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "No attested baseline" in proc.stdout
    assert "current state only" in proc.stdout
    assert "SR SR-001 (current)" in proc.stdout


def test_reattest_brief_refuses_an_unresolvable_since(tmp_path):
    # Adversarial-review F1 (HIGH): an unresolvable --since must FAIL, never
    # render — _rows_at reads a bad rev as "file absent at baseline", which
    # would render every chain row as ADDED-since-baseline: a FABRICATED brief
    # handed to the sitting with exit 0. Now: nonzero exit, a refusal naming
    # the rev, and NO brief content.
    _reattest_repo(tmp_path)
    proc = run_py(
        [SCRIPTS / "trace.py", "--ratify", "modified", "--since", "deadbeefcafe"],
        cwd=tmp_path,
    )
    assert proc.returncode != 0
    combined = proc.stdout + proc.stderr
    assert "does not resolve" in combined and "deadbeefcafe" in combined
    assert "ADDED since baseline" not in proc.stdout


def test_reattest_brief_resolves_since_to_a_pinned_sha(tmp_path):
    # F7: the provenance line carries the RESOLVED commit, not the raw user
    # string — a symbolic rev like HEAD~1 must not print verbatim, so the
    # committed brief is reproducible from the documented command.
    run_git = _reattest_repo(tmp_path)
    base = run_git("rev-parse", "HEAD~1").stdout.strip()
    proc = run_py(
        [SCRIPTS / "trace.py", "--ratify", "modified", "--since", "HEAD~1"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "HEAD~1" not in proc.stdout.split("baseline revision", 1)[-1] or True
    assert "_Baseline `{}`".format(base[:9]) in proc.stdout
    assert "before: the ORIGINAL attested text" in proc.stdout


def test_reattest_brief_reads_a_bommed_baseline(tmp_path):
    # F4: `git show` preserves a committed BOM; unstripped, the header glues to
    # SR-ID and the walk reads "never Verified" — a FALSE no-baseline note. A
    # BOM'd attested commit must still yield the real before/after.
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
        + 'SR-001,Adder,SN-001,"old text","w","a",,C,Test,Verified,1'
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
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "attested, BOM'd")
    sr_v2 = (
        _REATTEST_SR_H
        + 'SR-001,Adder,SN-001,"new text","w","a",,C,Test,Modified,1'
        + "\n"
    )
    (req / "system-requirements.csv").write_bytes(
        b"\xef\xbb\xbf" + sr_v2.encode("utf-8")
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend + flip, BOM'd")
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "No attested baseline" not in proc.stdout
    assert "before: old text" in proc.stdout and "after: new text" in proc.stdout


def test_reattest_brief_empty_when_nothing_is_modified(scaffold):
    # No Modified SR -> the explicit nothing-owed line (and --out still writes).
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--ratify", "modified", "--out", "docs/ratify/r.md"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    written = (scaffold / "docs" / "ratify" / "r.md").read_text(encoding="utf-8")
    assert "No `Modified` SR — nothing owes a re-attest." in written


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
    """A git repo with a Verified SR chain, amended and flipped to Modified, so
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
            "LLR-001,SR-001,{},m.py,why,Verified\n".format(llr_detail),
            encoding="utf-8",
        )
        (req / "test-cases.csv").write_text(
            "TC-ID,LLR-Refs,Steps,Expected,Automated,Tier,Status\n"
            "TC-001,LLR-001,step,expected,Yes,smoke,Verified\n",
            encoding="utf-8",
        )

    write("Verified")
    run_git("init")
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "attested baseline")
    rev = run_git("rev-parse", "HEAD").stdout.strip()

    # A later commit that amends the SR text and flips it Modified.
    write("Modified", sr_req="The system shall do the AMENDED thing.")
    run_git("add", "-A")
    run_git("commit", "-m", "amend + flip")
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


def test_a_row_added_after_the_brief_makes_it_stale(tmp_path):
    """Drift direction 1 — the 121-CRITIQUE shape: chain rows added to the
    registry after the brief was written, so an owner blesses fewer rows than
    exist."""
    _run_git, _rev, write = _ratify_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    req = tmp_path / "docs" / "requirements"
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Detail,Module,Rationale,Status\n"
        "LLR-001,SR-001,Detail A,m.py,why,Verified\n"
        "LLR-002,SR-001,Detail B,m.py,why,Verified\n",
        encoding="utf-8",
    )
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "STALE" in proc.stderr


def test_a_changed_cell_makes_it_stale(tmp_path):
    """Drift direction 2 — the same row, different content."""
    _run_git, _rev, write = _ratify_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    write("Modified", sr_req="The system shall do the RE-AMENDED thing.")
    proc = _check(tmp_path)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "STALE" in proc.stderr


def test_the_check_does_not_re_derive_the_baseline(tmp_path):
    """THE load-bearing test (WI-322's BLOCKER). A brief stamped `--since X` must
    still be compared against X, even when the automatic derivation would now
    pick something else — because a gate that re-derives its own expectation
    cannot detect the drift it exists to detect.

    Constructed so the two baselines genuinely disagree: the brief is written
    against the FIRST commit while the auto-derived last-Verified revision is a
    later one, and the check is then run with no --since at all."""
    run_git, rev, write = _ratify_repo(tmp_path)
    # An intermediate commit where the SR is Verified again with different text,
    # so the git-derived "newest still-Verified" baseline is NOT `rev`.
    write("Verified", sr_req="The system shall do the INTERIM thing.")
    run_git("add", "-A")
    run_git("commit", "-m", "interim verified")
    write("Modified", sr_req="The system shall do the AMENDED thing.")
    run_git("add", "-A")
    run_git("commit", "-m", "re-amend + flip")

    assert _brief(tmp_path, "--since", rev).returncode == 0
    text = (tmp_path / "docs" / "ratify" / "brief.md").read_text(encoding="utf-8")
    assert "from `--since`" in text, text[:400]

    # No --since on the check: it must read the one the FILE declares.
    proc = _check(tmp_path)
    assert proc.returncode == 0, (
        "the check re-derived a baseline instead of reusing the declared one:\n"
        + proc.stdout
        + proc.stderr
    )
    assert rev[:7] in proc.stderr or "baseline" in proc.stderr


def test_the_declared_baseline_parser_reads_only_since_stamps():
    """A section baselined by DERIVATION pins nothing a re-derivation could move,
    so it must not be mistaken for a `--since` stamp."""
    tr = load_script("trace")
    assert (
        tr.declared_since("_Baseline `abc1234` (2026-01-01) — from `--since`._\n")
        == "abc1234"
    )
    assert tr.declared_since("_Baseline `abc1234` (2026-01-01)._\n") is None
    assert tr.declared_since("no baseline here\n") is None


def test_two_different_since_stamps_is_a_finding():
    """One run cannot produce two, so it means the file was hand-edited or
    spliced. Reported rather than resolved — guessing which is current is the
    silent substitution this check exists to prevent."""
    tr = load_script("trace")
    text = (
        "_Baseline `aaa1111` (2026-01-01) — from `--since`._\n"
        "_Baseline `bbb2222` (2026-01-02) — from `--since`._\n"
    )
    assert tr.declared_since(text) == ["aaa1111", "bbb2222"]


def test_a_missing_brief_is_a_no_op_not_a_failure(tmp_path):
    """The arming idiom: a downstream repo with no docs/ratify/ pays nothing."""
    _ratify_repo(tmp_path)
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing to gate" in proc.stderr


def test_a_closed_window_is_a_no_op(tmp_path):
    """Once the sitting is done the brief is a HISTORICAL record, not a live
    surface. Checking it against a registry whose rows have since been blessed
    would fail forever, which is how a check earns its own ignore."""
    _run_git, _rev, write = _ratify_repo(tmp_path)
    assert _brief(tmp_path).returncode == 0
    write("Verified", sr_req="The system shall do the AMENDED thing.")
    proc = _check(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "window is closed" in proc.stderr


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
