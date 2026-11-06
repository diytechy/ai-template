# WI-993 plan: an owner-held step is an open item

Planned against lane `C:/Projects/ai-template.wt/wi-993`, head `2ebfb6951`. The planner is a fresh session that did not write the spec and will not build it.

Read in full: the spec `docs/work/active/wi-993/WI-993-owner-held-step-is-an-oi.md`, its specref `docs/specs/WI-993.md`, OI-126, OI-70, OI-119 and OI-117, and the closed owner row WI-981 as the hand precedent. Also read: SR-049, SR-148, SR-174, SR-178, SR-228, LLR-118, LLR-153, LLR-154, LLR-288, LLR-298, LLR-299, LLR-364, TC-123, TC-147, TC-301, TC-314, IF-054, IF-073, IF-074, IF-091, IF-224, IF-264, IF-287, Flow 4, and the code the spec names. `docs/status.md`, `docs/log.md` and session notes were not read.

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. Each step's result:

1. **Mode classes (A2).** None added. The work item and open item classes keep their states and transitions. `schedule._disposition` confirms the spec's claim: an `active` row goes through the same `hard_preds_satisfied` test as a `queued` one, so a claimed row citing a pending item already reads `blocked`.
2. **Value domains (A3, A6).** One value joins one domain, and three interface rows change their form, all in P1.
   - IF-073: citers of a pending item go from {queued} to {queued, claimed}. `data`, `notes`, and `version` to v2. IF-074 `data` follows.
   - IF-091 gains one reader, `unanchored_rows` (see decision 3).
   - IF-224 gains one requestor, `scripts/intake` (see decision 2). The spec's delta says the mint reads the dial across a seam it already holds. Read against the code, it does not; see decision 2.
3. **Output-on-input dependencies (A4).** Three new cells, recorded here as the skill allows when planning:

   | Output | Inputs today | Input added |
   |---|---|---|
   | Queue projection (`cards`, `uncited`, `held`), and through it the page, the status snapshot and the uncited-item error | queued rows, pending items | claimed rows |
   | The mint's drafts at a landing | merged range's routed cells, act ledger, snapshot copy, closes, dispositions | accepted verdicts in the range (IF-287); the hold per registry (IF-224); the copy of each ruled row (IF-091) |
   | The amendment row's `adjudicates` set | routed records less settled ones | less the rows the owner row carries |
   | Readiness, the claim, dispatch, the worker brief | unchanged | none (call 7) |

4. **Descent (A8).** No new requirement descends: no SR text moves, and LLR-153, LLR-299, LLR-118 and LLR-364 take the behaviour. No new component or sub-component: every touched module keeps its component, and no new module is added (see decision 6). No boundary is new: IF-224 and IF-091 are existing rows between modules already joined. Flow 6 stays; Flow 4's post-merge step gains the arm.

So the WI adds a value and new inputs, and P1, P3 and P5 carry them. No refactor is owed, so `beyond` does not apply.

## Build order

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The spine set, once, before any test or code: IF-073, IF-074, IF-091 and IF-224; LLR-299, LLR-118, LLR-153 and LLR-364; TC-314, TC-123 and TC-147 with their evidence cells; Flow 4 | D4; D5; SR-049; SR-148; SR-174; TC-123; TC-147; TC-314 | IF-073; IF-074; IF-091; IF-224 | |
| P2 | The tests alone, committed before the code, each under its evidence class | D4; D5; SR-049; TC-123; TC-147; TC-314 | IF-073; IF-074; IF-091; IF-224 | P1 |
| P3 | Deliverable 1, the claimed citer: the projection, its readers' wording, the IF-073 and IF-074 contract bodies, and the RESYNC entry's heading with this deliverable's part | D5; D8; SR-049; SR-148; TC-123; TC-314 | IF-073; IF-074 | P2 |
| P4 | Deliverable 2, the policy text: PROCESS.md's one statement and every site that points at it | D1; D2; D3; D6; D7; SR-049 | IF-073 | P3 |
| P5 | Deliverable 3, the mint arm: `intake.py`, `acceptance_record.unanchored_rows`, the recipe's hand step retired, the RESYNC entry completed, and the exact size stamp | D4; D8; SR-049; SR-174; TC-147 | IF-091; IF-224; IF-287 | P4 |
| P6 | The checkpoint: reconcile the set against settled code, one combined sitting, the in-lane acts, and the no-detector inspection | D7; SR-049; TC-123; TC-147; TC-314 | IF-073; IF-074; IF-091; IF-224 | P5 |

