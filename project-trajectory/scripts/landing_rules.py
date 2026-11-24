"""THE LANDING RULES — what the coordinator's landing runs on top of the
acceptance record.

The boundary, in one sentence: **everything here is a rule the landing (the
pre-commit hook, the merge slot and the trunk mint) applies to two git trees,
reading the spine and the acceptance record through `acceptance_record`'s
readers; nothing here classes a cell itself, and nothing reads the working
tree.** The comparison, the mirror rules, the merge slot's acceptance-act
refusal and the judged-text identity stay in `acceptance_record.py`
(CMP-006). The import runs one way: nothing there imports this module.

Moved here whole and unchanged from `acceptance_record.py` (WI-1045): a file
doing two components' work gets its own row (queue-drill hand-off §3.5 R2),
and these three rule families are the coordinator's, not the spine's.

    the ruling sync     `ruling_sync_lines`, `staged_ruling_sync_lines`,
                        `commit_ruling_sync_lines` (LLR-298)
    the parent-first    `parent_first_lines`, `parent_first_tiers`,
      judgement         `staged_parent_first_lines`,
                        `commit_parent_first_lines` (LLR-358, IF-308)
    the mint's arms     `settled_amendments` (LLR-364), `unanchored_rows`
                        and `text_as_bound` (LLR-153)

WHAT IT READS OF THE RECORD is IF-091's readers and IF-129's two:
`_spine_rows_at`, `_tier_reads`, `_snapshot_copy_rows`, `_reaccepted_added`,
`_tier_of`, `PARENT_FIRST_CSVS`, `_commit_parents` and `_empty_tree`, and
`split_changed_cells` and `accepted_text_digest`. The judged-text identity
stays one function there: `text_as_bound`, the held-MEANING mint's reading of
which ruled rows a held verdict keeps, calls the identity the held act and the
held-claim exception call.

Stdlib only.

Component: CMP-008

Contracts: IF-308 — the interface seam this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-308: the parent-first commit judgement, offered as a call.
    `staged_parent_first_lines(root)` judges the index against HEAD (and
    MERGE_HEAD during a merge) and `commit_parent_first_lines(root, rev)` one
    commit against every parent of its commit object; both return refusal
    lines, `[]` when the tree passes, and both read through
    `parent_first_lines(root, bases, head)`. A line names the tree (`the
    index:` or `commit <sha10>:`) and an accepted child (`Accepted` or
    `Founded`) left under a declared parent that is not accepted, where the
    child's or the parent's status differs from that row's status in some
    parent tree (an absent row counting as a value), with its own remedy
    (`kitlib.spine.parent_first_line`). A tree whose name list touches no
    carrier of the need, requirement, design or test registry is not read
    further. A name list git cannot produce, or a commit-side registry that
    is listed but cannot be read or does not parse, is a refusal line naming
    it, never a skip; a parent-side registry that fails either way counts
    every status as moved; an absent registry is no rows. No HEAD yet, or a
    root commit, is not judged. Reads two trees and writes nothing.

THE RULING SYNC (WI-790; OI-102 Q3) is a two-tree rule with no dial: a commit
that takes an open item out of `pending` must, in the same diff, update the
Done-when of every work item open in its PARENT tree whose `needs` cites that
item, or close or remove that row (`ruling_sync_lines`). It reads one commit
and its parent and nothing further, so it never skips for missing history;
the pre-commit hook asks it of HEAD and the staged tree
(`staged_ruling_sync_lines`), and the merge slot of every lane commit and its
first parent (`commit_ruling_sync_lines`) — one function over two trees in
both places. It decides only that mechanical condition: whether the change
carries the ruling, and whether a row's other fields must move, is the
reviewer's judgement.

The same rule couples the operator's OVERRULE of a delegated decision to work
(WI-818): a commit that sets a decisions-record entry `operator = "overruled"`
must, in the same diff, file or amend a queued or active work item whose spec
cites the entry (`kitlib.decisions.overrule_sync_lines`, which owns the
record's format and is handed the two trees as readers; `ruling_sync_lines`
asks it of the same diff, so both places ask it with no second step or rung).
The sync's two git reads, a NUL-delimited path list and a blob read that
refuses a listed but unreadable blob, are `kitlib.git`'s.

THE TRUNK MINT'S ACCEPTANCE ARMS, called by `intake` inside this component,
so through no seam. `settled_amendments(root, base, head, records,
routed_cells)` returns `(settled ids, refusal)` for the trunk mint: the records
whose row an act ledger entry the range added re-accepts (IF-220) and whose
accepted and routed traced cells at `head` equal the row's snapshot copy
there. A ledger or copy the tree lists that cannot be read or does not parse
is the refusal, naming the carrier and revision; nothing else suppresses.
`text_as_bound(root, head, ruled)` returns the ids of `ruled` still at the
text their recorded verdict's binding records. `unanchored_rows(root, head,
ids, routed_cells)` returns `({row id: registry}, refusal)` for the mint's
held-act arm: the `ids` whose row at `head` is not settled against its
snapshot copy there, by the one comparison `settled_amendments` makes. A
missing row or copy reads as differing, an id in no tier is left out, and a
copy the tree lists that cannot be read or does not parse is the refusal.
"""

