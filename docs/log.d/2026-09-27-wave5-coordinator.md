## 2026-09-27 — The fifth coordinator session: spine-acts batch B, WI-679, then the remaining groups

Resumed from [the wave-4 handoff](../handoff-2026-09-27-wave4-coordinator.md),
after reading it, [its log fragment](2026-09-27-wave4-consolidation.md) and
[its arbitration file](../reviews/2026-09-27-wave4/ARBITRATION.md).
Arbitration for this session:
[../reviews/2026-09-27-wave5/ARBITRATION.md](../reviews/2026-09-27-wave5/ARBITRATION.md).

**Open count at start: 13** (12 queued, 1 deferred), as the handoff states.
fig: `git ls-tree --name-only HEAD docs/work/queued/ docs/work/deferred/ | grep WI- | grep -v WI-000 | wc -l` at 4e141893.

### The smoke tier, confirmed quietly

`python scripts/check_smoke_budget.py --mode enforce` at 4e141893, with no
agent running: 1647 passed / 3 skipped, **34.5 s within the 60 s budget**.

### Spine-acts batch B filed: WI-680 (amendments) and WI-681 (first approvals)

Two rows, because the two verdict grammars differ; one adjudicator session
judges both and takes one act. The populations were computed from the
registries against `docs/archive/last_approved/`, not copied from the
handoff:

- **WI-680, 29 amendments:** exactly the handoff's list (WI-582, WI-656,
  WI-672, WI-638). Seven more approved rows differ in traced cells only, and
  the copy carries them.
- **WI-681, 32 first approvals:** the handoff's twenty, plus every older
  Drafted row the dial now releases (SR-183 to SR-186, LLR-205, LLR-206,
  TC-199 to TC-204, TC-209 to TC-211). At `human_approval_through =
  "DevStg-Boundary"`, `trace.py --approve modified` puts all 29 owing chains
  in its "Waiting for automated adjudication" block, and none on a held rung.
  `adjudicate_brief.compose` fills both briefs in full, and the first-approval
  brief marks all 32 rows as the session's, with none held or out of scope.

Found while computing it: **TC-256 (WI-657) and TC-258 (WI-672) were authored
with no `status` cell**, and they and LLR-261 and LLR-263 had no `phase`.
`trace.py --strict-integrity` reported 0 integrity findings and the approval
brief rendered neither case, so the handoff's two rows would have owed an
approval no brief showed. The coordinator filled `status = "Drafted"` and
`phase = 6` (the parents' phase) in the filing commit. The checker gap is
folded into WI-651 (the snapshot and its readers), not filed as a new row.

**Open count: 15** (14 queued, 1 deferred): WI-680 and WI-681 filed.

### Spine-acts batch B lands: WI-680 and WI-681 in one sitting, one act

One independent Fable adjudicator judged both rows from the kit's own briefs
(`adjudicate_brief.compose`, both filled in full), then took ONE snapshot act
(act ledger seq 4): 25 `Status` flips and `intake.py snapshot --reattests
<30 rows> --approves "<the three spine registries>=WI-681"`.

- **WI-680: `VERDICT: MEANING rows=30`.** 20 MEANING, all blessed; 10
  CLARITY. All 30 are re-anchored. The CLARITY rows are named in
  `--reattests` too: the copy takes whole registries and refuses to absorb
  text that differs from it unnamed.
- **WI-681: `OUTCOME: RETURN rows=32`.** 25 approved: SR-183 to SR-186,
  SR-221, LLR-210, LLR-259 to LLR-261, LLR-263, and 15 test cases. 7
  returned byte-exact: LLR-205, LLR-206, TC-201, TC-203, TC-204, SR-220 and
  LLR-262. The adjudicator caught SR-220's two `shall`s and LLR-262's open
  "such as" list by driving the flipped tree under `trace.py --strict`
  before the act, because those form findings fire only on an Approved row.
- **Folded, not minted:** SR-220's fix goes to WI-679, which realises SR-220.
  The other six rows go to WI-616, the open spine-text sweep, together with
  the adjudicator's non-blocking findings on that surface.

Codex Sol reviewed three rounds (wave-5 rulings 1 to 4). Round one was NOT
YET SOUND. TC-055 had been re-attested over an `expected` that its declared
`max_age = 90` made false, and TC-201 and TC-203 had been approved with
changelog prose in their methods. The act was reverted in the lane.
The coordinator amended TC-055's `expected` and SR-054's `rationale` in
place (SR-054 joined the scope). The adjudicator then refused the
coordinator's first wording, which omitted the checkpoint's no-record
trigger, and its own wording replaced it. The act was re-taken. Round two was
NOT YET SOUND on the verdict files' consistency, and round three was SOUND:
[sol-batchb.md](../reviews/2026-09-27-wave5/sol-batchb.md),
[sol-batchb-fix.md](../reviews/2026-09-27-wave5/sol-batchb-fix.md),
[sol-batchb-fix2.md](../reviews/2026-09-27-wave5/sol-batchb-fix2.md).

Found on the way: the coordinator's hand squash-merges do not run the kit's
merge checkpoint, so the five observation cases `rejudge.due_cases` reports
due (TC-036, TC-055, TC-209, TC-210, TC-211) have no re-judge rows. Folded
into WI-679 (ruling 4).

For the owner: the adjudicator recommends widening SN-025's acceptance to
state SR-220's obligation, and keeping SR-221 derived under SN-012.

**Open count: 13** (12 queued, 1 deferred): WI-680 and WI-681 closed.

Commit bar at batch B: `check_trajectory --strict` clean, `trace
--strict-integrity` 0 (drafts 7), approve-modified current, `gen_open_items`
current, `check_docs --stale` 0 broken, smoke 1647 passed / 3 skipped.
**Seconds FAILED: 154.7 s and 155.6 s against the 60 s budget**, recorded and
not re-stamped. No agent or test of this session was running, but the box
was at 88% CPU from desktop applications. As a control, the same tier at the
parent commit 1ea526ac, in a fresh worktree at the same minute, took 197.7 s;
it took 42.1 s there two hours earlier. The change moves specs and registry
cells and adds no test.

### WI-679 lands: consolidation through the kit's own census, judgement and close

One builder, three Codex Sol rounds (wave-5 rulings 5 to 9): NOT YET SOUND
at f646eff0 (a silent Done-when skip, guard 3 keyed on scope rather than an
enacted outcome, an unenforced ordering argument, thin coverage), NOT YET
SOUND at 1b783955 (a nested absorption dropped from `{prior}`), SOUND at
fb9ca52a: [sol-wi679.md](../reviews/2026-09-27-wave5/sol-wi679.md),
[sol-wi679-fix.md](../reviews/2026-09-27-wave5/sol-wi679-fix.md),
[sol-wi679-fix2.md](../reviews/2026-09-27-wave5/sol-wi679-fix2.md).

What it decided (the Deliverable has the detail):
- **Guard 1 narrows.** A queued judgement blocks the census only when it
  names a candidate row or would run first in the scheduler's own order, so
  an unrelated open adjudication no longer freezes consolidation forever.
  Judgement rows and the `-000` example are no longer candidates.
- **No surface signal.** At 8aae3af3 the old signals joined 1 of the 11 hand
  groups (12 of 66 pairs). With the population fix, the candidate set holds
  34 of the 40 grouped ids, and 6 groups whole. A component signal found 0 of
  66, and a module-by-spec signal bought one group for about 200 noise lines.
  fig: `measure_census.py` and `measure_surface.py` over a detached worktree
  at 8aae3af3 (the builder's scratch scripts, recorded in its report).
- **Guard 3 reads only an enacted consolidation**, so the wave-4 hand hosts
  are ordinary rows again, and `{prior}` labels each absorption "judged by"
  or "by hand".
- **The hand-merge gap has a command:** `intake.py sweep --merged`, run after
  each hand squash-merge, mints what the merge slot would have.

LLR-210 and TC-208 are amended in place (status Approved); SR-220 (one
`shall` now), LLR-264, LLR-265, TC-260, TC-261, IF-243 and IF-244 are
Drafted. Those rows are minted for adjudication by the sweep below, not
hand-filed into a batch. **Open count: 12** (11 queued, 1 deferred).

Commit bar at WI-679: `check_trajectory --strict` clean, `trace
--strict-integrity` 0 (drafts 11), approve-modified current, `gen_open_items`
current, `check_docs --stale` 0 broken, smoke 1661 passed / 3 skipped,
**seconds 28.2 s within 60 s** on a quiet box. Touched modules, slow ones
included, plus both ratchets (test_consolidate, test_consolidate_close,
test_intake, test_rejudge, test_adjudicate_brief, test_frame_context,
test_module_size_ratchet, test_complexity_ratchet, test_resync_pack,
test_dogfood_sync, test_rule_sync, test_schedule), run by the coordinator:
443 passed / 2 skipped. `check_complexity --mode enforce`: OK, 204 rows,
unchanged. Trunk before this squash: 464dc7ac.

### WI-679's end-to-end run: the kit's sweep, census, judgement and close on the live queue

**Open count before: 12** (11 queued, 1 deferred), at 77fb0936.

1. **The post-merge sweep**, `intake.py sweep --before 464dc7ac --after
   77fb0936 --branch build/wi-679 --merged WI-679`, minted seven rows
   (21d8f49d). WI-682 is the amendment adjudication of LLR-210 and TC-208.
   WI-683 is the first approval of SR-220, LLR-264, LLR-265, TC-260 and
   TC-261. WI-684 to WI-688 re-judge TC-036, TC-055, TC-209, TC-210 and
   TC-211, the five observation cases the hand merges had never checkpointed.
   It said by name that WI-679's Done-when check could not run (no trunk
   claim of a hand-cut lane). **Open: 19.**
2. **The census**, `intake.py consolidate --dry-run` and then without the
   flag, did not refuse, although seven adjudications were queued: guard 1's
   narrowing working. It proposed 7 candidates (WI-615, WI-616, WI-620,
   WI-651, WI-655, WI-657, WI-667), digests `af589a4f5319|edd7832b0dd6`, on
   ten overlap lines (a shared spec, a shared plan, and `trace.py`,
   `acceptance_record.py` and `gen_skills_index.py` touched by several). It
   minted WI-689 (e26e22aa). **Open: 20.**
3. **The claim was refused** by the owner's `docs/work/pause` (since
   2026-09-04). Wave-5 ruling 10 records how the rest ran. Every step but the
   claim and the merge slot went through the kit; the pause stands, and is
   put to the owner.
