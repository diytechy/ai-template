# WI-798 checkpoint adjudication at 4826e3e (amendment; first-approval)

One sitting, two judgements, made afresh at this tip. I read the cells I was
given and their chains. I checked each claim against the settled code at
4826e3e (`session_service.py`, `session_keep.py`, `agent_route.py`,
`dev-setup.template.sh`, `tests/test_accounts.py`) and against the TC registry.
I did not read the authoring session.

Two cross-cutting facts decide several rows:

1. **The naming rule (§0) is new since sitting 004 and binds every amendment.**
   No row's text names an implementation carrier, and an amendment adds no
   name the rule forbids. A name already in the approved cell may stay. An
   amendment that introduces a function or attribute name is not blessable,
   however correct its obligation.
2. **Seventeen tests in `tests/test_accounts.py` are still cited by no TC.**
   Sitting 004 found this and the lane has not answered it. Among them are the
   declared-account credential-boundary tests that LLR-305 now states:
   - test_a_qualified_login_launch_withholds_every_ambient_credential_its_cli_ranks_above_the_home
   - test_a_login_account_whose_route_or_account_declares_a_competing_source_is_refused
   - test_a_gemini_login_account_whose_route_declares_a_vertex_source_is_refused
   - test_a_token_account_launch_carries_only_its_own_token
   - test_an_ambient_entry_keeps_the_ambient_environment

## amendment

All 14 rows change meaning. Each adds an account, a qualifier, a refusal, a
prohibition or a changed home that a correct implementation of the anchored
text could fail.

