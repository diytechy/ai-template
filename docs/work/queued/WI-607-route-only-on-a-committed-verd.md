+++
id = "WI-607"
title = "Route only on a committed verdict: read_verdict parses the file on disk, committed or not (review pack C3)"
workstream = "unattended"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "medium"
priority = 4
safety_class = "ordinary"
+++

## Context

Found by the 2026-09-24 code-facts research; filed by the owner from the
review pack's Part C.

`read_verdict` (`agent_loop.py:1072-1085`) parses the verdict file on disk
whether or not the reviewer committed it, while the merge gate reads committed
round files at the branch tip. The loop can therefore route (approve, re-route,
re-critique) on a verdict the gate cannot see.

Related: the owner's S9 ruling (sister plan §5, 2026-09-24) checks each review
session's committed range and fails the draw on a dirty tree. This row closes
the routing side; design it so the uncommitted verdict cannot be read, rather
than adding a second check beside S9's.

## Done-when

- The loop routes on the verdict as committed on the lane, and an uncommitted
  verdict file is treated as no verdict (the existing failed-draw path).
- A test drives a review session that writes but does not commit its verdict,
  and shows the loop does not route on it.
