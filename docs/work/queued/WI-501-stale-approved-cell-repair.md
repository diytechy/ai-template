+++
id = "WI-501"
title = "The stale-Approved-cell repair batch: the CodeSymbol dozen plus the seven post-unification prose rows, one commit, per-row dossier (OI-53 ruled (b), 2026-08-22)"
specref = "docs/requirements/open-items.toml#OI-53"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Context

Executes OI-53's ruling (b): the batch repairs under a tracked row and the
ordinary review round, sanctioned by the `DevStg-Needs` approval dial (only
the Needs tier is human-held; SR/LLR/TC amendments proceed under review).

The population, from the rulings and the program close:
- **The CodeSymbol dozen** (OI-53's decision cell): LLR-175
  (`LaneState`→`RoutingState`), LLR-011 (the `write` half), and the
  campaign-skipped group LLR-143/089/050/157/142/057/104/108/068 plus the
  LLR-172-adjacent note — each repaired to the symbol the honest
  `Implements:` tag already sits on, or the cell narrowed to what exists.
- **The WI-498 stale-vocabulary rows — RE-SCOPED 2026-08-22 at the program
  close (worklist W-9), and the population is THREE TIMES the banked list.**
  The banked count was "six, plus SR-148 as a seventh". Both adversarial
  reviewers found it short (ROUND-SOL-RAW 8: "materially undercounts";
  ROUND-OPUS 4: "undercounts by class, for the fourth time"), and neither
  reviewer's list was complete either. The close therefore rebuilt the
  population BY VALUE rather than from row names — grepping `docs/gate`,
  `derive_gate`, `derived-gate`, the retired 0–4 ordinal, the retired
  `spine_rules` CLI modes (`--check`/`--print`/basis line/`--next-phase`),
  the bar-axis vocabulary and the retired `arch-map` regen step across ALL
  registry carriers (SN/SR/LLR/TC/IF/PB/CMP/EXT).

  **The census: 22 rows carrying 37 dirty cells; 18 of those rows are
  `Approved`.** Every count below is a row count.

  | tier | rows | ids |
  | --- | --- | --- |
  | SN | 1 | SN-029 |
  | SR | 4 | SR-006, SR-049, SR-139, SR-148 |
  | LLR | 9 | LLR-050, LLR-051, LLR-142, LLR-147, LLR-148, LLR-155, LLR-156, LLR-157, LLR-186 |
  | TC | 4 | TC-050, TC-051, TC-142, TC-170 |
  | IF | 2 | IF-040, IF-081 |
  | PB | 2 | PB-001, PB-004 |
  | EXT | 1 | REL-002 |

  **Already repaired, and NOT this row's work:** the five prose cells the
  slice-5 sweep itself falsified (LLR-142 `Rationale`, LLR-124 `Detail`,
  TC-050 `Expected`, TC-141 `Method`, SR-140 `Rationale`) were re-authored
  at the close under `intake.py snapshot --approves`; and **PB-004**
  (re-keyed to `derived-stage` and re-measured at 9.00s) and **IF-081**
  (`--regen` order re-stated as REGEN_STEPS) were repaired inline there.
  Two of those rows are only PARTLY clean and remain in this population:
  **LLR-142's `detail`** (still names `arch-map` and `derived-gate` twice)
  and **TC-050's `method`** (still says "derive the gate … `--print`
  reports the derived current phase"). The close deliberately moved only
  the text the sweep had moved.

  **The three sharpest rows, so they are not lost in a list:**
  - **SR-139** — four dirty cells, and the damage is in the NORMATIVE
    `requirement` cell, not merely its test: it still mandates "a cumulative
    integer 0-4 … (0=SN..4=nothing in process) … mapping to the harness
    gate". WI-493 re-keyed the dial to rung strings and the harness gate is
    deleted. This is strictly worse than SR-148 (the banked "seventh"),
    which states retired values only as an acceptance criterion. **SR-139
    also feeds WI-499** — coordinate, do not repair the same cell twice.
  - **TC-170** — `tier = "Smoke"`, `automated = "Yes"`, so it is part of the
    "70 mechanized" verification basis the approval act reports; its
    `method` describes the regen order as "arch-map before okf, derived-gate
    before its two consumers", and the test it points at
    (`tests/test_trunk_step.py`) asserts `okf, derived-stage, trajectory,
    status, open-items`. An Approved row counted as mechanized evidence
    names two retired steps its own test does not assert.
  - **TC-051** — carries a SECOND defect beyond vocabulary: its `evidence`
    names two pytest ids that no longer exist (renamed to
    `…_current_stage_highlight_follows_docs_stage` / `…_without_stage`), so
    the row is a dangling evidence pointer as well as stale prose.

  **LLR-155 likewise carries a non-vocabulary defect:** its `code_symbol`
  names `ratification_level`, which is not a symbol in `agent_common.py` —
  the function is `ratification_through`. That is a dangling CodeSymbol
  anchor and belongs with the CodeSymbol dozen above, not with the prose.

  Where the OBLIGATION died with the bar axis rather than merely changing
  spelling, the narrowing is recorded on the row rather than silently
  applied — LLR-050 designates a DELETED behaviour whose successors already
  have rows (LLR-185/186), so it may want RETIRING rather than re-wording.
  Re-read each row's original rationale before touching it (the standing
  findings-are-claims discipline).

- **The phase rule's own requirement row (W-15).** `derive_stage.
  phase_rule_findings` carried `Implements: SR-139`, which is a mis-trace —
  SR-139 governs the ratification dial, not the stage-decrease rule — so
  `backlink-coverage` was crediting a ratification requirement with a false
  edge. The false edge is REMOVED at the close; the rule is now rowless.
  Mint the SR that carries "a spine edit that LOWERS the effective stage
  must surface as a phase change" (ruled plan §4 + owner answer §6.1) and
  re-point the declaration at it.

THE REVIEW SURFACE, per the owner's ruling: ONE commit for the registry
edits, and this spec's Deliverable carries the per-row dossier table —
`row | cell | old text | new text | evidence (file:line that warrants it)`
— so the owner's review at merge is a single table read. The
approved-snapshot machinery (docs/archive/last_approved) will surface the
amendments on the drift/re-attest brief as designed: reconcile the
snapshot per the declared level in the same commit, never suppress it.
Verify each repaired symbol EXISTS at the cited site before writing it
(the WI-482 precedent: each target READ before citing). check_doc_refs and
check_trajectory --strict must both improve or hold — paste the
before/after finding counts.
