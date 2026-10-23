"""TEXT THEN ACT — the spine text before the approval act (WI-806).

OI-101 Q2, amended for landings by the owner's README Q-8 answer: a commit that
writes the approval record changes, as its own, no cell of an approval-act row
but `Status` and adds or removes no row (`text_then_act_lines`), so
amend-plus-flip is no longer approval. The hook asks it of the staged tree
(`staged_text_then_act_lines`, a squash landing judged by the commits it folds
in) and the merge slot of each lane commit (`commit_text_then_act_lines`).

A separate judgement from the acceptance record's, moved here whole and
unchanged by WI-892. It reads that module's approval-act registries, record
directory and row reader, and shares `acceptance_record._commit_parents`, the
ruling sync's parent reader, which stays there as its one home.

THE LANE-COMMIT WALK. `lane_commit_walk` is the one walk the hook's squash
path and the merge slot's per-lane-commit rungs share: each listed lane
commit, oldest first, judged against its own parents by each rider in turn.
`LANE_COMMIT_RIDERS` is the tuple of per-commit rules that ride it, text then
act first; the merge slot's ruling sync rides the same walk with its own
judge. Each caller lists the range, because what an unlistable range means
differs: the hook reads it as no squash to exempt, and the slot refuses the
lane in git's own words.
"""

from pathlib import PurePosixPath

# What this rule reads of the acceptance record: the approval-act registries,
# the record directory, a registry's rows at one tree, and the parent reader.
try:
    import adoption_record
    import spine_carrier
    from acceptance_record import (
        APPROVAL_ACT_CSVS,
        SNAPSHOT_DIR,
        _commit_parents,
        _spine_rows_at,
        commit_parent_first_lines,
    )
    from kitlib import git as _kitgit
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adoption_record
    import spine_carrier
    from acceptance_record import (
        APPROVAL_ACT_CSVS,
        SNAPSHOT_DIR,
        _commit_parents,
        _spine_rows_at,
        commit_parent_first_lines,
    )
    from kitlib import git as _kitgit

# The kit's one `git, or None` read, and a tier's carriers, as the acceptance
# record aliases them.
_git = _kitgit.git_out
_tier_carriers = spine_carrier.tier_carriers


# --- TEXT THEN ACT: the spine text before the approval act (WI-806) ----------
# OI-101 Q2 (risk 6), its trunk scope amended for landings by the owner's README
# Q-8 answer, 2026-10-04: a commit that writes under `SNAPSHOT_DIR` changes, as
# its own, no cell of an `APPROVAL_ACT_CSVS` row except `Status`, and adds or
# removes no such row. The text is committed first; the act (the flips, the
# copy, the ledger and the views) second, so every byte a copy blesses was
# committed, and readable, before the commit that blesses it. Flips and their
# copy stay ONE commit (SR-140): that is the act. One function over two trees,
# asked by the pre-commit hook of the staged tree and by the merge slot of each
# lane commit, so a `--no-verify` commit is still refused before it lands.
TEXT_THEN_ACT_REMEDY = (
    "commit the text on its own first, then take the act (the `Status` flips, "
    "`intake.py snapshot` and the views it regenerates) as a second commit that "
    "changes no other spine cell and adds or removes no row"
)
SQUASH_REBASE_HINT = (
    "a squash is exempt only of a lane tip that contains HEAD, its spine and "
    "record staged as the tip's: rebase the lane onto trunk first"
)


def _text_changes(root, bases, head):
    """`{(registry, row id, what)}` the tree `head` (None: the index) writes in
    the approval-act tiers as its OWN against `bases`, its parents: `what` is a
    cell, `Status` and the id excepted, whose value differs from its value in
    EVERY parent, or `added` / `removed` for a row whose presence differs from
    every parent. Values are compared, never per-parent change labels, so a row
    only one parent carried is judged by its cells. Keyed on the registry
    constant, so the two sides of a carrier change still join.

    Implements: SR-140, LLR-302
    """
    new_prefix = ":" if head is None else head + ":"
    out = set()
    for rel, id_col in APPROVAL_ACT_CSVS:
        now = _spine_rows_at(root, new_prefix, rel, id_col)
        sides = [_spine_rows_at(root, base + ":", rel, id_col) for base in bases]
        for rid in set(now).union(*sides):
            moves = _row_text_moves(rid, now, sides, id_col)
            out |= {(rel, rid, what) for what in moves}
    return out


def _row_text_moves(rid, now, sides, id_col):
    """What row `rid` of `now` holds that no side in `sides` holds: `added` or
    `removed` when its presence differs from every side, else each cell whose
    value differs from every side's (a side without the row holds no value).

    Implements: SR-140, LLR-302
    """
    row = now.get(rid)
    if all((rid in side) != (row is not None) for side in sides):
        return ["added" if row is not None else "removed"]
    if row is None:
        return []
    cells = set(row).union(*(side.get(rid, {}) for side in sides))
    return [
        c
        for c in cells - {id_col, "Status"}
        if all(
            rid not in side or (side[rid].get(c) or "") != (row.get(c) or "")
            for side in sides
        )
    ]


