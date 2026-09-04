## 2026-09-04 — WI-592: spot-check of the clean close of WI-588

Sample-tier `complete_review` (`docs/process.toml [attestation] complete_review =
'sample'`) on a GREEN close. Nothing is alleged; the close stands. The one
question: does what shipped answer what the row asked for?

WI-588's row asked for three things, and said all three shipped:

1. a regression that drives the trunk regen path (not the generator directly),
2. `TC-206` citing that node in `evidence` and stating the arm in `method`,
3. `LLR-208.detail` NAMING the wiring (`verdict-rollup` id, `docs/reviews/`
   guard, LEAF position, membership-is-contract).

### What is being driven here

Reading the three cells is not the check — the whole subject of WI-588 was a
cell that *read true* while nothing drove it. So the spot-check re-drives the
mutation at THIS tip: delete the `verdict-rollup` tuple from
`trunk_step.REGEN_STEPS` and confirm the new node reds and the pre-existing
arms stayed as described.

(session in progress — findings below)
