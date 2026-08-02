# WI-381 — REVIEW-A (2026-08-02)

Verdict: APPROVE — the barrier, the authority flip, the ladder, the dial and
the scaffold surface all reproduce under my own scratch drives, the two
barrier arms are mutation-pinned (I reproduced and extended the builder's
2-failed figure), the byte-identical single-claim shape is proven against
trunk's own literal, and the serial degeneration at one lane is
transcript-identical to trunk's drive.py on the same fixture. Four bounded
findings are recorded below; none blocks. `staged_spine_amendments` over the
branch range returns **no ratified-cell amendment** (one traced `Evidence`
cell only), so **no adjudication act is required and none is taken** — this
APPROVE carries no Status authority.

Reviewed: branch `wi-381-spine-barrier-batch-and-wait` at `585f5a65`
(six commits walked in order: `81cac0e1` split, `82f516b2` barrier+flip,
`a119065e` ladder+banner+seed, `d520d43f` registration, `82c64d46` seams,
`585f5a65` close); merge-base/claim `a8549cdf`; trunk
`ConcurrencyTrainRewrite`. All commands under the worktree's
`.venv/bin/python`. Per the brief: `docs/log.d/` was not read, and the full
unfiltered suite was not re-driven (the refresh bar owns it — the
Deliverable's watched 1924 passed / 5 skipped is taken as the builder's
claim). My tier: module suites, smoke, strict checks, and the scratch
drives below.

## Hunt 1 — the barrier, driven

**Total wait.** Pure-decision pins verified:
`_admission([("WI-500","spine"),("WI-401","ordinary")], busy=True)` answers
`("wait", [])` — the ordinary row behind the spine row does NOT slip into
the free lane (`test_an_exclusive_row_with_a_busy_lane_does_not_admit`).
At the loop level the wait is structural: `_admit` computes
`free = 0 if exclusive_live else …` and `_admission` is consulted with
`busy=bool(table)`, so nothing admits past an exclusive-kind frontier row
while any lane (worker OR refresh phase) is out.

**Batch as one claim, one worker.** My own scratch drive (two spine rows +
`Recorder` worker):

```
worker calls: [('wi-501-alpha', ('WI-501', 'WI-502'))]
claim lines:  ['dispatch: cycle 1 - claiming WI-501;WI-502 on wi-501-alpha (exclusive)']
recent subjects: ['claim: WI-501;WI-502 -> active/wi-501-alpha (bookkeeping)', …]
claim commit moves:
  R100  docs/work/queued/WI-501-alpha.md  docs/work/active/wi-501-alpha/WI-501-alpha.md
  R100  docs/work/queued/WI-502-beta.md   docs/work/active/wi-501-alpha/WI-502-beta.md
```

ONE claim commit moving both specs, ONE worker invocation with both ids.
The builder's loop-level test (`test_the_spine_batch_admits_first_and_together`)
additionally proves the ordinary row admits only after the window closes.

**High-risk/protected alone.** `_admission` answers `admit-exclusive`
with `[first]` only (`test_high_risk_admits_alone_not_batched`), and
`_branch_exclusive` fails toward exclusivity on unreadable frontmatter for
the parked-resume path.

**Single-WI batch byte-identical.** Trunk's literal is
`"claim: {} -> active/{} (bookkeeping)".format(wi_id, branch)`; the branch
joins a one-element list with `";"` — same bytes — and the commit BODY
paragraph is character-identical between trunk `integrate.py:671` and the
branch. Driven: my hand claim of WI-401 produced
`claim: WI-401 -> active/wi-401-widget (bookkeeping)`, and the abandoned-claim
reader parses both shapes through the one `_claim_subject` home.

**Mutation checks (reproduced and extended).** Neutering BOTH wait arms in
`_admission` (`if busy:` → `if False:` in the batch/exclusive arm and the
single-ratify close arm):

