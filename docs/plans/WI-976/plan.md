# WI-976 implementation plan — retire the perspective-record sidecar; the hat block in decomposition-round briefs

Planner: a fresh session that did not write the spec and will not build it. Read at lane tip `aa36a5b6e`
(`C:/Projects/ai-template.wt/wi-976`): the spec, its specref (review-churn plan item 14 with its
revisions 21–25, 30, 31), and the ruling it quotes (`contract_split` tip `961f9e47`, `docs/log.md`
"2026-09-06 — SN-036 / SR-161 owner ruling: review pass, not a guard", with that tip's SN-036,
SR-161, LLR-183, TC-178, TC-211 and decomposition-proportionality procedure text).

**Revision 2** (the one allowed revision), answering `docs/plans/WI-976/critique-1.md` at lane
tip `d848abda2`. Only P9, P10 and P11 change, plus the F1 cites in their table rows. Every other
step stands as planned.

## Revision 2: the critique's finding, judged

**F1 [MAJOR], the TC-211 sample after a re-sit: confirmed, and adopted.** Checked against the
spec and the code:

- The finding holds. P9 step 6 said "If the sample sitting is re-sat, TC-211's `inputs` move to
  the re-sit's `B` and `V`", with no condition. A RETURN of only the new LLR or the new TC is a
  normal outcome. SKILL §3 "Checkpoint" step 3 then re-sits "returned rows and any affected chain
  or newly changed rows", and those rows alone make a first-approval set of LLR and TC rows. So
  does a re-sit of SR-161 alone, which is an SR amendment. Under P5 (and D17) both sittings get
  `NOT_A_ROUND`, with no questions and no outcome lines. If such a re-sit became the sample, the
  P11 inspection would have no questions or outcomes to read, so D26, D27 and SR-161's acceptance
  could not be met.
- It is worse than the finding says. `inputs` is a statement the TC row makes: it is a TC-ID key
  in `project-trajectory/scripts/kitlib/spine.py`, beside `verifies` and `expected`. So moving
  TC-211's `inputs` after its sitting is itself a row change, and it must be re-sat. P9 step 6 did
  not carry TC-211 into that re-sit.
- The repair, carried in P9 step 6, P10 and P11:
  - The sample is the latest sitting of this lane that is itself a decomposition round: its judged
    set holds SN-036 as amended. No SR here awaits first approval, so SN-036 is the only trigger.
    Its brief must carry the perspectives part, and its verdict must name each applicable hat's
    outcome.
  - A narrow follow-up re-sit (the new LLR or TC, SR-161, LLR-183 or TC-178, without SN-036) leaves
    the sample and TC-211's `inputs` unchanged. Its verdicts are chain evidence: P11 reads them and
    names them in its record, so that the inspected record is a *completed* chain.
  - The sample moves only to a re-sit that judges SN-036: a sitting return of SN-036 (P9), or the
    owner's return of its text (D31, P10). TC-211 then joins that re-sit, with its `inputs` set to
    the re-sit's pre-fixed paths, as P9 step 1 does for the first sitting.

## The architectural-delta answer

DELTA: within

The WI makes an output depend on a new input: the two spine sitting briefs (first-approval,
amendment, and the combined sitting that composes them) and the spine-author prompt come to
depend on the hats roster and on the parent needs' and work item's tags. It adds no state (the
sidecar files, a kind of state, leave), no domain value, and no new boundary crossing: the new
call is `adjudicate_brief` → `plan_briefs`, both CMP-008 (`docs/requirements/components.toml`), so
the architecture rule demands no seam row, and `plan_briefs` → `hats` is the existing intra-CMP-008
read. The rows below carry the change explicitly: IF-133's `data` loses `load` (P2), the brief
composer's new input is drawn in runtime flow 6 of `docs/runtime-flows.md` (P5), and IF-115's
`compose(...)` contract (`docs/requirements/interfaces.toml`) keeps its signature and its
all-or-nothing rule, which the new refusal (a malformed roster in a round) obeys. No refactor
beyond this item is needed, given the size budget stated under P5.

