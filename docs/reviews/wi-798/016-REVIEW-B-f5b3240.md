Reviewed: f5b3240614eacd24529294b20b5a1797248d501f

## WI-798 full-lane review (REVIEW-A, convergence stance, rubric docs/rubrics/kit-change-review.md)

**Verified.** The checkout HEAD was f5b3240614eacd24529294b20b5a1797248d501f. I read the full diff (scoped as the brief says) against the spec, its Trust section and the PROCESS.md threat model. I looked hardest at three failure classes: one account's credential or home leaking into another account's launch (fail-open), a malformed or unreadable consent input read as routing off or as the ambient login, and retained-record identity crossing accounts.

I drove the shipped code in scratch probes (scratch dir only):
- **Two homes, isolated credentials.** Two codex accounts compose two distinct `CODEX_HOME`s. The route env (`FOO`) is kept and the account env (`BAR`) is added. Ambient `OPENAI_API_KEY` is withheld under both accounts and kept for the unqualified entry.
- **Token account.** It refuses with the variable named while the variable is unset. Once set, it carries only its own `CLAUDE_CODE_OAUTH_TOKEN`; ambient `ANTHROPIC_API_KEY` and ambient `CLAUDE_CODE_OAUTH_TOKEN` are dropped. Its home is created empty.
- **Login account.** With no home it is refused, naming the provisioning prose, and the home is not created. It prints UNVERIFIED.
- **Malformed inputs.** Lower-case ids, `CON` and an `env` naming `codex_home` are registry errors, and those tables are dropped. `R@`, `@A`, `R@A@B`, an undeclared account, a lower-case account and a cross-CLI account are each an enable-list error, never the unqualified entry.
- **Empty-home half of the isolation check.** I reproduced it with real claude 2.1.296: `claude auth status` under an empty `CLAUDE_CONFIG_DIR` printed `"loggedIn": false` at exit 1. `signin_status` reads that home `missing` and an absent home `missing`. The ambient login reads `signed-in`.
- **This repo's own registry and list.** They load with zero errors, and `agent_route.py --list` exits 0 and lists `ANTHROPIC-OPUS-STRONG@ADJUDICATOR`.

**Red-before checks.** For each code-fix commit I ran its added tests (located with `git log -p --format=%h`) against its parent's scripts. Each fix's regression tests fail on the parent code:
- afa7da16c: 19 failed, 5 passed. The 5 that pass pin preserved ambient behaviour.
- 31b8d6eeb: 1 failed.
- 6a70de32a: 5 failed, 1 passed (the unqualified-unchanged pin).
- 3e405dab9: 5 failed. The 2 that pass are the unreadable-list arms it adds as coverage, not as fixes.
- 4ecb6d970: 1 failed.

**The structural commit preserves behaviour.** Commit 0257de471 is the lane's first code commit. Under it, the base 9c4971543 tests (test_agent_route, test_agent_loop_routing, test_coordinator_adjudicate) pass 150/150. Every caller of `load_enabled`/`load_enabled_entries` handles `EnabledUnreadable`. No test function was deleted. `HOME_VARIABLES`, `dedicated_home`, `dedicated_home_env`, `TOKEN_VARIABLES` and `route_env` are gone from shipped code.

