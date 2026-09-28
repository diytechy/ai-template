# SPOTCHECK — WI-719 — the clean close of WI-620, judged at d7e1be0e

A sampled spot check of a GREEN close (`docs/process.toml [attestation]
complete_review = "sample"`). One question: does what shipped answer what the
row asked for — WI-620's own Done-when and the three Done-when blocks it
quotes verbatim from the rows it absorbed, WI-605, WI-606 and WI-551. (The
coordinator's brief names "WI-617's quoted Done-when"; that is the WI-692
brief's wording carried over — WI-617 is the absolutes sweep, restructured
into WI-616, and WI-620 quotes nothing from it. The quoted blocks checked
here are the three the row actually carries.) The close stands whatever is
found here; a finding is a successor row.

What was read: the closed spec
`docs/archive/work/complete/WI-620-one-session-service-for-every.md`; the
absorbed `docs/archive/work/restructured/WI-605-*.md`, `WI-606-*.md` and
`WI-551-*.md`; `project-trajectory/scripts/session_service.py`,
`session_adapters.py` and `session_keep.py`, with their callers in
`agent_loop.py`, `plan_runner.py` and `dispatch.py`; the four fixtures under
`tests/golden/sessions/`; `tests/test_session_service.py`,
`test_session_adapters.py` and `test_session_keep.py`; the `[adjudicator]`
table in `docs/process.toml` and `project-trajectory/process.toml.template`;
`docs/agents.toml`; TC-262 to TC-268 in `docs/test/test-cases.toml`; the five
Codex Sol rounds `docs/reviews/2026-09-27-wave5/sol-wi620*.md`; the log
section "WI-620 lands" in `docs/log.d/2026-09-27-wave5-coordinator.md`; the
squash `b90e84b6` (`--stat` and `--numstat`); and the open row
`docs/work/queued/WI-541-verify-retention-layer.md`. Nothing below rests on
the builder's account of its own work: every clause was driven against the
code, the tests or the diff. No live model or provider CLI was run, by the
brief's rule. HEAD stayed at d7e1be0e throughout.

What was run, on this tree:

- `python -m pytest -q -n 4 tests/test_session_service.py tests/test_session_adapters.py tests/test_session_keep.py tests/test_agent_loop.py tests/test_dual_plan_routing.py tests/test_session_stdin.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_dispatch.py tests/test_seam_resolution.py tests/test_dogfood_sync.py -p no:cacheprovider`
  -> `295 passed, 2 skipped in 204.85s (0:03:24)`, exit 0 (a loaded box;
  the slow modules are in the set).
- `git show --numstat b90e84b6` over the seven pre-existing scripts the
  squash touched -> 218 added, 411 deleted, the Deliverable's figures exactly.
- `grep -rnE "invoke_and_persist|invoke_session\b|_result_accounting|_run_attached_session|family_context_telemetry" project-trajectory/scripts tests`
  -> no hit in any kit script; the only hits are the name list inside
  `test_the_retired_launch_and_logging_paths_are_gone` and a ratchet comment.
- `grep -rnE "run_session\(|subprocess\.(run|Popen)\("` over `agent_loop.py`,
  `plan_runner.py`, `dispatch.py`, `agent_common.py` -> the three
  `subprocess.run` left in `agent_common.py` (lines 1665, 2305, 3185) are
  git and tooling calls, not provider launches; every model call site reads
  `session_service.call(...)` / `.act(...)` / `.record(...)` /
  `.plan_keep(...)` / `.keep_warmer(...)` (`agent_loop.py:2160, 3428, 3462,
  3616, 4182`; `plan_runner.py:173`; `dispatch.py:1433`).
- `tomllib` over both policy files -> `[adjudicator]` is
  `{context_reset_pct: 0, retain_for: [disposition, amendment, red-tc],
  keepwarm_minutes: 0, reset_on_same_artifact: false}` in each, key for key.
