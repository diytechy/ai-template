#!/usr/bin/env python3
"""spec_move.py — the link-aware spec-move ritual: move a registry/spec file and
keep every markdown link in the repo true, as ONE indivisible operation.

WI-393, rehoming what concurrency-restructure Phase 5 (31ad569d) deleted with
the dispatcher: WI-288 built the INBOUND half (redirect every link whose target
resolves to the moved file, by path relative to the file holding it) and WI-353
its mirror, the OUTBOUND half (re-relativise the moved file's OWN targets
against its new directory) — plus the two primitives they share. Their
docstrings said "one indivisible ritual — no caller can do part of it", and
that is the constraint this module restores: `move_spec` is the only public
write, and it performs move + rebase + redirect together, so the two-thirds
state (a moved file with stranded links) is unrepresentable for its callers.
Both defects were reproduced live after the deletion (WI-391 REVIEW-A,
2026-08-01: a bare `git mv` of a probe spec took the broken-link count from 4
to 8 — 3 outbound, 1 inbound), which is the driven evidence this row shipped
on.

THE THREE MOVES THIS RITUAL SERVES (each a real, driven instance):

  claim     `integrate.claim`: docs/work/queued/ -> docs/work/active/<branch>/
            (one directory DEEPER; broke the 2026-08-01 backlog plan's row
            links at claim time — that table is un-linked to this day);
  return    `handback.hand_back`: active/<branch>/ -> queued/ (one SHALLOWER,
            with the returned spec's text rewritten on the way — `new_text`);
  close     the worker's own terminal move (active/ -> complete|cancelled/)
            and the spec-of-record archival (docs/specs/<name>.md ->
            docs/archive/specs/<name>.<date>.md, `--archive`) — by-hand moves
            today, so the CLI below is how a closing session performs them
            without re-deriving the ritual. WI-394's close did this BY HAND
            and recorded the deviation; this module retires that deviation.

The discipline is the originals', verbatim: the link TEXT is never touched and
only the TARGET is redirected; `#fragment`s are carried; external, protocol-
relative and bare-anchor targets are left alone; a root-relative `/path` is
excused only in the REBASE half (moving the holding file cannot break it —
moving the TARGET can); and line endings ride through `newline=""` so a CRLF
checkout is not silently relaid to LF (the WI-234/WI-337 lesson). The per-link
DECISION is split out of each traversal (`_redirected_link_target` /
`_rebased_link_target`) — the C901 lesson WI-288 paid for at complexity 11.

`expected_relink` is the pure oracle of the inbound half: what a file WOULD say
after the redirect. `integrate._abandoned_claim` uses it to recognise the
relink writes inside a crashed claim's one commit without loosening its
conviction to "any .md edit".

Stdlib only; Windows+POSIX (all link math is `posixpath`, I/O is `pathlib`).

Usage (from the repo root):
    python scripts/spec_move.py --root . SRC DEST
    python scripts/spec_move.py --root . --archive docs/specs/WI-123.md \\
        [--date 2026-08-01]
"""

from __future__ import annotations

import argparse
import datetime
import posixpath
import re
import sys
from pathlib import Path

import agent_common as ac

# Inline markdown link target, e.g. `](specs/WI-1.md)` — no whitespace inside the
# target, which is this repo's convention and keeps titled links (`](p "T")`) out
# of the rewrite rather than risking mangling them (WI-288).
_MD_LINK_TARGET_RE = re.compile(r"(\]\()([^)\s]+)(\))")
_URL_SCHEME_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)

ARCHIVE_DIR = "docs/archive/specs"


def _resolvable_link(target, skip_absolute=False):
    """`(base, sep, frag)` for a link target worth rewriting, or None to leave it.

    The shared "is this even a repo-relative path?" test both halves of the
    ritual run before they decide anything. A bare `#fragment` and any
    scheme-ish or protocol-relative URL are never rewritten — an external link
    that merely CONTAINS a moved path must survive intact. `skip_absolute`
    additionally excuses a root-relative `/path`, which resolves independently
    of the holding directory and therefore cannot be broken by moving the file
    (it CAN be broken by moving the target, so only the rebase half sets it)."""
    if target.startswith("#") or _URL_SCHEME_RE.match(target):
        return None
    if skip_absolute and target.startswith("/"):
        return None
    base, sep, frag = target.partition("#")
    return (base, sep, frag) if base else None


