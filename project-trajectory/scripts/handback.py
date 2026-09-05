"""handback.py — the lane closes that are not a clean merge (concurrency-v2 §A3,
rewritten onto the SR-144/LLR-161 outcome model).

`integrate.py` owns the ordinary outcome: a lane finishes, its specs land in
`complete/`, the branch merges. This module owns the others, so that **every**
lane ends in a merge and no branch is ever left hanging:

  close_partial  the lane could not finish. The work so far is committed AS-IS,
                 an immutable PER-CLOSE REPORT is written under
                 `docs/handbacks/`, and each claimed spec moves to the terminal
                 `partial/`. The branch then merges like any other, which is the
                 whole point: the close is a trunk fact, the partial work is
                 reachable history, and the run keeps going.

  quarantine     the RULED red arm (owner decision 1, 2026-07-31). Every outcome
                 merges and a merge needs a green bar, so a lane handing back
                 code the bar refuses would be the one branch that could still
                 hang. The ruling: revert the code, keep the record — the
                 failing diff lands as a bar-inert `.patch` under `docs/work/`,
                 the product paths go back to what trunk had, and nothing live
                 can red anything.

WHAT CHANGED, AND WHY IT HAD TO. The old contract moved a returned spec back to
`queued/` with a `## Handback` section and a `blockref`, and **that was the whole
record of the return**. There was no artifact for the event itself — only a
mutable, movable, self-referencing spec. So every mechanism that tried to answer
*"given this spec, is a disposition still owed for THIS return?"* had to
reconstruct the event from a proxy, and five successive ones leaked:

    merge sha in the title        a bare sweep uses symbolic HEAD; every
                                  re-sweep re-minted
    the spec's last-touch commit  any lifecycle edit moves it
    a digest of the note          the note is mutable and not section-bounded
    an open-disposition state read a seven-char title token stayed authoritative
    provenance via WI-Refs/SpecRef broad relationship fields, not provenance —
                                  unrelated rows STARVED a genuine return

Every failure was starvation-class: an owed judgement silently not happening.
The per-close report dissolves the class rather than mitigating it, because
**the document IS the event's identity** — immutable, so it never moves; unique,
so a second close is a second document; and citable, so a disposition's
provenance is positive rather than inferred.

THE LANE'S MOVE IS A CLAIM, NOT A VERDICT. The lane says what happened
(`complete` / `partial` / `cancelled`) — a fact it is entitled to assert. What
that means is the adjudicator's, and it is made authoritative BY MINTING: a
corrective successor row, never a mutation of the closed one. Where the
adjudicator overrules the claim, the byte-identical spec moves to the corrected
terminal folder (the folder stays the single truth of final status) and the
report stays on record as the claim it was.

CANCELLED has no function here on purpose. It is a JUDGEMENT — this will never
be built, and here is why — so the lane that makes it writes the move and the
report itself; only `integrate.branch_outcomes` needs to read it back.

A sibling of `integrate.py`, and the dependency runs ONE WAY: this module
imports it (for the lane worktree, the claim read and the sha helpers) and it
does not import back. That sentence was FALSE for as long as it stood in this
header — `integrate._partial_report_refusal` carried a function-local `import
handback` to reach the report's path and refusal, so the header's "never the
reverse" described an intention rather than the code. WI-483 slice 2 made it
true by moving the report's SHAPE down to `kitlib/station.py`, below both
modules, rather than by softening the sentence. `dispatch.py` calls both — it
decides which outcome a cycle reached, and the writes live here.

Contracts: IF-137 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-137: the terminal-outcome WRITES for the two lane closes that are
    not a clean merge. `close_partial(root, branch, reason, fields)` commits the
    lane's work as-is, writes an IMMUTABLE per-close report under
    `docs/handbacks/` in the SAME commit as the move, and moves every claimed
    spec to the terminal `partial/` folder; it returns `(closed WI ids, None)`
    or `(None, refusal)` and refuses rather than half-closing.
    `quarantine(root, branch, why)` is the ruled red arm: the failing diff is
    kept as a bar-inert `.patch` under the work tree, every non-bookkeeping path
    is reverted to the lane's merge base, and it returns a refusal string or
    None. Neither function DECIDES which outcome a lane reached — that judgement
    is the caller's — so decision and write stay in separate modules and every
    lane still ends in a merge.
"""

from __future__ import annotations

import re
import subprocess

import agent_common as ac
import consolidate
import integrate
import spec_move
from kitlib import station

# The frontmatter `specref = ...` line, cleared at a terminal close (R-E: an
# open row's forward bridge resolves; a closed row carries none).
_SPECREF_LINE_RE = re.compile(r"(?m)^specref\s*=\s*.*$")


def spec_move_split(text):
    """`(frontmatter_text, body)` for one spec — the frontmatter WITHOUT its
    `+++` fences (trailing newline kept) and everything after the closing fence.
    Raises ValueError naming no file when the fences are absent."""
    lines = text.split("\n")
    if not lines or lines[0] != "+++" or "+++" not in lines[1:]:
        raise ValueError("no closed +++ frontmatter fence")
    close = lines.index("+++", 1)
    return "\n".join(lines[1:close]) + "\n", "\n".join(lines[close + 1 :])


