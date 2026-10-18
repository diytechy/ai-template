<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     THE ACT, TAKEN FROM A COMMITTED VERDICT (WI-912). A sitting ends at its
     committed verdict; its act is a later adjudicator turn taken from that
     verdict (revision 32 of the review-churn plan; Q1 of
     coordinator-2026-10-14 D-003: an adjudicator turn with its own brief,
     since OI-45 (b) keeps scripted approval retired). Revision 31 lets a
     lane's verdicts be sat at any time while its acts keep landing order;
     revision 36 carries the split into the shipped briefs and the
     coordinator's entry point. The act is the `Status` flips and the
     anchoring copy, text before act (WI-806), each part in its own reviewed
     commit, and the merge admits it only when an accepted verdict over the
     act's own rows backs it (owner ruling 6, 2026-10-07). This brief is the
     one home of the act's instructions: the judging briefs no longer carry
     them.

     Every value is DERIVED by `scripts/adjudicate_act.py` from the verdict
     and its binding as committed at the lane's HEAD, the registries and
     their recorded copies at HEAD, and the dial at HEAD. It lists only the
     acts still owed there: a part already taken is `none owed`, and a
     verdict that owes nothing, or whose rows are in a state no act explains,
     is refused before this brief is composed (all or nothing). A held
     MEANING row, a MEANING row without the bless mark, a held APPROVE row, a
     RETURN row and a Done-when part owe no act and are never listed.

     Slots (single-brace, strict fill — a missing one refuses):
       {verdict}        the committed verdict that authorizes this act, as a
                        repo path; a held-rung re-attestation names it.
       {wi}             the adjudication work item, for each act commit's
                        trailer.
       {amendment_act}  the re-attestation the amendment part still owes:
                        the rows and the one `intake.py snapshot --reattests`
                        command, or `none owed`.
       {approval_act}   the flips the first-approval part still owes: the
                        rows, each with its registry, and the one
                        `intake.py snapshot --approves` command, or
                        `none owed`.
       {registries}     the `--approves` value of that command: one
                        `REGISTRY=REF` token per registry holding an owed
                        APPROVE row and no other, or `none owed`.
       {approves_rows}  which rows each of those tokens covers, or
                        `none owed`.

     WHAT IS DELIBERATELY ABSENT: any judging question and any verdict path
     to write. The judgement is recorded already; this turn writes nothing
     under docs/reviews/.
-->

You are the adjudicator taking the ACT a committed verdict authorizes. The judgement is already recorded, in {verdict}, and it is not yours to revisit: do not re-judge a row, and write nothing under `docs/reviews/`. Your work is the act below and nothing else.

The act is derived from that verdict and from this lane's committed tree. It lists only what is still owed. Take each part listed, in the order given, each in its own reviewed commit ending with the trailer `WI: {wi}`, and take nothing that is not listed.

--- 1. THE AMENDMENT ACT (re-attestation) ---
{amendment_act}
--- 2. THE FIRST-APPROVAL ACT (flips) ---
{approval_act}
--- END ---

The first-approval act's `--approves` value is `{registries}`. Its `;`-joined tokens cover exactly these rows:

{approves_rows}

How to take each part:

- THE AMENDMENT ACT comes first. Leave every row's `Status` at `Approved` and every registry cell byte-exact, run its one `python scripts/intake.py snapshot --reattests ...` command exactly as listed (with `--verdict` where it is listed), and commit the copy it writes. Never widen `--reattests` to a row that is not listed: re-attesting text no verdict ruled is the laundering the snapshot's refusal exists to stop.
- THE FIRST-APPROVAL ACT comes second. Move each listed row's `Status` from `Drafted` to `Approved`, and change nothing else in any registry: every other cell of every row stays byte-exact. Then run its one `python scripts/intake.py snapshot --approves "..."` command exactly as listed, and commit the flips and the copy together as one commit. KEEP THE QUOTES: the value joins registries with `;`, which every shell reads as a command separator, so an unquoted value spanning two registries snapshots only the first and runs the second as a command.
- A part listed as `none owed` is already taken, or was never owed. Skip it.

If the snapshot REFUSES, naming a row that is not listed, that row is an approved one whose text drifted from its recorded copy: an amendment another verdict owes. Do not add it to `--reattests` and do not edit it. Stop there: commit nothing further, and report the refusal. The coordinator discards what the refusal left uncommitted and takes the case from there.

You may not write or edit anything under `docs/reviews/`, edit any registry cell but a listed row's `Status`, or approve or re-attest a row that is not listed. The act turn reports success only when every listed part is committed.
