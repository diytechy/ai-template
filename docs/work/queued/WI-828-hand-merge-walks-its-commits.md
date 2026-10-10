+++
id = "WI-828"
title = "A hand merge on trunk judges the commits it brings in, as the squash landing does"
workstream = "process"
sr_refs = ["SR-140"]
specref = "docs/reviews/wi-806-text-then-act/004-ADJUDICATE-44c9ddf.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the wave-15 coordinator on 2026-10-05 from the independent
adjudicator's separate finding at WI-806 (`docs/reviews/wi-806-text-then-act/`,
the 003/004 sitting): on trunk, a hand `git merge` of a side branch holding a
commit made with `--no-verify` that mixes spine text with the approval act passes
the pre-commit hook (exit 0). The squash landing walks the squashed commits
(each judged against its parents); the merge path judges only the merge commit,
which counts what neither parent carried, so a mixed commit behind the merge's
second parent is never judged at the hook. The merge slot's per-lane-commit walk
catches it for a lane landed through the integrator, so this opens no sanctioned
path; it closes the hand-merge route the coordinator does not use but an adopter
might.

## Trust

`MERGE_HEAD` gains authority at the hook: it selects the commits whose
judgment admits or refuses a hand merge (`project-trajectory/PROCESS.md` §3,
"When a guard is owed": a file on disk another process writes).

- **Producer:** git itself, through `git merge` (and `git pull`, which runs
  it), writing `.git/MERGE_HEAD` through its own lock file before the merge
  commit is made. The kit never writes it. A merge that fails or stops on
  conflicts leaves it in place for the resolving commit; `git merge --abort`
  removes it.
- **Consumers** (found by grep for `MERGE_HEAD` under
  `project-trajectory/scripts/`), every one reading it through
  `git rev-parse --verify MERGE_HEAD`, never as a file:
  - `acceptance_record.py` `staged_text_then_act_lines` (via `check.py`'s
    text-then-act step): the reader that gains the range authority.
  - `acceptance_record.py` `pending_status_moves`, `trace.py` (the merge's own
    status moves and conflict reads) and `trunk_step.py` (fragment
    composition): unchanged by this row.
  - `check.py` reads `SQUASH_MSG` for the squash path this row reuses;
    `integrate.py` owns the merge slot's per-lane-commit walk. Neither
    carrier's contract changes.
- **Ruling:**
  - *Absent* (`rev-parse` resolves nothing): not a merge; the index is
    judged against HEAD as today.
  - *Present and resolving to a commit:* the authority binds to HEAD and
    that commit, and to every commit `HEAD..MERGE_HEAD` judged against its
    own parents. An octopus merge's further heads are not read, as
    `pending_status_moves` already states; the merge commit itself is still
    judged against both parents.
  - *Present but not resolving* (unreadable or malformed): the hook refuses
    the commit, naming `MERGE_HEAD`, rather than judging it as a non-merge.
    Git would refuse that commit itself after the hook, so the refusal costs
    nothing and keeps the walk from reading a merge as plain.
  - A walk that cannot list `HEAD..MERGE_HEAD` (a failed git call) refuses
    the commit; it never admits the merge unjudged.
  - Under the review threat model (PROCESS.md §6), a hand-forged
    `MERGE_HEAD` naming another commit is a tampered host and owes no guard.

## Done-when

- A commit that is a merge in progress (MERGE_HEAD present) is judged at the hook
  on every commit HEAD..MERGE_HEAD against its parents by the hook's one
  lane-commit walk, the walk the squash landing already uses, with text-then-act
  as its first rider, so later per-commit checks ride the same walk.
- LLR-302's detail and a TC are amended to state the walk, authored with the code
  and judged at the lane's checkpoint.
- Tests: a hand merge of a side branch with a mixed commit is refused at the hook;
  a hand merge of a clean side branch passes; the refresh-merge cases stay green.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