# Where a quarantined red close's failing diff lands. Under `docs/work/` because
# that is where the work item's own record lives, and as a `.patch` because no
# bar reads one: the doc checkers discover `*.md`, the stub check reads
# `src/**/*.py`, and check.py ignores `docs/work/*` outright — so the artefact is
# inert by its extension, not by a rule someone has to keep.
ARTEFACTS = integrate.WORK + "/handback"

# --- the per-close report's shape: RE-EXPORTED from the read model -------------
#
# WI-483 slice 2 moved the report's PATH, FORMAT, READ and REFUSAL down into
# `kitlib/station.py`, beside the terminal-outcome vocabulary they belong to:
# `SR-144` says every lane close is a terminal state WITH AN IMMUTABLE RECORD,
# and the two clauses had been living in two modules. The cost of the split was
# an import edge in the wrong direction — the merge coordinator refuses a
# `partial` merge whose report is silent about the keep/discard split, so
# `integrate` reached UP into this module for `report_path`/`report_refusal`,
# a deferred function-body import that was a back edge of the five-module
# strongly connected component the 2026-08-19 review recorded (H-02).
#
# WHAT STAYED: the WRITES. `close_partial` and `quarantine` are effects on a
# worktree and a git tree, and effects live at the edge. What left is the
# decision half — a path from two strings, text from a dict, and "is this report
# actionable?" — which is testable without a repository.
#
# These aliases are the no-caller-moves half, the same shape `integrate` used
# for the outcome vocabulary after slice 1.
REPORTS = station.REPORTS
CLAIMED_OUTCOMES = station.CLAIMED_OUTCOMES
SUGGESTED_TIERS = station.SUGGESTED_TIERS
SPLIT_DECIDERS = station.SPLIT_DECIDERS
report_path = station.report_path
render_report = station.render_report
read_report = station.read_report
report_refusal = station.report_refusal
mechanical_close_subject = station.mechanical_close_subject

# R3's outcome vocabulary, stated ONCE and imported by intake for the
# disposition row's title. `re-queue` retired with LLR-161: a terminal row is
# never put back on the frontier, so continuing means drafting a SUCCESSOR.
DISPOSITION_OUTCOMES = "cancel / defer / draft a successor / surface an open item"


def _git_stdout(cwd, *args):
    """One git call whose STDOUT survives byte for byte: `(code, stdout)`.

    `ac.git` strips its output, which is right for every sha/porcelain read in
    the sibling module and wrong for exactly two calls here: a `--name-status
    -z` walk (the NUL delimiters matter) and a diff destined for a `.patch`
    file, whose last line can legitimately be a single space — the context line
    for a blank line — which stripping would turn into an unappliable patch."""
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    return proc.returncode, proc.stdout or ""


# The surfaces a revert must never touch: the spec move, the report and the log
# fragments ARE the record being kept, so reverting them would revert the close
# itself.
BOOKKEEPING = (integrate.WORK + "/", "docs/log.d/", REPORTS + "/")


def diff_records(fields):
    """`--name-status -z` fields as `[(status, [paths])]`, or None if truncated.

    RECORDS, NOT PAIRS. `diff.renames` has defaulted true since Git 2.9, so
    `R<score>` and `C<score>` are ordinary output and each emits THREE fields —
    the status, the old path, the new path. Reading the stream two fields at a
    time desynchronises at the first one and every field after it lands in the
    wrong slot: paths get read as statuses, the bookkeeping filter stops
    matching, and the last record falls off the end of the loop bound. REVIEW-A
    round 1 drove exactly that and the quarantine printed a confident
    "4 path(s) reverted" over a branch whose failing file was untouched.

    A stream that ends mid-record is a TRUNCATED READ, not an empty diff, and
    returns None so the caller refuses instead of quarantining a partial list.
    """
    records, i = [], 0
    while i < len(fields):
        status = fields[i]
        wanted = 2 if status[:1] in ("R", "C") else 1
        if i + wanted >= len(fields):
            return None
        records.append((status, fields[i + 1 : i + 1 + wanted]))
        i += 1 + wanted
    return records


def _revert_ops(status, paths):
    """The git operations that undo one diff record: `[(op, path)]`.

    A rename or copy is TWO undo steps, which is the other half of why the
    pair-parse was wrong: the NEW path is an addition this branch made and has
    to go, and the OLD path is what the base had and has to come back. (For a
    copy the old path is unchanged at the base, so restoring it is a harmless
    no-op — uniform beats a special case nobody will remember.)

    THE `C` ARM IS DEFENSIVE, not dead: from the call `quarantine` actually
    makes it cannot fire, because plain `--name-status` reports a copied file
    as `A` even at `diff.renames=copies` — git needs `--find-copies-harder` to
    emit `C` (measured, REVIEW-A round 2). It stays because `diff_records` and
    this function have to agree about the three-field forms as a PAIR: a caller
    that ever adds the flag would otherwise get a parse that reads copies and
    an undo that mishandles them, which is the silent shape this whole function
    exists to have stopped making.
    """
    if status[:1] in ("R", "C"):
        return [("rm", paths[1]), ("checkout", paths[0])]
    if status[:1] == "A":
        return [("rm", paths[0])]
    return [("checkout", paths[0])]


