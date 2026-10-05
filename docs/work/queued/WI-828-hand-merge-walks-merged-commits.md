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

## Done-when

- A commit that is a merge in progress (MERGE_HEAD present) is judged at the hook
  on every commit HEAD..MERGE_HEAD against its parents, as the squash landing's
  squashed commits are, reusing the one text-then-act function.
- Tests: a hand merge of a side branch with a mixed commit is refused at the hook;
  a hand merge of a clean side branch passes; the refresh-merge cases stay green.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
