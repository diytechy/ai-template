#!/usr/bin/env python3
"""adoption_record.py - only the close writes a disposition's adoption record
(WI-969, carrying WI-902's spec of record).

WHY THIS EXISTS. A disposition row may adopt an already-filed successor
instead of drafting one (`kitlib.adoption`). The close validates the adoption
once, in the tree its closing commit is made on, and writes the validated ids
into the closed spec's `adopted` cell, the record; the sweep then trusts that
record and re-points from it without re-validating. A record the sweep trusts
is authority, so a record anyone else writes must never land. This module
holds both halves of that bargain:

  * validation at a named revision (`validate_at` over `tree_specs`), which
    `handback.close_adjudication` runs on the lane's HEAD before it moves
    anything, and which the commit rule re-runs on the closing commit's
    parent, so both bind the record to the same tree;
  * the per-commit rule (`commit_adoption_record_lines`), which admits a
    record change only in the machinery's own close, its record equal to its
    request and valid in its parent's tree, or carried unchanged with its
    request, and a merge by what neither parent carried; it rides the lane-commit walk at the merge
    slot and runs as the pre-commit hook's `adoption-record` step (`main`).

THE CLOSE TEST is the shared close shape (`kitlib.verdict.mechanical_close`)
read with `spec_move.exact_relink` injected: the peel's shape, except that a
changed path outside `docs/work/` is admitted when it is exactly the inbound
relink of the commit's own moves (a review drawn while the row was in
`active/` links it, and the close's move rewrites that link). The peel reads
the same shape with no oracle, so such a close is admitted here and still not
peeled. A record refusal carries this rule's own remedy, never text then
act's.

THE SQUASH LANDING. The hook step owns its squash handling: when git's
`SQUASH_MSG` names a lane tip that contains HEAD, each lane commit HEAD..tip
is judged by this rule (so the lane's close meets the same close test as at
the slot), and a staged spec equal to the tip's own is carried; any other
staged record change is judged like any commit's. Text then act's squash
exemption is keyed to the approval-act registries, so it is not borrowed.

Contracts: IF-303, IF-304 - the seams this module declares (process.md §8;
rows of record in docs/requirements/interfaces.toml).

Contract IF-303: the adoption record, as calls the close and the lane-commit
    walk make. `tree_specs(root, rev)` lists the work specs in the tree of
    `rev` as `(relpath, read)` entries, `read()` the spec's strict UTF-8
    text; `validate_at(root, rev, title, owes, adoptions)` returns
    `(record, refusal)`, the record the request's validated ids in block
    order, validated in the tree of `rev`; `commit_adoption_record_lines(root,
    rev)` returns one refusal line per record change the commit `rev` makes
    against its parents that only the close may make, `[]` when it makes
    none. The owner reads named git trees and writes nothing.

Contract IF-304: the adoption-record step, as a command.
    `adoption_record.py [--root <dir>]` judges the commit being made in the
    checkout at `<dir>` (default: the working directory): the index against
    HEAD, and against MERGE_HEAD while a merge is in progress, and, on a
    squash landing, each lane commit it carries. It prints one step line,
    `FAIL` with each refusal or `ok`, and exits 1 when any record change is
    refused, else 0. It writes nothing. `check.py` runs it as the built-in
    `adoption-record` step.

Usage:
    python scripts/adoption_record.py [--root DIR]

exits 0 when the staged commit changes no adoption record it may not, 1
naming each refusal (the pre-commit hook's `adoption-record` step).
"""

import argparse
import functools
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from acceptance_record import _commit_parents  # noqa: E402  (path set above)
from kitlib import adoption as _kadoption  # noqa: E402
from kitlib import git as _kitgit  # noqa: E402
from kitlib import registry as _kregistry  # noqa: E402
from kitlib import verdict as _kverdict  # noqa: E402
from kitlib.config import utf8_console  # noqa: E402

#: The work root, from the repository root; every listed spec's relpath is
#: taken from it, the form `kitlib.adoption.row_refusal` judges.
WORK = "docs/work"
#: Both spec roots the commit rule reads: the work root and its archive.
SPEC_ROOTS = (WORK, "docs/archive/work")
#: A spec path under either root: its state folder (`active/` one level
#: deeper, under its branch) and the WI id its file name leads with.
_SPEC_PATH = re.compile(
    r"^docs/(?:archive/)?work/([^/]+)/(?:[^/]+/)?(WI-\d+)-[^/]*\.md$"
)
#: The terminal folder a requesting spec may enter only with its record.
_COMPLETE = "complete"
#: What a refused record change is told to do instead.
REMEDY = (
    "only `handback.close_adjudication` writes the record; close the row through it"
)
#: Appended when a squash in progress was not admitted as one.
SQUASH_HINT = (
    "a squash is judged by its lane commits only when the lane tip contains "
    "HEAD: rebase the lane onto trunk first"
)


