+++
id = "WI-636"
title = "Build held off-spine status refusal, the loop provenance trailer and its history check (SR-208..SR-210)"
workstream = "unattended"
specref = ""
sr_refs = ["SR-208", "SR-209", "SR-210"]
needs = ["WI-642"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

- The loop's provenance: every loop writer appends a well-formed
  `Loop-Session` trailer (`kitlib/provenance.py`), the commit-msg hook and
  the merge slot refuse a loop commit without one.
- Lane ownership at the slot (arbitration ruling 4): a lane is the loop's
  when its claim or any loop-writer commit in its range carries the trailer;
  both rungs judge every commit of a loop lane whoever runs the slot, a
  person's commit there carrying the trailer or moving to their own lane;
  commits before the lane's first marked loop-writer commit are exempt from
  the trailer rung only. Validity is present and well-formed.
- A loop-made held status change is refused: the rung maps in
  `kitlib/authority.py`, the assumptions registry at DevStg-Boundary and the
  needs file (needs and stakeholders) at DevStg-Needs, routed through
  `rung_for` by every approval predicate; one silent, legacy-aware dial
  reader over a committed tree or the index (`dial_at`/`read_dial`) for the
  hook, the writers and the slot; a merge judged against both parents. The
  history check keeps approved LLR-249's legacy-as-most-held reading
  (ruling 9).
- Amended, status left Approved, for the joint adjudication: SR-209
  `acceptance_criteria`, LLR-246 and LLR-248 `detail`. Traced pointers moved:
  LLR-246 and LLR-248 `module` and `code_symbol`.

## Context

`kitlib/provenance.py` and `kitlib/authority.py`; the loop marker set in-process; the trailer on every loop writer; the held-status refusal at every loop writer and at the merge slot; and the history advisory for a loop commit that changed a held status. Hooks are opt-in, so the merge-slot re-check is the enforcement in a checkout without `core.hooksPath`. Design rows: LLR-246, LLR-247, LLR-248, LLR-249. Test cases: TC-241, TC-242, TC-243. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
