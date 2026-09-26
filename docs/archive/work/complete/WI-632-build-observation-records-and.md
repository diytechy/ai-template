+++
id = "WI-632"
title = "Build observation records, the evidence level, the falsification worklist and accepted-risk triggers (SR-199..SR-202)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-199", "SR-200", "SR-201", "SR-202"]
needs = ["WI-631", "WI-635"]
buildtier = "strong"
safety_class = "ordinary"
priority = 4
+++

## Deliverable

- `kitlib/observation.py` (IF-214): one TOML record per result under
  `docs/test/observations/`, parsed only whole and only under the name
  `record_name(tc, observed_at)` gives it; atomic write.
- `record_observation.py` (IF-215): the one writer, refusing before it
  writes; `inputs_digest` digests any registry row id from its cells, the
  tier mapping derived from the registry machinery and tested against it.
- `assumption_rules` (IF-216): the shared record policy, the evidence level
  from current results, the falsification worklist and the accepted-risk
  state; the unevidenced-assumption advisory.
- `baseline_snapshot` (IF-217, IF-220): every snapshot act appends a typed
  entry to the act ledger `docs/archive/last_approved/acts.toml` (seq, date,
  approved, re-attested), and `risk_acceptance_act` reads that ledger, never
  the prose README (arbitration ruling 8). A malformed ledger fails closed,
  is reported on the integrity floor and refuses an act before the record
  moves.
- TC-229 stays Smoke (ruling 1). Traced pointer moved: TC-234 `verifies`
  gains IF-220. No attesting cell changed.

## Context

`kitlib/observation.py` and `record_observation.py`, the evidence level derived from current results under the cumulative tier contract, the falsification worklist, and the accepted risk anchored to its approval act (LLR-239 reads the act record WI-635 adds). Design rows: LLR-234, LLR-235, LLR-236, LLR-237, LLR-238, LLR-239. Test cases: TC-229, TC-230, TC-231, TC-232, TC-233, TC-234. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
