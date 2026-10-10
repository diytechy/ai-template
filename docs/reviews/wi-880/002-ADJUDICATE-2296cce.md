# WI-880 lane checkpoint: adjudication sitting 002 at 2296cce

Read with sitting 001 (`001-ADJUDICATE-9a39f47.md`) and the lane's answers in `501e55e4` and `2296cce7` (decisions D-002 and D-003 in `docs/decisions/wi-880.toml`).

## amendment

Anchor: `docs/archive/last_approved` (system-requirements.toml at fb1990aa; low-level-requirements.toml and test-cases.toml at d0a4b623).

- [MEANING] SR-019 AcceptanceCriteria -> the hook runs the integrity floor and secrets scan on staged content and blocks a failing commit; `--no-verify` is caught by the hosted re-run -> the same, PLUS: with no interpreter at the runtime floor the commit hooks refuse the commit, name the install step, and neither run below the floor nor skip it -> not the same: a new acceptance case. BLESSED. The cell is unchanged since sitting 001, which blessed it; the "commit hooks" note recorded there stands.
- [MEANING] LLR-021 Detail -> a probe that runs candidates and skips or reports clearly, shared by pre-commit and pre-push -> `kit_python`, one probe for pre-commit, commit-msg and pre-push: venv candidates, then developer setup's search, the first 3.11+ executable, and with none a refusal naming the install step (overridable by `KIT_DEV_SETUP_INSTALL`), never an older interpreter or a skipped floor; candidate parity with developer setup -> not the same: skip became refuse, a floor was added, commit-msg was added, parity is new. BLESSED, unchanged since sitting 001: `hooks/kit-python.sh` and the three hooks match it.
- [MEANING] TC-021 Expected + Method -> the hooks' probe cases, where a missing or aliased python3 reports clearly -> all three hooks driven with stand-ins and a real pre-3.11; pre-commit on a real 3.11+ venv; one shared probe in the hooks and scaffold; candidate parity -> not the same: new acceptance conditions. BLESSED, unchanged since sitting 001.
- [MEANING] SR-020 AcceptanceCriteria -> scan the push range and block a secret, or PII under privacy-check -> the same, PLUS: refuse the push with no floor interpreter, naming the install step, never scanning below the floor or skipping -> not the same: a new acceptance case. BLESSED, unchanged since sitting 001.
- [MEANING] SR-032 AcceptanceCriteria -> the scaffolded onboard/dev-setup scripts run to a green setup -> the same, PLUS: when THIS REPOSITORY's Windows developer setup has no floor interpreter, its attended install offers one consent-first through an available provisioner, searches again after either response, and otherwise exits with the install step; a decline runs no provisioner -> not the same: a new behaviour and acceptance case. BLESSED. Sitting 001's finding was that the clause bound the shipped templates to behaviour only this repository's setup has. That is answered by scoping (D-002): the clause now names its actor. `scripts/dev-setup.ps1` meets it: `Offer-Python` tries uv before winget, runs the provisioner only on `y`, and `Find-Runtime` runs again on either response. Keeping the shipped templates on their adopter-configured install is the conservative choice. One observation, not a return: the Requirement cell still speaks only of "the templates", so this AC clause is anchored to the kit's own instance rather than measuring the Requirement's words. The same is already true of LLR-322's module and TC-342's this-repository cases. If SR-032 is next amended, its Requirement could say that it covers this repository's own developer setup too.
- [MEANING] LLR-322 Detail -> the consent-first, guard-only, idempotent merge into machine-local settings, where a decline and a hookless example change nothing -> the same, PLUS: in this repository the committed settings contain no guard group, the inert example declares every guard group the guard serves at the repository guard path, and developer setup reports the opt-in as on or off and, when off, where it is offered -> not the same: three new obligations. BLESSED. This answers sitting 001's TC-345 return: the obligations TC-345 asserts now have a stated home under SR-032, following the owner's ruling D-004. Minor, not a return: `test_the_guard_hooks_are_this_repos_opt_in_not_its_tracked_settings` checks "every group the guard serves" against a hard-coded event list. Deriving that list from the guard's own served events would keep it true if the guard grows an event.
- [MEANING] TC-345 Expected + Method -> the opt-in's merge, idempotence, decline, hookless example, older-Python denial and git-ignore -> the same, PLUS: inspect this repository's committed settings and inert example, and run this repository's readiness report on both families -> not the same: new acceptance conditions. BLESSED: every new clause now verifies a stated LLR-322 obligation.
- [MEANING] SR-046 AcceptanceCriteria -> the menu, direct, discovery, readiness and delegation conditions -> the same, PLUS: a declared command invoking the runtime "by a bare runtime name its platform provides" runs on the floor-resolved interpreter rather than the first on the search path -> not the same: a new acceptance case. NOT BLESSED: the narrowing (D-003) did not close the condition.
  - The pass/fail line hangs on which names "its platform provides", and on Windows that is not just `python`. The official python.org Python install manager provides `python3` on Windows: this box's WindowsApps holds `python3.exe`, linked into `PythonSoftwareFoundation.PythonManager`.
  - Reproduced this session. With the menu running on python.org 3.11, a `[run]` line `python3 -c "...print(sys.executable)"` printed `...\Python312\python.exe`, the install manager's default, not the floor-resolved 3.11.
  - Under the natural reading the clause therefore requires `python3` to be exact on Windows, which LLR-047 deliberately does not deliver. That is an acceptance condition two readers would score differently.
  - The Requirement's "on Windows and POSIX alike" also makes the platform split something the AC should state outright, not leave to "its platform provides".
