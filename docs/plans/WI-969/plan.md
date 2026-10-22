# WI-969 plan: the close validates an adoption once and records it; the commit check judges the record and admits the close's exact relinks; the sweep trusts it

## Revision 3 of WI-902's plan, on the owner's route: what changed, and why

WI-969 supersedes WI-902 and carries WI-902's spec of record byte for byte
(its spec's "Spec of record, carried"; wi-969 D-001; Done-when sitting
`docs/reviews/wi-969/001-ADJUDICATE-b67768d.md` blessed the 23 items). This
plan starts from WI-902's committed plan (`docs/plans/WI-902/plan.md`,
revision 2) and changes what dispute sitting 016
(`docs/reviews/wi-902/016-ADJUDICATE-7ffa12c.md`, F1 FIX) requires, on the
owner's route (`docs/decisions/coordinator-2026-10-20.toml` D-008). The
plan's own records are this row's: `docs/plans/WI-969/` and
`docs/decisions/wi-969.toml`.

Planner: fresh session, 2026-10-21. Read in full: the WI-969 spec, its
specref (`docs/work/partial/WI-902-disposition-adopts-existing-successor.md`),
WI-902's plan and both critiques, sitting 016, D-008, the lane record
(`docs/plans/2026-10-11-review-churn/wi-902-lane-record.md`, parts (a) and
(b)), `docs/decisions/wi-902.toml` (trunk's D-011) and
`docs/decisions/wi-969.toml` (D-001). The critiques' findings were judged as
claims: critique 1's F1 was already answered by revision 2 (the order
iterate, checkpoint, land), and that order is kept. Critique 2's F1 was
confirmed by sitting 016 on the code, and I confirmed it again at this tree
(below).

### The ruling's change (sitting 016, F1 FIX)

**Confirmed at this tree.** `kitlib/verdict._closed_wi_ids` returns None for
any changed path outside `docs/work/`, and `mechanical_close_attestation`
reads its result. `handback._archive_one_adjudication_row` closes through
`spec_move.move_spec`, whose `_relink_inbound_links` rewrites and stages
every inbound markdown link over the whole repository (`_markdown_files`).
So a genuine `close_adjudication` whose row is linked from, say,
`docs/reviews/...` writes a path outside `docs/work/` and is not peeled.
Revision 2's P5 read "the machinery's close" off the attestor, so it would
refuse that close at the slot and the hook, with no route back.

**What changes (all in P7, the commit check; one function in
`kitlib/verdict.py`):**
- Record admission gets its own close test. The close-shape reading moves
  out of `_closed_wi_ids` into one shared reader in `kitlib/verdict.py`
  that takes an optional relink oracle. Without an oracle it is the peel's
  reading, unchanged: any path outside `docs/work/` refuses. With the oracle
  (the commit check passes `spec_move.exact_relink`, the shared byte-exact
  reading that `plan_gate.build_paths`, `integrate._relinked_exactly` and,
  injected, `kitlib.done_when.staged_hold` already use), a path outside
  `docs/work/` is admitted only when it is an `M` entry whose new bytes are
  exactly the inbound relink of the commit's own paired moves.
  `kitlib/verdict.py` imports no script; the oracle is injected, as
  `done_when.staged_hold` takes it.
- Unchanged, as the ruling binds: the record/request compare, the
  parent-tree validation, the close-shape validation (one parent, one source
  branch, paired moves from `active/<branch>/` into `complete/`, nothing
  else created or destroyed, the composed subject) and the peel itself
  (`mechanical_close_attestation` calls the reader with no oracle, so it
  still refuses that close and the gate still asks for one more review).
- Revision 2's P5 paragraph "A residual stated, not built against" is
  removed, and so is its matching risk ("The peel/check agreement").
