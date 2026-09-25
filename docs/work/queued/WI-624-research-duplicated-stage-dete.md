+++
id = "WI-624"
title = "Research duplicated-stage detection: call-sequence and near-miss methods, measured against past consolidations (S14)"
workstream = "research"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#41-minimizing-the-number-of-expressed-operations-note-3"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
+++

## Context

Ruled by the owner 2026-09-24 (sister plan S14, §4.1): researched before
anything is built. The owner's goal: when two modules process A->B->C and
A->B->D, bring A->B out unless it is very small.

`check_dupes_census.py` hashes whole function bodies, so a shared prefix inside
two different functions is invisible to it, and exact matching misses small
deviations; D-7 found 93% of the old gate's findings were accepted idioms. The
pass builds a ground truth from past consolidation findings (WI-448's
duplicates, the redesign's consolidations) and measures recall and noise for
call-sequence fingerprints (the ordered operations a function invokes) and for
near-miss similarity over normalized AST or token windows. It designs a
judged-once ledger, so an accepted idiom is never raised again. Stdlib options
are preferred; a dependency needs a ledger row.

## Done-when

- A written result under `docs/plans/`: the ground-truth set, each method's
  recall and noise on it, and a recommendation for the owner.
- Any prototype stays out of the gate and the commit bar.
- No detector is adopted by this item; adoption is the owner's ruling on the
  result.
