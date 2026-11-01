# WI-977 checkpoint sitting at fddc055 (the whole spine set)

## amendment

This sitting judges WI-977's 23 amended rows together, so that one verdict authorizes the one act the set needs. Sitting 005's act alone was refused, because the registries it copies also held the rows that 006 and 007 judged.

**The text has not moved since it was judged.** Every row's JUDGED-TEXT identity in this brief equals the one I judged at an earlier sitting:
- SR-144, SR-148, SR-156, LLR-058 and TC-146 at 005;
- the sixteen re-authored rows at 006;
- LLR-207 and TC-205 at 007.

So no normative cell has changed since those sittings. I re-checked at this tip:
- a word-diff of every LLR and TC cell against its anchor (2aaf9f66f) shows only the batch-clause hunks judged before, and none of the swapped words sitting 006 returned;
- neither registry holds a U+FFFD character;
- `trace.py --strict` exits 0.

**The traced-cell fix from dispute sitting 011 has landed.** TC-205's evidence holds 90 entries and TC-156's holds 8, and `trace.py --tests-for` on `kitlib/verdict.py` lists `tests/test_bar_attestation.py` again. The traced cells are trace homes, not row text, so they owe no judgement here.

The verdict: every row is MEANING except LLR-058, which is CLARITY. I would bless all twenty-two MEANING rows.

