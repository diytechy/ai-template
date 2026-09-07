+++
id = "WI-621"
title = "Complete exact carrier refusal and read-only replay proofs"
workstream = "process"
sr_refs = ["SR-156", "SR-174"]
needs = ["WI-619", "WI-622"]
buildtier = "strong"
safety_class = "spine"
+++

## Deliverable

Extended actual publication fixtures with named carrier refusal classes and byte-exact cold primary-state preservation for scoped and required-bar replay. Added the reachable status-refusal regression. Source, proof mapping, actual validation and independent source review are recorded in docs/reviews/wi620-authoring/. Supervised execution under the existing pause without an ordinary claim; this records source/proof completion, not semantic acceptance. No registry Status change, accepted snapshot, batch deletion, control window, push or main merge.

## Context

Separately scoped verification prerequisite of WI-620, required by the published WI-619 RETURN R3/R4. Extend real publication fixtures to exercise the named TC-205 carrier refusal classes with unrelated conditions valid; map directly driven cases and any inference through TC-147 construction explicitly. Verify cold carrier recognition preserves primary refs, index, worktree, objects and FETCH_HEAD, including required-bar replay in the disposable checkout. Preserve the existing obligations and fixture-versus-real-review distinction. Inspect the recorded SystemExit limit rather than adding speculative guards. This test-work scope changes no production behavior, registry Status, accepted snapshot, or batch implementation/test. Done when focused publication/approval/primary tests, independent source review, smoke budget and strict repository checks pass, and WI-620's full-scope reanchor waits for this completed proof prerequisite. Supervised work while the coordinator remains paused; no ordinary claim, control window, push or main merge.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-138 [project-trajectory/scripts/agent_common.py :: tracked_pause/pause_reason] tests: (see TC-131) — Tracked pause reader (dual-home)
- LLR-140 [project-trajectory/scripts/integrate.py;project-trajectory/scripts/primary_adjudication.py;project-trajectory/scripts/primary_publication.py :: claim/finished_branches/_verdict_gate/integrate_one/audit;pending/begin/run/completion_refusal;derive_tree/publish/publication_commit] tests: (see TC-132) — Local integrator (claim + queue + audit)
- LLR-145 [project-trajectory/scripts/spec_move.py :: move_spec/expected_relink/archive_dest] tests: (see TC-139) — Link-aware spec-move ritual (move + relink indivisible)
- LLR-150 [project-trajectory/scripts/lane.py :: ensure_worktree/worker_argv/spawn_worker/run_worker/spawn_refresh] tests: (see TC-144) — Lane mechanics: worktree, worker subprocess, §A2 refresh su…
- LLR-151 [project-trajectory/scripts/integrate.py :: _dispatch_lock/claim/_claim_refusal/_abandoned_claim] tests: (see TC-145) — Dispatch-lock ownership and single-WI claim
- LLR-153 [project-trajectory/scripts/intake.py;project-trajectory/scripts/primary_approval.py;project-trajectory/scripts/primary_publication.py;project-trajectory/scripts/primary_close.py;project-trajectory/scripts/spec_move.py;project-trajectory/scripts/publication_verify.py :: intake_after_merge/mint_gap_rows/parse_dispositions/next_wi_id/context_block;approval_projection/absorption_census/impact_census;derive_tree/publish;stage_primary_adjudication;move_spec;run/branch_tree_script/passed_steps/run_bar/generated_table/generated_paths/ADJUDICATION_SURFACES] tests: (see TC-147) — The unified trunk-side intake mint + the context block + th…

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