def tree_specs(root, rev):
    """`[(relpath, read)]` of every work spec in the tree of `rev`, `relpath`
    from the work root and `read()` its strict UTF-8, LF-normalised text.
    Raises OSError naming the tree when git cannot list it: an unavailable
    listing is a refusal, never an empty registry.

    Implements: SR-148, LLR-335
    """
    listing = _kitgit.git_paths(root, ["ls-tree", "-r", "--name-only", rev, "--", WORK])
    if listing is None:
        raise OSError(
            "the registry cannot be loaded: git cannot list {} at {}".format(WORK, rev)
        )
    prefix = WORK + "/"
    return [
        (path[len(prefix) :], functools.partial(_tree_text, root, rev, path))
        for path in listing
        if path.startswith(prefix)
        and "/" in path[len(prefix) :]
        and path.rsplit("/", 1)[-1].startswith("WI-")
        and path.endswith(".md")
    ]


def _tree_text(root, rev, path):
    """The text of `path` in the tree of `rev`, its bytes decoded as strict
    UTF-8 with line endings normalised to LF (an undecodable spec is
    unreadable, never replacement-character text); raises OSError when git
    cannot show it, UnicodeDecodeError when it is not UTF-8.

    Implements: SR-148, LLR-335
    """
    data = _kitgit.git_bytes(root, ["show", "{}:{}".format(rev, path)])
    if data is None:
        raise OSError("git cannot show {} at {}".format(path, rev))
    return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


def validate_at(root, rev, title, owes, adoptions):
    """`(record, refusal)`: the request's adopted ids, in block order,
    validated in the tree of `rev` against the row the title disposes
    (`owes`: whether the title is a disposition row's at all). No adoptions
    answers `(None, None)`: there is no record to write. Each adopted id must
    be accepted by `kitlib.adoption.row_refusal` over one listing of that
    tree; the first refusal is returned, with no record.

    Implements: SR-148, LLR-335
    """
    if not adoptions:
        return None, None
    disposed, refusal = _kadoption.disposed_id(title, owes)
    if refusal:
        return None, refusal
    try:
        specs = tree_specs(root, rev)
    except OSError as exc:
        return None, "adopts {} but {}".format(", ".join(adoptions), exc)
    for adopted in adoptions:
        refusal = _kadoption.row_refusal(specs, adopted, disposed)
        if refusal:
            return None, refusal
    return tuple(adoptions), None


def commit_adoption_record_lines(root, rev):
    """One line per record change the commit `rev` makes against its parents
    that only the close may make; `[]` when it makes none.

    The parents are read off the commit object (`_commit_parents`), and a
    parent the repository cannot read is one line naming it, never a root. A
    commit touching no spec under either spec root costs no further read. A
    touched spec's record is judged by `kitlib.adoption.record_change`, the
    close being `kitlib.verdict.mechanical_close` read with
    `spec_move.exact_relink` and validated in its parent's tree
    (`validate_at`), the tree the close validated in. A merge is judged by
    what neither parent carried.

    Implements: SR-148, LLR-345
    """
    question = "it changes an adoption record only the close may write"
    parents, unread = _commit_parents(root, rev, question)
    if unread or not parents:
        return unread
    lines = _record_lines(root, parents, rev, _commit_close(root, rev))
    return ["commit {}: {}".format(rev[:10], line) for line in lines]


def _commit_close(root, rev):
    """`close(wi, data, request) -> (close, invalid)` for the commit `rev`:
    whether `rev` is the machinery's close of `wi` (the shared close shape,
    its exact relinks admitted), and the request's validation in its parent's
    tree. The shape is read once, on the first ask.

    Implements: SR-148, LLR-345
    """

    @functools.lru_cache(maxsize=None)
    def shape():
        import spec_move  # the shared byte-exact relink; deferred until a record moves

        return _kverdict.mechanical_close(root, rev, relinked=spec_move.exact_relink)

    def close(wi, data, request):
        import intake  # the owed-successor reading's home; deferred

        closed = shape()
        if not closed or wi not in closed[1]:
            return False, None
        title, owes = data.get("title"), intake.owes_successor(data)
        return True, validate_at(root, closed[0], title, owes, request)[1]

    return close


def _not_a_close(_wi, _data, _request):
    """The staged form's close: never one, since the close commits with the
    hook skipped.

    Implements: SR-148, LLR-345
    """
    return False, None