- `grep -rn "1\.18\.29|recorded live|corrected occupancy|corrected meaning"`
  over `docs/status.md`, `docs/work/{queued,active,deferred}`,
  `docs/requirements/open-items.toml`, `docs/agents.toml` -> no hit: the two
  owed gaps are recorded only on closed surfaces (the archived spec and the
  log).

## WI-620 Done-when

- [MET] Every model call goes through the service; no role or provider
  keeps its own launch or logging path (grep evidence, and the SLOC removed)
  -> the grep and numstat lines above; `session_service.act` is the one
  launch (`_launch` -> `agent_session.run_session` or `run_attached`) and
  `session_service.record` the one writer (`agent_common.write_session_log`
  + `commit_telemetry`); the worker loop (`launch_session`), the route probe,
  the dual-plan hats (`plan_runner`), the hands-on sitting and the
  dispatcher's keep-warm all hand over a `Call`. Pinned structurally by
  `test_only_the_service_launches_a_provider_runner` and
  `test_only_the_service_writes_a_session_log` over every kit script's
  syntax tree, with seven planted launch mutations and six planted writer
  mutations (`test_the_launch_guard_bites_on_a_direct_provider_launch`,
  `test_the_writer_guard_bites_on_a_second_session_log_writer`), and the
  retired names by `test_the_retired_launch_and_logging_paths_are_gone`.
  Sol's round-1 "not structurally pinned" finding and round-2 "bypassable
  through ordinary indirection" finding are what those mutations answer
  (rulings 53, 54 (e)); round 3 records both forms recognised.
- [MET] The record step writes the S8 schema for Claude, codex and opencode,
  pinned to a named OTel commit, with raw usage verbatim; a fixture test per
  provider -> `session_adapters.OTEL_SEMCONV` pins
  `open-telemetry/semantic-conventions-genai@e57c543b...`; `USAGE_KEYS` is
  one column set for every adapter (`gen_ai.provider.name`,
  `gen_ai.response.model`, `gen_ai.conversation.id`, the five
  `gen_ai.usage.*` counts, `fresh-input-tokens`, `cost-usd`, `usage-scope`,
  `raw-usage`, `cli`, `semconv`); `usage_record` derives inclusive input and
  fresh input by one formula and `_blank` keeps an unreported count "" not
  0; `_verbatim` joins the CLI's own lines unmodified (`json_events` pairs
  each parsed event with the line as written). Per provider:
  `test_claude_usage_is_mapped_to_the_pinned_otel_names` (live fixture),
  `test_codex_usage_is_mapped_inclusive_with_fresh_input_derived` and
  `test_opencode_usage_is_summed_over_its_steps_and_made_inclusive`
  (documented-shape fixtures — see the WI-606 clause below), plus the
  byte-for-byte parametrised cases over all three in
  `test_session_adapters.py` (TC-262). The fixture provenance is stated on
  each non-live fixture's first line, in the test module docstring and in
  TC-262/263/264/267's method cells.
- [MET] Claude's `reasoning-tokens` and `reported-model` defects are fixed
  in its adapter -> `_claude_usage` reads
  `usage.output_tokens_details.thinking_tokens` (the old reader looked for a
  `reasoning_tokens` field no CLI emits) and `_claude_model` takes the last
  assistant event's `message.model`, then the result's `model`, then the one
  `modelUsage` entry whose counters match — never blank because a
  background model's entry sits beside it. Pinned by
  `test_claude_reasoning_tokens_are_read_from_the_field_the_cli_emits`,
  `test_claude_reported_model_survives_a_background_model_beside_it` and
  `test_claude_reported_model_without_assistant_events_is_the_matching_entry`;
  the live fixture carries the haiku background entry the defect tripped on.
- [MET] The service exposes the keep operation WI-551 lands through ->
  `Call.keep` and `Call.one_turn`; `act` calls `session_keep.keep_argv`
  before launch, `keep_bookkeep` after, `keep_abandon` on a raised launch;
  `plan_keep` and `keep_warmer` are the service's entry points and
  `agent_loop.adjudication_keep` / `dispatch.py:1433` use them. The rules
  and the store are `session_keep`'s; nothing there launches or logs
  (the writer guard covers it).
