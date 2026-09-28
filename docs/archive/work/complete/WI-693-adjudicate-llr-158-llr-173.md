+++
id = "WI-693"
title = "adjudicate: LLR-158, LLR-173, LLR-245, SR-178, TC-167, TC-240 - approved/routed cell(s) amended on merged trunk e520b6e..fe96ec6 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-178"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-158", "LLR-173", "LLR-245", "SR-178", "TC-167", "TC-240"]
+++

## Deliverable

Ruled in spine-acts batch C by an independent Fable adjudicator from the kit's own brief, cross-reviewed by Codex Sol over four rounds (wave-5 rulings 37, 38, 44, 45). The verdict (`docs/reviews/wi-693-adjudicate-llr-158-llr-173/001-ADJUDICATE-1d84d77c.md`) ends:

    VERDICT: MEANING rows=6

The act (ledger seq 5) was narrowed to the LLR and TC registries (ruling 38): 31 rows approved, 9 amendment rows re-attested. The SR registry was not copied, so SR-220, SR-223 and SR-224 stay Drafted, and the SR-tier amendments (WI-695's cells, SR-178) stay drifted and visible for a later act. Batch C's returns are one follow-up, drafted in WI-695's `## Dispositions` and minted at this merge.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-178 `AcceptanceCriteria`: 'An artifact whose normative text has moved since the copy that recorded its acceptance is reported whether or not its S…' -> 'An artifact whose normative text has moved since the copy that recorded its acceptance is reported whether or not its S…'
- SR-178 `Rationale`: 'THE DRIFT half, separable from SR-140 in the direction that matters: a record that exists and rides its approval commit…' -> 'THE DRIFT half, separable from SR-140 in the direction that matters: a record that exists and rides its approval commit…'
- SR-178 `Requirement`: 'The kit shall report any recorded artifact whose text has moved away from the copy recording its acceptance - stakehold…' -> 'The kit shall report any recorded artifact whose text has moved away from the copy recording its acceptance - stakehold…'
- LLR-158 `Detail`: 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…' -> 'An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that c…'
- LLR-173 `Detail`: "The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invar…" -> "The approval RECORD SR-140 requires, sited: LLR-158's comparison basis (SR-178's drift rule) and LLR-178's mirror invar…"
- LLR-245 `Detail`: 'refresh_refusal computes, per registry, the absorbed rows (approved text drifted from the recorded copy) minus the rows…' -> 'refresh_refusal computes, per registry, the absorbed rows (approved text drifted from the recorded copy) minus the rows…'
- TC-167 `Expected`: 'Satisfies SR-140 AcceptanceCriteria via the LLR-173 detail contract, and covers the IF-123 provider seam with the two s…' -> 'Satisfies SR-140 AcceptanceCriteria via the LLR-173 detail contract, and covers the IF-123 provider seam with the two s…'
- TC-167 `Method`: 'Run the record half of the baseline-snapshot suite over real temp repos - the half TC-153 does not cover, which is drif…' -> 'Run the record half of the baseline-snapshot suite over real temp repos - the half TC-153 does not cover, which is drif…'
- TC-240 `Method`: 'Driven on real git repositories through the snapshot command, parameterized over every row-compared tier: requirements,…' -> 'Driven on real git repositories through the snapshot command, parameterized over every row-compared tier: requirements,…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-158 [project-trajectory/scripts/acceptance_record.py :: split_changed_cells/spine_cell_class/_APPROVED_TEXT/_spine_row_sides/staged_spine_amendments/_approval_act/staged_approval_acts/staged_drafted_rows/lane_approval_refusal/SPINE_CSVS/APPROVAL_ACT_CSVS/OUTSIDE_THE_APPROVAL_ACT] tests: TC-153 — The one comparison basis an amendment is measured by
- LLR-271 [project-trajectory/scripts/baseline_snapshot.py;project-trajectory/scripts/trace.py :: NEED_TIERS/load_all/owing_rows/needs_owing/_approved_by_act/need_brief_lines] tests: - — The needs file's two tiers compared with their recorded copy
- LLR-273 [project-trajectory/scripts/baseline_snapshot.py;project-trajectory/scripts/trace.py;project-trajectory/scripts/adjudicate_brief.py :: registry_stamps/_baseline_lines/_spine_stamps/_copy_stamp_lines] tests: - — Each registry's own recorded copy named on the owner's and …
- LLR-278 [project-trajectory/scripts/acceptance_record.py :: amendment_scope/reattested_between/reattest_scope_refusal] tests: - — A re-attestation held at merge to its amendment row's scope
- TC-153 -> tests/test_baseline_snapshot.py::test_the_amendment_seam_is_BLIND_to_an_amend_plus_flip; tests/test_baseline_drift.py::test_a_approved_cell_moving_under_an_approved_row_is_DRIFT; tests/test_baseline_drift.py::test_a_TRACED_cell_moving_is_NOT_drift; tests/test_baseline_drift.py::test_status_itself_is_never_the_amendment; tests/test_baseline_drift.py::test_a_row_below_approval_can_never_be_drifted
- TC-269 -> tests/test_snapshot_readers.py::test_a_drifted_approved_need_is_reported_and_briefed_with_its_diff; tests/test_snapshot_readers.py::test_a_drifted_approved_stakeholder_is_reported_and_briefed; tests/test_snapshot_readers.py::test_an_approved_stakeholder_is_recorded_by_the_act_that_approves_it; tests/test_snapshot_readers.py::test_a_drifted_need_refuses_the_snapshot_until_it_is_reattested

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene

### Interface seams via the touched modules
- IF-001 scripts/trace -> scripts/check: stdout orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-145 scripts/trace -> scripts/check: exit-code 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a stale brief under -…
- IF-146 scripts/trace -> external:downstream adopter: file docs/test/report.md — metric counts, the orphan and finding lists, the joined SN -> SR -> LLR -> TC forest
- IF-166 scripts/trace -> external:downstream adopter: file docs/test/report.html — a self-contained collapsible <details> tree of the SN -> SR -> LLR -> TC forest, writ…
- IF-021 docs/requirements/ -> scripts/trace;external:downstream adopter: file id-keyed TOML, one file per spine tier; ids are the table keys
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys


## Follow-up: no disposition owed

The adjudication is recorded at
`docs/reviews/wi-693-adjudicate-llr-158-llr-173/001-ADJUDICATE-1d84d77c.md`,
governing line `VERDICT: MEANING rows=6`. At the first sitting LLR-173 was
withheld and a one-clause corrective draft sat here; the coordinator amended
the clause in place (2f9912cb, wave-5 ruling 37, status left Approved), the
second sitting blessed the cell on its text, and all six rows are named in
batch C's `--reattests`. No draft remains, so nothing is minted at this row's
merge.

Surfaced, not owed here: the older history sentences the verdict's
non-blocking findings list (LLR-245's "two snapshot tests", LLR-158's
status-fold parenthetical, TC-167's "uncited today", SR-178's "last to
reach"), which predate or sit beside this amendment and are a clarity sweep
of their own.
