"""handback.py — the two lane closes that are not a merge (concurrency-v2 §A3).

`integrate.py` owns the ordinary outcome: a lane finishes, its specs land in
`complete/`, the branch merges. This module owns the other two, so that
**every** lane ends in a merge and no branch is ever left hanging:

  hand_back   the HANDBACK outcome. The lane could not finish, so the work so
              far is committed AS-IS and each claimed spec moves back to
              `queued/` carrying a `## Handback` section and a `blockref`. The
              branch then merges like any other, which is the whole point: the
              return is a trunk fact, the partial work is reachable history a
              future WI can pick up, and the run keeps going. This is what
              replaces the `EXIT_NEEDS_HUMAN` run-stop and the parked-branch
              stop — one WI wanting a human used to freeze a walk-away run and
              leave its work where nobody would look.

  quarantine  the RULED red arm (owner decision 1, 2026-07-31). Every outcome
              merges and a merge needs a green bar, so a lane handing back code
              the bar refuses would be the one branch that could still hang.
              The ruling: revert the code, keep the record — the failing diff
              lands as a bar-inert `.patch` under `docs/work/`, the product
              paths go back to what trunk had, and nothing live can red
              anything.

CANCELLED has no function here on purpose. It is a JUDGEMENT — this will never
be built, and here is why — so the lane that makes it writes the move and the
reason itself; only `integrate.branch_outcomes` needs to read it back. What is
mechanised here is what a lane that has already stopped deciding cannot do for
itself.

A one-way sibling of `integrate.py`: this module imports it (for the lane
worktree, the claim read and the sha helpers), never the reverse. `drive.py`
calls both — it decides which outcome a cycle reached, and the writes live here.

No `Contracts:` line, deliberately: the integrator seam this extends is IF-080,
whose row already sits in the interface registry with NO script declaring it —
part of the drift `docs/concurrency-v2.md` §A9.1 hands to the program-close row
(WI-390) rather than to any single builder. Declaring it here, from the sibling
rather than from `scripts/integrate` the row names as its provider, would paper
over that drift instead of recording it.
"""

from __future__ import annotations

import re
import subprocess

import agent_common as ac
import integrate

# Where a quarantined red handback's failing diff lands. Under `docs/work/`
# because that is where the work item's own record lives, and as a `.patch`
# because no bar reads one: the doc checkers discover `*.md`, the stub/dupes
# checks read `src/**/*.py`, and check.py ignores `docs/work/*` outright — so
# the artefact is inert by its extension, not by a rule someone has to keep.
ARTEFACTS = integrate.WORK + "/handback"


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


# The surfaces a revert must never touch: the spec move and the log fragments
# ARE the record being kept, so reverting them would revert the handback itself.
BOOKKEEPING = (integrate.WORK + "/", "docs/log.d/")


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


def _note(branch, reason, span):
    """The `## Handback` section a returned spec carries: what happened, and
    where the work so far is. The commit RANGE is the load-bearing sentence —
    the branch is deleted after its merge, so a future WI's only handle on the
    partial work is trunk history, and naming the range turns "it is in trunk
    somewhere" into a command someone can run."""
    return (
        "\n## Handback\n\n"
        "Returned unfinished from lane `{branch}`: {reason}\n\n"
        "**What remains:** whatever this spec asks for that `{span}` did not "
        "finish. Read that range (`git log --oneline {span}`, `git diff "
        "{span}`) before re-claiming — the work so far is in trunk, not on a "
        "branch. Clearing the `blockref` puts this back on the ready "
        "frontier.\n".format(branch=branch, reason=reason, span=span)
    )


