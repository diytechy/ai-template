+++
id = "WI-1071"
title = "WI-1068's verdict answered: four rows restore dropped clauses, three test cases fixed, LLR-423's overlap resolved"
workstream = "process"
specref = "docs/reviews/wi-1068-adjudicate-eighth-sitting/001-ADJUDICATE-fbd50be.md"
sr_refs = ["SR-022", "SR-046", "SR-070", "SR-178", "SR-224", "SR-229"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, to answer
the eighth automated adjudication sitting's verdict (WI-1068, sitting A,
Gemini Neon; the specref): its second and third `## amendment`
dispositions and its three `## first-acceptance` dispositions. They are
one row because each is small and text-led and none waits on another.
WI-1070 answers the first amendment disposition (the brief's gap).

**Dropped clauses (MEANING, not blessed; each still `Accepted`, owed at
its recorded text).** WI-1024's slice 1 rewrote these rows without code
names, and the sitting found the rewrite dropped obligations:
1. LLR-047: no interpolation in the run-capability parse; capability names
   keep their case; an orphan `.desc` and an empty-value command are
   dropped.
2. LLR-039: a freshness failure on a document edit and on a missing bundle
   file; the legacy opt-out sentinel; JSON-quoted YAML scalars (the rewrite
   says "quoted").
3. LLR-199: the unplaced design rows in the counted unplaced table; the
   staleness header; the trunk regeneration wiring (beside adopting
   LLR-403's placement).
4. LLR-281: the `SHORT` output marker and that the floor is checked first.

For each clause the builder reads the code: a clause the code still
enforces is restated in the row, without code names, unless an accepted
spine row already states it (named in the Deliverable; an interface row is
off-spine and no sitting reads it, so it is not such a home); a clause the
code no longer enforces is reported, and the row's text says what holds.
These rows also carry a `constrains` link WI-1070's brief must show, so
their re-sitting follows both rows.

**TC-398 (MEANING, not blessed).** LLR-359 now says an unequal-identity
refusal names the row and both digests; TC-398's method and expected check
only that it names the row. TC-398 states and a test asserts both digests.

**TC-530 (RETURN; `Drafted`).** Its method adds `constrains` and
`dimensions` (an accepted cell) to one design row in one commit, which
masks whether a `constrains`-only change routes to adjudication with no
accepted cell moved. Its method, expected and tests separate the two.
LLR-420 was accepted by this sitting and is not amended here.

**TC-571 (RETURN; `Drafted`).** Its expected says a row's other moved
trace cells show under the label owing no act, but its method moves them
only on a row that lists no chain. Its method names a rendered row that
also moves another trace cell (the test that drives the three labels
together already does). LLR-484 was accepted and is not amended here.

**LLR-423 and TC-533 (RETURN; `Drafted`).** LLR-423 states that the
coordinator guard identifies a claim's caller by the agent tool's exported
session variable; the accepted LLR-300 states the same, and TC-316 checks
it beside TC-533. One decision gets one home. WI-1024's slice 1 wrote
LLR-423 as a focused row for IF-277 beside the large LLR-300 (its record,
§6 item 1). **Settled at the scope critique:** LLR-423 and TC-533 stay the
one home; the session-variable clause is removed from LLR-300 (text only,
still `Accepted`, owed), whose lease-admission obligations stay, and
TC-316's check of it moves to TC-533 (TC-316 amended in text, owed).
LLR-423 and TC-533 stay `Drafted` for the next sitting.

Critiqued 2026-11-24 (Sol and Hydrogen;
`docs/reviews/2026-11-24-scope-critiques/WI-1071.md`): `planmode` is `single`, and the
session-variable decision's home is settled (above).

## Done-when

- [ ] LLR-047, LLR-039, LLR-199 and LLR-281 each state every obligation the
      code enforces that the slice's rewrite dropped, or the Deliverable
      names the accepted row that states it, or reports that the code no
      longer enforces it; text only, each still `Accepted`, owed.
- [ ] TC-398 states and a test asserts that an unequal-identity refusal
      names both digests (red first where the assertion is new).
- [ ] TC-530 drives a `constrains`-only change, with no accepted cell
      moved, through the amendment walk and the trunk mint, apart from the
      accepted-cell change.
- [ ] TC-571's method names a rendered row that moves another trace cell,
      matching its expected.
- [ ] The session-variable decision has one home, LLR-423 (verified by
      TC-533): LLR-300 no longer states it and TC-316 no longer checks it,
      and each test that drove it is named by TC-533.
- [ ] Each row it touches keeps the three row rules (no code names,
      inherited ones included; one obligation with every clause tested; a
      child within its parent).
