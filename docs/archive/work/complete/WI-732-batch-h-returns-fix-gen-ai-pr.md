+++
id = "WI-732"
title = "Batch H returns: fix gen_ai.provider.name for reconfigurable runners (SR-222, LLR-268, TC-264), close SR-227's held-session acceptance, drop LLR-266's -o absolute, keep SR-177's rationale inside its acceptance, scope LLR-223's contradiction advisory to the joint class"
workstream = "process"
sr_refs = ["SR-222", "SR-227", "SR-177", "SR-193"]
specref = ""
buildtier = "medium"
priority = 3
safety_class = "spine"
bar = "DevStg-Reqs"
+++

## Deliverable

Batch H's seven returns are answered, every status left as it was.

- **The two registry-blocking cells:**
  - SR-177's rationale states only the gap its acceptance holds;
  - LLR-223's contradiction sentence is scoped to the classes SR-193,
    TC-220 and the code report (a joint row with a waiver; a non-joint row
    with DA-Refs and a waiver).

  The review probed both and found them exact.
- **SR-222 and LLR-268:** `gen_ai.provider.name` holds the runner's default
  provider (anthropic for claude, openai for codex, empty for a
  provider-agnostic runner or a stand-in), and a runner reconfigured to
  another provider is not detected. TC-264 and its tests cover the
  reconfigured codex and the stand-in.
- **SR-227:** it "waits a bounded time and then runs unretained, stating
  why". TC-267 and its test assert that the reason names the holder.
- **LLR-266:** its absolute over adopter templates is gone.
- **Classification:** SR-222 and SR-227 are bridged through two new Drafted
  assumptions, both landing at B-09:
  - DA-016: runners serve their default provider unless reconfigured;
  - DA-017: a provider honours its documented resume form.

  The review wanted B-10. An independent Opus arbiter ruled B-09, the
  stakeholder's crossing, per SR-195 and the kit's own reach check
  ([ARBITRATION.md](../../../reviews/2026-09-28-wave6/ARBITRATION.md),
  ruling 1).
- **Evidence:** both new assertions already held, because the behaviour was
  present. The required modules ran `370 passed, 1 skipped` (builder) and
  `319 passed` (reviewer). The flip probe found no form finding.
- **Review:** [sonnet-wi732.md](../../../reviews/2026-09-28-wave6/sonnet-wi732.md).
- **Owed at this merge's adjudication:** the carry-over, which is the first
  approvals of LLR-267, LLR-269 and LLR-270, and the re-attestations of
  LLR-222, LLR-286 and SR-193. The coordinator adds them to the minted rows.

## Context

Drafted by WI-731 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

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

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-196 [project-trajectory/scripts/agent_common.py :: regenerate_index/per_turn_pace/per_turn_context] tests: (see TC-191) — Per-session fan-out utilisation telemetry, unaggregated
- LLR-222 [project-trajectory/scripts/kitlib/spine.py;project-trajectory/scripts/spine_carrier.py;project-trajectory/scripts/migrate_carrier.py;project-trajectory/scripts/acceptance_record.py;project-trajectory/registries/system-requirements.template.toml :: SPINE_TIER_KEYS/SPINE_COLUMN/KEY/SPINE_APPROVED_CELLS] tests: - — The requirement's assumption citations, joint-delivery sibl…
- LLR-223 [project-trajectory/scripts/assumption_rules.py :: SR_CLASSES/sr_classification_advisories/da_citing_srs] tests: - — The requirement classification advisories
- LLR-225 [project-trajectory/scripts/acceptance_record.py :: SPINE_TRACED_CELLS/SPINE_APPROVED_CELLS/OFFSPINE_TRACED_CELLS] tests: - — Each new cell's class: traced or approved content
- LLR-266 [project-trajectory/scripts/session_adapters.py :: adapter_for/CodexAdapter/OpencodeAdapter/json_events] tests: (see TC-262) — One adapter per provider runner captures its structured out…
- LLR-267 [project-trajectory/scripts/session_adapters.py :: ClaudeAdapter.context/CodexAdapter.context/OpencodeAdapter.context] tests: (see TC-263) — Context occupancy is read from the latest request's prompt

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-061 scripts/plan_artifacts <- scripts/plan_runner: call allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