## The table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The ruling record: the log fragment carrying the 2026-09-06 decision, its four acts, its closing line, the 2026-10-13 direction and the revision 25 SAFETY ruling, committed alone before any row text changes | D1; D2; SR-161 | no interface: a log fragment, no code | |
| P2 | The intent spine set (Terra intent turn): SN-036, SR-161, LLR-183, TC-178, TC-211 amended; the new LLR under SR-161 and its new TC drafted; IF-133's `data` cell amended | D3; D4; D6; D7; SR-161; SR-186; TC-178; TC-211 | IF-133 | P1 |
| P3 | Tests first, committed alone: the hat-block states, the verdict-parse invariance, the author-prompt slot, the roster pin split | D24; SR-161; TC-178 | no interface: tests only | P2 |
| P4 | The retirement: the `record` subcommand and its test module, LLR-297 and TC-312 retired through `retire.py`, the sidecar and its pointer paragraph | D5; D10; D11; D12; SR-161; TC-312 | IF-133 | P3 |
| P5 | The hat block in the sitting composition: `plan_briefs` round functions, `adjudicate_brief` reports judged parents and fills the optional `{hats}` slot, the two sitting templates declare it, flow 6 draws the new input, catalogue regenerated | D16; D17; D18; D19; D20; D21; D22; SR-161; TC-211 | IF-115; IF-113; the new adjudicate_brief to plan_briefs call is intra-component (both CMP-008), so no interface row is demanded | P3 |
| P6 | The spine-author prompt's `@HATS@` slot: `mkprompt.py` computes the block from the lane's work item; the template, the `coordinator-cycle` skill's dispatch step and the recipe name it | D23; SR-161 | no interface: this repo's own coordinator tooling under `scripts/coordinator/`, outside the component map | P5 |
| P7 | No instruction asks for the record: PROCESS.md §1, `spine-questions.md` (c3), both roster headers, the recipe line in all three copies; SAFETY leaves this repo's roster; the proportionality procedure and rubric | D8; D9; D13; D14; SR-161; SR-186; TC-211 | no interface: prose and registry comments only | P4; P5 |
| P8 | Shipping: one RESYNC entry superseding the 9233772b entry; generated pages and prompt catalogue regenerated; byte-budget delta and restamp; the live-surface sweep | D15; D32; D33; D34; SR-161 | no interface: docs and generated views | P6; P7 |
| P9 | The checkpoint: Terra reconciles the set (TC-211's `inputs` name this sitting's brief and verdict), the closure check, the combined sitting composed with the block, its brief committed beside its verdict; the sample stays a decomposition-round sitting through any re-sit | D25; D26; F1; SR-161; SR-186; TC-178; TC-211 | IF-115 | P8 |
| P10 | The acts: the adjudicator's act turn takes every act but one; SN-036's re-attestation is the owner's, attended, in text-then-act order; a headless leg stops before it; no landing before it; an owner return re-sits SN-036 with TC-211 as the new sample | D28; D29; D30; D31; F1; SR-161; TC-211 | IF-115 | P9 |
| P11 | TC-211's re-judge: a fresh session inspects the decomposition-round sample named in TC-211's `inputs`, with any follow-up re-sits as chain evidence, under the amended procedure; the result goes into the procedure's result section, then through `record_observation.py` | D27; F1; SR-161; SR-186; TC-211 | no interface: an Inspection and the existing observation writer | P10 |
| P12 | The bar on the landing tip: the commit bar green, `trace.py --strict` and `check_trajectory.py --strict` clean | D35; SR-161; SR-186; TC-178; TC-211 | no interface: verification only | P11 |

Excludes: TC-198 — it verifies SR-161 through LLR-202's `Hat-Refs` staging arm, which the spec keeps unchanged on purpose ("Unchanged, on purpose: `Hat-Refs` (LLR-183, LLR-202; TC-178, TC-198)"); no row amends or re-points it, and its tests run unchanged in the full suite at phase close.

## The steps

### P1 — The ruling record (D1, D2)

- Write `docs/log.d/2026-10-25-wi976-sn036-ruling.md`. It carries the 2026-09-06 decision ("satisfied
  by construction — a recorded hat-by-hat review of each decomposition round — and not by a
  machine-readable no-finding record plus a check"), its four acts, and its closing line verbatim
  ("Do NOT build `hats_no_finding`, a sidecar record, or a coverage check."). It cites `f6c7360f` (the
  fragment's first landing) and `contract_split`'s `docs/log.md` heading at `961f9e47`. It adds the
  owner's 2026-10-13 direction (revision 21; with 22, 23, 24, 30, 31 as the scope rulings) and the
  revision 25 SAFETY ruling (no application in a software-only repo; the shipped template keeps it).
  It states that SN-036's act cites this fragment directly, with no open item. It follows the fragment
  form the hook checks: a `Deferred open items:` line if the hook asks for one.
- Commit it alone, before P2. D2 is the commit order: `git log --format=%H -- docs/log.d/2026-10-25-wi976-sn036-ruling.md`
  is older than the first commit that touches a registry row.
- This path is the `<the fragment>` of P10's owner command. Record it in the lane's decisions record.
- Tests: none. The evidence is the commit order.

### P2 — The intent spine set (D3, D4, D6, D7)

Dispatch Terra's intent turn (SKILL §3 "Intent", recipes "Terra, first turn"), with `CHANGES=none` and
the spec's "Proposed row text" as the target meaning. Terra edits only the registries. New rows stay
`Drafted`, and no status flips.

- **SN-036 `acceptance`:** `contract_split`'s, verbatim. `need` and `why` unchanged.
- **SR-161:**
  - title "Each decomposition round is reviewed against its applicable perspectives";
  - `requirement` and `acceptance_criteria`: `contract_split`'s;
  - `verification` Test → Inspection;
  - `rationale`: `contract_split`'s, naming the ruling by its dates (2026-09-06, re-affirmed
    2026-10-13) and never by a file path (ruling 5);
  - `coincident`: the spec's text verbatim;
  - `hat_refs` and the other traced cells unchanged.
- **LLR-183 `detail`:** `contract_split`'s opening ("The row-level provenance part of perspective
  review, sited on the row rather than beside it.") and its closing clause ("Per-decomposition
  coverage is discharged by the existing review path ... let them go stale."). This replaces the
  `NOT DISCHARGED ... built under LLR-297.` tail. The middle stays this branch's text, and the traced
  cells are unchanged.
- **TC-178 `expected`:** `contract_split`'s split ("Satisfies LLR-183's Hat-Refs provenance,
  name-resolution, severity and effective-set mechanics; SR-161's perspective-review acceptance is
  inspected by TC-211."). Every other cell stays, including this branch's `tier = "Full"`.
- **TC-211:**
  - `verifies` becomes `["SR-161", "SR-186"]`;
  - `method` and `expected`: `contract_split`'s (one actual completed decomposition review record,
    its complete chain, an extra paraphrasing child; a missing outcome or a purposeless child is a
    finding);
  - at intent, `inputs` becomes `["docs/test/inspection-procedures.md", "SR-161", "SR-186",
    "docs/requirements/hats.toml"]`. The sidecar and the old sample's `DECOMPOSITION-AMENDMENTS.md`
    leave, because the sample moves to this lane's round. P9 adds the brief and the verdict once
    their paths are fixed;
  - `level`, `tier`, `automated`, `evidence`, `max_age`, `rubric`, `trigger` and `min_work_items` stay.
