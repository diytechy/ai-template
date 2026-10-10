# WI-834 rework round 3: coverage plan

Answers `docs/reviews/wi-834/009-REVIEW-A-ecca75b.md` (F1..F2: the two lines
under its "Findings:" heading, in the order written; plan_coverage reads the
same two).

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| R1 | F1: a keep-warm tick leaves a session another call's live lease holds to that call, and applies the blackout retirement only to an unleased record | F1; D16; D20; SR-227; TC-341 | IF-248 | |
| R2 | F2 (code part): dev-setup's two owner headers state the launcher's invocation and its readiness result as two seams, landing with the spine author's IF-292 split | F2; D33 | IF-292; IF-157; IF-158 | |
| R3 | The round's regression bar: the retention, lease and keep-warm pins and the launcher readiness pins re-run unchanged | SR-227; SR-229; SR-230; TC-266; TC-267; TC-268; TC-303; TC-329; TC-339; TC-340 | intra-module (no seam changes in this row) | R1; R2 |

## R1 (F1)

- **Confirmed** on the real code path. Probe
  `C:/Projects/ai-template.wt/review-tmp/2026-10-09-leg03/wi834-r3-f1-probe.py`
  (run under pytest with the lane's `retained` fixture and both the window
  clock, `agent_policy._utcnow`, and `session_keep.time` set to one controlled
  clock): the real `session_keep.keep_for` at Monday 18:59 (inside the
  `12:00-19:00` window, the wrap-up, the session last used 11:00), the real
  `session_service.KeepWarmer.tick` (-> `take_warm_lease`) at 19:01 while that
  call's lease is live, the real `keep_bookkeep` of a successful call at
  19:03, then the real `keep_for` at 19:10. Lane against the base source
  (`git show 07340664:project-trajectory/scripts/session_keep.py`, swapped in
  through `KEEP_SOURCE`):

  ```text
  lane  18:59 keep_for: session_id='S1' lease='adjudicate'
  lane  19:01 tick: lines=[] state=retired reset_reason='blackout' lease_live=True pinged=False
  lane  19:03 bookkeep: cols={'session-gen': 1, 'reset-reason': 'blackout'} state=retired reset_reason='blackout' last_used=19:03
  lane  19:10 next keep_for: session_id='' (expected 'S1')    -> AssertionError
  base  19:01 tick: lines=['keep-warm: skipped (the session is leased to adjudicate:...)'] state=active
  base  19:03 bookkeep: state=active reset_reason='' last_used=19:03
  base  19:10 next keep_for: session_id='S1'                  -> passed
  ```

  The tick retires a session whose wrap-up is in flight, the call's own
  bookkeeping then lands on a retired record (last use 19:03, after the
  window's end), and the next adjudication mints. A regression of this lane:
  the base tick refused on the live lease.
- **Class:** a retirement path that decides on a session's record without
  first honouring a live lease another call holds on it.
- **Sites examined** (every locked or lockless read of a retained record that
  can retire it or decide on its last use or state):
  - (a) IN THE CLASS: `take_warm_lease` (:1070-1081). Under the store lock,
    per due record, `retire_after_blackout(root, record)` (:1074) runs and
    saves BEFORE `_lease_held` (:1078) is asked, so a live adjudication lease
    does not stop the retirement. The only site in the class.
  - `keep_for` -> `_hold` (:765) calls `retire_after_blackout` only once
    `_lease_held` (:732) has returned "" (no lease, the caller's own, or an
    expired one, which `retire_stale_lease` :731 has already retired): the
    lease is honoured first. Not in the class.
  - `retire_stale_lease` (:599-619, called :731 and :1073): retires only on an
    EXPIRED lease (`until <= now`), by design (LLR-270's unreleased-lease
    rule). Not in the class.
  - `_before_launch` (:652-662, same-artifact guard and drain-to-clear-point
    retirements): reached only from `_hold`, after the lease check. Not in the
    class.
  - `keep_bookkeep` (:840-892) and `keep_release` (:387-400): the lease
    holder's own call retiring or releasing its own session. Not in the class.
  - `keep_abandon` (:938-956) -> `write_tombstone` -> `load_honoured` ->
    `_apply_tombstone` (:328-368): the tombstone is written by the lease
    holder about its own launch; any later locked read applies the holder's
    decision. Not in the class.
  - `due_routes` (:1019-1032), `_warm_candidates` (:1035-1044) and
    `keepwarm_due` (:997-1016): read state and last use, lockless, but only
    to SELECT candidates; they never retire or save, and the decision is
    re-taken under the lock in `take_warm_lease`. Not in the class.
  - `session_service` (:396 `keep_abandon`, :434 `keep_bookkeep`, :368
    `keep_release`, :1219 `due_routes`, :1222 `take_warm_lease`): no record
    write of its own; it reaches the store only through the session_keep
    entry points above.
- **Searches:**
  - `rg -n "retire_after_blackout|take_warm_lease|_retire\(|retire_stale_lease|STATE_RETIRED|keep_abandon|write_tombstone|last_end_epoch" project-trajectory/scripts`
    -> the two `retire_after_blackout` callers (:765 `_hold`, :1074
    `take_warm_lease`), the seven `_retire` call sites (:367, :617, :648,
    :656, :662, :877, :879) and the two service entry points;
  - `rg -n "store_save|store_remove|load_honoured|_lease_held|keepwarm_due|due_routes" project-trajectory/scripts`
    -> every store writer (:381, :383, :771, :887, :1075, :1085) and every
    lease reader (:732, :1078); only :1075 saves a retirement taken without
    the lease read;
  - `rg -n "reset_reason|\"retired\"|STATE_DRAINING" project-trajectory/scripts`
    outside session_keep.py -> no other module writes a retained record's
    state;
  - `rg -on "session_keep\.[a-z_]*" project-trajectory/scripts` -> the
    external entry points (`keep_for`, `keep_bookkeep`, `keep_release`,
    `keep_abandon`, `due_routes`, `take_warm_lease`, `applies`, config and
    path readers).
- **Owning boundary:** `take_warm_lease`'s locked per-record decision, with
  `_lease_held` the one live-lease reader. The lease check moves ahead of the
  blackout retirement under the same lock and the same clock read: a record
  another call's live lease holds is not retired (its owner's bookkeeping
  lands the last use; the next unleased tick or keep call applies the
  predicate to it), and, if due, the tick returns the existing "the session
  is leased to ..." reason as the base did. `retire_after_blackout` and
  `_hold` are unchanged. No compensating reset in `keep_bookkeep`
  (un-retiring there would be a second rule over one decision).
  `take_warm_lease` stays at or below 15 (12 today; one boolean added).
