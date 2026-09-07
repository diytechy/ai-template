+++
id = "WI-616"
title = "Prove abrupt primary publication and exclusive-writer boundaries"
workstream = "process"
sr_refs = ["SR-174"]
needs = ["WI-610", "WI-611"]
buildtier = "strong"
safety_class = "spine"
+++

## Deliverable

Proved abrupt process loss before and after the real atomic-commit call, explicit pre-commit residue reconciliation and no duplicate successor, plus held-slot exclusion through the actual primary engine. Evidence, measured checks, obligation mapping and independent source review are recorded in docs/reviews/wi612-authoring/. Supervised execution under the existing pause without an ordinary claim; this records source/proof completion, not semantic acceptance or interface approval. No batch implementation/test deletion, coordinator/control window, push or main merge.

## Context

Separate proof prerequisite of complete combined impact acceptance under WI-612. TC-147 requires crash boundaries, and TC-148 requires exclusion throughout the primary turn. Existing hook rejection and normal replay do not prove abrupt process death. Add real child-process abrupt exits immediately before and after atomic publication commit; preserve pending versus derived completion and no duplicate successor, stating any required explicit residue reconciliation rather than promising automatic recovery. Exercise held-slot writer exclusion at primary admission, judgment/review callback and pre-commit boundaries through the actual primary engine and publication. No production behavior, registry approval or batch code/test deletion. Record platform and fixture limits honestly. Done when these proofs and relevant primary tests pass, independent review and commit checks pass; the complete-scope reanchor waits for this work. Supervised while coordinator paused, no control window/push/main merge.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-153 [project-trajectory/scripts/intake.py;project-trajectory/scripts/primary_approval.py;project-trajectory/scripts/primary_publication.py;project-trajectory/scripts/primary_close.py;project-trajectory/scripts/spec_move.py;project-trajectory/scripts/publication_verify.py :: intake_after_merge/mint_gap_rows/parse_dispositions/next_wi_id/context_block;approval_projection/absorption_census/impact_census;derive_tree/publish;stage_primary_adjudication;move_spec;generated_table/generated_paths/run_bar] tests: (see TC-147) — The unified trunk-side intake mint + the context block + th…
- LLR-154 [project-trajectory/scripts/integrate.py;project-trajectory/scripts/primary_adjudication.py;project-trajectory/scripts/primary_publication.py :: integrate_one/_lane_bar_directives/_refresh_bar/_dispatch_lock/_slot;run;publish] tests: (see TC-148) — The merge slot's post-merge intake arm
- TC-147 -> tests/test_intake.py; tests/test_primary_approval.py; tests/test_primary_publication.py
- TC-148 -> tests/test_integrate_station.py; tests/test_dispatch.py; tests/test_primary_adjudication.py
- TC-158 -> tests/test_id_watermark.py::test_the_rules_are_actually_WIRED_INTO_the_integrity_floor; tests/test_id_watermark.py::test_the_mint_does_not_reissue_a_deleted_id

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-123 scripts/baseline_snapshot <- scripts/intake;scripts/primary_adjudication;scripts/primary_publication;scripts/primary_turn: call copy_live, load_all, rows_for, exists, stamp, is_drifted, unanchored_findings
