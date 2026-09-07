+++
id = "WI-613"
title = "Correct the verdict interface carrier attribution"
workstream = "process"
sr_refs = ["SR-156"]
needs = ["WI-610", "WI-611"]
buildtier = "strong"
safety_class = "spine"
+++

## Deliverable

Corrected IF-175 carrier attribution while retaining its Drafted status and existing first-approval owner. Evidence, measured checks, obligation mapping and independent source review are recorded in docs/reviews/wi612-authoring/. Supervised execution under the existing pause without an ordinary claim; this records source/proof completion, not semantic acceptance or interface approval. No batch implementation/test deletion, coordinator/control window, push or main merge.

## Context

Scoped counterpart-authoring prerequisite of WI-612 and its complete-scope primary reanchor, explicitly required by the published WI-610 RETURN. Correct IF-175.Notes attribution of both refresh and adjudication close as disposable: retain refresh-only disposal and explain verified primary-carrier mapping consistently with the reworked LLR-207 recognition contract. Preserve shared reader/bindings, phase-span roles, distinct read-only/reset traversals and all other interface semantics. IF-175 stays Drafted; retain its existing first-approval ownership and obtain any approval only through its applicable authority. This scope authorizes authoring only, no interface approval, accepted snapshot, new interface or wider IF-090/IF-091 meaning. Done when the exact counterpart change is independently reviewed with the complete WI-612 authoring packet, trace/docs/trajectory and commit checks pass, and the complete-scope reanchor has this explicit completed prerequisite. Supervised work while pause remains; no ordinary claim, control window, push or main merge.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-138 [project-trajectory/scripts/agent_common.py :: tracked_pause/pause_reason] tests: (see TC-131) — Tracked pause reader (dual-home)
- LLR-140 [project-trajectory/scripts/integrate.py;project-trajectory/scripts/primary_adjudication.py;project-trajectory/scripts/primary_publication.py :: claim/finished_branches/_verdict_gate/integrate_one/audit;pending/begin/run/completion_refusal;derive_tree/publish/publication_commit] tests: (see TC-132) — Local integrator (claim + queue + audit)
- LLR-145 [project-trajectory/scripts/spec_move.py :: move_spec/expected_relink/archive_dest] tests: (see TC-139) — Link-aware spec-move ritual (move + relink indivisible)
- LLR-150 [project-trajectory/scripts/lane.py :: ensure_worktree/worker_argv/spawn_worker/run_worker/spawn_refresh] tests: (see TC-144) — Lane mechanics: worktree, worker subprocess, §A2 refresh su…
- LLR-151 [project-trajectory/scripts/integrate.py :: _dispatch_lock/claim/_claim_refusal/_abandoned_claim] tests: (see TC-145) — Dispatch-lock ownership and single-WI claim
- LLR-207 [project-trajectory/scripts/kitlib/verdict.py;project-trajectory/scripts/primary_turn.py;project-trajectory/scripts/primary_approval.py;project-trajectory/scripts/primary_publication.py;project-trajectory/scripts/primary_close.py;project-trajectory/scripts/publication_verify.py :: RECORD_PREFIXES/fold_listing/tree_identity/refresh_subject/refresh_attestation/work_tip/governing_rev/governing_identity/format_trailer/parse_trailer/round_file/session_log/branch_paths/logged_rounds/round_entries/declared_phases/phases_owed/round_count/format_branch_trailer/branch_trailers;record_path/validate/validate_candidate;approval_projection/absorption_census/impact_census;derive_tree/publish/publication_commit/completed;stage_primary_adjudication;run/branch_tree_script/passed_steps/run_bar/generated_table/generated_paths/ADJUDICATION_SURFACES] tests: TC-205 — The verdict record: what carries a governing verdict, and w…

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