**Done-when map.**
- **Two homes per adapter, route env never overridden, home-variable route env refused, per-family home gone.** Covered by test_two_accounts_of_one_cli_launch_under_two_homes[claude|codex|gemini|opencode] and test_the_launch_rule_refuses_a_route_env_that_names_the_home_or_a_shared_key. The removed symbols confirm the family home is gone.
- **Unqualified entries unchanged.** Covered by test_an_ambient_entry_has_no_kit_held_home and test_an_ambient_entry_keeps_the_ambient_environment, plus the re-pointed test_session_keep retained cases.
- **Cooldowns key on the entry, structural commit first.** Covered by test_cooldowns_key_on_the_entry_not_its_route and test_two_accounts_on_one_route_cool_and_select_independently; the structural-commit check is above.
- **Unverified printed, never refused.** Covered by test_preflight_prints_each_enabled_unverified_account_only, test_the_loop_preflight_prints_the_unverified_account_and_passes_it and test_the_signin_probe_reads_a_login_account_from_its_own_home.
- **Empty-home half recorded.** Partial: see the last finding.
- **Spine rows.** LLR-266/267/268/270/305/306, IF-044/045/162/245/246/247/282..285 and TC-262..265 are amended. LLR-336 and TC-361..366 are added, Drafted. No Status flipped. Whether each passed adjudication is a process record outside my reading scope.
- **Test bar.** The affected-module run is below; the smoke tier was not run, per the round facts; the scaffold bootstrap is covered by test_bootstrap.
- **Token moves to the account.** Covered by test_adjudicator_token (re-pointed), test_a_token_account_home_is_created_empty_and_carries_the_token, test_the_token_is_read_at_launch_and_never_logged and test_a_record_written_before_accounts_is_not_its_own_and_mints_once. The in-lane sitting's evidence lives in docs/reviews and docs/iteration, which the stance excludes, so I did not verify it. In my shell `signin` reads `signin [ADJUDICATOR] token: missing`, as expected with `AGENT_CLAUDE_TOKEN_FILE` unset here.
- **Trust rulings per consumer.** Covered by tests/test_accounts.py (absent, unreadable and malformed arms for the loader, the loop, plan_runner, coordinator_adjudicate, keep-warm and the route CLI) and tests/test_run_devsetup.py.
- **RESYNC entry anchored at 9c4971543.** Present.

**Requirement/interface counterparts.** For each changed row, its counterpart and my decision:
- **LLR-305, LLR-270, LLR-336 against SR-227.** Retain SR-227. Its credential and sign-in clauses read true for an account home, and an ambient entry has no dedicated home, so they impose nothing on it. The wording is a clarity finding below.
- **LLR-044 against SR-154; LLR-072 against SR-155.** Retain both. An entry is still a selection over declared (family x model x tier) rows under the consent surface.
- **LLR-266/267/268 against SR-222.** Retain. The additions only say what environment the adapter reads.
- **LLR-306 against SR-231, SR-227, SR-209.** Retain.
- **IF-044/045/162/245/247/283/285 against their owner and consumer code.** Each was carried correctly.
- **IF-246 and IF-282.** Not carried correctly (finding 1).
- **LLR-336's decomposition into TC-361..366.** Each case verifies a distinct arm: parse and qualifier, launch environment, cooldown and planner, record identity, adjudicator, sign-in and dev-setup, and unverified. Each already enumerates per-arm tests, so splitting further adds no independent decision.
- **K2.** No SN or SR row changed. The LLR and TC rows name only shipped boundary artifacts (docs/agents.toml, docs/agents-enabled, templates).

**Coverage-extension note (no severity).** opencode and gemini login accounts have no `SIGNIN_PROBES` entry. A retained launch on one therefore always reads `unknown` and is refused: it fails closed.

**Disclosures.**
- One `git show 3e405dab9` printed that commit's message. I did not rely on it.
- `trace.py` rewrote the gitignored `docs/test/report.md` in the worktree. `git status` stays clean.

**Commands**
- `git rev-parse HEAD` -> f5b3240614eacd24529294b20b5a1797248d501f
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../g-opus/wi-798 tests/conftest.py tests/test_accounts.py ... tests/test_session_keep.py` (the round's 15 paths) -> `811 passed, 42 skipped in 397.33s` (29 skips are the posix-shell gate)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (950 work item(s), 839 done (88%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=132 LLR=307 TC=326 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.`
- Red-before checks, each with the fix commit's tree plus its parent's `project-trajectory/scripts` and `scripts`, running `pytest tests/test_accounts.py -k <added tests>`:
  - afa7da16c: 19 failed, 5 passed
  - 31b8d6eeb: 1 failed
  - 6a70de32a: 5 failed, 1 passed
  - 3e405dab9: 5 failed, 2 passed
  - 4ecb6d970: 1 failed
