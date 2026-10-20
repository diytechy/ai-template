<!--
Contracts: IF-163 — the interface seam this file declares (process.md §8; row of
record in requirements/interfaces.toml).

Contract IF-163: the forward-only blackboard's HAND-AUTHORED bytes — everything
    outside the GENERATED STATUS marker pair — read as data by the kit's checks
    and by a resuming session; the block between the markers is its writer's
    own row. Markdown with `##` sections: `## Current State` is the section a
    stopping coordinator excerpts into its exit banner (the generated block
    rides inside that excerpt as the writer's bytes). Only what must happen
    NEXT belongs here — what already happened lives in log.md — so a work-item
    id recorded closed must not appear in the hand-authored prose, and a claim
    naming one there is refused; inside the generated block that rule stands
    down, because the generated frontier legitimately names queued ids.
-->

# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself. **Forward-only**, held to
the declared S-1 budget (`docs/status-lint`; raised 2026-08-31 to carry the
supervisor prompt at the owner's request). Backward-looking homes:
[log.md](log.md) (sessions, verdicts, **Decisions**), [open-items.html](open-items.html)
(the generated **Open items** owner surface), [docs/work/](work/) (the WI registry —
status = directory; terminal rows under [archive/work/](archive/work/)),
[archive/](archive/README.md), and the folder map [docs/README.md](README.md).

- **RESUME HERE:** start with the coordinator's
  [handoff-2026-10-20b-leg04-coordinator.md](handoff-2026-10-20b-leg04-coordinator.md),
  run in **headless legs** under the overnight launcher (the handoff
  carries no stop line). The owner ruled the review-churn program
  ([plans/2026-10-11-review-churn/](plans/2026-10-11-review-churn/README.md):
  every call is ruled; read its Status, then its rulings). The batch's
  process-text, strict-lints and plan-gate landing-shapes rows have
  landed, and the reviewer trial has ended: each round runs two reviewers,
  Sol and Opus. The adjudication split has landed: a checkpoint sitting
  now ends at its committed verdict, and its act is a later turn
  (`coordinator_adjudicate.py act`), and the machine-line reader row has
  landed through it. A landing's bar
  runs on the box as it is, read beside its parent's (owner, 2026-10-17);
  a CPU-time smoke budget is queued after the batch (owner, 2026-10-17).
  The re-sync entry check is in the commit bar: a lane rebased onto a
  newer trunk re-anchors its own RESYNC entry at its new base.
  The headless coordinator's marking row has landed, and the guard-hooks
  row has landed, and so have the bless-mark row, the re-claim reader
  row, the launcher's follow-ups row, the trunk-by-name row (the trunk
  is now the branch `docs/process.toml` declares) and the hooks-on row
  (every agent route refuses a checkout whose commit hooks are not on),
  and the guard hook's per-call cost row (its PreToolUse group runs only
  for the launch and shell tools). The two merge-slot rows are claimed; their
  coordinator-landing gap is the one-landing row's
  (owner, 2026-10-17). The
  disposition-adoption row was re-cut and closed partial at its rebuild's
  plan cap: the cap's sitting ruled a FIX, which is the owner's to route,
  and its minted disposition row waits on that choice. The
  account-homes row has landed: the adjudicator runs on its declared
  token account through a qualified entry.
  The coordinator's procedure lives in the `coordinator-cycle` skill, its
  headless legs in its section 7. The owner directed (2026-10-18,
  coordinator-2026-10-18 D-004, D-006) that the queue turn toward headless
  runs: its two gate rows, the re-claim reader row and the launcher's
  follow-ups row, have landed, so the handoff carries no stop line, the owner
  starts the overnight launcher (`scripts/coordinator/overnight_legs.py`),
  and the rest of the queue runs in headless legs, continuing the lanes
  claimed attended with no re-claim.
  Delegated decisions take the owner's verdict as `owner = "confirmed"` or
  `"overruled"`; entries not yet seen, high-risk first, render under "Decisions
  to review" in [open-items.html](open-items.html), and an overrule must change
  open work citing it in the same commit.
  Approval acts run to seq 142 on trunk. The context guard's hooks are machine-local
  (installed through dev-setup's consented offer, or at a lease take run at a terminal; this
  workstation is on), and the guard is live where they are: take the coordinator
  lease (`coordinator_guard.py take`) before any claim, and hand it back
  (`coordinator_guard.py handback --handoff <path>`) as the close-out's last act.
  Every adjudication sitting now authenticates with the owner's long-lived token:
  set `AGENT_CLAUDE_TOKEN_FILE` to its path before `coordinator_adjudicate.py`.
  0. **The handoff's queue table in order:** the program's first batch,
     then the lane in flight (claimed, on its branch; the handoff names its
     returns), then the phase-1 rows.
     Review rule (owner, 2026-10-11, superseding 2026-10-07): no narrow rounds.
     Each round runs two full-lane reviewers in parallel (Codex Sol and
     Claude Opus; the three-reviewer trial ended 2026-10-16), at most three rounds, with a dispute sitting at the cap; the
     handoff states the rest. Review threat model (owner,
     2026-10-08, PROCESS.md §6): a finding that needs a compromised or
     contrived host is dismissed in one recorded line; a contested or
     third-round finding goes to the coordinator's `dispute` sitting
     (`coordinator_adjudicate.py adjudicate --brief dispute`), whose ruling is
     final.
  1. **Build the S788-* successor rows** of the approved design note
     ([plans/2026-10-04-wi788-design/README.md](plans/2026-10-04-wi788-design/README.md),
     its ruling section first; it overrides the chapters), in their `needs`
     order with the wave-11 cycle, claiming each batch under one scoped unpause.
     The generated ready frontier below lists the rows that can start; the
     handoff names them. The owner directed (2026-10-04) that this campaign
     runs by coordinator session, not the unattended loop. OI-105 (the
     FreeLLMAPI endpoint and pinned models) waits for the owner's router; it
     holds only the FreeLLMAPI row of S788-routes.
  2. OI-98: the owner re-syncs `C:\Projects\FileBackup` (stamp `9b697cc`) as a
     scratch trial, after TC-036's inputs gain `RESYNC_PACK.md`, then rules it.

  `docs/work/pause` is still tracked (since 2026-09-04): the unattended
  dispatcher claims nothing until a reviewed commit deletes it, so work is
  taken by a coordinator session, not the loop. Owner direction 2026-10-04: a coordinator
  session claims its whole batch of rows under ONE scoped unpause (a reviewed
  deletion commit, the claims, then a byte-identical restore), not one per row;
  the control ruling's pause deletion is not spent. The roles (owner, 2026-10-04): Claude Opus builds and plans at medium
  effort and the coordinator commits for it; GPT Terra (`gpt-5.6-terra`,
  medium) authors spine rows; Codex 6.1 (`gpt-6.1-sol`, high) reviews code
  through the CLI; and an independent Opus agent adjudicates and resolves
  disputes. File new work as a row; an open item is filed together with the queued
  placeholder row whose `needs` cites it, and the commit that rules it updates
  that row's Done-when (OI-102). The reviewers' `codex exec` launch
  runs under a temporary `Bash(codex exec *)` allow rule in
  `.claude/settings.local.json` (owner, 2026-09-28): remove it when the
  queue drains. Recheck Git and the generated frontier before choosing
  work; earlier handoffs are historical context.
