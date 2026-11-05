# WI-983 plan: a decomposition round's sitting brief names a stopping-boundary line

Planner: fresh session, 2026-11-04, at lane tip `e73e49cf8`. Read in full: the spec `docs/work/active/wi-983/WI-983-sitting-records-stopping-boundary.md`, its specref `docs/reviews/wi-976/021-ADJUDICATE-095bb79.md`, and the queued row `docs/work/queued/WI-998-reinspect-tc-211.md`. SR-186, SR-161, LLR-360, TC-178, TC-198, TC-211 and TC-399 were read as rows. The findings below were confirmed against the code at this tip.

## What the build changes, in one paragraph

`plan_briefs.round_hat_block` gains one instruction, `_STOPPING_INSTRUCTION`, placed after the hat outcome instruction and carried on both of that function's paths, so a round with no roster or no applicable hat carries it too. `sitting_tail` stops treating a no-hats round as having nothing to place. The two sitting templates change only in their dispatcher notes, and `prompts/CATALOG.md` is regenerated. LLR-360 takes SR-186 as a second parent and states the line, and TC-399 verifies it. SR-186, SR-161, `docs/test/inspection-procedures.md` and `docs/requirements/hats.toml` are untouched, because all four are TC-211 inputs and moving one would stale the observation of record that WI-998 replaces.

## Design decisions the rows depend on

1. **The line lives in the composer's block, not in template text.** The spec needs the line in a round and nowhere else, and it needs a template with no slot to compose unchanged. Static template text would reach every non-round and could never be absent from one. So "the shipped templates carry it" means a brief composed from each shipped template carries it, through the `{hats}` slot both already declare. D2's test composes the real shipped text, so it fails if either template loses the slot.

2. **It goes in `round_hat_block`, never `round_questions`.** `scripts/coordinator/mkprompt.py` fills the spine author's `@HATS@` from `round_questions`, so the author's prompt does not move. `hat_surface` and the planner brief do not move either. The spec promises the line to the sitting brief only.

3. **The line's text.** It cites no id of this repo, so it means the same in an adopter's brief (CLAUDE.md, "Templates must stay copy-ready").

   ```python
   _STOPPING_INSTRUCTION = (
       "For each chain this round retains, state why further splitting would "
       "only paraphrase or duplicate, on its own line beside your row lines and "
       "under no heading of its own:\n\n"
       "    - STOPPING BOUNDARY <chain, top row first> -> <why further splitting "
       "would only paraphrase or duplicate>\n\n"
       "A stopping-boundary line rules no row and is no machine line. A retained "
       "chain with no stopping-boundary line is a finding for the review of this "
       "verdict, never a check."
   )
   ```

   The form must not use `->` inside the chain, and the instruction's `<chain, top row first>` keeps the chain as one field. `<chain ...>` is angle-bracketed, so `prompts.fill` sees no slot. It stays a private constant beside `_OUTCOME_INSTRUCTION`, so LLR-360's `CodeSymbol` cell, which already names `round_hat_block`, does not change.

4. **Why the verdict parses the same.** `kverdict._ruled_row` matches only a line opening with a declared tag (`- [APPROVE]`, `- [RETURN]`, `- [MEANING]`, `- [CLARITY]`, `- [MEANING+BLESS]`). `- STOPPING BOUNDARY` opens with none, even when the chain names a ruled row. P3 pins this rather than assuming it.

