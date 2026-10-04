# Chapter 4: adjudication, mint and landing authority

**Status:** design for the owner's checkpoint ([README.md](README.md)). Read-only against lane base
`c3be7be0`; nothing here is built. Code cites are `path:line` under
`project-trajectory/scripts/` unless another root is given.

**Base.** This chapter builds on the S11 plan's §6 as ruled
([plan](../2026-10-03-s11-in-lane-adjudication.md); OI-101 Q6). It applies:
- OI-101 Q1 and Q2;
- OI-103 Q1 to Q4;
- B3 to B6, and B10.

Neighbouring chapters own:
- state derivation and records: [chapter 1](1-state-evidence-recovery.md);
- `ask`, session families and the session lease:
  [chapter 2](2-sessions-routing-accounts.md);
- planning: [chapter 3](3-planning-tiering.md).

**It amends S11 in five places** (§8 states each):
- §4.1's freshness rung is replaced by the authority;
- §4.2's filter becomes a drift reading;
- §4.6 changes for spine text;
- step 9's `--no-ff` becomes a squash;
- the post-merge mint moves before the merge.

## 1. The sitting, end to end

```
REVIEW_REWORK done (APPROVE, or every open finding disputed)
 LOCK          the session leases (waited for holding nothing), then one
               non-blocking try of the station authority (§2)
 REFRESH       merge trunk in, trunk_step, commit-tier bar
 RESOLVE       rule each recorded dispute            } one retained
 JUDGE         acts on the previewed scope            } adjudicator
 MINT          consume every item, consolidate, allocate
 MERGE_ACTION  merge | merge-partial | cancel | return
   final evidence: independent review, regen, declared bar (§5)
 MERGE         squash under the authority             } mechanical
 ARCHIVE       archive/lanes, branch, worktree        }
 release (after ARCHIVE; at once on `return`)
```

A lane with nothing to rule (no dispute, an empty preview, an empty consumption
list) launches no session. The same states run with empty inputs. This is the
one path with zero items, not a second mode.

## 2. One station authority (LS4, B3, B4; OI-103 Q1)

OI-103 Q1 (ruled): nothing the tool runs writes to trunk except through a work
item's merge, under complete writer exclusion. The **station authority** is the
one exclusion that every such writer takes.

- **A lease record, not a kernel lock.** A sitting spans many processes, and the
  hand path has no long-lived one, so no file descriptor can hold it.
- **One canonical location:** `out/station/authority.json` under the *primary
  checkout*. It is resolved through the git common directory, as
  `session_keep.store_dir` already resolves its own path (`session_keep.py:165`),
  so every lane worktree names the same file. It is untracked.
- **Mutation.** Every read-modify-write holds `out/station/.lock`, a kernel lock
  taken non-blocking with a short bounded retry and held for milliseconds.
- **Fail closed.** A filesystem that cannot lock refuses, naming the cause and
  the fix (a local disk). This authority never runs unguarded
  (`agent_common.py:946-957`; chapter 1's D12 retires that arm for the other
  locks).
- **The record's fields:**
  - `holder`: the branch, WI ids, host, pid and kind (`sitting`, `claim` or
    `station-lane`);
  - `generation`: the fencing token;
  - `taken`, `renewed` and `until`.
