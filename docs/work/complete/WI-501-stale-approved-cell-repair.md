+++
id = "WI-501"
title = "The stale-Approved-cell repair batch: the CodeSymbol dozen plus the seven post-unification prose rows, one commit, per-row dossier (OI-53 ruled (b), 2026-08-22)"
specref = ""
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Deliverable

Executed under OI-53's ruling (b). One commit carries the whole batch;
`docs/archive/last_approved` reconciled in the same commit under
`intake.py snapshot --approves "OI-53 (b), 2026-08-22 -- docs/log.d/2026-08-22-oi53-54-rule.md"`.

**Rows repaired: 27** (11 CodeSymbol-class edits + LLR-050's title/detail/
rationale narrowing counted once + 1 minted SR + 14 vocabulary-census rows
edited). **Rows verified and left untouched, with the finding recorded:**
LLR-142 CodeSymbol, LLR-155 vocabulary, LLR-156, LLR-172(-adjacent),
LLR-186, IF-081, PB-004 — 7 rows the population named where the cited cell
was already honest; touching them would have been the mechanical
sweep this repair explicitly avoids.

### The CodeSymbol dozen + LLR-155's dangling anchor

| row | cell | old text | new text | evidence (file:line) |
| --- | --- | --- | --- | --- |
| LLR-175 | CodeSymbol | `LaneState.note_session/main` | `RoutingState.note_session/main` | `agent_loop.py:913` (`class RoutingState`), `:1152` (`note_session`), `Implements: SR-172, LLR-175` at `:1156` |
| LLR-011 | CodeSymbol | `write/--force + write_kit_version` | `copy_kit_files/--force + write_kit_version` | `bootstrap.py:2743` (`def copy_kit_files`, docstring `Implements: SR-011, LLR-011` at `:2748`), `:2358` (`write_kit_version`) |
| LLR-143 | CodeSymbol | `run/_resume_or_claim/_stranded_claims/_default_worker` | `run` (narrowed) | `dispatch.py:1104` (`run` exists); `_resume_or_claim`/`_stranded_claims`/`_default_worker` grep zero hits repo-wide — `_stranded_claims` named as retired (past tense) at `integrate.py:702` |
| LLR-089 | CodeSymbol | `structural_safety/classify` | `kind_of/classify` | `schedule.py:298` (`classify`), `:272` (`kind_of`); `structural_safety` grep zero hits |
| LLR-050 | Title/CodeSymbol/Detail/Rationale | `Derived-gate computation + hybrid cache` / `compute` / (BAR-axis prose) | narrowed to a retirement record; SSOT principle attributed to LLR-185/LLR-186 | `spine_rules.py:1-11,755-768` (module docstring records the two-act deletion; `compute`/`_raw_level`/`sr_bar` etc. confirmed absent by grep) |
| LLR-157 | CodeSymbol | `spine_stage/stage_to_gate/_decomposed_sr_ids` | `spine_stage/_decomposed_sr_ids` | `spine_rules.py:605` (`spine_stage`), `:466` (`_decomposed_sr_ids`); `stage_to_gate` grep zero hits (`stage_to_bar`, its likely predecessor, recorded retired at `:755-756`) |
| LLR-057 | CodeSymbol | `when_view/_tier_column/_svg_node` | `when_view` (narrowed) | `traj_views.py:982` (`when_view`); `_tier_column`/`_svg_node` grep zero hits in the module |
| LLR-104 | Module/CodeSymbol | `gen_trajectory.py` / `--nhead/.stgt/.stgn/.hooplab/.hubname` | `traj_panels.py` / `--nhead/.stgt/.stgn/.slotname` | `traj_panels.py:540,544` (`.stgt`/`.stgn` emit), `:1038-1039,1050` (CSS incl. `.slotname`); `.hooplab`/`.hubname` grep zero hits |
| LLR-108 | Module | `gen_trajectory.py` | `traj_render.py;gen_trajectory.py` | `traj_render.py:978` (`def _render_drill`), imported at `gen_trajectory.py:180`; the row's other half (`role=img` emit sites) still lives in both |
| LLR-068 | CodeSymbol | `spec_interface_findings/_spec_interfaces_section/_proposed_rationale_present` | `spec_interface_findings/_spec_interfaces_section` (narrowed) | `check_trajectory.py:1861,1831`; `_proposed_rationale_present`'s own former docstring at `spec_interface_findings` records it "RETIRED AT WI-442" |
| LLR-172-adjacent note | (verification only) | — | no edit — `component_findings` confirmed live | `check_trajectory.py:1738` (`def component_findings`); matches the WI-484 log entry (`docs/log.d/2026-08-20-program-grind.md:1975-1984`) that already settled this as resolved |
| LLR-155 | CodeSymbol | `.../ratification_level/human_holds` | `.../ratification_through/human_holds` | `agent_common.py:595` (`def ratification_through`); `ratification_level` grep zero hits |