- The real-close regression is added (P7's tests): a real
  `close_adjudication` with an inbound link from outside `docs/work/`
  passes the lane rider and the squash hook, while a hand-written record
  beside the same relink is still refused.
- The architectural answer gains one interface edit: IF-175's Contract
  (`kitlib/verdict.py`) names the shared reader, and its requestors gain
  `scripts/adoption_record`. P1 authors it and P7 builds it.

### Changes beyond the ruling, each with its reason

1. **Intent before the build, and the tests committed alone first** (new
   P1 and P2; revision 2's P8 moves up). The coordinator-cycle skill §3
   "Intent" now orders Terra's whole change set before build round 1 (for a
   `single` row, after its pass record) and makes build round 1's first
   deliverable the tests, committed alone, each under one evidence class
   (WI-955, landed after revision 2 was written). A lane claimed before that
   order keeps its old order; WI-969 was claimed after it, so D18 ("the shape
   the skill carries") requires the new order. Revision 2's P8 ("authored
   once after the first build round") would contradict the skill.
2. **The attested bar before each review** (P11, step 1, and the red cap).
   Skill §3 "Iterate" step 1 now requires the tip to carry the review bar's
   attestation (`integrate.py attest --tests ...`; WI-956, WI-957), and
   `review_brief.py review` refuses any other tip. "The red cap" counts a red
   attest as a red round, and at `[build] red_rounds_max` consecutive reds
   the lane closes partial (WI-958).
3. **The ported decisions go to this row's record.** Revision 2's P0 copied
   the old lane's `docs/decisions/wi-902.toml` over the re-cut lane's. Trunk
   now holds WI-902's record with D-011 (the partial close), and WI-902 is
   closed. So the old D-001 to D-010 fates are recorded in
   `docs/decisions/wi-969.toml`, each citing the entry at `d3d301216`, and
   WI-902's trunk record is not edited.
4. **The lane's first counted review** is the next sequence number in
   `docs/reviews/wi-969/` (002 today, after sitting 001), not "review 016",
   which is WI-902's sitting on trunk.
5. **Numbering.** The table is renumbered for the new order. Old to new:
   P0 to P0; P8 to P1; (new) P2; P1 to P3; P2 to P4; P3 to P5; P4 to P6;
   P5 to P7; P6 to P8; P7 to P9; P9 to P10; P10 to P11; P11 to P12; P12 to
   P13.
6. **Smoke wording.** The bar reports the smoke tier's seconds; the audit
   judges them against `docs/stack.ini` `[smoke-budget]`. "Within 60 s"
   becomes "within its budget", as D23 says.
7. **New ids.** The watermark now stands at LLR 344, TC 382 and IF 302, so
   the commit check's rows take LLR-345 and TC-383 (or the floor the
   coordinator briefs), and its two interface rows IF-303 and IF-304.

Nothing else in revision 2 is changed in substance.

### Citations re-checked at this tree (lane tip `e077a9cc8`)

Present and as revision 2 read them:
- `intake.py`: `parse_dispositions`, `_TOML_FENCE_RE`, `_DRAFT_KEYS`,
  `owes_successor`, `_close_drafts`, `_successor_drafts`,
  `_disposition_drafts`, `_draft_refusal`, `_apply_supersedes`,
  `_supersede_source_refusal`, `_mint`, `_write_mint`, `_mint_message`,
  `intake_after_merge`. `_merged_dispositions`, `_standing_successors`,
  `_title_identity_refusal` and `_repoint_owed` are lane functions (at
  `d3d301216`), not on trunk: P4 and P8 port them.
- `handback.py`: `_loop_commit`, `_ADJUDICATION_CLOSE_DELIVERABLE`,
  `_adjudication_close_text(text, deliverable)`, `_consolidation_close`,
  `_archive_one_adjudication_row`, `close_adjudication`.
- `text_then_act.py`: `TEXT_THEN_ACT_REMEDY`, `commit_text_then_act_lines`,
  `LANE_COMMIT_RIDERS = (commit_text_then_act_lines,)`, `lane_commit_walk`,
  `_squash_lines`, `staged_text_then_act_lines`.
- `integrate.py`: `_text_then_act_refusal` (appends `TEXT_THEN_ACT_REMEDY`
  to every rider line), `_each_lane_commit`, `_verdict_owed`,
  `_relinked_exactly` (an `exact_relink` caller).
- `check.py`: the step table (`text-then-act`, `plan-gate`) and
  `_text_then_act_refusal`; `hooks/pre-commit`'s `--run-steps` list ends
  `...,text-then-act,done-when-blessed,plan-gate`.
- `plan_gate.py`: `_close_homes`, `build_paths` (the precedent for
  admitting a close's exact relinks), `lane_rider`, `landing_refusal`,
  `_squash_lines`.
- `spec_move.py`: `_relink_inbound_links`, `_markdown_files`,
  `expected_relink`, `exact_relink(old, new, rel, remap)`, `move_spec`.
- `kitlib/verdict.py`: `_closed_wi_ids`, `mechanical_close_attestation`
  (Contract IF-175 in the module header); `kitlib/station.py`:
  `mechanical_close_order`, `mechanical_close_subject` (revision 2 wrote
  `station.`; the module is `kitlib/station.py`).
- `acceptance_record._commit_parents(root, rev, question, first=False)`.
- `kitlib/registry.py`: `WI_COLUMNS`, `SPEC_SCALARS`, `SPEC_LISTS`
  (`("Adjudicates", "adjudicates")`), `parse_spec_row`; the column lists in
  `wi_convert.py` and `plan_artifacts.py`.
- `consolidate._section_blocks`, `consolidate._enacted_supersedes`;
  `agent_loop.dispositions_drafted`; `agent_policy.adjudication_review_owed`;
  `kitlib/bootstrap_manifest.MAPPING`.
- Recipes: §8's "Until WI-902 lands, close the row by hand" paragraph and
  §3's "(WI-902, act 117)" are both present.
- Tests: `test_handback`, `test_intake`, `test_consolidate_close`,
  `test_verdict_record`, `test_text_then_act`, `test_wi_convert`,
  `test_plan_gate` and `test_ruling_sync` exist; the first six are in
  `SLOW_MODULES`; `hooks_on` is in `tests/conftest.py`;
  `test_an_unreadable_claim_is_never_closed_early` (TC-331) and the four
  empty-section refusal tests (`test_a_disposition_row_with_no_successor_is_refused`,
  `test_a_cancelled_close_with_no_successor_is_refused_at_merge`,
  `test_the_refusal_invariant_stops_a_disposition_with_no_successor`,
  `test_the_refusal_invariant_stops_a_cancelled_close_with_no_successor`)
  exist. `kitlib/adoption.py`, `adoption_record.py`,
  `tests/test_disposition_adoption.py` and `tests/test_adoption_record.py`
  do not exist yet; this plan adds them.
- The D12 census probe: 66 tracked files under `docs/work/`,
  `docs/archive/work/` and `docs/reviews/` carry a `## Dispositions`
  section today.
- The old lane's record at `d3d301216` (on `archive/lanes`): reviews 001 to
  015 and adjudications 004/006/007/009/011/013 with their `.requested` and
  three `DISPUTE-findings.toml` files are absent from trunk; six of its
  `docs/iteration/call_*-20261011-*.log` files are absent from trunk.

**Rows of record:**
- the item's SRs, SR-148 and SR-220, in
  `docs/requirements/system-requirements.toml`;
- the TCs that verify them, in `docs/test/test-cases.toml` (re-read; the
  same set as revision 2): TC-058, TC-059, TC-060, TC-091, TC-097, TC-143,
  TC-146, TC-154, TC-183, TC-208, TC-254, TC-260, TC-313, TC-314 and TC-331.
  A row names each, or an `Excludes:` line gives the reason. TC-147
  (SR-174, SR-228, LLR-153) and TC-156 (SR-144, LLR-161) do not verify
  either SR today, but the Done-when re-sits them, so rows name them;
  TC-173 (LLR-302, the shared walk) is named as a regression;
- LLR-153, LLR-161, LLR-181, LLR-298, LLR-302, LLR-312 and LLR-337, in
  `docs/requirements/low-level-requirements.toml`;
- in `docs/requirements/interfaces.toml`: IF-040, IF-047, IF-078, IF-079,
  IF-090, IF-092, IF-102, IF-123, IF-134, IF-137, IF-159, IF-161, IF-173,
  IF-175, IF-186, IF-244 and IF-295 (plan_gate's exit-code row, the
  precedent for the new one). `spec_move` owns no interface row today; the
  check calls `exact_relink` as `plan_gate` and `integrate` already do;
- CMP-006, CMP-007 and CMP-008, in `docs/requirements/components.toml`;
- `docs/runtime-flows.md`, Flow 4.

**Runtime flows: no edit.** Flow 4 draws the merge slot and its post-merge
intake arm, but none of the close, the per-commit rungs or the hook steps.
This row changes only those, so Flow 4 stays true as drawn.

**Ids not yet in the registries.** LLR-335, TC-360 and IF-294 have no row on
trunk (D-011 of the old lane keeps their ids). The coverage gate validates
cited ids against the lane's registries, so this plan names them in prose
and titles only, never in a `Covers` or `Interfaces` cell; likewise the
commit check's new ids.

## Architectural delta

The row does three of the four things.

**It adds a value to a domain.**
- The work-item row gains a declared `Adopted` column (front-matter key
  `adopted`), beside `Adjudicates` and `Digests` (D-012 of 2026-10-14).
- The `## Dispositions` grammar gains a second block shape, the adoption
  block `adopts = "WI-NNN"`.
- The section grammar tightens: fences must pair.

**Outputs depend on a new input.**
- The close's output, the closed spec, now carries the record, and the
  record depends on the request and on the lane HEAD's registry.
- The sweep's re-point now depends on the record.
- A per-commit verdict depends on the record and the request, at the commit
  and at its parent, and, for the close, on whether each path outside
  `docs/work/` is exactly the close's relink.

**It crosses no new system boundary.**
- The commit check reads git trees, as `text_then_act` and `plan_gate`
  already do; the relink reading is `spec_move`'s existing shared one.
- The close already runs git in the lane worktree.
- The old lane's git-history read (`rev-list --first-parent`, the shallow
  boundary test) is not ported, so one input is removed.

**It adds internal seams, and the plan's rows carry them.**
- The new module `scripts/adoption_record.py` (P6, P7): the tree reader at
  a revision, validation at a revision, the per-commit rule and its staged
  form.
- `kitlib/adoption.py` (P3, P5): pure; the request grammar, the disposed-id
  reader, the validation rule, the record's strict reader and the
  record-change judgement.
- `kitlib/verdict.py` (P7): the close-shape reading becomes one shared
  reader with an optional injected relink oracle; the peel calls it without
  one. IF-175's Contract and requestors are amended.
- Two interface rows for `adoption_record.py`: a call row to `handback` and
  `text_then_act`, and an exit-code row to `scripts/check`, mirroring
  IF-295. IF-294 is re-added with its Contract rebuilt. All are authored at
  intent (P1) and stated finally at the checkpoint (P12).

There is no state machine to extend. The record is data on a terminal row,
written once.

DELTA: within

## Steps, in build order

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | Port the old lane's record into this lane: WI-902's reviews 001 to 015, adjudications 004/006/007/009/011/013 with their request and dispute files into `docs/reviews/wi-902/`, and the six missing adjudicator call logs, from `d3d301216`; record in `docs/decisions/wi-969.toml` each old decision's fate (kept, re-made or withdrawn, per the lane record's part (b)) and the decisions the rebuild owes (round count from zero at this lane's next review; the reviewer shape the coordinator-cycle skill carries; acts 113 to 117 not ported; the TC-first order) | D17; D18; SR-148 | IF-047 (the review verdict files are ported byte for byte; no seam change) | |
| P1 | The spine at intent, after the pass record and before build round 1 (skill §3 Intent): SR-148's acceptance re-stated; LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254 amended per this plan; LLR-335 and TC-360 re-added Drafted in record-at-close text; the commit check's LLR and TC minted Drafted, its relink admission stated; IF-294 re-added as rebuilt, the two adoption-record interface rows minted, IF-175 amended for the shared close-shape reader; new rows Drafted, existing statuses unchanged; verified and committed without a sitting | D13; D14; D15; D16; SR-148; SR-220; TC-147; TC-156; TC-254 | IF-102; IF-161; IF-175 | P0 |
| P2 | Build round 1's first deliverable: every new test P3 to P8 name, committed alone before any code, new behaviour as strict expected assertion failures reaching their own assertions (stubs where a module is absent), characterizations unmarked with their adequacy witness, the census with its planted live-instrument case | D3; D11; D12; SR-148; SR-220; TC-147; TC-156; TC-254; TC-313 | no interface (test modules only; stubs carry no contract until P3 to P8 build them) | P1 |
| P3 | One complete-section parser with fence pairing, and the pure adoption module ported from `d3d301216` (block parser, disposed-id reader, validation rule over a supplied listing; `work_specs` not ported), its bootstrap MAPPING row | D3; D11; D12; D20; D1; SR-148 | IF-090; Proposed: the pure kitlib adoption call seam, re-added under the lane record's kept id; nearest existing IF-090 (intake's call surface) falls short because the new owner is a kitlib module shared by the close, the sweep and the commit check, not intake | P2 |
| P4 | The mint's lineage corrections (deliverable 10, the old lane's D-003 and D-004), ported: a replay keeps an already-minted draft in the successor set, and a title match on another lineage refuses before any write | D3; D10; D22; SR-148; TC-147 | IF-244; IF-186; IF-090 | P2 |
| P5 | The record's cell: the declared `Adopted` column in the registry reader, the converter and the plan-artifact column list, documented in the WI-000 template; its one strict reader and the pure record-change judgement in the adoption module | D3; D1; SR-148 | IF-092; IF-078; IF-079; IF-159 | P3 |
| P6 | The close validates once, in the lane HEAD's tree, and writes the record in the rewrite that clears `specref`; the consolidation arm refuses an adoption before its first write; the new `adoption_record.py` holds the tree reader and validation at a revision | D1; D2; D3; D4; D11; SR-148; SR-220; TC-254; TC-156; TC-331 | IF-137; IF-173; Proposed: the adoption-record module's call seam (validation at a revision for handback, the per-commit rule for text_then_act); nearest existing IF-175 (kitlib/verdict's record readers) falls short because it reads verdict records and owns no git tree reads of work specs | P3; P5 |
| P7 | The commit check: one rule judging a commit against its parents, with its own close test (the shared close-shape reader in `kitlib/verdict.py` with `spec_move.exact_relink` injected, so the close's exact inbound relinks outside `docs/work/` are admitted while record/request, parent-tree and close-shape validation stay and the peel calls the reader without the oracle); riding `LANE_COMMIT_RIDERS` at the merge slot, and a staged form run by the pre-commit hook's new `adoption-record` step with its own squash-landing walk; the record never borrows text-then-act's remedy; the peel's stated premise names the record; the real-close regression | D3; D5; D6; D7; D8; D9; D1; SR-148; TC-313; TC-173 | IF-040; IF-134; IF-175; IF-173; Proposed: the adoption-record exit-code seam to scripts/check, the same shape as IF-295 (plan_gate), which falls short only because its owner is plan_gate | P6 |
| P8 | The sweep trusts the record: it compares the request with the record, re-points from the record beside the drafts, and refuses an unreadable merged spec; none of the old lane's history readers is ported | D1; D2; D3; D10; D11; D21; SR-148; TC-147 | IF-244; IF-090 | P4; P5; P6 |
| P9 | The consumer text: the disposition prompt teaches the adoption form and the lane-tree rule, and the prompt catalog is regenerated; recipes §8 says an adopting disposition closes through `handback.close_adjudication` and lands inside the squash, and §3's citation of act 117 is replaced; the skill copies are synced | D1; D2; SR-148 | no interface (prompt and skill prose; the catalog and the skill copies are regenerated by their own steps) | P6; P8 |
| P10 | The RESYNC_PACK.md entry: one entry anchored at the trunk commit the lane is based on, naming the three tightenings, the kit-owned files and no forced migration | D19; D20; D21; D22; SR-148 | IF-244; IF-134 (adopter-facing prose naming the sweep's new refusals and the hook's new step) | P7; P8; P9 |
| P11 | Iterate, before any sitting: each round's tip attested through `integrate.py attest` with the round's tests (a red attest is a red round, and `[build] red_rounds_max` reds close the lane partial), the lints, then the counted full review rounds in the skill's shape from this lane's next review (count from zero, at most three, the third in convergence stance after its convergence map), each with its coverage plan, threat-model triage and dispute sittings, until one round has no BLOCKER or MAJOR; code and trace fields only, row-text proposals to the spine change list | D18; D23; SR-148; SR-220; TC-147; TC-156; TC-254; TC-313; TC-173; TC-331 | no seam crossed beyond P3 to P9's (fix rounds stay inside the rows' declared interfaces; a fix that needs a new one stops the round, skill §3 Iterate step 8) | P10 |
| P12 | The checkpoint, after the settled rounds, then the gate: Terra reconciles P1's intent set and the spine change list against P11's settled code; the closure check and both strict lints; one combined sitting (SR-148 and the six re-sat rows, first approval of LLR-335, TC-360 and the check's rows, the interface rows stated); returns routed and re-sat; the trunk-only views restored; then the uncounted gate in convergence stance over the checkpoint tip | D13; D14; D15; D16; D18; SR-148; SR-220; TC-147; TC-156; TC-254 | IF-123 | P11 |
| P13 | Land, after the gate: rebase onto trunk and re-anchor the RESYNC entry; a repeat checkpoint and an uncounted convergence round only if the rebase changed code or authored rows; the unchanged-rows check; the act turn above trunk's ledger top; the five old act commits proven absent; the full suite once; the squash landing (whose own hook runs the new step); the bar again on the landing tip | D17; D19; D23; SR-148; SR-220; TC-147; TC-156; TC-254; TC-313; TC-173; TC-331 | IF-123; IF-134 (the landing commit meets the hook) | P12 |

Excludes: TC-058; TC-059; TC-060; TC-091; TC-097; TC-143; TC-146; TC-154; TC-183 — they verify SR-148's work-selection order (the frontier and its ordering, the safety classifier, the generated status surface, the structural safety cross-check, the dual-plan class, the admission table, the adjudication kind's rank slot, admission order with the red-TC census, the gap census); none of that code (`schedule`, `dispatch` admission, `census`, the status generators) changes here, and SR-148's amended acceptance adds only a third way an unresolved handback is resolved, which TC-147 and TC-360 carry. The full suite at P13 still runs them.

Excludes: TC-314 — pending open-item citation integrity (LLR-299) reads `needs` tokens that cite open items; the adoption carries none, and the re-point P4 and P8 extend rewrites only work-item edges, which TC-147 covers.

Excludes: TC-208; TC-260 — the consolidation census and its command (LLR-210, LLR-264) read only `consolidate._enacted_supersedes`, which this row leaves unchanged because an adoption carries no `supersedes`. P3's `test_an_adoption_never_counts_as_an_absorption` pins that. The one consolidation behaviour this row adds, the close refusing an adoption, is TC-254's.

### Clauses covered by more than one row

Each row does a separate part.

- **D1:** the parser (P3), the cell (P5), the close (P6), the commit check's
  admission of the real close (P7), the sweep (P8) and the prompt (P9).
- **D2:** the close's discharge rule (P6), the sweep's OI-73 guard (P8) and
  the prompt's wording (P9). See "D2" under P9.
- **D3:** the tests committed first (P2), and every row that turns its own
  tests green (P3 to P8).
- **D10:** the mint's replay correction (P4) and the sweep's recorded
  re-point (P8).
- **D11:** the tests (P2), the parser (P3), the close (P6) and the sweep
  (P8).
- **D12:** the census written (P2) and passing over the tightened parser
  (P3).
- **D13 to D16:** the rows authored at intent (P1), and reconciled and sat
  at the checkpoint (P12).
- **D17:** the decision recorded at the port (P0), and the ancestry proof
  at the act and again on the landing tip (P13).
- **D18:** the lane decision (P0), the counted rounds run in that shape
  (P11), and the gate in that shape (P12).
- **D19:** the entry written (P10), and re-anchored after the rebase (P13).
- **D20, D21 and D22:** built in P3, P8 and P4, and named in P10.
- **D23:** the bar on the lane tip at every round (P11), and on the landing
  tip (P13).
- **The order:** intent (P1), tests (P2), code (P3 to P10), iterate (P11),
  checkpoint and gate (P12), land (P13); each row's predecessors are earlier
  rows.

### Every commit meets the smoke bar

Every row ends at the per-commit bar (`run.cmd smoke`, `run_menu.py smoke`).
A red tier fails it; its seconds are reported against `[smoke-budget]`.

- A row that grows a ratcheted module re-stamps it in its own commit, in
  `tests/test_module_size_ratchet.py` or `docs/complexity-baseline`, with a
  reason line.
- Git-repo tests go in modules listed in `tests/conftest.py`
  `SLOW_MODULES`: `test_handback`, `test_intake`, `test_consolidate_close`,
  `test_verdict_record`, `test_text_then_act`, `test_wi_convert`, and the
  new `test_adoption_record`, which P2 adds to the set.
- Each family keeps an in-process pin in the smoke module
  `tests/test_disposition_adoption.py`.

## P0: port the lane's record (D17, D18)

**What is ported, unchanged** (lane record, "Mechanics"), each with
`git show d3d301216:<path>` and committed alone, as record:
- `docs/reviews/wi-902/` 001 to 015 (beside trunk's 016);
- the six adjudications 004, 006, 007, 009, 011 and 013, each with its
  `.requested` file;
- the three `NNN-DISPUTE-findings.toml` files (004, 009, 011);
- the six `docs/iteration/call_*-20261011-*.log` files trunk lacks
  (`call_06c6bded…`, `call_1c043b6d…`, `call_8c9ed99b…`, `call_9f339b31…`,
  `call_e5c7c70d…`, `call_f003a9cb…`).

**The old decisions' fates, in `docs/decisions/wi-969.toml`** (changed from
revision 2: WI-902's trunk record holds D-011 and is not edited). One entry
per survivor, each citing `d3d301216:docs/decisions/wi-902.toml#D-00N` and
the lane record's part (b), open for the owner to confirm or overrule:
- D-002 re-made (P12 finalises the stamp at the reconciliation);
- D-003 and D-004 kept;
- D-005 re-made (P1 retags);
- D-006 F2 kept; D-007 F2 kept and moved to the close;
- D-008 kept, amended in P1;
- D-010 kept, folded into P3.

One entry records the withdrawn, with nothing to confirm: D-001; D-006 F1
(ruling 2 supersedes ruling 009's mechanism); D-007 F1; D-009, with act 117.

**The new decisions:**
- **D18.** A lane in flight when the review shape landed "starts its count
  at zero at its next review, recorded as a decision". The count starts at
  zero at this lane's next review (`docs/reviews/wi-969/`, 002 today). The
  entry names the reviewers and the model behind each REVIEW file by the
  skill's current roles.
- **D17.** Acts 113 to 117 (`a2a95f847`, `7c4544ef3`, `acab09035`,
  `a588ae83f` and `97ea2e47d`) are not ported, and no seq between 113 and
  117 is taken by this lane.
- **The order.** The lane follows the skill's current Intent order (P1
  before build, P2's tests alone first), since it was claimed after that
  order landed.

**Not ported:** the act commits; their `docs/archive/last_approved/`
copies, `acts.toml` rows and README lines; the old lane's spec edit (the
carried spec governs); its `docs/id-watermark` and
`docs/complexity-baseline` edits (regenerated where the rebuild needs them).

**No test.** This is record, not behaviour. D17's proof is P13's ancestry
check.

## P1: the spine at intent (D13 to D16)

This is coordinator-cycle skill §3, "Intent", run after the pass record and
before build round 1 (moved from revision 2's P8; see "Changes beyond the
ruling", 1). Terra authors the whole change set once, from SR-148 down, with
the arms map, from this plan. New rows are `Drafted`; existing statuses are
unchanged; interface rows carry no status. The coordinator verifies,
regenerates and commits it through `integrate.py attest`, with no sitting.
These rows give the builder the tests to write and the P11 reviewers the
obligations. They are reconciled against settled code and sat only at P12.

**Rows to be re-sat at P12, with text expected to stand:**
- **SR-148.** The acceptance gains "or names an already-open item that
  supersedes it as its successor".
- **LLR-153 and TC-147.** The mint's arms: an adopts-only block allocates
  no id, title identity and lineage are resolved together, and replays use
  the full successor set. Both gain SR-148. TC-147's Evidence names P4's
  and P8's tests.
- **LLR-161 and TC-156:** "drafts a successor, or adopts an already-filed
  one".
- **LLR-312 and TC-254:** a consolidation verdict that adopts refuses
  before its first write. TC-254's Evidence gains P6's consolidation test.

**LLR-335, re-added Drafted.** Record-at-close, contract voice, no function
named in its detail (ruling 5); its `module` and `code_symbol` cells stay
filled until plan item 5's schema lane. It states the request grammar; the
disposed row read from the title's one event token; the open-state and
`supersedes` rule; validation once, in the tree the closing commit is made
on, with the record written in that commit; the sweep trusting the record
and refusing the four bad pairs, a malformed record and an unreadable merged
spec; fence pairing; the narrowed no-cell-change clause (D-006 F2). The
landing-tree, shallow-boundary and replay clauses are gone.

**TC-360, re-added Drafted.** Verifies SR-148, LLR-335 and the re-added
seam row. Its Evidence names P3's, P5's, P6's and P8's tests.

**The commit check's LLR and TC under SR-148** (LLR-345 and TC-383 at
today's watermark, or the floor the coordinator briefs). The LLR has
LLR-298's per-commit shape and states:
- the close's own commit, recognised by its own close test: one parent,
  paired moves out of one `active/<branch>/` into `complete/`, nothing
  else created or destroyed, the composed subject, and each changed path
  outside `docs/work/` exactly the inbound relink those moves write (the
  shared byte-exact relink reading); its record equal to the request and
  every adopted id valid in the parent's tree;
- a carried record, and a merge's neither-parent rule;
- refusal of every other record change, and of a requesting spec moved into
  `complete/` without a record;
- a parent that cannot be read, reported by name;
- the slot walk and the staged step with its squash handling.

The TC names P7's tests, the real-close regression among them. Tier:
`Full`. Its smoke pins are P5's `test_the_record_change_table` and P7's
`test_the_close_shape_admits_outside_paths_only_through_the_oracle`.

**Interface rows** (no approval status):
- **IF-294, re-added** (D-008 kept, amended): owner
  `scripts/kitlib/adoption`; requestors `scripts/intake`,
  `scripts/handback` and `scripts/adoption_record`; its Contract header in
  `kitlib/adoption.py` loses `work_specs` and gains `record_ids` and the
  record-change judgement.
- **Two new rows** for `scripts/adoption_record` (IF-303 and IF-304 at
  today's watermark): a call row with requestors `scripts/handback` and
  `scripts/text_then_act`, and an exit-code row with consumer
  `scripts/check`, in IF-295's shape. Each has a Contract header in the
  module; CMP-008.
- **IF-175, amended** (new against revision 2, the ruling's seam): its
  Contract in `kitlib/verdict.py` names the shared close-shape reader and
  its injected relink oracle, and states that the peel calls it without
  one; its requestors gain `scripts/adoption_record`.

**Code tags (D-005, re-made).** Each `Implements:` line names every row its
function serves (sitting 007's advisory 1): the shared parser serves SR-148,
LLR-153 and LLR-335; `_archive_one_adjudication_row` serves SR-220, SR-148,
LLR-312 and LLR-335; the rider and the shared close-shape reader serve
SR-148 and the check's new LLR (the reader keeps the peel's existing tags
too); `lane_commit_walk` and `_each_lane_commit` add that LLR. CMP-008's
notes name `adoption_record` if the `component-view` step asks.

**Generated references.** The derived references the hook checks
(`interface-reference`, `component-view`, `cli-reference`) are regenerated
in the lane; the trunk-only views are restored at P12, before the gate
(recipes §3).

**Check at intent:** `trace.py --strict` and `check_trajectory.py --strict`
with the commit bar, so the Drafted set is whole before the build. The
closure check runs at P12.

## P2: the tests, committed alone (D3, D11, D12)

Build round 1's first deliverable (skill §3 Intent step 2): every new test
named in P3 to P8, in one commit before any code, each under one evidence
class.
- **New or corrected behaviour:** strict expected assertion failure
  (`@pytest.mark.xfail(strict=True, raises=(AssertionError,
  pytest.fail.Exception))`). Its red must reach the test's own assertion,
  never an import error, so `kitlib/adoption.py`, `adoption_record.py` and
  the new `kitlib/verdict.py` reader land as stubs where a test imports
  them (the builder's choice of stub). Each build row removes its own
  marks.
- **Characterization of already-correct behaviour:** unmarked, with an
  adequacy witness in the test (the wrong implementation it would catch).
  These are: `test_an_adoption_never_counts_as_an_absorption`,
  `test_a_replay_with_nothing_left_to_re_point_commits_nothing`,
  `test_the_peel_still_refuses_a_close_whose_relink_leaves_docs_work`, and
  the regressions kept green (TC-156's suite, TC-331's test, TC-173's and
  TC-313's modules, the four empty-section refusals).
- **The census** (D12) is neither: its live-instrument case (a planted
  unpaired copy) is strict-xfail until P3; the census over the repository
  itself passes before and after.

`test_adoption_record` joins `SLOW_MODULES` in this commit. A test that
fits no class is named, with its disposition, in `docs/decisions/wi-969.toml`
before the code commit.

## P3: one complete-section parser and the pure adoption module (D11, D12, D20)

**`project-trajectory/scripts/kitlib/adoption.py` (new).** Ported from
`d3d301216`: `KEY`, `OPEN_STATES`, `parse_block`, `disposed_id`,
`row_refusal` and `_hits`. Not ported: `work_specs` (the close no longer
reads trunk's working tree) and the docstring's landing-tree paragraph. The
module stays pure: no git, no writes. The repeated-id rule is enforced where
the section is assembled; `_hits` keeps its open-state filter. Its
`bootstrap_manifest.MAPPING` row is ported, its readers `intake.py`,
`handback.py` and `adoption_record.py`.

**`intake.py`:**
- `parse_disposition_section(text, where)` is the one parser, returning
  `(drafts, adoptions, refusal)`; `_section_block` is ported.
- `parse_dispositions` stays a wrapper returning drafts only; its callers
  (`agent_loop.dispositions_drafted`, `integrate._verdict_owed`,
  `handback`, `_successor_drafts`) keep their shape.

**Fence pairing, the S3 grammar.** Within the section every line that begins
with three backticks must be an opening `` ```toml `` or a bare closing
`` ``` ``; the fences alternate, open then close, starting with an open; the
count is even. Anything else refuses the whole section, naming the line,
before any block is read. Only then are the blocks harvested from the paired
fences, so the complete-fence regex can no longer skip an unclosed block.
The prose between blocks (each draft's `scope`) is cut at the same pairs.

`consolidate._section_blocks` stays as it is: the Trust section rules the
historical absorption reader unchanged, and no consolidation verdict carries
an adoption (P6 refuses one).

**Tests, in `tests/test_disposition_adoption.py`** (new, smoke, pure):
- Ported from `d3d301216`, each red at trunk (the module and the adoption
  shape are absent; `adopts` is refused as an unknown draft key):
  `test_an_adoption_block_is_parsed_apart_from_the_drafts`;
  `test_a_malformed_adoption_block_is_a_parse_refusal` (another key beside
  `adopts`; a value that is not one id);
  `test_the_disposed_row_is_read_from_either_minted_title_form`;
  `test_acceptance_is_read_against_the_registry_with_distinct_refusals`,
  re-fixtured over a supplied listing, covering missing, closed, unreadable
  (non-UTF-8 bytes; front matter that does not parse) and non-superseding
  rows.
- `test_an_adoption_never_counts_as_an_absorption` (characterization).
- `test_a_repeated_adoption_is_a_parse_refusal`. Red: trunk refuses the
  unknown key, not the repeat; the test asserts the repeat's reason.
- `test_a_valid_block_then_an_unclosed_one_is_refused`, parametrised over an
  adoption pair and a draft pair: review 015's reproduction at the parser.
  Red: for drafts, trunk's `_TOML_FENCE_RE.findall` returns the first draft
  with no refusal; the adoption variant fails on the unknown key.
- `test_a_fence_that_is_not_toml_or_a_bare_close_is_refused` (for example
  `` ```text ``). Red: trunk ignores it.
- `test_every_dispositions_section_in_the_repository_passes_the_fence_grammar`
  (D12): walks the files `git ls-files` lists under `docs/work/`,
  `docs/archive/work/` and `docs/reviews/` that carry a `## Dispositions`
  section (66 today), asserting the fence-pairing step refuses none; for
  specs, also that the new parser returns the drafts trunk's parser returned
  (through a frozen copy of trunk's regex in the test); verdict files are
  checked for pairing only. Its live-instrument case feeds one planted
  unpaired copy and asserts a refusal.

## P4: the mint's lineage corrections (D10, D22)

**Ported from `d3d301216`** (the old D-003, D-004; D-014 keeps them in the
row): `_standing_successors`, `_title_identity_refusal` and `_repoint_owed`;
`_apply_supersedes`, now returning its edits;
`_supersede_source_refusal(..., adopted=())`, `_mint(..., adopted=())`,
`_write_mint(..., adopted=())` and `_mint_message(..., adopted=())`. The
`adopted` parameter defaults to empty, so P4 lands before the record exists;
P8 fills it.

**Tests, in `tests/test_intake.py`** (slow):
- `test_a_replay_re_points_a_late_dependent_to_the_full_successor_set`,
  drafts-only form (P8 adds the adoption form). Red: trunk's dedup drops the
  already-minted draft before the lineage is built, so a dependent filed
  after the first sweep stays on the closed row.
- `test_a_title_match_off_the_drafts_lineage_refuses_the_mint`: exit 1, the
  rows named, nothing written. Red: trunk swallows the draft and returns
  `([], None)`.
- `test_a_drafts_title_match_on_its_own_lineage_stays_standing`. Red: the
  partition does not exist at trunk.
- `test_a_replay_with_nothing_left_to_re_point_commits_nothing`: a
  characterization pin of `_repoint_owed` (it may pass at trunk for drafts);
  kept because P8's adoption-only replays depend on it.

## P5: the record's cell (D1)

**The column:**
- `kitlib/registry.py`: an `Adopted` entry in `WI_COLUMNS`, with a comment
  in the voice of `Adjudicates` and `Digests`, and `("Adopted", "adopted")`
  in `SPEC_LISTS`. The generic list join carries it as data.
- `wi_convert.py`: the same entries in its column list and key map.
- `plan_artifacts.py`: its column list gains `Adopted`.
- `project-trajectory/work/WI-000.template.md`: a paragraph documenting the
  key (only the close writes it, as a non-empty TOML list of WI ids; a row
  that adopts nothing carries no key).

**The registry readers grant the cell nothing.** `parse_spec_row` does not
validate it, so a malformed record does not break every registry read; the
three consumers that act on it refuse it through the one strict reader.

**The strict reader:** `kitlib/adoption.record_ids(data, where)` returns
`(ids, refusal)`: an absent key answers `None`; it accepts only a non-empty
list of distinct, well-formed WI ids; it refuses a bare string, an empty
list, a table, a non-string element, a repeated id and a malformed id.

**The record-change judgement:** a pure function in `kitlib/adoption.py`
that P7 wraps. It takes the record each parent holds for a spec, the
commit's record and request, whether the spec moved into `complete/`,
whether the commit is the machinery's close (P7's close test), and the
validation result, and returns the S3 case: pass, or a named refusal. The
whole S3 table is thus pinned in the smoke tier, with git kept out.

**Tests:**
- `test_disposition_adoption.py` (smoke):
  `test_the_record_reader_accepts_only_a_list_of_distinct_ids` (every shape
  above; red: the reader is absent);
  `test_an_adopted_cell_survives_the_spec_row_reader` (`parse_spec_row`
  returns `Adopted == "WI-1;WI-2"`; red: trunk drops the key);
  `test_the_record_change_table`, one case per S3 row: the close's own
  commit with record equal to request and validation passing passes;
  anything carried unchanged passes; a merge's value held by any parent
  passes; refused: a record added, changed or removed outside the close, a
  record that differs from the request, a record that fails validation, a
  requesting spec moved into `complete/` with no record. Red: absent.
- `test_wi_convert.py` (slow):
  `test_an_adopted_cell_round_trips_through_the_converter` (the spec written
  by `write_spec_file` reads back cell-exact; red: the column is absent).

## P6: the close validates once and writes the record (D1, D2, D4, D11)

**`adoption_record.py` (new, CMP-008, beside `plan_gate.py`).**
- `tree_specs(root, rev)` and `_tree_text(root, rev, path)`, ported from the
  old lane's `intake._tree_specs` and `_tree_text`, keeping strict UTF-8 and
  LF normalisation (D-007 F2 kept, moved).
- `validate_at(root, rev, title, owes, adoptions)` returns
  `(record, refusal)`: the disposed id from the title
  (`kitlib/adoption.disposed_id`); each id through `row_refusal` over
  `tree_specs(root, rev)`; the record is the request's ids in block order. A
  tree git cannot list is a refusal, never a fallback.

Its MAPPING row joins the bootstrap manifest.

**`handback._archive_one_adjudication_row`:**
- reads `parse_disposition_section` once;
- `owes_successor` is discharged by drafts or adoptions;
- `_consolidation_close(..., adoptions)` refuses an adoption before its
  first write (ported);
- then `adoption_record.validate_at(wt, "HEAD", ...)` runs before any move:
  the lane's HEAD is the tree the closing commit is made on, so that
  commit's parent;
- `_adjudication_close_text(text, deliverable, adopted)` writes
  `adopted = [...]` into the front matter in the same rewrite that clears
  `specref`, where `wi_convert.write_spec_file` would serialise the key, so
  a converter round trip of the closed spec is byte-stable;
- on any refusal nothing moves, no record is written, and the refusal names
  the reason.

`close_adjudication`'s loop over a multi-row lane is unchanged; its
behaviour when a later row refuses after an earlier row moved predates this
row, so the tests here are single-row, and a builder who sees that gap
surfaces it as a finding. The old lane's `intake.adoption_lineage` and its
read of trunk's working tree are not ported.

**Tests, in `tests/test_handback.py`** (slow). Fixtures file the successor
on trunk before the lane is cut (lane record, "Survives"). The trunk
baseline every adoption test fails against: trunk refuses an `adopts` block
as an unknown draft key, or as "drafted NO successor".
- `test_an_adoption_of_a_superseding_row_closes_and_writes_the_record`:
  the spec is in `complete/`, its front matter holds `adopted = ["WI-…"]`,
  `specref` is cleared, the commit carries the machinery's subject.
- `test_an_adoption_that_is_not_accepted_refuses_the_close`, parametrised
  over missing, closed (in `complete/` and in `cancelled/`), unreadable
  (committed non-UTF-8 bytes; front matter that does not parse, with the
  distinct "cannot read" reason) and non-superseding. Each asserts the lane
  worktree's `git status --porcelain` is empty, HEAD is unchanged, the spec
  is still in `active/<branch>/`, and no file contains `adopted =`.
- `test_an_adoption_without_a_disposition_event_token_refuses`, same
  asserts.
- `test_a_repeated_adoption_refuses_the_close`, same asserts.
- `test_a_drafted_successor_beside_an_adoption_still_mints`: the close
  writes the record; the merge sweep mints the draft (a new id); a
  dependent of the closed row ends on both successors. It needs P8: its
  strict-xfail mark names P8 and P8's commit removes it.
- `test_a_valid_block_then_an_unclosed_one_refuses_the_close`, parametrised
  over adoption and draft (D11 at the close). Red: for drafts, trunk closes
  and the second draft is lost; for adoptions the unknown-key refusal is a
  different reason, and the test asserts the fence reason.

Then:
- `tests/test_consolidate_close.py` (slow):
  `test_a_consolidation_verdict_that_adopts_refuses_the_close` (ported),
  asserting the lane tree is byte-identical. Red: trunk refuses on the
  unknown key, not by this reason.
- Kept green: TC-156's handback suite, TC-331's
  `test_an_unreadable_claim_is_never_closed_early`, and
  `test_the_refusal_invariant_stops_a_disposition_with_no_successor` /
  `..._cancelled_close_with_no_successor`.

## P7: the commit check (D5 to D9, and D1 for the real close)

**The rule:** `adoption_record.commit_adoption_record_lines(root, rev)`.

**Parents.** Read with `acceptance_record._commit_parents`, the one parent
reader of the per-commit rules. A parent the repository cannot read,
including one behind a shallow boundary, is a line naming it, never a root
(TC-313's precedent).

**What it reads.** One `git diff --name-only --no-renames <parent> <rev> --
docs/work docs/archive/work` per parent. If no spec path is touched it
returns `[]` with no further read, so a lane's ordinary commits cost one git
call each.

**What it judges.** For each touched spec, keyed by the WI id in its file
name, across both spec roots and every state folder: the record at the
commit and at each parent, with `record_ids`; the request at the commit,
read only when the record changed or the spec moved into a `complete/`
folder. It then applies P5's judgement.

**The close test (changed, sitting 016's FIX).** "The machinery's close"
is no longer read off the peel's attestor. It is read by one shared
close-shape reader in `kitlib/verdict.py`, extracted from `_closed_wi_ids`
and `mechanical_close_attestation`:
- `mechanical_close(root, rev, relinked=None)` (the builder may name it)
  returns `(parent, closed ids)` or None. It reads the one parent (a merge
  is never a close), the `--name-status --no-renames -z` stream, and applies
  the existing shape unchanged: paired deletions from one
  `docs/work/active/<branch>/` and additions of the same names to
  `docs/work/complete/`; no other `A` or `D`; `M` inside `docs/work/`
  unrestricted (the relink of other rows); the ids ordered by
  `mechanical_close_order` and composed through `mechanical_close_subject`,
  equal to the subject.
- **A path outside `docs/work/`.** With `relinked=None` it refuses, exactly
  as today. With an oracle, each such path must be an `M` entry and
  `relinked(old_bytes, new_bytes, path, remap)` must be true, where `old`
  and `new` are the path's blobs at the parent and at `rev`, and `remap`
  maps each paired active path to its `complete/` path (the commit's own
  moves, re-derived from the A/D records, as `integrate._relinked_exactly`
  and `plan_gate._close_homes` derive theirs). An `A` or `D` outside
  `docs/work/`, an unreadable blob, non-UTF-8 bytes, or any byte beyond the
  relink refuses.
- `mechanical_close_attestation(root, rev)` becomes `mechanical_close(root,
  rev)`'s parent with no oracle, so the peel is unchanged and the existing
  `test_verdict_record.py` attestor tests stay green untouched.
- The record rule calls `mechanical_close(root, rev,
  relinked=spec_move.exact_relink)`, with the WI id among its closed ids.
  `kitlib/verdict.py` imports no script; the oracle is injected, as
  `kitlib.done_when.staged_hold` takes it.

For the close, validation is `validate_at(root, parent, title, ...)`: the
same function P6 ran, in the same tree. The record/request compare and the
parent-tree validation are unchanged.

**A merge** is judged by what neither parent carried. Merges and the moves
after a landing (`complete/` to the archive's `complete/`) carry the record
unchanged, and pass.

**Where the rule runs:**
1. **The merge slot.** The rule is appended to
   `text_then_act.LANE_COMMIT_RIDERS` (Deliverable 3, Trust), so
   `integrate._each_lane_commit` judges every lane commit with it.
   - `integrate._text_then_act_refusal` currently appends
     `TEXT_THEN_ACT_REMEDY` to whatever line any rider returns. Its
     composition changes so the remedy is added to text-then-act lines only.
     The record rule's lines carry their own remedy: "only
     `handback.close_adjudication` writes the record; close the row through
     it".
   - The rung's label, "text and act", becomes the walk's.
2. **The pre-commit hook.** A new `adoption-record` step: a row in
   `check.py`'s step table with `[sys.executable, adoption_record.py]` as
   its command (IF-295's shape, `plan_gate`'s precedent); the step name
   appended to the shipped `hooks/pre-commit` `--run-steps` list; a comment
   block beside `text-then-act`'s there. `adoption_record.main` judges the
   index against HEAD, and against MERGE_HEAD while a merge is in progress.
   Outside a squash landing, any staged record change, or any requesting
   spec moved into `complete/`, is refused. The close commits with the hook
   skipped, so it never meets this step in that position.

**The squash landing in the hook.** The record step owns its squash
handling rather than standing down on `text_then_act._squash_lines`, whose
exemption is keyed to the approval-act registries (a squash whose spine
matches the tip while its index carries a hand-edited record would go
unjudged). When git's `SQUASH_MSG` names a tip that contains HEAD: a staged
record equal to that tip's own record for the spec is exempt; the commits
HEAD..tip are walked with this rule
(`text_then_act.lane_commit_walk(root, commits, (rule,))`), so the lane's
close commit meets the relink-admitting close test there too; any other
staged record change is judged as above. `text_then_act._squash_lines` then
walks only text-then-act's own rule, so its lines never carry a record
refusal under the wrong remedy and its tests stay green. This is recorded
as a lane decision, with WI-913's `plan_gate` shape (its own rider, slot
rung and squash walk) named as the alternative, passed over because the spec
and Trust name `LANE_COMMIT_RIDERS` for the slot.

**The peel's premise.** The docstring of `mechanical_close_attestation`
names the record ("the record it adds is the request's validated result,
which the adoption-record rule verifies") and states that it reads the
shared shape with no relink oracle. What it verifies is unchanged.

**Removed from revision 2:** the paragraph "A residual stated, not built
against". A close whose relink reaches outside `docs/work/` is now admitted
by the record rule when the relink is exact; it is still not peeled.

**Tests, in `tests/test_adoption_record.py`** (new, real git, in
`SLOW_MODULES`). Every refusal test is red at trunk because no rule exists
and the commit is accepted; every pass test is red because trunk's close
refuses the adoption.
- **D5:** `test_the_closes_own_commit_passes` (made by the real
  `handback.close_adjudication`);
  `test_a_later_commit_carrying_the_record_unchanged_passes` (the move to
  `docs/archive/work/complete/`, and an unrelated edit to the closed spec's
  body).
- **The real-close regression (sitting 016):**
  - `test_a_real_close_relinking_a_file_outside_docs_work_passes_the_rider_and_the_squash_hook`.
    The lane carries a committed `docs/reviews/<lane>/NNN-REVIEW-A-….md`
    linking the active spec by a relative path (as a review drawn while the
    row is in `active/` does, LLR-207). The real `close_adjudication` runs.
    Asserted: the close commit modifies that review file (the case is
    real); `kverdict.mechanical_close_attestation(root, close) is None`
    (the peel is unchanged); `integrate._each_lane_commit` with
    `LANE_COMMIT_RIDERS` returns None over the lane; then on trunk a
    `git merge --squash` of the lane, with `adoption_record.main` and
    `check.py --run-steps adoption-record` both exiting 0. Red at trunk:
    the adoption close refuses.
  - `test_a_hand_written_record_beside_the_same_relink_is_refused`,
    parametrised, each at the slot (`_each_lane_commit`) and at the hook
    step: (a) the same paired move, the same exact relink of the review
    file and an `adopted` record written by hand under a hand subject;
    (b) the composed subject and paired moves, with the review file's relink
    plus one byte more (not the exact relink); (c) the composed subject,
    paired moves and the exact relink, with a record that differs from the
    request. Red at trunk: no rule, accepted.
- **D6:** `test_a_record_written_in_a_lane_commit_is_refused_at_the_slot`
  (through `integrate._each_lane_commit` with `LANE_COMMIT_RIDERS`);
  `test_a_hand_close_writing_a_record_is_refused` (the right move under a
  hand subject); `test_a_record_staged_on_trunk_is_refused_by_the_hook_step`
  (through `adoption_record.main` and `check.py --run-steps
  adoption-record`).
- **D7:**
  `test_a_close_shaped_commit_whose_record_differs_from_the_request_is_refused`;
  `test_a_close_shaped_commit_whose_adoption_fails_in_the_parent_tree_is_refused`
  (the adopted row was closed in the parent; the commit carries the composed
  subject and paired moves, built by hand so the shape holds).
- **D8:** `test_a_record_changed_later_is_refused`,
  `test_a_record_removed_later_is_refused`.
- **D9:**
  `test_a_requesting_spec_moved_into_complete_without_a_record_is_refused`,
  at the slot and at the hook step.
- **Merges, parents and squashes:**
  `test_a_refresh_merge_carrying_trunks_record_passes`;
  `test_a_parent_behind_a_shallow_boundary_is_refused_by_name`;
  `test_a_rebased_lanes_squash_landing_is_admitted`;
  `test_a_squash_whose_index_edits_the_tips_record_is_refused`.
- **Wiring:** `test_the_pre_commit_hook_runs_the_adoption_record_step`
  (red: absent); `test_the_record_rule_rides_the_lane_commit_walk`
  (`LANE_COMMIT_RIDERS` contains it; red: absent);
  `test_a_record_refusal_at_the_slot_does_not_carry_the_text_then_act_remedy`
  (red: today's composition appends the remedy to every rider line).

Also:
- `tests/test_disposition_adoption.py` (smoke, pure):
  `test_the_close_shape_admits_outside_paths_only_through_the_oracle`. Over
  a hand-built name-status field list and a fake oracle: an outside `M`
  path is refused with no oracle, admitted when the oracle answers true,
  refused when it answers false; an outside `A` or `D` is refused even with
  an oracle that answers true; the oracle receives the commit's own remap.
  Red: the reader is a stub. (If the builder keeps the shape pure over
  fields with blobs read by a callable, this pin needs no git.)
- `tests/test_verdict_record.py` (slow):
  `test_the_peel_still_refuses_a_close_whose_relink_leaves_docs_work`, a
  characterization: a real close with an outside relink is not peeled.
  Adequacy witness: an implementation that passed the oracle to the
  attestor (widening the peel, which the ruling forbids) fails it.

**Regressions.** TC-173's `tests/test_text_then_act.py`, TC-313's
`tests/test_ruling_sync.py`, the attestor tests in
`tests/test_verdict_record.py` and `tests/test_handback.py`'s attestor pin
stay green unchanged.

## P8: the sweep trusts the record (D1, D2, D10, D11, D21)

**`intake._merged_dispositions(root, hit, relpath)`** (ported from
`d3d301216` without its history arm) returns `(meta, drafts, lineage,
refusal)`. It refuses, with nothing minted: a merged spec it cannot read or
whose front matter does not parse (trunk's `_disposition_drafts` today
`continue`s past it); and the four bad request/record pairs (request with no
record, record with no request, the two differing, a malformed record
through `record_ids`). With no adoption, the OI-73 empty-section guard keeps
its text and adds "or adopted". The lineage is `[(adopted, [disposed])]`,
built from the record, with `disposed` read from the title by
`disposed_id`; an untokened title is a refusal. Nothing is validated, and no
git or adopted-row state is read.

**`_disposition_drafts`** returns `(drafts, lineage, refusal)`, and
`intake_after_merge` passes the lineage to `_mint` (P4's parameter).

**Not ported:** `_landing_commit`, `_UNLANDED`, `import retire`,
`import functools`, `from kitlib import git as kgit`; `adoption_lineage`;
intake's `_tree_specs` and `_tree_text` (moved to P6).

**`_successor_drafts`** reads through the same parser, so an unpaired fence
in a SUCCESSOR Done-when verdict's section is refused there too.

**Tests, in `tests/test_intake.py`** (slow). Fixtures produce the record
through the real close (P6) where the case allows; refusal cases write the
spec by hand on a fixture branch (the fixtures' hooks are `hooks_on` stubs).
The trunk baseline for the adoption tests: trunk rejects `adopts` as an
unknown draft key.
- `test_a_recorded_adoption_re_points_a_dependents_needs`, minting nothing.
- `test_drafts_and_adoptions_together_hold_the_full_successor_set`.
- `test_a_replay_re_points_a_late_dependent_to_the_full_successor_set`, the
  adoption form beside P4's drafts form.
- `test_a_consumed_adoption_replays_after_its_successor_completes`
  (ported).
- `test_a_shallow_clone_sweeps_a_recorded_adoption`: `git clone --depth 1
  file://…` of the landed fixture, then `intake.py sweep --merged WI-…` in
  the clone, asserting the re-point (the sweep reads no history). Run with
  `MSYS_NO_PATHCONV` unset (recipes §7).
- `test_the_sweep_refuses_a_request_and_record_mismatch`, parametrised over
  the four pairs; asserts exit 1, nothing minted, no bookkeeping commit, an
  unchanged dependent. (Request with no record: trunk refuses on the key,
  the test asserts the record reason; record with no request: trunk ignores
  the key; the other two: trunk has no record reader.)
- `test_an_unreadable_merged_adjudication_spec_refuses_the_sweep`
  (ported). Red: trunk `continue`s past it and returns `([], None)`.
- `test_a_valid_block_then_an_unclosed_one_refuses_the_sweep`, over adoption
  and draft. Red, for drafts: trunk mints the first and drops the second.
- `test_a_successor_done_when_verdict_with_an_unclosed_block_is_refused`.
  Red: trunk's `findall` drops it.

Then:
- `tests/test_verdict_record.py` (slow):
  `test_the_scheduler_and_the_gate_read_an_adoption_by_its_shape` (ported):
  a well-formed adoption owes no review round, and a malformed section
  still fails toward review. Red: trunk's unknown-key refusal reads as
  review owed.
- Rewritten, not ported: the old lane's
  `test_the_sweep_accepts_an_adoption_only_of_a_superseding_row` becomes the
  record-trusting case above; the five history-read regressions the lane
  record lists are not ported. The two empty-section refusals in
  `test_intake.py` stay green unchanged.

## P9: the consumer text (D1, D2)

**`prompts/adjudicate-disposition.template.md`.** Item 3 gains the adoption
form, re-worded from `d3d301216`: when a row superseding the closed one is
already open, adopt it with a block holding exactly `adopts = "WI-…"`; an
adoption mints nothing and is the same successor exit, not a third one. The
old lane's "the close and the merge accept it only while…" is replaced: the
close accepts an adoption only if that row is open and supersedes the closed
row in the lane's tree when the row closes, and it records the adoption
there. The machine-line paragraph says `successors=` counts drafts and
adoptions together, and that a disposition which neither drafted nor adopted
is refused. `prompts/CATALOG.md` is regenerated; the `prompt-catalog` step
checks it.

**`project-trajectory/skills/coordinator-cycle/references/recipes.md`,
synced to `.claude/skills/` and `.agents/skills/`** (`skills-sync` checks
the copies):
- **§8.** The "Until WI-902 lands" hand-close paragraph is replaced: an
  adopting disposition closes through `handback.close_adjudication` and
  lands inside the squash, never by a hand close, which the adoption-record
  step refuses; an inbound link elsewhere in the repository needs no
  workaround (the close's exact relink is admitted).
- **§3.** "(WI-902, act 117)" becomes a citation of the archived lane tip
  `d3d301216`, with no act number (D-009's withdrawal).

This repo's tooling, so no RESYNC entry.

**D2.** OI-73's "no third exit" is kept: the prompt, the OI-73 guard's
message at the close and the sweep, and LLR-335's text (P1) all state an
adoption as the successor exit. The guard still refuses a section that
neither drafts nor adopts, and an open item alone still does not discharge
it.

**No new tests.** The `prompt-catalog` and `skills-sync` steps are the
checks. P8's and P6's kept empty-section refusals pin D2's refusal half at
the sweep and the close.

## P10: the RESYNC_PACK.md entry (D19 to D22)

**One new entry in `project-trajectory/RESYNC_PACK.md` §3**, "A disposition
can adopt an already-filed successor", anchored `[since <sha>]` at the trunk
commit the lane is based on when P10 is written, so the P11 reviewers read
it. P13 re-anchors it at the trunk commit the landing is rebased on. The old
lane's entry is never ported, so this one replaces it.

**"What changed":** the adoption block; the close's single validation and
its `adopted` record; the hook's new `adoption-record` step and the slot
rule (only the close writes the record; its exact relinks are admitted);
the sweep's trust of the record.

**The three tightenings:**
- **D20.** An unpaired fence in a `## Dispositions` section is refused, for
  drafts too, where a trailing unclosed block was silently dropped.
- **D21.** An unreadable merged spec, or one whose front matter does not
  parse, refuses the sweep (exit 1, the merge stands), where it was skipped.
- **D22.** A drafted title held by a row on another lineage, or by two
  rows, refuses the mint before any write, where the draft was swallowed.

**Kit-owned files to overwrite:** `scripts/intake.py`,
`scripts/handback.py`, `scripts/text_then_act.py`, `scripts/integrate.py`,
`scripts/check.py`; `scripts/adoption_record.py` (new);
`scripts/kitlib/adoption.py` (new), `scripts/kitlib/registry.py`,
`scripts/kitlib/verdict.py`, `scripts/kitlib/bootstrap_manifest.py`;
`scripts/wi_convert.py`, `scripts/plan_artifacts.py`; `hooks/pre-commit`;
`prompts/adjudicate-disposition.template.md`, `prompts/CATALOG.md`;
`work/WI-000.template.md`.

**"What to do":** no registry or setting migration. Before the first sweep
after upgrading, check that no merged `complete/` spec has unparseable front
matter, no pending `## Dispositions` section has an unpaired fence, and no
pending drafted title is already a row's title under another `supersedes`.
The sweep now stops on each, naming the file or rows.

**Check:** reviewers verify the anchor with `git merge-base --is-ancestor`.

## P11: iterate, in counted rounds, before any sitting (D18, D23)

Coordinator-cycle skill §3, "Iterate" and "Rounds, the cap and the
convergence round". It runs after P3 to P10's build is committed, and before
anything is sat.

**Each round:**
1. **The tip carries the review bar's attestation** (changed from revision
   2; WI-956, WI-957): the round's work is committed through `integrate.py
   attest` with the round's `--tests`; `review_brief.py review` refuses any
   other tip. A hook-refused commit or a red bar attests nothing.
2. **The lints after the build round:** `check_trajectory.py --strict`
   clean and `trace.py --strict` with no finding beyond LLR-292's, with the
   commit bar (`run.cmd smoke`; its seconds reported against
   `[smoke-budget]`).
3. The full-lane reviewers in the skill's shape under Roles, each from its
   own brief rendered by `review_brief.py review --scope full` from the
   lane's trunk base to its tip, filed with `review_brief.py file --phase
   REVIEW-A` or `REVIEW-B`. The first counted round is this lane's next
   review in `docs/reviews/wi-969/`, and its count is zero before it (P0's
   decision, D18).
4. Triage under the review threat model; a `Plan-WI` coverage plan per round
   file through `plan_coverage.py --findings`; findings confirmed or refuted
   on the real code path; a dispute sitting for a contested finding.
5. Fixes are code and trace fields only (`Implements:`, the LLR module and
   symbols, TC Evidence). Proposed row text goes to the lane's spine change
   list, for P12.

**The red cap** (new against revision 2; WI-958): each red `integrate.py
attest` is a red round in `docs/decisions/wi-969.toml`; at `[build]
red_rounds_max` consecutive red rounds the lane closes partial (recipes §8),
never a new stop.

**The cap.** At most three counted rounds; the third renders `--stance
convergence` after the convergence map is recorded in the lane's decisions.
At the cap, every open BLOCKER or MAJOR goes to one dispute sitting. P11
ends at the first counted round with no BLOCKER or MAJOR; P12 starts only
then.

**The Done-when hold.** No Done-when change is planned. If one arises, a
verdict bound to its exact text, or an owner ruling, comes before the next
build round.

**No new tests beyond findings.** Each accepted finding's fix carries its
regression test, red before the fix, through the coverage plan.

## P12: the checkpoint, then the gate (D13 to D16, D18)

Coordinator-cycle skill §3, "Checkpoint", when a counted P11 round has no
BLOCKER or MAJOR.

**1. Reconcile.** Terra, resumed, reconciles P1's whole set against the
settled code: the spine change list P11 accumulated, plus the arms map,
including D-002's final `intake.py` stamp (and D-002's alternative,
decomposing the Dispositions parsing out of `intake.py`, weighed again and
recorded for the owner) and TC Evidence names a fix round renamed. The
coordinator verifies, regenerates and commits it before the sitting. The
turn is omitted only if no round proposed row text and no code moved since
P1, recorded with the mechanical check the skill names.

**2. The closure check** passes (`spine-authoring`,
`references/in-lane.md`); `trace.py --strict` and `check_trajectory.py
--strict` are clean.

**3. One combined sitting**, composed by `coordinator_adjudicate.py
adjudicate --brief combined`, top-down: SR-148's amendment; the re-sit of
LLR-153, LLR-161, LLR-312, TC-147, TC-156 and TC-254; the first approval of
LLR-335, TC-360 and the commit check's LLR and TC; the interface rows
(IF-294, the two new rows, IF-175's amendment) stated in their final form.
The sitting ends at its committed verdict; its act is P13's. Returns are
routed per the skill (text to Terra, code to the builder), and the returned
rows and any chain they change are re-sat.

**4. Restore** the trunk-only generated views on the lane (recipes §3). The
module-size stamp stays.

**5. The gate.** The full-lane reviewers run uncounted over the checkpoint
tip (attested as in P11 step 1), from the lane's trunk base, with
`review_brief.py review --scope full --stance convergence`, after the
convergence map. They review code and rows together. An open BLOCKER or
MAJOR goes to the dispute sitting; a fix round it orders is followed by one
more checkpoint (steps 1 to 4) before P13.

## P13: land (D17, D19, D23)

Coordinator-cycle skill §4, after P12's gate.

**1. Rebase** onto current trunk (recipes §3 and §4). P10's entry is
re-anchored `[since <sha>]` at the trunk commit the lane now sits on. If the
rebase changed code or authored rows, P12's affected checkpoint steps are
repeated and an uncounted convergence round runs over the rebased tip.

**2. The unchanged-rows check.** The rows the P12 verdict judged, read at
the verdict's own commit, are compared with the rebased tip; a changed or
renumbered row is re-sat.

**3. The act turn**, `coordinator_adjudicate.py act --verdict <path> --wi
WI-969`, takes its acts at one above trunk's ledger top at that time: the
lane's last spine commit.

**4. D17's proof.** For each of `a2a95f847`, `7c4544ef3`, `acab09035`,
`a588ae83f` and `97ea2e47d`, `git merge-base --is-ancestor <sha> <lane tip>`
exits 1; and `docs/archive/last_approved/acts.toml` on the lane adds only
rows above trunk's top, each citing this lane's own verdicts.

**5. The full suite once**, alone on the box: `python -m pytest -q -n auto`;
its real output is pasted into the log.

**6. The squash landing.** The squash's own commit meets the hook, so the
new `adoption-record` step judges the squash by its tip's commits (the
lane's own close, if it has one, through the relink-admitting close test).
Then the row is closed, the tips archived, and the sweep run (recipes §3).

**7. The bar on the landing tip** (D23): the smoke tier within its budget,
read quiet; `check_trajectory.py --strict` clean; `trace.py --strict` with
no finding beyond LLR-292's. D17's ancestry check is re-run there.

The landing lands alone (spec S1, "Landing"; skill §4): it changes the
close, the sweep and a hook step.

## Risks the builder should know

- **The squash condition (P7).** The text-then-act squash exemption is keyed
  to the approval-act registries; the record step must not stand down on
  it. P7's last squash test is the pin.
- **The shared close-shape reader (P7).** Extracting it must leave the peel
  byte-for-byte in behaviour: the attestor passes no oracle, and the
  existing attestor tests plus
  `test_the_peel_still_refuses_a_close_whose_relink_leaves_docs_work` pin
  that. The oracle's `remap` must use the same full-path form `move_spec`
  passes to `_relink_inbound_links` (active spec path to `complete/` spec
  path), or `exact_relink` will never match a real relink; the real-close
  regression catches a mismatch.
- **Red reaching the assertion (P2).** A strict-xfail test whose red is an
  import error does not count; stub the absent modules and functions.
- **Smoke budget.** All new git tests are in slow modules; the smoke pins
  are pure. Read the tier's reported seconds at each commit.
- **Shallow-clone tests on Windows.** Run with `MSYS_NO_PATHCONV` unset
  (recipes §7). A sandboxed `sh.exe` failing CreateFileMapping is a launcher
  limit, not a finding (review 015's note).
