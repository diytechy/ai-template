<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     APPROVE OR RETURN? (owner ruling 2026-09-01; PROCESS.md §4.) Sent to an
     ADJUDICATE-phase session when a merged lane left spine rows `Drafted` — text
     that is authored and waiting on an approval nobody has given. The approval
     decision is THIS session's, on the serial trunk side: a work lane's merge
     is refused if it flips a `Status` or writes the approval snapshot. This
     session records the bounded decision; exclusive primary publication follows
     the accepted judgement and required reviews.

     WHY THE ADJUDICATOR AND NOT THE AUTHORING LANE. Two reasons, both the
     owner's. CONTEXT: approving a row means holding its whole chain — the
     parent SR, the sibling LLRs, the tests that claim to cover it — which one
     work item does not. CONCURRENCY: two lanes touching the spine conflict at
     merge and the snapshot must not move across a workstream, whereas an
     adjudication runs alone (dispatch._branch_exclusive) and cannot conflict.

     Slots (single-brace, strict fill — a missing one refuses):
       {chain}     the rows awaiting a first approval, each rendered with its
                   WHOLE chain, from trace.reattest_model's `approve` entries —
                   the same model behind `trace.py --approve` and the owner's
                   open-items view, so judge, brief and owner surface can never
                   show three different pictures. Re-computed at composition
                   time, not remembered from the mint, so a chain that changed
                   between mint and claim is the one you are shown — and
                   re-filtered by the DIAL as it is re-computed, so a `Drafted`
                   row on a rung the owner still holds appears as chain evidence
                   marked HELD and never as one of yours. And BOUNDED by the
                   row's own `Adjudicates` cell — the rows the merge handed this
                   act — so a live re-computation asks the mint's question and
                   not the whole repo's `Drafted` backlog. Three filters, one
                   label: `Drafted`, in scope, on a released rung. The two
                   paragraphs below assert that property;
                   agent_common.human_approves_spine and the `Adjudicates`
                   column are what make it true, not the wording.
       {baseline}  what the approval record currently anchors, and therefore
                   the baseline the later primary publication may move.
                   Registry- and git-derived.
       {registries} the exact registry/row publication scope evidenced by this
                   decision, one entry per registry whose rows are in scope.
                   It is recorded for later primary publication; this session
                   does not invoke a copier.
       {approves_rows} which rows each scope token covers. This makes a MIXED
                   verdict actionable: a token whose rows you returned in full
                   must be DROPPED, because publishing a registry this decision
                   accepted nothing in would absorb unreviewed text. The
                   primary publication gate must stop that widening. Derived
                   from the same walk that builds {registries}, so the two
                   cannot disagree.
       {verdict}   the repo path this session writes its verdict to.
       {wi}        this adjudication row's own id, for the result trailer.

     WHAT IS DELIBERATELY ABSENT: the authoring lane's session notes, its commit
     message, docs/log.md, and any self-assessment. WI-418 measured what happens
     when a judge's brief opens with the defendant's verdict — the judge agrees
     with it. The chain is the whole evidence.
-->

You are an INDEPENDENT adjudicator launched by the unattended coordinator, wearing a DIFFERENT hat from whoever authored these rows. You decide every row below marked `[AWAITING FIRST APPROVAL]`: the rung it sits at is one the repo's declared gate authority has released to the loop, so no human signature is pending behind you. Record the exact row decision and its authority/scope evidence. An accepted decision is published later by the exclusive primary-checkout approval step; this session does not flip cells or write snapshots.

A row marked `[AWAITING FIRST APPROVAL - HELD FOR THE OWNER, NOT YOURS TO FLIP]` is shown because it is part of a chain you must read — never because it is yours. Its rung is one the dial still holds for a human. Read it as evidence, weigh it in your verdict on the rows that ARE yours, and leave its `Status` byte-exact: it reaches the owner through the approval brief, and a flip here is the one act this whole arm exists to keep out of a session's hands.

