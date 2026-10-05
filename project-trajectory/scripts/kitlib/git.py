"""The best-effort-off-git subprocess pattern — one home for "git, or None".

Most of the kit's git reads are ENRICHMENT, not gating: a commit clock behind a
staleness warn, a short SHA in a stamp, the branch behind a status line. Every
one of them must degrade to "I don't know" rather than crash, because the kit
has to run in three environments where git legitimately answers nothing — no
git binary on PATH, a directory that is not a repository (a tarball adopter,
a scaffold before its first `git init`), and a shallow or detached checkout
where the rev exists but the history does not.

`git_out` is that degrade, stated once. It was copied into `check.py`,
`trace.py` and `trunk_step.py`, each carrying a docstring that pointed at the
others as the pattern's home — three homes and no owner, which is the shape D-8
(`OI-16`) retired. A FOURTH copy survived that pass and is folded in here at
WI-521 slice 1: `check_trajectory._git`, which was the same body plus an
optional `stdin`. The `stdin` argument is the whole reason it was missed — it
looked like a different function — so it is a parameter here rather than a
private variant, and both readers of it (`check_trajectory`, `acceptance_record`)
now alias this one home the way `check.py` already did.

WHAT THIS MODULE DELIBERATELY DOES NOT DO: it never decides what an absent
answer MEANS. `None` is "git had nothing to say"; whether that is benign (skip
the enrichment) or fatal (a gate that requires history) is the caller's
fail-direction to declare, and folding that choice in here would hide it.

TWO READS FOR A TWO-TREE RULE (WI-818). A commit-time rule comparing a commit
with its parent needs two answers `git_out` cannot give losslessly: the paths a
listing prints, which a plain listing quotes and escapes under `core.quotePath`
(`git_paths` reads them NUL-delimited), and a blob read that tells a path the
tree does not list from one it lists but cannot read (`git_show`, raising
`UnreadableBlob` for the second). Neither decides what that MEANS: the ruling
sync and the overrule sync in `acceptance_record` refuse an unreadable blob.
"""

import subprocess

__all__ = ["UnreadableBlob", "git_bytes", "git_out", "git_paths", "git_show"]


def _git_stdout(root, args, **kwargs):
    """Run one read-only git command and preserve its requested stdout type."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, **kwargs
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def git_out(root, args, stdin=None):
    """stdout of `git -C <root> <args>`, or None on ANY failure.

    None covers all of: no git binary (`OSError`), a bad argument vector
    (`ValueError`), not a repository, an unknown rev or path, and any non-zero
    exit. Decoded as UTF-8 with `errors="replace"`, so a commit message or path
    in another encoding degrades to replacement characters instead of raising
    inside a check that only wanted a SHA.

    `stdin` feeds a BATCH command — `cat-file --batch-check` is the live caller
    — which is how a scan asks about many blobs in ONE subprocess instead of two
    per file. It matters where the scan rides an always-on floor rather than a
    gate. `None` (the default) passes nothing, which is byte-for-byte the
    no-input behaviour every other caller already had.

    Not a security boundary and not a general git wrapper: `args` is passed as
    a list to a non-shell `subprocess.run`, so nothing here interpolates into a
    shell, but a caller passing attacker-controlled `args` owns that choice.

    Contract:
      Inputs:  root: path-like repo root; args: sequence of git arguments;
               stdin: str | None — batch input, or nothing
      Outputs: str | None — stdout on success; None on any failure
    """
    return _git_stdout(
        root,
        args,
        text=True,
        encoding="utf-8",
        errors="replace",
        input=stdin,
    )


def git_bytes(root, args):
    """Raw stdout of `git -C <root> <args>`, or None on ANY failure.

    This is the binary counterpart to `git_out` for Git protocols whose bytes
    carry identity rather than display text. Callers parse their ASCII framing
    before deciding whether any field may be decoded.
    """
    return _git_stdout(root, args)


def git_paths(root, args):
    """The paths a path-listing git subcommand (`args[0]`: `diff`, `ls-files`,
    `ls-tree`) prints, read LOSSLESSLY: `-z` makes the listing NUL-delimited
    and unquoted, where a plain listing under `core.quotePath` (git's default)
    quotes and escapes any path with a non-ASCII byte, which then matches no
    prefix and names no blob. None when git cannot answer. The ruling sync and
    the overrule sync read every path list through it.

    Implements: SR-225, LLR-303
    """
    out = git_out(root, [args[0], "-z"] + list(args[1:]))
    if out is None:
        return None
    return [path for path in out.split("\0") if path]


class UnreadableBlob(Exception):
    """A path its tree lists whose blob git cannot read (a partial clone
    offline, a damaged object store). The ruling sync refuses it by name:
    a failed read is never an absent file (A1)."""


def git_show(root, prefix, path):
    """The text of `prefix + path` (`prefix` a `git show` prefix: `"<rev>:"` or
    `":"` for the index), None when the tree does not list the path; raises
    `UnreadableBlob` when it lists the path but its blob cannot be read.

    Implements: SR-148, SR-225, LLR-303
    """
    text = git_out(root, ["show", prefix + path])
    if text is not None:
        return text
    if prefix == ":":
        listed = git_out(root, ["ls-files", "--", path])
    else:
        listed = git_out(root, ["ls-tree", "--name-only", prefix[:-1], "--", path])
    if listed is None or listed.strip():
        raise UnreadableBlob(prefix + path)
    return None