def _record_lines(root, bases, head, close):
    """One line per spec whose record the tree `head` (None: the index)
    changes against `bases` as only the close may, each naming the spec and
    carrying `REMEDY`. A spec counts as touched only when it differs from
    every base, so a merge is judged by what neither parent carried. A diff,
    a listing or a spec git cannot read is a line, never a skip.

    Implements: SR-148, LLR-345
    """
    touched, unread = _touched_ids(root, bases, head)
    if unread or not touched:
        return unread
    try:
        now = _spec_paths(root, head)
        sides = [_spec_paths(root, base) for base in bases]
    except OSError as exc:
        return [str(exc)]
    lines = []
    for wi in sorted(touched):
        refusal = _spec_refusal(root, bases, head, wi, (now, sides), close)
        if refusal:
            lines.append("{}: {}; {}".format(wi, refusal, REMEDY))
    return lines


def _touched_ids(root, bases, head):
    """`(ids, lines)`: the WI ids of the specs under either spec root that the
    tree `head` (None: the index) changes against every base, and a line when
    a diff cannot be read.

    Implements: SR-148, LLR-345
    """
    common = None
    for base in bases:
        args = ["diff", "--name-only", "--no-renames"]
        args += ["--cached", base] if head is None else [base, head]
        paths = _kitgit.git_paths(root, args + ["--", *SPEC_ROOTS])
        if paths is None:
            return set(), [
                "cannot read the diff against {}, so whether it changes an "
                "adoption record is unknown".format(base)
            ]
        common = set(paths) if common is None else common & set(paths)
    return {m.group(2) for m in map(_SPEC_PATH.match, common or ()) if m}, []


def _spec_paths(root, rev):
    """`{wi: [path]}` of the specs under either spec root in the tree `rev`
    (None: the index); raises OSError naming the tree git cannot list.

    Implements: SR-148, LLR-345
    """
    args = ["ls-files"] if rev is None else ["ls-tree", "-r", "--name-only", rev]
    listing = _kitgit.git_paths(root, args + ["--", *SPEC_ROOTS])
    if listing is None:
        raise OSError("git cannot list the specs at {}".format(rev or "the index"))
    found = {}
    for path in listing:
        match = _SPEC_PATH.match(path)
        if match:
            found.setdefault(match.group(2), []).append(path)
    return found


def _spec_refusal(root, bases, head, wi, listings, close):
    """The refusal for spec `wi`'s record across the tree `head` against
    `bases` (`listings`: the `_spec_paths` of `head` and of each base), or
    None. The tree `head` is read strictly and each base through
    `_base_spec`. The request is read when the tree holds a record, the record
    changed or the spec moved into a `complete/` folder, and the close asked
    only when the record changed.

    Implements: SR-148, LLR-345
    """
    now, sides = listings
    try:
        record, path, data, text = _spec_at(root, head, now.get(wi, []))
        olds = [_base_spec(root, b, s.get(wi, [])) for b, s in zip(bases, sides)]
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        return str(exc)
    parents = [old[0] for old in olds]
    moved = _in_complete(path) and not any(_in_complete(old[1]) for old in olds)
    changed = record not in parents and not (record is None and not any(parents))
    if not (moved or changed or record):
        return None
    _drafts, request, refusal = _parse_request(text, path)
    if refusal:
        return refusal
    is_close, invalid = close(wi, data, request) if changed else (False, None)
    held = [(old[0], _carried_request(old, record)) for old in olds]
    return _kadoption.record_change(held, record, request, moved, is_close, invalid)


def _carried_request(old, record):
    """The request a base's spec `old` (`_spec_at`'s tuple) holds when it
    carries `record`, read through the one parser; None when it carries
    another record or its section does not parse (so it carries no request).

    Implements: SR-148, LLR-345
    """
    if not record or old[0] != record:
        return None
    _drafts, request, refusal = _parse_request(old[3], old[1])
    return None if refusal else request


def _parse_request(text, path):
    """`(drafts, adoptions, refusal)` of the spec text's `## Dispositions`
    section, through the one parser; a spec absent from the tree requests
    nothing.

    Implements: SR-148, LLR-345
    """
    if text is None:
        return [], [], None
    import intake  # the one disposition parser's home; deferred

    return intake.parse_disposition_section(text, path)


