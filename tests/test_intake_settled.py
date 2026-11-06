"""The trunk mint skips an amendment the merged range already settled (TC-403).

The trunk mint (`intake._routed_amendments`, reached by `intake_after_merge` from
the merge slot's post-merge arm and by `intake.py sweep`) files one
`adjudicate:` row for every approved row whose text moved across a merge. A
lane that amended a row, sat it and re-attested it in its own act has already
settled that change, so minting it again files a redundant row. The filter
drops a record only when an act-ledger entry the range ADDED re-attests the row
AND the row's whole approved and routed traced cell set at the range's `after`
tree equals its copy in the approved snapshot at that tree (LLR-364).

Every ledger, copy and range here is produced by the real producer,
`baseline_snapshot.copy_live` (what `intake.py snapshot` and the act turn
reach), committed into a real git repo. Only the refusal arms, and the
missing-copy guard, break a carrier by hand: a file that does not parse, a
loose object deleted so the tree still lists the path but its blob cannot be
read (a partial clone offline, a damaged store), or a copy without the row.

A guard test characterizes behaviour that held before the filter existed, and
its docstring names the wrong filter it would catch.
"""

import os
import subprocess
import tomllib

import pytest
from conftest import (
    ROOT,
    SCRIPTS,
    env_gate_skipif,
    hooks_on,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
)

# The tree still lists the path, but its blob cannot be read.
from test_ruling_sync import _drop_blob

pytestmark = env_gate_skipif("git")

intake = load_script("intake")
acceptance_record = load_script("acceptance_record")
SNAP = load_script("baseline_snapshot")
trace = load_script("trace")


SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
COPY_REL = "{}/{}".format(SNAP.SNAPSHOT_DIR, SR_REL)
ACTS_REL = "{}/{}".format(SNAP.SNAPSHOT_DIR, SNAP.ACTS)

ORIGINAL = "The system shall add two numbers."
AMENDED = "The system shall add two integers."
AC_ORIGINAL = "add(1, 2) == 3"
AC_AMENDED = "add(1, 2) == 3 and add(-1, 1) == 0"

T0 = 1_000_000


