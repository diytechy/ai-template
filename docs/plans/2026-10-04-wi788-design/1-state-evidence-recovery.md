# Chapter 1: state, evidence and recovery

Part of the WI-788 design note ([README.md](README.md)). Read at lane base
`c3be7be0`. Code cites are `path:line` under `project-trajectory/scripts/` unless
another root is given. Siblings: [2 sessions, routing, accounts](2-sessions-routing-accounts.md),
[3 planning, tiering](3-planning-tiering.md),
[4 adjudication, mint, landing](4-adjudication-mint-landing.md).

**This chapter settles:**
- the lane-state provider `lane_state`, under B1 and B2;
- every carrier's fate;
- LS2;
- recovery at each effect boundary;
- LS10 at the state level;
- risk 7's dual-path census.

Its slice is **representation only** (B12): today's flow moves onto it with
the same behaviour, and it adds no locking, minting authority or archive
ordering. Those belong to chapter 4.

## 1. Derived state, recorded decisions

- **The rule (B1).** A lane's state is computed on every ask, from two inputs:
  - committed evidence: trees, trailers, refs and files;
  - live ownership: a held kernel lock or a child process.

  Nothing records that a lane *is in* a state. A committed record carries
  only a **decision**: an outcome, a verdict, a merge action or a resolution.
  This keeps two existing contracts true:
  - "no state file" (`dispatch.py:682-690`; IF-136 at `lane.py:28-42`);
  - SR-156's "reconstructing claim and queue state from version-control
    history alone at any crash boundary".
- **What a state means.** It names the stage whose work is owed next, or is
  running now. `ARCHIVE` is the last stage. When it completes, the lane is
  `closed` and leaves nothing to derive from.
- **B2, tree identity.** The landing reproduces the refreshed lane tree byte
  for byte, and `Bar-Green` names that tree (`integrate.py:9-14`;
  `kitlib/verdict.py:414-461`). So `MERGE` and `ARCHIVE` are never written into
  a tree, and every decision the landing depends on is committed in the lane
  before the final bar. Today's merge intent already obeys this: it is the
  outcome folder the lane moved its specs into (`kitlib/station.py:99-129`),
  committed before the refresh.
