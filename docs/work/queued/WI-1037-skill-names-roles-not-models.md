+++
id = "WI-1037"
title = "The coordinator-cycle skill names each role, never the model that fills it, which is a setting"
workstream = "docs"
sr_refs = []
needs = []
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md#33-the-second-round-raised-by-q1a-answered-2026-11-21"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-21 at the operator's direction (queue-drill
hand-off §3.3 N5). The operator: "The targeting LLM to run prose through and
spine authoring would just be configurable, I wouldn't expect a skill to be
touched."

Which model fills a coordinator role is a setting. `codex_call.py` resolves
each role to an enabled roster row (today `ROLE_ROUTES` maps `REVIEW-A` and
`CRITIQUE` to `OPENAI-SOL` and `AUTHOR` to `OPENAI-TERRA`, with `--route`
as the override). The models themselves are declared in `docs/agents.toml`.
WI-1033 moves the role defaults into `process.toml`. The skill text,
however, names the model where it means the role:

| File | "Terra" | "Sol" | Other model names |
|---|---|---|---|
| `skills/coordinator-cycle/SKILL.md` | 8 | 7 | 7 |
| `skills/coordinator-cycle/references/recipes.md` | 36 | 12 | 2 |
| `scripts/coordinator/README.md` | 4 | 2 | 0 |

The Roles table also states models and efforts that have since drifted: it
says Sol at medium, where this drill runs Sol at low. No other shipped
skill, prompt, `PROCESS.md`, `PROCESS_OPTIONS.md` or `AGENTS.template.md`
names these models. The skill is `scope: this-repo` and is copied
byte-equal into `.claude/skills/` and `.agents/skills/` (the skills-sync
check). It is not one of the byte-budget-guard's watched documents.

Settled here:

- **Roles in the text:** "the author" (the `AUTHOR` role), "the critic"
  (`CRITIQUE`), "the code reviewer" (`REVIEW-A`, `REVIEW-B`) and "the
  adjudicator". The Roles table names each role and says its model is the
  route the role resolves to, never a model or effort.
- **Observations stay, labelled.** A gotcha seen with one model (CRLF and
  cp1252 writes, the basetemp lock, compressed cells, reworded accepted
  phrases) keeps its evidence and says which model showed it and when, so
  it is checked again if the route changes.
- **No behaviour change.** File names such as
  `terra-spine-prompt.template.md`, the role ids and `codex_call.py` stay as
  they are. Renaming them is not this row's scope.

## Done-when

- [ ] The coordinator-cycle skill and `scripts/coordinator/README.md` name
      roles, not models, except in labelled observations. The Roles table
      points at the route setting.
- [ ] The three copies of the skill are byte-equal, and the skills index
      and skills-sync checks pass.