4. **The judgement.** An independent Fable adjudicator judged WI-689 from the
   kit's consolidate brief: `OUTCOME: QUEUE-WITH-EDGE needs=WI-655 absorbs=-`,
   with the block `edges = ["WI-655 needs WI-616"]` (d60e549d). WI-616's
   absolutes sweep produces the open-world-absolute list "for C2", and
   WI-655 is C2 and rewrites the same SRs' assumption and boundary cells. So
   C2 follows. Every other pair was judged separate work that merely shares
   files, so nothing was absorbed. Codex Sol found the verdict SOUND and re-ran
   the close's refusal logic: the digest was exact, all seven were queued, and
   the counters were reconciled ([sol-wi689.md](../reviews/2026-09-27-wave5/sol-wi689.md)).
5. **The close.** `handback._consolidation_close`, with `close_refusal` over
   the trunk registry, enacted it: "outcome queue-with-edge (0 absorbed, 1
   edge(s), 0 returned)". WI-655's `needs` became `["WI-643", "WI-616"]`, and
   WI-689 moved to `docs/work/complete/` (0fbd91fa on the lane, squashed
   here).

The verdict's two side findings were folded, not filed. WI-667's gate has no
`needs` target, which is noted in its Context. WI-657's stale "do not run
the two lanes at once" sentence was replaced. **Open count after: 19**
(18 queued, 1 deferred): the kit's machinery closed its own judgement, and
the seven rows it minted are real owed work. None of them is a consolidation.

### The remaining groups, first wave: WI-620, WI-651, WI-616, WI-657 (part 4)

Four builders at once, each in its own worktree cut from 0ded5c77, with
disjoint surfaces: WI-615 waits on WI-616 (both edit the spine-authoring
skill), and WI-655 waits on WI-616 by the WI-689 verdict. The spine
adjudications WI-682 and WI-683 wait for the adjudication rows this wave's
merges mint, so that they are judged together in one sitting and one act.

### WI-616 lands: absolutes, the check then the sweep, with batch B's returns

One builder, three Codex Sol rounds (wave-5 rulings 11 to 18, and 23):
[sol-wi616.md](../reviews/2026-09-27-wave5/sol-wi616.md),
[sol-wi616-fix.md](../reviews/2026-09-27-wave5/sol-wi616-fix.md),
[sol-wi616-fix2.md](../reviews/2026-09-27-wave5/sol-wi616-fix2.md).
The absolutes check (`absolute_terms.py`) scans needs, SRs and LLRs,
warn-only. The sweep record, `docs/plans/2026-09-28-absolutes-sweep.md`,
bounded SN-003, SN-008 and SN-009, moved SN-025's mechanisms down to SR-148,
and needed no SR rewrite. Batch B's six returned rows are re-authored and
still Drafted. LLR-203 and LLR-233 are amended in place.
fig: `python project-trajectory/scripts/trace.py --root .` console line, "278 absolute-term advisories (SN 30, SR 98, LLR 150)", at the builder's tip 3241f337.

The Sol rounds found, among others: approved LLR-203 made false by the new
SR-163 design rows (amendment granted, ruling 11); a blanket Inspection
exemption that would hide a real two-methods row (made subject-aware,
rulings 13 and 18); three sweep rows misclassified; and a vacuous TC-276. For
the owner: the four SN amendments go to your brief, once WI-651 puts needs in
the drift comparison. SN-025's acceptance lost its "never from prose, never
predefined tracks" wording (SR-148 carries it), which bears on the batch-B
adjudicator's advice to widen SN-025 for SR-220. **Open count: 18**
(17 queued, 1 deferred).

The merge composed two reds the builder's modules could not see. First,
`trace.analyze` was 242 lines against its 240-line composer budget
(tests/test_trace_coherence.py), from WI-616's four-line comment. The
coordinator trimmed the comment to two lines; nothing was re-stamped.
Second, the smoke membership was 1697 against its 1690 ceiling, from real
in-process growth in WI-679 and WI-616. It was re-stamped 1690 -> 1765 in
`docs/stack.ini` with its reason; the 60 s budget stands. Wave-5 ruling 23's
docstring correction is in the same commit.

