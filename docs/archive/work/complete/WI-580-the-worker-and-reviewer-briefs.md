+++
id = "WI-580"
title = "The worker and reviewer briefs: batch assignment block, one-turn close bar, rows under review, scratch home"
workstream = "process"
needs = ["~WI-579"]
specref = ""
buildtier = "medium"
priority = 8
safety_class = "ordinary"
supersedes = "WI-559;WI-560;WI-562"
+++

## Deliverable

Both shipped briefs now say what is true of the lane they are sent to.

`worker.template.md` gained a fifth computed block, `{assignment_block}`
(`agent_loop.assignment_block`): on a lane claimed with more than one row it
lists EVERY assigned row — id, title, SpecRef — tagged `this session's focus` /
`built` / `started, not closed` / `not started` off `lane_completion`, the one
home of the completion predicate `current_assignment_wi` walks on (a committed
`WI:` trailer AND the spec gone from `active/<branch>/`), so the brief can never
call a row the walk will return to `built`; on a one-row lane it renders
NOTHING, so
the single-row brief is unchanged by the mechanism. The opening sentence no
longer asserts "ONE work item", which was false for a batch and is how a
session took WI-569 without ever learning WI-575 was on its lane; the
work-only-the-assignment rule follows it. The close ritual now names a bar a
worker can finish in one turn — the commit bar, with the full unfiltered suite
left to the lane's refresh inside the merge slot — names an AMENDMENT of an
already-approved cell alongside a mint as staling the approval brief, and names
the scratch home.

`reviewer.template.md` gained `{wis}` (`agent_loop.reviewed_rows_block`): the
rows under review, id + title, so a round maps Done-when items to coverage
instead of inferring scope from the diff. It renders even with no assignment (a
sentence saying so, never a literal slot in a sent brief), and an operator
override without the slot renders unchanged.

`LLR-061` amended in-lane (detail + `code_symbol`, `Status` untouched); the
module-size baseline for `agent_loop.py` bumped +36 with its reason;
`prompts/CATALOG.md` regenerated. Five new tests, each driven red on the
pre-change behaviour.

## Context

Minted by the owner-directed backlog restructure of 2026-09-02 (plan of record `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.2; executed out of band as a hand trunk commit series, not by a lane). The absorbed rows are archived under `docs/archive/work/restructured/` with their scope text untouched; their Done-when blocks are QUOTED below under their old ids and remain the spec this row must satisfy — decompose, don't paraphrase.

**Why one row.** Three absorbed items each add a line or a block to
`project-trajectory/prompts/worker.template.md`, and the batch finding below
adds a fourth. One lane, one reviewed diff of the template, instead of three
lanes for one file.

**The batch finding (plan §0; measured on lane
`wi-569-wi-508-spine-reseal-one-clean`, 2026-09-02).** The dispatcher admits a
spine batch as ONE lane with `--wi 'A;B'`, and `agent_loop.current_assignment_wi`
correctly walks the assignment one row per session. But
`agent_loop.worker_prompt(root, wi_rows, wi, train, base, ...)` renders ONE row,
and the template opens "You are assigned ONE work item on ONE claimed branch;
this assignment is your whole scope" — false for a batch. The session that took
WI-569 never learned WI-575 existed on its lane; the human saw `wi=WI-569;WI-575`
in the launch banner and the model saw one row. The reviewer brief
(`reviewer.template.md`) names NO work item at all and judges the whole train
diff without being told which rows it covers.

## Done-when

1. WI-559 Done-when 1 below (the one-turn close bar), as written.
2. `worker_prompt` takes the whole assignment: a new `{assignment_block}` slot
   lists EVERY assigned row (id, title, SpecRef) with its evidence state
   (`built` / `this session's focus` / `not started`), and the opening
   sentence states the truth for both a single row and a batch. The single-row
   render is byte-identical to today's except for that sentence (test).
3. `reviewer_prompt` gains a `{wis}` slot naming the rows under review (id +
   title), so a round can map Done-when items to coverage instead of inferring
   scope from the diff (an operator override without the slot still renders).
4. WI-560 Done-when 2 below: the worker brief names the approval-brief
   regeneration for a lane that AMENDS an approved cell, not only one that
   mints or re-statuses.
5. WI-562 Done-when 2 below: the worker brief names the scratch home in one
   line.
6. Tests: a two-id assignment renders both rows with the right focus; the
   reviewer brief names its rows; `prompts/CATALOG.md` regenerated
   (`gen_prompt_catalog.py`); full suite green.

### From WI-559 (Done-when 1 and 3, verbatim — item 2 went to WI-579; item 3 is shared)

1. The close ritual names a bar a worker can complete in ONE turn: the
   commit bar (smoke + budget + docs) at close, with the full unfiltered
   suite run by the lane's refresh inside the slot (which already runs the
   declared bar outside any session's turn) or a declared batched form. A
   close instruction that cannot execute in one turn is treated as the
   stall generator it measurably is.
3. Tests drive the false-partial class (built-and-verified lane, long
   suite) and the adjudicate round scheduling on a scaffold.

### From WI-560 (Done-when 2 and 4, verbatim — item 4 is shared with WI-579 and WI-581)

2. The worker brief names the approval-brief regeneration for a lane that
   AMENDS an approved cell, not only one that mints or re-statuses.
4. Tests drive all three.

### From WI-562 (Done-when 2, verbatim)

2. The worker brief names the scratch home in one line, so a session's
   temporary files land where the unload expects nothing.
