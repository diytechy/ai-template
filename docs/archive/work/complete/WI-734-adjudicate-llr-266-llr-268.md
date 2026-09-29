+++
id = "WI-734"
title = "adjudicate: LLR-266, LLR-268, SR-222, SR-227, TC-264 - spine row(s) authored Drafted on merged trunk 69902bc..03debc7 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-222", "SR-227"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-266", "LLR-267", "LLR-268", "LLR-269", "LLR-270", "SR-222", "SR-227", "TC-264"]
+++

## Deliverable

`OUTCOME: RETURN rows=8`, from spine-acts batch I, act seq 11. The verdict is
[001-ADJUDICATE-22e7b24.md](../../../reviews/wi-734-adjudicate-llr-266-llr-268/001-ADJUDICATE-22e7b24.md).

- **Approved and anchored:** LLR-266, LLR-267, LLR-268, LLR-269 and LLR-270.
  The last three were carried from batches G and H.
- **Returned:**
  - SR-222 and TC-264: the shipped gemini route is neither provider-agnostic
    nor a stand-in, so the row's open domain needs a bound, and its
    "including when..." clause is ambiguous;
  - SR-227: its acceptance obliges the keep-warm and whole-write clauses its
    `shall` never states.
- **Follow-up:** the exact replace-this-with-that Dispositions draft below,
  with an explicit out-of-scope list. The sweep mints it.
- **Cross-review:** Sonnet found the act SOUND
  ([sonnet-batch-i.md](../../../reviews/2026-09-28-wave6/sonnet-batch-i.md)).

## Context

Carry-over added 2026-09-29 by the coordinator, from spine-acts batches G and H. LLR-267, LLR-269 and LLR-270 were approved in both batches' verdicts, but their flips were held behind the blocked LLR snapshot, which LLR-223 blocked until WI-732 answered it. They are added to `adjudicates` so this brief renders them. Judge them on their current text (unchanged since batch G), and flip them in this act if they hold.

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-222 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, DA-Refs, Requirement)
- SR-227 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, DA-Refs)
- LLR-266 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- LLR-268 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-264 amended in `docs/test/test-cases.toml` (Method)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

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

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-734-adjudicate-llr-266-llr-268/001-ADJUDICATE-22e7b24.md`,
under the governing line `OUTCOME: RETURN rows=8`. WI-733's verdict,
`docs/reviews/wi-733-adjudicate-llr-223-sr-177-t/001-ADJUDICATE-22e7b24.md`
(`VERDICT: MEANING rows=6`), returns nothing.

LLR-266 to LLR-270 are approved and anchored in batch I's act, beside
WI-733's re-attestations of SR-177, SR-193, LLR-222, LLR-223, LLR-286 and
TC-267. SR-222, SR-227 and TC-264 are RETURNED and stay `Drafted`, every cell
byte-exact. This is one draft: one lane, and one adjudication at its merge.

```toml
title = "Batch I returns: bound SR-222's usage record to the runners the loop reads (the shipped gemini route is not one) and add TC-264's case for any other runner; put SR-227's keep-warm and whole-write acceptance clauses into its shall"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 3
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-222", "SR-227"]
bar = "DevStg-Reqs"
```

IN SCOPE: exactly the text replacements below, copied as written, in three
Drafted rows, plus one test. Every `Status` stays `Drafted`. Do not reword,
extend or "improve" any other part of these cells or of any other cell. The
last two sittings each stalled on one rewritten cell that said more than its
row. A replacement that differs from the words given here is a new
obligation, and the adjudication at this merge will return it.

1. **SR-222 (Drafted)**. The defect: the kit's shipped routing template carries a gemini route. The plain adapter records that runner with no runner name, no provider, no raw usage and no counts, while the row promises its default provider and its usage "whichever provider command-line runner serves it". There is also an ambiguous "including when …" clause (the WI-735 spot check, observation 1).
   - `requirement`: replace `the vocabulary's gen_ai.provider.name holding the runner's default provider — anthropic for claude and openai for codex — and empty for a provider-agnostic runner or a stand-in, with runner reconfiguration to another provider not detected, and the context occupancy of the session's latest request kept apart from its billed tokens.` with `the vocabulary's gen_ai.provider.name holding the runner's default provider for claude and codex and empty for any other runner, with runner reconfiguration to another provider not detected, and the context occupancy of the session's latest request kept apart from its billed tokens; for a runner other than claude, codex and opencode, the runner name is left empty, and so is every count or raw usage the loop cannot read from the runner's output.`
   - `acceptance_criteria`: replace `For a recorded session of each routed runner,` with `For a recorded session of the claude, codex and opencode runners,`.
   - `acceptance_criteria`: replace `gen_ai.provider.name is anthropic for claude, openai for codex, and empty for a provider-agnostic runner or a stand-in, including when runner reconfiguration means the default-provider value does not identify the provider serving the call;` with `gen_ai.provider.name is anthropic for claude and openai for codex, also when that runner is reconfigured to another provider, and empty for opencode;`.
   - `acceptance_criteria`: replace the closing `because counts accumulated across its requests.` with `because counts accumulated across its requests; and a session of any other runner, a stand-in included, carries the same columns, with its runner and its gen_ai.provider.name empty, and every count or raw usage the loop cannot read from the runner's output empty.`
   - `rationale`: insert this one sentence immediately before `Fed back to the need:`: `A runner whose output the loop does not read is still recorded, with what it cannot read left empty rather than guessed, so the record shows which calls carry no usage instead of reporting them as zero.`
   - Nothing else in SR-222 changes: not `SN-Refs`, `Boundary-Refs`, `DA-Refs`, `Hat-Refs`, `Title`, or any other words of these three cells.
2. **TC-264 (Drafted)**, `method`: immediately after `a stand-in's provider name is empty;` insert ` a runner other than claude, codex and opencode, over output carrying no claude-shaped result (a gemini --output-format json result), gets the same columns with its runner, its provider name, its raw usage and every token count empty;`. Add the one matching test to `tests/test_session_service.py`: a `gemini` argv over a gemini-shaped result, asserting `cli`, `gen_ai.provider.name`, `raw-usage` and the five `USAGE_COUNT_KEYS` plus `fresh-input-tokens` are `""`, and the keys equal `USAGE_KEYS`. The behaviour already holds (probed at 22e7b24: `adapter_for` gives the plain adapter, and all of those are empty), so no code changes. Nothing else in TC-264 changes.
3. **SR-227 (Drafted)**, `requirement`: replace `retire it at once when a call on it fails; and let no two calls use one retained session at once.` with `retire it at once when a call on it fails; let no two calls use one retained session at once; write the retention state only whole, by one writer at a time; and make any keep-warm call one bounded turn that never blocks the scheduler.`. Nothing else in SR-227 changes. The acceptance already states these two conditions, and LLR-270 and TC-266 to TC-268 already implement and test them.

OUT OF SCOPE, and a lane touching any of it is refused at review:

- LLR-266 to LLR-270, which batch I approved. Their text already states the rules above, and any edit re-opens them.
- Every other row, DA-016 and DA-017 included.
- All code.
- A gemini output reader. If one is wanted, it is a new decomposition across LLR-266, LLR-267, LLR-268 and their test cases, through its own intake.
- The two observations WI-733's verdict records and does not draft (LLR-223's failed-row precedence, and SR-177's "stated build gap" clause).
