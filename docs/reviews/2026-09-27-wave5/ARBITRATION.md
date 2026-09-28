# Arbitration — the fifth build wave (2026-09-27)

The session that resumes from
[the wave-4 handoff](../../handoff-2026-09-27-wave4-coordinator.md): spine-acts
batch B, then WI-679, then the remaining groups. Builders work in their own
worktrees; codex Sol reviews each commit read-only (the `sol-*.md` files beside
this one). The coordinator rules where a builder and Sol disagree, where it
disagrees with Sol, and where a queued item asks for a ruling that is not the
owner's, citing the governing text. Rulings a Fable arbiter makes are marked as
such.

1. **Batch B (8a960cf1), the blocker: TC-055 re-attested over a false
   `expected` — SOL.** WI-638 declared `max_age = 90` on TC-055 (wave-4
   ruling 2), so the re-judge checkpoint now re-fires the case on expiry, while
   its unamended `expected` still says the recorded verdict "is a one-time
   judgement that nothing re-fires". The adjudicator saw it and called the
   sentence "the weaker of two true statements". It is not true: the row now
   says both that nothing re-fires it and when it is re-fired. The governing
   text is PROCESS.md §7: an approval blesses the row's TEXT, and the
   amendment brief lets a MEANING row be re-anchored only when its new text is
   one the adjudicator would bless. Approved SR-054's rationale makes the same
   claim ("a recorded one-time judgement rather than a standing
   re-judgement"). **Ruling:** the act is reverted in the lane. The
   coordinator amends TC-055's `expected` and SR-054's `rationale` in place,
   status left Approved, to say the verdict is re-judged when a declared input
   changes or the record expires, never on every commit. SR-054 joins WI-680's
   scope, and the same adjudicator judges both amended cells. Then ONE act is
   re-taken. The adjudicator authored neither amendment, so it stays
   independent of what it judges.

2. **Batch B, major: LLR-205's disposition is too narrow — SOL.** Deleting
   the closing status sentence leaves the rationale calling itself "a live,
   dated finding" with a dated plan citation, and the `detail` narrating the
   state before the table. Both break the spine-authoring skill's
   cell-hygiene rule (a living cell states the system and its standing
   reason, never its history). The rows are returned either way, so no act
   changes. The fold into WI-616 states the whole fix.

3. **Batch B, major: TC-201 and TC-203 approved with changelog prose — SOL.**
   TC-201's method narrates what "now" catches against what "was", and a
   pattern record "BEFORE this table existed"; TC-203's opens "Re-tiered
   into". The adjudicator noted TC-203's and passed it on SR-176's approved
   precedent. An existing approved row with the same defect is a reason to
   fix that row too, not to approve a new one. Both cases verify design rows
   this act returns (LLR-205, LLR-206) for the same class of defect.
   **Ruling:** TC-201 and TC-203 are returned with their design rows and
   rewritten in the same WI-616 part. The act approves 25 rows, not 27.

4. **Batch B, second sitting: the coordinator's TC-055 amendment was itself
   wrong — ADJUDICATOR.** Ruling 1's amended `expected` said the verdict is
   re-judged "only when a declared input changes or the record passes its
   declared max_age". The adjudicator withheld the blessing: the code's first
   trigger (`rejudge.due_cases`, a case with no result on record) is missing,
   and it is TC-055's state at HEAD. It drove `due_cases` to show it, and the
   snapshot refused on TC-055 as it should. The error was the coordinator's.
   **Ruling:** the cell takes the adjudicator's drafted wording, which names all
   three triggers, as a second in-place amendment. The adjudicator re-judges
   it before the one act. The revert of the first act left the snapshot copies
   unequal to the live files at the commit that wrote them (the mirror
   invariant, red under `--strict-integrity`); the re-taken act clears it. Any
   later revert of an act needs the same care.

   The adjudicator also found that the five observation cases the checkpoint
   reports due (TC-036, TC-055, TC-209, TC-210, TC-211, none recorded) have no
   re-judge rows, although three lanes merged after WI-638 declared their
   inputs. The coordinator's hand squash-merges do not run the kit's merge
   checkpoint, so the rows were never minted. That is the hand path bypassing
   the kit's machinery, WI-679's surface, and it is folded there.