try:
    import spine_carrier
    from acceptance_record import (
        PARENT_FIRST_CSVS,
        _commit_parents,
        _empty_tree,
        _reaccepted_added,
        _snapshot_copy_rows,
        _spine_rows_at,
        _tier_of,
        _tier_reads,
        accepted_text_digest,
        split_changed_cells,
    )
    from kitlib import decisions as _kitdecisions
    from kitlib import git as _kitgit
    from kitlib import registry as _kitregistry
    from kitlib import sitting as _kitsitting
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier
    from acceptance_record import (
        PARENT_FIRST_CSVS,
        _commit_parents,
        _empty_tree,
        _reaccepted_added,
        _snapshot_copy_rows,
        _spine_rows_at,
        _tier_of,
        _tier_reads,
        accepted_text_digest,
        split_changed_cells,
    )
    from kitlib import decisions as _kitdecisions
    from kitlib import git as _kitgit
    from kitlib import registry as _kitregistry
    from kitlib import sitting as _kitsitting
    from kitlib import spine as _kitspine

# The kit's one `git, or None` read, and a registry's and a tier's carriers, as
# the acceptance record aliases them: the same objects, so no second body.
_git = _kitgit.git_out
_spine_carriers = spine_carrier.carriers
_tier_carriers = spine_carrier.tier_carriers


# --- THE RULING SYNC: a ruling updates the rows that cite it (WI-790) ---------
# OI-102 Q3, ruled 2026-10-03: a commit-time block over ONE diff, a commit
# against its own parent, with no history walk and no second path. The
# trigger is the registry state (a row going from `pending` to anything else,
# a deleted pending row included), never page membership; the citing set is
# read from the PARENT tree, so dropping the `needs` token in the ruling's own
# commit discharges nothing. Every terminal state discharges the obligation —
# a closed row has no criteria left to update — because a terminal row lives
# under the archive, so a row the commit moved there or removed is satisfied.
OPEN_ITEMS_REGISTRY = "docs/requirements/open-items.toml"
WORK_DIR = "docs/work"
ARCHIVE_WORK_DIR = "docs/archive/work"
_PENDING = "pending"


# The ruling sync's two git reads, homed in `kitlib.git` (WI-818): every
# path list read NUL-delimited, and a blob read that refuses a listed path
# whose blob cannot be read rather than reading it as absent.
_git_paths = _kitgit.git_paths
_show = _kitgit.git_show


def _tree_specs(root, rev):
    """`{WI id: path}` of every spec in a tree (`rev` None is the index), or
    None when git cannot list it: a view over `kitlib.registry`'s one
    work-spec listing, the id being the file name's first two dash fields. A
    `-000` example is never a row, and of two paths carrying one id the later
    listed wins.

    Implements: SR-148, LLR-298
    """
    paths = _kitregistry.tree_spec_paths(root, rev)
    if paths is None:
        return None
    specs = {}
    for path in paths:
        wid = "-".join(path.rsplit("/", 1)[-1].split("-")[:2])
        if not wid.endswith("-000"):
            specs[wid] = path
    return specs


