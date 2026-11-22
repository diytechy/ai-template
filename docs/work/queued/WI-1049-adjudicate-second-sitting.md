+++
id = "WI-1049"
title = "adjudicate: the chains waiting after WI-1048, 32 amendments and 25 first acceptances, in one combined sitting"
workstream = "process"
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
sr_refs = ["SR-070", "SR-157", "SR-159", "SR-168", "SR-169", "SR-178", "SR-202", "SR-208", "SR-212", "SR-215", "SR-217", "SR-225", "SR-233", "SR-243"]
needs = []
buildtier = "medium"
safety_class = "adjudication"
brief = "combined"
adjudicates = ["amendment:CMP-006", "amendment:IF-312", "amendment:LLR-041", "amendment:LLR-042", "amendment:LLR-067", "amendment:LLR-080", "amendment:LLR-199", "amendment:LLR-239", "amendment:LLR-244", "amendment:LLR-257", "amendment:LLR-283", "amendment:LLR-293", "amendment:LLR-311", "amendment:LLR-373", "amendment:SR-233", "amendment:SR-243", "amendment:TC-044", "amendment:TC-049", "amendment:TC-067", "amendment:TC-080", "amendment:TC-081", "amendment:TC-195", "amendment:TC-250", "amendment:TC-293", "amendment:TC-332", "amendment:TC-385", "amendment:TC-409", "amendment:TC-410", "amendment:TC-428", "amendment:TC-429", "amendment:TC-435", "amendment:TC-436", "first-acceptance:LLR-393", "first-acceptance:LLR-394", "first-acceptance:LLR-395", "first-acceptance:LLR-396", "first-acceptance:LLR-397", "first-acceptance:LLR-398", "first-acceptance:TC-455", "first-acceptance:TC-456", "first-acceptance:TC-457", "first-acceptance:TC-458", "first-acceptance:TC-459", "first-acceptance:TC-460", "first-acceptance:TC-461", "first-acceptance:TC-462", "first-acceptance:TC-463", "first-acceptance:TC-464", "first-acceptance:TC-465", "first-acceptance:TC-466", "first-acceptance:TC-467", "first-acceptance:TC-468", "first-acceptance:TC-469", "first-acceptance:TC-470", "first-acceptance:TC-471", "first-acceptance:TC-474", "first-acceptance:TC-475"]
priority = 2
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator: the second
automated adjudication sitting the operator ruled (queue-drill HANDOFF §3.6,
its first question: "Yes, run through antigravity cli (agy) model neon
high"; §0 step 2). The first sitting, WI-1047, recorded its verdict, but its
act was refused: LLR-080 and LLR-373 drifted in the design registry the act
copies and the verdict did not bless them (SR-207). WI-1048 answered every
MEANING and RETURN finding. This sitting judges everything still owed,
WI-1047's 20 blessed rows again among them, so that one verdict yields one
act. It runs, and its act is taken, before F-3 (WI-1023) merges: F-3 amends
the accepted text of further design and test-case rows, which would drift in
the registries this act copies.

**Scope.** Every row `docs/ratify/CURRENT.md` lists under "Waiting for
automated adjudication" at `6eff30f85`, fourteen chains: each drifted
`Accepted` row as an `amendment:` token (TC-049, TC-409, TC-410, TC-428 and
TC-429 changed only their routed `Verifies` cell, as at WI-1047), each
`Drafted` SR, LLR or TC as a `first-acceptance:` token, and the two amended
`Accepted` off-spine rows the census names (IF-312, CMP-006's `Notes`) as
`amendment:` tokens. Since WI-1047: TC-081, LLR-257 and TC-250 are new
amendments (WI-1048, WI-1042), and TC-468 to TC-471, TC-474 and TC-475 new
first acceptances (WI-1042, WI-1048). The first-acceptance brief covers SR,
LLR and TC rows only, so `Drafted` interface rows stay `Drafted`.

**How it runs** (HANDOFF §3.7, and WI-1047's record). As at WI-1047: the
kit's adjudication launcher needs a claimed lane and an adjudicator route
enabled in `docs/agents.toml` and `docs/agents-enabled`, and no `agy` or
Gemini route is registered there (adding one is the operator's consent
change). So the coordinator runs the kit's own pieces on trunk and only the
launch differs: the brief composed by `adjudicate_brief.compose` (through
`scripts/coordinator/compose_lane.py`), the verdict path reserved and the
request bound as the entry point does (`reserve_verdict`,
`bind_requested`), one Gemini Neon session at high effort through the
Antigravity CLI in plan mode, its reply kept verbatim as the verdict,
`record_outcome` deciding recorded or failed, and the act
`adjudicate_act.compose_act` derives from the recorded verdict, run with
this repository's path to `intake.py`. One session, never fanned out
(PROCESS.md §6). The adjudicator's family (Google) differs from the
authors' and builders' (OpenAI, Anthropic).

## Done-when

- [ ] The verdict is recorded beside its binding under
      `docs/reviews/wi-1049-adjudicate-second-sitting/`, as the adjudicator
      returned it, and `record_outcome` reads it recorded.
- [ ] The act `compose_act` derives is taken: the CLARITY and
      `MEANING+BLESS` amendments re-accepted, then the ACCEPT rows flipped
      with their copies, each in its own commit; `left_owed` reads nothing.
- [ ] Each MEANING amendment and RETURN row is listed in the Deliverable
      with its finding, and its follow-up is filed or named.
- [ ] `docs/ratify/CURRENT.md` regenerates with no chain left that this
      sitting judged and accepted.
