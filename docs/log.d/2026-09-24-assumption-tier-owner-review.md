## 2026-09-24 — The owner's answers on the assumption-tier and sister plans, and a review pack for the next session

An attended owner session (2026-09-23/24) that turned both plans' open
questions into decisions, then prepared the next review. Documentation only:
no script, test, registry row or template changed.

**Owner decisions recorded** (each in its plan's decision table, with the
owner's words):

- **Assumption-tier plan §12.1:**
  - Q3, Q5, Q6, Q8, Q10 and Q11 were accepted as revised.
  - Q16, Q19 (`mediates`, no attendance mechanism), Q20 (activation in one
    commit, reconfirmed), Q22/Q25 (evidence as results; `max_age` floor 7 days)
    and Q24 were decided, as were Q23 and Q27 on conditions.
  - Q26 was ruled as row-level refusal in the snapshot refresh; Q28 draws
    hosted CI as an external party; Q29 reopens `accepted_risk` on triggers;
    Q30 adopts "enabling system" only; Q18 and the bundle rows were confirmed.
- **Sister plan §5:**
  - S1, S2, S7 (one consolidated, schema-neutral session service), S10, S12
    and S15 were decided, and S4 on a condition.
  - S9 became "verify, don't isolate", which withdrew S16 and S17.
  - S3, S5, S6, S8, S11, S13 and S14 were re-posed.

**Reviews.**

- **Sol review round 5** (a decisions check; the sister plan's round 4) found
  18 open points, all of which held. It corrected the stage-drop rule and the
  deselected-step count (three steps, `smoke` included, not two). It made C4
  one commit, gave S6/Q25 one freshness model, staged `max_age`, the S3
  provenance cell and a terminology package, enabled C5 here, and added
  Q28–Q30.
- **Sol cross-check of the review pack:** 13 findings, 12 applied (see the
  pack's cross-check record).

**Research for the next review.** Four read-only passes fed
`docs/plans/2026-09-24-owner-review-pack.md`:

- a GilbertCore adopter cross-check, which reopened Q6, Q16 and S4, and flagged
  S2;
- CLI token-usage research, with one live fixture per CLI;
- code facts for S9/S11 and for S3, S5, S6, S13, S14.

The pack also lists seven defects the research surfaced. The largest is
context occupancy: `agent_loop.py:3253` computes it from cumulative usage,
giving readings up to 34,836% in `docs/iteration_index.md`.

**Deviations.**

- The first Sol invocation failed because codex was not installed on this
  machine; `@openai/codex` 0.156.1 was installed globally with the owner's
  go-ahead, and was already signed in.
- The S8 research made one live call per CLI to capture usage fixtures, about
  $0.24 in total.
- Earlier plan sessions (2026-09-20 to 2026-09-23) wrote no log fragment; the
  plans carry their own review logs.

**Byte deltas on budgeted files:** none. No capped file was edited.

**Commit bar, on this machine.**

- Results: smoke **1681 passed, 3 skipped**.
- Seconds: **FAIL**. `check_smoke_budget.py --mode enforce` measured 242.8 s
  against the 60 s budget.
- Why: this box has 8 logical cores (the budget was measured on 24), and other
  codex and node sessions were running. The changes are documentation only and
  cannot move the tier's timing.
- Following the standing rule that one machine is one data point, the budget
  was not re-stamped; the over-budget reading is recorded here instead.
- `check_docs.py --root . --stale`: **OK**, 1470 docs, 0 broken links.

<!-- fig: cmd="python -m pytest -q -n auto -m smoke; python scripts/check_smoke_budget.py --mode enforce; python project-trajectory/scripts/check_docs.py --root . --stale" rev=c4d1d1ec -->

Deferred open items: none minted. The owner's pending decisions are gathered in
`docs/plans/2026-09-24-owner-review-pack.md`, which `docs/status.md` names as
where the next session starts. The seven defects in its Part C are not yet
filed as work items; that is the owner's call.
