+++
id = "WI-631"
title = "Build assumption evidence on test cases and the observation test declaration (SR-197, SR-198)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-197", "SR-198"]
needs = ["WI-629"]
buildtier = "medium"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

- The test-case tier's `assumption_refs` (traced) and an observation case's
  `inputs`, `max_age`, `sampling`, `sample_size`, `acceptance_rule`;
  `Verifies` required only when `Assumption-Refs` is empty; an undeclared
  assumption fails naming the case.
- `derive_stage` places an assumption-only case in the phase of every
  requirement citing its assumptions (`assumption_rules.da_citing_srs`,
  IF-201).
- `trace.assumption_evidence_rows` is the one partition of evidence; the
  report and `census.red_tc_census(assumptions=True)` count assumption
  evidence apart. `gap_census` states that the assumption half is not on the
  dispatch seam (arbitration ruling 2).
- `assumption_rules.observation_tc_findings` (IF-200): omissions advise,
  malformed lifetime, policy or sampling model fail the integrity floor. An
  empty `AcceptanceRule` reads as absent, the carrier's rule (ruling 6, which
  reversed c6a43dd9's key-presence reading); a whitespace-only one fails.
- This repository's five observation cases gain two advisories each (no
  `Inputs`, no `MaxAge`).
- No approved-row cell changed.

## Context

The test case's `assumption_refs` with a conditional `Verifies`, phase placement and separate counting of assumption evidence; the observation test case's inputs, lifetime, sampling policy and sampling model cells and their findings. Design rows: LLR-229, LLR-230, LLR-231, LLR-232, LLR-233. Test cases: TC-225, TC-226, TC-227, TC-228. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
