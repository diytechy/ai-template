+++
id = "WI-720"
title = "SR-222/SR-227 chains: name the provider column, drop the decision frame, restate the history and time-relative sentences as standing prose, describe claude's raw-usage line as the code holds it, and pin TC-268's second-tick assertion"
workstream = "process"
sr_refs = ["SR-222", "SR-227"]
specref = ""
buildtier = "quick"
priority = 3
safety_class = "spine"
bar = "DevStg-Reqs"
+++

## Deliverable

Fourteen cells across ten Drafted rows are restated as the standing
system, every status left Drafted, for the first-approval adjudication the
sweep mints:

- **SR-222:** the requirement and acceptance name the route's `provider`
  (from its roster row, for every routed call) and `gen_ai.provider.name`
  (where the runner reports one). The decision frame is gone from the
  rationale.
- **SR-227:** the rationale states the standing cost of a fresh adjudicator
  per item. The review noted that the builder also dropped the "hour-long
  cache / standing process" comparison in that sentence; it is accepted as
  still true, for the adjudication to judge.
- **LLR-266 to LLR-270:** each detail and rationale carries no history or
  receipt. LLR-268 and `session_adapters.py`'s IF-245 docstring describe
  claude's raw usage as the whole result event line, verbatim.
- **TC-262, TC-264:** the expected cells state conditions, not "as before"
  or "defects fixed".
- **TC-268:** its evidence asserts the second tick's skip line exactly.
  HEAD already produces it deterministically, so the test was green before
  and after.

**Evidence:** the session modules ran `103 passed` (builder and reviewer).
With the rows flipped to Approved, `trace.py --strict` showed no
requirement-form finding.

**Review:** the Sonnet reviewer found it SOUND at 9a7c063d, with one minor
finding ([sonnet-wi720.md](../../../reviews/2026-09-28-wave6/sonnet-wi720.md)).

## Context

Drafted by WI-718 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

IN SCOPE — fourteen cells across ten Drafted rows, amended in place with every
status left `Drafted`, then the first-approval adjudication the merge's sweep
mints. The rule behind ten of them (spine-authoring §6): a rationale, a
method or an expected cell states the STANDING system — what breaks without
the row, which alternative lost, what is observed — never its own history, a
fix it answers or a status; keep the reason, send the account to the log.

1. `SR-222.requirement` and `SR-222.acceptance_criteria`: "the provider and
   the runner that produced the row named" / "the provider and runner columns
   are filled" — say WHICH provider column: the route's `provider` (the
   family from the roster row, filled for every routed call), with the
   vocabulary's `gen_ai.provider.name` filled where the runner reports one
   (opencode names none — LLR-268). The obligation set is unchanged; the
   children keep their `SR-Refs`/`Verifies`.
2. `SR-222.rationale`: drop the decision frame "was the owner's choice";
   keep the argument (the problem is not novel; the vocabulary has no tagged
   release, so the record pins a revision).
3. `SR-227.rationale`: "an unattended run that re-spun a fresh adjudicator
   for every small work item reloaded the spine each time, and its usage was
   extreme" — restate as the standing consequence in present voice (a run
   that spins a fresh adjudicator per item reloads the spine each call; the
   record makes that cost visible), without the past observation or the
   unquantified word.
4. `LLR-266.detail`: "no longer reads any file back" — state what holds (the
   launch captures the stream whole; the adapter, not the launch, reads the
   final text). `LLR-266.rationale`: drop "Before this, ..." and state what
   breaks without the row (a route whose final text replaces its stream loses
   its usage; a route asked for no structured output has none to keep).
5. `LLR-267.rationale`: drop "read up to 34,836% in the iteration index";
   the standing argument stands alone (the counters accumulate over every
   request, so their sum over the window overstates occupancy).
