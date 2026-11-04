+++
id = "WI-993"
title = "An owner-held step is an open item: any step only the owner can take is filed as a pending item the row's needs cites, never only as handoff prose"
workstream = "process"
sr_refs = ["SR-049"]
specref = "docs/specs/WI-993.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
needs = ["OI-126"]
+++

## Context

Filed by hand on 2026-11-02 (attended) at the owner's request, carrying the
owner's ruling of 2026-10-25 and its seven filing calls
(coordinator-2026-11-02 D-004); the ruling and its calls are the spec of
record, `docs/specs/WI-993.md`. Call (5)'s pending items (OI-121 to OI-123)
and OI-124 were filed in the same commit, outside this row. Owes its scope
critique before its claim.

**Architectural delta (S5).** No new state and no new boundary. The work
item and open item mode classes keep their states and transitions: a claimed
row citing a pending item already reads `blocked` (LLR-288), and an item
still goes from `pending` to `ruled`. One value joins one domain: IF-073's
citers of a pending item become queued or claimed rows, and a draft, deferred
or closed row still does not count. Two outputs gain an input: the queue
projection (`kitlib/spine.py`, feeding the owner page, the status snapshot's
Blocked list and the uncited-item error) now reads claimed rows, and the
merge slot's intake mint (CMP-008, the writer's owner) now reads the accepted
verdicts of the merged range and the held dial, both across seams it already
holds (IF-287, `intake.adjudication_action`). Flow 6 stays as it is: the
judging turn stops at its verdict, and a sitting writes nothing to trunk. The
writer is a new arm of Flow 4's post-merge step, so its citer is a queued
row and a claim copy is never touched. The two citers do not overlap: a
hand-filed item for a planned step cites the claimed row, and a held-rung
MEANING act, which can never land from a lane (`held_status`, wi-976 D-023),
is carried by the minted queued row. The lane updates IF-073 (`data`, `notes`
and its version), IF-074's `data`, LLR-299 (it says "a citer that is not
queued does not count"), LLR-153, TC-314 and Flow 4. No refactor row is owed.

## Landing order

Three deliverables could land alone. The RESYNC entry is written with the
last of them and is not a fourth.

1. **The claimed citer** (the owner queue item, with IF-073, IF-074, LLR-299
   and TC-314). It lands first: until it does, an item only a claimed row
   cites is the checker's uncited-item error, so the policy text would
   instruct a filing the bar refuses.
2. **The policy text** (the PROCESS.md, claim, push and closure items). It
   needs deliverable 1.
3. **The mint arm** (the sitting verdict item). It needs neither, because
   its citer is a queued row, and it lands third only to keep the lane's
   review in one order.

One row or several is the owner's answer (rubric S1), recorded here before
the claim. Recommended: one lane, in this order, one commit each; deliverables
1 and 2 cannot usefully separate, and a split of deliverable 3 is filed on
trunk before the claim.

## Done-when

- PROCESS.md's open-items paragraph states the ruling once: an open item is
  anything keeping a row from building forward (an owner decision, an owner
  act, an approval or signature, a credential, the owner's presence), filed
  as a pending row the held work item's `needs` cites in the same commit;
  the coordinator-cycle skill's "Owner-held steps" step 3 points at it
  instead of restating it, and every other site stating the narrower
  "a decision only the owner can make" rule is amended to point there.
- A lane keeps its claim at a planned owner-held step only while the
  pending item is filed and cited on trunk; the text sites of OI-70's
  "partial is the only stop" are amended to say so; a re-scoping owner
  answer still closes the lane partial (call 1). A planned step is one the
  claim copy's Done-when names.
- A sitting verdict that rules MEANING on a held-rung row writes the
  pending open item for its owner act (the row, the verdict, the command),
  so no coordinator files it by hand (call 1, mechanized). The writer is the
  merge slot's intake mint, at the landing that brings the verdict and the
  row's text to trunk: one queued owner row citing the item, filed in the
  mint's one commit. Those rows leave that landing's amendment row, and the
  recipe's hand step for them retires.
- The owner queue on `open-items.html` counts claimed rows that cite a
  pending item, not only queued ones (call 2).
- A routine push files no item (call 3); an act's item closes by the
  owner's ruling or a delegated decision (call 4).
- No detector is built for a session that stopped and filed nothing
  (call 7).
- RESYNC_PACK: one entry; adopters' owner-held rows gain pending items at
  their next re-sync.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).

## Trust

**What gains authority.** One carrier: a claimed row's `needs` now clears the
checker's uncited-item error and puts the item on the owner's page. The hold
itself is not new (IF-054, IF-264). Two carriers gain none, on purpose:

- *The claim.* Nothing reads an open item or a `needs` edge to keep, drop or
  release a claim, and this row adds no such reader (call 7). "Keeps its
  claim" is a rule for the coordinator, stated in the text sites.
- *The verdict.* It holds no lane and releases nothing. Its one new effect is
  an item whose edge holds the single row the same mint writes. The act stays
  the owner's, under the held-status rule, unchanged.

The guard follows `project-trajectory/PROCESS.md` §3, "When a guard is owed".

