# WI-798 checkpoint adjudication at 00a353f (amendment; first-approval)

This sitting judges the whole change set at the gated tip in one sitting, so
that one verdict can authorize the act. Every row was judged before, across
sittings 012, 013 and 014. I checked that the text judged then is the text
here now, rather than taking the context note on trust:

- **No row changed.** Each of the 22 rows at HEAD is identical, cell for cell,
  to the copy its last sitting judged:
  - at 4826e3e: LLR-266, LLR-267, LLR-268, LLR-306, TC-267, TC-321, TC-323,
    TC-330, LLR-336, TC-361, TC-363 and TC-366;
  - at b1afd77: LLR-044, LLR-072, LLR-270, LLR-305, LLR-321, TC-324, TC-362,
    TC-364 and TC-365;
  - at 49d91cd: TC-344.
- **No code or test changed.** `git diff 49d91cd38 HEAD` touches only review,
  decision and session-log records.
- **The evidence still holds.** Every test the in-scope TCs cite exists at
  this tip, and every test in `tests/test_accounts.py` is cited by a TC.

Two observations, for the record. Neither is a ruling on a row.

1. **Review 016 left a MINOR "for clarity" on LLR-305:** its composition
   sentence names the removal of competing credential names without the
   declared-account condition. This is the reading sitting 013 examined. In
   the same cell, "competing" means a source ranked above a declared
   account's home, so an unqualified entry has none, which matches the code.
   I keep the blessing; a later clarity amendment could state the condition
   outright. Review 016's other MINORs fall outside the rows judged here:
   - the interfaces rows (IF-246, IF-248, IF-282);
   - the `Implements: SR-222` code back-links on LLR-336's symbols, whereas
     the row traces to SR-154 and SR-227;
   - the SR-227 wording, which goes to the owner;
   - a dial comment;
   - where the empty-home observation is recorded.
2. **Commit 00a353fae edited the committed verdicts 004, 012 and 013.** It
   renamed each `## Dispositions` heading to "Returns answered in the lane"
   and added a line naming the commits that answered them. No row ruling and
   no machine line changed, and the evident purpose is to stop intake minting
   follow-ups the lane has already done. Still, an accepted verdict is a
   ruled record. The owner should see that it was edited after acceptance;
   the commit message and the added lines say so.

## amendment

All 15 rows change meaning against the 41375927d anchor, and I would bless each
one. The reasons are the ones the earlier sittings recorded, and the text has
not moved since.

