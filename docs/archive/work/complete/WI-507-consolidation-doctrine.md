+++
id = "WI-507"
title = "The consolidation doctrine lands: the 0->A->B clause in the three guides, the overlap baseline measured, antidote vendored (OI-58 ruled, 2026-08-22)"
specref = ""
workstream = "process"
sr_refs = ["SR-182"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

All three of OI-58's ruled halves landed in one commit.

- **The doctrine, one home.** `PROCESS.md` §3 carries the full clause
  ("Consolidate, don't duplicate — the 0→A→B rule"): edit-conservatively
  stays scoped to the task in front of you; consolidation is scoped to the
  whole codebase when the task IS consolidation — prefer the change that
  minimizes total behavior, extract the shared stage a duplicated fix wants
  (0→B, 0→D become 0→A→B, 0→A→D), restructure where outputs overlap, and
  validate/implement once at the boundary that owns the behavior.
  `CLAUDE.md` and `AGENTS.template.md` each carry one pointer line beside
  their existing conservatism bullet, not a restatement. Byte deltas: CLAUDE.md
  7238->7513 (+275, cap 8500); AGENTS.template.md 9941->9980 (+39, cap 10000,
  paid for by tightening the "one fact, one home" bullet in the same edit);
  PROCESS.md 84881->85889 (+1008, FLAGGED, watched not capped).
- **The measurement, standing.** `scripts/check_dupes_census.py` (NEW) — the
  WI-448 duplicated-function-body census as one named function, wired
  `[step:dupes-census]` (product layer, DevStg-Impl), **warn-first FOREVER**:
  never exits nonzero, not even under `--strict`. Baseline stamped in
  `docs/stack.ini` `[dupes-census]`: 15 groups / 15 redundant copies / 202
  redundant lines (a fresh measurement at commit 1806f5c8, not a restatement
  of WI-448's own stale 15/15/194 figure — trunk moved between the two
  reads). Deliberately narrower than the `[step:dupes]` machinery owner
  ruling D-7 (2026-08-10) tore down: that step gated on an unbounded
  population; this one re-arms only the measurement, never the gate, and
  says so in its own docstring so a later editor does not wire in real
  `--strict` teeth without bringing that case back to the owner. New spine:
  SR-182 / LLR-195 / TC-190 (`tests/test_check_dupes_census.py`, 5 cases).
  The call-graph behavioral-overlap measure is NOT added here — it is
  OI-58's own (c) program row, already minted as **WI-508** and sequenced
  behind the wi448/wi483 lanes, so building a second instrument here would
  have pre-empted that program's own design.
- **Antidote, vendored.** Read whole before vendoring (pure-prompt, MIT,
  no scripts/network/dependencies — confirmed, not just claimed).
  `project-trajectory/skills/antidote/SKILL.md`: verbatim upstream content
  below a provenance note (source, license, pinned commit
  `8e0350e3d86df36852d56ad0a502376e24de870c`, upstream v1.1.0), frontmatter
  rewritten to this kit's schema, `scope: kit` / `domains: [any]` (a default
  every adopter's bootstrap materializes). `skills/INDEX.csv` regenerated;
  dogfooded byte-identical into `.claude/skills/antidote/` and
  `.agents/skills/antidote/`. `docs/dependencies.md` gains a new `kit` tier
  (vendored content, not a Python import) and a row naming what it replaces
  and why. **No pre-existing vendored-skill pattern existed** — every shipped
  skill was kit-authored; this WI establishes the convention (recorded as a
  deviation from the WI text's premise, not a blocker: the owner's OI-58
  ruling names vendoring as the explicit intended act regardless).
- **RESYNC + scaffold verification.** Two `RESYNC_PACK.md` entries (`[since
  1806f5c8]`) for the doctrine+census pair and the antidote skill.
  `bootstrap.py --dest <scratchpad> --agents claude --domain any` lands
  `.claude/skills/antidote/SKILL.md` byte-identical to the kit source.

Gates: `pytest -q -n auto -m smoke` 1404 passed / 5 skipped (`docs/stack.ini`
`[smoke-budget]` re-stamped 1409->1416 for the 5 new tests); `check_docs.py
--stale` 0 broken; `check_trajectory.py --strict` clean; `trace.py
--strict-integrity` integrity=0 (new rows ride `docs/archive/last_approved/`
via `intake.py snapshot` in this commit). Full suite (settled, closed tree):
**2899 passed, 14 skipped in 1092.39s** — full record in
`docs/log.d/2026-08-22-wi507-consolidation-doctrine.md`.

## Context

Executes OI-58's (a)+(b) halves plus the owner's vendoring instruction:

1. **The doctrine** — CLAUDE.md, AGENTS.template.md and PROCESS.md gain
   the consolidation clause BESIDE edit-conservatively (the two scoped:
   conservative WITHIN a task, consolidating ACROSS the codebase when the
   task is consolidation): "prefer the change that minimizes TOTAL
   behavior; when a fix wants the same code in two places, extract the
   shared stage — the 0→A→B rule; where outputs overlap, restructure so
   each behavior has one home." Byte-budget-guard convention on all three
   (AGENTS is at its cap — relocation, not growth).
2. **The measurement** — the WI-448 duplication census (function-body
   hashing; 477 residual lines at last stamp) becomes a standing
   warn-first check with a stamped baseline and downward-only restamps,
   burn-down visible; a call-graph behavioral-overlap measure added if it
   stays stdlib-cheap, else recorded as the follow-up.
3. **Vendor antidote** — the skill at C:/Projects/antidote/skills/antidote
   joins project-trajectory/skills/ as a default skill the pack ships
   (the existing vendored-skill pattern: source recorded, version/commit
   stamped, dogfooded into .claude/skills/), with a dependencies-ledger
   row naming what it is and why (external content entering the kit).
   State the shared principle once in the doctrine text: validate and
   implement at the boundary that owns the behavior, never at each
   caller.

RESYNC entries for the guide and skill changes; scaffold-verify the skill
lands in a fresh scaffold's agent surfaces.
