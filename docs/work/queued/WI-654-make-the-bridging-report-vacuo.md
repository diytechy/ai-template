+++
id = "WI-654"
title = "Make SR-211's interface-bridging report vacuous until the assumptions registry holds a real row"
workstream = "scripts"
specref = "docs/log.d/2026-09-26-owner-rulings-oi82-oi94.md"
sr_refs = ["SR-211"]
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Context

OI-94 ruled 2026-09-26: option (b). Approved SR-211 reports every boundary interface that names no bridging assumption and records no coincidence, with no "until adopted" clause, so this repository carries 43 advisories and an adopter that never adopts the tier gets one per boundary interface forever. The requirement side (SR-193/SR-194, LLR-224: "a repo that never adopts the tier is never asked") is vacuous until a real assumption row exists; SR-211 takes the same adoption rule.

Draft the amendment to SR-211, its design row and its test case (status left Approved), build the one condition in WI-637's bridging report (the same "real row" predicate the requirement side uses, not a copy of it), and file the adjudication. The owner's condition on the ruling: queued work returns to close the gap. That work is WI-655 (C2), which writes each boundary interface's `bridged_by` or `coincident`; the advisories return the moment it writes the first assumption row.

## Done-when

- SR-211, its design row and test case carry drafted amendments, and an adjudication is filed.
- A test shows no bridging advisory on a repository whose assumptions registry holds no real row, and the advisory on one that does.
- The report shares the requirement side's adoption predicate; the commit bar passes.