6. `LLR-268.detail`: claude's raw usage is the WHOLE result event line,
   verbatim (`session_adapters._claude_raw`; pinned by
   `tests/test_session_service.py::test_claude_usage_is_mapped_to_the_pinned_otel_names`),
   not "the result's usage, modelUsage and total_cost_usd values" — say so,
   and that the line carries the result text, which is why the log writer
   redacts header values (LLR-177). Fix the same sentence in
   `session_adapters.py`'s Contract IF-245 docstring paragraph in the same
   commit (a code comment, not a registry cell; no registry row moves).
   `LLR-268.rationale`: drop "The two claude fields were misread before:
   ..." and state the standing reasons (the reasoning count lives under
   `output_tokens_details`; the response model is read from the request that
   answered, so a background model's entry beside it cannot blank it).
7. `LLR-269.rationale`: "Two recording wrappers and an in-line logging path
   existed, so a fix ... landed in one of them" — restate as what breaks
   without the row (a launch or logging path per role sends a fix to one path
   and not the others).
8. `TC-262.expected`: replace "while the final text is read as before" with
   the condition (the final text is codex's last-message file and opencode's
   last speaking step).
9. `TC-264.expected`: replace "and the two claude defects fixed" with the two
   conditions (the reasoning count read from the field the runner emits; the
   response model filled beside a background model's usage). Optionally
   assert the pinned revision for codex and opencode too, as the Method
   claims it for each adapter.
10. `TC-268.method` or its evidence: `tests/test_session_keep.py`
    `test_a_keep_warm_ping_is_one_bounded_turn_off_the_tick_and_recorded_on_it`
    asserts `lines == [] or lines == ["keep-warm: skipped (a ping is in
    flight)"]` while the Method says a second tick "starts nothing and says
    so". Pin the assertion to the line (the path is deterministic at HEAD),
    or drop "and says so" from the Method; the row claims what its evidence
    asserts.
11. `LLR-270.rationale`: "at the off dial the launch must be exactly
    today's" — a time-relative receipt (ruling 59, the same class as
    TC-262's "read as before"); state the standing condition the parent's
    acceptance and the code hold: at the off dial the launch is exactly a
    fresh session's.

Before handing back, flip the ten rows to `Approved` in the working tree,
run `python project-trajectory/scripts/trace.py --root . --strict`, confirm
no `requirement form` finding, and flip them back: the gate is silent on a
Drafted row. Run `python -m pytest -q -n 4 tests/test_session_adapters.py
tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider`
(103 cases at d7e1be0e).

OUT OF SCOPE: every other cell of the ten rows (the acceptance criteria,
`Hat-Refs`, `SN-Refs`, `Boundary-Refs`, `Verifies`, tiers and levels all
HOLD); the four approved rows TC-263, TC-265, TC-266, TC-267; the
codex and opencode live recordings and the opencode re-check (owed to a
person under WI-606's open Done-when, not to this lane); the `Form` advisory
`trace.py` prints (no SR declares one); SR-222's and SR-227's unclassified
assumption state (SR-193 reports it without failing; do not invent a DA or a
waiver).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-266 [project-trajectory/scripts/session_adapters.py :: adapter_for/CodexAdapter/OpencodeAdapter/json_events] tests: (see TC-262) — One adapter per provider runner captures its structured out…
- LLR-267 [project-trajectory/scripts/session_adapters.py :: ClaudeAdapter.context/CodexAdapter.context/OpencodeAdapter.context] tests: (see TC-263) — Context occupancy is read from the latest request's prompt
- LLR-268 [project-trajectory/scripts/session_adapters.py :: OTEL_SEMCONV/USAGE_KEYS/USAGE_COUNT_KEYS/usage_record/_claude_usage/CodexAdapter.usage/OpencodeAdapter.usage] tests: (see TC-264) — Each adapter maps its runner's usage to the pinned OpenTele…
- LLR-269 [project-trajectory/scripts/session_service.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/plan_runner.py :: Call/act/record/call;launch_session;_dp_session] tests: (see TC-265) — One session service launches and records every model call
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/store_lock/store_load/write_tombstone/load_honoured/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/take_warm_lease;cli_version/plan_keep/KeepWarmer/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268) — The keep operation retains adjudicator sessions through act…
- TC-262 -> tests/test_session_adapters.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-061 scripts/plan_artifacts <- scripts/plan_runner: call allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-064 scripts/agent_session <- scripts/agent_loop;scripts/session_service;scripts/plan_runner: call build_argv, run_session, parse_json_result and the console renderers