def _revert(wt, base, branch, changed):
    """Undo every changed record in `wt`, back to `base`. A refusal, or None.

    EVERY return code is read. A revert that half-happened is the one outcome
    worse than not quarantining at all, so a failing step resets the lane to its
    tip and refuses by name — and a DISCARDED code here is exactly how the
    pair-parse defect stayed silent while four no-match git calls ran and the
    run printed a confident "4 path(s) reverted" (REVIEW-A round 1).
    """
    for status, paths in changed:
        for op, path in _revert_ops(status, paths):
            if op == "rm":
                code, out = ac.git(wt, "rm", "-q", "-f", "--", path)
            else:
                code, out = ac.git(wt, "checkout", base, "--", path)
            if code != 0:
                ac.git(wt, "reset", "--hard", "HEAD")
                return (
                    "the quarantine revert of {} FAILED on {} ({} {}) - the "
                    "lane is reset to its tip and nothing was quarantined:"
                    "\n{}".format(branch, path, op, status, ac._failure_tail(out))
                )
    return None


# --- the close itself: the writes that stay here -------------------------------


def _lane(root, branch):
    """`(lane worktree, None)` for a close, or `(None, refusal)`."""
    holder, is_primary = integrate._worktree_holding(root, branch)
    if is_primary:
        return None, (
            "the MAIN checkout at {} has {} checked out, so there is no trunk "
            "checked out to close the lane INTO; switch it back (git -C {} "
            "checkout <trunk>) and re-run".format(holder, branch, holder)
        )
    return integrate.lane_worktree(root, branch)


def _span(root, branch):
    """`<merge-base>..<branch tip>` in short shas — the range the report names
    as the home of the work so far."""
    code, base = ac.git(root, "merge-base", branch, integrate._head(root))
    return "{}..{}".format(
        (base.strip() or "")[:10] if code == 0 else "(trunk)",
        (integrate._rev(root, branch) or "")[:10],
    )


def _no_recursion_refusal(root, branch, specs):
    """THE NO-RECURSION INVARIANT (WI-388, ruling R3): a DISPOSITION row — the
    adjudication kind — may never itself close early. Enforced HERE, at the
    machinery that would perform the act, not by prose: the refusal stops the
    run for a human, because a disposition that cannot dispose is the one
    state the outcome model cannot express. Read off the TRUNK's claimed copy
    (the same one-home read the slot uses); an unreadable frontmatter falls
    through — the close path's own read fails on it by name."""
    for _wi_id, name in specs:
        try:
            meta = integrate._spec_frontmatter(root / integrate.ACTIVE / branch / name)
        except (OSError, ValueError):
            continue
        if (meta.get("safety_class") or "").strip().lower() == "adjudication":
            return (
                "{} claims the adjudication row {} - a disposition row never "
                "closes early (ruling R3, no recursion: its outcomes are {}). "
                "The run stops for a human to read the lane".format(
                    branch, name, DISPOSITION_OUTCOMES
                )
            )
    return None


def _restore(wt, written, refusal):
    """Un-write every report this close produced, then return `refusal` — the
    same restore-on-refusal shape `_revert` and the mint's
    `_bookkeeping_commit` use. Leaving a staged report behind would leave the
    lane DIRTY (§5.6 refuses to GC one) and would leave a record on disk for a
    close that did not happen."""
    for rel in reversed(written):
        # `git rm` on an UNTRACKED path fails and leaves the file — and the
        # `cannot stage the close report` arm is reached with the report
        # written but not yet added, so that is exactly the arm the restore
        # most needs to work in. Unlink after, unconditionally: the file was
        # created by this call, and a report on disk for a close that did not
        # happen is the dirty lane §5.6 refuses to GC.
        ac.git(wt, "rm", "-q", "-f", "--", rel)
        try:
            (wt / rel).unlink()
        except OSError:
            pass
    return refusal


def open_claimed_specs(wt, branch, specs):
    """Of the TRUNK's claimed `specs`, the ones still in `active/<branch>/` on
    the LANE — the rows a close still has a claim over.

    ONE HOME FOR THE BATCH FILTER, because both closes need it and neither may
    answer it differently. The claimed set is read off the trunk, which lists
    every row of a §A4 batch; a batch closes its rows one at a time, so by the
    time the lane reaches a close the earlier rows are already in `complete/` on
    the branch. Reading one of those as a claim made a four-row lane's DONE a
    FATAL run exit (measured 2026-09-03, `wi-589-…`: "cannot read the claimed
    spec", which the dispatcher turns into EXIT_PREFLIGHT and the whole loop
    exits 2), and would have had the partial close move a row a second time,
    overwriting an outcome the lane itself declared.
    """
    return [
        (wi_id, name)
        for wi_id, name in specs
        if (wt / "{}/{}/{}".format(integrate.ACTIVE, branch, name)).is_file()
    ]


