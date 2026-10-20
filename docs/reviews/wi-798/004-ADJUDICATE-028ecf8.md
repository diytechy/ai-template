# WI-798 checkpoint adjudication at 028ecf8 (amendment; first-approval)

One sitting, two judgements. I read the cells I was given, their chains, and the
settled code at 028ecf8 (`session_service.py`, `session_keep.py`,
`session_adapters.py`, `coordinator_adjudicate.py`, `plan_runner.py`,
`tests/test_accounts.py`) to check what the text claims. I did not read the
authoring session.

## amendment

All ten rows change meaning. Each one adds a qualifier, an actor (the
account), a refusal or a prohibition that the anchored text did not have. So a
correct implementation of the old text could fail the new one, and none of
these is clarity.

- [MEANING] LLR-044 Detail -> selection, preference and cooldowns carry the bare route id -> one entry per enable-list line is what selection, preference and cooldowns carry, a row is read only through entry_route, and a qualified key is ROUTE@ACCOUNT -> two accounts on one route now cool and select independently, and the old text never required that; I would bless it (TC-046 cites the entry-key tests)
- [MEANING] LLR-072 Detail -> two fresh planner sessions with fallback reason codes -> each session also carries its enabled entry, and its model_id is the route that entry selects -> this adds a required carried field and a binding; I would bless it (TC-072 cites test_planner_sessions_carry_their_entry)
- [MEANING] LLR-266 Detail -> adapter choice, prepare, final text and raw usage -> the same, plus the adapter takes the call's composed environment and never selects, replaces or infers an account home -> this is a new prohibition on the adapter; I would bless the text. Note that only TC-362's two-home launches exercise this clause, and TC-362 does not list LLR-266 in Verifies (see first-approval)
- [MEANING] LLR-267 Detail -> codex reads the rollout under the launch environment's CODEX_HOME, or codex's default home when unset -> a qualified Codex call reads only its composed CODEX_HOME and considers no other account's rollout -> for a qualified call this takes away the default-home fallback, which narrows the old rule; I would bless it
- [MEANING] LLR-268 Detail -> the usage(stream) mapping per runner -> the same, plus "usage mapping consumes the environment the call selected" and never sources telemetry from a family or another account's home -> this adds an obligation. I would NOT bless it: usage(stream) reads the stream only and takes no environment (`session_adapters.py`, `usage(self, stream)`), so the new sentence describes an input the mechanism does not have, and the row's own opening clause contradicts it
- [MEANING] LLR-270 Detail -> the retained record is keyed by family, route and scope -> family, route, account and scope, and a record with no account or another account's is no record and mints once -> this changes the record identity. I would NOT bless it. The unchanged LAUNCH clause still says a retained launch runs "under the family's dedicated home (HOME_VARIABLES: CLAUDE_CONFIG_DIR, CODEX_HOME) created under the store's home/ ... opencode keeps its shared home". This row retires that home: the code takes the Prepared account home under the user config directory (`session_keep._hold`, `account_home`), an unqualified entry has no kit-held home, and HOME_VARIABLES now covers opencode and gemini. The amended row contradicts LLR-336 and the code. The new identity sentence also restates LLR-336's record rule, so the same rule has two homes
- [MEANING] LLR-305 Detail -> the family's declared env, dedicated home and token, with refuse_competing for a token route -> the selected entry's account supplies the environment, home and token; refuse_competing applies to "a token account"; compose_env removes competing names, then applies route, account, home and token -> the credential boundary moves from family to account. I would NOT bless it, because it misstates the boundary in both directions. (1) refuse_competing refuses ANY declared account, login accounts included, whose route or account env declares a source its CLI ranks above the account's own (`session_service.refuse_competing`, the round-3/4 Gemini and Claude cases). (2) compose_env withholds competing ambient names only for a declared account. An ambient entry keeps them (`_compose`: `if account is not None`). The row says the removal is unconditional
- [MEANING] LLR-306 Detail -> refuses an unusable route or an unreadable brief -> also refuses an invalid account or a registry error, and the sign-in reading names the adjudicator entry's account -> these are new refusal arms and a new reported field; I would bless the text. Its new refusal arms are verified only by TC-365's test_the_adjudicator_refuses_a_registry_error_an_undeclared_account_or_an_unreadable_list, and TC-365 does not list LLR-306 (see first-approval)
- [MEANING] TC-321 Expected -> the default route is ANTHROPIC-OPUS-STRONG -> the default entry is ANTHROPIC-OPUS-STRONG@ADJUDICATOR -> a test that checks the old default fails the new one; I would bless it (it matches `coordinator_adjudicate.DEFAULT_ROUTE` and `docs/agents-enabled`)
- [MEANING] TC-324 Expected+Method -> a retained launch for a family with a dedicated home needs a readable sign-in, and a family without one passes unprobed -> "Only a retained launch for a login account" needs a readable sign-in, and an unqualified entry has no gate -> the subject moves from family to account. I would NOT bless it. The "Only" excludes token accounts, yet the row's own Method still asserts that an unset, missing, unreadable or empty token file refuses. LLR-305 calls a token account "signed-in" by its file, and `require_signin` refuses a token account, so the Expected contradicts its own Method and its parent

