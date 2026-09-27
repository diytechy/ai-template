+++
id = "WI-650"
title = "Count a requirement's test case from its first approved-and-associated commit, and warn when a result rests on an unapproved test case (SR-217 amendment)"
workstream = "scripts"
specref = "docs/log.d/2026-09-26-owner-rulings-oi82-oi94.md"
sr_refs = ["SR-217"]
needs = ["WI-664"]
buildtier = "strong"
safety_class = "spine"
priority = 4
+++

## Context

OI-87 ruled 2026-09-26: option (a) plus the owner's addition. (1) Amend SR-217, LLR-257 and TC-250 so a requirement's test case is approved at the earliest commit where it reads approved AND names the requirement or one of its design rows (arbitration ruling 5 of the wave-2 ARBITRATION.md; the built check reads membership at the tip, which a re-pointed old test case passes). (2) A defined test whose implementation is done still runs; nothing here blocks a run. (3) The owner's addition: "if that test was not approved, the test should warn it has not yet been approved and there is a chance that its result may not reflect intended behavior." Where a requirement's result rests on a test case that is not approved, or was approved only after the implementation, the report names the case with that warning.

Place (3) on the spine by the spine-authoring skill (an SR-217 acceptance clause, or a derived row with its lens recorded) — decide which and say why. Draft the amendments in this change with status left Approved (the builder brief's rule for an approved row's attesting text), build the one history condition in `first_approval_commits`' walk and the warning, and file the adjudication. Order is still read only from history, never from a cell. LLR-257 is also in the wave-2 joint amendment adjudication; build on its adjudicated text.

## Done-when

- SR-217, LLR-257 and TC-250 carry drafted amendments stating association-aware approval and the unapproved-result warning, and an adjudication item is filed for them.
- A test (written first and seen failing) shows an approved test case re-pointed at a requirement after its implementation landed reported as not test-first, and a Drafted test case's passing result reported with the not-approved warning.
- The check stays warn-only; the commit bar and `trace.py --strict-integrity` pass.