- **Owner header and docstring** (code comments, this row): the IF-248
  contract body in `session_keep.py`'s module docstring (:87-91, "both it and
  `keep_for` first retire a live session ...") and `take_warm_lease`'s
  docstring (:1059-1061) gain that a session another call's live lease holds
  is left to that call. The IF-248 row's `data` cell needs no change.
- **Pin (red first):** one test in `tests/test_blackout_window.py`, beside
  `test_a_keep_warm_tick_first_after_the_window_retires_and_never_refreshes`,
  driving the service flow: an active claim, `svc.act` of a retained
  ADJUDICATE call admitted at 18:59 whose runner advances the clock to 19:01
  and runs the real `KeepWarmer.tick` mid-call, the call's bookkeeping at
  19:03, then `keep_for` at 19:10 resuming `S1`; the tick reports the lease
  and the record stays `active`. Red on the lane before R1, green after. The
  existing first-after-window tick pin stays green (an unleased stale record
  is still retired).

## R2 (F2, the code part)

- **Confirmed** by reading: IF-292 (`docs/requirements/interfaces.toml:2634`)
  carries the launchers' invocation AND the readiness exit result in one
  `channel = "cli"` row with `consumers`, where PROCESS.md §8 says "a CLI's
  arguments and its exit code are two" rows, `Requestors` for the invocation
  and `Consumers` for the exit code. The lane amended IF-157's and IF-158's
  `data` to readiness and pause behaviour that `run_menu.py` does not have
  (its header :68-82 is unchanged, and the reviewer's real `run_menu.py`
  run opened the menu with no dev-setup step). Census:
  `rg -n 'channel = "cli"' docs/requirements/interfaces.toml` -> 22 cli rows;
  three carry `consumers`: IF-292 (this lane), IF-267 and IF-279 (both on
  base 07340664, not this lane's change; surfaced to the coordinator as a
  separate observation, not planned here). Cli rows with `requestors` (e.g.
  IF-157, IF-280) are the pattern; exit codes are their own `exit-code` /
  `consumers` rows (e.g. IF-158).
- **Class:** a seam row that does not describe its owner's real surface in
  one direction and channel.