- **Assumption tier — C1 and C2 have landed and are approved:** the
  redrawn frame, checkpoint re-judging of observation tests, the assumption
  gate's four steps (behind `[checks] assumption_gate = false`), and C2's
  assumption and surrogate rows with every SR's bridging. The owner signed
  the assumption ruling on 2026-10-02: an assumption carries status and standing
  only, falsification is the one signal, and there is no evidence ladder, so
  C3 shrinks to the falsification route and C5 loses its evidence arm. OI-97's joint-delivery class has
  landed and is anchored.
- **Sister plan — one plan still owed:** every question in the
  [notes on spine, sessions and tests](plans/2026-09-23-owner-notes-spine-sessions-and-tests.md)
  §5 is ruled except S11. The owner said yes to adjudication inside the lane
  (2026-10-03): a return is fixed in the lane, not minted as a follow-up row.
  Its plan, with S9's reviewer-commit check, is
  [plans/2026-10-03-s11-in-lane-adjudication.md](plans/2026-10-03-s11-in-lane-adjudication.md).
  Its §6 questions are ruled as recommended (owner, 2026-10-03, recorded with
  OI-101 Q6). Hand integration already follows it (owner direction 2026-09-28): one
  squash commit per item, with lane tips kept reachable in `archive/lanes`. S7's session service has landed, writing S8's adopted OTel schema, with
  retention shipped off; its live verification closed 2026-10-03 (a real adjudication peaked at 44% of the codex window), and the dial stays off. S6 is designed
  with the assumption tier before its C3. S14's flag-axis count and
  duplicate-detection research have both landed.
