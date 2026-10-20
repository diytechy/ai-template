Reviewed: 6e6efb9496c852038bd0d17da4d335c993c796a3

Verified (convergence stance; full-lane range 9f934456f..6e6efb949, read through the three-dot diff with the brief's exclusions; no earlier verdict, decision record, critique or lane log content read). Worst failure classes hunted first: (a) fail-open, where the narrowed PreToolUse matcher lets a call the blackout denial should refuse skip the hook; (b) silent behaviour change from the deferred imports or the `main` fast path, meaning a wrong root, a lost usage error, or a deferred import that fails inside a window; (c) a session_keep regression from swapping `agent_common.git` for `kitlib.git.git_out`. None reproduced:
- (a) The matcher `Agent|SendMessage|Bash|PowerShell` equals the `LAUNCH_TOOLS`/`SHELL_TOOLS` keys (coordinator_guard.py:930-932). `launch_reason` (coordinator_guard.py:981-986) returns None for every other tool name, so no deny moves. `on_monitored` holds no permission decision, and the claim's own `claim_refusal` reading is untouched.
- Real-path drive: I ran the HEAD script as a subprocess hook in a scratch repository with the blackout window `00:00-23:59` open. It denied PreToolUse `Bash` `claude -p hi`, PowerShell `$x = codex exec y` and `Agent`. For PreToolUse `Bash git status` it only told the close-down. A PostToolUse `Read` from a fresh session got the close-down and no permissionDecision. Every call exited 0. So the deferred `agent_common`/`agent_route` imports in `model_clis` resolve on the shipped script-run path.
- (b) `main`'s fast path takes only `["hook"]` and `["--root", R, "hook"]` with R not starting with `-`. It resolves the root the same way the parser path does (`_root`). Every other spelling still goes through argparse, so usage errors keep exit 2 (IF-281).
- (c) `git_out` returns None on any failure. The old code returned None on a non-zero exit, so the two agree, and the only new edge is no git binary falling back to `out/`, which is benign. The `.strip()` handling matches.
- Red-before for Done-when (1): I ran a probe equivalent to the new e2e test against `git archive` extracts of both commits (guard off, and guard on with no lease, for both argv forms). BASE gives `"heavy": ["agent_common", "agent_route", "argparse"]` in all four cases; HEAD gives `"heavy": []` in all four. The pin fails on the pre-fix code.
- Red-before for Done-when (2): BASE's guard PreToolUse group carries no matcher, so `test_the_pre_tool_use_matcher_names_exactly_the_launch_and_shell_tools` and `test_every_denied_launch_reaches_the_pre_tool_use_matcher` fail their `assert matcher` there (checked by inspection of the base file).
- Re-measure: 12 runs each, interleaved, in a quiet window on this box. A no-op PostToolUse hook call took a median of 215 / 213 ms on BASE and 161 / 160 ms on HEAD, about 53 ms saved per call.

Done-when map:
- (1) No-op path imports neither module: covered by tests/test_coordinator_guard_e2e.py::test_the_no_op_hook_imports_no_route_or_cli_module, which is red at base. The existing test bodies are unchanged; the diff only adds tests.
- (2) Matcher in the example: covered by test_the_pre_tool_use_matcher_names_exactly_the_launch_and_shell_tools, for both the kit file and this repo's example; dogfood_sync passes.
- Consented install carries the matcher, and the post-call groups stay unmatched: covered by test_the_consented_install_writes_the_pre_tool_use_matcher.
- Equality pin: covered (the same matcher test).
- Denial for each WI-834 tool: covered by test_the_hooks_deny_each_launch_form_with_the_guard_off and test_every_denied_launch_reaches_the_pre_tool_use_matcher.
- WI-822 fixture: covered by test_the_crossing_replys_claim_refuses_with_no_hook_run.
- The moved measurement for `Read` at PostToolUse and PostToolUseFailure: covered by test_a_tool_outside_the_matcher_latches_at_its_post_tool_event.
- Blackout cadence with no deny: covered by test_a_tool_outside_the_matcher_hears_the_close_down_after_the_call.
- Re-measure in the lane log: the file docs/log.d/WI-897-guard-hook-per-call-cost.md exists. Its content is outside my reading scope; my own measurement is above.
- Checkpoint on LLR-300, IF-274, IF-275 and IF-281: I read each row myself. No sentence is made untrue by the matcher, because LLR-300's cadence counts "monitored events" the hook receives, its deny list is the same four tools, and IF-274/275/281's vocabularies, shapes and exit codes are unchanged.
- RESYNC entry anchored at trunk `9f934456f`: present, with the remove-and-consent route and the `hooks --enable` note.

K3:
- `_root` is tagged LLR-301 and was added to LLR-301's code_symbol. `model_clis` stays in LLR-300.
- The amended cells on Approved rows (LLR-301 code_symbol; TC evidence cells) are traced cells only, and no Status flips.
- The archived snapshot equals the live LLR and TC registries at both ends of the range.

Interface relationships:
- IF-065 (agent_common's requestors) drops `scripts/session_keep`. The counterpart is session_keep.py, which no longer imports agent_common, so the drop is correct.
- But session_keep and coordinator_guard now call `agent_policy.process_config` directly, and the counterpart seam IF-261 still names only agent_common. IF-291 (blackout_at) already lists both. See the second finding.

Commands:
- `git rev-parse HEAD` -> 6e6efb9496c852038bd0d17da4d335c993c796a3
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-19e/gate/opus/wi-897 tests/test_coordinator_guard.py tests/test_blackout_window.py tests/test_coordinator_guard_e2e.py tests/test_import_layers.py tests/test_dogfood_sync.py tests/test_run_devsetup.py` -> 317 passed, 41 skipped in 53.74s. 27 of the skips are environment-gated (posix-shell gate unsatisfied on this box).
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (949 work item(s), 838 done (88%), 30 cancelled, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=132 LLR=306 TC=320 orphans=0 integrity=0 verified-mechanized=125 verified-demonstrated=6 verified-attested=0 drafts=1 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=246 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. This rewrote the gitignored docs/test/report.md; the tracked tree is unchanged.
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-19e/gate/opus/wi-897-extra tests/test_session_keep.py tests/test_module_size_ratchet.py tests/test_hooks_on_routes.py` -> 184 passed in 25.12s. This is supplementary, because session_keep.py changed.
- `git archive` base/head `project-trajectory/scripts` into the scratch directory. The import probe and the subprocess blackout drive are quoted above.
- 12-run interleaved timing of a no-op hook -> base median 215/213 ms, head median 161/160 ms.

Coverage-extension note (no severity): the kit's other PreToolUse group matches `Task|Agent`, so a Claude Code build that names its subagent tool `Task` reaches neither `LAUNCH_TOOLS` nor the new matcher. That was equally unrefused before this range, since `launch_reason` never named `Task`. The equality pin keeps the matcher and the tables in step, so this lane neither widens nor narrows it.

- [MINOR] docs/archive/last_approved/README.md:164 -> This lane's refresh is cited as authorised by WI-926's adjudication records ("ref: docs/reviews/wi-926/004-ADJUDICATE-fb6c77e.md", "ref: docs/reviews/wi-926/005-ADJUDICATE-ac2e5ea.md"). The copy absorbed only WI-897's traced cells: the snapshot equals the live registries at both 9f934456f and 6e6efb949, and the only changed cells are LLR-301 code_symbol and three TC evidence cells. The README's own rule (line 7) says such a refresh "needs no entry", and earlier traced refreshes cite their own WI. So the act ledger now names another lane's rulings as the authority for this lane's copy. -> Cite the lane's own act (`ref: WI-897`, matching the earlier traced-refresh lines) or record no entry, as line 7 prescribes. -> @owner
- [MINOR] docs/requirements/interfaces.toml:2330 -> K1, for clarity. The lane drops `scripts/session_keep` from IF-065, correctly, but leaves the counterpart seam stale: session_keep.py (`keep_config`) and coordinator_guard.py (`guard_config`) now import agent_policy and call `agent_policy.process_config` directly, yet IF-261 (agent_policy's process-config readers) still names only `scripts/agent_common` as requestor, and agent_policy.py:12's contract text still says agent_common imports and re-exports it. IF-291 (blackout_at) already lists both callers. Neither trace.py (interface-findings=0) nor check_trajectory flags this, so the declared seam now under-states two live call edges this range created. -> Add `scripts/session_keep` and `scripts/coordinator_guard` to IF-261's requestors, or record in the lane's decisions why they stay off it. -> @owner

VERDICT: APPROVE findings=2
