+++
id = "WI-1057"
title = "adjudicate: WI-1056's and the leftovers' rows, 11 amendments and 18 first acceptances, in one combined sitting"
workstream = "process"
specref = ""
sr_refs = ["SR-036", "SR-052", "SR-157", "SR-159", "SR-202", "SR-206", "SR-212", "SR-221", "SR-248", "SR-249", "SR-250", "SR-251"]
needs = []
buildtier = "medium"
safety_class = "adjudication"
brief = "combined"
adjudicates = ["amendment:CMP-006", "amendment:IF-312", "amendment:LLR-239", "amendment:LLR-243", "amendment:LLR-244", "amendment:LLR-263", "amendment:LLR-398", "amendment:SR-212", "amendment:SR-221", "amendment:TC-239", "amendment:TC-258", "first-acceptance:LLR-403", "first-acceptance:LLR-405", "first-acceptance:LLR-406", "first-acceptance:LLR-408", "first-acceptance:SR-248", "first-acceptance:SR-249", "first-acceptance:SR-250", "first-acceptance:SR-251", "first-acceptance:TC-480", "first-acceptance:TC-481", "first-acceptance:TC-482", "first-acceptance:TC-483", "first-acceptance:TC-484", "first-acceptance:TC-485", "first-acceptance:TC-500", "first-acceptance:TC-501", "first-acceptance:TC-504", "first-acceptance:TC-508"]
priority = 2
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator: the fourth
automated adjudication sitting (queue-drill HANDOFF §0 step 2). It runs on
the operator's standing ruling for these sittings (HANDOFF §3.6, its first
question: "Yes, run through antigravity cli (agy) model neon high"). It
judges what WI-1056 and the drill's leftovers (WI-1051 to WI-1054) left
owed.

**Scope.** Every row whose accepted text drifts from its recorded copy at
`b819f6dcb` (`baseline_snapshot.refresh_ledger`), each as an `amendment:`
token:
- WI-1056's re-landed and amended rows: SR-212, SR-221, LLR-244, LLR-263,
  TC-239 and TC-258.
- WI-1052's LLR-239 and LLR-243.
- WI-1053's LLR-398, whose `test_refs` also routes a traced change (TC-504
  added).
- IF-312's and CMP-006's off-spine drift, as at the earlier sittings.

Every `Drafted` SR, LLR or TC is a `first-acceptance:` token:
- WI-1056's SR-248 (rewritten), SR-249 to SR-251, LLR-403, LLR-405,
  LLR-406, LLR-408, and TC-480 to TC-485.
- WI-1052's TC-500 and TC-501.
- WI-1053's TC-504.
- WI-1054's TC-508.

No other routed traced change is owed.

**How it runs** (HANDOFF §3.7; WI-1055's Context and Deliverable). The
kit's own pieces run on trunk, with the launch by hand:
1. `adjudicate_brief.compose` composes the brief, through
   `scripts/coordinator/compose_lane.py`.
2. The verdict path is reserved and the request bound, as the entry point
   does.
3. One Gemini Neon session at high effort runs through the Antigravity
   CLI in plan mode. Its reply is kept verbatim as the verdict, and
   `record_outcome` records it.
4. `adjudicate_act.compose_act` derives the act. Its first snapshot is
   tested read-only before it is taken.

One session, never fanned out (PROCESS.md §6).

## Done-when

- [ ] The verdict is recorded beside its binding under
      `docs/reviews/wi-1057-adjudicate-fourth-sitting/`, as the adjudicator
      returned it, and `record_outcome` reads it recorded.
- [ ] The act `compose_act` derives is taken, each part in its own commit;
      or, if its first snapshot is refused, the choice is put to the
      operator.
- [ ] Each MEANING amendment and RETURN row is listed in the Deliverable
      with its finding, and its follow-up is filed or named.