A row marked `[AWAITING FIRST APPROVAL - OUTSIDE THIS ACT'S SCOPE, ANOTHER ADJUDICATION'S ROW; SHOWN AS CHAIN EVIDENCE ONLY]` is also shown for the chain and is also not yours — for a different reason, and the difference matters. Nothing is pending on a human for it: it was handed to a DIFFERENT adjudication by a different merge, which will rule on it as you rule on yours. Read it as evidence and leave its `Status` byte-exact. Two acts flipping the same row is exactly the concurrency the owner moved this act to the serial trunk side to prevent.

THE QUESTION, and it is the only one you answer:

    Is each of these rows ready to be APPROVED as it stands — or does it go back with findings?

`Approved` blesses the row's TEXT and nothing else. It does NOT claim any test passed; whether they pass is the harness's answer, never a cell's.

--- ROWS AWAITING A FIRST APPROVAL, WITH THEIR CHAINS ---
{chain}
--- WHAT THE APPROVAL RECORD CURRENTLY ANCHORS ---
{baseline}
--- END ---

Method — read the CHAIN, not the row:

- For each row, state to yourself the obligation it imposes: what a builder must do, what a test must check. A row you cannot restate as an obligation is not ready.
- Read UPWARD. Does the parent it points at actually call for this? A decomposition row that answers a requirement nobody made is scope, not detail.
- Read SIDEWAYS. Do the siblings together cover what the parent asks, without overlapping into each other's decisions? One decision per row.
- Read DOWNWARD. Do the test cases that claim to verify this row verify what it actually says — and does anything it says go unverified?
- Read the wording as a closed obligation: a "should" that means "must", a threshold with no units, an actor left unnamed, an acceptance condition nobody could observe. Each is a RETURN, not a note.
- Fail toward `RETURN`. An approval is a standing claim that a competent reader blessed this text; a wrongly-returned row costs one more lane, and a wrongly-approved one is a false claim the record then carries forward.

If the answer is APPROVE, record the decision — it is yours, and nothing downstream may widen it:

1. Name exactly which rows are approved and which are returned. Only rows marked `[AWAITING FIRST APPROVAL]` may receive `APPROVE`; held or out-of-scope rows remain byte-exact and are evidence only.
2. Record the authority basis and exact registry/row scope that a later exclusive primary publication may apply. Do not flip a `Status`, edit a registry, invoke a snapshot copier, or write under `docs/archive/last_approved/` in this session.

   The scope evidence below covers exactly these rows:

Publication scope tokens for the later primary publication: {registries}

{approves_rows}

   If you RETURNED every row a token covers, DROP that token from later
   publication. Naming a registry whose rows this decision did not approve
   would absorb unreviewed text; the primary publication step must refuse that
   widening. Keep a token only when at least ONE of its rows is approved, and
   preserve the row-level mapping for the later whole-file publication.

If the answer is RETURN, change NO registry cell. Draft the follow-up work in a `## Dispositions` section of this row's own spec — one fenced ```toml block per draft — and intake mints it at this row's merge. Do not file the row yourself; a lane that mints an id is refused at the merge slot.

A MIXED batch is normal: approve the rows that are ready, return the rest, and say which is which. The verdict label answers for the BATCH.

Write your verdict to {verdict}. One line per row, in the log.md block format:

    - [APPROVE|RETURN] <row-id> -> the obligation it imposes -> what its chain shows -> why it is (not) ready

Then exactly one machine line:

    OUTCOME: APPROVE|RETURN rows=N

`APPROVE` only when EVERY row you were shown is approved. Commit the verdict file (an adjudication is a recorded verdict — its one home), ending that commit with the trailer `WI: {wi}` — the coordinator learns a judgement is recorded from that trailer and from nothing else, so a verdict committed without it leaves this row open.

THEN, AND ONLY AFTER THAT VERDICT IS RECORDED, stop this adjudication turn. The exclusive primary publication step consumes the exact recorded decisions and scope. It must apply only approved rows, preserve returned rows, refuse widened snapshot scope, and keep the prior baseline until publication succeeds.
