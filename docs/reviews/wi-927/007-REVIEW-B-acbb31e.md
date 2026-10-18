Reviewed: acbb31e9a201835359e0c6d352d2bb2de2feacc9

**Verified.** The checkout is the reviewed commit. I read the whole full-lane diff (scope as briefed) against the WI-927 spec and its `specref`, and against the LLR-300, LLR-322, TC-345, IF-280/IF-281 and SR-032/SR-229/SR-237 rows. I hunted fail-open first: any route that goes on at `occupied`, or at `absent` without a consented install that re-reads `on`. Then data loss, meaning an install that drops another key or event or writes outside `absent`. Then silently wrong content, meaning a reader failure turned into `none`.

`kitlib/guard_hooks.read_state` answers none/absent/on/occupied and denies by default. A parsed JSON `null` document, a null event, a `hooks` that is not an object, a group with no `hooks` list, a command that is not a string, a `type: prompt` hook, a BOM-prefixed file, an unreadable file and an unreadable example all read `occupied` (some by probe, some by the parametrized READINGS table). `install_hooks` writes only from `absent`. It keeps every other key and event and returns the re-read. `consent_install` goes on only at none/on or after a yes whose re-read is `on`. An OSError, or a partial write, comes back as a refusal naming the file, the error and the fix. `take` calls `_hooks_admission` after the session-id check and before the lease lock, and records nothing on any refusal.

Windows `_is_terminal` correctly rejects the NUL device; I confirmed `open(os.devnull).isatty()` is True on this host. Both dev-setup templates and this repo's two copies treat the reader's word as trusted only at exit 0 with one of on/absent/none, and report any other result on a `[missing]` line. In the templates that line is counted. The offers keep stdin and stdout on the terminal and capture only stderr.

`hooks --enable`, `enable_hooks`, `merged`, `command_shapes`, `_owns` and `_without_guard` are gone. `kitlib/guard_hooks.py` has no ratchet entry. The RESYNC entry covers all five items of deliverable 7.

Spine and rubric checks:
- K3: every `Implements:` tag names an LLR whose module holds the file and whose `code_symbol` lists the function. No Status flips. The amended rows are exactly those the spec grants.
- K2: no SN or SR cell is touched.
- Interface pair: IF-280 changed `[--enable]` to `[--offer]`, and its counterpart callers (both dev-setup families) carry the same change. IF-281 is retained and justified: "1 refusal" already covers `hooks` exiting 1 at `occupied`. WI-897's queued counterpart text is the coordinator's to amend on trunk (spec deliverable 6).

**Red before the fix (convergence).** I ran the tip's new tests against a `git archive` of base 2268a9a8. 18 failed, 1 passed (the null-document CLI case, which the old code also refused with exit 1), 4 skipped (sh-gated). The failing tests are:
- the occupied take
- the no-terminal take (in-process and CLI)
- the mixed PreToolUse group (the inverted `test_the_hook_opt_in_merges_and_keeps_existing_hooks`)
- each occupied shape
- the `--enable` refusal
- the reader-failure `[missing]` case, in both ps1 copies

The in-lane null fix (patch 9bbcfb351) is pinned by `test_a_json_null_in_the_settings_refuses_the_take_and_is_never_asked`: the pre-fix code read `null` as absent and asked, and the test's `_never_asked` raises. The failed-install fix text (patch 4b20a7bc3) is pinned by the Windows-console failed-install test, which passes.

**Done-when coverage:**
- **Absent, yes:** `test_at_a_terminal_a_yes_installs_every_guard_group_keeping_other_keys` (pty; skipped on this Windows host). `test_at_a_windows_console_a_yes_installs_...[root/template × 3]` passed. `test_an_absent_install_binds_every_group_and_keeps_other_keys` passed.
- **Absent, no / empty / EOF, asks again:** `test_a_declined_or_empty_or_eof_answer_writes_nothing_and_asks_again` passed. `test_a_denial_changes_no_configuration_or_credential` is pty-only (skipped here).
- **On, byte for byte:** `test_an_on_file_is_left_byte_for_byte_and_nothing_is_asked` passed. `test_an_on_file_is_unchanged_and_not_offered_at_a_terminal` is pty (skipped here).
- **Occupied (mixed, second group, missing event, unparseable) at both routes:** `test_an_occupied_slot_is_reported_and_never_offered[4]` passed. `test_each_occupied_shape_refuses_and_writes_nothing` (consent_install and CLI) passed. `test_a_user_command_beside_the_guards_reads_occupied_and_nothing_is_written` passed. `test_an_occupied_slot_refuses_the_take` passed.
- **Take, no terminal and absent:** the in-process and CLI e2e tests passed.
- **Take at on/none:** `test_the_take_goes_on_at_on_and_at_none` passed.
- **Take at occupied:** passed.
- **Take at a terminal, yes/no:** in-process passed. `test_the_cli_take_at_a_windows_console_asks_and_installs[y,n]` passed. The pty variant was skipped here.
- **Failed install refuses the take:** `test_a_consented_install_whose_write_fails_refuses_the_take[2]` passed.
- **Reader failure reported missing in both templates:** `test_a_failing_or_silent_hooks_reader_is_reported_missing_never_none[8]` passed with Git `sh` on PATH.
- **No-guard example:** passed.
- **`--enable` refused:** passed. `test_the_hooks_command_reports_each_state_and_writes_nothing` passed.
- **Kept tests:** the older-Python test, the gitignore test, the tracked-settings test and the readiness-report test all passed.
- **No merge/ownership code:** `test_guard_hooks_holds_no_merge_or_ownership_code` passed. The ratchet holds no entry for the module.
- **Spine rows, RESYNC entry:** present (see the findings).

