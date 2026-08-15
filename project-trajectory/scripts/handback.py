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

A one-way sibling of `integrate.py`: this module imports it (for the lane
worktree, the claim read and the sha helpers), never the reverse. `dispatch.py`
calls both — it decides which outcome a cycle reached, and the writes live here.

No `Contracts:` line, deliberately: the integrator seam this extends is IF-080,
whose row already sits in the interface registry with NO script declaring it —
part of the drift `docs/concurrency-v2.md` §A9.1 hands to the program-close row
rather than to any single builder. Declaring it here, from the sibling rather
than from `scripts/integrate` the row names as its provider, would paper over
that drift instead of recording it.
"""

from __future__ import annotations

import re
import subprocess

import agent_common as ac
import integrate
import spec_move

# Where a quarantined red close's failing diff lands. Under `docs/work/` because
# that is where the work item's own record lives, and as a `.patch` because no
# bar reads one: the doc checkers discover `*.md`, the stub check reads
# `src/**/*.py`, and check.py ignores `docs/work/*` outright — so the artefact is
# inert by its extension, not by a rule someone has to keep.
ARTEFACTS = integrate.WORK + "/handback"

# THE PER-CLOSE REPORT'S HOME, and the one constraint that fixes it.
# `agent_common.spec_files` is `work_dir.rglob("WI-*.md")` filtered only on "not
# directly in work_dir" — so a report at `docs/work/handbacks/WI-413-x.md` WOULD
# be walked, `parse_spec_status("handbacks")` would raise, and `read_spec_rows`
# would SILENTLY SKIP it, while `intake.next_wi_id` counted its id as taken.
# That is the invisible-spec trap that earned `draft/` its declaration. Putting
# the reports outside `docs/work/` entirely avoids the question.
REPORTS = "docs/handbacks"

# The claimed outcomes a lane may assert. `complete` is here for completeness of
# the vocabulary — a clean finish needs no report and never reaches this module —
# so that the report schema names every state rather than only the sad ones.
CLAIMED_OUTCOMES = ("complete", "partial", "cancelled")

# The review tier a close SUGGESTS for its disposition — a TYPED field, which is
# the whole point. Before LLR-161 this rode as the magic substring `NEEDS-HUMAN`
# inside a free-prose reason, and `tier_signal` case-folded a search for it: so
# `NEEDS_HUMAN`, `needs human`, or a typo silently downgraded the judgement, with
# no constant, no validation and no refusal on a miss. Prose that carries control
# flow must be a typed field.
SUGGESTED_TIERS = ("quick", "medium", "strong")

# WHO DECIDES THE KEEP/DISCARD SPLIT, and the reason this is a field rather than
# an assumption. A `partial` close merges its work-so-far onto trunk, and on
# 2026-08-03 that merged code a lane had REJECTED, because nothing had asked
# which commits should survive. The rung that answers it has to hold for BOTH
# closers, and they know different things:
#
#   "lane"        the closing party judged its own work and says which commits
#                 to keep. `keep_commits` / `discard_commits` are authoritative.
#   "adjudicator" the closer COULD NOT judge — the dispatcher closing a lane
#                 whose worker exited or crashed has no view of the work at all.
#                 The split is explicitly OWED, and the disposition row minted
#                 for this close is what owes it.
#
# What is refused is a report that declares NEITHER: silence about the split is
# how the incident happened, and "I could not judge" is a different statement
# from saying nothing. Both are actionable; only silence is not.
SPLIT_DECIDERS = ("lane", "adjudicator")

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


# --- the per-close report ------------------------------------------------------


def report_path(branch, wi_id):
    """The repo-relative path of one close's report.

    `<wi>-<branch>.md`, and that pair is the EVENT IDENTITY the old contract
    lacked. It is well-defined because a WI is claimed on exactly one branch at
    a time and `partial/` is terminal, so the same (wi, branch) pair cannot
    close twice; and it is STABLE, which is what lets a disposition's dedup be
    "does a disposition citing this report exist?" — a positive-provenance
    question — instead of the five reconstructions that leaked."""
    return "{}/{}-{}.md".format(REPORTS, wi_id, branch)


def render_report(wi_id, branch, claimed_outcome, reason, span, fields=None):
    """The report TEXT: TOML frontmatter carrying every typed field, then the
    prose sections a human reads.

    Typed, not prose, for the fields anything downstream keys off — the
    disposition's review tier reads `suggested_tier`, not a substring of
    `reason`. `keep_commits` / `discard_commits` exist because a green handback
    once merged REJECTED code onto trunk as-is (2026-08-03, live): under this
    contract a `partial` close must say which commits are keep and which are
    discard, and the integrator refuses one that does not. The revert decision
    becomes the adjudicator's explicit call instead of a hand cleanup.
    """
    fields = dict(fields or {})
    tier = fields.pop("suggested_tier", "medium")
    if tier not in SUGGESTED_TIERS:
        tier = "medium"
    keep = fields.pop("keep_commits", [])
    discard = fields.pop("discard_commits", [])
    decider = fields.pop(
        "split_decided_by", "lane" if (keep or discard) else "adjudicator"
    )
    if decider not in SPLIT_DECIDERS:
        decider = "adjudicator"
    delivered = fields.pop("delivered", "")
    not_delivered = fields.pop("not_delivered", "")
    front = [
        "+++",
        'wi = "{}"'.format(wi_id),
        'branch = "{}"'.format(branch),
        'claimed_outcome = "{}"'.format(claimed_outcome),
        "reason = {}".format(_toml_str(reason)),
        'commit_range = "{}"'.format(span),
        'suggested_tier = "{}"'.format(tier),
        "keep_commits = [{}]".format(", ".join(_toml_str(c) for c in keep)),
        "discard_commits = [{}]".format(", ".join(_toml_str(c) for c in discard)),
        'split_decided_by = "{}"'.format(decider),
        "+++",
    ]
    body = [
        "",
        "## What happened",
        "",
        "Lane `{}` closed `{}` as **{}**: {}".format(
            branch, wi_id, claimed_outcome, reason
        ),
        "",
        "The work so far is in trunk, not on a branch — the lane merges like any",
        "other. Read it with `git log --oneline {span}` / `git diff {span}`.".format(
            span=span
        ),
        "",
        "## Delivered",
        "",
        delivered or "_(the close named nothing as delivered)_",
        "",
        "## Not delivered",
        "",
        not_delivered or "_(the close named nothing as outstanding)_",
        "",
        "## Keep / discard",
        "",
        _split_lines(keep, discard, decider),
        "",
    ]
    return "\n".join(front + body)


def _toml_str(value):
    """A TOML basic string — the reason is free prose and may carry quotes."""
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    text = text.replace("\n", " ").replace("\r", " ")
    return '"{}"'.format(text)


def _split_lines(keep, discard, decider):
    lines = []
    for label, commits in (("keep", keep), ("discard", discard)):
        lines.append("- **{}**: {}".format(label, ", ".join(commits) or "(none)"))
    lines.append("- **decided by**: {}".format(decider))
    if decider == "adjudicator":
        lines.append("")
        lines.append(
            "The closing party could not judge this work — a dispatcher closing "
            "a lane whose worker exited or crashed has no view of it. The split "
            "is therefore OWED, and the disposition row minted for this close is "
            "what owes it: read the commit range, decide which commits survive, "
            "and mint a corrective successor for anything that should not."
        )
    return "\n".join(lines)


_FRONT_RE = re.compile(r"\+\+\+\n(.*?)\n\+\+\+", re.S)


def read_report(path):
    """One report's frontmatter as a dict, or None when it is unreadable or
    carries no `+++` block. Read with the same TOML parser every spec uses."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    match = _FRONT_RE.search(text)
    if match is None:
        return None
    data = ac.read_toml_text(match.group(1))
    return data if isinstance(data, dict) else None


