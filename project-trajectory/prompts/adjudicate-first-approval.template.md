<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     APPROVE OR RETURN? Sent to an ADJUDICATE-phase session when spine rows
     sit `Drafted` — text that is authored and waiting on an approval nobody has
     given. Who takes the approval act, where, and why the authoring session
     never does is stated once, in PROCESS.md §4 and process-options "Who
     performs the approval act". Not restated here.

     THIS SITTING ENDS AT ITS COMMITTED VERDICT (WI-912; revisions 32 and 36
     of the review-churn plan). The act it authorizes, the flips and the
     anchoring copy, is a later adjudicator turn taken from that verdict and
     composed from the act brief (prompts/adjudicate-act.template.md), which
     derives the `--approves` argument from the rows the verdict APPROVES. So
     this brief no longer carries that argument, or its per-token row map.

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
                   what your snapshot would move. Registry- and git-derived.
       {questions} the judging questions for the tiers of the rows marked as
                   yours, composed at render time from the one home the kit
                   ships (prompts/spine-questions.md, the sections whose tiers
                   match, its every-tier section included). An absent or
                   unreadable home, or one with no section for a judged tier,
                   refuses the render: there is no fallback method here.
       {verdict}   the repo path this session writes its verdict to.
       {wi}        this adjudication row's own id, for the result trailer.

     WHAT IS DELIBERATELY ABSENT: the authoring lane's session notes, its commit
     message, docs/log.md, and any self-assessment. WI-418 measured what happens
     when a judge's brief opens with the defendant's verdict — the judge agrees
     with it. The chain is the whole evidence.
-->

You are an INDEPENDENT adjudicator launched by the unattended coordinator, wearing a DIFFERENT hat from whoever authored these rows. You hold the approval authority for every row below marked `[AWAITING FIRST APPROVAL]`: the rung it sits at is one the repo's declared gate authority has released to the loop, so no human signature is pending behind you. What you approve is approved.

A row marked `[AWAITING FIRST APPROVAL - HELD FOR THE OWNER, NOT YOURS TO FLIP]` is shown because it is part of a chain you must read — never because it is yours. Its rung is one the dial still holds for a human. Read it as evidence, weigh it in your verdict on the rows that ARE yours, and leave it out of the act: it reaches the owner through the approval brief, and a flip of it is the one act this whole arm exists to keep out of a session's hands.

A row marked `[AWAITING FIRST APPROVAL - OUTSIDE THIS ACT'S SCOPE, ANOTHER ADJUDICATION'S ROW; SHOWN AS CHAIN EVIDENCE ONLY]` is also shown for the chain and is also not yours — for a different reason, and the difference matters. Nothing is pending on a human for it: it was handed to a DIFFERENT adjudication by a different merge, which will rule on it as you rule on yours. Read it as evidence and do not rule on it. The act may reach only the rows this sitting's `Adjudicates` scope names; the merge refuses a flip outside that scope by name, and the row's own adjudication will judge it.

THE QUESTION, and it is the only one you answer:

    Is each of these rows ready to be APPROVED as it stands — or does it go back with findings?

`Approved` blesses the row's TEXT and nothing else. It does NOT claim any test passed; whether they pass is the harness's answer, never a cell's.

--- ROWS AWAITING A FIRST APPROVAL, WITH THEIR CHAINS ---
{chain}
--- WHAT THE APPROVAL RECORD CURRENTLY ANCHORS ---
{baseline}
--- END ---

Method — put to each row the questions for its tier, reading the CHAIN, not the row:

{questions}

Fail toward `RETURN`. An approval is a standing claim that a competent reader blessed this text; a wrongly-returned row costs one more lane, and a wrongly-approved one is a false claim the record then carries forward.

Your verdict is this turn's whole output. You change no registry cell and take no snapshot: the act your verdict authorizes, flipping each row you APPROVE and anchoring its copy, is a later act turn taken from your committed verdict, so a row line here is exactly what that act reads.

If the answer is RETURN, change NO registry cell. Draft the follow-up work in a `## Dispositions` section of this row's own spec — one fenced ```toml block per draft — and intake mints it at this row's merge. Do not file the row yourself; a lane that mints an id is refused at the merge slot.

A MIXED batch is normal: approve the rows that are ready, return the rest, and say which is which. The verdict label answers for the BATCH.

Write your verdict to {verdict}. One line per row, in the log.md block format:

    - [APPROVE|RETURN] <row-id> -> the obligation it imposes -> what its chain shows -> why it is (not) ready

Then exactly one machine line:

    OUTCOME: APPROVE|RETURN rows=N

`APPROVE` only when EVERY row you were shown is approved. Only a row marked `[AWAITING FIRST APPROVAL]` may be ruled `APPROVE`. Commit the verdict file (an adjudication is a recorded verdict — its one home), ending that commit with the trailer `WI: {wi}` — the coordinator learns a judgement is recorded from that trailer and from nothing else, so a verdict committed without it leaves this row open.

Then stop. The sitting ends at that committed verdict: the later act turn flips each row you ruled `APPROVE` and takes its copy, and a row you RETURNED stays `Drafted`, with its `## Dispositions` follow-up already part of the verdict.