def _existing_report_refusal(wt, branch, specs):
    """The immutability refusal if any of `specs` already carries a close
    report, else None.

    IMMUTABLE MEANS IMMUTABLE. The report IS the close event's identity, and an
    identity that can be overwritten is a mutable proxy again — the exact shape
    five dedup mechanisms died on. A second close of the same (wi, branch) is
    not a thing this contract permits (`partial/` is terminal), so meeting one
    means something upstream is wrong and the honest act is to refuse rather
    than to rewrite the record of the first close.

    ASKED BEFORE ANY REPORT IS WRITTEN, which is also why it is asked here
    rather than per-iteration: nothing is on disk yet, so the refusal needs no
    restore, and a row this close would otherwise SKIP (already terminal on the
    branch) is still caught — a second close of a row already in `partial/` must
    refuse, never pass silently as a no-op.
    """
    for wi_id, _name in specs:
        rep_rel = report_path(branch, wi_id)
        if (wt / rep_rel).exists():
            return (
                "a close report already exists at {} - the report is the close "
                "EVENT's immutable identity, so a second close of {} on {} is "
                "refused rather than overwriting it".format(rep_rel, wi_id, branch)
            )
    return None


def _commit_residue_as_is(wt, branch, ids, reason):
    """Commit whatever the lane left uncommitted, AS IS — a refusal, or None on
    a clean tree or a good commit.

    The hook is skipped because "as-is" has to mean it: the branch's own §A2
    refresh regenerates and BARS this tree before anything merges, so a hook
    refusal here would only trade a merge that is checked for a branch that
    hangs.
    """
    if not ac.working_tree_dirty(wt):
        return None
    ac.git(wt, "add", "-A")
    code, out = ac.git(
        wt,
        "commit",
        "--no-verify",
        "-m",
        "{}: the work so far, committed as-is (partial close)\n\n{}".format(
            ", ".join(ids), reason
        ),
    )
    if code != 0:
        return "the as-is work commit failed on {}:\n{}".format(
            branch, ac._failure_tail(out)
        )
    return None


def close_partial(root, branch, reason, fields=None):
    """Close `branch` on the PARTIAL outcome. `(closed WI ids, None)`, or
    `(None, refusal)`.

    Three deliberate choices. The as-is commit skips the commit hook, because
    "as-is" has to mean it: the branch's own §A2 refresh regenerates and BARS
    this tree before anything merges, so a hook refusal here would only trade a
    merge that is checked for a branch that hangs. The specs move to the
    TERMINAL `partial/` rather than back to `queued/`, because terminal is what
    stops a driver claiming, closing and re-claiming the same row forever —
    the property the old contract bought with a `blockref` and a mutable note.
    And the report is written in the SAME COMMIT as the move: a lane that has
    already moved its specs out of `active/` is left alone by the dispatcher
    (it cannot read the claim any more), so a report written in a later commit
    would be a report the close can no longer produce.
    """
    specs = integrate._claimed_specs(root, branch)
    if not specs:
        return None, "trunk holds no claimed specs for {}".format(branch)
    wt, err = _lane(root, branch)
    err = err or _no_recursion_refusal(root, branch, specs)
    if err:
        return None, "cannot close {}: {}".format(branch, err)
    refusal = _existing_report_refusal(wt, branch, specs)
    if refusal:
        return None, refusal
    specs = open_claimed_specs(wt, branch, specs)
    if not specs:
        # Every claimed row had already declared its own terminal outcome, so
        # the branch IS finished and there is nothing to close. The dispatcher's
        # "specs are already out of active/" arm is the ordinary way here; this
        # is the same answer for a batch that got there one row at a time.
        return [], None
    ids = [wi_id for wi_id, _name in specs]
    refusal = _commit_residue_as_is(wt, branch, ids, reason)
    if refusal:
        return None, refusal
    span = _span(root, branch)
    # Every report THIS CALL has written, so a refusal on spec #3 restores #1
    # and #2 as well. A per-iteration undo only ever cleaned up the current
    # spec, so a multi-spec lane could refuse and still leave earlier reports
    # staged beside specs already moved to `partial/` — a half-close, which is
    # the one state this all-or-nothing ritual exists to make unrepresentable.
    written = []
    for wi_id, name in specs:
        rel = "{}/partial/{}".format(integrate.WORK, name)
        src_rel = "{}/{}/{}".format(integrate.ACTIVE, branch, name)
        # The report FIRST: it is the event's identity, and a move without one
        # is the artifact-less return this contract exists to end. Its
        # immutability rung ran over the whole claimed set above, before
        # anything was written.
        rep_rel = report_path(branch, wi_id)
        dest = wt / rep_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_report(wi_id, branch, "partial", reason, span, fields))
        written.append(rep_rel)
        code, out = ac.git(wt, "add", "--", rep_rel)
        if code != 0:
            return None, _restore(
                wt,
                written,
                "cannot stage the close report {}:\n{}".format(
                    rep_rel, ac._failure_tail(out)
                ),
            )
        # The move is the link-aware ritual (WI-393): the spec lands in
        # `partial/` with its own links rebased and every inbound link
        # redirected, staged into this same commit, never as relink residue.
        # No `new_text`: the spec's own definition does NOT change — only where
        # it sits and what the report says about delivery. That is the whole
        # "scope definitions never change; only whether they were delivered".
        _touched, refusal = spec_move.move_spec(wt, src_rel, rel)
        if refusal:
            # RESTORE, like every sibling refusal path (`_revert`, the mint's
            # `_bookkeeping_commit`). Leaving the staged report behind would
            # leave the lane DIRTY — which §5.6 refuses to GC — and would leave
            # a report on disk for a close that did not happen.
            return None, _restore(
                wt, written, "cannot close {}: {}".format(name, refusal)
            )
    code, out = ac.git(
        wt,
        "commit",
        "--no-verify",
        "-m",
        "partial: {} -> partial/ ({})\n\nThe SR-144 outcome: this lane could not finish, so each claimed spec\nmoves to the TERMINAL partial/ and an immutable per-close report lands in\ndocs/handbacks/. The report is the event's identity - the disposition row\nintake mints cites it, so 'is a judgement still owed for THIS close?' is a\npositive-provenance question rather than one of the five reconstructions\nthat leaked. The branch merges like any other; nothing hangs, and nothing\nre-claims a terminal row.".format(
            ", ".join(ids), reason
        ),
    )
    if code != 0:
        return None, "the partial-close commit failed on {}:\n{}".format(
            branch, ac._failure_tail(out)
        )
    print(
        "handback: closed {} as partial from {} ({})".format(
            ", ".join(ids), branch, reason
        )
    )
    return ids, None


