+++
id = "WI-729"
title = "Batch G returns: name the adapter as gen_ai.provider.name's source, give SR-227's shall its mint and held-session cases, restate LLR-266's two phrases, pin TC-264's revision asserts, and make the joint class need a sibling that shares a need (LLR-223, TC-220, the classifier)"
workstream = "process"
sr_refs = ["SR-222", "SR-227", "SR-193"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "medium"
priority = 3
safety_class = "spine"
bar = "DevStg-Reqs"
+++

## Context

Drafted by WI-724 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

IN SCOPE: the cells below, amended in place. Every `Status` stays as it is:
`Drafted` rows stay `Drafted`, and LLR-223 and TC-220 stay `Approved` with
their amendment owed a re-attestation. The rule behind the wording items is
spine-authoring §6 (a cell states what holds, never its history) and §2(d2)
(an absolute is a promise every child keeps).

1. `SR-222.requirement` and `SR-222.acceptance_criteria`: replace "the
   vocabulary's gen_ai.provider.name filled where the runner reports one" and
   "gen_ai.provider.name is filled where the runner reports one and empty where
   it does not" with the standing fact. No runner reports a provider. The
   adapter names the provider its runner serves, and leaves it empty where the
   runner may route to any provider (the opencode gateway). The obligation set
   is otherwise unchanged.
2. `LLR-268.detail`: state that source: claude's record names `anthropic`,
   codex's names `openai`, and opencode's and a stand-in's name none.
   `ClaudeAdapter.provider` / `CodexAdapter.provider`; the plain adapter's `""`.
3. `TC-264.method` and `tests/test_session_service.py`: the Method claims
   every adapter's record carries the pinned revision, but only claude's
   `semconv` is asserted. Add the assert to the codex and opencode usage cases
   (the preferred fix), or narrow the Method. Name the provider-name asserts
   the cases already make (`anthropic`, `openai`), and add opencode's empty
   one, so the case verifies item 1's clause.
4. `LLR-266.detail`: "so a stand-in agent is accounted as before" becomes the
   condition (a stand-in gets the plain adapter, which leaves argv, final text
   and usage as the claude-shaped reader returns them). "codex gets --json
   beside the --output-last-message temp file it already carried" becomes
   what holds: the adapter adds both `--json` and the `-o` temp file, and no
   codex template carries `-o`.
5. `SR-227.requirement`: the shall launches EACH retained-class adjudication
   "in its model runner's resume form against a session an earlier
   adjudication on the same route started". That is broken by the row's own
   acceptance (a first launch, or a launch after a retirement, starts one
   whose id is recorded) and by LLR-270 (a held session is waited on up to
   `lease_wait`, then the adjudication runs unretained, saying why). Restate
   the response to cover all three cases: resume the route's active, unheld
   session; otherwise mint one and record its id; and a held session is
   waited on for a bounded time, then run unretained, saying why. Add that
   last clause to `SR-227.acceptance_criteria` (TC-267 already drives it: "an
   adjudication meeting a keep-warm lease runs unretained"). LLR-270's text
   already matches and does not change.
6. `project-trajectory/scripts/session_adapters.py` (code comments, no
   registry row): the module docstring's "the codex route threw its usage
   away on every successful call", `_claude_usage`'s "the old reader looked
   for …", and the plain adapter's "accounted exactly as before" (line 206)
   and "as the kit always read one" (line 223) become what holds.
7. `LLR-223.detail` and `project-trajectory/scripts/assumption_rules.py`
   `_classify`: SR-193 makes a row joint when ONE OR MORE declared siblings
   share at least one of its needs. The Detail's "a non-empty Delivered-With
   whose entries are declared requirements sharing a need" reads as every
   entry, and the code returns `joint` for any non-empty, all-declared list
   (`elif siblings:`). So a row whose only sibling shares no need is `joint`
   with no unclassified report, where SR-193 says it is unclassified. Make the
   Detail state SR-193's condition exactly. Make `_classify` classify joint
   only when at least one declared sibling shares a need; otherwise the row
   falls through to bridged, coincident or unclassified, with the disjoint
   advisory still raised per sibling.
8. `TC-220.method` / `expected` and `tests/test_assumption_rules.py`: assert
   the CLASS in the two cases the text claims. A row whose only sibling shares
   no need is not joint (it is unclassified when it carries nothing else). A
   row naming one sharing and one disjoint sibling is joint, with the disjoint
   one reported. Today `test_a_joint_requirement_and_sibling_with_no_shared_need_are_reported`
   checks only the advisory, which is how item 7's departure passed.

OPTIONAL, folded here because the lane is already in these registries (each
re-opens its row, and the merge's adjudication then judges it):

9. `LLR-222.title` names only "assumption citations and coincident waiver".
   Name `delivered_with` too.
10. `SR-193.rationale` does not argue the joint class: why a sibling list is
    neither a DA (a premise about the world) nor a coincident waiver (a sole
    delivery claim), and why Delivered-With re-opens attestation while
    DA-Refs does not. State both reasons as standing prose.
11. `SR-177.rationale` still reads "NOT DECOMPOSED … the row lands
    Drafted-undecomposed" at `Status = Approved`, with LLR-196 beneath it,
    and cites a plans document by section. State the standing build gap (the
    per-run aggregation) without the receipt or the citation frame.

CARRY-OVER THE MERGE'S ADJUDICATION MUST ALSO TAKE. These rows will not be in
the brief derived from this lane's delta, because the lane does not amend
them. The coordinator composing that adjudication adds them:

- first approval (ruled APPROVE in batch G; flip plus the LLR/TC snapshot):
  LLR-267, LLR-269, LLR-270, TC-262;
- re-attestation (ruled MEANING and blessed in batch G; `--reattests`):
  LLR-222 (unless item 9 amends it, which puts it in the derived brief),
  TC-222, and WI-728's LLR-286.

The LLR and TC registries cannot be anchored until items 7 and 8 are
answered and LLR-223 and TC-220 are re-attested, so no approval in those two
registries should be attempted before this lane merges. Out of scope: the
live recording of the codex and opencode fixtures, which is owed to a person,
as TC-262, TC-263, TC-264 and TC-267 already state.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-222 [project-trajectory/scripts/kitlib/spine.py;project-trajectory/scripts/spine_carrier.py;project-trajectory/scripts/migrate_carrier.py;project-trajectory/scripts/acceptance_record.py;project-trajectory/registries/system-requirements.template.toml :: SPINE_TIER_KEYS/SPINE_COLUMN/KEY/SPINE_APPROVED_CELLS] tests: - — The requirement's assumption citations and coincident waive…
- LLR-223 [project-trajectory/scripts/assumption_rules.py :: SR_CLASSES/sr_classification_advisories/da_citing_srs] tests: - — The requirement classification advisories
- LLR-225 [project-trajectory/scripts/acceptance_record.py :: SPINE_TRACED_CELLS/SPINE_APPROVED_CELLS/OFFSPINE_TRACED_CELLS] tests: - — Each new cell's class: traced or approved content
- LLR-266 [project-trajectory/scripts/session_adapters.py :: adapter_for/CodexAdapter/OpencodeAdapter/json_events] tests: (see TC-262) — One adapter per provider runner captures its structured out…
- LLR-267 [project-trajectory/scripts/session_adapters.py :: ClaudeAdapter.context/CodexAdapter.context/OpencodeAdapter.context] tests: (see TC-263) — Context occupancy is read from the latest request's prompt
- LLR-268 [project-trajectory/scripts/session_adapters.py :: OTEL_SEMCONV/USAGE_KEYS/USAGE_COUNT_KEYS/usage_record/_claude_usage/CodexAdapter.usage/OpencodeAdapter.usage] tests: (see TC-264) — Each adapter maps its runner's usage to the pinned OpenTele…

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-058 scripts/plan_round <- scripts/plan_runner;scripts/agent_loop: call disposition: CONTINUE · SELECTED · PAGE
- IF-061 scripts/plan_artifacts <- scripts/plan_runner: call allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
