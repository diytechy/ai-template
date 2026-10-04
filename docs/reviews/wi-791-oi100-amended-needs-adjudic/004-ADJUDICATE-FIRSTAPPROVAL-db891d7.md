# ADJUDICATE (first approval, round 2): WI-791, SR-228 at db891d7f

An independent spine adjudicator (Claude Opus) re-judged this row after fix round 2. It made none
of the changes it judges. It returned the row in round 1 (`002-ADJUDICATE-FIRSTAPPROVAL-ab06150.md`)
for its chain, not its text. The judgement used the kit brief recomposed at db891d7f, read in the
lane as the owner directed on 2026-10-03 (S11). SR-228 sits on a rung that
`human_approval_through = "DevStg-Boundary"` releases, so its first approval is this session's
act.

The adjudicator re-read the chain at db891d7f: SN-029, SR-178, SR-207, SR-228, LLR-153, LLR-245,
LLR-278, TC-147, TC-240 and TC-278. The probes cited below are in
`003-ADJUDICATE-AMENDMENT-db891d7.md` beside this file.

- [APPROVE] SR-228 -> the obligation: where the dial holds a tier, an adjudication may re-attest an amended approved row only on a verdict ruling it CLARITY; the act is refused by row on a MEANING verdict and on an absent, unreadable or non-CLARITY verdict; the recorded act names its verdict; a first draft is never re-attested this way -> the chain: UPWARD, SN-029 and the owner's OI-100 ruling (a) call for exactly this boundary, and the rationale states what breaks without it and which alternative lost, with no provenance. SIDEWAYS, it overlaps neither SR-178 nor SR-207. DOWNWARD, round 1's two gaps are closed. Each acceptance clause is now decomposed under this row: LLR-278 (the merge refusal), LLR-153 (adjudication_action) and LLR-245, which now traces SR-228, for the verdict the act records. Each clause is also verified by a test case that names SR-228 and states it in its method. TC-278 covers the absent, unreadable, non-CLARITY and MEANING verdicts, the conflicting tag, the first draft and the trunk-tip dial; M1, M2, M3, M5, M6b and M13b are caught. TC-240 covers the verdict recorded in the act ledger and its three refusals; M10 to M13 are caught. TC-147 covers adjudication_action's arms; M7 is caught -> ready. The two rows returned in the amendment verdict this round (LLR-118 and LLR-167) are outside this row's chain: neither decomposes SR-228, and the held-rung refusal SR-228 states is enforced and pinned without them.

OUTCOME: APPROVE rows=1

## Aftermath: the flip waits for the lane's single act

The owner's in-lane direction (S11) closes the lane with ONE act, its last spine commit. That act
flips SR-228 and re-attests every amended row this adjudicator blesses or rules CLARITY. The same
direction forbids the act while any row still needs fixing. Two rows were returned this round
(LLR-118 and LLR-167, Fixes 8 and 9 in `003-ADJUDICATE-AMENDMENT-db891d7.md`), and the act could
not anchor the low-level-requirements copy while they drift.

So SR-228 stays `Drafted` for now, and no snapshot was taken. After the re-judge, the act is:

- flip SR-228 to `Approved`;
- `intake.py snapshot --approves "docs/requirements/system-requirements.toml=WI-791" --reattests
  <the rows blessed or ruled CLARITY>`.

This verdict records that the row's text and chain are ready. Nothing in SR-228's chain needs
another fix.