# The Deliverable a mechanical adjudication close writes when the row itself has
# not — a valid `## Deliverable` cell that records what happened and points at
# where the successors and any human-owed answer land.
_ADJUDICATION_CLOSE_DELIVERABLE = (
    "Adjudication verdict recorded on the lane; this row is closed MECHANICALLY "
    "at its DONE (OI-70/OI-73). Its `## Dispositions` successors mint at this "
    "row's own merge (drafts-not-mints), the mint replaces the superseded row's "
    "inbound hard edges, and any human-owed answer becomes a `pending` open "
    "item the successor depends on. The verdict artifact is under "
    "`docs/reviews/`."
)


def _adjudication_close_text(text, deliverable):
    """Rewrite an in-`active/` adjudication spec for its terminal close: clear
    `specref` and insert a `## Deliverable` BEFORE the rest of the body (its
    `## Context` and, crucially, its `## Dispositions` section, which the merge
    reads to mint the successors). Idempotent on the Deliverable — a row an
    agent already self-closed keeps its own."""
    fm, body = spec_move_split(text)
    fm = _SPECREF_LINE_RE.sub('specref = ""', fm, count=1)
    if "\n## Deliverable" not in ("\n" + body):
        body = "\n## Deliverable\n\n" + deliverable + "\n" + body
    return "+++\n" + fm + "+++\n" + body


def _consolidation_close(root, wt, branch, src_rel, text, drafts, meta):
    """The CONSOLIDATION arm of the close (the 2026-09-02 restructure plan
    §1.5): enact this verdict's outcome on the queue it judged.
    `(True, None)` enacted, `(False, None)` when the row is not a
    consolidation, `(False, refusal)` otherwise.

    WHAT THIS ARM DOES AND WHAT IT DELIBERATELY LEAVES TO THE MINT. It enacts
    everything that needs no id that does not yet exist: `queue-with-edge`
    writes the hard `needs` edge on the named waiter, `return-to-draft` moves
    the named rows `queued/ -> draft/` with the verdict's finding quoted into
    their Context, and `queue` writes nothing. The absorbed rows' move into
    `archive/work/restructured/` happens at the MINT
    (`intake._archive_absorbed`), for two reasons that both point the same way:
    their whole Deliverable is `Restructured into WI-<successor>.` and the
    successor's id is allocated by `_mint`, which runs at this row's merge; and
    `intake._supersedes_refusal` refuses a `supersedes` naming an ALREADY
    `restructured` row, so archiving them here would make the mint refuse its
    own successor. The rule lives once, in `consolidate`; this is its call site.

    ALL-OR-NOTHING: every refusal is read before the first write
    (`close_refusal` over the trunk registry), so a half-enacted verdict is not
    a state this can reach."""
    record, refusal = consolidate.parse_verdict(text, src_rel)
    if record is None:
        # No `## Consolidation` section: not this arm's case. Every other
        # adjudication brief reads this way, which is what lets one close serve
        # all five.
        return False, refusal
    absorbed = consolidate.absorbed_ids(drafts)
    # THE TRUNK REGISTRY, not the lane's. The lane was cut before this close
    # ran, so its copy of `queued/` is a snapshot: a row another lane claimed
    # in the meantime still reads `queued` there, and the one guard that exists
    # to catch exactly that race would pass on stale bytes.
    rows = ac.read_spec_rows(root / integrate.WORK)
    refusal = consolidate.close_refusal(
        root,
        record,
        absorbed,
        rows,
        src_rel,
        scope=consolidate.scope_of(meta),
        drafts=drafts,
        recorded=str(meta.get("digests") or ""),
    )
    if refusal:
        return False, refusal
    # THE MACHINE LINE AND THE TYPED BLOCK ARE ONE FACT, checked. `absorbs=` and
    # `needs=` are required on every alternative of this brief's verdict grammar
    # and NOTHING read them: a verdict file could say `OUTCOME: QUEUE needs=-
    # absorbs=-` while the block said `consolidate` and three rows were
    # archived. Rather than keep a second unread carrier (or quietly re-spec the
    # plan's own grammar), the close reconciles them and refuses on divergence.
    refusal = _machine_line_refusal(root, wt, branch, record, absorbed, src_rel)
    if refusal:
        return False, refusal
    for waiter, blocker in record["edges"]:
        refusal = _write_edge(wt, waiter, blocker)
        if refusal:
            return False, refusal
    for wid in record["returns"]:
        refusal = _return_to_draft(wt, wid, record["finding"])
        if refusal:
            return False, refusal
    print(
        "handback: consolidation {} -> outcome {} ({} absorbed, {} edge(s), "
        "{} returned)".format(
            meta.get("id") or "?",
            record["outcome"],
            len(absorbed),
            len(record["edges"]),
            len(record["returns"]),
        )
    )
    return True, None