def _registry_states(root, prefix):
    """`{OI id: status}` of the open-items registry in ONE tree (`prefix` a
    `git show` prefix), read through whichever carrier that tree uses (TOML,
    else CSV — `spine_carrier`'s resolution, as `_spine_rows_at` reads a spine
    registry): `{}` when the tree has neither, None when it does not parse.
    `-000` example rows are dropped.

    Implements: SR-148, LLR-298
    """
    for cand in _spine_carriers(OPEN_ITEMS_REGISTRY):
        text = _show(root, prefix, cand)
        if text is None:
            continue
        rows = spine_carrier.rows_from_text(text, "OI-ID", "." + cand.rsplit(".", 1)[1])
        if rows is None:
            return None
        return {
            rid: (row.get("Status") or "").strip()
            for rid, row in rows.items()
            if not str(rid).endswith("-000")
        }
    return {}


def _ruled_items(before, after):
    """The open items `pending` in `before` and not in `after` (two
    `_registry_states` maps), or None when either side does not parse
    (unreadable is not unchanged).

    Implements: SR-148, LLR-298
    """
    if before is None or after is None:
        return None
    return sorted(
        oid
        for oid, state in before.items()
        if state.lower() == _PENDING and after.get(oid, "").lower() != _PENDING
    )


def _citing_rows(root, base, specs, ruled):
    """`[(WI id, [ruled OI ids it cites], spec text)]` for every row OPEN in
    the `base` tree (under `docs/work/`) whose `needs` cites a ruled item.

    Implements: SR-148, LLR-298
    """
    rows = []
    for wid, path in sorted(specs.items()):
        if not path.startswith(WORK_DIR + "/"):
            continue  # under the archive: terminal, nothing owed
        text = _show(root, base + ":", path)
        try:
            data, _body = _kitregistry.parse_spec_frontmatter(text or "", path)
        except ValueError:
            continue  # a malformed spec is the validator's finding, not this rule's
        needs = ";".join(str(t) for t in data.get("needs") or [])
        cited = [o for o in _kitspine.split_pred_edges(needs)[1] if o in ruled]
        if cited:
            rows.append((wid, cited, text))
    return rows


def _sync_gap(root, new_prefix, head_path, before_text):
    """Why one citing row is out of sync in the new tree, or None when it is
    satisfied: removed, closed (moved under the archive), or open with a
    non-empty Done-when section whose RAW text differs from the parent's (A1:
    read from the raw spec text; whether the change carries the ruling is the
    reviewer's judgement, not this rule's).

    Implements: SR-148, LLR-298
    """
    if head_path is None or not head_path.startswith(WORK_DIR + "/"):
        return None
    after = _raw_done_when(_show(root, new_prefix, head_path))
    if not after:
        return "it keeps no Done-when"
    if after == _raw_done_when(before_text):
        return "its Done-when is unchanged"
    return None


def _raw_done_when(text):
    """A spec's Done-when section as raw text, outer blank lines trimmed."""
    return "\n".join(_kitregistry.done_when_section(text or "")).strip()