# --- the repo, its registry and its commits -------------------------------------


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _commit(root, message):
    """Commit the whole tree at a strictly later fixed time than the last."""
    _commit.tick = getattr(_commit, "tick", T0) + 10
    stamp = "@{} +0000".format(_commit.tick)
    env = dict(os.environ, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
    for args in (("add", "-A"), ("commit", "-qm", message)):
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
    return _git(root, "rev-parse", "HEAD")


def _sr_row(rid, requirement, acceptance, status, sn_refs="SN-001", phase=1):
    return (
        "[requirement.{rid}]\n"
        'title = "Adder"\n'
        'sn_refs = ["{sn_refs}"]\n'
        'requirement = "{req}"\n'
        'rationale = "Realizes SN-001."\n'
        'acceptance_criteria = "{ac}"\n'
        'priority = "M"\n'
        'verification = "Test"\n'
        'status = "{status}"\n'
        "phase = {phase}\n"
    ).format(
        rid=rid,
        req=requirement,
        ac=acceptance,
        status=status,
        sn_refs=sn_refs,
        phase=phase,
    )


def _write_srs(root, requirement=ORIGINAL, acceptance=AC_ORIGINAL, extra="", **cells):
    """The SR registry: the one Approved row SR-001 (its traced `cells`, if
    given: `sn_refs`, `phase`), plus any `extra` rows."""
    path = root / SR_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    text = _sr_row("SR-001", requirement, acceptance, "Approved", **cells) + extra
    path.write_bytes(text.encode("utf-8"))


def _write_llrs(root, text):
    path = root / LLR_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def _repo(tmp_path, seed=True, extra="", llrs=""):
    """A trunk carrying SR-001 Approved (plus any `extra` SR rows and any
    `llrs` LLR registry text) and, when `seed`, its first snapshot (ledger
    seq 1). `(root, sha)`."""
    skip_without_env_gates("git")
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    pin_autocrlf(root)
    hooks_on(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    (root / "docs").mkdir()
    (root / trace.WATERMARK).write_text(
        trace.render_watermark({s: 0 for s in trace.WATERMARK_SPACES}),
        encoding="utf-8",
        newline="\n",
    )
    _write_srs(root, extra=extra)
    if llrs:
        _write_llrs(root, llrs)
    if seed:
        SNAP.copy_live(root, seed=True)
    return root, _commit(root, "the owner's first signing")


def _act(root, *rids):
    """The act turn's snapshot: copy the live rows, re-attesting `rids`."""
    SNAP.copy_live(root, reattests=frozenset(rids))
    return _commit(root, "act: re-attest " + ", ".join(rids))


def _trunk_moves_on(root):
    """One more act on trunk after the range, re-attesting SR-001 again. The
    mint cuts its scratch worktree at HEAD, so HEAD must not hold a blob the
    test drops: a sweep over an earlier range sees exactly this."""
    _act(root, "SR-001")


def _settled(tmp_path):
    """The lane that already settled its amendment: the range amends SR-001's
    requirement, then commits the act re-attesting it (ledger seq 2), so the
    row at `after` equals its copy. `(root, before, after)`."""
    root, before = _repo(tmp_path)
    _write_srs(root, requirement=AMENDED)
    _commit(root, "amend SR-001")
    return root, before, _act(root, "SR-001")


# --- what the mint did ------------------------------------------------------------


def _frontmatter(root, relpath):
    text = (root / relpath).read_text(encoding="utf-8")
    return tomllib.loads(text.split("+++")[1])


def _amendment_rows(root, minted):
    """The minted rows whose title is the amendment arm's."""
    return [
        meta
        for meta in (_frontmatter(root, rel) for _wid, rel in minted)
        if "approved/routed cell(s) amended" in meta["title"]
    ]


def _sweep(root, before, after):
    """`intake.py sweep --before --after`, the hand landing's route, as a
    subprocess: `(proc, HEAD before the sweep, HEAD after it)`."""
    head = _git(root, "rev-parse", "HEAD")
    proc = run_py(
        [
            SCRIPTS / "intake.py",
            "--root",
            root,
            "sweep",
            "--before",
            before,
            "--after",
            after,
        ],
        cwd=root,
    )
    return proc, head, _git(root, "rev-parse", "HEAD")


def _assert_sweep_refused(root, before, after):
    proc, head, new_head = _sweep(root, before, after)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert new_head == head, "the refused sweep wrote a mint commit"


def _assert_refused(refusal, carrier, rev, kind):
    """The refusal names the carrier, the revision and what went wrong, and
    says the MINT was refused: at the post-merge arm the merge has landed."""
    assert refusal, "no refusal"
    assert carrier in refusal, refusal
    assert rev[:7] in refusal, refusal
    assert kind in refusal, refusal
    assert "mint was refused" in refusal, refusal
    assert "nothing was merged" not in refusal, refusal
    # The recovery: a same-range sweep re-reads the same blob at `after`, so it
    # succeeds only once a blob that could not be read is fetched; a carrier
    # fixed in a reviewed commit is swept with `--after` at that commit.
    assert "fetched" in refusal, refusal
    assert "`--after` at the fixing commit" in refusal, refusal


# --- D1: a settled row mints nothing, at both routes -------------------------------


def test_a_row_reattested_in_range_and_equal_to_its_copy_mints_nothing(tmp_path):
    """Implements: TC-403"""
    root, before, after = _settled(tmp_path)
    # The hand landing's route first: today it mints the redundant row.
    proc, head, new_head = _sweep(root, before, after)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing to mint." in proc.stdout, proc.stdout
    assert new_head == head, "the sweep wrote a mint commit"
    # The merge slot's post-merge arm: the same one filter.
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    assert minted == [], minted
    # The walk itself is unfiltered, so the pre-commit warn still sees it.
    walk = acceptance_record.staged_spine_amendments(root, before, after)
    assert [rec["id"] for rec in walk] == ["SR-001"]


# --- D2, D3: what the filter must not drop ---------------------------------------


def test_a_row_amended_again_after_its_act_still_mints(tmp_path):
    """Guard: a row re-attested in the range and then amended again still
    mints. Catches a filter that reads only the ledger and skips the snapshot
    comparison: the ledger alone says SR-001 was settled.

    Implements: TC-403
    """
    root, before, _act_sha = _settled(tmp_path)
    _write_srs(root, requirement=AMENDED + " Again.")
    after = _commit(root, "amend SR-001 after its act")
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


def test_an_amendment_with_no_act_in_range_still_mints(tmp_path):
    """Guard: an older act outside the range settles nothing in it. Before the
    range, an act re-attests SR-001 at text A and a later commit moves it to
    text B; the range restores A. At `after` the row equals its copy and the
    WHOLE ledger re-attests it, but no entry the range added does. Catches a
    filter that reads the whole ledger rather than the entries the range
    added.

    Implements: TC-403
    """
    root, _seed = _repo(tmp_path)
    _write_srs(root, requirement=AMENDED)
    _commit(root, "amend SR-001")
    _act(root, "SR-001")
    _write_srs(root, requirement=AMENDED + " Drifted.")
    before = _commit(root, "amend SR-001 with no act")
    _write_srs(root, requirement=AMENDED)
    after = _commit(root, "the range restores the copied text")
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["title"].startswith(
        "adjudicate: SR-001 - approved/routed cell(s) amended on merged trunk "
        "{}..{} ".format(before[:7], after[:7])
    ), row["title"]
    assert row["adjudicates"] == ["SR-001"]


# --- D4: the fail directions -------------------------------------------------------


def test_an_absent_ledger_filters_nothing(tmp_path):
    """Guard: a fresh adopter has no ledger before its first signing, and that
    is no acts, never a refusal. Catches an absent ledger read as a refusal,
    and a tri-state reader that treats "the tree does not list it" as a read
    failure. The contrast the unreadable-blob refusal is measured against.

    Implements: TC-403
    """
    root, before = _repo(tmp_path, seed=False)
    _write_srs(root, requirement=AMENDED)
    after = _commit(root, "amend SR-001")
    assert ACTS_REL not in _git(root, "ls-tree", "-r", "--name-only", after)
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


def _close_report(root, wi):
    """One early close: a `partial/` spec and its report, so the close arm
    mints a disposition row the outcomes map names."""
    spec = root / "docs" / "work" / "partial" / "{}-returned.md".format(wi)
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_bytes(
        '+++\nid = "{}"\ntitle = "Returned"\nspecref = "docs/id-watermark"\n+++\n'.format(
            wi
        ).encode("utf-8")
    )
    report = root / "docs" / "handbacks" / "{}-b.md".format(wi)
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_bytes(
        "\n".join(
            [
                "+++",
                'wi = "{}"'.format(wi),
                'branch = "b"',
                'claimed_outcome = "partial"',
                'reason = "stopped early"',
                'commit_range = "aaa..bbb"',
                'suggested_tier = "strong"',
                'keep_commits = ["aaa"]',
                "discard_commits = []",
                "+++",
                "",
            ]
        ).encode("utf-8")
    )


@pytest.mark.parametrize("broken", ["malformed", "unreadable"])
def test_the_filter_is_not_consulted_without_amendment_records(tmp_path, broken):
    """Guard: a range that amends no approved row never reads the ledger, so a
    broken one cannot refuse an unrelated mint, and the other arms still run.
    Catches a filter consulted unconditionally.

    Implements: TC-403
    """
    root, before = _repo(tmp_path)
    _close_report(root, "WI-005")
    if broken == "malformed":
        (root / ACTS_REL).write_bytes(b"[[act]\nseq = \n")
    else:
        with (root / ACTS_REL).open("ab") as fh:
            fh.write(b"\n# a byte the seed's blob does not carry\n")
    after = _commit(root, "an early close lands")
    if broken == "unreadable":
        _trunk_moves_on(root)
        _drop_blob(root, after, ACTS_REL)
    minted, refusal = intake.intake_after_merge(
        root, before, after, {"WI-005": "partial"}, ""
    )
    assert refusal is None, refusal
    assert _amendment_rows(root, minted) == []
    titles = [_frontmatter(root, rel)["title"] for _wid, rel in minted]
    assert len(titles) == 1 and "WI-005" in titles[0], titles


def test_a_malformed_ledger_refuses_the_mint_by_name(tmp_path):
    """...and the recovery the refusal states works: the same range re-reads
    the same blob and refuses again, while a sweep whose `--after` is the
    reviewed commit that fixes the ledger passes.

    Implements: TC-403
    """
    root, before, act_sha = _settled(tmp_path)
    good = _git(root, "show", "{}:{}".format(act_sha, ACTS_REL)) + "\n"
    (root / ACTS_REL).write_bytes(b"[[act]\nseq = \n")
    after = _commit(root, "a ledger that does not parse")
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert minted == [], minted
    _assert_refused(refusal, ACTS_REL, after, "does not parse")
    _assert_sweep_refused(root, before, after)
    (root / ACTS_REL).write_bytes(good.encode("utf-8"))
    fixed = _commit(root, "fix the ledger")
    _assert_sweep_refused(root, before, after)
    proc, head, new_head = _sweep(root, before, fixed)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing to mint." in proc.stdout, proc.stdout
    assert new_head == head


@pytest.mark.parametrize("side", ["after", "before"])
def test_an_unreadable_ledger_blob_refuses_the_mint_by_name(tmp_path, side):
    """A ledger the tree lists but whose blob cannot be read is never read as
    absent: absent would mint, as the absent-ledger guard does. The two sides'
    blobs differ, since the act appended seq 2.

    Implements: TC-403
    """
    root, before, after = _settled(tmp_path)
    _trunk_moves_on(root)
    rev = after if side == "after" else before
    assert _git(root, "rev-parse", "{}:{}".format(before, ACTS_REL)) != _git(
        root, "rev-parse", "{}:{}".format(after, ACTS_REL)
    )
    _drop_blob(root, rev, ACTS_REL)
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert minted == [], minted
    _assert_refused(refusal, ACTS_REL, rev, "cannot be read")
    _assert_sweep_refused(root, before, after)


def test_a_malformed_snapshot_copy_refuses_the_mint_by_name(tmp_path):
    """Implements: TC-403"""
    root, before, _act_sha = _settled(tmp_path)
    copy = root / COPY_REL
    copy.write_bytes(copy.read_bytes() + b"\n[requirement.SR-001\n")
    after = _commit(root, "a snapshot copy that does not parse")
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert minted == [], minted
    _assert_refused(refusal, COPY_REL, after, "does not parse")


def test_an_unreadable_snapshot_copy_blob_refuses_the_mint_by_name(tmp_path):
    """The copy of a settled registry is byte-identical to the live file at the
    act, so the two would share one blob and dropping it would also empty the
    walk: the filter would never be consulted and the test would pass
    vacuously. The range therefore ends by adding a Drafted row to the live
    registry, so the live blob differs from the copy's and SR-001 stays
    settled.

    Implements: TC-403
    """
    root, before, _act_sha = _settled(tmp_path)
    _write_srs(
        root,
        requirement=AMENDED,
        extra="\n" + _sr_row("SR-002", "A drafted row.", "ac", "Drafted"),
    )
    after = _commit(root, "a Drafted row after the act")
    copy_blob = _git(root, "rev-parse", "{}:{}".format(after, COPY_REL))
    assert copy_blob != _git(root, "rev-parse", "{}:{}".format(after, SR_REL))
    assert copy_blob != _git(root, "rev-parse", "{}:{}".format(before, SR_REL))
    _trunk_moves_on(root)
    assert copy_blob != _git(root, "rev-parse", "HEAD:" + COPY_REL)
    _drop_blob(root, after, COPY_REL)
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert minted == [], minted
    _assert_refused(refusal, COPY_REL, after, "cannot be read")


@pytest.mark.parametrize("copy", ["without-the-row", "absent"])
def test_a_reattested_row_missing_from_its_copy_still_mints(tmp_path, copy):
    """Guard: a row the ledger re-attests is not proven settled unless its copy
    holds it, and an absent copy is not a refusal. Catches a missing copy (or a
    missing row in it) read as settled, and an absent copy read as a refusal.
    The copy is broken by hand: no supported act writes either shape, but the
    filter's answer to them is part of its contract.

    Implements: TC-403
    """
    root, before, _act_sha = _settled(tmp_path)
    if copy == "absent":
        _git(root, "rm", "-q", COPY_REL)
    else:
        other = _sr_row("SR-002", "Another row.", "ac", "Approved")
        (root / COPY_REL).write_bytes(other.encode("utf-8"))
    after = _commit(root, "the copy loses SR-001")
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


# --- D5: the whole-row comparison --------------------------------------------------


def test_a_cell_restored_after_the_act_still_mints(tmp_path):
    """Guard: the range moves two approved cells, the act copies the row, and
    one cell is then restored to its pre-range text. The net diff reports only
    the other cell, which equals its copy, but the restored cell differs from
    the copy. Catches a filter that compares only the net diff's cells.

    Implements: TC-403
    """
    root, before = _repo(tmp_path)
    _write_srs(root, requirement=AMENDED, acceptance=AC_AMENDED)
    _commit(root, "amend two cells of SR-001")
    _act(root, "SR-001")
    _write_srs(root, requirement=ORIGINAL, acceptance=AC_AMENDED)
    after = _commit(root, "restore the requirement after the act")
    (rec,) = acceptance_record.staged_spine_amendments(root, before, after)
    assert set(rec["approved"]) == {"AcceptanceCriteria"}, rec["approved"]
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


def test_a_routed_traced_cell_moved_after_the_act_still_mints(tmp_path):
    """Guard: the range amends SR-001 and the act copies it; then its
    `SN-Refs`, a traced cell the mint routes to adjudication, is re-pointed.
    Every approved cell still equals the copy, but the routed cell does not.
    Catches a filter whose whole-row comparison reads only the approved
    cells.

    Implements: TC-403
    """
    root, before, _act_sha = _settled(tmp_path)
    _write_srs(root, requirement=AMENDED, sn_refs="SN-002")
    after = _commit(root, "re-point SR-001 after its act")
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


def test_an_unrouted_traced_cell_moved_after_the_act_still_settles(tmp_path):
    """Guard, the contrast: as above, but the cell moved after the act is
    `Phase`, a traced cell the mint does not route. The routed half compares
    the routed cells only, so the row is still settled. Catches a filter that
    compares every traced cell.

    Implements: TC-403
    """
    root, before, _act_sha = _settled(tmp_path)
    _write_srs(root, requirement=AMENDED, phase=2)
    after = _commit(root, "re-phase SR-001 after its act")
    (rec,) = acceptance_record.staged_spine_amendments(root, before, after)
    assert set(rec["traced"]) == {"Phase"}, rec["traced"]
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    assert minted == [], minted


# --- the last writer: a later act's copy of the registry vouches for nothing -------

SR2_ORIGINAL = "The system shall subtract two numbers."
SR2_AMENDED = "The system shall subtract two integers."
LLR_ORIGINAL = "Adds with the + operator."
LLR_AMENDED = "Adds with the + operator, integers only."


def _sr002(requirement):
    return "\n" + _sr_row("SR-002", requirement, "sub(3, 1) == 2", "Approved")


def _llr001(detail):
    return (
        "[design.LLR-001]\n"
        'sr_refs = ["SR-001"]\n'
        'title = "Adder"\n'
        'module = "adder.py"\n'
        'code_symbol = "add"\n'
        'detail = "{}"\n'
        'test_refs = "(see TC-001)"\n'
        'status = "Approved"\n'
        "phase = 1\n"
    ).format(detail)


def _lane(root):
    """Cut the lane a squashed landing builds on, from trunk's HEAD."""
    _git(root, "checkout", "-q", "-b", "lane")


def _land(root, squashed, after):
    """The range's `after`: the lane tip itself, or the one commit `git merge
    --squash` lands on trunk, which holds every act the lane took."""
    if not squashed:
        return after
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "--squash", "lane")
    return _commit(root, "land the lane, squashed")


def _strip_copied(root):
    """Rewrite the ledger as a kit that predates `copied` wrote it: every entry
    a legacy entry, its copy set unknown."""
    path = root / ACTS_REL
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    path.write_bytes(
        "".join(ln for ln in lines if not ln.startswith("copied")).encode("utf-8")
    )


@pytest.mark.parametrize("squashed", [False, True], ids=["unsquashed", "squashed"])
def test_a_later_act_copying_the_registry_does_not_settle_a_row_it_did_not_reattest(
    tmp_path, squashed
):
    """Act A re-attests SR-001; SR-001's routed `SN-Refs` is then re-pointed
    and SR-002 amended; act B re-attests SR-002 alone, and its copy of the SR
    registry carries SR-001's re-point. SR-001 still mints, SR-002 settles.
    Over a squashed landing the one commit holds both acts, so the copy at
    `after` is act B's either way: only the ledger's record of what each act
    copied tells the two acts apart.

    Implements: TC-403
    """
    root, before = _repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    if squashed:
        _lane(root)
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_ORIGINAL))
    _commit(root, "amend SR-001")
    _act(root, "SR-001")
    _write_srs(root, requirement=AMENDED, sn_refs="SN-002", extra=_sr002(SR2_AMENDED))
    _commit(root, "re-point SR-001, amend SR-002")
    after = _land(root, squashed, _act(root, "SR-002"))
    walk = acceptance_record.staged_spine_amendments(root, before, after)
    assert sorted(rec["id"] for rec in walk) == ["SR-001", "SR-002"]
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