def _lane_verdict(root, wt, branch):
    """The ADJUDICATE verdict file this lane recorded, or None.

    Derived from the branch's own delta against trunk (`git diff --name-only
    <trunk>...<branch> -- docs/reviews/`), not from a path only `agent_loop`
    knows: the close is handed `(root, branch)` and nothing else. The newest by
    name wins, which is the ordering `agent_loop.fresh_verdict_path` builds into
    the filename (session number, then the implementer's HEAD sha)."""
    trunk = ac.trunk_name(root)
    code, out = ac.git(
        root,
        "diff",
        "--name-only",
        "{}...{}".format(trunk, branch),
        "--",
        "docs/reviews",
    )
    if code != 0:
        return None
    names = sorted(
        line.strip()
        for line in out.splitlines()
        if line.strip().endswith(".md") and "-ADJUDICATE-" in line
    )
    for rel in reversed(names):
        path = wt / rel
        if path.is_file():
            return path
    return None


def _machine_line_refusal(root, wt, branch, record, absorbed, where):
    """Refuse when the verdict file's `OUTCOME:` line and the typed
    `## Consolidation` block do not describe the same judgement.

    Both are the session's own output, written minutes apart, and the loop reads
    them for different things — the machine line is what `agent_loop` grades the
    session DONE on, the block is what the close enacts. Two carriers of one
    fact that nothing compares is how a session reports one verdict and the
    machinery performs another; the brief template asserts they cannot disagree,
    so this is that assertion made true.

    A lane with no readable verdict file is NOT refused here: `close_adjudication`
    is called only on a worker's EXIT_DONE, where `agent_loop.worker_endstate`
    has already gated on the verdict, and re-deriving that precondition from a
    git range would turn a fixture or a hand close into a false refusal."""
    path = _lane_verdict(root, wt, branch)
    if path is None:
        return None
    parsed = consolidate.parse_machine_line(path.read_text(encoding="utf-8"))
    if parsed is None:
        return None
    return consolidate.reconcile_refusal(parsed, record, absorbed, where)


def _queued_spec(wt, wi_id):
    """`(path, relpath)` of one QUEUED spec on the lane, or `(None, None)`."""
    queued = wt / integrate.WORK / "queued"
    for path in sorted(queued.glob(wi_id + "-*.md")) if queued.is_dir() else []:
        return path, "{}/queued/{}".format(integrate.WORK, path.name)
    return None, None


def _write_edge(wt, waiter, blocker):
    """QUEUE-WITH-EDGE: the hard `needs` edge the conflict brief promised and
    never got a reader for. A refusal, or None."""
    path, rel = _queued_spec(wt, waiter)
    if path is None:
        return "cannot add the {} -> {} edge: {} is not a queued spec".format(
            waiter, blocker, waiter
        )
    text = path.read_text(encoding="utf-8")
    edged = consolidate.edged_text(text, blocker)
    if edged is None:
        return (
            "cannot add the {} -> {} edge: {} carries no readable `needs` line".format(
                waiter, blocker, rel
            )
        )
    if edged == text:
        print(
            "handback: {} already waits on {} - no edge written".format(waiter, blocker)
        )
        return None
    path.write_text(edged, encoding="utf-8", newline="\n")
    code, out = ac.git(wt, "add", "--", rel)
    return (
        None if code == 0 else "cannot stage {}:\n{}".format(rel, ac._failure_tail(out))
    )