Re-anchor (released rung, mine to re-attest): LLR-044, LLR-072, LLR-266,
LLR-267, LLR-306, TC-321. Not re-anchored, returned through the draft below:
LLR-268, LLR-270, LLR-305, TC-324. Each of those stays drifted in its registry,
so the snapshot refuses to copy either registry until this rework lands (see
the act report).

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-20 headless leg 04): commits 4826e3eec and b1afd77c7, re-sat at sittings 012 and 013. No row is minted from these drafts.

```toml
title = "Restate LLR-268, LLR-270, LLR-305 and TC-324 against the account design WI-798 settled"
workstream = "process"
buildtier = "strong"
sr_refs = ["SR-222", "SR-227"]
priority = 3
specref = "docs/reviews/wi-798/004-ADJUDICATE-028ecf8.md#amendment"
```

What the draft owes, finding by finding:

1. **LLR-268:** drop or restate the environment sentence. usage(stream) reads
   only the call's own stream and reads no home.
2. **LLR-270:** replace the LAUNCH clause's per-family dedicated home under
   the store's home/ (and "opencode keeps its shared home") with the Prepared
   launch's account home. State the unqualified entry's no-home case. Keep the
   record-identity rule in one row and link to it from the other.
3. **LLR-305:** state refuse_competing for every declared account (login and
   token), keep `--bare` as token-only, and make the withholding of competing
   ambient names conditional on a declared account.
4. **TC-324:** restate the Expected so that token accounts and login accounts
   both need their own readable sign-in, consistent with the Method's token
   arm.

VERDICT: MEANING rows=10

## first-approval

The batch goes back. LLR-336 decomposes the right outcome, but its text omits
the credential boundary that rounds 3 and 4 of this lane settled. Its parent
set and the TCs' Verifies cells over-claim and under-claim in specific places.
A first approval would bless an incomplete account boundary as the design of
record.

