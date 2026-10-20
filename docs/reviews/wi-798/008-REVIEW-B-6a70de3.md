Reviewed: 6a70de32ac534ac00c5f4fa6203249ca774db057

# WI-798 full-lane review (independent, Claude Opus), range 9c4971543..6a70de32a

Verified. `git rev-parse HEAD` in the lane printed 6a70de32ac534ac00c5f4fa6203249ca774db057. I read the whole code diff (agent_route, session_service, session_keep, session_adapters, agent_loop, plan_runner, coordinator_adjudicate, the four dev-setup scripts) and the spine, template and RESYNC diffs against the spec, and hunted the failure classes this change allows, worst first: a qualified launch running as the wrong credential (fail-open), a malformed qualifier or account being quietly read as the ambient entry, a token reaching output, and the kit touching a provider home (data loss). I found no code defect in any of them:
- Every launch site goes through `_launch_parts`/`_compose`: the loop worker and probe through `entry_env`/`launch_env`, the dual-plan hats through `_hat_routes`, the coordinator's adjudicate and act through `launch_env`, retained launches through `prepare_launch`, and the version and sign-in probes through `probe_env`. No `parse_env`, `route_env` or family-home read is left outside agent_route and session_service (grep).
- A qualified launch withholds `COMPETING_CREDENTIALS[cli]`, or keeps only `BASE_ENVIRONMENT` for opencode, and refuses a declared competing source.
- Qualifier and account errors are named errors, never stripped. An unreadable enable list raises at all five readers. Records and markers carry `account`. Nothing moves, copies or deletes a home.
- Every `Implements:` tag I checked names an LLR whose `module` has that file and whose `code_symbol` has the symbol (K3). `check_doc_refs` binds `code_symbol` as a union of names, so LLR-305's empty `;;` segment does no harm. No Status flipped, and no SR or SN cell changed.

Real-path evidence:
1. **Empty account home.** I drove `session_service.signin_status` on a scratch empty account home, with no model call. An absent home read `missing`, an empty home read `missing`, an unqualified entry read `ambient`, and the ambient login read `signed-in` through `_claude_signin`. This reproduces the no-spend empty-home half on this box.
2. **Red-before.** I extracted the pre-fix tree at 20bb00a8e into scratch with 6a70de3's tests/test_accounts.py. The round-2 opencode tests fail there (5 failed, 2 passed), so they are red before the fix.
3. **Unreadable enable list.** `keep_warmer` and `agent_route --list` behave correctly on an unreadable enable list: the warmer is off, and `--list` exits 1.
4. **Template example.** Following agents.template.toml's account example literally fails closed (see the template finding below).

Done-when coverage:

| # | Done-when item | Covering test or status |
|---|---|---|
| 1 | Homes, two accounts per CLI, route env never overridden, home variable in a route env refused | test_two_accounts_of_one_cli_launch_under_two_homes[claude/codex/gemini/opencode] and test_the_launch_rule_refuses_a_route_env_that_names_the_home_or_a_shared_key. The family home is gone: the `no family home` asserts in test_session_keep, test_adjudicator_token and test_coordinator_adjudicate. |
| 2 | Unqualified entries as today | test_an_ambient_entry_has_no_kit_held_home, test_an_ambient_entry_keeps_the_ambient_environment |
| 3 | Cooldowns keyed on the entry | test_cooldowns_key_on_the_entry_not_its_route, test_two_accounts_on_one_route_cool_and_select_independently. Unit (b) is in-lane commit 0257de471, which lands squashed. |
| 4 | Unverified accounts printed | test_preflight_prints_each_enabled_unverified_account_only, test_the_loop_preflight_prints_the_unverified_account_and_passes_it, test_the_signin_probe_reads_a_login_account_from_its_own_home. The lane record is UNCOVERED (see the evidence finding). |
| 5 | Spine rows | UNCOVERED at this tip (MAJOR below) |
| 6 | Test bar | Affected-module tests are green below. The smoke tier was not run, per the round facts. |
| 7 | Token account and adjudicator | test_adjudicator_token.py, test_coordinator_act.py's two account tests, TC-365's tests. In-lane signed-in evidence is UNCOVERED. |
| 8 | Trust arms | Covered except the keep-warm and `agent_route --list` unreadable arms (MINOR below). |
| 9 | Review bar | This review. |
| 10 | RESYNC entry | Present, anchored `[since 9c4971543]`. |

Disclosure: trace.py rewrote the gitignored docs/test/report.md in the lane. `git status` stayed clean, and I created nothing else in the worktree.