The pty-driven variants were not observed running on this host. Their Windows-console counterparts were.

**Coverage-extension notes (no severity).** These inputs fail closed:
- A BOM-prefixed `settings.local.json` reads `occupied` ("Unexpected UTF-8 BOM").
- A `type: prompt` hook on a guard event reads `occupied`.

One input outside the Trust set (a kit-written example that parses but whose `hooks` is not an object) reads `none`. It is not a failed-write shape bootstrap produces, so I dismiss it under PROCESS.md §6.

**Commands:**
- `git rev-parse HEAD` -> acbb31e9a201835359e0c6d352d2bb2de2feacc9
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../wi927-gate-opus/wi-927 tests/test_blackout_window.py tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_run_devsetup.py` -> `256 passed, 40 skipped in 65.58s` (27 skipped for the posix-shell gate)
- The same four files with `C:\Program Files\Git\bin` on PATH (`--basetemp .../wi-927-sh`) -> `283 passed, 13 skipped in 89.77s` (only the pty-gated tests skipped)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (941 work item(s), 823 done (87%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ...`
- `python -m pytest ... tests/test_session_keep.py tests/test_module_size_ratchet.py` (`--basetemp .../wi-927-extra`) -> `171 passed in 15.61s`
- Red-before: the tip's four test files over `git archive 2268a9a8` (`--basetemp .../base-run`), selected new tests -> `18 failed, 1 passed, 4 skipped in 9.81s`
- Probe (`wi927-gate-opus/probe/probe.py`, the real `take`/`hooks_state` over a git repo with a lane worktree) -> take from the primary with hooks `on`: None. Take from the lane worktree (primary `on`, lane file absent, no terminal): the NO_TERMINAL refusal, naming `lane\.claude\settings.local.json`. BOM file: occupied. Prompt-type hook: occupied.

- [MINOR] project-trajectory/scripts/coordinator_guard.py:1512 -> `_hooks_admission` reads `.claude/settings.json.example` and `settings.local.json` under the `root` the take was given, while `take` records the lease under the primary checkout (`lease_dir` -> `session_keep.primary_out_dir`; LLR-300 "A primary-checkout lease"). A take run from a lane worktree is the supported path `tests/test_coordinator_guard_e2e.py::test_a_lane_worktree_shares_the_primary_checkouts_lease` pins (its fixture has no example, so it reads `none`). In a real repository it refuses with the "not installed" text, naming the lane's git-ignored file, even when the primary checkout's hooks read `on`. At a terminal it would offer to install into the lane's file instead. This fails closed, and it is reachable only when the take's root is not the session's project directory (confirmed by probe) -> decide which checkout's settings govern the take and read the hooks there. Either resolve the hooks root through the same primary-checkout boundary the lease uses, or state in LLR-300 and the residue that the take reads the hooks of the checkout it runs in. Add a lane-worktree case with the example present to the take tests (anchor K1) -> @builder
- [MINOR] docs/test/test-cases.toml:3511 -> TC-345's `verifies` adds SR-237 (the blackout pause), but nothing in TC-345's method, expected or evidence exercises a blackout window. LLR-300's other TCs (TC-315: SR-229 and LLR-300 only) show that the trace rules do not require it. So the row credits SR-237 with verification it does not perform -> drop SR-237 from TC-345's `verifies`, keeping SR-032, LLR-322, SR-229 and LLR-300 (anchors K1, K3) -> @builder
- [MINOR] docs/requirements/low-level-requirements.toml:3442 -> for clarity. LLR-322's detail, and TC-345's expected at docs/test/test-cases.toml:3515, read "A missing machine-local file, or all missing guard events, is absent". The code and the spec's deliverable 1 ("no guard event in the settings holds any hook") also read guard events present as `[]` as absent (READINGS "events as []"). "Missing" understates the rule -> reword to "a missing machine-local file, or one in which no guard event holds a hook, is absent" in both cells (anchor K1) -> @builder
- [MINOR] docs/requirements/low-level-requirements.toml:3177 -> for clarity. The take's hooks refusal is now stated twice. LLR-300's added sentence ("records no holder unless it reads none or on ... without a terminal at absent, or at occupied, it refuses naming the consent step or the hooks to move") overlaps LLR-322's sentences on the same take ("Without a terminal, the lease take refuses and names the consent step ... the lease take refuses without recording a holder"). The two rows agree today but can drift -> let LLR-300 own the take's admission rule and LLR-322 own the reading and the install, cross-referring rather than restating, at the next amendment of either (anchor K1) -> @coordinator
- [MINOR] docs/status.md:58 -> outside the diff, but it goes stale through it. The working surface tells the coordinator the hooks are "opted in through dev-setup or `coordinator_guard.py hooks --enable`". This lane deletes that command (the parser now refuses it), so after landing the instruction names a dead command -> at landing, reword to "installed through dev-setup's consented offer, or a take at a terminal" (anchor K1) -> @coordinator

VERDICT: APPROVE findings=5
