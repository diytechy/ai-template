+++
id = "WI-689"
title = "adjudicate queue overlap [af589a4f5319]: WI-615;WI-616;WI-620;WI-651;WI-655;WI-657;WI-667"
workstream = "process"
specref = ""
buildtier = "strong"
priority = 9
safety_class = "adjudication"
brief = "consolidate"
adjudicates = ["WI-615", "WI-616", "WI-620", "WI-651", "WI-655", "WI-657", "WI-667"]
digests = "af589a4f5319|edd7832b0dd6"
+++

## Deliverable

Adjudication verdict recorded on the lane; this row is closed MECHANICALLY at its DONE (OI-70/OI-73). Its `## Dispositions` successors mint at this row's own merge (drafts-not-mints), the mint replaces the superseded row's inbound hard edges, and any human-owed answer becomes a `pending` open item the successor depends on. The verdict artifact is under `docs/reviews/`.

## Context

Minted by the CONSOLIDATION CENSUS (the 2026-09-02 backlog-restructure plan §1.3), which runs from an idle station with no judgement in progress and none queued over these rows or ahead of this one. The candidate cluster is 7 queued row(s): WI-615;WI-616;WI-620;WI-651;WI-655;WI-657;WI-667.

The mechanical pre-filter selected them; it has concluded NOTHING. Each line below is a hint a string comparison can produce, and two rows deliberately cut from one plan share its path and always will:

> WI-615 and WI-655 are both open and share one spec of record (docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md#11-staging)
> WI-615 and WI-655 were commissioned by the same docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md
> WI-615 and WI-657 both touch gen_skills_index.py
> WI-616 and WI-620 were commissioned by the same docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md
> WI-616 and WI-651 both touch trace.py
> WI-616 and WI-655 both touch trace.py
> WI-616 and WI-667 both touch trace.py
> WI-651 and WI-655 both touch trace.py
> WI-651 and WI-667 both touch acceptance_record.py;trace.py
> WI-655 and WI-667 both touch trace.py

This row's `Adjudicates` cell fixes the population — judge those rows and no others. Its `Digests` cell is `af589a4f5319|edd7832b0dd6`: the queue state and the spine state this question was asked against, so the census never asks it twice and a verdict that has gone stale is detectable rather than assumed fresh.

## Consolidation

```toml
outcome = "queue-with-edge"
edges = ["WI-655 needs WI-616"]
```

Judged 2026-09-27 at e26e22aa; verdict at `docs/reviews/wi-689-adjudicate-queue-overlap-af58/001-ADJUDICATE-e26e22a.md`. One real collision: WI-616's absolutes sweep rewrites the same approved SR rows WI-655's C2 gives `da_refs`, `coincident` and re-pointed `boundary_refs`, and the sweep's list of open-world absolutes is C2's declared input, so WI-655 waits. Every other pair is separate work that shares a file or a plan, and stays as it is.