5. **The set the line reaches.** No classifier is added. `sitting_hat_block`'s existing `if not srs and not needs` decides it.

   | Sitting | Line | Pinned by |
   |---|---|---|
   | first approval of an SR, alone | yes, once | `test_a_round_sitting_composed_alone_carries_the_stopping_boundary_line_once` |
   | amended approved need, alone | yes, once | the same, second parameter |
   | combined, either kind makes the round | yes, once, in the perspectives part after the last section | `test_a_combined_round_carries_the_stopping_boundary_line_once_after_its_last_section` |
   | round, no roster or no applicable hat | yes, beside `NO_HATS`, no `- HAT` form | `test_a_round_with_no_applicable_hat_still_carries_the_stopping_boundary_line`, `test_a_combined_round_with_no_applicable_hat_is_told_where_to_write_the_line` |
   | SR amended alone; LLR and TC rows only; combined non-round | no: `NOT_A_ROUND` as today | `test_a_non_round_carries_no_stopping_boundary_line`, `test_a_sitting_that_is_no_round_carries_no_stopping_boundary_line` |
   | template with no perspective slot | composes unchanged | existing `test_an_override_without_the_hats_slot_composes_unchanged`, whose `text == plain fill` already covers it |
   | roster that cannot be read, in a round | refuses, naming it | existing `test_a_malformed_roster_refuses_a_round_naming_the_roster`, `test_a_malformed_roster_refuses_a_round_sitting_by_name` |

   Both composing routes (`agent_loop` and `scripts/coordinator/compose_lane.py`) call `adjudicate_brief.compose`, which calls `fill_hat_slot`, so one edit reaches both.

6. **Bounds, stated so they are not silent.** The line asks and nothing checks, so no verdict reader, gate or lint is added. A round that retains no chain owes no line: the instruction is "for each chain", and every row returned means none is retained. An override that declares `{hats}` gets the line, because that is the slot's meaning. The `--- PERSPECTIVES ---` heading in both templates stays, since a heading edit would change every non-round's brief for no gain.

## Which row states each behaviour

SR-186 already states the obligation: its requirement says the process shall "record the stopping decision in the scoped decomposition record", and its acceptance says the record "states why the process stops at that independent-value boundary". SR-186 needs no text, and its rationale's "new machine gate" exclusion holds, because the line only asks. No LLR states how a brief asks. SR-186 has no LLR today, and LLR-360 names only SR-161. So every behaviour below is added to LLR-360 by amendment, and TC-399 states only what the amended LLR-360 states.

| Behaviour | Stated today by | Plan |
|---|---|---|
| a round's brief carries the named line, per retained chain | SR-186 (the obligation); no LLR | LLR-360 `Detail`, new sentence; `SR-Refs` gains SR-186 |
| a round with no roster or no applicable hat carries it | none | LLR-360 `Detail`, same sentence |
| another judged set carries no line | none | LLR-360 `Detail`, amended sentence |
| the line fills the slot only where a template declares it | none | LLR-360 `Detail`, amended sentence |
| a combined sitting carries it once, after its last section, and says where the verdict writes it | none (the row says "carries the questions once") | LLR-360 `Detail`, amended sentence |
| the line is no row ruling and no machine line, and a missing reason is a review finding | none | LLR-360 `Detail`, new sentence |
| an unreadable roster refuses a round | LLR-360, last sentence | unchanged |

This is one amendment and no new row. The spec says the lane's spine change "amends design and test rows", and the line shares LLR-360's round classification, slot, code and test.

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. The spec's S5 answer holds: no new mode class, no new boundary, no new authority. Its "added content" is a new case in a domain, so the honest clause is "add a value", and the rows below carry it.

1. **Mode classes (A2): none added.** `plan_briefs` stays a stateless function of its inputs. I read Flow 6 in `docs/runtime-flows.md`. Its line "a decomposition round's judging brief reads the applicable hats' questions, and any other sitting's says it is none (SR-161, LLR-360)" stays true, the line touches no roster and adds no message or transition, so `docs/runtime-flows.md` is not edited.

