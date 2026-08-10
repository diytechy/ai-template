+++
id = "WI-425"
title = "Repoint the ~71 live source citations of the three SN ids the 2026-08-10 sitting retired (SN-030, SN-031, SN-032) at the SR rows that now carry their obligation. The sitting ruled all three MIS-LEVELLED - each stated a mechanism rather than a need, and each decomposed into 1-3 SRs against a core-need mean of 12.7 - so their rows were deleted and their children re-parented: SR-141/142/143 to SN-025, SR-144/145 to SN-027, SR-146 to SN-005. What the ruling did NOT touch is the ~71 places kit scripts and tests cite the retired ids in comments and docstrings, which now name nothing. This is a live dangling pointer, NOT the case check_doc_refs already blesses: its docstring rules that a HISTORICAL document naming a retired file is accurate history, and that doctrine covers the plan/handoff/log records, which must keep their tokens. It does not cover an explanatory comment in shipped code. METHOD, and most of it is mechanical because the comments self-classify: an SN-030 comment names its rung (rung 1 -> SR-141 dispose-first, rung 3 -> SR-143 queue overlap, rung 6 -> SR-142 red-TC census), and an SN-031 comment names its shape (terminal / per-close report -> SR-144; lineage / successor / disposition -> SR-145). Read each site rather than sedding it: a comment citing the PROGRAM ('the SN-031 program retired X') is history and keeps its token, while one citing the OBLIGATION ('SN-031 LINEAGE: partial work continues by minting a successor') must move to the SR. Leave project-trajectory/EXAMPLE.md alone - its SN-030 is the shipped worked example's own namespace, not this repo's id. NOT a rewrite of the comments themselves: swap the citation, keep the prose."
workstream = "scripts"
specref = "docs/repo-lock.md"
buildtier = "medium"
safety_class = "ordinary"
+++

## Context

Measured at mint time, 2026-08-10 on `infra/mechanized-loop`:

| retired id | kit scripts | kit tests | now carried by |
|---|---|---|---|
| SN-030 | 11 | 4 | SR-141 · SR-142 · SR-143 (under SN-025) |
| SN-031 | 35 | 18 | SR-144 · SR-145 (under SN-027) |
| SN-032 | 1 | 2 | SR-146 (under SN-005) |

**Nothing currently fails on this, and that is the reason it needs a row.**
`check_docs`' SN scan reads the registry to find ids that need a README bullet;
it never validates an `SN-###` token appearing in a `.py` comment. So the tree
stays green while ~71 comments cite ids that no longer exist — the silent-rot
shape the kit exists to prevent, sitting in the kit's own source.

**Why the ids are not being re-minted.** D-4 rules that supersession is deletion
and ids are never reused; the watermark (`docs/id-watermark`) holds `SN = 32`,
so the three numbers stay spent. A future `SN-030` would silently re-point every
one of these comments at a different meaning — which is exactly the hazard the
watermark was built for, and the reason repointing is worth doing while the
mapping is still obvious to a reader.

## Deliverable

The classified list, not just the diff: for each of the ~71 sites, which SR it
moved to — or, for the history-citing ones, why it kept its retired token.
