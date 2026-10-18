Reviewed: 9bbcfb351e257fac219ddd7776712578a3654612

WI-927 full-lane review (2268a9a8c..9bbcfb351), independent reviewer (Claude Opus), rubric docs/rubrics/kit-change-review.md.

Worst failure classes for this change, hunted first: (1) fail-open, where the lease take records a holder while the guard hooks are not `on`, or anyone other than a person at a terminal consents; (2) data loss, where the install overwrites a user's keys, events or hooks; (3) silent wrong content, where dev-setup reads a failed reader as `none`, or a malformed settings file reads `absent` and gets written over.

Verified. I drove the real paths. The CLI `take` against a scratch root with the kit example: from a stdin that is not a terminal (the Bash tool) it exits 1 with the NO_TERMINAL text, records no holder and writes nothing; through `< /dev/null`, `subprocess.DEVNULL` and the PowerShell tool (stdin on NUL) it exits 1, again records nothing and writes nothing (see finding 1 for the message it gives). A pipe or a regular file always reads as no terminal, so an agent cannot consent for itself. No fail-open path was found. `take` returns early only at `none`/`on`, or after a consented install that reads `on` again (coordinator_guard.py:1504-1518; guard_hooks.py:273-298). `install_hooks` writes only from `absent`, keeps every other key and event, and goes through `write_atomic`. Fix round 1's JSON-null regression is confirmed red-before. Fed the pre-fix kitlib (7d04a1bde), `read_state` reads `null` and `{"hooks":{"PreToolUse":null}}` as `absent`, an install-over. At the tip both read `occupied`. The pre-fix `input()` prompt goes to stderr at a tty, so the sh offer's `2>&1 1>&3` capture hid it; I confirmed this by reading the code, and the tip's pseudo-terminal tests pass. The dev-setup reader-failure fix is red-before by reading: the base mapped it with `|| HOOKS="none"` and `if (-not $hooks) { $hooks = "none" }`. This repository's main checkout reads `on` with the new reader (read-only), so landing does not strand the live coordinator's take. Every Done-when item maps to a test that ran green somewhere, including the POSIX pseudo-terminal cases, which I ran under WSL Ubuntu:
- absent-yes: test_at_a_terminal_a_yes_installs_every_guard_group_keeping_other_keys (WSL) and the Windows-console variant (ran);
- absent-no: test_a_denial_changes_no_configuration_or_credential (WSL) and test_a_declined_or_empty_or_eof_answer_writes_nothing_and_asks_again;
- on: test_an_on_file_is_left_byte_for_byte_and_nothing_is_asked and test_an_on_file_is_unchanged_and_not_offered_at_a_terminal;
- occupied, both routes, four shapes: test_each_occupied_shape_refuses_and_writes_nothing and test_an_occupied_slot_is_reported_and_never_offered (sh copies run under Git sh on Windows);
- take: the test_coordinator_guard.py take cases, plus test_the_cli_take_at_a_pseudo_terminal_asks_and_installs (WSL) and the Windows-console case;
- failed write: test_a_consented_install_whose_write_fails_refuses_the_take;
- reader failure: test_a_failing_or_silent_hooks_reader_is_reported_missing_never_none (all four copies);
- no-guard example: test_the_hook_opt_in_with_no_guard_hooks_changes_nothing (its take half reads `none` from an absent example, not a guard-less one; read_state's "no guard group" case covers the latter);
- `--enable` refused: test_the_hooks_command_refuses_enable;
- no merge code: test_guard_hooks_holds_no_merge_or_ownership_code.

The one exception is the module-size item (finding 3).

Interface and requirement pairs:
- IF-280: the data cell `[--enable]` becomes `[--offer]`. Its counterpart IF-281 is retained, because occupied and no-terminal are refusals (exit 1) inside its existing categories.
- LLR-322 and TC-345 are amended together. LLR-300's detail gains its sentence, its approved text otherwise verbatim. TC-315 to TC-317 are retained, since the blackout and lease cases are unchanged. SR-032 is unchanged and still covered.
- SR-229 is retained pending the checkpoint sitting: its "may take" reads as a permission, not an exhaustive list (finding 5).
- No Status flips.
- The spine checkpoint sitting that judges these amended Approved rows is still owed before landing (decisions record: "unjudged until the checkpoint sitting").

Commands:
- `git rev-parse HEAD`: 9bbcfb351e257fac219ddd7776712578a3654612
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../wi927-r2-opus/wi-927 tests/test_blackout_window.py tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_run_devsetup.py tests/test_session_keep.py`: 419 passed, 39 skipped in 71.83s (27 posix-shell-gated skips)
- `python project-trajectory/scripts/check_trajectory.py --strict`: check_trajectory: clean (941 work item(s), 823 done (87%), 30 cancelled, graph acyclic). exit=0
- `python project-trajectory/scripts/trace.py --strict-integrity`: Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0. exit=0
- the same pytest set filtered `-k "hook or take or offer or windows_console or occupied or reader"`, with Git\bin on PATH (sh-gated cases): 64 passed, 7 skipped in 38.65s (only the pseudo-terminal cases skipped)
- WSL Ubuntu `python3 -m pytest tests/test_run_devsetup.py -k 'terminal or pseudo or occupied or on_file or reader or hooks'`: 23 passed, 5 skipped (PowerShell-only), 49 deselected
- WSL Ubuntu `python3 -m pytest tests/test_run_devsetup.py tests/test_coordinator_guard_e2e.py -k 'denial or older_python or no_terminal'`: 2 passed, 1 skipped (no sub-3.11 Python)
- red-before probe: read_state from 7d04a1bde kitlib on `null` and on a null PreToolUse: both `absent`; at the tip both `occupied`
- real CLI `take` on a scratch root: no-terminal stdin gives NO_TERMINAL, exit 1; stdin on NUL or DEVNULL (Windows) gives the question on stdout plus DECLINED, exit 1; no holder and no settings file either way
- real CLI `hooks` (read-only) on this repo's main checkout: `on`, exit 0
- `git status --porcelain` in the lane worktree after all runs: empty

Coverage-extension notes, no severity:
- A 0-byte settings.local.json reads `occupied` (it does not parse), not `absent`. The command form `coordinator_guard.py hook` without an interpreter word, and tab-separated words, also read `occupied`. A BOM-prefixed settings file reads `occupied`.
- All of these fail closed with the file named.

Findings:
- [MINOR] project-trajectory/scripts/coordinator_guard.py:1521 -> `_terminal_ask` treats any character device as a terminal, so on Windows a stdin on NUL counts as one. That covers Claude Code's PowerShell tool and `subprocess.DEVNULL`. There the take prints the consent question into the agent's stdout, reads EOF and refuses with DECLINED ("take again and answer yes"), an instruction the agent cannot follow. It should take deliverable 3's no-terminal branch (NO_TERMINAL, naming dev-setup's consent step). The refusal stays fail-closed. tests/test_coordinator_guard_e2e.py:122 says "never a terminal" for DEVNULL, which is false on Windows. Its assertion at :138 ("dev-setup", "answer yes") matches both texts, so on Windows CI the test passes through the wrong branch -> make the terminal predicate require a real console on Windows (for example GetConsoleMode on the stdin handle, matching dev-setup.ps1's `[Console]::IsInputRedirected`), and assert the NO_TERMINAL wording ("no terminal can consent") in the e2e test. This corrects the predicate at the trust boundary the spec's Trust section names (the terminal answer); it adds no compensating guard -> @owner
- [MINOR] project-trajectory/scripts/kitlib/guard_hooks.py:294 -> the failed-install texts ("could not be written: <error>" at :294 and "the install did not read on: <problems>" at :298) name the file and the error but not the fix. The spec's Trust section asks for "a `[missing]` line naming the file, the error and the fix (move or repair the file, then run again)". dev-setup's offer echoes these texts verbatim (dev-setup.template.sh:318; dev-setup.template.ps1:286 says only "printed above") -> append the move-or-repair-then-run-again fix to both texts, as `refusal_text` does with FIX at occupied -> @owner
- [MINOR] project-trajectory/scripts/kitlib/guard_hooks.py:1 -> the Done-when "`kitlib/guard_hooks.py` holds no merge or ownership code. The module-size ratchet's entry for it shrinks" (and deliverable 1, "shrunk") is half unmet as written. tests/test_module_size_ratchet.py has no entry for guard_hooks.py, and its SLOC grew from 50 to 172 (measured with check_complexity.module_sloc at 2268a9a8c and 9bbcfb351) once `hooks_state`, `install_hooks` and `consent_install` moved in at coordinator_guard.py's 1000-SLOC limit. The no-merge half holds -> amend the spec's Done-when through its authority to record the move, or have the checkpoint sitting rule the item met, rather than leave a Done-when line no test or entry can satisfy -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3441 -> (K3) LLR-322's code_symbol lists `take`, but `take`'s `Implements:` tag names only LLR-300 (project-trajectory/scripts/coordinator_guard.py:473). The take's hooks reading, `_hooks_admission` (coordinator_guard.py:1504), which the spec says the cell gains, carries no tag. `hooks_state`, `install_hooks` and `consent_install` also sit in the cell's coordinator_guard segment, though they now live in guard_hooks.py. Separately, LLR-300's test_refs (low-level-requirements.toml:3179) still reads TC-315;TC-316;TC-317, while TC-345 now verifies LLR-300 -> list `_hooks_admission` in LLR-322's code_symbol with an `Implements: SR-032, LLR-322` tag (or give `take` that tag), move the three moved symbols into the guard_hooks segment, and add TC-345 to LLR-300's test_refs -> @owner
- [MINOR] docs/requirements/system-requirements.toml:1755 -> for clarity (K1): SR-229's acceptance ends "a subsequent session may take the freed lease". LLR-300's amended detail now says the take "records no holder unless it reads none or on, or a terminal consent installs them". Read together, the SR states an unconditional take that the LLR conditions on the hooks -> have the checkpoint sitting rule whether SR-229's acceptance gains the hooks precondition (the spec's own SR-229 item), and record the ruling with the sitting -> @owner

VERDICT: CHANGES-REQUESTED findings=5
