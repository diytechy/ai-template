"""Spine text before the act, enforced on every lane commit (WI-806; OI-101 Q2,
amended for landings by the owner's README Q-8 answer, 2026-10-04).

One function over two trees: a commit that writes under
`docs/archive/last_approved/` may, against its parent, change no spine cell
except `Status` and add or remove no row. The text is committed first and the
act (the flips, the snapshot, the ledger and the views) second. The pre-commit
hook asks it of the staged tree; the merge slot asks it of every lane commit,
so a `--no-verify` commit is still refused. A merge, a lane's refresh merge
included, is judged by what NEITHER parent carried, and a squash landing is
admitted only when the squashed lane tip contains HEAD, the staged spine and
record are the tip's own, and every commit it squashes passes.
"""

import subprocess

from conftest import SCRIPTS, load_script, pin_autocrlf, run_py

ar = load_script("acceptance_record")
integrate = load_script("integrate")
snap = load_script("baseline_snapshot")

SR = "docs/requirements/system-requirements.csv"
COPY = "docs/archive/last_approved/" + SR
HEADER = "SR-ID,Title,Requirement,Status\n"


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, encoding="utf-8"
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip()


def _repo(root):
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q", "-b", "main")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    _git(root, "config", "commit.gpgsign", "false")
    return root


def _rows(root, *rows):
    """The live SR registry: `(id, title, status)` per row."""
    path = root / SR
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        HEADER + "".join("{},{},the text,{}\n".format(*r) for r in rows),
        encoding="utf-8",
    )


def _act(root):
    """The approval act's copy: the live registry, byte for byte."""
    path = root / COPY
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((root / SR).read_bytes())


def _commit(root, msg):
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "--no-verify", "-m", msg)
    return _git(root, "rev-parse", "HEAD")


def _base(tmp_path):
    """SR-001 approved and recorded; SR-002 drafted and recorded."""
    root = _repo(tmp_path / "repo")
    (root / "README.md").write_text("r\n", encoding="utf-8")
    _commit(root, "first")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two", "Drafted"))
    _act(root)
    _commit(root, "the first signing")
    return root


def _squashed(root):
    """The commits a squash in progress folds in, newest first, as the hook
    step reads them off git's own `SQUASH_MSG`."""
    text = (root / ".git" / "SQUASH_MSG").read_text(encoding="utf-8")
    return [ln[7:] for ln in text.splitlines() if ln.startswith("commit ")]


def _step(root):
    return run_py([SCRIPTS / "check.py", "--run-steps", "text-then-act"], root)


