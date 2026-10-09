+++
id = "WI-872"
title = "adjudicate: SR-146 - approved/routed cell(s) amended on merged trunk 15d3673..f7e492b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-146"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-146"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). WI-852's in-lane adjudicator, through the retained session, ruled SR-146's amendment MEANING and blessed it (verdicts 001 to 003 under `docs/reviews/wi-852-coordinator-renders-kit-briefs/`), and re-attested it in the lane (act 71). The system, low-level and test-case registries are byte-identical to their anchors in `docs/archive/last_approved/` at `bbe148ea`.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-146 `AcceptanceCriteria`: 'An unknown or unfilled slot is a refusal; a missing shipped template is a named preflight refusal rather than a first-s…' -> 'An unknown or unfilled slot is a refusal and an attended render writes no brief; a missing shipped template is a named …'
- SR-146 `Requirement`: 'Every prompt the delivered loop launches shall be a shipped, reviewable file with strictly filled slots — listed by dig…' -> 'Every prompt the delivered loop launches or an attended launcher renders as a review or critique brief shall be a shipp…'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested naming its `--verdict` and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-162 [project-trajectory/scripts/prompts.py :: load/fill/strict_check/digest/catalog_rows/preflight] tests: TC-157 — Prompts as loaded files, catalogued and fingerprinted
- LLR-163 [project-trajectory/scripts/agent_session.py :: substitute/split_cmd/build_argv] tests: TC-157 — Argv arrays, and the adjudicator as a routed phase
- LLR-164 [project-trajectory/scripts/gen_prompt_catalog.py :: render/main] tests: TC-192 — The generated prompt catalogue and its freshness gate
- LLR-167 [project-trajectory/scripts/adjudicate_brief.py :: compose/_assemble/disposition_values/red_tc_values/consolidate_values/amendment_values/_unchained_amended_rows/first_approval_values/_line_refusal/declared_brief/adjudicates] tests: TC-161; TC-331 — The adjudicator briefs' evidence, and the refusal that keep…
- LLR-273 [project-trajectory/scripts/baseline_snapshot.py;project-trajectory/scripts/trace.py;project-trajectory/scripts/adjudicate_brief.py :: registry_stamps/_baseline_lines/_spine_stamps/_copy_stamp_lines] tests: - — Each registry's own recorded copy named on the owner's and …
- LLR-295 [project-trajectory/scripts/adjudicate_brief.py :: _assumption_case_chain/_render_assumption_cases/_rejudge_case_text] tests: TC-308;TC-309 — Assumption-only observation cases in adjudicator briefs

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-041 external:agent CLI <- scripts/agent_session: cli headless invocation; the prompt on stdin
- IF-064 scripts/agent_session <- scripts/agent_loop;scripts/session_service;scripts/plan_runner: call build_argv, run_session, parse_json_result and the console renderers
- IF-075 scripts/trace <- scripts/gen_open_items;scripts/adjudicate_brief: call reattest_model entries: chain rows, changed cells, baseline rev and date, and each spine registry's own copy …
- IF-097 scripts/prompts <- scripts/agent_loop;scripts/plan_briefs: call load | fill | preflight | digest | template_path | strip_dispatcher_block; KIT_PROMPTS is the key vocabulary
- IF-098 scripts/prompts <- scripts/gen_prompt_catalog: call catalog_rows() -> (key, file, slots, digest) per shipped prompt
