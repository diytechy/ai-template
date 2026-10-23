# WI-851 checkpoint sitting at 5a56d69

## amendment

Eight approved rows moved against their copies, recorded at commit 90ddd6f5f. I read each before and after cell against WI-851's Trust section and Done-when, and against the code and tests at this tip.

Checks I ran:
- `trace.py --strict` exits 0. Its only advisories on these rows (no Form, unclassified) are ones nearly every SR in the registry carries.
- All 102 evidence and test-ref nodes of TC-241, TC-243, TC-278, TC-398 and LLR-359 resolve to an existing test.
- `tests/test_held_status.py`, `tests/test_adjudicate_brief.py` and `tests/test_adjudicate_act.py` pass: 152 run, 0 failed.

Every row changed MEANING: each one retires, narrows, moves or adds an obligation. The rung is released.

I would bless five rows: SR-208, SR-228, LLR-278, LLR-246 and TC-241. Three I would not: LLR-249, TC-243 and TC-278. Each of the three adds a code name to its row text, and TC-278 also has a dangling reference. §0's rule is that an amendment adds no name the rule forbids. LLR-249's own change shows why: the function it names moved module in this lane, so a row pinned to a location went false at the first refactor.

**Consequence for the act.** The three unblessed rows stay drifted, in the design and test-case registries. A snapshot copying those two registries refuses while they drift unread. So the act turn can take the system-requirements registry (SR-208, SR-228) now. The design and test-case registries, which carry LLR-278, LLR-246, TC-241 and the two first approvals below, have to wait until the three re-sit.

- [MEANING+BLESS] SR-208 Requirement, AcceptanceCriteria, Rationale, Coincident, Title -> before: where the dial holds an off-spine registry's rung, the delivered loop refuses any status change it makes there, at its own commits and at merge, and a human's commit is not governed -> after: where the dial holds any snapshotted registry's rung, the delivered harness refuses before landing two things. First, a lane's approval claim, unless it is a CLARITY re-attestation bound to the row's judged text. Second, a marked autonomous commit outside a lane that moves held state. The claim shapes and the cases not judged are enumerated, an unmarked plain trunk commit is not judged, and unreadable inputs refuse by name -> not the same: the domain widens from off-spine registries to all eight snapshotted ones, the actor changes from the loop's writers to any lane, and a bound-text exception enters. Ready to bless:
  - One `shall` governs one decision (a held rung is guarded at landing), with two coordinated refusals.
  - The `Where` fronts a declared feature.
  - No cell names a file.
  - The acceptance is the fit criterion of both refusals, and is fail-closed on unreadable input and an unreadable rung.
  - The unmarked-trunk residual is the owner's ruling 5, which the spec carries.
  - The Rationale says why selected writers are not enough and why the binding exists.
- [MEANING+BLESS] SR-228 AcceptanceCriteria -> before: the recorded act names the verdict for later audit -> after: when supplied, the recorded act names the verdict for later audit -> not the same: an act that names no verdict no longer fails this criterion. Ready to bless. It is the Done-when's ruling ("`intake.py snapshot --verdict` stays optional and recorded"). The permission now rests on the bound accepted verdict, which the first clause still requires ("its recorded verdict names that row as CLARITY", the committed verdict being this repository's record of an adjudication). The audit name is kept wherever it is given.
- [MEANING+BLESS] LLR-278 Detail -> before: the merge applies scope and backing bounds and, through a held-rung clause, refuses a held re-attestation whose act ledger names no accepted CLARITY verdict, reading the dial at trunk's tip -> after: the same bounds with the held clause removed -> not the same: the ledger-based held refusal leaves this row. Ready to bless. The Done-when retires that arm into the lane rule ("LLR-278's held clause ... retires into this one rule"), which LLR-246 now states and TC-241 verifies. The remaining text is byte-identical to what was blessed, and it adds no name.
- [MEANING+BLESS] LLR-246 Detail, Title, SR-Refs -> before: every loop writer and the hook's marker-armed step refuse a held status move at commit, and the slot re-judges every loop lane -> after:
  - the writers refuse only outside a claimed lane;
  - the step judges a squash landing by its lane commits and arms on the marker outside a lane;
  - a lane rider after parent-first judges every lane commit against each parent;
  - the held claim's four shapes and its every-parent rule are defined;
  - the held set is every snapshotted tier;
  - the bound-copy exception has its four conditions;
  - unreadable inputs refuse by name, and the slot's loop-lane rung no longer runs;
  - a row tagged two ways reads MEANING;
  - SR-228 joins its parents.

  -> not the same: the subject moves from loop provenance to lane state, as the spec intends. Ready to bless. Each new sentence is a Done-when clause stated as an observable outcome or refusal. "Every handback commit runs the refusal" and "the refusal fires only outside a claimed lane" agree, and TC-241 now holds the outside-a-lane handback case. No `shall` appears, and no name is added: the new sentences use no symbol.
