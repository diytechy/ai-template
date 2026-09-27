"""bookkeeping.py — the ONE trunk bookkeeping commit: build it away from the
owner's checkout, install exactly what it wrote, and advance trunk.

WHY IT EXISTS (WI-612). The loop's two trunk-side writers, the claim
(`integrate.claim`) and the intake mint (`intake._mint`), run in the PRIMARY
checkout, which is also where the owner works. Each used to treat that whole
working tree as its own: `git add -A` staged whatever lay there into the
bookkeeping commit, `git reset --hard HEAD` (plus the mint's `git clean -fd`)
threw it away on a refusal, and `git reset --hard <commit>` advanced trunk over
it. An uncommitted edit was either committed under the loop's name or lost, and
a clean-trunk refusal in front of the claim only GUARDED against that, at the
top of a tick. This module narrows the whole tree to the step's own SCOPE.

WHY THE STEP RUNS ELSEWHERE (WI-647). Narrowing to the scope still left the
step writing in the checkout, so an owner edit landing on an in-scope path
while it ran (the prose of `docs/status.md`, which the status splice rewrites
whole) could be swept into the commit or overwritten, and the regeneration read
the checkout, so an uncommitted edit to a generator INPUT shaped the artifacts
the commit carried. The step and its regeneration now run in a SCRATCH
worktree cut from HEAD, and the checkout is written only by the install.

WHAT IT PROMISES, AND WHERE IT STOPS:

  * A path OUTSIDE the scope is never touched by this module and never
    committed: not staged, not reset, not checked out, not removed. A write the
    step makes outside its scope stays in the scratch worktree and is discarded
    with it.
  * The commit is HEAD plus what the step wrote plus what the regeneration
    derived from exactly that: every file the step and the generators READ is
    the scratch's, so no uncommitted edit in the checkout, in scope or out, a
    generator input included, reaches the commit or shapes it - save the reads
    named under WHAT IT CANNOT SEE.
  * The SCOPE is planned over HEAD: a caller whose write set depends on
    what the files say (the claim's relink plan reads every markdown file)
    passes a callable, which is handed the scratch worktree's root, so an
    uncommitted edit that hides or adds a link neither narrows nor widens it.
    The pre-check and the commit use that one plan.
  * A path INSIDE the scope is guarded twice: at the pre-check, before the
    step runs, and at the drift check, immediately before the install and
    after the caller's `before_advance`, which refuses BY NAME any in-scope
    path that no longer equals HEAD and installs nothing. An owner edit made
    while the step, its regeneration or the caller's callback ran therefore
    survives untouched and is named.
  * The window that remains is the INSTALL itself: the few git calls between
    the drift check and the trunk advance that write the commit's paths into
    the checkout. An edit landing on one of those paths in that interval can
    be overwritten; nothing here closes it. A refusal inside the
    install (the compare-and-swap losing to a trunk that moved, a git failure)
    restores what the install wrote and LEAVES any path whose file no longer
    matches what the install put there, naming each so the operator can
    reconcile it by hand.

THE SEQUENCE, in `commit`:

  1. SCRATCH. A detached worktree is cut from HEAD in the system's temporary
     directory.
  2. PRE-CHECK. The caller's SCOPE - every path (or `/`-terminated prefix) the
     step may write, or a callable planning it in the scratch - is resolved,
     and every path `trunk_step.py --regen` may write joins it
     (`trunk_step.regen_writes`, asked of the copy the regeneration runs),
     because every bookkeeping commit folds the regeneration in (RULING-6).
     Any uncommitted change inside that scope in the checkout refuses BY NAME
     before anything is written: the install would overwrite it.
  3. STEP. The caller's `write(scratch)` performs the step in the scratch
     (spec moves, drafted specs, the watermark), then the kit's committed
     `trunk_step.py --regen` re-derives the generated artifacts with the
     scratch as its root.
  4. COMMIT what changed inside the scope in the scratch, from a TEMPORARY index
     seeded from HEAD. The scratch is then removed, whatever the outcome.
  5. `before_advance(sha)`, when given. The claim cuts its branch here, BEFORE
     trunk moves: the §A3 order that makes a half-claim benign, so a refusal
     from here on leaves at worst a branch holding a claim trunk never took.
  6. DRIFT CHECK. HEAD must still be the commit the scratch was cut from, and
     every in-scope path in the checkout must still equal it.
  7. INSTALL AND ADVANCE. The paths the commit removes leave the index and the
     disk, the rest are checked out from it, index and file together, then
     `update-ref` moves trunk with the old head as its compare-and-swap.

  Any refusal before step 7 has written nothing in the checkout, and one
  before step 5 has cut no branch either. A step that RAISES propagates with a
  note saying so, and a scratch worktree that would not remove (a file another
  process holds open on Windows) is named on stderr with the command that
  removes it, rather than left as silent residue.

WHY THE REGENERATION'S SHARE IS `trunk_step`'S TABLE, NOT `[generated]`. The
stack.ini section declares OWNERSHIP, and an adopter's copy can lag what the
regeneration writes (the shipped template names three rows while the step writes
`docs/stage` and `docs/open-items.html` too), so staging only declared rows would
leave a scaffold's claim DIRTY behind itself. The table that runs the generators
is the one place that knows what they write. Every generator's path is taken,
applicable here or not: one that does not apply writes nothing, so its path
costs only a refusal while it is dirty.

WHAT IT CANNOT SEE: an edit landing on an in-scope path during the install
(above). Everything else the commit is made of is read from HEAD: the scope
plan, the step's and the generators' inputs, the held-status dial (the one
committed in HEAD, `agent_common.loop_held_status_refusal`), and the generator
CODE, because the regeneration runs the scratch's committed copy of
`trunk_step.py` - and so its generators and its write table - wherever the
running kit lies inside the repository. What still comes from the checkout is
the running process itself: this module and its caller as loaded, and the
harness interpreter (a `.venv` is never committed). A kit HEAD does not carry
(run from outside the repository, or not yet committed) is no committed input
of it, and runs as loaded.

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
    refusal from `scope`, `write` or `before_advance`, a failed regeneration, a
    git failure, an in-scope path edited in the checkout or a trunk that moved
    while the step or `before_advance` ran (nothing installed), or - under the loop marker - a
    tree that would change a status the approval level holds for a human,
    judged before `commit-tree`; an exception from the step propagates with a
    note saying what it left. `scope` is the paths the step may write, or a
    callable `scope(scratch) -> (paths, refusal)` that plans them over HEAD in
    the scratch; the pre-check and the commit use that one plan.
    `write(scratch)` performs the step in a scratch worktree cut from HEAD,
    where the regeneration also runs the kit's committed scripts, so neither
    writes in the checkout and an uncommitted edit there, to an input or to a
    generator the repository carries, reaches nothing they read. Under the loop marker the commit's
    message carries the `Loop-Session` trailer. A path outside the scope is
    never touched or committed. A path inside it is guarded at the pre-check
    and again immediately before the install, after `before_advance`; the one
    window left is the install itself, where an edit landing on a path the commit writes can be
    overwritten, and a refusal inside the install restores what it wrote,
    leaving and naming any path edited since. `message` is the commit message,
    or a zero-argument callable that builds it once the writes are done. The
    claim and the intake mint are the callers, and neither stages, restores or
    advances trunk by any other route.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import agent_common as ac
import trunk_step
from kitlib import provenance as _kitprovenance

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

    `scope` is every path or `/`-terminated prefix the step may write, or a
    callable planning them in the scratch worktree (`(paths, refusal)`);
    `write(scratch)` performs the step inside the scratch worktree whose root it
    is handed and returns a refusal string or None; `label` names the step in
    every refusal ("the claim"). The module docstring states the sequence and
    why each step is shaped the way it is.

    Implements: SR-156, LLR-151
    """
    root = Path(root)
    try:
        head = _checked(root, "rev-parse", "--verify", "HEAD", why="no HEAD").strip()
    except _Refused as exc:
        return None, "{} cannot start: {}".format(label, exc)
    untouched = "{} wrote nothing in the checkout".format(label)
    try:
        sha, written, scope = _build(root, head, scope, write, message, label)
        installing = _blobs_at(root, sha, written)
        if before_advance is not None:
            _raise_on(before_advance(sha))
        # The drift check runs LAST, after the caller's callback too, which
        # nothing here bounds: only the install's own git calls follow it.
        _drift_check(root, head, scope, label)
    except _Refused as exc:
        return None, "{} ({})".format(exc, untouched)
    except Exception as exc:
        # A crash before the install owes the operator the word a refusal gets:
        # the checkout is as it was (PEP 678 notes, 3.11+).
        exc.add_note("{} raised; {}".format(label, untouched))
        raise
    try:
        _install(root, head, sha, installing, label)
    except _Refused as exc:
        return None, _restore(root, scope, str(exc), label, installing)
    except Exception as exc:
        # A crash inside the install still owes the checkout its restore, and
        # the exception carries the restore's own report, success or failure.
        exc.add_note(
            _restore(root, scope, "{} raised".format(label), label, installing)
        )
        raise
    return sha, None