2. **Value domains (A3, A6): one case added, one case widened, carried by P2 and P6.**

   | Domain | Today | After |
   |---|---|---|
   | `{hats}` slot value | not a round: `NOT_A_ROUND`; round with hats: questions and outcome instruction; round with none: `NO_HATS` | the same three cases, with the two round cases gaining the stopping instruction |
   | a sitting verdict's lines | row lines, the machine line, `- HAT` lines | those, plus `- STOPPING BOUNDARY` lines, which are read by the verdict's review only |
   | the parsed verdict (`kitlib/verdict`, `kitlib/sitting`) | rulings, judged rows | unchanged, pinned by `test_stopping_boundary_lines_change_no_ruling` |

   The home of the domain statement is LLR-360's `Detail`, as it is for the `- HAT` line. I checked `docs/requirements/interfaces.toml`: no row states the slot's values or a sitting verdict's non-ruling lines. IF-115 states `compose`'s signature, IF-113 the template loads, and IF-175 and IF-287 the parsed readers, and none of those texts changes. `plan_briefs` owns no IF row, as WI-982's plan also recorded. So no interface row is edited.

3. **Output against input (A4): no new cell.** Recorded here, as the skill allows when planning.

   | Output | Inputs today | Input added |
   |---|---|---|
   | whether the block asks for stopping lines (new) | `srs`, `needs` (already what makes a round) | none |
   | `sitting_tail`'s placement sentence | the composed block | none; only its test narrows to `NOT_A_ROUND` |
   | hat questions, outcome instruction | as today | none |

4. **Boundaries (A6, A8): none added.** `docs/requirements/components.toml` keeps CMP-008 as the home of `plan_briefs`, `adjudicate_brief` and `prompts`, and LLR-360's `Component` stays CMP-008. Requirement descent (A8): adding a separate LLR under SR-186 would duplicate LLR-360's classification and slot with no independent decision, so it stops at LLR-360.

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Confirm WI-998 is on trunk before the claim, with the spec's steps and order; no file changes | D3; SR-186; SR-161 | no interface: reads a spec and the commit order | |
| P2 | The spine trace cells: LLR-360 `SR-Refs` gains SR-186; TC-399 `Verifies` gains SR-186 and `Evidence` names P3's tests | D1; D2; SR-186; SR-161; TC-399 | no interface: row trace cells only | P1 |
| P3 | The tests alone, under strict xfail marks with the characterisations beside them; no shipped file | D1; D2; SR-186; SR-161; TC-399 | IF-115; IF-175; IF-287 | P2 |
| P4 | The line: `_STOPPING_INSTRUCTION`, `round_hat_block`, `sitting_tail`, both templates' dispatcher notes, and the regenerated catalogue | D1; D2; SR-186; SR-161; TC-399 | IF-115; IF-113; IF-098 | P3 |
| P5 | The one RESYNC_PACK entry | D4; SR-186; SR-161 | no interface: documents only | P4 |
| P6 | LLR-360's and TC-399's text, written after the code settles, and the lane's one sitting | D1; SR-186; SR-161; TC-399 | no interface: row text only | P5 |
| P7 | The commit bar and both strict lints on the landing tip | D4; SR-186; SR-161; TC-399 | no interface: runs the bar | P6 |

Excludes: TC-178 — it verifies LLR-183's Hat-Refs resolution and effective-set mechanics, and this row touches neither Hat-Refs nor the roster.
Excludes: TC-198 — it verifies LLR-202's staged Hat-Refs amendment guard, which this row does not touch.
Excludes: TC-211 — its re-inspection is WI-998's by the spec's S1 split: the amended inputs need a round composed after this row lands, so this lane changes none of its inputs and its fail stands as the observation of record.

**Why clauses are cited twice.** D1 sits on P2 (the chain), P3 (the failing tests), P4 (the behaviour) and P6 (the row text). D2 sits on P2, P3 and P4 the same way. D4 sits on P5 (the RESYNC entry) and P7 (the bar and lints). These are separate deliverables of one clause, not overlapping scope.

**Commit boundaries.** P2 and P3 are one commit touching no shipped file, so `Evidence` never names a test that is absent. P4 and P5 are one code commit, for two reasons: strict xfail marks turn red on the first XPASS, so they all come off together, and the commit bar refuses a shipped-file change without a RESYNC entry. P6 follows review.

