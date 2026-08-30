<!--
Contracts: IF-156, IF-168 — the interface seams this directory declares
(process.md §8; rows of record in ../requirements/interfaces.toml).

Contract IF-156: the log fragment drop-box. One `*.md` file per session named
    `<id>-<slug>.md` — a nonempty slug is what makes the name unique, and a
    unique name is what makes the medium conflict-free across parallel
    branches. A fragment must open with a `## ` heading of its own and may not
    claim one of `docs/log.md`'s reserved section headings (`## Sittings`,
    `## Decisions log`, `## Audit log`), and it must be COMMITTED: order is
    read from the commit that ADDED each file, oldest first with the filename
    breaking ties, so an uncommitted fragment has no position. Links are
    written relative to THIS directory and are rebased one level up as the
    fragment lands in `docs/log.md`; anchors, URLs and root-absolute targets
    are left exactly as written. Dotfiles are not fragments (`.gitkeep` holds
    the empty directory).
Contract IF-168: what MUTATES this drop-box, and there are exactly two acts.
    A session ADDS one file under the fragment grammar and touches no other:
    the unique name is what keeps the medium conflict-free across parallel
    branches, so a branch's only write here is its own. `trunk_step.py
    --compile-log` REMOVES each fragment it compiled — the unlink runs in the
    working tree once every ordered fragment has been appended, all-or-nothing
    with the append, and the caller stages and commits the deletion; the step
    itself never commits. A refused compile writes nothing and leaves every
    fragment on disk, `--dry-run` names what it would fold and deletes
    nothing, and dotfiles and `README.md` are outside the fragment set and are
    never removed.
-->

# `docs/log.d/` — the log fragment drop-box

Session records wait here to be folded into [`../log.md`](../log.md). A work
branch never edits the log itself: it drops one fragment, and the serial trunk
step appends every committed fragment in git-derived merge order and deletes it.
That is what keeps `docs/log.md` off the merge-conflict surface — two branches
that both wrote history land two files, never two edits to one file end.