- [MEANING] LLR-321 Detail -> the report reads signed-in only for a readable token, missing when the token cannot be read -> it also reads signed-in for a documented signed-in status from the account's own home -> a new signed-in source. I would NOT bless it. The added arm is half-stated: dev-setup also reports a login account that is not signed in as missing, and an unresolved adjudicator entry as missing (`dev-setup.template.sh`, the `login:missing` and unresolved arms). The text still says missing is "when the token cannot be read", so a closed reading leaves those cases unaccounted for. TC-344, the row's only TC, drives token inputs only. The dev-setup login tests sit in TC-365, which does not verify LLR-321
- [MEANING] LLR-044 Detail -> routing, selection and cooldowns keyed by route -> one entry per enable-list line carried by selection, preference and cooldowns, with ROUTE@ACCOUNT as the qualified key -> a new identity rule. I would NOT bless it as worded: the amendment introduces two function names, resolve_enabled and entry_route, which the anchored cell did not carry, and §0 forbids that. The obligation itself is sound, and TC-046 holds it. It needs restating as observable behaviour, for example "each enable-list line is one entry; selection, preference and cooldowns carry the entry; a registry row is read only through the entry's route"
- [MEANING] LLR-072 Detail -> two fresh planner sessions with the nonresponse fallback -> each session also carries its enabled entry, and its model is the route that entry selects -> a new carried field. I would NOT bless it as worded: the amendment introduces `model_id`, a code attribute (`agent_route`'s planner-session property), where the anchored cell named no symbol. Restate it as "its model is the registry route that entry selects". TC-072 holds the obligation
- [MEANING+BLESS] LLR-306 Detail -> refuses an unusable route or an unreadable brief; one sign-in reading -> also refuses an invalid account or a registry error, the sign-in reading names the entry's account, and the act turn runs under the judging turn's account -> new refusal arms and a pinned act-turn account. The text adds no symbol, matches the code, and is verified by TC-321 (the act-turn account tests) and TC-365's refusal test
- [MEANING+BLESS] TC-321 Expected -> the default route is ANTHROPIC-OPUS-STRONG -> the default entry is ANTHROPIC-OPUS-STRONG@ADJUDICATOR -> a check of the old default fails the new one. It matches the shipped enable list and the entry point's default; an enable-list entry is a boundary artifact a TC may name
- [MEANING+BLESS] LLR-266 Detail -> adapter choice, flags, final text and raw usage -> the same, plus the adapter takes the call's composed environment and never selects, replaces or infers an account home -> a new prohibition on the adapter. The text adds no name, and TC-362 now verifies it
- [MEANING+BLESS] LLR-267 Detail -> codex reads the rollout under the launch's CODEX_HOME, else codex's default home -> a qualified Codex call reads only its composed CODEX_HOME -> this narrows the fallback for a qualified call. CODEX_HOME is the provider CLI's documented variable, not a kit carrier. TC-263 and TC-362 verify it
- [MEANING+BLESS] LLR-268 Detail -> the usage mapping per runner -> the same, plus usage reads only the call's own captured stream, with account-home telemetry left to LLR-267 -> this adds a closed input boundary, and it answers sitting 004's finding: the sentence is now true of the mechanism. It reuses the subject name the anchored cell already opens with and introduces none
- [MEANING+BLESS] LLR-270 Detail -> a retained launch runs under a per-family dedicated home under the store's home/ -> it runs under LLR-305's environment (the account home for a qualified entry, ambient for an unqualified one, no per-family home); a lease-only record also holds the account; a record lacking the account or naming another reads as no record and mints once -> the home and the record identity both moved. This answers sitting 004's finding and matches the code (the hold records the account; the Keep's home is the prepared launch's). TC-364 and TC-267 verify it. One note for the successor below: the unamended Rationale still says the dedicated homes keep a retained transcript out of a person's own sessions, which is no longer true for an unqualified entry. The approved Detail governs
- [MEANING] LLR-305 Detail+Rationale+Title -> a family-level token and dedicated home, with refuse_competing for a token route -> the entry's account supplies environment, home and token; refuse_competing applies to every declared account; a qualified OpenCode launch starts from a declared base plus kit-owned names -> the credential boundary moved from family to account, and the Detail cell carried that change. I would NOT bless it, for two reasons. (1) The amendment replaces `_name_key` with a different function name, env_name_key, adding a carrier name §0 forbids; "names compare under the platform's case rules" carries the obligation without it. (2) Read downward, the new declared-account arms (withholding ambient sources above a login account's home, refusing a declared competing source on a login account, the OpenCode base) are pinned only by tests no TC cites: the five credential-boundary tests listed above. TC-362, the TC that claims this row's account arms, does not cite them, so the boundary this row states is unverified in the trace
- [MEANING+BLESS] TC-267 Method -> a retained codex route launches under a dedicated CODEX_HOME created under the store -> under the account CODEX_HOME -> the test now checks a different home. This matches LLR-270 as amended, and the Evidence tests drive it
- [MEANING+BLESS] TC-323 Expected+Method -> the dedicated-home probe -> the account-home and login-account-home probe -> the subject of the three readings moved from family home to account home; the readings and the token arm are unchanged, and the cited tests drive them
- [MEANING] TC-324 Expected+Method -> a family with a dedicated home needs a readable sign-in, and a family without one passes unprobed -> "Only a retained launch for a login account" needs a readable sign-in, and an unqualified entry has no gate -> the subject moved. I would NOT bless it: this Expected is unchanged from the text sitting 004 returned. "Only ... a login account" still excludes token accounts, while the same row's Method asserts that an unset, missing, unreadable or empty token file refuses, and `require_signin` refuses a token account. The Method also no longer runs test_a_family_with_no_dedicated_home_passes_require_signin_unprobed, the Evidence test that holds the "unqualified entry has no account sign-in gate" arm, while still asserting that arm
- [MEANING+BLESS] TC-330 Expected -> the dedicated home's CLI transcript is excluded -> the account home's CLI transcript is excluded -> the exclusion now names a different home, which matches the account design

The rung is released, so the later act turn re-attests the nine rows marked
`[MEANING+BLESS]`. The five plain `[MEANING]` rows are not re-anchored and go
back through the draft below:

- LLR-321, LLR-044, LLR-072 and LLR-305 stay drifted in
  `low-level-requirements.toml`.
- TC-324 stays drifted in `test-cases.toml`.

Each registry therefore still holds unblessed drift, so I expect the snapshot
copy for either registry to be refused until this draft lands, as at sitting
004. In that case the blessed rows wait for the same act as the returned ones.

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-20 headless leg 04): commits b1afd77c7, 88324f6b4 and 49d91cd, re-sat at sittings 013 and 014. No row is minted from these drafts.

```toml
title = "Restate LLR-044, LLR-072, LLR-305, LLR-321 and TC-324 without carrier names and closed over their arms; cite the account-boundary tests"
workstream = "process"
buildtier = "strong"
sr_refs = ["SR-032", "SR-154", "SR-155", "SR-227"]
priority = 3
specref = "docs/reviews/wi-798/012-ADJUDICATE-4826e3e.md#amendment"
```

What the draft owes, row by row:

1. **LLR-044, LLR-072 and LLR-305:** restate the added sentences without
   resolve_enabled, entry_route, model_id or env_name_key. The obligations
   stand as they are.
2. **LLR-305:** give the declared-account boundary a verifying TC, by citing
   the five credential-boundary tests listed at the top of this verdict.
3. **LLR-321:** state the login-account and unresolved-entry `missing`
   readings, and extend TC-344 (or link the dev-setup login tests to LLR-321)
   so the new signed-in source and those readings are verified.