### P1: WI-998

D3 is already delivered and this step confirms it, changing nothing. Checked at planning and to be re-checked by the builder:

- `git merge-base --is-ancestor e72b1f700 2965e4762` exits 0, so WI-998's filing precedes this row's claim.
- `docs/work/queued/WI-998-reinspect-tc-211.md` has `needs = ["WI-983"]`, and its Done-when runs in the spec's order: amend TC-211's `inputs` through the amendment route; a fresh session inspects; the result goes in the procedure's result section; the observation writer records it last.
- The builder confirms WI-998 is off the queue table in `docs/status.md`, which this planner was told not to read.

### P2: the spine trace cells

Authored before the build, as `spine-authoring/references/in-lane.md` orders. No new id is reserved.

- **LLR-360 `SR-Refs`:** `SR-161;SR-186`. It routes to adjudication (`intake.ROUTED_TRACED_CELLS`), so it joins P6's sitting.
- **TC-399 `Verifies`:** add SR-186, since in-lane.md requires a TC to name its LLR and that LLR's SR. This also routes to P6's sitting.
- **TC-399 `Evidence`:** append every P3 test by `file::name`.
- `Module` is unchanged, since it already names `plan_briefs.py` and both templates. `CodeSymbol` is unchanged (decision 3).

### P3: the tests

Each new test's docstring carries `Implements: TC-399` on its own line. New behaviour takes `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`, so the red must reach the test's own assertion. Tests match the literal `- STOPPING BOUNDARY ` rather than a private constant, as the existing tests match `- HAT `, so a missing symbol cannot stand in for a red.

| Test | Class | Fails before the change on |
|---|---|---|
| `tests/test_plan_briefs.py::test_a_round_block_asks_a_stopping_boundary_line_beside_the_hat_outcome_lines` | new | the block holds the `- HAT` form and no `- STOPPING BOUNDARY` form; it also asserts the line follows the outcome instruction and says "paraphrase or duplicate" (D1) |
| `tests/test_plan_briefs.py::test_a_round_with_no_applicable_hat_still_carries_the_stopping_boundary_line`, over no roster and a roster whose only hat does not apply | new | the block is `NO_HATS` alone; it also asserts `NO_HATS` stays and no `- HAT` form appears |
| `tests/test_plan_briefs.py::test_a_stopping_boundary_form_is_no_row_line_and_no_machine_line` | new | no form is found; then, as the existing hat form test does, each form must match no row tag or machine keyword and yield `{}` from `kverdict.row_rulings` |
| `tests/test_plan_briefs.py::test_each_shipped_sitting_template_carries_the_stopping_boundary_line`, over `ADJUDICATE_FIRST_APPROVAL` and `ADJUDICATE_AMENDMENT` | new | D2. It loads the real shipped template, runs `fill_hat_slot` with parents that make a round, fills the remaining slots with stubs through `prompts.fill`, and finds no line in the text. It runs in-process, so it is the smoke tier's pin |
| `tests/test_plan_briefs.py::test_a_non_round_carries_no_stopping_boundary_line` | characterisation | passes before. Witness: the instruction appended in `sitting_hat_block` ahead of its round test |
| `tests/test_adjudicate_brief.py::test_a_round_sitting_composed_alone_carries_the_stopping_boundary_line_once`, over a drafted SR and an amended need | new | the real `compose` gives a count of 0, not 1 |
| `tests/test_adjudicate_brief.py::test_a_combined_round_carries_the_stopping_boundary_line_once_after_its_last_section` | new | the count is 0; it also asserts the line follows `_PERSPECTIVES_HEAD` and the last `_SECTION_HEAD` |
| `tests/test_adjudicate_brief.py::test_a_combined_round_with_no_applicable_hat_is_told_where_to_write_the_line` | new | with no roster the tail is `NO_HATS` alone, with neither line nor placement sentence |
| `tests/test_adjudicate_brief.py::test_a_sitting_that_is_no_round_carries_no_stopping_boundary_line`, over an SR amended alone, LLR and TC rows only, and a combined non-round | characterisation | passes before. Witness: a line added to the template text, or a round test widened to `amended` |
| `tests/test_adjudicate_brief.py::test_stopping_boundary_lines_change_no_ruling`, over `test_hat_outcome_lines_change_no_ruling`'s three verdicts | characterisation | passes before. Its fixture names a ruled row in the chain. Witness: a reader counting any `- ` line, or any line naming a row, as a ruling |