def _return_to_draft(wt, wi_id, finding):
    """RETURN-TO-DRAFT: `queued/ -> draft/` with the finding quoted into the
    row's Context. A refusal, or None.

    Through `spec_move` and not a bare rename, like every other terminal move
    here: the spec changes directory depth, so its own relative links and every
    inbound link to it are part of the same indivisible operation."""
    path, rel = _queued_spec(wt, wi_id)
    if path is None:
        return "cannot return {} to draft: it is not a queued spec".format(wi_id)
    new_text = consolidate.returned_text(path.read_text(encoding="utf-8"), finding)
    dest = "{}/draft/{}".format(integrate.WORK, path.name)
    _touched, refusal = spec_move.move_spec(wt, rel, dest, new_text=new_text)
    return "cannot return {} to draft: {}".format(wi_id, refusal) if refusal else None


def _archive_one_adjudication_row(root, wt, branch, name):
    """Move ONE claimed adjudication spec into `complete/` on the lane —
    `(True, None)` moved, `(False, None)` when the row is not an adjudication
    row at all, `(False, refusal)` otherwise. Nothing is committed here.

    Split out of `close_adjudication` so that function stays a LOOP with a
    commit on the end: everything a single row can be judged on — is it this
    close's business, does its disposition parse, does it owe a successor —
    is one question about one file, and it is asked here.
    """
    import intake  # a sibling reader; deferred so a non-adjudicating run pays nothing

    src_rel = "{}/{}/{}".format(integrate.ACTIVE, branch, name)
    try:
        text = (wt / src_rel).read_text(encoding="utf-8")
        meta = integrate._spec_frontmatter(wt / src_rel)
    except (OSError, ValueError):
        return False, "cannot read the claimed spec {} on {}".format(name, branch)
    if (meta.get("safety_class") or "").strip().lower() != "adjudication":
        # Not this close's case: a non-adjudication DONE lane that did not move
        # its specs is the stall candidate the dispatcher already handles, not a
        # row this mechanical close owns.
        return False, None
    # THE REFUSAL INVARIANT, at the close: a partial/cancelled close MUST queue
    # at least one successor (OI-70/OI-73, no third exit). The signal is
    # `intake.owes_successor` (the durable title prefix), NOT the `brief` cell —
    # the `partial` arm carries `brief = "disposition"` but the `cancelled` arm
    # is brief-LESS by design, so a `brief`-only guard let a cancelled close
    # queue no successor and archive silently. A clean-close spot check owes
    # none and is not caught.
    parsed, drefusal = intake.parse_dispositions(text, src_rel)
    if drefusal:
        return False, "cannot close {}: {}".format(branch, drefusal)
    if intake.owes_successor(meta) and not parsed:
        return False, (
            "{} judged a partial/cancelled close but drafted NO successor in "
            "its ## Dispositions section — such a close must queue at least "
            "one successor (OI-70/OI-73, no third exit). The run stops for a "
            "human to draft the continuation".format(name)
        )
    # THE CONSOLIDATION ARM (restructure plan §1.5), before the row is archived:
    # it acts on the QUEUE this verdict judged, and the guards it runs read the
    # trunk registry, so it must happen while the state it validated still
    # holds. A row with no `## Consolidation` section answers `(False, None)`
    # and every other brief passes straight through.
    _enacted, crefusal = _consolidation_close(
        root, wt, branch, src_rel, text, parsed, meta
    )
    if crefusal:
        return False, "cannot close {}: {}".format(name, crefusal)
    new_text = _adjudication_close_text(text, _ADJUDICATION_CLOSE_DELIVERABLE)
    dest_rel = "{}/complete/{}".format(integrate.WORK, name)
    _touched, refusal = spec_move.move_spec(wt, src_rel, dest_rel, new_text=new_text)
    if refusal:
        return False, "cannot close {}: {}".format(name, refusal)
    return True, None