def test_a_mixed_commit_is_refused_at_pre_commit(tmp_path):
    root = _base(tmp_path)
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _git(root, "add", "-A")
    (line,) = ar.staged_text_then_act_lines(root)
    assert "SR-002" in line and "Title" in line and "Status" not in line
    proc = _step(root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    out = proc.stdout + proc.stderr
    assert "FAIL  text-then-act" in out and "SR-002" in out
    assert "amend-plus-flip" not in out.lower()


def test_the_two_commit_form_is_accepted(tmp_path):
    root = _base(tmp_path)
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Drafted"))
    _git(root, "add", "-A")
    assert ar.staged_text_then_act_lines(root) == []  # text alone, no act
    _commit(root, "the text")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _git(root, "add", "-A")
    assert ar.staged_text_then_act_lines(root) == []  # the act: flips and copy
    proc = _step(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_row_added_or_removed_beside_the_act_is_refused(tmp_path):
    root = _base(tmp_path)
    _rows(
        root,
        ("SR-001", "One", "Approved"),
        ("SR-002", "Two", "Approved"),
        ("SR-003", "Three", "Approved"),
    )
    _act(root)
    _git(root, "add", "-A")
    (line,) = ar.staged_text_then_act_lines(root)
    assert "SR-003" in line and "added" in line
    _git(root, "reset", "-q", "--hard")
    _rows(root, ("SR-001", "One", "Approved"))
    _act(root)
    _git(root, "add", "-A")
    (line,) = ar.staged_text_then_act_lines(root)
    assert "SR-002" in line and "removed" in line


def test_a_traced_cell_beside_the_act_is_text_too(tmp_path):
    # "No spine cell except Status": a re-pointed traced cell is committed
    # before the act like any other text.
    root = _base(tmp_path)
    (root / SR).write_text(
        "SR-ID,Title,Requirement,Status,SN-Refs\n"
        "SR-001,One,the text,Approved,SN-001\n"
        "SR-002,Two,the text,Drafted,\n",
        encoding="utf-8",
    )
    _act(root)
    _git(root, "add", "-A")
    (line,) = ar.staged_text_then_act_lines(root)
    assert "SR-001" in line and "SN-Refs" in line


def test_a_commit_that_writes_no_record_is_never_judged(tmp_path):
    root = _base(tmp_path)
    _rows(root, ("SR-001", "One amended", "Approved"), ("SR-009", "New", "Drafted"))
    _git(root, "add", "-A")
    assert ar.staged_text_then_act_lines(root) == []


def test_a_no_verify_lane_commit_is_refused_at_the_landing(tmp_path):
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-001")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    bad = _commit(root, "text and act together")  # --no-verify
    _git(root, "checkout", "-q", "main")
    refusal = integrate._text_then_act_refusal(root, "wi-001")
    assert refusal is not None and bad[:10] in refusal
    assert "SR-002" in refusal and "nothing was merged" in refusal
    assert "amend-plus-flip" not in refusal.lower()
    # The two-commit lane lands.
    _git(root, "checkout", "-q", "-b", "wi-002")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Drafted"))
    _commit(root, "the text")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _commit(root, "the act")
    _git(root, "checkout", "-q", "main")
    assert integrate._text_then_act_refusal(root, "wi-002") is None


def test_the_merge_ladder_consults_the_text_then_act_rung(tmp_path, monkeypatch):
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-001")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    bad = _commit(root, "text and act together")
    _git(root, "checkout", "-q", "main")
    monkeypatch.setattr(
        integrate, "branch_outcomes", lambda r, b: ({"WI-009": "merged"}, [])
    )
    for rung in (
        "_close_record_refusal",
        "_minted_id_refusal",
        "_approval_act_refusal",
        "_held_status_refusal",
        "_loop_trailer_refusal",
        "_ruling_sync_refusal",
    ):
        monkeypatch.setattr(integrate, rung, lambda *a, **k: None)
    _outcomes, refusal = integrate._merge_refusal(root, "wi-001", ["WI-009"])
    assert refusal is not None and bad[:10] in refusal and "SR-002" in refusal


def test_a_refresh_merge_is_judged_by_what_neither_side_carried(tmp_path):
    # Trunk took its text and its act in two commits; a lane that merges trunk
    # in carries both in one first-parent diff, and that is not the lane's own.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-001")
    (root / "lane.txt").write_text("lane\n", encoding="utf-8")
    _commit(root, "lane work")
    _git(root, "checkout", "-q", "main")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Drafted"))
    _commit(root, "trunk text")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _commit(root, "trunk act")
    _git(root, "checkout", "-q", "wi-001")
    _git(root, "merge", "-q", "--no-ff", "--no-edit", "main")
    merge = _git(root, "rev-parse", "HEAD")
    assert ar.commit_text_then_act_lines(root, merge) == []
    _git(root, "checkout", "-q", "main")
    assert integrate._text_then_act_refusal(root, "wi-001") is None
    # A merge that writes text AND the record of its own is still refused. A
    # new trunk commit gives the lane something to merge, so this is a real
    # merge in progress (MERGE_HEAD set), not a plain staged commit.
    (root / "trunk.txt").write_text("trunk\n", encoding="utf-8")
    _commit(root, "trunk moves on")
    _git(root, "checkout", "-q", "wi-001")
    _git(root, "merge", "-q", "--no-ff", "--no-commit", "-s", "ours", "main")
    assert _git(root, "rev-parse", "-q", "--verify", "MERGE_HEAD")
    _rows(root, ("SR-001", "One evil", "Approved"), ("SR-002", "Two", "Drafted"))
    _act(root)
    _git(root, "add", "-A")
    (line,) = ar.staged_text_then_act_lines(root)
    assert "SR-001" in line


def test_a_squash_landing_is_admitted_only_when_its_lane_commits_pass(tmp_path):
    # The landing's own squash carries text and act together and is exempt
    # because the rule held on every commit it squashes - which the hook
    # checks rather than assumes, since a hand landing never meets the slot.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-002")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Drafted"))
    _commit(root, "the text")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _commit(root, "the act")
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "-q", "--squash", "wi-002")
    assert ar.staged_text_then_act_lines(root) != []  # judged as a plain commit
    assert ar.staged_text_then_act_lines(root, _squashed(root)) == []
    proc = _step(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _git(root, "commit", "-q", "--no-verify", "-m", "WI-002: land")
    # A lane holding a --no-verify mixed commit cannot be squashed past the hook.
    _git(root, "checkout", "-q", "-b", "wi-003")
    _rows(root, ("SR-001", "One amended", "Approved"), ("SR-002", "Two", "Approved"))
    _act(root)
    bad = _commit(root, "text and act together")
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "-q", "--squash", "wi-003")
    lines = ar.staged_text_then_act_lines(root, _squashed(root))
    assert lines and bad[:10] in lines[0] and "SR-001" in lines[0]
    proc = _step(root)
    assert proc.returncode == 1 and bad[:10] in proc.stdout, proc.stdout + proc.stderr


def test_a_first_commit_has_nothing_before_it(tmp_path):
    root = _repo(tmp_path / "repo")
    _rows(root, ("SR-001", "One", "Approved"))
    _act(root)
    _git(root, "add", "-A")
    assert ar.staged_text_then_act_lines(root) == []
    sha = _commit(root, "first")
    assert ar.commit_text_then_act_lines(root, sha) == []


def test_the_pre_commit_hook_runs_the_text_then_act_step():
    hook = (SCRIPTS.parent / "hooks" / "pre-commit").read_text(encoding="utf-8")
    line = next(
        ln for ln in hook.splitlines() if ln.startswith('"$PY"') and "--run-steps" in ln
    )
    assert "text-then-act" in line.split("--run-steps", 1)[1].split()[0].split(",")


def test_no_refusal_text_offers_amend_plus_flip(tmp_path):
    blocked = [(SR, {"SR-001": {"Title": ("a", "b")}})]
    for text in (
        snap._refusal_text(blocked, {SR}),
        snap._refusal_text(blocked, set()),
        ar.TEXT_THEN_ACT_REMEDY,
    ):
        assert "amend-plus-flip" not in text.lower()
        assert "same tree" not in text and "same commit" not in text
    # The amend-without-flip warn names the two commits, not "in this commit".
    root = _base(tmp_path)
    _rows(root, ("SR-001", "One amended", "Approved"), ("SR-002", "Two", "Drafted"))
    _git(root, "add", "-A")
    (warn,) = ar.staged_spine_findings(root)
    assert "SR-001" in warn and "in this commit" not in warn
    assert "intake.py snapshot --reattests SR-001" in warn


def test_a_commit_whose_parent_cannot_be_read_is_refused_by_name(tmp_path):
    # A shallow clone holds the commit but not its parent: an unread parent is
    # never read as a root (which would pass), it is named.
    root = _base(tmp_path)
    parent = _git(root, "rev-parse", "HEAD~1")
    clone = tmp_path / "shallow"
    _git(tmp_path, "clone", "-q", "--depth", "1", root.as_uri(), str(clone))
    sha = _git(clone, "rev-parse", "HEAD")
    (line,) = ar.commit_text_then_act_lines(clone, sha)
    assert parent[:10] in line and "cannot be read" in line


def test_a_diff_git_cannot_read_is_reported_not_skipped(tmp_path):
    root = _base(tmp_path)
    (line,) = ar.text_then_act_lines(root, ["0" * 40])
    assert "0" * 40 in line and "unknown" in line


def test_a_row_only_one_parent_carried_is_judged_by_its_cell_values(tmp_path):
    # Sol REVIEW-A BLOCKER: a row on the second parent alone reads "added"
    # against the first and "Title" against the second; intersecting those
    # labels hid a Title the merge itself wrote beside the record.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-003")
    _rows(
        root,
        ("SR-001", "One", "Approved"),
        ("SR-002", "Two", "Drafted"),
        ("SR-003", "Three", "Drafted"),
    )
    _commit(root, "lane adds SR-003")
    _git(root, "checkout", "-q", "main")
    (root / "trunk.txt").write_text("trunk\n", encoding="utf-8")
    _commit(root, "trunk moves on")
    _git(root, "merge", "-q", "--no-ff", "--no-commit", "wi-003")
    _rows(
        root,
        ("SR-001", "One", "Approved"),
        ("SR-002", "Two", "Drafted"),
        ("SR-003", "Three edited", "Approved"),
    )
    _act(root)
    _git(root, "add", "-A")
    (line,) = ar.staged_text_then_act_lines(root)
    assert "SR-003: Title" in line
    _git(root, "commit", "-q", "--no-verify", "-m", "merge with its own text")
    merge = _git(root, "rev-parse", "HEAD")
    (line,) = ar.commit_text_then_act_lines(root, merge)
    assert "SR-003: Title" in line
    # The same merge carrying the lane's row unchanged, with only the flip and
    # the copy, is the lane's text and an act: it passes.
    _git(root, "reset", "-q", "--hard", "HEAD~1")
    _git(root, "merge", "-q", "--no-ff", "--no-commit", "wi-003")
    _rows(
        root,
        ("SR-001", "One", "Approved"),
        ("SR-002", "Two", "Drafted"),
        ("SR-003", "Three", "Approved"),
    )
    _act(root)
    _git(root, "add", "-A")
    assert ar.staged_text_then_act_lines(root) == []


def test_a_stale_squash_message_exempts_no_other_commit(tmp_path):
    # Sol REVIEW-A MAJOR: `git restore` abandons a squash but leaves git's
    # SQUASH_MSG behind. The exemption holds only while the squashed tip
    # contains HEAD and the staged spine and record are the tip's own, so a
    # different direct commit made afterwards is judged like any other.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-002")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Drafted"))
    _commit(root, "the text")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _commit(root, "the act")
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "-q", "--squash", "wi-002")
    _git(root, "restore", "--staged", ".")
    _git(root, "restore", ".")
    _git(root, "clean", "-q", "-fd")
    assert (root / ".git" / "SQUASH_MSG").is_file()  # left behind
    # RESIDUE (D-004): the lane tip's own spine and record, retyped by hand,
    # ARE its squash in content: every byte was committed and judged there.
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _git(root, "add", "-A")
    assert ar.staged_text_then_act_lines(root, _squashed(root)) == []
    # Any other spine text beside that record is not the tip's, so the stale
    # message exempts nothing and the commit is judged plainly.
    llr = root / "docs/requirements/low-level-requirements.csv"
    llr.write_text(
        "LLR-ID,Title,Detail,Status\nLLR-001,New,the text,Drafted\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    line, hint = ar.staged_text_then_act_lines(root, _squashed(root))
    assert "LLR-001: added" in line and hint == ar.SQUASH_REBASE_HINT
    proc = _step(root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    # git deletes SQUASH_MSG at the next commit, so the residue's window is
    # that one commit.
    _git(root, "commit", "-q", "--no-verify", "-m", "a direct commit")
    assert not (root / ".git" / "SQUASH_MSG").exists()


def _requirement(root, lines):
    """SR-001, approved, its Requirement one multiline cell of `lines`."""
    path = root / SR
    path.parent.mkdir(parents=True, exist_ok=True)
    cell = "\n".join(lines)
    path.write_text(
        HEADER + 'SR-001,One,"{}",Approved\n'.format(cell), encoding="utf-8"
    )


def _text_then_reattest(root, lines, what):
    """The two-commit form: the amended cell, then its re-attesting copy."""
    _requirement(root, lines)
    _commit(root, what + " text")
    _act(root)
    return _commit(root, what + " act")


def _combined_cell_lanes(tmp_path):
    """Trunk and lane wi-004 each amend a different line of SR-001's one
    multiline Requirement cell, each in the two-commit form; git merges the
    two into a third value no judged commit carried."""
    root = _repo(tmp_path / "repo")
    lines = ["line {}".format(n) for n in range(1, 10)]
    _requirement(root, lines)
    _act(root)
    _commit(root, "the first signing")
    _git(root, "checkout", "-q", "-b", "wi-004")
    _text_then_reattest(root, ["lane"] + lines[1:], "lane")
    _git(root, "checkout", "-q", "main")
    _text_then_reattest(root, lines[:-1] + ["trunk"], "trunk")
    return root


def test_a_squash_combining_two_judged_cells_into_a_third_is_refused(tmp_path):
    # Sol REVIEW-A r2 BLOCKER: git cleanly squashes the lane into trunk as a
    # Requirement value holding both edits, live and recorded alike, which no
    # judged commit carried. A lane not containing HEAD gets no exemption.
    root = _combined_cell_lanes(tmp_path)
    _git(root, "merge", "-q", "--squash", "wi-004")
    staged = _git(root, "show", ":" + SR)
    assert "lane" in staged and "trunk" in staged  # the third value
    lines = ar.staged_text_then_act_lines(root, _squashed(root))
    assert lines and "SR-001: Requirement" in lines[0]
    assert "rebase" in lines[-1]
    proc = _step(root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "SR-001" in proc.stdout and "rebase" in proc.stdout


def test_a_squash_of_a_lane_not_containing_head_is_refused_with_the_rebase_hint(
    tmp_path,
):
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-002")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Drafted"))
    _commit(root, "the text")
    _rows(root, ("SR-001", "One", "Approved"), ("SR-002", "Two amended", "Approved"))
    _act(root)
    _commit(root, "the act")
    _git(root, "checkout", "-q", "main")
    (root / "trunk.txt").write_text("trunk\n", encoding="utf-8")
    _commit(root, "trunk moves on")
    _git(root, "merge", "-q", "--squash", "wi-002")
    lines = ar.staged_text_then_act_lines(root, _squashed(root))
    assert lines and "SR-002" in lines[0]
    assert "rebase the lane onto trunk" in lines[-1]
    proc = _step(root)
    assert proc.returncode == 1 and "rebase" in proc.stdout, proc.stdout


def test_a_refreshed_lanes_squash_is_admitted(tmp_path):
    # Rebased onto trunk, the lane's own commits carry the combined cell, each
    # judged against its parent; its squash is exactly its tip for the spine
    # and the record, so the landing is exempt.
    root = _combined_cell_lanes(tmp_path)
    _git(root, "checkout", "-q", "wi-004")
    _git(root, "rebase", "-q", "main")
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "-q", "--squash", "wi-004")
    assert ar.staged_text_then_act_lines(root) != []  # judged as a plain commit
    assert ar.staged_text_then_act_lines(root, _squashed(root)) == []
    proc = _step(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
