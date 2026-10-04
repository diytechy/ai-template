# ADJUDICATE (first approval): WI-791, SR-228 at ab061501

An independent spine adjudicator (Claude Opus) judged this row. It made none of the changes it
judges. The judgement used the kit brief composed for this lane's merge, read in the lane as the
owner directed on 2026-10-03 (S11). SR-228 sits on a rung `human_approval_through =
"DevStg-Boundary"` releases, so its first approval is this session's act.

The adjudicator read the chain SN-029, SR-178, SR-207, SR-228, LLR-153, LLR-245, LLR-278,
TC-147, TC-240 and TC-278, OI-100 and its ruling record, PROCESS.md §3 and §4 (including this
lane's new §4 sentence), and the code at ab061501 that the chain names. It ran the cited tests
unmodified (57 passed) and mutation-probed the code on a scratch export of the lane; the probe
table is in `001-ADJUDICATE-AMENDMENT-ab06150.md` beside this file, and the probes this row
depends on are cited by number below.

- [RETURN] SR-228 -> the obligation: where the dial holds a tier, an adjudication may re-attest an amended approved row only on a verdict ruling it CLARITY; the act is refused by row on a MEANING verdict and on an absent, unreadable or non-CLARITY verdict; the recorded act names its verdict; a first draft is never re-attested this way -> the chain: UPWARD, SN-029 asks that the loop stop for a human only where the dial reserves the judgement, that every failure direction lean toward more human involvement, and that an automated act leave a durable record; the owner's OI-100 ruling (a) draws exactly this line, and the rationale states what breaks without it and which alternative lost, with no provenance in any cell. SIDEWAYS, it overlaps neither SR-178 (moved text is reported) nor SR-207 (a refresh is refused while unjudged drift sits in it): it adds the authority boundary both lack. DOWNWARD, LLR-278 (the merge refusal) and LLR-153 (adjudication_action) trace it and the code does what they say; probes M1, M3, M6 and M13b show the trunk-tip dial, the first-draft guard, the head-side verdict read and the merge-side need for a recorded verdict are pinned. But two of its acceptance clauses are verified by nothing and one is decomposed outside its chain: (1) "an unreadable or non-CLARITY verdict" — probe M5, which refuses only a MEANING ruling and so admits a verdict that does not name the row or that the act's head does not carry, survives every cited test; (2) "the recorded act names the verdict for later audit" is decomposed by LLR-245, which traces SR-207 alone, and its test case TC-240 neither verifies SR-228 nor states the verdict in its Method -> not ready. The row's own cells need no change; its chain does. The fixes are Fix 3 (LLR-245 detail and SR-Refs), Fix 6 (TC-278 method, evidence and three tests) and Fix 7 (TC-240 method, expected, verifies, evidence and one test) in `001-ADJUDICATE-AMENDMENT-ab06150.md`. After they land, the row is re-judged with them.

OUTCOME: RETURN rows=1

## Aftermath

Every row line says RETURN, so no registry cell and no approval snapshot moved. SR-228 stays
`Drafted`. Under the owner's in-lane direction the follow-up is not drafted as `## Dispositions`:
the coordinator routes the fixes named above to the author and resumes this adjudicator to
re-judge.
