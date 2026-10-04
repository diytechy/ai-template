+++
id = "WI-792"
title = "adjudicate: LLR-118, LLR-153, LLR-158, LLR-167, LLR-245, LLR-271, LLR-278, SR-178, TC-123, TC-147, TC-153, TC-161, TC-240, TC-278 - approved/routed cell(s) amended on merged trunk 2aad71a..9c9e83b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-174", "SR-178", "SR-207"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-118", "LLR-153", "LLR-158", "LLR-167", "LLR-245", "LLR-271", "LLR-278", "SR-178", "TC-123", "TC-147", "TC-153", "TC-161", "TC-240", "TC-278"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second sitting is held (the re-mint trap, S11 plan §4.2; owner-agreed close, 2026-10-03). The fourteen rows were ruled by the in-lane adjudicator over three rounds (verdicts 001, 003 and 005 under `docs/reviews/wi-791-oi100-amended-needs-adjudic/`; SR-178 CLARITY, the rest MEANING and blessed) and re-attested at act seq 29. The system-requirements, low-level-requirements and test-cases registries are byte-identical to their `docs/archive/last_approved/` anchors at this row's mint (c27d316d).

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-178 `AcceptanceCriteria`: 'An artifact whose normative text has moved since the copy that recorded its acceptance is reported whether or not its S…' -> 'An artifact whose normative text has moved since the copy that recorded its acceptance is reported whether or not its S…'
- LLR-118 `Detail`: 'The RENDERED half of the Modified/Draft attestation regime whose gate SR-049 derives. gen_open_items renders (a) every …' -> 'The RENDERED half of the Modified/Draft attestation regime whose gate SR-049 derives. gen_open_items renders (a) every …'
- LLR-153 `Detail`: 'The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id count…' -> 'The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id count…'
- LLR-153 `SR-Refs`: 'SR-174' -> 'SR-174;SR-228'
- LLR-158 `Detail`: 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…' -> 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…'
- LLR-167 `Detail`: "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint that has a brief to…" -> "The row's DECLARED `Brief` cell selects the template (`intake` writes it at every adjudication mint that has a brief to…"
- LLR-245 `Detail`: 'refresh_refusal computes, per registry, the absorbed rows (approved text drifted from the recorded copy) minus the rows…' -> 'refresh_refusal computes, per registry, the absorbed rows (approved text drifted from the recorded copy) minus the rows…'
- LLR-245 `SR-Refs`: 'SR-207' -> 'SR-207;SR-228'
- LLR-271 `Detail`: "baseline_snapshot.NEED_TIERS names the needs file's need tier (SN-ID) and stakeholder tier (STK-ID), and SNAPSHOT_TIERS…" -> "baseline_snapshot.NEED_TIERS names the needs file's need tier (SN-ID) and stakeholder tier (STK-ID), and SNAPSHOT_TIERS…"
- LLR-278 `Detail`: 'acceptance_record.merge_approval_refusal calls reattest_scope_refusal first for an adjudication lane, and it acts only …' -> 'acceptance_record.merge_approval_refusal calls reattest_scope_refusal and held_reattest_refusal for an adjudication lan…'
- LLR-278 `SR-Refs`: 'SR-178' -> 'SR-178;SR-228'
- LLR-278 `Title`: "A re-attestation held at merge to its amendment row's scope" -> 'An adjudication re-attestation constrained at merge'
- TC-123 `Method`: 'Drive gen_open_items over temp repos: assert a pending registry row renders as a brief and a RULED row does not; that D…' -> 'Drive gen_open_items over temp repos: assert a pending registry row renders as a brief and a RULED row does not; that D…'
- TC-147 `Method`: "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…" -> "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…"
- TC-147 `Verifies`: 'SR-174;LLR-153;IF-091' -> 'SR-174;SR-228;LLR-153;IF-091'
- TC-153 `Method`: 'Run the drift half of the baseline-snapshot suite. It first drives the premise: test_the_amendment_seam_is_BLIND_to_an_…' -> 'Run the drift half of the baseline-snapshot suite. It first drives the premise: test_the_amendment_seam_is_BLIND_to_an_…'
- TC-153 `Verifies`: 'SR-178;LLR-158' -> 'SR-178;LLR-158;IF-091'
- TC-161 `Method`: 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…' -> 'Drive the real loop against a fake agent CLI over throwaway git repos for the disposition, red-TC and amendment briefs,…'
- TC-240 `Expected`: "Satisfies SR-207's acceptance: a drifted row outside the act refuses the refresh naming row and cell; adding it clears …" -> "Satisfies SR-207's acceptance: a drifted row outside the act refuses the refresh naming row and cell; adding it clears …"
- TC-240 `Method`: 'Driven on real git repositories through the snapshot command, parameterized over every row-compared tier: requirements,…' -> 'Driven on real git repositories through the snapshot command, parameterized over every row-compared tier: requirements,…'
- TC-240 `Verifies`: 'SR-207;LLR-245' -> 'SR-207;SR-228;LLR-245'
- TC-278 `Expected`: "Satisfies LLR-278 (parent SR-178): a re-attestation outside the amendment row's Adjudicates scope is refused at merge b…" -> "Satisfies LLR-278 (parents SR-178 and SR-228): a re-attestation outside the amendment row's Adjudicates scope is refuse…"
- TC-278 `Method`: 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…' -> 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…'
- TC-278 `Verifies`: 'SR-178;LLR-278;IF-091' -> 'SR-178;SR-228;LLR-278;IF-091'

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
- LLR-153 [project-trajectory/scripts/intake.py :: intake_after_merge/_amendment_drafts/mint_gap_rows/parse_dispositions/next_wi_id/context_block/adjudication_action/flip_verified] tests: (see TC-147) — The unified trunk-side intake mint + the context block + th…
- LLR-154 [project-trajectory/scripts/integrate.py :: integrate_one/_lane_bar_directives/_refresh_bar] tests: (see TC-148) — The merge slot's post-merge intake arm
- LLR-158 [project-trajectory/scripts/acceptance_record.py :: split_changed_cells/spine_cell_class/_APPROVED_TEXT/_spine_row_sides/staged_spine_amendments/_amended_cells/_approval_act/staged_approval_acts/staged_drafted_rows/lane_approval_refusal/SPINE_CSVS/AMENDMENT_CSVS/APPROVAL_ACT_CSVS/OUTSIDE_THE_APPROVAL_ACT] tests: TC-153 — The one comparison basis an amendment is measured by
- LLR-245 [project-trajectory/scripts/baseline_snapshot.py;project-trajectory/scripts/intake.py :: refresh_refusal/_unattested_rows/parse_reattests/verdict_rel/_refuse_verdict] tests: - — Row-level refusal in the snapshot refresh
- LLR-271 [project-trajectory/scripts/baseline_snapshot.py;project-trajectory/scripts/trace.py :: NEED_TIERS/load_all/owing_rows/needs_owing/tier_owing/_approved_by_act/need_brief_lines] tests: - — The needs file's two tiers compared with their recorded copy
- LLR-273 [project-trajectory/scripts/baseline_snapshot.py;project-trajectory/scripts/trace.py;project-trajectory/scripts/adjudicate_brief.py :: registry_stamps/_baseline_lines/_spine_stamps/_copy_stamp_lines] tests: - — Each registry's own recorded copy named on the owner's and …

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-021 docs/requirements/ -> scripts/trace;external:downstream adopter: file id-keyed TOML, one file per spine tier; ids are the table keys
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
