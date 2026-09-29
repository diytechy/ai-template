+++
id = "WI-731"
title = "adjudicate: LLR-266, LLR-268, SR-222, SR-227, TC-264 - spine row(s) authored Drafted on merged trunk a20b496..17c54c2 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-222", "SR-227"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-266", "LLR-267", "LLR-268", "LLR-269", "LLR-270", "SR-222", "SR-227", "TC-262", "TC-264"]
+++

## Deliverable

`OUTCOME: RETURN rows=9`, from spine-acts batch H, act seq 10. The verdict is
[001-ADJUDICATE-3e8a87d.md](../../../reviews/wi-731-adjudicate-llr-266-llr-268/001-ADJUDICATE-3e8a87d.md).

- **Approved and anchored:** TC-262.
- **Approved but not flipped:** LLR-267, LLR-269 and LLR-270. The LLR
  registry is blocked by LLR-223.
- **Returned:**
  - SR-222, LLR-268 and TC-264: a codex routed through `model_providers` is
    recorded as `openai`, and "the adapter" is a mechanism written into an
    SR;
  - SR-227: its "declared bound" is a code default, the reason goes only to
    stderr, and no test asserts it;
  - LLR-266: "no codex command template carries -o" is an absolute over the
    templates adopters write.
- **Follow-up:** the one consolidated Dispositions draft below, with seven
  items. It includes WI-730's SR-177 and LLR-223 and the carry-over.
- **Cross-review:** Sonnet found the act SOUND
  ([sonnet-batch-h.md](../../../reviews/2026-09-28-wave6/sonnet-batch-h.md)).

## Context

Carry-over added 2026-09-29 by the coordinator, from spine-acts batch G. LLR-267, LLR-269, LLR-270 and TC-262 were APPROVED in batch G's WI-724 verdict, but their Status flip was held: the LLR and TC snapshot was refused while WI-726's returned LLR-223 and TC-220 drifted. They are added to `adjudicates` so this brief renders them. Judge them afresh on the current text (WI-729 did not touch them), and flip them in this act if they still hold.

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-222 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, Requirement)
- SR-227 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, Requirement)
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
`docs/reviews/wi-731-adjudicate-llr-266-llr-268/001-ADJUDICATE-3e8a87d.md`,
under the governing line `OUTCOME: RETURN rows=9`. WI-730's verdict,
`docs/reviews/wi-730-adjudicate-llr-222-llr-223/001-ADJUDICATE-3e8a87d.md`
(`VERDICT: MEANING rows=7`), returns SR-177 and LLR-223, and its follow-up
is folded in here: one draft, one lane, one adjudication at its merge.

TC-262 is approved and anchored in batch H's act, and TC-220 and TC-222 are
re-attested there. LLR-267, LLR-269 and LLR-270 are approved on their text
but NOT flipped, and LLR-222 and LLR-286 are blessed but NOT anchored,
because the LLR registry cannot be copied while LLR-223 holds amended text
that has not been blessed. SR-193 is blessed as CLARITY but NOT anchored,
because the SR registry cannot be copied while SR-177 does. SR-222, SR-227,
LLR-266, LLR-268 and TC-264 are RETURNED and stay `Drafted`, every cell
byte-exact.

```toml
title = "Batch H returns: fix gen_ai.provider.name for reconfigurable runners (SR-222, LLR-268, TC-264), close SR-227's held-session acceptance, drop LLR-266's -o absolute, keep SR-177's rationale inside its acceptance, scope LLR-223's contradiction advisory to the joint class"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 3
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-222", "SR-227", "SR-177", "SR-193"]
bar = "DevStg-Reqs"
```

IN SCOPE: the cells below, amended in place. Every `Status` stays as it is.
`Drafted` rows stay `Drafted`. SR-177 and LLR-223 stay `Approved`, and each
amendment to them is owed a re-attestation. The rules behind these items are
spine-authoring §2(b) (voice), §2(d2) (an absolute is a promise every child
keeps), §3 (does anything the row says go unverified) and §6 (a reason cell
holds reasons, not obligations).