- [MEANING+BLESS] LLR-321 Detail -> the report reads signed-in only for a readable token, missing when it cannot be read -> also signed-in for a documented signed-in status from the account's own home, missing for an unreadable token file, a login account not signed in, or an unresolved entry -> new readings. The text names no carrier and matches the report's branches; TC-344 drives every arm (sittings 013, 014)
- [MEANING+BLESS] TC-344 Expected+Method -> readable, missing and unreadable inputs -> token and login accounts, a signed-in login account verified and unverified, a login account not signed in, and an unresolved entry, on both launcher families, with the unverified annotation asserted -> new cases. The cited test drives each one (sitting 014)
- [MEANING+BLESS] LLR-044 Detail -> routing and cooldowns keyed by route -> each enable-list line is one entry carried by selection, preference and cooldowns, with ROUTE@ACCOUNT as the qualified key -> a new identity rule. The text names no carrier, and TC-046 holds it (sitting 013)
- [MEANING+BLESS] LLR-072 Detail -> two fresh planner sessions -> each also carries its enabled entry, and its model is the route that entry selects -> a new carried field. The text names no carrier, and TC-072 holds it (sitting 013)
- [MEANING+BLESS] LLR-306 Detail -> refuses an unusable route or brief -> also refuses an invalid account or a registry error, names the entry's account in its sign-in reading, and runs the act turn under the judging turn's account -> new refusals and a pinned account. TC-321 and TC-365 verify it (sitting 012)
- [MEANING+BLESS] TC-321 Expected -> the default route ANTHROPIC-OPUS-STRONG -> the default entry ANTHROPIC-OPUS-STRONG@ADJUDICATOR -> a check of the old default fails the new one; an enable-list entry is a boundary artifact (sitting 012)
- [MEANING+BLESS] LLR-266 Detail -> adapter choice and capture -> the same, plus the adapter takes the composed environment and never selects, replaces or infers an account home -> a new prohibition. TC-362 verifies it (sitting 012)
- [MEANING+BLESS] LLR-267 Detail -> rollout read under the launch's CODEX_HOME, else codex's default -> a qualified Codex call reads only its composed CODEX_HOME -> the fallback narrows for a qualified call (sitting 012)
- [MEANING+BLESS] LLR-268 Detail -> the usage mapping -> the same, plus usage reads only the call's own captured stream -> a closed input boundary, true of the mechanism, with no new name (sitting 012)
- [MEANING+BLESS] LLR-270 Detail+Rationale -> a per-family dedicated home under the store; family, route and scope identity -> LLR-305's environment with no per-family home; account in the record identity and the lease-only record; an account-less or other-account record mints once -> the Detail carries the meaning. The Rationale now matches it: only a qualified account home keeps a transcript out of a person's sessions (sittings 012, 013)
- [MEANING+BLESS] LLR-305 Detail+Rationale+Title -> a family-level token and dedicated home -> the entry's account supplies environment, home and token; every declared account is checked for a declared source ranked above its home; a qualified OpenCode launch starts from its declared base plus kit-owned names -> the credential boundary moves from family to account. The text names no carrier, and TC-362 cites the boundary's tests (sitting 013; review 016's clarity MINOR noted above)
- [MEANING+BLESS] TC-267 Method -> launches under a dedicated CODEX_HOME created under the store -> launches under the account CODEX_HOME -> the test checks a different home, matching LLR-270 (sitting 012)
- [MEANING+BLESS] TC-323 Expected+Method -> the dedicated-home probe -> the account-home and login-account-home probe -> the subject of the three readings moves to the account home; the token arm is unchanged (sitting 012)
- [MEANING+BLESS] TC-324 Expected+Method -> a family with a dedicated home needs a readable sign-in -> a token account needs its readable token file and a login account its documented signed-in status, and an unqualified entry has no gate -> the subject moves to the account. Both account kinds are covered, and the Method runs the test that holds the unqualified arm (sitting 013)
- [MEANING+BLESS] TC-330 Expected -> the dedicated home's transcript is excluded -> the account home's transcript is excluded -> the exclusion names a different home, matching the account design (sitting 012)

The LLR and TC rungs are released, so the later act turn re-attests all 15
rows. Neither registry holds an unblessed row among those judged here, so the
copy should not be refused for drift.

VERDICT: MEANING rows=15

## first-approval

All seven rows are ready. Each was approved before, at 012 or 013, on text
unchanged since.

- [APPROVE] LLR-336 -> account tables are parsed and malformed ones dropped with named errors; ROUTE@ACCOUNT resolves only to a declared account of the route's CLI, with no fallback; homes sit under the user config directory and only token-account homes are created; entry identity keys cooldowns and planner routing; the adjudicator and dev-setup report the account; an unverified non-ambient Claude login is printed, not refused -> it traces to SR-154 and SR-227 and delegates the launch boundary to LLR-305 and record identity to LLR-270, one home each, with TC-361..366 covering its own arms. Its text names only boundary artifacts and registry keys -> ready (sitting 012)
- [APPROVE] TC-361 -> account declaration and qualifiers fail visibly with no ambient fallback, and a cli mismatch refuses -> Verifies SR-154 and LLR-336, both earned by its cited tests -> ready (sitting 012)
- [APPROVE] TC-362 -> every launch and probe uses its selected account's environment, including the declared-account credential boundary and the OpenCode base -> Verifies SR-154, SR-222, SR-227, LLR-266/267/268, LLR-305 and LLR-336, each earned; it cites the boundary tests -> ready (sitting 013)
- [APPROVE] TC-363 -> two accounts on one route cool and select independently, and the planner fallback carries its entry -> Verifies SR-154 and LLR-336, earned -> ready (sitting 012)
- [APPROVE] TC-364 -> retained state never crosses an account boundary -> Verifies SR-154, SR-227, SR-239, LLR-270 and LLR-336, each earned by a cited test -> ready (sitting 013)
- [APPROVE] TC-365 -> the adjudicator refuses invalid account and registry input, accounts report only their own credential state, and dev-setup neither signs in nor exposes credentials -> Verifies SR-154, SR-227, SR-231, LLR-305, LLR-306 and LLR-336, earned; its sign-in and registry-error tests are cited -> ready (sitting 013)
- [APPROVE] TC-366 -> an unverified non-ambient login account is printed, neither refused nor fallen back from; the owner-held two-login half is excluded -> Verifies SR-154 and LLR-336, earned -> ready (sitting 012)

OUTCOME: APPROVE rows=7

SITTING: JUDGED kinds=amendment;first-approval