@pytest.mark.parametrize("squashed", [False, True], ids=["unsquashed", "squashed"])
def test_a_later_act_copying_another_registry_leaves_the_row_settled(
    tmp_path, squashed
):
    """Guard, the contrast: act B re-attests an LLR row and copies only the LLR
    registry, and SR-001 is untouched after act A. Both rows settle. Catches a
    filter that reads any later act as unsettling, whatever it copied.

    Implements: TC-403
    """
    root, before = _repo(tmp_path, llrs=_llr001(LLR_ORIGINAL))
    if squashed:
        _lane(root)
    _write_srs(root, requirement=AMENDED)
    _commit(root, "amend SR-001")
    _act(root, "SR-001")
    _write_llrs(root, _llr001(LLR_AMENDED))
    _commit(root, "amend LLR-001")
    after = _land(root, squashed, _act(root, "LLR-001"))
    copied = [
        a.get("copied")
        for a in SNAP.parse_acts((root / ACTS_REL).read_text(encoding="utf-8"))
    ]
    assert copied[-1] == [LLR_REL], copied
    walk = acceptance_record.staged_spine_amendments(root, before, after)
    assert sorted(rec["id"] for rec in walk) == ["LLR-001", "SR-001"]
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    assert minted == [], minted


def test_a_later_legacy_act_leaves_the_row_unsettled(tmp_path):
    """The contrast above over a ledger a kit before `copied` wrote: act B's
    copy set is unknown, so it may have written SR-001's registry, and SR-001's
    routed `SN-Refs` moved over the range (judged by act A, but a later writer
    could have absorbed a move after it), so SR-001 is not proven settled.
    Act B's own row is re-attested by the last act, so it still settles.

    Implements: TC-403
    """
    root, before = _repo(tmp_path, llrs=_llr001(LLR_ORIGINAL))
    _strip_copied(root)
    before = _commit(root, "the ledger as a kit before copied wrote it")
    _write_srs(root, requirement=AMENDED, sn_refs="SN-002")
    _commit(root, "amend and re-point SR-001")
    _act(root, "SR-001")
    _write_llrs(root, _llr001(LLR_AMENDED))
    _commit(root, "amend LLR-001")
    SNAP.copy_live(root, reattests=frozenset({"LLR-001"}))
    _strip_copied(root)
    after = _commit(root, "act: re-attest LLR-001, written as a legacy entry")
    assert all(
        "copied" not in a
        for a in SNAP.parse_acts((root / ACTS_REL).read_text(encoding="utf-8"))
    )
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