**One existing test is amended here.** `tests/test_plan_briefs.py::test_an_absent_roster_yields_the_opt_out_line_in_a_round` asserts `block == hats_roster.NO_HATS`, which P4 makes false. It becomes `hats_roster.NO_HATS in block`, which holds on both sides of P4, so it can move in this commit. Its `"- HAT " not in block` stays.

**Which tier runs what.** `test_adjudicate_brief` is in `SLOW_MODULES`, so the smoke tier skips it. Each build round runs its tests by name through `integrate.py attest --tests`. The `test_plan_briefs` tests are the smoke tier's in-process pin. The builder confirms `_hat_repo(tmp_path, roster=None, ...)` leaves no roster in the demo spine before relying on it.

### P4: the line

In `project-trajectory/scripts/plan_briefs.py`:

```python
def round_hat_block(root, row, needs=(), srs=()):
    block = round_questions(root, row, srs, needs)
    if block != hats_roster.NO_HATS:
        block += "\n\n" + _OUTCOME_INSTRUCTION
    return block + "\n\n" + _STOPPING_INSTRUCTION
```

- Add `_STOPPING_INSTRUCTION` after `_OUTCOME_INSTRUCTION` (decision 3).
- Rewrite `round_hat_block`'s docstring, since "asks for nothing" stops being true, and extend the section comment above `HAT_SLOT` by one clause.
- In `sitting_tail`, the test `block in (NOT_A_ROUND, hats_roster.NO_HATS)` becomes `block == NOT_A_ROUND`, since the second value can no longer occur. A no-hats round then gets its placement sentence, which it needs. The sentence becomes "Write these lines once for the whole sitting, under the last section's `## <kind>` heading.", because a no-hats round has no outcome lines. No test pins the old wording.
- `round_hat_block` and `sitting_tail` read `Implements: SR-161, SR-186, LLR-360`.

In `project-trajectory/prompts/adjudicate-first-approval.template.md` and `adjudicate-amendment.template.md`, the `{hats}` dispatcher note gains: "It also asks the verdict for one `- STOPPING BOUNDARY` line per retained chain, and a round with no applicable hat still carries that." These notes are stripped before sending, so no brief changes through them, but they would otherwise misdescribe the slot. The digest moves, so run `project-trajectory/scripts/gen_prompt_catalog.py` to regenerate `project-trajectory/prompts/CATALOG.md`, and remove P3's xfail marks.

No size stamp is owed. `plan_briefs.py` is 607 lines, under the 1000 SLOC threshold and absent from `tests/test_module_size_ratchet.py`. Neither edited function is in `docs/complexity-baseline`, which lists only `_parent_need_ids` from this module.

### P5: the RESYNC entry

One new §3 entry in `project-trajectory/RESYNC_PACK.md`, after "A minted adjudication row carries its authoring work item's tags" and before "## 5. Promotion", anchored `[since <sha>]` at the lane's trunk base as read at build time, with the anchored-at-the-preceding-commit note the last entries use.

