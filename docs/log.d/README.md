<!--
Contracts: IF-156 — the interface seam this directory declares (process.md §8;
row of record in ../requirements/interfaces.toml).

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
    the empty directory), and a compiled fragment is deleted from here.
-->

# `docs/log.d/` — the log fragment drop-box

Session records wait here to be folded into [`../log.md`](../log.md). A work
branch never edits the log itself: it drops one fragment, and the serial trunk
step appends every committed fragment in git-derived merge order and deletes it.
That is what keeps `docs/log.md` off the merge-conflict surface — two branches
that both wrote history land two files, never two edits to one file end.
