+++
id = "WI-350"
title = "The census-audit guard still admits a catch-all under two labels instead of one (129-REVIEW-A BLOCKER 1). WI-340's anti-catch-all rule - a class charged to a WI must name a WI that exists, is open, and whose row names every module in the class - was DRIVEN and bypassed by the reviewer: all 64 same-file blocks were rebuilt into two arbitrary 32-entry classes `misc-a`/`misc-b` plus one synthetic open WI whose Title merely LISTED the module basenames, and every one of the six checks returned clean. Two rules are too weak. tests/test_dupes_census_audit.py:314-329 bans only a single MAJORITY class, so an even split evades it; and :220-246 accepts ownership on a substring match, so a keyword-stuffed row satisfies it without the WI having any relationship to the code. The property actually wanted is that a class states a rationale a reader can CHECK against the block - which is not the same as any predicate over path strings and WI text, and may not be fully mechanizable; if it is not, say so and move the residue to the enforcement audit as a Reviewer-tier rule rather than leaving a guard that advertises a property it does not hold. Whatever replaces it must be tested against the reviewer's exact bypass (an even split plus a cosmetic WI row), not only against a renamed single bucket."
workstream = "scripts"
specref = "docs/reviews/129-REVIEW-A.md"
buildtier = "medium"
priority = 2
safety_class = "ordinary"
order = 347
+++
