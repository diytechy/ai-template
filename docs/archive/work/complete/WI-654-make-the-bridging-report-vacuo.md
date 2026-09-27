+++
id = "WI-654"
title = "Make SR-211's interface-bridging report vacuous until the assumptions registry holds a real row"
workstream = "scripts"
specref = ""
sr_refs = ["SR-211"]
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Deliverable

SR-211's interface-bridging rule is now vacuous until the assumptions
registry holds a real assumption row. It uses the same `_adopted` predicate
the requirement side (SR-193, SR-194) gates on, not a copy of it. Before
adoption nothing is judged: a boundary interface naming neither `bridged_by`
nor `coincident` is not reported, and a `bridged_by` naming an undeclared
assumption does not fail. This repository's 43 advisories drop to 0, and they
return with C2's first real assumption row (WI-655, filed as the condition of
the ruling).

- **Amendments (in place, status left Approved, for WI-664's joint
  adjudication):** SR-211 `acceptance_criteria` (a vacuity clause), LLR-250
  `detail`, TC-244 `method` and `expected`, and LLR-224 `detail` ("absent"
  becomes "holds no real assumption row", which is what the shared predicate
  reads).
- **Review:** in the first round Sol held that the undeclared-citation
  failure must wait for adoption too ("one adoption rule across the tier"),
  and the coordinator ruled for Sol (arbitration ruling 3). The fix round was
  SOUND.
- **Evidence:** `tests/test_trace_interfaces.py`, where the vacuity cases
  (blank form and absent registry) were red against the first commit, then
  green. The module run was `315 passed, 1 skipped`.
- **Adopter note:** a RESYNC_PACK entry, "The interface-bridging rule waits
  until your assumptions registry holds a real row".

## Context

OI-94 ruled 2026-09-26: option (b). Approved SR-211 reports every boundary interface that names no bridging assumption and records no coincidence, with no "until adopted" clause, so this repository carries 43 advisories and an adopter that never adopts the tier gets one per boundary interface forever. The requirement side (SR-193/SR-194, LLR-224: "a repo that never adopts the tier is never asked") is vacuous until a real assumption row exists; SR-211 takes the same adoption rule.

Draft the amendment to SR-211, its design row and its test case (status left Approved), build the one condition in WI-637's bridging report (the same "real row" predicate the requirement side uses, not a copy of it), and file the adjudication. The owner's condition on the ruling: queued work returns to close the gap. That work is WI-655 (C2), which writes each boundary interface's `bridged_by` or `coincident`; the advisories return the moment it writes the first assumption row.

## Done-when

- SR-211, its design row and test case carry drafted amendments, and an adjudication is filed.
- A test shows no bridging advisory on a repository whose assumptions registry holds no real row, and the advisory on one that does.
- The report shares the requirement side's adoption predicate; the commit bar passes.
