# WI-847 amendment adjudication: 001 at 7825c62

Anchor: `docs/archive/last_approved` (both registries copied 2026-10-10, commit 2b9817a2).
Question judged: did each amended cell change the row's MEANING or only its CLARITY?

- [MEANING] LLR-045 Detail -> managed review dispatch: a declared policy of N schedules N reviewers; a broken prompt map fails preflight; no enable-list keeps legacy behaviour; queued phases are always named by the caller, an empty list being an empty round -> all of that unchanged, PLUS a new arm: `narrow_reviewer_prompt` renders a narrow round's brief by strictly filling the phase override or the shipped reviewer template through `prompts.fill`, with the round delta as the reading scope and round facts that state the shared narrow range sentence and name the findings file as a claim under judgement; a template with missing or unknown slots refuses rather than yielding a full-lane or unfilled scope; the rendered brief carries no attended recording facts and leaves the reviewer to commit its own verdict -> not the same: a correct implementation of the old text has no narrow renderer at all, and it fails the new delta-scope, shared-sentence and strict-refusal obligations.
- [MEANING] TC-082 Expected + Method -> Expected: scheduling matches policy, bad prompts fail preflight, unmanaged mode stays legacy. Method: drive the policy 0/1/2, prompt-map, redaction, logging, verdict and unmanaged cases, and treat the queue's phases as a required argument -> both cells unchanged, PLUS: render the narrow brief with prior findings; compare its delta scope and narrow range sentence with the attended narrow render; confirm no unfilled slot and no attended recording facts; confirm an override lacking the range slots refuses -> not the same: a new acceptance condition and new test obligations were added in both cells.

## Would I bless the new text? (LLR/TC rung: released)

Yes, both rows. I judged them against the code as it stands, per the owner's 2026-10-10 split:

- **No overclaim.** LLR-045's new arm describes what `agent_brief.narrow_reviewer_prompt` does. It does not claim the loop schedules a narrow round. Scheduling is the split row's, WI-884, and neither cell promises it. Against `agent_brief.py`, every clause holds:
  - the fill is strict, through `prompts.fill(prompts.REVIEWER, ...)`, with the phase override or else the shipped template;
  - `{trunk}`/`{head}` are set to the round's base and sha, so the reading scope is the delta;
  - `{round_facts}` states `narrow_scope_line`, which names the findings file as "a claim under judgement";
  - a slot mismatch raises `PromptError`;
  - no attended recording facts are added.
- **Up the chain.** SR-154 asks that each review the policy requires come from an independent session. A narrow round answering earlier findings is one such review. Its brief must read the right scope and must not trust the findings it judges. That is SR-154's obligation, decomposed.
- **Across the chain.** The narrow range sentence has one home, `narrow_scope_line`, shared with the attended `review_brief` render. The two rows do not overlap.
- **Down the chain.** TC-082's new clauses map onto the new arm. `test_the_loop_narrow_round_renders_its_delta_through_the_one_render` checks the delta scope, the shared sentence (which also appears in the attended render), the absence of recording facts, and that no slot is left unfilled. `test_a_loop_narrow_round_refuses_an_override_that_cannot_carry_its_range` checks the refusal. The "unknown slot" half of the refusal rests on `prompts.fill`'s own strictness, which is verified at its own row. In this session, `tests/test_review_brief.py -k "narrow or new_slot"` gave 5 passed, and the LLR-045 policy, prompt-map, redaction, legacy and queue cases gave 8 passed.
- **Wording.** The LLR names symbols, which is this tier's job, and contains no `shall`. The TC's conditions are observable.

One minor wording note, which does not send the row back: "builds a narrow round" reads more naturally as "builds a narrow round's brief". The rest of the arm, "by strictly filling ... template", makes clear that a brief is meant, and no scheduling is implied.

VERDICT: MEANING rows=2