- **A change to B2, stated.** B2 says `MERGE` is "derived from git ancestry".
  - OI-103 Q4 makes every landing a squash, and a squash leaves the lane tip
    out of trunk's ancestry.
  - So `MERGE` is derived from **trunk's tree** instead: each spec the tip
    holds in a terminal folder sits at the same path on trunk. (Until claims
    move lane-side, [chapter 4 §3](4-adjudication-mint-landing.md#3-every-trunk-writer-today-and-where-it-moves),
    trunk's `docs/work/active/<branch>/` is also gone; after it, trunk never
    holds one.)
  - This holds for `--no-ff` and squash alike, and it needs no history walk.
  - Ancestry is kept where it stays true: an archived tip is reachable from
    `archive/lanes`, a chain of two-parent `archive: <branch> at <sha>`
    commits.
  - The squash's `Lane-Tip:` trailer (chapter 4 §6) is the landing audit's
    link from the squash to its attested tip. It is not a state input. This is
    the one derivation both chapters use ([README](README.md#changes-to-existing-rulings)).

**Where each record lives, and which checkout writes it:**

| Record | Kind | Lives | Writer (checkout) | When |
|---|---|---|---|---|
| Claim | evidence | the branch ref (created only if absent) whose first commit moves the spec into `active/<branch>/`; trunk keeps it in `queued/` until the landing | lane-side, under the station authority ([chapter 4 §3](4-adjudication-mint-landing.md#3-every-trunk-writer-today-and-where-it-moves); OI-103 Q1). Today: trunk, via `bookkeeping.commit` (`integrate.py:814-896`), which the provider slice keeps unchanged | birth |
| Build done per WI | evidence | `WI:`, or `Blocked-WI:`+`BlockRef:` (`agent_common.py:790-830`) | lane, builder | each WI's last commit |
| Outcome (= merge intent) | decision | the spec's terminal folder on the branch | lane: builder, or machinery (`handback`) | before refresh |
| Per-close report, quarantine patch | decision | `docs/handbacks/`, `docs/work/handback/` | lane, machinery, in the move's commit | close |
| Review verdict | decision | `docs/reviews/<tag>/` + `Review-Verdict:` | lane, reviewer + telemetry commit | round |
| Decisions record | decision | `docs/decisions/<branch>.toml` | lane, session | before close |
| Session log | evidence | `docs/iteration/` | lane (keep-warm logs land on trunk today, `dispatch.py:1370-1377`; chapters 2 and 4 move them) | after each call |
| `Bar-Green` refresh commit | evidence | lane tip | lane, refresh | last |
| Merge action, resolution, mint dispositions | decision | the **sitting record**: typed `[merge_action]`, `[resolution]` and `[consumption]` blocks in the adjudicator's lane verdict file ([chapter 4 §4.1](4-adjudication-mint-landing.md#41-refresh-and-resolve-ls5-oi-103-q3)) | lane, adjudicator, in its ADJUDICATE range | before the final bar (B5) |
| `MERGE` done / `ARCHIVE` done | derived | trunk tree / `archive/lanes` + refs + worktree list | never written | — |

## 2. The provider

It has two homes, the split WI-483 already uses for outcomes (`station.py:175-186`
decides, `integrate.branch_outcomes` reads):
- **`kitlib/station.py` (pure):** the enums and `state_of`. No I/O.
- **`scripts/lane_state.py` (effects):** gathers evidence and is the one door
  for lifecycle effects. It ranks below `dispatch` and above `lane`, `handback`,
  `integrate` and `intake` in `tests/test_import_layers.py:104-110`.

```python
# kitlib/station.py
class LaneState(StrEnum): PLANNING, BUILD, REVIEW_REWORK, ADJUDICATION, MERGE, ARCHIVE
class Substate(StrEnum):  SINGLE, DUAL_DRAFT, DUAL_CROSS_CRITIQUE, DUAL_ARBITRATION,
                          LOCK, REFRESH, RESOLVE, JUDGE, MINT, MERGE_ACTION
class Condition(StrEnum): LIVE, PARKED, REVIEW_OWED, REWORK_OWED, UNCOMMITTED,
                          STASHED_LEFTOVERS, INTERRUPTED_REFRESH, ABANDONED_CLAIM,
                          QUARANTINED, UNLOAD_INCOMPLETE, SESSION_UNACCOUNTED
def state_of(ev) -> tuple[LaneState, Substate | None, frozenset[Condition]]

# scripts/lane_state.py
LaneView(branch, wi_ids, kind, outcomes, state, substate, conditions, closed, evidence)
derive(root, branch, live=None) -> LaneView     # live = the dispatcher's Popen handles
census(root, live=None) -> list[LaneView]       # every lane with a claim dir, ref or worktree
decide(root, branch, decision) -> (sha, refusal)          # the ONE setter for decisions
enact(root, branch, transition) -> (LaneView, refusal)    # the ONE door for effects
on_worker_exit(view, code) -> Decision | None   # pure; today's dispatch._lane_close mapping
```

- **Liveness.** In the dispatcher it comes from the handles it holds. Anywhere
  else it is a non-blocking probe of the lane worktree's `out/agent-loop.lock`,
  which the worker holds for its life (`agent_loop.py:3387-3398`) and the OS
  frees on death. Hand lanes hold no lock, so their liveness is reported as
  unknown until risk 8 moves hand sittings onto `ask`
  ([chapter 2](2-sessions-routing-accounts.md)).
- **`decide` covers machinery decisions.** It checks admission, then calls
  today's writer unchanged: `close_partial` (`handback.py:449`), `quarantine`
  (`:927`) and `close_adjudication` (`:857`).
- **Session decisions keep their own commits.** A builder's move, a reviewer's
  verdict and an adjudicator's block are committed by the session, then
  admitted after the fact by the range rules: S9 `review_scope_refusal`, and
  S11 §4.7's ADJUDICATE rule (chapter 4). Routing them through `decide` would
  change every session's commit path.

### 2.1 Admission, per transition

| Transition | Effect or decision (owner, unchanged) | Admitted when |
|---|---|---|
| birth → `PLANNING`/`BUILD` | claim (`integrate.py:738-811`) | today's `_claim_refusal` ladder; the planning declaration is [chapter 3's](3-planning-tiering.md) |
| `PLANNING` → `BUILD` | plan accepted (chapter 3) | an accepted-plan artifact names the WI |
| `BUILD` → `REVIEW_REWORK` | derived | every assigned WI's newest trailer in `base..tip` is `WI:` (`agent_common.py:822`) |
| in `REVIEW_REWORK` | a round or rework | `REVIEW_OWED`: a declared phase has no verdict at the governing identity (`kverdict.phases_owed`). `REWORK_OWED`: the newest round there is CHANGES-REQUESTED |
| → `ADJUDICATION` | derived | no spec is left in the tip's `active/<branch>/`, each spec names one outcome (`branch_outcomes`), and `_verdict_gate` passes (chapter 4 §4.1 later also admits a CHANGES-REQUESTED whose every finding is disputed) |
| `ADJUDICATION.REFRESH` → `MERGE` | `integrate.refresh` (`:2592`) | `_merge_ready`: trunk is an ancestor, and a verified `Bar-Green` (`:2731-2748`) |
| `MERGE` → `ARCHIVE` | `integrate_one` (`:2912`) | `_merge_refusal` is clear and the slot is held (the station authority, after S788-station-authority) |
| `ARCHIVE` → closed | `_unload_branch` (`:2207`) | landed (§1); the worktree is clean apart from declared residue |
| decide `partial` | `close_partial` | `on_worker_exit` yields a decided outcome (`dispatch.py:565-574`), and the lane is not finished |
| decide quarantine | `quarantine` | a red refresh on an outcome other than `merged`, and no patch yet for the branch. This replaces the in-memory `retried` |
| decide adjudication close | `close_adjudication` | an adjudication-kind lane, a DONE worker, not finished (`dispatch.py:722-740`) |

**Today's flow on these states:**
- `ADJUDICATION` runs only `REFRESH`.
- `MERGE_ACTION` is already satisfied by the outcome folder.
- `LOCK`, `RESOLVE`, `JUDGE` and `MINT` stay empty until chapter 4.
- An adjudication-kind row's sitting derives as that lane's `BUILD`.

## 3. Carrier inventory

Each carrier's fate is one of three:
- **evidence**: it stays as an input to `derive`;
- **fold**: its logic moves into the provider;
- **retire**: it is deleted, with nothing kept beside its replacement
  (risk 7).

| Carrier | Fate | Note |
|---|---|---|
| Spec folder (`queued/`, `active/<branch>/`, terminal) | evidence | claim, outcome, landed |
| `WI:`, `Blocked-WI:`/`BlockRef:`, `Review-Verdict:`, `Bar-Green:` trailers | evidence | |
| `Loop-Session:` | evidence of provenance (SR-209) | not state |
| Session logs, verdict files | evidence / decision | attribution is [chapter 2's](2-sessions-routing-accounts.md) |
| `out/review-owed` (`agent_loop.py:2909-2948`) | **retire** | owed-ness is already "the evidence decides, alone" (`:3084`); `family` already falls back to the build's log (`last_build_family`); `base` comes from `claim_base` (`agent_common.py:1239-1301`). Behaviour changes only for an unclaimed manual worker on the primary checkout, which OI-103 Q1 removes. TC-205 amended |
| `out/agent-loop.lock` | evidence (live ownership) | kept |
| `out/integrate.lock` | evidence (live ownership) in the provider slice; then **retire** | chapter 4 §2 folds it into the station authority (S788-station-authority); two locks over one decision is risk 7's dual path |
| Worker exit codes (`dispatch._advance`) | fold | a report about the process, read once by `on_worker_exit`; never stored |
| Dispatcher lane table (`dispatch.py:692-700`) | fold, partly | `phase`, `exclusive` and `retried` are derived; it keeps `proc` and the stall baseline `head` |
| Two "review owed" readers (`dispatch._round_owed` `:118-166`; `agent_loop.review_owed_by_evidence` `:2969`) | fold | one `REVIEW_OWED` over one `kitlib.verdict` reader, so `lane_state` never imports `agent_loop` |
| `dispatch.py` | stays the scheduler (LLR-149) | `_parked_branches`, `_round_owed`, `_branch_exclusive` and `_lane_close` fold |
| `lane.py`, `handback.py`, `bookkeeping`, `trunk_step`, `spec_move` | effect owners | called through `enact`/`decide` |
| `integrate.py` | effect owner | its tree readers (`finished_branches`, `branch_outcomes`, `claimed_ids_on_branch`, `_claimed_specs`) move to `lane_state` with their callers, with no alias left |
| `agent_loop.py` | the worker | `resume_owed_round` reads `REVIEW_OWED` |
| `intake.py` | effect owner | its post-merge mint is reached via `enact(MERGE)`; chapter 4 folds it into the landing |
| `schedule.py` | unchanged | readiness comes before a lane exists |
| `docs/id-watermark`, `last_approved/acts.toml`, plan artifacts, session leases | evidence | owned by chapters 4, 4, 3 and 2 |
| Branch refs, `archive/lanes`, `git worktree list` | evidence | liveness comes from the inventory, never a path convention (hand lanes live in `ai-template.wt/`, loop lanes in `-drive/`, `integrate.py:207`) |
| Uncommitted or stashed residue | evidence | conditions (§5) |

## 4. LS2

| Today's word | Is | Evidence |
|---|---|---|
| Parked (crash, preflight) | condition `PARKED` | a claim, no live owner, not finished (or finished with a round owed) |
| Parked (review owed, no reviewer) | `REVIEW_OWED` on `REVIEW_REWORK` | committed evidence only |
| Parked (rate limit) | not lane state | a waiting worker is `LIVE`. Exit 5 hands back today (`dispatch.py:565-574`); that is unchanged and is the owner's open call at `:536-550` |
| Handed back / partial | a **decision** (outcome `PARTIAL`) | the lane still runs `ADJUDICATION` → `MERGE` → `ARCHIVE`; `partial/` is then the row's registry status |
| Claimed | not a state | birth evidence. Today a ref with no trunk claim is `ABANDONED_CLAIM` (`integrate.py:395-464`). Once the claim is one create-only ref write in the lane (chapter 4 §3), that shape cannot arise and the condition retires with S788-station-authority |
| Quarantined | decision + `QUARANTINED` | the patch file |

## 5. Recovery at every effect boundary

OI-103 Q6: today's agent-judged recovery stays. The provider *sees* each crash
shape by deriving it, and adds no repair.

| Boundary | Today's order | A crash after it derives as | Recovery (kept) |
|---|---|---|---|
| Lease: dispatch or slot lock | kernel locks the OS frees (`agent_common.py:946-976`) | no `LIVE` owner | none needed |
| Lease: retained session | expires by time (`session_keep.py:475-493`) | the session retired; the lane resumes, the session does not (B9) | chapter 2 |
| Trunk advanced: claim | scratch → object → branch cut (`integrate.py:865-871`) → drift check → install → `update-ref` (`bookkeeping.py:68-80`) | `ABANDONED_CLAIM` between the cut and the advance; `BUILD` with no worktree after | `_drop_abandoned` re-cuts (`integrate.py:554-595`); `ensure_worktree` at launch |
| Process: worker | holds the lane's `agent-loop.lock` | `PARKED`, + `UNCOMMITTED` if dirty | relaunch, with the reconcile note (`agent_loop.py:341-346`) |
| Process: judging session | stash on dirt (`agent_loop.py:2414-2429`) | `STASHED_LEFTOVERS` | the named stash |
| Process: refresh | `merge --no-commit` (`integrate.py:2570`) → trunk step → bar → commit | `INTERRUPTED_REFRESH`; the next refresh refuses it as dirty (`:2446-2453`) | **gap**: F1 |
| Process: model session, hard kill | the log is written after the call (`session_service.py:304-339`) | `SESSION_UNACCOUNTED` (a launch note with no log) | U1 harvest, [chapter 2](2-sessions-routing-accounts.md) |
| Trunk advanced: landing | merge (`integrate.py:2962-2986`) → unload → intake mint, a second trunk commit (`:3008`) | landed + `UNLOAD_INCOMPLETE`; a mint owed | **gap**: "nothing ever retries" the unload (`:2918-2922`), and the mint is recovered by hand (`intake.py sweep`). `census` now sees the lane. Chapter 4 folds the mint into the landing (Q1) |
| Worktree removed | `branch -d`, else `worktree remove` → `prune` → `branch -d` (`:2207-2300`) | `ARCHIVE` owed | re-run unload. Chapter 4 orders the `archive/lanes` write first (Q4) |

**The U1 hook (chapter 2 owns U1).** The provider guarantees one thing: no
`enact` or `decide` effect that drops commits or untracked logs runs before
chapter 2's harvester has taken their usage. Those effects:
- the reset in `quarantine`;
- a dropped act (S11 §3.8);
- `branch -D` of a lane holding sessions;
- `worktree remove` with `out/run-logs/`.

`SESSION_UNACCOUNTED` calls the same harvester before any relaunch.

## 6. LS10 at the state level, and B9

- **A lane resumes from evidence.** `census` derives each lane, and the
  dispatcher relaunches the stage that `state` names. Nothing else is stored,
  so nothing can disagree with the evidence. LS10's "same commit" promise is
  moot, and B1 supersedes it.
- **Uncommitted work in a worktree (Q6, agent-judged):**
  - the relaunched session gets today's reconcile note: commit what is
    complete, discard the rest, log which;
  - judging sessions' leftovers are stashed by name;
  - a decided handback commits the residue as is (`handback.py:415-446`).
- **A correction to the spec.** LS10 says "today's refresh resets". It does
  not reset uncommitted work. It **refuses** a dirty lane
  (`integrate.py:2446-2453`), and resets only its own disposable refresh commit
  (`:2412-2464`).
- **The session resumes** only when its id and ownership are valid under the
  reset terms (B9). That is [chapter 2's](2-sessions-routing-accounts.md)
  design.

## 7. Risk 7: the dual-path census

**Not a dual path:** "a second recording wrapper". `session_service.record`
(`session_service.py:304-339`) is the only session-log writer.

| # | Dual path | Verdict → successor |
|---|---|---|
| D1 | The SN-028 one-word config window (`agent_policy.py:365-391`), with its copies in `subagent_gate.py:306-311`, `gen_okf.py:174-185`, `check_trajectory.py:471-480` and `check_privacy.py:303-319`, and its guard `config_conflicts` (`agent_policy.py:1218-1265`) | **retire**; the RESYNC step runs `bootstrap.py:1295 migrate_legacy_config` → S788-retire-legacy-config-and-carriers |
| D2 | Approval-dial spellings (ordinal, `human_ratification_through`, the `gate_policy` enum): `kitlib/authority.py:117-219`, `agent_policy.py:415-551, 824-842, 1022-1033` | **retire** the translations; keep `dial_from_config` (`authority.py:160-172`), which reads history → same row |
| D3 | `gates =` vs `from-stage =` (`kitlib/config.py:281-365`); retired bar aliases, duplicated at `integrate.py:1812-1843` and `intake.py:196-226` | **retire** → same row |
| D4 | Raw `[stack] test` vs `[product] test` (`agent_common.py:502-538`), unwarned | **retire** → same row |
| D5 | `weak`/`quick`, `Provider`/`Family`, `--provider` (`agent_route.py:121-126, 247-265`; `score_reviews.py:90-91`) | **retire** → same row |
| D6 | CSV/markdown carriers beside TOML (`spine_carrier.py:537-542, 657-738, 938-1110`), their probes (`intake.py:1668-1680`, `integrate.py:1861-1882`, `kitlib/stage.py:140-144`, `trunk_step.py:498-580`) and `agents.csv` (`agent_route.py:233-305`) | **retire** the runtime readers. `migrate_carrier.py` stays as the one-shot converter the RESYNC runs → same row |
| D7 | Dead CSV arm, `intake.py:2706-2760` (its writer is gone) | **retire** → S788-retire-runtime-dual-paths |
| D8 | `work-items.csv` reads (`trunk_step.py:411-415`, `traj_parse.py:353`, `rendering/traj_panels.py:594`), while `check_trajectory.py:541` errors on that file | **retire** → same row |
| D9 | The open item in `needs` (`kitlib/spine.py:204-243`; `schedule.py:481-496`) vs the `wi_refs` hold (IF-073; `schedule.py:314-324`) | **WI-790 (contract)**: `needs` becomes the one path, `wi_refs` retires, TC-253 is amended |
| D10 | The hand-written review rollup window (`integrate.py:1394-1442, 1536-1558`) | **retire** (nothing in the kit writes it) → S788-retire-runtime-dual-paths |
| D11 | Two terminal homes, `docs/work/<t>/` and `docs/archive/work/<t>/` (`integrate.py:186-191, 988-1030`; `kitlib/registry.py:276-286`; `intake.py:947-957`). Live: `docs/work/complete/WI-689-*.md` (`0ded5c77`) | **retire**: move WI-689 and drop the second read → same row |
| D12 | The lock runs unguarded on ENOLCK/ENOTSUP (`agent_common.py:946-976`) | **retire**: fail closed, naming the filesystem (an environment failure surfaced, per LS9). The station authority is chapter 4's (B4); this covers the per-worktree lock → same row |
| D13 | Name shims: `_name_status` (`integrate.py:390-392`); re-exports kept "so no caller had to move" (`dispatch.py:998-1001`, `handback.py:140-143`, `integrate.py:215-216`) | **retire**: the re-exports → S788-lane-state-provider; `_name_status` → S788-retire-runtime-dual-paths |
| D14 | Two review-owed readers, plus the marker (§3) | **fold** → S788-lane-state-provider |
| D15 | Managed vs unmanaged routing (`agent_loop.py:2398-2400, 3476-3507`) | [chapter 2](2-sessions-routing-accounts.md): `ask` owns routing |
| D16 | `claim_base` vs merge-base for a manual worker (`agent_common.py:1239-1301`) | **justified** until hand sittings run on `ask` (risk 8) and OI-103 Q1 leaves no unclaimed work; re-judged there |
| D17 | Retention records without `rollout_requests` (`session_keep.py:719-721`) | chapter 2's session store; the RESYNC resets the store |
| D18 | Speculative vs in-slot refresh (`dispatch.py:243-283`; `integrate.py:2942-2958`) | **justified**: both run in production; the in-slot refresh is the race's loser, not a fallback |

## 8. Findings outside this slice

Each is surfaced here and not fixed in this design.

- **F1. An interrupted refresh wedges the lane.** A refresh killed after
  `merge --no-commit` leaves the worktree mid-merge. The next refresh refuses
  it as dirty, and a person must run `git merge --abort`. The fix: the refresh
  aborts its own unfinished merge, identified by a `MERGE_HEAD` that equals a
  trunk commit with no other change. It belongs in chapter 4's landing rows.
  UNVERIFIED by probe.
- **F2. Nothing retries an incomplete unload.** `census` now shows the lane.
  Who retries it belongs to chapter 4's archive ordering.
- **F3. `refs/stash` is one per repository.** So a lane's named leftovers stash
  is visible from every worktree. UNVERIFIED by probe.

## 9. Closing sections

### 9.1 Matrix rows

| Item | Kind | Action | Why | Successor |
|---|---|---|---|---|
| SR-156 | row | preserve | B1 realizes "reconstruct ... from version-control history alone" | — |
| SR-144, LLR-144, LLR-161, IF-137, SR-148, LLR-149, LLR-262 | row/contract | preserve | the writers, admission and S9 are unchanged; only callers move | — |
| LLR-140 | row | amend `code_symbol` and detail | `finished_branches` moves out | S788-lane-state-provider |
| LLR-150, IF-136 | row/contract | amend | the requestor becomes `scripts/lane_state` | S788-lane-state-provider |
| IF-173 | contract | amend | the readers leave its data; `lane_state` joins its requestors | S788-lane-state-provider |
| LLR-182 | row | amend: add SR-156; `code_symbol` += `LaneState/Substate/Condition/state_of` | the vocabulary keeps one home | S788-lane-state-provider |
| new LLR (`module` `scripts/lane_state.py`, SR-156); new IF (owner `lane_state`, requestors `dispatch`, `agent_loop`); new TCs (`state_of` per state, one fixture per §5 shape) | row/contract | add | the provider | S788-lane-state-provider |
| TC-205 | row | amend `method` | the stale-marker case becomes "evidence only" | S788-lane-state-provider |
| TC-132, TC-143, TC-144 | row | amend only if a cited test moves | confirm at build | S788-lane-state-provider |
| `tests/test_import_layers.py` `LIFECYCLE_RANK`; `dispatch`, `lane`, `integrate`, `handback`, `agent_loop`, `kitlib/station`, `kitlib/verdict` | module | amend | §3 | S788-lane-state-provider |
| `docs/runtime-flows.md` (lane lifecycle), `docs/iteration/wi-lifecycle.html`, `docs/registry-machinery-reference.md` | doc | amend | name the provider and its states | S788-lane-state-provider |
| `docs/concurrency-v2.md` §A4.2 "no state file" | doc | preserve | still true | — |
| PROCESS.md lane lifecycle; GLOSSARY (lane state, condition, decision) | doc | amend | the states are named once | S788-glossary |
| SR-027, LLR-029, LLR-030 | row | amend | D12 | S788-retire-runtime-dual-paths |
| LLR-140 (rollup window) and its TC; IF-023 (`docs/work/README.md`) | row/contract | amend | D10, D11 | S788-retire-runtime-dual-paths |
| SR-006, SR-137, SR-139, SR-147, LLR-155, LLR-277, LLR-291, IF-079 | row/contract | amend the cells that state a dual read (which ones: UNVERIFIED) | D1–D6 | S788-retire-legacy-config-and-carriers |
| TC-253, LLR-058, IF-073 | row/contract | amend | D9 | WI-790 |

### 9.2 Proposed successor rows

**S788-lane-state-provider:** the lane-state provider, representation only.
- **Scope:**
  - the station enums and `state_of`;
  - `scripts/lane_state.py`;
  - `dispatch`, `lane`, `handback`, `integrate` and `agent_loop` moved onto it;
  - `out/review-owed` retired, the review-owed readers made one, and the D13
    re-exports removed.
- **Done-when:**
  - every §2.1 transition and decision goes through `enact` or `decide`, and no
    lifecycle module calls another's effect directly;
  - there is a pure test per state and per condition;
  - a repo fixture covers each §5 crash shape;
  - the existing `test_dispatch`, `test_integrate_*`, `test_handback*` and
    `test_agent_loop_*` suites pass with only call sites edited;
  - no new lock, mint or archive ordering is added;
  - the import rank is enforced.
- **needs:** S788-glossary.
- **BuildTier:** strong.
- **Test bar:** the affected modules plus the smoke tier.
- **RESYNC:** yes. Kit-owned files only; a stray `out/review-owed` is ignored.

**S788-retire-runtime-dual-paths:** retire the dual paths that need no
adopter migration.
- **Scope:** D7, D8, D10, D11 (moving WI-689), D12 and `_name_status`.
- **Done-when:**
  - each path is deleted, and its tests become refusal tests;
  - a lock on an unsupported filesystem exits with the filesystem named;
  - nothing reads `docs/work/<terminal>/`.
- **needs:** S788-lane-state-provider (both edit `integrate.py`).
- **BuildTier:** medium.
- **Test bar:** the affected modules plus the smoke tier.
- **RESYNC:** yes. It names the end of the rollup window and the lock refusal.

**S788-retire-legacy-config-and-carriers:** retire the SN-028 window and the
non-TOML carriers.
- **Scope:** D1 to D6.
- **Done-when:**
  - the runtime reads only `process.toml`, `[product]`, `from-stage` and TOML
    carriers;
  - the RESYNC entry runs `migrate_legacy_config` and `migrate_carrier.py`;
  - a scaffold bootstrapped from an old-form fixture migrates and passes
    `check.py`;
  - the amended rows pass in-lane adjudication.
- **needs:** S788-accounts (both edit IF-045 and `agent_route`; chapter 2 §7's
  CSV-reader and `Provider`/`weak` retirements are built here).
- **BuildTier:** strong.
- **Test bar:** the affected modules, the smoke tier, and one scaffold
  bootstrap.
- **RESYNC:** yes. **It forces migration** on un-migrated adopters (Q-1).

### 9.3 Questions for the owner

(Consolidated as [README Q-1](README.md#questions-for-the-owner-at-the-checkpoint).)

**Q-1. Retiring D1–D6 makes every adopter still on one-word config files or
CSV/markdown carriers run the migrators at their next resync.** Risks 7 and 9
already say to retire them, with the RESYNC entry as the migration. CLAUDE.md
asks that a forced downstream migration be flagged, so it is flagged here.
- **(a) Retire in one row, with RESYNC running both migrators.**
  Recommended.
- **(b)** Keep D6 for one more kit release, as a named and justified
  exception.

Nothing else here needs the owner; the calls are logged in §10.

### 9.4 Research record

**Read in full:**
- the brief;
- `CLAUDE.md`;
- the WI-788 spec;
- `sol-review.md`;
- the S11 plan;
- the OI-103 log fragment and its `decision` cell
  (`docs/requirements/open-items.toml:3813-3821`).

**Read in part** (the ranges cited above):
- all of `dispatch.py` and `lane.py`;
- `integrate.py`;
- `bookkeeping.py`, `handback.py`;
- `kitlib/station.py`, `kitlib/verdict.py`;
- `agent_loop.py`, `agent_common.py`;
- `session_service.py`, `session_keep.py`;
- `schedule.py`;
- `tests/test_import_layers.py`.

**The census:** a read-only search agent swept `scripts/` for legacy, fallback,
compatibility and dual-carrier reads. Each line a verdict rests on was then
re-read: `agent_policy.py:386-391`, `schedule.py:486-497`,
`integrate.py:390-393, 1394-1400`, `trunk_step.py:409-416`,
`intake.py:2745-2760`, `agent_common.py:960-970, 1240-1250`.

**Probes (each exited 0):**
- `git log --oneline -5 archive/lanes`: `b574535c archive: build/wi-787 at
  c3fc567a`.
- `git log --format=%P -1 archive/lanes | wc -w`: `2`.
- `ls docs/work/complete`: `WI-689-adjudicate-queue-overlap-af58.md` (last
  commit `0ded5c77`).
- `git worktree list`: hand lanes live at `C:/Projects/ai-template.wt/<branch>`.
- `grep -rn "archive/lanes" project-trajectory/scripts`: no hit, so only the
  hand path keeps that ref today.
- A `tomllib` read of SR-144/156, LLR-140/150/182, IF-073/080/093/136/137/173/186
  and TC-132/143-148/205/253/278 checked the cited cells.

**UNVERIFIED:**
- F1, from reading `integrate.py:2570, 2446`;
- F3, from memory of git-worktree(1);
- whether a non-blocking probe of `out/agent-loop.lock` can make a concurrent
  real acquirer refuse during the probe on Windows. The dispatcher avoids the
  probe by passing `live`;
- which cells in the D1–D6 rows state the dual reads.

## 10. Calls no spec or ruling settles

| Decided | Alternative | Reversal cost | Why not escalated |
|---|---|---|---|
| A state names the stage owed next; `ARCHIVE` plus a `closed` flag | add a `DONE` state | low | the owner's list has no terminal value, and this adds none |
| `MERGE` is derived from trunk's tree, a change to B2 | keep ancestry and add a squash trailer | low | Q4's squash makes B2's wording false, and the evidence already exists |
| Session decisions are admitted after the fact, by the range rules | route every session commit through `decide` | medium | B12: representation only |
| Pure `state_of` in `kitlib/station.py`, effects in `lane_state.py` | one module | low | WI-483's existing split for `outcome_of` |
| Liveness from the handles, else a lock probe | the pid in the lock file | low | the pid is "DIAGNOSTICS only" (`agent_common.py:851`) |
| Retire `out/review-owed` in the provider slice | keep it until chapter 2 | low | both its fields have committed sources; LS1 retires markers |
| D12 covers the per-worktree lock too | justify it | low | the no-degenerate-mode rule, and LS9 |
| D16 justified for now | retire now | low | unclaimed manual workers exist until risk 8 and Q1 land |
