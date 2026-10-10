+++
id = "WI-882"
title = "The prompt catalogue covers composed prompt text, or records that it excludes it"
workstream = "process"
sr_refs = ["SR-146"]
specref = "project-trajectory/prompts/CATALOG.md"
needs = ["WI-854"]
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by the coordinator on 2026-10-10 from WI-854's amendment sitting
(`docs/reviews/wi-854/001-ADJUDICATE-8d43a5c.md`, its separate finding).
WI-854 moves the spine tier questions into one composed home,
`prompts/spine-questions.md`, which the first-approval and amendment briefs
read at render time. The freshness-gated catalogue `prompts/CATALOG.md` is
generated from `KIT_PROMPTS` and lists only the templates. An edit to the
home therefore moves no catalogued digest, and `gen_prompt_catalog.py
--check` stays green. Each session's rendered `prompt-sha` still changes, so
SR-146's per-session audit trail holds, and the adjudicator ruled that
SR-146's text needs no change.

The gap is the catalogue's coverage: its template rows no longer name every
source of a launched brief's static instruction text.

Landing order (scope critique, 2026-10-10): one deliverable, the catalogue
contract for the composed home, either way; its evidence lands with it.

## Trust

Applies only if the lane chooses to list the composed home: its content
then takes part in a freshness gate (`project-trajectory/PROCESS.md` §3,
"When a guard is owed"). The exclusion option adds no gate authority.

- **Producer:** `project-trajectory/scripts/gen_prompt_catalog.py`, which
  rewrites `project-trajectory/prompts/CATALOG.md` in place (an open for
  write, not a replace). An unreadable source exits non-zero before the
  write and leaves the previous catalogue; a write that fails part-way can
  leave a truncated one. Either way the check then reads it as stale.
- **Consumers** (found by grep): `project-trajectory/scripts/check.py` is
  the one executing reader: its freshness step runs
  `gen_prompt_catalog.py --check`. A human operator also reads the
  catalogue to join a session log's `prompt-sha` back to its template.
  `project-trajectory/scripts/agent_loop.py` only writes that log's
  template path and `prompt-sha`; it never reads the catalogue.
  `docs/stack.ini` only declares the catalogue as a generated output.
- **Ruling**, by input:
  - *The composed home* (a source): absent or unreadable fails generation
    and the freshness check. It is never listed as skipped or digested as
    empty. Its row binds to the home's exact bytes by digest, so any edit
    is stale until regenerated.
  - *The catalogue* (the generated file): absent, unreadable or malformed
    fails the freshness check in `check.py`, which blocks the commit. The
    operator's join is a reading aid and gates nothing.

## Done-when

- Either the catalogue lists the composed home by digest, freshness-gated
  like the templates, or the catalogue's rows (IF-098) record that composed
  fragments are excluded, as IF-100 already does for the dual-plan hats. The
  choice and its reason go in the lane's decisions record.
- If the home is listed, a test edits it and sees `gen_prompt_catalog.py
  --check` go red.
- Review bar: A (one cross-family REVIEW-A).
