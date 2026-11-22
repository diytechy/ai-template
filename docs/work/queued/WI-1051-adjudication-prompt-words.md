+++
id = "WI-1051"
title = "The adjudication prompts: the act names the repository's own scripts path, and first acceptance asks for ACCEPT"
workstream = "process"
sr_refs = ["SR-231"]
needs = []
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, from the two
automated adjudication sittings run by hand (WI-1047, WI-1049; queue-drill
HANDOFF §3.7). Two prompt templates say something other than what the code
reads:

- **The act brief names an adopter's path.**
  `project-trajectory/prompts/adjudicate-act.template.md` hard-codes
  `python scripts/intake.py snapshot ...` in its instructions (lines 65 and
  66) and in the commands `adjudicate_act.compose_act` fills. That is the
  path in a scaffolded repository; in this repository the script is
  `project-trajectory/scripts/intake.py`, so an act taken here exactly as
  the brief words it fails, and the coordinator substituted the path by
  hand at both sittings. The reviewer and worker templates already take a
  `{scripts}` placeholder (`scripts` in a scaffolded repository, the kit
  master's path here; `prompts/CATALOG.md`).
- **The first-acceptance brief asks for a word its grammar refuses.**
  `adjudicate-first-acceptance.template.md` line 106 says "`APPROVE` only
  when EVERY row you were shown is accepted", but the section's machine line
  takes `OUTCOME: ACCEPT rows=N` or `OUTCOME: RETURN rows=N`, and the
  verdict grammar knows no APPROVE. Both sittings had to tell the
  adjudicator in a preface to read ACCEPT there.

## Done-when

- [ ] The act template's commands name the repository's scripts directory
      through the same `{scripts}` value the reviewer and worker templates
      take, and `compose_act` fills it; a test shows the filled act naming
      `project-trajectory/scripts/intake.py` in this repository and
      `scripts/intake.py` in a scaffold.
- [ ] The first-acceptance template asks for `ACCEPT` where it says
      `APPROVE`, and a test reads every machine-line word a template asks
      for against its section's verdict grammar.
- [ ] `prompts/CATALOG.md`'s hashes and placeholder lists are regenerated.
