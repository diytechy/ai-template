"""Whether a checkout's commit hooks are on (`kitlib.commit_hooks`), and the
fixture helper that turns them on (`conftest.hooks_on`).

Real git in `tmp_path`, in process. "Not on" is deny by default, so each
not-on case asserts the refusal names its cause and the fix that repairs that
cause: the hooks path's fix names the setup step (setup, or dev-setup where a
repository carries no setup script) and the git command both run; a missing
hook is restored; a hook that lost its mode bit is made executable.
"""

import ast
import os
import subprocess

import pytest
from conftest import SCRIPTS, hooks_on, skip_without_env_gates

from kitlib import commit_hooks
from kitlib import git as kitgit

SETUP = "scripts/setup.sh"
ACTIVATE = (SETUP, "dev-setup", "git config core.hooksPath .githooks")
RESTORE = ("git checkout -- .githooks", "re-run bootstrap")
MAKE_EXECUTABLE = ("chmod +x", "git update-index --chmod=+x")


def git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def make_repo(root):
    skip_without_env_gates("git")
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "t@example.com")
    git(root, "config", "user.name", "T")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "config", "core.autocrlf", "false")
    return root


def write_hooks(root, names=("pre-commit", "commit-msg"), mode=0o755):
    hooks = root / ".githooks"
    hooks.mkdir(exist_ok=True)
    for name in names:
        hook = hooks / name
        with hook.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write("#!/bin/sh\nexit 0\n")
        hook.chmod(mode)
    return hooks


def commit_all(root, message="seed"):
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", message)


def assert_refused(text, cause, fix=ACTIVATE):
    assert text is not None, "expected a refusal"
    assert "not on" in text, text
    assert cause in text, text
    for step in fix:
        assert step in text, (step, text)


# --- not on ------------------------------------------------------------------


def test_unset_hooks_path_is_not_on(tmp_path):
    root = make_repo(tmp_path / "r")
    write_hooks(root)
    assert_refused(commit_hooks.hooks_refusal(root), "unset or names .git/hooks")


def test_git_hooks_dir_is_not_on(tmp_path):
    root = make_repo(tmp_path / "r")
    write_hooks(root)
    git(root, "config", "core.hooksPath", ".git/hooks")
    assert_refused(commit_hooks.hooks_refusal(root), "unset or names .git/hooks")


def test_another_directory_is_not_on(tmp_path):
    root = make_repo(tmp_path / "r")
    other = tmp_path / "manager-hooks"
    other.mkdir()
    write_hooks(root)
    git(root, "config", "core.hooksPath", str(other))
    assert_refused(commit_hooks.hooks_refusal(root), "manager-hooks")


def test_an_empty_hooks_path_is_not_on(tmp_path):
    root = make_repo(tmp_path / "r")
    write_hooks(root)
    git(root, "config", "core.hooksPath", "")
    # git 2.49 refuses the absolute-path form of an empty hooks path outright;
    # older gits answer the top itself. Either way it reads "not on".
    text = commit_hooks.hooks_refusal(root)
    cause = "git could not say" if "git could not say" in (text or "") else "names"
    assert_refused(text, cause)


@pytest.mark.parametrize("missing", ["pre-commit", "commit-msg"])
def test_a_missing_hook_is_not_on(tmp_path, missing):
    root = make_repo(tmp_path / "r")
    present = [n for n in commit_hooks.REQUIRED_HOOKS if n != missing]
    write_hooks(root, names=present)
    git(root, "config", "core.hooksPath", ".githooks")
    assert_refused(
        commit_hooks.hooks_refusal(root),
        "the {} hook is missing".format(missing),
        RESTORE,
    )


@pytest.mark.skipif(os.name == "nt", reason="the executable bit is POSIX-only")
def test_a_non_executable_hook_is_not_on(tmp_path):
    root = make_repo(tmp_path / "r")
    write_hooks(root)
    (root / ".githooks" / "commit-msg").chmod(0o644)
    git(root, "config", "core.hooksPath", ".githooks")
    assert_refused(commit_hooks.hooks_refusal(root), "not executable", MAKE_EXECUTABLE)