def ruling_sync_lines(root, base, head=None):
    """One line per (row, item) the diff `base` -> `head` leaves out of sync
    (`head` None is the index): an open item leaves `pending` while a work item
    open in `base` cites it in `needs`, and the same diff neither updates that
    row's Done-when (non-empty afterwards, and its raw section changed) nor
    closes or removes the row. The registry is read through either carrier.
    `[]` when nothing leaves `pending`. A diff git cannot read is a line,
    never a skip. The diff's overrules are judged too
    (`kitlib.decisions.overrule_sync_lines`, reading both trees through `_show`).

    Implements: SR-148, LLR-298
    """
    args = ["diff", "--name-only", "--no-renames"]
    args += ["--cached", base] if head is None else [base, head]
    changed = _git_paths(root, args)
    if changed is None:
        return [
            "cannot read the diff against {}, so whether it rules an open item "
            "is unknown".format(base)
        ]
    try:
        lines = []
        if set(_spine_carriers(OPEN_ITEMS_REGISTRY)) & set(changed):
            lines = _judged_lines(root, base, head)
        new_prefix = ":" if head is None else head + ":"
        return lines + _kitdecisions.overrule_sync_lines(
            changed,
            lambda rel: _show(root, base + ":", rel),
            lambda rel: _show(root, new_prefix, rel),
        )
    except _kitgit.UnreadableBlob as exc:
        return [
            "{} is listed in its tree but its contents cannot be read, so whether "
            "this commit rules an open item or overrules a decision is unknown: "
            "fetch it (a partial clone offline or a damaged object store), or "
            "name it in UTF-8, and retry".format(exc)
        ]


def _judged_lines(root, base, head):
    """`ruling_sync_lines` once the diff touches the registry: the ruled items,
    then each citing row. Every blob it reads goes through `_show`.

    Implements: SR-148, LLR-298
    """
    new_prefix = ":" if head is None else head + ":"
    ruled = _ruled_items(
        _registry_states(root, base + ":"), _registry_states(root, new_prefix)
    )
    if ruled is None:
        return [
            "the open-items registry does not parse on one side of the diff, "
            "so whether it rules an open item is unknown"
        ]
    if not ruled:
        return []
    return _sync_lines(root, base, head, ruled)


def _sync_lines(root, base, head, ruled):
    """The per-row half of `ruling_sync_lines`, once the ruled items are known.

    Implements: SR-148, LLR-298
    """
    base_specs, head_specs = _tree_specs(root, base), _tree_specs(root, head)
    if base_specs is None or head_specs is None:
        return ["cannot list the work items on both sides of the diff"]
    new_prefix = ":" if head is None else head + ":"
    lines = []
    for wid, cited, text in _citing_rows(root, base, base_specs, ruled):
        gap = _sync_gap(root, new_prefix, head_specs.get(wid), text)
        if gap:
            lines.append(
                "{} cites {}, which this commit takes out of pending, and {}: "
                "the ruling's commit updates the row's Done-when with the decided "
                "criteria, citing the item, or closes or removes the row".format(
                    wid, ", ".join(cited), gap
                )
            )
    return lines


def staged_ruling_sync_lines(root):
    """`ruling_sync_lines` for the commit being made: the index against HEAD,
    or against the empty tree before the first commit (which closes nothing).

    Implements: SR-148, LLR-298
    """
    head = _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])
    base = head.strip() if head and head.strip() else _empty_tree(root)
    if base is None:
        return ["cannot read HEAD or the empty tree, so the commit is unjudged"]
    return ruling_sync_lines(root, base)


def commit_ruling_sync_lines(root, rev):
    """`ruling_sync_lines` for one commit against its FIRST parent, read off
    the commit object itself (not `rev^1`, which a shallow boundary hides). A
    true root commit — no parent in its object — has nothing to close and
    answers `[]`; a parent the repository cannot read (a shallow clone, a
    missing object) is refused by name, never read as a root (A1).

    Implements: SR-148, LLR-298
    """
    parents, unread = _commit_parents(root, rev, "it rules an open item", first=True)
    if unread or not parents:
        return unread
    return ruling_sync_lines(root, parents[0], rev)


# --- THE PARENT-FIRST COMMIT JUDGEMENT (LLR-358; IF-308) ----------------------
# The registries it reads are the record's universe, `PARENT_FIRST_CSVS`, which
# `held_status` reads too; the carrier loop is the record's `_tier_reads`.