```
FAILED tests/test_dispatch_admission.py::test_an_exclusive_row_with_a_busy_lane_does_not_admit
FAILED tests/test_dispatch_admission.py::test_single_ratify_keeps_non_dependent_work_running
2 failed, 14 passed
```

— the builder's "2 failed / 12 passed" figure reproduces (the +2 passes are
the ladder/dial tests `a119065e` added after their run). Mutating the
SURFACE arm (`_kind_action` returns `exclusive` for attestation/gate at
every level) fails 4: the table pin, the pure surface pin, the single-ratify
pin, AND the loop-level attended drive
(`test_attended_ratification_row_drains_and_exits_zero_with_the_banner`) —
the surface arm is pinned at both altitudes. File restored after each run
(`git status` clean).

## Hunt 2 — the authority flip

**Live lock refuses a hand claim.** Scratch drive: a holder process took
`out/agent-loop.lock` (flock), then the CLI ran:

```
hand claim vs LIVE lock -> rc=1
  integrate: REFUSED - the dispatch lock …/out/agent-loop.lock is held - a
  dispatcher's lanes are live, and a hand claim mid-flight is unrepresentable
  (WI-381, §A4.1 …)
```

No branch cut, spec still in `queued/`. Holder killed → the same CLI claim
succeeded (rc=0, branch cut + trunk advance), and the hand path unlinked its
lock file so the next clean-trunk rung is not tripped.

**Bypass hunt: clean.** The CLI (`integrate.py main`) exposes no flag
reaching `dispatch_lock_held` (grepped the argparse surface); the only
`dispatch_lock_held=True` caller in shipped code is `dispatch.py:767`, and
its process really holds the lock (`agent_loop._drive_entry` acquires via
`_coordinator_lock` BEFORE `dispatch.run`). No other module calls
`integrate.claim` (grepped agent_loop/agent_session/plan_runner/handback/
trunk_step); `_claim_locked` is reachable only through `claim`. The ladder
runs BEFORE the lock so the clean-trunk rung never refuses over the lock's
own file, and the lock file is excluded from the claim commit (`reset -q --`)
— both corners have recorded rationale in the code. A worker session locks
its own worktree's `out/agent-loop.lock`, not trunk's, so lanes cannot
shadow the trunk lock. The one behavior shift: `_dispatch_lock` refuses on
ANY lock error where `acquire_lock` degrades to a warning on
no-advisory-lock filesystems — fail-closed in the conservative direction,
acceptable.

## Hunt 3 — §A8 policy

**Attended arm, driven.** The builder's loop test passes; my scratch drives
made the two banner reads DISAGREE (see finding 1): with 2 Modified SRs on
the registry and one queued gate row, the exit-0 banner said
`queue drained - 2 ratification(s) waiting in open-items.html` — following
`pending_block` — and worker calls stayed empty. With a queued gate row and
ZERO pending cards it said `1 ratification(s)` — the surfaced-count floor,
NOT the pending read (finding 1).