- **What changed:** a decomposition round's sitting brief asks for a `- STOPPING BOUNDARY` line per retained chain, beside the hat outcome lines, including a round with no roster or no applicable hat. A combined sitting carries it once.
- **What to do (no forced migration):** overwrite the kit-owned files. A template override declaring `{hats}` gets the line, and one without the slot composes unchanged. No setting or registry changes. A reader of adopters' verdicts needs no edit, since the line is no row ruling and no machine line. Verdicts now owe the line, and a missing one is a finding for the verdict's review.
- **Kit-owned files — overwrite:** `scripts/plan_briefs.py`, `prompts/adjudicate-first-approval.template.md`, `prompts/adjudicate-amendment.template.md`, `prompts/CATALOG.md` (regenerate).

### P6: the row text

Written once the code stops moving, then judged top-down in the lane's one sitting with P2's two routed cells: LLR-360 before TC-399. That sitting amends LLR and TC rows only, so it is no decomposition round and its own brief carries no line, as the spec says.

**LLR-360.**

- **`Title`:** "Perspective questions and the stopping-boundary line in a decomposition-round sitting".
- **`Detail`, new sentences** after "...parses to the same rulings and judged rows as one without them.": "A decomposition round's brief also carries a named stopping-boundary line, asking the verdict to state, for each retained chain, why further splitting would only paraphrase or duplicate; a round with no roster or no applicable perspective carries it beside its no-perspective line, because the stopping decision rests on no perspective. A stopping-boundary line is likewise neither a row-ruling line nor a machine line, and nothing checks for it: a retained chain with no stopping reason is a finding for the review of the verdict."
- **`Detail`, amended sentences:**
  - "another judged set carries no perspective question" becomes "another judged set carries no perspective question and no stopping-boundary line".
  - "Questions fill the perspective slot only when the sitting template declares it" becomes "Questions and the stopping-boundary line fill the perspective slot only when the sitting template declares it".
  - "A sitting composed from several judgement kinds carries the questions once." becomes "A sitting composed from several judgement kinds carries the questions and the stopping-boundary line once, after its last section, and says under which section the verdict writes those lines."
- **`Rationale`, added:** "A verdict's stated form otherwise has no place for a chain's stopping reason, so a sitting answering the form exactly drops it; a named line gives the reason that place without a new record carrier or check."

**TC-399.** Each clause states only what the amended LLR-360 states.

- **`Method`, added before "and those outcome lines do not alter":** "every decomposition round, whichever shipped sitting template composes it and with or without a roster or an applicable perspective, carries one stopping-boundary line asked of each retained chain; a non-round carries none; a combined sitting carries it once after its last section and says where the verdict writes it;". The tail becomes "and those outcome and stopping-boundary lines do not alter parsed row rulings or judged rows".
- **`Expected`:** "(parent SR-161)" becomes "(parents SR-161 and SR-186)", and add: "a decomposition round's brief asks the verdict for each retained chain's stopping reason; SR-186's recorded-stopping-decision acceptance is inspected by TC-211."

SR-161, SR-186 and TC-211 stay as they are.

### P7: the bar

On the landing tip, run `run.cmd smoke` (`run_menu.py smoke` from a shell). It carries `trace.py --strict`, `check_trajectory.py --strict`, the docs staleness and RESYNC entry checks, and the smoke tier. Also run P3's `test_adjudicate_brief` tests by name, since smoke skips them, and `gen_prompt_catalog.py --check`. Paste the real output. Generated views follow the coordinator's landing regeneration.

## Downstream effect

No forced migration. Adopters take the line on their next resync of the kit-owned files. The one visible change: a decomposition round's verdict is now asked for one more line kind, and a round with no hats now asks for something where it asked for nothing. No machine reads the line.

## Findings outside this row, not fixed here

- WI-998's sample depends on a round being scheduled after this landing, and its spec says none is. That is already listed for the owner there.
- `docs/test/inspection-procedures.md` reads "Record why further splitting stops", which can be read as the inspector's duty rather than a check of the sample's record. It is a TC-211 input, so any edit belongs to WI-998's amendment route, not here.