def test_a_later_writer_leaves_a_row_with_unmoved_routed_cells_settled(tmp_path):
    """Act A re-attests SR-001's amended requirement; act B then re-attests
    SR-002 and copies the same registry. A later act re-attesting another row
    cannot carry an unjudged approved-cell change (the snapshot refuses to copy
    approved drift no act blesses), and SR-001's routed `SN-Refs` are the same
    at the range's two ends: both rows settle. Catches a filter that reads
    every later writer of the registry as unsettling.

    Implements: TC-403
    """
    root, before = _repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_ORIGINAL))
    _commit(root, "amend SR-001")
    _act(root, "SR-001")
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_AMENDED))
    _commit(root, "amend SR-002")
    after = _act(root, "SR-002")
    copied = [
        a.get("copied")
        for a in SNAP.parse_acts((root / ACTS_REL).read_text(encoding="utf-8"))
    ]
    assert copied[-1] == [SR_REL], copied
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    assert minted == [], minted


def test_a_later_writer_leaves_a_row_with_moved_routed_cells_unsettled(tmp_path):
    """Guard, the contrast: as above, but SR-001's routed `SN-Refs` is
    re-pointed BEFORE act A, which judges it. The cells moved over the range
    and a later act copied the registry, so the ledger cannot tell a move act A
    judged from one act B absorbed: SR-001 mints. Catches a routed-cell arm
    that reads the copy rather than the range's two ends.

    Implements: TC-403
    """
    root, before = _repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    _write_srs(root, requirement=AMENDED, sn_refs="SN-002", extra=_sr002(SR2_ORIGINAL))
    _commit(root, "amend and re-point SR-001")
    _act(root, "SR-001")
    _write_srs(root, requirement=AMENDED, sn_refs="SN-002", extra=_sr002(SR2_AMENDED))
    _commit(root, "amend SR-002")
    after = _act(root, "SR-002")
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