def close_adjudication(root, branch):
    """Mechanically CLOSE a DONE adjudication row (OI-70/OI-73, Done-when 1).

    The ADJUDICATE session records its verdict and drafts its successors in the
    row's own `## Dispositions` section, but until now NOTHING moved the row
    terminal — the dispatcher resumed a finished adjudication row in a cycle
    until a supervisor closed it by hand (OI-70 decision 21; the C6 loop). This
    is that close, performed by the machinery: the row's spec archives into
    `complete/`, so the drain merges it and `intake._disposition_drafts` mints
    the drafted successors (with the OI edge and the inbound-edge replacement)
    at the merge.

    Returns `(closed WI ids, None)`; `(None, None)` when the claimed row is NOT
    an adjudication row (the caller leaves the DONE lane to its own tree — a
    non-adjudication worker that did not move its specs is the stall candidate,
    not this close); or `(None, refusal)` for the refusal invariant or a close
    failure. THE REFUSAL INVARIANT (OI-73): a row judging a PARTIAL or CANCELLED
    close (told apart from a clean-close spot check by `intake.owes_successor`,
    the durable title signal) that drafted NO successor is refused — such a close
    must queue at least one successor, an OI alone no longer discharges it, and
    there is no third exit.

    The caller invokes this ONLY on a worker's EXIT_DONE, where the verdict is
    already recorded (`agent_loop.worker_endstate` gates DONE on it), so the
    verdict's existence is the caller's precondition, not re-proven here.
    """
    specs = integrate._claimed_specs(root, branch)
    if not specs:
        return None, "trunk holds no claimed specs for {}".format(branch)
    wt, err = _lane(root, branch)
    if err:
        return None, "cannot close {}: {}".format(branch, err)
    specs = open_claimed_specs(wt, branch, specs)
    if not specs:
        # Every claimed row has already left `active/` on the branch, so there
        # is nothing for this close to do — the no-op the docstring promises,
        # never a refusal.
        return None, None
    closed = []
    for wi_id, name in specs:
        moved, refusal = _archive_one_adjudication_row(root, wt, branch, name)
        if refusal or not moved:
            return None, refusal
        closed.append(wi_id)
    code, out = ac.git(
        wt,
        "commit",
        "--no-verify",
        "-m",
        station.mechanical_close_subject(closed)
        + "\n\n"
        "The OI-70/OI-73 adjudication close: the verdict is recorded, so the "
        "machinery archives this row terminal rather than leaving it in active/ "
        "for the dispatcher to resume forever (the C6 loop). Its drafted "
        "successors mint at this row's merge.\n\nWI: {}".format(", ".join(closed)),
    )
    if code != 0:
        return None, "the adjudication-close commit failed on {}:\n{}".format(
            branch, ac._failure_tail(out)
        )
    print(
        "handback: closed adjudication {} -> complete/ from {}".format(
            ", ".join(closed), branch
        )
    )
    return closed, None


def quarantine(root, branch, why):
    """Turn a RED non-merged lane into a BAR-INERT artefact. A refusal, or None.

    Bookkeeping paths are exempt by construction — the spec moves, the close
    report and the log fragments ARE the record being kept, and reverting them
    would revert the close itself. Nothing is lost by the revert either: the
    reverted commits stay reachable in trunk history once the branch merges,
    and the `.patch` is the convenience copy a future WI can apply without
    archaeology.
    """
    wt, err = _lane(root, branch)
    if err:
        return "cannot quarantine {}: {}".format(branch, err)
    code, base = ac.git(root, "merge-base", branch, integrate._head(root))
    if code != 0 or not base.strip():
        return "cannot name {}'s base to revert to: {}".format(branch, base)
    base = base.strip()
    code, raw = _git_stdout(wt, "diff", "--name-status", "-z", base, "HEAD")
    if code != 0:
        return "cannot read {}'s diff against {}".format(branch, base[:10])
    records = diff_records([f for f in raw.split("\0") if f])
    if records is None:
        return (
            "{}'s --name-status stream against {} ends mid-record - the diff "
            "was read short, and quarantining a partial file list would revert "
            "some of the lane and leave the rest live".format(branch, base[:10])
        )
    # A record touching a bookkeeping surface is exempt WHOLE - a rename with
    # one foot in docs/work/ is not something to half-undo.
    changed = [
        (status, paths)
        for status, paths in records
        if not any(p.startswith(BOOKKEEPING) for p in paths)
    ]
    if not changed:
        return (
            "{} changed nothing outside the bookkeeping surfaces, so its red "
            "bar is not its own code to revert - there is nothing to "
            "quarantine and the refusal stands".format(branch)
        )
    # Every path of every record, renames included, so the patch carries the
    # rename rather than half of it.
    paths = [p for _s, record_paths in changed for p in record_paths]
    code, patch = _git_stdout(wt, "diff", base, "HEAD", "--", *paths)
    if code != 0:
        return "cannot render {}'s failing diff as a patch".format(branch)
    refusal = _revert(wt, base, branch, changed)
    if refusal:
        return refusal
    rel = "{}/{}.patch".format(ARTEFACTS, branch)
    dest = wt / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(patch, encoding="utf-8", newline="")
    # Named, not swept: `git rm` and `git checkout <tree-ish> -- <path>` both
    # stage what they did, so the artefact is the only thing left to add.
    code, out = ac.git(wt, "add", "--", rel)
    if code != 0:
        return "cannot stage the quarantine artefact {}:\n{}".format(
            rel, ac._failure_tail(out)
        )
    code, out = ac.git(
        wt,
        "commit",
        "--no-verify",
        "-m",
        "handback: revert {} to a bar-inert artefact\n\nThe §A3 red-close ruling: this lane's code is red and the lane cannot\nfix it, so the code goes back to {} and the failing diff lands as {} -\nin trunk, findable, pickable by a future WI, and unable to red anything.\nThe reverted commits stay reachable in trunk history once this merges.\n\nThe bar said: {}".format(
            branch, base[:10], rel, why
        ),
    )
    if code != 0:
        return "the quarantine commit failed on {}:\n{}".format(
            branch, ac._failure_tail(out)
        )
    print(
        "handback: quarantined {} -> {} ({} path(s) reverted)".format(
            branch, rel, len(paths)
        )
    )
    return None