1. `SR-222.requirement` and `SR-222.acceptance_criteria`: "set by the
   adapter to the provider its runner serves and left empty for a
   provider-agnostic runner" treats a runner as bound to one provider. The
   kit's shipped `agents.template.toml` codex row notes "third-party
   providers via the codex model_providers config", and the claude CLI can
   be pointed at other hosts. So the clause does not decide whether a
   reconfigured codex records `openai` or nothing, and under the child's
   per-runner constant it records a false provider. Restate the value so
   something the call actually knows fixes it, for example the route's
   declared family where that names exactly one provider, and empty
   otherwise. Or state the limit plainly: the runner's default provider,
   with a reconfigured runner not detected. State WHAT the value is, not
   which component sets it, since "the adapter" is a mechanism in the SR
   voice. Also decide SR-222's classification: trace reports it
   unclassified, and a usage record whose truth rests on the runner's own
   usage events is a premise about the world.
2. `LLR-268.detail` and `session_adapters.py` (`ClaudeAdapter.provider`,
   `CodexAdapter.provider`, and the plain and opencode adapters): implement
   and state item 1's rule. Everything else in the Detail stands.
3. `TC-264.method` and `tests/test_session_service.py`: make the
   provider-name assertions item 1's rule, including a case for the
   reconfigured or undetermined provider if the rule names one. The rest of
   the Method stands.
4. `SR-227.acceptance_criteria`: in "waits up to the declared bound and then
   runs unretained with the reason recorded", "the declared bound" names no
   declaration. The wait is `keep_for`'s default `lease_wait=120.0`, and
   `[adjudicator]` does not declare it. "With the reason recorded" is also
   stronger than the row's own shall ("state why") and than LLR-270
   ("saying why"): the reason is printed to stderr, and the unretained
   call's accounting carries none. The smallest fix is "waits a bounded
   time and then runs unretained, stating why". Then add to `TC-267.method`
   and `test_an_adjudication_waits_out_a_keep_warm_lease_then_runs_unretained`
   an assertion that the reason is stated (it names the holder). TC-267 is
   Approved, so that amendment re-opens it. If the lane instead declares the
   bound or records the reason in the call's accounting, amend LLR-270 and
   its code with it. Also decide SR-227's classification: it is reported
   unclassified.
5. `LLR-266.detail`: "and no codex command template carries -o" is an
   absolute over templates that adopters write, and nothing verifies it.
   `_codex_lastmsg_setup`'s own docstring handles a template that carries
   `-o` (the adapter's temp file is appended last, and codex takes the last
   one). Drop the clause, or state that behaviour instead.
6. `SR-177.rationale`: "The report must aggregate the existing per-session
   wall time, API time, turns and token telemetry by lane and by run" is an
   obligation wider than the row's acceptance, which asks for no token or
   per-lane aggregation. Restate the build gap as a reason, not a `must`,
   with no added inputs. That gap is that no per-run aggregation joins
   configured lanes, occupied lanes and integrated work per wall-hour from
   the telemetry that already exists. If token or per-lane aggregation is
   wanted, it is an acceptance change and belongs to its own approval, not
   the rationale.
7. `LLR-223.detail`: "DA-Refs with Coincident, or Delivered-With with
   Coincident, is an advisory naming the contradiction" says any
   Delivered-With beside a waiver is reported as a contradiction. SR-193's
   acceptance ("both joint delivery and a waiver"), TC-220 and
   `sr_classification_advisories` scope it to the JOINT class. A row whose
   only sibling is disjoint and which records a waiver classifies
   `coincident`, with only the disjoint advisory, and a joint row with
   DA-Refs and a waiver gets the joint-waiver advisory only. Scope the
   sentence to the classes (a joint row with a waiver; a non-joint row with
   DA-Refs and a waiver). If the lane holds that any Delivered-With beside a
   waiver contradicts, change the code, TC-220 and SR-193 together instead.

CARRY-OVER THE MERGE'S ADJUDICATION MUST ALSO TAKE. The derived brief will
not show these rows, because this lane does not amend them. The coordinator
composing that adjudication adds them:

- first approval (approved in batch G and again in batch H; flip plus the
  LLR snapshot): LLR-267, LLR-269, LLR-270;
- re-attestation (`--reattests`): LLR-222 and LLR-286, blessed as MEANING
  in batch G and batch H, and SR-193, blessed as CLARITY in batch H. Each
  of their drifted cells must be named once its registry can be copied.

The LLR registry cannot be anchored until item 7 is answered and LLR-223
re-attested. The SR registry cannot be anchored until item 6 is answered
and SR-177 re-attested. Out of scope: the live recording of the codex and
opencode fixtures, which is owed to a person, as TC-262, TC-263, TC-264 and
TC-267 already state.