- **The new LLR** (`sr_refs = ["SR-161"]`, component CMP-008, contract voice, no `shall`): the spec's
  "New LLR" text. Its `module` and `code_symbol` name what P5 creates:
  - `project-trajectory/scripts/plan_briefs.py`: `sitting_hat_block`, `round_hat_block`,
    `fill_hat_slot`, `sitting_tail`, `hat_surface_for_work_item`, `NOT_A_ROUND`, `HAT_SLOT`;
  - `project-trajectory/scripts/adjudicate_brief.py`: `compose`, `combined_values`;
  - the two shipped templates, as boundary artifacts an LLR may name.
- **The new TC** (`verifies` the new LLR and SR-161, `level = "Unit"`, `tier = "Smoke"`). Every cited
  module is outside `conftest.SLOW_MODULES`; check that before the sitting. Its `method` names each
  state of D17–D22, and its `evidence` names P3's nodes in `tests/test_plan_briefs.py` and
  `tests/test_adjudicate_brief.py`. The P6 author-prompt tests are not cited: they pin this repo's
  unshipped tooling, which SR-161 does not ask for (TC-372's retirement reason).
- **IF-133 `data`:** drop `load`. It becomes "spine_carrier.load_needs, resolve, stem, folded,
  NEED_CARRIERS; absent registry [] and VACUOUS, unreadable carrier SystemExit". Its notes stand.
- LLR-297 and TC-312 are not deleted here. Their deletion rides P4's code commit, because deleting
  them now would leave `Implements: SR-161, LLR-297` tags and `tests/test_hats_record.py` pointing at
  nothing, which reds the strict lints until the code goes. They join the sitting's scope at P9
  (SKILL §3, "Carry retired rows into scope explicitly").
- Verify with `trace.py --strict` and `check_trajectory.py --strict` (an intent symbol binds at P9's
  reconcile). Grep the new LLR detail for `shall`. Diff the registries row by row against the turn's
  set (recipes, wi-960 D-012). Commit.

### P3 — Tests first (D24)

Commit the tests alone, before any code, each under one evidence class (SKILL §3, "Intent", step 2).
A new-behaviour test is `xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))` and must
fail at its own assertion. It probes `hasattr` or `prompts.slots`, or uses a stub, never an import
error. The code commit removes the marks.

`tests/test_plan_briefs.py` (new behaviour; each fails before because `plan_briefs` has no round
functions and `hat_surface_for_work_item` takes no `needs`):

- `test_a_sitting_with_no_first_approval_sr_and_no_amended_need_says_it_is_no_decomposition_round`:
  `sitting_hat_block(root, row, [], [])` returns `NOT_A_ROUND`.
- `test_outside_a_round_the_roster_is_not_read`: a malformed roster plus no parents still returns
  `NOT_A_ROUND`.
- `test_an_amended_need_is_a_parent_the_work_items_refs_do_not_reach`: a hat gated on a tag that only
  the amended SN carries appears when that SN is passed as `needs`, and not without it.
- `test_a_judged_sr_reaches_hats_through_the_need_it_names`: the judged SRs replace the row's own
  `SR-Refs`, and its `SpecRef` does not contribute.
- `test_the_work_items_tags_widen_each_need_and_sibling_needs_never_merge`: a conjunctive hat
  (`tags contains "a" and tags contains "b"`), with `a` on one need and `b` on another, does not apply.
  With `b` on the WI, it applies through the first need.
- `test_an_absent_roster_yields_the_opt_out_line_in_a_round`: `hats.NO_HATS`, with no outcome
  instruction.
- `test_a_malformed_roster_refuses_a_round_naming_the_roster`: the error names
  `docs/requirements/hats.toml`.
- `test_the_round_block_asks_one_outcome_line_per_hat_in_a_non_ruling_form`: the instruction's line
  form starts `- HAT ` and matches no `kitlib.verdict.ROW_RULINGS` tag and no grammar keyword.

`tests/test_adjudicate_brief.py` (new behaviour unless marked; each fails before because no template
declares `{hats}` and `compose` adds nothing):

- `test_a_first_approval_of_a_drafted_sr_carries_the_hat_block`
- `test_a_first_approval_of_llr_and_tc_rows_only_says_no_decomposition_round`
- `test_an_amendment_of_an_approved_need_carries_the_hat_block`
- `test_an_amendment_of_an_sr_only_says_no_decomposition_round`
- `test_an_override_without_the_hats_slot_composes_unchanged`: an override template with no `{hats}`
  composes byte-identically to `prompts.fill` of that override over the assembler's slot values, even
  over a malformed roster. Before the change this passes for the first half. Its strict-xfail witness
  is the malformed-roster half, written to assert that the round's brief on the shipped template
  refuses.
- `test_a_combined_sitting_carries_the_hat_questions_once_over_the_union`: an amendment section
  amending SN-A and a first-approval section with an SR under SN-B. Each need reaches its own
  tag-gated hat, and both questions appear exactly once. Each section's slot carries the pointer line.
- `test_a_combined_sitting_that_is_no_round_states_it_once`
- `test_a_malformed_roster_refuses_a_round_sitting_by_name`: `compose` returns `(None, reason)`, and
  the reason names the roster.
- `test_no_other_brief_declares_the_hats_slot`: characterization, unmarked. The done-when, red-tc,
  rejudge, disposition, consolidate, dispute, act and combined templates carry no `{hats}`. Adequacy
  witness: a slot added to the done-when template fails it.
- `test_hat_outcome_lines_change_no_ruling`: characterization, unmarked. A single-kind amendment
  verdict, a single-kind first-approval verdict and a combined verdict each parse through
  `kitlib.sitting.parse`, with `verdict.row_rulings` and `sitting.judged_rows` read alike, with and
  without `- HAT <NAME> -> ...` lines. Adequacy witness: a reader counting any `- ` line as a row line
  would add a ruling.
- The existing pin `set(values) == {"chain", "baseline", "questions"}` (line 1360) follows: it gains
  the reported-parents key.

`tests/test_prompts.py`:

- `test_the_two_spine_sitting_templates_declare_the_hats_slot` (fails before). The existing
  dispatcher-notes test then requires `{hats}` in their notes.
- `test_the_terra_brief_has_an_intent_form_before_build_round_1`: its slot pin gains `HATS` (fails
  before).
- `test_mkprompt_expands_hats_for_a_decomposition_turn`: a tmp WTROOT and lane holding a roster, a
  needs registry and the WI spec. `HATS=SN-001` yields the hat question in the output. Fails before,
  because the literal `SN-001` is substituted.
- `test_mkprompt_says_no_decomposition_round_for_hats_none`
- `test_mkprompt_refuses_without_hats`: exit 2, unfilled `@HATS@`. Fails before, because the template
  has no slot and exit is 0.
- `test_the_cycle_names_the_hats_slot_at_dispatch`: the `coordinator-cycle` SKILL's dispatch step and
  the recipe's "Terra, first turn" bullet name `HATS`. Fails before.

`tests/test_hats.py` (the D14 pin split):

- `LIVE_NAMES` drops SAFETY, and a new `TEMPLATE_NAMES` keeps it in place.
- `test_the_shipped_roster_selects_the_always_on_hats_at_minimum` compares the live roster with
  `LIVE_NAMES` (fails before: the live roster still has SAFETY).
- `test_template_and_instance_share_structure_and_the_template_ships_thirteen` compares the template
  with `TEMPLATE_NAMES`.
- `test_aspect_hats_ship_silent_by_design_and_switch_on_by_tag` reads SAFETY's condition from the
  template roster. The live roster has none, so reading it there would raise `KeyError`. Mark it
  per class.

Run the commit bar on the test commit, with the strict xfails red-as-expected.

### P4 — The retirement (D5, D10, D11, D12)

- `project-trajectory/scripts/hats.py`: delete everything the record section and its command alone
  use:
  - the code: `RECORD_SUFFIX`, `SPINE_ROWS`, `DECOMPOSITION_KEYS`, `_LIST_KEYS`, `PERSPECTIVE_KEYS`,
    `DERIVED_KEYS`, `RECORD_HEADER`, `_BARE_KEY_RE`, `_is_str_list`, `_record_shape_errors`,
    `AUTHORSHIP_KEYS`, `_authorship_errors`, `read_record`, `_spine_index`, `_parent_srs`,
    `_parent_needs`, `_with_tags`, `_record_contexts`, `derive_record`, `render_record`,
    `write_record`, `_perspective_findings`, `record_findings`, `_cmd_record`, and the `record`
    subparser;
  - the imports only they use: `datetime`, `write_atomic`, `toml_fields`, `toml_string`. Each has one
    use outside its import line today, inside the record section; confirm with a grep after the edit;
  - the docstring's record paragraph and its three `record` usage lines. The module docstring's
    opening becomes the review-path statement (the brief carries the questions; the sitting's verdict
    names each outcome), never a pointer that names a need as a claim.

  `spine_carrier.load_needs`, `context_from_need` and `_as_tags` stay, because the audit and the
  contexts use them.
- Delete `tests/test_hats_record.py`.
- `python project-trajectory/scripts/retire.py LLR-297 --reason "<...>"` and `... TC-312 --reason
  "<...>"`. Each reason says that the per-decomposition record is withdrawn by the 2026-09-06 owner
  ruling, re-affirmed 2026-10-13, and that coverage is discharged by the review path (SR-161 as
  amended; the new LLR states the brief's hat block). Name the new LLR and TC as `--successor` only if
  the sitting would read them as replacements. This plan's reading is no successor: the new rows
  state a different obligation. Record that choice as a decision.
- Delete `docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.perspectives.toml` and
  the "2026-10-03 (WI-688): this decomposition's SR-161 perspective record is ..." paragraph of
  `DECOMPOSITION-AMENDMENTS.md`. The six lane-authored sidecars under `docs/plans/` stay as inert
  lane records (coordinator-2026-10-25 D-003, the spec's default).
- One commit: code, test-module deletion, both deletions with their `docs/log.d/retired/` records,
  and the sidecar. A grep for `LLR-297` and `TC-312` over `project-trajectory/`, `tests/` and the
  registries is empty apart from the retirement records.
- Tests: P3's are unaffected. This commit makes no xfail pass. Its evidence is the removed module, the
  grep, and green strict lints (no dangling `Implements:` and no TC citing a missing test).

### P5 — The hat block in the sitting composition (D16–D22)

**Size budget.** `adjudicate_brief.py` is 984 SLOC (`check_complexity.module_sloc`) against the
ratchet's 1000-SLOC threshold, and a new module may not cross it without a reviewed baseline
(`tests/test_module_size_ratchet.py`). So every hat decision lives in `plan_briefs.py` (222 SLOC), and
`adjudicate_brief` only reports judged parents and makes calls: about +10 SLOC. The complexity
baseline row for `plan_briefs._parent_need_ids` (16) must not grow, so the `needs` widening goes
around it, not into it. If the composer cannot stay at or under 1000, the builder stops and reports
to the coordinator. It does not bump the baseline.

`project-trajectory/scripts/plan_briefs.py` (all `Implements: SR-161, <new LLR>`):

- `hat_surface_for_work_item(root, row, needs=())`: `needs` (exact SN ids) join the parents
  `_parent_need_ids` reaches. `_parent_need_contexts` takes the id map instead of the row. Each
  parent is still one WI-widened context, never merged (D18). `plan_runner`'s call is unchanged.
- `HAT_SLOT = "hats"`, the sitting templates' optional single-brace slot.
- `NOT_A_ROUND`: the stated line that this sitting judges no SR awaiting its first approval and no
  amended need, so no perspective question is put and no outcome is owed.
- `round_hat_block(root, row, needs=())`: the block for a decomposition round. It is
  `hats.brief_block` of the hats applicable to the WI context and each parent need, then one outcome
  instruction: name every listed hat once in the verdict, one line each, `- HAT <NAME> -> <rows it
  raised, or no finding> -> <why>`. A missing outcome is a finding for the review, never a check.
  With no applicable hat, or an absent roster, the block is `hats.NO_HATS` and asks for no outcome.
- `sitting_hat_block(root, row, srs, needs)`: `NOT_A_ROUND` when `srs` and `needs` are both empty, and
  then the roster is not read (D21's refusal applies to a round). Otherwise it is
  `round_hat_block(root, dict(row, **{"SR-Refs": ";".join(srs), "SpecRef": ""}), needs)`: the judged
  SRs replace the work item's own anchors, and its tags stay (D18).
- `fill_hat_slot(root, row, base, values, sitting=None)`: pops the assembler's reported parents
  (default none). It sets `values[HAT_SLOT]` only when `HAT_SLOT in prompts.slots(base)` (D19), and
  turns a `HatsError` into `prompts.PromptError` naming the roster, so `compose`'s existing refusal
  path carries it (D21).
  - Standalone (`sitting=None`): the value is `sitting_hat_block(...)`.
  - Inside a combined sitting: the parents and the "declared" bit go into `sitting` (a list), and the
    value is a pointer line saying the block follows the sitting's last section.
- `sitting_tail(root, row, sitting)`: returns `("", None)` when no section declared the slot (D19).
  Otherwise it returns `(text, None)`: one `=== THIS SITTING'S PERSPECTIVES ===` part over the union
  of every section's parents. The questions, or `NOT_A_ROUND`, appear once, and the instruction to
  write the outcome lines once, under the last section's heading (D20). On a malformed roster it
  returns `(None, reason)`. The outcome lines never take a `## ` heading, which `kitlib.sitting` would
  read as a kind.

`project-trajectory/scripts/adjudicate_brief.py`:

- Import `plan_briefs`. This adds no import cycle: `plan_briefs` imports `spine_carrier`, `prompts`
  and `hats` only.
- `amendment_values` reports the amended SN ids: the `unchained` rows whose id column is `SN-ID`.
- `first_approval_values` reports the SR ids it marks as this session's: the SR registry's entries in
  `registries`.
- Both report them under `plan_briefs`' parents key, which is never a slot.
- `compose(root, row, verdict_path, prompt_templates=None, sitting=None)` calls
  `plan_briefs.fill_hat_slot` inside its existing `try` before `prompts.fill`.
- `combined_values` passes one list to each section's `compose`, then appends `sitting_tail`'s text
  to `sections`. It refuses on its reason (all-or-nothing, rule 2).
- Other briefs: their templates declare no slot, so they are unchanged (D17).
- `governing_templates` is unchanged. The roster is evidence composed fresh into each brief, like the
  registries, not a template.

The two templates, `project-trajectory/prompts/adjudicate-first-approval.template.md` and
`adjudicate-amendment.template.md`:

- a `--- PERSPECTIVES (the declared hats this decomposition round must face) ---` / `{hats}` /
  `--- END ---` block before "Write your verdict to {verdict}";
- `{hats}` declared in the dispatcher notes as filled by the composer only where declared, so an
  override without it composes unchanged.

The verdict's machine lines and row-line forms are untouched (D22). `kitlib.verdict.ROW_RULINGS` and
`kitlib.sitting` are not edited.

`docs/runtime-flows.md` flow 6:

- a `Roster` participant and the line `Coord->>Roster: a decomposition round's judging brief reads
  the applicable hats' questions; any other sitting's says it is none (SR-161, <new LLR>)`;
- SR-161 added to the heading's id list. `check_flows` validates the ids, which exist after P2.

Regenerate `project-trajectory/prompts/CATALOG.md` (`gen_prompt_catalog.py`) in this commit: the
hook's `prompt-catalog` step refuses a stale catalogue.

Remove P3's marks for these tests. Run the full suite once before P9, because every first-approval
and amendment brief now carries a slot value, and the slow modules (`test_agent_loop*`,
`test_integrate*`) compose them.

### P6 — The author prompt (D23)

- `scripts/coordinator/terra-spine-prompt.template.md`: a `## Perspectives` section with `@HATS@`,
  with one sentence: when the turn adds an SR under a need or amends a need, put each question to the
  rows and say in the final message which rows each hat raised or that it raised none. Otherwise the
  slot says the turn is no decomposition round.
- `scripts/coordinator/mkprompt.py`: a `HATS` value is `none` or the `;`-joined SN ids the turn's
  change set amends or adds an SR under.
  - For `none` it fills `plan_briefs.NOT_A_ROUND`.
  - Otherwise it reads the lane worktree, `<WTROOT>/<LANE_SLUG>`. It loads the WI row there (`WI`,
    through `consolidate.read_rows`, as `compose_lane.py` does), and fills
    `plan_briefs.round_hat_block(lane, row, needs)`: the work item's own parents plus the named needs,
    WI-tag-widened, per need.
  - The kit is imported from the checkout the tool lives in (`layout.REPO`).
  - A missing `HATS` stays the existing unfilled-slot refusal (exit 2). An unknown WI, or a
    `HatsError`, is exit 2 with the reason.
- The `coordinator-cycle` skill: SKILL §3 "Intent" step 1 and "Checkpoint" step 1 name the slot. The
  recipe's "Terra, first turn" bullet states the fill. Then `bootstrap.py --dest . --sync`, so
  `.claude/skills/` and `.agents/skills/` match.
- No RESYNC entry: the tooling is unshipped.
- This lane's own checkpoint turn (P9) is filled by the lane's `mkprompt.py`, with `HATS=SN-036` and
  explicit `WTROOT` and `PY`, as this slot's first use. Record that as a decision.
- Remove P3's marks for these tests.

### P7 — Instructions, roster, procedure and rubric (D8, D9, D13, D14)

- **`project-trajectory/PROCESS.md` §1:** the sentence "Each decomposition also leaves a perspective
  record beside it (`scripts/hats.py record`): ... rather than the authoring transcript." goes. The
  clause before it, "the planning briefs put each applicable hat's question to the decomposition",
  widens to name the decomposition round's sitting brief and its verdict naming each hat's outcome.
  The rule stays in one home, and the net change shrinks the file. Run `byte-budget-guard` before and
  after (P8 restamps).
- **`project-trajectory/prompts/spine-questions.md` (c3)** becomes the ruling's rule. In a
  decomposition round the brief carries each applicable hat's question, and the review record (the
  sitting's verdict) names each applicable hat's outcome: the rows it raised, by their `Hat-Refs`, or
  no finding with its reason. A missing outcome is a review finding, never a coverage gate. The
  adjudicator judges adequacy. Keep (c2)'s `hats.py list` and `applicable` lines. This is a composed
  fragment, so regenerate the catalogue.
- **The template roster `project-trajectory/registries/hats.template.toml`:** "THE PER-DECOMPOSITION
  RECORD" paragraph becomes the same rule. It keeps SAFETY and its sixteen-hat count.
- **This repo's `docs/requirements/hats.toml`:**
  - the "WHAT IS NOT BUILT YET" paragraph goes, and the same rule paragraph replaces it;
  - "Sixteen hats today" and "review all sixteen" become fifteen;
  - the open SAFETY call closes, citing the revision 25 ruling (owner: no application in a
    software-only repo; the shipped template keeps it for adopters with physical products, a values
    divergence the dogfood rule allows);
  - `[hat.SAFETY]` is deleted.

  Confirm that no live row's `Hat-Refs` or need tag names SAFETY:
  `grep -rn "SAFETY" docs/requirements docs/test project-trajectory/scripts tests`. Expected: only
  the template, the test fixtures, and the `tests/test_hats.py` pins P3 split.
  `tests/test_dogfood_sync.py` must stay green: the structure is shared, the values diverge.
- **The recipe's perspective-record line** ("A lane that drafts a derived SR owes its perspective
  record ... wi-960 sitting 005)"), in `project-trajectory/skills/coordinator-cycle/references/recipes.md`,
  goes. Then `bootstrap.py --dest . --sync`, so the `.claude/skills/` and `.agents/skills/` copies
  follow.
- **`docs/test/inspection-procedures.md`:**
  - "Decomposition proportionality inspection" takes `contract_split`'s procedure text verbatim
    (roster, brief, review record, applicable-hat outcomes, no new carrier or machine coverage check);
  - "Bounded abnormal inputs" gains `contract_split`'s "Missing perspective outcome" item, here: the
    actual completed review record with one applicable hat's outcome omitted;
  - the closing "SR-161 machine-generated perspective-record producer remains ..." paragraph becomes
    `contract_split`'s closing paragraph, worded for this branch;
  - the INCOMPLETE 2026-09-06 result stays as history, relabelled "Historical INCOMPLETE" with
    `contract_split`'s explanatory sentences, linking the P1 fragment for the ruling. The 2026-10-03
    pass gets one line naming its observation record, so the section stops reading as if INCOMPLETE
    were current;
  - P11 adds the new result.
- **`docs/rubrics/decomposition-proportionality.md`:**
  - the header reads "Adjudicates: SR-161, SR-186";
  - R1: "The sample is one actual completed decomposition review record whose brief presents every
    applicable hat's question and whose record names each applicable hat's outcome, within the
    required spine boundary.";
  - B1: "An applicable hat's outcome is missing from the review record, or prose or Hat-Refs is
    presented in place of the review record's outcomes.";
  - R2, R3 and B2 unchanged.
- Tests: P3's `tests/test_hats.py` marks come off here. The rest is prose, checked by P8's sweep and
  P11's inspection.

### P8 — Shipping (D15, D33, D34)

- **`project-trajectory/RESYNC_PACK.md`:** one new §3 entry anchored at the lane's trunk base
  (`[since <base>]`, which the commit bar's RESYNC check holds). It states:
  - the `hats.py record` subcommand is gone, so an adopter's script calling it now fails (argparse
    refuses the unknown subcommand);
  - existing `*.perspectives.toml` files are inert notes, which nothing reads, so keep or delete them;
  - `adjudicate-first-approval.template.md` and `adjudicate-amendment.template.md` gain an optional
    `{hats}` slot, filled only where a template declares it, so an overridden template without it
    composes unchanged;
  - the roster template's header changed, so a preserved `docs/requirements/hats.toml` header comment
    is stale and is the adopter's to reword;
  - what to re-sync: `scripts/hats.py`, `scripts/plan_briefs.py`, `scripts/adjudicate_brief.py`, the
    two templates, `prompts/spine-questions.md` and `PROCESS.md`.

  The 9233772b entry gains the italic "*(Superseded by ... below ...)*" note (the pack's §1.3
  convention).
- **Regenerate:** `trunk_step.py --regen` (or by hand, with `--src project-trajectory/scripts` on both
  `gen_arch_map.py` forms). That covers `docs/cli-reference.md`,
  `docs/requirements/components.derived.toml`, `PROJECT_STATE.html` and `docs/open-items.html`, plus
  `trace.py` for the local `docs/test/report.md` and `gen_prompt_catalog.py` for the catalogue.
- **`byte-budget-guard`:** report PROCESS.md's byte delta and restamp its watched row, plus the
  skill's own capped row, whose size moves with the restamp. Edit the source and every tracked copy
  in one commit (`bootstrap.py --dest . --sync`).
- **The sweep (D15)**, as verification output pasted into the commit message, not as a test (a test
  would have to name the strings itself):
  `grep -rnE "perspectives\.toml|hats(\.py)? record|_cmd_record|RECORD_SUFFIX|write_record|record_findings" project-trajectory scripts tests .claude/skills .agents/skills CLAUDE.md AGENTS.md docs/requirements docs/test docs/rubrics PROJECT_STATE.html docs/cli-reference.md docs/open-items.html`.
  Expected hits: only the superseded entry and the new superseding entry in `RESYNC_PACK.md` (the
  retirement notice D33 requires), and none in the generated pages. "Perspective record" meaning
  `Hat-Refs` stays, on purpose.

### P9 — The checkpoint and its sample (D25, D26, F1)

1. Fix the sitting's paths before the checkpoint turn:
   - verdict `V = docs/reviews/wi-976/<NNN>-ADJUDICATE-<sha7>.md`, where `<sha7>` is the build tip the
     checkpoint reconciles;
   - brief `B = <V without .md>.brief.md`.

   TC-211 must name both before the commit that adds them exists, so the label names the reconciled
   build tip rather than the post-reconcile tip. Record that as a decision.
2. Terra, resumed: the checkpoint turn, filled per P6 with `HATS=SN-036`. It confirms the builder's
   change list, binds the new LLR's `code_symbol` and the new TC's `evidence` to the built names, and
   sets TC-211's `inputs` to the P2 set plus `B` and `V`. Carry LLR-297 and TC-312 into scope as
   retired rows.
3. The closure check and the arms map (SKILL §3 "Checkpoint", step 2; recipes). Run `trace.py
   --strict` and `check_trajectory.py --strict`.
4. Compose with `compose_lane.py` (`combined`, scope tokens `amendment:` SN-036, SR-161, LLR-183,
   TC-178, TC-211, LLR-297, TC-312, and `first-approval:` the new LLR and TC). Check for a
   `REFUSED` line before any append (WI-894). The composed brief must carry the perspectives part with
   SN-036's applicable hats (SN-036 is an amended need, so this is a decomposition round), and the
   sections' pointer lines. Write the launched brief to `B` and commit it, so the lane is clean, the
   brief sits beside its verdict, and it is the exact text sent.
5. Launch with `coordinator_adjudicate.py adjudicate --brief-file B --brief combined --wi WI-976
   --verdict V`. The sitting writes `V`, with one `- HAT <NAME> -> ...` line per applicable hat
   (D20/D26), and commits it.
6. Check that `V` names every hat in the perspectives part. A missing one is a finding to re-sit,
   never a check. A RETURN is re-sat alone (SKILL §3 "Checkpoint", step 3: the returned rows and
   any affected chain or newly changed rows). Which sitting is TC-211's sample depends on what the
   re-sit judges (F1):
   - **A re-sit without SN-036.** Examples: only the new LLR or TC, or SR-161, LLR-183 or TC-178
     returned for their own text. This re-sit is not a decomposition round, so its brief says
     `NOT_A_ROUND` (P5, D17).
     - The sample stays `B` and `V`, and TC-211's `inputs` are not touched.
     - The re-sit's verdict, committed as usual under `docs/reviews/wi-976/`, is chain evidence for
       P11. It is not a sample.
     - Record in `docs/decisions/wi-976.toml` that the sample stays and why.
   - **A re-sit with SN-036.** Here the sitting returned SN-036, so its children return with it for
     their chain. This re-sit is a decomposition round, and it becomes the sample.
     - Before the reconcile turn that precedes it, fix its paths `B'` and `V'` as in step 1.
     - Terra sets TC-211's `inputs` to the P2 set plus `B'` and `V'`. `inputs` is a row statement
       (`kitlib/spine.py`'s TC-ID keys), so TC-211 joins the re-sit's scope.
     - Compose the re-sit as in step 4. Its brief must again carry the perspectives part.
     - Commit `B'` beside `V'`, and check `V'` as above.
   - **Never move TC-211's `inputs` to a sitting whose brief says `NOT_A_ROUND`.**

### P10 — The acts and the owner-held step (D28–D31, F1)

- The act turn (SKILL §4; recipes) takes every act the verdict authorizes except SN-036's. The
  amendment act goes first: SR-161, LLR-183, TC-178 and TC-211 by their marks, with LLR-297 and
  TC-312 listed in `--reattests` until the recorded copy drops them. Then the first-approval act for
  the new LLR and TC.
- **SN-036 is the owner's.** Attended in the lane, after the text commit:
  `intake.py snapshot --approves stakeholder-needs=docs/log.d/2026-10-25-wi976-sn036-ruling.md --reattests SN-036`,
  adding `--verdict V` where the route asks for it. If a headless leg marked the lane, it is re-claimed
  first (SKILL §7, "The re-claim").
- **A headless leg** brings the lane to that act and stops. It commits the verdict and takes every
  other act. It records the exact command, `V`, the rows and the fragment path in
  `docs/decisions/wi-976.toml` and under the handoff's "For the owner". It never takes the act.
- **No landing before the act.** If the owner returns SN-036's text, Terra reworks it, together with
  any row whose meaning follows it (SR-161's acceptance and `coincident`), and the reworked rows are
  re-sat alone. That re-sit judges an amended SN-036, so it is a decomposition round and becomes the
  sample under P9 step 6's second case (F1):
  - TC-211 joins it, with its `inputs` moved to the re-sit's pre-fixed `B'` and `V'`;
  - the re-sit's acts follow, and the owner's SN-036 act names `V'`;
  - P11 waits for those acts.
- Evidence: the act ledger entry and the snapshot copy at the act commit. `trace.py --strict` shows
  no unattested drift.

### P11 — TC-211's re-judge (D27, F1)

- After the acts (the last ones, if P9 or P10 re-sat anything), a fresh session inspects the
  sample.
  - **The sample** is the brief and verdict TC-211's `inputs` name: `B` and `V`, or `B'` and `V'`
    if the sample moved under P9 step 6. By that rule it is always a decomposition-round sitting
    (F1). This step reads it from TC-211's `inputs`, so P9 and P11 agree.
  - **The inspector** wrote none of the rows, the sample's brief or the sample's verdict: not Terra,
    not any of the lane's adjudicators, not the coordinator.
  - **What it checks**, against the sample, the roster and the chain:
    - it re-derives the applicable set from the roster for SN-036, widened by WI-976's tags;
    - it confirms that the sample's brief presents every question and that its verdict names every
      outcome;
    - it reads the lane's narrow follow-up verdicts under `docs/reviews/wi-976/`, the ones P9 step 6
      kept as chain evidence. With them it confirms that the chain the sample judged is completed:
      every row that was returned has since been re-sat and approved;
    - it checks the chain's child purposes and the stopping reason;
    - it rejects the two abnormal inputs (missing perspective outcome, paraphrasing child).
  - **The follow-up verdicts are not added to TC-211's `inputs`.** Adding them would change an
    approved row after its sitting.
- Its record goes under `docs/reviews/wi-976/`. It names the sample and each follow-up verdict it
  read.
- Then, in one commit, in this order: write the dated result into "Decomposition proportionality
  inspection result" (it is a declared input, so it must be written before the digest), then
  `record_observation.py --tc TC-211 --outcome pass|fail --by "<model, session, TC-211>"`. A fail is
  recorded as a fail and routed as a finding, never re-run until it passes.

### P12 — The bar (D32, D35)

- On the landing tip: `run_menu.py smoke` green. Paste the real output.
- `trace.py --strict` and `check_trajectory.py --strict` are clean.
- `check_docs.py --root . --strict-orphans` is clean (the lane adds `B`, which sits under the
  orphan-exempt `docs/reviews/`, and a log fragment).
- The full unfiltered suite once (phase close).
- The lane lands alone (revision 37), and only after P10's owner act.

## Cited rows, in one place

- SRs: SR-161 (amended), SR-186 (unchanged; verified by TC-211) — `docs/requirements/system-requirements.toml`.
- TCs: TC-178 and TC-211 (amended), TC-312 (retired, P4), TC-198 (excluded above), the new TC (P2) —
  `docs/test/test-cases.toml`.
- Interfaces: IF-133 (`data` loses `load`), IF-115 (the composer's contract, signature kept), IF-113
  (the loader the two templates resolve through) — `docs/requirements/interfaces.toml`.
- Components: CMP-008 owns `hats`, `plan_briefs` and `adjudicate_brief` (no change); CMP-006 owns
  LLR-183's modules (no change) — `docs/requirements/components.toml`.
- Runtime flows: flow 6 gains the roster read (P5) — `docs/runtime-flows.md`.
