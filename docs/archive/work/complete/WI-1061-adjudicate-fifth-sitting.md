+++
id = "WI-1061"
title = "adjudicate: WI-1058's answer to the fourth sitting, SR-251's chain whole, in one first-acceptance sitting"
workstream = "process"
specref = ""
sr_refs = ["SR-251"]
needs = []
buildtier = "medium"
safety_class = "adjudication"
brief = "first-acceptance"
adjudicates = ["LLR-406", "SR-251", "TC-483"]
priority = 2
+++

## Deliverable

Run on trunk by the queue drill's coordinator on 2026-11-23. The fifth
adjudication sitting judged SR-251's chain whole, the three rows its
`adjudicates` names (Gemini Neon, 321 seconds, one session). Its verdict
(`docs/reviews/wi-1061-adjudicate-fifth-sitting/001-ADJUDICATE-0385b75.md`,
`bba8aeac3`) was recorded by `record_outcome` (`4e3e9bf4b`). It authorizes
no act, and `compose_act` reads "owes no act".

- **Returned, still `Drafted`: SR-251, LLR-406 and TC-483.**
  - SR-251 scopes the rewrite to every test case while LLR-406 says live
    cases, and it states no all-or-nothing write although it carries the
    integrity-recoverability concern.
  - LLR-406 does not say what happens outside its live scope, gives a
    keyless case a key unconditionally (a keyless case that no declaration
    names stays as it is), and states no atomic replacement.
  - TC-483 verifies none of those three.
  Follow-up: WI-1062, filed with this close.
- **LLR-406's flip held under WI-1057's verdict is void.** The fourth
  sitting accepted LLR-406's text, and this sitting, judging the same text,
  returned it. No act takes the flip from WI-1057's verdict; LLR-406's flip
  comes from the sitting that next judges its chain. (This corrects the
  Context's last sentence on a return, written before the verdict.)
- **The verdict file, and one change to Neon's reply.** The coordinator's
  preface was the combined sittings' one. It asked the reply to open with
  its `## <kind>` heading and close with a `SITTING:` line, which a
  single-kind verdict does not carry, and `verdict_refusal` refused the
  reply as returned. The coordinator removed those two wrapper lines and
  nothing else; every ruling, hat, stopping-boundary and Dispositions line
  is as returned (`bba8aeac3`'s message gives the removed lines exactly). A
  single-kind sitting's preface now asks for the brief's own format
  (queue-drill HANDOFF §9).
- **The row's first filing** named IF-312 and CMP-006 as amendment tokens
  in a combined brief. The amendment brief shows no off-spine row, so with
  no spine drift its section was empty and the compose refused. The row was
  corrected to a first-acceptance sitting with bare ids (`0385b759e`).
  IF-312 and CMP-006 still drift in their off-spine registries, owed as at
  every sitting so far.

`docs/ratify/CURRENT.md` still waits on one chain, SR-251.

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

- [x] The verdict is recorded beside its binding under
      `docs/reviews/wi-1061-adjudicate-fifth-sitting/`, as the adjudicator
      returned it, and `record_outcome` reads it recorded.
- [x] The act `compose_act` derives is taken.
      If its first snapshot is refused over an unblessed row, the
      operator's standing revert ruling applies (HANDOFF §0 step 2); a
      refusal of another kind goes to the operator.
- [x] Each RETURN row is listed in the Deliverable
      with its finding, and its follow-up is filed or named.
