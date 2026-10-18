# WI-942 plan: the merge slot reads an acted row's registry from its id

Spec: `docs/work/active/wi-942/WI-942-merge-floor-lone-retirement.md`
(specref `docs/decisions/wi-912.toml`, D-009 and D-013 F5). Delivers SR-207
and SR-178 through the amended LLR-278 and TC-278. Read in the lane worktree
at `396ff9f44`. The probe the spec cites
(`review-tmp/2026-10-17e/drafts/probe/probe_floor.{py,out}`) was read too.

## The architectural-delta answer

DELTA: none

The work item does none of the four.

- **No new state.** No field, file or record is added. `acts.toml` (IF-220)
  and the snapshot copies are read as before.
- **No new domain value.** `lane_acted_set` returns the same
  `{"approve": {id: registry}, "reattest": {id: registry}}` shape. Its values
  are still members of `APPROVAL_ACT_CSVS`'s registries or `None`.
- **No new input.** The registry of a ledger-named id is now read from the id
  itself, through `_tier_of`. The id was already an input, and the same module
  already uses `_tier_of` on the same ids in `held_reattest_refusal`. The
  output *stops* depending on one input: the head's live rows.
- **No new boundary.** No new module or reader is called. IF-091's call
  contract is unchanged in shape, and so is IF-220's ledger.

This matches the spec's S5. The spec found, but does not fix, three prefix
readers over two tier sets (`baseline_snapshot._reattested_registry`,
`adjudicate_act._tier`, `acceptance_record._tier_of`). This plan uses the
floor's own `_tier_of` and keeps its universe. It consolidates nothing,
because the spec leaves that call to the coordinator.

## What the code reads today

- `acceptance_record.lane_acted_set` (line ~839) builds
  `approve = {act["id"]: act["registry"]}` from the two-tree walk. It then
  resolves `ledger | reattested` through `_registries_holding(root, head,
  ids)` (line ~827), which searches the head's live rows in
  `APPROVAL_ACT_CSVS`. A retired row is absent at the head, so it maps to
  `None`.
- `_copy_lines` drops `None` registries (`if reg`). The retirement's own
  registry copy therefore reads `snapshot WIDENED to <registry> without an
  approved row`. The probe reproduces this on a released rung for a scoped
  lane and an unscoped lane: `{'reattest': {'TC-001': None}}`.
- `_tier_of(rid)` returns `(canonical registry, id column)` by prefix over
  `AMENDMENT_CSVS` (an alias of `APPROVAL_ACT_CSVS`): `SR-`, `LLR-`, `TC-`,
  `SN-`, `DA-`, `SUR-`. Otherwise it returns `(None, None)`. For an id present
  at the head, it returns the same canonical path that `_registries_holding`
  returns: `_spine_rows_at` resolves carriers, and DA and SUR share
  `assumptions.toml`. The CSV-carrier and markdown-needs tests pin that.
  Their assertions are `{SR_REL}` and `{NEEDS_REL}`. So the only behaviour
  that changes is for an id absent at the head.
- `merge_approval_refusal` runs its refusals in this order: malformed
  scope, `reattest_scope_refusal` (OUTSIDE), `held_reattest_refusal` (by
  row, including "below approval (or absent) at the act"),
  `unaccepted_refusal`, `backed_act_refusal` (`uncovered_refusal`: "no
  ACCEPTED verdict in this branch judged", naming each row), and then
  `adjudication_approval_refusal` (OUTSIDE flips, WIDENED, WITHOUT ITS
  ANCHOR). The three pins (D5, D6, D7) are refused by earlier checks. They
  pass before the change and after it.
- The fixtures in `tests/test_snapshot_readers.py` are real git repos on a
  bootstrapped scaffold: `_release`, `_append`, `_rewrite`, `_commit`,
  `_bind_branch` and `SNAP.copy_live`. The file is in `SLOW_MODULES`, so the
  new tests do not enter the smoke tier.

## Design decisions the builder follows

1. **The reader change** (`project-trajectory/scripts/acceptance_record.py`,
   `lane_acted_set` only):
   - Delete `_registries_holding`.
   - Replace its two uses with the id's tier:
     `approve.update({rid: _tier_of(rid)[0] for rid in ledger})` and
     `"reattest": {r: _tier_of(r)[0] for r in reattested}`.
   - A live flip keeps the registry from `acts`, which is the walk's.
   - An id of no walked tier maps to `None`, so its copy stays WIDENED, as
     it does today.
   - Docstring: "with the registry that holds it" becomes "with the registry
     its id's tier names (a live flip: the registry the two-tree walk
     reports), present at the head or not, so a retired row authorizes its
     own registry's copy".
   - Keep the `Implements: SR-178, LLR-278` tag.
   - No other function changes. `_tier_of` is already defined in this module
     (line ~1096), and a call inside a function body needs no reordering.