Commit bar at WI-616: `check_trajectory --strict` clean, `trace
--strict-integrity` 0 (drafts 18), approve-modified current, `gen_open_items`
current, `check_docs --stale` 0 broken, smoke 1694 passed / 3 skipped,
**seconds 28.5 s within 60 s**. The touched slow modules plus both ratchets
(test_trace_rules, test_trace_golden, test_mapping_purpose_cli,
test_bootstrap, test_trace_briefs, test_check_complexity_cli,
test_baseline_drift, test_module_size_ratchet, test_complexity_ratchet,
test_resync_pack, test_frame_context, test_rule_sync, test_assumption_rules),
run by the coordinator: 411 passed. `check_complexity --mode enforce`: OK,
204 rows. Trunk before this squash: 0ded5c77.

WI-616's post-merge sweep (`intake.py sweep --merged WI-616`) minted three
rows. WI-690 is the amendment adjudication of LLR-203 and LLR-233; WI-691 is
the first approval of the re-authored and new Drafted rows; WI-692 is a
sampled spot check of WI-616's clean close. **Open count: 21** (20 queued,
1 deferred).

### WI-657 part 4 lands; the row stays open for one owner question

WI-624's research write-up, `docs/plans/2026-09-28-duplicated-stage-detection.md`,
went through two Codex Sol rounds
([sol-wi657.md](../reviews/2026-09-27-wave5/sol-wi657.md),
[sol-wi657-fix.md](../reviews/2026-09-27-wave5/sol-wi657-fix.md)); the
coordinator corrected the last phrase at integration (ruling 23). Its ground
truth is 39 instances read from 13 consolidation commits' own diffs. No
function-level method both finds shared stages and stays quiet: call
sequences found 11 of 12 stages at 4,988 to 21,300 pairs, and none of 36
sampled findings was an extractable stage. It recommends adopting nothing,
and offers a warn-only near-miss report (5 of 6 pairs at Jaccard 0.7 or
more were real duplicates the census misses).

Part 2 stopped correctly. The stage-gated sensor steps (`complexity`,
`dupes-census`, and now `smoke` and `readability`) never select at the
derived stage, which has not read DevStg-Impl since 2026-08-20. Moving their
rung contradicts OI-68 Q3's ruled "runs at DevStg-Impl", so it is put to the
owner, and WI-657 stays open for it with a Done-when bullet. The live
duplicates the research sampled are recorded in WI-545's Context for the
owner's burn-down call, not as obligations. **Open count unchanged at 21.**

Commit bar at WI-657 part 4: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1694 passed / 3 skipped, seconds 49.4 s
within 60 s (two builder lanes on the box). The change is documents only.

### WI-651 lands: the snapshot and its readers, the need tier funded (with WI-666 and WI-671)

One builder, five commits, four Codex Sol rounds (wave-5 rulings 17, 19 to
22, 24 and 25):
[sol-wi651.md](../reviews/2026-09-27-wave5/sol-wi651.md),
[sol-wi651-fix.md](../reviews/2026-09-27-wave5/sol-wi651-fix.md),
[sol-wi651-fix2.md](../reviews/2026-09-27-wave5/sol-wi651-fix2.md).
The builder stopped twice on approved rows written before OI-91's ruling:
LLR-245 and TC-240 said the needs file "stays outside" the snapshot tiers,
and SR-178 said needs carry "no status cell". The coordinator granted each
amendment the ruling called for, rather than let a row that realises an
owner's ruling stop short of it. Sol's rounds found a Markdown needs file
never compared, two design rows each holding two decisions (split, with
LLR-277, LLR-278 and TC-278), coverage gaps, and two stale cells. The
coordinator ruled for the builder on one point: the pre-existing,
deliberate whole-ledger arm for an act that copies nothing (ruling 25).

