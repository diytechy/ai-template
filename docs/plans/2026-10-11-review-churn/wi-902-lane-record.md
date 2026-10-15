# WI-902: the lane's record, decided under record-at-close

**The lane.** Branch `wi-902`, worktree `C:/Projects/ai-template.wt/wi-902`,
tip `d3d301216`. It was rebased on trunk at `ccd66391` and is now 48 commits
ahead. Its earlier pre-rebase tips, `c1ab6585` and `6611b160`, are cited by
its verdicts.

**The ledgers.** Trunk's act ledger runs to seq 112 and the lane's to 117.
Trunk's watermark is LLR 326, TC 351, IF 293; the lane's is LLR 335, TC 360,
IF 294.

**How this record was settled.** A planner drafted it and the coordinator
ruled it on 2026-10-14, as written except where its five calls say
otherwise: `docs/decisions/coordinator-2026-10-14.toml` D-009 (no act of
113–117 lands), D-010 (re-cut, not rebase), D-011 (the kept ids), D-012 (the
record's carrier) and D-013 (the parser fix stays in the row). The survivors
in (b) go to the owner to confirm or overrule, through the re-cut lane's
decisions record. The amended spec is WI-902's own, under `docs/work/`; its
plan item is [item 2](README.md#2-record-the-decision-at-its-event-checked-at-the-commit).

## What the rebuild throws away, and what survives

**Thrown away: the history-reading sweep.** In all, this is about 40 lines of
`intake.py` plus five regressions:
- `intake._landing_commit`, which runs
  `git rev-list --first-parent --reverse HEAD -- <both complete/ paths>`.
  With it go its `retire.shallow_boundary` test, the `retire` import and the
  `_UNLANDED` refusal.
- The sweep's own adoption validation, i.e. the
  `adoption_lineage(root, meta, adoptions, relpath, landing)` call in
  `_merged_dispositions`. The sweep now builds its lineage pairs from the
  record and validates nothing.
- The close's read of trunk's working tree (`kadoption.work_specs` over
  `root`). The close now reads the lane HEAD's tree, which becomes the parent
  of its commit, because that is the tree the commit check can re-run the
  same validation on. `work_specs` goes once it is unused.
- Text that describes the landing-tree rule, the shallow-clone refusal and
  `git fetch --unshallow`: the module docstrings, the IF-294 Contract
  wording and the lane's RESYNC entry. The prompt's sentence "the close and
  the merge accept it only while…" goes too.
- The five regressions of the history read:
  - `test_the_first_sweep_of_an_adoption_still_reads_its_open_state`
  - `test_a_rejected_adoption_stays_refused_on_replay`
  - `test_an_adoption_whose_landing_commit_cannot_be_read_refuses`
  - `test_an_adoption_whose_landing_lies_past_a_shallow_boundary_refuses`
  - `test_an_adoption_of_a_successor_whose_landed_spec_is_not_utf8_stays_refused`

  The amended Done-when replaces each with a case at the close, the check or
  the sweep.
- `test_the_sweep_accepts_an_adoption_only_of_a_superseding_row` is
  rewritten. The sweep now accepts a recorded adoption and refuses a request
  that has no record.

**Survives: everything else the lane built.**
- **`kitlib/adoption.py`:** `KEY`, `OPEN_STATES`, `parse_block`,
  `disposed_id`, `row_refusal` and `_hits`, with their docstring re-worded.
- **`intake.py` parsing:** `parse_disposition_section`, `_section_block` and
  the `parse_dispositions` wrapper. The parser gains the unpaired-fence
  refusal (D-010).
- **`_merged_dispositions`:** its unreadable-spec refusal, and its role as
  the home of the OI-73 empty-section guard.
- **`_tree_specs` and `_tree_text`:** these read strict UTF-8 and normalise
  to LF. They are repurposed as the one tree reader shared by the close (the
  lane's HEAD) and the check (the commit's parent).
- **The lineage join:**
  - `_apply_supersedes`, which takes adopted pairs and returns its edits;
  - `_supersede_source_refusal(..., adopted)`;
  - `_mint(..., adopted)` and `_write_mint(..., adopted)`;
  - `_mint_message` and `_repoint_owed`.
- **Title identity:** `_standing_successors` and `_title_identity_refusal`
  (D-003, D-004).
- **`handback`:** the consolidation arm's refusal of an adoption, and the
  rule that `owes_successor` is discharged by adoptions.
- **Prompt, manifest and recipe:** the prompt's adoption form and its
  `successors=` sentence, the bootstrap `MAPPING` row, and the §8 recipe
  edit (re-worded).
- **Tests:**
  - all five in `test_disposition_adoption.py`;
  - the four adoption cases in `test_handback.py`, extended to assert the
    record. They now file the successor before the lane is cut, as WI-893 was
    filed before WI-894's lane; today's fixtures file it on trunk afterwards,
    which the lane-tree validation would refuse;
  - `test_consolidate_close.py::test_a_consolidation_verdict_that_adopts_refuses_the_close`;
  - `test_verdict_record.py::test_the_scheduler_and_the_gate_read_an_adoption_by_its_shape`;
  - in `test_intake.py`: the unreadable-spec, re-point, full-successor-set,
    late-dependent-replay and title-identity cases, and
    `test_a_consumed_adoption_replays_after_its_successor_completes`, with
    their fixtures carrying the record.

**New in the rebuild:**
- the `adopted` cell and its strict reader;
- the close's write of the record;
- the commit check, both as a rider and in staged form;
- the sweep's comparison of request against record;
- fence pairing in the parser.

## (a) Acts 113–117

The ledger rows for 113–117 carry no `verdict` key. Each act's verdict is
named in its act commit's message, and in the line that commit adds to
`docs/archive/last_approved/README.md`. All five rows are dated 2026-10-11.

| Seq | Commit | From verdict | Approved / re-attested | What it blessed |
|---|---|---|---|---|
| 113 | `a2a95f847` | `docs/reviews/wi-902/006-ADJUDICATE-a52f1fb.md` (amendment, MEANING, released rung) | re-attested SR-148 | SR-148's AcceptanceCriteria gains the third outcome: "or names an already-open item that supersedes it as its successor". The act copied `system-requirements.toml` whole. |
| 114 | `7c4544ef3` | `007-ADJUDICATE-48b41d7.md` (amendment, MEANING ×6, released rung) | re-attested LLR-153, LLR-161, LLR-312, TC-147, TC-156, TC-254 | <ul><li>LLR-153/TC-147: the mint's adoption arms. An adopts-only block allocates no id. Title identity and lineage are resolved together. Replays use the full successor set. A replay that does nothing commits nothing. An unreadable merged spec refuses. SR-148 is added to the row.</li><li>LLR-161/TC-156: a continuation "drafts or adopts".</li><li>LLR-312/TC-254: a consolidation adoption refuses.</li></ul> |
| 115 | `acab09035` | `007-ADJUDICATE-48b41d7.md` (first approval, APPROVE ×2) | approved LLR-335, TC-360 (Drafted to Approved; `--approves "…=WI-902"`) | The first replay design. The close and the landing sweep apply the open-state rule; a later sweep applies a lineage-only rule. |
| 116 | `a588ae83f` | `013-ADJUDICATE-6bf8953.md` (amendment, MEANING ×2, released rung) | re-attested LLR-335, TC-360 | Rounds 5–6: every sweep judges in the landing commit's tree, a shallow-boundary landing refuses, and history reads use strict UTF-8 (rulings 009 and 011, review 010 F2). |
| 117 | `97ea2e47d` | none of its own; `--approves` names sitting 013 | re-attested nothing | A traced-only re-anchor of `test-cases.toml` after IF-294 joined TC-360's Verifies (lane D-009). The same commit adds D-009's text. |

**Ruled (D-009): no act lands. Rows whose text survives are re-judged; acts
that blessed the replay design are retired.**

- **113, re-judged (SR-148).** The amended AC does not depend on the
  mechanism, and it stays true under record-at-close: the adoption is still
  "an already-open item that supersedes it", judged at the close. The text is
  expected to stand unchanged. Re-sit it at the rebuilt lane's checkpoint
  with the other rows, and take its act there, above trunk's top. The
  cheaper alternative would save SR-148's re-sit: keep verdict 006's SR-148
  blessing and re-take the act from it after the re-cut, under WI-912's act
  turn, provided SR-148's bytes are unchanged since 006 and on trunk. This
  record does not recommend that. Act 113 copied the lane's whole SR
  registry as of a tree the re-cut replaces, and the checkpoint sits anyway.
- **114, re-judged (all six rows).** None of the six states the history read,
  so each text is expected to stand. LLR-153 and TC-147 cite LLR-335 for
  acceptance and re-point "any adoption accepted under LLR-335", which a
  recorded adoption still is. The rebuild does change the code their trace
  homes cite: the close writes the record, the sweep's adoption path
  changes, and the tests are re-fixtured. `coordinator-cycle` §4 repeats a
  checkpoint when code changes, so these rows are re-sat at the rebuilt
  checkpoint and their act is taken there.
- **115, retired.** It approved the first replay design. LLR-335 and TC-360
  are rewritten (part (c)). They return to Drafted when the act is dropped,
  and take a first approval of the new text at the rebuilt checkpoint.
- **116, retired.** It blessed exactly the landing-tree, shallow-boundary and
  UTF-8 replay arms that ruling 2 removes.
- **117, retired.** There is nothing to keep, because the rebuilt lane
  anchors its registries through its own acts.

**Mechanics (D-010: re-cut, not rebase).**
- **Re-cut.** At the rebuild the lane is re-cut from trunk's tip and the
  survivors above are ported, so the five act commits, their snapshot
  copies, their `acts.toml` rows and their README lines never come across.
  Act 117's commit also carries D-009's text in `docs/decisions/wi-902.toml`;
  the ported decisions record keeps that text, marked withdrawn. The lane's
  reviews 001–015 and its adjudications 004, 006, 007, 009, 011 and 013 are
  ported unchanged, as its record.
- **No renumbering.** Because no act is kept, nothing needs renumbering, and
  no duplicate seq can reach trunk (WI-866's failure, its D-002). WI-914's
  (B2's) LLR-292 act takes seq 113 freely.
- **Status.** LLR-335 and TC-360 are added `Drafted` in the re-cut lane,
  since act 115's flip does not come across.
- **Archive.** Archive the old tip `d3d301216` whole to `archive/lanes`
  (recipes §3); it contains the five act commits. Add the earlier
  pre-rebase tips its verdicts cite, `c1ab6585` and `6611b160`, as extra
  parents unless `archive/lanes` already reaches them.
- **New acts.** The rebuilt lane takes its acts at its own checkpoint, one
  above trunk's ledger at that time.
- **Passed over.** A rebase of the 48 commits that drops the five act
  commits: no interactive rebase is available here, and each replayed
  registry commit risks the recipes' §4 conflicts (D-010). Either way, no
  seq from 113 to 117 lands.

## (b) Decisions D-001 to D-010 (`docs/decisions/wi-902.toml` in the lane)

| Id | What it decided | Code it covered | Ruling |
|---|---|---|---|
| D-001 (high risk) | Review 001 F1 is fixed by splitting first consumption from replay (`_landed_before`). The landing sweep applies the open-state rule, and a replay accepts on lineage only. A residual gap was recorded. D-006 already superseded it. | `_landed_before` and `row_refusal`'s consumed arm, both deleted in round 5 | **Withdrawn.** Record-at-close removes the distinction between first consumption and replay, because no sweep validates. Its rejected alternative, a durable consumed marker written at the landing sweep, is the nearest shape to the ruling. The ruling instead writes the record at the close and checks it at the commit. Nothing for the owner to confirm. Record it as withdrawn under plan ruling 2. |
| D-002 | `intake.py`'s module-size stamp rises 1719 → 1823 over rounds 1–4. Rounds 5–6 later took it to 1853 and then 1854, each with a reason line. | the `intake.py` row of `tests/test_module_size_ratchet.py` | **Re-made at the rebuild.** The history readers leave `intake.py`, and `_tree_specs`/`_tree_text` may move to where the close and the check share them, so the rise shrinks. The rebuild records its own stamp and reason. It should weigh D-002's alternative again: decompose the Dispositions parsing and sweep wiring out of `intake.py`. Leg 03's handoff raised the same point, and P5 edits `intake.py`'s mint next. **To the owner.** |
| D-003 | Review 002 found that a replay re-pointed a late dependent to the adoption alone. This is fixed, for drafts-only replays too, at `_standing_successors`: dedup suppresses only allocation, and an already-minted draft keeps its place in the successor set. | `_standing_successors`; `_mint`'s standing arm; `_write_mint` and `_supersede_source_refusal` taking the adopted pairs; `_repoint_owed`; `_apply_supersedes` returning its edits; `_mint_message` | **Kept.** It is mint-side and reads no history. Every replay still re-runs the mint, and the full successor set (drafts plus recorded adoptions) still needs it. **To the owner.** |
| D-004 | Dispute 004's DA FIX is built. A standing row needs exactly one title match whose recorded `supersedes` equals the draft's; a mismatch or a duplicate title refuses the mint before any write. | `_standing_successors`'s refusal arm; `_title_identity_refusal` | **Kept.** The ruling is final, and this decision records how it was built. **To the owner.** |
| D-005 (the lane's; not coordinator-2026-10-11 D-005) | Checkpoint 006's returns were answered in the lane: <ul><li>LLR-335 is the adoption decision's one home;</li><li>LLR-153 keeps the mint's arms, cites LLR-335 and gains SR-148;</li><li>TC-360's Evidence drops the two title-identity tests;</li><li>eleven `Implements:` lines were retagged;</li><li>verdict 006's Dispositions heading was moved.</li></ul> | registry cells, and docstring tags in `kitlib/adoption.py`, `intake.py` and `handback.py` | **Re-made.** The one-home structure stands. The symbol list is redone for the rebuilt code: the history readers leave, and the record writer, the record reader and the commit check join (the check under its own new row). The tags follow. Apply sitting 007's advisory 1 this time: a shared function names every row it serves, as `_archive_one_adjudication_row` does. **To the owner.** |
| D-006 | Review 008 F1 went to dispute 009, ruled DB FIX: bind replay to evidence that first consumption accepted, derivable from git. This superseded D-001's residual. F2 was accepted for the checkpoint: LLR-335's blanket claim that no cell of the adopted row changes. | the round-5 landing-tree judgement (`_landing_commit`, `_tree_specs`, `adoption_lineage(rev=…)`) and its regressions | **F1: withdrawn.** Ruling 009's mechanism, re-deriving the landing verdict from git history, is what the owner's ruling 2 replaces. Its invariant holds by construction. A close that refuses writes no record and archives nothing, so no refused adoption reaches a sweep. A recorded adoption is never re-decided. The amended Done-when keeps a regression for each half. Record that ruling 2 supersedes ruling 009's mechanism, since an owner ruling outranks a dispute sitting. **F2: kept.** The shared re-point still rewrites the adopted row's own `needs` edge to the disposed row, so LLR-335 keeps the narrowed clause. **To the owner: the F2 part.** |
| D-007 | Review 010: <ul><li>F1, a shallow-boundary commit taken as the landing, went to dispute 011, ruled DC FIX;</li><li>F2, the lossy history decode, was accepted: one strict-UTF-8 reader at the history-read boundary;</li><li>F3 went to the checkpoint;</li><li>out-of-surface sites were recorded as unfiled topics.</li></ul> | `_landing_commit`'s shallow-boundary test; `_tree_text`'s strict decode; their regressions | **F1: withdrawn.** No landing commit is sought any more. The check reads only its own commit's parent, through the walk's parent reader, which already refuses an unreadable shallow parent by name (TC-313). **F2: kept, moved.** The close and the check read trees from git, so `_tree_text`'s strict decode stays as the one reader. A regression moves to the close: a successor whose spec is not UTF-8 refuses the close. The unfiled topics feed plan item 2's history-reader audit (phase 3). **To the owner: the F2 part.** |
| D-008 | Review 014's MINOR was accepted. IF-294 was added (owner `scripts/kitlib/adoption`, requestor `scripts/intake`, call, CMP-008), with its Contract header. IF-294 joined TC-360's Verifies, and VerifiedBy was dropped. | the IF-294 row; `adoption.py`'s Contract block; TC-360's Verifies | **Kept, amended.** The seam survives. Its Contract loses `work_specs`, and its requestors gain the close's and the check's modules if they call it directly. TC-360 still verifies it. Its owner and requestor cells follow trunk's current schema; component-id owners come with item 11's migration. **To the owner.** |
| D-009 | D-008's planned TC-360 sitting was refused as traced-only, and `test-cases.toml` was re-anchored by act 117. | act 117's snapshot | **Withdrawn,** along with act 117. Its lesson is already in trunk's recipes §3, which cites "(WI-902, act 117)". That act will not reach trunk, so the citation should name the archived lane tip, or drop the act number and keep the rule. Nothing for the owner. |
| D-010 | Review 015's MAJOR was accepted: `parse_disposition_section` harvests only complete fences, so a valid block followed by an unclosed adoption block loses the second successor silently. The lane was left committed under the breaker. | `parse_disposition_section` (fix unbuilt) | **Kept and folded in.** The reshape keeps this parser, and both the close and the sweep read it, so the fix is deliverable 5 of the amended spec. It is widened to drafts, which trunk loses the same way today. "Left committed" is superseded by the rebuild. **To the owner.** |

**Survivors for the owner to confirm or overrule** (carried into the re-cut
lane's `docs/decisions/wi-902.toml`, each entry marked kept, re-made or
withdrawn):
- D-002 (re-made)
- D-003
- D-004
- D-005 (re-made)
- D-006, the F2 part
- D-007, the F2 part (moved)
- D-008 (amended)
- D-010

**Withdrawn and recorded, with nothing to confirm:** D-001, D-006's F1 part,
D-007's F1 part and D-009.

**Owed as new lane decisions at the rebuild:**
- the round count restarting at zero (plan, revision 6–7 clarifications);
- the reviewer stand-ins and the three-reviewer trial (rulings 7 and 4,
  revision 37), naming the model behind each REVIEW-B file.

## (c) Spine rows

**The handoff's ranges are not rows.** Leg 03's handoff gives LLR 327–335,
TC 352–360 and IF 294. Those ranges are the lane's watermark rise. The lane
adds three rows, LLR-335, TC-360 and IF-294, and amends seven trunk rows.

**The gaps are burned numbers.** LLR-327 to LLR-334 and TC-352 to TC-359
hold no row on any branch: `git log --all -S` finds none. They were floors
briefed for other lanes (handoff 2026-10-10b) and stay burned, which is
harmless.

**New ids sit above WI-798's.** WI-798's lane holds LLR-336 and TC-361 to
TC-366, so any id minted here comes above those, at the floor the
coordinator briefs.

| Row | What the lane changed | Act | Under record-at-close | Id |
|---|---|---|---|---|
| SR-148 | AC: "…or names an already-open item that supersedes it as its successor" | 113 | Keep the text and re-sit it. | trunk row |
| LLR-153 | The mint's adoption arms (above); SR-148 added; title-identity symbols | 114 | Keep the text: it cites LLR-335 for acceptance and holds without the history read. The trace cells follow the rebuilt symbols. Re-sit. | trunk row |
| LLR-161 | "drafts a successor, or adopts an already-filed one" | 114 | Keep and re-sit. | trunk row |
| LLR-312 | A consolidation disposition that adopts refuses before its first write | 114 | Keep, since the consolidation refusal stands by the owner's verdict. Re-sit. | trunk row |
| TC-147 | Verifies SR-148; the Method gains the mint's arms; the Evidence names five tests | 114 | Keep the Method. Re-check the Evidence against the rebuilt tests. Re-sit. | trunk row |
| TC-156 | A continuation can draft or adopt | 114 | Keep and re-sit. | trunk row |
| TC-254 | A consolidation verdict that adopts refuses the close | 114 | Keep and re-sit. | trunk row |
| LLR-335 | New. Adoption parsing and successor validation; every sweep judges in the landing tree; shallow-boundary and UTF-8 refusals | 115, 116 | **Amend** to record-at-close. <ul><li>The close validates in its commit's parent tree and writes the record.</li><li>The sweep trusts the record, and refuses a missing, mismatched or malformed one.</li><li>The landing-tree, shallow and replay clauses leave.</li><li>The narrowed no-cell-change clause (D-006 F2) stays.</li></ul> Re-author it in ruling 5's contract voice: the lane's Detail names `parse_block`, `disposed_id` and `row_refusal`, which ruling 5 forbids in a requirement's text. Its `module` and `code_symbol` cells stay filled until item 5's schema lane. It returns to Drafted and is first-approved at the rebuilt checkpoint. | **Kept** (below) |
| TC-360 | New. Verifies LLR-335, including the landing-tree, shallow and UTF-8 replay cases; IF-294 in Verifies | 115, 116, 117 | **Amend.** Cover the close's validation and record, the record surviving completion, the sweep's refusals and the full successor set. The history-reading cases leave. Back to Drafted; first-approved at the rebuilt checkpoint. | **Kept** (below) |
| IF-294 | New, Drafted: the adoption module's call seam | none | **Amend** the Contract and requestors as rebuilt (D-008). | **Kept**: spirit retained, never acted on |
| *(new)* LLR and TC for the commit check | — | — | **Mint** at the rebuild's spine step under SR-148. No existing row has this spirit: it is the record's integrity rule, with the per-commit shape LLR-298 has for ruling sync. If the check's module is a new seam, PROCESS.md §8 owes an IF row too (review 014's precedent). | **Minted** |
| *(maybe)* LLR-181 | — | — | Amend only if the record's strict reader sits in `kitlib.registry` beside `adjudicates_tokens`. | trunk row |
| *(maybe)* the section grammar | — | — | Its one home (LLR-335 as the parser's home, or LLR-153 for drafts) is settled at the spine step. Sitting 007's advisory 1 already asked that the shared parser name both rows. | — |

**Keep-or-mint for LLR-335 and TC-360 (plan revision 26, and the revision 31
cross-reference; ruled keep, D-011):**
- **Spirit retained.** The spirit is one rule and one home for the adoption
  decision, shared by both of its ends. Only where and when the rule runs
  changes.
- **Fewer changes.** Every live user cites the id already and is rebuilt
  anyway, so keeping the ids re-points none of them. Those users are:
  - the `SR-148, LLR-335` tags on the surviving functions;
  - TC-360's `verifies`;
  - IF-294's note;
  - LLR-153's citation.
- **Trunk never saw the old text.** With acts 115 and 116 retired, trunk's
  ledger first approves LLR-335 at the record-at-close text.
- **The old citers are records, not users.** The lane's verdicts 006, 007
  and 013 and its reviews 008–015 cite the old meaning. They are records of
  the texts they judged, each quoting its own text, and they act on nothing.
- **When to mint instead** (passed over). Mint new ids only if those
  historical citations should point at a retired id, rather than at a live
  one whose meaning moved. In that case, re-tag the survivors.

## Notes for the rebuild

- **Coordinator-2026-10-11 D-005.** Recorded overruled on trunk, with the
  owner's 2026-10-14 verdict, in the commit that filed this record. Its
  rejected alternative ("accept the adoption once at the close and trust it
  at the sweep") is now the ruling.
- **The spec at the re-cut.** The lane's own spec edit (SR-148 added to
  `sr_refs`, the history-read sentence) is not ported: the amended trunk
  spec governs.
- **Review numbering.** Reviews 001–015 and adjudications 004, 006, 007, 009,
  011 and 013 stay as the lane's record and land with it. New-shape reviews
  number from 016. Plan item 2's phase-2 measure counts the reshaped rounds
  from there.
- **G's id.** The amended spec's `needs` carries `~WI-913` (G), in the
  batch's soft-edge convention; WI-913 is filed on trunk, so the edge
  resolves.
- **The record's carrier** (ruled, D-012). The amendment makes the record a
  declared `Adopted` column. It follows the precedent of `Adjudicates` and `Digests`:
  "a frontmatter key outside this table is dropped by `parse_spec` at the one
  moment it matters". The alternative is a raw front-matter key read only by
  the close, the check and the sweep. That avoids the column-table change,
  at the cost of the drop risk. The critique may weigh it.
- **What the binding leaves open.** The record binds to the tree the row was
  closed on. A successor cancelled on trunk between the lane's cut and a
  landing that is not rebased, which is the loop's merge-slot path, is not
  re-checked. Dependents re-pointed onto it surface as dead dependencies,
  which `check_trajectory` reports. This is the owner's "validate once"
  trade, now stated in the spec's Trust section. Coordinator landings rebase
  first, so they re-check against current trunk.
