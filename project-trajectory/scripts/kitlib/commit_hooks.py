"""Whether this checkout's commit hooks are on: the one check every agent
route calls before it starts.

WHY IT EXISTS (WI-926). The kit's commit hooks are opt-in per checkout: only
setup and dev-setup set `core.hooksPath`, and git cannot install a hook at
clone. In a fresh clone, or where setup was skipped, every commit runs with
no hook and nobody typed a bypass. So each agent route (the loop's launch,
the session service's launch, the trunk bookkeeping commit, the refresh, the
merge slot, the coordinator lease's take) asks this module first and refuses
to start when the answer is "not on".

WHAT "ON" MEANS, deny by default. git's hooks directory, read once
(`rev-parse --git-path hooks`, which honours `core.hooksPath`), is the
`.githooks` directory at the top of this worktree or of the main worktree,
and `pre-commit` and `commit-msg` are files there (on POSIX, executable,
since git skips a hook that is not). Everything else is "not on":
`core.hooksPath` unset, empty or naming another directory (a hook manager's,
or `.git/hooks`), a missing or non-executable hook, a git call that fails.

WHAT IT DOES NOT DO. It never reads the hooks' contents: whether a hook can
find the kit scripts is the hook's own refusal. It reads no environment
variable and takes no parameter besides the checkout's root, so nothing can
turn it off.

Contracts: IF-297 — the interface seam this module declares (process.md §8;
row of record in docs/requirements/interfaces.toml).

Contract IF-297: hooks_refusal(root) -> None | refusal text.
    None when the checkout's commit hooks are on; otherwise one line naming
    the cause found and the step that repairs it: for the hooks path, the
    setup step that turns them on (setup, or dev-setup where a repository
    carries no setup script) and the git command it runs; for a missing hook,
    restoring it; for a hook without its mode bit, making it executable.
    Every agent route calls it before any work and refuses on a text.
"""

import os
from pathlib import Path

from kitlib import git as kitgit

__all__ = ["REQUIRED_HOOKS", "hooks_refusal"]

# The two hooks a commit runs through; pre-push guards a push, not a commit.
REQUIRED_HOOKS = ("pre-commit", "commit-msg")

# The repair for each kind of cause. The hooks path is set by setup (a
# scaffold's scripts/setup.*) or, in a repository that carries no setup
# script, by its dev-setup; both run the same git command, named last as the
# step every checkout has. Neither creates a hook or sets a mode bit, so those
# two causes name their own repair.
_ACTIVATE = (
    "Turn the hooks on: sh scripts/setup.sh (Windows: scripts\\setup.ps1; a "
    "repository without them: its dev-setup), or git config core.hooksPath "
    ".githooks"
)
_RESTORE = (
    "Restore it: git checkout -- .githooks in that checkout, or re-run "
    "bootstrap, which writes it"
)
_MAKE_EXECUTABLE = (
    "Make it executable: chmod +x {hook}, and git update-index --chmod=+x on "
    "it so the tracked mode keeps the bit"
)


def _key(path):
    """A path in the form two spellings of one directory compare equal in."""
    return os.path.normcase(str(Path(path).resolve()))


def _git_dirs(root):
    """(hooks dir, common git dir, this worktree's top) from one git call, or
    None when git does not answer three lines."""
    out = kitgit.git_out(
        root,
        [
            "rev-parse",
            "--path-format=absolute",
            "--git-path",
            "hooks",
            "--git-common-dir",
            "--show-toplevel",
        ],
    )
    lines = [ln for ln in (out or "").splitlines() if ln.strip()]
    if len(lines) != 3:
        return None
    return tuple(Path(ln.strip()) for ln in lines)


def _directory_cause(hooks, common, top):
    """(cause, repair) when the hooks directory is not this checkout's
    `.githooks`, or None."""
    allowed = {_key(top / ".githooks"), _key(common.parent / ".githooks")}
    if _key(hooks) in allowed:
        return None
    if _key(hooks) == _key(common / "hooks"):
        cause = "core.hooksPath is unset or names .git/hooks, so git runs no kit hook"
    else:
        cause = "core.hooksPath names {}, not this checkout's .githooks".format(hooks)
    return cause, _ACTIVATE


def _file_cause(hooks):
    """(cause, repair) when a required hook in `hooks` cannot run, or None."""
    for name in REQUIRED_HOOKS:
        hook = hooks / name
        if not hook.is_file():
            return "the {} hook is missing from {}".format(name, hooks), _RESTORE
        if os.name != "nt" and not os.access(hook, os.X_OK):
            cause = "the {} hook in {} is not executable, so git skips it".format(
                name, hooks
            )
            return cause, _MAKE_EXECUTABLE.format(hook=hook)
    return None


def hooks_refusal(root):
    """None when this checkout's commit hooks are on, else the refusal text,
    naming the cause found and the step that repairs that cause.

    Contract:
      Inputs:  root: path-like — the checkout an agent route starts in
      Outputs: str | None — None when on; the refusal text when not on

    Implements: SR-240, LLR-340
    """
    dirs = _git_dirs(root)
    if dirs is None:
        cause = "git could not say where {} runs its hooks (git missing, or not a work tree)".format(
            root
        )
        found = (cause, _ACTIVATE)
    else:
        found = _directory_cause(*dirs) or _file_cause(dirs[0])
    if found is None:
        return None
    return "this checkout's commit hooks are not on: {}. {}.".format(*found)