The merge conflicted in five files. `docs/id-watermark` took trunk's copy and
was re-bumped. The RESYNC entries kept both, and only WI-651's was
re-anchored to `[since e520b6e6]`. `trace.py`'s size ratchet was
re-measured on the merged tree, 3798 with both reasons. The two registries
exposed a trap. Git's line merge aligned the identical `status`/`component`/
`phase` tail of WI-616's LLR-274 with WI-651's LLR-272, so keeping both hunks
would have stripped LLR-274's tail. They were merged table by table from the
merge base instead (`toml_merge3.py` in the coordinator's scratchpad), and
every row's tail was checked.

For the owner: needs are now in the drift comparison, so WI-616's
amendments to SN-003, SN-008, SN-009 and SN-025 are on your brief. Any act
that copies the needs registry is refused until you re-attest them (`intake.py
snapshot --reattests SN-003,SN-008,SN-009,SN-025` in your own reviewed commit);
acts that copy only the SR, LLR and TC registries are not blocked.
**Open count: 20** (19 queued, 1 deferred).

One composition red at the merge was the handoff's known trap: the line-number
pin in `tests/test_generated_newlines.py`. The one non-literal write site in
`gen_open_items.py` moved from 1383 to 1392, because WI-651's view lists each
registry's copy stamp above it; the site itself is unchanged. The pin moved
with its reason.

Commit bar at WI-651: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1697 passed / 3 skipped, seconds 43.3 s
within 60 s (three builder lanes on the box). The touched slow modules plus
both ratchets (test_snapshot_readers, test_baseline_snapshot,
test_accepted_risk, test_trace, test_trace_briefs, test_trajectory_arch,
test_intake, test_integrate, test_acceptance_record,
test_module_size_ratchet, test_complexity_ratchet, test_resync_pack,
test_frame_context, test_rule_sync, test_dogfood_sync, test_derive_stage),
run by the coordinator: 636 passed / 2 skipped. `check_complexity --mode
enforce`: OK, 204 rows. Trunk before this squash: e520b6e6.

WI-651's post-merge sweep minted two rows: WI-693 (amendments of LLR-158,
LLR-173 and the other amended rows) and WI-694 (the first approval of
WI-651's new Drafted rows). **Open count: 22.**

### WI-655 lands: C2, the assumption and surrogate rows, and every SR's and boundary interface's bridging

One builder, three Codex Sol rounds (wave-5 rulings 26 to 30 and 32):
[sol-wi655.md](../reviews/2026-09-27-wave5/sol-wi655.md),
[sol-wi655-fix.md](../reviews/2026-09-27-wave5/sol-wi655-fix.md).
DA-001 to DA-015 and SUR-001 to SUR-003 are Drafted, and every SR carries
`da_refs` or `coincident` (78 coincident). 72 `boundary_refs` moved off
B-05, each listing every crossing its approved text names. All 43 boundary
interfaces carry `bridged_by` or `coincident`.
The bridging report reads 0, from 43 with the DAs and no interface cells.
fig: `python project-trajectory/scripts/trace.py --root .`, lines containing "realizes boundary crossing", at the landing tree.
Sol's rounds moved DA-005 to its real crossing and took SR-157 off DA-001.
They restored B-01 wherever an SR governs a write. They re-authored DA-011
to the D5 premise, with TC-279's inputs declared so a change stales it. They
gave IF-030 its own waiver and made the census test render the brief.
The coordinator set SR-174's crossing to B-01 at integration (ruling 32).
Remaining, named: three frame-spanning SRs (SR-139, SR-146, SR-148), B-11
unnamed, SN-040's gap, the 114 "no Form" advisories (form is outside this
row's grant; C3 or C4 takes it), and SN-007's missing derived obligation (for
the owner). The merge conflicted in `docs/id-watermark` (trunk's, re-bumped)
and `docs/test/test-cases.toml` (merged table by table). **Open count: 21.**

Commit bar at WI-655: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1697 passed / 3 skipped, seconds 34.6 s
within 60 s. The touched modules plus both ratchets (test_trace_briefs,
test_dogfood_sync, test_assumption_rules, test_frame_context, test_rule_sync,
test_cell_classes, test_id_watermark, test_external_frame, test_frame_rules,
test_frame_system, test_trace_interfaces, test_assumptions_registry,
test_derive_stage, test_module_size_ratchet, test_complexity_ratchet), run by
the coordinator: 507 passed / 1 skipped. `check_complexity --mode enforce`:
OK, 204 rows. Trunk before this squash: 47198652.

WI-655's post-merge sweep minted three rows: WI-695 (the amendment
adjudication of the SR cells C2 wrote), WI-696 (the first approval of the DA,
SUR and TC-279 rows) and WI-697 (TC-279's re-judge, owed because no result
is recorded). **Open count: 24.**

### The five overdue re-judges: WI-684 to WI-688

An independent Fable adjudicator judged the five observation cases the hand
merges had never checkpointed, one commit per row. Codex Sol cross-reviewed
them ([sol-rejudge.md](../reviews/2026-09-27-wave5/sol-rejudge.md); ruling 31).

- **TC-209 and TC-210: RECORDED pass** (Sol: earned).
- **TC-036 and TC-211: NEEDS-JUDGEMENT** (Sol: honest). TC-036 owes a
  person's re-sync of a stamped adoption, and TC-211 owes the SR-161 record
  producer. Their rows, WI-684 and WI-688, stay open with the owed act in
  their Context. The checkpoint suppresses a second draft only while a row
  is open, so closing them would re-mint them at every merge.
- **TC-055: RECORDED pass, by a cross-family judge.** The first session
  was the rendering code's own model family, which TC-055's Method excludes,
  so Sol found its pass unearned. Its record was withdrawn in the lane. Codex
  Sol then critiqued the same 30-shot matrix
  ([sol-tc055.md](../reviews/2026-09-27-wave5/sol-tc055.md)). Its one
  finding, T4 labels too small at 390 px, came from downsampling a 24,076 px
  screenshot to one image. Re-judged on 58 native-resolution tiles
  ([sol-tc055-t4.md](../reviews/2026-09-27-wave5/sol-tc055-t4.md)), T4
  passes, so the verdict is APPROVE on T2, T4, T5 and T8. The coordinator
  recorded it through the kit's writer, naming the judge. Lesson for the
  next critique: attach tall screenshots as native tiles, never whole.

Folded, not filed: TC-036's `inputs` omit `RESYNC_PACK.md` (into WI-684).
`inspection-procedures.md` hand-restates results inside a declared input,
beside the observation writer (into WI-688). The adjudicator's non-blocking
dashboard observation (the What drill's scroll card shows 9 of 31 SN blocks
with no visible affordance under overlay scrollbars) is recorded here for
the owner. **Open count: 21** (20 queued, 1 deferred).

Commit bar at the re-judges: `check_trajectory --strict` clean, `trace
--strict-integrity` 0 (three observation records accepted), approve-modified
current, `gen_open_items` current, `check_docs --stale` 0 broken (one link
to the withdrawn record, in Sol's cross-review, made plain text), smoke 1697
passed / 3 skipped, seconds 29.7 s within 60 s. No code changed. Trunk before
this squash: e5b25bd6.

The re-judges' own sweep minted three more re-judge rows at once: WI-698
(TC-055), WI-699 (TC-209) and WI-700 (TC-210), each "declared inputs changed".
The records were judged at fe96ec69, and WI-651 and WI-655 landed before them.
What moved was SR-054's `boundary_refs` and `da_refs`, SR-184's `da_refs`,
SR-185's `coincident`, and a new TC-279 section in
`docs/test/inspection-procedures.md`. The rubric and the rendering code did
not move. So the machinery is right that the records are stale, but three
things about the observation surface cost a re-judge here, and they are
recorded for the owner:
- a registry-id input digests the row's traced pointer cells, which "re-open
  no attestation" everywhere else;
- a whole-file input stales every case declaring it, whichever section
  changed;
- the re-judge brief lists every declared input rather than the ones that
  changed, so a judge must diff to find out.
Coordinator lesson: judge observation re-judges on the latest trunk, and land
them before lanes that touch their inputs. **Open count: 24.**

### The second re-judges: WI-698 to WI-700, and TC-055's first qualifying result

On trunk at 8bebd4cf, a fresh Fable adjudicator re-judged TC-209 and TC-210
(RECORDED pass, both: the input changes touched neither procedure nor
acceptance). For TC-055 it only rendered the declared matrix at HEAD and cut
all 30 shots into 180 unscaled native-resolution tiles, because it is the
same family as the rendering code's authors. Codex Sol judged it
cross-family, one width per pass
([390](../reviews/2026-09-27-wave5/sol-tc055b-390.md),
[1280](../reviews/2026-09-27-wave5/sol-tc055b-1280.md),
[1680](../reviews/2026-09-27-wave5/sol-tc055b-1680.md)). 1280 px approves.
At 1680 px the default selection fade leaves the When roadmap's non-selected
phase cards pale with white text (T5). At 390 px the light-theme descend
arrows wash into pastel blocks (T5), and diagram labels are small (T4).
The coordinator looked at the 1680 px tile, not as judge but to rule out a
capture state: the default render auto-selects a card, so the fade is what a
reader first sees. **TC-055 records FAIL.** The same judge's focused T4-at-390
pass at fe96ec69 is recorded as a disagreement. So the pass recorded an hour
earlier from downsampled whole images was the judge's miss, not the
dashboard's health. A failing result is kept.

The dashboard work those findings owe had no open row, so **WI-701 is
filed**, together with the What drill's scroll-affordance observation. Its
Done-when ends in a cross-family re-judge that records a pass.
**Open count: 22** (21 queued, 1 deferred): WI-698 to WI-700 closed, WI-701
filed.

Commit bar at the second re-judges: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1697 passed / 3 skipped, seconds 27.4 s
within 60 s. No code changed. Trunk before this squash: 8bebd4cf.

### WI-615 lands: the doctrine sitting, seven of eight parts, and OI-95 for the eighth

One builder, ten commits, three Codex Sol rounds (wave-5 rulings 33 to 36):
[sol-wi615.md](../reviews/2026-09-27-wave5/sol-wi615.md),
[sol-wi615-fix.md](../reviews/2026-09-27-wave5/sol-wi615-fix.md),
[sol-wi615-fix2.md](../reviews/2026-09-27-wave5/sol-wi615-fix2.md).
The parts built:
- "When a guard is owed" and the fan-out rules, stated once in PROCESS.md
  and linked from the briefs;
- the reviewer brief's spec of record;
- the adopter-true worker brief;
- the children-coverage rule;
- the knowledge-pack edits, among them a `subagent-brief` skill and
  multi-file skills (the B5 defect fixed);
- the terminology pass, *system specification* and *design expectation*
  in prose, labels and the report table;
- PROCESS.md §4's absolutes rule made matrix-wide.

Sol's first round found three shipped behaviours no row claimed: per-model
guardrail payloads, the skills-index description floor, and whole-directory
materialization. They are now traced, and the two with no honest approved
parent became labelled derived requirements, SR-223 and SR-224. The
second round moved the floor off SR-112, which it had been hung on
"by ruling, not by fit", and gave `--check` its own exit-code interface row.
Byte budgets: AGENTS.template.md 9,996 of 10,000, PROCESS.md +2,208 and
PROCESS_OPTIONS.md +619, both watched.

Part 7 (WI-610) asks where the Review-Verdict trailer rides, which only the
owner can decide, so it becomes **OI-95** (pending, typed brief,
recommendation (a): amend OI-76's wording to the code). It is not built. The
merge conflicted in the watermark (trunk's, re-bumped), three registries
(merged table by table) and RESYNC_PACK (both kept; only WI-615's three
entries re-anchored to `[since 47f8b573]`, because WI-651's entry already
reads `[since e520b6e6]`). **Open count: 21** (20 queued, 1 deferred).

The merge's slow modules found a red that WI-615 did not cause.
`tests/test_traj_render.py`'s theme lock (TC-122: one `prefers-color-scheme`
block, at `:root`) failed on the shipped dashboard. WI-633's per-need style
had carried its own dark-mode `@media` block scoped to `.detail`, which is
emitted only when assumption rows exist. WI-655 wrote the first real DA
rows, so trunk has been red on this slow test since WI-655 landed; that
merge did not run `test_traj_render`. The coordinator made the fix at the
root: a `--danger` token in both theme blocks under `:root`, read by the
per-need style. The page golden `tests/golden/dashboard-no-assumptions.html`
was regenerated for that intended change (the two token lines). Lesson: a
lane that writes the first rows of a registry changes what every emitter
renders, so run the dashboard's slow modules at its merge.

Commit bar at WI-615: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1708 passed / 3 skipped, seconds 26.6 s
within 60 s. The touched slow modules plus both ratchets (test_prompts,
test_agent_loop, test_skills_sync, test_bootstrap, test_trace_golden,
test_traj_render, test_traj_views, test_gen_okf, test_gen_trajectory,
test_mapping_purpose, test_dogfood_sync, test_rule_sync, test_skills_index,
test_check_docs, test_trajectory_arch, test_module_size_ratchet,
test_complexity_ratchet, test_resync_pack, test_frame_context,
test_skill_materialization, test_guardrails_payload), run by the
coordinator: 595 passed / 2 skipped. `check_complexity --mode enforce`: OK,
204 rows. Trunk before this squash: 47f8b573.

### WI-701 lands: the dashboard's T5 contrast fixed, T4 at 390 px measured within its floor

One builder, one Codex Sol round, SOUND at 86ea26c8
([sol-wi701.md](../reviews/2026-09-27-wave5/sol-wi701.md)). The two T5
findings had one cause. Every node de-emphasis faded by opacity, and white
labels on phase fills fell to 1.28 to 2.0:1. All four de-emphasis rules now
use one `:root` token, `--mute: saturate(.2)`, pinned by new Drafted
LLR-285 and TC-296, red first. T4 at 390 px sits exactly on TC-121's scale
floor (labels at 6.2 and 5.27 px), so nothing changed. For the owner:
SHRINK_FLOOR looks miscalibrated for today's node type, and moving it is an
LLR-116 and TC-121 amendment. The What drill's overflow card fades its
bottom edge. **Open count: 21** (20 queued, 1 deferred).

Commit bar at WI-701: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1708 passed / 3 skipped, seconds 30.9 s
within 60 s. The dashboard's slow modules plus both ratchets
(test_traj_render, test_traj_render_sweeps, test_traj_views,
test_traj_panels, test_gen_trajectory, test_traj_graph, test_gen_open_items,
test_dogfood_sync, test_rule_sync, test_module_size_ratchet,
test_complexity_ratchet, test_resync_pack), run by the coordinator: 306
passed / 1 skipped (20 min 52 s, with three agents on the box).
`check_complexity --mode enforce`: OK, 204 rows. The dashboard was
regenerated at the merge, which clears the builder's one stale-artifact red.
WI-703 (TC-055's re-judge) now waits on WI-701 by a `needs` edge. Trunk
before this squash: 1d84d77c.

WI-701's sweep minted WI-704 (the first approval of LLR-285 and TC-296).

### WI-557 lands: the delegated-decisions record under the decision_recording dial

One builder, two Codex Sol rounds (wave-5 rulings 39 to 43):
[sol-wi557.md](../reviews/2026-09-27-wave5/sol-wi557.md),
[sol-wi557-fix.md](../reviews/2026-09-27-wave5/sol-wi557-fix.md).
It is the owner's OI-74 and OI-75 built: a per-run TOML record, a three-value
dial (this repository sets "record"), a merge-ladder refusal naming the
missing record as a hold for a person, and a PROCESS_OPTIONS layer. Sol's
first round removed the builder's partial-close exemption, because the
owner's text says every delegated run. It also judged the dial's
configuration before the record, split the file and call seams, and made
SR-225 a one-`shall` labelled derived requirement. The coordinator ruled for
the builder on the supervisor-resume clause, whose surface is retired.
**Open count: 22** (21 queued, 1 deferred).

The merge composed one red: the smoke membership, 1801 against 1765, from
real in-memory growth (WI-557's 89 format and dial cases, WI-701's contrast
sweep, WI-615's four regressions moved to fast modules). It was re-stamped
1765 -> 1875 in `docs/stack.ini` with its reason; the 60 s budget stands.
The merge also conflicted in the watermark (trunk's, re-bumped), two
registries (merged table by table) and RESYNC (both kept; WI-557's entry
re-anchored to `[since 4b7f6dae]`).

Commit bar at WI-557: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1798 passed / 3 skipped, seconds 51.4 s
within 60 s (two agents on the box). The touched slow modules plus both
ratchets (test_decision_record, test_decision_record_merge,
test_integrate_admission, test_agent_loop, test_bootstrap, test_dogfood_sync,
test_rule_sync, test_module_size_ratchet, test_complexity_ratchet,
test_process_config, test_handback, test_verdict_record,
test_approval_level, test_resync_pack, test_frame_context,
test_derive_stage), run by the coordinator: 676 passed / 2 skipped.
`check_complexity --mode enforce`: OK, 204 rows. Trunk before this squash:
4b7f6dae.

WI-557's sweep minted WI-705 (the first approval of WI-557's Drafted rows).

### Spine-acts batch C lands: nine rows, one narrowed act

One independent Fable adjudicator judged the nine adjudication rows the
kit's post-merge sweeps had minted. There were four amendment rows (WI-682,
WI-690, WI-693, WI-695) and five first-approval rows (WI-683, WI-691,
WI-694, WI-696, WI-702). Codex Sol cross-reviewed over four rounds
([sol-batchc.md](../reviews/2026-09-27-wave5/sol-batchc.md),
[sol-batchc-fix.md](../reviews/2026-09-27-wave5/sol-batchc-fix.md),
[sol-batchc-fix2.md](../reviews/2026-09-27-wave5/sol-batchc-fix2.md);
wave-5 rulings 37, 38, 44, 45).

- The first act refused on LLR-173, whose rewritten detail recorded its own
  arming history. The coordinator amended that one sentence to the
  adjudicator's standing wording, after checking it against the code.
- Sol then found the first full act unsound. Four of twelve sampled
  WI-695 `coincident` waivers restated the need to make coincidence true.
  SR-224's deriving hat cannot reach SN-005, and TC-290 does not test
  SR-223's last clause. **The act was narrowed to the LLR and TC
  registries.** The SR registry is not copied, so SR-220, SR-223 and SR-224
  stay Drafted, and WI-695's cells and SR-178 stay drifted and visible.
- The re-sitting applied the test "does the requirement's effect alone
  deliver the outcome its cited need states?" to every waiver: 66 blessed,
  13 withheld. It returned SR-223, SR-224, TC-290 and TC-272.
- **Act seq 5 approved 31 LLR and TC rows and re-attested 9 amendment
  rows.** WI-701 and WI-557 had added Drafted rows to the LLR and TC
  registries since the lane was cut, so the act was replayed on trunk with
  the adjudicator's exact command. The new Drafted rows ride along as
  Drafted, and both copies equal their live files.
- **Folded, not filed:** batch C's three follow-up drafts (the thirteen
  waivers; SR-223 with TC-290 and SR-224; TC-272's tier) are one draft in
  WI-695's Dispositions, so the sweep mints one row. For the owner: SR-224
  waits on SN-005's applicability tags, which are a need, so yours.
- Derived-requirement advice for the owner: widen SN-025 for SR-220; keep
  SR-223 derived; tag SN-005 `process` for SR-224.

**Open count: 14** (13 queued, 1 deferred): nine adjudication rows closed.

Commit bar at batch C: `check_trajectory --strict` clean, `trace
--strict-integrity` 0 (the SR copy's last writer stays 464dc7ac, where copy
and live were equal), approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1798 passed / 3 skipped, seconds 28.5 s
within 60 s. Trunk before this squash: e1b7cf9f.

Batch C's sweep minted two rows. WI-707 is the one folded follow-up. WI-706,
an amendment adjudication of LLR-173, is redundant: LLR-173 was judged and
re-attested inside the same squash. The sweep's amendment trigger
(`staged_spine_amendments`) does not check whether the merged range also
re-attests the row, so it mints for an amendment the range already
settled. That happens only when an amendment and its act share one merge,
as the coordinator's hand path made them here. WI-706 is closed with that
stated, and the gap is recorded for the owner. **Open count: 15** (14 queued,
1 deferred).

### WI-703: TC-055 re-judged on the fixed dashboard, and OI-96 for the shrink floor

After WI-701 landed, the coordinator rendered the matrix at 4b7f6dae and cut
180 native-resolution tiles, without judging them. Codex Sol judged them
cross-family, one width per pass
([390](../reviews/2026-09-27-wave5/sol-tc055c-390.md),
[1280](../reviews/2026-09-27-wave5/sol-tc055c-1280.md),
[1680](../reviews/2026-09-27-wave5/sol-tc055c-1680.md)). 1680 px approves,
and WI-701's T5 fix holds at 390 and 1680 px. Two findings remain:
- T4 at 390 px, on labels exactly at the approved TC-121 shrink floor;
- T5 at 1280 px, on the far-right card. The coordinator's look at the tile
  suggests the overflow edge fade rather than the de-emphasis. It is
  recorded as the judge ruled.
**TC-055 records FAIL again**, and the fail is kept. The floor is approved
design (LLR-116, TC-121), so the question is the owner's: **OI-96**
(pending, typed brief, recommendation (a): a rendered-pixel minimum).
Across three cross-family passes, the judge's per-width calls moved
between runs on the same rendering code. A single Critique pass is a noisy
instrument, and the log records each.

Commit bar at WI-703: all green; smoke 1798 passed / 3 skipped, seconds 29.2 s. Trunk before this
squash: 312b2033.

### WI-692: the sampled spot check of WI-616's clean close — CONFIRMED

An independent Fable adjudicator checked WI-616's close against its nine
Done-when clauses. It ran the cited tests and re-derived the sweep's 48 + 166
absolutes exactly from the shipped check at 0ded5c77. Result: CONFIRMED, no
successor. Codex Sol cross-reviewed it SOUND and reproduced the re-derivation
([sol-wi692.md](../reviews/2026-09-27-wave5/sol-wi692.md)). Recorded for the
owner, not filed:
- the check keeps reporting the absolutes the sweep judged closed (121
  cells hold only closed or non-promise classes; Sol corrected the
  adjudicator's 128, which counted seven C2 premises). Whether a judged row
  should carry its classification is a design question;
- the LLR tier was never in the sweep's scope;
- `docs/registry-machinery-reference.md` does not yet mention the
  absolute-term rule or its waiver marker.

Commit bar at WI-692: documents only, all green; smoke 1798 passed / 3 skipped, seconds 32.8 s. Trunk before this
squash: 32687d47. **Open count: 13** (12 queued, 1 deferred).

### WI-707 lands: batch C's returns, and OI-97 for joint delivery

One builder, three Codex Sol rounds (wave-5 rulings 46 and 47):
[sol-wi707.md](../reviews/2026-09-27-wave5/sol-wi707.md),
[sol-wi707-fix.md](../reviews/2026-09-27-wave5/sol-wi707-fix.md).
Six of the thirteen waivers were re-worded or re-parented until they hold
for every need they cite. Seven cannot hold: each row contributes one part
of a need that several requirements deliver together, and approved SR-193
defines `coincident` as "alone delivers its needs". Those seven, and the
derived SR-223 and SR-225, drop the waiver and stay unclassified, SR-193's
honest third state. Nothing was forced into an invented DA. The tier has no
class for joint delivery, so C2's aim that every SR be classified cannot be
met honestly yet: **OI-97** (pending, typed brief, recommendation (a), a
declared joint-delivery class). SR-223's last clause is pinned by TC-290's
new arm and narrowed to what it observes. TC-272 was split into TC-297.
SR-224 still waits on the owner's SN-005 tags. **Open count: 12**
(11 queued, 1 deferred).

Commit bar at WI-707: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1799 passed / 3 skipped, seconds 42.6 s
within 60 s. Affected modules and both ratchets (test_guardrails_payload,
test_snapshot_readers, test_assumption_rules, test_trace_briefs,
test_frame_rules, test_dogfood_sync, test_module_size_ratchet,
test_complexity_ratchet), run by the coordinator: 308 passed / 1 skipped.
Trunk before this squash: 83d866c8.

WI-707's sweep minted WI-708 (the amendment adjudication of the thirteen
SRs) and WI-709 (the first approval of SR-223, TC-272, TC-290 and TC-297).

### Spine-acts batch D lands: the SR tier anchored at last

One independent Fable adjudicator judged four rows: WI-704, WI-705, WI-708
and WI-709. It also relied on three batch-C rulings after confirming by git
that their cells were unchanged: the 66 blessed WI-695 waivers, SR-178, and
SR-220's approval. Codex Sol cross-reviewed over three rounds
([sol-batchd.md](../reviews/2026-09-27-wave5/sol-batchd.md),
[sol-batchd-fix.md](../reviews/2026-09-27-wave5/sol-batchd-fix.md),
[sol-batchd-fix2.md](../reviews/2026-09-27-wave5/sol-batchd-fix2.md);
wave-5 rulings 49, 51, 52).
- **Routed pointers had been absorbed unruled.** `SN-Refs` and
  `Boundary-Refs` route to adjudication, but WI-707's nine `sn_refs`
  re-points and C2's 72 `boundary_refs` moves had never been ruled; the
  amendment brief does not render routed pointer cells. The adjudicator
  ruled all 81. Four lists were incomplete (SR-156, SR-164, SR-176,
  SR-220), so the coordinator completed them and the act was re-taken.
- **Act seq 6 copied all three spine registries.** It approved 13 rows
  (SR-220, SR-223, SR-225, LLR-282 to LLR-285, TC-272, TC-290, TC-292 to
  TC-294, TC-297) and re-attested 76. TC-296 returned on one self-referential
  sentence, and the sweep mints its follow-up.
- SR-164 now names both frames (B-05 delivery, B-09 operation), as its
  approved text does. It joins SR-139, SR-146 and SR-148 as a named
  frame-spanning advisory, not split (ruling 27).
- For the owner, a kit gap: the amendment brief shows an adjudicator the
  attesting cells but not the routed pointer cells, so a row can be blessed
  without its re-points being seen. Batches C and D both hit it.

**Open count: 10** (9 queued, 1 deferred): four adjudication rows closed.

Commit bar at batch D: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1799 passed / 3 skipped, seconds 42.9 s
within 60 s. Trunk before this squash: 126cf5f2.

Batch D's sweep minted WI-710, which was redundant in the same way as WI-706
(the four completed crossings and their act shared one squash), so it is
closed with that stated, and WI-711 (TC-296's one-clause follow-up).
**Open count: 11** (10 queued, 1 deferred).

### WI-618 lands: retired spine rows recorded as structured fragments

One builder, three Codex Sol rounds (wave-5 rulings 48 and 50):
[sol-wi618.md](../reviews/2026-09-27-wave5/sol-wi618.md),
[sol-wi618-fix.md](../reviews/2026-09-27-wave5/sol-wi618-fix.md),
[sol-wi618-fix2.md](../reviews/2026-09-27-wave5/sol-wi618-fix2.md).
`retire.py` deletes a spine row and writes its record under
`docs/log.d/retired/` in the same commit, and D-4 names that home. Two
warn-first checks watch the records, and the dashboard gains a Retired tab.
Sol's rounds made the census reservation-aware, gave shallow clones an
honest "unverifiable" advisory, closed a freshness exemption, tightened the
record format, and split the file seam (IF-257) from the command seam
(IF-258). At the merge the coordinator regenerated the census on trunk:
`retire.py --seed --replace --exclude SR-222,LLR-266..270,TC-262..268,IF-245..249`.
That excludes WI-620's reserved ids, which stay in the warn-only report
until that lane lands, and keeps the genuinely spent-unused ids (TC-277,
TC-280 to TC-288, TC-295, TC-298). **Open count: 10** (9 queued, 1 deferred).

Commit bar at WI-618: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken, smoke 1799 passed / 3 skipped, seconds 29.5 s
within 60 s. The touched slow modules plus both ratchets (test_retire,
test_retire_dashboard, test_trace, test_dogfood_sync, test_rule_sync,
test_resync_pack, test_gen_trajectory, test_traj_views, test_traj_render,
test_frame_context, test_check_docs, test_bootstrap, test_trunk_step,
test_skills_sync, test_module_size_ratchet, test_complexity_ratchet), run by
the coordinator: 448 passed / 2 skipped. `check_complexity --mode enforce`:
OK, 204 rows. The merge conflicted only in the watermark (trunk's,
re-bumped). The auto-merged registries were checked, and every row keeps
its status and phase. Trunk before this squash: ec05c5ce.

WI-618's sweep minted WI-712 (the first approval of WI-618's Drafted rows)
and WI-713. WI-713 is TC-055's re-judge, legitimately due because the Retired
tab changed the rendering code. It now waits on OI-96 by a `needs` edge,
since a re-judge before the owner rules on the shrink floor would fail
again on T4 at 390 px. WI-711, a one-clause authoring edit to Drafted
TC-296, was done by the coordinator as the batch-D adjudicator drafted it,
and TC-296 goes to the next batch. **Open count: 11** (10 queued, 1 deferred).

### Spine-acts batch E lands: WI-712 and WI-714

One independent Fable adjudicator judged WI-618's rows (WI-712) and TC-296
(WI-714), and ruled the routed pointer cells the brief does not render.
Codex Sol cross-reviewed it SOUND
([sol-batche.md](../reviews/2026-09-27-wave5/sol-batche.md)). Act seq 7
approved LLR-286, TC-299 and TC-296. SR-226, LLR-287 and TC-300 returned
on form findings the gate raises only on Approved rows: two `shall`s, an
unsupported waiver and a missing B-01 on SR-226, "such as" on LLR-287,
"minimal" on TC-300. The adjudicator found them by driving the flipped tree
and corrected the verdict before the act. The follow-up is one Dispositions
draft, minted at this merge; the coordinator corrected its cell count.
Recorded for the owner, a kit observation: the first-approval brief cannot
show a form finding the gate raises only on Approved rows, so every
adjudicator must flip and run `--strict` to see it. **Open count: 10**
(9 queued, 1 deferred).

Batch E's sweep minted WI-715 (SR-226's chain: the six cell fixes).
**Open count: 11.** WI-697 (TC-279's re-judge) cannot be briefed: the kit's
re-judge composer refuses an assumption-only case ("TC-279 has no
`Verifies` cell"). The same gap let batch C's first-approval brief skip
TC-279 silently. Both are the same surface as WI-667 (how assumption
evidence reaches the adjudication machinery), so the gap is folded into
WI-667's Context and Done-when, and WI-697 now waits on WI-667.

### WI-715 lands: SR-226's chain made approvable

One builder, one Codex Sol round, SOUND at 2305a648
([sol-wi715.md](../reviews/2026-09-27-wave5/sol-wi715.md)). The six cell
fixes are in: SR-226 has one `shall`, no waiver it cannot hold, and B-01;
LLR-287 has no "such as"; TC-300 has no "minimal". The rows stay Drafted,
and a scratch flip shows no form finding. The sweep mints their first
approval. Trunk before this squash: 9b16cde1. **Open count: 10**
(9 queued, 1 deferred).

### WI-620 lands: one session service for every model call

One builder, seven commits, five Codex Sol rounds (wave-5 rulings 53 to 56):
[sol-wi620.md](../reviews/2026-09-27-wave5/sol-wi620.md),
[sol-wi620-fix.md](../reviews/2026-09-27-wave5/sol-wi620-fix.md),
[sol-wi620-fix2.md](../reviews/2026-09-27-wave5/sol-wi620-fix2.md),
[sol-wi620-fix3.md](../reviews/2026-09-27-wave5/sol-wi620-fix3.md),
[sol-wi620-fix4.md](../reviews/2026-09-27-wave5/sol-wi620-fix4.md), SOUND
at 706cadc7. WI-620 absorbed WI-605, WI-606 and WI-551 at the consolidation.

- **One path.** `session_service.py` (act, keep, record) is the one path
  every model call takes. `session_adapters.py` holds one adapter per
  provider. `session_keep.py` is the retention keep operation, inert at the
  `[adjudicator]` table's `context_reset_pct = 0`, which is the shipped
  value.
- **Sol's later rounds** held retention to the ruled plan, bounded
  keep-warm, and made a failed or overrun retained launch retire rather
  than be reused (the lineage, the tombstone, the unreleased-lease rule, one
  clock per decision).

**WI-606 (lossless capture).** The codex route runs `exec --json` beside
`--output-last-message`; the file still gives a successful call's final
text. The opencode route runs `run --format json`. Each runner's
usage-bearing line is kept verbatim in the session log's `raw-usage` header,
and no parsed column gains a mapping from it. The claude fixture is a live
recording; the codex and opencode fixtures
(`tests/golden/sessions/codex-exec-json.jsonl`, `opencode-run-json.jsonl`)
are built from the documented event shapes and say so. **The opencode
pathway checks were not re-run on the installed 1.18.29**: the permission
classifier refused the builder's live runs, and they were not worked around.
So `docs/agents.toml` still records the version last tested, 1.17.18. Two
things are owed to the owner: recording both fixtures live, and re-running
the opencode checks over the changed route. WI-606's last Done-when stays
open until then.

**WI-605 (occupancy).** A session log's `context-used`, `context-window` and
`context-pct` now hold the occupancy of the session's latest request (the
final call's input plus cache read plus cache write), not the cumulative
counters that had read up to 34,836%. No session log has yet been written
under the corrected meaning, because the loop has made no claim since the
pause (`docs/work/pause`, 2026-09-04). The last log written,
`docs/iteration/wi521-decomposition-debt-owner-004-20260830-082452.log`,
carries the old meaning, so the first log written after this merge is the
first under the new one.

**At the merge.**
- *Conflicts:* the watermark (trunk's, re-bumped: SR 226 -> 227), the four
  registries (merged table by table from the base, 126cf5f2), RESYNC_PACK
  (both kept, and WI-620's three entries re-anchored to `[since 46970249]`),
  and the bootstrap ratchet.
- *The ratchet:* trunk's WI-618 row (1701) composed with WI-620's three
  MAPPING rows, re-measured at 1704. agent_common fell 1487 -> 1466 and
  agent_loop 2801 -> 2752.
- *Smoke:* WI-620's lane re-stamped the ceiling 1875 -> 1955.
- Trunk before this squash: 46970249.

**A lane red, found at the merge's bar.** IF-247, the retained-session
record file, named `scripts/session_keep` as both its owner and its
consumer; it had since Sol's second round moved the record to that module.
So `test_seam_resolution` failed, on the lane as well as on trunk, because
no one had run the whole smoke tier there. The coordinator set its far side
to the two processes that share the record through that module:
`scripts/agent_loop`, whose adjudication writes it, and `scripts/dispatch`,
whose keep-warm tick reads it. That is what the row's rationale already
states. IF-247 is Drafted, and its first approval judges the cell.

Commit bar at WI-620: `check_trajectory --strict` clean, `trace
--strict-integrity` 0, approve-modified current, `gen_open_items` current,
`check_docs --stale` 0 broken. Smoke: 1890 passed / 3 skipped, 1893
collected under the 1955 ceiling, 38.6 s within 60 s. WI-620's slow modules
plus both ratchets, run by the coordinator: 559 passed / 2 skipped. Those
modules are test_session_keep, test_session_service, test_session_adapters,
test_agent_loop, test_agent_loop_policy, test_dispatch,
test_dual_plan_routing, test_session_stdin, test_routing_and_prompts,
test_bootstrap, test_baseline_snapshot, test_seam_resolution,
test_frame_context, test_resync_pack and test_dogfood_sync, with
test_module_size_ratchet and test_complexity_ratchet. `check_complexity
--mode enforce`: OK, 203 rows. WI-541 (verify the retention layer on this
box) and WI-545 are unblocked. **Open count: 10** (9 queued, 1 deferred)
before the sweep.

### WI-620's sweep, and WI-719 lands: the spot check of its close

WI-620's sweep (d7e1be0e) minted three rows:
- WI-717: the amendment adjudication of LLR-177 and TC-172;
- WI-718: the first approval of WI-620's fourteen Drafted rows;
- WI-719: a sampled spot check of the close.

**Open count: 13** (12 queued, 1 deferred). WI-716, WI-717 and WI-718 went
to one batch-F sitting.

**WI-719.** An independent Fable adjudicator checked WI-620's nineteen
clauses. Codex Sol cross-reviewed it
([sol-wi719.md](../reviews/2026-09-27-wave5/sol-wi719.md)) and found two
recorded-fixture clauses marked MET over fixtures built from documented
shapes. Ruling 57: a clause that asks for a recorded fixture is not met by a
constructed one, however openly labelled. The correction re-accounted them,
and Sol confirmed it SOUND
([sol-wi719-fix.md](../reviews/2026-09-27-wave5/sol-wi719-fix.md)). The
tally is thirteen met, one met by supersession, and four clause parts
openly owed. `OUTCOME: FOLLOW-UP drafts=0`.

The owed parts lived only on closed surfaces, so nothing open tracked them.
The coordinator folded them into WI-541 instead of filing a row, as the
verdict proposed:
- WI-541's occupancy clause now also names the first corrected-occupancy
  log;
- two new Done-when bullets carry the live fixture recordings (WI-606's and
  WI-551's clauses) and the opencode pathway re-check (WI-606's last,
  verbatim).

The verdict's one observation, a stale sentence in `session_adapters.py`'s
docstring (it named `agent_session` as its importer; `session_service` is),
was corrected at the merge. Trunk before this squash: d7e1be0e.
**Open count: 12** (11 queued, 1 deferred).

### Spine-acts batch F lands: WI-716, WI-717 and WI-718

One independent Fable adjudicator ruled three rows from the kit's briefs,
routed pointer cells included, and took one act (seq 8).

Codex Sol cross-reviewed the first act
([sol-batchf.md](../reviews/2026-09-27-wave5/sol-batchf.md)) and found
three things:
- LLR-270 was approved with a time-relative receipt in its rationale ("the
  launch must be exactly today's"), the class the same sitting returned
  TC-262 for;
- LLR-177's routed `SR-Refs` went unruled;
- the draft miscounted its cells.

Ruling 59 upheld all three. As with ruling 51, the act was reverted in the
lane, the verdicts corrected, and the act re-taken. Sol confirmed it SOUND
([sol-batchf-fix.md](../reviews/2026-09-27-wave5/sol-batchf-fix.md)). Sol's
one remaining minor, the draft's "rule behind nine of them" (ten, with
LLR-270), was corrected at the merge.

**The coordinator's own error, ruling 58.** The coordinator's note to the
adjudicator had the amendment aftermath backwards: re-attest on CLARITY,
draft on MEANING. The kit's brief says CLARITY owes nothing, and a MEANING
verdict on a released rung is re-attested by the adjudicator. The
adjudicator followed the brief and the act stands. Lesson: a coordinator
note points at the brief's aftermath, never restates it.

- **WI-716:** `OUTCOME: APPROVE rows=3`. SR-226, LLR-287 and TC-300 are
  approved, so WI-618's chain is anchored.
- **WI-717:** `VERDICT: MEANING rows=2`. LLR-177's Detail and TC-172's
  Method now cover header values, and both are re-attested. SR-176 holds
  as LLR-177's parent.
- **WI-718:** `OUTCOME: RETURN rows=14`.
  - Approved: TC-263, TC-265, TC-266 and TC-267.
  - Returned: SR-222, SR-227, LLR-266 to LLR-270, TC-262, TC-264 and
    TC-268, on fourteen cells. Most are history or receipts in standing
    cells. Two are substantive: LLR-268 misdescribes claude's raw-usage
    line (the whole result line is kept, not three values), and TC-268's
    method claims a message its evidence makes optional.
  - The follow-up is one quick spine lane, minted at this merge. The same
    misdescription sits in `session_adapters.py`'s IF-245 docstring, so
    that lane corrects it too.
- `trace` now advises that LLR-267 and LLR-269 read Drafted while every
  test case citing them is Approved. That is expected from the mixed
  verdict, and it clears when the follow-up lands.

Trunk before this squash: e827e697.
**Open count: 9** (8 queued, 1 deferred) before the sweep.
