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


def test_a_citing_row_whose_path_git_would_quote_is_still_judged(tmp_path):
    # core.quotePath quotes a non-ASCII path in plain listings; the sync lists
    # the diff and each tree NUL-delimited, so the row is found and judged at
    # the commit and at the merge slot.
    root = _repo(tmp_path / "repo")
    _git(root, "config", "core.quotePath", "true")
    _items(root, OI_5="pending")
    path = _spec(root, "WI-001", ["OI-5"], "- OI-5 is ruled.")
    path.rename(path.with_name("WI-001-ré.md"))
    _commit(root, "base")
    _git(root, "checkout", "-q", "-b", "wi-002")
    _items(root, OI_5="ruled")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert line.startswith("WI-001 cites OI-5")
    bad = _commit(root, "ruling, row untouched")
    _git(root, "checkout", "-q", "main")
    refusal = integrate._ruling_sync_refusal(root, "wi-002")
    assert refusal is not None and bad[:10] in refusal


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


# --- rework round 1 (Sol review 1, MAJOR 1, 2 and 4) --------------------------


def _shallow_ruling(tmp_path):
    """A ruling commit whose citing row's Done-when is untouched, at a shallow
    boundary: the commit object names its parent, but git hides the ancestry."""
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")
    sha = _commit(root, "rule OI-5 without the row")
    parent = _git(root, "rev-parse", sha + "^1")
    (root / ".git" / "shallow").write_text(sha + "\n", encoding="utf-8")
    return root, sha, parent


def test_a_shallow_boundary_is_judged_never_read_as_a_root_commit(tmp_path):
    # MAJOR 1: `rev^1` does not resolve at a shallow boundary, yet the commit
    # object carries a parent; reading that as "a root commit closes nothing"
    # skipped the rule. The parent is read off the commit object instead.
    root, sha, _parent = _shallow_ruling(tmp_path)
    assert _git(root, "rev-parse", "--is-shallow-repository") == "true"
    (line,) = ar.commit_ruling_sync_lines(root, sha)
    assert "WI-001 cites OI-5" in line


def test_a_parent_the_repository_cannot_read_is_refused_by_name(tmp_path):
    # ...and where the parent object is genuinely absent (a depth-one clone),
    # the commit is refused by name: never a skip, never a degraded pass.
    root, sha, parent = _shallow_ruling(tmp_path)
    loose = root / ".git" / "objects" / parent[:2] / parent[2:]
    loose.chmod(0o644)  # git writes objects read-only
    loose.unlink()
    (line,) = ar.commit_ruling_sync_lines(root, sha)
    assert parent[:10] in line and "cannot be read" in line and sha[:10] in line
    # Sol final review, MAJOR 1: so is a blob its tree lists but the store
    # cannot read — the parent's registry, or a parent citing spec — never
    # read as an absent registry or a skipped row.
    _unreadable_registry_blob_is_refused(tmp_path / "registry")
    _unreadable_citing_spec_blob_is_refused(tmp_path / "spec")


def test_the_csv_carrier_is_judged_like_the_toml_one(tmp_path):
    # MAJOR 2: the registry is read through whichever carrier each tree uses.
    root = _repo(tmp_path / "repo")
    csv = root / "docs/requirements/open-items.csv"
    csv.parent.mkdir(parents=True)
    csv.write_text("OI-ID,Title,Status\nOI-5,t,pending\n", encoding="utf-8")
    _spec(root, "WI-001", ["OI-5"], "- OI-5 is ruled.")
    _commit(root, "base")
    csv.write_text("OI-ID,Title,Status\nOI-5,t,ruled\n", encoding="utf-8")
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert "WI-001 cites OI-5" in line
    sha = _commit(root, "rule on the CSV carrier")
    (line,) = ar.commit_ruling_sync_lines(root, sha)
    assert "WI-001 cites OI-5" in line


def test_an_added_criterion_carrying_a_path_counts_as_an_update(tmp_path):
    # MAJOR 4: the raw Done-when section is compared (A1); the claim-time
    # evidence-stripping reading took the added path for completion evidence.
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")
    _spec(
        root,
        "WI-001",
        ["OI-5", "OI-6"],
        "- OI-5 and OI-6 are ruled. — Use scripts/export.py as the canonical "
        "export entry.",
    )
    _git(root, "add", "-A")
    assert ar.staged_ruling_sync_lines(root) == []


