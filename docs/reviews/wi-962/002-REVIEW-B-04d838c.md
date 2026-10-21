Reviewed: 04d838ca879ee00c2c872625b2b00c65143c7ddf

**Verified.** The checkout is the reviewed commit (`git rev-parse HEAD` = 04d838ca8…). First I named the failure classes this change could let in. The worst is fail-open: the hook reads privacy OFF, or reads the reviewer posture as `warn-unwired`, where the one parse says otherwise (the 2026-08-08 decoy class). Next is silent wrong content: a near-token or a stray CR is accepted. Last is a refusal that no longer fires: the scripts dir, a mixed config, an unreadable file. I hunted them in that order.

- **The token gate.** `kit_policy` (`project-trajectory/hooks/kit-python.sh`) acts only on the five exact tokens. Every other path, nonzero exit included, returns 1 explicitly. `check_privacy.py --hook-policy` writes no newline, so on Windows there is no CR. Tests drive both through all three real hooks: stubs that exit 3, print a foreign token, print nothing, or print `privacy=off\r`.
- **Inputs outside the table.** I drove `--hook-policy` directly over shapes the table lacks. Duplicate key → `refuse=unreadable` with the parser's message. UTF-16 bytes → `refuse=unreadable`. `[[policies]]` array-of-tables → on/require. Empty file → off. A legacy file holding only a comment, beside a declared key → `refuse=mixed`. A `privacy_review` decoy in another section, beside a legacy `warn-unwired` → require. Off with a wrong-typed `privacy_review` → off. Every one fails closed or answers as the Trust section rules.
- **Red-before.** I extracted the base tree (e79075c46) with the tip's tests into scratch and ran every new test against the pre-change hooks and checker. 73 failed, among them every case in the unreadable, mixed, foreign-answer, after-probe, scripts-dir, posture-decoy, structural and scaffold tests, and both fail-open D4 rows (`multiline-string-false`, `wrong-section-false`). The other D4 rows pass on base as characterization. `test_the_scan_finds_the_hooks_and_launchers` also failed, but only because the scratch tree is not a git checkout.
- **Done-when map:**
  - No text read: `test_shell_portability.py::test_no_hook_reads_the_policy_as_text`.
  - One read, after the probe: `test_each_hook_runs_the_one_read_once_after_the_probe` and `test_process_config.py::test_the_mixed_refusal_runs_after_the_interpreter_probe`.
  - Adversarial table through the real pre-push (decoy, dotted, inline, multi-line, wrong section, BOM, wrong type): `test_the_shipped_hook_and_the_checker_agree_on_every_shape`.
  - Mixed, unreadable and foreign answers at all three hooks: `test_every_hook_refuses_a_mixed_config_with_one_text`, `test_every_hook_refuses_an_unreadable_policy_file`, `test_every_hook_refuses_a_failed_or_foreign_policy_answer`.
  - Review posture, privacy on and off, legacy included: `test_pre_push_hook.py::test_the_review_posture_follows_the_one_parse`.
  - Missing `KIT_SCRIPTS_DIR` at all three hooks: `test_pre_commit_hook.py::test_every_hook_refuses_a_kit_scripts_dir_naming_a_missing_directory` (pre-commit, commit-msg) and `test_pre_push_refuses_a_kit_scripts_dir_naming_a_missing_directory`.
  - Shell parse: `test_every_shell_file_parses_under_sh`.
  - Scaffold: `test_bootstrap.py::test_a_fresh_scaffold_ships_the_probe_and_commits_through_its_hooks`.
  - SR-031, TC-031 and LLR-021 amended as drafted. The RESYNC entry is present, with both forced changes. Strict lints are clean.
  - Nothing is UNCOVERED.
- **K3 back-links.** `kit_policy` → LLR-021, whose module is `kit-python.sh`. The checker functions → LLR-031 or LLR-018, whose module is `check_privacy.py`, with each symbol in `code_symbol`. No Status flips.
- **IF-037.** Dropping the hooks from IF-037's consumers is correct: no hook opens `docs/process.toml` any more.
- **No repeat.** `_load_process_toml` moves `_process_gate`'s own load into one place rather than adding a copy. `read_privacy_review` has no prior Python twin.

I also drove the real `pre-push` by hand, base hook against lane hook, with a legacy `docs/privacy-check` = `TRUE`. Base: exit 0, the review skipped, while the checker armed "privacy + secrets floor". Lane: exit 1, FAILING CLOSED. Finding 3 below.

`trace.py` rewrote the gitignored `docs/test/report.md`; no tracked file changed.