**Single-ratify mechanical reading — judged FAITHFUL.** The ruled cell is
"dispatch only the queued batch at the phase `[g2]` close; otherwise
surface". The dispatcher has no phase-close event; the tree-derived proxy
implemented — surfaced rows admit as one exclusive batch exactly when
nothing else is dispatchable and the station is idle — is the honest
mechanical reading: while any phase work is ready or active, "something
else remains" holds and the batch keeps waiting; a WAITING row implies a
ready/active/blocked predecessor, and the only leak (every sibling blocked
on a human) is a state where running the queued ratification is defensible.
The conservative direction of the proxy (next-phase ready rows postpone the
batch past this phase's close) is noted, not a defect. Driven at the pure
level in `test_single_ratify_keeps_non_dependent_work_running` including
the busy-close wait arm.

**Autonomous.** `_kind_action` returns `exclusive` for attestation/gate at
`autonomous` (table pin + `test_autonomous_gate_rows_dispatch_exclusive`).
The attended combination rule (a surfaced row trumps a dispatchable spine
row) matches the owner-confirmed premise "once a ratification is pending,
no work can be taken" and stops at exit 0 rather than today's nonzero.

## Hunt 4 — the empty-frontier ladder

**Rung 1 mints NOTHING — driven.** My scratch repo (unverified SR + draft
SN): rc=0, census lines printed
(`gap census: SR SR-001 has no LLR …`, `SN SN-002 is a draft need
(unratified)`, `… nothing was minted - no silent planner mints.`), the
`WI-*.md` file set before/after is IDENTICAL and the tree is clean
(`git status --porcelain` empty). Rung 2's count derives from
`_pending_cards` (the pure read, no floor), rung 3's drained banner counts
merged+residue.

**gap_census vs WI-388's amended spec — usable.** WI-388 trigger 3 expects
"the empty-frontier gap census handed over by the dispatcher … become
concrete gap-closure rows with derived descriptions". The seam is
`dispatch.gap_census(root) -> list[str]`, importable trunk-side, ids
embedded (`SR SR-001 …`, `SN SN-002 …`), reusing `trace.analyze` (the one
orphan/status engine) with `require_verified=True` — exactly the three gap
classes the amendment names, and the strings ARE the derived descriptions.
No shape mismatch that would cost WI-388 a rework.

## Hunt 5 — the lanes dial

Ladder pinned (`test_lanes_ladder_cli_over_env_over_stack_ini`), absent key
= 1 pinned, malformed/sub-1 falls to serial loudly. The TEMPLATE seeds
`lanes = 2` on a live line (verified in `stack.ini.template` AND in the
fresh scaffold's `docs/stack.ini:129`); this repo's own `docs/stack.ini`
carries NO key (grepped — comment only), so the meta-repo stays serial.

**Serial degeneration vs trunk — transcript-identical.** I ran the same
stub-harness repo + closing worker through trunk's `drive.py` and the
branch's `dispatch.py` at one lane: rc=0 both, same worker call, same claim
subject bytes, same merge subject, and the same final banner
`queue drained - no ready work items; 1 WI(s) integrated this run.` The
only diffs were commit-graph print order and the refresh PASS line arriving
via the branch's refresh SUBPROCESS (which also confirms `spawn_refresh`
runs even at lanes=1 — the §A4.3 overlap machinery is live, not vacuous).

## Hunt 6 — the scaffold run

Reproduced the Deliverable's figure: `bootstrap.py --dest <tmp> --agents
none`, git init/commit, then the scaffold's OWN
`AGENT_CMD='stub-agent {prompt}' python scripts/agent_loop.py --root .`:

```
exit=0
integrate: no finished claimed branches - nothing to merge.
dispatch: queue drained - no ready work items; 0 WI(s) integrated this run.
```

The scaffold ships `dispatch.py` + `lane.py` byte-identical to the kit
copies and no `drive.py`. Bootstrap MAPPING rows, `test_bootstrap` file
lists, kit README rows (schedule/dispatch/lane/handback), ADOPTING.md §6
(a full resync note: copy both, DELETE your old drive.py, absent-key
warning) and the downstream-resync skill copies are all coherent.

## Hunt 7 — registration + adjudication-grade checks

**Cells true.** TC-143/144/145's evidence suites re-run:
`tests/test_dispatch_admission.py tests/test_dispatch.py
tests/test_integrate.py` → **159 passed in 56.70s**. Every specific claim
in the three Method cells maps to a real test I read (the lock refusal,
the one-commit batch subject, the red-then-green safety-arm flip, the
ladder rungs). LLR-149/150/151 Module/CodeSymbol cells match the shipped
symbols.

**IF-088/IF-089 driven-need — reproduced.** In a scratch clone at
`585f5a65` with the arch-map regenerated (the station's first act), strict
is rc=0 WITH the rows; with the two rows removed:

```
ERROR - cross-component import scripts/dispatch (CMP-004) -> scripts/gen_trajectory (CMP-002) has no declared IF-### seam …
ERROR - cross-component import scripts/dispatch (CMP-004) -> scripts/trace (CMP-001) has no declared IF-### seam …
rc=1
```

— exactly the two reds the seams commit names. (But see finding 2: the
docstring side of the declaration doesn't harvest.)

**LLR-143/TC-137 deferral — honest, driven.** Repointing LLR-143's Module
at `dispatch.py` NOW (pre-regen clone) reds strict:
`ERROR - docs/knowledge/ holds 6 pack(s) but 1 arch-map module(s) are in no
CMP-### component …` — the committed arch-map still inventories
`scripts/drive`, so the unhook genuinely cannot land before the trunk-side
regen, and WI-390's spec §2 explicitly owns the move plus the inherited
no-IF-row WARNs (which shift `drive` → `dispatch`+`lane` post-regen, as
specced). `docs/declared-absences` carries the three old paths with the
§A9.1 pointer. Honest per §A9.1: this is inherited-and-recorded drift, not
mothballing.

**Amendment scan.** `staged_spine_amendments(root, a8549cdf, HEAD)`:

```
[{'ratified': {}, 'traced': {'Evidence': ('tests/test_drive.py', 'tests/test_dispatch.py')}, 'registry': 'docs/test/test-cases.csv', 'id': 'TC-137'}]
```

No ratified cell moved anywhere on the branch; the one traced `Evidence`
follow-the-rename is silent by the §A5 ruling and was disclosed in the
registration commit. No adjudication act owed; none taken.

## Hunt 8 — the deleted drive.py, walked

Each behavior of trunk `drive.py` located in `dispatch.py` or accounted:
stall counter (`_poll`'s trunk-unmoved count against `ln.head`, guard
survives with equivalent terminal behavior); resume-first
(`_admit_parked` runs before the frontier read; an exclusive resume waits
for an idle station); session-config refusal (`_session_config_refusal`
verbatim, still lazily applied so an unwired scaffold drains to 0);
dirty-tree hoist and pause check (tick-top, extended to freeze-only while
lanes are live — the documented §5.6 shape); residue counting at exit
(kept — but see finding 3 for the barrier-open path); quarantine-once
(`_refresh_or_quarantine` verbatim for residue, `_refresh_failed` the
subprocess twin with the `retried` bound); `_WORKER_OUTCOMES` and the
EXIT_BUDGET/EXIT_STALL trade note carried verbatim (that trade was filed in
the WI-387 round, not this row's debt); EXIT_TRAIN_END's absence recorded.
`_drain` gained a `_merge_ready` skip (don't re-run a bar already attested
for this exact tip) — sound, and the e2e test pins the speculative half.
Nothing silently dropped.

## Hunt 9 — mechanical

- Module suites: **159 passed in 56.70s** (dispatch_admission + dispatch +
  integrate; there is no `test_lane.py` — lane.py is driven through
  test_dispatch, which is what TC-144's Evidence cell truthfully says).
- Smoke: **645 passed, 2 skipped in 10.22s** (matches the close's figure).
- `trace.py --strict` rc=0; `check_trajectory --strict` rc=0 (2 pre-existing
  SpecRef-clock WARNs on WI-389/WI-390, not this row's);
  `check_doc_refs --strict` rc=0; `check_figures --strict` rc=0;
  `derive_gate --check` rc=0 (`docs/gate up to date (G3)`, basis
  LLR=134 TC=131 — the WI-401/402 regen precedent honored at the close).
- Ratchet: exactly four baseline bumps (agent_loop +12, bootstrap +9,
  agent_common +32, integrate +126), each with a recorded reason;
  dispatch.py (957 lines) and lane.py stay under THRESHOLD=1500.
- Dupes: `check_dupes.py --src project-trajectory/scripts` → OK over 50
  files; the new `kind-resolution` census row is a real, reasoned sanction.
- Byte stamps: AGENTS.template 9,991 ≤ 10,000 (test green); PROCESS.md
  64,460 = stamp; PROCESS_OPTIONS 169,138 = 169,125 + the flagged +13
  (see finding 4). Ruff format + check rc=0. R-A/R-F ride
  `check_trajectory --strict` rc=0. `docs/work` branch delta is
  WI-381-only (the spec's own move + Deliverable).

## Findings

1. **MINOR — the attended banner's surfaced-count floor can disagree with
   the owner surfaces.** `_surface_banner` returns
   `max(len(_pending_cards(root)), len(surfaced))`. Driven both ways: with
   2 Modified SRs + 1 queued gate row the banner says **2** (follows
   `pending_block`); with a queued gate row and ZERO pending cards it says
   `queue drained - 1 ratification(s) waiting in open-items.html` while
   `pending_block` renders "_None — no durable owner action is pending._"
   — exactly the disagreement the ruled amendment says must never happen
   ("must derive from the SAME pending_block(root) read … can never
   disagree"). The corner requires a mis-filed gate/attestation row with
   nothing actually pending, the divergence over-reports rather than
   hides, and the builder recorded the floor judgment in the docstring —
   bounded, not blocking. Recommend dropping the floor or naming the
   queued row itself ("1 queued attestation row") so the banner never
   points at cards that are not there.

2. **MINOR — IF-088/IF-089 fall out of the Contracts harvest after the
   station regen.** `gen_arch_map.module_contracts` collects IF ids only
   from LINES containing the word `Contracts`; dispatch.py's Contracts
   paragraph wraps, leaving `IF-088`/`IF-089` on continuation lines. In
   the post-regen scratch clone the arch-map's line reads
   `Contracts (interfaces): IF-015` and strict emits two NEW WARNs:
   `IF IF-088 is in the registry but no script declares it via a
   Contracts: docstring line` (and IF-089) — undisclosed additions to the
   very registered-but-undeclared drift family (IF-055/IF-081) that §A9.1
   says to record, not silently grow. Strict stays rc=0 (warn-tier); the
   seam ROWS are load-bearing regardless (hunt 7). One-line fix: keep the
   ids on `Contracts`-bearing lines; natural home is WI-390's connectivity
   batch, which already owns the Contracts moves.

3. **MINOR — residue merged at barrier-open is dropped from the drained
   banner's count.** `_drain` at the admit-exclusive arm merges finished
   residue branches without crediting `state["merged"]`, and by exit time
   they are no longer residue. Driven: a hand-finished `wi-777` + a queued
   spine `WI-501` → both specs land in `complete/`, both merges print, and
   the run ends `queue drained - no ready work items; 1 WI(s) integrated
   this run.` — an undercount of the exact shape trunk's REVIEW-A rounds 1
   and 2 fixed (trunk counted `finished_branches` before every drain).
   Cosmetic (nothing merges wrongly), but it regresses a twice-reviewed
   banner contract. Fix: count `finished_branches(root)` before the
   barrier-open `_drain` as `_station_exit` already does.

4. **MINOR — the flagged +13 bytes were not re-stamped into the
   byte-budget-guard skill.** PROCESS_OPTIONS.md is 169,138 bytes; the
   skill's baseline (all tracked copies) still reads 169,125, and its own
   rule is "re-stamp this number, every tracked skill copy, when a flagged
   growth lands". The delta WAS flagged with a reason in the Deliverable —
   the stamp housekeeping is the only miss. Convention-tier (no check
   reds); re-stamp on the next touch.

## Verdict

The largest build of the program holds up under independent drives: the
wait is total and mutation-pinned, the batch is one commit and one worker
with the single-WI shape byte-identical to trunk, the hand-claim hole is
closed by a constraint I could not bypass, the ladder mints nothing, the
dial fails toward serial, a fresh scaffold walks away clean through the
shipped modules, and the registration is adjudication-grade with the one
staged amendment traced-only. Four minor findings — a floored banner corner
the builder disclosed, a Contracts-harvest wrap, a residue count
regression, and a stamp housekeeping miss — all bounded, with named homes.

VERDICT: APPROVE findings=4