- [RETURN] LLR-336 -> account tables, the ROUTE@ACCOUNT qualifier, named errors with no fallback, one composition order, account homes under the user config dir, entry identity for cooldowns, planners and records, the adjudicator and dev-setup reporting the account, unverified printed -> SR-154 calls for the registry and consent half, and SR-227 for homes and credentials. SR-222 (the usage record) calls for none of this, and the row says nothing about the usage record -> not ready. (1) The row says a qualified launch uses "ambient, route env, account env and account-home variables in that order". The code (`session_service._compose`, `refuse_competing`) withholds every ambient source the CLI ranks above a declared account's own home or token, and refuses a login or token account whose route or account env declares one. That is the account's credential boundary, and no row states it for login accounts. Five tests in tests/test_accounts.py pin it (test_a_qualified_login_launch_withholds_every_ambient_credential_its_cli_ranks_above_the_home, test_a_token_account_launch_carries_only_its_own_token, test_an_ambient_entry_keeps_the_ambient_environment, test_a_login_account_whose_route_or_account_declares_a_competing_source_is_refused, test_a_gemini_login_account_whose_route_declares_a_vertex_source_is_refused), and no TC cites them. (2) The SR-222 parent is unearned unless the row states an SR-222 arm. (3) Sideways, the row restates entry identity (LLR-044), record identity (LLR-270's new sentence) and the composition order (LLR-305), so each rule has two homes
- [RETURN] TC-361 -> account tables and qualifiers load, malformed ones fail visibly, a cli mismatch refuses, and nothing falls back to ambient -> the evidence covers those arms, but Verifies claims SR-222 and SR-227, and parsing the registry is evidence for neither. Tests of the registry-error arms LLR-336 states (test_an_empty_registry_declares_nothing_and_an_unparseable_one_is_an_error, test_an_account_id_a_platform_would_alias_is_a_registry_error, test_two_ids_that_alias_one_windows_directory_cannot_both_load, test_token_locators_the_platform_resolves_as_one_name_drop_both_accounts, test_a_non_string_account_field_is_the_named_table_error, test_an_absent_registry_with_an_enable_list_fails_preflight) are cited nowhere -> not ready while its SR claims over-reach and its parent is going back
- [RETURN] TC-362 -> every launch and probe uses its selected account's environment -> per the arms map, this is the only verification of the new home clauses in LLR-266, LLR-267, LLR-268 and LLR-305, but Verifies names LLR-336 alone. Its "precedence" assertion follows LLR-336's ambient-first order, which leaves out the withholding the code does. test_the_user_config_dir_follows_the_platform_rule and test_a_token_account_whose_token_cannot_be_read_is_refused_before_its_home, which hold LLR-336's home arms, are cited nowhere -> not ready
- [RETURN] TC-363 -> two accounts on one route cool and select independently -> the evidence holds it, but Verifies claims SR-222 (usage record) and SR-227 (retention), and cooldown selection verifies neither -> not ready while it over-claims those SRs
- [RETURN] TC-364 -> retained state never crosses an account boundary -> the evidence holds it. Verifies claims SR-154 and SR-222, for which this is no evidence, and omits LLR-270, whose new record-identity sentence this TC alone exercises -> not ready
- [RETURN] TC-365 -> the adjudicator uses its declared account without exposing credentials -> the evidence includes LLR-306's new refusal arms (registry error, undeclared account, unreadable list), but Verifies omits LLR-306. Its Method ("Run coordinator sign-in and developer setup against account fixtures") names an instrument and asserts nothing. test_the_signin_probe_names_an_ambient_or_unresolved_entry and test_the_claude_status_reader_takes_only_its_documented_pairs are cited nowhere -> not ready
- [RETURN] TC-366 -> an unverified non-ambient login account is printed, neither refused nor fallen back from, and the owner-held two-login half is excluded -> the text is sound, but Verifies claims SR-222 and SR-227, which an unverified-account print does not evidence -> not ready while its SR claims over-reach. A one-cell fix

## Returns answered in the lane

Answered in the lane (coordinator, 2026-10-20 headless leg 04): commits 4826e3eec and b1afd77c7, re-sat at sittings 012 and 013. No row is minted from these drafts.

```toml
title = "Rework LLR-336 and TC-361..366: state the declared-account credential boundary, earn each parent link, cite every account test"
workstream = "process"
buildtier = "strong"
sr_refs = ["SR-154", "SR-227"]
priority = 3
specref = "docs/reviews/wi-798/004-ADJUDICATE-028ecf8.md#first-approval"
```

What the draft owes:

1. **LLR-336:** state the declared-account credential boundary, using the
   same rule as the amended LLR-305: withholding, and refusal of a declared
   competing source. Either drop SR-222 or state the arm that earns it. Keep
   entry identity, record identity and the composition order each in one row
   and link to it from the others.
2. **TC-361..366:** narrow each Verifies cell to the SRs and LLRs its
   evidence actually holds. Add LLR-266/267/268/305 to TC-362, LLR-270 to
   TC-364 and LLR-306 to TC-365. Cite the 17 uncited tests in tests/test_accounts.py
   where they hold a stated arm, and give TC-365 a Method that asserts
   something.

OUTCOME: RETURN rows=7

SITTING: JUDGED kinds=amendment;first-approval
