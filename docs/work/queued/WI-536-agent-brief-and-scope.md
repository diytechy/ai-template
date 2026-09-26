+++
id = "WI-536"
title = "Agent-brief and scope: the knowledge-pack review's six byte-paid edits and two kit findings"
specref = "docs/plans/2026-08-29-knowledge-pack-review-synthesis.md#3-ranked-distillation-backlog"
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

The knowledge-pack review's third plan folder, agent-brief-and-scope (specref
§5 item 3), scoped as the title says: the small byte-paid edits of §3's ranks
4, 5, 6, 7, 13 and 14, and the two kit findings §6 files separately. §3 states
each item in full.

IN SCOPE:

- rank 4, the partial-search rule: one `AGENTS.template.md` bullet, paid for by
  tightening another, because the file is capped;
- rank 5, a `subagent-brief` skill (`scope: kit`): the seven-part brief
  contract, with the six-section return contract folded in;
- rank 6, the receipt doctrine and the fresh-context restatement test in the
  `spine-authoring` skill body, plus one sentence of mechanism in PROCESS.md §3;
- rank 7, the spec-determinacy `BuildTier` discriminator and the
  inline-versus-dispatch conditions, in PROCESS_OPTIONS.md "Per-WI build tier"
  and PROCESS.md §6;
- rank 13, a description-length floor in `gen_skills_index.py --check`;
- rank 14, one guardrail payload per model substring through the existing
  `[policies] guardrails` matcher, naming no model in kit-owned text;
- §6's finding B5: bootstrap a two-file skill to confirm whether
  `bootstrap.materialize_agent_layer` scaffolds only `SKILL.md` while
  `gen_skills_index.check_agent_sync` compares every file, then fix it or
  document the limit in `skills/README.md`;
- §6's `EXTERNAL_SKILLS.md` finding: the `anthropics/skills` row calls that
  repo's skills orthogonal task tools, but `frontend-design` is a
  design-quality skill.

NOT IN SCOPE: the folder's other two entries (the delta-versus-ask reverting
pass, which §3 routes to a plan with a kill criterion, and Q1 on write-surface
maps), and every other §3 rank.

## Done-when

- `AGENTS.template.md` carries the partial-search rule as one bullet and is
  still within its byte cap; each capped or watched doc touched has its byte
  delta reported and its row re-stamped.
- The `subagent-brief` skill ships with `scope: kit`, `INDEX.csv` is
  regenerated, and `gen_skills_index.py --check` passes.
- The `spine-authoring` skill states the receipt doctrine and the restatement
  test, PROCESS.md §3 carries the one-sentence mechanism, and the build-tier
  discriminator and inline-versus-dispatch conditions are in the two sections
  rank 7 names.
- `gen_skills_index.py --check` refuses a description under the floor, and a
  guardrail payload is selected by model substring; a test pins each.
- A two-file skill has been bootstrapped into a scaffold and the finding closed
  either way (fixed with a test, or the limit stated in `skills/README.md`), the
  `anthropics/skills` row is corrected, and the commit bar passes.
