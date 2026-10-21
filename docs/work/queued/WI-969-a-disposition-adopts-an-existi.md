+++
id = "WI-969"
title = "A disposition adopts an existing successor: the record-at-close rebuild, its plan revised for sitting 016's FIX"
workstream = "process"
sr_refs = ["SR-148", "SR-220"]
specref = "docs/work/partial/WI-902-disposition-adopts-existing-successor.md"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
planmode = "single"
supersedes = "WI-902"
+++

## Context

Drafted by WI-953 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Advisory registry joins (WI-388; never gating):

### Cancelled precedent on the same SRs (do not re-propose the refuted)
- WI-810 (cancelled) MINT in the lane: one allocator, the consumption list and station lan… — reason: CANCELLED (owner, 2026-10-20; coordinator-2026-10-20 D-009): split, then cancelled. Its one bullet still owed, a settled amendment is never minted, is WI-963. …

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
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