Commands:
- `git rev-parse HEAD` (lane) -> `6a70de32ac534ac00c5f4fa6203249ca774db057`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r2-opus/wi-798 tests/conftest.py tests/test_accounts.py ... tests/test_session_keep.py` (the round facts' list) -> `801 passed, 40 skipped in 375.86s` (27 posix-shell gated skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (950 work item(s), 839 done (88%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=132 LLR=307 TC=326 orphans=0 integrity=0 ... drafts=8 ... interface-findings=0 ...`
- scratch probe `probe/signin_probe.py` (real `signin_status`, `_run_status`, `_claude_signin`) -> `absent home: missing`, `empty home: missing`, `ambient entry: ambient`, `ambient claude auth status -> signed-in`
- `git archive 20bb00a8e` into scratch + 6a70de3's tests/test_accounts.py, `pytest -k opencode` -> `5 failed, 2 passed`
- scratch probe `probe/tmpl_probe.py` (agents.template.toml with its account example uncommented + `ANTHROPIC-OPUS-STRONG@ADJUDICATOR` enabled) -> `'ANTHROPIC-OPUS-STRONG@ADJUDICATOR' is not a row in docs/agents.toml ...`
- scratch probe `probe/kw_probe.py` (enable list as a directory) -> `keep-warm: off (...)`, `warmer: None`, `agent_route --list exit: 1`
- `python project-trajectory/scripts/coordinator_adjudicate.py signin --retained --root .` (lane) -> `signin [ADJUDICATOR] token: missing` (AGENT_CLAUDE_TOKEN_FILE is unset at process, user and machine scope in this reviewer's environment)

Findings:

- [MAJOR] docs/requirements/low-level-requirements.toml:3039 -> K1, Done-when item 5. At the reviewed tip the spine text is false against the code. **LLR-270 (line 3039):** LAUNCH still says a retained launch runs "under the family's dedicated home (HOME_VARIABLES: CLAUDE_CONFIG_DIR, CODEX_HOME) created under the store's home/". Its lease-only record still holds "family, route_id and the lease", and its rationale still says "The dedicated homes keep a retained transcript out of a person's own sessions". In the code, `session_keep.HOME_VARIABLES` and `dedicated_home_env` are deleted, and `_hold`/`_warm_keep` take `prepared.home`: the account home, or nothing for an unqualified entry, which now runs in the person's own home. **LLR-305 (line 3241):** `refuse_competing` still applies to "a token account" and compares names "by _name_key". That helper is deleted. The code refuses login accounts too (`_LOGIN_SOURCE`) and compares with `agent_route.env_name_key`. The row also says `compose_env` removes competing names, but an ambient entry withholds nothing and a qualified opencode launch keeps only `BASE_ENVIRONMENT`. **LLR-336 (line 3469):** says "provider state is never read", but `session_adapters._codex_rollout` reads Codex rollouts under the account's `CODEX_HOME`. It also states neither the withholding of ambient credentials nor opencode's declared base. **Status:** LLR-336 and TC-361..TC-366 are still Drafted, returned at sitting 004. -> Amend those cells to match the code: account home or ambient login, the account in the lease-only record, `env_name_key`, refusal for login and token accounts, ambient withholding and `BASE_ENVIRONMENT`, rollout reading for telemetry only. Then carry LLR-336 and TC-361..366 through the checkpoint adjudication before landing (adds no guard, so no unrepresentable clause is owed). -> @coordinator
- [MINOR] docs/requirements/system-requirements.toml:1710 -> for clarity (K2). SR-227's long-lived-credential and sign-in clauses apply "before retaining a family that uses a dedicated CLI home", and this change retires that home. So the Approved SR no longer states the obligations LLR-305 and LLR-336 implement for a token account: read the token at each launch, keep it out of every output, refuse an unreadable token. Its rationale ("escaping into a person's default home") also now describes the designed behaviour of an unqualified retained launch. -> File the owner-authority wording successor that restates these clauses per declared account. The approved text stays until it is amended through its authority. -> @owner
- [MINOR] project-trajectory/agents.template.toml:73 -> The example says "uncomment it, name that entry on docs/agents-enabled". But the template has no `ANTHROPIC-OPUS-STRONG` row, so a scaffold that follows it gets `'ANTHROPIC-OPUS-STRONG@ADJUDICATOR' is not a row in docs/agents.toml` (driven above), and with agents-enabled present the managed preflight fails. RESYNC_PACK.md:9199 (step 3) is also conditional ("If your retained adjudicator used the long-lived token"). Yet the new `DEFAULT_ROUTE` refuses every adopter's default `adjudicate`/`act`/`signin` that lacks the account, whatever their retention. -> Say the route side must be a row of their own registry (or name their own entry), and make "declare the account or pass `--route`" an unconditional RESYNC step. This fails closed with a named error, hence MINOR. -> @coordinator
- [MINOR] project-trajectory/scripts/session_service.py:1762 -> Done-when item 8 ("a test for each consumer's absent, unreadable and malformed arms"). No test covers the unreadable enable-list arm of `keep_warmer` (it prints `keep-warm: off` and returns None) or of `agent_route.main` (project-trajectory/scripts/agent_route.py:1658, exit 1). I drove both and they behave correctly, but deleting either `except EnabledUnreadable` would fail no test. -> Add one test per arm (a test, not a guard: no clause owed). -> @coordinator
- [MINOR] docs/work/active/wi-798/WI-798-account-tables-and-homes.md:317 -> Done-when items 4 and 7 need lane evidence, and the range holds none:
  - no lane record of the no-spend empty-home half;
  - no lane record of `signin --retained` reading signed-in on the declared account;
  - the in-lane sitting's session log names no account.

  Only a docstring claim exists (`session_service._claude_signin`). I reproduced the empty-home half (above). I could not reproduce signed-in, because AGENT_CLAUDE_TOKEN_FILE is not set in this environment. -> Record both observations, with the account the sitting launched under, in the lane log before close (no clause owed). -> @coordinator
- [MINOR] docs/process.toml:297 -> for clarity. "Since WI-798 the adjudicator runs on the declared token account ADJUDICATOR" sits on the dial that governs both routes. But the loop's adjudications draw the unqualified `ANTHROPIC-OPUS-STRONG` under the person's ambient login, because the `@ADJUDICATOR` entry is weighted 0 in every phase. Only `coordinator_adjudicate.py`'s default entry runs on ADJUDICATOR. -> Name the coordinator route, and say the loop route runs on the ambient login. -> @coordinator

Coverage-extension note (no severity): a template whose first token is a quoted path containing a space resolves to no IF-245 CLI in `route_cli`. A qualified entry on it is refused with a CLI-mismatch error, which fails closed.

VERDICT: CHANGES-REQUESTED findings=6
