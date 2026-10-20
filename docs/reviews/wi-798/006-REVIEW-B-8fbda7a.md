Reviewed: 8fbda7ac24bf704123bf0fb107507cd9f55b5caf

WI-798, full-lane review (REVIEW-B, Claude Opus), range 9c4971543..8fbda7ac2, rubric docs/rubrics/kit-change-review.md.

**Failure classes hunted first, worst first:** (1) silent wrong credential: a qualified entry launching under the ambient login, another account's home or an ambient competing credential, or an unqualified one picking up a kit home or token; (2) fail-open on bad input: an unreadable enable list read as routing off, a malformed qualifier reduced to the bare route, registry errors thrown away; (3) a retained session crossing an account boundary (record or marker identity); (4) the token leaking into a log, record or refusal; (5) the kit creating, moving or deleting a provider home.

**Verified.** I read the whole reading-scope diff, drove the shipped code from scratch probes, and found no fail-open, data-loss or credential-crossing path. The details:

- **Code paths I drove:** `agent_route.load_registry`, `resolve_enabled`, `session_service.entry_env`, `prepare_launch`, `probe_env`, `signin_status`, `require_signin`, and `coordinator_adjudicate signin` on a scratch registry. It had two codex accounts, a claude login account, a claude token account, an opencode account, a home-variable route env and five bad qualifiers.
  - The two codex accounts got two different `CODEX_HOME`s.
  - `CLH@L` (the route env sets `claude_config_dir`, lower-case, on Windows) was refused.
  - `CX@L` (wrong CLI), `CX@`, `@A1`, `CX@A1@A2` and `CX@NOPE` each came back as an enable-list error naming its line. None was reduced to the bare route.
  - A claude login account dropped the ambient `ANTHROPIC_API_KEY` and `CLAUDE_CODE_OAUTH_TOKEN`. A codex account dropped `OPENAI_API_KEY`. A token account carried only its own token, and its probe environment did not carry it.
  - The unqualified `CL` inherited the ambient environment exactly, with no home.
