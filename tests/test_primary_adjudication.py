"""Real Git ownership and restart boundaries for branchless adjudication."""

import argparse
import subprocess
from pathlib import Path

import pytest

import agent_common as ac
import dispatch
import integrate
import primary_adjudication as primary


def git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


@pytest.fixture
def root(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Test")
    git(repo, "config", "user.email", "test@example.invalid")
    (repo / ".gitignore").write_text("out/\n")
    queued = repo / "docs/work/queued"
    queued.mkdir(parents=True)
    (queued / "WI-1-judge.md").write_text(
        '+++\nid = "WI-1"\ntitle = "Judge"\nworkstream = "process"\n'
        'buildtier = "medium"\nsafety_class = "adjudication"\n+++\n\n'
        "## Context\n\nJudge the clean close.\n"
    )
    (repo / "docs/requirements").mkdir()
    (repo / "docs/requirements/system-requirements.toml").write_text("# registry\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "initial")
    return repo


def commit(root):
    git(root, "add", "-A")
    git(root, "commit", "-qm", "judgment progress")


def test_selection_and_resume_never_claim_or_create_a_branch(root):
    branches = git(root, "branch", "--list")
    worktrees = git(root, "worktree", "list", "--porcelain")
    turn = primary.begin(root, "WI-1")
    assert (root / turn["spec"]).is_file()
    assert not (root / "docs/work/active").exists()
    assert git(root, "branch", "--list") == branches
    # HEAD advances for the selection record; the checkout population does not.
    assert (
        git(root, "worktree", "list", "--porcelain").count("worktree ")
        == worktrees.count("worktree ")
        == 1
    )
    assert primary.pending(root) == turn
    assert primary.validate(root, turn) is None


def test_only_judgment_sections_may_change_while_pending(root):
    turn = primary.begin(root, "WI-1")
    spec = root / turn["spec"]
    spec.write_text(
        spec.read_text()
        + "\n## Approval\n\n```toml\n## Payload comment, not a document heading\nversion = 1\n```\n\n## Dispositions\n\nNo successor.\n"
    )
    commit(root)
    assert primary.validate(root, turn) is None
    spec.write_text(
        spec.read_text().replace('title = "Judge"', 'title = "Different scope"')
    )
    commit(root)
    with pytest.raises(ValueError, match="outside Approval/Dispositions"):
        primary.validate(root, turn)


def test_registry_drift_and_selection_rewrite_are_not_resume_progress(root):
    turn = primary.begin(root, "WI-1")
    registry = root / "docs/requirements/system-requirements.toml"
    registry.write_text("# changed during judgment\n")
    commit(root)
    with pytest.raises(ValueError, match="registry_blobs changed"):
        primary.validate(root, turn)


def test_immutable_selection_cannot_be_rebound_to_new_scope(root):
    turn = primary.begin(root, "WI-1")
    path = root / primary.record_path(turn)
    path.write_text(path.read_text().replace("scope = []", 'scope = ["SR-999"]'))
    commit(root)
    changed = primary.pending(root)
    with pytest.raises(ValueError, match="selection was changed"):
        primary.validate(root, changed)


def test_pending_selection_excludes_new_turn_claim_and_direct_integration(root):
    turn = primary.begin(root, "WI-1")
    assert "pending" in integrate._claim_refusal(root, ["WI-2"], "wi-2")
    assert "pending" in integrate._slot(root)
    with pytest.raises(ValueError, match="pending"):
        primary.begin(root, "WI-1")
    assert primary.pending(root) == turn


def test_primary_engine_runs_in_process_and_human_hold_retains_selection(root):
    calls = []

    def session(args, *, primary_turn):
        calls.append((Path(args.root), args.wi, args.base, args.train))
        assert "pending" in integrate._slot(root)
        assert (root / primary_turn["spec"]).is_file()
        return ac.EXIT_NEEDS_HUMAN

    code = primary.run(root, argparse.Namespace(), session, wi="WI-1")
    assert code == ac.EXIT_NEEDS_HUMAN
    turn = primary.pending(root)
    assert calls == [(root, "WI-1", turn["base"], "main")]
    assert primary.validate(root, turn) is None


def test_pending_turn_precedes_pause_and_parked_lane_resume(root, monkeypatch):
    turn = primary.begin(root, "WI-1")
    seen = []
    monkeypatch.setattr(
        dispatch,
        "_admit_primary",
        lambda *a, **kw: (seen.append(kw["turn"]) or True, None),
    )
    monkeypatch.setattr(
        dispatch,
        "_parked_branches",
        lambda root: pytest.fail("parked lane admitted before pending judgment"),
    )
    result = dispatch._admit(
        root,
        [],
        argparse.Namespace(),
        None,
        "all",
        False,
        False,
        1,
        None,
        {},
        paused={"reason": "stop new claims"},
    )
    assert result == (True, None)
    assert seen == [turn]


def test_a_linked_checkout_cannot_select_a_primary_turn(root, tmp_path):
    linked = tmp_path / "linked"
    git(root, "worktree", "add", "-qb", "worker", str(linked))
    with pytest.raises(ValueError, match="designated primary"):
        primary.begin(linked, "WI-1")
    assert not (linked / primary.RECORDS).exists()