def returned_spec(text, rel, note):
    """`text` rewritten as a RETURNED spec: a `blockref` in the frontmatter and
    `note` as the body's last section. None when it carries no frontmatter.

    The blockref is the spec's OWN new path, which is what both its readers
    want. `schedule._disposition` reads queued+blockref as BLOCKED, so a
    returned WI leaves the ready frontier until a human clears it — without
    that the driver would claim, hand back and re-claim the same WI forever —
    and the pending projection renders the ref as the pointer to go read. A
    spec that already declares one keeps it.
    """
    m = re.match(r"(\+\+\+\n)(.*?)(\n\+\+\+\n)", text, re.S)
    if m is None:
        return None
    front = m.group(2)
    if not re.search(r"^blockref\s*=", front, re.M):
        front += '\nblockref = "{}"'.format(rel)
    body = text[m.end() :].rstrip("\n")
    return m.group(1) + front + m.group(3) + (body + "\n" if body else "") + note


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
    """`<merge-base>..<branch tip>` in short shas — the range the returned spec
    names as the home of the work so far."""
    code, base = ac.git(root, "merge-base", branch, integrate._head(root))
    return "{}..{}".format(
        (base.strip() or "")[:10] if code == 0 else "(trunk)",
        (integrate._rev(root, branch) or "")[:10],
    )


def hand_back(root, branch, reason):
    """Close `branch` on the HANDBACK outcome. `(returned WI ids, None)`, or
    `(None, refusal)`.

    Two deliberate choices. The as-is commit skips the commit hook, because
    "as-is" has to mean it: the branch's own §A2 refresh regenerates and BARS
    this tree before anything merges, so a hook refusal here would only trade a
    merge that is checked for a branch that hangs. And the specs go back to
    `queued/` rather than staying claimed, because `active/<branch>/` is what
    the dispatcher reads as "a lane is building this" — leaving them there
    would hand the WI back to nobody.
    """
    specs = integrate._claimed_specs(root, branch)
    if not specs:
        return None, "trunk holds no claimed specs for {}".format(branch)
    wt, err = _lane(root, branch)
    if err:
        return None, "cannot hand back {}: {}".format(branch, err)
    ids = [wi_id for wi_id, _name in specs]
    if ac.working_tree_dirty(wt):
        ac.git(wt, "add", "-A")
        code, out = ac.git(
            wt,
            "commit",
            "--no-verify",
            "-m",
            "{}: the work so far, committed as-is (handback)\n\n{}".format(
                ", ".join(ids), reason
            ),
        )
        if code != 0:
            return None, "the as-is work commit failed on {}:\n{}".format(
                branch, ac._failure_tail(out)
            )
    note = _note(branch, reason, _span(root, branch))
    for _wi_id, name in specs:
        rel = "{}/queued/{}".format(integrate.WORK, name)
        src = wt / integrate.ACTIVE / branch / name
        try:
            returned = returned_spec(src.read_text(encoding="utf-8"), rel, note)
        except OSError as exc:
            return None, "cannot read the claimed spec {}: {}".format(name, exc)
        if returned is None:
            return None, "{}: no +++ frontmatter - refusing to return it".format(name)
        dst = wt / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(returned, encoding="utf-8", newline="\n")
        ac.git(wt, "rm", "-q", "--", "{}/{}/{}".format(integrate.ACTIVE, branch, name))
        ac.git(wt, "add", "--", rel)
    code, out = ac.git(
        wt,
        "commit",
        "--no-verify",
        "-m",
        "handback: {} -> queued/ ({})\n\nThe §A3 handback outcome: this lane could not finish, so the WI goes back\nto the queue IN TRUNK - blocked on a blockref, its `## Handback` section\nnaming what remains and where the partial work is. The branch merges like\nany other; nothing hangs.".format(
            ", ".join(ids), reason
        ),
    )
    if code != 0:
        return None, "the handback commit failed on {}:\n{}".format(
            branch, ac._failure_tail(out)
        )
    print("handback: returned {} from {} ({})".format(", ".join(ids), branch, reason))
    return ids, None


def quarantine(root, branch, why):
    """Turn a RED non-merged lane into a BAR-INERT artefact. A refusal, or None.

    Bookkeeping paths are exempt by construction — the spec moves and the log
    fragments ARE the record being kept, and reverting them would revert the
    handback itself. Nothing is lost by the revert either: the reverted commits
    stay reachable in trunk history once the branch merges, and the `.patch` is
    the convenience copy a future WI can apply without archaeology.
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
        "handback: revert {} to a bar-inert artefact\n\nThe §A3 red-handback ruling: this lane's code is red and the lane cannot\nfix it, so the code goes back to {} and the failing diff lands as {} -\nin trunk, findable, pickable by a future WI, and unable to red anything.\nThe reverted commits stay reachable in trunk history once this merges.\n\nThe bar said: {}".format(
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
