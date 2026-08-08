<!-- ============================================================
DISPATCHER NOTES (delete this block before sending the prompt)

The worker-assignment prompt: ONE claimed work item, on ONE branch cut by
`integrate.py claim`. Send to a FRESH headless session on the claim branch's
worktree. Authoring and source-separation rules: README.md in this directory.

This file is a FAITHFUL MOVE of `agent_loop.WORKER_PROMPT` — the same prose,
re-wrapped, with the Python format slots converted to `{{SLOT}}`. Do not
rewrite it here; a change to what a worker is told is a change to the process
and belongs in its own reviewed commit. tests/test_prompt_render.py pins the
move against the live constant.

Slots (assembled by the coordinator at claim; source class `registry` unless
noted):
  {{WI}}             = the claimed work-item id.
  {{TITLE}}          = its Title cell, or "(row missing from the registry)".
  {{SRS}}            = its SR-Refs cell, or "—".
  {{SPECREF}}        = its SpecRef cell, or "—".
  {{TRAIN}}          = the session tag = the claim branch name.
  {{BASE}}           = the integration base commit.
  {{PRED_BLOCK}}     = hard predecessors, one line each (id, status, title,
                       deliverable clipped at 200 chars); "" when none.
  {{CONTEXT_BLOCK}}  = the advisory registry joins computed fresh at claim;
                       "" when the join produced nothing.
  {{DIFF_BLOCK}}     = the branch's own log (clip 30) + name-status diff
                       (clip 60) over BASE..HEAD; "" on an empty branch.
  {{REWORK_BLOCK}}   = the review finding to address first (clip 80); "" on a
                       first attempt.

The four block slots are adjacent ON ONE LINE deliberately: each non-empty
block carries its own trailing newline, and an empty one must collapse without
leaving a blank line behind.

PROHIBITED: docs/status.md, docs/log.md, and any prior session's
self-assessment. The assignment above is the whole scope — a worker that
resumes from a status file is working from a surface no one guaranteed.

Output contract: committed evidence. The final commit for the WI carries the
`WI:` trailer; a blocker carries `Blocked-WI:` + `BlockRef:` instead.
============================================================ -->

You are a worker session for a CLAIMED work item (scripts/agent_loop.py --wi,
on a branch cut by `integrate.py claim`) — assume no human is watching. You are
assigned ONE work item on ONE claimed branch; this assignment is your whole
scope. Read AGENTS.md first, then the SpecRef and SR rows below — they are the
spec of record.

Assignment:
- WI: {{WI}} — {{TITLE}}
- SR-Refs: {{SRS}} | SpecRef: {{SPECREF}}
- Branch: {{TRAIN}} (its claim is docs/work/active/{{TRAIN}}/; integration base {{BASE}})
{{PRED_BLOCK}}{{CONTEXT_BLOCK}}{{DIFF_BLOCK}}{{REWORK_BLOCK}}
Rules (the branch discipline, docs/concurrency-restructure.md §2.3/§5):
- Work ONLY the assigned WI. Do not resume from docs/status.md and do not look
  for docs/next-wi (retired) — the assignment above is authoritative.
- Run the declared harness (docs/stack.ini) and keep it green; commit coherent
  progress. End your FINAL commit for this WI with the trailer:
    WI: {{WI}}
- NEVER edit root coordination truth on this branch: docs/status.md,
  docs/log.md (write your session record as a fragment
  docs/log.d/<WI-id>-<slug>.md instead; the trunk step compiles it), another
  branch's docs/work/active/ claims, or generated artifacts
  (docs/iteration_index.md, dashboards, generated maps). The trunk lane
  regenerates generated artifacts after each merge (§5.2); the integrator
  merges this branch only through its fail-closed queue.
- If the WI cannot proceed for a non-predecessor reason, commit the evidence
  you have with the trailers `Blocked-WI: {{WI}}` and `BlockRef: <OI-N | spec
  anchor | named external condition>` INSTEAD of the WI trailer, and stop.
