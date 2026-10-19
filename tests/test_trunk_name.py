"""WI-925: the trunk is one declared name.

`agent_common.trunk_name` reads `docs/process.toml [policies] trunk` and
nothing else: no worktree list, no current branch, no worker base. An absent,
non-string, empty or unknown name is refused, naming the line to add. These
are the reader's in-process pins; each runs git only to build its repository.
"""

import subprocess

import pytest
from conftest import env_gate_skipif, load_script, trunk_repo

pytestmark = env_gate_skipif("git")

ac = load_script("agent_common")


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, encoding="utf-8"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _two_branch_repo(tmp_path):
    """A repository declaring `main` its trunk, its primary checkout switched
    to a second branch, `side`."""
    root = trunk_repo(tmp_path / "repo")
    _git(root, "checkout", "-q", "-b", "side")
    return root


def test_a_repository_with_the_key_reads_it_and_one_without_refuses(tmp_path):
    root = _two_branch_repo(tmp_path)
    assert ac.trunk_name(root) == "main"
    (root / "docs" / "process.toml").unlink()
    with pytest.raises(ac.TrunkUndeclared, match=r"\[policies\] trunk"):
        ac.trunk_name(root)


def test_the_reader_reads_no_worktree_list_and_no_current_branch(tmp_path, monkeypatch):
    root = _two_branch_repo(tmp_path)
    real = ac.git

    def guarded(where, *args):
        if args[:2] == ("worktree", "list") or args == ("branch", "--show-current"):
            raise AssertionError("the trunk reader asked git {}".format(args))
        return real(where, *args)

    monkeypatch.setattr(ac, "git", guarded)
    assert ac.trunk_name(root) == "main"


_SHAPES = {
    "absent": None,
    "not a string": "[policies]\ntrunk = 1\n",
    "empty": '[policies]\ntrunk = ""\n',
    "no such branch": '[policies]\ntrunk = "nosuch"\n',
    "unparseable": "[policies\ntrunk = 'main'\n",
}


@pytest.mark.parametrize("shape", sorted(_SHAPES))
def test_each_undeclared_shape_is_refused_naming_the_key(tmp_path, shape):
    root = _two_branch_repo(tmp_path)
    path = root / "docs" / "process.toml"
    if _SHAPES[shape] is None:
        path.unlink()
    else:
        path.write_text(_SHAPES[shape], encoding="utf-8", newline="\n")
    with pytest.raises(ac.TrunkUndeclared) as caught:
        ac.trunk_name(root)
    text = str(caught.value)
    assert "docs/process.toml [policies] trunk" in text, text
    assert 'trunk = "<your integration branch>"' in text, text