def _full_scope(root, scope, scratch, label):
    """The step's write set planned over HEAD - a callable scope is handed the
    scratch, which is HEAD - joined by the regeneration's."""
    if callable(scope):
        scope, refusal = scope(scratch)
        _raise_on(refusal)
    paths = {str(p).replace("\\", "/").strip() for p in scope}
    paths.update(_regen_writes(root, scratch, label))
    return sorted(p for p in paths if p)


def _regen_writes(root, scratch, label):
    """The regeneration's write table, read from the SAME `trunk_step.py` the
    regeneration runs: the committed copy's, asked in a subprocess (importing
    it here would collide with the loaded kit's modules), so an uncommitted
    REGEN_STEPS edit cannot drop a committed output from the commit. Where the
    regeneration runs the loaded kit, the loaded table is the one it writes."""
    script = _committed_trunk_step(root, scratch)
    if script == SCRIPTS / "trunk_step.py":
        return trunk_step.regen_writes()
    ask = (
        "import sys; sys.path.insert(0, sys.argv[1]); import trunk_step; "
        "print('\\n'.join(trunk_step.regen_writes()))"
    )
    proc = subprocess.run(
        [str(ac.harness_python(root)), "-X", "utf8", "-c", ask, str(script.parent)],
        cwd=str(scratch),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        raise _Refused(
            "{} could not read the committed regeneration's write table:\n{}".format(
                label, ac._failure_tail((proc.stdout or "") + (proc.stderr or ""))
            )
        )
    return proc.stdout.splitlines()


def _pre_check(root, scope, label):
    """Refuse BY NAME any in-scope path the checkout holds uncommitted edits
    on, before the step writes anything: the install would overwrite it."""
    clash = _changed(root, scope)
    if clash:
        raise _Refused(
            "{} writes paths that carry uncommitted edits: {} - commit or set "
            "them aside, then re-run".format(label, ", ".join(clash))
        )


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


def _blobs_at(root, sha, paths):
    """`{path: its blob id in sha, or None where sha removes it}`: what the
    install is about to put in the checkout, read before it writes anything, so
    a refusal inside the install can tell its own writes from somebody's edit
    by comparing against the same ids `_blobs` reads off the disk."""
    out = _each_chunk(
        root, ("ls-tree", "-r", "-z", sha), paths, why="the commit could not be listed"
    )
    found = {}
    for entry in filter(None, out.split("\0")):
        meta, _tab, path = entry.partition("\t")
        found[path] = meta.split()[-1]
    return {p: found.get(p) for p in paths}


@contextlib.contextmanager
def _scratch(root, head, label):
    """A detached worktree at `head`, in the temporary directory, for the step
    to write in. It shares the repository's objects and refs, so the commit
    built there is trunk's to take and a branch cut from it is a real branch;
    it has its own index and files, so nothing done there reaches the checkout.
    Removed on the way out whatever happened, forced because the step leaves it
    dirty; one that will not remove is named on stderr with the command that
    removes it, since a refusal or a crash may already be on its way out."""
    path = Path(tempfile.mkdtemp(prefix="bookkeeping-"))
    code, out = _git(root, "worktree", "add", "--detach", str(path), head)
    if code != 0:
        shutil.rmtree(path, ignore_errors=True)
        raise _Refused(
            "{} could not cut its scratch worktree:\n{}".format(
                label, ac._failure_tail(out)
            )
        )
    try:
        yield path
    finally:
        code, out = _git(root, "worktree", "remove", "--force", str(path))
        if code != 0:
            print(
                "bookkeeping: {}'s scratch worktree {} would not remove - run: "
                "git worktree remove --force {}\n{}".format(
                    label, path, path, ac._failure_tail(out)
                ),
                file=sys.stderr,
            )


def _build(root, head, scope, write, message, label):
    """`(sha, written, scope)`: the scope planned, the pre-check, the step, its
    regeneration and the commit object, all against a scratch worktree cut from
    `head`. `written` is every in-scope path the step and the regeneration
    changed there; `scope` is the one plan the drift check then reads too."""
    with _scratch(root, head, label) as scratch:
        scope = _full_scope(root, scope, scratch, label)
        _pre_check(root, scope, label)
        _write_and_regenerate(root, scratch, write, label)
        written = _changed(scratch, scope)
        sha = _commit_object(root, scratch, head, written, message)
        return sha, written, scope


def _write_and_regenerate(root, scratch, write, label):
    """The step, then `trunk_step.py --regen`, both with `scratch` as their
    root, so the generators read HEAD plus the step's writes and nothing else.
    The interpreter is the checkout's harness: a `.venv` is never committed, so
    the scratch has none."""
    _raise_on(write(scratch))
    proc = subprocess.run(
        [
            str(ac.harness_python(root)),
            str(_committed_trunk_step(root, scratch)),
            "--root",
            ".",
            "--regen",
        ],
        cwd=str(scratch),
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


def _committed_trunk_step(root, scratch):
    """The `trunk_step.py` the regeneration runs: the scratch's copy, which is
    HEAD's, whenever the running kit lies inside the repository and HEAD
    carries it - so its generators, imported beside it, are HEAD's too, and an
    uncommitted edit to a generator script shapes nothing committed. A kit
    outside the repository, or one HEAD does not carry, is no committed input
    of it and runs as loaded."""
    loaded = SCRIPTS / "trunk_step.py"
    try:
        committed = scratch / loaded.resolve().relative_to(root.resolve())
    except ValueError:
        return loaded
    return committed if committed.is_file() else loaded


def _commit_object(root, scratch, head, written, message):
    """The commit object for HEAD plus exactly `written` as the scratch holds
    them, built in a TEMPORARY index. `update-index --add --remove` takes an
    addition, an edit and a deletion alike, through the repo's own clean
    filters.

    Under the loop marker this is where the loop's two trunk writers meet the
    held-status rule and the provenance trailer (SR-208, SR-209): the tree is
    named, then judged, BEFORE `commit-tree` writes anything - plumbing never
    reaches a commit hook, so the rule has to run here - and the message gains
    the `Loop-Session` trailer. A person running the claim by hand passes
    neither, because a person's commit is not the loop's. The dial is the one
    committed in `head`, the tree this commit is built on.

    Implements: SR-208, SR-209, LLR-246, LLR-248
    """
    text = _kitprovenance.with_loop_trailer(message() if callable(message) else message)
    with tempfile.TemporaryDirectory(prefix="bookkeeping-") as tmp:
        env = {"GIT_INDEX_FILE": str(Path(tmp) / "index")}
        _checked(
            scratch, "read-tree", head, why="HEAD could not seed an index", env=env
        )
        _each_chunk(
            scratch,
            ("update-index", "--add", "--remove"),
            written,
            why="the written paths could not be staged",
            env=env,
        )
        tree = _checked(
            scratch, "write-tree", why="the tree could not be named", env=env
        )
    # The dial is the one committed at `head`, the tree this commit is built
    # on, never the working file: an uncommitted owner edit is not this tree.
    _raise_on(
        ac.loop_held_status_refusal(root, root, head, tree.strip(), trunk_rev=head)
    )
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


def _drift_check(root, head, scope, label):
    """Refuse, by name, whatever moved in the checkout while the step ran:
    trunk itself, or an in-scope path - clean at the pre-check - that no longer
    equals HEAD. It runs immediately before the install, the only write this
    module makes there, and after the caller's `before_advance`, so an edit
    made while the step, its regeneration or that callback ran is named and
    left, never installed over."""
    now = _checked(
        root, "rev-parse", "--verify", "HEAD", why="HEAD could not be read"
    ).strip()
    if now != head:
        raise _Refused(
            "trunk moved from {} to {} while {} ran - re-run it on the new "
            "trunk".format(head[:10], now[:10], label)
        )
    moved = _changed(root, scope)
    if moved:
        raise _Refused(
            "{} found paths it writes edited in the checkout while it ran: {} - "
            "commit or set them aside, then re-run".format(label, ", ".join(moved))
        )


def _install(root, head, sha, installing, label):
    """Every path `installing` names takes `sha`'s copy in the checkout, index
    entry and file together (`git checkout <sha> --`), or leaves both index and
    disk where the commit removes it, then trunk moves to `sha` only if it
    still stands at `head`. The drift check has just found those paths equal to
    HEAD, so what this overwrites is HEAD's copy - save an edit landing in the
    install's own few calls, the window the module docstring states. A removed
    file's emptied directory stays, as a step writing in the checkout left it
    (`git rm` would prune it, and a caller may write there next)."""
    gone = [p for p, blob in installing.items() if blob is None]
    kept = [p for p, blob in installing.items() if blob is not None]
    if gone:
        _each_chunk(
            root,
            ("rm", "-q", "--cached", "--ignore-unmatch"),
            gone,
            why="the paths the commit removes could not be unstaged",
        )
        for rel in gone:
            try:
                (root / rel).unlink(missing_ok=True)
            except OSError as exc:
                raise _Refused("{} could not be removed: {}".format(rel, exc)) from exc
    if kept:
        _each_chunk(
            root,
            ("checkout", "-q", sha),
            kept,
            why="the commit's files could not be checked out",
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


def _restore(root, scope, refusal, label, installed):
    """Undo what the install wrote and return the refusal, saying whether the
    restore held and naming any path it left.

    `installed` is what the install meant to put in the checkout. A dirty
    in-scope path whose file no longer matches it - edited after the install
    wrote it, or dirty although the install never wrote it - is somebody else's
    edit landing in the window: its index entry goes back to HEAD, which
    touches no file, but its file is LEFT and named."""
    dirty, left = [], []
    try:
        dirty = _changed(root, scope)
        now = _blobs(root, dirty)
        left = [p for p in dirty if p not in installed or now[p] != installed[p]]
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
