# WI-850 first-approval sitting at ab4b6d8

## first-approval

This re-sits SR-224 after sitting 001 returned it. Commit ab4b6d8c2 answers both of 001's findings.

**Finding (1), the perspective record, is closed.** `docs/plans/WI-850/sr-224.perspectives.toml` covers SR-224 under SN-005, and `hats.py record ... --check --strict` reports no findings when I run it. FIRST-RUN-ADOPTER produced the row, which matches its `Hat-Refs`, and every other applicable hat carries a no-finding I judge adequate. The row neither writes durable state, adds a rendered surface, nor touches an authority boundary, and TC-291 already holds both outcomes.

**Finding (2) is answered in substance but not yet in form.** The Requirement now reads: "The skill descriptions the kit ships are at or above the declared description floor, and if a skill's description is shorter than that floor, then the kit's skills-index check shall fail, naming that skill." Decision D-002 records why it took this shape. Terra's first wording put the shipped-skills clause inside the If-then's consequent, where it read as conditional. My own example in 001 held two `shall`s, which this repository's one-`shall` form rule reports. So the coordinator kept one `shall` and stated the shipped-skills obligation as an indicative ahead of the If-then.

`trace.py --strict` exits 0, with only the advisories nearly every SR carries.

- [RETURN] SR-224 -> the obligation it means to impose: the skill descriptions the kit ships clear the declared floor, and the skills-index check fails, naming the skill, on any description under it -> what its chain shows: LLR-281 and TC-291 (both Approved, unchanged) hold both arms. LLR-281 states one floor and the named refusal, and TC-291's case (b) runs the shipped set. The derivation and the record are now complete -> why it is not ready: the shipped-skills obligation is still outside the row's obligation. "Are at or above" is a statement of fact. It sits in the Requirement, but before and outside the one `shall`, so a reader cannot tell from the cell's own grammar whether it binds or merely describes. The repository's form rule names exactly that defect: a statement of fact in normative text, where a reader cannot tell which part is binding. The one-`shall` rule exists to catch two obligations in one row, and stating the second without `shall` satisfies the rule's letter while defeating its purpose. Both clauses are one decision (the description floor, and the check that holds every skill to it), so the remedy is not a split. It is one `shall` that governs both, in the coordinated-response form this registry already uses for compound obligations (SR-244's Requirement is one example). The miss is partly mine: 001's example wording invited the two-`shall` form that the lane then had to work around.

OUTCOME: RETURN rows=1

## Returns answered in the lane

```toml
title = "WI-850 spine rework: SR-224's Requirement with both floor clauses under its one shall; re-sit SR-224"
workstream = "process"
sr_refs = ["SR-224"]
needs = ["WI-850"]
safety_class = "ordinary"
buildtier = "quick"
```

This is one cell of spine text. No code change and no record change are called for, because the perspective record stands.
1. **SR-224's Requirement:** state both clauses under one `shall`, for example: "The kit shall hold every skill description to the declared description floor: the descriptions it ships are at or above it, and its skills-index check fails, naming the skill, on any description shorter than it." The failing case becomes a response qualifier after the `shall`, which is its honest place here, since what the row obliges is the floor, not a fault-triggered reaction alone. The acceptance, the Rationale, LLR-281 and TC-291 stay as they are, and the record needs no rewrite because the row's subject and lens are unchanged.

Then re-sit SR-224 for first approval, still as the Done-when's first act.

SITTING: JUDGED kinds=first-approval
