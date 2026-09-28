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
