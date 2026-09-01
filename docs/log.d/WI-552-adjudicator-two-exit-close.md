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

- **Arm 2 (the OI-mint arm) — DONE.** A disposition draft carries a new
  `open_item` key (the human question). At the mint, `intake._mint_open_item`
  appends a `pending` OI row to open-items.toml (id from `next_oi_id`, the same
  watermark read-and-bump as WI ids), and the OI id is injected into the
  successor's `needs` BEFORE the row is written — so the ruling gates the
  successor's readiness. `open-items.html` regenerates in the mint's bookkeeping
  commit (`trunk_step --regen` runs `gen_open_items`). Refuses on a non-TOML
  registry (all-or-nothing). Also fixed `gen_trajectory`'s `validate` call to
  pass `known_ois` (it validates the WI graph during regen). Tests: OI minted
  pending + gates successor; non-TOML refusal.

- **Arm 3 (refusal invariant) — DONE.** Enforced in TWO places: (i)
  `intake._disposition_drafts` at merge — a `disposition`-brief adjudication row
  that merged with an empty `## Dispositions` section is refused (the merge
  stands, the mint refuses, the run stops); (ii) `handback.close_adjudication`
  at the mechanical close — refuses before the spec moves terminal. An OI alone
  no longer discharges it; no third exit. Tests at both levels.
- **Arm 1 (mechanical adjudication close) — DONE.** `handback.close_adjudication`
  moves a DONE adjudication row's spec to `complete/` (inserting a valid
  `## Deliverable`, clearing `specref`, preserving `## Context`/`## Dispositions`
  so the merge mints), commits with the WI trailer; no-ops for a
  non-adjudication lane; refuses a successor-less disposition. Wired into
  `dispatch._advance`'s EXIT_DONE path: a DONE adjudication row whose specs are
  still in active/ is closed mechanically instead of resumed forever (the C6
  loop OI-70 measured). The agent self-close path still works (finished_branches
  short-circuits). Tests: archives-terminal + finishes, mints the successor at
  merge, refusal invariant, non-adjudication no-op; updated the shared
  `then_closing` dispatch stub to draft a conformant successor.

- **Arm 7 (brief contract text) — DONE.** `adjudicate-disposition.template.md`:
  the successor is mandatory (OI-73); the new `open_item` key mints a pending OI
  the successor depends on; the machinery performs the close (the manual
  self-close instruction is gone); a successor-less disposition is refused.
  `PROCESS_OPTIONS.md` Predecessors prose widened tolerantly for the typed hard
  `OI-###` edge (+342, flagged; byte-budget-guard SKILL.md re-stamped, all three
  copies). `prompts/CATALOG.md` regenerated.

### Baselines / hygiene

- Broke the `check_trajectory -> trace` import cycle my first cut introduced
  (read open-items via `spine_carrier` directly in `load_known_ois`).
- Decomposed the three functions the C901 ratchet flagged
  (`_mint`, `validate`, `_advance`) back under threshold — no complexity-baseline
  bump. Reviewed SLOC restamp for `check_trajectory`/`intake`/`integrate`
  (legitimate feature growth).
- At close: ran `ruff format` over the WI's own touched files (six had
  non-canonical blank-line spacing the earlier commits left); re-stamped the
  module-size baseline ±2 for `intake.py` (1174 -> 1176) and
  `check_trajectory.py` (2247 -> 2245) — format-only, no executable change.

### Bar

- Smoke tier: 1429 passed / 8 skipped, 23.1s wall vs 60s budget (within).
- Full unfiltered suite: run at close (see the close commit).
- No spine rows minted or re-statused, so no approval brief regeneration owed.

### Outcome

All seven Done-when arms delivered and tested. Smoke tier green within budget
(1429 passed / 8 skipped, 22.2s wall; budget check 23.3s vs 60s). Full
unfiltered suite green at close. No spine rows minted or re-statused, so no
approval brief regeneration owed. Closing COMPLETE.

### REVIEW-A rework (005 CHANGES-REQUESTED, 3 findings)

REVIEW-A found the refusal invariant gated on `brief == "disposition"`, but a
CANCELLED original close mints a brief-LESS adjudication row (its brief is
omitted so `agent_loop` gives it the ordinary assignment rather than holding it
for a report the close never owed). So neither guard fired for a cancelled
close that queued no successor — it archived/merged silently, contradicting
OI-73, Done-when 3 and the shipped contract text. Two MINORs: the scheduler's
dead-edge reason omitted `partial` (Done-when 6 made it terminal too), and a
stale `_OI_PENDING` comment clause.