4. **TC-324:** make the Expected cover token and login accounts alike, and
   either keep the unprobed-entry test in its Method or drop the arm it holds.
5. **LLR-270 (blessed here, so this is a follow-up, not a fix):** its
   Rationale should stop claiming a dedicated home for every retained
   transcript.

VERDICT: MEANING rows=14

## first-approval

A mixed batch: four rows are ready and three go back.

- [APPROVE] LLR-336 -> account tables (cli, notes, optional env, optional token_file_variable, verified) are parsed and malformed ones are named errors and dropped; ROUTE@ACCOUNT resolves only to a declared account of the route's CLI; malformed qualifiers, unreadable enable lists, home-variable route envs and route/account conflicts are named errors with no fallback; homes sit under the user config directory; only token-account homes are created; entry identity keys cooldowns and planner routing; the adjudicator and dev-setup report the account; an unverified non-ambient Claude login is printed, not refused -> upward, SR-154 calls for the registry and consent half and SR-227 for homes and credentials, and the unearned SR-222 link is gone. Sideways, the launch composition, credential boundary and retained-record identity now each have one home (LLR-305, LLR-270) and this row links to them rather than restating them. Downward, TC-361..366 cover its own arms. Its text names only boundary artifacts and registry keys -> ready. It answers each of sitting 004's three findings against it
- [APPROVE] TC-361 -> account declaration and qualifiers fail visibly with no ambient fallback, and a cli mismatch refuses -> its Verifies is now SR-154 and LLR-336, both earned. The cited tests hold the stated arms: malformed tables, qualifiers, collisions, unreadable enable lists, preflight, preference, template forms. The uncited registry-error tests strengthen the malformed-table arm the cited test already holds -> ready
- [RETURN] TC-362 -> every launch and probe uses its selected account's environment -> Verifies now names LLR-266/267/268 and LLR-305 as sitting 004 asked. It also claims SR-239, reviewer retention, and nothing in its evidence drives a reviewer scope. As the TC claiming LLR-305's account arms, it still omits the five credential-boundary tests that alone pin the declared-account withholding and the login competing-source refusal -> not ready: one SR over-claim, plus a gap at the very boundary this lane exists to draw
- [APPROVE] TC-363 -> two accounts on one route cool and select independently, and the planner fallback carries its entry -> Verifies SR-154 and LLR-336, both earned, and the cited tests hold it -> ready
- [RETURN] TC-364 -> retained state never crosses an account boundary -> the evidence holds it, and the LLR-270 link sitting 004 asked for is present. Verifies now also claims SR-238 (a deadline or interruption ends the session process tree), which none of its five tests touches; the claim was copied from LLR-270's parent set -> not ready while it over-claims SR-238
- [RETURN] TC-365 -> the adjudicator refuses invalid account and registry input, accounts report only their own credential state, and dev-setup neither signs in nor exposes credentials -> its Method now asserts conditions and Verifies adds LLR-306, as asked. Verifies also claims SR-239 (reviewer retention), which no cited test touches. test_the_signin_probe_names_an_ambient_or_unresolved_entry and test_the_claude_status_reader_takes_only_its_documented_pairs, which hold its reporting arm, are still cited nowhere -> not ready
- [APPROVE] TC-366 -> an unverified non-ambient login account is printed, neither refused nor fallen back from, and the owner-held two-login half is excluded -> Verifies is now SR-154 and LLR-336, both earned, and the cited tests hold it -> ready

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-20 headless leg 04): commits b1afd77c7, 88324f6b4 and 49d91cd, re-sat at sittings 013 and 014. No row is minted from these drafts.

```toml
title = "Narrow TC-362, TC-364 and TC-365 to the SRs their tests evidence and cite the uncited account tests"
workstream = "process"
buildtier = "strong"
sr_refs = ["SR-154", "SR-227"]
priority = 3
specref = "docs/reviews/wi-798/012-ADJUDICATE-4826e3e.md#first-approval"
```

What the draft owes, row by row:

1. **TC-362:** drop SR-239 from Verifies, and cite the five credential-boundary
   tests, plus test_the_user_config_dir_follows_the_platform_rule and
   test_a_token_account_whose_token_cannot_be_read_is_refused_before_its_home.
2. **TC-364:** drop SR-238 from Verifies.
3. **TC-365:** drop SR-239 from Verifies, and cite
   test_the_signin_probe_names_an_ambient_or_unresolved_entry and
   test_the_claude_status_reader_takes_only_its_documented_pairs.
4. **Anywhere they hold a stated arm:** the remaining uncited registry-error
   tests.

OUTCOME: RETURN rows=7

SITTING: JUDGED kinds=amendment;first-approval