Excludes: D9 — the A+B review bar is what the coordinator runs on the built lane; no build step delivers it.
Excludes: TC-050; TC-141; TC-142 — they verify SR-049's stage derivation (LLR-050, LLR-147, LLR-148), which this row does not touch. A held row stays drifted exactly as it does today, so the derived stage and the pending-amendment count do not move.

P3, P4 and P5 are the spec's three deliverables, in its order, one commit each. P1 and P2 precede them because `coordinator-cycle` §3 Intent puts rows and tests before code. A review round's rework adds commits as usual, and the landing squashes.

## P1: the spine set

One Terra turn writes the whole set. Existing statuses stay. Requirement rows name no code and no provenance in `title`, `detail` or `rationale` (PROCESS.md §3); `module` and `code_symbol` carry the code.

- **IF-073.** `data`: queued or claimed work-item needs edges cite pending items. `notes`: a pending item has at least one queued or claimed citer; a queued citer is the item's placeholder; a claimed citer holds a step its Done-when names. `version` v2.
- **IF-074.** `data`: pending items a queued or claimed row cites, and uncited items.
- **IF-091.** `data` adds `unanchored_rows(root, head, ids, routed_cells) -> ({row id: registry}, refusal)`.
- **IF-224.** `requestors` adds `scripts/intake`.
- **LLR-299.** "no queued or claimed work item cites"; "a citer that is neither queued nor claimed does not count".
- **LLR-118.** The pending items and the integrity notice are worded for queued or claimed citers.
- **LLR-153.** A new trigger stating the spec's closed set: an accepted verdict in the merged range whose latest amendment ruling on a row is MEANING, blessed or not, on a rung the dial holds, with the row at the range's end differing from its approved-snapshot copy, yields one queued owner row per verdict and one pending open item naming the rows, the verdict and the act's command, the item cited in that row's needs, in the mint's one commit. Those rows leave the amendment row. Every other state writes nothing, and a row left over stays on the amendment row as any other record does. A row sat more than once reads at its latest accepted verdict in the range. A replay mints no second item. **Its closing sentence also changes:** "Trigger (a) excludes only records the merged range already settled" stops being true, so it adds "and the rows the owner row carries". `module` adds `acceptance_record.py`; `code_symbol` adds the new symbols.
- **LLR-364.** It opens "the trunk mint excludes only a record…", which the arm falsifies. It gains one clause setting the owner row's rows apart. The spec's Context does not list this row; see decision 4.
- **TC-314.** A claimed citer clears the error and is a card; a draft, deferred or closed citer does not. Evidence names P2's tests.
- **TC-123.** Its method's "queued work item" clauses move with LLR-118, and it gains the claimed citer's card and Blocked line. Evidence names P2's test.
- **TC-147.** Gains a clause for each state of the closed set, and `verifies` adds IF-224. Evidence adds `tests/test_intake_held_act.py`.
- **Flow 4.** The `Intake-->>Slot` line adds the owner row and pending item for a held row a sitting ruled MEANING (LLR-153). Flow 6 is not edited.

The rows sit on the LLR and test rungs, which the dial in `docs/process.toml` releases today. Read it again at the sitting. On that reading this lane has no owner-held step of its own, and no SN, SR or boundary row moves.

## P2: the tests

The behaviour column names the row that states it, as the coordinator directs. A test case states only what these rows state, so each row below must carry the clause P1 gives it.