- [MET] The C901 pin and the module-size ratchet hold without re-stamping
  -> `tests/test_complexity_ratchet.py` and `tests/test_module_size_ratchet.py`
  are in the run above; `docs/complexity-baseline` lost exactly the
  `agent_session.py _result_accounting 22` row (the diff at `b90e84b6`);
  the ratchet table reads `agent_common.py: 1466`, `agent_loop.py: 2752`,
  `bootstrap.py: 1704`, each with a dated WI-620 reason. bootstrap's +3 is
  a reviewed bump for the three MAPPING rows, stated in the Deliverable and
  the log — an upward move with its reason, not a silent re-stamp.
- [MET except in the four owed parts it carries] Every absorbed row's
  Done-when quoted below holds; their per-row commit-bar lines are this
  row's one bar -> the thirteen quoted clauses below: eight met, one met by
  supersession, and four NOT met in whole or part and stated as owed in the
  Deliverable, the log and the commit body (the log-fragment half of
  WI-605's third; WI-606's third and WI-551's third for codex and opencode,
  whose fixtures are constructed, not recorded; WI-606's last). One
  bar at the close (smoke 1890 passed / 3 skipped, 38.6 s within 60 s; the
  slow modules and both ratchets 559 passed / 2 skipped; `check_complexity
  --mode enforce` OK), per the log.

## WI-605 Done-when (quoted verbatim into WI-620)

- [MET] Occupancy is computed from the final model call's prompt tokens
  (its input plus cache read plus cache write), not the result's cumulative
  counters, and the docstring names the source field ->
  `ClaudeAdapter.context` sums the LAST `assistant` event's `message.usage`
  `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`
  (fallback: the result's last `usage.iterations` entry) and its docstring
  opens "Source field: the LAST `assistant` event's `message.usage`", and
  states why the result's `usage` is not the source (cumulative; read up to
  34,836%). `OpencodeAdapter.context` reads the last `step_finish`'s
  `part.tokens`; `CodexAdapter.context` refuses the cumulative `exec --json`
  usage and reads the rollout's `last_token_usage.input_tokens` under the
  launch's `CODEX_HOME`. Pinned by
  `test_claude_occupancy_docstring_names_its_source_field`.
- [MET] A test pins it with a recorded multi-call stream where the
  cumulative and last-request values differ ->
  `test_claude_occupancy_is_the_final_calls_prompt_not_the_cumulative_usage`
  over `claude-stream-json.jsonl`, a LIVE two-call recording (CLI 2.1.266,
  2026-09-28): asserts `used == 2 + 48084 + 181`, `cumulative != used`,
  window 1,000,000 from the named model's `modelUsage` entry.
- [MET in the code and the test; the log-fragment half NOT met, owed] No
  newly written session log reports occupancy above 100%; the fix's log
  fragment names the first session recorded under the corrected meaning ->
  `test_claude_occupancy_through_the_invocation_boundary_stays_under_the_window`
  drives the fixture through `act` and asserts `0 <= context-pct <= 100`;
  `_pct` returns "" rather than a guess when no window is reported. No
  session log has been written under the new meaning because the loop has
  made no claim since `docs/work/pause` (2026-09-04); the log names the last
  old-meaning log (`wi521-decomposition-debt-owner-004-20260830-082452.log`)
  and states the first post-merge log is the first under the new one. Honest
  and evidenced; it cannot be met inside a lane while the pause holds. Where
  it should live: see the fold below.

## WI-606 Done-when (quoted verbatim into WI-620)

- [MET] The codex route runs `exec --json` beside `-o`: a successful
  session's final text still comes from `-o`, and its raw usage events are
  kept verbatim in the session's raw record -> `CodexAdapter.prepare` is
  `_ensure(argv, "--json")` then `_codex_lastmsg_setup` (the
  `--output-last-message` temp file); `final_text` returns the file's text
  on exit 0; `raw_usage` keeps every usage-bearing line as written. Pinned
  by `test_codex_route_runs_exec_json_beside_the_last_message_file`,
  `test_codex_json_flag_is_not_doubled_when_the_template_carries_it`,
  `test_a_successful_codex_call_keeps_its_usage_and_its_final_text`
  (asserts the fixture's `turn.completed` line is a substring of
  `raw-usage`).
- [MET] The opencode route runs `run --format json`, and its raw usage
  events are kept verbatim the same way -> `OpencodeAdapter.prepare` is
  `_ensure(argv, "--format", "json")` (the registry's `cmd_template` stays
  `opencode run --dir . -m {model} --auto`; the adapter adds the flag, so
  the route runs it); `raw_usage` keeps every `step_finish` line. Pinned by
  `test_opencode_route_runs_format_json` and
  `test_a_successful_opencode_call_keeps_its_usage_and_its_final_text`
  (both `step_finish` lines survive; the argv ends `--format json`).
- [NOT MET for codex and opencode, openly owed; MET for claude] Each route
  is pinned by a test over a recorded fixture of that CLI's output, showing
  the usage survives a successful call -> the tests above run over
  `tests/golden/sessions/codex-exec-json.jsonl` and
  `opencode-run-json.jsonl`, whose first line each reads "NOT LIVE: built
  from the documented ... event shapes ... The live recording is owed to a
  person." `codex-rollout.jsonl` says the same. The clause asks for a
  fixture "recorded" from "that CLI's output"; a fixture built from
  documented shapes is not that, however openly it is labelled (ruling 57),
  so the clause is not met for the two routes. The builder says so in four
  places (the fixtures, the test docstring, TC-262/263/264/267, the
  Deliverable), so nothing is claimed that was not done. The risk is real
  and stated: a documented shape can drift from the installed CLI (opencode
  is at 1.18.29 against the 1.17.18 last tested), and the adapter would
  then parse blanks silently (`_blank`, `_pct` -> "") rather than fail.
  Where it should live: see the fold below.
- [MET by supersession] Today's parsed columns are unchanged: no new field
  mapping is added -> read on its own this clause is contradicted by the
  shipped adapters, which map codex and opencode usage into the `gen_ai.*`
  columns. But WI-606's Context scopes it as "this row CAPTURES and does
  not map ... S7's adapter maps it once", and WI-620 is S7's adapter: its
  own second clause requires exactly that mapping. Both landed in one
  lane, so the clause's condition (capture without S7) never existed; the
  log's "no parsed column gains a mapping from it" is the same reading —
  the mapping is the adapter's, not an ad-hoc one in the capture. No
  historical log is rewritten. Not a gap.
- [NOT MET, openly owed] The opencode pathway checks are re-run on the
  installed version over the changed route, their output quoted in the log
  fragment, and `docs/agents.toml` records the version actually tested; a
  failing check disables the route or is filed, and the version is not
  bumped over it -> `docs/agents.toml` lines 82, 90 and 98 still read
  "PATHWAY-TESTED 2026-07-19 on the installed CLI (1.17.18)"; no re-run
  output is quoted; the version was not bumped — which is the clause's own
  rule for a check nobody ran. The Deliverable ("Not met here, and owed"),
  the log ("WI-606's last Done-when stays open until then") and the commit
  body all state it, with the cause: the permission classifier refused the
  builder's live runs and they were not worked around. That refusal is
  consistent with this brief's own rule (no live provider run in a lane),
  so the gap is not a lapse; it is a check that only a person on this box
  can run. Honestly stated. Where it should live: see the fold below.

## WI-551 Done-when (quoted verbatim into WI-620)

- [MET] Adjudicator retention runs through the session service's keep
  operation: resume, occupancy, drain and reset, and keep-warm each go
  through the service's act and record steps, and no role or provider code
  launches or logs a retained session on its own (grep evidence) -> resume
  and mint are `session_keep.keep_argv(adapter, argv, keep)` inside `act`;
  occupancy is `adapter.context(...)` inside `act` and bookkept by
  `keep_bookkeep`; drain and reset are `drain_reason` / `is_clear_point` /
  `_retire` in `session_keep`, applied at `keep_for` before the launch;
  keep-warm is `KeepWarmer._ping` -> `act` on its own thread, recorded by
  `_record_call` on the tick's thread. The launch and writer guards cover
  `session_keep.py` like every other kit script (`LAUNCH_HOMES` and
  `WRITER_HOMES` do not exempt it).
- [MET] With `context_reset_pct = 0`, a test shows the layer inert: no
  session id minted, no resume argument, and the launch identical to a
  fresh session's ->
  `test_at_dial_zero_an_adjudication_launches_exactly_as_a_fresh_session`:
  `plan_keep` returns None and reads no CLI version, the retained and fresh
  argv lists are equal, the environment is `None` (ambient, exactly), no
  `--session-id` or `--resume`, and no store directory exists; also
  `test_the_dispatcher_keeps_nothing_warm_at_dial_zero` and
  `test_the_loop_retains_nothing_at_the_shipped_dial`.
- [MET for the reset rules and for claude; NOT MET for codex and opencode's
  resume and occupancy parsing from recorded fixtures, openly owed] With
  the dial on, tests pin the reset rules
  (drain at the dial, retire at a clear point, retire at once on an errored
  session) and each provider's resume and occupancy parsing from recorded
  fixtures -> `test_cresting_the_dial_drains_and_does_not_retire`,
  `test_a_draining_session_retires_at_a_clear_point`,
  `test_an_errored_session_retires_at_once`, plus the further rules Sol's
  rounds forced (transitive lineage, tombstone, expired lease, one clock
  per decision — rulings 54 to 56); resume and occupancy per family in
  `test_a_first_adjudication_mints_and_the_next_resumes` (parametrised over
  ANTHROPIC / OPENAI / OPENCODE: claude `--resume <id>`, codex `exec resume
  <id>`, opencode `--session <id>`) and
  `test_a_retained_codex_route_runs_under_its_dedicated_home_and_reads_occupancy`.
  The same shortfall as WI-606's third clause: the codex and opencode
  streams, and the codex rollout the occupancy reader is driven over, are
  constructed from documented shapes, not recorded from the CLI, and
  TC-267 says so; the clause says "recorded fixtures", so for those two
  routes it is not met (ruling 57). Where it should live: see the fold
  below.
- [MET] A keep-warm ping appears in the session log like any other call ->
  `test_a_keep_warm_ping_is_one_bounded_turn_off_the_tick_and_recorded_on_it`
  reads the written `call_*.log` back through `read_log_meta`: role
  `KEEP-WARM`, source-event `keep-warm`, outcome COMPLETED, `context-pct`
  filled; the argv carried `--resume <minted>` and `--max-turns 1`; the
  commit ran on the tick's thread, none while the ping was in flight.
- [MET] The `[adjudicator]` table ships at 0 in both `docs/process.toml`
  and the template, with matching structure, and the commit bar passes ->
  the `tomllib` comparison above (four keys, identical values, dial 0);
  `test_the_shipped_dial_is_off_in_both_policy_files_with_one_structure`
  asserts the key sets equal and `keep_config(ROOT) == KeepConfig()`;
  `tests/test_dogfood_sync.py` is in the run above; the bar at the close is
  in the log.

## The owed gaps: honestly stated, but homeless

The Deliverable states two owed items (the live codex and opencode
recordings with the opencode re-check; the first corrected-occupancy log),
which are the four not-met clause parts above. Both are stated in the same
words in the Deliverable, the log and the commit body, each with its cause,
and neither is dressed as met. That is the right way to close over a gap a
lane cannot fill. What is missing is a home: neither is on any
forward-looking surface. `docs/status.md`, the
queued rows, `open-items.toml` and `docs/agents.toml` carry no mention of
the owed recordings, the 1.18.29 re-check, or the first corrected-occupancy
log (the grep above). "Owed to a person" and "owed to the first loop run"
are addressees, not rows, and the Deliverable is archived; nothing will
resurface them.

They belong on WI-541, not on a new row. WI-541 ("Verify the retention layer
on this box before the dial is turned") is queued, `needs = ["WI-620"]` is
now satisfied, and its Done-when is already the set of live runs on this box
that produce exactly this evidence: it records each routed family's context
window as reported on this machine, drives a real multi-step, tool-using
adjudication and checks its occupancy "against the latest request's prompt
size, the rule the reset trusts", measures the codex and opencode cache TTLs
and replay times (which is a live codex and a live opencode run), keeps the
dial at 0, and puts each reading in the log fragment under `fig:`. A live
`codex exec --json` and `opencode run --format json` capture, the opencode
pathway checks on the installed CLI, and the first session log written under
the corrected occupancy are by-products of those runs, not new work. A
separate row would duplicate WI-541's setup for three artefacts its runs
already produce, against the owner's direction that the queue shrink.

**Fold into WI-541's Done-when (for the coordinator; no row drafted):**

- The first live `codex exec --json` and `opencode run --format json`
  sessions on this box are recorded into `tests/golden/sessions/` in place
  of the documented-shape fixtures (`codex-exec-json.jsonl`,
  `codex-rollout.jsonl`, `opencode-run-json.jsonl`), their NOT LIVE first
  lines removed, `tests/test_session_adapters.py`'s provenance note and
  TC-262/263/264/267's method cells updated to say so, and the adapter
  tests still green over the recordings; a shape the installed CLI emits
  differently from the documented one is a finding on the adapter, filed,
  not patched into the fixture (WI-606's third clause, "a test over a
  recorded fixture of that CLI's output", and WI-551's third, "each
  provider's resume and occupancy parsing from recorded fixtures" —
  `codex-rollout.jsonl` serves both).
- The opencode pathway checks (stdin prompt delivery, the global `--auto`
  flag, final-text-only stdout under `--format json`, auth) are re-run on
  the installed opencode over the changed route, their output quoted in the
  log fragment, and `docs/agents.toml`'s OPENCODE family and row notes
  record the version actually tested; a failing check disables the route or
  is filed, and the version is not bumped over it (WI-606's last clause,
  carried here verbatim).
- The log fragment names the first session log written under the corrected
  occupancy meaning (the latest request's prompt over the window), and its
  `context-pct` reads at or under 100 (WI-605's third clause, second half).

## Observations, none owed by a clause

1. WI-541's third clause and the fold's third bullet overlap by design:
   the "real multi-step, tool-using adjudication" WI-541 drives is the
   natural first log under the corrected meaning. The coordinator may
   merge them into one clause rather than append.
2. The Deliverable's SLOC sentence ("lost 411 lines and gained 218") is
   exact against `--numstat`, and the ratchet moves it names match the
   table to the line. A close that reports its own numbers this precisely
   is what the sample is for; nothing to fold.
3. `session_adapters.py`'s module docstring says "the session layer
   (`agent_session`) imports it"; the import runs the other way
   (`session_service` imports both, and `agent_session` does not import
   `session_adapters`). One stale sentence, for the next docstring-hygiene
   pass, not a row.

Nineteen clauses checked (WI-620's six, WI-605's three, WI-606's five,
WI-551's five): thirteen met, one met by supersession (WI-606's "no new
field mapping"), four not met in whole or part and openly owed (the
log-fragment half of WI-605's third; WI-606's third and WI-551's third for
codex and opencode, whose fixtures are constructed rather than recorded;
WI-606's last), and WI-620's sixth, the roll-up of the absorbed blocks,
met except in those four parts. All four owed parts fold into WI-541. No
successor row is drafted. The close stands as recorded.

OUTCOME: FOLLOW-UP drafts=0
