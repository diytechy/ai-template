# WI-1014 plan: the README's registry map and the dashboard's lifecycle panel show today's tiers and stage ladder

Planned on branch `maint/wi-1014` at `0d67302bd` (the critique dispositions),
cut from `refactor_again` at the same commit. A maintenance-branch build: no
plan critique or pass record.

## The S5 question: where panel 1 reads its rungs and tiers

**Answer: from their homes, and the panel gains one input.** Panel 1 drifted
because its six rows were a list written into `process_panel`: it never
gained `DevStg-Release` once `derive_stage` could return it, and it never
gained the frame, assumption or stakeholder tiers once `spine_rules` read
them. So the panel stops holding a list:

- **The rungs** come from `kitlib.ladder.STAGE_ORDER`, the ladder's one home
  (on the shared-kernel surface, so reading it is not a seam).
- **Each rung's tiers** come from a new table in `spine_rules`,
  `RUNG_TIERS`, beside `spine_stage`.
- **The counts** come from `spine_rules.load_spine`, the rows the
  derivation itself reads (example `-000` rows already dropped), plus the
  committed evidence record for the one input that is not a row set
  (`kitlib.evidence.read`, also on the kernel surface).

The new input is the edge `traj_parse -> spine_rules`, which crosses from the
dashboard component (CMP-009) into the spine's (CMP-006), so it is declared
as interface row IF-325 and stated as a `Contract IF-325:` block in
`spine_rules`'s header.

**Why a table and not `spine_stage` itself.** `spine_rules` holds no table
today: which tier holds which rung is the control flow of `spine_stage`. Making
drift unrepresentable would mean rewriting `spine_stage` to run from a table,
and its needs-coverage arm (an accepted need with no answering requirement
returns `DevStg-Needs`, checked after the Reqs arm) breaks a flat table; the
function also implements accepted rows (LLR-147, LLR-157, LLR-241). That is
not a small change. So the table is pinned to the function by a driven test
instead (TC-455): over an otherwise settled spine, putting each tier in work
returns the rung the table names; the table's rungs are exactly the ladder's;
and the keywords the table names, with their companions (`sn_draft`,
`cited_srs`, `have_bifs`, `have_cmps`), are exactly `spine_stage`'s
parameters, so a new input to `spine_stage` fails the test until the table
names it.

### The table

"Holds" is `spine_rules`'s own word: a tier in work keeps the repository at
that rung. Each tier is its id prefix and the `spine_stage` keyword carrying
its rows.

| Rung | Tiers holding it | Why |
|---|---|---|
| `DevStg-Needs` | SN (`sn_ids`), STK (`stks`) | a Drafted or unanswered need; an active stakeholder tier with a Drafted row |
| `DevStg-Boundary` | B (`bifs`), DA (`das`), SUR (`surs`) | an adopted frame with no or a Drafted crossing; an active assumption or surrogate tier with a Drafted row |
| `DevStg-Reqs` | SR (`srs`) | a Drafted requirement |
| `DevStg-Arch` | CMP (`cmps`) | an adopted partition with no, a Drafted or a `has-gap` component |
| `DevStg-LLReqs` | LLR (`llrs`) | a requirement with no design row, or a Drafted one |
| `DevStg-Tests` | TC (`tcs`) | a requirement with no test case, or a Drafted one |
| `DevStg-Impl` | evidence record (`evidence_passed`) | every tier settled and no passing harness record for this tree |
| `DevStg-Release` | none | nothing in work (`STAGE_DESC`) |

## Deliverable 1, first: the README's registry map (prose only)

`README.md`, "The registries & trace artifacts — one map". Every registry
under `project-trajectory/registries/` and the work-item folder gets a node,
and every cell that names another registry's row gets an edge, labelled with
the template's key as written today (TOML keys in snake case, CSV headers as
the CSV templates spell them):

- **Removed:** `IF -- req_refs --> SR` (retired, `migrate_carrier.IF_RETIRED`);
  the CSV-era labels (`Entity`, `From/To`, `Boundary-Refs`, `SR-Refs`) become
  `entity`, `from` / `to`, `boundary_refs`, `sr_refs`.
- **Added:** a subgraph for the tiers the stage reads from their first
  acceptance: STK (in the needs file), DA and SUR (`assumptions.toml`). Edges
  SN `stakeholder_refs` -> STK, STK `party` -> EXT, SR `da_refs` -> DA, TC
  `assumption_refs` -> DA, IF `bridged_by` -> DA, DA `effect_at` -> B, DA
  `realized_by` -> SUR, SUR `emulates` -> EXT; the hats roster as a node with
  SR and LLR `hat_refs` and DA `obstacle_hats`; OI with WI `needs` -> OI; TC
  `verifies` -> IF, SR -> TC (a case verifies a requirement directly), IF
  `verified_by` -> TC and LLR, and PB and ASSET `Refs` to both SR and LLR.