def _restored_between_acts(tmp_path, squashed, later_act):
    """SR-001 is amended and its routed `SN-Refs` re-pointed, act A re-attests
    it, and `SN-Refs` is then restored to its pre-range value. With
    `later_act`, SR-002 is amended and act B re-attests it, copying the same
    registry. `(root, before, after)`."""
    root, before = _repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    if squashed:
        _lane(root)
    _write_srs(root, requirement=AMENDED, sn_refs="SN-002", extra=_sr002(SR2_ORIGINAL))
    _commit(root, "amend and re-point SR-001")
    _act(root, "SR-001")
    sr2 = SR2_AMENDED if later_act else SR2_ORIGINAL
    _write_srs(root, requirement=AMENDED, extra=_sr002(sr2))
    tip = _commit(root, "restore SR-001's SN-Refs after its act")
    if later_act:
        tip = _act(root, "SR-002")
    return root, before, _land(root, squashed, tip)


@pytest.mark.parametrize("squashed", [False, True], ids=["unsquashed", "squashed"])
def test_a_routed_cell_restored_between_two_acts_copying_the_registry_settles(
    tmp_path, squashed
):
    """Pins the arm's documented limit, not a guarantee: a routed traced cell
    moved before the re-attesting act and restored after it is re-anchored by
    a later act's copy of the registry, as any traced refresh is, so the row
    settles. The arm proves only that the routed traced cells are the same at
    the range's two ends, and here they are.

    Implements: TC-403
    """
    root, before, after = _restored_between_acts(tmp_path, squashed, True)
    walk = acceptance_record.staged_spine_amendments(root, before, after)
    assert sorted(rec["id"] for rec in walk) == ["SR-001", "SR-002"]
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    assert minted == [], minted


