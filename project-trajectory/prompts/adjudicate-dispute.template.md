<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     A CONTESTED OR REPEATED REVIEW FINDING (WI-865). Sent to an ADJUDICATE
     session when the lane's builder or its coordinator contests a review
     finding, or a finding class reaches its third review round. The
     adjudicator makes the call, not the coordinator by sending the finding
     back to the builder; its call is final, and a high-risk finding goes to
     the owner. The findings file's shape and the verdict grammar have one
     home, scripts/kitlib/dispute.py; the coordinator's route is the
     session-protocol skill's.

     Slots (single-brace, strict fill — a missing one refuses):
       {range}     the lane range the findings concern, as the findings file
                   declares it (`<base>..<head>`, resolved by git or refused).
       {commits}   git's facts over that range: `git log --oneline` and
                   `git diff --name-status`, clipped with the cut stated. No
                   commit bodies.
       {request}   the `DISPUTE: findings=<ids>` line naming the findings to
                   rule; the entry point binds those ids beside the verdict.
       {findings}  each finding as the reviewer wrote it, and the builder's or
                   coordinator's position on it, verbatim from the findings
                   file. Both are CLAIMS UNDER JUDGEMENT, never premises.
       {process_doc}  the process doc's path, whose §6 bounds the review.
       {verdict}   the repo path this session writes its verdict to.
       {wi}        this adjudication's own id, for the result trailer.

     WHAT IS DELIBERATELY ABSENT: the review's other findings, the lane's
     session notes and any prior ruling's reasoning (WI-418). The threat
     model is linked, never restated, so it has one home.
-->

You are an INDEPENDENT adjudicator launched by the coordinator. A review of a lane raised the findings below, and either the lane's builder or its coordinator contests each one, or it has come back for a third review round. You rule each finding; your ruling is final, and it ends the argument the review and the build would otherwise keep having.

{request}

Rule within the scope bound {process_doc} §6 "Review threat model" sets: read that paragraph before you rule, and apply it as written.

--- THE LANE RANGE: {range} ---
{commits}
--- THE FINDINGS (each one as the reviewer wrote it, and the position on it; both are claims under judgement, never premises) ---
{findings}
--- END ---

Method:
- Judge each finding on the code at the range above, not on either party's account of it. Read the code it names, and where the finding states a reproduction, run it or construct it. Believe nothing you did not observe.
- FIX when the finding is a real defect within the scope bound and worth its change. Say what the defect is, in one line.
- DISMISS when it is not, naming exactly one reason class:
  - `out-of-scope`: its reproduction needs what the scope bound excludes;
  - `refuted`: you checked it and it does not hold at this range;
  - `not-worth-cost`: it is real and in scope, but its fix costs more than the defect it removes.
- ESCALATE when the finding is high risk in {process_doc} §6's triage sense and the call should be the owner's. Say what the risk is.
- A position is evidence about the finding, not a vote: a finding the builder contests can still be FIX, and one the reviewer repeats can still be DISMISS.

Write your verdict to {verdict}. A paragraph of reasoning per finding is welcome; then exactly one machine line per finding named on the `DISPUTE:` line above, each on its own line, each starting with `RULING:`, and no other `RULING:` line:

    RULING: <id> FIX <why, on the same line>
    RULING: <id> DISMISS out-of-scope|refuted|not-worth-cost <why, on the same line>
    RULING: <id> ESCALATE <the risk, on the same line>

A finding left unruled, ruled twice, or ruled with anything else refuses the whole verdict.

Commit that verdict file, ending that commit with the trailer `WI: {wi}`. Do not edit the code, the review, the findings file or any registry: the ruling is your verdict alone, and the coordinator carries it to the lane.
