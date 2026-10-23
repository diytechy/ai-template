# WI-850 first-approval sitting at 4c842bc

## first-approval

One row awaits a first approval: SR-224. Its children have stood `Approved` beneath it since WI-615. LLR-281 refuses a description under the floor by name, and TC-291 drives that refusal and the shipped set. Settling this chain is the first item of WI-850's Done-when. I read SR-224 against:
- its parent SN-005 (Approved);
- its boundary B-05, the packaged deliverable;
- the FIRST-RUN-ADOPTER entry in the roster (`hats.py list`);
- LLR-281 and TC-291, whose two evidence cases exist in `tests/test_skills_index.py`.

`trace.py --strict` exits 0. Its only SR-224 advisories (no Form, unclassified) are ones nearly every SR in the registry carries.

The row is close, and most of it is sound:
- The Requirement is an `If … then` on a fault condition, with the response after the `shall`.
- The threshold is a declared floor, whose value and unit (100 characters) LLR-281 carries.
- No cell names a file.
- It is honestly labelled DERIVED. The Rationale argues the lens against that hat's own `listens_for` (guidance an adopter's agent never reads, usable only with undocumented knowledge), names the rejected alternative (a reviewer's judgement of every description) and feeds back to SN-005.

It goes back for two findings, both cheap and needing no code.

- [RETURN] SR-224 -> the obligation: if a skill's description is shorter than the declared floor, the kit's skills-index check fails, naming that skill. Its acceptance adds that a skill at the floor passes and is not named, and that the kit's shipped skills clear the floor -> what its chain shows: LLR-281 decomposes the refusal exactly (one declared floor, one SHORT line per skill, exit 1 at the check, the regenerating path left total), and TC-291 holds both acceptance arms: (a) the refusal and (b) the shipped set. The derivation itself is sound -> why it is not ready, two findings:
  - (1) **No perspective record.** No `*.perspectives.toml` in the repository covers SR-224 (a `git grep` over every record finds none). The row's `Hat-Refs` says which lens produced it. Only a record can say that every other applicable hat was weighed and found nothing, and `hats.py record ... --check` is the instrument the adjudicator reads. Derived SRs in WI-957, WI-958, WI-960 and WI-961 were held to the same rule: each was returned, or approved only once its record existed. Write one for SR-224 with a `no_finding` per applicable hat, and it must pass `--check --strict`.
  - (2) **The acceptance carries an obligation the Requirement does not state.** "The kit's shipped skills clear the floor" is an obligation on the shipped skills' descriptions, not a fit criterion of the check failing. A check that fails on short descriptions is satisfied whether or not any shipped skill is short. An acceptance cell measures its Requirement; it cannot mint a second obligation. TC-291 (Approved) verifies that clause against SR-224 through its case (b), so dropping the clause would orphan a verified arm. Widen the Requirement to state it instead: the skill descriptions the kit ships are at or above the floor. That leaves the acceptance as the fit criterion of both, and TC-291 unchanged.

OUTCOME: RETURN rows=1

## Returns answered in the lane

```toml
title = "WI-850 spine rework: SR-224's perspective record and its Requirement stating the shipped-skills floor; re-sit SR-224"
workstream = "process"
sr_refs = ["SR-224"]
needs = ["WI-850"]
safety_class = "ordinary"
buildtier = "quick"
```

This is spine text, plus one record file, and no code change is called for.
1. **The perspective record:** run `python project-trajectory/scripts/hats.py record <the lane's record stem>.perspectives.toml --row SR-224 --by <who>` and write a `no_finding` for each applicable hat that produced nothing. It must pass `--check --strict`.
2. **SR-224's Requirement:** add the shipped-skills obligation, for example "…shall fail, naming that skill, and the skill descriptions the kit ships shall be at or above that floor". The acceptance, LLR-281 and TC-291 stay as they are.

Then re-sit SR-224 for first approval, still as the Done-when's first act and before any code commit. The fallback the plan names, returning LLR-281 and TC-291 to `Drafted`, stays open to the lane if it prefers it. This verdict does not choose it, because the row is two small edits from ready.

SITTING: JUDGED kinds=first-approval