- **Real-CLI check:** under the real `claude` 2.1.296, a login account with an empty home read `missing` through `_claude_signin`, and `require_signin` refused it, naming `CLAUDE_CONFIG_DIR=<home> claude auth login`. I reproduced the no-spend empty-home half of the isolation check myself: an empty `CLAUDE_CONFIG_DIR` gives `loggedIn: false`, exit 1; the ambient login gives `loggedIn: true`, exit 0.
- **Record identity:** `_IDENTITY` makes `account` required, so a record written before accounts fails `_variant` and reads as not its own. Markers carry `account`. `_record_name`, `_marker_name`, `_pending`, `store_load` and `retire_scope` all take the one `_identity_of` tuple order.
- **Keep-warm:** it pings only `(route, account)` pairs still enabled whose account resolves.
- **No home deletion:** nothing in the diff deletes or moves a home. Only a token account's home is ever created (`_launch_parts`), and only after its token reads.
- **Redaction:** it now also covers an unretained launch whose environment carries a token variable.
- **Commit order:** the first lane commit (0257de471) is the structural, behaviour-preserving entry-identity commit, as the spec orders.
- **Regression tests fail on the pre-fix behaviour** (checked with a pytest plugin in the scratch directory that restores the old rule):
  - D-010, the act turn ignoring its account environment: `test_an_act_turn_on_the_default_entry_launches_under_its_accounts_environment[fresh]` FAILS (`assert None is not None`).
  - Review 001, competing sources withheld only when a credential is carried: `test_a_qualified_login_launch_withholds_every_ambient_credential_its_cli_ranks_above_the_home[claude|codex|gemini]` FAILS (3 failed, 1 passed; opencode's list is empty).
- **Tests are re-pointed, not deleted:** WI-846's and WI-834's tests are re-pointed at the account (for example, test_adjudicator_token's canary sweep now includes the account home).
- **Rubric anchors:**
  - K2: no SN or SR row changed.
  - K3: `trace.py --strict-integrity` reports integrity 0. The new `Implements:` tags name LLRs whose `module` holds the file. LLR-336 is the only new LLR, and it is Drafted. No Status flipped. I checked for mojibake in the edited registries: there is none, the bytes are clean UTF-8.

**Done-when map.**

1. **Two accounts, two homes, per adapter; route env never overridden; a home-variable route env refused; family home gone.** Covered by tests/test_accounts.py::test_two_accounts_of_one_cli_launch_under_two_homes[claude|codex|gemini|opencode] and ::test_the_launch_rule_refuses_a_route_env_that_names_the_home_or_a_shared_key, plus my probe. `session_keep.HOME_VARIABLES`, `dedicated_home` and `dedicated_home_env` are deleted. COVERED.
2. **Unqualified entries as today; a retained one moves to no family home.** Covered by ::test_an_ambient_entry_has_no_kit_held_home and ::test_an_ambient_entry_keeps_the_ambient_environment, and by my probe (`prepare_launch` gives home `{}`). COVERED.
3. **Entry-keyed cooldowns, landed first.** Covered by tests/test_agent_route.py::test_cooldowns_key_on_the_entry_not_its_route and test_accounts::test_two_accounts_on_one_route_cool_and_select_independently. First commit 0257de471. COVERED.
4. **Unverified account printed at preflight and by signin; empty-home half recorded.** Covered by ::test_preflight_prints_each_enabled_unverified_account_only, ::test_the_loop_preflight_prints_the_unverified_account_and_passes_it and ::test_the_signin_probe_reads_a_login_account_from_its_own_home. I reproduced the empty-home half independently; the lane's log record of it is outside my reading scope. COVERED.
5. **Spine rows amended and adjudicated.** NOT MET at this tip: see the MAJOR and the first MINOR below. LLR-336 and TC-361..366 are still Drafted, waiting for the checkpoint D-013 sequences.
6. **Test bar.** The affected modules ran green under me. I did not run the smoke tier, because the round facts forbid it. The scaffold-bootstrap tests are green, and so is test_run_devsetup with sh on PATH.
7. **The token moves to the declared account; the adjudicator runs there; the record re-mints once; signin and dev-setup report the account; RESYNC.** Covered by test_adjudicator_token (all of it), test_accounts::test_a_record_written_before_accounts_is_not_its_own_and_mints_once, the test_run_devsetup sign-in tests, and the RESYNC entry. PARTIAL. The live sitting and `signin --retained` reading signed-in could not be seen on this box: `AGENT_CLAUDE_TOKEN_FILE` is unset in process, user and machine scope here, so signin reads `signin [ADJUDICATOR] token: missing`. The base's family probe would read missing on this box too, so this is not a regression.
8. **Every Trust ruling has absent, unreadable and malformed arms per consumer.** Covered by test_accounts: loader, loop preflight, dual-plan and its fallback, adjudicator, session service, store. The rollout reader is unchanged and keeps its existing tests. COVERED.
9. **RESYNC entry anchored at 9c4971543.** Present. COVERED.

**Relationship decisions (changed side -> counterpart -> my decision).**

- **IF-045 (agents.toml data) -> LLR-044 / LLR-336 (the agent_route reader):** carried.
- **IF-162 -> agent_route:** carried (`EnabledUnreadable`).
- **IF-162 -> dispatch:** retained. It reads the file's presence only, and the spec's ruling on unchanged readers covers it. Accepted.
- **IF-044 -> the loop, session_service, plan_runner and coordinator_adjudicate:** carried. Each reads rows through `entry_route` / `account_of`. I grepped for any other caller and found none.
- **IF-245 -> LLR-266 (amended) and TC-262 (retained):** retaining TC-262 is justified. Its purpose, adapter selection and structured output, is unchanged, and the home-variable facts are verified by TC-362 under LLR-336, so a copy under LLR-266 would add nothing independent.
- **LLR-267 / LLR-268 -> TC-263 / TC-264:** retained, justified. The added sentences restate unchanged pass-through behaviour.
- **IF-247 -> LLR-270:** only partly carried (the MAJOR below).
- **IF-247 -> TC-267, and IF-248's notes:** stale (the first MINOR below).
- **IF-282 -> LLR-305:** only partly carried (the MAJOR below).
- **IF-282 -> TC-324 and TC-330:** stale (the first MINOR below).
- **IF-283, IF-284, IF-285 -> LLR-306 and TC-323:** carried (the default entry, exit 7, the signin lines). One gap: LLR-306 does not yet state that the act turn runs under the entry's account, which D-010 owes (folded into the MAJOR).
- **SR-227 (parent):** retained unchanged, as the brief requires. Its clause now reads vacuously (the `for clarity` MINOR below).
- **SR-154 / SR-222 (parents):** retained. LLR-336's obligations sit inside them.

**Decomposition of LLR-336.** Each child verifies a separate consumer boundary with its own failure class:

- TC-361: the loader and the qualifier grammar.
- TC-362: launch-environment composition across the four adapters.
- TC-363: entry-keyed cooldown, selection and the planner pool.
- TC-364: record and marker identity, the one re-mint, and keep-warm.
- TC-365: the adjudicator's and dev-setup's readings.
- TC-366: unverified visibility.

Splitting further, per adapter or per arm, would add no independent decision, because the tests already parametrize those arms.

**Inputs outside the declared set that fail closed (notes, no severity):**

- A route template whose first token is a wrapper (`npx claude`, `uv run …`) names no IF-245 CLI, so every qualifier on it is refused.
- Whether macOS keychain storage isolates logins per home is WI-908's question (held by OI-114). It is printed as unverified, not tested.

I also considered D-002, which lets the weight-0 line hand loop draws to the token account when its tier's other entries are cooling. Under an ambient login a worker can already read the login's credential file in its home, so the token in the environment is no new exposure. I leave it to D-002's owner confirmation.

**Commands** (run from C:/Projects/ai-template.wt/wi-798 with GIT_CEILING_DIRECTORIES set as the round facts say):

- `git rev-parse HEAD` -> `8fbda7ac24bf704123bf0fb107507cd9f55b5caf`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1-opus/wi-798 <the 15 listed modules>` -> `796 passed, 40 skipped in 690.61s (0:11:30)` (27 of the skips are gated on posix-shell)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (950 work item(s), 839 done (88%), 30 cancelled, graph acyclic).` (advisory WARNs only; one is the expected `completion WI-798: status=active but a commit ... carries a WI: WI-798 trailer`)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=132 LLR=307 TC=326 orphans=0 integrity=0 verified-mechanized=125 verified-demonstrated=6 verified-attested=0 drafts=8 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=246 interface-findings=0 ac-advisories=1 paraphrase-advisories=2.` exit 0; `git status --short` was empty afterwards
- PATH prefixed with Git\bin, `pytest -n 2 --basetemp .../r1-opus/devsetup-sh tests/test_run_devsetup.py tests/test_accounts.py` -> `152 passed, 13 skipped in 83.45s`
- `pytest -p mut_act_env --basetemp .../r1-opus/mut-act2 tests/test_coordinator_act.py -k accounts_environment` (D-010 fix reverted) -> `1 failed, 1 passed` (the [fresh] arm fails)
- `pytest -p mut_compose --basetemp .../r1-opus/mut-compose tests/test_accounts.py -k withholds_every_ambient_credential` (pre-fix withholding rule) -> `3 failed, 1 passed`
- `python project-trajectory/scripts/coordinator_adjudicate.py signin --retained --root .` -> `signin [ADJUDICATOR] token: missing` / `signin [ADJUDICATOR]: token_file_variable AGENT_CLAUDE_TOKEN_FILE` (the variable is unset in every scope on this box)
- `python project-trajectory/scripts/agent_route.py --list` -> seven entries, `ANTHROPIC-OPUS-STRONG@ADJUDICATOR strong ANTHROPIC` last, exit 0
- `claude auth status` with CLAUDE_CONFIG_DIR set to an empty scratch home -> `"loggedIn": false`, exit 1; ambient -> `loggedIn=true`, exit 0 (claude 2.1.296)
- Scratch probes probe/p1.py, probe/p2.py, and `coordinator_adjudicate.py signin --retained` on scratch root probe/s3 (retention on, no account) -> `signin [-] unresolved: unknown ('ANTHROPIC-OPUS-STRONG@ADJUDICATOR': account ADJUDICATOR is not declared in docs/agents.toml)`

**Findings.**

- [MAJOR] docs/requirements/low-level-requirements.toml:3039 -> Done-when gap and K1: the two Approved rows the spec names as made untrue are still false in the text they keep. LLR-270's detail still says a retained launch runs "under the family's dedicated home (HOME_VARIABLES: CLAUDE_CONFIG_DIR, CODEX_HOME) created under the store's home/ … opencode keeps its shared home". Its rationale (line 3040) says "The dedicated homes keep a retained transcript out of a person's own sessions". In the code, `session_keep.HOME_VARIABLES` and `dedicated_home_env` are deleted, and `_hold` takes `prepared.home`, which is `{}` for an unqualified entry, so an ambient retained session runs in the person's own home; opencode accounts now get homes. LLR-305's detail (line 3241) says compose_env removes "competing credential names" with no condition and that refuse_competing refuses "a token account". In the code, `_compose` withholds those names only under a declared account (project-trajectory/scripts/session_service.py:1332), and `refuse_competing` refuses any declared account, login accounts included. Also, LLR-306 does not yet state that the act turn runs under the entry's account (owed by D-010). -> Rewrite those sentences to the account-home rule; add the act-under-account sentence to LLR-306; and take LLR-270, LLR-305, LLR-306 and the Drafted LLR-336 / TC-361..366 through the D-013 checkpoint before landing. A text amendment, no guard. -> @coordinator
- [MINOR] docs/test/test-cases.toml:3310 -> K1: TC-324's expected cell says "Only a retained launch for a login account requires a readable sign-in". That is false: a token account's retained launch is refused when its token cannot be read (`launch_credential`, and test_a_token_that_cannot_be_read_refuses_before_launch in the row's own evidence). Its method still says the launch "leaves no dedicated home". Three counterparts still describe the retired per-family home: TC-267 expected (line 3021, "under its dedicated home"), TC-330 expected (line 3044, "the dedicated home's CLI transcript"), and IF-248 notes (docs/requirements/interfaces.toml:2317, "the dedicated CLI home directories it creates there"; session_keep creates no home now). -> Reword each to the account home, and state the token-account arm in TC-324's expected cell. -> @coordinator
- [MINOR] docs/requirements/system-requirements.toml:1710 -> for clarity, K1: the Approved parent SR-227 binds its long-lived-credential clause to "a family that uses a dedicated CLI home". After this change no family uses one, so read literally the clause binds nothing, while LLR-305 and LLR-336 implement it for token accounts. It is retained unchanged here, as the brief requires. -> Sharper SR language ("a retained call whose account authenticates with a long-lived credential"), amended through its own authority. -> @owner
- [MINOR] project-trajectory/scripts/dev-setup.template.ps1:222 -> `signin [-] unresolved: unknown (<why>)` falls into the default arm. The reader is told the check "could not be read (it needs a Python 3.11+ runtime …)"; the probe's real reason is thrown away and nothing counts as missing. The same arm exists in dev-setup.template.sh:261, scripts/dev-setup.ps1:218 and scripts/dev-setup.sh:246. This is reachable: an adopter who turns retention on and resyncs without RESYNC step 3 (or this repo, if its account table is dropped as malformed) sees this line. My scratch root printed `account ADJUDICATOR is not declared`, and test_run_devsetup.py:670 pins `[unknown]` for exactly this state. Before this change the same scaffold was told `[missing] … claude setup-token`. -> Add an `unresolved` arm that prints the probe's reason and the step-3 remedy, and counts it as missing. -> @coordinator
- [MINOR] scripts/coordinator/README.md:57 -> for clarity: the operator steps still say "Confirm the dedicated home is signed in" and give exit 7 as "a home that is not signed in (sign in through dev-setup)". project-trajectory/skills/coordinator-cycle/references/recipes.md:339 and its .claude copy say "The retained Claude home authenticates with the owner's long-lived token". The adjudicator now runs on the declared ADJUDICATOR account, and signin prints `signin [ADJUDICATOR] token: <status>`. The spec lists recipes.md as a wording consumer. -> Reword both to the account and its signin line. -> @coordinator
- [MINOR] project-trajectory/scripts/session_service.py:1090 -> simplification: `_name_key` and `_CASE_INSENSITIVE` restate `agent_route.env_name_key` (project-trajectory/scripts/agent_route.py:299). So the registry-time checks (`qualifier_problem`, `_account_problem`, the token-variable duplicate drop) and the launch-time ones (`_compose`, `refuse_competing`) fold environment names through two copies of one platform rule, which can drift (one is a patchable module constant, the other reads `os.name`). -> Have `_name_key` delegate to `agent_route.env_name_key` and delete the second constant. This removes code; it adds no guard. -> @coordinator

VERDICT: CHANGES-REQUESTED findings=6
