+++
id = "WI-775"
title = "adjudicate: SR-215, TC-055 - approved/routed cell(s) amended on merged trunk f2bc66c..ba68016 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-215"]
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-215", "TC-055"]
+++

## Deliverable

Act seq 23 (retaken): TC-055's `expected` amendment ruled MEANING and re-attested.
SR-215's `rationale`, ruled MEANING and first blessed, was NOT re-attested.
Codex Luna's cross-review found it misleading, and an independent Opus arbiter
ruled B (`docs/reviews/2026-10-03-wave8/ARBITRATION.md`). Its exact replacement
rides WI-776's drafted successor.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-215 `Rationale`: 'Judgements cost time and model calls and vary across sessions. Written pass criteria fixed before the first judgement m…' -> 'Judgements cost time and model calls and vary across sessions. Written pass criteria fixed before the first judgement m…'
- TC-055 `Expected`: 'APPROVE citing numbered anchors. The rubric is the single home of the live-vs-retired anchor set: its header states the…' -> 'APPROVE citing numbered anchors. The rubric is the single home of the live-vs-retired anchor set: its header states the…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-254 [project-trajectory/scripts/rejudge.py :: observation_test_cases/checkpoint_for/checkpoint_drafts/_open_rejudge/due_cases/BRIEF/CHECKPOINTS] tests: - — The checkpoint re-judge decision
- LLR-255 [project-trajectory/scripts/intake.py;project-trajectory/scripts/gen_release_checklist.py :: intake_after_merge/mint_rejudge/_cmd_rejudge/_rejudge_checklist_line] tests: - — The merge, release and stage-gate checkpoints file the re-j…
- LLR-265 [project-trajectory/scripts/intake.py :: merged_outcomes/_merged_shape_refusal/_cmd_sweep] tests: - — The merge-slot intake re-run for a merge made outside the s…
- LLR-293 [project-trajectory/scripts/observation_cadence.py :: Cadence] tests: - — The observation cadence policy
- LLR-294 [project-trajectory/scripts/observation_cadence.py :: observation_rubric_findings] tests: - — The observation rubric-reference advisory
- LLR-295 [project-trajectory/scripts/adjudicate_brief.py :: _assumption_case_chain/_render_assumption_cases/_rejudge_case_text] tests: TC-308;TC-309 — Assumption-only observation cases in adjudicator briefs

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — human-verified rows use `- [ ] <ID> — <what to confirm> (refs)`; assumption confi…
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-034 docs/requirements/ -> scripts/gen_release_checklist;external:downstream adopter: file None
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-075 scripts/trace <- scripts/gen_open_items;scripts/adjudicate_brief: call reattest_model entries: chain rows, changed cells, baseline rev and date, and each spine registry's own copy …