### The stale-vocabulary census (edited rows; verified-clean rows recorded above)

| row | cell | old text (substring) | new text (substring) | evidence |
| --- | --- | --- | --- | --- |
| SN-029 | acceptance | `A cumulative 0-4 level ... with a declared mapping to the harness gate` | `A cumulative level ... via a declared, auditable mapping` | `docs/gate`/BAR axis deleted, `spine_rules.py:755-768` |
| SR-006 | requirement | `cached in docs/gate` | `cached in docs/stage` | `docs/stage` is the live file (`derive_stage.py` writes it; `docs/gate` does not exist on disk) |
| SR-049 | title/requirement/acceptance_criteria | `Derived gate ...` / `derive the gate ...` / `per-phase gates` | `Derived stage ...` / `derive the stage ...` / `per-phase stage` | same |
| SR-139 | requirement/acceptance_criteria | `cumulative integer 0-4 ... (0=SN..4=nothing in process) ... mapping to the harness gate` / `stage 4 is held by no level` | `cumulative level ... via a declared, auditable rung ordering` / `the terminal stage rung is held by no level` | ROUND-OPUS.md:254-289 (the reviewer's own finding); WI-499 owns the "ratification"/"ratify" word itself — untouched here (coordination note below) |
| SR-148 | acceptance_criteria | `levels 1 through 4 hold exactly their documented cumulative tiers` | `each higher level holds exactly its documented cumulative tiers` | the ordinal 1-4 range is retired (WI-493 re-keyed the dial); wording generalized rather than re-numbered |
| LLR-051 | detail | `... gates panel derived from the live registries + docs/gate (current-gate highlight ...)`, `slices -> phase -> gates panel` | `... stage panel ... docs/stage (current-stage highlight ...)`, `slices -> phase -> stage panel` | `docs/gate` absent on disk; `docs/stage` is current |
| LLR-142 | detail | `Regenerates arch-map, okf, derived-gate, dashboard, status block ...` | `Regenerates okf, derived-stage, trajectory, status block ...` | `trunk_step.py:411-459` `REGEN_STEPS` (arch-map retired per its own comment at `:411`) |
| LLR-147 | title/CodeSymbol/detail/rationale | `SN-coverage gate rung + uncovered basis count` / `sn_gate/sn_cited_ids` / (basis-line prose) | narrowed to record `sn_gate`'s deletion; coverage check folded into `spine_stage` | `spine_rules.py:711-715` (the inline coverage check within `spine_stage`); `sn_gate` grep zero hits |
| LLR-148 | detail | `docs/gate never written` / `raw derived-gate drop` | `docs/stage never written` / `raw derived-stage drop` | `derive_stage.py:507-528` (`--next-phase` lives here today) |
| LLR-157 | detail | `stage_to_gate states the mapping ... rides docs/gate as an APPENDED basis field` | records `stage_to_gate`'s deletion; value now rides `docs/stage` via `derive_stage.py` | see CodeSymbol row above |
| TC-050 | method | `derive the gate from fixture states ...` | `derive the stage from fixture states across every rung predicate ...` | matches `expected`'s already-clean `DevStg-*` wording (this cell was the "partly clean" half named in WI-501's Context) |
| TC-051 | method/evidence | `... docs/gate (the current-gate highlight matches docs/gate ...)` / two evidence ids naming `..._gate` | `... docs/stage (the current-stage highlight matches docs/stage ...)` / `..._current_stage_highlight_follows_docs_stage`, `..._tab_omitted_and_byte_identical_without_stage` | `tests/test_traj_panels.py:239,317` (both replacement test ids confirmed present) |
| TC-142 | method | `leaves docs/gate byte-identical` | `leaves docs/stage byte-identical` | `derive_stage.py` is the module under test |
| TC-170 | method | `arch-map before okf, derived-gate before its two consumers (trajectory, status), open-items last` | `okf before derived-stage ..., derived-stage before its two consumers (trajectory, status), open-items last` + the retired arch-map step noted as no longer part of the sequence | `tests/test_trunk_step.py:276-299` (`test_regen_runs_in_declared_dependency_order`, asserting `okf, derived-stage, trajectory, status, open-items`) |
| IF-040 | contract | `check.py --run-step arch-map/trajectory-map/okf` | `check.py --run-steps okf,trajectory-map,...` (the full step list) | `project-trajectory/hooks/pre-commit:273` (`--run-steps okf,trajectory-map,status-map,open-items,trajectory,registry-integrity,derived-stage,skills-sync,skills-index,prompt-catalog,ratify-fresh,staged-divergence`; no `arch-map`) |
| REL-002 | flow | `docs/status.md, docs/gate and the console reports` | `docs/status.md, docs/stage and the console reports` | `docs/stage` is the live generated file |
| PB-001 | Notes | `(docs/stack.ini "traceability" step, BAR_RELEASE)` | notes `BAR_RELEASE` as retired with the bar axis | `check.py:1105-1106`/`kitlib/ladder.py:47-48` record `BAR_RELEASE` gone |

