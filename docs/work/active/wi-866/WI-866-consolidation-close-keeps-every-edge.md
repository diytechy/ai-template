+++
id = "WI-866"
title = "A consolidation close writes every edge its verdict names, several on one waiter included"
workstream = "process"
specref = "docs/decisions/wi-864.toml"
buildtier = "quick"
safety_class = "ordinary"
priority = 7
+++

## Context

Filed by hand by the coordinator on 2026-10-08. WI-864's consolidation verdict named three edges on one waiter (WI-848 needs WI-852, WI-853 and WI-860); the mechanical close (`handback.close_adjudication`) wrote only the last. `handback._enact_plan` computes each planned write from the spec's on-disk text before any write, so two writes to one file keep only the last (docs/decisions/wi-864.toml D-003; the coordinator restored the lost edges by hand).

## Done-when

- The close's plan composes every edge on one waiter into one write, and any other two planned writes to one file likewise; none is lost.
- A test closes a verdict naming two edges on one waiter and finds both in its `needs`; it fails before the fix.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
