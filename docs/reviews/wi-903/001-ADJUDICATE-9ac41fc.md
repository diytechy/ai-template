# ADJUDICATE — WI-903 — queue overlap at 9ac41fc

Independent adjudication of the 29-row cluster the consolidation census minted
(digests `9bafb7b507a5|e3900a5ad95a`, unchanged when judged).

Disclosure. Besides the brief I read WI-875's verdict
(`docs/reviews/wi-875-adjudicate-queue-overlap-4214/001-ADJUDICATE-6fe2f8b.md`)
and its typed block, decisions D-015 and D-016 of
`docs/decisions/coordinator-2026-10-10.toml`, OI-113, the rider registry in
`text_then_act.py` (`LANE_COMMIT_RIDERS`, `lane_commit_walk`), the record
identity in `session_keep.py` (`HOME_VARIABLES`, `_store_path`,
`_load_path`), the `sr_refs` of LLR-167, LLR-246, LLR-265 and LLR-312, and
the priority key in `schedule.py`. I checked the state of every row the
cluster's `needs` name: WI-797, WI-834, WI-846, WI-847, WI-849, WI-852,
WI-853, WI-860, WI-865, WI-881, WI-884 and WI-892 are complete; WI-802 is in
draft. HEAD stayed at 9ac41fc throughout.

**What changed since WI-875.** Its five edges are in the files and its
judgement on the rows it sat on stands; I do not re-litigate it. New rows:
WI-878, WI-887, WI-893, WI-895, WI-897, WI-901, WI-902. Newly claimable
together, because their prerequisites landed: WI-798, WI-799, WI-832,
WI-850, WI-851 (WI-892 and WI-849 complete), WI-856, WI-878, WI-887 (WI-884
complete), WI-895 (WI-881 complete), WI-897, WI-901, WI-902. This sitting
judges the new rows against the rest and the pairs that are now claimable
on one day.

**Shape 1, contradiction with the spine: none.** WI-893 carries WI-828's
hand-merge path behind OI-113 and contradicts no SR. WI-901's and WI-902's
rows fix refusals that SR-144 and SR-220 do not require. WI-887's persisted
final reviewer stays inside SR-227's retention terms (a scope-keyed record,
dial shipped off).

**Shape 3, already answered: none.** WI-892 moved the walk and changed no
behaviour, so the riders WI-833, WI-850 and WI-851 owe are still owed.
WI-901's empty-range refusal and WI-902's missing "existing successor" exit
are both live (`_commit_facts`; `handback.py:870`, `intake.owes_successor`).
No absorbed row of an earlier consolidation is in this cluster.

**Shape 2, scope overlap: nothing is one work item wearing two ids.** The
WI-788 slices (WI-798..WI-817) are a deliberate cut of one design and are
ordered among themselves; WI-832/WI-833 share a ruling and are ordered;
WI-850/WI-851/WI-857 share a proposal but state three rules. Three pairs are
unordered collisions, each answered with a hard edge:

- [MAJOR] WI-887 -> WI-798 and WI-887 are both claimable today and both
  redefine what identifies a retained session in `session_keep.py`. Today the
  record's identity is `(family, route_id)` (`_store_path`, `_load_path`)
  and the dedicated home is per family (`HOME_VARIABLES`). WI-798 retires the
  per-family home for per-account homes and adds the `ROUTE@ACCOUNT`
  qualifier; WI-887 re-keys the record on the route id plus a scope and
  states "a record naming another family, route or scope is no record".
  Neither names the account as part of the record's identity. Built in
  parallel, two accounts of one route share one retained record while
  launching under two homes, so a session minted under one account's home is
  resumed under the other's. -> add the edge WI-798 needs WI-887. WI-887
  sorts first (P5 over P3) and its chain to WI-800 runs through WI-858, so
  this order keeps WI-800's critical path shorter than the reverse. WI-798
  then extends WI-887's scoped key with the account, so a record naming
  another account is no record either.
- [MINOR] WI-902 -> WI-810 retires `intake.py sweep` (LLR-265) and moves
  every disposition into the MINT consumption list, whose `successor` exit
  must keep the rule WI-902 adds: naming an already-queued row carrying
  `supersedes` discharges the successor obligation (OI-73's "no third exit"
  kept). WI-902 amends the sweep and `close_adjudication` (LLR-312, LLR-265).
  Nothing orders them; if WI-810 landed first, WI-902 would amend retired
  rows. -> add the edge WI-810 needs WI-902, as WI-875 did for WI-856.
- [MINOR] WI-878 -> WI-811 has a finding the builder disputed and the
  adjudicator resolved count as covered for WI-853's gate "citing the
  resolution", in the loop, where rework rounds number their findings F1..Fn
  afresh each round. That is exactly the reuse WI-878 fixes: today the gate
  scans sibling findings files and refuses a valid cited dismissal when two
  rounds reuse ids. WI-878 makes the binding record the findings file it
  ruled. Nothing orders them. -> add the edge WI-811 needs WI-878, so the
  loop's dispute sitting writes and reads the same binding record.

Recorded for the builders and the coordinator; no edge or outcome change:

- [MINOR] WI-851 -> WI-901 cites SR-208 and names "LLR-246's chain" as the
  rows its change makes untrue. `disposition_values` is LLR-167's
  (`adjudicate_brief.py`, sr_refs SR-146/SR-144/SR-148); LLR-246 is the
  held-status refusal under SR-208, which WI-851 rewrites in a combined
  sitting and which is claimable the same day. -> at WI-901's claim, the
  coordinator re-anchors its `sr_refs` to SR-144 and the parenthetical to
  LLR-167's chain; WI-901 amends neither SR-208 nor LLR-246.
- [MINOR] WI-893 -> WI-833's and WI-851's Done-when still say the rule rides
  "WI-828's" walk on "a squash or merge landing". By D-015 the walk is
  WI-892's (`LANE_COMMIT_RIDERS`) and the hand-merge arm is WI-893's, behind
  OI-113. -> each row's merge-landing clause is discharged by registering its
  rule as a rider of the one walk; WI-893 then brings the hand-merge path to
  every rider. Neither row waits on WI-893 (that would hold WI-851, and with
  it WI-800/807/808/809/810, behind an owner ruling).

WI-850 and WI-851 both add a rider to `LANE_COMMIT_RIDERS` and a step to the
pre-commit set; their spine rows differ (SR-178's chain vs SR-208, LLR-246,
LLR-278), so the collision is textual and a rebase resolves it, as WI-875
found. WI-895 (the keep-warm ping's `TreeNotEnded`), WI-897 (the guard
hook's imports and matcher), WI-856 (`edged_text`), WI-832 and WI-827 share
modules with others only at different functions, and each is its own
decision. WI-799's refactor touches the call sites of most ready rows in
`integrate.py` and `handback.py`, but it is representation only, "with only
call sites edited", so those collisions are textual too.

OUTCOME: QUEUE-WITH-EDGE needs=WI-798;WI-810;WI-811 absorbs=-