- **Control launch:** retain the tracked `docs/work/pause` while preparing
  route-complete spending bounds, including in-flight drain, against the
  [settled control ruling](ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md#owner-ruling-2026-09-06).
  Revalidate the [preflight](ai-template-redesign-2026-09-05-codex/CONTROL-PREFLIGHT.md)
  at the proposed frozen launch commit, then obtain the ruling's owner-reviewed
  pause deletion. Replacement packages follow the control's evidence decision.
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). The held wi508
  branch is on origin; the queued wi508-partial-close row is the only
  sanctioned act on it (`OI-71`).
- **Standing constraints:** the depth-0 frame is **LOCKED and APPROVED** (4
  entities · 4 crossings · 3 relationships, watermark-held); `OI-61` (c) stays deferred
  on its condition (a demonstrated residual drift class), not owner-owed.
- **Unfiled follow-ups** (topics, no ids): the wave-11 log's follow-ups (the claim
  reads the working-tree pause; an in-lane act never meets the held-rung
  re-attestation refusal; a refresh merge must carry a citer's update for a
  trunk ruling); the wave-9 log's session-close list (removed approved rows mint no adjudication; six batch-R row-text residues); the stage-ladder program's deferred
  codex round; the SN-036 coverage record (re-derive — basis reads
  `uncovered=0`); the archived [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md)
  findings; the [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md)
  residues (§7 items 2/4/5 need a destination); whether the `ruling-sync`
  and `held-status` hook riders share the hand-merge shapes the plan gate's
  contract now states as residue (text-then-act's is accepted by its
  approved requirement; owner, 2026-10-15); from the process-text row's
  last gate (wi-911 D-020): PROCESS.md §3 still places a concrete filename
  in an SR's acceptance as carrier evidence, against ruling 5's text in
  `spine-questions.md` (to plan item 5's schema lane), and SR-233's
  acceptance states convergence duties its requirement does not (wording,
  at its next sitting); from the landing-shapes row's first round (wi-922
  D-005): LLR-337's rationale reads wider than the residue the plan gate's
  contract states (wording, at its next sitting); from the bar row's gate
  (wi-935 D-005): CLAUDE.md, the session-protocol skill and the budget
  script's docstring date OI-52 ruling (a) 2026-08-23, its wiring date,
  where the record reads 2026-08-21 (wording, in all three together);
  from the session-kill row's gate (wi-931 D-009): SR-238's acceptance
  clause on a process that joins the session job late in the kill has no
  verifying TC clause (wording, at its next sitting: keep it in the
  rationale's residue, or name its verification in TC-026); from the
  adjudication split's lane (wi-912 D-013): the intake module's minted
  first-approval and amendment rows'
  Context still tells the judging session to act in-turn (to the row that
  builds the loop route's act turn); the judging composer's first-approval
  comments still describe the removed `--approves` slot; LLR-167's detail
  still says its tiers come from that walk, and an "it" in its addition
  lacks a referent, and SR-231's new act-turn sentences sit outside its one
  `shall` (wording, at their next sitting); from the merge-slot rows'
  drafting (their specs' S5 and Trust): the held-rung act rule has two
  homes, three readers map a row id to its registry over two tier sets,
  and an act ledger deleted alone is admitted on a scope-bound lane, which
  no kit route reaches; from the re-sync
  check's gate (wi-916 D-008): the enforcement audit's row and the
  check's docstrings say a retitled entry counts zero, where one keeping
  its old anchor is refused by the anchor rule, and a lost landed heading
  that cancels a valid added entry is refused with the plain no-entry
  reason, naming neither (wording, and a clearer message); from the guard-hooks row's
  fix round (wi-927 D-007): a shipped coordinator-hook example holding JSON
  null reads none, which its Trust section does not rule; from the same
  lane's POSIX run: two `run.command` cases in the dev-setup tests fail on
  POSIX at trunk itself (a bare run's check order and interpreter); from
  the guard-hooks row's gate (wi-927 D-012): a take run from a lane
  worktree reads the hooks under that worktree, not the primary checkout's
  where the lease lives, so it refuses naming the lane's file; TC-345's
  `verifies` cites SR-237, which none of its cases exercises; LLR-322's and
  TC-345's "all missing guard events" understates the absent reading, which
  also covers events present and empty (wording); and the take's hooks
  refusal is stated in both LLR-300 and LLR-322 (cross-refer at the next
  amendment of either); from
  the trunk-by-name row's build: a spec move rewrites the moved spec's own relative links, so a
  row whose Done-when holds one reads as changed at its own close; and the
  dispatcher may keep looping on a worker that refuses at preflight;
  from the guard-hooks row's second fix (wi-927 D-009): bootstrap's setup
  prompt reads a NUL stdin as a terminal on Windows (harmless: it takes the
  default); nothing checks an LLR's code_symbol entries back against the
  tags, and trace.py does not compare a TC's `verifies` with an LLR's
  `test_refs` (so `--strict` missed a back-link gap); the occupied fix text
  also prints for an unparseable settings file or a broken shipped example;
  a crashed hooks reader's `[missing]` line carries only its traceback;
  from the trunk-by-name row's gate (wi-925 D-011): TC-369's expected joins
  an existing policy file's preservation to the no-repository and detached
  defaults, where the scaffold leaves an existing file's trunk alone and
  prints no note, and TC-206's method still explains its single-checkout
  fixtures as their own trunk (wording, at each row's next sitting);
  LLR-307's bound and the shipped hook's heading call all seven fail-open
  items routes outside the supported ones, where three are shapes inside
  them (wording, in both homes together); from its fix round (wi-925
  D-008): with the trunk undeclared, the readability report skips a
  measure the profile declares gating (LLR-256's exit contract), and the
  plan record repeats a schema comment's corrected reason;
  from the hooks-on row's gate (wi-926 D-014): IF-194's notes and IF-197's
  rationale still say the commit-msg hook reads the loop marker to fail
  closed, where it now reads none and refuses every commit without the kit
  scripts (wording, at each row's next touch); the row's archived
  Done-when says a missing or non-executable hook's refusal names the setup
  command, where the code and the approved SR-240, LLR-340 and TC-370 name
  the repair for that cause; TC-370's evidence omits four existing check
  cases (the `.git/hooks` path, an empty hooks path, a directory that is
  not a work tree, a linked worktree on the main worktree's absolute
  `.githooks`; traced-only, at its next touch); and LLR-140's and
  LLR-300's test_refs do not list TC-370, which now verifies both;
  from the bless-mark row's gate (wi-943 D-007): the act module's
  docstring still calls the merge slot's checks unchanged, where they now
  read the same judged-rows reader (wording); TC-278's method claims the
  two-way-tagged refusal through a named verdict as well as through the
  backing check, and its evidence covers only the backing check (add a
  named-verdict case to the two-ways test, or narrow the sentence);
  from the re-claim reader row's gate (wi-918 D-008): the lane window's
  state advances in log order, not along ancestry, so in a loop lane
  holding a lane-local side line merged back in, an unmarked side commit
  that does not descend from the re-claim is exempted (no kit route
  merges such a line; derive each record's state from its parents');
  SR-209's rationale still says the floor judges every commit of a loop
  lane and gives no reason for the re-claim exception (wording, at its
  next amendment); IF-194's data spells three names in brace notation,
  so a search for them misses the row, and nothing forced it: the
  160-character data rule is a warn-first advisory (spell them out at
  the row's next touch);
  from the launcher's follow-ups row's gate (wi-946 D-012): LLR-246, the
  held-status rung's row, does not state that the rung refuses a lane
  whose claim cannot be read, which it inherits through the slot's
  window read (wording, at its next amendment: add the sentence or
  cross-refer LLR-248); and from its sitting: TC-242's method says "a
  loop lane whose claim record cannot be read", where an unread claim
  cannot show the lane is the loop's (wording, "a lane", at its next
  sitting);
  from the guard hook cost row's gate (wi-897 D-007): IF-261 (the policy
  file's readers) still names only `scripts/agent_common` as requestor,
  while `session_keep` and `coordinator_guard` now read it directly, and
  `agent_policy`'s contract text still says `agent_common` re-exports it
  (add the two requestors at the row's next touch); and the traced-only
  re-anchor recipe names the sitting that last anchored each registry as
  the refresh's ref, where the snapshot README's rule reads as asking for
  the lane's own WI or no entry (wording, in the recipe or the README);
  from the account-homes row's gate (wi-798 D-024): IF-246 and IF-282
  list a `route_runner(entry)` the session service does not define, and
  IF-044 omits the route module's `route_runner(template, model)`; IF-248's
  notes still say the keep module creates account homes; the row's
  Implements tags name SR-222 beside LLR-336, which traces to SR-154 and
  SR-227 only; LLR-305's compose_env sentence reads unconditional, where
  the withholding applies under a declared account; `docs/process.toml`'s
  adjudicator comment says the loop draws the unqualified route, where a
  heterogeneity-filtered draw or a win-stay pin picks the weight-0
  adjudicator entry when the ambient Opus route cools (wording, at each
  row's next touch); and SR-227 still binds its credential clause to a
  family with a dedicated home (the owner's wording, at its next
  amendment);
  **owner intake 2026-09-22:** the self-test
  suite should fail fast when its dev toolchain is missing, and name the run
  menu's setup action as the fix. Today a missing pytest-xdist dies on
  `unrecognized arguments: -n`. This depends on the root launchers SN-034/SN-035
  require, which do not exist yet, and needs stepping through as a requirement
  before it is built.
- **Conventions:** [specs/README.md](specs/README.md) · [rubrics/README.md](rubrics/README.md) · partial closes [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-Impl** (stage 7 of 8, implementation in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-Impl;6=DevStg-Impl`, derived current **phase=6**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=31 SR=132 LLR=307 TC=326** (21 drafts) · 246 seams · 4 components.
- **Open items** _(the pending rows of [requirements/open-items.toml](requirements/open-items.toml) a queued work item cites; each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-98** — The owner must perform the re-sync from 2026-10-03 and rule this item to release WI-684. _(holds WI-684)_
  - **OI-105** — When the owner's FreeLLMAPI router is running, name its endpoint and the models to pin, and confirm it holds a one-model chain per pinned id, so the FreeLLMAPI route row can ship and take its one live call. _(holds WI-795)_
- **Decisions to review:** 668 — [open-items.html](open-items.html#decisions-to-review)
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-920** — re-judge TC-055: declared trigger fired [sha256:5bdf43dafa30] at merge b803dd0
  - **WI-953** — dispose: the close recorded at docs/handbacks/WI-902-wi-902.md
  - **WI-851** `P5` — Held-rung spine rows are protected by state: the registry, the snapshot and the dial
  - **WI-850** `P5` — A spine row is approved only after the rows it hangs from are
  - **WI-940** `P5` — The smoke budget step judges the tier's own CPU-seconds, which other load and process pri…
  - **WI-878** `P4` — A dispute sitting's binding records the findings file it ruled, and the coverage gate rea…
  - **WI-799** `P3` — Lane-state provider that derives each lane's state from evidence, representation only
  - **WI-832** `P3` — A decisions record has an identity no other run can share
  - **WI-856** `P3` — A queue-with-edge verdict edges a waiter filed without a needs line
  - **WI-817** `P3` — Retire the SN-028 one-word config window and the non-TOML carriers
  - **WI-827** `P3` — Owner signs SN-029's amendment after text-before-act
  - **WI-906** `P3` — A coordinator-lease hook that meets store-lock contention never leaves the lease with an…
  - _(+2 more ready — see the dashboard)_
- **Blocked** _(held by a pending open item its `needs` cites):_
  - **WI-684** — re-judge TC-036: no result recorded [sha256:2f2f30dfba87] at merge 77fb093 — [OI-98 — Owner re-sync from 2026-10-03](open-items.html#OI-98)
  - **WI-795** — Owner provisioning: the FreeLLMAPI endpoint and pinned models — [OI-105 — FreeLLMAPI provisioning: the endpoint and the pinned models](open-items.html#OI-105)
<!-- END GENERATED STATUS -->

- **Bar (per commit)** and the **standing rules** (claim refusal on prose ids,
  never sanction a check to green a step, line-ending hygiene, claiming through
  the integrator): the `session-protocol` skill §2–§3. Run
  `check_trajectory.py --strict` unfiltered before claiming anything done;
  route a critique dispatch by PROVIDER, probing first.
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) · working rules
  [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill · lock items
  [repo-lock.md](repo-lock.md) · external (not this repo's work): guardrails
  content in `TheColliny/FableClaudeMDForOpus`.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the `PROJECT-VISION:`
  tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only, Python 3.11+.
- **Non-goals (self-application boundary):** no product **launch** — the kit's
  "product" is `project-trajectory/` + `tests/`; an actions-menu launcher is in
  scope, a `run.*` product launcher is not. No scaffolded `docs/process.md` (the
  masters live in `project-trajectory/`).
