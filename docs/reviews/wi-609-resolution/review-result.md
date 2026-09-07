Reviewing the WI-609 design against the pasted source only, with no tool use.

## Verdict

OUTCOME: **RETURN** for resolution-design readiness.

Preparation under current authority: **partly**. Tests that reproduce the deadlock and a merge-time hold can be written now on a lane. The judgment-only mechanism itself should wait for one owner decision that the design wrongly claims is not needed.

## Root-cause reading is correct

The deadlock is real and the pasted source confirms it. The scope check in `_decision_rows` forbids foreign decisions. The census enumerates every changed approved row in the file. The ledger check then refuses any approved-change entry without an accepted scoped decision. The projection has only two exits, return with zero effect or publish with a copy. Two owners with drift in one file can therefore never close. The rejected shortcuts are rightly rejected.

## Where the design is unsound or unfinished

- **First approvals under judgment-only are an orphan.** An `approve` decision recorded judgment-only closes the WI while the row stays Drafted. The design defers the later Status flip and separately forbids any other turn from promoting it. Nothing can ever flip that row. Correction: refuse the `approve` classification when intent is judgment-only. The collection covers only amendments to already-Approved rows. First approvals simply wait until the copy lands, which the existing path then handles unchanged.

- **The hold is stated but not enforced, so termination is not guaranteed.** Item 6 says bytes stay fixed during collection but names no enforcer. If any spine-authoring merge lands between A and B, B's turn record binds different blob maps, A's evidence is stale forever, and A's WI is already closed. The design says collection "restarts" but defines no path to renew a judgment whose WI no longer exists. Correction: add a coordinator refusal, in the same place `writer_refusal` lives, that blocks spine-authoring merges and admissions while any judgment-only publication remains unabsorbed. With that hold, item 4's history check reduces to ancestry plus "every intervening commit is record-only or a verified primary publication", which is checkable and cannot fail by accident.

- **Prior snapshot publications can never be foreign evidence.** A snapshot copy changes the approved blob map, so item 4's identity test always refuses it. Item 2 lists it anyway. Drop it. Only judgment-only publications within one held baseline are reusable. That also removes the recursive replay case where a snapshot turn cites a snapshot turn.

- **Freshness for meaning versus equivalent is over-coupled.** For `equivalent`, only registry bytes matter, and the turn record already binds them. The source-tree segment proof only matters for `meaning`, where impact review can rot. With the enforced hold above, the segment proof becomes a cheap assertion rather than a second verifier. Keep it, but state it as a consequence of the hold, not a standalone mechanism.

- **Ledger citation is underspecified.** The current code stores one evidence ref per registry. The snapshot turn's approves entry should cite its own judgment, with foreign judgment refs living in the absorption ledger of the spec. Say so.

- **The "no owner decision" sentence is false.** See the bootstrap section.

## Replay and provenance

The reuse verifier replays each foreign publication with `derive_tree` at its own candidate. Foreign refs must strictly precede the current base, so the chain is finite and acyclic. Judgment-only projections carry no absorption ledger, so replaying them recurses no further. Memoization on the existing set is adequate. Fail-closed behaviour for missing, returned, uncertain or forged judgments follows from the existing evidence reader once the foreign-turn lookup is routed through `publication_commit`. This part is sound.

## Bootstrap: the design cannot enable itself

The design gates runtime enablement behind an adjudicated amendment to LLR-140/152/153/154/158/167/207 and their TCs. Those rows sit in the very registry file that already carries drift from WI-601, WI-603, the PC patch and LLR-207. Adjudicating the amendment therefore hits the same census refusal. The only exits are either code before governing text, which the design forbids, or an owner exception. A governing exception is genuinely necessary. The design must say so instead of denying it.

Three routes exist, and all three are owner decisions:

1. **One-time combined-scope adjudication under existing code.** Intake queues a single adjudication proposal whose scope is every changed approved row in the drifted registries, superseding the per-owner queued adjudication WIs. The existing census and ledger then pass with zero code change. This merges adjudication ownership once, which the owner must rule on.
2. **Owner-authorized enablement ahead of text.** Ship the mechanism behind a process.toml dial, default off. The owner turns it on for the bootstrap, and the amendment rows ride the first collection.
3. **Owner hand-publication.** Blocked by the same whole-file absorption rule, so not recommended.

## The smaller sound solution

Ask why two owners' drift ever coexists in one registry file. The governing rule already serializes spine authoring but does not require adjudication of registry R before the next spine-authoring merge touching R. Adding that merge-time hold prevents recurrence with one preflight refusal and no new protocol intent. Route 1 above drains the current backlog. Together they resolve the blocker with no new publication carrier, no foreign-evidence verifier and no governing amendment beyond the scheduling rule. The cost is spine-authoring throughput coupled to adjudication latency.

The judgment-only design is the minimal change only if the owner wants concurrent multi-owner drift in one file to remain a supported state. That is a product choice, not a technical one, so name it as the decision to put to the owner.

## What the owner must decide, and what they need not

Needed for this repair:

- Route 1 or route 2 for the bootstrap.
- Whether to prevent recurrence by the merge hold alone or to keep the judgment-only mechanism.

Not needed: the legacy migration window. Nothing here touches it.

## Preparation allowed now

- Write the executable two-owner deadlock reproduction on temporary Git repos.
- Write the merge-time hold refusal and its tests, since both routes need it.
- Hold the intent discriminator and foreign-evidence verifier until the owner chooses, or write them behind a default-off dial with `publication` absent meaning unchanged behaviour. No activation, no snapshot, no primary selection, no merge to main.
