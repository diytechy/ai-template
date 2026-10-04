# ADJUDICATE (amendment, round 3): WI-791, fourteen amended rows at fa4356e1

An independent spine adjudicator (Claude Opus) re-judged this amendment after fix round 3. It
made none of the changes it judges. In round 2 it wrote Fixes 8 and 9
(`003-ADJUDICATE-AMENDMENT-db891d7.md`), and here it judges whether they landed as required. The
judgement used the kit brief recomposed at fa4356e1, read in the lane as the owner directed on
2026-10-03 (S11). The anchor is unchanged: `docs/archive/last_approved/`, with
system-requirements at 1fda46ed, low-level-requirements at 439a2bb0 and test-cases at a9791303.

## What fix round 3 changed, checked

A cell-by-cell comparison of db891d7f and fa4356e1 finds exactly two rows moved: TC-123
(`method`, `evidence`) and TC-161 (`method`, `evidence`). Each of those four cells equals, byte
for byte, the replacement round 2 prescribed.

The three prescribed test blocks are in `tests/test_gen_open_items_render.py` and
`tests/test_adjudicate_brief.py`, byte for byte, and no test line was removed. No script changed.
The twelve rows ruled in round 2 have not moved since, so those rulings carry. SR-228's chain
(SR-228, LLR-153, LLR-245, LLR-278, TC-147, TC-240, TC-278) did not move either, so
`004-ADJUDICATE-FIRSTAPPROVAL-db891d7.md` (APPROVE) stands.

Every row the kit reports as owing an act in the three registries this act copies is one of the
fourteen below, except for two `Drafted` rows. One is SR-228, which this act flips. The other is
SR-224, a first draft that is not this act's; it stays `Drafted` inside the copy.

## Probes

The probes ran on a fresh scratch export of fa4356e1 (`git archive`, outside the lane), each
reverted before the next. The baseline, the open-items and adjudicate-brief modules at fa4356e1,
gave 120 passed. Round 2's four survivors, re-run against the lane's own tests:

| # | Mutation | Result |
|---|---|---|
| P1 | the audit list ordered oldest first | caught (`test_the_verdict_audit_list_is_newest_first`) |
| P4 | DA and SUR dropped from the unchained tiers | caught (`test_assumption_and_surrogate_scoped_amendment_rows_compose_within_their_scope`) |
| P5 | unchained rows not bounded by the scope | caught (the same test) |
| P6 | the held arms swapped | caught (`test_the_held_aftermath_gives_each_verdict_its_own_arm`) |

Every clause probed across the three rounds is now pinned, except one: M4, the unknown-tier
fail-safe, which no row states. The probes caught in earlier rounds stand, because no script
changed. Those are M1, M2, M3, M5, M6b, M7 to M13b, P2, P3 and P7.

## Rulings

- [MEANING] LLR-118 detail -> the open-items renderer's pending decisions, attestation chains and contracts -> the same, plus the owner's audit list of every verdict-naming act, newest first, or None recorded -> not the same: a new rendered list. Accurate to the code, and every clause is now pinned (P1, P2, P3). I bless it.
- [MEANING] LLR-153 detail -> as ruled in round 2 (Fix 1) -> unchanged since -> I bless it.
- [MEANING] LLR-158 detail -> as ruled in round 2 (Fix 2) -> unchanged since -> I bless it.
- [MEANING] LLR-167 detail -> the brief selection, assemblers and refusals -> the same, plus need, assumption and surrogate scopes rendered through tier_owing and the held-rung arm taken from adjudication_action -> not the same: two new behaviours. Accurate to the code, and every clause is now pinned (P4, P5, P6). I bless it.
- [MEANING] LLR-245 detail, sr_refs -> as ruled in round 2 (Fix 3) -> unchanged since -> I bless it.
- [MEANING] LLR-271 detail -> as ruled in round 2 (tier_owing, P7 caught) -> unchanged since -> I bless it.
- [MEANING] LLR-278 detail, title -> as ruled in round 2 (Fix 4) -> unchanged since -> I bless it.
- [CLARITY] SR-178 acceptance_criteria -> any artifact whose text moved from its recorded copy is reported, a stakeholder need included -> the same, naming needs, assumptions and surrogates -> the same obligation: assumptions and surrogates were already recorded artifacts, as ruled in rounds 1 and 2.
- [MEANING] TC-123 method, evidence -> gen_open_items driven over temp repos: briefs, chains, empty states, check, escaping, word diff, theme tokens -> the same, plus verdict_reattest_block: verdict-naming entries listed newest first with rows and verdict file, others left out, None recorded when none, the list on the page -> not the same: a new verified behaviour. It is Fix 8 byte for byte, each clause is pinned (P1, P2, P3), and the evidence names exactly the tests the method describes. I bless it.
- [MEANING] TC-147 method -> as ruled in rounds 1 and 2 -> unchanged since -> I bless it.
- [MEANING] TC-153 method, verifies, evidence -> as ruled in round 2 (Fix 5) -> unchanged since -> I bless it.
- [MEANING] TC-161 method, evidence -> the brief arms, refusals and routing; "what a MEANING verdict owes next is derived from the declared approval dial" -> the same, plus need, assumption and surrogate rows rendered within the scope, and each verdict's own arm: released re-attestation naming no verdict, held CLARITY re-attested naming its verdict, held MEANING stopping for the owner -> not the same: two new verified behaviours. It is Fix 9 byte for byte, and P4, P5 and P6 are caught. I bless it.
- [MEANING] TC-240 method, expected, verifies, evidence -> as ruled in round 2 (Fix 7) -> unchanged since -> I bless it.
- [MEANING] TC-278 expected, method, evidence -> as ruled in round 2 (Fix 6) -> unchanged since -> I bless it.

VERDICT: MEANING rows=14

## Aftermath

Every row is settled. The dial releases SR, LLR and TC, so all fourteen are re-attested by this
adjudicator, in the lane's single act and its own commit after this one. That act also flips
SR-228 under its first-approval verdict (004):

`intake.py snapshot --approves "docs/requirements/system-requirements.toml=WI-791" --reattests
LLR-118,LLR-153,LLR-158,LLR-167,LLR-245,LLR-271,LLR-278,SR-178,TC-123,TC-147,TC-153,TC-161,TC-240,TC-278`
