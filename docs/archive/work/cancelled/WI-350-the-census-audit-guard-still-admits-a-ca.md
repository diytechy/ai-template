+++
id = "WI-350"
title = "The census-audit guard still admits a catch-all under two labels instead of one (129-REVIEW-A BLOCKER 1). WI-340's anti-catch-all rule - a class charged to a WI must name a WI that exists, is open, and whose row names every module in the class - was DRIVEN and bypassed by the reviewer: all 64 same-file blocks were rebuilt into two arbitrary 32-entry classes `misc-a`/`misc-b` plus one synthetic open WI whose Title merely LISTED the module basenames, and every one of the six checks returned clean. Two rules are too weak. tests/test_dupes_census_audit.py:314-329 bans only a single MAJORITY class, so an even split evades it; and :220-246 accepts ownership on a substring match, so a keyword-stuffed row satisfies it without the WI having any relationship to the code. The property actually wanted is that a class states a rationale a reader can CHECK against the block - which is not the same as any predicate over path strings and WI text, and may not be fully mechanizable; if it is not, say so and move the residue to the enforcement audit as a Reviewer-tier rule rather than leaving a guard that advertises a property it does not hold. Whatever replaces it must be tested against the reviewer's exact bypass (an even split plus a cosmetic WI row), not only against a renamed single bucket."
workstream = "scripts"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
order = 347
+++

## Deliverable

RETIRED 2026-07-29, concurrency-restructure Phase 5 item 7, per the 2026-07-28
audit ruling (handoff-2026-07-28c §3: "guard-on-a-guard; record as a
Reviewer-tier gap"). The row's own text already conceded the property "may not
be fully mechanizable; if it is not, say so and move the residue to the
enforcement audit" — that is what happened, forced by measurement: at the Phase
5 item-1 commit the same-file majority rule FALSE-POSITIVED in the opposite
direction from 129-REVIEW-A's bypass (deleting the dispatcher's same-file
classes honestly concentrated the survivors in graph-layout, which the
arithmetic cannot tell from a rebuilt catch-all). The rule was retired from
tests/test_dupes_census_audit.py and recorded as a Reviewer-tier row in
docs/enforcement-audit.md in that commit. The checkable halves — per-section
counts, distribution-table consistency, charged-class-names-open-WI-and-modules
— remain tests.