@pytest.mark.parametrize("squashed", [False, True], ids=["unsquashed", "squashed"])
def test_a_routed_cell_restored_after_the_act_with_no_later_copy_still_mints(
    tmp_path, squashed
):
    """Guard, the contrast: the same restore with no later act copying the
    registry. The copy at `after` is act A's own, which holds the re-pointed
    `SN-Refs`, so the restored row differs from it and mints. Catches an arm
    that settles on equality at the range's two ends without a later writer.

    Implements: TC-403
    """
    root, before, after = _restored_between_acts(tmp_path, squashed, False)
    minted, refusal = intake.intake_after_merge(root, before, after, {}, "")
    assert refusal is None, refusal
    (row,) = _amendment_rows(root, minted)
    assert row["adjudicates"] == ["SR-001"]


# --- D6: the two real landings that minted a redundant row --------------------------

# WI-926's landing (minted WI-952) and WI-956's (minted WI-959): every row each
# walk returns was re-attested in its range and equals its copy at `after`.
REAL_LANDINGS = (
    (
        "5245ac82cf9d2132f7c6c1940f9a1f3c49294ba3",
        "08bbb71b60b060e0ceed4fa8baaac924b2be42c6",
        {"SR-019", "SR-020", "LLR-019", "LLR-020", "LLR-140", "LLR-300"},
    ),
    (
        "be80354d9297eac08952a9d3a1efeab0d31b28a5",
        "ed84e25107cce3b18fb4977fd0afc7fe567f3bca",
        {"LLR-207", "TC-132", "TC-205"},
    ),
)


