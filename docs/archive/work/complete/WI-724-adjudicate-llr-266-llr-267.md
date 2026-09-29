+++
id = "WI-724"
title = "adjudicate: LLR-266, LLR-267, LLR-268, LLR-269, LLR-270, SR-222, SR-227, TC-262, TC-264 - spine row(s) authored Drafted on merged trunk 4dd6827..bbe00d8 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
sr_refs = ["SR-222", "SR-227"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-266", "LLR-267", "LLR-268", "LLR-269", "LLR-270", "SR-222", "SR-227", "TC-262", "TC-264"]
+++

## Deliverable

`OUTCOME: RETURN rows=9`, from spine-acts batch G. An independent Opus
adjudicator sat once over WI-724, WI-726 and WI-728 and took one act (seq 9).
The verdict is
[001-ADJUDICATE-f1733da.md](../../../reviews/wi-724-adjudicate-llr-266-llr-267/001-ADJUDICATE-f1733da.md).

- **Approved in the verdict but not flipped:** LLR-267, LLR-269, LLR-270 and
  TC-262. The snapshot refuses to copy the LLR and TC registries while
  WI-726's returned LLR-223 and TC-220 drift, so these four stay Drafted,
  and their first approval is owed to the adjudication after the follow-up
  lane.
- **Returned:**
  - SR-222: "where the runner reports one", when the adapter names the
    provider as a constant;
  - SR-227: its one shall has no mint case or held-session case;
  - LLR-266: "as before", and the false "already carried";
  - LLR-268: the provider name's source is decomposed nowhere;
  - TC-264: the pinned revision is asserted for claude only.
- **Follow-up:** the one consolidated `## Dispositions` draft below. It also
  carries WI-726's LLR-223 and TC-220 returns, and the carry-over of owed
  first approvals and re-attestations. Intake mints it at this merge.
- **Cross-review:** Sonnet found the act SOUND
  ([sonnet-batch-g.md](../../../reviews/2026-09-28-wave6/sonnet-batch-g.md)).

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- SR-222 amended in `docs/requirements/system-requirements.toml` (AcceptanceCriteria, Rationale, Requirement)
- SR-227 amended in `docs/requirements/system-requirements.toml` (Rationale)
- LLR-266 amended in `docs/requirements/low-level-requirements.toml` (Detail, Rationale)
- LLR-267 amended in `docs/requirements/low-level-requirements.toml` (Rationale)
- LLR-268 amended in `docs/requirements/low-level-requirements.toml` (Detail, Rationale)
- LLR-269 amended in `docs/requirements/low-level-requirements.toml` (Rationale)
- LLR-270 amended in `docs/requirements/low-level-requirements.toml` (Rationale)
- TC-262 amended in `docs/test/test-cases.toml` (Expected)
- TC-264 amended in `docs/test/test-cases.toml` (Expected)

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

Folded 2026-09-28 from WI-725's spot check of WI-720's close
(`docs/reviews/wi-725-spot-check-the-clean-close-of/001-SPOTCHECK-bbe00d8a.md`).
Judge these as part of the chain. Each is a return with findings if it
holds:

1. **LLR-266 `detail`** still reads as history in two places:
   - "so a stand-in agent is accounted as before", the time-relative kind
     WI-720 fixed in TC-262;
   - "the --output-last-message temp file it already carried", which is
     untrue: `CodexAdapter.prepare` adds `--json` and `-o`, and no codex
     template in `docs/agents.toml` carries `-o`.
2. **TC-264 `method`** claims that each adapter's record carries the pinned
   revision, but only claude's `semconv` is asserted. The fix is to add the
   assert to the codex and opencode usage tests, or to narrow the Method.
3. **SR-222's "where the runner reports one":** the adapters name the
   provider as a constant, and no runner reports it. Decide whether the
   wording should say the adapter names it.

Beside the rows, and not for this act: `session_adapters.py`'s module
docstring and the "old reader" note in `_claude_usage` still describe
history. A returning lane that touches the file should restate them.

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-724-adjudicate-llr-266-llr-267/001-ADJUDICATE-f1733da.md`,
governing line `OUTCOME: RETURN rows=9`. LLR-267, LLR-269, LLR-270 and TC-262
are APPROVED on their text but NOT flipped: the copy of the LLR and TC
registries is refused while WI-726's returned LLR-223 and TC-220 hold drifted
approved text. SR-222, SR-227, LLR-266, LLR-268 and TC-264 are RETURNED and
stay `Drafted`, every cell byte-exact. WI-726's verdict
(`docs/reviews/wi-726-adjudicate-llr-222-llr-223/001-ADJUDICATE-f1733da.md`)
returns LLR-223 and TC-220, and its follow-up is consolidated here. One draft,
one lane, one adjudication at its merge: the LLR and TC registries can only be
anchored again once both sets are answered.

```toml
title = "Batch G returns: name the adapter as gen_ai.provider.name's source, give SR-227's shall its mint and held-session cases, restate LLR-266's two phrases, pin TC-264's revision asserts, and make the joint class need a sibling that shares a need (LLR-223, TC-220, the classifier)"
workstream = "process"
safety_class = "spine"
buildtier = "medium"
priority = 3
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-222", "SR-227", "SR-193"]
bar = "DevStg-Reqs"
```

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
