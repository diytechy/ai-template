"""Git identity helpers used by the approval-record ownership boundary."""

import subprocess

from kitlib import git as kitgit


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _repo(tmp_path):
    root = tmp_path / "primary"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    (root / "seed").write_text("seed\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "seed")
    return root


def test_worktree_identity_is_git_identity_not_a_path_spelling(tmp_path):
    root = _repo(tmp_path)
    (root / "docs").mkdir()
    linked = tmp_path / "linked"
    _git(root, "worktree", "add", "-q", "-b", "linked", str(linked), "HEAD")

    assert kitgit.is_linked_worktree(root) is False
    assert kitgit.is_linked_worktree(root / "docs") is False
    assert kitgit.is_linked_worktree(linked) is True


def test_worktree_identity_does_not_misclassify_an_unrelated_nested_repo(tmp_path):
    root = _repo(tmp_path)
    nested = root / "vendor" / "unrelated"
    nested.mkdir(parents=True)
    _git(nested, "init", "-q")

    assert kitgit.is_linked_worktree(nested) is False


def test_worktree_identity_fails_open_off_git(tmp_path):
    assert kitgit.worktree_records(tmp_path) == []
    assert kitgit.primary_worktree_root(tmp_path) is None
    assert kitgit.is_linked_worktree(tmp_path) is False
