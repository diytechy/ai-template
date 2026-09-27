+++
id = "WI-650"
title = "Count a requirement's test case from its first approved-and-associated commit, and warn when a result rests on an unapproved test case (SR-217 amendment)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-217"]
needs = ["WI-664", "WI-669"]
buildtier = "strong"
safety_class = "spine"
priority = 4
+++

## Deliverable

OI-87 is carried out: option (a) plus the owner's addition. SR-217's
test-first check (`check_test_first.py`) now dates a test case for a
requirement from the earliest commit at which it reads approved AND names
the requirement, directly or through a design row whose SR-Refs name it at
that commit (`first_association_commits`). A test case re-pointed at code
already written therefore no longer inherits its earlier approval date. A
requirement whose implementation has landed names each test case that is
not approved, and every late or unapproved case carries the owner's
warning: "a result from those test cases may not reflect the intended
behaviour". The check stays warn-only, so nothing blocks a run. The design
registry is held to both unreadable-history rules, so an LLR registry on an
older carrier is reported, never passed in silence.

- **Amendments (in place, left Approved):** SR-217's requirement, rationale
  and acceptance; LLR-257's detail; TC-250's method and expected. The
  owner's warning is an SR-217 clause, not a derived row, because SN-042's
  acceptance already covers a never-approved test case. The amendment
  adjudication is **WI-675**.
- **Evidence:** seven new tests in `tests/test_check_test_first.py`, each
  red first. The module now runs 32 passed.
- **Review:** Sol's first round asked for the design registry in the
  unreadable-history guard and the README row (arbitration ruling 17). The
  fix round was SOUND.
- **Cost:** the check takes about 16 s on this repository, up from 8.6 s,
  because it also walks the design registry's history.

## Context

OI-87 ruled 2026-09-26: option (a) plus the owner's addition. (1) Amend SR-217, LLR-257 and TC-250 so a requirement's test case is approved at the earliest commit where it reads approved AND names the requirement or one of its design rows (arbitration ruling 5 of the wave-2 ARBITRATION.md; the built check reads membership at the tip, which a re-pointed old test case passes). (2) A defined test whose implementation is done still runs; nothing here blocks a run. (3) The owner's addition: "if that test was not approved, the test should warn it has not yet been approved and there is a chance that its result may not reflect intended behavior." Where a requirement's result rests on a test case that is not approved, or was approved only after the implementation, the report names the case with that warning.

Place (3) on the spine by the spine-authoring skill (an SR-217 acceptance clause, or a derived row with its lens recorded) — decide which and say why. Draft the amendments in this change with status left Approved (the builder brief's rule for an approved row's attesting text), build the one history condition in `first_approval_commits`' walk and the warning, and file the adjudication. Order is still read only from history, never from a cell. LLR-257 is also in the wave-2 joint amendment adjudication; build on its adjudicated text.

## Done-when

- SR-217, LLR-257 and TC-250 carry drafted amendments stating association-aware approval and the unapproved-result warning, and an adjudication item is filed for them.
- A test (written first and seen failing) shows an approved test case re-pointed at a requirement after its implementation landed reported as not test-first, and a Drafted test case's passing result reported with the not-approved warning.
- The check stays warn-only; the commit bar and `trace.py --strict-integrity` pass.
