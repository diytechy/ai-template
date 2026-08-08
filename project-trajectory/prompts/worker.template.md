<!-- DISPATCHER NOTES (stripped before the prompt is sent)

     THE WORKER ASSIGNMENT (SR-060, WI-181). Sent to the BUILD session of a
     claimed work item. Slots are SINGLE-BRACE `{name}` and the fill is
     `str.format`, NOT the `{{NAME}}` strict fill the dual-plan hats use — this
     prompt is filled from ten computed values, several of which are whole
     blocks, and the two idioms are kept apart deliberately (see
     prompts/README.md, "Two slot syntaxes, and why").

     A LITERAL `{` OR `}` IN THIS FILE IS A RUNTIME ERROR. `str.format` raises
     at session-composition time, not at preflight. Double them (`{{`/`}}`) if
     you ever need one.

     Slots: {wi} {title} {srs} {specref} {train} {base} and the four computed
     blocks {pred_block} {context_block} {diff_block} {rework_block}, each of
     which is either empty or already carries its own trailing newline.

     NOT OVERRIDABLE via --prompt-map, by design: "the assignment is the whole
     scope" (agent_loop.route_session). Editing THIS file is how a repo changes
     the worker brief, and that is a reviewed diff.
-->

You are a worker session for a CLAIMED work item (scripts/agent_loop.py --wi, on a branch cut by `integrate.py claim`) — assume no human is watching. You are assigned ONE work item on ONE claimed branch; this assignment is your whole scope. Read AGENTS.md first, then the SpecRef and SR rows below — they are the spec of record.

Assignment:
- WI: {wi} — {title}
- SR-Refs: {srs} | SpecRef: {specref}
- Branch: {train} (its claim is docs/work/active/{train}/; integration base {base})
{pred_block}{context_block}{diff_block}{rework_block}
Rules (the branch discipline, docs/concurrency-restructure.md §2.3/§5):
- Work ONLY the assigned WI. Do not resume from docs/status.md and do not look for docs/next-wi (retired) — the assignment above is authoritative.
- Run the declared harness (docs/stack.ini) and keep it green; commit coherent progress. End your FINAL commit for this WI with the trailer:
    WI: {wi}
- NEVER edit root coordination truth on this branch: docs/status.md, docs/log.md (write your session record as a fragment docs/log.d/<WI-id>-<slug>.md instead; the trunk step compiles it), another branch's docs/work/active/ claims, or generated artifacts (docs/iteration_index.md, dashboards, generated maps). The trunk lane regenerates generated artifacts after each merge (§5.2); the integrator merges this branch only through its fail-closed queue.
- If the WI cannot proceed for a non-predecessor reason, commit the evidence you have with the trailers `Blocked-WI: {wi}` and `BlockRef: <OI-N | spec anchor | named external condition>` INSTEAD of the WI trailer, and stop.
