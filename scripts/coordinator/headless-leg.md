HEADLESS LEG. Before step 1, run `echo "$KIT_LOOP_SESSION"`. It must print the session that the LOOP PROVENANCE line at the end of this prompt names. If it does not, write nothing and end the reply.

This session is one headless leg of an overnight run: one turn, and ending the reply ends the leg. Nobody answers a question or a notification. Where the prompt above says otherwise (that you run attended, that you ask the owner, that background tasks or notifications are fine), this block governs.

Follow the `coordinator-cycle` skill's headless-leg section (SKILL.md section 7, "Headless legs") for every step: the trailer on every commit, foreground only, the owner-held steps, the lane-mode rule and a leg's landing.

At close-out, the new handoff's session prompt block is the prompt above this block, copied verbatim. Never copy this block or the LOOP PROVENANCE line into it. Add the `Overnight: stop` line only when the queue is done or no row can move without the owner.

Rulings: the review-churn plan's revisions 35 ("The coordinator role") and 36 ("Headless coordinator legs are marked now"); docs/decisions/coordinator-2026-10-14.toml D-016 (Q2: one attended prompt, this fixed block and the kit's trailer note, so nothing is copied and nothing drifts).