def report_refusal(meta):
    """Why a report is not actionable, or None.

    The integrator's rung: a `partial` close whose report omits the keep/discard
    split refuses the MERGE. That is deliberately strict — the alternative is
    the live defect this contract closes, where a close merged rejected code
    onto trunk because nobody had said which commits were which."""
    if not isinstance(meta, dict):
        return "the close report is missing or has no +++ frontmatter"
    outcome = str(meta.get("claimed_outcome") or "").strip()
    if outcome not in CLAIMED_OUTCOMES:
        return "the close report claims outcome {!r}, not one of {}".format(
            outcome, "/".join(CLAIMED_OUTCOMES)
        )
    if outcome == "partial":
        decider = str(meta.get("split_decided_by") or "").strip()
        declared = bool(meta.get("keep_commits") or meta.get("discard_commits"))
        if not declared and decider not in SPLIT_DECIDERS:
            return (
                "the `partial` close report is SILENT about the keep/discard "
                "split — no keep_commits, no discard_commits, and no "
                "split_decided_by. A close that says nothing about which of its "
                "commits should survive leaves the revert decision to a hand "
                "cleanup, which is exactly how a rejected diff once merged onto "
                'trunk as-is. Declaring split_decided_by = "adjudicator" is a '
                "valid answer — the disposition row then owes it; saying "
                "nothing is not"
            )
    return None


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
    ids = [wi_id for wi_id, _name in specs]
    if ac.working_tree_dirty(wt):
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
            return None, "the as-is work commit failed on {}:\n{}".format(
                branch, ac._failure_tail(out)
            )
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
        # is the artifact-less return this contract exists to end.
        rep_rel = report_path(branch, wi_id)
        dest = wt / rep_rel
        # IMMUTABLE MEANS IMMUTABLE. The report IS the close event's identity,
        # and an identity that can be overwritten is a mutable proxy again —
        # the exact shape five dedup mechanisms died on. A second close of the
        # same (wi, branch) is not a thing this contract permits (`partial/` is
        # terminal), so meeting one means something upstream is wrong and the
        # honest act is to refuse rather than to rewrite the record of the
        # first close.
        if dest.exists():
            return None, _restore(
                wt,
                written,
                "a close report already exists at {} - the report is the close "
                "EVENT's immutable identity, so a second close of {} on {} is "
                "refused rather than overwriting it".format(rep_rel, wi_id, branch),
            )
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
