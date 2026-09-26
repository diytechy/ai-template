+++
id = "WI-628"
title = "Build the stakeholder list and the needs' source pointer (SR-189, SR-190)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-189", "SR-190"]
needs = ["WI-642"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built test-first against SR-189 and SR-190 (for SN-044), LLR-215..217,
TC-215 and TC-216 by a builder session in its own worktree, reviewed, and
squash-merged.

- The needs file gains a stakeholder tier, `[stakeholder.STK-##]` (name,
  description, optional party, status), loaded by its own id column so its
  status never mixes with the needs' draft state. Each need gains
  `stakeholder_refs` and `source`; the STK id space joins the watermark. The
  template ships STK-000 and an SN-000 that cites it.
- `frame_rules.stakeholder_findings`: a need citing an undeclared stakeholder,
  a party naming an undeclared entity, and a stakeholder missing a required
  cell fail the frame class. A need naming no stakeholder is an advisory once
  the list has a real row. An out-of-vocabulary status fails both the
  always-on integrity floor (TC-215) and the frame class (LLR-216).
- `frame_rules.need_source_findings`: each `source` entry, written
  `path#anchor`, must resolve to an existing markdown file inside the
  repository and an anchor the kit's markdown anchor reader finds there. The
  `source` cell sits outside the provenance rule's scanned cells, and
  PROCESS.md names it among the pointer columns.
- `kitlib.spine.sn_all_ids(text, carrier)` decides the carrier from the file's
  suffix, so a TOML needs file contributes need ids from its `[need.*]` tables
  only.
- Tests: `tests/test_stakeholders.py` (TC-215, registered slow) and TC-216's
  cases in `tests/test_trace_rules.py`, each red first except the vacuous and
  existing-behaviour pins the builder named.
- This repository's live needs file gains no stakeholder rows or cells. They
  are the C1 sitting commit's (WI-643), whose Done-when now also retires
  `LIVE_ROWS_PENDING`.

Review: codex Sol (medium) NOT YET SOUND, 2 major (carrier sniffing; test
coverage of both status findings, the no-table case and the source
semantics) and 1 minor (the PROCESS.md byte re-stamp, done at merge). All
fixed.

## Context

The `[stakeholder.STK-##]` tier in the needs file, each need's `stakeholder_refs`, the `source` pointer column exempt from the provenance rule, their findings and the STK id space. The rows themselves are written in the C1 sitting commit (WI-643). Design rows: LLR-215, LLR-216, LLR-217. Test cases: TC-215, TC-216. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- Each listed test case is written first and seen failing, then passes; its `Evidence` file exists.
- Each listed design row's `CodeSymbol` binds in its `Module`, and the code carries `Implements:` back-links to the requirement and design rows it realizes.
- A new seam the work creates gains its interface row and `Contract IF-###:` body in the same change.
- Each new test module that drives git, subprocesses or a scaffold (the spine map's D31 names them) is added to `tests/conftest.py`'s `SLOW_MODULES` in the same change, or it silently joins the per-commit tier; in-memory rule tests stay in the per-commit tier.
- A kit script or registry template that ships to adopters is in `bootstrap.MAPPING`, and a schema change has a resync-pack entry naming what an adopter must do.
- The commit bar and `trace.py --strict-integrity` pass, and nothing in the change approves a spine row.
