## 2026-09-01 — WI-552: the adjudicator's two exits (adjudication-row close, successor mint, OI mint with refusal invariant, OI-70/OI-73)

Session claimed `WI-552` on branch `wi-552-adjudicator-two-exit-close`. SpecRef
`docs/requirements/open-items.toml#OI-70` (as refined by OI-73). The work owns
seven Done-when arms spanning the adjudication-row close, the OI-mint arm, the
refusal invariant, inbound-needs replacement, typed OI edges in `needs`, the
`dead_dependency_findings` partial-predecessor net, and the brief contract text.

### Design (the two exits, OI-73 posture)

The adjudicator's exits are realised through the `## Dispositions` section the
ADJUDICATE session drafts in its own spec, minted at merge by
`intake._disposition_drafts`. OI-73 refines OI-70: every partial/cancelled
close MUST queue a successor; a minted OI becomes a typed hard dependency of
that successor (not a standalone exit); the mint REPLACES the superseded row's
inbound hard edges; and `OI-###` ids become valid hard `needs` tokens.

Seven arms, built lower-risk foundation first.

### Progress

- Read the OI-70 / OI-73 rulings and the spec's seven Done-when; mapped the
  touched modules (handback, station, intake, adjudicate_brief, agent_loop,
  dispatch, schedule, check_trajectory, trace, gen_open_items).
- **Arm 5 (typed OI edges in `needs`) — DONE.** New `kitlib.spine.split_pred_edges`
  is the one home for the widened grammar: `(hard_wi, hard_oi, soft)`. Both
  loaders (`schedule.load_wis`, `check_trajectory.load_wis`) carry an `oi_preds`
  list, kept OUT of the WI graph (no acyclicity node, no downstream count).
  Scheduler readiness: `hard_preds_satisfied(wi, status, oi_status)` — an OI
  edge is satisfied once its row leaves `pending`, read from
  `schedule.load_oi_status` (wraps `trace.open_item_states`); new
  `waiting:open-item-pending:` reason code; `oi_status` threaded through
  `evaluate`/`frontier`/`simulate` and the four external callers (dispatch,
  integrate, traj_status, traj_panels). Validator: `validate(..., known_ois)`
  resolves an OI edge against the open-items registry (dangling → ERROR); new
  `check_trajectory.load_known_ois`. Shipped grammar prose widened tolerantly
  in `registries/work-items.template.csv`.
- **Arm 6 (`dead_dependency_findings` → partial) — DONE.** The finding now
  fires on `partial` predecessors too (the WI-541→WI-540 strand class), message
  reworded to "terminal WI(s)".
- Tests: OI scheduler readiness (pending/ruled/absent/mixed), validator
  existence + non-cycle, dead-dep partial case; updated the reworded cancelled
  assertion. `test_schedule`/`test_trajectory`/`test_dispatch`/
  `test_gen_trajectory` green.

- **Arm 4 (mint replaces inbound edges) — DONE.** `intake._replace_inbound_edges`
  re-points every OPEN row's HARD `needs` edge on a superseded row to the
  successor, in the same commit as the mint; soft edges and terminal rows'
  history left alone; surgical `needs`-line rewrite preserves each dependent's
  `## Context`/Deliverable. Wired into `_mint` per minted successor carrying
  `supersedes`. Test added.

### Still to build

- Arm 2: the OI-mint arm — a disposition draft can mint an OI row into
  open-items.toml (id from watermark OI space, `status="pending"`,
  `gen_open_items` regenerated same commit) and land that OI id in the queued
  successor's `needs`.
- Arm 3: the refusal invariant (OI-73) — a partial/cancelled disposition that
  queues NO successor is REFUSED at the close.
- Arm 1: mechanical adjudication-row close — a DONE adjudication session's row
  closes mechanically (drafts minted to queued/, row archived terminal) instead
  of relying on the agent's self-close (the C6 loop OI-70 measured).
- Arm 7: ADJUDICATE brief contract text matches the machinery; full suite.
