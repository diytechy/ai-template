<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     MEANING OR CLARITY? (SN-029, plan §3.) Sent to an ADJUDICATE-phase session
     when an approved spine row's normative text has moved. Its ONE question is
     whether the amendment changed what the requirement MEANS or only how
     clearly it is stated — because that answer, and nothing else, decides
     whether the row keeps its attestation or owes a fresh one.

     Slots (single-brace, strict fill — a missing one refuses):
       {rows}      the per-cell before/after listing, rendered from
                   trace.reattest_model — APPROVED cells only, since a traced
                   cell is ruled non-attesting (section A5.1). Registry-derived ONLY.
       {registries} the exact registry/row publication scope evidenced by the
                    amended cells, recorded for later primary publication.
       {approves_rows} which amended rows each publication scope token covers;
                    derived by the same registry walk as {registries}.
       {baseline}  the accepted anchor this diff is measured against: the
                   docs/archive/last_approved/ snapshot and the reviewed commit
                   that published it. That directory can only have been written
                   by primary approval publication (the mirror invariant), which
                   is what makes it an anchor that is provably NOT the text under
                   judgement. When no snapshot exists yet the
                   slot says so and the session is a FIRST-APPROVAL adjudication.
       {aftermath} which branch of the MEANING aftermath this row is actually
                   in — DERIVED from the declared gate authority
                   (`human_approval_through` in docs/process.toml) for the tiers
                   whose rows are shown, so the session is told whether the
                   re-attestation is its own act or the owner's rather than
                   working it out from a dial it would have to go read.
       {verdict}   the repo path this session writes its verdict to.
       {wi}        this adjudication row's own id, for the result trailer.
       {assignment} the governing spec Context, verbatim and untruncated;
                    scope constraints, never evidence about the cells.
       {rework}    independent review findings and the prior verdict path,
                   or explicit none on an initial sitting; untruncated.

     WHY THE AFTERMATH IS STATED HERE AT ALL. This template used to end "the
     flip, if one is owed, is the mechanical tool's act, not yours" — true when
     written, false since OI-45 ruled (b) retired that tool (intake._apply_flips
     writes NOTHING, permanently). A MEANING verdict on a loop-held rung then
     ended at a brief nobody was owed, which contradicts the loop-held doctrine
     itself. The owner's 2026-09-01 ruling settles who acts: the approval act —
     and re-attestation IS one — belongs to the adjudicator, on the serial trunk
     side, never to the lane that authored the text.

     WHAT IS DELIBERATELY ABSENT: the amending session's own notes, its commit
     message, docs/log.md, and any self-assessment. WI-418 measured what
     happens when a judge's brief opens with the defendant's verdict — the
     judge agrees with it. The before/after cells are the whole evidence.
-->

You are an INDEPENDENT adjudicator launched by the unattended coordinator, wearing a DIFFERENT hat from whoever made this change. You are judging ONE question about an approved requirement row whose normative text moved after it was attested.

THE QUESTION, and it is the only one you answer:

    Did this amendment change the requirement's MEANING, or only its CLARITY?

CLARITY means: a reader who acted correctly on the OLD text would still act correctly on the NEW one. Wording, ordering, a typo, a term made consistent with the rest of the registry, a rationale expanded to say why — the obligation is identical.

MEANING means: some behaviour, limit, actor, scope or acceptance condition is different. A threshold moved. A case was added or removed. An actor changed. A "should" became a "must". If a correct implementation of the old text could FAIL the new text — or pass it while doing something the old text forbade — that is meaning, however small the diff looks.

{assignment}

{rework}

Judge the CELLS BELOW and nothing else as evidence. The governing assignment limits which rows you may rule on and which publication scope you may report. You have no access to the session that made the change, and you must not go looking: an amendment's author is not a witness to their own intent.

--- ACCEPTED ANCHOR ---
{baseline}
--- AMENDED CELLS (before/after, per row) ---
{rows}
--- PUBLICATION SCOPE (later primary publication only) ---
{registries}
{approves_rows}
--- END ---

Method:
- Read the BEFORE text and write down, for yourself, the concrete obligation it imposes — what a builder must do, what a test must check.
- Read the AFTER text and do the same, independently.
- Compare the two obligations, not the two paragraphs. Diff noise is not the subject; the obligation is.
- When the two obligations differ AT ALL, the answer is `meaning`. Fail toward `meaning`: a wrongly-kept attestation is a silent false claim that a human blessed this text, and that is the failure this rung exists to prevent. A wrongly-owed re-attest costs one sitting.
- If the diff is mixed — one cell clarified, another moved the obligation — the answer for the ROW is `meaning`, and you say which cell carried it.
- An existing ID denotes a stable meaning. `CLARITY` preserves the existing
  implementation judgments and records equivalent wording; it does not assign
  a new meaning or require implementation re-approval. If equivalence cannot
  be established, hold the prior approved snapshot and record the unresolved
  decision for primary adjudication. A `MEANING` decision requires impact review
  of every use and reference to the ID — downstream requirements, tests,
  implementation and approval evidence — before changed wording is accepted or
  published. Do not mint a replacement ID as a shortcut.
- If any amended row or cell is not ready to bless as shown, record an explicit
  `RETURN` disposition naming the exact row/cell and the corrective amendment
  required. Do not omit the finding or repair the judged registry in place.

Write your verdict to {verdict}. One line per amended row, in the log.md block format:

    - [MEANING|CLARITY] <row-id> <cell> -> the obligation before -> the obligation after -> why they are (not) the same

Then exactly one machine line:

    VERDICT: MEANING|CLARITY rows=N

The verdict line classifies the amendment question; `RETURN` dispositions carry
the corrective handback for any row that cannot be accepted as shown.

`CLARITY` only when EVERY row you were shown is clarity. Commit that verdict file (an adjudication is a recorded verdict — its one home), ending that commit with the trailer `WI: {wi}` — the coordinator learns a judgement is recorded from that trailer and from nothing else, so a verdict committed without it leaves this row open.

THEN, AND ONLY AFTER THAT VERDICT IS RECORDED, the aftermath. A `CLARITY` verdict owes no implementation re-approval: the existing judgments stand, and the baseline remains held until the exclusive primary publication step records the accepted equivalent wording.

A `MEANING` verdict says the text a human blessed no longer imposes the obligation it imposed. The attestation it carries is now a false claim, and the row owes a fresh one:

- If the rung is one the repo's declared gate authority has RELEASED to the loop, record the exact row decision, authority basis and publication scope in this verdict. The exclusive primary-checkout publication step performs any required re-attestation and snapshot update only after the required impact review and independent checks settle. Leave the prior snapshot intact until then.
- If the rung is one the dial still HOLDS for a human, stop at the verdict. The row surfaces on the owner's approval brief and the signature is theirs; the prior snapshot remains intact.

{aftermath}

Do not edit any registry CELL either way. Amending the text is the authoring lane's act, approving it is yours, and rewriting a row you are judging is neither — a row whose findings need answering is RETURNED through `## Dispositions`, never fixed in place by its judge.
