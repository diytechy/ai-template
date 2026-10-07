<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     ONE SITTING PER LANE CHECKPOINT (SR-156, WI-841). A lane can owe several
     in-lane judgements at once: approved rows whose text drifted (the
     amendment question), Drafted rows awaiting a first approval, and a changed
     Done-when. Judged one sitting each, WI-835's lane took five sittings for
     what one could hold. This brief COMPOSES them: each section below is the
     kind's own shipped brief, composed by the kind's own assembler over the
     ids this row's `Adjudicates` cell scopes to it (`<kind>:<id>` tokens), so
     each section keeps its own grammar and its own acts, and text-then-act
     still applies to every act a section owes. A section that cannot be
     composed refuses the whole sitting (all-or-nothing). A RETURNED item is
     re-sat alone: the next sitting names only the returned ids.

     Slots (single-brace, strict fill — a missing one refuses):
       {sections}  the composed per-kind briefs, in the order amendment,
                   first-approval, done-when; each one's {verdict} names its
                   `## <kind>` section of this sitting's verdict file.
       {kinds}     the `;`-joined kinds composed, which the closing
                   `SITTING:` line restates verbatim.
       {verdict}   the repo path of this sitting's one verdict file.
       {wi}        this adjudication row's own id, for the result trailer.
-->

You are an INDEPENDENT adjudicator holding ONE sitting for a lane checkpoint. It composes several judgements, each in its own section below. Each section is a complete brief for its kind: answer each one exactly as its section asks, with its own machine line, and take each act a section owes in its own reviewed commit, text before act.

Write ONE verdict file at {verdict}, with one heading per section, spelled exactly `## <kind>` (for this sitting: {kinds}). Under each heading write that section's verdict lines and its machine line, and nothing for another kind. A section that asks for a `## Dispositions` draft takes it under its own heading.

End the file with exactly one machine line naming every section you judged:

    SITTING: JUDGED kinds={kinds}

Each section below says to commit its verdict file: commit this ONE file once, after every section is written, ending that commit with the trailer `WI: {wi}`; then take each act a section owes.

{sections}
