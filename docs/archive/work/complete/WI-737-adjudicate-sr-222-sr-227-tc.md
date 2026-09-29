+++
id = "WI-737"
title = "adjudicate: SR-222, SR-227, TC-264 - spine row(s) authored Drafted on merged trunk a0445a8..5b75c39 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-222", "SR-227"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["SR-222", "SR-227", "TC-264"]
+++

## Deliverable

`OUTCOME: APPROVE rows=3`, from spine-acts batch J, act seq 12. An independent
Opus adjudicator ruled it. The verdict is
[001-ADJUDICATE-349eef9.md](../../../reviews/wi-737-adjudicate-sr-222-sr-227-tc/001-ADJUDICATE-349eef9.md).

- **Approved and anchored:** SR-222, SR-227 and TC-264. These are the rows
  batches G, H and I returned.
- **One real code gap:** it came from WI-738's spot check, passed as chain
  evidence. Keep-warm selects by family, and only the claude adapter bounds
  a call to one turn. The gap is drafted as a successor build item, not a
  return of text that is itself correct. It is below, and the sweep mints
  it.
- **Cross-review:** Sonnet found the act SOUND, with two minors: a
  mislabelled skill section, and a defensible "runner version" reading
  ([sonnet-batch-j.md](../../../reviews/2026-09-28-wave6/sonnet-batch-j.md)).

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-222 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, Rationale, Requirement)
- SR-227 amended in `docs/requirements/system-requirements.toml` (Requirement)
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
`docs/reviews/wi-737-adjudicate-sr-222-sr-227-tc/001-ADJUDICATE-349eef9.md`,
under the governing line `OUTCOME: APPROVE rows=3`. SR-222, SR-227 and TC-264
are approved and anchored in batch J's act. Nothing is returned. The one draft
below fixes a code and design gap that the sitting found under SR-227's
approved text, which is why no requirement text changes: the WI-738 spot check
(observation 2) found it, and the sitting confirmed it at 349eef9.

```toml
title = "Keep warm only a route whose runner bounds a call to one turn: an ANTHROPIC-family route served through opencode, codex or any other runner is pinged today with no turn bound, which breaks SR-227's approved keep-warm clause"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 3
specref = "docs/requirements/low-level-requirements.toml"
sr_refs = ["SR-227"]
```

THE DEFECT, confirmed at 349eef9. SR-227 (Approved) requires the loop to
"make any keep-warm call one bounded turn that never blocks the scheduler".
The keep-warm picks its sessions by family: `keepwarm_due` reads
`record["family"] == "ANTHROPIC"`, and `due_routes` globs `ANTHROPIC-*.json`.
It does not look at the runner. But only `ClaudeAdapter.one_turn` bounds the
argv (`--max-turns 1`). The codex, opencode and plain adapters return it
unchanged. A roster row's `family` is "who trained it" (`agents.template.toml`),
so an adopter's row `family = "ANTHROPIC"` with `cmd_template = "opencode run
-m anthropic/..."` is admissible. Its retained session would be pinged as an
open agentic session, bounded only by `KEEPWARM_TIMEOUT`'s 300 s wall. No
shipped route does this (the template and `docs/agents.toml` route ANTHROPIC
through claude only), so the fix changes no behaviour of a shipped
configuration.

IN SCOPE, exactly the following:

1. **Code.** The dispatcher's keep-warm pings a retained session only on a
   route whose runner's adapter bounds a call to one turn. Today that is the
   claude runner alone. The decision reads the route's adapter
   (`session_adapters.adapter_for` over the row's command template), so a
   runner gaining a one-turn bound later needs no second edit. Do not add a
   runner-name list to `session_keep.py`. A route that fails the test is
   never pinged. Leave its retention, resume, drain and retirement exactly as
   they are.
2. **LLR-270 (Approved)**, `detail`: replace
   `keepwarm_due is true for an ANTHROPIC active session idle keepwarm_minutes while lanes are out;`
   with
   `keepwarm_due is true for an ANTHROPIC active session idle keepwarm_minutes while lanes are out, and a ping is taken only on a route whose runner's adapter bounds a call to one turn (claude's), so a route served through any other runner is never pinged;`.
   If the code adds a symbol, append it to `code_symbol` in the group of the
   module that holds it. Nothing else in LLR-270 changes.
3. **TC-268**, `method`: immediately after
   `for an active ANTHROPIC session idle past the minutes while work is pending,`
   insert
   ` and only on a route whose runner bounds a call to one turn (an ANTHROPIC route served through opencode is never pinged),`.
   Add the one matching test to `tests/test_session_keep.py`. It uses a
   retained ANTHROPIC session, idle past the minutes, whose registry row
   launches `opencode`. Assert that the warmer takes no lease and starts no
   ping. Beside it, the same session on a `claude` row is pinged with
   `--max-turns 1` in its argv. Nothing else in TC-268 changes. If TC-268's
   Method no longer carries that anchor, stop and report it: do not re-place
   the clause.

OUT OF SCOPE, and a lane touching any of it is refused at review:

- SR-227, SR-222 and TC-264, which this sitting approved. Their text is right
  as it stands.
- Every other cell of LLR-270 and TC-268, and every other row, DA-016 and
  DA-017 included.
- A one-turn bound for opencode or codex. If one is wanted, it is its own
  intake.
- The sitting's other readings of the WI-738 observations: the conversation
  id for another runner, the tombstone's lock-free whole write, the 0.5 s
  lock wait on the tick, and basename-prefix matching. They were ruled
  wording, not defects.