def parent_first_tiers(root, prefix):
    """`({label: rows}, failures)` of the parent-first registries at the tree
    `prefix`: each tier from the first carrier the tree lists, an absent
    registry no rows, and one `"<path> cannot be read"` or `"<path> does not
    parse"` failure per registry that fails. Public because the act
    derivation (`adjudicate_act`, WI-1059) judges the flips it lists over the
    same rows this judgement reads.

    Implements: SR-246, LLR-358"""
    tiers, failures = {}, []
    for path, col in PARENT_FIRST_CSVS:
        tiers[col[:-3]] = []
        for cand, rows, failure in _tier_reads(root, prefix, path, col):
            if failure:
                failures.append("{} {}".format(cand, failure))
            else:
                tiers[col[:-3]] = list(rows.values())
            break
    return tiers, failures


def _parent_first_names(root, base, head):
    """The parent-first carriers the tree `head` (the index when None) changes
    against `base`, or None when git cannot list them.

    Implements: SR-246, LLR-358"""
    watched = [c for path, col in PARENT_FIRST_CSVS for c in _tier_carriers(path, col)]
    side = [head] if head else ["--cached"]
    return _kitgit.git_paths(
        root, ["diff", "--name-only", "--no-renames", base, *side, "--", *watched]
    )


def _status_moved(entry, statuses):
    """Whether the child's or the parent's status in `entry` differs from that
    row's status in one parent tree's `statuses` (`{id: status}`, an absent
    row reading None); a parent tree that failed to read (None) moved all.

    Implements: SR-246, LLR-358"""
    child, child_status, parent, parent_status = entry
    side = statuses or {}
    moved = (side.get(child), side.get(parent)) != (child_status, parent_status)
    return statuses is None or moved


def _parent_statuses(root, base):
    """`{id: status}` of the parent-first tiers at `base`, or None when any of
    its registries cannot be read or does not parse.

    Implements: SR-246, LLR-358"""
    tiers, failures = parent_first_tiers(root, base + ":")
    if failures:
        return None
    return {
        str(r.get(label + "-ID") or "").strip(): (r.get("Status") or "").strip()
        for label, rows in tiers.items()
        for r in rows
    }


def parent_first_lines(root, bases, head=None):
    """The parent-first refusal lines for the tree `head` (the index when
    None) against each tree of `bases`: one per accepted child its tree leaves
    under an unaccepted parent where either status moved against some base
    (`_status_moved`), or one per failed read. Not read further when no base
    sees a parent-first carrier change.

    Implements: SR-246, LLR-358"""
    tree = "the index" if head is None else "commit " + head[:10]
    touched = False
    for base in bases:
        names = _parent_first_names(root, base, head)
        if names is None:
            return [
                "{}: git cannot list what it changes against {}, so whether it "
                "leaves an accepted row under an unaccepted parent is "
                "unknown".format(tree, base[:10])
            ]
        touched = touched or bool(names)
    if not touched:
        return []
    tiers, failures = parent_first_tiers(root, ":" if head is None else head + ":")
    if failures:
        return [
            "{}: {} in {}, so whether it leaves an accepted row under an "
            "unaccepted parent is unknown".format(tree, failure, tree)
            for failure in failures
        ]
    entries = _kitspine.parent_first_findings(tiers)
    sides = [_parent_statuses(root, base) for base in bases] if entries else []
    return [
        "{}: {}".format(tree, _kitspine.parent_first_line(entry))
        for entry in entries
        if any(_status_moved(entry, side) for side in sides)
    ]


def staged_parent_first_lines(root):
    """`parent_first_lines` for the commit being made: the index against HEAD,
    and against MERGE_HEAD during a merge. No HEAD yet judges nothing.

    Implements: SR-246, LLR-358"""
    shas = [
        _git(root, ["rev-parse", "--verify", "--quiet", ref + "^{commit}"])
        for ref in ("HEAD", "MERGE_HEAD")
    ]
    bases = [sha.strip() for sha in shas if sha and sha.strip()]
    return parent_first_lines(root, bases) if shas[0] and shas[0].strip() else []


def commit_parent_first_lines(root, rev):
    """`parent_first_lines` for one lane commit against every parent of its
    commit object; a root commit is not judged, and a parent the repository
    cannot read is `_commit_parents`' line.

    Implements: SR-246, LLR-358"""
    parents, unread = _commit_parents(
        root, rev, "it leaves an accepted row under an unaccepted parent"
    )
    if unread or not parents:
        return unread
    return parent_first_lines(root, parents, rev)