- **MAJOR (cancelled-close refusal gap) — FIXED.** The signal is now the
  durable `dispose:` TITLE prefix the two early-close arms share, read by a new
  single-sourced `intake.owes_successor(meta)` + `_DISPOSITION_TITLE_PREFIX`
  (the two title builders now reference the constant). Both guards
  (`intake._disposition_drafts` at merge, `handback.close_adjudication` at the
  close) refuse when the row owes a successor and none was drafted; the
  clean-close spot check (`spot-check …`), the amendment (`adjudicate: …`) and
  the census rows do NOT carry the prefix and owe none. WHY TITLE, not specref
  or brief: `brief == "disposition"` is set only on the partial arm (cancelled
  is brief-LESS by design); `specref` names the outcome but the close CLEARS it
  (`_adjudication_close_text`) — and the merge-side guard is the PRIMARY
  enforcement for the cancelled case, because a cancelled row is dispatched as
  an ordinary worker that SELF-closes past `close_adjudication`
  (`dispatch._close_done_adjudication` short-circuits on a finished branch), so
  by merge time specref is already gone. The title is the one signal that both
  survives the close AND distinguishes the arms. Tests: a cancelled close with
  no successor is refused at BOTH guards (`test_intake` models the self-close
  with specref CLEARED; `test_handback`), plus the brief-less cancelled row that
  DID queue a successor still closes (no over-fire). DW7's contract prose is now
  accurate — the machinery it described covers cancelled.
- **MINOR (scheduler/validator disagree on partial) — FIXED.**
  `schedule._waiting_reasons` now emits `waiting:hard-pred-partial:<ids>`
  alongside `waiting:hard-pred-cancelled`, so `--explain` and the validator's
  `dead_dependency_findings` (which flags cancelled AND partial) agree an edge
  is dead. Test added.
- **MINOR (stale `_OI_PENDING` comment) — FIXED.** Dropped the "or the row
  simply gone … satisfies the edge" clause that contradicted the code (a gone/
  absent OI fails closed); the comment now matches `_oi_satisfied`.
- Baseline: `intake.py` re-stamped 1176 → 1179 (+3, `owes_successor` +
  `_DISPOSITION_TITLE_PREFIX`; reviewed bump). No spine rows touched — no
  approval brief owed.

### REVIEW-A (009) rework — the un-restamped ratchet left the smoke bar red

- **BLOCKER (per-commit bar red) — FIXED.** After the +3 bump above, a later
  ruff/format pass (blank-line normalization) shrank `intake.py` to 1177 SLOC
  without the ratchet being re-stamped in the same commit. Because
  `test_module_size_ratchet` compares `check_complexity.module_sloc` exact-
  equality in BOTH directions, the committed 1179 baseline vs the measured 1177
  failed under `-m smoke` on the clean tree — so the per-commit bar was red and
  the Deliverable's "smoke tier green" claim was false. Re-stamped the
  `intake.py` entry **1179 → 1177 (RE-STAMPED DOWN -2)** with the reason inline,
  per this file's record-the-drop-in-the-same-commit rule. Re-ran the bar:
  `pytest -q -n auto -m smoke` → 1430 passed, 8 skipped in 20.9s;
  `check_smoke_budget.py --mode enforce` → 20.9s vs 60s within. No executable
  line changed — a test baseline only.

### Surfaced (not fixed here): dormant cognitive-complexity baseline drift

- The `docs/complexity-baseline` cognitive census (`check_complexity.py --mode
  enforce`, `[step:complexity]`) has drifted against this branch's reviewed code:
  tightenings `check_trajectory.load_wis 23→17` / `validate 24→20` and removals
  `intake._mint 21→∅` / `schedule.load_wis 17→∅`, plus growths/new rows
  `dispatch._advance 16→20`, `intake._disposition_drafts 21→25`,
  `handback.close_adjudication ∅→16`, `intake._replace_inbound_edges ∅→18`.
  This is **not** fixed in this WI and does **not** gate it: `[step:complexity]`
  is `from-stage = DevStg-Impl` and the repo's effective `stage = DevStg-LLReqs`,
  so the sensor is dormant — the norm since WI-538 armed it is that
  script-touching branches do not re-stamp while dormant (no WI has). Recorded
  here so the DevStg-Impl transition re-stamps the tightenings/removals and takes
  the reviewed bumps (code already APPROVE'd at REVIEW-A 007) with reasons, per
  the stack.ini escape hatch. The SLOC module-size ratchet above (smoke tier) is
  a separate sensor and is green.