- **Not drawn, named in one sentence under the map:** links inside one
  registry (SR `delivered_with`, IF `carried_by`, CMP `part_of` /
  `superseded_by` / `derivation`, EXT `mediates`, WI `needs` to a WI), cells
  naming paths rather than rows (IF `owner` / `requestors` / `consumers`, LLR
  `module`, SN `source`, CMP `knowledge`), and a case's observation cells
  (`inputs`, `trigger`), which name rows only to say when a result goes stale.
  The per-run decisions record (`decisions.template.toml`) is not a registry
  any row names by id and is not drawn.
- **The text around it** follows: the intro counts four kinds, not three; a
  table section for the stakeholder and assumption tiers; an open-items row in
  the optional table; the interfaces row loses `req_refs` and its stale owner
  sentence (an owner is the providing thing, never a requirement or design
  id). The legend sentence says spine arrows run parent to child and every
  other arrow runs from the row holding the cell to the row it names.
- **Left as it is:** the `LLR-### design` label (the last Done-when item; the
  operator has not ruled on the spine's design depth).

## Deliverable 2: panel 1

- `spine_rules.RUNG_TIERS` (above) and IF-325's contract block.
- `traj_parse.rung_tiers(root)`: `[(rung, [(tier, count), ...])]` in ladder
  order, from `RUNG_TIERS` and `load_spine`'s rows; the evidence tier counts
  the committed record (0 or 1).
- `traj_panels.process_panel`: the hand list goes. One row per rung, after the
  Vision lead row (which keeps its "—" rung): the tiers' prefixes in bold, the
  rung, and a count per tier (`N SN`, or `no STK` at zero). A tier-less rung
  shows `—` and the rung's `STAGE_DESC`. A row is `now` when the recorded
  stage equals its rung, so exactly one row is current at any rung.
  `data-stages` keeps its name and now carries one rung. The caption and the
  rationale comment are rewritten to say this (the comment's "nothing derives
  `DevStg-Release`" goes).
- `PROJECT_STATE.html` regenerated (`trunk_step.py --regen`). The stored
  golden page (`tests/golden/dashboard-no-assumptions.html`) renders a repo
  with no `docs/stage`, so it has no Process tab; its test staying green shows
  the change does not leak into the stage-less page.
- RESYNC entry at the end of §4: kit-owned `scripts/spine_rules.py`,
  `scripts/traj_parse.py`, `scripts/rendering/traj_panels.py`; regenerate
  `PROJECT_STATE.html`; nothing forced.

## Spine rows (all Drafted)

- **LLR-393** (SR-168, CMP-006, `spine_rules.py`, `RUNG_TIERS`): the table and
  its pin.
- **LLR-394** (SR-168, CMP-009, `traj_parse.py;rendering/traj_panels.py`,
  `rung_tiers/process_panel`): the panel's rows, tiers, counts and highlight.
- **TC-455** verifies SR-168, LLR-393: `tests/test_spine_rules.py`, the driven
  pin above.
- **TC-456** verifies SR-168, LLR-394, IF-325: `tests/test_traj_panels.py`,
  in process: every rung has a row in ladder order with `RUNG_TIERS`'s tiers;
  the counts follow fixture registries carrying stakeholders, crossings,
  assumptions, surrogates, components and an evidence record; each rung,
  recorded in turn, marks exactly its own row.
- **IF-325** (owner `scripts/spine_rules`, requestor `scripts/traj_parse`,
  `call`, CMP-009).

No accepted row changes: LLR-051 and TC-051 already say the panel is drawn
from the live registries and `docs/stage` with per-tier counts, which stays
true; TC-051's two process-tab tests change their asserted strings (the
`2 SR · 1 accepted` note and the old rung spans) but not their names.

## Done-when, item by item

1. Map: the edges above, checked against each template; no `req_refs`.
2. Panel: eight rung rows, `DevStg-Release` included, tiers from
   `RUNG_TIERS`, counts from `load_spine`; TC-455 and TC-456.
3. Golden files and tests: TC-051's tests updated; the golden page's test run
   and green; `PROJECT_STATE.html` regenerated.
4. The `LLR-### design` label unchanged.

## Tests run (rule 5)

`tests/test_spine_rules.py`, `tests/test_traj_panels.py` and every module
importing `spine_rules`, `traj_parse` or `traj_panels` (grep, plus
`trace.py --tests-for`), with `tests/test_import_layers.py`,
`tests/test_module_size_ratchet.py`, `tests/test_dogfood_sync.py`.
