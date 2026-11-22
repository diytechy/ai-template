+++
id = "WI-1047"
title = "adjudicate: the chains waiting after F-2, 29 amendments and 19 first acceptances, in one combined sitting"
workstream = "process"
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
sr_refs = ["SR-070", "SR-157", "SR-159", "SR-168", "SR-169", "SR-178", "SR-202", "SR-208", "SR-212", "SR-215", "SR-225", "SR-233", "SR-243"]
needs = []
buildtier = "medium"
safety_class = "adjudication"
brief = "combined"
adjudicates = ["amendment:CMP-006", "amendment:IF-312", "amendment:LLR-041", "amendment:LLR-042", "amendment:LLR-067", "amendment:LLR-080", "amendment:LLR-199", "amendment:LLR-239", "amendment:LLR-244", "amendment:LLR-283", "amendment:LLR-293", "amendment:LLR-311", "amendment:LLR-373", "amendment:SR-233", "amendment:SR-243", "amendment:TC-044", "amendment:TC-049", "amendment:TC-067", "amendment:TC-080", "amendment:TC-195", "amendment:TC-293", "amendment:TC-332", "amendment:TC-385", "amendment:TC-409", "amendment:TC-410", "amendment:TC-428", "amendment:TC-429", "amendment:TC-435", "amendment:TC-436", "first-acceptance:LLR-393", "first-acceptance:LLR-394", "first-acceptance:LLR-395", "first-acceptance:LLR-396", "first-acceptance:LLR-397", "first-acceptance:LLR-398", "first-acceptance:TC-455", "first-acceptance:TC-456", "first-acceptance:TC-457", "first-acceptance:TC-458", "first-acceptance:TC-459", "first-acceptance:TC-460", "first-acceptance:TC-461", "first-acceptance:TC-462", "first-acceptance:TC-463", "first-acceptance:TC-464", "first-acceptance:TC-465", "first-acceptance:TC-466", "first-acceptance:TC-467"]
priority = 2
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, on the
operator's ruling (queue-drill HANDOFF §3.6, its first question: "Yes, run
through antigravity cli (agy) model neon high"). One automated adjudication
sitting after F-2 (WI-1022) merges and before F-3's (WI-1023) batch act,
since that act is refused while a registry it copies holds drifted accepted
text it does not name (SR-207). It also clears `docs/ratify/CURRENT.md`'s
waiting block and lets WI-1038 start once LLR-395 is accepted.

**Scope.** Every row `docs/ratify/CURRENT.md` listed under "Waiting for
automated adjudication" at `6915cde7d`, thirteen chains: each drifted
`Accepted` row as an `amendment:` token, each `Drafted` SR, LLR or TC as a
`first-acceptance:` token, and the two amended `Accepted` off-spine rows the
census names (IF-312, CMP-006's `notes`) as `amendment:` tokens. The
first-acceptance brief covers SR, LLR and TC rows only, so the `Drafted`
interface rows (IF-325, IF-326) stay `Drafted`; `Drafted` rows do not block
F-3's act.

**How it runs** (HANDOFF §3.7). The kit's adjudication launcher,
`coordinator_adjudicate.py`, needs a claimed lane and an adjudicator route
enabled in `docs/agents.toml` and `docs/agents-enabled`, and no `agy` or
Gemini route is registered there (adding one is the operator's consent
change). So the coordinator runs the kit's own pieces on trunk and only the
launch differs: the brief composed by `adjudicate_brief.compose` (through
`scripts/coordinator/compose_lane.py`), the verdict path reserved and the
request bound as the entry point does (`reserve_verdict`,
`bind_pending(exclusive=True)`), one Gemini Neon session at high effort
through the Antigravity CLI in plan mode, its reply kept as the verdict,
`record_outcome` deciding recorded or failed, and the act
`adjudicate_act.compose_act` derives from the recorded verdict. One session,
never fanned out (PROCESS.md §6). The adjudicator's family (Google) differs
from the authors' and builders' (OpenAI, Anthropic).

## Done-when

- [ ] The verdict is recorded beside its binding under
      `docs/reviews/wi-1047-adjudicate-f2-sitting/`, as the adjudicator
      returned it, and `record_outcome` reads it recorded.
- [ ] The act `compose_act` derives is taken: the CLARITY and
      `MEANING+BLESS` amendments re-accepted, then the ACCEPT rows flipped
      with their copies, each in its own commit; `left_owed` reads nothing.
- [ ] Each MEANING amendment and RETURN row is listed in the Deliverable
      with its finding, and its follow-up is filed or named.
- [ ] `docs/ratify/CURRENT.md` regenerates with no chain left that this
      sitting judged and accepted.