Red tests take `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`; P3 and P5 remove their own marks. Characterization tests are unmarked and name their adequacy witness, the wrong code each would catch, in the docstring. Mint tests drive `intake.intake_after_merge` and `intake.py sweep`, never a new symbol, so the red reaches the test's assertion and no stub is needed.

In `tests/test_open_item_queue.py` and `tests/test_open_item_readiness.py` (smoke tier, four cases):

| Test | TC | Row stating it | Fails before the change on |
|---|---|---|---|
| `test_a_claimed_citer_counts_beside_a_queued_one` | TC-314 | LLR-299; IF-073 | an `active` citer is missing from `held` and `cards`, and its item reads `uncited` |
| `test_an_item_only_a_claimed_row_cites_is_no_error` | TC-314 | LLR-299; IF-073 | `check_trajectory` reports the uncited-item error |
| `test_a_claimed_citer_is_a_card_and_on_the_blocked_list` | TC-123; TC-314 | LLR-118; IF-074; LLR-299 | the page shows the integrity notice, not a card, and the Blocked list omits the row |
| `test_a_draft_or_deferred_citer_still_reads_uncited` | TC-314 | LLR-299 | characterization; witness: a filter widened to "any open row" |

In the new `tests/test_intake_held_act.py` (slow tier; real git and the real `copy_live`, as `tests/test_intake_settled.py` builds them; `Implements: TC-147`), all stated by LLR-153 unless noted:

| Test | Fails before the change on |
|---|---|
| `test_a_held_meaning_verdict_mints_one_owner_row_and_one_pending_item` (the item names the rows, verdict and command; the row's `needs` cites it; `specref` is the item's record; item, row and watermark are one commit) | no item and no owner row exist |
| `test_a_blessed_meaning_on_a_held_rung_mints_the_same` | as above |
| `test_a_held_row_leaves_the_amendment_row_beside_a_released_one` (also LLR-364) | both rows sit in the amendment row's `adjudicates` |
| `test_the_hold_is_read_per_registry_not_from_the_stage` (IF-224) | no owner row exists; afterwards it pins the wrong reader of decision 2 |
| `test_a_row_with_no_amendment_record_in_the_range_still_mints` (text amended earlier, verdict in the range, differs from copy; IF-091) | no owner row exists |
| `test_the_latest_accepted_verdict_decides_a_row_sat_twice` (MEANING then CLARITY: nothing; CLARITY then MEANING: one; accepted MEANING then a failed sitting: one) | the two minting cases have no owner row |
| `test_each_verdict_files_its_own_row_and_item` | no rows exist |
| `test_a_replay_mints_no_second_item` (sweep twice; again after the owner row closes to the archive) | the count is 0, not 1 |
| `test_a_non_toml_registry_refuses_and_the_merge_stands` | no refusal is returned |
| `test_a_minted_item_passes_the_strict_checks` (no uncited error, no dangling edge, no brief-lint warning) | no item exists to check |
| `test_the_same_ruling_on_a_row_equal_to_its_copy_mints_nothing` (IF-091) | characterization; witness: an arm that skips the copy comparison |
| `test_clarity_or_a_released_rung_mints_no_owner_row` | characterization; witness: an arm that ignores the ruling or the dial |
| `test_an_unaccepted_verdict_leaves_the_row_on_the_amendment_row` (no binding, pending, failed, invalid) | characterization; witness: an arm reading the verdict without `accepted_at` |

`tests/conftest.py` adds `test_intake_held_act` to `SLOW_MODULES` with its measured seconds in the comment.

The smoke tier collected 3391 of `max-tests = 3410` at this head (`pytest --collect-only -q -m smoke tests`). Four more fit, but `test_smoke_budget` bites inside the tier and two other lanes are open, so re-measure after each refresh.

## P3: the claimed citer