- **Acquisition order.** Take them in this order:
  1. the process's own `out/agent-loop.lock` (the dispatcher's in the primary
     checkout, the worker's in a lane worktree);
  2. the session leases the sitting needs, [adjudicate] and [adjudication
     review] (chapter 2). This is the only wait (up to 1200 s,
     [chapter 2 §3 step 5](2-sessions-routing-accounts.md#3-the-one-entry-point)),
     and it holds no authority;
  3. the station authority, one non-blocking try. If it is held, the sitting
     releases its leases and re-enters `LOCK` on a later tick;
  4. the millisecond store locks.

  **Nothing waits while holding the authority** (OI-103 Q2). Under it, every
  acquisition is one non-blocking try: a lease found busy then (a keep-warm
  ping) gives that call a fresh, non-replacing session at once. No cycle can
  form, because nothing that holds the authority waits, and nothing that waits
  holds it ([README](README.md#how-the-locks-and-the-lease-compose)).
- **Where it lives.** The authority's code is a lifecycle effect, so it sits in
  `scripts/lane_state.py` (B11), and its CLI is `lane_state.py release
  --reason`. This avoids a second `station` module beside `kitlib/station.py`.
- **Waiting is never blocking.** The dispatcher tries once per tick; a held
  authority leaves the lane deriving as `ADJUDICATION.LOCK` (holder named) and
  the tick moves on. The hand CLI refuses at once, or polls under `--wait`
  holding nothing. Nothing waits inside the merge or the tick. A sitting runs
  in the lane's worker process, so the tick never blocks on one.
- **Ownership transfer** happens only within a lane: the sitting keeps the
  authority through `MERGE` and `ARCHIVE`, so it is held through the trunk
  advance (B3). It is never handed between lanes.
- **Release and cancellation.** The authority is released after `ARCHIVE`, or at
  once on `return` and on a refused `REFRESH`. The owner can cancel with
  `lane_state.py release --reason`, which is recorded. Cancellation, in order:
  1. stop the sitting's process (the holder's recorded pid);
  2. harvest its sessions' usage (chapter 1 §5's U1 hook);
  3. bump `generation`, so the cancelled holder can never land;
  4. clear the record.

  The lane then derives as `PARKED` (plus `UNCOMMITTED` if dirty). Its relaunch
  gets today's reconcile note (OI-103 Q6), and it re-enters `LOCK`. Nothing is
  discarded: a refresh refuses a dirty lane, as today (chapter 1 §6).
- **Expiry.** `until` is the last renewal plus a TTL. The TTL is a dial,
  `[station] authority_ttl_minutes`, shipped at 120: above the p90 sitting on a
  loaded box (below). Every substate transition renews it. An acquirer that
  finds an expired lease retires it, bumps `generation` and records the steal.
- **Fencing.** Every tool advance of a ref (the landing's trunk update, the
  claim's branch create) happens while holding the mutation lock: re-read the
  record, check that `generation` is the caller's, then `git update-ref <ref>
  <new> <old>` (compare-and-swap; `""` as `<old>` for a create), then release.
  The check and the advance are one critical section, so an expired or
  cancelled holder can never land, and no tool writer can slip between them.
- **Risk 5.** A fresh, non-replacing session drawn after the 20-minute lease
  wait still takes the authority afterwards, by the same non-blocking try: the
  authority is the lane's, the lease is the session's.
- **`out/integrate.lock` retires** (`integrate.py:3016-3030`). Its exclusivity
  is the authority held for the merge, and two locks over one decision is the
  dual path that risk 7 forbids.
- **Who is outside the tool.** Only the owner's own commits (OI-103 Q1: "the
  user might approve an item, but that generally not be done while the thread
  is running"). A coordinator session is an agent, so everything it writes to
  trunk lands through a work item's lane under the authority, like any tool
  writer: filing rows, recording rulings, status and log fragments go through
  a station lane (Q-4.1). The one coordinator write that cannot wait for a
  landing is the pause file, which must stop claims at once; that is an owner
  question (README Q-12).
- **The owner's own trunk commits.** The pre-commit hook refuses one while a
  holder has the authority. That check is advisory: the owner's commit is not
  the tool's, and the exclusion that matters is the landing's compare-and-swap
  above. If the owner's commit (or a `--no-verify` one) moves trunk under a
  sitting, the landing's swap fails, naming the foreign commit; the lane re-runs
  `REFRESH` inside its own authority, and a session retakes any stale act (S11
  Q6).

**Expected hold time.** The session figures are measured from session logs; the
bar times are from CLAUDE.md:

| Lane | What runs inside the authority | Median | p90, loaded box |
|---|---|---|---|
| No adjudication input | the `REFRESH` smoke (~0.5 min) and the final declared bar (~10 min) | ~11 min | ~40 min |
| Spine or handback | plus one adjudicator session (median 5.5 min, p90 15.5) and the final review (median 7.5, p90 17) | ~25 min | ~75 min |
| Each inner spine round (§7) | plus a reviewer edit and a final pass | +~13 min | +~30 min |

Merges serialize for that long, and claims wait too: Q1 (a) names claims. Lanes
already building keep building.

**When the authority replaces S11 §4.1's freshness rung:** only once every
writer in §3 has moved (B3, B11). The proof needs no new rung. The landing's
compare-and-swap and today's ancestor check (`integrate.py:1648`, `:2731`)
refuse any trunk move the authority did not make, naming the foreign commit.
The landing has one answer to that refusal, whoever moved trunk: the lane
re-runs `REFRESH` inside its own authority, and a session retakes any stale
act (S11 Q6). Under full coverage only the owner's own commit (above) can
cause it. A foreign commit the tool made exposes a defect, a writer the
authority does not cover; the fix moves that writer (the writer census,
S788-dual-pickup) and adds no second answer for it.

## 3. Every trunk writer today, and where it moves

| Writer | Today | Moves to |
|---|---|---|
| Claim | `integrate.py:738-896` via `bookkeeping.commit`, under the dispatch lock | **Lane-side**, under the authority (sub-second). No live lane may claim the WI (chapter 1's reader). The branch is a create-only ref (`git update-ref <ref> <sha> ""`; probed: a second create fails). The spec move is the lane's first commit, so trunk keeps the spec in `queued/` until the landing. The authority replaces `_dispatch_lock` (`:598-647`). |
| Post-merge intake mint | `integrate.py:3006-3013` → `intake.py:2373-2401`, a second trunk commit | Into the lane, before the final evidence (§8). |
| CLI mints: `census`, `consolidate`, `rejudge`, `sweep`; the dispatcher's idle arms | `intake.py:2992-3070`; `dispatch.py:1142`, `:1304` | `sweep` retires, because every landing passes the one operation. The rest mint in a **station lane**, which enters at `ADJUDICATION` and lands like any lane (Q-4.1). |
| Plan-artifact allocation | `plan_artifacts.py:258-351`; `log.md` append, `:355` | The decomposition lane's `MINT`, through the one allocator (flow: chapter 3). |
| Keep-warm and trunk-rooted session logs | `session_service.py:333` → `commit_telemetry` on trunk | The untracked spool `out/sessions/spool/` under the primary checkout. The next landing's final `trunk_step` harvests it under the authority, deduplicated by invocation id (U1: [chapter 2 §6](2-sessions-routing-accounts.md#6-u1-the-usage-ledger), which builds the spool in S788-session-store). |
| `trunk_step` (log compile, regen) | bookkeeping scratch and lane refresh | Lane-side only, inside the authority. This amends SR-170: "the serial merge step" becomes "under the station authority, on the tree that lands". |
| Acts (flip and snapshot) | trunk-side adjudication lanes (`integrate.py:1154`) | In the lane, in `JUDGE` (§5, §7). |
| The landing | `merge --no-ff` in the primary checkout (`:2962`) | A squash built away from the checkout and installed by `bookkeeping.py`'s scratch-and-install. That module stays as the landing's install; its claim and mint callers go (§6). |
| Coordinator commits (filing rows, rulings records, status, log fragments, claims by hand) | the hand path, straight to trunk | A **station lane** under the authority, landed like any lane (Q-4.1). The pause file is the open exception (README Q-12). |
| The owner's own commits | the owner, rarely while the loop runs | Outside the tool: the hook's advisory check, and the landing's swap catches a move (§2). |

## 4. The sitting's states

### 4.1 REFRESH and RESOLVE (LS5; OI-103 Q3)

**REFRESH.** This runs before the adjudicator reads anything: merge trunk in, run
`trunk_step`, then the commit-tier bar. The watermark and the queue are then
current, and no test runs on a stale checkout. The full declared bar runs once,
on the final tree (§5). The speculative refresh before the lock
(`integrate.py:2614`) is unchanged.

**The dispute record.** In rework, the builder fixes each finding or disputes it,
with its evidence and one class:
- `refuted`;
- `mitigable-setting`;
- `mitigable-retry`;
- `guard-on-valid-input`;
- `out-of-scope`.

It writes one typed entry per finding, in the lane decision file chapter 1
places. A lane enters `ADJUDICATION` on APPROVE, or on a CHANGES-REQUESTED
whose every finding is disputed.

**RESOLVE.** The adjudicator rules each dispute `uphold`, `dismiss` or `advice`,
with a reason, in the `[resolution]` block of the **sitting record**: the
adjudicator's verdict file in the lane, with typed `[resolution]`,
`[consumption]` and `[merge_action]` blocks. Chapter 1 asked this chapter to
name it.
- **The call is final (Q3).** `_verdict_gate` (`integrate.py:1445`) treats a
  CHANGES-REQUESTED as cleared when a recorded resolution dismisses, or marks
  as advice, every one of its findings. No endorsing review is drawn.
- **Any `uphold` returns the lane.** The sitting's outcome is `return`.
- **`advice` goes to MINT**, as an item on the consumption list.

This replaces the hand path's separate arbiter for these disputes (LS5), and it
changes RULING-7's verdict gate.

### 4.2 JUDGE

**The scope record.** After REFRESH, the provider computes the preview
mechanically and commits it as the lane's **scope record**, before any
adjudicator runs (B6). It covers:
- the merge-base-to-tip range read by `_amendment_drafts` and
  `_first_approval_drafts` (`intake.py:791`, `:895`);
- the close outcome;
- the Done-when changes (`:1165`);
- the clean-close sample (`:1264`).

**The adjudicator then rules:**
- first approvals and amendments, as meaning or clarity, with the act on
  released rungs (§7);
- a `partial` or `cancelled` close, with the disposition brief's four questions
  asked in the lane;
- a builder's edit of its own Done-when;
- a sampled clean close.

Held rungs get a recommendation only. Held-rung CLARITY acts follow WI-791's
contract.

### 4.3 MINT (LS6; R1 amended)

**One allocator.** `intake._mint`'s writer runs in the lane worktree as a lane
commit, at the lane's watermark. The lane is locked and refreshed, so that
watermark is trunk's. `plan_artifacts` allocates through it too. No two
sittings collide, because each sits only after the last has landed.

**The consumption list** is enumerated mechanically, one `C-NNN` per item:
- every per-close report item;
- every `advice` resolution, and every recorded environment failure (§9);
- every spine row left unsettled: returned at exhaustion, held, or blocked by
  foreign drift;
- every lane follow-up. R1's "record it as prose" becomes a typed follow-up
  entry, so it can be counted;
- every re-judge due at the final tree (`rejudge.checkpoint_drafts`;
  mechanical).

**Dispositions.** Each item gets exactly one, in `[consumption]`:
- `open-item`, with its WI-790 placeholder row and table;
- `decision`, an entry in `docs/decisions/<branch>.toml`, which feeds WI-790's
  "Decisions to review";
- `successor`, a draft;
- `no-action`, with its reason.

**Checkable.** The MINT step refuses, and the lane cannot leave it, if any of
these hold:
- the ids in `[consumption]` differ from the list;
- an `open-item` has no table;
- a `no-action` has no reason.

**Consolidation, at the same moment.** The composer supplies the open rows each
draft overlaps, using `consolidate.census_draft`'s clustering over the queue
plus the drafts. The consolidate brief's three shapes (contradiction, overlap,
already answered) fold into the MINT brief. A duplicate becomes a `no-action`
naming its row; an overlap is absorbed through `supersedes`, or gets an edge.

**No waiting (Q2).** Owner-owed items never hold the sitting. They are minted
as placeholder rows and handled after the merge.

**The MINT brief's wording** (the owner asked for it):

> MINT: CONSUME EVERY ITEM. Below is this lane's CONSUMPTION LIST: {n} items,
> each with an id and its source. Nothing on it may be dropped, and nothing
> reaches the owner or the queue unless you route it here. Write exactly one
> entry per item in the `[consumption]` block:
> - `open-item`: only the owner can decide it, or work is blocked until the
>   owner acts. Draft its placeholder row with the four-cell `[open_item]`
>   table.
> - `decision`: it was decided on the owner's behalf, or it is advice the
>   owner may simply take (an environment cause and its recommended setting).
>   Write the entry in {decisions} with its four disclosure fields.
> - `successor`: real work remains. First read OPEN ROWS. If an open row
>   already covers it, write `no-action` naming that row, absorb it, or add an
>   edge. Never mint a duplicate.
> - `no-action`: nothing is owed. Give a reason a reader can check: the commit
>   that fixed it, the row that covers it, or why it is not a defect.
>
> The machinery compares your block with the list. A missing entry, an extra
> entry, an `open-item` without its table or a `no-action` without a reason
> refuses the mint, and this lane cannot merge. Do not group items: one item,
> one entry. Never wait for the owner. Route the item; the owner handles it
> after the merge, through its row.

### 4.4 MERGE_ACTION (LS7)

| Value | Lands as | Note |
|---|---|---|
| `merge` | complete | the settled acts and the mints land with it |
| `merge-partial` | partial (SR-144 report; the keep/discard split is ruled in `JUDGE`) | a successor is mandatory (OI-73). Quarantine is the case with an empty keep set and a `.patch` |
| `cancel` | cancelled | judged never to be built; report and successor as today |
| `return` | nothing: back to `BUILD` with the required fixes | releases the authority at once. The sitting's commit moves the specs back to `active/<branch>/`, so the lane derives as `BUILD` ([chapter 1 §2.1](1-state-evidence-recovery.md#21-admission-per-transition)). A fourth sitting may not return (S11 Q2): see exhaustion below |

**Exhaustion: the fourth sitting, when a return is owed.** S11 Q2's ruled bound
(3 returns, then land) applies to code as well as spine rows, and the red bar is
never waived. The fourth sitting's outcome is `merge-partial`, never `merge`:
- **an upheld code finding, bar green:** the work lands as `partial`, and `MINT`
  mints the mandatory successor (OI-73) carrying each upheld finding as its
  Done-when, with the parent cited in its `needs`;
- **a red bar caused by the lane's own work:** the keep set is empty (the
  quarantine shape): nothing of the lane's code lands, the `.patch` and the
  report land, and the successor carries the patch and the failing bar output;
- **unsettled spine rows:** minted unsettled, as S11 Q2 already rules.

So the lane always leaves the station, and nothing red reaches trunk.

The `[merge_action]` block is committed before the final bar: it is chapter 1's
merge intent (B2). The specs' terminal folders are its effect, written in the
same commit, and the landing refuses a lane where the two disagree. `MERGE`
and `ARCHIVE` then carry it out mechanically.

## 5. Final evidence (B5) and authorization (B6)

**Final evidence.** After the last substantive sitting write, three steps run in
order:
1. **The final independent review** (S11 Q4). It is owed whenever the sitting
   wrote anything, and it checks only the adjudicator's own writes:
   - the acts, against the scope record;
   - `[consumption]`, against its list;
   - the minted rows.

   It never reopens a resolved dispute (Q3). It is never a session that
   authored any range in this sitting (an author-review session included), and
   its family differs from the adjudicator's where the pool allows (chapter 2
   §3 step 2's table). Its range adds only its verdict (S9).
2. **Regeneration and the declared bar** run on the final staged tree, which is
   committed with `Bar-Green`. This is today's sequence
   (`integrate.py:2653-2712`).
3. **Nothing tracked changes after that.** `MERGE` lands exactly that tree.

**The back edge.** A CHANGES-REQUESTED final review drops the offending sitting
commits (their tip archived first, S11 §3.8) and re-enters `JUDGE` or `MINT`,
still holding the authority. This counts as an inner round, bounded at 3. At
exhaustion the acts are dropped and their rows are minted unsettled. A red bar
caused by a sitting write takes the same edge. A red bar caused by the lane's
own work leads to `return`, or at the fourth sitting to §4.4's exhaustion.

**The lock is not authorization.** `merge_approval_refusal`
(`acceptance_record.py:805-818`) takes its scope from claimed adjudication rows
(`first_approval_scope` `:740`, `amendment_scope` `:821`; LLR-278, TC-278). A
build lane claims none, so its scope is empty. The design replaces that source
and keeps every check:

| Check | Kept as |
|---|---|
| Scope | the provider's scope record (§4.2). The merge re-derives it at its commit and compares it byte for byte, so it is independently recorded and tamper-evident |
| Actor independence | each flip and snapshot write lies in a recorded `ADJUDICATE` range whose session is an eligible `adjudicate` draw for the scoped rows under [chapter 2 §3 step 2's table](2-sessions-routing-accounts.md#3-the-one-entry-point): it is a different session from every build, plan and author-review session of those rows; its family follows chapter 2's ranked preferences (not the latest build author's family, then not an earlier one's, an unmet preference recorded per call); and a row whose text its own `author` range wrote is admitted only under B10's exception (an author-review range by another session follows it, and the act's pass changed no byte of it). This replaces `_adjudication_lane` (`integrate.py:1139`) |
| Held-rung authority | `_held_status_refusal` (SR-208), unchanged |
| Named rows, snapshot coverage, out-of-scope acts | `adjudication_approval_refusal` (`:753`) and `reattest_scope_refusal` (`:873`), fed the recorded scope |
| Authority | the act lies after the lane's `LOCK`, under the current `generation` |

## 6. One landing (OI-103 Q4), and the decisions record on every path

**The operation.** The loop and the coordinator both land through `MERGE`
(risk 8; B11):
- One landing per lane, one ref advance by compare-and-swap (§2). Its last
  commit's tree is the final attested tree, and it carries `Lane-Tip:`, every
  item's `WI:` and outcome. For a lane holding one item (every lane except a
  spine batch) that is OI-103 Q4's one squash commit per item.
- **A lane that took an act** collides with risk 6 on trunk (§7, README Q-8):
  under option (a) the landing is two commits in the one ref advance (text,
  then act); under option (b) it is one. This is the owner's ruling to make.
- **A spine batch** (one branch, several WIs sharing one re-attest window,
  `dispatch.py:25-38`) cannot be split per item: its items share one act and
  one tree, and per-WI outcomes already live in each spec's folder. It lands
  as one landing naming every item, which is what the hand path does today
  (`eecd656d` closed nine WIs in one squash). Reading Q4's "per item" as "per
  lane" for batches is README Q-11.
- `ARCHIVE` then appends the two-parent `archive/lanes` commit (the
  `d4b36d71` recipe) by compare-and-swap.
- Only then does it delete the branch and remove the worktree.

**What this changes:**
- RULING-6's `audit` (`integrate.py:3142`): "a product-touching trunk commit is
  a merge" becomes "is a landing commit whose tree equals its `Lane-Tip`'s
  attested tree".
- LLR-140 and IF-080: `--no-ff` and `branch -d` go.
- B2's ancestry: chapter 1 derives `MERGE` from trunk's tree instead.
  `Lane-Tip:` is the audit's link from the squash to its attested tip, never a
  state input (one derivation in both chapters).

**One record check.** `_close_record_refusal` (`integrate.py:2845`) becomes the
landing's single check of the per-close report and the decisions record,
whichever path lands. `ask` hands every delegated session its note
(`kitlib.decisions.session_note`; chapter 2).

**The gap, measured.** Every first-parent commit in `655c60ab^..c3be7be0`
(2026-09-28 to 2026-10-04), with `decision_recording = "record"` set from
`655c60ab`:
- **Records.** 77 commits closed work items, and only 2 carry a record
  (`build-wi-557.toml`, `wi-688.toml`).
- **No loop merges.** All 77 landed by hand, outside the slot's check.
- **Owed and missing: 75** (owed in `kdecisions.owed`'s reading):
  - 34 build lanes;
  - 22 spine-act sittings;
  - 6 re-judges;
  - 6 spot checks;
  - 7 trunk-side closes.

<details><summary>The 75 closing commits with no record (commit: work items)</summary>

eecd656d: WI-682 WI-683 WI-690 WI-691 WI-693 WI-694 WI-695 WI-696 WI-702; 312b2033: WI-706; 32687d47: WI-703; 83d866c8: WI-692; 5934f4c3: WI-707; e7fe487d: WI-704 WI-705 WI-708 WI-709; ec05c5ce: WI-710; cfef8d1d: WI-618; 78fd8fcd: WI-711; 6763d08d: WI-712 WI-714; 3bb6186c: WI-715; b90e84b6: WI-620; e827e697: WI-719; 2d264589: WI-716 WI-717 WI-718; bbe00d8a: WI-720; e86cae4f: WI-725; 3b872471: WI-723; d05b4b05: WI-721; 6f6613e2: WI-724 WI-726 WI-728; 17c54c2f: WI-729; b689eada: WI-727; e40ae0ae: WI-730 WI-731; 03debc71: WI-732; 5c71129f: WI-735; 7a6536f9: WI-733 WI-734; 5b75c39a: WI-736; 205d02cf: WI-738; 5dfd78c1: WI-545; d46c5278: WI-737; 4cbb73cf: WI-739; 3ecef627: WI-740; 896e88b4: WI-743; a4919610: WI-741 WI-742; dcef1f16: WI-744; 2a902b50: WI-745; 6a40d7b2: WI-722; 579cd187: WI-713; 9dbb5103: WI-746; 83db9d75: WI-749; b4b0ea39: WI-751; 85016f90: WI-752; bd9c2d54: WI-750; 183ff1c2: WI-753; ba0ea431: WI-748; d9424572: WI-755 WI-756; 7be21bc3: WI-754; 3a4afaf4: WI-757; 4873bef1: WI-759; dc80849f: WI-761; 87736778: WI-760; c58af7a6: WI-657; 1d688694: WI-762 WI-763; 5c74722c: WI-758; db0bc37f: WI-764; 46ececa8: WI-765; 1f1dc64e: WI-747; 4ba58905: WI-667; e4a44886: WI-766 WI-767; 1ffd8c5b: WI-770; f7d5a12a: WI-768 WI-769 WI-772 WI-773; ba68016b: WI-774; f0050d4c: WI-697; dfcb7a81: WI-775 WI-776; 758519de: WI-778; ed92c3fb: WI-779 WI-780; 25f7f0ad: WI-771; 5afc9270: WI-781; be6500f5: WI-784; 1fda46ed: WI-782 WI-783; 2e46707c: WI-785; c76acd99: WI-777; 863ee89b: WI-786; e78204b4: WI-541; 439a2bb0: WI-787; 5d0db869: WI-789

</details>

**Recommendation: accept the gap as history, with no backfill.** The four
disclosure fields are the deciding session's own account, and those sessions
are gone. A record written now would present reconstruction as disclosure,
which is fabrication. The landing row's log fragment records the range and the
count, and the gap closes from here because the check sits where every landing
passes.

## 7. Spine authoring and risk 6

**The flow (OI-101 Q1), inside `JUDGE`:**

| | Today (2026-09-01) | Ruled flow |
|---|---|---|
| Drafts spine text | the builder | the **adjudicator** (it holds the chain), or it adopts the builder's text |
| Edits | nobody; a RETURN mints a lane | the **adjudication reviewer**, on the same text |
| Approval act | the adjudicator, trunk-side, in a later sitting | the adjudicator's **final pass**, only if it changes no byte |
| A changed byte | — | back to the reviewer; at most **3 rounds**, then the rows land unsettled and are minted (Q2) |

**Why this is not self-approval.** Every approved byte has been read by a session
that did not write it:
- the builder's bytes, by the adjudicator;
- the adjudicator's, by the reviewer;
- the reviewer's, by the adjudicator's unchanged final pass.

**B10's one exception** to "a review never runs in a session that authored what
it judges" is that non-mutating pass. It is carried, with the same scope, into
`ask`'s routing and session reuse (chapter 2 §3 steps 2 and 3) and into act
admission (§5), so all three admit exactly the flow above and nothing wider.

**What stays with the builder.** Code findings still go back to the builder
(`return`). This changes S11 §4.6 for spine text only. The two bounds stay
separate: 3 inner rounds per sitting, and 3 returns per lane.

**The amendment brief changes.** "A judge never amends the row it judges"
(`prompts/adjudicate-amendment.template.md:96`, and its twin in
`adjudicate-first-approval.template.md:99`) becomes:

> In a sitting you may draft replacement text for a row you would not approve.
> Commit it on its own. It goes to the adjudication reviewer, and you approve
> only on a later pass that changes no byte. Never approve text no other
> session has read.

**Risk 6, on lane and trunk (OI-101 Q2).** A commit that writes under
`docs/archive/last_approved/` must, against its first parent, change no spine
cell except `Status`, and add or remove no row. Text is committed first; the
act (the flips, `snapshot`, the ledger and the views) second.

**Where it is checked.** One function over two trees, at the commit, in three
places:
- an ERROR step in the pre-commit hook;
- each lane commit at the landing, as `_loop_trailer_refusal` already does
  (`integrate.py:1289`), so a `--no-verify` commit is still caught;
- each commit the landing itself writes to trunk, against its trunk parent.

**The collision on trunk (owner question, not settled here).** OI-101 Q2 says no
commit changes spine text together with a snapshot update, on lane *and* trunk.
OI-103 Q4 says one squash commit per item. A lane that amended spine text and
then took the act has both changes in its range, so its one squash would carry
both against its trunk parent. The two rulings cannot both hold for that lane.
README Q-8 puts the options:
- **(a) Two commits in one landing** (amends Q4 for act-taking lanes only). The
  landing writes the text commit (the lane's tree at the parent of its first act
  commit), then the act commit (the final attested tree), and advances trunk
  once, by one compare-and-swap, to the second. Trunk's ref never points at the
  first. Each is checked against its parent like any commit. The landing refuses
  a lane whose range changes spine text after its first act (the sitting must
  drop and retake that act, the existing back edge). Recommended: the coupling
  rule then holds at every commit that changes trunk, which is the owner's
  standing rule, and the lane still lands as one operation.
- **(b) The squash as a replay** (amends Q2 on trunk). The landing writes one
  commit; risk 6 is checked on each archived lane commit instead. The check no
  longer runs at the commit that makes the trunk change.

**What retires:**
- the executable allowance, `baseline_snapshot.py:851-853` (documented at
  `:833-836`), which becomes unreachable;
- the refusal's "amend-plus-flip is approval" (`:1039`);
- `staged_spine_findings`' "re-attest it in this commit"
  (`acceptance_record.py:1097-1120`);
- PROCESS.md:488, "Amend and re-copy in the same commit".

**What stays:** flips and their copy in one commit, because that is the act
(SR-140).

**Consequences:**
- The owner's held-rung approvals become two commits.
- An act-taking lane's landing shape waits on README Q-8 (above).

## 8. Rulings this changes (LS8, owner-confirmed)

**R1 and the act refusal.** R1 ("a work branch never mints a work-item id",
`_minted_id_refusal`, `integrate.py:1033`) and the approval-act refusal
(`_approval_act_refusal`, `:1154`) both become: **only a lane in
`ADJUDICATION`, under the authority, mints or takes an act.**
- **The mint rung** admits an added id only if both hold:
  - the id is above the watermark at the lane's `REFRESH`;
  - `[consumption]` names it.
- **The act rung** is §5.

**S11 §4.1's freshness rung** is replaced by the authority. It was never built.

**The 2026-09-01 ruling's "serial trunk side"** stays serial, through the
authority. PROCESS.md:447-451 and the PROCESS_OPTIONS.md table (`:455-470`)
are amended.

**Intake's post-merge arms** all move before the merge:

| Arm (`intake.py`) | New home | Session |
|---|---|---|
| amendment `:791` | `JUDGE`; unsettled rows go to `MINT` | yes |
| first-approval `:895` | `JUDGE`; held rows still never minted (`:834-856`) | yes |
| dispose `:1033`, and its spot-check sample | `JUDGE` → `MINT` successor | yes |
| successors `:1570` | `MINT`: the drafts sit in the sitting record | same session |
| Done-when changed `:1165` | `JUDGE` | yes |
| re-judge at merge | `MINT`, mechanical, at the final tree | no |

None stays after the merge: the landing commit carries every mint, and
`intake_after_merge`'s trunk commit retires.

**The S11 re-mint trap ends structurally.** `MINT` reads an amendment as
unsettled when an in-range row's text differs from its record copy at the final
tree. A row re-attested in the lane has no drift, so it cannot be minted. S11
§4.2's filter becomes unnecessary, and the "close as already settled" rows
(WI-785, WI-786, WI-789) cannot recur.

**Further S11 changes:**
- §4.7's ADJUDICATE-range rule widens to `MINT` writes and resolutions, and
  an `author` range (chapter 2's kind) may edit in-scope spine cells only;
- an adjudication-reviewer range may edit only in-scope cells, plus its
  verdict;
- "an adjudication runs alone" (`dispatch._branch_exclusive`; LLR-149,
  LLR-152) is replaced by the authority.

## 9. LS9, as the owner refined it

**The rework brief.** `agent_brief.py:312`'s "REWORK FINDING (address this before
anything else)" becomes:

> REVIEW FINDINGS TO ANSWER. Each is a claim, not an order. For each one,
> confirm or refute it with evidence you produced (a run, a test, the code
> path). Then do exactly one:
> - FIX it, when it is confirmed and neither a user setting nor a simple retry
>   of an OS operation would mitigate it.
> - DISPUTE it, recording the finding id, your evidence and its class in the
>   dispute record, when your evidence refutes it; or when its cause is the
>   environment (a file lock, a virus scanner, a sandbox) and a setting or a
>   retry mitigates it; or when it asks for a guard on an input the design
>   already constructs as valid.
>
> The adjudicator resolves disputes, and its call is final. Identify every
> failure, but change code only when the work-around pays for its complexity
> against the failure's likelihood. Never leave a finding unanswered.

**The reviewer brief's reciprocal**, added at `prompts/reviewer.template.md:39`:

> A finding whose cause is the environment, and which a user setting or a
> simple retry of an OS operation mitigates, is ADVICE, not a defect. Write it
> as `[ADVICE]` with the cause and the recommended setting, and leave it out of
> `findings=N`. Do not ask for a guard on an input the design constructs as
> valid.

`kitlib/verdict.py` learns the `[ADVICE]` severity.

**`AGENTS.template.md`'s retry rule** (`:172-176`): "never retry past a failure
whose cause you haven't found" becomes:

> Identify every failure's cause. Retry a known transient class a bounded
> number of times: a file read, write or delete refused by a lock or a
> scanner, or a network timeout. Never retry an unexplained failure; find its
> cause first. Surface an environment cause with its fix; do not tool around
> it.

The change adds about 150 bytes, which the byte-budget guard checks in that
row.

**Where an environment failure surfaces.**
- **By default: a "Decisions to review" entry.** The builder records the call
  in the lane's decisions record, for example "did not tool around the scanner
  lock; recommend excluding `tests/`".
- **Only when work is blocked until the owner acts: an open item** with a
  placeholder row. `MINT` routes it, because a builder never mints.

## 10. Matrix rows

| item | kind | fate | why | successor |
|---|---|---|---|---|
| LLR-140, IF-080, IF-154, IF-173 | row/contract | amend | squash, one landing, claim lane-side, no `integrate.lock` (SR-156 preserved: README matrix) | S788-landing |
| SR-170, LLR-151 | row | amend | the authority replaces the "serial merge step" and the dispatch-lock claim | S788-station-authority |
| SR-174, SR-140, SR-179, SR-207, SR-144, SR-208, SR-209, IF-101, IF-220 | row/contract | preserve | one allocator; flip and copy one act; mirror, report, held status and provenance unchanged | — |
| SR-178, LLR-158, LLR-278, TC-153, TC-278, IF-091 | row/contract | amend | the act's scope comes from the lane's scope record (B6) | S788-sitting |
| LLR-149, LLR-152, TC-143, TC-146 | row | amend | exclusive adjudication is replaced by the authority | S788-sitting |
| LLR-161, LLR-144, LLR-262, TC-257 | row | amend | disposition in the lane; quarantine as `merge-partial`; the range rules | S788-sitting |
| SR-215, SR-220, LLR-153, LLR-154, LLR-255, LLR-264, TC-147, TC-148, TC-248, TC-260, IF-090, IF-229, IF-243 | row/contract | amend | the mint runs in the lane; CLI and idle mints go through a station lane | S788-mint |
| LLR-265, TC-261, IF-244 | row/contract | retire | `sweep`: no landing happens outside the one operation | S788-mint |
| SR-225, LLR-284, TC-294 | row | amend | one record check at every landing | S788-landing |
| LLR-173, LLR-245, LLR-178, TC-167, TC-173 | row | amend | text before act; amend-plus-flip retired | S788-text-then-act |
| SR-154 (shared with ch.2) | row | amend | the resolution is final; the final-review family excludes every author | S788-resolve-ls9 |
| SR-027, LLR-029, LLR-030 | row | amend | no unguarded lock | S788-retire-runtime-dual-paths |
| IF-186 | contract | amend | bookkeeping becomes the landing's install | S788-landing |
| IF-247, IF-248, IF-255, IF-256 | contract | ch.2 / WI-790 | lease order rule stated here | — |
| New rows: the authority; text/snapshot separation; consumption completeness; dispute resolution | row | add | B4, risk 6, LS6, LS5 | per row in §11 |
| `integrate`, `intake`, `acceptance_record`, `baseline_snapshot`, `bookkeeping`, `dispatch`, `handback`, `consolidate`, `session_service`, `agent_common`, `agent_brief`, `kitlib/verdict`, `kitlib/decisions`, `hooks/pre-commit` | module | amend | §2 to §9 | as above |
| `adjudicate-first-approval`, `-amendment`, `-disposition`, `-consolidate` (folds into MINT) | prompt | amend | §4, §7 | S788-sitting, S788-mint, S788-spine-authoring |
| `reviewer.template.md`; `worker.template.md:68-71` | prompt | amend | LS9; the act moves into the sitting | S788-resolve-ls9, S788-sitting |
| PROCESS.md:447-451, :486-489; PROCESS_OPTIONS.md:435-513; AGENTS.template.md:172-176; concurrency-v2 §A2.0, §A5.2; runtime-flows.md; registry-machinery-reference.md | doc | amend | §7 to §9 | as above |
| S11 plan §4.1, §4.2, §4.6, §7 | doc | superseded in part | §8 | — |
| SR-173, LLR-220 | row | preserve | regeneration stays ordered and all-or-nothing, now at the final evidence; assumptions and surrogates stay inside the act | — |
| LLR-137 | row | amend | `trunk_step` runs lane-side under the authority (and appends the ledger: chapter 2) | S788-station-authority, S788-session-store |
| LLR-246 | row | amend | its writers move (`_claim_locked` lane-side, `commit_telemetry` to the spool, `_mint` into the lane); the held-status refusal applies at each new writer and at every lane commit at the landing | S788-station-authority, S788-session-store, S788-mint |
| TC-218 | row | amend | a lane flip is refused unless it lies in an eligible ADJUDICATE range (§5), not refused at the slot by name | S788-sitting |
| IF-123 | contract | amend | intake reads drift at the final tree, in `MINT` | S788-mint |
| IF-129 | contract | amend | `staged_spine_findings` loses "re-attest it in this commit" | S788-text-then-act |
| IF-228 | contract | amend | `checkpoint_drafts` is read at `MINT`, in the lane | S788-mint |

## 11. Proposed successor rows

Each row's test bar is the commit bar plus the modules named. Each row's review
bar is the README graph's "Review" column. Each row is landable on its own: its
Done-when tests only what it and its `needs` provide.

**S788-text-then-act:** risk 6 on lane and trunk.
- **Scope:**
  - the one separation function, at the hook and per lane commit;
  - the §7 retirements.
- **Done-when:**
  - a mixed commit is refused at pre-commit;
  - a `--no-verify` lane commit is refused at the landing;
  - the two-commit form is accepted;
  - no refusal text offers amend-plus-flip.
- **needs:** none.
- **BuildTier:** medium. **Modules:** snapshot and acceptance. **RESYNC:** yes.

**S788-station-authority:** the lease and the trunk-writer moves.
- **Scope:**
  - the record, the mutation lock, fencing, expiry and the `lane_state.py release` CLI;
  - the claim moved lane-side;
  - today's landing (`integrate_one`) taking the authority; `integrate.lock` retired;
  - cancellation (§2);
  - the hook check.
- **Done-when:**
  - one acquirer wins and the other is refused, with the holder named;
  - an expired or cancelled holder cannot advance a ref (the check and the
    `update-ref` swap are one critical section);
  - an unlockable filesystem refuses;
  - a claim is refused while a landing holds the authority, and succeeds after;
  - nothing that holds the authority waits: a test holds a lease elsewhere and
    sees the holder take a fresh session at once;
  - a cancelled sitting is stopped, its usage harvested, and the lane derives
    `PARKED`; its relaunch gets the reconcile note.
  (The census that no tool writer remains outside the landing belongs to the
  last writer move, S788-dual-pickup.)
- **needs:** S788-lane-state-provider, S788-session-store.
- **BuildTier:** strong. **Modules:** integrate, dispatch, session. **RESYNC:**
  yes.

**S788-landing:** the one landing.
- **Scope:**
  - one landing per lane by compare-and-swap, its shape per README Q-8 and Q-11,
    and `archive/lanes`;
  - `Lane-Tip:` and the audit;
  - one record check, with the hand path on it;
  - **F1:** the refresh aborts its own interrupted merge (a `MERGE_HEAD` that is
    a trunk commit, with no other change); any other dirt still refuses;
  - **F2:** `ARCHIVE` is ordered (`archive/lanes` first, then the branch, then
    the worktree) and re-derived every tick, so an incomplete unload is re-run
    until the lane is closed;
  - the gap's log fragment.
- **Done-when:**
  - both paths yield one landing per lane whose final tree equals the attested
    tree, and a single-item lane yields one commit per item (two under Q-8 (a)
    when it took an act);
  - a trunk moved under the lane fails the swap, naming the foreign commit;
  - the tip is reachable from `archive/lanes`;
  - a refresh killed after `merge --no-commit` is recovered by the next one;
  - an unload killed after `archive/lanes` and before `worktree remove` is
    finished by the next tick;
  - a close that owes a record and has none is refused on either path.
- **needs:** S788-station-authority, S788-ask.
- **BuildTier:** strong. **Modules:** integrate, handback. **RESYNC:** yes.

**S788-sitting:** `LOCK`, `REFRESH`, `JUDGE`, `MERGE_ACTION` and the final
evidence.
- **Scope:**
  - the scope record and B6;
  - acts taken in the lane;
  - the range rules;
  - the back edge;
  - the briefs.
- **Done-when:**
  - a build lane's Drafted rows are approved in the lane;
  - an out-of-scope act, an act outside an ADJUDICATE range, or an act by a
    session that chapter 2's judged-scope table makes ineligible is refused;
  - a rejected final review drops the act;
  - a landing whose swap fails on a foreign trunk commit re-enters `REFRESH`
    under the same authority, and a stale act is retaken by a session;
  - a fourth `return` is refused, and the sitting's outcome is `merge-partial`
    (green: the work lands; red: an empty keep set), with no red tree landed.
- **needs:** S788-landing, S788-text-then-act, S788-session-families, WI-791.
- **BuildTier:** strong. **Modules:** acceptance, integrate, agent_loop.
  **RESYNC:** yes.

**S788-mint:** `MINT`.
- **Scope:**
  - the in-lane allocator and the consumption list;
  - consolidation folded in;
  - the moved arms;
  - the station lane;
  - `sweep` retired.
- **Done-when:**
  - an undisposed item refuses;
  - `open-item` yields a blocked placeholder row;
  - a settled amendment is never minted;
  - a merge re-judge is minted in the lane;
  - an exhausted lane's upheld findings become its successor's Done-when;
  - a coordinator's filing lands through a station lane;
  - sequential sittings never collide on an id.
- **needs:** S788-sitting, WI-790.
- **BuildTier:** strong. **Modules:** intake, consolidate. **RESYNC:** yes.

**S788-resolve-ls9:** `RESOLVE` and LS9.
- **Scope:**
  - the dispute record;
  - the verdict gate reading resolutions;
  - the three wordings and `[ADVICE]`.
- **Done-when:**
  - a fully dismissed CHANGES-REQUESTED lands with no re-review;
  - an `uphold` returns the lane;
  - `[ADVICE]` is not counted;
  - the byte budget holds.
- **needs:** S788-sitting.
- **BuildTier:** medium. **Modules:** verdict, brief. **RESYNC:** yes.

**S788-spine-authoring:** the OI-101 Q1 flow.
- **Scope:**
  - the draft, the edit and the non-mutating final pass;
  - the 3-round bound;
  - the B10 exception;
  - the amendment brief.
- **Done-when:**
  - a final pass that changes any byte cannot act;
  - with the two-family pool, every kind in the flow has an eligible draw
    (chapter 2 §3 step 2), and the act admits exactly B10's exception;
  - a fourth round is refused, and its rows are minted unsettled.
- **needs:** S788-sitting, S788-session-families, S788-mint.
- **BuildTier:** strong. **Modules:** prompts and range rules. **RESYNC:** yes.

## 12. Questions for the owner

Consolidated in the [README](README.md#questions-for-the-owner-at-the-checkpoint):
Q-4.1 is Q-7 and Q-4.2 is Q-8.

**Q-4.1. Idle and CLI mints have no lane.** These are the gap census, the
consolidation census and the release re-judge. Options:
- (a) A station lane mints its own carrier row first, then lands like any
  lane. Every landing is then a work item's.
- (b) A station lane with no row.
- (c) Drop idle mints. An empty frontier could then never file gap rows.

**Recommend (a):** it keeps your words, "through a WI", literally.

**Q-4.2. OI-101 Q2 and OI-103 Q4 collide for a lane that took an act.** The
options and what each amends are in §7 ("The collision on trunk"): (a) two
commits in one landing, amending Q4 for such lanes; (b) the squash as a replay,
amending Q2 on trunk. **Recommend (a).** Neither is settled until the owner
rules.

## 13. Research record

**Read:**
- the spec in full; the S11 plan; the Sol review; WI-790; chapter 1 (draft);
- the OI-101 and OI-103 rows and their log records;
- `integrate.py:1-140, 598-896, 1033-1315, 2592-3076`;
- `intake.py:60-130, 680-700, 1033-1280, 1570-1590, 2266-2630, 2982-3255`;
- `acceptance_record.py:740-970, 1020-1130, 1259-1330`;
- `baseline_snapshot.py:1-30, 820-880, 990-1060`;
- `bookkeeping.py:1-130`;
- `agent_common.py:880-1010, 1651-1760`;
- `session_keep.py` (its header, and `:464-600`);
- `session_service.py:540-600`;
- `plan_artifacts.py:290-371`;
- `consolidate.py:1-120`;
- `handback.py:1-130`;
- `kitlib/decisions.py`;
- `agent_brief.py:290-335`;
- `agent_policy.py:940-985`;
- the amendment, disposition, first-approval and consolidate prompts, and
  `reviewer.template.md`;
- `AGENTS.template.md:155-185`;
- `PROCESS.md:438-495`;
- `PROCESS_OPTIONS.md:455-515`;
- concurrency-v2 §A5.2 and §B3;
- commit `d4b36d71`.

**Probes:**
- **The gap.** For each first-parent commit in `655c60ab^..c3be7be0`, I read
  `git diff --name-status --no-renames c^1 c`: terminal-folder adds, and
  `docs/decisions` touched. Exit 0: 77 closing commits, 2 with records.
- **No loop merges.** `git log --first-parent 655c60ab..c3be7be0 | grep -c
  "integrate: merge"` returned 0.
- **The dial.** `docs/process.toml:192` reads `decision_recording = "record"`,
  set in `655c60ab` (`git log -S`).
- **Session walls.** The `# wall-secs:` header of `docs/iteration/*.log`,
  ERROR outcomes excluded:
  - ADJUDICATE: n=33, median 332 s, p90 933 s;
  - REVIEW: n=146, median 451 s, p90 1032 s.
- **Create-only ref.** In a scratch repo, `git update-ref refs/claims/WI-1
  <sha> ""` exited 0 the first time and 128 the second ("reference already
  exists"), on git 2.49.0.windows.1.

**UNVERIFIED:**
- that `rejudge.checkpoint_drafts` at the lane's final tree equals the
  post-merge reading (the build tests it);
- the loaded-box bar times (CLAUDE.md's 3-4x);
- chapter 2 and chapter 3 row ids (the integrator names them);
- whether any adopter relies on `out/integrate.lock`'s path.

**Calls no spec or ruling settles:**

| Decided | Alternative | Reversal cost | Why not escalated |
|---|---|---|---|
| The REFRESH in the lock runs the commit-tier bar; the full bar runs once, at the end | the full bar at both | low | B5 and "no stale tests" both hold, at half the hold |
| The authority is a lease with fencing | a long-held flock | medium | the hand path has no long-lived process |
| Nothing waits under the authority: leases first (waiting holding nothing), then one non-blocking try of the authority | wait for the lease inside the authority | low | OI-103 Q2's reading, "a sitting never waits while holding the lock" |
| The TTL is 120 min, as a dial | 30 min, or none | low | it covers the p90 loaded sitting |
| `integrate.lock` folds into the authority | keep both | low | that would be risk 7's dual path |
| Lane-side claims still take the authority | claims run free | low | Q1 (a) names claims |
| Spine rounds stay in the sitting; code fixes `return` | every finding goes to the builder | medium | OI-101 Q1 gives the text to the adjudicator |
| The gap is accepted as history | backfill | none | backfill would fabricate disclosures |
| ~~Coordinator hand commits take only the hook check~~ Withdrawn in the fix round: a coordinator is an agent, so its trunk writes go through a station lane; only the owner's commits are outside the tool, and the pause file is README Q-12 | — | — | OI-103 Q1's owner words |