- Structural check (base 9c4971543 tests on 0257de471 scripts): `pytest tests/test_agent_route.py tests/test_agent_loop_routing.py tests/test_coordinator_adjudicate.py` -> `150 passed`
- Probes probe1.py, probe2.py and probe3.py in the scratch dir (results above). probe3 runs `select()` over this repo's real registry and enable list.
- `CLAUDE_CONFIG_DIR=<empty scratch dir> claude auth status` -> `"loggedIn": false`, exit=1 (claude 2.1.296)

**Findings**

- [MINOR] docs/requirements/interfaces.toml:2291 -> (K1) IF-246's `data` lists `route_runner(entry)` in session_service's call surface, and IF-282 does the same at :2531. session_service defines no `route_runner`. The function is `agent_route.route_runner(template, model)` (project-trajectory/scripts/agent_route.py:320), and IF-044 (interfaces.toml:778), the agent_route seam it belongs to, does not list it. -> drop `route_runner(entry)` from IF-246 and IF-282, and add `route_runner(template, model)` to IF-044's `data` -> @owner
- [MINOR] project-trajectory/scripts/agent_route.py:248 -> (K3) the 35 new `Implements: SR-222, LLR-336` tags across the scripts name SR-222 as the parent. LLR-336 traces only to SR-154 and SR-227 (docs/requirements/low-level-requirements.toml:3465), so each tag claims an SR its LLR does not trace to. trace.py does not catch this (integrity=0). -> either add SR-222 to LLR-336's `sr_refs` (it is the work item's SR) or re-tag the functions with LLR-336's actual parents -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3241 -> (K1, for clarity) LLR-305's detail says, without condition, that "compose_env builds the launch environment by removing names the launch sets and competing credential names". `_ambient_base` (project-trajectory/scripts/session_service.py:1420) withholds competing names only under a declared account: a retained launch on an unqualified entry inherits them. -> scope the sentence to "under a declared account (an ambient entry inherits the ambient environment)", re-attested through LLR-305's authority -> @owner
- [MINOR] docs/requirements/system-requirements.toml:1710 -> (K1, for clarity) Approved SR-227 still frames the credential and sign-in obligation as "before retaining a family that uses a dedicated CLI home". Its changed children (LLR-270, LLR-305, LLR-336) now bind it per declared account and exempt unqualified entries. I keep the parent, because its text stays true read per account home, but "family" now misleads a reader. -> at SR-227's next amendment through its authority, word the clause per account home ("a retained launch under an account with a home or token") -> @owner
- [MINOR] docs/process.toml:301 -> (K1) the dial comment says "The loop's adjudication draws the unqualified route, on the person's ambient login". docs/agents-enabled:58 weights the adjudicator's token entry 0, and that zero weight does not hold it out of heterogeneity-filtered draws. probe3 runs `select()` over this repo's own registry and enable list with ANTHROPIC-OPUS-STRONG cooling and OPENAI excluded. In the REVIEW, ADJUDICATE and BUILD phases it picks `ANTHROPIC-OPUS-STRONG@ADJUDICATOR` on every counter, and an ANTHROPIC win-stay pin picks it too. So loop sessions run on the owner's adjudicator token whenever ambient Opus cools. Where `AGENT_CLAUDE_TOKEN_FILE` is unset in the loop's environment, that draw stops the run NEEDS-HUMAN (project-trajectory/scripts/agent_loop.py:1754) rather than cooling the entry. -> make the process.toml comment state that the entry is reachable from the loop's strong-tier cross-family draws and pins while the ambient row is cooling (as agents-enabled's own comment half-says), or decide that the coordinator's entry should not be loop-drawable at all -> @owner
- [MINOR] project-trajectory/scripts/session_service.py:888 -> (Done-when, the empty-home half) the only in-range record of the no-spend empty-home observation is the `_claude_signin` docstring ("an empty home read `loggedIn: false` at exit 1 ... on this box 2026-10-11"). The range adds no log fragment, while the spec says the result is "recorded in the lane log". I reproduced the observation independently (above), so the behaviour holds; only its record is thin. -> record the empty-home check, with its date, CLI version and readings, in the lane's close-out log fragment at landing -> @owner

VERDICT: APPROVE findings=6