def text_then_act_lines(root, bases, head=None):
    """One line naming each approval-act row the commit `head` (None: the
    index) changes as its OWN while it also writes the approval record, judged
    against `bases`, its parents: a record path or a cell counts only when it
    differs from EVERY base. So a merge is judged by what neither side carried,
    and a lane's refresh merge bringing in trunk's text and act, made as two
    commits, is not the lane's. `[]` when the commit writes no record, or
    changes only `Status`. A diff git cannot read is a line, never a skip.

    Implements: SR-140, LLR-302
    """
    writes = None
    for base in bases:
        args = ["diff", "--name-only", "--no-renames"]
        args += ["--cached", base] if head is None else [base, head]
        own = _git(root, args + ["--", SNAPSHOT_DIR])
        if own is None:
            return [
                "cannot read the diff against {}, so whether it writes the "
                "approval record is unknown".format(base)
            ]
        paths = set(own.splitlines()) - {""}
        writes = paths if writes is None else writes & paths
    rows = {}
    for rel, rid, what in sorted(_text_changes(root, bases, head) if writes else ()):
        rows.setdefault("{} {}".format(PurePosixPath(rel).stem, rid), []).append(what)
    if not rows:
        return []
    named = ("{}: {}".format(row, ", ".join(cells)) for row, cells in rows.items())
    return ["{} in a commit that writes {}".format("; ".join(named), SNAPSHOT_DIR)]


def commit_text_then_act_lines(root, rev):
    """`text_then_act_lines` for one commit against EVERY parent, read off the
    commit object (`_commit_parents`), each line naming the commit. A root
    commit has no text before it and answers `[]`; a parent the repository
    cannot read is refused by name.

    Implements: SR-140, LLR-302
    """
    parents, unread = _commit_parents(root, rev, "it mixes text and the act")
    if unread or not parents:
        return unread
    lines = text_then_act_lines(root, parents, rev)
    return ["commit {}: {}".format(rev[:10], line) for line in lines]


# The per-commit rules that ride the lane-commit walk, each `rule(root, rev) ->
# lines` judging one commit against its own parents. Text then act is the
# first rider; the adoption record's rule (WI-969) the second and the
# parent-first rule (`acceptance_record.commit_parent_first_lines`) the third,
# each carrying its own remedy. The merge slot walks every rider; each hook
# step's squash path walks only its own rule, and the parent-first step has
# none: a squash's staged tree is judged like any other.
LANE_COMMIT_RIDERS = (
    commit_text_then_act_lines,
    adoption_record.commit_adoption_record_lines,
    commit_parent_first_lines,
)


def lane_commit_walk(root, commits, riders=LANE_COMMIT_RIDERS):
    """The ONE lane-commit walk: `(rev, lines)` for each commit of `commits`
    (listed by the caller, oldest first) that a rider in `riders` reports lines
    for, each rider asked of each commit in turn. Lazy, so a caller that stops
    at the first report judges no commit after it.

    Implements: SR-148, SR-140, LLR-298, LLR-302
    """
    return (
        (rev, lines)
        for rev in commits
        for rule in riders
        for lines in (rule(root, rev),)
        if lines
    )


def _squash_lines(root, head, tip):
    """The lines of every commit `head..tip` when the index IS the squash of
    `tip` for everything this rule reads, else None: `tip` contains `head` (the
    lane was rebased onto trunk, as acts serialize) and the index's
    approval-act registries and record are byte-equal to the tip's own. So a
    squash combining two judged cells into a third, and a `SQUASH_MSG` left
    behind by an abandoned squash, exempt nothing unless the staged spine and
    record are a judged commit's. Only this rule's own rider walks here, so a
    line never carries another rule's refusal under this rule's remedy.

    Implements: SR-140, LLR-302
    """
    paths = [c for rel, col in APPROVAL_ACT_CSVS for c in _tier_carriers(rel, col)]
    staged = ["diff", "--cached", "--name-only", tip, "--", SNAPSHOT_DIR, *paths]
    commits = _git(root, ["rev-list", "--reverse", head + ".." + tip])
    within = _git(root, ["merge-base", "--is-ancestor", head, tip]) == ""
    if not within or _git(root, staged) != "" or commits is None:
        return None
    walk = lane_commit_walk(root, commits.split(), (commit_text_then_act_lines,))
    return [ln for _rev, lines in walk for ln in lines]


def staged_text_then_act_lines(root, squashed=()):
    """`text_then_act_lines` for the commit being made: the index against HEAD,
    or against HEAD and MERGE_HEAD while a merge is in progress.

    A SQUASH LANDING is the one commit not held to the rule (owner, README
    Q-8): it carries a lane's text and act together, and is admitted because
    the rule held on every commit it squashes. The hook checks that rather than
    assuming it, since a hand landing never meets the merge slot: `squashed`
    names the commits git's `SQUASH_MSG` lists, newest first (the caller reads
    the file, as this module reads no file). When that tip contains HEAD and
    the index's approval-act registries and record are the tip's own, each
    commit HEAD..tip is judged and the index is not (`_squash_lines`);
    otherwise the index is judged like any commit, a refusal ending with
    `SQUASH_REBASE_HINT`. Before the first commit nothing is judged.

    Implements: SR-140, LLR-302
    """
    head = (_git(root, ["rev-parse", "--verify", "--quiet", "HEAD"]) or "").strip()
    if not head:
        return []
    merging = (_git(root, ["rev-parse", "-q", "--verify", "MERGE_HEAD"]) or "").strip()
    squash = None if merging or not squashed else _squash_lines(root, head, squashed[0])
    if squash is not None:
        return squash
    lines = text_then_act_lines(root, [head] + ([merging] if merging else []))
    hint = [SQUASH_REBASE_HINT] if squashed and not merging else []
    return lines and lines + hint
