+++
id = "WI-973"
title = "adjudicate: LLR-246, LLR-249, LLR-278, SR-208, SR-228, TC-241, TC-278 - approved/routed cell(s) amended on merged trunk 31b8ed9..afb57ae (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-208", "SR-228"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-246", "LLR-249", "LLR-278", "SR-208", "SR-228", "TC-241", "TC-278"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-851's in-lane sitting
`docs/reviews/wi-851/004-ADJUDICATE-d860906.md` blessed all seven rows as
MEANING+BLESS, and the lane's act turn took act seq 156 (and 157 for its
two first approvals). At the landing afb57ae33 the stakeholder, system,
low-level and test registries are byte-equal to their approved snapshots
under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-208 `AcceptanceCriteria`: 'With the rung held, a change the loop or a dispatched session makes to a status cell of that registry, including a row …' -> "With a snapshotted registry's rung held, a lane approval claim is refused naming the row, its rung and the dial unless …"
- SR-208 `Coincident`: "The need asks for a held tier changed only by a person; the loop's own status changes refused before they land is that …" -> 'The need asks for a held tier changed only by a person; refusing an unbound lane approval claim and a marked autonomous…'
- SR-208 `Rationale`: "The approval level names the rungs a human still approves, and an automated approval of the spine's own rows is already…" -> "The approval level names the rungs a human still approves, and an automated approval of the spine's own rows is already…"
- SR-208 `Requirement`: "Where the declared approval level holds an off-spine registry's rung for a human, the delivered loop shall refuse any c…" -> "Where the declared approval level holds a snapshotted registry's rung for a human, the delivered harness shall refuse, …"
- SR-208 `Title`: 'The loop never changes a status the approval level holds for a human' -> 'Held-rung changes are refused before they land'
- SR-228 `AcceptanceCriteria`: 'On a held tier, an adjudication act re-attesting a row is refused unless its recorded verdict names that row as CLARITY…' -> 'On a held tier, an adjudication act re-attesting a row is refused unless its recorded verdict names that row as CLARITY…'
- LLR-246 `Detail`: 'staged_status_moves(root, base, head) reports every change to a status cell of an off-spine registry between two trees …' -> 'staged_status_moves(root, base, head) reports every change to a status cell of an off-spine registry between two trees …'
- LLR-246 `SR-Refs`: 'SR-208' -> 'SR-208;SR-228'
- LLR-246 `Title`: 'Refusing a loop-made status change on a held off-spine registry, at every loop writer' -> 'Refusing held-rung claims from a lane or marked autonomous commit'
- LLR-249 `Detail`: 'kitlib/authority.py holds a pure dial comparison: dial_from_config(table) reads human_approval_through from a parsed po…' -> 'kitlib/authority.py holds a pure dial comparison: dial_from_config(table) reads human_approval_through from a parsed po…'
- LLR-278 `Detail`: 'acceptance_record.merge_approval_refusal applies the additional adjudication bounds whenever any claimed row records a …' -> 'acceptance_record.merge_approval_refusal applies the additional adjudication bounds whenever any claimed row records a …'
- TC-241 `Expected`: "Satisfies SR-208's acceptance: a held status change is refused naming registry, row and rung where the loop commits and…" -> 'Satisfies SR-208, SR-228 and LLR-246: A held claim is refused unless it is a copy claim whose live Status is unchanged …'
- TC-241 `Method`: 'Driven on real git repositories with the dial holding DevStg-Boundary. A lane whose range changes a frame or assumption…' -> 'Driven on real git repositories with the dial holding DevStg-Boundary. A lane whose commit flips a row into approval, a…'
- TC-241 `Verifies`: 'SR-208;LLR-246;IF-196' -> 'SR-208;SR-228;LLR-246;IF-196'
- TC-278 `Expected`: "Satisfies LLR-278 (parents SR-178 and SR-228): a re-attestation outside the amendment row's Adjudicates scope is refuse…" -> 'Satisfies LLR-278 (parent SR-178): Every id re-attested by an act the merge base does not hold outside the amendment sc…'
- TC-278 `Method`: 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…' -> 'Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requi…'
- TC-278 `Verifies`: 'SR-178;SR-228;LLR-278;IF-091' -> 'SR-178;LLR-278;IF-091'

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested, bound to the text the verdict judged, and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-153 [project-trajectory/scripts/intake.py :: intake_after_merge/_amendment_drafts/mint_gap_rows/parse_dispositions/parse_disposition_section/next_wi_id/context_block/_inject_open_item/_pending_oi_lines/adjudication_action/flip_verified/_standing_successors/_title_identity_refusal/_repoint_owed] tests: (see TC-147) — The unified trunk-side intake mint + the context block + th…
- LLR-245 [project-trajectory/scripts/baseline_snapshot.py;project-trajectory/scripts/intake.py :: refresh_refusal/_ledger_live_rows/_unattested_rows/parse_reattests/verdict_rel/_refuse_verdict] tests: - — Row-level refusal in the snapshot refresh
- LLR-246 [project-trajectory/scripts/held_status.py;project-trajectory/scripts/integrate.py;project-trajectory/scripts/intake.py;project-trajectory/scripts/handback.py;project-trajectory/scripts/agent_common.py;project-trajectory/scripts/agent_policy.py;project-trajectory/scripts/check.py;project-trajectory/scripts/bookkeeping.py;project-trajectory/scripts/kitlib/authority.py;project-trajectory/scripts/text_then_act.py;project-trajectory/scripts/kitlib/git.py :: staged_status_moves/held_status_refusal/_held_status_refusal/_claim_locked/_mint/_commit_residue_as_is/commit_telemetry/APPROVAL_RUNGS/_commit_object/dial_at/read_dial/merge_status_moves/pending_status_moves/registry_held/held_claims/held_approval_lines/commit_held_approval_lines/marked_refusal/_spine_status_moves/_held_squash_refusal/loop_held_status_refusal/squash_walk/grep_files] tests: TC-241 — Refusing held-rung claims from a lane or marked autonomous …
- LLR-278 [project-trajectory/scripts/acceptance_record.py;project-trajectory/scripts/kitlib/verdict.py :: first_approval_scope/adjudication_approval_refusal/merge_approval_refusal/_registry_identity/lane_acted_set/_copy_lines/amendment_scope/reattested_between/_wrote_ledger/_added_acts/row_rulings/verdict_rulings/_tier_of/reattest_scope_refusal] tests: TC-278; TC-331 — An adjudication re-attestation constrained at merge
- LLR-359 [project-trajectory/scripts/acceptance_record.py;project-trajectory/scripts/adjudicate_brief.py;project-trajectory/scripts/kitlib/sitting.py;project-trajectory/scripts/adjudicate_act.py :: approved_text_digest/amendment_values/_identity/requested_identities/bind_pending/record_outcome/render_requested/write_binding/read_identities/accepted_identities/_state/_unbound_text] tests: TC-398; tests/test_adjudicate_brief.py::test_the_amendment_brief_states_each_shown_rows_digest; tests/test_adjudicate_brief.py::test_bind_pending_records_the_briefs_identities; tests/test_adjudicate_brief.py::test_record_outcome_keeps_the_identity_cell; tests/test_adjudicate_act.py::test_a_held_CLARITY_act_whose_text_changed_after_the_verdict_is_refused; tests/test_coordinator_act.py::test_the_act_turn_refuses_before_launch_when_held_text_moved — A held re-attestation carries the text identity its verdict…
- TC-147 -> tests/test_intake.py; tests/test_intake.py::test_a_replay_re_points_a_late_dependent_to_the_full_successor_set; tests/test_intake.py::test_a_title_match_off_the_drafts_lineage_refuses_the_mint; tests/test_intake.py::test_a_drafts_title_match_on_its_own_lineage_stays_standing; tests/test_intake.py::test_a_replay_with_nothing_left_to_re_point_commits_nothing; tests/test_intake.py::test_drafts_and_adoptions_together_hold_the_full_successor_set; tests/test_intake.py::test_a_recorded_adoption_re_points_a_dependents_needs

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/dispatch;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict;scripts/plan_coverage;scripts/review_brief: call parse_verdict: typed verdict findings, where a finding is a bullet whose bracket names one of the module's de…
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup;scripts/plan_coverage;scripts/review_brief: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N; finding is - [BLOCKER|MAJOR|MINOR] <text>, case-insensitive;…
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-175 scripts/kitlib/verdict <- scripts/integrate;scripts/agent_loop;scripts/dispatch;scripts/gen_verdict_rollup;scripts/score_reviews;scripts/acceptance_record;scripts/adjudicate_act;scripts/review_brief;scripts/adoption_record: call tree identity; branch rounds/trailers; row rulings and blessed rows; scope, phase, filing and trailer readers…
