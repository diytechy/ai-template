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

### Re-affirm, take 2 (2026-08-11)

The first Re-affirm paragraph below landed in the SAME commit as the
`queued/` -> `active/` move, so git's own rename detection read the pair as
one `R` status; `--diff-filter=AM` (the row-clock's own row-history mode)
drops a rename whatever else the commit did (WI-362's documented blind spot),
so the clock did not move. This paragraph is a content edit at the row's now
STABLE path, no rename riding along, which is what actually clears the warn.

`check_trajectory`'s backlog-staleness warn compares this row's own last-touched
commit against its SpecRef (`docs/repo-lock.md`); the row was minted at
`14925426` (2026-08-10) and repo-lock has moved four times since
(`cb7c27a5`, `da90b487`, `bb69a622`, `f1b4e0a8`, the last landing the D-5
carrier cutover). None of that movement touches this row's premise: repo-lock's
§8.4/D-5 material is the carrier migration and the queued sitting record, not
the SN-030/031/032 retirement or the SR-141…146 re-parenting this row repoints
against — that ruling is already landed on the spine
(`docs/requirements/system-requirements.toml`), independently verified below
before any site is touched. This content edit is the re-affirmation the clock
asks for.

## Deliverable

The classified list, not just the diff: for each of the ~71 sites, which SR it
moved to — or, for the history-citing ones, why it kept its retired token.