**Producers and their failed writes.**

- *The verdict and its binding.* Written by the adjudicator and recorded by
  the sitting's route, unchanged. A failed sitting is a binding with no
  accepted outcome.
- *The minted item and row.* `project-trajectory/scripts/intake.py`:
  `intake_after_merge`, then `_mint` through the `open_item` draft path
  (`_inject_open_item`), so item, row and watermark are one bookkeeping
  commit. A failed write mints nothing, the merge stands, the refusal is
  named (a non-TOML registry included) and `intake.py sweep` replays it. The
  draft's title is built from the verdict and its rows, so the mint's
  exact-title dedup makes a replay safe. An item without its citation is not
  a state this route produces.
- *A hand-filed item and edge on a claimed row.* A person or the coordinator,
  in one trunk commit, on the claim copy. It is filed when the lane reaches
  the step: a row citing a pending item is off the frontier, so it cannot be
  claimed, and a claimed one draws no worker assignment.

**Consumers, by path** (under `project-trajectory/scripts/`).

- Changed: `kitlib/spine.py` (`open_item_queue`, `_held_rows`), and through
  it `pending.py`, `gen_open_items.py`, `traj_status.py` and
  `check_trajectory.py` (`uncited_open_item_findings`).
- New reader: `intake.py`, reading verdicts through `kitlib/sitting.py`
  (`branch_verdicts`, `accepted_at`).
- Unchanged: `schedule.py`, and through it `integrate.py` (the claim),
  `dispatch.py`, `agent_brief.py` and `traj_status.py`; and
  `acceptance_record.py` (`ruling_sync_lines`).

**The ruling, one for all of them.** The writer's input is a closed set, and
every state not listed writes nothing. A row sat more than once is read at
its latest accepted verdict in the range.

| Verdict in the merged range | Row at the landing | Result |
| --- | --- | --- |
| Accepted, the row ruled MEANING, blessed or not, on a held rung | differs from its anchored copy | one owner row and one pending item |
| Accepted, the same ruling | equals its copy | nothing |
| Accepted, any other ruling, or a released rung | any | nothing; the act route is unchanged |
| No binding, or pending, failed or invalid | any | nothing; an unsettled row stays on the amendment row, as today, and is sat again |

| Item | Citers | Reads as |
| --- | --- | --- |
| Pending | a queued or a claimed row | a card, the Blocked list, no error |
| Pending | none, or only draft, deferred or closed rows | the uncited-item error, as today |
| Named in `needs`, absent from the registry | any | blocked and the dangling-edge error, as today |
| Ruled | any | satisfied; the ruling sync applies, as today |

So a lane does not close complete on a pending item: its close would leave
the item uncited. A re-scoping answer rules the item, and the close follows.

Ruling a claimed citer ticks the Done-when item naming the step, in the
ruling commit, and adds no evidence there: the raw change satisfies the
ruling sync, a tick moves no digest, and evidence on the claim copy does. The
decision lives in the item. An item on a claimed row whose Done-when names no
such step keeps today's route, OI-119's: the sync demands a Done-when edit, a
`single` row's pass record then unbinds, and that goes to the owner. This row
changes neither rule.

**The bound** (PROCESS.md §6, "Review threat model"). The promise reaches what
supported workflows and the kit's own routes produce. A hand edit of a
verdict, a binding or a minted row, and sub-second timing windows, are outside
it. A hand-filed item and a `needs` edit are a person's supported route and
are inside it, read by the existing parse and dangling-edge checks.

## Critique dispositions

Round 1 (fresh Sol, 2026-11-04): CHANGES-REQUESTED, four MAJORs. The writer's
shape is re-derived here from the calls and the code, as coordinator-2026-11-02
D-004 directs.

- **S1, adopted, with one answer owed.** "Three deliverables could land alone"
  and each item's order are recorded under `## Landing order`. The finding's
  suggested order (policy first) is not taken: "until it does, an item only a
  claimed row cites is the checker's uncited-item error". The rest is the
  owner's: "One row or several is the owner's answer (rubric S1), recorded
  here before the claim."
- **S2/S3, adopted in part.** Adopted: producers, failed writes, consumers by
  path, one ruling and the bound, in `## Trust`, including "every state not
  listed writes nothing". Rejected: an authority over the claim. The finding
  reads "keeps its claim" as a carrier's authority, but no reader consumes it
  and call 7 forbids one; the spec now says "Nothing reads an open item or a
  `needs` edge to keep, drop or release a claim". Rejected as a state to rule:
  an item committed without its `needs`. Moving the writer to the mint removes
  it, "An item without its citation is not a state this route produces", so
  nothing guards it. The finding's scenario (a coordinator unable to tell
  whether filing completed) has no claim to decide, since the writer's item
  never touches the lane.
- **S4, adopted.** `planmode = "single"`: the row has a `## Trust` section and
  crosses IF-073 and the merge slot's mint.
- **S5, adopted.** The Context's delta states "One value joins one domain:
  IF-073's citers of a pending item become queued or claimed rows", names the
  writer "a new arm of Flow 4's post-merge step" and lists the records the
  lane updates. Nothing is beyond the row's scope.
