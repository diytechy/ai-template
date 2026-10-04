"""A ruling updates the rows that cite it, in the same commit (WI-790; OI-102 Q3).

One function over two trees: a commit that takes an open item out of `pending`
must, in the same diff, update the Done-when of each work item OPEN in its
parent tree whose `needs` cites the item, or close or remove that row. The
pre-commit hook asks it of HEAD and the staged tree; the merge slot asks it of
every lane commit against its first parent, so a `--no-verify` commit is still
refused before it reaches trunk.
"""

import os
import subprocess

from conftest import SCRIPTS, load_script, pin_autocrlf, run_py

ar = load_script("acceptance_record")
integrate = load_script("integrate")
ct = load_script("check_trajectory")

OI = "docs/requirements/open-items.toml"


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        env=env,
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


def _items(root, **states):
    path = root / OI
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            '[open_item.{}]\ntitle = "t"\nstatus = "{}"\n\n'.format(
                o.replace("_", "-"), s
            )
            for o, s in states.items()
        ),
        encoding="utf-8",
    )


def _spec(root, wid, needs, done_when=None, where="queued"):
    body = "" if done_when is None else "\n## Done-when\n\n" + done_when + "\n"
    for old in (root / "docs/work").rglob("{}-*.md".format(wid)):
        old.unlink()
    path = root / "docs/work" / where / "{}-row.md".format(wid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '+++\nid = "{}"\ntitle = "row"\nneeds = [{}]\nsafety_class = "ordinary"\n'
        'specref = "{}#OI-5"\n+++\n{}'.format(
            wid, ", ".join('"{}"'.format(n) for n in needs), OI, body
        ),
        encoding="utf-8",
    )
    return path


def _commit(root, msg, env=None):
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "--no-verify", "-m", msg, env=env)
    return _git(root, "rev-parse", "HEAD")


def _base(tmp_path):
    """A row citing two pending items, with a Done-when, committed."""
    root = _repo(tmp_path / "repo")
    _items(root, OI_5="pending", OI_6="pending")
    _spec(root, "WI-001", ["OI-5", "OI-6"], "- OI-5 and OI-6 are ruled.")
    _commit(root, "base")
    return root


def test_a_ruling_with_the_citing_rows_done_when_untouched_is_refused(tmp_path):
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")  # one of the two items is ruled
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert line.startswith("WI-001 cites OI-5, which this commit takes out of pending")
    assert "Done-when is unchanged" in line
    # The pre-commit hook's step names the row and the item and refuses.
    proc = run_py([SCRIPTS / "check.py", "--ruling-sync"], root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FAIL  ruling-sync" in proc.stdout and "WI-001" in proc.stdout
    assert "OI-5" in proc.stdout


def test_the_same_ruling_with_the_done_when_updated_is_accepted(tmp_path):
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")
    _spec(
        root,
        "WI-001",
        ["OI-5", "OI-6"],
        "- OI-5 ruled 2026-10-04: the export flag is dropped.\n- OI-6 is ruled.",
    )
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    proc = run_py([SCRIPTS / "check.py", "--ruling-sync"], root)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_removing_the_token_in_the_ruling_commit_does_not_discharge_it(tmp_path):
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")
    _spec(root, "WI-001", ["OI-6"], "- OI-5 and OI-6 are ruled.")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert "WI-001 cites OI-5" in line  # the citing set is the parent tree's


def test_a_row_closed_in_the_ruling_commit_is_accepted(tmp_path):
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")
    path = root / "docs/work/queued/WI-001-row.md"
    closed = root / "docs/archive/work/cancelled"
    closed.mkdir(parents=True)
    path.rename(closed / path.name)
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    # ...and so is a row removed outright, and a row emptied of its Done-when
    # while still open is not.
    (closed / path.name).unlink()
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    _git(root, "reset", "-q", "--hard")
    _items(root, OI_5="ruled", OI_6="pending")
    _spec(root, "WI-001", ["OI-5", "OI-6"])
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert "keeps no Done-when" in line


def test_a_first_commit_has_nothing_to_close(tmp_path):
    root = _repo(tmp_path / "repo")
    _items(root, OI_5="ruled")
    _spec(root, "WI-001", ["OI-5"], "- done.")
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []
    sha = _commit(root, "first")
    assert ar.commit_ruling_sync_lines(root, sha) == []


def test_a_no_verify_lane_commit_is_refused_at_the_merge_slot(tmp_path):
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-001")
    _items(root, OI_5="ruled", OI_6="pending")
    bad = _commit(root, "rule OI-5 without the row")  # --no-verify
    _git(root, "checkout", "-q", "main")
    refusal = integrate._ruling_sync_refusal(root, "wi-001")
    assert refusal is not None and bad[:10] in refusal
    assert "WI-001 cites OI-5" in refusal and "nothing was merged" in refusal
    # Fixed in a LATER commit is still refused: each commit is judged against
    # its own parent, not the lane's net diff.
    _git(root, "checkout", "-q", "wi-001")
    _spec(root, "WI-001", ["OI-5", "OI-6"], "- OI-5 ruled: dropped.\n- OI-6.")
    _commit(root, "update the row afterwards")
    _git(root, "checkout", "-q", "main")
    assert integrate._ruling_sync_refusal(root, "wi-001") is not None
    # A lane whose ruling commit carries the update lands.
    _git(root, "checkout", "-q", "main")
    _git(root, "checkout", "-q", "-b", "wi-002")
    _items(root, OI_5="ruled", OI_6="pending")
    _spec(root, "WI-001", ["OI-5", "OI-6"], "- OI-5 ruled: dropped.\n- OI-6.")
    _commit(root, "rule OI-5 with the row")
    _git(root, "checkout", "-q", "main")
    assert integrate._ruling_sync_refusal(root, "wi-002") is None


def _dated(when):
    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "{} +0000".format(when)
    return env


def test_a_registry_specref_is_clocked_per_cited_item(tmp_path):
    # WI-790: backlog staleness reads a placeholder's registry specref per
    # cited item, so a NEW unrelated item filed later warns no placeholder,
    # while an edit to the item it cites does.
    root = _repo(tmp_path / "repo")
    _items(root, OI_5="pending")
    _spec(root, "WI-001", ["OI-5"])
    _commit(root, "placeholder", env=_dated(1_700_000_000))
    path = root / OI
    path.write_text(
        path.read_text(encoding="utf-8")
        + '[open_item.OI-6]\ntitle = "t"\nstatus = "pending"\n',
        encoding="utf-8",
    )
    _commit(root, "an unrelated item", env=_dated(1_700_001_000))
    wis = ct.load_wis(ct.read_registry_rows(root / ct.WI_CSV))[0]
    assert ct.backlog_staleness_findings(root, wis) == []
    path.write_text(
        path.read_text(encoding="utf-8").replace('title = "t"', 'title = "t2"', 1),
        encoding="utf-8",
    )
    _commit(root, "edit OI-5", env=_dated(1_700_002_000))
    (finding,) = ct.backlog_staleness_findings(root, wis)
    assert finding.startswith("WI-001: cites OI-5 amended after")
