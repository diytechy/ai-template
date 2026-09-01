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

Deferred open items: none — OI-70 is ruled and this WI mechanizes it; no new
question is raised.
