+++
id = "WI-610"
title = "Reconcile OI-76's ruling text with where the code puts the Review-Verdict trailer (review pack C6)"
workstream = "process"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

## Context

Found by the 2026-09-24 code-facts research; filed by the owner from the
review pack's Part C.

OI-76's ruling says the `Review-Verdict` trailer rides "the round's own
commit" (`docs/log.md:54643-54656`). The code puts it on the commit that
RECORDS the round, written by the coordinator, never by a session, and says so
(`kitlib/verdict.py:70-71`). One statement has to move. The ruling text is the
owner's, so the choice is the owner's: amend the ruling's wording to the code,
or change the code to the ruling. The owner's S9 ruling (2026-09-24) keeps
reviewers committing their own verdict files, which bears on the choice.

## Done-when

- The owner's choice is recorded: surfaced as an open item with both options
  unless the owner has already ruled.
- The chosen side is changed, so one statement of where the trailer rides
  remains, and the other side cites it.