def _base_spec(root, rev, paths):
    """`_spec_at` for a base: a spec whose text, front matter or record a
    base holds malformed held no readable record (the tree under judgement
    is read strictly, so a record cannot hide behind a malformed base, and a
    commit repairing a malformed spec is not refused for its parent). A spec
    git cannot show still raises OSError.

    Implements: SR-148, LLR-345
    """
    try:
        return _spec_at(root, rev, paths)
    except (ValueError, UnicodeDecodeError):
        return None, next(iter(paths), None), {}, None


def _spec_at(root, rev, paths):
    """`(record, path, front matter, text)` of the one spec `paths` names in
    the tree `rev` (None: the index); all None when the tree holds none.
    Raises ValueError when several specs carry the id or the record is
    malformed, OSError or UnicodeDecodeError when the spec cannot be read.

    Implements: SR-148, LLR-345
    """
    if not paths:
        return None, None, {}, None
    if len(paths) > 1:
        raise ValueError("{} specs carry one id: {}".format(len(paths), paths))
    (path,) = paths
    data = _kitgit.git_bytes(root, ["show", "{}:{}".format(rev or "", path)])
    if data is None:
        raise OSError("git cannot show {} at {}".format(path, rev or "the index"))
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    meta, _body = _kregistry.parse_spec_frontmatter(text, path)
    record, refusal = _kadoption.record_ids(meta, path)
    if refusal:
        raise ValueError(refusal)
    return record, path, meta, text


def _in_complete(path):
    """Whether `path` stands in a `complete/` folder of either spec root.

    Implements: SR-148, LLR-345
    """
    match = _SPEC_PATH.match(path or "")
    return bool(match) and match.group(1) == _COMPLETE


def staged_adoption_record_lines(root):
    """`commit_adoption_record_lines` for the commit being made: the index
    against HEAD, and against MERGE_HEAD while a merge is in progress. Before
    the first commit nothing is judged.

    A SQUASH LANDING (git's `SQUASH_MSG`, read by `kitlib.git.squash_commits`)
    whose tip contains HEAD is judged by its lane commits: each commit
    HEAD..tip is judged by this rule (`_squash_walk`), and the index is
    judged against the tip too, so a staged spec equal to the tip's own is
    carried and any other staged record change is refused. A squash whose tip
    does not contain HEAD is judged like any commit, its refusal ending with
    `SQUASH_HINT`.

    Implements: SR-148, LLR-345
    """
    head = (
        _kitgit.git_out(root, ["rev-parse", "--verify", "--quiet", "HEAD"]) or ""
    ).strip()
    if not head:
        return []
    merging = (
        _kitgit.git_out(root, ["rev-parse", "-q", "--verify", "MERGE_HEAD"]) or ""
    ).strip()
    if merging:
        return _record_lines(root, [head, merging], None, _not_a_close)
    squashed = _kitgit.squash_commits(root)
    tip = squashed[0] if squashed else None
    within = (
        tip and _kitgit.git_out(root, ["merge-base", "--is-ancestor", head, tip]) == ""
    )
    if not within:
        lines = _record_lines(root, [head], None, _not_a_close)
        return lines + [SQUASH_HINT] if lines and squashed else lines
    walked = _squash_walk(root, head, tip)
    return walked + _record_lines(root, [head, tip], None, _not_a_close)


def _squash_walk(root, head, tip):
    """The lines of every commit `head..tip`, oldest first, each judged by
    `commit_adoption_record_lines` against its own parents, as the merge
    slot's lane-commit walk judges it with this rule as a rider; a line when
    git cannot list the range. The commits are walked here, not through
    `text_then_act.lane_commit_walk`, because that module imports this one
    for `LANE_COMMIT_RIDERS`, and the import graph admits no cycle.

    Implements: SR-148, LLR-345
    """
    commits = _kitgit.git_out(root, ["rev-list", "--reverse", head + ".." + tip])
    if commits is None:
        return ["cannot list the squashed commits {}..{}".format(head[:10], tip[:10])]
    return [
        line
        for rev in commits.split()
        for line in commit_adoption_record_lines(root, rev)
    ]


def main(argv=None):
    """The pre-commit hook's `adoption-record` step: exit 1 naming each
    refused record change, 0 when the staged commit makes none. Off a git
    work tree there is no commit to judge.

    Implements: SR-148, LLR-345
    """
    utf8_console()
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--root", default=".", help="the checkout (default: cwd)")
    args = ap.parse_args(argv)
    inside = _kitgit.git_out(args.root, ["rev-parse", "--is-inside-work-tree"])
    lines = staged_adoption_record_lines(args.root) if inside is not None else []
    msg = "\n".join(lines) or (
        "no staged commit changes an adoption record only the close may write"
    )
    print("  {:5} adoption-record  {}".format("FAIL" if lines else "ok", msg))
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main())