- `kitlib/spine.py`: `_held_rows` takes `queued` and `active` through one named constant. The `open_item_queue` docstring drops "claimed" from what surfaces nothing.
- `check_trajectory.py`: the `uncited_open_item_findings` message and docstring. `gen_open_items.py`: `_uncited_notice`, `_brief_card`'s "Holds" label, the header and the IF-074 contract body. `traj_status.py`: its wording at the snapshot and Blocked lines.
- `docs/requirements/open-items.toml` and `registries/open-items.template.toml`: the IF-073 contract body and "FILE EVERY OPEN ITEM WITH ITS PLACEHOLDER" admit a claimed citer. `tests/test_dogfood_sync.py` holds the structure.
- Tests pinning the old words change here: `test_open_item_queue.py:88` and `:123`, `test_open_item_readiness.py:203`.
- `check_trajectory.py` has an exact stamp of 1658 SLOC, so its message keeps its line count, or this row carries the re-stamp and reason. `gen_open_items.py`, `spine.py` and `traj_status.py` sit under the threshold.
- Regenerate `docs/open-items.html` and the status block through the recipes' attest step. `PROJECT_STATE.html` is never generated on a work branch.
- **RESYNC.** The heading goes in here, not with the last deliverable; see decision 1.

Adds no test beyond P2's; it removes the marks on the first three.

## P4: the policy text

**No new tests.** These are prose sites. A phrase-pinning test would fix wording and prove nothing a reviewer cannot read, so the evidence is the review, with this list as its checklist. A final search for "a decision only the owner", "only sanctioned stop", "only stop" and "queued work item" over `project-trajectory/`, the skill copies and `docs/handbacks/README.md` must return only sites this list keeps on purpose. Kit text cites no repo-local ruling id it does not already cite: a token mandated into an adopter's file must mean something in their repo.