- [MEANING] LLR-249 Detail -> before: `acceptance_record.committed_status_moves(root, rev)` lists status moves -> after: `held_status.committed_status_moves(root, rev)` lists them -> not the same: the contract now places the function in another module, and an implementation true to the old text fails the new. NOT blessed. The amendment trades one module name for another and adds a name the naming rule forbids. Drop the module qualifier, keeping the approved symbol verbatim, so the row survives the next move.
- [MEANING] TC-243 Method -> before: the history advisory's cases and the pure dial comparison -> after: the same, plus "APPROVAL_RUNGS and the spine rung map live in kitlib/authority, and agent_common re-exports them" -> not the same: a module-location arm enters the verified set. NOT blessed. The added sentence names three code carriers in a TC cell. State the arm without them, for example "the rung maps have one home, which the shared helpers re-export", or leave the arm to LLR-249's trace homes.
- [MEANING] TC-278 Expected and Method -> before: Expected paraphrases LLR-278, including the held CLARITY permission. Method drives the scope, combined, released-rung and retirement cases, and reads the held authority at trunk's tip -> after: Expected is LLR-278's text copied verbatim. Method drops the trunk-tip sentence, and gains the held-tier refusal arms, the ledger-parse refusal, acts on trunk not re-read, and the carrier-path authorization -> not the same: the verified set changes on both sides. NOT blessed, for three findings:
  - (1) **New code names.** The Expected adds `amendment_scope`, and the Method adds `reattested_between`. Both are function names, new to these cells.
  - (2) **A dangling reference.** The Expected now opens "Every such id outside amendment_scope". Its antecedent ("the ids re-attested by the entries whose seq the base does not hold") is a sentence of LLR-278 that the TC did not copy, so the claim cannot be read from the cell.
  - (3) **Verified arms the Expected does not claim.** TC-278 verifies SR-208, SR-228 and LLR-246, but its Expected now claims nothing on the held tier. The held CLARITY permission it used to state lives only in Method. Either claim the held-tier outcome in Expected, or drop SR-208 and LLR-246 from `Verifies`, since TC-241 holds them.

VERDICT: MEANING rows=8

## first-approval

Two lane-added rows await a first approval: LLR-359 and TC-398. They sit under SR-178 and SR-208, both approved. SR-208's amended acceptance requires "an accepted amendment verdict [that] rules that row CLARITY and binds its equal approved-text digest". The spec's Architectural delta declares that digest and its one producer and two readers.

- [APPROVE] LLR-359 -> the obligation:
  - one approved-text digest over a row's nonempty approved cells, with id and Status excluded, so the carrier and an empty versus absent cell do not change it;
  - one judged-text identity line per shown row in the amendment brief;
  - the identities written into the binding at reservation, and kept through the accepted or failed rewrite;
  - a held CLARITY re-attestation actable only when the accepted binding's identity equals the committed row's digest, so that an absent, malformed or unequal identity is refused before launch, naming the row.

  -> what its chain shows:
  - Upward, it decomposes SR-208's bound-text clause, and through the shared cell classes it is SR-178's comparison basis.
  - Sideways, it is the identity and the act turn's refusal. LLR-246 owns the landing rule that reads the same identity, so the two rows do not overlap.
  - Downward, TC-398's fourteen cases hold each clause. That includes the malformed cell at the act turn (`test_a_malformed_identity_cell_refuses_the_held_act_by_row`, which drives `owed_acts` and asserts that the row and its digest are named), the carrier-blind digest, and both outcome rewrites.

  -> why it is ready: a contract in observable inputs, outcomes and refusals. No `shall`, no symbol in its text, and fail-closed on every bad identity. It carries no own Hat-Refs, rightly.
- [APPROVE] TC-398 -> the obligation: the digest's exclusions and invariance, one identity line per shown row, the identities kept through reservation and both outcome rewrites, and a held CLARITY act refused before launch when its text moved or its identity is absent or malformed -> what its chain shows: its Expected is LLR-359's text sentence for sentence, and every evidence node exists and runs among the 152 that pass -> why it is ready: an observable Expected over existing cases, with Integration at Full honest for its git cases.

OUTCOME: APPROVE rows=2

## Returns answered in the lane

```toml
title = "WI-851 spine rework: LLR-249, TC-243 and TC-278 amended without new code names, TC-278's antecedent and held-tier claim; re-sit the three"
workstream = "process"
sr_refs = ["SR-208", "SR-210", "SR-228"]
needs = ["WI-851"]
safety_class = "ordinary"
buildtier = "quick"
```

This is spine text only, and no code change is called for.
1. **LLR-249:** write "committed_status_moves(root, rev) lists status moves ..." without a module qualifier.
2. **TC-243:** restate the added arm without code names, or drop it and leave the location to LLR-249's trace homes.
3. **TC-278:**
   - replace "amendment_scope" and "reattested_between" with plain words (the amendment scope, the re-attestation ledger reader);
   - give "Every such id" its antecedent, for example "Every id re-attested by an act the merge base does not hold";
   - either claim the held-tier outcome in Expected (a held re-attestation lands only under an accepted CLARITY verdict bound to its text, and is otherwise refused by row), or drop SR-208 and LLR-246 from `Verifies`.

Then re-sit LLR-249, TC-243 and TC-278 for the amendment. The five rows blessed here, and the two approved, keep their rulings, because none of these changes touches their text. As noted above, the act copying the design and test-case registries has to wait for that re-sit.

SITTING: JUDGED kinds=amendment;first-approval