- [MEANING+BLESS] SR-144 Requirement, AcceptanceCriteria -> before: a terminal partial close with one immutable report; a refused multi-spec close restores every report -> after: the same, also refusing a close whose claim is other than one work item before any report or state change; a refused single-item close restores its one report and leaves the claim and terminal state unchanged -> not the same: a cardinality refusal is added. Ready to bless (as at 005).
- [MEANING+BLESS] SR-148 Requirement, AcceptanceCriteria -> before: select the work an unattended run does next -> after: select exactly one work item for each admitted assignment, spine admission included; an ordinary frontier fills lanes through separate single-item assignments -> not the same: admission cardinality is bounded. Ready to bless (as at 005).
- [MEANING+BLESS] SR-156 Requirement, AcceptanceCriteria -> before: bounded, isolated lanes -> after: exactly one work item per lane; empty or multi-item claim, assignment and resume inputs refuse before changing state; historical multi-item records stay readable and are never run -> not the same: lane cardinality is bounded. Ready to bless (as at 005).
- [CLARITY] LLR-058 Title -> before: "WI-DAG frontier + deterministic traincar ordering" -> after: "WI-DAG dependency-ready frontier" -> the same: the detail, which is unchanged, never stated ordering; ordering is LLR-123's (as at 005).
- [MEANING+BLESS] LLR-061 Detail, Title -> before: on a multi-row lane, every assigned row with its walk state -> after: exactly one assigned work item, and an empty, malformed, repeated or multi-item assignment refuses by name before any session; every other clause verbatim -> not the same: cardinality narrows and a refusal is added. Ready to bless (as at 006).
- [MEANING+BLESS] TC-061 Method -> before: the two-row prompt-block and walk-state arms -> after: an empty, malformed, repeated or list assignment is refused before provider launch with no claim, lock or worktree; a committed trailer with the spec still open reads built but not done; every other arm verbatim -> not the same: the verified set changes. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-123 Detail, Title -> before: orders traincars, with the first WI id as the tiebreak -> after: orders work items, with the work-item id as the tiebreak; the named views kept -> not the same: the ordered unit changes. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-144 Detail -> before: moves each claimed spec, and a refusal restores every report -> after: moves the one spec; a claim of zero items or more than one refuses before any report, move or commit; a refusal restores the one report -> not the same: cardinality narrows and a refusal is added. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-149 Detail -> before: all spine rows admit as one batch, and approval rows admit as the queued batch at single-approve's close -> after: the first spine row admits alone and the rest wait; held rows surface even under keep-nondependent, which never releases their hold; delegated rows admit one at a time, exclusive -> not the same: the batch arm retires and the stale sentence is corrected to the code. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-150 Detail -> before: the worker argv carries the lane's assignment -> after: the argv is for the lane's one work item; a parked claim of several items stops the run by name before any mutation or relaunch -> not the same: cardinality narrows and a refusal is added. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-151 Detail, Rationale, Title -> before: batch-aware claims, one commit moving every batched spec, and one shared re-attest window -> after: one claim commit moves one queued spec; empty or multi-item input refuses before any move, commit, branch or worktree; historical multi-item commits are neither split nor re-claimed; separate exclusive windows -> not the same: cardinality narrows and a refusal is added. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-152 Detail -> before: a mixed batch fails toward the bar, and the batch's strictest bar value is forwarded -> after: a lane whose one row is any other kind runs the bar, and that one row's value is forwarded -> not the same: the batch arms become one-row arms. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-161 Detail -> before: a refusal restores EVERY report, so a multi-spec lane cannot half-close -> after: a refusal restores the one report, so a refused close leaves no report behind -> not the same: the restore narrows. Ready to bless (as at 006).
- [MEANING+BLESS] LLR-207 Detail -> before: sorted multi-row ids, the batch close, and the empty close refused by pairing and an empty id list -> after: exactly one moved row; any other shape declines to peel; the one-row clause refuses the empty and multi-row closes; one deletion implies one source branch; the composer takes one id -> not the same: the peel narrows to one row. Ready to bless (as at 007).
- [MEANING+BLESS] TC-058 Method -> before: traincar order -> after: work-item order; the named views kept -> not the same: the ordered unit changes. Ready to bless (as at 006).
- [MEANING+BLESS] TC-138 Method -> before: moves each claimed spec -> after: moves its one spec, and a claim of zero or several items is refused before any report, move or commit -> not the same: a refusal arm is added. Ready to bless (as at 006).
- [MEANING+BLESS] TC-143 Method -> before: every spine row admits as one batch, and the queued approval batch admits at the close -> after: the first spine row alone, the rest waiting; held rows drain and surface at keep-nondependent's close without releasing their hold; autonomous rows exclusive, one at a time -> not the same: the verified set changes. Ready to bless (as at 006).
- [MEANING+BLESS] TC-144 Method -> before: a spine batch in one commit, its worker receiving both ids -> after: one item per spine claim; a one-item parked lane resumes; a parked claim of several items stops the run before mutation or relaunch -> not the same: the verified set changes. Ready to bless (as at 006).
- [MEANING+BLESS] TC-145 Method -> before: a spine batch claims as one commit whose subject joins the ids -> after: one spec in one commit whose subject names one id; empty, separator-only or multi-item input refused by name before the lock and any write; a historical joined claim never re-run -> not the same: the verified set changes. Ready to bless (as at 006).
- [MEANING+BLESS] TC-146 Method -> before: adjudication cases with a mixed-batch bar arm -> after: a lane whose one row is any other kind runs the bar; the declared, undeclared and malformed bar arms kept -> not the same: the batch arm becomes a one-row arm. Ready to bless (as at 005).
- [MEANING+BLESS] TC-154 Method -> before: ahead of a ready spine batch -> after: ahead of a ready spine work item; the other arms verbatim -> not the same: the unit changes. Ready to bless (as at 006).
- [MEANING+BLESS] TC-156 Method -> before: no single-report restore arm -> after: an injected failure after a single close's report restores that one report and leaves claim and terminal state unchanged; the other arms verbatim -> not the same: an arm is added. Ready to bless (as at 006).
- [MEANING+BLESS] TC-205 Method -> before: the batch-shape arm, and a one-source-branch account of the second-lane and empty closes -> after: a two-row close does not peel under either subject; the one-row clause refuses the second-lane and empty closes, and no empty-id subject is composed -> not the same: the verified peel changes. Ready to bless (as at 007).

**What the act needs.**
- The rung is released, so the later act turn re-attests all 23 rows in one act: the twenty-two `[MEANING+BLESS]` rows, and LLR-058 re-anchored as CLARITY.
- That one act covers every drifted row in the system-requirements, low-level-requirements and test-cases registries that this lane amended, so the snapshot has no unnamed row to refuse over.
- No row here is on a held rung, and nothing waits on the owner.

VERDICT: MEANING rows=23

SITTING: JUDGED kinds=amendment