- **Header lines that must change, landing in the same commit as the spine
  author's IF rows** (the new readiness-result row's id is the spine
  author's mint, written `IF-NNN` here):
  - `project-trajectory/scripts/dev-setup.template.sh:32`
    `# Contracts: IF-292 — the interface seam this script declares (process.md §8;`
    -> `# Contracts: IF-292, IF-NNN — the interface seams this script declares (process.md §8;`
    and :33 `# row of record ...` -> `# rows of record ...`;
  - `project-trajectory/scripts/dev-setup.template.sh:35-37` (`# Contract
    IF-292:` body): narrowed to the invocation only (`--for-run`, from the
    repository root, once, by a bare launcher run before its menu), and a new
    `# Contract IF-NNN:` body after it: exit 0 says the runtime is ready;
    nonzero leaves the menu unopened after setup guidance;
  - `project-trajectory/scripts/dev-setup.template.ps1:29-30` and `:32-34`:
    the same two changes, with `-ForRun`.
- **Header lines that stay** (checked, no change):
  - `project-trajectory/scripts/run_menu.py:56-82` (`Contracts: IF-048,
    IF-157, IF-158` and their three bodies): already true to run_menu's
    surface, which this lane did not change; the spine author's IF-157/IF-158
    `data` cells return to run_menu's own argv and exit codes to match them
    (spec D33: amended only "where the arguments or exit behaviour change",
    and run_menu's do not);
  - `project-trajectory/scripts/run.template.cmd:10-16`,
    `project-trajectory/scripts/run.template.sh:9-15`,
    `project-trajectory/scripts/run.template.command:4-6` and the repo's
    root `run.{cmd,sh,command}`: they carry no `Contracts:` marker (the far
    side, `external:run.* launchers`, of IF-292 and IF-NNN), and their prose
    already describes the call and its result separately. The Windows
    closing-pause skip is the launcher's own behaviour (SR-046/LLR-047,
    TC-342), stated in `run.template.cmd`'s header, not a run_menu seam.
- **Generated, not hand-edited:** `docs/interface-reference.md` and
  `docs/cli-reference.md` are regenerated by the coordinator at landing
  (`gen_arch_map.py --contracts-doc`).
- **Search:** `rg -n "IF-157|IF-158|IF-292|IF-048" --glob '!docs/archive/**'`
  -> the owner headers above, `docs/if-tc-coverage-allow:198-199`,
  `tests/test_frame_context.py:143` (IF-157 only, unchanged), TC-342
  (`docs/test/test-cases.toml:3478`) and the spec :238; and
  `rg -n "IF-|Contract|Consumes|Provides" project-trajectory/scripts/run.template.* project-trajectory/scripts/dev-setup.template.*`
  -> markers only in the two dev-setup templates.
- **Owning boundary:** each seam's owner header; the row is the spine
  author's.

## R3 (regression bar)

- **Class:** none new; the other retention and launcher readings must not
  move.
- **Sites:** `tests/test_session_keep.py` (TC-266, TC-267, TC-268, TC-303,
  TC-329: lease, mint race, warm-lease and reset pins),
  `tests/test_blackout_window.py` (TC-339, TC-340, TC-341), and
  `tests/test_run_devsetup.py` plus `tests/test_seam_resolution.py`
  (launcher readiness; header grammar, so a malformed `Contracts:` line
  fails here).
- **Search:** `rg -n "def test_" tests/test_session_keep.py tests/test_blackout_window.py`.
- **Owning boundary:** unchanged; re-run, no edit.

## Exclusions

Excludes: F2 — spine text (IF-292 split into a cli/Requestors invocation row and a new exit-code/Consumers readiness-result row; IF-157's and IF-158's data returned to run_menu's own surface; TC-342's verifies list naming the new row): the spine author reconciles it at the lane's checkpoint (coordinator-cycle skill §3) and it lands in one commit with R2's header lines; this builder does not touch the registries.
Excludes: TC-321; TC-322; TC-323; TC-324; TC-330 — their modules (coordinator_adjudicate, the adjudicator token, the sign-in probe) are untouched by this round; they run in the smoke tier unchanged.
Excludes: TC-315; TC-316; TC-317; TC-318 — the coordinator guard and relaunch paths are untouched by this round; they run in their tiers unchanged.
Excludes: D1; D2; D3; D4; D5; D6; D7; D8; D9; D10; D11; D12; D13; D14; D15; D17; D18; D19; D21; D22; D23; D24; D25; D26; D27; D28; D29; D30; D31; D32; D34; D35; D36; D37; D38; D39; D40; D41; D42; D43; D44; D45; D46; D47; D48; D49; D50; D51; D52; D53; D54; D55; D56; D57; D58; D59; D60; D61; D62; D63; D64; D65; D66; D67; D68 — built in the lane's earlier rounds (785a004d, 9bc1eb2a and the adjudicated rounds through ecca75b9) and not reopened by this round's REVIEW-A; this round reopens only F1 (D16's retention across the window, D20's tick pin) and F2 (D33's seam rows).
