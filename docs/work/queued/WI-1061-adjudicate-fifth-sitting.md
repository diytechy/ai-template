+++
id = "WI-1061"
title = "adjudicate: WI-1058's answer to the fourth sitting, SR-251's chain whole, in one first-acceptance sitting"
workstream = "process"
specref = "docs/archive/work/complete/WI-1058-answer-wi-1057-verdict.md"
sr_refs = ["SR-251"]
needs = []
buildtier = "medium"
safety_class = "adjudication"
brief = "first-acceptance"
adjudicates = ["LLR-406", "SR-251", "TC-483"]
priority = 2
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator: the fifth
automated adjudication sitting (queue-drill HANDOFF §0 step 2). It runs on
the operator's standing ruling for these sittings (HANDOFF §3.6, its first
question: "Yes, run through antigravity cli (agy) model neon high"). It
judges what WI-1058 (the specref) left owed: the fourth sitting's two
returns, answered.

**Scope.** Every `Drafted` SR, LLR or TC is in its scope:
SR-251 and TC-483, as WI-1058 rewrote them, and LLR-406, unchanged. No
spine row drifts from its recorded copy at `6925769b1`
(`baseline_snapshot.refresh_ledger`), so the sitting is a first-acceptance
one, not combined. IF-312 and CMP-006 still drift in their off-spine
registries, but the amendment brief shows no off-spine row: filed as
amendment tokens alone, they leave its section empty, and the compose
refuses (it did, at the first filing of this row). They stay owed, as at
every sitting so far.

**Why LLR-406 is judged again.** The fourth sitting ruled LLR-406 ACCEPT,
and its flip has been held under WI-1057's verdict since then, because its
parent SR-251 was returned (the commit hook's parent-first step). TC-483
verifies both SR-251 and LLR-406. So TC-483 can be flipped only with
LLR-406, or after it. Judging the chain whole lets one act flip all three
together, which the parent-first rule allows. If this sitting accepts
LLR-406, its act takes the flip, and WI-1057's verdict then reads it as
taken. If this sitting returns LLR-406, its flip stays owed under
WI-1057's verdict once SR-251 is accepted, and TC-483 waits on it.

No routed traced change is owed.

**How it runs** (HANDOFF §3.7; WI-1057's Context and Deliverable). The
kit's own pieces run on trunk, with the launch by hand:
1. `adjudicate_brief.compose` composes the brief, through
   `scripts/coordinator/compose_lane.py`.
2. The verdict path is reserved and the request bound, as the entry point
   does.
3. One Gemini Neon session at high effort runs through the Antigravity
   CLI in plan mode. Its reply is kept verbatim as the verdict, and
   `record_outcome` records it.
4. `adjudicate_act.compose_act` derives the act. Its first snapshot is
   tested read-only before it is taken. A flip the parent-first rule would
   refuse is left out of the act, as at WI-1057 (taking less than listed,
   never more).

One session, never fanned out (PROCESS.md §6).

## Done-when

- [ ] The verdict is recorded beside its binding under
      `docs/reviews/wi-1061-adjudicate-fifth-sitting/`, as the adjudicator
      returned it, and `record_outcome` reads it recorded.
- [ ] The act `compose_act` derives is taken.
      If its first snapshot is refused over an unblessed row, the
      operator's standing revert ruling applies (HANDOFF §0 step 2); a
      refusal of another kind goes to the operator.
- [ ] Each RETURN row is listed in the Deliverable
      with its finding, and its follow-up is filed or named.
