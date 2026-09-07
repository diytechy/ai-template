+++
id = "WI-608"
title = "Apply the reviewed PC single-WI contract amendments"
workstream = "process"
sr_refs = ["SR-144", "SR-148", "SR-156"]
specref = "docs/ai-template-redesign-2026-09-05-codex/PC-BATCH-CONTRACT.md"
buildtier = "strong"
safety_class = "spine"
+++

## Context

Owner-authorized PC continuation from 14ac5251. Apply the exact reviewed PC-BATCH-AMENDMENTS.patch as exclusive spine authoring, rechecking current cells and the correction-verification hashes first. Preserve every Status, parent, evidence, phase and perspective field. The patch file is a proposal, not an already applied amendment. No snapshot write, batch-code deletion or test deletion belongs to this authoring WI.

At authoring close, normal amendment intake must reuse WI-601 for the cumulative final LLR-061 text; do not mint a second owner. The remaining proposed rows belong to the future PC amendment adjudication, whose hard predecessor must name WI-601 and whose TC-061 acceptance depends on that exact final LLR-061 judgment. Recheck all queued ownership, including SR-144/LLR-152 cumulative prior drift. If ordinary automatic intake proposes an overlapping scope, reconcile it explicitly before binding any primary turn. A new patch revision requires independent review; the existing conditional opinion covers only the recorded exact corrections.

Done when the exact source amendments are committed through normal exclusive authoring with unchanged approval baselines, strict trace/commit checks pass, and the resulting amendment owners and hard dependency are recorded without duplication. No claim of implementation verification or live semantic acceptance. Preserve the coordinator pause, no new control window, no push and no merge to main. Before starting any adjudication, resolve the publication-composition preflight conflict recorded alongside this intake; more authoring does not remove it.

The current intake._amendment_drafts derives ONE amendment WI per merge, not per row. Its derived scope initially includes every amended row, including LLR-061; reconcile that proposed overlap through reviewed intake before any selection, preserving WI-601 as the sole owner. Applying the patch increases the whole-file drift population: WI-601 remains inadmissible afterward while composition is unresolved.

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
