+++
id = "WI-1063"
title = "adjudicate: WI-1059's two amendments and SR-251's chain as WI-1062 answered it, in one combined sitting"
workstream = "process"
specref = ""
sr_refs = ["SR-231", "SR-251"]
needs = []
buildtier = "medium"
safety_class = "adjudication"
brief = "combined"
adjudicates = ["amendment:LLR-338", "amendment:TC-368", "first-acceptance:LLR-406", "first-acceptance:SR-251", "first-acceptance:TC-483"]
priority = 2
+++

## Deliverable

Run on trunk by the queue drill's coordinator on 2026-11-23. The sixth
combined adjudication sitting judged the five rows its `adjudicates` names
(Gemini Neon, 237 seconds, one session). Its verdict
(`docs/reviews/wi-1063-adjudicate-sixth-sitting/001-ADJUDICATE-6a585b4.md`,
`e10a261cb`) was recorded by `record_outcome` (`f16f4e361`), and the act it
derives is taken whole. No operator ruling was needed: every amendment was
blessed, and the act's first snapshot was tested read-only and read no
refusal.

- **Re-accepted (`76192dab6`), both MEANING+BLESS:** LLR-338 (the derived
  act's waiting flips, WI-1059) and TC-368.
- **Accepted (`43f711b6d`):** SR-251, LLR-406 and TC-483, SR-251's chain as
  WI-1062 answered the fifth sitting, flipped together in one commit, as
  the parent-first rule allows. LLR-406's flip is taken from this verdict,
  which judged its current text; the flip once held under WI-1057's verdict
  was void after the fifth sitting's return.
- **Returned:** none. No follow-up is owed.
- **Not shown:** IF-312 and CMP-006 still drift in their off-spine
  registries, and IF-296 and IF-308 stay `Drafted`; the brief shows no
  off-spine row.

`compose_act` over this verdict and over WI-1057's now reads no act owed.
`docs/ratify/CURRENT.md` reads: no spine row differs from its recorded
copy, and no row awaits a first acceptance.

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator: the sixth
automated adjudication sitting (queue-drill HANDOFF §0 step 2). It runs on
the operator's standing ruling for these sittings (HANDOFF §3.6, its first
question: "Yes, run through antigravity cli (agy) model neon high"). It
judges what WI-1059 and WI-1062 (the specref) left owed.

**Scope.** Every spine row whose accepted text drifts from its recorded
copy at `4279a7c33` (`baseline_snapshot.refresh_ledger`), each as an
`amendment:` token: WI-1059's LLR-338 (`detail`) and TC-368 (`method` and
`expected`). Every `Drafted` SR, LLR or TC is a `first-acceptance:` token:
SR-251's chain, SR-251, LLR-406 and TC-483, as WI-1062 rewrote it after
the fifth sitting returned it whole. No routed traced change is owed.

IF-312 and CMP-006 still drift in their off-spine registries, and IF-296
and IF-308 (WI-1059's rewrites) are `Drafted` interface rows. The brief
shows no off-spine row, so none is a token; all stay owed, as at every
sitting so far.

**The act.** If this sitting blesses LLR-338 and accepts LLR-406, both sit
in the design registry. The whole-file copy (until WI-1060 lands) then
records both, and the first-acceptance act flips SR-251, LLR-406 and
TC-483 together, which the parent-first rule allows. A row left
unblessed in a registry the act copies makes the snapshot refuse. The
operator's standing revert ruling then applies (HANDOFF §0 step 2). With
WI-1059 merged, the derived act no longer lists a flip whose parent stays
`Drafted`. It names such a flip as waiting instead.

**How it runs** (HANDOFF §3.7; WI-1057's Context and Deliverable). The
kit's own pieces run on trunk, with the launch by hand:
1. `adjudicate_brief.compose` composes the brief, through
   `scripts/coordinator/compose_lane.py`.
2. The verdict path is reserved and the request bound, as the entry point
   does.
3. One Gemini Neon session at high effort runs through the Antigravity
   CLI in plan mode, with a combined sitting's preface. Its reply is kept
   verbatim as the verdict, and `record_outcome` records it.
4. `adjudicate_act.compose_act` derives the act. Its first snapshot is
   tested read-only before it is taken.

One session, never fanned out (PROCESS.md §6).

## Done-when

- [x] The verdict is recorded beside its binding under
      `docs/reviews/wi-1063-adjudicate-sixth-sitting/`, as the adjudicator
      returned it, and `record_outcome` reads it recorded.
- [x] The act `compose_act` derives is taken, each part in its own commit.
      If its first snapshot is refused over an unblessed row, the
      operator's standing revert ruling applies (HANDOFF §0 step 2); a
      refusal of another kind goes to the operator.
- [x] Each MEANING amendment and RETURN row is listed in the Deliverable
      with its finding, and its follow-up is filed or named.