# --- THE TRUNK MINT'S ACCEPTANCE ARMS (LLR-364, LLR-153) ------------------------
# The settled-amendment filter and the held-act arms `intake` mints through.
# The act ledger and the record's copies are read through the record's own
# readers (IF-091), the cells compared and digested on its basis (IF-129).


def _latest_reaccept(added, rid):
    """The index in the range-added ledger entries `added` of the latest one
    that re-accepts `rid`, or None. Entries are in file order, which IF-220
    makes `seq` order.

    Implements: SR-178, LLR-364"""
    marks = [
        i for i, a in enumerate(added) if rid in map(str, a.get("reaccepted") or ())
    ]
    return marks[-1] if marks else None


def _no_later_writer(later, rel_path):
    """Did none of the ledger entries `later` write `rel_path`? An entry whose
    `copied` names the registry wrote it, and a legacy entry (no `copied`: its
    copy set is unknown, IF-220) may have.

    Implements: SR-178, LLR-364"""
    stem = spine_carrier.stem(rel_path)
    return not any(
        "copied" not in a or stem in {spine_carrier.stem(p) for p in a["copied"] or ()}
        for a in later
    )


def _row_settled(rel_path, id_col, copy_row, live_row, routed):
    """Does the live row equal its snapshot copy in every accepted cell and
    every routed traced cell? A row missing from either side is not settled.

    Implements: SR-178, LLR-364"""
    if copy_row is None or live_row is None:
        return False
    changed = split_changed_cells(rel_path, id_col, copy_row, live_row)
    return not changed["accepted"] and not set(changed["traced"]) & set(routed)


def _routed_unmoved(rel_path, id_col, before_row, live_row, routed):
    """Does the live row carry the routed traced cells it carried before the
    range? A row missing from either side has moved.

    Implements: SR-178, LLR-364"""
    if before_row is None or live_row is None:
        return False
    changed = split_changed_cells(rel_path, id_col, before_row, live_row)
    return not set(changed["traced"]) & set(routed)


def _tier_sides(root, base, head, rel_path, id_col):
    """`(sides, failure)`: one tier's `(copy at head, live at head, live at
    base)` row maps, or the snapshot copy's failure (`_snapshot_copy_rows`).

    Implements: SR-178, LLR-364"""
    copy, failure = _snapshot_copy_rows(root, head, rel_path, id_col)
    if failure:
        return None, failure
    live = _spine_rows_at(root, head + ":", rel_path, id_col)
    return (copy or {}, live, _spine_rows_at(root, base + ":", rel_path, id_col)), None


def _settled_row(added, rid, rel_path, id_col, sides, routed):
    """Is `rid` settled by the range-added ledger entries `added`, given its
    tier's `sides` (`_tier_sides`)? It needs an entry re-accepting it and its
    whole accepted and routed traced cell set equal to its copy at the range's
    end. That copy is the re-accepting act's own when no later entry wrote the
    registry. A later writer re-accepting another row cannot have absorbed an
    accepted-cell change to this one (the snapshot refuses to copy unaccepted
    accepted drift), only a routed traced one, so a later writer still leaves
    it settled when its routed traced cells are the same at the range's two
    ends. That proves equality at the ends, not that no routed cell moved in
    between; its one limit: a routed traced cell moved before the re-accepting
    act and restored after it is re-anchored by the later copy, as any traced
    refresh is, and the row settles.

    Implements: SR-178, LLR-364"""
    mark = _latest_reaccept(added, rid)
    copy, live, before = sides
    if mark is None or not _row_settled(
        rel_path, id_col, copy.get(rid), live.get(rid), routed
    ):
        return False
    return _no_later_writer(added[mark + 1 :], rel_path) or _routed_unmoved(
        rel_path, id_col, before.get(rid), live.get(rid), routed
    )