def test_a_directory_that_is_not_a_work_tree_is_not_on(tmp_path):
    skip_without_env_gates("git")
    bare = tmp_path / "plain"
    bare.mkdir()
    assert_refused(commit_hooks.hooks_refusal(bare), "git could not say")


def test_an_unanswering_git_is_not_on(tmp_path, monkeypatch):
    root = make_repo(tmp_path / "r")
    write_hooks(root)
    git(root, "config", "core.hooksPath", ".githooks")
    monkeypatch.setattr(kitgit, "git_out", lambda *a, **k: None)
    assert_refused(commit_hooks.hooks_refusal(root), "git could not say")


# --- on ----------------------------------------------------------------------


def test_a_relative_githooks_is_on(tmp_path):
    root = make_repo(tmp_path / "r")
    write_hooks(root)
    git(root, "config", "core.hooksPath", ".githooks")
    assert commit_hooks.hooks_refusal(root) is None


def test_an_absolute_githooks_is_on(tmp_path):
    root = make_repo(tmp_path / "r")
    hooks = write_hooks(root)
    git(root, "config", "core.hooksPath", str(hooks))
    assert commit_hooks.hooks_refusal(root) is None


def test_a_linked_worktree_is_on_with_a_tracked_relative_githooks(tmp_path):
    root = make_repo(tmp_path / "r")
    write_hooks(root)
    git(root, "config", "core.hooksPath", ".githooks")
    commit_all(root)
    lane = tmp_path / "lane"
    git(root, "worktree", "add", "-q", "-b", "lane", str(lane))
    assert commit_hooks.hooks_refusal(lane) is None


def test_a_linked_worktree_is_on_with_the_main_worktrees_absolute_githooks(tmp_path):
    root = make_repo(tmp_path / "r")
    hooks = write_hooks(root)
    (root / ".gitignore").write_text(".githooks/\n", encoding="utf-8")
    git(root, "config", "core.hooksPath", str(hooks))
    commit_all(root)
    lane = tmp_path / "lane"
    git(root, "worktree", "add", "-q", "-b", "lane", str(lane))
    assert not (lane / ".githooks").exists()
    assert commit_hooks.hooks_refusal(lane) is None


# --- no override -------------------------------------------------------------


def test_the_check_reads_no_override():
    # Nothing turns the check off: no environment read anywhere in the module,
    # and the one public function takes the checkout's root and nothing else.
    path = SCRIPTS / "kitlib" / "commit_hooks.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    for word in ("environ", "getenv", "environb", "putenv"):
        assert word not in names | attrs, word
    fn = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "hooks_refusal"
    )
    args = fn.args
    assert [a.arg for a in args.args] == ["root"]
    assert not args.defaults and not args.kw_defaults
    assert args.vararg is None and args.kwarg is None
    assert not args.kwonlyargs and not args.posonlyargs


# --- the fixture helper --------------------------------------------------------


def test_hooks_on_makes_a_fixture_read_on(tmp_path):
    root = make_repo(tmp_path / "r")
    assert commit_hooks.hooks_refusal(root) is not None
    hooks_on(root)
    assert commit_hooks.hooks_refusal(root) is None
    commit_all(root)
    lane = tmp_path / "lane"
    git(root, "worktree", "add", "-q", "-b", "lane", str(lane))
    assert commit_hooks.hooks_refusal(lane) is None


def test_hooks_on_leaves_an_untracked_githooks_clean(tmp_path):
    root = make_repo(tmp_path / "r")
    hooks_on(root)
    commit_all(root)
    assert git(root, "status", "--porcelain") == ""


def test_hooks_on_leaves_a_tracked_githooks_clean(tmp_path):
    root = make_repo(tmp_path / "r")
    hooks = root / ".githooks"
    hooks.mkdir()
    for name in ("pre-commit", "commit-msg", "pre-push"):
        (hooks / name).write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    commit_all(root)
    hooks_on(root)
    assert git(root, "status", "--porcelain") == ""
    (root / "more.txt").write_text("more\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "more")
    assert git(root, "status", "--porcelain") == ""
    assert commit_hooks.hooks_refusal(root) is None
