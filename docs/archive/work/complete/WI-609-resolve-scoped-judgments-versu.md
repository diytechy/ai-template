+++
id = "WI-609"
title = "Resolve scoped judgments versus whole-file snapshot publication"
workstream = "process"
sr_refs = ["SR-148", "SR-156"]
buildtier = "strong"
safety_class = "spine"
needs = ["OI-88"]
+++

## Deliverable

OI-88 authorizes the independently reviewed existing-publisher resolution in docs/reviews/wi-609-resolution/DECISION.md. Applied canonical intake/spec-move transfer to WI-610; original owners are restructured, not accepted or complete. Actual committed census matches proposed scope; exact lineage and fail-closed scope/absorption behavior are reviewed in docs/reviews/pc-transfer/. Existing primary approval/publication tests validate missing/stale/outside-authority refusals. The owner-authorized combined scope supersedes the earlier separate-owner composition requirement: there are no foreign judgments to compose. No runtime or publisher semantics changed. This supervised resolution close records an executable route and successor, not live acceptance, a claim, or a new control window.

## Context

Concrete PC preflight finding at 14ac5251: WI-601 owns only LLR-061. The actual LLR snapshot census also includes approved changes to LLR-140/152/153/154/158/167/183/207. With evidence validation assumed successful for diagnostic isolation, primary_approval._absorption_refusal still refuses LLR-140 without an accepted scoped decision; _decision_rows rejects adding that decision because it is outside WI-601's scope. No primary turn has started.

Scope: resolve the composition of independently scoped judgments with one whole-registry publication, starting from the existing carrier, policy and verifier rather than introducing another ledger. Preserve WI-601, WI-603 and WI-605 ownership and exact before/after plus committed reviewer/session provenance. Never widen a current turn, silently transfer ownership, classify changed meaning as equivalence, weaken the complete-absorption check, or copy a partially judged snapshot. Determine whether an existing valid publication route was missed before proposing a repair. Author any needed governing amendments first; actual approval remains a separate exclusive primary act.

Done when an independently reviewed concrete resolution states the minimal correct existing route or scoped implementation change, its governing contract impact, and executable acceptance cases: valid judgments from distinct owners compose; missing, stale, contradictory and outside-authority evidence refuse. The review must explain how separate owners can finish without circular snapshot dependencies and without weakening each original scope. File necessary implementation/adjudication continuations through normal intake; this WI does not itself approve its authored contracts.

This is a separate publication prerequisite discovered during PC, not authority to change runner behavior inside the batch-deletion package. Keep coordinator and primary selection paused while the conflict is unresolved. No control window, push, merge to main, snapshot write or batch deletion in this preparation.

Distinguish an existing valid judgment owned by another WI from a row with no completed judgment: the latter must remain unaccepted. Inventory all affected rows and reuse existing queued owners before proposing any new adjudication. Current explicit LLR owners are WI-601 for LLR-061, WI-603 for LLR-167 and WI-605 for LLR-183; LLR-152 belongs to the future PC amendment owner. The remaining LLR-140/153/154/158/207 have no explicit queued adjudicates owner in the checked baseline, which does not establish absence of historical judgments. Recheck the full SR/TC populations too. See docs/reviews/pc-intake/preflight.md for the actual diagnostic and the independent opinion, including corrected reviewer assumptions.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-058 [project-trajectory/scripts/schedule.py :: ready/frontier/evaluate] tests: (see TC-058) — WI-DAG frontier + deterministic traincar ordering
- LLR-059 [project-trajectory/scripts/schedule.py :: classify/safety_class] tests: (see TC-059) — Pure safety classifier
- LLR-060 [project-trajectory/scripts/trunk_step.py :: REGEN_STEPS/regen] tests: (see TC-060) — next-wi/run-phase retirement + generated status/run-state
- LLR-089 [project-trajectory/scripts/schedule.py :: kind_of/classify] tests: (see TC-091) — Structural safety cross-check
- LLR-123 [project-trajectory/scripts/schedule.py :: frontier/evaluate] tests: (see TC) — Deterministic traincar ordering
- LLR-131 [project-trajectory/scripts/schedule.py :: classify] tests: (see TC) — Contradiction-safe dual-plan class

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-010 scripts/gen_arch_map <- scripts/check;scripts/trunk_step: cli --doc | --cli-doc | --contracts-doc | --src | --mode | --check | --strict-parse | --backlink-coverage | --str…
- IF-150 scripts/gen_arch_map -> scripts/check;scripts/trunk_step: exit-code 0 current · 1 a stale target under --check, an unparseable module under --strict-parse, or coverage below the…
- IF-012 scripts/gen_okf -> scripts/check;scripts/trunk_step: exit-code 0 clean, vacuous or opted out · 1 stale, missing or extra bundle file under --check
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
- IF-164 scripts/traj_status -> scripts/agent_common;external:downstream adopter: file docs/status.md — the block between the GENERATED STATUS markers: derived stage, spine counts, the ready front…
