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
judgment admits or refuses a hand merge
(`project-trajectory/PROCESS.md` §3, "When a guard is owed":
a file on disk another process writes). The squash path this row reuses
reads a second git carrier, `SQUASH_MSG`, whose contract is unchanged and is
restated here so the walk's two inputs sit side by side.

**Producers.** Git alone writes both files; the kit writes neither, and no
model output reaches them.
- `MERGE_HEAD`: `git merge` (and `git pull`, which runs it) writes
  `.git/MERGE_HEAD` through git's lock file, committed by rename, so a reader
  sees the whole file or none. A merge stopped on conflicts leaves it for the
  resolving commit; `git merge --abort` and the merge commit remove it. Git
  runs as a local subprocess, so there is no network timeout; a failed or
  killed `git merge` leaves either no file or a whole one. A file that is
  present but does not resolve (hand-edited, or naming a pruned object) is
  the one malformed shape.
- `SQUASH_MSG`: `git merge --squash` writes `.git/SQUASH_MSG` with one
  `commit <40-hex>` header per folded commit, newest first; the squash
  commit removes it, and `git stash` (its reset) deletes it.

**Consumers and rulings** (found by grep for `MERGE_HEAD` and `SQUASH_MSG`
under `project-trajectory/scripts/`):

| Consumer | Role | Absent | Unreadable or malformed | Binds to |
|---|---|---|---|---|
| `acceptance_record.py` `staged_text_then_act_lines`, via `check.py` `_text_then_act_refusal` (CHANGED by this row) | selects the range the hook judges | not a merge: the index is judged against HEAD | present but not resolving, or `HEAD..MERGE_HEAD` not listable (a failed git call): the hook REFUSES the commit, naming `MERGE_HEAD`, and never judges it as a non-merge. Telling present from absent reads `git rev-parse --git-path MERGE_HEAD` for the file, not `--verify` alone. Git would refuse such a merge commit itself after the hook. | HEAD, the resolved `MERGE_HEAD`, and each commit `HEAD..MERGE_HEAD` against its own parents; the merge commit is judged against both parents. An octopus merge's further heads are not read (as `pending_status_moves` states). |
| `acceptance_record.py` `pending_status_moves` (unchanged) | the merge's own status moves for the held-rung check | the index against HEAD | `--verify` fails, so the merge reads as the index against HEAD: every move counts as the commit's own, the held direction (it refuses more, never less) | HEAD and the resolved `MERGE_HEAD` |
| `trace.py` `committed_watermark` (unchanged) | the id watermark baseline: max over HEAD, `MERGE_HEAD` and HEAD's parents, so resolving `--ours` cannot drop the other side's marks | HEAD and its parents only | read as absent; the other side's marks are then compared when the merge commit lands, through `HEAD^2` | the parsed watermark at each rev; None (rule SKIPPED, reported) when git supplies no baseline |
| `trace.py` `committed_corrections` (unchanged) | the watermark's ruled-correction records, longest list per space across the same revs | as above | as above | as above |
| `trunk_step.py` fragment adding-commit lookup (unchanged) | orders log fragments during a merge composition | a fragment with no adding commit on HEAD's side is refused | read as absent, so the same refusal | the fragment's adding commit on HEAD or `MERGE_HEAD` |
| `check.py` `_text_then_act_refusal` reading `SQUASH_MSG` (unchanged) | names the commits a squash folds in, for the squash exemption | no folded commits: the index is judged like any commit | an unreadable file raises and fails the step (the commit is refused); lines not matching `commit <40-hex>` are skipped, and with none left the index is judged and a refusal carries `SQUASH_REBASE_HINT` | the listed tip, admitted only when it contains HEAD and the index's act registries and record are the tip's own (`_squash_lines`) |

`integrate.py` owns the merge slot's per-lane-commit walk and reads neither
file. Under the review threat model (PROCESS.md §6), a hand-forged
`MERGE_HEAD` or `SQUASH_MSG` naming other commits is a tampered host and
owes no guard.

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