- [MEANING] LLR-047 Detail -> the parse, list, direct, launch, menu and launcher-resolution contract -> the same, PLUS: `launch` prepends a directory whose bare `python` is exact on every platform (Windows: the interpreter's own directory; POSIX: per-launch exec shims that keep a venv's configuration); on POSIX bare `python3` is exact too, and a line meant for Windows declares `python` -> not the same: a new mechanism and guarantee. BLESSED. It is now true of the code, which `_interpreter_dir` and its docstring match. D-003's reason for not shimming `python3` on Windows is sound: a `.cmd` shim re-parses `%*` and reopens the WI-227 data-argument contract, and a copied exe loses its home. This is the design SR-046 should be worded to match.
- [MEANING] TC-047 Expected + Method -> "Satisfies SR-046" and the run-menu suite -> the same, PLUS: bare `python` runs on the menu interpreter on every platform with a pre-3.11 first on PATH; on POSIX bare `python` and `python3` stay exact beside another python, and each shim keeps its venv -> not the same: new acceptance conditions. BLESSED: it covers each claim LLR-047 now makes, on the platforms where it makes them.

Verification run this session: the arms-map tests for LLR-021, LLR-047, LLR-322 and LLR-326, plus the run-menu suite cases, gave 32 passed and 2 skipped. The skips are platform skips on this Windows box: `test_a_denial_changes_no_configuration_or_credential`, which needs a pseudo-terminal, and the POSIX-only `..._exact_where_its_directory_holds_another`.

VERDICT: MEANING rows=10

Aftermath, as this section rules it:
- Blessed: SR-019, SR-020, SR-032, LLR-021, LLR-047, LLR-322, TC-021, TC-047, TC-345.
- Not blessed: SR-046.
- The LLR and TC rows are re-attested in their own act. The SR rows (SR-019, SR-020, SR-032) cannot be: SR-046's drift sits in the same registry, and the copy refuses while it does. They wait for SR-046's next sitting and should be put in it.

### Dispositions

WI-880 is an ordinary work lane, and intake mints drafts only from adjudication-kind specs, so this draft is the lane's to answer before merge. It is written in the shape intake reads, for the coordinator to route:

```toml
title = "WI-880 return: SR-046's bare-runtime-name clause does not close on Windows"
safety_class = "ordinary"
```

State the platform split that LLR-047 and D-003 already decide in SR-046's acceptance clause. For example: a declared command invoking the runtime by its bare `python` name runs on the floor-resolved interpreter on every supported platform, and by `python3` on POSIX. Do not use "a bare runtime name its platform provides", because Windows' official Python install manager provides `python3` (reproduced above). Then re-submit SR-046 with SR-019, SR-020 and SR-032, which are blessed here and wait on its registry.

## first-approval

- [APPROVE] LLR-326 -> at an attended `-Install` of this repository's Windows developer setup with no 3.11+ interpreter, `Find-Runtime` searches, `Offer-Python` asks consent for one available provisioner (uv before winget), which runs only after consent; the search runs again after either response; a decline runs no provisioner; still missing exits 1 with the install step -> SR-032's amended clause, blessed in this sitting's amendment section, now calls for exactly this, scoped to this repository's setup per D-002. `scripts/dev-setup.ps1` (`Offer-Python`, then `Find-Runtime` on both paths, then exit 1 with the step) matches it clause for clause -> ready: both of sitting 001's findings are answered. The parent now asks for this row, and the "searches again" disagreement with TC-350 is gone. "Asks for consent ... runs only after consent" is now the right wording.
- [APPROVE] TC-350 -> at a Windows console with only a pre-3.11 runtime, decline and accept the install offer: a decline runs no provisioner, acceptance runs the declared one, both search again and exit 1 with the install step -> it verifies every arm of LLR-326, and its "both paths search again" now agrees with the LLR; `test_at_a_windows_console_install_offers_the_missing_runtime` passed this session -> ready.

OUTCOME: APPROVE rows=2

The act flips LLR-326 and TC-350 to `Approved` with the scoped snapshot, in its own commit after the amendment section's re-attestation, which moves the same two registries.

SITTING: JUDGED kinds=amendment;first-approval
