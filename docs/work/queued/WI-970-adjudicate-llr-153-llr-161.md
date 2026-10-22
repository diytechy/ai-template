+++
id = "WI-970"
title = "adjudicate: LLR-153, LLR-161, LLR-312, SR-148, TC-147, TC-156, TC-254 - approved/routed cell(s) amended on merged trunk 8c03d50..802f723 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-148"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-153", "LLR-161", "LLR-312", "SR-148", "TC-147", "TC-156", "TC-254"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-148 `AcceptanceCriteria`: 'A ready adjudication row admits ahead of every other class, the ruled rank table unchanged (--explain still reports it)…' -> 'A ready adjudication row admits ahead of every other class, the ruled rank table unchanged (--explain still reports it)…'
- LLR-153 `Detail`: 'The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id count…' -> 'The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id count…'
- LLR-161 `Detail`: "`close_partial` writes the report FIRST (it is the event's identity), refuses when one already exists, and restores EVE…" -> "`close_partial` writes the report FIRST (it is the event's identity), refuses when one already exists, and restores EVE…"
- LLR-312 `Detail`: 'The consolidation close resolves and validates every affected queued specification before its first write. It plans one…' -> 'The consolidation close resolves and validates every affected queued specification before its first write. It plans one…'
- TC-147 `Expected`: 'Satisfies SR-174 AcceptanceCriteria via the LLR-153 detail contract' -> 'Satisfies SR-174 AcceptanceCriteria via the LLR-153 detail contract; an adopts-only block allocates no id, title identi…'
- TC-147 `Method`: "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…" -> "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…"
- TC-147 `Verifies`: 'SR-174;SR-228;LLR-153;IF-091' -> 'SR-174;SR-228;SR-148;LLR-153;IF-091'
- TC-156 `Expected`: 'Satisfies SR-144 AcceptanceCriteria via the LLR-161 detail contract' -> 'Satisfies SR-144 AcceptanceCriteria via the LLR-161 detail contract; the disposition may adopt the already-open work it…'
- TC-156 `Method`: 'Run the handback suite over real git worktrees: a partial close is clean under the REAL trajectory check (not a stub), …' -> 'Run the handback suite over real git worktrees: a partial close is clean under the REAL trajectory check (not a stub), …'
- TC-156 `Verifies`: 'SR-144;LLR-161' -> 'SR-144;SR-148;LLR-161'
- TC-254 `Method`: 'Driven on real git repositories and lanes, in a module registered as slow: a queue with an overlapping cluster mints ex…' -> 'Driven on real git repositories and lanes, in a module registered as slow: a queue with an overlapping cluster mints ex…'
- TC-254 `Verifies`: 'SR-220;LLR-210;LLR-312' -> 'SR-220;SR-148;LLR-210;LLR-312'

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
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;external:downstream adopter: file sections: attestation, policies, checks, build; one key = value per line
- IF-163 docs/status.md -> scripts/agent_common;scripts/check_docs;scripts/check_trajectory;scripts/gen_okf;scripts/integrate;scripts/trunk_step: file the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between the markers is its w…