2. **The tighter direction is accepted, not tested.** A ledger-only approval
   of a row absent at the head now owes its registry's copy (WITHOUT ITS
   ANCHOR) where it owed none before (spec Trust, "Tighter, not looser"). No
   kit route produces that act. The snapshot writer refuses an id that names
   no live or recorded row, and a first approval of a row absent at HEAD is
   refused upstream. The Done-when names no test for it, so none is added.
3. **The new tests** sit in `tests/test_snapshot_readers.py`, beside the
   TC-278 block (after `test_a_held_rung_row_ruled_both_ways_reads_MEANING_and_is_refused`).
   They share one fixture:
   - `_retirement_act(root, held=False, judged=("SR-002",))`:
     - Unless `held`, `_release(root)`.
     - Append `SR-001` and `SR-002`, both Approved (`_SR`). Then
       `SNAP.copy_live(root, seed=True)` and commit "seed"; that commit is
       `base`.
     - Delete the `SR-002` block with
       `_rewrite(root, SR_REL, _SR.format(rid="SR-002", title="row two"), "")`
       and commit "retire SR-002".
     - `_bind_branch(root, {"amendment": list(judged)})`, which writes an
       accepted amendment verdict ruling those rows CLARITY.
     - `SNAP.copy_live(root, reattests=frozenset({"SR-002"}))`, which copies
       the SR registry alone and appends one ledger entry.
     - Commit "the retirement act"; that commit is `head`.
     - Return `(base, head)`.

     `SR-001` stays in the registry untouched, so the registry holds an
     approved row but no other act.
   - The metas are `_RETIRE = [("WI-900.md", {"brief": "amendment",
     "adjudicates": ["SR-002"]})]`, and the D6 case uses the existing
     `_AMENDMENT` (scoped to `SR-001`).
   - If `copy_live` refuses the held-rung act inside the fixture (it should
     not: `test_a_held_rung_reattestation_without_a_verdict_is_refused` takes
     the same writer call on a held dial), the builder stops and reports it.
     It must not reshape the fixture to avoid the refusal.

## The tests, and what each fails on before the change