Commands:
- `git rev-parse HEAD` → 04d838ca879ee00c2c872625b2b00c65143c7ddf
- pytest, the brief's eight modules as given → `223 passed, 181 skipped in 211.24s`. 168 of the skips were environment-gated (posix-shell: Git\bin not on PATH), so the hook cases did not run.
- The same with `C:\Program Files\Git\bin` prepended to PATH (the gate's stated remedy), `--basetemp .../opus/wi-962b` → `391 passed, 13 skipped in 348.24s`
- `check_trajectory.py --strict` → `check_trajectory: clean (959 work item(s), 844 done (88%), 30 cancelled, graph acyclic).` exit 0
- `trace.py --strict-integrity` → `Traceability: SN=31 SR=132 LLR=307 TC=326 orphans=0 integrity=0 ... drafts=1 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.` exit 0
- `trace.py --strict` → the same line, exit 0
- Red-before: base tree e79075c46 with the tip's `tests/`, the new tests only → `73 failed, 59 passed, 2 skipped`
- `check_privacy.py --root <probe> --hook-policy` over 10 constructed repos (results above)
- Real `pre-push`, base against lane, over legacy `TRUE` and `privacy_review = 'warn-unwired'` (results in finding 3)

- [MINOR] project-trajectory/process.toml.template:6 -> **Stale "pure-sh grep" claims.** Several shipped texts still say the git hooks read `docs/process.toml` with a keyed pure-sh grep "so a Python-less box still fails closed":
  - the template header (lines 6-19, and the KEYED-GREPPABLE notes at 188-189 and 197; the same text in docs/process.toml);
  - project-trajectory/README.md:127;
  - the user-facing refusal in `process_shape_findings` (project-trajectory/scripts/agent_policy.py:317-318, "The git hooks read this file line-by-line in pure sh").

  After this lane that is false. The lane-edited project-trajectory/PROCESS_OPTIONS.md:55-57 now sends readers to "the file's own header" for the reason, while the header gives the opposite one. The RESYNC entry also lists `README.md` as a changed kit-owned file (project-trajectory/RESYNC_PACK.md:9329). Read kit-relative, as its siblings are, that is project-trajectory/README.md, which this range did not change; the lane changed the root README, which adopters never receive. -> Rewrite the template and docs/process.toml header lines, the kit README cell and the refusal message to the one-parse reason. Or, since the shape-rule retirement is its own row (S1), name each of these sites in that row's spec, so a deletion-only row does not leave them untouched. Correct the RESYNC file list (K1). -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:341 -> **LLR-031's detail no longer covers its symbols.** Its `code_symbol` (line 340) now names `_load_process_toml`, `_policies`, `read_privacy_review` and `hook_policy_answer`. Its detail still states only "the single first-non-comment-line reader". So the review-posture rule now lives in no LLR detail: exactly `"warn-unwired"` under `[policies]` opts down; a copy elsewhere, or an unreadable file, means require; the legacy file answers when the key is absent. The closed answer set and the unreadable/mixed precedence are stated only in IF-298's `data` cell and, from the consumer side, LLR-021. The lane also changed approved rows beyond the spec's named grant (SR-031, TC-031, LLR-021): LLR-018's and LLR-031's `code_symbol`, TC-021's verifies, method, expected and evidence. Those changes are recorded only in docs/decisions/wi-962.toml D-001 and D-003, and D-003 defers the LLR-031 detail to a later reconcile that has not reached this tip. -> Amend LLR-031's detail to state the one parse, the posture rule and the answer set, or give `hook_policy_answer`/`read_privacy_review` their own LLR under SR-031. Carry the out-of-grant cell changes to the lane's sitting explicitly, before landing (K1, K3). -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:9323 -> **Two adopter-observable changes are missing from "Also observable".** I drove both on the real `pre-push`, base hook against lane hook.

  1. A legacy `docs/privacy-check` reading `TRUE` (any non-lowercase spelling). The base hook read it OFF: exact-match `[ "$p" = "true" ]`, so the push exited 0 with no review, even though `check_privacy` armed the privacy layer — a latent fail-open. The lane hook reads it ON and refuses the push when no reviewer is wired. That is a forced change, and the fix has no pinning row: the D4 table's `legacy-only-true` is lowercase only.
  2. `privacy_review = 'warn-unwired'`, a TOML literal string. Base: require, refused. Lane: warns and proceeds.

  Separately, when the gate is on only through the legacy file, the refusal at project-trajectory/hooks/pre-push:158 says "the privacy gate ([policies] privacy_check) is on", which names the wrong home. -> Add (1) to Forced changes and (2) to Also observable. Add a `legacy-only-TRUE` row to `_d4_rows` in tests/test_process_config.py, so the fixed hook-vs-checker divergence stays pinned. Word the refusal so it does not name `[policies]` when the legacy file armed the gate (K1). -> @owner
- [MINOR] docs/requirements/stakeholder-needs.toml:265 -> **Requirement sweep: two approved texts state a reason that is now false.** SN-028's acceptance says the shape is checked "because two grammars read the file (a TOML parser and the hooks' plain-sh parse)". SR-137's rationale (docs/requirements/system-requirements.toml:489) says the same: "the three git hooks in pure sh". After this lane, amended SR-031 says the hooks read through one parse. The approved need and its sibling SR now state a premise the delivered code no longer has. This is not a wording ambiguity: the stated reason is untrue. -> Route SN-028's acceptance and SR-137's rationale through their authority in the S1 shape-retirement row, and name both in that row's spec now, so the contradiction has a recorded owner (K1). -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:230 -> **Wording, for clarity.** LLR-021's new clause, "with none named, the default directory in either case", does not say what "either case" means: the `scripts/` and `Scripts/` spellings. -> Write "with none named, the default scripts directory, in either letter case" (K1, for clarity). -> @owner

VERDICT: APPROVE findings=5