| Clause | Site | Change |
|---|---|---|
| D1, D2, D3, D6 | `PROCESS.md` §5, "Open items" | The one home. An open item is anything keeping a row from building forward (the five kinds), filed as a pending row the held work item's `needs` cites in the same commit. A lane keeps its claim at a planned step, one its claim copy's Done-when names, only while the item is filed and cited on trunk; a re-scoping answer closes it partial. A held-rung approval is never such a step: the lane lands its text and the act is ruled on trunk, on `open-items.html`, and the mint files that item for a MEANING ruling; an approval on a released rung, or delegated to the adjudicator, stays in the lane. A routine push files no item. An act's item closes by the owner's ruling or a delegated decision. "Filed with the queued row citing it" widens to a queued or claimed row. Nothing reads an item to keep a claim: it is the coordinator's rule |
| D3 | `PROCESS.md` §4, "A held rung's approval is the owner's act" | One pointer to §5 |
| D1 | `coordinator-cycle/SKILL.md` §7, "Owner-held steps" step 3 | Points at §5 and stops restating it |
| D1 | `coordinator-cycle/SKILL.md` §5, "A decision only the owner can make…" | Points at §5 |
| D3, D6 | `coordinator-cycle/SKILL.md` §7 list | The held-rung and push bullets say the lane lands its text, and that a routine push files no item |
| D1 | `registries/open-items.template.toml` header and `docs/requirements/open-items.toml` header | "a work item that waits on a decision" points at §5. Ruling a claimed citer ticks the Done-when item naming the step, in the ruling commit, and adds no evidence (the spec's Trust section; it needs a home an author reads) |
| D1 | `project-trajectory/README.md:24`, `STATUS.template.md:10` | "per pending decision" follows |
| D2 | `docs/handbacks/README.md:11` | The partial close is the only stop, save a planned step under §5 |
| D2 | `skills/session-protocol/SKILL.md:74` and `:210` | As above. `:210`'s "only a stop the owner must act on closes partial" contradicts the ruling directly |
| D2 | `work/WI-000.template.md:47` and its identical copy `docs/work/queued/WI-000-example.md` | As above |
| D2 | `prompts/adjudicate-disposition.template.md:24` | As above: "a lane is never HELD" |
| D2 | `check_trajectory.py` `holdbyrename_findings` docstring; `PROCESS_OPTIONS.md:2008` | As above. A docstring moves no SLOC. The rename ban stands |
| D3 | `skills/spine-authoring/SKILL.md:111` and `references/in-lane.md`, "A MEANING change awaits the owner" | The lane lands the text; the act is ruled on trunk |

Examined and kept: `docs/work/README.md:27` (describes the edge, states no narrow rule); the `adjudicate-disposition` prompt's step 4 (the human-owed exit of a close, a different route); `gate-advance` (already points at process.md); `AGENTS.template.md` (states none of this, and has under 1% of its cap free, so it stays untouched); `docs/decisions/`, `docs/archive/` and ruled open items (history).

Each skill edit goes in `project-trajectory/skills/` and the same bytes in `.claude/skills/` and `.agents/skills/`.

`PROCESS.md` and `PROCESS_OPTIONS.md` are watched. Report the byte delta and re-stamp them in `byte-budget-guard/SKILL.md` in this row, along with that skill's own pinned baseline. D7 is delivered here as text: the rule is stated as a rule, and nothing is built.

## P5: the mint arm

- **`acceptance_record.py`:** `unanchored_rows(root, head, ids, routed_cells)` returns `{row id: registry}` for the ids whose live row is not settled against its copy at `head`. It reuses `_tier_of`, `_snapshot_copy_rows`, `_spine_rows_at` and `_row_settled`, so "differs from its copy" keeps LLR-364's one meaning. A missing row or copy reads as differing; an id in no tier is left out; a copy that cannot be read is the refusal. About +14 SLOC to about 949, under the threshold, so no stamp. The IF-091 contract body follows.
- **`intake.py`:**
  - `_latest_rulings(root, before, after)` walks `ksitting.branch_verdicts`, reads each through `accepted_at` at `after`, and keeps each row's last amendment ruling with its verdict.
  - `_held_act_drafts(root, before, after)` returns `(drafts, row ids, refusal)`. It keeps MEANING rows, asks `unanchored_rows`, keeps those `ac.human_approves_spine(root / "docs", registry)` holds, and groups by verdict.
  - `_held_act_brief` writes the four `OPEN_ITEM_CELLS`: the rows, the verdict, and options (a) take the act, `intake.py snapshot --approves <registry>=<record> --reattests <rows> --verdict <verdict>`, one `--approves` pair per registry, or (b) return the text. WI-981's list is the shape.
  - The draft: title `owner act: <rows> ruled MEANING on a held rung by <verdict>`, `kind = "ordinary"`, `workstream = "process"`, a `context`, and the `open_item` table. `_inject_open_item` supplies the `needs` edge and the `specref`.
  - `_amendment_drafts` gains one parameter, the ids to leave out, defaulted so its other callers stand. `_held_act_drafts` runs first in `intake_after_merge`; its refusal returns as the other arms' do, naming the sweep.
- **`agent_common.py`:** the IF-224 contract body names intake.
- **`recipes.md`:** "What the sweep mints after the act" drops the hand step and its `needs`-filing clause, and says the owner row and item arrive minted. Same bytes in the three copies.
- **`tests/test_module_size_ratchet.py`:** the exact `intake.py` stamp and its reason, in this row, because the ratchet is smoke tier and an unstamped commit is red. See decision 6.
- **`RESYNC_PACK.md`:** the entry completes. One entry, covering the wider definition, the claim rule, the held-rung rule, and the mint arm with its non-TOML refusal. Adopters' owner-held rows gain pending items at their next re-sync. No file migrates mechanically.

Adds no test beyond P2's; it removes the remaining marks.

## P6: the checkpoint

Reconcile the set against the settled code: `code_symbol` and evidence cells, and the stamps. Then one combined sitting over LLR-118, LLR-153, LLR-299, LLR-364, TC-123, TC-147 and TC-314, parents first, with its acts in the lane. Interface rows carry no approval and owe no sitting.

The D7 inspection, recorded in the lane's decisions record: the lane's diff leaves `schedule.py`, `integrate.py`, `dispatch.py` and `agent_brief.py` unchanged, and no added line reads an open item or a `needs` edge to keep, drop or release a claim.

## Decisions the spec leaves, or where the code differs from it

The critic should check these first.

1. **The RESYNC entry cannot wait for the last deliverable.** The spec says it is "written with the last of them". `scripts/check_resync.py` compares the trunk base to the working tree and runs in the smoke bar, so P3's commit, the first to touch `project-trajectory/`, is red without an added entry. Its `### Reserved:` heading does not count, and the pack's shape tests hold it at zero. So the heading and P3's part land in P3, and P5 completes the text; an edit adds no second heading, so it stays one entry and D8 holds. The anchor is the trunk base, so a refresh that moves the base re-anchors it. P1 and P2 touch nothing shipped.
2. **The hold is read through IF-224, not `adjudication_action`.** The spec's delta names `intake.adjudication_action` as the seam. That function takes a bool and reads nothing, and `flip_verified`'s `ac.human_holds(docs, ac.spine_stage_of(root))` asks about the repo's current stage, not the row's rung, so it answers wrongly for an SN row at a later stage. `human_approves_spine` is the per-registry reader, its docstring says anything telling a session which rows it may approve must filter through it, and intake reaches it through `ac`, so no import changes. `held_status.registry_held` is the alternative, but it would add intake to IF-196 and read the dial by another path. Cost: one requestor on an existing row. Not a new boundary.
3. **`unanchored_rows` is a new reader, because the spec's table needs one.** The table's first row turns on the copy, not on an amendment record, and a verdict can land for a row whose text moved in an earlier range. The filtered amendment records would miss that row. `baseline_snapshot.is_drifted` is not it either: it omits routed traced cells, and `settled_amendments` already defined this comparison.
4. **Three records join the spec's list.** LLR-364 and LLR-153's closing sentence both say "excludes only", which the arm falsifies. TC-147 and TC-123 must change because a test case states only what its rows state, and LLR-153 and LLR-118 gain behaviour. All are in the same sitting.
5. **One owner row and item per verdict, not per row or per landing.** The spec's Trust section builds the title "from the verdict and its rows", and the act names one verdict. One sitting gives one item. A row re-sat in a later landing before the owner acts gets a second item naming the later verdict; the owner's ruling settles both.
6. **The arm stays in `intake.py`, with a reviewed size bump, not in a new module.** `intake.py` sits exactly at its 1890 stamp, and the ratchet's first answer is decomposition. `rejudge.checkpoint_drafts` is a precedent for a sibling draft producer. For about +50 SLOC, a sibling adds an interface row, a citing TC and an import-layer entry, against a delta two critiques confirmed as no new boundary. Earlier arms took this route (+42, +39, +35), and moving the comparison to `acceptance_record` already keeps the bump small. If the arm passes +70 SLOC, the builder stops and reports, and the cut moves to a sibling in `rejudge`'s shape.
7. **"Latest" is `branch_verdicts`' path order.** Sittings number `NNN-` within a lane, so path order is sitting order there. The merge slot's arm always reads one lane's range. Only a hand sweep across lanes could order a row's two lanes by name, and that needs one row sat in two lanes in one range. That is left outside the bound (PROCESS.md §6) and is not built against.
8. **A row edited after its verdict.** The table has no identity column, and the spec's first row applies whenever the row differs from its copy. The arm adds no check: the item names the verdict, and the owner reads the live text. A held MEANING act is not bound to a digest today, and this row changes no such rule.
9. **The minted row carries no Done-when.** That is the placeholder shape TC-314 already passes. The ruling commit writes the Done-when or closes the row, as IF-073 requires, and the item's options say so.
10. **The dial is read at the working tree,** as `flip_verified` reads it. A sweep at an old `--after` reads today's dial; an unreadable dial reads held. That errs toward the owner.

## Downstream

No migration is forced. A CSV open-items adopter gets a named refusal at a landing that owes an item, then files by hand and sweeps, as `_mint_open_item` already does for a disposition. An adopter with `human_approval_through` at the shipped default holds every tier, so the arm reaches every MEANING ruling there.
