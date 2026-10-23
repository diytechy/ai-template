## 2026-10-22 — headless leg 13: WI-961 through its counted rounds

Loop session `20261021T045653Z-213020`, leg 13. The coordinator took the
lease and worked the handoff's queue from its first row.

- **WI-961** (Claude coordinator sessions and their sub-agents recorded
  from their transcripts). Claimed alone under one scoped unpause; its
  2026-10-20 scope critique and confirming round stood (coordinator-2026-10-22
  D-001).
  - **The plan.** A fresh Claude Opus planner surveyed the box's
    transcripts read-only: usage repeats across a message's records, and
    the last record carries the count. Critique 1 (Codex Sol) raised two
    MAJORs: a message still being written was passed by the cursor, and
    two contributions could collide on one log name. One revision added a
    finality boundary and moved a log's stamp past the invocation's
    earlier stamps. Critique 2, in convergence stance, raised one MAJOR:
    a kill inside the shared writer's write. The cap routed it to dispute
    sitting 002, which ruled DISMISS out-of-scope, and the pass record
    followed (wi-961 D-001).
  - **P0's probes** (D-002, D-003):
    - a `--resume` and a `SendMessage` both append to the same transcript
      file;
    - a `claude -p` result's usage excludes its sub-agents;
    - a depth-3 agent exists;
    - the survey confirmed the finality premises over 186,577 assistant
      records.
  - **The build.**
    - Terra's intent turn drafted SR-244, LLR-347 to LLR-356, TC-386 to
      TC-395 and IF-305, which rode the test commit (D-004).
    - 49 tests went in as strict expected failures, each red at its own
      assertion.
    - The code made them pass.
  - **Round 1.** Both reviewers returned CHANGES-REQUESTED.
    - Sol's MAJOR: a finished agent's last hand-back message had no stop
      record and stayed uncounted.
    - Opus's MAJOR: the planned live run was missing. It was re-graded,
      because the plan puts it after the rounds (D-006).
    - The fix counts that message once a finish notice for the agent
      follows it: a task notification, or the spawner's tool result.
      Four regression tests were red before the fix (D-007).
  - **Round 2.** Both reviewers returned APPROVE with MINORs only (D-008).
  - **P8's live run** reproduced leg 3's figures exactly (D-009):
    - coordinator: 151,014 output and 33,486,394 cache read;
    - builders: 564,463 output;
    - Plan: 51,313 output.

    No prompt text appeared in any log, and a second run recorded only the
    new message.
  - **A consolidation stage** answered round 2's in-surface MINOR.
  - The lane is clean at `8566393ad`. The checkpoint comes next.
- Nothing landed and no trunk code changed, so the full suite did not run.