| Test (in `tests/test_snapshot_readers.py`) | Clause | Before the change | After |
|---|---|---|---|
| `test_a_retirement_alone_in_its_registry_merges`: `merge_approval_refusal(..., _RETIRE, trunk=head) is None`, and also with `metas=[]` (unscoped) | D2 | FAILS: `snapshot WIDENED to docs/requirements/system-requirements.toml without an approved row` (the probe's refusal) | passes |
| `test_the_acted_set_names_a_retired_rows_registry`: `lane_acted_set(...)[0] == {"approve": {}, "reattest": {"SR-002": SR_REL}}`, and `copy_live`'s written list is the SR copy alone | D3 | FAILS: `{"SR-002": None}` | passes |
| `test_a_lone_retirement_on_a_held_rung_is_refused_by_row` (`held=True`): refusal contains `SR-002 is below approval (or absent) at the act` | D5 | passes (pin) | passes |
| `test_a_retirement_outside_the_amendment_scope_is_refused` (`_AMENDMENT`, scoped to SR-001): refusal contains `SR-002 re-attested OUTSIDE` | D6 | passes (pin) | passes |
| `test_a_retirement_no_accepted_verdict_rules_is_refused` (`judged=("SR-001",)`, `_RETIRE`): refusal contains `no ACCEPTED verdict` and `SR-002`, not `WIDENED` | D7 | passes (pin) | passes |
| `test_a_combined_act_copying_a_registry_neither_section_moved_is_widened` (existing, unedited) | D8 | passes | passes |

The builder records the red run of the two new D2/D3 tests against the
unchanged `acceptance_record.py`: the tests are added first, run, and the
output is pasted. The same run shows the four pins green. After the change,
all six pass. That run is D1's evidence.

## Plan table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Tests first: `_retirement_act` fixture, the D2/D3 tests and the D5/D6/D7 pins in `tests/test_snapshot_readers.py`; run against unchanged code, D2/D3 red, pins and D8 green, output recorded | D1; D2; D3; D4; D5; D6; D7; D8; SR-178; SR-207; TC-278 | IF-091; IF-220 |  |
| P2 | `lane_acted_set` places each ledger-named id by `_tier_of`; `_registries_holding` deleted; docstring amended; the six tests green; `tests/test_snapshot_readers.py`, `tests/test_integrate_admission.py` and `tests/test_acceptance_record.py` run whole | D1; D2; D3; D8; D9; SR-178; SR-207; TC-278; TC-331; TC-269; TC-271; TC-153 | IF-091; IF-220 | P1 |
| P3 | Recipes sentence removed from `project-trajectory/skills/coordinator-cycle/references/recipes.md` §3 "The act turn"; `bootstrap.py --dest . --sync`; `.claude/` and `.agents/` copies byte-identical (`cmp`) | D10 | intra-module: a skill reference document, no code seam | P2 |
| P4 | Spine rows by Terra: LLR-278 detail and `code_symbol` amended, TC-278 method/expected/evidence amended; judged at the lane's checkpoint sitting (amendment kind), then the act | D11; SR-178; SR-207; TC-278 | IF-091 | P2 |
| P5 | `RESYNC_PACK.md` entry (kit-owned `scripts/acceptance_record.py`; nothing migrates) | D12; SR-178 | IF-091 | P2 |
| P6 | The landing tip: commit bar (`run_menu.py smoke`, budget enforced), `check_trajectory.py --strict`, `trace.py --strict`, full suite at close | D13; SR-178; SR-207; TC-278; TC-331; TC-240; TC-153; TC-269; TC-271 | IF-091; IF-220 | P3; P4; P5 |

P1 and P2 both cite D1, D2, D3 and D8, and the split is deliberate. P1
writes the tests and shows them red against the unchanged code. P2 makes
them green. D1 needs both sides of that run.

### P1: the tests first

- Add the fixture and the five tests in the table above, and leave the D8
  test unedited.
- Run `python -m pytest -q tests/test_snapshot_readers.py -k "retire or
  retirement or neither_section_moved"` on the unchanged module. Exactly
  the D2 and D3 tests must fail, with the messages in the table. If a pin
  fails, the fixture is wrong, not the code. Fix the fixture and rerun.
- The bootstrapped scaffold runs its own copies of the kit scripts
  (`test_the_scripts_under_test_are_the_scaffolds_copies`). The red run
  therefore needs the unchanged `acceptance_record.py` in the lane tree.
  Take it before P2 edits the module, or with that edit stashed.

### P2: the reader change

- Make design decision 1 exactly.
- `grep -rn _registries_holding project-trajectory tests` returns nothing
  (D9).
- Run these files whole:
  - `tests/test_snapshot_readers.py`, which holds TC-278's evidence and
    TC-269's and TC-271's tests;
  - `tests/test_integrate_admission.py`: TC-331, the merge slot's own path
    through `merge_approval_refusal` and `lane_acted_set`;
  - `tests/test_acceptance_record.py`: TC-153's module, for the
    `APPROVAL_ACT_CSVS` partition pin.
- Check `tests/test_module_size_ratchet.py` and
  `tests/test_complexity_ratchet.py`. The module shrinks by about ten lines.
  If either ratchet carries an exact entry for `acceptance_record.py` or for
  `lane_acted_set`, re-stamp it down in the same commit. Never stamp it up.

### P3: the recipes sentence

- In the act-turn paragraph, "...on a held rung it owes no act (removing a
  held row is the owner's); and the merge slot still refuses a retirement
  whose registry carries no other act in the branch (a residue left to a
  follow-up row). A first approval..." becomes "...on a held rung it owes no
  act (removing a held row is the owner's). A first approval...".
- Re-wrap the paragraph's lines without changing any other word.
- `PROCESS_OPTIONS.md` is unchanged (spec deliverable 2).

### P4: the spine rows (Terra authors; the coordinator runs the sitting)

- **LLR-278 `detail`.** "a snapshot is WIDENED only when the complete acted
  set holds no approved or re-attested row in that registry identity:"
  becomes "a snapshot is WIDENED only when the complete acted set holds no
  approved or re-attested row in that registry identity, a row the act
  ledger names being placed in the registry its id's tier names whether or
  not the row remains in the live registry at the head, so a retirement
  authorizes its own registry's copy:". The rest of the cell stays
  byte-identical.
- **LLR-278 `code_symbol`.** Drop `_registries_holding/`. That is traced
  upkeep, and `_tier_of` is already listed. `sr_refs`, `module`, `test_refs`
  and `rationale` are unchanged.
- **TC-278 `method`.** Append: "On a RELEASED rung, an act whose only
  re-attestation retires an Approved row the lane deleted, ruled by an
  accepted amendment verdict inside the amendment scope, merges with that
  registry's copy as its only copy. The same retirement on a held rung is
  refused by row."
- **TC-278 `expected`.** Append the clause "a retired row's re-attestation
  authorizes its own registry's copy, whether or not another act moved that
  registry".
- **TC-278 `evidence`.** Append the five new test ids
  (`tests/test_snapshot_readers.py::<name>`, `;`-separated, in the table's
  order).
- **Unchanged and not edited:**
  - SR-207, SR-178 and SR-228;
  - LLR-245 and TC-240, the writer's half;
  - LLR-338 and TC-368;
  - SR-226 and LLR-286;
  - IF-091 and IF-220 (data shapes);
  - CMP-006 and CMP-008;
  - `docs/runtime-flows.md`. Flow 4's merge slot and flow 6's act turn
    name no registry-resolution step, so no flow text moves.
- Both rows are Approved on released rungs. The lane's checkpoint sitting
  judges the two amendments: CLARITY or MEANING+BLESS is the adjudicator's
  call. The act then re-attests them (`intake.py snapshot --reattests`
  naming LLR-278 and TC-278). The checkpoint check is that each changed approved cell
  keeps its approved text verbatim except for the named insertion, with no
  CR bytes.

### P5: `RESYNC_PACK.md`

Add a new `###` entry at the end, in the house shape:

- the title: "The merge slot admits a retirement alone in its registry",
  `[since <landing parent>]`, with the anchoring note;
- **What changed:** the acted set places each row the act ledger names in
  the registry its id's tier names, so a retirement whose registry carries
  no other act in the branch is no longer refused as WIDENED;
- **Kit-owned files — overwrite:** `scripts/acceptance_record.py`;
- **What to do:** overwrite the file; nothing migrates, and no setting,
  registry or record format changes.

The coordinator re-anchors `[since ...]` at landing.

### P6: the landing tip

- Run the commit bar, `run_menu.py smoke`, with the smoke tier's 60 s
  budget enforced. Run `check_trajectory.py --strict` and `trace.py
  --strict`, both clean. Paste the real output.
- Run the full unfiltered suite once at close. It covers:
  - TC-240's `tests/test_baseline_snapshot.py`, the unchanged writer half;
  - TC-153's smoke pins;
  - TC-269, TC-271, TC-278 and TC-331.
- Regenerating the generated surfaces at landing (the dashboard and the
  architecture map) is the coordinator's landing step.
