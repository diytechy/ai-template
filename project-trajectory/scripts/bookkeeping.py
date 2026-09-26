"""bookkeeping.py — the ONE trunk bookkeeping commit: commit what the step wrote,
restore only that on a refusal, and advance trunk without touching anything else.

WHY IT EXISTS (WI-612). The loop's two trunk-side writers, the claim
(`integrate.claim`) and the intake mint (`intake._mint`), run in the PRIMARY
checkout, which is also where the owner works. Each used to treat that whole
working tree as its own: `git add -A` staged whatever lay there into the
bookkeeping commit, `git reset --hard HEAD` (plus the mint's `git clean -fd`)
threw it away on a refusal, and `git reset --hard <commit>` advanced trunk over
it. An uncommitted edit was either committed under the loop's name or lost, and
a clean-trunk refusal in front of the claim only GUARDED against that, at the
top of a tick. This module narrows the whole tree to the step's own SCOPE.

WHAT IT PROMISES, AND WHERE IT STOPS:

  * A path OUTSIDE the scope is never touched by this module and never
    committed: not staged, not reset, not checked out, not removed.
  * A path INSIDE the scope is guarded at the pre-check only. An owner edit that
    lands on one DURING the helper's run can be swept into the commit, or
    overwritten by the regeneration (the status splice rewrites
    `docs/status.md` whole), or, on a refusal, restored over if it landed while
    the step was still writing. The window is the helper's own duration, and
    only for the scope's paths (`_full_scope`); nothing here closes it.
  * The one loss inside that window that is cheap to close is closed: once the
    step and its regeneration have written, their blobs are snapshotted, and a
    refusal after that point LEAVES any in-scope path whose file no longer
    matches the snapshot (somebody edited it after the step wrote it), restores
    the rest, and names each path it left so the operator can reconcile it by
    hand. On success such an edit is simply left unstaged beside the commit,
    because the advance never writes the working tree.

THE SEQUENCE, in `commit`:

  1. PRE-CHECK. The caller declares its SCOPE, every path (or `/`-terminated
     prefix) the step may write, and every path `trunk_step.py --regen` may
     write joins it (`trunk_step.regen_writes`), because every bookkeeping
     commit folds the regeneration in (RULING-6). Any uncommitted change inside
     that scope refuses BY NAME before anything is written: an edit there could
     only be overwritten by the step or swept into its commit. Because the
     scope is clean at this point, everything dirty inside it afterwards is
     taken to be the step's own writing - an edit landing there in the window
     above being the exception this module states and does not close.
  2. WRITE. The caller's `write()` performs the step (spec moves, drafted specs,
     the watermark), then `trunk_step.py --regen` re-derives the generated
     artifacts.
  3. COMMIT what changed inside the scope, from a TEMPORARY index seeded from
     HEAD, never the real one, which may hold the owner's staged work.
  4. `before_advance(sha)`, when given. The claim cuts its branch here, BEFORE
     trunk moves: the §A3 order that makes a half-claim benign.
  5. ADVANCE. The real index takes the new commit's entries for the written
     paths, then `update-ref` moves trunk with the old head as its compare-and-
     swap. No working-tree write at all: the files on disk already are the
     commit's.

  Any refusal from step 2 on restores the in-scope changes: index entries
  reset to HEAD, tracked files checked out, files the step created removed -
  except a path edited after the step wrote it (above), which is left and
  named. Nothing outside the scope is read back, reset or removed. A step that
  RAISES is restored the same way, and the restore's outcome rides the
  exception as a note, so a restore that failed (a file another process holds
  open on Windows) is named rather than left as silent residue.

WHY THE REGENERATION'S SHARE IS `trunk_step`'S TABLE, NOT `[generated]`. The
stack.ini section declares OWNERSHIP, and an adopter's copy can lag what the
regeneration writes (the shipped template names three rows while the step writes
`docs/stage` and `docs/open-items.html` too), so staging only declared rows would
leave a scaffold's claim DIRTY behind itself. The table that runs the generators
is the one place that knows what they write. Every generator's path is taken,
applicable here or not: one that does not apply writes nothing, so its path
costs only a refusal while it is dirty.

WHAT IT CANNOT SEE: the regeneration READS the working tree, so an uncommitted
edit to a generator INPUT stays out of the commit but shapes the artifacts it
carries, until a regeneration over committed state (the next bookkeeping commit,
or a lane's refresh) re-derives them.

WHAT IT DOES NOT COVER: the lane-worktree resets in `handback.py` and in
`integrate.py`'s refresh and unload paths. Those run in the loop's own
worktrees, where nobody else's work lives.

Stdlib only; Windows and POSIX. Every git call here runs with
GIT_LITERAL_PATHSPECS set, so a path is a path and never a glob.

Contracts: IF-186 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-186: the shared trunk bookkeeping commit, by importer.
    `commit(root, scope, write, message, *, label, before_advance=None)` returns
    `(sha, None)` once trunk has advanced to a commit holding exactly the paths
    the step changed inside its scope plus the regeneration, or `(None,
    refusal)` with the reason named: a dirty in-scope path (nothing written), a
    refusal from `write` or `before_advance`, a failed regeneration, or a git
    failure; an exception from the step propagates with the restore's report
    as a note. A path outside the scope is never touched or committed. A path
    inside it is guarded at the pre-check only: an edit landing on one during
    the helper's run can be swept into the commit, overwritten by the
    regeneration, or restored over on a refusal - except that once the step
    has written, a refusal leaves any in-scope path edited since and names it.
    Every other in-scope change is restored on a refusal. `message` is the
    commit message, or a zero-argument callable that builds it once the writes
    are done. The claim and the intake mint are the callers, and neither
    stages, restores or advances trunk by any other route.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import agent_common as ac
import trunk_step

# Where `trunk_step.py` is found. A module attribute rather than a literal in
# the call, so a test can stand a failing regeneration in for the real one.
SCRIPTS = Path(__file__).resolve().parent

# Paths per git invocation: a long write set stays under the Windows command-
# line ceiling without depending on a pathspec-file flag an older git lacks.
_CHUNK = 100


class _Refused(Exception):
    """A refusal raised inside the sequence and returned at its boundary: the
    contract is a return value, never a raise."""


def commit(root, scope, write, message, *, label, before_advance=None):
    """The trunk bookkeeping commit: `(sha, None)` or `(None, refusal)`.

    `scope` is every path or `/`-terminated prefix the step may write; `write()`
    performs the step and returns a refusal string or None; `label` names the
    step in every refusal ("the claim"). The module docstring states the
    sequence and why each step is shaped the way it is.

    Implements: SR-156, LLR-151
    """
    root = Path(root)
    scope = _full_scope(scope)
    try:
        head = _checked(root, "rev-parse", "--verify", "HEAD", why="no HEAD").strip()
        clash = _changed(root, scope)
    except _Refused as exc:
        return None, "{} cannot start: {}".format(label, exc)
    if clash:
        return None, (
            "{} writes paths that carry uncommitted edits: {} - commit or set "
            "them aside, then re-run; nothing was written".format(
                label, ", ".join(clash)
            )
        )
    # What the step left on disk, once it has written: None until then, so a
    # refusal during the step restores every in-scope change (the declared
    # window), and a refusal after it leaves any path edited since.
    wrote = None
    try:
        _write_and_regenerate(root, write, label)
        written = _changed(root, scope)
        wrote = _blobs(root, written)
        sha = _commit_object(root, head, written, message)
        if before_advance is not None:
            _raise_on(before_advance(sha))
        _advance(root, head, sha, written, label)
    except _Refused as exc:
        return None, _restore(root, scope, str(exc), label, wrote)
    except Exception as exc:
        # A step that CRASHES still owes the tree its restore, and the operator
        # owes a word on how it went: the exception propagates carrying the
        # restore's own report, success or failure (PEP 678 notes, 3.11+).
        exc.add_note(_restore(root, scope, "{} raised".format(label), label, wrote))
        raise
    return sha, None


def _full_scope(scope):
    paths = {str(p).replace("\\", "/").strip() for p in scope}
    paths.update(trunk_step.regen_writes())
    return sorted(p for p in paths if p)


def _git(root, *args, env=None, stdin=None):
    """`(code, stdout)`, with stderr appended on failure (the `ac.git` shape).
    stdout is NOT stripped: a `status --porcelain` entry can open with a
    meaningful space. `stdin` feeds a batch command; otherwise stdin is closed."""
    feed = {"input": stdin} if stdin is not None else {"stdin": subprocess.DEVNULL}
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=dict(os.environ, GIT_LITERAL_PATHSPECS="1", **(env or {})),
        **feed,
    )
    out = proc.stdout or ""
    if proc.returncode != 0 and proc.stderr:
        out = (out + "\n" + proc.stderr).strip()
    return proc.returncode, out


def _checked(root, *args, why, env=None, stdin=None):
    code, out = _git(root, *args, env=env, stdin=stdin)
    if code != 0:
        raise _Refused("{}:\n{}".format(why, ac._failure_tail(out)))
    return out


def _each_chunk(root, args, paths, why, env=None):
    """Run `git <args> -- <paths>` in bounded chunks; the outputs, joined."""
    return "".join(
        _checked(root, *args, "--", *paths[i : i + _CHUNK], why=why, env=env)
        for i in range(0, len(paths), _CHUNK)
    )


def _raise_on(refusal):
    if refusal:
        raise _Refused(refusal)


def _changed(root, scope):
    """Every path inside `scope` that differs from HEAD - staged, unstaged or
    untracked - sorted. `--no-renames` names both sides of a move."""
    out = _each_chunk(
        root,
        ("status", "--porcelain=v1", "-z", "--no-renames", "--untracked-files=all"),
        scope,
        why="the working tree could not be read",
    )
    return sorted({entry[3:] for entry in out.split("\0") if len(entry) > 3})


def _blobs(root, paths):
    """`{path: the blob id of the file on disk, or None when there is none}`,
    in ONE `hash-object --stdin-paths` call, through the repo's own clean
    filters - so two readings of a path compare the way git would."""
    present = [p for p in paths if (root / p).is_file()]
    ids = []
    if present:
        ids = _checked(
            root,
            "hash-object",
            "--stdin-paths",
            why="the written files could not be read",
            stdin="".join(p + "\n" for p in present),
        ).split()
    found = dict(zip(present, ids))
    return {p: found.get(p) for p in paths}


def _write_and_regenerate(root, write, label):
    _raise_on(write())
    proc = subprocess.run(
        [
            str(ac.harness_python(root)),
            str(SCRIPTS / "trunk_step.py"),
            "--root",
            ".",
            "--regen",
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        raise _Refused(
            "{}'s regeneration failed:\n{}".format(
                label, ac._failure_tail((proc.stdout or "") + (proc.stderr or ""))
            )
        )


def _commit_object(root, head, written, message):
    """The commit object for HEAD plus exactly `written`, built in a TEMPORARY
    index. `update-index --add --remove` takes an addition, an edit and a
    deletion alike, through the repo's own clean filters."""
    text = message() if callable(message) else message
    with tempfile.TemporaryDirectory(prefix="bookkeeping-") as tmp:
        env = {"GIT_INDEX_FILE": str(Path(tmp) / "index")}
        _checked(root, "read-tree", head, why="HEAD could not seed an index", env=env)
        _each_chunk(
            root,
            ("update-index", "--add", "--remove"),
            written,
            why="the written paths could not be staged",
            env=env,
        )
        tree = _checked(root, "write-tree", why="the tree could not be named", env=env)
    return _checked(
        root,
        "commit-tree",
        tree.strip(),
        "-p",
        head,
        "-m",
        text,
        why="the commit object could not be written",
    ).strip()