### W-15 — the phase-decrease rule's mis-trace

**Minted SR-181** ("A spine edit that lowers the effective stage surfaces as
a phase change"), `docs/requirements/system-requirements.toml`, `status =
"Approved"` (machine-approvable: only `DevStg-Needs` is human-held, per the
same mint-status precedent WI-483 used for LLR-188/LLR-189 earlier the same
day). `sn_refs = ["SN-004", "SN-008"]`, `boundary_refs = ["B-05"]`,
`aspect = "process"`, `phase = 5`. Verified against the machinery rather
than asserted: `intake.py snapshot --approves ...` ran clean (no refusal),
and `trace.py --strict --strict-integrity`'s `approval record`/`integrity`
findings that a fresh mint produces cleared once the snapshot absorbed it
(before/after below).

`project-trajectory/scripts/derive_stage.py`'s `phase_rule_findings`
docstring re-pointed: the "NO `Implements:` LINE" paragraph replaced with
`Implements: SR-181` plus a short note recording the SR-139 mis-trace this
corrects (citation-frame-free, per `trace.py`'s spine/provenance rule —
the full account lives in this fragment and the log, not the docstring).

### SR-139 / WI-499 coordination

SR-139 carries **2 cells repaired here** (`requirement`,
`acceptance_criteria`) for the retired 0-4 ordinal / harness-gate mapping
only. WI-501's Context named "four dirty cells" for this row; only two are
independently substantiated (by this session's own re-check and by
ROUND-OPUS.md itself, which names the same two). **The word
"ratification"/"ratify" in SR-139 — and everywhere else in this batch — is
untouched: that rename is WI-499's scope**, not WI-501's (WI-499's Context,
`docs/work/queued/WI-499-ratification-becomes-approval.md`, claims exactly
this vocabulary). WI-499's worker should re-check SR-139 for a possible
third/fourth dirty cell independently rather than assume this row's "four"
count is settled.

### LLR-050 disposition

Re-worded rather than formally retired: no `Status = Retired` vocabulary
exists in the schema (`check_trajectory.py` closed-vocabulary check
confirmed), so the row is kept `Approved` with its `title`/`code_symbol`/
`detail` rewritten to state plainly that the mechanism it named (`compute`,
the per-artifact gate rules, `docs/gate`) was deleted wholesale at the ruled
stage unification, that no successor occupies its identity, and that the
SSOT principle it argued for is fully carried by LLR-185/LLR-186. The
original `rationale` is kept verbatim, marked as historical, per the
findings-are-claims discipline (its argument was never wrong — only the
mechanism it was pinned to).

### Gates, before/after (this session, Windows, `.venv` Python 3.11.9)

- `check_doc_refs.py --root . --strict`: dangling references **197 -> 196**
  (LLR-050's `compute` WARN cleared; zero new dangling introduced) <!-- fig: cmd="python project-trajectory/scripts/check_doc_refs.py --root . --strict" rev=8848f6fb -->.
- `check_trajectory.py --root . --strict`: **identical** WARN/FINDING set
  before and after (105 lines both sides, exit 0 both sides) — HOLD <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=8848f6fb -->.
- `trace.py --root . --strict --strict-integrity`: citation-frame/spine
  stand-alone findings introduced by this session's own new prose (6 WARN +
  6 FINDING lines) were all cleared by a second reword pass — zero
  surviving. `integrity=0` unchanged before/after once the snapshot
  absorbed SR-181. The only surviving diff against the pre-session baseline
  is expected and benign: `orphans` 13->15 (SR-181, freshly minted, has no
  LLR/TC yet — the same pattern every other pending SR in this registry
  carries) and the `hat coverage` denominator moving 244->245 (one more
  requirement row exists to be attributed).

Deferred open items: none — SR-139's possible third/fourth dirty cell is
flagged above for WI-499 to independently verify, not deferred as an open
item (it is a scope note between two tracked rows, not an owner decision).

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
