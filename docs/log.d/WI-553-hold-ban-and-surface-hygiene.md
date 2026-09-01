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

Deferred open items: none — this WI mechanizes a ruling already made; no new
question is raised. (File-level, so it speaks for the whole fragment.)

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
- **Done-when 2c (templates + docs) LANDED.** The `-000` example twin
  (`docs/work/queued/WI-000-example.md` + `project-trajectory/work/WI-000.template.md`)
  rewrites the `blocked`-has-no-directory bullet to the current model (a stopped
  lane closes PARTIAL; hold-by-rename banned, OI-70) and drops `blockref` from
  the scheduler-inputs list. The shipped `work-items.template.csv` header +
  teaching text, the `docs/work/README.md`+template README twin (its IF-054
  contract comment is the SOURCE for generated `interface-reference.md`, which
  the trunk lane regenerates), and the authored docs (`runtime-flows.md`,
  `project-trajectory/README.md`, `knowledge/unattended-operation.md`,
  `PROCESS_OPTIONS.md`) all drop the retired-mechanism teaching. Stale-producer
  doc `concurrency-restructure.md` left as dated Phase-5 history (already hedged
  "retiring"). A RESYNC_PACK.md §3 entry documents the optional column-drop
  migration + the new check (anchored at the preceding kit commit). Byte
  budgets: `PROCESS_OPTIONS.md` 181,326→181,369 (+43, FLAGGED, re-stamped in the
  byte-budget-guard skill, which re-stamped its own 4,829 row); skill copies
  re-fanned. `interface-reference.md` left stale on the branch by design.
- **Done-when 3 (fragment `none` cross-checked) LANDED.** `gen_open_items` gains
  ARM 4 (`_none_declaration_findings` + `_scope_span`): a fragment declaring
  `Deferred open items: none` while its own SCOPE cites a PENDING open item is
  contradicted — the TRUTH check OI-70 named, the reverse of ARM 2's presence
  check. POSITION IS SCOPE (a section-scoped `none` judged against that section,
  a file-level one against the whole fragment); warn-first, never the exit code;
  fail-soft (only pending citations contradict — a ruled/absent id a `none`
  fragment mentions is history — and a `none` citing nothing pending passes
  clean). Four tests in `test_gen_open_items.py` (contradiction; ruled/absent
  cite passes; position-is-scope both ways).
- **Done-when 4 (ban stated where supervisors read) LANDED.** The
  session-protocol skill gains a Standing rule (partial close is the only
  sanctioned stop; hold-by-rename BANNED; cites OI-70; names the claim-ref
  check) — re-fanned to the `.claude`/`.gemini`/`.agents` copies.
  `docs/handbacks/README.md` states the same after its opening. The ADJUDICATE
  `adjudicate-disposition` prompt's opening now names the partial close as the
  ONLY sanctioned stop and cites OI-70 (it already carried OI-73's two-exit
  rule); `prompts/CATALOG.md` regenerated (a commit-time gate). The worker
  `Blocked-WI:`/`BlockRef:` block path was deliberately left unchanged — it is
  the sanctioned worker stop (the loop turns it into a partial close), distinct
  from the banned ref-rename, which is a SUPERVISOR action.

### Review-A rework (CHANGES-REQUESTED, 5 MAJOR — addressed)

Review A rejected leaving the stale spine cells for a later pass: they are the
DIRECT consequence of this diff removing the mechanism, so an Approved
requirement that still specifies the deleted behaviour is a spec-vs-code
contradiction, not out-of-lane prose drift. Re-pointed all five (the reviewer's
line numbers, not the earlier fragment's mis-ids):

- **LLR-058** (`schedule` frontier): dropped "a queued WI carrying a blockref
  reads as blocked"; a lane stopped early now leaves the frontier through its
  terminal `partial/` move (its spec is no longer `queued/`). "excludes
  blocked/…" → "excludes terminally-closed/…".
- **LLR-144** (`handback.close_partial`): "schedule reads queued+blockref as
  blocked …" → the terminal `partial/` move ALONE is the anti-livelock property.
- **LLR-198** (`pending`): CodeSymbol `blocked_pending`→`pause_pending`; Detail
  now names TWO sources (spine, pause), records `blocked_pending`'s retirement as
  a parenthetical, and the facade re-exports the THREE surviving names
  (spine_pending, pause_pending, pending_block), reached through ONE private name.
- **TC-138** (handback): "an already-declared blockref … survive" → a close
  writes NO blockref because the `partial/` folder is itself terminal (the
  contract that now verifies LLR-144's anti-livelock property —
  `test_a_close_writes_no_blockref_because_the_folder_is_terminal`).
- **TC-194** (pending read model): dropped the blocked-row arm and the IF-138
  loader-seam arm; Method + names → spine/pause projections and the three
  surviving former names; `verifies` drops `IF-138`.

Swept one stale cell the review did not enumerate but is the same defect class:
**TC-147** (intake) "id max+1, blockref empty, …" → the minted adjudication row
carries no blockref field at all (intake.py already dropped it this WI).

**IF-138 retired (completes done-when 2).** `blocked_pending` was `pending.py`'s
ONLY reader of the `check_trajectory` loaders (`read_registry_rows`/`load_wis`/
`WI_CSV`); removing it deleted that import, so the IF-138 loader seam no longer
exists in code. Retired the Drafted `IF-138` row from `interfaces.toml`, its
`Contract IF-138:` docstring block + `Contracts:` list entry in
`check_trajectory.py` (docstring-only — SLOC unchanged, no ratchet re-stamp), its
`TC-194` coverage, and the dangling `IF-084` rationale pointer. Interfaces carry
no Retired status in this kit (all 163 are Drafted), so retirement is row
deletion.

**Consequences.** The five edited Approved cells now DRIFT from their
`docs/archive/last_approved/` snapshot → they owe the owner a re-attest;
regenerated `docs/ratify/CURRENT.md` carries them. Generated surfaces still
naming IF-138 (`interface-reference.md`, `cli-reference.md`,
`components.derived.toml`, trace `report.md`) are left STALE on-branch for the
trunk regen — the same posture this WI already took for `interface-reference.md`.
Targeted suites green: trajectory/specs/arch/views/pending/holdban 254; import-
layers/intake/handback/schedule 112; freshness-wiring/gen-components/arch-map/
check-lane 106; `check_trajectory.py --root .` exits 0 (only the expected wi508
hold-by-rename WARN + shared-spec WARNs).