def _advance(root, head, sha, written, label):
    """The real index takes `sha`'s entries for `written`, then trunk moves to
    `sha` only if it still stands at `head`."""
    _each_chunk(
        root,
        ("reset", "-q", sha),
        written,
        why="the index could not take the new commit's entries",
    )
    _checked(
        root,
        "update-ref",
        "-m",
        "bookkeeping: {}".format(label),
        "HEAD",
        sha,
        head,
        why="trunk did not advance onto {}".format(sha[:10]),
    )


def _restore(root, scope, refusal, label, wrote=None):
    """Undo the in-scope changes - which, the scope having been clean at the
    pre-check, are the step's writes - and return the refusal, saying whether
    the restore held and naming any path it left.

    `wrote` is the snapshot taken once the step had written (None when the
    refusal came first). A dirty path whose file no longer matches it - edited
    after the step wrote it, or dirty although the step never wrote it - is
    somebody else's edit landing in the window: its index entry goes back to
    HEAD, which touches no file, but its file is LEFT and named."""
    dirty, left = [], []
    try:
        dirty = _changed(root, scope)
        if wrote is not None:
            now = _blobs(root, dirty)
            left = [p for p in dirty if p not in wrote or now[p] != wrote[p]]
        if dirty:
            _each_chunk(root, ("reset", "-q"), dirty, why="the index kept its entries")
            tracked = set(
                _each_chunk(
                    root,
                    ("ls-tree", "-r", "-z", "--name-only", "HEAD"),
                    dirty,
                    why="HEAD could not be listed",
                ).split("\0")
            )
            undo = [p for p in dirty if p not in left]
            back = [p for p in undo if p in tracked]
            if back:
                _each_chunk(root, ("checkout",), back, why="the checkout failed")
            for rel in (p for p in undo if p not in tracked):
                (root / rel).unlink(missing_ok=True)
    except (_Refused, OSError) as exc:
        return (
            "{} - and the restore FAILED, so these paths {} wrote may still be "
            "dirty: {} ({})".format(refusal, label, ", ".join(dirty) or "unread", exc)
        )
    kept = ""
    if left:
        kept = "; it LEFT {}, edited after it wrote them - reconcile by hand".format(
            ", ".join(left)
        )
    return "{} ({} restored the paths it wrote and nothing else{})".format(
        refusal, label, kept
    )