def _redirected_link_target(target, doc_dir, remap):
    """The rewritten target for ONE inline markdown link, or None to leave it
    alone (WI-288). Split out of the traversal so each half stays under the
    C901 ratchet — the per-link decision is the branchy part.

    `doc_dir` is the posix directory of the file holding the link, so the
    target resolves the way a reader's browser would. Left alone: a bare
    `#fragment`, any scheme-ish or protocol-relative URL, and anything whose
    resolved path is not in `remap`. A `#fragment` on a redirected link is
    carried over."""
    parts = _resolvable_link(target)
    if parts is None:
        return None
    base, sep, frag = parts
    dest = remap.get(posixpath.normpath(posixpath.join(doc_dir, base)))
    if dest is None:
        return None
    return posixpath.relpath(dest, doc_dir or ".") + sep + frag


def _rebased_link_target(target, old_dir, new_dir):
    """The rewritten target for ONE link inside a file that MOVED, or None to
    leave it alone (WI-353).

    The mirror of `_redirected_link_target`. That one asks "did this link's
    TARGET move?"; this one asks "did the file HOLDING it move?" — and the two
    cannot be one function, because their answers come from opposite ends. The
    loop over inbound links structurally cannot catch these: it rewrites a link
    whose target resolves to a moved SOURCE, and here the targets did not move
    at all, the document did.

    Same exclusions as its mirror plus the root-relative one (see
    `_resolvable_link`). Everything else is resolved against the OLD directory
    and re-relativised against the NEW one; the `#fragment` and the link TEXT
    survive untouched."""
    parts = _resolvable_link(target, skip_absolute=True)
    if parts is None:
        return None
    base, sep, frag = parts
    resolved = posixpath.normpath(posixpath.join(old_dir, base))
    new = posixpath.relpath(resolved, new_dir or ".")
    if new == base:
        return None
    return new + sep + frag


def rewrite_text(text, rewrite_target):
    """`text` with `rewrite_target(target) -> new|None` applied to every inline
    markdown link target — the pure core both halves and the `expected_relink`
    oracle share. A None decision leaves the link byte-identical."""

    def _sub(match):
        new = rewrite_target(match.group(2))
        return match.group(0) if new is None else match.group(1) + new + match.group(3)

    return _MD_LINK_TARGET_RE.sub(_sub, text)


def _rewrite_md_links(path, rewrite_target):
    """Apply `rewrite_target` to every inline markdown link in `path`; True when
    the file changed.

    The traversal primitive both halves share (WI-353): only the per-link
    DECISION differs between them — did this link's target move, or did the
    file holding it? — so the "leave it alone" contract (a None decision) and
    the I/O discipline live here once.

    Line endings are preserved (read and write with `newline=""`) so a CRLF
    checkout is not silently rewritten to LF — the WI-234 splice discipline.
    Any unreadable/unwritable or non-UTF-8 file is skipped rather than raised
    on: this runs over a whole worktree, where one odd file must not abort the
    ritual."""
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError):
        return False
    new_text = rewrite_text(text, rewrite_target)
    if new_text == text:
        return False
    try:
        with path.open("w", encoding="utf-8", newline="") as fh:
            fh.write(new_text)
    except OSError:
        return False
    return True


def _rebase_moved_spec_links(root, moves):
    """Re-relativise each moved file's OWN relative links (WI-353).

    WI-288 made archival link-aware in one direction only, so a link-rich spec
    was stranded by its own move: `docs/specs/` to `docs/archive/specs/` is one
    directory deeper, and every `](../log.md)` inside it then resolves one
    short — demonstrated 2026-07-28 archiving WI-328's spec by hand
    (`check_docs` went from OK to SIX broken links on the spot) and again by
    WI-391 REVIEW-A after the machinery died. Runs on the destination file,
    after the move. Returns the destination paths rewritten."""
    touched = []
    for src, dest in moves:
        old_dir = posixpath.dirname(src)
        new_dir = posixpath.dirname(dest)
        if old_dir == new_dir:
            continue
        changed = _rewrite_md_links(
            Path(root) / dest,
            lambda target, _old=old_dir, _new=new_dir: _rebased_link_target(
                target, _old, _new
            ),
        )
        if changed:
            touched.append(dest)
    return touched