def _landings_unavailable():
    """A named reason the pinned landings cannot be read, or None: a shallow
    clone or a source export is an environment fact, not a defect."""

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(ROOT), *args], capture_output=True, encoding="utf-8"
        )

    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        return "no git work tree at the repo root (source export?)"
    for before, after, _rows in REAL_LANDINGS:
        for sha in (before, after):
            if git("cat-file", "-e", sha + "^{commit}").returncode != 0:
                shallow = git("rev-parse", "--is-shallow-repository").stdout.strip()
                depth = (
                    " (shallow clone - fetch full history)" if shallow == "true" else ""
                )
                return "landing commit {} is not in this checkout's history{}".format(
                    sha[:9], depth
                )
    return None


def test_the_two_real_redundant_landings_mint_nothing():
    """Read-only: `git show` against the kit's own object database, nothing
    written. `test_a_row_amended_again_after_its_act_still_mints` is the
    fixture amended after its act that still mints. The premise is the walk's
    records with an approved or routed traced change, the rows the redundant
    mint named: the walk also returns traced-only records (a moved `Evidence`
    or `CodeSymbol` cell), which are silent by ruling.

    Implements: TC-403
    """
    reason = _landings_unavailable()
    if reason:
        pytest.skip("the real landings are unavailable: " + reason)
    routed = set().union(*intake.ROUTED_TRACED_CELLS.values())
    for before, after, rows in REAL_LANDINGS:
        walk = acceptance_record.staged_spine_amendments(ROOT, before, after)
        judged = {
            rec["id"] for rec in walk if rec["approved"] or set(rec["traced"]) & routed
        }
        assert judged == rows
        assert intake._routed_amendments(ROOT, before, after) == ([], None)
        assert intake._amendment_drafts(ROOT, before, after) == ([], None)
