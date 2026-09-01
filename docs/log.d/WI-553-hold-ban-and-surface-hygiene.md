## 2026-09-01 — WI-553: the hold ban mechanized (OI-70)

Mechanizing OI-70's ruling that hold-by-rename is BANNED — a lane closes or it
gets lost — plus the two dead surfaces that rode with the ruling and the
doctrine statement supervisors read. Four Done-when arms:

1. **Claim-ref check.** A harness-run check (warn-or-gate per the declared
   policy) reports every `docs/work/active/<branch>/` claim directory with no
   matching git branch ref — the rename-hold's exact signature (spec in
   `active/`, ref renamed away), the same scheduler/dispatcher disagreement the
   phantom-head finding names. Driven on a scaffold both ways.
2. **`blockref` hold vocabulary retired.** `pending.blocked_pending` reads
   `queued/` rows carrying a `blockref` frontmatter field and NOTHING produces
   one any more (LLR-161 removed the producers when `close_partial` began
   moving specs to terminal `partial/`). Retire the source, the `BlockRef`
   loader field, the `-000` example row, and the docs that teach it. **Kept,
   distinct:** the `Blocked-WI:`/`BlockRef:` COMMIT TRAILERS a worker uses to
   signal a block — a different instrument, still live.
3. **Fragment `none` cross-checked.** `gen_open_items.py` cross-checks a
   fragment's deferred-open-items declaration against the registry — a fragment
   claiming `none` while it should have deferred a row is contradicted, not
   merely presence-checked.
4. **Ban stated where supervisors read.** The session-protocol skill and the
   handback/ADJUDICATE docs name the sanctioned stop (the partial close; nothing
   else) and cite OI-70 as the ruling of record.

### Progress

- Read OI-70 (ruled 2026-08-31), the four Done-when arms, and the core surfaces
  (`pending.py`, `gen_open_items.py` deferral arms, `check_trajectory.load_wis`
  blockref field). Launched three mapping passes (blockref retirement surface,
  claim-ref check design, doctrine surfaces).
- **Done-when 1 (claim-ref check) LANDED.** `check_trajectory.holdbyrename_findings`
  reports every `docs/work/active/<branch>/` claim directory with no matching
  `refs/heads/<branch>` — the exact rename-hold / phantom-head signature. Same
  warn-plain / ERROR-under-`--strict` tier as R-E/R-F (silent off-git). Wired
  into `main()`. Tests `tests/test_trajectory_holdban.py` drive it both ways
  (matching ref: silent; renamed ref: named + gated), plus the empty-dir and
  off-git fail-soft edges. On the real tree it correctly names the wi508
  phantom head (WARN on this branch; tracked by WI-555). Tiered into
  `conftest.SLOW_MODULES` (git-scaffold subprocesses); `check_trajectory.py`
  SLOC baseline bumped 2245→2274.
- **Done-when 2 (blockref vocabulary retired) — code + tests LANDED.**
  - `pending.blocked_pending` (the owner-surface source with zero producers)
    removed, with its BLOCKED kind, wiring (`pending_items`/`owner_cards`/
    IF-088), the `traj_status`/`gen_trajectory` `_blocked_pending` re-exports,
    and the dispatcher's owner-surface docstrings.
  - The `blockref` FIELD retired from both loaders (`check_trajectory.load_wis`,
    `schedule.load_wis`), the canonical `kitlib.registry.WI_COLUMNS`+`SPEC_SCALARS`,
    `wi_convert`, `plan_artifacts`, and the shipped `work-items.template.csv`
    header. Its three derivation consumers gone: `schedule._disposition`'s
    blocked arm and `traj_views._wi_status`'s blocked derivation (and
    `blocked_pending`).
  - **Scope boundary (recorded):** `blocked` stays a WI-384 *lifecycle status
    word* — kept in `OPEN_STATUSES`/`BACKLOG_STALE_STATUSES`/`STATUS_GLYPH`/
    `STATUS_BUCKET` as defensive vocabulary — because OI-70 retires the blockref
    *mechanism*, not the status model. With the mechanism gone `blocked` has no
    current producer; the two `traj_views` render tests that produced a blocked
    WI *via* blockref drop that case (5→6 producible statuses still covered).
  - Stale comments that implied a live blockref producer corrected
    (`integrate`, `agent_loop`, `adjudicate_brief`, `dispatch`): a handback now
    moves specs to the TERMINAL `partial/`, read as `partial`, not queued+blockref.
  - Tests updated: `test_gen_trajectory_pending` (spine cards in place of a
    blocked WI), `test_schedule`, `test_traj_views`, `test_handback`,
    `test_intake`, `test_wi_folder_loaders` (retired blocked test removed),
    `test_plan_artifacts`/`test_wi_convert` (header pinning), `conftest`
    + `traj_fixtures` + the `SR_WI_COLUMNS` fixtures. `test_dispatch` banner
    reworked to a Drafted-SR card. SLOC re-stamped 2274→2273 (net of the field).
  - The COMMIT-B trailers `Blocked-WI:`/`BlockRef:` (a worker's block signal)
    are a distinct instrument and were left intact.
  - PRE-EXISTING failure noted: `test_dispatch::test_drive_end_to_end...` fails
    on a `lint` (ruff I001) finding in a *scaffolded demo* file — a ruff-version
    skew, reproduced on the clean tree before this WI; not in scope.

Deferred open items: none — OI-70 is ruled and this WI mechanizes it; no new
question is raised.