def test_removing_a_pending_items_row_takes_it_out_of_pending_too(tmp_path):
    # LLR-298: the trigger is an item leaving `pending`, and deleting its
    # pending row leaves it; each citing row's Done-when is owed the update.
    root = _base(tmp_path)
    _items(root, OI_6="pending")  # OI-5's pending row removed outright
    _git(root, "add", "-A")
    (line,) = ar.staged_ruling_sync_lines(root)
    assert line.startswith("WI-001 cites OI-5, which this commit takes out of pending")


def test_the_merge_ladder_consults_the_ruling_sync_rung(tmp_path, monkeypatch):
    # TC-313: merge admission itself refuses a lane's --no-verify ruling
    # commit. The cheaper rungs ahead of this one are passed so the ladder
    # reaches it on a minimal repository; the rung is the real one.
    root = _base(tmp_path)
    _git(root, "checkout", "-q", "-b", "wi-001")
    _items(root, OI_5="ruled", OI_6="pending")
    bad = _commit(root, "rule OI-5 without the row")
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
    ):
        monkeypatch.setattr(integrate, rung, lambda *a, **k: None)
    _outcomes, refusal = integrate._merge_refusal(root, "wi-001", ["WI-009"])
    assert refusal is not None and bad[:10] in refusal
    assert "WI-001 cites OI-5" in refusal


def test_the_pre_commit_hook_runs_the_ruling_sync_step(tmp_path):
    # TC-313: the staged check is in the pre-commit hook's failing set, and the
    # step the hook names refuses a staged ruling that leaves its citer stale.
    hook = (SCRIPTS.parent / "hooks" / "pre-commit").read_text(encoding="utf-8")
    line = next(
        ln for ln in hook.splitlines() if ln.startswith('"$PY"') and "--run-steps" in ln
    )
    assert "ruling-sync" in line.split("--run-steps", 1)[1].split()[0].split(",")
    root = _base(tmp_path)
    _items(root, OI_5="ruled", OI_6="pending")
    _git(root, "add", "-A")
    proc = run_py([SCRIPTS / "check.py", "--run-steps", "ruling-sync"], root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "WI-001" in proc.stdout + proc.stderr


# --- Sol final review, MAJOR 1: a listed path whose blob cannot be read --------


def _drop_blob(root, rev, path):
    """Delete the loose object of `rev:path`: the tree still lists the path,
    but its blob cannot be read (a partial clone offline, or a damaged store)."""
    sha = _git(root, "rev-parse", "{}:{}".format(rev, path))
    loose = root / ".git" / "objects" / sha[:2] / sha[2:]
    loose.chmod(0o644)  # git writes objects read-only
    loose.unlink()


def _unreadable_registry_blob_is_refused(tmp_path):
    # A1: a failed read is never an absent registry. Before this fix the
    # parent's unreadable registry read as "no registry", nothing was pending,
    # and the stale ruling passed both the staged and the committed checks.
    root = _base(tmp_path)
    base = _git(root, "rev-parse", "HEAD")
    _items(root, OI_5="ruled", OI_6="pending")
    _git(root, "add", "-A")
    _drop_blob(root, base, OI)
    (line,) = ar.staged_ruling_sync_lines(root)
    assert OI in line and "cannot be read" in line
    sha = _commit(root, "rule OI-5 without the row")
    (line,) = ar.commit_ruling_sync_lines(root, sha)
    assert OI in line and "cannot be read" in line


def _unreadable_citing_spec_blob_is_refused(tmp_path):
    # ...and an unreadable citing spec is never dropped from the citing set.
    root = _base(tmp_path)
    base = _git(root, "rev-parse", "HEAD")
    spec = "docs/work/queued/WI-001-row.md"
    _items(root, OI_5="ruled", OI_6="pending")
    path = root / spec
    path.write_text(
        path.read_text(encoding="utf-8").replace('title = "row"', 'title = "row2"'),
        encoding="utf-8",
    )  # a new blob for the row, its Done-when untouched
    _git(root, "add", "-A")
    _drop_blob(root, base, spec)
    (line,) = ar.staged_ruling_sync_lines(root)
    assert spec in line and "cannot be read" in line