def _relink_inbound_links(root, moves):
    """Redirect inbound markdown links to files the ritual just moved (WI-288's
    `_relink_archived_specs`, generalised to any spec move). Without this, a
    move strands a DANGLING link: a train whose own `docs/log.md` entry links
    its live spec breaks the moment the spec moves, and the break surfaces on
    the composed tree as a red `check_docs` — after the work is done.

    Resolution is by PATH, not by pattern: each link target is resolved
    relative to the file containing it and compared against the moved source,
    so `](specs/WI-n.md)` from `docs/log.md`, `](docs/specs/WI-n.md)` from the
    root, and `](../specs/WI-n.md)` from `docs/reviews/` are all caught by one
    rule instead of three regexes. The replacement is re-relativised to the
    linking file's own directory; the link TEXT is untouched and any
    `#fragment` survives. Returns the repo-relative paths rewritten."""
    if not moves:
        return []
    remap = {src: dest for src, dest in moves}
    root = Path(root)
    touched = []
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if ".git" in parts or "node_modules" in parts:
            continue
        rel = path.relative_to(root).as_posix()
        doc_dir = posixpath.dirname(rel)
        changed = _rewrite_md_links(
            path,
            lambda target, _dir=doc_dir: _redirected_link_target(target, _dir, remap),
        )
        if changed:
            touched.append(rel)
    return touched


def expected_relink(text, doc_dir, remap):
    """What `text` (held at posix directory `doc_dir`) WOULD say after the
    inbound redirect for `remap` — the pure oracle of that half.

    `integrate._abandoned_claim` compares a crashed claim commit's .md
    modifications against this to convict or excuse them: a byte-exact match is
    the claim's own relink write; anything else is somebody's work and the
    branch is a collision, not an orphan to delete."""
    return rewrite_text(
        text, lambda target: _redirected_link_target(target, doc_dir, remap)
    )


def _place_moved_file(root, src_rel, dest_rel, new_text):
    """The move itself: `git mv` (staged, the caller's history keeps a rename)
    with a plain rename as the fallback for an untracked file or a non-repo
    tree — or, with `new_text`, a rewrite-on-the-way move (write the new text
    at the destination, remove the source) for callers like the handback whose
    return changes the spec's own content. A refusal string or None.

    Both arms end by `git add`ing the destination, and for the `git mv` arm
    that add is THE FIX for this module's first field defect (WI-408): `git mv`
    moves the working-tree file but stages the rename from the INDEX blob, so
    a source carrying unstaged edits — a worker who has just filled the spec's
    `## Deliverable` and then runs the close move — had those edits silently
    dropped from the staged copy (WI-401's close, 2026-08-02; caught only
    because rename-similarity read 100% where the edit should have lowered
    it). Re-adding the destination stages its WORKING-TREE content, so an
    unstaged edit rides the move instead of vanishing."""
    src = Path(root) / src_rel
    dest = Path(root) / dest_rel
    if new_text is None:
        code, _out = ac.git(root, "mv", src_rel, dest_rel)
        if code != 0:
            try:
                src.replace(dest)
            except OSError as exc:
                return "cannot move {} -> {}: {}".format(src_rel, dest_rel, exc)
    else:
        try:
            with dest.open("w", encoding="utf-8", newline="") as fh:
                fh.write(new_text)
        except OSError as exc:
            return "cannot write {}: {}".format(dest_rel, exc)
        code, _out = ac.git(root, "rm", "-q", "--", src_rel)
        if code != 0:
            try:
                src.unlink()
            except OSError as exc:
                return "cannot remove the moved source {}: {}".format(src_rel, exc)
    ac.git(root, "add", "--", dest_rel)
    return None


