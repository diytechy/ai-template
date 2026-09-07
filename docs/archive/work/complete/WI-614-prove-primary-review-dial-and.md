+++
id = "WI-614"
title = "Prove primary review dial and shared evidence behavior"
workstream = "process"
sr_refs = ["SR-156", "SR-174"]
needs = ["WI-610", "WI-611", "WI-615"]
buildtier = "strong"
safety_class = "spine"
+++

## Deliverable

Added actual pending-primary dial/class matrix, committing ADJUDICATE scheduling and queued-to-terminal shared-evidence proofs; retained historical lane tests as lane proofs. Evidence, measured checks, obligation mapping and independent source review are recorded in docs/reviews/wi612-authoring/. Supervised execution under the existing pause without an ordinary claim; this records source/proof completion, not semantic acceptance or interface approval. No batch implementation/test deletion, coordinator/control window, push or main merge.

## Context

Separately scoped test-work prerequisite of WI-612 and its complete-scope primary reanchor, required by WI-610. Add actual pending-primary and verified-publication proofs of the adjudication review dial, committing ADJUDICATE review scheduling and shared scheduler/verdict-reader inputs. Exercise never/when-minting/always with ordinary versus spine or derived-dual drafts; verify no-review returns can publish, review-owed returns refuse until actual test-fixture independent evidence exists, and queued-to-terminal publication preserves the same review answer. Test with real primary selection/publication and Git fixture provenance, not a closed lane relabelled primary. Preserve the existing ordinary-lane tests and clarify which proof maps to each TC obligation. No production source or registry authoring, snapshot acceptance, weakening checks or batch-test deletion is authorized here. Done when the new proof cases pass with existing primary and verdict suites, independent source review and commit/strict checks pass, and the reanchor explicitly waits for this completed prerequisite. Supervised work while pause remains; no ordinary claim, control window, push or main merge.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-138 [project-trajectory/scripts/agent_common.py :: tracked_pause/pause_reason] tests: (see TC-131) — Tracked pause reader (dual-home)
- LLR-140 [project-trajectory/scripts/integrate.py;project-trajectory/scripts/primary_adjudication.py;project-trajectory/scripts/primary_publication.py :: claim/finished_branches/_verdict_gate/integrate_one/audit;pending/begin/run/completion_refusal;derive_tree/publish/publication_commit] tests: (see TC-132) — Local integrator (claim + queue + audit)
- LLR-145 [project-trajectory/scripts/spec_move.py :: move_spec/expected_relink/archive_dest] tests: (see TC-139) — Link-aware spec-move ritual (move + relink indivisible)
- LLR-150 [project-trajectory/scripts/lane.py :: ensure_worktree/worker_argv/spawn_worker/run_worker/spawn_refresh] tests: (see TC-144) — Lane mechanics: worktree, worker subprocess, §A2 refresh su…
- LLR-151 [project-trajectory/scripts/integrate.py :: _dispatch_lock/claim/_claim_refusal/_abandoned_claim] tests: (see TC-145) — Dispatch-lock ownership and single-WI claim
- LLR-153 [project-trajectory/scripts/intake.py;project-trajectory/scripts/primary_approval.py;project-trajectory/scripts/primary_publication.py :: intake_after_merge/mint_gap_rows/parse_dispositions/next_wi_id/context_block;approval_projection/absorption_census/impact_census;derive_tree/publish] tests: (see TC-147) — The unified trunk-side intake mint + the context block + th…

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
- IF-046 scripts/score_reviews <- scripts/agent_loop;scripts/integrate;scripts/gen_verdict_rollup;scripts/kitlib/verdict: call score_reviews.parse_verdict, substance, merge_verdict, fired_tripwires, record_round, latest_phase_verdicts; …
- IF-047 docs/reviews/ -> scripts/score_reviews;scripts/check_trajectory;scripts/integrate;scripts/kitlib/verdict;scripts/gen_verdict_rollup: file VERDICT: APPROVE | CHANGES-REQUESTED findings=N
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
