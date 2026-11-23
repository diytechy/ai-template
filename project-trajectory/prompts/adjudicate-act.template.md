<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     THE ACT, TAKEN FROM A COMMITTED VERDICT (WI-912). A sitting ends at its
     committed verdict; its act is a later adjudicator turn taken from that
     verdict (revision 32 of the review-churn plan; Q1 of
     coordinator-2026-10-14 D-003: an adjudicator turn with its own brief,
     since OI-45 (b) keeps scripted acceptance retired). Revision 31 lets a
     lane's verdicts be sat at any time while its acts keep landing order;
     revision 36 carries the split into the shipped briefs and the
     coordinator's entry point. The act is the `Status` flips and the
     anchoring copy, text before act (WI-806), each part in its own reviewed
     commit, and the merge admits it only when a recorded verdict over the
     act's own rows backs it (operator ruling 6, 2026-10-07). This brief is the
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
     A first-acceptance flip WAITS (WI-1059) when a parent the parent-first
     rule reads for it would still not be accepted after this act: it stays
     owed, is never listed, and is named under `Not in this act` in
     `{acceptance_act}` with each parent it waits on, so the act lists only
     flips the commit hook's parent-first step admits. A verdict whose every
     remaining act waits is refused before this brief is composed.

     Slots (single-brace, strict fill — a missing one refuses):
       {verdict}        the committed verdict that authorizes this act, as a
                        repo path; a held-rung re-acceptance names it.
       {wi}             the adjudication work item, for each act commit's
                        trailer.
       {amendment_act}  the re-acceptance the amendment part still owes:
                        the rows and the one `intake.py snapshot --reaccepts`
                        command, or `none owed`.
       {acceptance_act}   the flips the first-acceptance part still owes: the
                        rows, each with its registry, and the one
                        `intake.py snapshot --accepts` command (or that no
                        flip can be taken in this act), then any waiting
                        flip under `Not in this act`; or `none owed`.
       {registries}     the `--accepts` value of that command: one
                        `REGISTRY=REF` token per registry holding an owed
                        APPROVE row and no other, or `none owed`.
       {accepts_rows}  which rows each of those tokens covers, or
                        `none owed`.
       {scripts}        the directory the snapshot script runs from: `scripts`
                        in a scaffolded repository, the kit's own
                        `project-trajectory/scripts` in the kit master
                        (`agent_brief.scripts_dir`, the value the reviewer and
                        worker briefs take). The commands in the two act parts
                        name the same directory.

     WHAT IS DELIBERATELY ABSENT: any judging question and any verdict path
     to write. The judgement is recorded already; this turn writes nothing
     under docs/reviews/.
-->

You are the adjudicator taking the ACT a committed verdict authorizes. The judgement is already recorded, in {verdict}, and it is not yours to revisit: do not re-judge a row, and write nothing under `docs/reviews/`. Your work is the act below and nothing else.

The act is derived from that verdict and from this lane's committed tree. It lists only what is still owed. Take each part listed, in the order given, each in its own reviewed commit ending with the trailer `WI: {wi}`, and take nothing that is not listed.

--- 1. THE AMENDMENT ACT (re-acceptance) ---
{amendment_act}
--- 2. THE FIRST-ACCEPTANCE ACT (flips) ---
{acceptance_act}
--- END ---

The first-acceptance act's `--accepts` value is `{registries}`. Its `;`-joined tokens cover exactly these rows:

{accepts_rows}

How to take each part:

- THE AMENDMENT ACT comes first. Leave every row's `Status` at `Accepted` and every registry cell byte-exact, run its one `python {scripts}/intake.py snapshot --reaccepts ...` command exactly as listed (with `--verdict` where it is listed), and commit the copy it writes. Never widen `--reaccepts` to a row that is not listed: re-accepting text no verdict ruled is the laundering the snapshot's refusal exists to stop.
- THE FIRST-ACCEPTANCE ACT comes second. Move each listed row's `Status` from `Drafted` to `Accepted`, and change nothing else in any registry: every other cell of every row stays byte-exact. Then run its one `python {scripts}/intake.py snapshot --accepts "..."` command exactly as listed, and commit the flips and the copy together as one commit. KEEP THE QUOTES: the value joins registries with `;`, which every shell reads as a command separator, so an unquoted value spanning two registries snapshots only the first and runs the second as a command.
- A part listed as `none owed` is already taken, or was never owed. Skip it.

If the snapshot REFUSES, naming a row that is not listed, that row is an accepted one whose text drifted from its recorded copy: an amendment another verdict owes. Do not add it to `--reaccepts` and do not edit it. Stop there: commit nothing further, and report the refusal. The coordinator discards what the refusal left uncommitted and takes the case from there.

You may not write or edit anything under `docs/reviews/`, edit any registry cell but a listed row's `Status`, or accept or re-accept a row that is not listed. The act turn reports success only when every listed part is committed.
