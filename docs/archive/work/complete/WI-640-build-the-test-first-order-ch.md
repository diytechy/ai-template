+++
id = "WI-640"
title = "Build the test-first order check over committed history (SR-217)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-217"]
needs = ["WI-642"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

- `check_test_first.py` (IF-198, IF-199) and check.py's built-in
  `test-first` step, warn-only: a requirement's implementation landing (an
  `Implements:` line naming it or one of its design rows) read from
  first-parent history against its test cases' approval commits, each late
  approval reported naming both commits.
- The `[checks] test_first_since` start gates only which requirements are
  judged; test-case approvals are read over the whole readable history
  (Sol's blocker). An approval the TOML history cannot date exactly is
  bounded at or before the cutover and reported unread unless the bound
  settles the order (arbitration ruling 7); an unread requirement fails
  `--strict`. Test-case membership is read at the tip and disclosed as such:
  association timing is OI-87.
- `PROCESS_ONLY_KEYS` types the start; PROCESS.md names the step beside the
  TDD rule (+191 bytes).
- Amended, status left Approved, for the joint adjudication: LLR-257
  `detail`. This repository reports `test-first: OK` from its declared start.

## Context

`check_test_first.py` and a warn-only step; the declared start is `[checks] test_first_since`. This repository declares its start at the approval act of these chains, so the chains themselves are judged by it. WI-642 could not declare the key: `tests/test_rule_sync.py` holds this repo's `[checks]` keys equal to the template's, and the template gains the key only here. This item ships the key and sets this repository's value to `f537fc531dd37b372259ba84f8836a290d1efddb`, the phase-6 act's parent, so the act's approvals fall after the start (SR-217 judges requirements "approved after" it). Design rows: LLR-257. Test cases: TC-250. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