def settled_amendments(root, base, head, records, routed_cells):
    """`(settled ids, refusal)`: which amendment `records` the range
    `base..head` already settled. A record is settled when a ledger entry the
    range added re-accepts its row, the row's whole accepted and routed traced
    cell set at `head` equals its snapshot copy at `head`, AND either no entry
    the range added after the latest such one wrote (or, a legacy entry, may
    have written) the row's registry, or the row's routed traced cells are the
    same at the range's two ends, `base` and `head` (`_settled_row`). That
    second arm's one limit: a routed traced cell moved before the re-accepting
    act and restored after it is re-anchored by a later act's copy of the
    registry, and the row settles. The test reads what each act
    copied, so it holds on a squashed range whose one commit carries every
    act. The whole row, not the net diff's cells, so a cell edited after the
    act and then restored still differs. `routed_cells` is the caller's
    routing rule, keyed by registry. With no records nothing is read. A
    ledger or copy the tree lists but that cannot be read or does not parse
    is the refusal, naming the carrier, revision and which; a missing copy or
    row is unsettled, so it mints.

    Implements: SR-178, LLR-364"""
    if not records:
        return frozenset(), None
    added, refusal = _reaccepted_added(root, base, head)
    if refusal:
        return frozenset(), refusal
    routed = {spine_carrier.stem(k): v for k, v in routed_cells.items()}
    settled, tiers = set(), {}
    for rid in sorted({rec["id"] for rec in records}):
        rel, col = _tier_of(rid)
        if rel is None or _latest_reaccept(added, rid) is None:
            continue
        if rel + col not in tiers:
            tiers[rel + col], refusal = _tier_sides(root, base, head, rel, col)
            if refusal:
                return frozenset(), refusal
        stem = spine_carrier.stem(rel)
        if _settled_row(added, rid, rel, col, tiers[rel + col], routed.get(stem, ())):
            settled.add(rid)
    return frozenset(settled), None


def unanchored_rows(root, head, ids, routed_cells):
    """`({row id: registry}, refusal)`: the `ids` whose live row at `head`
    differs from its snapshot copy there, in an accepted cell or a routed
    traced one (`_row_settled`). A missing row or copy reads as differing, an
    id in no tier is left out, and a copy the tree lists that cannot be read
    or does not parse is the refusal, naming the carrier and revision.
    `routed_cells` is the caller's routing rule, keyed by registry.

    Implements: SR-174, LLR-153"""
    routed = {spine_carrier.stem(k): v for k, v in routed_cells.items()}
    found, tiers = {}, {}
    for rid in sorted(ids):
        rel, col = _tier_of(rid)
        if rel is None:
            continue
        if rel + col not in tiers:
            copy, failure = _snapshot_copy_rows(root, head, rel, col)
            if failure:
                return {}, failure
            live = _spine_rows_at(root, head + ":", rel, col)
            tiers[rel + col] = copy or {}, live
        copy, live = tiers[rel + col]
        cells = routed.get(spine_carrier.stem(rel), ())
        if not _row_settled(rel, col, copy.get(rid), live.get(rid), cells):
            found[rid] = rel
    return found, None


def text_as_bound(root, head, ruled):
    """The ids of `ruled` (`{row id: recorded verdict path}`) whose accepted
    text at `head` is the text their verdict's binding records. A row gone
    from its registry has no text to differ, so it counts; a binding that
    records no text for the row (`kitlib.sitting.recorded_identities`) does
    not, and neither does an id in no tier.

    Implements: SR-174, LLR-153"""
    kept, tiers, bound = set(), {}, {}
    for rid, verdict in ruled.items():
        rel, col = _tier_of(rid)
        if rel is None:
            continue
        if rel + col not in tiers:
            tiers[rel + col] = _spine_rows_at(root, head + ":", rel, col)
        if verdict not in bound:
            identities, _why = _kitsitting.recorded_identities(root, head, verdict)
            bound[verdict] = identities or {}
        row = tiers[rel + col].get(rid)
        if row is None or (
            bound[verdict].get(rid) == accepted_text_digest(rel, col, row)
        ):
            kept.add(rid)
    return kept
