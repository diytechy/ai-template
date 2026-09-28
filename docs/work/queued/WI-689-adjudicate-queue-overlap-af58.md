+++
id = "WI-689"
title = "adjudicate queue overlap [af589a4f5319]: WI-615;WI-616;WI-620;WI-651;WI-655;WI-657;WI-667"
workstream = "process"
specref = "docs/work/README.md"
buildtier = "strong"
priority = 9
safety_class = "adjudication"
brief = "consolidate"
adjudicates = ["WI-615", "WI-616", "WI-620", "WI-651", "WI-655", "WI-657", "WI-667"]
digests = "af589a4f5319|edd7832b0dd6"
+++

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
