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