def move_spec(root, src_rel, dest_rel, *, new_text=None):
    """THE RITUAL — move `src_rel` to `dest_rel` and keep every repo link true,
    indivisibly: `(rewritten repo-relative paths, None)` or `(None, refusal)`.

    Moving the file is only a THIRD of the operation, and all three run here so
    no caller can do part of it (the WI-288/WI-353 contract, restored):
    `_rebase_moved_spec_links` re-relativises the moved file's OWN outbound
    links — it changed directory depth, so every `](../x)` inside it would
    otherwise resolve wrong — and `_relink_inbound_links` redirects every
    INBOUND link to the new path, because a log entry commonly links the spec
    it discusses. The two are mirrors and neither implies the other: one asks
    whether a link's TARGET moved, the other whether the file HOLDING it did.
    The rebase reads the destination, so it runs after the move.

    Every rewritten file is `git add`ed (a no-op outside a repo), so the whole
    ritual lands in the caller's next commit as one changeset — never a staged
    move with dirty relink residue beside it."""
    root = Path(root)
    src_rel = str(src_rel).replace("\\", "/")
    dest_rel = str(dest_rel).replace("\\", "/")
    if not (root / src_rel).is_file():
        return None, "no file to move at {}".format(src_rel)
    # A DESTINATION THAT MEANS A DIRECTORY GETS THE SOURCE'S FILENAME APPENDED —
    # a trailing slash, or a path that already IS a directory. The 2026-08-21
    # review (Sol 8) measured the alternative: invoked with a lane directory
    # (`docs/work/active/wi448-common-module/`), the trailing slash was
    # normalized away and this function wrote a FILE named like the lane, so the
    # spec vanished from registry discovery — and if no predecessor referenced
    # the row, nothing fired at all. Directory intent is the ONE ambiguity worth
    # resolving rather than refusing, because it is what a caller naturally
    # types for a state-is-the-directory registry.
    if not dest_rel.strip("/ ") or dest_rel.startswith("/"):
        return None, (
            "the destination {!r} is not a repo-relative path to a file or lane".format(
                dest_rel
            )
        )
    if dest_rel.endswith("/") or (root / dest_rel).is_dir():
        if not dest_rel.endswith("/"):
            dest_rel += "/"
        dest_rel += posixpath.basename(src_rel)
    if dest_rel.endswith("/") or not posixpath.basename(dest_rel):
        return None, "the destination {!r} names no file".format(dest_rel)
    if (root / dest_rel).exists():
        return None, "the destination {} already exists".format(dest_rel)
    (root / dest_rel).parent.mkdir(parents=True, exist_ok=True)
    refusal = _place_moved_file(root, src_rel, dest_rel, new_text)
    if refusal:
        return None, refusal
    moves = [(src_rel, dest_rel)]
    touched = set(_rebase_moved_spec_links(root, moves))
    touched.update(_relink_inbound_links(root, moves))
    for rel in sorted(touched):
        ac.git(root, "add", "--", rel)
    return sorted(touched), None


def archive_dest(src_rel, stamp):
    """The spec-of-record archival destination for `src_rel` (the
    docs/specs/README.md close-ritual): `docs/archive/specs/<stem>.<stamp>.md`
    — the close date appended so no live plan file can re-grow onto the working
    surface. Pure of clocks; the caller supplies `stamp` (YYYY-MM-DD)."""
    stem = posixpath.basename(str(src_rel).replace("\\", "/"))
    if stem.endswith(".md"):
        stem = stem[: -len(".md")]
    return "{}/{}.{}.md".format(ARCHIVE_DIR, stem, stamp)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("src", help="repo-relative path of the file to move")
    ap.add_argument("dest", nargs="?", help="repo-relative destination path")
    ap.add_argument(
        "--archive",
        action="store_true",
        help="derive the destination: docs/archive/specs/<stem>.<date>.md",
    )
    ap.add_argument(
        "--date",
        default=None,
        help="the archival date stamp (YYYY-MM-DD; default: today)",
    )
    args = ap.parse_args(argv)
    if bool(args.dest) == bool(args.archive):
        ap.error("give exactly one of DEST or --archive")
    root = Path(args.root).resolve()
    dest = args.dest
    if args.archive:
        dest = archive_dest(args.src, args.date or datetime.date.today().isoformat())
    touched, refusal = move_spec(root, args.src, dest)
    if refusal:
        print("spec_move: REFUSED - {}".format(refusal), file=sys.stderr)
        return 1
    print("spec_move: {} -> {}".format(args.src, dest))
    for rel in touched:
        print("spec_move: relinked {}".format(rel))
    return 0


if __name__ == "__main__":
    sys.exit(main())
