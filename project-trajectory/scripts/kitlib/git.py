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
and `git_out`'s replacing decoder turns into other paths (`git_paths` reads
them NUL-delimited as bytes, decoded without loss), and a blob read that tells
a path the tree does not list from one it lists but cannot read (`git_show`,
raising `UnreadableBlob` for the second, and for a path that is not UTF-8,
which it cannot hand back to git). Neither decides what that MEANS: the ruling
sync and the overrule sync in `acceptance_record` refuse an unreadable blob.

ONE CLAIMED-BRANCH READER. `claimed_work_branch` answers whether the checkout
is a claimed lane. It moved here from `check.py` so every caller that must
tell a lane from the trunk shares one reader; as with `git_out`, None is
"no claim found", and each caller declares what that means for it.
"""

import subprocess
from pathlib import Path

__all__ = [
    "UnreadableBlob",
    "claimed_work_branch",
    "git_bytes",
    "git_out",
    "git_paths",
    "git_show",
    "grep_files",
    "squash_commits",
]


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
    prefix and names no blob; and the bytes are decoded as UTF-8 with
    `surrogateescape`, so a byte that is not UTF-8 is kept as a lone surrogate
    (`path.encode("utf-8", "surrogateescape")` is git's exact path), never
    replaced by U+FFFD, which would name another path. None when git cannot
    answer. The ruling sync and the overrule sync read every path list
    through it.

    Implements: SR-225, LLR-303
    """
    out = git_bytes(root, [args[0], "-z"] + list(args[1:]))
    if out is None:
        return None
    return [path for path in out.decode("utf-8", "surrogateescape").split("\0") if path]


class UnreadableBlob(Exception):
    """A path its tree lists whose blob git cannot read (a partial clone
    offline, a damaged object store), or whose name is not UTF-8 and so cannot
    be handed back to git as an argument on every platform. The ruling sync
    refuses it by name: a failed read is never an absent file (A1)."""


def _shown(path):
    """`path` printable on any UTF-8 stream: a byte that is not UTF-8 (a lone
    surrogate from `git_paths`) shown as `\\xNN`.

    Implements: SR-225, LLR-303
    """
    return path.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace")


def grep_files(root, rev, needle, path):
    """The paths under `path` in the tree `rev` (None: the index) whose text
    holds the fixed string `needle`, read NUL-delimited like `git_paths`; []
    when none does, and None when git cannot answer. `git grep` exits 1 for
    "no match" and higher for a failure, so the two are told apart here: a
    search that could not run is never read as "nothing found".

    Implements: SR-208, LLR-246
    """
    args = ["grep", "-l", "-z", "-F", "-e", needle]
    args += ["--cached"] if rev is None else [rev]
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args, "--", path], capture_output=True
        )
    except (OSError, ValueError):
        return None
    if proc.returncode == 1 and not proc.stdout and not proc.stderr.strip():
        return []
    if proc.returncode != 0:
        return None
    prefix = "" if rev is None else rev + ":"
    found = proc.stdout.decode("utf-8", "surrogateescape").split("\0")
    return [p[len(prefix) :] if p.startswith(prefix) else p for p in found if p]


def git_show(root, prefix, path):
    """The text of `prefix + path` (`prefix` a `git show` prefix: `"<rev>:"` or
    `":"` for the index), None when the tree does not list the path; raises
    `UnreadableBlob` when it lists the path but its blob cannot be read, and
    for a path that is not UTF-8 before asking git at all: such a path cannot
    be passed back to git losslessly (a Windows command line re-encodes it to
    another path), so its answer could only be a wrong "absent".

    Implements: SR-148, SR-225, LLR-303
    """
    if _shown(path) != path:
        raise UnreadableBlob(_shown(path) + " (a path that is not UTF-8)")
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


_HEX = frozenset("0123456789abcdef")


def squash_commits(root):
    """The commits a `git merge --squash` in progress folds in, newest first,
    read off git's own `SQUASH_MSG` (each `commit <full id>` header line); []
    when no squash is in progress or the file cannot be read. One reader for
    every pre-commit step that judges a squash landing by the commits it
    carries (text then act, the plan gate): the two-tree rules read no file.

    Implements: SR-140, LLR-302
    """
    rel = (git_out(root, ["rev-parse", "--git-path", "SQUASH_MSG"]) or "").strip()
    path = Path(root) / rel
    try:
        text = path.read_text(encoding="utf-8") if rel and path.is_file() else ""
    except (OSError, UnicodeDecodeError):
        return []
    return [
        ln[7:]
        for ln in text.splitlines()
        if ln.startswith("commit ") and len(ln) >= 47 and set(ln[7:]) <= _HEX
    ]


def claimed_work_branch(root, notice=None):
    """The checkout's branch name IF it is a CLAIMED work branch, else None.

    A claimed branch's work-item specs live in `docs/work/active/<branch>/`,
    moved there by the serial trunk commit that cut the branch, so the branch
    itself carries the evidence: in its working tree, or, once the close moves
    the specs to their terminal directory, in its own history. Off git, on a
    detached HEAD, with an implausible branch name, or with neither a matching
    `active/` directory nor a claim in history, the answer is None; what None
    MEANS (the strict bar, a judged commit) is each caller's to declare.

    `notice`, when given, is called with an implausible branch name before the
    reader answers None for it, so a caller can say out loud that something fed
    it a fake ref; the reader itself prints nothing.

    Implements: SR-006, SR-170, LLR-141
    """
    branch = (git_out(root, ["symbolic-ref", "--short", "HEAD"]) or "").strip()
    if not branch:
        return None  # no git, not a repo, or a detached HEAD
    # A branch name is used here as a relative PATH. git's own ref rules already
    # forbid `..` and `\`, but the answer decides whether a gate runs, so it
    # refuses rather than trusts.
    if ".." in branch or "\\" in branch or branch.startswith("/"):
        if notice is not None:
            notice(branch)
        return None
    active = Path(root) / "docs" / "work" / "active"
    spec_dir = active / branch
    try:
        # Belt-and-braces containment: whatever the name, the claim directory
        # must sit UNDER docs/work/active/ for this to be a claimed branch.
        spec_dir.resolve().relative_to(active.resolve())
    except (OSError, ValueError):
        return None
    if spec_dir.is_dir():
        return branch
    # The working tree alone cannot answer this: the close MOVES the claim out
    # of active/, so from the close commit on the tree holds no claim. History
    # outlives the move: the commit that cut the branch added the directory, and
    # that add stays reachable. One path-limited git call, stopped at the first
    # hit. FAIL-DIRECTION: no git, a failing git or an empty answer all read as
    # unclaimed, because a false positive would relax the trunk's own bar.
    # Residual (review-confirmed breadth): ANY branch whose name ever appeared
    # under docs/work/active/ in reachable history reads as claimed forever (a
    # retired WI branch re-cut, or a throwaway reusing its name); bounding the
    # walk would need a configured trunk name this rule deliberately has not.
    # Cost note: on the trunk the pathspec never matches, so the -1 walk pays
    # full history, measured ~0.05 ms/commit (61 ms at 1.2k commits); a caller
    # that asks often memoizes the answer.
    log = git_out(
        root, ["log", "-1", "--format=%H", "--", "docs/work/active/" + branch]
    )
    return branch if (log or "").strip() else None
