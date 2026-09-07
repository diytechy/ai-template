"""Stage the primary-only adjudication close without coordinator imports."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import agent_common as ac
import consolidate
import spec_move

WORK = "docs/work"
_SPECREF_LINE_RE = re.compile(r"(?m)^specref\s*=\s*.*$")


def spec_move_split(text):
    lines = text.split("\n")
    if not lines or lines[0] != "+++" or "+++" not in lines[1:]:
        raise ValueError("no closed +++ frontmatter fence")
    close = lines.index("+++", 1)
    return "\n".join(lines[1:close]) + "\n", "\n".join(lines[close + 1 :])


def _spec_frontmatter(path):
    frontmatter, _body = spec_move_split(path.read_text(encoding="utf-8"))
    return tomllib.loads(frontmatter)


# The Deliverable a mechanical adjudication close writes when the row itself has
# not — a valid `## Deliverable` cell that records what happened and points at
# where the successors and any human-owed answer land.
_ADJUDICATION_CLOSE_DELIVERABLE = (
    "The held primary adjudication recorded and independently reviewed its "
    "judgment. The verified atomic publisher closed this queued row and minted "
    "its recorded `## Dispositions` successors in the same primary commit; any "
    "human-owed answer is a `pending` open item the successor depends on. The "
    "judgment and review evidence remain under `docs/reviews/`."
)


def _adjudication_close_text(text, deliverable):
    """Rewrite a turn-bound queued adjudication spec for its terminal close: clear
    `specref` and insert a `## Deliverable` BEFORE the rest of the body (its
    `## Context` and, crucially, its `## Dispositions` section, which the merge
    reads to mint the successors). Idempotent on the Deliverable — a row an
    agent already self-closed keeps its own."""
    fm, body = spec_move_split(text)
    fm = _SPECREF_LINE_RE.sub('specref = ""', fm, count=1)
    if "\n## Deliverable" not in ("\n" + body):
        body = "\n## Deliverable\n\n" + deliverable + "\n" + body
    return "+++\n" + fm + "+++\n" + body


def _consolidation_close(
    root, wt, branch, src_rel, text, drafts, meta, judgment_path=None
):
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
    rows = ac.read_spec_rows(root / WORK)
    # A primary adjudication remains queued until this atomic close. The
    # consolidation digest was recorded immediately before that judge row was
    # minted, so exclude the selected carrier itself just as the retired claim
    # move excluded it from queued/ while preserving every subject row.
    if src_rel.startswith(WORK + "/queued/"):
        rows = [row for row in rows if row.get("WI-ID") != meta.get("id")]
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
    if record["outcome"] == "consolidate":
        for draft in drafts:
            draft["consolidated"] = True
    # THE MACHINE LINE AND THE TYPED BLOCK ARE ONE FACT, checked. `absorbs=` and
    # `needs=` are required on every alternative of this brief's verdict grammar
    # and NOTHING read them: a verdict file could say `OUTCOME: QUEUE needs=-
    # absorbs=-` while the block said `consolidate` and three rows were
    # archived. Rather than keep a second unread carrier (or quietly re-spec the
    # plan's own grammar), the close reconciles them and refuses on divergence.
    refusal = _machine_line_refusal(
        root, wt, branch, record, absorbed, src_rel, judgment_path=judgment_path
    )
    if refusal:
        return False, refusal
    # PLAN, THEN APPLY. Both loops used to write one target at a time and could
    # refuse mid-way: a two-edge verdict whose SECOND waiter carried no readable
    # `needs` line left the first waiter's spec rewritten AND STAGED on the lane,
    # reported nowhere, to be committed by whatever committed next - even if the
    # verdict was then withdrawn. That is the half-enacted state this function's
    # own docstring says is unreachable, so it is now unreachable: every target
    # is resolved to a readable, rewritable queued spec BEFORE the first write.
    plan, refusal = _enact_plan(wt, record)
    if refusal:
        return False, refusal
    refusal = _apply_plan(wt, plan)
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
    if not branch:
        found = sorted((Path(wt) / "docs" / "reviews").glob("*-ADJUDICATE-*.md"))
        return found[-1] if found else None
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


def _machine_line_refusal(
    root, wt, branch, record, absorbed, where, judgment_path=None
):
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
    if judgment_path is not None:
        path = Path(wt) / judgment_path
        if not path.is_file():
            return "the bound primary judgment is absent: {}".format(judgment_path)
    elif not branch:
        return "a primary consolidation close requires its bound judgment path"
    else:
        path = _lane_verdict(root, wt, branch)
    if path is None:
        return None
    parsed = consolidate.parse_machine_line(path.read_text(encoding="utf-8"))
    if parsed is None:
        return None
    return consolidate.reconcile_refusal(parsed, record, absorbed, where)


def _queued_spec(wt, wi_id):
    """`(path, relpath)` of one QUEUED spec on the lane, or `(None, None)`."""
    queued = wt / WORK / "queued"
    for path in sorted(queued.glob(wi_id + "-*.md")) if queued.is_dir() else []:
        return path, "{}/queued/{}".format(WORK, path.name)
    return None, None


def _enact_plan(wt, record):
    """`([(kind, ...)], None)` - every write this verdict owes, resolved and
    validated - or `([], refusal)` naming the first target that cannot be
    written. NOTHING is written here.

    The same preflight-then-act shape `consolidate._archive_plan` uses on the
    absorbed rows, for the same reason and bought by the same class of defect.
    Order is preserved so the apply half is a straight walk."""
    plan = []
    for waiter, blocker in record["edges"]:
        path, rel = _queued_spec(wt, waiter)
        if path is None:
            return [], (
                "cannot add the {} -> {} edge: {} is not a queued spec on this "
                "lane; nothing written".format(waiter, blocker, waiter)
            )
        text = path.read_text(encoding="utf-8")
        edged = consolidate.edged_text(text, blocker)
        if edged is None:
            return [], (
                "cannot add the {} -> {} edge: {} carries no readable `needs` "
                "line; nothing written".format(waiter, blocker, rel)
            )
        plan.append(("edge", path, rel, edged, waiter, blocker))
    for wid in record["returns"]:
        path, rel = _queued_spec(wt, wid)
        if path is None:
            return [], (
                "cannot return {} to draft: it is not a queued spec on this "
                "lane; nothing written".format(wid)
            )
        new_text = consolidate.returned_text(
            path.read_text(encoding="utf-8"), record["finding"]
        )
        dest = "{}/draft/{}".format(WORK, path.name)
        plan.append(("return", path, rel, new_text, dest, wid))
    return plan, None


def _apply_plan(wt, plan):
    """Enact a validated `_enact_plan`, or RESTORE the lane and refuse.

    The preflight makes a mid-walk refusal unreachable through the causes it
    checks; the restore is for the ones it cannot (a `spec_move` link rewrite
    that fails, a filesystem that goes away). `git checkout -- docs/work` plus
    `git reset -- docs/work` returns both the worktree and the index to the
    lane's own HEAD, which is exactly the state the close started from: nothing
    else has written under `docs/work` by this point, because the absorbed rows
    are archived at the MINT and this row's own spec moves after."""
    for entry in plan:
        kind = entry[0]
        if kind == "edge":
            _kind, path, rel, edged, waiter, blocker = entry
            path.write_text(edged, encoding="utf-8", newline="\n")
            code, out = ac.git(wt, "add", "--", rel)
            refusal = (
                None
                if code == 0
                else "cannot stage {}:\n{}".format(rel, ac._failure_tail(out))
            )
        else:
            _kind, _path, rel, new_text, dest, wid = entry
            _touched, refusal = spec_move.move_spec(wt, rel, dest, new_text=new_text)
            if refusal:
                refusal = "cannot return {} to draft: {}".format(wid, refusal)
        if refusal:
            _restore_lane_work(wt)
            return (
                refusal + " (the lane's docs/work was restored; this verdict enacted"
                " nothing)"
            )
    return None


