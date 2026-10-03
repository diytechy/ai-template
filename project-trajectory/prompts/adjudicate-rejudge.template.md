<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     THE CHECKPOINT RE-JUDGE (SR-215). Sent when a work-item merge or release
     preparation found an OBSERVATION test case (one recorded as not
     automated: a judgment the harness cannot rerun) due for a fresh judgment:
     its declared inputs no longer hash to its latest result's judged digest,
     that result expired, or it has none. The check that filed the row hashed
     files and ran no model; this session is where the judgment happens.

     Slots (single-brace, strict fill):
       {case}      the test case: id, what it verifies, Method, Expected, the
                   inputs it declares it reads and its result lifetime.
                   Registry-derived at HEAD.
       {reason}    what made it due, RE-DERIVED LIVE from the same decision
                   that filed the row (rejudge.due_cases at HEAD), so a case
                   re-judged since the mint refuses here rather than briefing a
                   session to judge it twice.
       {tc}        the case id, for the record command.
       {verdict}   the repo path this session writes its verdict to.
       {wi}        this adjudication row's own id, for the result trailer.

     The row's `Adjudicates` cell names the one case; the brief never reads
     the row's title or Context, which are prose.
-->

You are an INDEPENDENT adjudicator launched by the unattended coordinator. A checkpoint found an OBSERVATION test case due for re-judging: a test the harness cannot rerun, whose last result no longer covers the state of the project, or which has never been judged.

--- THE CASE ---
{case}
--- WHY IT IS DUE ---
{reason}
--- END ---

Judge the case by its Method, against its Expected, on the project as it stands at HEAD. Read the declared inputs; do not take the case's own earlier result, or anyone's notes about it, as evidence.

An assumption-only observation case is shown under its assumption's chain,
including the statement, falsifier and standing. Follow its Method against the
real thing: a failed observation is falsification evidence; a passed sample
establishes nothing beyond that sample. A person or adjudication sets standing.

If the Method is one you can carry out yourself (reading a rendered page, inspecting a document, critiquing an output), do it, then record the result with:

    python scripts/record_observation.py --tc {tc} --outcome pass|fail --by "<your model and this row's id>"

and commit the record file it writes. Record `fail` when the case does not meet its Expected; a failing result is kept, never replaced by a softer one.

If the Method needs a person's act (an attestation, a demonstration on real hardware, a measurement across an adopter's week), do NOT record a result: say in the verdict what the person must do and against which Expected.

Write your verdict to {verdict}: one `- [BLOCKER|MAJOR|MINOR] <what you checked> -> what you saw` line per point of the Expected you judged. Then exactly one machine line:

    OUTCOME: RECORDED|NEEDS-JUDGEMENT result=pass|fail|-

`RECORDED` when you judged the case and committed the record; `result=` is the outcome you recorded.
`NEEDS-JUDGEMENT` when the judgment is not yours to make; `result=-`. (The label names the owed ACT, not an actor.)

Commit that verdict file, ending that commit with the trailer `WI: {wi}` — the coordinator learns a judgement is recorded from that trailer and from nothing else — and stop. Never edit the test-case registry.
