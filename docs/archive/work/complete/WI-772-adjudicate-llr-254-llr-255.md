+++
id = "WI-772"
title = "adjudicate: LLR-254, LLR-255, SR-215, TC-247, TC-248 - approved/routed cell(s) amended on merged trunk 00467fc..1ffd8c5 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-215"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-254", "LLR-255", "SR-215", "TC-247", "TC-248", "TC-036", "TC-055", "TC-209", "TC-210", "TC-211"]
+++

## Deliverable

Spine-acts batch O (act seq 22): `MEANING rows=10`, all re-attested: SR-215,
LLR-254, LLR-255, TC-247, TC-248, and the carried TC-036, TC-055, TC-209, TC-210
and TC-211. A dated addendum records two misses that the cross-review found and
that ride WI-773's follow-up: TC-055's `expected` still stated the old cadence
when re-attested, and SR-215's rationale overclaimed the floor's bound.

## Context

Carried in by the coordinator 2026-10-03, as WI-770's spec (WI-766's draft, "Landing") commits: TC-036, TC-055, TC-209, TC-210 and TC-211. Their WI-747 amendments were ruled MEANING and blessable in WI-766's verdict, but could not be re-anchored while TC-248 stayed unblessed; no merge since has touched them, so no mint routes them here. Judge them afresh.

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-215 `AcceptanceCriteria`: 'Every observation case references a numbered rubric written before its first judgement; existing omissions warn. No res…' -> 'A case with no result is due at once, and a case whose result expired is due at once; neither waits for the floor. Othe…'
- SR-215 `Coincident`: "The needs ask for an observation's result re-judged when what it judged changes; one re-judge item filed per stale case…" -> 'The needs ask that an accepted observation not stand on a state it never judged, and that it be judged against written …'
- SR-215 `Rationale`: 'Judgements cost time and model calls and vary across sessions. A fixed rubric makes the pass criterion reviewable; a cl…' -> 'Judgements cost time and model calls and vary across sessions. Written pass criteria fixed before the first judgement m…'
- SR-215 `Requirement`: 'When a work item merges, a release is prepared or a stage gate is checked, the delivered harness shall file one re-judg…' -> 'When a work item merges, a release is prepared or a stage gate is checked, the delivered harness shall file one re-judg…'
- SR-215 `Title`: 'At a checkpoint, a changed or expired observation test is queued once for re-judging' -> 'At a checkpoint, an unjudged, expired or triggered observation test is queued once for re-judging'
- LLR-254 `Detail`: 'A sibling of consolidate.py imported by intake. observation_test_cases(root, rev) reads observation cases at a revision…' -> 'A sibling of consolidate.py imported by intake. observation_test_cases(root, rev) reads observation cases at a revision…'
- LLR-255 `Detail`: 'intake_after_merge adds rejudge.checkpoint_drafts(root, after, "merge") to its drafts inside the held merge slot, so th…' -> 'intake_after_merge adds rejudge.checkpoint_drafts(root, after, "merge") to its drafts inside the held merge slot, so th…'
- LLR-255 `Title`: 'The merge and release checkpoints file the re-judge items' -> 'The merge, release and stage-gate checkpoints file the re-judge items'
- TC-247 `Method`: 'checkpoint_drafts driven on a real git repository. No result and expiry are due independently of the floor. Changed inp…' -> 'checkpoint_drafts driven on a real git repository. No result and expiry are due independently of the floor. Changed inp…'
- TC-248 `Expected`: "Satisfies SR-215's acceptance at both checkpoints: a work-item merge and release preparation each file one re-judge ite…" -> "Satisfies SR-215's acceptance at every checkpoint: a work-item merge, release preparation and stage-gate preparation ea…"
- TC-248 `Method`: 'Driven through intake on a real git repository. A merged work item satisfying an observation case’s trigger and closed-…' -> "Driven through intake on a real git repository. A merged work item satisfying an observation case's trigger and closed-…"

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