def _restore_lane_work(wt):
    """Put the lane's `docs/work` back to its own HEAD, worktree and index."""
    ac.git(wt, "checkout", "--", WORK)
    ac.git(wt, "reset", "-q", "--", WORK)


def stage_primary_adjudication(root, spec_rel, judgment_path=None):
    """Stage one queued adjudication close on primary; never commit.

    Returns ``(closed_ids, drafts, refusal)``.  The caller supplies the exact
    turn-bound queued path, avoiding every branch/claim discovery seam.
    """
    from pathlib import Path
    import intake

    root = Path(root)
    path = root / spec_rel
    try:
        text = path.read_text(encoding="utf-8")
        meta = _spec_frontmatter(path)
    except (OSError, ValueError) as exc:
        return None, None, "cannot read {}: {}".format(spec_rel, exc)
    wi = str(meta.get("id") or "")
    if not wi or "/queued/" not in "/" + str(spec_rel).replace("\\", "/"):
        return None, None, "primary close requires the bound queued WI spec"
    if str(meta.get("safety_class") or "").lower() != "adjudication":
        return None, None, "{} is not adjudication-class".format(wi)
    drafts, refusal = intake.parse_dispositions(text, spec_rel)
    if refusal:
        return None, None, refusal
    if intake.owes_successor(meta) and not drafts:
        return None, None, "{} owes a successor".format(wi)
    drafts = [
        intake._disposition_draft(root, draft, meta, wi, spec_rel) for draft in drafts
    ]
    _done, refusal = _consolidation_close(
        root,
        root,
        "",
        spec_rel,
        text,
        drafts,
        meta,
        judgment_path=judgment_path,
    )
    if refusal:
        return None, None, refusal
    closed = _adjudication_close_text(text, _ADJUDICATION_CLOSE_DELIVERABLE)
    dest = "docs/archive/work/complete/{}".format(path.name)
    _touched, refusal = spec_move.move_spec(root, spec_rel, dest, new_text=closed)
    return ([wi], drafts, None) if not refusal else (None, None, refusal)
