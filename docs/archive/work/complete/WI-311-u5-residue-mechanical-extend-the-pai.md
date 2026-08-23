+++
id = "WI-311"
title = "U5 residue -> mechanical: extend the pairwise deltaE floor ACROSS vocabularies, not just within PHASE_ACCENTS. Measured 2026-07-25: seven cross-vocabulary pairs fall under the existing 15 floor (worst 9.5, SR #0e7490 vs phase[3] #155e75) and sw-node external #334155 vs component #475569 is 8.6, the closest pair in the document; 120-CRITIQUE reported this class independently, so it is confirmed live rather than merely computable. The floor is a JUDGEMENT and must be recorded as one - rec: keep 15 within a vocabulary, adopt 12 across, which clears the confirmed conflations without a wholesale re-hue."
workstream = "scripts"
sr_refs = ["SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 308
+++

## Deliverable

The pairwise deltaE floor now holds WITHIN and ACROSS every declared colour vocabulary, not just inside PHASE_ACCENTS - which is what made LLR-102's residue ('a collision the identity check misses') look perceptual: it was the same formula on a set nobody had widened. Two floors, both judgements, both recorded in the test rather than in a commit message: 15 WITHIN a vocabulary (every member can sit beside every other in one legend, so the strict bar the phase accents already met) and 12 ACROSS (two colours from different vocabularies share no legend, so a lower bar - but not none, because 120-CRITIQUE reported a reader conflating exactly such a pair). The declared tier<->okf mirror is exempt BY DESIGN and the test asserts it is byte-equal rather than merely close. Three conflations found and re-hued: sw external/component 8.6 (component #475569 -> #44403c stone), SR/phase[3] 9.5 (phase[3] #155e75 -> #134e4a), Interface/phase[7] 10.5 (Interface #7c3aed -> #701a75 - the OKF entry moved rather than the phase, because a phase sequence reads as a progression). Chosen by a joint search maximising the worst pairwise distance subject to white-text AA contrast; closest surviving pair is now 12.5. Guard: tests/test_gen_trajectory.py::test_u5_pairwise_deltae_holds_within_and_across_every_vocabulary, verified to fail against all three original conflations and a newly-introduced one. Also tightened WI-300's U2 guard to PAINT surfaces (style blocks, style attributes, fill/stroke attributes): the rendered palette-rationale prose NAMES retired hexes, and a whole-document scan read those as emitters - which would have grown the non-concept allowlist by one entry per retirement, the exact 'widen the list rather than fix it' trap that list's own comment warns about. The allowlist is back to its one real entry.
